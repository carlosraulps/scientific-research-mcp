# 🔬 Scientific Research Log & Persistent Shared Memory Engine (`sciresearch`)

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![MCP 2.0](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green.svg)](https://modelcontextprotocol.io/)
[![Architecture](https://img.shields.io/badge/Literature%20Frameworks-12-purple.svg)](#-theoretical-foundations--literature-architecture)
[![Tools](https://img.shields.io/badge/MCP%20Tools-23-orange.svg)](#-mcp-tools-reference-23-tools)
[![Tests](https://img.shields.io/badge/tests-13%2F13%20passed-brightgreen.svg)](tests/test_sciresearch.py)
[![Graphify](https://img.shields.io/badge/Graphify-Knowledge%20Graph-cyan.svg)](graphify-out/)

An autonomous **Skill, CLI, and Model Context Protocol (MCP) Server** for scientific research logging, session-persistent shared memory, append-only provenance tracking, simulation checkpointing, and git-versioned reproducibility. Designed specifically for **Density Functional Theory (DFT)**, **Molecular Dynamics (MD)**, and **Multireference Quantum Chemistry** workflows.

---

## 🏛️ Theoretical Foundations & Literature Architecture

`sciresearch` synthesizes **12 foundational frameworks** from recent literature on autonomous scientific LLM agents, multireference quantum chemistry, and systems dynamics:

| Framework | Citation | Implemented Scientific Mechanism |
| :--- | :--- | :--- |
| **DREAMS** | Z. Wang et al., *arXiv:2507.14267* (2026) | **Centralized Shared Canvas** (Notes, Artifacts, Reports), **Append-Only Provenance Registry** (immutable 8-character SHA256 IDs, DAG dependency traversal, and anti-laundering verification gates). |
| **MDCrow** | Q. Campbell et al., *ML:ST* 7, 025037 (2026) | **Checkpoint-Based Memory**: Unique run directories (`runs/<run_id>/`), serialized manifests (`checkpoints/<run_id>.json`), trajectory & parameter registries, and non-blocking session resumption. |
| **TRITONDFT** | Z. Hu et al., *arXiv:2603.01258* (2026) | **Historical Memory Store** (`historical_memory.db`): Physical parameters ($\theta_{\text{phy}}$) decoupled from HPC settings ($\theta_{\text{hpc}}$), two-stage symmetry-first retrieval, and Pareto accuracy tiers (<1, <10, <20 meV/atom). |
| **MDAgent** | Y. Shi et al., *arXiv:2508.10931* (2025) | **Reflexion Evaluator**: Static simulation script scoring (1–10) with Ponytail zero-redundancy checks and structured parameter correction feedback. |
| **Lee & Rondinelli** | S. Lee & J. Rondinelli, *arXiv:2609.13357* (2026) | **Multireference Decision Ladder**: 8-rule deterministic diagnostics (`Rule A` through `Rule H`), 8-attempt recovery budget, and append-only decision logging (`logs/decisions.csv`, `EVIDENCE.md`). |
| **Liu et al.** | C. Liu et al., *arXiv:2602.04961* (2026) | **Lifelong Agent Memory**: Empirical facts and numerical traps (`facts_memory.db`), plus procedural skill crystallization (`skills_memory.db`) with automatic sync to `SKILL.md`. |
| **GENIUS** | M. Soleymanibrojeni et al., *arXiv:2603.08053* (2026) | **Protocol Engine**: Multi-step simulation protocol validation (topological ordering, step invariant tracking, PAW/functional consistency). |
| **MatSciAgent** | P. Chaudhari et al., *arXiv:2509.07684* (2025) | **Modular Architecture**: Decoupled execution domains (DFT, MD, CASSCF) with domain-specific diagnostic rules. |
| **Mi et al.** | K. Mi et al., *arXiv:2502.13170* (2025) | **Systems Agent**: Safe command and process lifecycle management with strict STDIO stream protection. |
| **Simthesizer** | Y. Kim et al., *arXiv:2601.12994* (2026) | **Workload Simulation**: Micro-benchmarking, parameter profiling, and execution-time bounds enforcement. |
| **Rosetta** | K. Sankaralingam et al., *arXiv:2603.01895* (2026) | **Dual Verification**: Strict separation of Functional Correctness from Scientific Validity and enforcement of the Scientific Constitution (non-circularity, calibration-as-overlay). |
| **Meadows** | D. Meadows, *Thinking in Systems* (2008) | **Systemic Feedback**: Reinforcing error loops, adaptive parameter damping, and systemic knowledge graph consolidation. |

---

## 🚀 Key Capabilities

### 1. DREAMS Shared Canvas & Anti-Laundering Provenance
- **Three-Store Canvas**:
  - `canvas/notes/`: Free-form markdown notes with validated artifact citations.
  - `canvas/artifacts/`: Append-only tool outputs keyed by 8-character SHA256 hashes (`a1b2c3d4.json`).
  - `canvas/reports/`: Structured, verified deliverables audited against the provenance DAG and sealed as permanently immutable.
- **Anti-Laundering Gates**: Rejects unverified numbers, context-free declarations (<20 chars), and trivial identity transformations (`x * 1.0`, `x + 0`) designed to launder unverified inputs.

### 2. Git Version Control & Reproducibility Locking
- **Automatic Provenance Binding**: Every registered artifact and simulation checkpoint automatically embeds the active Git commit hash (`short_hash`), branch name, and dirty status.
- **Scientific Commit Snapshots**: The `git_snapshot_state` tool and `sciresearch git snapshot` CLI command record atomic Git commits tagged with `SciResearch-Run`, `SciResearch-Artifact`, and `SciResearch-Report` metadata.
- **Report Tagging**: Automatically emits annotated Git tags (`report-<timestamp>`) when DREAMS reports are sealed.
- **Reproducibility Audits**: Checks whether working directory modifications compromise simulation reproducibility.

### 3. Checkpoint-Based Memory (MDCrow)
- Automatically manages unique simulation folders in `runs/<run_id>/` and manifests in `checkpoints/<run_id>.json`.
- Allows researchers and agents to pause long simulations and resume later sessions without losing agent traces or parameter setups.

### 4. Symmetry-First Historical Memory (TRITONDFT)
- Decouples physical converged parameters ($\theta_{\text{phy}}$: cutoff, k-points, smearing) from cluster execution parameters ($\theta_{\text{hpc}}$: nodes, NCORE, KPAR).
- Two-stage retrieval: Space group / crystal system match $\rightarrow$ formula & volume similarity.

### 5. Lifelong Facts, Traps & Procedural Skill Crystallization (Liu et al.)
- **Facts & Traps Memory**: SQLite store of empirical material rules, numerical traps (e.g., charge sloshing, Ghost states, supercell commensurability), and boundary conditions.
- **Procedural Skill Crystallization**: When an agent successfully diagnoses and recovers from a simulation failure, it crystallizes the procedure into a reusable skill stored in `memory/skills_memory.db` and synchronized with `SKILL.md`.

### 6. Rosetta Dual Verification & Scientific Constitution
- Separates **Functional Correctness** (Does the code run without syntax or execution errors?) from **Scientific Validity** (Does the model violate fundamental physical laws or constitutional rules?).
- **Scientific Constitution (PRIME DIRECTIVES)**:
  1. *Rule of Non-Circularity*: Target values (experimental bandgaps, lattice parameters) must NEVER appear in the forward functional form or calculation parameters.
  2. *Rule of Calibration-as-Overlay*: External benchmark data may only be used as comparative reference overlays on finished outputs.

---

## 📦 Directory Structure

```
scientific-research-mcp/
├── CLAUDE.md                   # System policies, Ponytail VASP rules, 8-rule decision ladder
├── TASK.md                     # Active loop tracking and subtask state
├── EVIDENCE.md                 # Theoretical justifications and append-only decision logs
├── SKILL.md                    # Antigravity skill reference documenting all 23 tools
├── cli.py                      # Unified CLI entry point ('sciresearch')
├── scripts/
│   ├── canvas_store.py         # DREAMS Notes, Artifacts, Reports & Anti-Laundering Gates
│   ├── checkpoint_manager.py   # MDCrow session checkpoints & file registries
│   ├── historical_memory.py    # TRITONDFT θ_phy / θ_hpc historical SQLite store
│   ├── facts_store.py          # Liu et al. lifelong empirical facts & traps store
│   ├── skill_crystallizer.py   # Liu et al. procedural skill crystallization engine
│   ├── dual_verifier.py        # Rosetta dual verification & Scientific Constitution
│   ├── protocol_engine.py      # GENIUS AEH Stage 1 multi-step protocol engine
│   ├── scientific_evaluator.py # MDAgent static scoring & 8-rule convergence diagnostics
│   ├── git_controller.py       # Scientific Git Version Controller & Reproducibility Auditor
│   ├── graphify_bridge.py      # Graphify synchronization bridge
│   └── mcp_server.py           # JSON-RPC 2.0 stdio MCP server (23 tools)
├── canvas/                     # DREAMS canvas stores (notes/, artifacts/, reports/)
├── checkpoints/                # MDCrow checkpoint manifests (*.json)
├── memory/                     # Persistent SQLite databases (historical, facts, skills)
├── runs/                       # Unique simulation run directories
├── tests/
│   └── test_sciresearch.py     # 13/13 passing unit tests
└── graphify-out/               # Graphify knowledge graph (238 nodes, 319 edges, 40 communities)
```

---

## 🔧 Installation & Global Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git 2.25+

### 2. Local Setup
```bash
git clone git@github.com:carlosraulps/scientific-research-mcp.git
cd scientific-research-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or install standard libs
```

### 3. CLI Installation
Make `cli.py` accessible system-wide:
```bash
ln -sf $(pwd)/cli.py ~/.local/bin/sciresearch
chmod +x ~/.local/bin/sciresearch
```

### 4. MCP Server Registration
Add `sciresearch` to your MCP client configuration (e.g. `~/.gemini/config/mcp_config.json` or Claude Desktop):
```json
{
  "mcpServers": {
    "sciresearch": {
      "command": "/usr/bin/python3",
      "args": ["/path/to/scientific-research-mcp/scripts/mcp_server.py"]
    }
  }
}
```

---

## 🛠️ MCP Tools Reference (23 Tools)

| Category | Tool Name | Description |
| :--- | :--- | :--- |
| **DREAMS Canvas** | `canvas_register_artifact` | Registers tool outputs with SHA256 IDs, checking rationales & anti-laundering gates. |
| | `audit_provenance_chain` | Traverses DAG ancestors to verify scientific claims. |
| | `canvas_write_note` | Creates or updates versioned markdown notes in the shared canvas. |
| | `canvas_create_report` | Compiles audited claims into an immutable, sealed scientific report. |
| | `canvas_inspect` | Lists keys and summaries across notes, artifacts, and reports. |
| | `canvas_read` | Retrieves full JSON or Markdown content of any canvas document. |
| **MDCrow Checkpoints** | `checkpoint_save_run` | Saves simulation state, parameter registries, and files to `runs/<run_id>/`. |
| | `checkpoint_resume_run` | Resumes an existing run session without re-executing completed stages. |
| | `checkpoint_list_runs` | Lists and filters checkpoints by status or keyword. |
| **TRITONDFT Memory** | `memory_store_calculation` | Stores converged $\theta_{\text{phy}}$ and $\theta_{\text{hpc}}$ parameters into historical SQLite memory. |
| | `memory_retrieve_similar` | Two-stage symmetry and formula retrieval for recommended calculation settings. |
| **Lifelong Memory** | `memory_save_fact` | Saves empirical material facts, numerical traps, and boundary conditions. |
| | `memory_search_facts` | Queries lifelong facts and traps database by system or failure mode. |
| **Skill Crystallization** | `skill_save_procedure` | Crystallizes verified recovery procedures into reusable skills. |
| | `skill_search_procedures` | Retrieves crystallized procedural workflows by error signature. |
| **Dual Verification** | `verifier_dual_audit` | Separates functional correctness from scientific constitution compliance. |
| **GENIUS Protocols** | `protocol_validate_multistep` | Validates multi-step protocols for topological ordering and parameter invariance. |
| **Reflexion & Decision** | `evaluator_score_input` | Scores simulation inputs (1–10) with Ponytail zero-redundancy checks. |
| | `diagnose_convergence_failure` | Evaluates convergence failures against the 8-rule decision ladder. |
| | `log_decision` | Appends decision logs to `logs/decisions.csv` and `EVIDENCE.md`. |
| **Git Version Control** | `git_snapshot_state` | Creates atomic Git commit snapshots linked to Run IDs, Artifacts, and Reports. |
| | `git_provenance_status` | Inspects Git repository state and verifies script reproducibility. |
| **Graphify Sync** | `graphify_sync_knowledge` | Updates `KNOWLEDGE_MAP.md` and rebuilds the local Graphify knowledge graph. |

---

## 💻 CLI Quickstart

```bash
# Check Git provenance status and reproducibility locking
sciresearch git status

# Record an atomic scientific Git snapshot
sciresearch git snapshot "Converged Pt (111) surface relaxation" --run-id run_pt111_01

# Inspect canvas artifacts and reports
sciresearch inspect --store all

# Audit artifact DAG dependencies
sciresearch audit <artifact_id>

# Search lifelong numerical failure traps
sciresearch facts --query "charge sloshing"

# Dual verification of simulation inputs against the Scientific Constitution
sciresearch verify INCAR --domain dft

# Sync documentation with Graphify knowledge graph
sciresearch sync
```

---

## 🧪 Testing

Run the full unit test suite:
```bash
pytest tests/test_sciresearch.py
```
All 13 tests validate:
- Anti-laundering context and identity checks
- DAG dependency traversal and ancestry verification
- Report immutability guarantees
- MDCrow checkpointing and session resumption
- TRITONDFT symmetry-first historical memory retrieval
- Ponytail zero-redundancy VASP input evaluation
- Lee & Rondinelli 8-rule convergence diagnostics
- Lifelong facts, traps, and procedural skill crystallization
- Rosetta dual verification and Scientific Constitution enforcement
- GENIUS multi-step protocol invariant tracking
- Git version controller status and reproducibility locking

---

## 📄 License & Attribution

This engine integrates open methodologies from:
- DREAMS (Z. Wang et al., *arXiv:2507.14267*)
- TRITONDFT (Z. Hu et al., *arXiv:2603.01258*)
- MDCrow (Q. Campbell et al., *ML:ST* 7, 025037, 2026)
- MDAgent (Y. Shi et al., *arXiv:2508.10931*)
- Multireference QC Agent (S. Lee & J. Rondinelli, *arXiv:2609.13357*)
- Lifelong Agent Memory (C. Liu et al., *arXiv:2602.04961*)
- GENIUS AEH (M. Soleymanibrojeni et al., *arXiv:2603.08053*)
- Rosetta Performance Modeling (K. Sankaralingam et al., *arXiv:2603.01895*)
- Systems Thinking (Donella H. Meadows, 2008)

Licensed under the [MIT License](LICENSE).
