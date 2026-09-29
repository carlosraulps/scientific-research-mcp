#!/usr/bin/env python3
"""
================================================================================
DREAMS Canvas & Append-Only Provenance Registry
================================================================================
Implements persistent shared memory across 3 specialized stores:
  1. Notes: Free-form version-controlled markdown notes with reference checks.
  2. Artifacts: Append-only registry of tool outputs with 8-character hash IDs,
     per-parameter rationales, sources, declared context, and DAG tracking.
  3. Reports: Structured scientific deliverables audited against the provenance
     DAG and sealed as immutable upon verification.
================================================================================
"""

import os
import sys
import json
import hashlib
import datetime
from typing import Dict, Any, List, Optional, Tuple

try:
    from git_controller import GitController
except ImportError:
    from scripts.git_controller import GitController


class CanvasStore:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.git = GitController(self.base_dir)
        self.canvas_dir = os.path.join(self.base_dir, "canvas")
        self.notes_dir = os.path.join(self.canvas_dir, "notes")
        self.artifacts_dir = os.path.join(self.canvas_dir, "artifacts")
        self.reports_dir = os.path.join(self.canvas_dir, "reports")
        self.logs_dir = os.path.join(self.base_dir, "logs")

        os.makedirs(self.notes_dir, exist_ok=True)
        os.makedirs(self.artifacts_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

        self.artifacts_registry_path = os.path.join(self.logs_dir, "artifacts_registry.json")
        self.notes_index_path = os.path.join(self.logs_dir, "notes_index.json")
        self.reports_index_path = os.path.join(self.logs_dir, "reports_index.json")

        self._init_registry()

    def _init_registry(self):
        if not os.path.exists(self.artifacts_registry_path):
            with open(self.artifacts_registry_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)
        if not os.path.exists(self.notes_index_path):
            with open(self.notes_index_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)
        if not os.path.exists(self.reports_index_path):
            with open(self.reports_index_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

    def _load_artifacts(self) -> Dict[str, Any]:
        with open(self.artifacts_registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_artifacts(self, data: Dict[str, Any]):
        with open(self.artifacts_registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load_notes_index(self) -> Dict[str, Any]:
        with open(self.notes_index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_notes_index(self, data: Dict[str, Any]):
        with open(self.notes_index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _load_reports_index(self) -> Dict[str, Any]:
        with open(self.reports_index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_reports_index(self, data: Dict[str, Any]):
        with open(self.reports_index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # -------------------------------------------------------------------------
    # 1. ARTIFACTS & PROVENANCE REGISTRY (DREAMS Specification)
    # -------------------------------------------------------------------------
    def register_artifact(
        self,
        producing_tool: str,
        value: Any,
        arguments: Dict[str, Any],
        rationales: Dict[str, str],
        sources: Dict[str, str],
        declared_context: str,
        sensitive_params: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Registers an immutable tool output artifact with anti-laundering verification.
        Returns the registered artifact dictionary including its 8-character result_id.
        """
        if not declared_context or len(declared_context.strip()) < 10:
            return {
                "error": "Anti-Laundering Violation: declared_context must be a descriptive statement (>= 10 chars) explaining the study.",
                "isError": True
            }

        if sensitive_params is None:
            sensitive_params = ["ecutwfc", "encut", "kpoints", "kspacing", "smearing", "degauss", "functional", "u_params"]

        artifacts = self._load_artifacts()

        # Check sources existence
        for param, src_id in sources.items():
            clean_src_id = src_id.split(".")[0]
            if clean_src_id not in artifacts:
                return {
                    "error": f"Anti-Laundering Violation: Sourced parameter '{param}' references unknown artifact ID '{src_id}'.",
                    "isError": True
                }

        # Check sensitive parameter sourcing rule (Rule R1)
        for sp in sensitive_params:
            if sp in arguments:
                has_src = sp in sources and sources[sp]
                has_rat = sp in rationales and len(rationales[sp].strip()) > 5
                if not has_src and not has_rat:
                    return {
                        "error": f"Anti-Laundering Violation (Rule R1): Sensitive parameter '{sp}' lacks a verified source and rationale.",
                        "isError": True
                    }

        # Anti-trivial math / identity check
        if producing_tool in ["math_eval", "calculator"]:
            expr = str(arguments.get("expression", "")).replace(" ", "")
            if any(id_pattern in expr for id_pattern in ["*1.0", "*1", "+0", "-0", "/1.0", "/1"]):
                return {
                    "error": f"Anti-Laundering Violation: Trivial identity expression '{expr}' detected to manufacture artificial provenance.",
                    "isError": True
                }

        # Generate deterministic 8-character ID
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        hasher = hashlib.sha256()
        hasher.update(producing_tool.encode("utf-8"))
        hasher.update(json.dumps(arguments, sort_keys=True).encode("utf-8"))
        hasher.update(json.dumps(value, sort_keys=True, default=str).encode("utf-8"))
        hasher.update(declared_context.encode("utf-8"))
        hasher.update(now_iso.encode("utf-8"))
        result_id = hasher.hexdigest()[:8]

        parent_ids = list(set([src_id.split(".")[0] for src_id in sources.values() if src_id]))

        git_state = self.git.get_status()
        artifact_data = {
            "result_id": result_id,
            "producing_tool": producing_tool,
            "value": value,
            "arguments": arguments,
            "rationales": rationales,
            "sources": sources,
            "declared_context": declared_context,
            "parent_ids": parent_ids,
            "created_at": now_iso,
            "git": {
                "commit": git_state.get("commit_hash"),
                "short_commit": git_state.get("short_hash"),
                "branch": git_state.get("branch"),
                "is_dirty": git_state.get("is_dirty")
            }
        }

        # Save individual file & update registry
        artifact_file = os.path.join(self.artifacts_dir, f"{result_id}.json")
        with open(artifact_file, "w", encoding="utf-8") as f:
            json.dump(artifact_data, f, indent=2)

        artifacts[result_id] = artifact_data
        self._save_artifacts(artifacts)

        return {
            "status": "REGISTERED",
            "result_id": result_id,
            "artifact": artifact_data,
            "isError": False
        }

    def audit_provenance_chain(self, result_id: str) -> Dict[str, Any]:
        """
        Traverses upstream DAG dependencies to produce an auditable provenance tree.
        """
        artifacts = self._load_artifacts()
        clean_id = result_id.split(".")[0]

        if clean_id not in artifacts:
            return {"error": f"Artifact ID '{clean_id}' not found in provenance registry.", "isError": True}

        visited = set()
        chain = []
        queue = [clean_id]

        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)

            art = artifacts.get(curr)
            if art:
                chain.append({
                    "result_id": curr,
                    "producing_tool": art.get("producing_tool"),
                    "value": art.get("value"),
                    "declared_context": art.get("declared_context"),
                    "parents": art.get("parent_ids", []),
                    "created_at": art.get("created_at")
                })
                for pid in art.get("parent_ids", []):
                    if pid not in visited:
                        queue.append(pid)

        return {
            "target_id": clean_id,
            "total_ancestors": len(chain) - 1,
            "verified": True,
            "provenance_chain": chain,
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 2. NOTES STORE (Version-Controlled & Append-Only)
    # -------------------------------------------------------------------------
    def write_note(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        references: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Creates or updates a version-controlled, append-only working note.
        Validates that all cited references exist in the artifact registry.
        """
        artifacts = self._load_artifacts()
        if references:
            for ref in references:
                clean_ref = ref.split(".")[0]
                if clean_ref not in artifacts:
                    return {
                        "error": f"Note Rejected: Cited reference '{ref}' does not exist in Artifact Registry.",
                        "isError": True
                    }

        index = self._load_notes_index()
        safe_key = "".join([c if c.isalnum() or c in "-_" else "_" for c in title.lower()]).strip("_")
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if safe_key not in index:
            version = 1
            history = []
        else:
            version = index[safe_key]["current_version"] + 1
            history = index[safe_key].get("history", [])

        note_filename = f"{safe_key}_v{version}.md"
        note_filepath = os.path.join(self.notes_dir, note_filename)

        header = f"---\ntitle: \"{title}\"\nversion: {version}\ncreated_at: \"{now_iso}\"\ntags: {json.dumps(tags or [])}\nreferences: {json.dumps(references or [])}\n---\n\n"
        full_content = header + content

        with open(note_filepath, "w", encoding="utf-8") as f:
            f.write(full_content)

        history.append({
            "version": version,
            "file": note_filename,
            "timestamp": now_iso
        })

        index[safe_key] = {
            "key": safe_key,
            "title": title,
            "current_version": version,
            "current_file": note_filename,
            "tags": tags or [],
            "references": references or [],
            "updated_at": now_iso,
            "history": history
        }
        self._save_notes_index(index)

        return {
            "status": "WRITTEN",
            "key": safe_key,
            "version": version,
            "file_path": note_filepath,
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 3. REPORTS STORE (Audited & Immutable)
    # -------------------------------------------------------------------------
    def create_report(
        self,
        title: str,
        objective: str,
        executive_summary: str,
        findings: List[Dict[str, Any]],
        claims_with_provenance: List[Dict[str, str]],
        author: str = "Scientific Research Agent"
    ) -> Dict[str, Any]:
        """
        Creates an immutable scientific report after auditing all claims against the provenance DAG.
        """
        artifacts = self._load_artifacts()
        reports_index = self._load_reports_index()

        # Audit every claim
        audited_claims = []
        for claim in claims_with_provenance:
            claim_text = claim.get("claim", "")
            src_id = claim.get("artifact_id", "").split(".")[0]

            if not src_id or src_id not in artifacts:
                return {
                    "error": f"Report Audit Failed: Claim '{claim_text}' cites unknown or missing artifact ID '{src_id}'.",
                    "isError": True
                }

            audit_res = self.audit_provenance_chain(src_id)
            audited_claims.append({
                "claim": claim_text,
                "artifact_id": src_id,
                "verified_ancestor_count": audit_res.get("total_ancestors", 0),
                "producing_tool": artifacts[src_id].get("producing_tool")
            })

        safe_key = "".join([c if c.isalnum() or c in "-_" else "_" for c in title.lower()]).strip("_")
        if safe_key in reports_index:
            return {
                "error": f"Report Immutability Violation: Report '{safe_key}' is already verified and sealed. Immutable reports cannot be overwritten.",
                "isError": True
            }

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        git_state = self.git.get_status()
        git_commit_str = f"`{git_state.get('short_hash')}` ({git_state.get('branch')})" if git_state.get("commit_hash") else "None (Untracked)"
        git_repro = "CLEAN / REPRODUCIBLE" if not git_state.get("is_dirty") else "DIRTY / UNCOMMITTED CHANGES"

        report_filename = f"{safe_key}.md"
        report_filepath = os.path.join(self.reports_dir, report_filename)

        report_md = f"""# {title}
**Status**: VERIFIED & SEALED IMMUTABLE
**Author**: {author}
**Date**: {now_iso}
**Git Commit**: {git_commit_str}
**Reproducibility**: {git_repro}
**Objective**: {objective}

---

## Executive Summary
{executive_summary}

---

## Verified Claims & Provenance Audit
| Claim | Artifact ID | Producing Tool | Verified Ancestors |
| :--- | :--- | :--- | :--- |
"""
        for ac in audited_claims:
            report_md += f"| {ac['claim']} | `{ac['artifact_id']}` | `{ac['producing_tool']}` | {ac['verified_ancestor_count']} |\n"

        report_md += "\n---\n\n## Scientific Findings & Numerical Data\n"
        for idx, f in enumerate(findings, 1):
            report_md += f"### Finding {idx}: {f.get('title', 'Observation')}\n"
            report_md += f"{f.get('description', '')}\n\n"
            if "data" in f:
                report_md += f"```json\n{json.dumps(f['data'], indent=2)}\n```\n\n"

        with open(report_filepath, "w", encoding="utf-8") as f:
            f.write(report_md)

        reports_index[safe_key] = {
            "key": safe_key,
            "title": title,
            "file": report_filename,
            "created_at": now_iso,
            "claim_count": len(audited_claims),
            "sealed": True,
            "git": {
                "commit": git_state.get("commit_hash"),
                "short_commit": git_state.get("short_hash"),
                "branch": git_state.get("branch"),
                "is_dirty": git_state.get("is_dirty")
            }
        }
        self._save_reports_index(reports_index)

        return {
            "status": "SEALED_IMMUTABLE",
            "key": safe_key,
            "report_path": report_filepath,
            "claims_verified": len(audited_claims),
            "git": git_state,
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 4. INSPECTION & READING PRIMITIVES
    # -------------------------------------------------------------------------
    def inspect(self, store: str = "all") -> Dict[str, Any]:
        """
        Lists available keys and metadata across canvas stores.
        """
        res = {}
        if store in ["all", "artifacts"]:
            artifacts = self._load_artifacts()
            res["artifacts"] = [
                {"id": k, "tool": v.get("producing_tool"), "context": v.get("declared_context", "")[:60]}
                for k, v in artifacts.items()
            ]
        if store in ["all", "notes"]:
            notes = self._load_notes_index()
            res["notes"] = [
                {"key": k, "title": v.get("title"), "version": v.get("current_version")}
                for k, v in notes.items()
            ]
        if store in ["all", "reports"]:
            reports = self._load_reports_index()
            res["reports"] = [
                {"key": k, "title": v.get("title"), "claims": v.get("claim_count")}
                for k, v in reports.items()
            ]
        return res

    def read(self, store: str, key_or_id: str) -> Dict[str, Any]:
        """
        Reads a specific item from notes, artifacts, or reports.
        """
        clean_key = key_or_id.split(".")[0]
        if store == "artifacts":
            artifacts = self._load_artifacts()
            if clean_key in artifacts:
                return {"store": "artifacts", "key": clean_key, "data": artifacts[clean_key], "isError": False}
            return {"error": f"Artifact '{clean_key}' not found in registry.", "isError": True}

        elif store == "notes":
            notes = self._load_notes_index()
            if clean_key in notes:
                fp = os.path.join(self.notes_dir, notes[clean_key]["current_file"])
                if os.path.exists(fp):
                    with open(fp, "r", encoding="utf-8") as f:
                        return {"store": "notes", "key": clean_key, "content": f.read(), "isError": False}
            return {"error": f"Note '{clean_key}' not found.", "isError": True}

        elif store == "reports":
            reports = self._load_reports_index()
            if clean_key in reports:
                fp = os.path.join(self.reports_dir, reports[clean_key]["file"])
                if os.path.exists(fp):
                    with open(fp, "r", encoding="utf-8") as f:
                        return {"store": "reports", "key": clean_key, "content": f.read(), "isError": False}
            return {"error": f"Report '{clean_key}' not found.", "isError": True}

        return {"error": f"Unknown store '{store}'. Choose 'notes', 'artifacts', or 'reports'.", "isError": True}
