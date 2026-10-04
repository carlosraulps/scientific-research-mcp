#!/usr/bin/env python3
"""
================================================================================
Scientific Research Log CLI (sciresearch)
================================================================================
Command-line utility for managing persistent shared memory, provenance
registry, historical parameters, lifelong facts/traps, crystallized skills,
dual verification, and Graphify sync.
================================================================================
"""

import os
import sys
import json
import argparse

# Add scripts directory (using realpath to correctly resolve global symlinks)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from canvas_store import CanvasStore
from checkpoint_manager import CheckpointManager
from historical_memory import HistoricalMemoryStore
from scientific_evaluator import ScientificEvaluator
from graphify_bridge import GraphifyBridge
from facts_store import FactsStore
from skill_crystallizer import SkillCrystallizer
from dual_verifier import DualVerifier
from protocol_engine import ProtocolEngine
from git_controller import GitController
from ponytail_delta import PonytailDeltaComposer
from structure_guard import StructureSanityGuard
from hypothesis_evaluator import HypothesisEvaluator
from sde_loop_verifier import SDELoopVerifier
from notebooklm_bridge import NotebookLMBridge


def main():
    parser = argparse.ArgumentParser(description="Scientific Research Log CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")

    # Inspect
    inspect_parser = subparsers.add_parser("inspect", help="Inspect Canvas stores (all, notes, artifacts, reports)")
    inspect_parser.add_argument("--store", default="all", choices=["all", "notes", "artifacts", "reports"])

    # Audit
    audit_parser = subparsers.add_parser("audit", help="Audit upstream provenance chain of an artifact")
    audit_parser.add_argument("result_id", help="8-character artifact ID")

    # List Checkpoints
    runs_parser = subparsers.add_parser("runs", help="List simulation checkpoints")
    runs_parser.add_argument("--status", help="Filter by status")
    runs_parser.add_argument("--query", help="Search query")

    # Memory Query
    mem_parser = subparsers.add_parser("memory", help="Query TRITONDFT Historical Memory for similar systems")
    mem_parser.add_argument("--formula", help="Target formula")
    mem_parser.add_argument("--space-group", help="Target space group")
    mem_parser.add_argument("--crystal-system", help="Crystal system")
    mem_parser.add_argument("--tier", default="standard", choices=["high_precision", "standard", "coarse"])

    # Facts & Traps
    facts_parser = subparsers.add_parser("facts", help="Search Liu et al. Lifelong Facts & Traps Memory")
    facts_parser.add_argument("--query", help="Keyword or system query")
    facts_parser.add_argument("--category", choices=["trap", "empirical_rule", "boundary_condition", "benchmark"])
    facts_parser.add_argument("--system", help="Specific material or system")

    # Crystallized Skills
    skills_parser = subparsers.add_parser("skills", help="Search crystallized procedural skills")
    skills_parser.add_argument("query", help="Search query or error signature")

    # Script Score
    eval_parser = subparsers.add_parser("eval", help="Evaluate simulation script against best practices")
    eval_parser.add_argument("file", help="Path to input script (INCAR, .pwi, in.*)")
    eval_parser.add_argument("--engine", default="vasp", choices=["vasp", "qe", "lammps", "orca"])

    # Dual Verifier
    verif_parser = subparsers.add_parser("verify", help="Rosetta Dual Verification (Functional + Scientific Validity)")
    verif_parser.add_argument("file", help="Path to specification, script, or model")
    verif_parser.add_argument("--domain", default="dft", choices=["dft", "md", "orca"])

    # Graphify Sync
    subparsers.add_parser("sync", help="Sync knowledge documents and trigger graphify update")

    # Git Controller
    git_parser = subparsers.add_parser("git", help="Scientific Git Version Control & Provenance Integrator")
    git_sub = git_parser.add_subparsers(dest="git_action", help="Git operation")
    git_sub.add_parser("status", help="Show git status and reproducibility locking")
    snap_p = git_sub.add_parser("snapshot", help="Record an atomic scientific git snapshot")
    snap_p.add_argument("message", help="Commit message")
    snap_p.add_argument("--run-id", help="Associated simulation Run ID")
    snap_p.add_argument("--artifact-id", help="Associated DREAMS Artifact ID")
    snap_p.add_argument("--report", help="Associated Report Title")
    snap_p.add_argument("--tag", action="store_true", help="Create annotated tag for report")
    snap_p.add_argument("--push", action="store_true", help="Push to origin remote")
    ver_p = git_sub.add_parser("verify", help="Verify reproducibility of input scripts against git commit")
    ver_p.add_argument("files", nargs="*", help="Optional target files to check")

    # Ponytail Compose
    comp_parser = subparsers.add_parser("compose", help="Compose self-documenting input from base template and delta")
    comp_parser.add_argument("--base", "-b", required=True, help="Path to base template (INCAR.base, template.fdf)")
    comp_parser.add_argument("--delta", "-d", help="Path to delta JSON file or raw JSON string")
    comp_parser.add_argument("--set", "-s", nargs="+", help="Direct key=value overrides (e.g. NSW=0 ISMEAR=-5)")
    comp_parser.add_argument("--output", "-o", required=True, help="Path to output file (e.g. 01_dos/INCAR)")
    comp_parser.add_argument("--engine", "-e", default="vasp", choices=["vasp", "siesta", "lammps"], help="Simulation engine")
    comp_parser.add_argument("--no-prune", action="store_true", help="Disable Ponytail zero-redundancy pruning")

    # Structure Sanity Guard
    guard_parser = subparsers.add_parser("guard-structure", help="Inspect structure file (POSCAR, XYZ, CIF) for coordinate hallucinations and atomic overlaps")
    guard_parser.add_argument("file", help="Path to structure file")

    # Hypothesis Evaluator
    hypo_parser = subparsers.add_parser("eval-hypothesis", help="Evaluate scientific hypothesis across Novelty, Validity, Clarity, and Feasibility")
    hypo_parser.add_argument("hypothesis", help="Text or JSON file containing hypothesis")

    # SDE Closed-Loop Verifier
    sde_parser = subparsers.add_parser("sde-verify", help="Audit closed-loop discovery step and check for reasoning saturation")
    sde_parser.add_argument("project", help="Project name")
    sde_parser.add_argument("round", type=int, help="Round index")
    sde_parser.add_argument("hypothesis", help="Hypothesis text")
    sde_parser.add_argument("--structure", help="Path to structure file")
    sde_parser.add_argument("--oracle", action="store_true", help="External computational/simulation oracle was called")
    sde_parser.add_argument("--metric", type=float, help="Observed property metric")
    sde_parser.add_argument("--goal", type=float, help="Target metric goal")
    sde_parser.add_argument("--reset", action="store_true", help="Reset project state history")

    # NotebookLM Grounding Lookup
    ground_parser = subparsers.add_parser("ground", help="Look up NotebookLM-grounded parameter rationale and literature citation")
    ground_parser.add_argument("engine", choices=["vasp", "siesta", "lammps", "orca", "all"], help="Simulation engine")
    ground_parser.add_argument("tag", help="Parameter tag (e.g. ALGO, POTIM, Tdamp, Pdamp, AMIX)")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    canvas = CanvasStore(BASE_DIR)
    checkpoints = CheckpointManager(BASE_DIR)
    memory = HistoricalMemoryStore(BASE_DIR)
    evaluator = ScientificEvaluator(BASE_DIR)
    graphify = GraphifyBridge(BASE_DIR)
    facts = FactsStore(BASE_DIR)
    skills = SkillCrystallizer(BASE_DIR)
    verifier = DualVerifier(BASE_DIR)
    git = GitController(BASE_DIR)
    structure_guard = StructureSanityGuard()
    hypothesis_evaluator = HypothesisEvaluator(BASE_DIR)
    sde_verifier = SDELoopVerifier(BASE_DIR)

    if args.subcommand == "inspect":
        res = canvas.inspect(args.store)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "audit":
        res = canvas.audit_provenance_chain(args.result_id)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "runs":
        res = checkpoints.list_runs(args.status, args.query)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "memory":
        res = memory.retrieve_similar(
            formula=args.formula,
            space_group=args.space_group,
            crystal_system=args.crystal_system,
            accuracy_tier=args.tier
        )
        print(json.dumps(res, indent=2))

    elif args.subcommand == "facts":
        res = facts.search_facts(
            query=args.query,
            category=args.category,
            material_or_system=args.system
        )
        print(json.dumps(res, indent=2))

    elif args.subcommand == "skills":
        res = skills.search_procedures(args.query)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "eval":
        if not os.path.exists(args.file):
            print(f"Error: file '{args.file}' not found.")
            sys.exit(1)
        with open(args.file, "r") as f:
            content = f.read()
        res = evaluator.evaluate_script(args.engine, content)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "verify":
        if not os.path.exists(args.file):
            print(f"Error: file '{args.file}' not found.")
            sys.exit(1)
        with open(args.file, "r") as f:
            content = f.read()
        res = verifier.audit_dual_verification(content, args.domain)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "sync":
        print("Synchronizing Knowledge Map and updating Graphify...")
        res = graphify.sync_graphify()
        print(json.dumps(res, indent=2))

    elif args.subcommand == "git":
        if args.git_action == "status" or not args.git_action:
            res = git.get_status()
            print(json.dumps(res, indent=2))
        elif args.git_action == "snapshot":
            res = git.create_snapshot(
                message=args.message,
                run_id=args.run_id,
                artifact_id=args.artifact_id,
                report_title=args.report,
                tag_report=args.tag,
                push=args.push
            )
            print(json.dumps(res, indent=2))
        elif args.git_action == "verify":
            res = git.verify_reproducibility(target_files=args.files if args.files else None)
            print(json.dumps(res, indent=2))

    elif args.subcommand == "compose":
        delta_dict = {}
        if args.delta:
            d_path = os.path.abspath(args.delta)
            if os.path.exists(d_path):
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
        print(json.dumps({
            "status": "success",
            "engine": args.engine,
            "output_file": str(out_file),
            "composed_tags_count": len(composer.composed_tags)
        }, indent=2))

    elif args.subcommand == "guard-structure":
        res = structure_guard.inspect_file(args.file)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("valid", False) else 1)

    elif args.subcommand == "eval-hypothesis":
        hypo_text = args.hypothesis
        if os.path.exists(hypo_text):
            with open(hypo_text, "r", encoding="utf-8") as f:
                hypo_text = f.read()
        res = hypothesis_evaluator.evaluate_hypothesis(hypo_text)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("passed", False) else 1)

    elif args.subcommand == "sde-verify":
        if args.reset:
            sde_verifier.reset_project(args.project)
        hypo_text = args.hypothesis
        if os.path.exists(hypo_text):
            with open(hypo_text, "r", encoding="utf-8") as f:
                hypo_text = f.read()
        res = sde_verifier.verify_discovery_step(
            project_name=args.project,
            round_index=args.round,
            hypothesis_text=hypo_text,
            structure_file=args.structure,
            observed_metric=args.metric,
            oracle_called=args.oracle,
            target_metric_goal=args.goal
        )
        print(json.dumps(res, indent=2))

    elif args.subcommand == "ground":
        bridge = NotebookLMBridge(BASE_DIR)
        res = bridge.lookup_grounding(args.engine, args.tag)
        if res:
            print(json.dumps(res, indent=2))
        else:
            print(json.dumps({"error": f"No cached NotebookLM grounding found for {args.engine}:{args.tag}", "isError": True}))


if __name__ == "__main__":
    main()
