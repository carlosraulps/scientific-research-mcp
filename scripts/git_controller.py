#!/usr/bin/env python3
"""
================================================================================
Scientific Git Version Controller & Provenance Integrator
================================================================================
Binds Git version control directly to the DREAMS Canvas, MDCrow Checkpoints,
and computational reproducibility audits:
  1. Status & Reproducibility: Captures exact commit SHA, branch, and dirty status.
  2. Scientific Snapshots: Automates structured git commits linked to Run IDs,
     Artifact IDs, or sealed DREAMS reports.
  3. Report Tagging: Emits annotated Git tags when reports are sealed.
  4. Non-Intrusive Fallback: Operates cleanly with graceful degradation if Git
     is not yet initialized or unavailable.
================================================================================
"""

import os
import subprocess
import datetime
from typing import Dict, Any, List, Optional


class GitController:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = os.path.abspath(base_dir)

    def _run_git(self, args: List[str]) -> subprocess.CompletedProcess:
        """Helper to run git commands in the base directory."""
        return subprocess.run(
            ["git"] + args,
            cwd=self.base_dir,
            capture_output=True,
            text=True
        )

    def is_git_repo(self) -> bool:
        """Checks if base_dir is inside an active git repository."""
        proc = self._run_git(["rev-parse", "--is-inside-work-tree"])
        return proc.returncode == 0 and proc.stdout.strip() == "true"

    def get_status(self) -> Dict[str, Any]:
        """
        Retrieves current git repository state for scientific audit trails.
        """
        if not self.is_git_repo():
            return {
                "is_git_repo": False,
                "commit_hash": None,
                "short_hash": None,
                "branch": None,
                "is_dirty": False,
                "modified_files": [],
                "untracked_files": [],
                "remote_origin": None,
                "reproducibility_warning": "Not a Git repository. Run 'git init' to enable full versioned provenance."
            }

        # Current commit hash
        hash_proc = self._run_git(["rev-parse", "HEAD"])
        commit_hash = hash_proc.stdout.strip() if hash_proc.returncode == 0 else None
        short_hash = commit_hash[:8] if commit_hash else None

        # Current branch
        branch_proc = self._run_git(["branch", "--show-current"])
        branch = branch_proc.stdout.strip() if branch_proc.returncode == 0 else None
        if not branch and commit_hash:
            branch = "HEAD (detached)"

        # Remote origin URL
        remote_proc = self._run_git(["remote", "get-url", "origin"])
        remote_origin = remote_proc.stdout.strip() if remote_proc.returncode == 0 else None

        # Porcelain status for dirty check
        status_proc = self._run_git(["status", "--porcelain"])
        modified_files = []
        untracked_files = []
        if status_proc.returncode == 0 and status_proc.stdout:
            for line in status_proc.stdout.strip().splitlines():
                if not line:
                    continue
                code = line[:2]
                path = line[3:].strip()
                if "??" in code:
                    untracked_files.append(path)
                else:
                    modified_files.append(path)

        is_dirty = len(modified_files) > 0 or len(untracked_files) > 0
        warning = None
        if is_dirty:
            warning = f"Working tree is dirty ({len(modified_files)} modified, {len(untracked_files)} untracked). Code state is not strictly frozen."

        return {
            "is_git_repo": True,
            "commit_hash": commit_hash,
            "short_hash": short_hash,
            "branch": branch,
            "is_dirty": is_dirty,
            "modified_files": modified_files,
            "untracked_files": untracked_files,
            "remote_origin": remote_origin,
            "reproducibility_warning": warning,
            "isError": False
        }

    def create_snapshot(
        self,
        message: str,
        run_id: Optional[str] = None,
        artifact_id: Optional[str] = None,
        report_title: Optional[str] = None,
        tag_report: bool = False,
        push: bool = False
    ) -> Dict[str, Any]:
        """
        Creates an atomic Git commit snapshot linking the workspace state
        to active scientific operations (Run IDs, Artifact IDs, sealed Reports).
        """
        if not self.is_git_repo():
            return {
                "error": "Cannot create Git snapshot: directory is not a Git repository.",
                "isError": True
            }

        # Stage files (excluding gitignore)
        add_proc = self._run_git(["add", "."])
        if add_proc.returncode != 0:
            return {
                "error": f"Failed to stage changes: {add_proc.stderr}",
                "isError": True
            }

        # Check if there is anything to commit
        status_proc = self._run_git(["status", "--porcelain"])
        if not status_proc.stdout.strip():
            status = self.get_status()
            return {
                "status": "NO_CHANGES",
                "message": "Working tree already clean; snapshot matches current HEAD.",
                "commit_hash": status.get("commit_hash"),
                "short_hash": status.get("short_hash"),
                "branch": status.get("branch"),
                "isError": False
            }

        # Construct structured scientific commit message
        lines = [f"sci: {message}", ""]
        if run_id:
            lines.append(f"SciResearch-Run: {run_id}")
        if artifact_id:
            lines.append(f"SciResearch-Artifact: {artifact_id}")
        if report_title:
            lines.append(f"SciResearch-Report: {report_title}")
        lines.append(f"SciResearch-Date: {datetime.datetime.now(datetime.timezone.utc).isoformat()}")

        commit_msg = "\n".join(lines)
        commit_proc = self._run_git(["commit", "-m", commit_msg])
        if commit_proc.returncode != 0:
            return {
                "error": f"Git commit failed: {commit_proc.stderr}",
                "isError": True
            }

        # Get updated commit info
        status = self.get_status()
        created_tag = None

        # Tag report if requested
        if tag_report and report_title:
            clean_tag = f"report-{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            tag_proc = self._run_git(["tag", "-a", clean_tag, "-m", f"Verified Report: {report_title}"])
            if tag_proc.returncode == 0:
                created_tag = clean_tag

        push_result = None
        if push and status.get("branch") and status.get("remote_origin"):
            push_proc = self._run_git(["push", "origin", status["branch"]])
            push_result = {
                "pushed": push_proc.returncode == 0,
                "stdout": push_proc.stdout.strip(),
                "stderr": push_proc.stderr.strip()
            }

        return {
            "status": "SNAPSHOT_RECORDED",
            "commit_hash": status.get("commit_hash"),
            "short_hash": status.get("short_hash"),
            "branch": status.get("branch"),
            "tag": created_tag,
            "push_result": push_result,
            "message": message,
            "isError": False
        }

    def verify_reproducibility(self, target_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Evaluates whether a simulation setup is strictly reproducible from Git.
        """
        status = self.get_status()
        if not status.get("is_git_repo"):
            return {
                "reproducible": False,
                "score": 0.0,
                "reason": "Not under Git version control. Input files and scripts cannot be validated against a fixed commit SHA.",
                "isError": False
            }

        if status.get("is_dirty"):
            if target_files:
                modified_targets = [f for f in target_files if f in status.get("modified_files", []) or f in status.get("untracked_files", [])]
                if modified_targets:
                    return {
                        "reproducible": False,
                        "score": 0.5,
                        "reason": f"Target files have uncommitted modifications: {', '.join(modified_targets)}",
                        "commit_hash": status.get("commit_hash"),
                        "isError": False
                    }
            return {
                "reproducible": False,
                "score": 0.7,
                "reason": "Repository has uncommitted modifications, though specific targets may be clean.",
                "commit_hash": status.get("commit_hash"),
                "isError": False
            }

        return {
            "reproducible": True,
            "score": 1.0,
            "reason": f"Repository is clean at commit {status.get('short_hash')}. Complete code and input state can be reconstructed perfectly.",
            "commit_hash": status.get("commit_hash"),
            "short_hash": status.get("short_hash"),
            "branch": status.get("branch"),
            "isError": False
        }
