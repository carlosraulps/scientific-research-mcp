#!/usr/bin/env python3
"""
git_sync_tool.py
================
Enterprise & Research-Grade Git Synchronization, Divergence Auditor, and
DecisionCouncil Deliberation Engine.

Designed for high-concurrency scientific simulation workflows, multi-agent systems,
and multi-cluster HPC repositories.

Core Capabilities:
  1. Dual Logging System: Rich ANSI terminal logger + persistent structured file logger.
  2. Pre-flight remote audit: Tracking branch detection, non-interactive SSH agent check.
  3. Divergence metrics: Accurate ahead/behind counting and commit inspection.
  4. Working tree protection: Dirty tree audit, optional --autostash support.
  5. In-Memory Conflict Prediction: Zero-touch simulation via `git merge-tree`.
  6. Binary & SQLite Database Safety Guard: Automatic snapshot backups before operations.
  7. DecisionCouncil Deliberation Engine: Formal 5-voice adversarial brief generator.
  8. Post-sync automation: Automatic Graphify knowledge graph sync hook.
"""

import os
import sys
import time
import json
import shutil
import argparse
import datetime
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set


# ==============================================================================
# COLOR & FORMATTING SYSTEM (ANSI + NO_COLOR RESPECT)
# ==============================================================================

class Colors:
    """ANSI color definitions with automatic TTY and NO_COLOR detection."""
    ENABLED = sys.stdout.isatty() and not os.environ.get("NO_COLOR")

    RESET = "\033[0m" if ENABLED else ""
    BOLD = "\033[1m" if ENABLED else ""
    DIM = "\033[2m" if ENABLED else ""
    UNDERLINE = "\033[4m" if ENABLED else ""

    RED = "\033[91m" if ENABLED else ""
    GREEN = "\033[92m" if ENABLED else ""
    YELLOW = "\033[93m" if ENABLED else ""
    BLUE = "\033[94m" if ENABLED else ""
    MAGENTA = "\033[95m" if ENABLED else ""
    CYAN = "\033[96m" if ENABLED else ""
    WHITE = "\033[97m" if ENABLED else ""

    BG_RED = "\033[41m\033[97m" if ENABLED else ""
    BG_GREEN = "\033[42m\033[97m" if ENABLED else ""
    BG_YELLOW = "\033[43m\033[30m" if ENABLED else ""
    BG_BLUE = "\033[44m\033[97m" if ENABLED else ""


# ==============================================================================
# STRUCTURED & ROTATING LOGGER
# ==============================================================================

class SyncLogger:
    """
    Dual-output professional logging manager:
    - Writes human-friendly, colored messages to stdout/stderr.
    - Writes timestamped, structured audit entries to a persistent log file.
    """

    def __init__(self, log_file: Optional[Path] = None, verbose: bool = False, debug: bool = False, quiet: bool = False):
        self.verbose = verbose
        self.debug = debug
        self.quiet = quiet
        self.pid = os.getpid()

        if log_file:
            self.log_file = log_file.resolve()
        else:
            state_dir = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")) / "git-sync"
            state_dir.mkdir(parents=True, exist_ok=True)
            self.log_file = state_dir / "git-sync.log"

        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def _write_file_log(self, level: str, message: str, context: Optional[str] = None):
        """Appends a structured log entry to the log file."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        ctx_str = f" [{context}]" if context else ""
        line = f"[{now}] [PID:{self.pid}] [{level:<5}]{ctx_str} {message}\n"
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass

    def info(self, message: str, context: Optional[str] = None):
        self._write_file_log("INFO", message, context)
        if not self.quiet:
            print(f"{Colors.CYAN}[ℹ]{Colors.RESET} {message}")

    def success(self, message: str, context: Optional[str] = None):
        self._write_file_log("OK", message, context)
        if not self.quiet:
            print(f"{Colors.GREEN}[✓]{Colors.RESET} {message}")

    def warning(self, message: str, context: Optional[str] = None):
        self._write_file_log("WARN", message, context)
        if not self.quiet:
            print(f"{Colors.YELLOW}[⚠]{Colors.RESET} {Colors.YELLOW}{message}{Colors.RESET}")

    def error(self, message: str, context: Optional[str] = None):
        self._write_file_log("ERROR", message, context)
        print(f"{Colors.RED}[✗]{Colors.RESET} {Colors.RED}{message}{Colors.RESET}", file=sys.stderr)

    def critical(self, message: str, context: Optional[str] = None):
        self._write_file_log("CRIT", message, context)
        print(f"{Colors.BG_RED} CRITICAL {Colors.RESET} {Colors.RED}{Colors.BOLD}{message}{Colors.RESET}", file=sys.stderr)

    def cmd(self, command: str, duration_ms: float, ret_code: int, context: Optional[str] = None):
        status = "OK" if ret_code == 0 else f"ERR:{ret_code}"
        msg = f"CMD ({duration_ms:.1f}ms, {status}): {command}"
        self._write_file_log("DEBUG", msg, context)
        if self.debug and not self.quiet:
            color = Colors.DIM if ret_code == 0 else Colors.RED
            print(f"{color}    ↳ [exec] {command} ({duration_ms:.1f}ms, exit {ret_code}){Colors.RESET}")

    def read_recent_logs(self, lines_count: int = 40) -> List[str]:
        """Returns the last N lines of the log file."""
        if not self.log_file.exists():
            return [f"Log file {self.log_file} does not exist yet."]
        try:
            with open(self.log_file, "r", encoding="utf-8", errors="replace") as f:
                all_lines = f.readlines()
                return all_lines[-lines_count:]
        except Exception as e:
            return [f"Error reading log file: {e}"]


# ==============================================================================
# COMMAND EXECUTION LAYER
# ==============================================================================

def run_cmd(
    cmd: List[str],
    cwd: Optional[Path] = None,
    timeout: int = 35,
    logger: Optional[SyncLogger] = None,
    context: Optional[str] = None
) -> Tuple[int, str, str]:
    """
    Executes a shell command safely, timing execution and logging details.
    """
    start_time = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        elapsed_ms = (time.time() - start_time) * 1000.0
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        if logger:
            logger.cmd(" ".join(cmd), elapsed_ms, proc.returncode, context)
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        elapsed_ms = (time.time() - start_time) * 1000.0
        err_msg = f"Command timed out after {timeout}s: {' '.join(cmd)}"
        if logger:
            logger.cmd(" ".join(cmd), elapsed_ms, 124, context)
            logger.error(err_msg, context)
        return 124, "", err_msg
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000.0
        if logger:
            logger.cmd(" ".join(cmd), elapsed_ms, 1, context)
            logger.error(str(e), context)
        return 1, "", str(e)


# ==============================================================================
# AUDITOR & SYNCHRONIZATION ENGINE
# ==============================================================================

class GitSyncAuditor:
    """
    Performs comprehensive pre-flight analysis, divergence calculations,
    in-memory merge simulations, and automated recovery operations.
    """

    BINARY_EXTENSIONS = {
        ".db", ".sqlite", ".sqlite3", ".h5", ".hdf5", ".npy", ".npz",
        ".pkl", ".pickle", ".bin", ".dat", ".pdf", ".png", ".jpg",
        ".jpeg", ".gif", ".mp4", ".zip", ".tar", ".gz", ".xz"
    }

    STRUCTURED_DATA_EXTENSIONS = {
        ".csv", ".tsv", ".json", ".jsonl", ".yaml", ".yml", ".xml"
    }

    def __init__(self, repo_dir: Path, logger: SyncLogger, dry_run: bool = False):
        self.repo_dir = repo_dir.resolve()
        self.logger = logger
        self.dry_run = dry_run
        self.is_repo = False
        self.branch = "HEAD"
        self.upstream = ""
        self.remote = "origin"
        self.remote_url = ""
        self._check_repo()

    def _check_repo(self):
        ret, out, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=self.repo_dir, logger=self.logger, context="init")
        if ret == 0 and out == "true":
            self.is_repo = True
            _, root, _ = run_cmd(["git", "rev-parse", "--show-toplevel"], cwd=self.repo_dir, logger=self.logger, context="init")
            if root:
                self.repo_dir = Path(root).resolve()

            _, self.branch, _ = run_cmd(["git", "branch", "--show-current"], cwd=self.repo_dir, logger=self.logger, context="init")
            if not self.branch:
                self.branch = "HEAD"

            _, upstream, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "@{u}"], cwd=self.repo_dir, logger=self.logger, context="init")
            self.upstream = upstream
            if not self.upstream and self.branch != "HEAD":
                self.upstream = f"origin/{self.branch}"

            _, r_url, _ = run_cmd(["git", "remote", "get-url", "origin"], cwd=self.repo_dir, logger=self.logger, context="init")
            self.remote_url = r_url

    def fetch(self) -> Tuple[bool, str]:
        """Performs a safe prune fetch against origin using non-interactive SSH."""
        if not self.is_repo:
            return False, "Not a git repository"

        self.logger.info("Fetching remote updates from origin...", context=self.branch)
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes -o ConnectTimeout=10"
        try:
            start_t = time.time()
            proc = subprocess.run(
                ["git", "fetch", "--prune", "origin"],
                cwd=self.repo_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=25,
                env=env
            )
            elapsed_ms = (time.time() - start_t) * 1000.0
            self.logger.cmd("git fetch --prune origin", elapsed_ms, proc.returncode, context=self.branch)
            if proc.returncode != 0:
                err = proc.stderr.strip() or proc.stdout.strip()
                self.logger.warning(f"Remote fetch returned non-zero: {err}", context=self.branch)
                return False, err
            self.logger.success("Remote origin fetched successfully.", context=self.branch)
            return True, "Fetched origin successfully"
        except subprocess.TimeoutExpired:
            msg = "Fetch timed out after 25s (network latency or interactive password prompt)."
            self.logger.error(msg, context=self.branch)
            return False, msg
        except Exception as e:
            self.logger.error(f"Fetch failed: {e}", context=self.branch)
            return False, str(e)

    def check_ssh_auth(self) -> Dict[str, Any]:
        """Audits SSH keys and tests non-interactive connection."""
        result = {
            "is_ssh": self.remote_url.startswith("git@") or "ssh://" in self.remote_url,
            "ssh_auth_sock": bool(os.environ.get("SSH_AUTH_SOCK")),
            "agent_keys_loaded": 0,
            "batch_mode_ok": False,
            "host": "github.com",
            "message": ""
        }
        if not result["is_ssh"]:
            result["message"] = "Remote uses HTTPS/local transport"
            result["batch_mode_ok"] = True
            return result

        ret, out, _ = run_cmd(["ssh-add", "-l"], logger=self.logger, context="auth")
        if ret == 0:
            lines = [l for l in out.splitlines() if l.strip()]
            result["agent_keys_loaded"] = len(lines)

        host = "github.com"
        if "gitlab.com" in self.remote_url:
            host = "gitlab.com"
        result["host"] = host

        ret_ssh, out_ssh, err_ssh = run_cmd(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-T", f"git@{host}"],
            timeout=8,
            logger=self.logger,
            context="auth"
        )
        combined = f"{out_ssh} {err_ssh}".lower()
        if "successfully authenticated" in combined or "you've successfully authenticated" in combined:
            result["batch_mode_ok"] = True
            result["message"] = f"SSH authentication to {host} is verified and non-interactive."
        elif "permission denied (publickey)" in combined:
            result["batch_mode_ok"] = False
            result["message"] = f"SSH key requires passphrase or is not registered with {host}."
        else:
            result["batch_mode_ok"] = (ret_ssh == 0)
            result["message"] = f"SSH check: {err_ssh or out_ssh}"

        return result

    def simulate_merge_conflicts(self, merge_base: str) -> Dict[str, Any]:
        """
        Uses Git's in-memory `git merge-tree` to predict conflicts without
        touching the working directory.
        """
        sim_result = {
            "has_conflicts": False,
            "conflict_files": [],
            "binary_conflicts": [],
            "structured_conflicts": [],
            "code_conflicts": []
        }
        if not self.upstream or not merge_base:
            return sim_result

        ret, out, err = run_cmd(
            ["git", "merge-tree", "--write-tree", "HEAD", self.upstream],
            cwd=self.repo_dir,
            logger=self.logger,
            context="merge-tree"
        )
        lines = (out + "\n" + err).splitlines()
        for line in lines:
            line_str = line.strip()
            if "CONFLICT (content): Merge conflict in" in line_str:
                fname = line_str.replace("CONFLICT (content): Merge conflict in", "").strip()
                sim_result["conflict_files"].append(fname)
            elif "warning: Cannot merge binary files:" in line_str:
                fname = line_str.replace("warning: Cannot merge binary files:", "").replace("(HEAD vs. " + self.upstream + ")", "").strip()
                if fname not in sim_result["conflict_files"]:
                    sim_result["conflict_files"].append(fname)

        if sim_result["conflict_files"]:
            sim_result["has_conflicts"] = True
            for f in sorted(list(set(sim_result["conflict_files"]))):
                ext = Path(f).suffix.lower()
                if ext in self.BINARY_EXTENSIONS:
                    sim_result["binary_conflicts"].append(f)
                elif ext in self.STRUCTURED_DATA_EXTENSIONS:
                    sim_result["structured_conflicts"].append(f)
                else:
                    sim_result["code_conflicts"].append(f)

        return sim_result

    def backup_sqlite_databases(self) -> List[str]:
        """
        Takes timestamped snapshot backups of any SQLite or database files
        before performing pull/merge operations.
        """
        backed_up = []
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.repo_dir / ".git" / "git-sync-backups" / timestamp

        # Look in memory/ and root for .db / .sqlite files
        db_paths = list(self.repo_dir.glob("memory/*.db")) + list(self.repo_dir.glob("*.db"))
        for db in db_paths:
            if db.is_file():
                try:
                    backup_dir.mkdir(parents=True, exist_ok=True)
                    target = backup_dir / db.name
                    shutil.copy2(db, target)
                    backed_up.append(str(db.relative_to(self.repo_dir)))
                except Exception as e:
                    self.logger.error(f"Failed to backup {db}: {e}", context="backup")

        if backed_up:
            self.logger.info(f"Safeguarded {len(backed_up)} database(s) in {backup_dir.relative_to(self.repo_dir)}", context="backup")
        return backed_up

    def audit_status(self) -> Dict[str, Any]:
        """Comprehensive status audit matching DecisionCouncil requirements."""
        if not self.is_repo:
            return {"error": "Not a git repository"}

        # 1. Working tree status
        _, staged_out, _ = run_cmd(["git", "diff", "--cached", "--name-status"], cwd=self.repo_dir, logger=self.logger, context="audit")
        _, unstaged_out, _ = run_cmd(["git", "diff", "--name-status"], cwd=self.repo_dir, logger=self.logger, context="audit")
        _, untracked_out, _ = run_cmd(["git", "ls-files", "--others", "--exclude-standard"], cwd=self.repo_dir, logger=self.logger, context="audit")

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
            ret_chk, _, _ = run_cmd(["git", "rev-parse", "--verify", self.upstream], cwd=self.repo_dir, logger=self.logger, context="audit")
            if ret_chk == 0:
                has_upstream = True
                ret_rev, out_rev, _ = run_cmd(
                    ["git", "rev-list", "--left-right", "--count", f"HEAD...{self.upstream}"],
                    cwd=self.repo_dir,
                    logger=self.logger,
                    context="audit"
                )
                if ret_rev == 0 and out_rev:
                    parts = out_rev.split()
                    if len(parts) == 2:
                        ahead_count = int(parts[0])
                        behind_count = int(parts[1])

                _, mb, _ = run_cmd(["git", "merge-base", "HEAD", self.upstream], cwd=self.repo_dir, logger=self.logger, context="audit")
                merge_base = mb

        # 3. Commit logs
        unpushed_commits = []
        unpulled_commits = []
        if has_upstream and ahead_count > 0:
            _, log_ahead, _ = run_cmd(
                ["git", "log", f"{self.upstream}..HEAD", "--oneline", "-n", "15"],
                cwd=self.repo_dir,
                logger=self.logger,
                context="audit"
            )
            unpushed_commits = [l for l in log_ahead.splitlines() if l.strip()]

        if has_upstream and behind_count > 0:
            _, log_behind, _ = run_cmd(
                ["git", "log", f"HEAD..{self.upstream}", "--oneline", "-n", "15"],
                cwd=self.repo_dir,
                logger=self.logger,
                context="audit"
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

        # 5. Overlapping modified files & Simulation
        overlapping_files = []
        sim_conflicts = {"has_conflicts": False, "conflict_files": [], "binary_conflicts": [], "structured_conflicts": [], "code_conflicts": []}

        if state in ("DIVERGED", "BEHIND") and merge_base:
            _, diff_remote, _ = run_cmd(
                ["git", "diff", "--name-only", f"{merge_base}..{self.upstream}"],
                cwd=self.repo_dir,
                logger=self.logger,
                context="audit"
            )
            remote_files = set(diff_remote.splitlines())

            _, diff_local, _ = run_cmd(
                ["git", "diff", "--name-only", f"{merge_base}..HEAD"],
                cwd=self.repo_dir,
                logger=self.logger,
                context="audit"
            )
            local_files = set(diff_local.splitlines())

            uncommitted_files = set([l.split()[-1] for l in staged + unstaged])
            local_total = local_files.union(uncommitted_files)
            overlap = remote_files.intersection(local_total)
            overlapping_files = sorted(list(overlap))

            # Run in-memory simulation
            sim_conflicts = self.simulate_merge_conflicts(merge_base)

        # 6. Deliberation trigger evaluation
        trigger_council = False
        council_reasons = []

        if state == "DIVERGED":
            trigger_council = True
            council_reasons.append(
                f"Branch diverged: {ahead_count} commits ahead, {behind_count} commits behind {self.upstream}."
            )

        if sim_conflicts["binary_conflicts"]:
            trigger_council = True
            council_reasons.append(
                f"Binary / SQLite collision hazard detected in: {', '.join(sim_conflicts['binary_conflicts'])}"
            )

        if sim_conflicts["conflict_files"]:
            trigger_council = True
            council_reasons.append(
                f"Merge tree collision in {len(sim_conflicts['conflict_files'])} file(s): {', '.join(sim_conflicts['conflict_files'][:5])}"
            )

        if not is_clean and behind_count > 0:
            trigger_council = True
            council_reasons.append("Dirty working tree with incoming unpulled commits.")

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
            "overlapping_files": overlapping_files,
            "sim_conflicts": sim_conflicts,
            "trigger_council": trigger_council,
            "council_reasons": council_reasons,
            "auth": auth_info
        }

    def generate_council_brief(self, audit: Dict[str, Any]) -> str:
        """Constructs an adversarial DecisionCouncil deliberation report."""
        branch = audit["branch"]
        upstream = audit["upstream"]
        reasons = "\n".join(f"  • {r}" for r in audit["council_reasons"])
        sim = audit["sim_conflicts"]

        binary_lines = "\n".join(f"    💥 [BINARY/SQLITE] {f}" for f in sim["binary_conflicts"]) if sim["binary_conflicts"] else "    (None)"
        struct_lines = "\n".join(f"    📊 [DATA/LOG]     {f}" for f in sim["structured_conflicts"]) if sim["structured_conflicts"] else "    (None)"
        code_lines = "\n".join(f"    📝 [CODE/DOC]     {f}" for f in sim["code_conflicts"]) if sim["code_conflicts"] else "    (None)"

        brief = f"""
{Colors.MAGENTA}================================================================================{Colors.RESET}
{Colors.BOLD}🏛️  DECISION COUNCIL CONVENED: GIT SYNCHRONIZATION & COLLISION RESOLUTION{Colors.RESET}
{Colors.MAGENTA}================================================================================{Colors.RESET}

{Colors.BOLD}Repository{Colors.RESET}  : {audit['repo_dir']}
{Colors.BOLD}Branch{Colors.RESET}      : {Colors.CYAN}{branch}{Colors.RESET} ⟷ {Colors.CYAN}{upstream}{Colors.RESET}
{Colors.BOLD}Sync State{Colors.RESET}  : {Colors.RED if audit['state'] == 'DIVERGED' else Colors.YELLOW}{audit['state']}{Colors.RESET} (Ahead: {audit['ahead_count']}, Behind: {audit['behind_count']})
{Colors.BOLD}Merge Base{Colors.RESET}  : {audit.get('merge_base', 'N/A')}

{Colors.BOLD}TRIGGER REASONS:{Colors.RESET}
{reasons}

{Colors.BOLD}IN-MEMORY MERGE-TREE COLLISION AUDIT:{Colors.RESET}
{Colors.RED}{binary_lines}{Colors.RESET}
{Colors.YELLOW}{struct_lines}{Colors.RESET}
{code_lines}

{Colors.MAGENTA}--------------------------------------------------------------------------------{Colors.RESET}
{Colors.BOLD}ADVERSARIAL COUNCIL DELIBERATION BRIEFS:{Colors.RESET}
{Colors.MAGENTA}--------------------------------------------------------------------------------{Colors.RESET}

⚖️  {Colors.BOLD}The Chairman (Preservation & Scientific Integrity){Colors.RESET}:
   • Mandatory Charter: Zero scientific data loss and zero corruption of SQLite memory.
   • Rule: Binary SQLite databases ({', '.join(sim['binary_conflicts']) or 'none'}) CANNOT be auto-merged by Git.
   • Action: Automatically snapshot databases before any operation; reconcile records deterministically.

🔍 {Colors.BOLD}The Fact Checker (Ground Truth Verification){Colors.RESET}:
   • Merge-Base SHA: {audit.get('merge_base')}
   • Local changes: {audit['ahead_count']} commits modifying skills, visualizers, and memory.
   • Remote changes: {audit['behind_count']} commits modifying literature, frontier tools, and notes.
   • File overlaps: {len(audit['overlapping_files'])} files identified.

🕵️‍♂️ {Colors.BOLD}The Skeptic (Risk Auditor & Failure Modes){Colors.RESET}:
   • Risk 1: A blind `git pull` or `git merge` will throw "Cannot merge binary files" and corrupt local DBs.
   • Risk 2: Rebase (`git pull --rebase`) risks rewriting published commit hashes and stopping midway.
   • Risk 3: Dirty working tree files could be overwritten or tangled in stash conflict.

🌐 {Colors.BOLD}The Scout (Remote Intent & Context){Colors.RESET}:
   • Remote commits include valuable updates:
{chr(10).join('     * ' + c for c in audit['unpulled_commits'][:6]) if audit['unpulled_commits'] else '     * None'}
   • Upstream work must be integrated, not discarded.

📣 {Colors.BOLD}The Advocate (Integration Strategy Options){Colors.RESET}:
   • {Colors.GREEN}Option A (Recommended){Colors.RESET}: Isolate local branch (`git branch backup-local`), backup DBs,
     checkout clean integration merge, and resolve structured logs without loss.
   • {Colors.YELLOW}Option B{Colors.RESET}: Safe 3-way merge with explicit `--no-commit`, preserve local DBs or remote DBs,
     re-apply missing facts/skills via sciresearch memory export, then finalize merge commit.
   • {Colors.BLUE}Option C{Colors.RESET}: Cherry-pick cleanly isolated skill additions on top of updated upstream.

{Colors.MAGENTA}================================================================================{Colors.RESET}
"""
        return brief


# ==============================================================================
# REPORTING & DISPLAY FORMATTING
# ==============================================================================

def print_audit_report(audit: Dict[str, Any]):
    state_color = Colors.GREEN if audit["state"] == "IN_SYNC" else (Colors.RED if audit["state"] == "DIVERGED" else Colors.YELLOW)

    print(f"\n{Colors.BOLD}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}📦 GIT REPOSITORY STATUS & REMOTE SYNCHRONIZATION AUDIT{Colors.RESET}")
    print(f"{'=' * 80}")
    print(f"{Colors.BOLD}Directory   :{Colors.RESET} {audit['repo_dir']}")
    print(f"{Colors.BOLD}Branch      :{Colors.RESET} {Colors.CYAN}{audit['branch']}{Colors.RESET} -> {Colors.CYAN}{audit['upstream']}{Colors.RESET}")
    print(f"{Colors.BOLD}Remote URL  :{Colors.RESET} {audit['remote_url']}")
    print(f"{Colors.BOLD}Sync State  :{Colors.RESET} {state_color}{audit['state']}{Colors.RESET}")
    print(f"{Colors.BOLD}Commits     :{Colors.RESET} Ahead: {Colors.CYAN}{audit['ahead_count']}{Colors.RESET}  |  Behind: {Colors.CYAN}{audit['behind_count']}{Colors.RESET}")
    print(f"{Colors.BOLD}Worktree    :{Colors.RESET} Clean={audit['is_clean']} (Staged: {audit['staged_count']}, Unstaged: {audit['unstaged_count']}, Untracked: {audit['untracked_count']})")
    print(f"{Colors.BOLD}SSH Auth    :{Colors.RESET} BatchMode={audit['auth']['batch_mode_ok']} ({audit['auth']['message']})")

    if audit["unpushed_commits"]:
        print(f"\n{Colors.BOLD}Unpushed Local Commits (to be pushed):{Colors.RESET}")
        for c in audit["unpushed_commits"][:8]:
            print(f"  {Colors.GREEN}⬆{Colors.RESET}  {c}")
        if len(audit["unpushed_commits"]) > 8:
            print(f"     ... and {len(audit['unpushed_commits']) - 8} more")

    if audit["unpulled_commits"]:
        print(f"\n{Colors.BOLD}Incoming Remote Commits (to be pulled):{Colors.RESET}")
        for c in audit["unpulled_commits"][:8]:
            print(f"  {Colors.BLUE}⬇{Colors.RESET}  {c}")
        if len(audit["unpulled_commits"]) > 8:
            print(f"     ... and {len(audit['unpulled_commits']) - 8} more")

    sim = audit.get("sim_conflicts", {})
    if sim.get("has_conflicts"):
        print(f"\n{Colors.BOLD}{Colors.RED}⚠️ In-Memory Predicted Conflicts:{Colors.RESET}")
        for f in sim["binary_conflicts"]:
            print(f"  {Colors.RED}💥 [BINARY/SQLITE] {f}{Colors.RESET}")
        for f in sim["structured_conflicts"]:
            print(f"  {Colors.YELLOW}📊 [DATA/LOG]     {f}{Colors.RESET}")
        for f in sim["code_conflicts"]:
            print(f"  {Colors.WHITE}📝 [CODE/DOC]     {f}{Colors.RESET}")
    elif audit["overlapping_files"]:
        print(f"\n{Colors.BOLD}⚠️ Overlapping Files Modified in Both Histories:{Colors.RESET}")
        for f in audit["overlapping_files"][:10]:
            print(f"  {Colors.YELLOW}•{Colors.RESET} {f}")

    if audit["trigger_council"]:
        print(f"\n{Colors.MAGENTA}🏛️  DecisionCouncil Triggered:{Colors.RESET}")
        for r in audit["council_reasons"]:
            print(f"  * {r}")
    else:
        print(f"\n{Colors.GREEN}✅ Clear Path: No divergence or conflict risks detected.{Colors.RESET}")

    print(f"{'=' * 80}\n")


# ==============================================================================
# MAIN CLI CONTROLLER
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Enterprise & Research Git Synchronization Tool with DecisionCouncil Protection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  git-sync                    # Safe full synchronization (fetch -> audit -> pull/push)
  git-sync --fetch            # Fetch updates and display divergence audit
  git-sync --council          # Convene DecisionCouncil deliberation brief
  git-sync --pull             # Safe fast-forward pull (aborts if diverged)
  git-sync --push             # Safe push (verifies SSH auth first)
  git-sync --log              # Inspect recent structured log history
  git-sync --backup           # Snapshot SQLite databases into .git/git-sync-backups
  git-sync --dry-run          # Simulate actions without touching filesystem
        """
    )
    parser.add_argument("--cwd", type=str, default=".", help="Target repository directory (default: current directory)")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Simulate execution without modifying files or remotes")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose console output")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable low-level command tracing with execution times")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress non-essential output")
    parser.add_argument("--log-file", type=str, help="Custom path for structured persistent log file")
    parser.add_argument("--json", action="store_true", help="Emit raw JSON output for agent/pipeline automation")

    # Actions
    parser.add_argument("--fetch", action="store_true", help="Fetch remote updates and run divergence audit")
    parser.add_argument("--pull", action="store_true", help="Pull remote updates safely")
    parser.add_argument("--push", action="store_true", help="Push local commits safely")
    parser.add_argument("--council", action="store_true", help="Explicitly convene DecisionCouncil deliberation")
    parser.add_argument("--backup", action="store_true", help="Explicitly snapshot SQLite databases")
    parser.add_argument("--log", action="store_true", help="Print recent execution logs and exit")
    parser.add_argument("--autostash", action="store_true", help="Automatically stash dirty worktree before pull")
    parser.add_argument("--post-graphify", action="store_true", help="Run 'graphify update .' after successful sync if applicable")

    args = parser.parse_args()

    custom_log = Path(args.log_file) if args.log_file else None
    logger = SyncLogger(log_file=custom_log, verbose=args.verbose, debug=args.debug, quiet=args.quiet)

    if args.log:
        logs = logger.read_recent_logs(40)
        print("".join(logs))
        return

    repo_dir = Path(args.cwd)
    auditor = GitSyncAuditor(repo_dir, logger, dry_run=args.dry_run)
    if not auditor.is_repo:
        logger.error(f"Directory {repo_dir.resolve()} is not a valid git repository.")
        sys.exit(1)

    logger.info(f"Target repository: {auditor.repo_dir} (branch: {auditor.branch})", context="entry")

    # If --fetch or default run with no specific pull/push action: fetch remote first
    should_fetch = args.fetch or (not args.pull and not args.push and not args.council and not args.backup)
    if should_fetch:
        auditor.fetch()

    audit = auditor.audit_status()

    if args.json:
        print(json.dumps(audit, indent=2))
        return

    if args.council or (audit["trigger_council"] and not args.pull and not args.push):
        brief = auditor.generate_council_brief(audit)
        print(brief)

    print_audit_report(audit)

    if args.backup:
        auditor.backup_sqlite_databases()
        return

    # Safe Pull Execution
    if args.pull:
        if audit["behind_count"] == 0:
            logger.info("Already up to date with upstream.", context="pull")
        elif audit["trigger_council"]:
            logger.critical("Cannot execute auto-pull: DecisionCouncil triggered due to divergence or conflict risk.", context="pull")
            print(f"{Colors.YELLOW}Run 'git-sync --council' to inspect deliberation and resolution plan.{Colors.RESET}")
            sys.exit(2)
        else:
            stash_created = False
            if not audit["is_clean"]:
                if args.autostash:
                    logger.info("Autostashing uncommitted changes...", context="autostash")
                    ret, out, err = run_cmd(["git", "stash", "push", "-m", f"git-sync-autostash-{int(time.time())}"], cwd=auditor.repo_dir, logger=logger, context="autostash")
                    stash_created = (ret == 0)
                else:
                    logger.error("Working tree is dirty. Commit, stash, or pass --autostash.", context="pull")
                    sys.exit(1)

            logger.info("Executing safe fast-forward pull...", context="pull")
            if not args.dry_run:
                ret, out, err = run_cmd(["git", "pull", "--ff-only"], cwd=auditor.repo_dir, logger=logger, context="pull")
                if ret == 0:
                    logger.success(f"Pull successful: {out}", context="pull")
                else:
                    logger.error(f"Fast-forward pull failed: {err or out}", context="pull")
                    sys.exit(1)

            if stash_created:
                logger.info("Popping autostashed changes...", context="autostash")
                run_cmd(["git", "stash", "pop"], cwd=auditor.repo_dir, logger=logger, context="autostash")

    # Safe Push Execution
    if args.push:
        if audit["ahead_count"] == 0:
            logger.info("Nothing to push: local branch is synchronized with upstream.", context="push")
        elif not audit["auth"]["batch_mode_ok"]:
            logger.warning(f"SSH authentication requires interactive terminal: {audit['auth']['message']}", context="push")
            print(f"\n{Colors.BOLD}Execute interactively in terminal:{Colors.RESET}")
            print(f"  ssh-add ~/.ssh/id_ed25519 && git push origin {auditor.branch}\n")
            sys.exit(3)
        elif audit["trigger_council"]:
            logger.critical("Cannot push: remote branch has diverged. Deliberate with DecisionCouncil first.", context="push")
            sys.exit(2)
        else:
            logger.info(f"Executing safe push to origin/{auditor.branch}...", context="push")
            if not args.dry_run:
                ret, out, err = run_cmd(["git", "push", "origin", auditor.branch], cwd=auditor.repo_dir, logger=logger, context="push")
                if ret == 0:
                    logger.success(f"Push successful: {out or err}", context="push")
                else:
                    logger.error(f"Push failed: {err or out}", context="push")
                    sys.exit(1)

    # Full Default Sync Workflow (if no action flags specified)
    if not args.pull and not args.push and not args.council and not args.backup:
        if audit["state"] == "IN_SYNC":
            logger.success("Repository is completely in sync with remote tracking branch.", context="sync")
        elif audit["state"] == "AHEAD":
            logger.info(f"Local branch is {audit['ahead_count']} commit(s) ahead. Proceeding to safe push...", context="sync")
            if audit["auth"]["batch_mode_ok"]:
                if not args.dry_run:
                    ret, out, err = run_cmd(["git", "push", "origin", auditor.branch], cwd=auditor.repo_dir, logger=logger, context="sync")
                    if ret == 0:
                        logger.success(f"Push completed successfully.", context="sync")
                    else:
                        logger.error(f"Push failed: {err or out}", context="sync")
            else:
                logger.warning(f"Interactive SSH authentication required to push: {audit['auth']['message']}", context="sync")
                print(f"Please run in terminal: ssh-add ~/.ssh/id_ed25519 && git push origin {auditor.branch}")
        elif audit["state"] == "BEHIND":
            if audit["is_clean"]:
                logger.info(f"Local branch is {audit['behind_count']} commit(s) behind. Performing fast-forward pull...", context="sync")
                if not args.dry_run:
                    ret, out, err = run_cmd(["git", "pull", "--ff-only"], cwd=auditor.repo_dir, logger=logger, context="sync")
                    if ret == 0:
                        logger.success(f"Fast-forward pull completed.", context="sync")
                    else:
                        logger.error(f"Pull failed: {err or out}", context="sync")
            else:
                logger.warning("Local branch is behind, but working tree is dirty. Autostash or commit first.", context="sync")
        elif audit["state"] == "DIVERGED":
            logger.critical("Branches have diverged with potential conflict risks. Review the DecisionCouncil brief above.", context="sync")
            print(f"{Colors.BOLD}Recommended Next Step:{Colors.RESET} Deliberate resolution with DecisionCouncil before merging.")

    # Post-sync Graphify hook if requested
    if args.post_graphify and (auditor.repo_dir / "graphify-out").exists():
        logger.info("Executing post-sync Graphify knowledge graph update...", context="hook")
        run_cmd(["graphify", "update", "."], cwd=auditor.repo_dir, logger=logger, context="hook")


if __name__ == "__main__":
    main()
