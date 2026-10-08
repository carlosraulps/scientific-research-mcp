#!/usr/bin/env python3
"""
CLI interface for the sciresearch ecosystem.
Provides command-line access to:
  - DREAMS Canvas stores (inspect, audit)
  - TRITONDFT Historical Memory
  - Liu et al. Lifelong Facts & Procedural Skills
  - Rosetta Dual Verifier
  - Ponytail Delta Composer
  - Microsoft Structure Sanity Guard
  - LLM4SR Hypothesis Evaluator
  - SDE Closed-Loop Discovery Verifier
  - NotebookLM Grounding Bridge
  - Scientific Visualization & Standardization Tools (Wyckoff, Compact Slice, Zero-Dilation, Strain Descriptors)
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.join(SCRIPT_DIR, "scripts") not in sys.path:
    sys.path.insert(0, os.path.join(SCRIPT_DIR, "scripts"))

from canvas_store import CanvasStore
from historical_memory import HistoricalMemoryStore
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
from guardrails_engine import GuardrailsEngine
from component_evaluator import ComponentEvaluator
from cache_store import CacheStore
from scientific_visualization_tools import (
    standardize_wyckoff_bader_charges,
    extract_compact_2d_slice,
    validate_animation_geometry,
    quantify_electronic_strain_metrics
)


def main():
    parser = argparse.ArgumentParser(description="SciResearch CLI: Research log, memory, guardrails, and visualization suite")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # Inspect
    insp_parser = subparsers.add_parser("inspect", help="Inspect Canvas stores")
    insp_parser.add_argument("--store", "-s", choices=["all", "notes", "artifacts", "reports"], default="all")

    # Audit
    audit_parser = subparsers.add_parser("audit", help="Audit DAG provenance chain")
    audit_parser.add_argument("result_id", help="8-character artifact ID")

    # Memory
    mem_parser = subparsers.add_parser("memory", help="Query TRITONDFT historical memory")
    mem_parser.add_argument("--formula", "-f", help="Chemical formula")
    mem_parser.add_argument("--space-group", "-sg", help="Space group symbol or number")
    mem_parser.add_argument("--crystal-system", "-cs", help="Crystal system")
    mem_parser.add_argument("--tier", "-t", choices=["high_precision", "standard", "screening"], default="standard")

    # Facts
    facts_parser = subparsers.add_parser("facts", help="Query lifelong facts and traps store")
    facts_parser.add_argument("--query", "-q", help="Text search query")
    facts_parser.add_argument("--category", "-c", choices=["trap", "empirical_rule", "boundary_condition", "benchmark"])
    facts_parser.add_argument("--system", "-s", help="Filter by material or system")

    # Skills
    skills_parser = subparsers.add_parser("skills", help="Search crystallized procedural skills")
    skills_parser.add_argument("query", help="Text search query")

    # Eval
    eval_parser = subparsers.add_parser("eval", help="Score input script with MDAgent Reflexion")
    eval_parser.add_argument("file", help="Path to input script (INCAR, etc.)")
    eval_parser.add_argument("--engine", "-e", choices=["vasp", "siesta", "lammps", "qe"], default="vasp")

    # Verify
    verify_parser = subparsers.add_parser("verify", help="Rosetta dual verification")
    verify_parser.add_argument("file", help="Path to input script or specification")
    verify_parser.add_argument("--domain", "-d", choices=["dft", "md", "cluster", "general"], default="dft")

    # Runs
    runs_parser = subparsers.add_parser("runs", help="List MDCrow simulation runs")
    runs_parser.add_argument("--status", "-s", choices=["INITIALIZED", "RUNNING", "COMPLETED", "FAILED", "SUSPENDED"])

    # Sync
    subparsers.add_parser("sync", help="Synchronize knowledge map and update Graphify graph")

    # Git
    git_parser = subparsers.add_parser("git", help="Provenance git operations")
    git_sub = git_parser.add_subparsers(dest="git_action")
    git_sub.add_parser("status", help="Check working tree state against git provenance standards")
    git_sub.add_parser("snapshot", help="Create a git commit capturing current state as provenance checkpoint")
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

    # Wyckoff Bader Standardization
    bader_p = subparsers.add_parser("bader-standardize", help="Standardize Bader charges by Wyckoff symmetry orbits and PAW z-core")
    bader_p.add_argument("file", help="Path to ACF.dat or bader charges file")
    bader_p.add_argument("--wyckoff", "-w", help="Path to JSON file or string mapping atom indices to Wyckoff sites")
    bader_p.add_argument("--z-core", "-z", type=float, default=4.0, help="Valence core electron charge offset (default: 4.0 for C)")
    bader_p.add_argument("--tolerance", "-t", type=float, default=0.15, help="Standard deviation threshold for warnings")
    bader_p.add_argument("--element", "-e", default="C", help="Target element symbol (default: C)")

    # Compact 2D Slice
    slice_p = subparsers.add_parser("slice-2d", help="Extract compact 2D planar slice from 3D volumetric CHGCAR")
    slice_p.add_argument("file", help="Path to CHGCAR or volumetric dataset")
    slice_p.add_argument("--output", "-o", help="Optional output .npz or .dat file")
    slice_p.add_argument("--z-slice", "-z", type=float, default=0.50, help="Fractional z coordinate for slice (0.0 to 1.0)")
    slice_p.add_argument("--plane", "-p", choices=["xy", "xz", "yz"], default="xy", help="Slice orientation plane")

    # Validate Animation Geometry
    anim_p = subparsers.add_parser("validate-anim", help="Validate uniform pixel geometry across animation frames (Zero-Dilation Rule)")
    anim_p.add_argument("frames", nargs="+", help="Image frame file paths")
    anim_p.add_argument("--target-res", "-r", nargs=2, type=int, help="Optional expected width height (e.g. 1920 1080)")

    # Strain Metrics
    strain_p = subparsers.add_parser("strain-metrics", help="Quantify electronic strain descriptors across 2D states")
    strain_p.add_argument("file", help="Path to CSV or JSON file containing band data")
    strain_p.add_argument("--pristine-ef", "-ef", type=float, help="Pristine Fermi level reference (eV)")

    # Defense-in-Depth Guardrail
    guard_p = subparsers.add_parser("guardrail", help="Audit scientific inputs, execution state, or outputs against defense-in-depth guardrails")
    guard_p.add_argument("--stage", "-s", choices=["input", "execution", "output"], default="input", help="Guardrail stage")
    guard_p.add_argument("--file", "-f", help="Target input or output file")
    guard_p.add_argument("--text", "-t", help="Inline text payload")
    guard_p.add_argument("--domain", "-d", default="dft", help="Scientific domain")
    guard_p.add_argument("--iter", "-i", type=int, default=1, help="Current iteration against recovery budget")

    # Component Evaluator
    comp_eval_p = subparsers.add_parser("test-components", help="Run isolated component-level benchmarks across SciResearch modules")
    comp_eval_p.add_argument("--component", "-c", help="Specific component to test (or omit for all)")

    # Cache
    cache_p = subparsers.add_parser("cache", help="Query or manage hierarchical semantic & exact cache")
    cache_p.add_argument("action", choices=["get", "set", "stats"], help="Cache operation")
    cache_p.add_argument("--key", "-k", help="Exact cache key")
    cache_p.add_argument("--text", "-t", help="Natural language query for semantic matching")
    cache_p.add_argument("--val", "-v", help="Value string or JSON for cache set")
    cache_p.add_argument("--namespace", "-ns", default="default", help="Cache namespace")
    cache_p.add_argument("--similarity", "-sim", type=float, default=0.85, help="Minimum semantic similarity")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    BASE_DIR = Path(SCRIPT_DIR).parent if os.path.basename(SCRIPT_DIR) == "scripts" else Path(SCRIPT_DIR)
    canvas = CanvasStore(BASE_DIR)
    history = HistoricalMemoryStore(BASE_DIR)
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

    elif args.subcommand == "memory":
        res = history.retrieve_similar(
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
        from mdagent_evaluator import MDAgentEvaluator
        evaluator = MDAgentEvaluator(BASE_DIR)
        res = evaluator.score_input_script(args.file, args.engine)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "verify":
        res = verifier.verify_domain(args.file, args.domain)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "runs":
        from checkpoint_manager import CheckpointManager
        checkpointer = CheckpointManager(BASE_DIR)
        res = checkpointer.list_runs(status_filter=args.status)
        print(json.dumps(res, indent=2))

    elif args.subcommand == "sync":
        from graphify_bridge import GraphifyBridge
        gbridge = GraphifyBridge(BASE_DIR)
        res = gbridge.sync_knowledge_map()
        print(json.dumps(res, indent=2))

    elif args.subcommand == "git":
        if args.git_action == "status":
            res = git.get_status()
            print(json.dumps(res, indent=2))
        elif args.git_action == "snapshot":
            res = git.snapshot_state()
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

    elif args.subcommand == "bader-standardize":
        wyckoff_map = None
        if args.wyckoff:
            if os.path.exists(args.wyckoff):
                with open(args.wyckoff, "r") as f:
                    wyckoff_map = json.load(f)
            else:
                wyckoff_map = json.loads(args.wyckoff)
        res = standardize_wyckoff_bader_charges(
            bader_data=args.file,
            wyckoff_mapping=wyckoff_map,
            z_core=args.z_core,
            tolerance=args.tolerance,
            element=args.element
        )
        print(json.dumps(res, indent=2))

    elif args.subcommand == "slice-2d":
        res = extract_compact_2d_slice(
            source_path=args.file,
            output_path=args.output,
            z_slice=args.z_slice,
            plane=args.plane
        )
        print(json.dumps(res, indent=2))

    elif args.subcommand == "validate-anim":
        target_res = tuple(args.target_res) if args.target_res else None
        res = validate_animation_geometry(
            frame_paths=args.frames,
            target_resolution=target_res
        )
        print(json.dumps(res, indent=2))

    elif args.subcommand == "strain-metrics":
        res = quantify_electronic_strain_metrics(
            band_data=args.file,
            reference_efermi=args.pristine_ef
        )
        print(json.dumps(res, indent=2))

    elif args.subcommand == "guardrail":
        guard = GuardrailsEngine(BASE_DIR)
        payload = {}
        if args.file and os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
            if args.file.endswith(".json"):
                try:
                    payload = json.loads(content)
                except Exception:
                    payload = {"content": content}
            else:
                payload = {"content": content}
        elif args.text:
            try:
                payload = json.loads(args.text)
            except Exception:
                payload = {"content": args.text}

        if args.stage == "input":
            res = guard.audit_input(payload, domain=args.domain)
        elif args.stage == "execution":
            res = guard.audit_execution(iteration_count=args.iter)
        elif args.stage == "output":
            raw_text = payload.get("content", str(payload)) if isinstance(payload, dict) else str(payload)
            res = guard.audit_output(raw_text, engine=args.domain)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("passed", False) else 1)

    elif args.subcommand == "test-components":
        evaluator = ComponentEvaluator(BASE_DIR)
        if args.component:
            res = evaluator.evaluate_component(args.component)
        else:
            res = evaluator.evaluate_all()
        print(json.dumps(res, indent=2))
        sys.exit(0 if res.get("passed", res.get("system_health") == "HEALTHY") else 1)

    elif args.subcommand == "cache":
        cache_store = CacheStore(BASE_DIR)
        if args.action == "get":
            res = cache_store.get(
                query_key=args.key or "",
                query_text=args.text,
                namespace=args.namespace,
                min_similarity=args.similarity
            )
            print(json.dumps(res if res else {"hit": False, "message": "Cache miss"}, indent=2))
        elif args.action == "set":
            val = args.val
            try:
                val = json.loads(args.val)
            except Exception:
                pass
            cid = cache_store.set(
                query_key=args.key or "",
                query_text=args.text or "",
                value=val,
                namespace=args.namespace
            )
            print(json.dumps({"stored": True, "cache_id": cid}, indent=2))
        elif args.action == "stats":
            res = cache_store.stats(namespace=args.namespace if args.namespace != "default" else None)
            print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
