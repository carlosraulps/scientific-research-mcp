# Blueprint: Global Architecture & Continuous Improvement Plan
## Scientific Research Log & Persistent Shared Memory Superpower (`sciresearch`)

---

## 1. Executive Vision
The goal of this project is to evolve `sciresearch` from a local session-logging utility into a **Globally Deployed, Operating-System-Grade Autonomous Scientific Research Framework**. 

By synthesizing the ten foundational papers:
- **DREAMS** (*Wang et al., 2026*): Anti-laundering provenance DAG and 3-store canvas.
- **MDCrow** (*Campbell et al., 2026*): Checkpoint-based memory and non-blocking session resumption.
- **TRITONDFT** (*Hu et al., 2026*): Decoupled $\theta_{phy} / \theta_{hpc}$ memory and symmetry-first retrieval.
- **MDAgent** (*Shi et al., 2025*): Reflexion pre-flight evaluator with structured scoring (1–10).
- **Lee & Rondinelli** (*2026*): File-based context partitioning, 8-Rule Decision Ladder, and 8-attempt recovery budget.
- **Liu et al.** (*2026*): Lifelong agent memory (Facts, Skills, continuous accumulation, cross-model inheritance).
- **GENIUS** (*Soleymanibrojeni et al., 2026*): Automated protocol design and two-stage error handling (AEH).
- **MatSciAgent** (*Chaudhari et al., 2025*): Modular multi-task domain routing.
- **Mi et al.** (*2025*): Computer systems memory hierarchy and context paging.
- **Simthesizer** (*Kim et al., 2026*): Workload execution simulation and token/node-hour profiling.

---

## 2. Four-Tier Memory & Systems Hierarchy (Mi et al. & Liu et al.)

```
┌────────────────────────────────────────────────────────────────────────┐
│ LEVEL 1: REGISTERS & L1 CACHE (Ultra-Fast, Volatile)                   │
│ - Active LLM Context Window (System Prompt, Scratchpad)               │
│ - Active Subtask State & Step Counter (TASK.md)                        │
├────────────────────────────────────────────────────────────────────────┤
│ LEVEL 2: L2/L3 CACHE (Working Memory & Session Checkpoints)            │
│ - DREAMS Canvas Notes (notes/*.md) & Active Run State (/runs/<run_id>/)│
│ - MDCrow Serialized Session Checkpoints (checkpoints/<run_id>.json)    │
├────────────────────────────────────────────────────────────────────────┤
│ LEVEL 3: MAIN MEMORY / RAM (Indexed High-Speed Storage)                │
│ - DREAMS Append-Only Provenance Registry (artifacts_registry.json)     │
│ - TRITONDFT Historical Memory Database (historical_memory.db)         │
│ - Liu et al. Structured Facts & Warnings Store (facts_memory.db)       │
├────────────────────────────────────────────────────────────────────────┤
│ LEVEL 4: SECONDARY STORAGE / DISK (Global Persistent Knowledge)        │
│ - Graphify Knowledge Graph (graphify-out/graph.json)                   │
│ - Sealed Immutable Scientific Reports (canvas/reports/*.md)            │
│ - Global Reusable Skills Registry (~/.gemini/config/skills/)           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Targeted Functional Enhancements for Global Deployment

### Milestone 1: Lifelong Continuous Memory & Skill Crystallization (Liu et al.)
- **Facts & Traps Registry**: Extend SQLite database to record materials traps and operational warnings (e.g., "Pt(111) CO adsorption requires dipole correction along z", "Perovskite SrTiO3 requires explicit G-type antiferromagnetic check").
- **Dynamic Skill Synthesis (`save_to_skill`)**: When the agent resolves an intricate simulation bug using the 8-Rule Decision Ladder, it automatically synthesizes a self-contained skill documentation or script and appends it to `SKILL.md` or a global skills repository.
- **Cross-Model / Cross-Session Portability**: Facts and skills are stored in standardized, human-readable markdown and JSON, ensuring future models (Claude 4, Gemini 2.0/3.0, GPT-5) immediately inherit past research experience.

### Milestone 2: Two-Stage Automated Error Handling & Protocol Generation (GENIUS)
- **Smart Knowledge Graph Protocol Synthesizer**: Expand `canvas_create_report` and evaluator tools to automatically construct end-to-end multi-step protocols (Relaxation $\rightarrow$ Static SCF $\rightarrow$ Band Structure / DOS $\rightarrow$ Elastic Constants) with validated parameter consistency across steps.
- **Stage 1 Static Pre-Flight Guard (AEH-1)**: Check pseudopotential compatibility, k-point density per reciprocal volume ($k \times a \ge 30$), and unphysical tag combinations prior to cluster dispatch.
- **Stage 2 Dynamic Runtime Remediation (AEH-2)**: Connect runtime diagnostics directly to Slurm job monitors to automatically catch node crashes and submit micro-batch continuations without human intervention.

### Milestone 3: Modular Multi-Task Tool Routing (MatSciAgent)
- **Domain-Specific Tool Clusters**: Partition the MCP server into modular namespaces:
  - `materials_retrieval`: Materials Project, MatWeb, OQMD, NIST potentials.
  - `structure_generation`: Symmetry space group builders, supercells, surface slab generators with vacuum padding.
  - `first_principles_sim`: VASP, Quantum ESPRESSO, ORCA.
  - `classical_md_sim`: LAMMPS, OpenMM, GROMACS.
- **Dynamic Routing**: The master agent dynamically loads and queries only the relevant tool cluster, preventing context pollution.

### Milestone 4: Synthetic Workload & Cost Simulation (Simthesizer)
- **Pre-Flight Resource Profiler**: Before submitting a 100-structure sweep, calculate estimated CPU-core hours, disk I/O volume (suppressing redundant DOSCAR/PROCAR files per Ponytail rules), and queue latency using the `server-info` superpower.
- **Pareto Trade-off Simulator**: Recommend whether a calculation should run in Coarse (<20 meV/atom), Standard (<10 meV/atom), or High-Precision (<1 meV/atom) mode based on user accuracy targets and cluster resource constraints.

### Milestone 5: Seamless Global System Integration
- **Global Path Discovery**: Ensure `sciresearch` and `sciresearch-mcp` are available in `/usr/local/bin/` or `~/.local/bin/` and detected by all agent clients (Antigravity CLI, Antigravity IDE, Claude Code, Cursor, Codex).
- **Automated Graphify Synchronization**: Add an event hook (`on_artifact_registered`, `on_report_sealed`) that automatically updates `graphify-out/` in the background with zero token overhead.

---

## 4. Implementation Roadmap & Phased Execution

```
[ Phase 1: Foundation (Current) ]
├── DREAMS 3-store Canvas + Provenance DAG (Done)
├── MDCrow Checkpoints & Session Resume (Done)
├── TRITONDFT Symmetry-first Historical Memory (Done)
├── MDAgent Evaluator & Lee 8-Rule Decision Ladder (Done)
└── Graphify Bridge & 15 MCP Tools (Done)
           │
           ▼
[ Phase 2: Lifelong Memory & Protocol Synthesis ]
├── Liu et al. Facts & Failure Traps Registry
├── GENIUS Two-Stage Automated Error Handling (AEH-1 & AEH-2)
└── Automated Skill Crystallization (`save_to_skill`)
           │
           ▼
[ Phase 3: Multi-Domain Modular Routing & Workload Profiling ]
├── MatSciAgent Domain-Specific Tool Clusters
├── Simthesizer HPC Cost & Latency Estimator
└── Multi-Cluster Micro-Batch Dispatch Integration
           │
           ▼
[ Phase 4: Global Deployment & Continuous Verification ]
├── Global PATH & multi-client MCP registration
└── Background Graphify auto-sync daemon
```
