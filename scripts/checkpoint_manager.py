#!/usr/bin/env python3
"""
================================================================================
MDCrow Checkpoint-Based Memory & Session Resumption Manager
================================================================================
Implements unique checkpoint directories linked to a Run ID, allowing
researchers to step away during long simulations, return in later sessions,
reload summaries, and continue or troubleshoot without repeating setup.
================================================================================
"""

import os
import sys
import json
import datetime
from typing import Dict, Any, List, Optional

try:
    from git_controller import GitController
except ImportError:
    from scripts.git_controller import GitController


class CheckpointManager:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.git = GitController(self.base_dir)
        self.runs_dir = os.path.join(self.base_dir, "runs")
        self.checkpoints_dir = os.path.join(self.base_dir, "checkpoints")
        self.index_path = os.path.join(self.checkpoints_dir, "index.json")

        os.makedirs(self.runs_dir, exist_ok=True)
        os.makedirs(self.checkpoints_dir, exist_ok=True)
        self._init_index()

    def _init_index(self):
        if not os.path.exists(self.index_path):
            with open(self.index_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

    def _load_index(self) -> Dict[str, Any]:
        with open(self.index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_index(self, data: Dict[str, Any]):
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def generate_run_id(self, prefix: str = "run") -> str:
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{now_str}"

    def save_run(
        self,
        run_id: str,
        prompt_summary: str,
        agent_trace: Optional[List[Dict[str, Any]]] = None,
        parameter_registry: Optional[Dict[str, Any]] = None,
        file_paths: Optional[Dict[str, str]] = None,
        figures: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        status: str = "RUNNING"
    ) -> Dict[str, Any]:
        """
        Saves or updates a simulation run checkpoint and its dedicated run directory.
        """
        run_folder = os.path.join(self.runs_dir, run_id)
        os.makedirs(run_folder, exist_ok=True)

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        checkpoint_path = os.path.join(self.checkpoints_dir, f"{run_id}.json")

        existing_data = {}
        if os.path.exists(checkpoint_path):
            try:
                with open(checkpoint_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except Exception:
                existing_data = {}

        updated_trace = agent_trace if agent_trace is not None else existing_data.get("agent_trace", [])
        updated_params = parameter_registry if parameter_registry is not None else existing_data.get("parameter_registry", {})
        updated_files = file_paths if file_paths is not None else existing_data.get("file_paths", {})
        updated_figures = figures if figures is not None else existing_data.get("figures", [])
        updated_metrics = metrics if metrics is not None else existing_data.get("metrics", {})

        git_state = self.git.get_status()
        checkpoint_data = {
            "run_id": run_id,
            "prompt_summary": prompt_summary or existing_data.get("prompt_summary", ""),
            "status": status,
            "run_directory": run_folder,
            "created_at": existing_data.get("created_at", now_iso),
            "updated_at": now_iso,
            "agent_trace": updated_trace,
            "parameter_registry": updated_params,
            "file_paths": updated_files,
            "figures": updated_figures,
            "metrics": updated_metrics,
            "git": {
                "commit": git_state.get("commit_hash"),
                "short_commit": git_state.get("short_hash"),
                "branch": git_state.get("branch"),
                "is_dirty": git_state.get("is_dirty")
            }
        }

        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, indent=2)

        # Update index
        index = self._load_index()
        index[run_id] = {
            "run_id": run_id,
            "prompt_summary": prompt_summary[:120],
            "status": status,
            "updated_at": now_iso,
            "metrics": updated_metrics,
            "git_commit": git_state.get("short_hash")
        }
        self._save_index(index)

        return {
            "status": "SAVED",
            "run_id": run_id,
            "checkpoint_path": checkpoint_path,
            "run_directory": run_folder,
            "isError": False
        }

    def resume_run(self, run_id: str) -> Dict[str, Any]:
        """
        Reloads memory summaries, trace, parameter registry, and files for an interrupted or completed run.
        """
        checkpoint_path = os.path.join(self.checkpoints_dir, f"{run_id}.json")
        if not os.path.exists(checkpoint_path):
            return {
                "error": f"Checkpoint for Run ID '{run_id}' not found.",
                "isError": True
            }

        with open(checkpoint_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "status": "RESUMED",
            "run_id": run_id,
            "checkpoint": data,
            "isError": False
        }

    def list_runs(self, status_filter: Optional[str] = None, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lists all runs with optional status and text search filtering.
        """
        index = self._load_index()
        runs = list(index.values())

        if status_filter:
            runs = [r for r in runs if r.get("status", "").upper() == status_filter.upper()]

        if query:
            q_lower = query.lower()
            runs = [
                r for r in runs
                if q_lower in r.get("run_id", "").lower() or q_lower in r.get("prompt_summary", "").lower()
            ]

        # Sort by updated_at descending
        runs.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return runs

    def append_trace_step(self, run_id: str, step_name: str, details: str, status: str = "IN_PROGRESS") -> Dict[str, Any]:
        """
        Appends a discrete milestone or action to the agent trace.
        """
        chk = self.resume_run(run_id)
        if chk.get("isError"):
            return chk

        data = chk["checkpoint"]
        trace = data.get("agent_trace", [])
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        trace.append({
            "step": step_name,
            "details": details,
            "status": status,
            "timestamp": now_iso
        })
        return self.save_run(
            run_id=run_id,
            prompt_summary=data.get("prompt_summary", ""),
            agent_trace=trace,
            status=status if status in ["CONVERGED", "FAILED", "ABORTED"] else data.get("status", "RUNNING")
        )
