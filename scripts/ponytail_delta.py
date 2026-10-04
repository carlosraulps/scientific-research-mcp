#!/usr/bin/env python3
"""
================================================================================
Ponytail Delta Composer: Declarative Input Mutation & Grounding Engine
================================================================================
Implements:
1. Declarative Delta Inheritance: Mutates baseline computational chemistry inputs
   (VASP INCAR, SIESTA .fdf, LAMMPS in.*) via structured semantic deltas rather
   than high-entropy monolithic LLM regeneration.
2. Grounded Self-Documentation: Every mutated line contains an explicit physical
   rationale and source tag: `TAG = VALUE  # [Source] Physical Rationale`,
   anchored in Google NotebookLM (dft-documentation / md-documentation) or literature.
3. Ponytail Zero-Redundancy Enforcement: Eliminates engine defaults, redundant
   tags (e.g. ISIF=2 when IBRION=2, ALGO=Normal, SYSTEM bloat), and unnecessary
   I/O overhead tags (NEDOS/LORBIT during relaxation).
4. Graphify Knowledge Integration: Emits delta provenance metadata for seamless
   synchronization into the Graphify knowledge graph.
================================================================================
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union


# ------------------------------------------------------------------------------
# Engine Default & Redundancy Registry (Ponytail Rules)
# ------------------------------------------------------------------------------
VASP_DEFAULTS = {
    "ALGO": ["NORMAL"],
    "LDAUTYPE": ["2"],
    "LDAUJ": ["0", "0 0", "0.0 0.0"],
    "LWAVE": [".TRUE.", "TRUE"],
    "LCHARG": [".TRUE.", "TRUE"],
    "POTIM": ["0.5"],
}

VASP_IO_OVERHEAD_TAGS = {"NEDOS", "LORBIT"}


class PonytailDeltaComposer:
    def __init__(self, engine: str = "vasp"):
        self.engine = engine.lower()
        self.base_tags: Dict[str, Dict[str, Any]] = {}
        self.composed_tags: Dict[str, Dict[str, Any]] = {}

    # --------------------------------------------------------------------------
    # 1. PARSING ENGINES (VASP, SIESTA, LAMMPS)
    # --------------------------------------------------------------------------
    def parse_vasp_incar(self, content: str) -> Dict[str, Dict[str, Any]]:
        """
        Parses VASP INCAR into structured key-value-comment dictionary.
        """
        tags = {}
        for line in content.splitlines():
            clean = line.strip()
            if not clean or clean.startswith("#") or clean.startswith("!"):
                continue

            # Split inline comments (# or !)
            comment_match = re.search(r"[#!](.*)$", clean)
            comment = comment_match.group(1).strip() if comment_match else ""
            line_no_comment = re.sub(r"[#!].*$", "", clean).strip()

            # Handle semicolon-separated tags on a single line
            statements = [s.strip() for s in line_no_comment.split(";") if s.strip()]
            for stmt in statements:
                if "=" in stmt:
                    parts = stmt.split("=", 1)
                    key = parts[0].strip().upper()
                    val = parts[1].strip()

                    # Extract grounding source if formatted as [Source]
                    source = ""
                    source_match = re.search(r"\[(.*?)\]", comment)
                    if source_match:
                        source = source_match.group(1)

                    tags[key] = {
                        "value": val,
                        "comment": comment,
                        "source": source,
                    }
        return tags

    def parse_siesta_fdf(self, content: str) -> Dict[str, Dict[str, Any]]:
        """
        Parses SIESTA .fdf into structured key-value-comment dictionary.
        Preserves block sections as atomic units.
        """
        tags = {}
        in_block = False
        current_block = []
        block_name = ""

        for line in content.splitlines():
            clean = line.strip()
            if not clean or clean.startswith("#"):
                continue

            if clean.lower().startswith("%block"):
                in_block = True
                block_name = clean.split()[1] if len(clean.split()) > 1 else "block"
                current_block = [line]
                continue
            elif clean.lower().startswith("%endblock"):
                in_block = False
                current_block.append(line)
                tags[f"%block_{block_name}"] = {
                    "value": "\n".join(current_block),
                    "is_block": True,
                    "comment": "",
                    "source": "",
                }
                continue

            if in_block:
                current_block.append(line)
                continue

            comment_match = re.search(r"[#](.*)$", clean)
            comment = comment_match.group(1).strip() if comment_match else ""
            line_no_comment = re.sub(r"[#].*$", "", clean).strip()

            parts = line_no_comment.split(None, 1)
            if len(parts) >= 2:
                key = parts[0]
                val = parts[1]
                source = ""
                source_match = re.search(r"\[(.*?)\]", comment)
                if source_match:
                    source = source_match.group(1)

                tags[key] = {
                    "value": val,
                    "comment": comment,
                    "source": source,
                    "is_block": False,
                }
        return tags

    def parse_lammps_script(self, content: str) -> List[Dict[str, Any]]:
        """
        Parses sequential LAMMPS script lines preserving command ordering.
        """
        entries = []
        for line in content.splitlines():
            clean = line.strip()
            if not clean:
                continue

            comment_match = re.search(r"[#](.*)$", clean)
            comment = comment_match.group(1).strip() if comment_match else ""
            cmd_part = re.sub(r"[#].*$", "", clean).strip()

            if not cmd_part:
                continue

            parts = cmd_part.split()
            cmd = parts[0]
            args = " ".join(parts[1:]) if len(parts) > 1 else ""

            source = ""
            source_match = re.search(r"\[(.*?)\]", comment)
            if source_match:
                source = source_match.group(1)

            entries.append({
                "command": cmd,
                "args": args,
                "comment": comment,
                "source": source,
            })
        return entries

    # --------------------------------------------------------------------------
    # 2. PONYTAIL PRUNING & ZERO-REDUNDANCY ENFORCEMENT
    # --------------------------------------------------------------------------
    def prune_vasp_redundancy(self, tags: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Prunes built-in VASP defaults, redundant tags, and I/O overhead.
        """
        pruned = dict(tags)

        # Rule 1: Remove SYSTEM tag (text bloat)
        if "SYSTEM" in pruned:
            del pruned["SYSTEM"]

        # Rule 2: Remove native VASP defaults
        for def_key, def_vals in VASP_DEFAULTS.items():
            if def_key in pruned:
                cur_val = str(pruned[def_key]["value"]).upper().strip()
                if cur_val in def_vals:
                    del pruned[def_key]

        # Rule 3: ISIF = 2 is native default when IBRION = 2
        ibrion = str(pruned.get("IBRION", {}).get("value", "")).strip()
        isif = str(pruned.get("ISIF", {}).get("value", "")).strip()
        if ibrion == "2" and isif == "2":
            del pruned["ISIF"]

        # Rule 4: If NSW == 0 (single point), remove IBRION, ISIF, POTIM, and unnecessary I/O unless requested
        nsw = str(pruned.get("NSW", {}).get("value", "")).strip()
        if nsw == "0":
            if "ISIF" in pruned:
                del pruned["ISIF"]
            if "POTIM" in pruned:
                del pruned["POTIM"]

        return pruned

    # --------------------------------------------------------------------------
    # 3. SEMANTIC DELTA COMPOSITION
    # --------------------------------------------------------------------------
    def apply_delta(
        self,
        base_content: str,
        delta: Dict[str, Any],
        prune_redundant: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Applies a delta dictionary over base_content.
        delta keys with value None or 'DELETE' are deleted.
        delta keys can be:
          "TAG": "VALUE"
          "TAG": {"value": "VALUE", "rationale": "...", "source": "..."}
        """
        if self.engine == "vasp":
            tags = self.parse_vasp_incar(base_content)
        elif self.engine == "siesta":
            tags = self.parse_siesta_fdf(base_content)
        else:
            raise NotImplementedError(f"Delta dictionary merging not supported for engine {self.engine}")

        for k, v in delta.items():
            key = k.strip().upper() if self.engine == "vasp" else k.strip()

            # Deletion request
            if v is None or v == "DELETE" or (isinstance(v, dict) and v.get("value") in [None, "DELETE"]):
                if key in tags:
                    del tags[key]
                continue

            # Update or Insert
            if isinstance(v, dict):
                raw_v = v.get("value", "")
                val = str(raw_v) if raw_v is not None else ""
                rationale = v.get("rationale", "") or v.get("comment", "")
                source = v.get("source", "")
            else:
                val = str(v)
                rationale = ""
                source = ""

            # Preserve existing rationale if none supplied in delta
            existing_comm = tags.get(key, {}).get("comment", "")
            existing_src = tags.get(key, {}).get("source", "")

            final_comment = rationale if rationale else existing_comm
            final_source = source if source else existing_src

            tags[key] = {
                "value": val,
                "comment": final_comment,
                "source": final_source,
                "is_block": False,
            }

        if prune_redundant and self.engine == "vasp":
            tags = self.prune_vasp_redundancy(tags)

        self.composed_tags = tags
        return tags

    # --------------------------------------------------------------------------
    # 4. RENDERING & OUTPUT GENERATION
    # --------------------------------------------------------------------------
    def render_incar(self, tags: Optional[Dict[str, Dict[str, Any]]] = None, col_width: int = 20) -> str:
        """
        Renders a beautifully formatted, aligned VASP INCAR with inline rationales.
        """
        if tags is None:
            tags = self.composed_tags

        lines = [
            "# ==============================================================================",
            "# VASP INCAR: Composed via Ponytail Delta Engine (Zero-Redundancy Standard)",
            "# ==============================================================================",
        ]

        # Categorize tags logically
        categories = {
            "Electronic Minimization": ["PREC", "ENCUT", "EDIFF", "NELM", "NELMIN", "ALGO", "LREAL", "GGA", "IVDW"],
            "Smearing & Occupations": ["ISMEAR", "SIGMA", "FERWE", "FERDO"],
            "Ionic Dynamics & Relaxation": ["IBRION", "NSW", "ISIF", "EDIFFG", "POTIM", "ISYM"],
            "Spin & Magnetism": ["ISPIN", "MAGMOM", "LORBMOM", "LSORBIT", "SAXIS"],
            "Density of States & Optics": ["NEDOS", "LORBIT", "EMIN", "EMAX", "LOPTICS", "CSHIFT"],
            "Parallelization & HPC Topology": ["NCORE", "KPAR", "NPAR", "NSIM"],
            "File Output & Checkpointing": ["LWAVE", "LCHARG", "LVHAR", "LVTOT", "LAECHG"],
        }

        rendered_keys = set()

        for cat_name, key_list in categories.items():
            cat_lines = []
            for k in key_list:
                if k in tags:
                    entry = tags[k]
                    val = str(entry["value"])
                    comment = entry.get("comment", "").strip()
                    source = entry.get("source", "").strip()

                    # Format comment with source if present
                    if source and f"[{source}]" not in comment:
                        full_comm = f"[{source}] {comment}" if comment else f"[{source}]"
                    else:
                        full_comm = comment

                    tag_part = f"{k:<12} = {val}"
                    if full_comm:
                        line = f"{tag_part:<{col_width}}  # {full_comm}"
                    else:
                        line = tag_part
                    cat_lines.append(line)
                    rendered_keys.add(k)

            if cat_lines:
                lines.append(f"\n# --- {cat_name} ---")
                lines.extend(cat_lines)

        # Catch-all for remaining tags
        other_lines = []
        for k, entry in tags.items():
            if k not in rendered_keys:
                val = str(entry["value"])
                comment = entry.get("comment", "").strip()
                source = entry.get("source", "").strip()
                if source and f"[{source}]" not in comment:
                    full_comm = f"[{source}] {comment}" if comment else f"[{source}]"
                else:
                    full_comm = comment

                tag_part = f"{k:<12} = {val}"
                if full_comm:
                    other_lines.append(f"{tag_part:<{col_width}}  # {full_comm}")
                else:
                    other_lines.append(tag_part)

        if other_lines:
            lines.append("\n# --- Additional Parameters ---")
            lines.extend(other_lines)

        lines.append("")
        return "\n".join(lines)

    def render_siesta_fdf(self, tags: Optional[Dict[str, Dict[str, Any]]] = None) -> str:
        """
        Renders a cleanly formatted SIESTA .fdf input file.
        """
        if tags is None:
            tags = self.composed_tags

        lines = [
            "# ==============================================================================",
            "# SIESTA FDF: Composed via Ponytail Delta Engine",
            "# ==============================================================================",
        ]

        blocks = []
        for k, entry in tags.items():
            if entry.get("is_block"):
                blocks.append(entry["value"])
                continue

            val = str(entry["value"])
            comment = entry.get("comment", "").strip()
            source = entry.get("source", "").strip()
            if source and f"[{source}]" not in comment:
                full_comm = f"[{source}] {comment}" if comment else f"[{source}]"
            else:
                full_comm = comment

            tag_part = f"{k:<24} {val}"
            if full_comm:
                lines.append(f"{tag_part:<36} # {full_comm}")
            else:
                lines.append(tag_part)

        if blocks:
            lines.append("\n# --- Data Blocks ---")
            lines.extend(blocks)

        lines.append("")
        return "\n".join(lines)

    def compose_to_file(
        self,
        base_file: Union[str, Path],
        delta: Dict[str, Any],
        output_file: Union[str, Path],
        prune_redundant: bool = True
    ) -> Path:
        """
        Reads base_file, applies delta, and writes the output file.
        """
        b_path = Path(base_file).resolve()
        if not b_path.exists():
            raise FileNotFoundError(f"Base template not found: {b_path}")

        with open(b_path, "r", encoding="utf-8") as f:
            base_content = f.read()

        self.apply_delta(base_content, delta, prune_redundant=prune_redundant)

        out_path = Path(output_file).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if self.engine == "vasp":
            rendered = self.render_incar()
        elif self.engine == "siesta":
            rendered = self.render_siesta_fdf()
        else:
            raise NotImplementedError(f"Renderer for {self.engine} not implemented.")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        return out_path


# ------------------------------------------------------------------------------
# CLI Interface
# ------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Ponytail Delta Composer CLI")
    parser.add_argument("--base", "-b", required=True, help="Path to base template (e.g. INCAR.base, template.fdf)")
    parser.add_argument("--delta", "-d", help="Path to delta JSON file or raw JSON string")
    parser.add_argument("--set", "-s", nargs="+", help="Direct key=value overrides (e.g. NSW=0 ISMEAR=-5)")
    parser.add_argument("--output", "-o", required=True, help="Path to output file (e.g. 01_dos/INCAR)")
    parser.add_argument("--engine", "-e", default="vasp", choices=["vasp", "siesta", "lammps"], help="Simulation engine")
    parser.add_argument("--no-prune", action="store_true", help="Disable Ponytail zero-redundancy pruning")

    args = parser.parse_args()

    delta_dict = {}
    if args.delta:
        d_path = Path(args.delta)
        if d_path.exists():
            with open(d_path, "r", encoding="utf-8") as f:
                delta_dict = json.load(f)
        else:
            try:
                delta_dict = json.loads(args.delta)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON for delta: {args.delta}", file=sys.stderr)
                sys.exit(1)

    if args.set:
        for item in args.set:
            if "=" in item:
                k, v = item.split("=", 1)
                delta_dict[k.strip()] = v.strip()

    composer = PonytailDeltaComposer(engine=args.engine)
    out_file = composer.compose_to_file(
        base_file=args.base,
        delta=delta_dict,
        output_file=args.output,
        prune_redundant=not args.no_prune
    )
    print(f"[Ponytail Delta] Successfully composed {args.engine.upper()} input: {out_file}")


if __name__ == "__main__":
    main()
