#!/usr/bin/env python3
"""
================================================================================
Scientific Research Log MCP Server (JSON-RPC 2.0 stdio)
================================================================================
Implements persistent shared memory, provenance tracking, checkpointing,
historical material retrieval, reflexion evaluator, lifelong facts/traps,
skill crystallization, dual verification, and Graphify sync grounded in
DREAMS, TRITONDFT, MDCrow, MDAgent, Lee & Rondinelli, Liu et al., GENIUS,
MatSciAgent, Mi et al., Simthesizer, Rosetta, and Meadows systems thinking.

Tools provided (21 Tools):
  - canvas_register_artifact
  - audit_provenance_chain
  - canvas_write_note
  - canvas_create_report
  - canvas_inspect
  - canvas_read
  - checkpoint_save_run
  - checkpoint_resume_run
  - checkpoint_list_runs
  - memory_store_calculation
  - memory_retrieve_similar
  - memory_save_fact
  - memory_search_facts
  - skill_save_procedure
  - skill_search_procedures
  - protocol_validate_multistep
  - verifier_dual_audit
  - evaluator_score_input
  - diagnose_convergence_failure
  - log_decision
  - graphify_sync_knowledge
================================================================================
"""

import os
import sys
import json
from typing import Dict, Any, Optional

# Add scripts directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

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

# Initialize singletons
BASE_DIR = os.path.dirname(SCRIPT_DIR)
CANVAS = CanvasStore(BASE_DIR)
CHECKPOINTS = CheckpointManager(BASE_DIR)
MEMORY = HistoricalMemoryStore(BASE_DIR)
EVALUATOR = ScientificEvaluator(BASE_DIR)
GRAPHIFY = GraphifyBridge(BASE_DIR)
FACTS = FactsStore(BASE_DIR)
SKILLS = SkillCrystallizer(BASE_DIR)
VERIFIER = DualVerifier(BASE_DIR)
PROTOCOLS = ProtocolEngine(BASE_DIR)
GIT = GitController(BASE_DIR)

TOOLS = [
    {
        "name": "canvas_register_artifact",
        "description": "Registers a simulation or calculation tool output in the DREAMS append-only provenance registry with an immutable 8-character ID, verifying sources and preventing data laundering.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "producing_tool": {"type": "string", "description": "Name of the simulation tool or python function that produced this value"},
                "value": {"description": "The exact numerical or structured result produced"},
                "arguments": {"type": "object", "description": "Full dictionary of inputs and simulation settings passed to the tool"},
                "rationales": {"type": "object", "description": "Per-parameter rationale explaining why each sensitive setting was chosen"},
                "sources": {"type": "object", "description": "Per-parameter artifact IDs where sensitive values originated (e.g. {'encut': 'a1b2c3d4'})"},
                "declared_context": {"type": "string", "description": "1-2 sentences stating which study or hypothesis this tool call belongs to"},
                "sensitive_params": {"type": "array", "items": {"type": "string"}, "description": "Optional list of sensitive parameters requiring explicit sourcing"}
            },
            "required": ["producing_tool", "value", "arguments", "declared_context"]
        }
    },
    {
        "name": "audit_provenance_chain",
        "description": "Traverses the upstream DAG dependencies of any artifact or claim to verify that every value traces back to machine-verified simulation outputs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "result_id": {"type": "string", "description": "8-character artifact ID to audit"}
            },
            "required": ["result_id"]
        }
    },
    {
        "name": "canvas_write_note",
        "description": "Creates or updates an append-only, version-controlled markdown note in the shared canvas, verifying that all cited artifact references exist.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the note"},
                "content": {"type": "string", "description": "Markdown body of the note with observations, formulas, and references"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Classification tags (e.g. ['dft', 'pt111', 'kpoints'])"},
                "references": {"type": "array", "items": {"type": "string"}, "description": "List of 8-character artifact IDs cited in the text"}
            },
            "required": ["title", "content"]
        }
    },
    {
        "name": "canvas_create_report",
        "description": "Creates an immutable verified scientific deliverable. Audits each claim against the provenance DAG before sealing the report permanently.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the final research report"},
                "objective": {"type": "string", "description": "Scientific objective being reported"},
                "executive_summary": {"type": "string", "description": "Executive summary of verified conclusions"},
                "findings": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of findings with 'title', 'description', and optional 'data' dictionary"
                },
                "claims_with_provenance": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "claim": {"type": "string"},
                            "artifact_id": {"type": "string"}
                        },
                        "required": ["claim", "artifact_id"]
                    },
                    "description": "List of claims paired with their producing artifact IDs"
                },
                "author": {"type": "string", "default": "Scientific Research Agent", "description": "Author or agent identity"}
            },
            "required": ["title", "objective", "executive_summary", "claims_with_provenance"]
        }
    },
    {
        "name": "canvas_inspect",
        "description": "Inspects available keys across Notes, Artifacts, and Reports in the DREAMS Shared Canvas.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store": {
                    "type": "string",
                    "enum": ["all", "notes", "artifacts", "reports"],
                    "default": "all",
                    "description": "Which store to inspect"
                }
            }
        }
    },
    {
        "name": "canvas_read",
        "description": "Reads a specific Note, Artifact, or Report from the DREAMS Shared Canvas by key or 8-character ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "store": {
                    "type": "string",
                    "enum": ["notes", "artifacts", "reports"],
                    "description": "Canvas store name"
                },
                "key_or_id": {"type": "string", "description": "Note key, report key, or artifact ID"}
            },
            "required": ["store", "key_or_id"]
        }
    },
    {
        "name": "checkpoint_save_run",
        "description": "Saves or updates an MDCrow simulation checkpoint and creates its isolated run directory, tracking parameters, files, and trace history.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string", "description": "Unique identifier for this calculation run"},
                "prompt_summary": {"type": "string", "description": "Summary of prompt and objectives"},
                "agent_trace": {"type": "array", "items": {"type": "object"}, "description": "Chronological trace of actions"},
                "parameter_registry": {"type": "object", "description": "Dictionary of physical and computational parameters"},
                "file_paths": {"type": "object", "description": "Dictionary of registered file paths (input, output, trajectory, logs)"},
                "figures": {"type": "array", "items": {"type": "string"}, "description": "List of generated plot figure paths"},
                "metrics": {"type": "object", "description": "Final convergence energies, RMSD, or physical metrics"},
                "status": {"type": "string", "enum": ["RUNNING", "CONVERGED", "FAILED", "ABORTED"], "default": "RUNNING"}
            },
            "required": ["run_id", "prompt_summary"]
        }
    },
    {
        "name": "checkpoint_resume_run",
        "description": "Reloads an MDCrow checkpoint, retrieving previous execution summaries, parameters, and verified files to resume or troubleshoot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string", "description": "Run ID to resume"}
            },
            "required": ["run_id"]
        }
    },
    {
        "name": "checkpoint_list_runs",
        "description": "Lists historical simulation checkpoints with status filtering and text search.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status_filter": {"type": "string", "description": "Optional status filter (e.g. CONVERGED, FAILED, RUNNING)"},
                "query": {"type": "string", "description": "Optional search term across run_id and prompt summary"}
            }
        }
    },
    {
        "name": "memory_store_calculation",
        "description": "Stores converged physical parameters (θ_phy) and HPC execution settings (θ_hpc) into the TRITONDFT Historical Memory database.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "system_name": {"type": "string", "description": "Descriptive name of the material system"},
                "formula": {"type": "string", "description": "Chemical formula (e.g. Pt, Fe, SrTiO3)"},
                "space_group": {"type": "string", "description": "Space group symbol (e.g. Fm-3m, Pnma)"},
                "crystal_system": {"type": "string", "description": "Crystal family (Cubic, Hexagonal, Tetragonal, etc.)"},
                "volume": {"type": "number", "description": "Unit-cell volume in cubic angstroms"},
                "electron_count": {"type": "number", "description": "Total valence electron count"},
                "theta_phy": {"type": "object", "description": "Physical parameters: kpoints, encut, smearing, functional, etc."},
                "theta_hpc": {"type": "object", "description": "HPC parameters: nodes, cores, ncore, kpar, walltime"},
                "accuracy_tier": {"type": "string", "enum": ["high_precision", "standard", "coarse"], "default": "standard"},
                "converged_energy": {"type": "number", "description": "Final ground-state energy in eV"},
                "notes": {"type": "string", "description": "Additional remarks or findings"}
            },
            "required": ["system_name", "formula", "theta_phy", "theta_hpc"]
        }
    },
    {
        "name": "memory_retrieve_similar",
        "description": "Queries TRITONDFT Historical Memory using two-stage symmetry-first retrieval to recommend Pareto-optimal starting parameters for a new material.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Target chemical formula"},
                "space_group": {"type": "string", "description": "Target space group (e.g. Fm-3m)"},
                "crystal_system": {"type": "string", "description": "Crystal system (e.g. Cubic)"},
                "volume": {"type": "number", "description": "Estimated cell volume in Å³"},
                "electron_count": {"type": "number", "description": "Total valence electron count"},
                "accuracy_tier": {"type": "string", "enum": ["high_precision", "standard", "coarse"], "description": "Desired accuracy level"},
                "top_k": {"type": "integer", "default": 3, "description": "Number of recommendations to return"}
            }
        }
    },
    {
        "name": "memory_save_fact",
        "description": "Liu et al. Lifelong Memory: Records an empirical material fact, operational trap, failure warning, or boundary condition that persists across models.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["trap", "empirical_rule", "boundary_condition", "benchmark"], "description": "Fact category"},
                "material_or_system": {"type": "string", "description": "System, material, or method name (e.g. 'Pt(111) CO adsorption')"},
                "statement": {"type": "string", "description": "The empirical rule or trap statement"},
                "remediation": {"type": "string", "description": "Prescribed fix or configuration setting"},
                "confidence": {"type": "number", "default": 1.0, "description": "Confidence score (0.0 to 1.0)"},
                "source_ref": {"type": "string", "description": "Citation, paper, or calculation artifact reference"}
            },
            "required": ["category", "material_or_system", "statement"]
        }
    },
    {
        "name": "memory_search_facts",
        "description": "Liu et al. Lifelong Memory: Searches empirical facts, traps, and boundary conditions before launching simulations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword or error description"},
                "category": {"type": "string", "description": "Optional category filter"},
                "material_or_system": {"type": "string", "description": "Optional material filter"}
            }
        }
    },
    {
        "name": "skill_save_procedure",
        "description": "Liu et al. Skill Crystallization: Converts a verified error recovery or simulation workflow into a permanent, reusable procedure synced with SKILL.md.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill_name": {"type": "string", "description": "Unique identifier for the procedure"},
                "description": {"type": "string", "description": "Human-readable description of what this procedure achieves"},
                "trigger_conditions": {"type": "string", "description": "When to apply this procedure (error messages, physical goals)"},
                "procedure_code": {"type": "string", "description": "Executable Python or script recipe"},
                "validation_criteria": {"type": "string", "description": "Expected verification or convergence checks"}
            },
            "required": ["skill_name", "description", "trigger_conditions", "procedure_code"]
        }
    },
    {
        "name": "skill_search_procedures",
        "description": "Liu et al. Skill Recall: Searches crystallized skills and procedural recipes matching an error or objective.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query or error signature"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "protocol_validate_multistep",
        "description": "GENIUS Protocol Engine (AEH Stage 1): Validates multi-step simulation protocols for topological ordering and parameter invariance (functional/PAW).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workflow_name": {"type": "string", "description": "Name of the multi-step study"},
                "steps": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of workflow steps with 'type', 'name', and 'parameters'"
                },
                "engine": {"type": "string", "default": "vasp", "description": "Software engine ('vasp', 'qe')"}
            },
            "required": ["workflow_name", "steps"]
        }
    },
    {
        "name": "verifier_dual_audit",
        "description": "Rosetta Dual Verification: Independently audits Functional Correctness (syntax, execution) and Scientific Validity (Scientific Constitution, non-circularity).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code_or_spec": {"type": "string", "description": "Specification text or script to audit"},
                "scientific_domain": {"type": "string", "description": "Domain ('dft', 'md', 'orca')"},
                "claims": {"type": "array", "items": {"type": "string"}, "description": "Optional list of scientific claims"},
                "literature_overlays": {"type": "array", "items": {"type": "object"}, "description": "Optional external benchmark values for overlay check"}
            },
            "required": ["code_or_spec", "scientific_domain"]
        }
    },
    {
        "name": "evaluator_score_input",
        "description": "MDAgent static script evaluator. Scores simulation scripts (1-10) and flags redundant VASP defaults, dangerous timesteps, or missing HPC topology tags.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "calc_type": {"type": "string", "description": "Software engine: 'vasp', 'qe', 'lammps', 'orca'"},
                "script_content": {"type": "string", "description": "Raw text of the simulation input script (INCAR, .pwi, in.*, etc.)"},
                "formula_or_system": {"type": "string", "description": "System description or formula for physics-aware bounds checking"}
            },
            "required": ["calc_type", "script_content"]
        }
    },
    {
        "name": "diagnose_convergence_failure",
        "description": "Applies the Lee & Rondinelli 8-Rule Decision Ladder and DREAMS Convergence Agent rules to diagnose simulation errors and prescribe exact parameter interventions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "engine": {"type": "string", "description": "Software code: 'vasp', 'qe', 'orca', 'lammps'"},
                "input_content": {"type": "string", "description": "Input file content"},
                "output_content": {"type": "string", "description": "Output log / stdout text tail"},
                "error_log": {"type": "string", "description": "Stderr or Slurm job error log"},
                "iteration_count": {"type": "integer", "default": 1, "description": "Current attempt count against the 8-attempt recovery budget"}
            },
            "required": ["engine"]
        }
    },
    {
        "name": "log_decision",
        "description": "Records an auditable procedural decision in logs/decisions.csv and EVIDENCE.md, preserving hypothesis, rule triggered, and intervention rationale.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "run_id": {"type": "string", "description": "Run ID this decision belongs to"},
                "step_name": {"type": "string", "description": "Descriptive step name (e.g. 'remedy_charge_sloshing')"},
                "hypothesis": {"type": "string", "description": "Physical hypothesis explaining the behavior"},
                "intervention": {"type": "string", "description": "Parameter or workflow intervention applied"},
                "outcome": {"type": "string", "description": "Observed or anticipated outcome"},
                "rule_id": {"type": "string", "default": "Rule B", "description": "Decision ladder rule ID (Rule A through Rule H)"},
                "evidence_ref": {"type": "string", "description": "Supporting artifact ID, paper reference, or calculation link"}
            },
            "required": ["run_id", "step_name", "hypothesis", "intervention", "outcome"]
        }
    },
    {
        "name": "graphify_sync_knowledge",
        "description": "Generates cross-linked Markdown bridge documentation for all Canvas Notes, Reports, and Checkpoints, then updates the local Graphify knowledge graph.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "git_snapshot_state",
        "description": "Creates an atomic Git commit snapshot linking the workspace state (code, inputs, logs) to an active simulation Run ID, Artifact ID, or sealed Report.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Descriptive commit message for the scientific snapshot"},
                "run_id": {"type": "string", "description": "Associated simulation Run ID"},
                "artifact_id": {"type": "string", "description": "Associated DREAMS artifact ID"},
                "report_title": {"type": "string", "description": "Associated sealed report title"},
                "tag_report": {"type": "boolean", "default": False, "description": "If true, creates an annotated Git tag"},
                "push": {"type": "boolean", "default": False, "description": "If true, pushes commit and tags to origin remote"}
            },
            "required": ["message"]
        }
    },
    {
        "name": "git_provenance_status",
        "description": "Inspects Git repository state (commit hash, branch, dirty files) to assess simulation reproducibility and provenance locking.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target_files": {"type": "array", "items": {"type": "string"}, "description": "Specific files to check for uncommitted modifications"}
            }
        }
    }
]


def handle_tool_call(name: str, args: Dict[str, Any]) -> Any:
    """Dispatches tool calls to the underlying engine."""
    if name == "canvas_register_artifact":
        return CANVAS.register_artifact(
            producing_tool=args.get("producing_tool", ""),
            value=args.get("value"),
            arguments=args.get("arguments", {}),
            rationales=args.get("rationales", {}),
            sources=args.get("sources", {}),
            declared_context=args.get("declared_context", ""),
            sensitive_params=args.get("sensitive_params")
        )
    elif name == "audit_provenance_chain":
        return CANVAS.audit_provenance_chain(args.get("result_id", ""))
    elif name == "canvas_write_note":
        return CANVAS.write_note(
            title=args.get("title", ""),
            content=args.get("content", ""),
            tags=args.get("tags"),
            references=args.get("references")
        )
    elif name == "canvas_create_report":
        return CANVAS.create_report(
            title=args.get("title", ""),
            objective=args.get("objective", ""),
            executive_summary=args.get("executive_summary", ""),
            findings=args.get("findings", []),
            claims_with_provenance=args.get("claims_with_provenance", []),
            author=args.get("author", "Scientific Research Agent")
        )
    elif name == "canvas_inspect":
        return CANVAS.inspect(store=args.get("store", "all"))
    elif name == "canvas_read":
        return CANVAS.read(store=args.get("store", ""), key_or_id=args.get("key_or_id", ""))
    elif name == "checkpoint_save_run":
        return CHECKPOINTS.save_run(
            run_id=args.get("run_id", ""),
            prompt_summary=args.get("prompt_summary", ""),
            agent_trace=args.get("agent_trace"),
            parameter_registry=args.get("parameter_registry"),
            file_paths=args.get("file_paths"),
            figures=args.get("figures"),
            metrics=args.get("metrics"),
            status=args.get("status", "RUNNING")
        )
    elif name == "checkpoint_resume_run":
        return CHECKPOINTS.resume_run(args.get("run_id", ""))
    elif name == "checkpoint_list_runs":
        return CHECKPOINTS.list_runs(
            status_filter=args.get("status_filter"),
            query=args.get("query")
        )
    elif name == "memory_store_calculation":
        return MEMORY.store_calculation(
            system_name=args.get("system_name", ""),
            formula=args.get("formula", ""),
            space_group=args.get("space_group"),
            crystal_system=args.get("crystal_system"),
            volume=args.get("volume"),
            electron_count=args.get("electron_count"),
            theta_phy=args.get("theta_phy", {}),
            theta_hpc=args.get("theta_hpc", {}),
            accuracy_tier=args.get("accuracy_tier", "standard"),
            converged_energy=args.get("converged_energy"),
            notes=args.get("notes", "")
        )
    elif name == "memory_retrieve_similar":
        return MEMORY.retrieve_similar(
            formula=args.get("formula"),
            space_group=args.get("space_group"),
            crystal_system=args.get("crystal_system"),
            volume=args.get("volume"),
            electron_count=args.get("electron_count"),
            accuracy_tier=args.get("accuracy_tier"),
            top_k=args.get("top_k", 3)
        )
    elif name == "memory_save_fact":
        return FACTS.save_fact(
            category=args.get("category", "trap"),
            material_or_system=args.get("material_or_system", ""),
            statement=args.get("statement", ""),
            remediation=args.get("remediation"),
            confidence=args.get("confidence", 1.0),
            source_ref=args.get("source_ref")
        )
    elif name == "memory_search_facts":
        return FACTS.search_facts(
            query=args.get("query"),
            category=args.get("category"),
            material_or_system=args.get("material_or_system")
        )
    elif name == "skill_save_procedure":
        return SKILLS.save_procedure(
            skill_name=args.get("skill_name", ""),
            description=args.get("description", ""),
            trigger_conditions=args.get("trigger_conditions", ""),
            procedure_code=args.get("procedure_code", ""),
            validation_criteria=args.get("validation_criteria")
        )
    elif name == "skill_search_procedures":
        return SKILLS.search_procedures(
            query=args.get("query", "")
        )
    elif name == "protocol_validate_multistep":
        return PROTOCOLS.validate_multistep_protocol(
            workflow_name=args.get("workflow_name", ""),
            steps=args.get("steps", []),
            engine=args.get("engine", "vasp")
        )
    elif name == "verifier_dual_audit":
        return VERIFIER.audit_dual_verification(
            code_or_spec=args.get("code_or_spec", ""),
            scientific_domain=args.get("scientific_domain", "dft"),
            claims=args.get("claims"),
            literature_overlays=args.get("literature_overlays")
        )
    elif name == "evaluator_score_input":
        return EVALUATOR.evaluate_script(
            calc_type=args.get("calc_type", ""),
            script_content=args.get("script_content", ""),
            formula_or_system=args.get("formula_or_system")
        )
    elif name == "diagnose_convergence_failure":
        return EVALUATOR.diagnose_convergence(
            engine=args.get("engine", ""),
            input_content=args.get("input_content", ""),
            output_content=args.get("output_content", ""),
            error_log=args.get("error_log", ""),
            iteration_count=args.get("iteration_count", 1)
        )
    elif name == "log_decision":
        return EVALUATOR.log_decision(
            run_id=args.get("run_id", ""),
            step_name=args.get("step_name", ""),
            hypothesis=args.get("hypothesis", ""),
            intervention=args.get("intervention", ""),
            outcome=args.get("outcome", ""),
            rule_id=args.get("rule_id", "Rule B"),
            evidence_ref=args.get("evidence_ref", "")
        )
    elif name == "graphify_sync_knowledge":
        return GRAPHIFY.sync_graphify()
    elif name == "git_snapshot_state":
        return GIT.create_snapshot(
            message=args.get("message", "Scientific research checkpoint"),
            run_id=args.get("run_id"),
            artifact_id=args.get("artifact_id"),
            report_title=args.get("report_title"),
            tag_report=args.get("tag_report", False),
            push=args.get("push", False)
        )
    elif name == "git_provenance_status":
        target_files = args.get("target_files")
        if target_files:
            return GIT.verify_reproducibility(target_files=target_files)
        return GIT.get_status()
    else:
        return {"error": f"Unknown tool: {name}", "isError": True}


def main():
    """Simple JSON-RPC 2.0 loop over stdin/stdout for MCP clients."""
    for line in sys.stdin:
        if not line.strip():
            continue
        req_id = None
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            # Ignore notifications
            if req_id is None or (isinstance(method, str) and method.startswith("notifications/")):
                continue

            if method == "initialize":
                protocol_version = req.get("params", {}).get("protocolVersion", "2024-11-05")
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": protocol_version,
                        "capabilities": {
                            "tools": {"listChanged": False}
                        },
                        "serverInfo": {"name": "sciresearch", "version": "2.0.0"}
                    }
                }
            elif method == "ping":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
            elif method == "tools/call":
                params = req.get("params", {})
                tname = params.get("name")
                targs = params.get("arguments", {})
                try:
                    res_content = handle_tool_call(tname, targs)
                    is_err = isinstance(res_content, dict) and res_content.get("isError", False)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(res_content, indent=2)}],
                            "isError": is_err
                        }
                    }
                except Exception as tool_err:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": f"Error executing tool {tname}: {str(tool_err)}"}],
                            "isError": True
                        }
                    }
            elif method == "resources/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"resources": []}}
            elif method == "prompts/list":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": []}}
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method {method} not found"}
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            if req_id is not None:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": str(e)}
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
