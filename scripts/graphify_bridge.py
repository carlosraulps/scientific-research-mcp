#!/usr/bin/env python3
"""
================================================================================
Graphify Seamless Knowledge Graph Synchronization Bridge
================================================================================
Bridges the Scientific Research Log (Canvas Notes, Artifacts, Reports,
Checkpoints, and Decisions) with the system's Graphify knowledge engine.
Generates interconnected Markdown documents with typed wikilinks and invokes
`graphify update .` to keep graphify-out/graph.json continuously synchronized.
================================================================================
"""

import os
import sys
import json
import subprocess
import glob
from typing import Dict, Any, List, Optional


class GraphifyBridge:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.docs_dir = os.path.join(self.base_dir, "docs")
        self.canvas_dir = os.path.join(self.base_dir, "canvas")
        self.checkpoints_dir = os.path.join(self.base_dir, "checkpoints")
        self.logs_dir = os.path.join(self.base_dir, "logs")
        self.graphify_out = os.path.join(self.base_dir, "graphify-out")

        os.makedirs(self.docs_dir, exist_ok=True)

    def generate_knowledge_map(self) -> str:
        """
        Creates an interconnected Markdown summary linking all Notes, Reports,
        Checkpoints, and Decisions to enable Graphify to construct rich semantic graphs.
        """
        map_path = os.path.join(self.docs_dir, "KNOWLEDGE_MAP.md")

        # Gather notes
        notes_index_path = os.path.join(self.logs_dir, "notes_index.json")
        notes = {}
        if os.path.exists(notes_index_path):
            with open(notes_index_path, "r", encoding="utf-8") as f:
                notes = json.load(f)

        # Gather reports
        reports_index_path = os.path.join(self.logs_dir, "reports_index.json")
        reports = {}
        if os.path.exists(reports_index_path):
            with open(reports_index_path, "r", encoding="utf-8") as f:
                reports = json.load(f)

        # Gather checkpoints
        checkpoints_index_path = os.path.join(self.checkpoints_dir, "index.json")
        checkpoints = {}
        if os.path.exists(checkpoints_index_path):
            with open(checkpoints_index_path, "r", encoding="utf-8") as f:
                checkpoints = json.load(f)

        # Gather artifacts
        artifacts_path = os.path.join(self.logs_dir, "artifacts_registry.json")
        artifacts = {}
        if os.path.exists(artifacts_path):
            with open(artifacts_path, "r", encoding="utf-8") as f:
                artifacts = json.load(f)

        content = f"""# Scientific Research Knowledge Map
*Auto-generated bridge document for Graphify indexing and cross-linking.*

## 1. DREAMS Shared Canvas Reports (Immutable Verified Deliverables)
"""
        if reports:
            for k, r in reports.items():
                content += f"- **[{r.get('title', k)}](file://{os.path.join(self.canvas_dir, 'reports', r.get('file', ''))})**: {r.get('claim_count', 0)} verified claims (Sealed: `{r.get('sealed', True)}`)\n"
        else:
            content += "- *No reports registered yet.*\n"

        content += "\n## 2. Canvas Working Notes (Version-Controlled & Append-Only)\n"
        if notes:
            for k, n in notes.items():
                content += f"- **[{n.get('title', k)}](file://{os.path.join(self.canvas_dir, 'notes', n.get('current_file', ''))})** (v{n.get('current_version')}) - Tags: `{', '.join(n.get('tags', []))}`\n"
        else:
            content += "- *No notes registered yet.*\n"

        content += "\n## 3. MDCrow Simulation Checkpoints (Resumable Runs)\n"
        if checkpoints:
            for k, c in checkpoints.items():
                content += f"- **Run `{c.get('run_id')}`** [{c.get('status')}]: {c.get('prompt_summary', '')} - Updated: `{c.get('updated_at')}`\n"
        else:
            content += "- *No checkpoints registered yet.*\n"

        content += f"\n## 4. Append-Only Provenance Registry Stats\n"
        content += f"- **Total Registered Artifacts**: {len(artifacts)}\n"
        content += f"- **Audit Log**: [`decisions.csv`](file://{os.path.join(self.logs_dir, 'decisions.csv')})\n"
        content += f"- **Evidence Store**: [`EVIDENCE.md`](file://{os.path.join(self.base_dir, 'EVIDENCE.md')})\n"
        content += f"- **Operational Protocol**: [`CLAUDE.md`](file://{os.path.join(self.base_dir, 'CLAUDE.md')})\n"
        content += f"- **Active Execution Tracking**: [`TASK.md`](file://{os.path.join(self.base_dir, 'TASK.md')})\n"

        with open(map_path, "w", encoding="utf-8") as f:
            f.write(content)

        return map_path

    def sync_graphify(self) -> Dict[str, Any]:
        """
        Regenerates knowledge documents and runs `graphify update .`
        """
        map_path = self.generate_knowledge_map()

        graphify_bin = "/home/cr/.local/bin/graphify"
        if not os.path.exists(graphify_bin):
            return {
                "error": "graphify binary not found at /home/cr/.local/bin/graphify",
                "isError": True
            }

        try:
            # Run graphify update (AST-only, no API cost)
            res = subprocess.run(
                [graphify_bin, "update", "."],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            stdout = res.stdout
            stderr = res.stderr
            return {
                "status": "SYNCED",
                "knowledge_map": map_path,
                "graphify_stdout": stdout.strip(),
                "graphify_stderr": stderr.strip(),
                "graph_json_exists": os.path.exists(os.path.join(self.graphify_out, "graph.json")),
                "isError": res.returncode != 0
            }
        except Exception as e:
            return {
                "error": f"Failed to execute graphify update: {str(e)}",
                "isError": True
            }
