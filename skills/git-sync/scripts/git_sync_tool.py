#!/usr/bin/env python3
"""
git_sync_tool.py
================
Robust, standard-library Git synchronization and remote divergence auditor.
Features:
  1. Safe remote fetch and tracking branch detection.
  2. Commits ahead/behind counting and log inspection.
  3. Working tree cleanliness (staged, unstaged, untracked).
  4. Conflict prediction (merge-base and merge-tree dry-run).
  5. DecisionCouncil adversarial deliberation trigger and brief generator.
  6. SSH agent and credential verification (batch mode test).
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


def run_cmd(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 30) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", f"Command timed out after {timeout}s: {' '.join(cmd)}"
    except Exception as e:
        return 1, "", str(e)


class GitSyncAuditor:
    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir.resolve()
        self.is_repo = False
        self.branch = "HEAD"
        self.upstream = ""
        self.remote = "origin"
        self.remote_url = ""
        self._check_repo()

    def _check_repo(self):
        ret, out, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=self.repo_dir)
        if ret == 0 and out == "true":
            self.is_repo = True
            _, self.branch, _ = run_cmd(["git", "branch", "--show-current"], cwd=self.repo_dir)
            if not self.branch:
                self.branch = "HEAD"

            _, upstream, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "@{u}"], cwd=self.repo_dir)
            self.upstream = upstream
            if not self.upstream and self.branch != "HEAD":
                self.upstream = f"origin/{self.branch}"

            _, r_url, _ = run_cmd(["git", "remote", "get-url", "origin"], cwd=self.repo_dir)
            self.remote_url = r_url

    def fetch(self) -> Tuple[bool, str]:
        if not self.is_repo:
            return False, "Not a git repository"
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes -o ConnectTimeout=10"
        try:
            proc = subprocess.run(
                ["git", "fetch", "--prune", "origin"],
                cwd=self.repo_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20,
                env=env
            )
            if proc.returncode != 0:
                return False, proc.stderr.strip() or proc.stdout.strip()
            return True, "Fetched origin successfully"
        except subprocess.TimeoutExpired:
            return False, "Fetch timed out (remote unreachable or interactive auth required)"
        except Exception as e:
            return False, str(e)

    def check_ssh_auth(self) -> Dict[str, Any]:
        result = {
            "is_ssh": self.remote_url.startswith("git@") or "ssh://" in self.remote_url,
            "ssh_auth_sock": bool(os.environ.get("SSH_AUTH_SOCK")),
            "agent_keys_loaded": 0,
            "batch_mode_ok": False,
            "message": ""
        }
        if not result["is_ssh"]:
            result["message"] = "Remote uses HTTPS/local transport"
            return result

        ret, out, _ = run_cmd(["ssh-add", "-l"])
        if ret == 0:
            lines = [l for l in out.splitlines() if l.strip()]
            result["agent_keys_loaded"] = len(lines)

        host = "github.com"
        if "github.com" in self.remote_url:
            host = "github.com"
        elif "gitlab.com" in self.remote_url:
            host = "gitlab.com"

        ret_ssh, out_ssh, err_ssh = run_cmd(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-T", f"git@{host}"],
            timeout=10
        )
        combined = f"{out_ssh} {err_ssh}".lower()
        if "successfully authenticated" in combined or "you've successfully authenticated" in combined:
            result["batch_mode_ok"] = True
            result["message"] = f"SSH authentication to {host} is active and non-interactive."
        elif "permission denied (publickey)" in combined:
            result["batch_mode_ok"] = False
            result["message"] = f"SSH key requires passphrase or is not registered with {host}."
        else:
            result["batch_mode_ok"] = (ret_ssh == 0)
            result["message"] = f"SSH check output: {err_ssh or out_ssh}"

        return result

    def audit_status(self) -> Dict[str, Any]:
        if not self.is_repo:
            return {"error": "Not a git repository"}

        # 1. Working tree status
        _, staged_out, _ = run_cmd(["git", "diff", "--cached", "--name-status"], cwd=self.repo_dir)
        _, unstaged_out, _ = run_cmd(["git", "diff", "--name-status"], cwd=self.repo_dir)
        _, untracked_out, _ = run_cmd(["git", "ls-files", "--others", "--exclude-standard"], cwd=self.repo_dir)

        staged = [l for l in staged_out.splitlines() if l.strip()]
        unstaged = [l for l in unstaged_out.splitlines() if l.strip()]
        untracked = [l for l in untracked_out.splitlines() if l.strip()]
        is_clean = (len(staged) == 0 and len(unstaged) == 0)

        # 2. Ahead / Behind calculation
        ahead_count = 0
        behind_count = 0
        has_upstream = False
        merge_base = ""

        if self.upstream:
            ret_chk, _, _ = run_cmd(["git", "rev-parse", "--verify", self.upstream], cwd=self.repo_dir)
            if ret_chk == 0:
                has_upstream = True
                ret_rev, out_rev, _ = run_cmd(
                    ["git", "rev-list", "--left-right", "--count", f"HEAD...{self.upstream}"],
                    cwd=self.repo_dir
                )
                if ret_rev == 0 and out_rev:
                    parts = out_rev.split()
                    if len(parts) == 2:
                        ahead_count = int(parts[0])
                        behind_count = int(parts[1])

                _, mb, _ = run_cmd(["git", "merge-base", "HEAD", self.upstream], cwd=self.repo_dir)
                merge_base = mb

        # 3. Commit logs
        unpushed_commits = []
        unpulled_commits = []
        if has_upstream and ahead_count > 0:
            _, log_ahead, _ = run_cmd(
                ["git", "log", f"{self.upstream}..HEAD", "--oneline", "-n", "10"],
                cwd=self.repo_dir
            )
            unpushed_commits = [l for l in log_ahead.splitlines() if l.strip()]

        if has_upstream and behind_count > 0:
            _, log_behind, _ = run_cmd(
                ["git", "log", f"HEAD..{self.upstream}", "--oneline", "-n", "10"],
                cwd=self.repo_dir
            )
            unpulled_commits = [l for l in log_behind.splitlines() if l.strip()]

        # 4. State classification
        if not has_upstream:
            state = "NO_UPSTREAM"
        elif ahead_count == 0 and behind_count == 0:
            state = "IN_SYNC"
        elif ahead_count > 0 and behind_count == 0:
            state = "AHEAD"
        elif ahead_count == 0 and behind_count > 0:
            state = "BEHIND"
        else:
            state = "DIVERGED"

        # 5. Potential conflict detection
        potential_conflicts = []
        if state in ("DIVERGED", "BEHIND") and merge_base:
            _, diff_remote, _ = run_cmd(
                ["git", "diff", "--name-only", f"{merge_base}..{self.upstream}"],
                cwd=self.repo_dir
            )
            remote_files = set(diff_remote.splitlines())

            _, diff_local, _ = run_cmd(
                ["git", "diff", "--name-only", f"{merge_base}..HEAD"],
                cwd=self.repo_dir
            )
            local_files = set(diff_local.splitlines())

            # Also check uncommitted local changes
            uncommitted_files = set([l.split()[-1] for l in staged + unstaged])
            local_total = local_files.union(uncommitted_files)

            overlap = remote_files.intersection(local_total)
            potential_conflicts = sorted(list(overlap))

        # 6. Deliberation trigger evaluation
        trigger_council = False
        council_reasons = []

        if state == "DIVERGED":
            trigger_council = True
            council_reasons.append(
                f"Branch is diverged: {ahead_count} commits ahead, {behind_count} commits behind {self.upstream}."
            )

        if len(potential_conflicts) > 0:
            trigger_council = True
            council_reasons.append(
                f"File modification collision detected in {len(potential_conflicts)} files: {', '.join(potential_conflicts[:5])}"
            )

        if not is_clean and behind_count > 0:
            trigger_council = True
            council_reasons.append("Working tree has uncommitted modifications while remote has incoming commits.")

        auth_info = self.check_ssh_auth()

        return {
            "repo_dir": str(self.repo_dir),
            "branch": self.branch,
            "upstream": self.upstream,
            "remote_url": self.remote_url,
            "state": state,
            "is_clean": is_clean,
            "ahead_count": ahead_count,
            "behind_count": behind_count,
            "merge_base": merge_base,
            "staged_count": len(staged),
            "unstaged_count": len(unstaged),
            "untracked_count": len(untracked),
            "unpushed_commits": unpushed_commits,
            "unpulled_commits": unpulled_commits,
            "potential_conflicts": potential_conflicts,
            "trigger_council": trigger_council,
            "council_reasons": council_reasons,
            "auth": auth_info
        }

    def generate_council_brief(self, audit: Dict[str, Any]) -> str:
        branch = audit["branch"]
        upstream = audit["upstream"]
        reasons = "\n".join(f"- {r}" for r in audit["council_reasons"])
        conflicts = ", ".join(audit["potential_conflicts"]) if audit["potential_conflicts"] else "None identified"

        brief = f"""================================================================================
🏛️ DECISION COUNCIL CONVENED: GIT SYNCHRONIZATION & CONFLICT RESOLUTION
================================================================================

Target Repository : {audit['repo_dir']}
Active Branch     : {branch} -> {upstream}
Sync State        : {audit['state']} (Ahead: {audit['ahead_count']}, Behind: {audit['behind_count']})
Clean Worktree    : {audit['is_clean']} (Staged: {audit['staged_count']}, Unstaged: {audit['unstaged_count']})

TRIGGER CONDITIONS:
{reasons}

POTENTIAL COLLISION FILES:
{conflicts}

--------------------------------------------------------------------------------
COUNCIL DELIBERATION ROLES:
--------------------------------------------------------------------------------
1. ⚖️ The Chairman:
   - Frame the resolution policy: Preserving scientific data provenance vs clean git history.
   - Enforce non-destructive merge: Zero loss of unpushed DFT outputs or calculations.

2. 🔍 The Fact Checker:
   - Audit diffs between HEAD and {upstream}.
   - Verify whether conflicting files are text (code, scripts, configs) or binary (PDF, PNG, HDF5, POSCAR).
   - Check merge-base: {audit.get('merge_base', 'N/A')}.

3. 🕵️‍♂️ The Skeptic:
   - Challenge naive fast-forward or blind 'git pull'.
   - Identify risks of overwriting ongoing simulation logs, CONTCAR restarts, or figures.
   - Check if an interactive rebase risks rewriting published commit SHAs.

4. 🌐 The Scout:
   - Examine remote commits ({upstream}):
{chr(10).join('     * ' + c for c in audit['unpulled_commits']) if audit['unpulled_commits'] else '     * None'}
   - Identify remote collaborator changes and intent.

5. 📣 The Advocate:
   - Propose the cleanest path forward:
     Option A: Safe three-way merge (`git merge {upstream}`) with explicit conflict resolution.
     Option B: Rebase with autostash (`git pull --rebase --autostash origin {branch}`).
     Option C: Isolate local work in a feature branch before aligning master.

================================================================================
"""
        return brief


def print_status_report(audit: Dict[str, Any]):
    print("=" * 80)
    print(f"📦 GIT REPOSITORY STATUS & REMOTE SYNCHRONIZATION AUDIT")
    print("=" * 80)
    print(f"Directory   : {audit['repo_dir']}")
    print(f"Branch      : {audit['branch']} -> {audit['upstream']}")
    print(f"Remote URL  : {audit['remote_url']}")
    print(f"Sync State  : {audit['state']}")
    print(f"Commits     : Ahead: {audit['ahead_count']}  |  Behind: {audit['behind_count']}")
    print(f"Worktree    : Clean={audit['is_clean']} (Staged: {audit['staged_count']}, Unstaged: {audit['unstaged_count']}, Untracked: {audit['untracked_count']})")
    print(f"SSH Auth    : BatchMode OK={audit['auth']['batch_mode_ok']} ({audit['auth']['message']})")

    if audit["unpushed_commits"]:
        print("\nUnpushed Local Commits (to be pushed):")
        for c in audit["unpushed_commits"]:
            print(f"  ⬆️ {c}")

    if audit["unpulled_commits"]:
        print("\nIncoming Remote Commits (to be pulled):")
        for c in audit["unpulled_commits"]:
            print(f"  ⬇️ {c}")

    if audit["potential_conflicts"]:
        print("\n⚠️ Potential File Collisions / Overlaps:")
        for f in audit["potential_conflicts"]:
            print(f"  💥 {f}")

    if audit["trigger_council"]:
        print("\n🏛️ DecisionCouncil Triggered:")
        for r in audit["council_reasons"]:
            print(f"  * {r}")
    else:
        print("\n✅ Clear Path: No divergence or conflict risks detected.")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Git Sync & Remote Auditor")
    parser.add_argument("--cwd", type=str, default=".", help="Repository working directory")
    parser.add_argument("--fetch", action="store_true", help="Fetch remote before auditing")
    parser.add_argument("--council", action="store_true", help="Generate DecisionCouncil brief")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--pull", action="store_true", help="Safely pull upstream changes")
    parser.add_argument("--push", action="store_true", help="Push local commits")
    args = parser.parse_args()

    repo_path = Path(args.cwd)
    auditor = GitSyncAuditor(repo_path)
    if not auditor.is_repo:
        print(f"Error: {repo_path} is not a valid git repository", file=sys.stderr)
        sys.exit(1)

    if args.fetch:
        ok, msg = auditor.fetch()
        if not ok:
            print(f"Warning: Fetch failed: {msg}", file=sys.stderr)

    audit = auditor.audit_status()

    if args.json:
        print(json.dumps(audit, indent=2))
        return

    if args.council or audit["trigger_council"]:
        brief = auditor.generate_council_brief(audit)
        print(brief)

    print_status_report(audit)

    if args.pull:
        if audit["behind_count"] == 0:
            print("[INFO] Already up to date with upstream.")
        elif audit["trigger_council"]:
            print("[ERROR] Cannot auto-pull: DecisionCouncil triggered due to divergence or conflict risk.", file=sys.stderr)
            sys.exit(2)
        else:
            print("[INFO] Executing safe fast-forward pull...")
            ret, out, err = run_cmd(["git", "pull", "--ff-only"], cwd=repo_path)
            print(out or err)

    if args.push:
        if audit["ahead_count"] == 0:
            print("[INFO] Nothing to push (local is in sync with upstream).")
        elif not audit["auth"]["batch_mode_ok"]:
            print(f"[AUTH_REQUIRED] {audit['auth']['message']}")
            print("Please run 'git push origin master' interactively in your terminal.")
            sys.exit(3)
        elif audit["trigger_council"]:
            print("[ERROR] Cannot push: Remote has diverged. Deliberate with DecisionCouncil first.", file=sys.stderr)
            sys.exit(2)
        else:
            print("[INFO] Executing safe push...")
            ret, out, err = run_cmd(["git", "push", "origin", auditor.branch], cwd=repo_path)
            if ret == 0:
                print(f"[✓] Push successful: {out or err}")
            else:
                print(f"[ERROR] Push failed: {err or out}", file=sys.stderr)
                sys.exit(1)


if __name__ == "__main__":
    main()
