# Graph Report - scientific-research  (2026-09-29)

## Corpus Check
- 96 files · ~440,550 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 4, .db 3, .csv 2)

## Summary
- 285 nodes · 380 edges · 48 communities
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5958522f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- __init__.py
- CanvasStore
- TestScientificResearchLog
- CheckpointManager
- HistoricalMemoryStore
- ScientificEvaluator
- MDCrow: Checkpoint-Based Memory & Session Resumption
- Sol27LC Benchmark Platinum Study
- Scientific Research Knowledge Map
- DREAMS: Shared Canvas & Append-Only Provenance Registry
- TritonDFT: Historical Memory & Symmetry-First Retrieval
- MDAgent: Role Specialization & Reflexion Evaluator Loop
- Liu et al. (2026): Lifelong Agent Memory for Materials Scientists
- GENIUS (2026): Autonomous Design & Execution of Simulation Protocols
- MatSciAgent (2025): Modular Multi-Task Materials Science Agents
- Mi et al. (2025): Computer Systems Insights for LLM Agents
- Simthesizer (2026): Agent-Driven Workload Simulation & Serving
- 3. Targeted Functional Enhancements for Global Deployment
- FactsStore
- SkillCrystallizer
- Sol27LC Benchmark Platinum Study Report a769b1
- Sol27LC Benchmark Platinum Study Report Unique
- Donella Meadows (2008): Thinking in Systems Applied to Scientific Agents
- GraphifyBridge
- PHOTH-Graphene Comprehensive Convergence Benchmarks & Supercell Scaling
- GitController
- Sol27LC Benchmark Platinum Study Report 18a8ee
- Sol27LC Benchmark Platinum Study Report 965f17
- Sol27LC Benchmark Platinum Study Report a1f321
- Multi-Cluster Distributed Execution & Baseline Benchmarks for Monolayer CrCl3

## God Nodes (most connected - your core abstractions)
1. `TestScientificResearchLog` - 25 edges
2. `CanvasStore` - 20 edges
3. `GitController` - 16 edges
4. `CheckpointManager` - 15 edges
5. `main()` - 10 edges
6. `FactsStore` - 10 edges
7. `HistoricalMemoryStore` - 10 edges
8. `ScientificEvaluator` - 10 edges
9. `SkillCrystallizer` - 9 edges
10. `GraphifyBridge` - 8 edges

## Surprising Connections (you probably didn't know these)
- `main()` --uses--> `CanvasStore`  [INFERRED]
  cli.py → scripts/canvas_store.py
- `main()` --uses--> `CheckpointManager`  [INFERRED]
  cli.py → scripts/checkpoint_manager.py
- `main()` --uses--> `DualVerifier`  [INFERRED]
  cli.py → scripts/dual_verifier.py
- `main()` --uses--> `FactsStore`  [INFERRED]
  cli.py → scripts/facts_store.py
- `main()` --uses--> `GitController`  [INFERRED]
  cli.py → scripts/git_controller.py

## Import Cycles
- None detected.

## Communities (48 total, 0 thin omitted)

### Community 0 - "__init__.py"
Cohesion: 0.11
Nodes (20): main(), ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================… (+12 more)

### Community 1 - "CanvasStore"
Cohesion: 0.21
Nodes (8): CanvasStore, Any, Traverses upstream DAG dependencies to produce an auditable provenance tree., Creates or updates a version-controlled, append-only working note. Validates…, Creates an immutable scientific report after auditing all claims against the…, Lists available keys and metadata across canvas stores., Reads a specific item from notes, artifacts, or reports., Registers an immutable tool output artifact with anti-laundering verification.…

### Community 2 - "TestScientificResearchLog"
Cohesion: 0.09
Nodes (7): DualVerifier, Any, Performs dual verification across Functional Correctness and Scientific…, ProtocolEngine, Any, AEH Stage 1: Static verification of multi-step simulation protocols., TestScientificResearchLog

### Community 3 - "CheckpointManager"
Cohesion: 0.24
Nodes (6): CheckpointManager, Any, Reloads memory summaries, trace, parameter registry, and files for an…, Lists all runs with optional status and text search filtering., Appends a discrete milestone or action to the agent trace., Saves or updates a simulation run checkpoint and its dedicated run directory.

### Community 4 - "HistoricalMemoryStore"
Cohesion: 0.27
Nodes (5): HistoricalMemoryStore, Any, Stores physical and computational settings from a converged calculation., Two-stage retrieval: 1. Symmetry filtering (space group / crystal system) 2.…, Seeds curated reference calculations if the database is newly initialized.

### Community 5 - "ScientificEvaluator"
Cohesion: 0.27
Nodes (5): Any, Executes the hierarchical 8-Rule Decision Ladder and Convergence Agent…, Appends an entry to logs/decisions.csv and updates EVIDENCE.md., Scores a simulation script (1-10) and flags redundant, dangerous, or unphysical…, ScientificEvaluator

### Community 6 - "MDCrow: Checkpoint-Based Memory & Session Resumption"
Cohesion: 0.29
Nodes (6): 1. Core Architecture & Scientific Problem, 2. Checkpoint-Based Memory System, 3. Resume & Troubleshoot Lifecycle, A. Unique Checkpoint Directories & Run IDs, B. Four Checkpoint Assets, MDCrow: Checkpoint-Based Memory & Session Resumption

### Community 7 - "Sol27LC Benchmark Platinum Study"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study, Verified Claims & Provenance Audit

### Community 8 - "Scientific Research Knowledge Map"
Cohesion: 0.33
Nodes (5): 1. DREAMS Shared Canvas Reports (Immutable Verified Deliverables), 2. Canvas Working Notes (Version-Controlled & Append-Only), 3. MDCrow Simulation Checkpoints (Resumable Runs), 4. Append-Only Provenance Registry Stats, Scientific Research Knowledge Map

### Community 9 - "DREAMS: Shared Canvas & Append-Only Provenance Registry"
Cohesion: 0.33
Nodes (5): 1. Core Architecture & Scientific Motivation, 2. Canvas Three-Store Topology, 3. Strict Provenance Rules (Anti-Laundering Gates), 4. Convergence Agent Patterns for DFT, DREAMS: Shared Canvas & Append-Only Provenance Registry

### Community 10 - "TritonDFT: Historical Memory & Symmetry-First Retrieval"
Cohesion: 0.40
Nodes (4): 1. Core Architecture & Scientific Problem, 2. Historical Memory Mechanism, 3. Pareto Accuracy-Cost Trade-Off Tiers, TritonDFT: Historical Memory & Symmetry-First Retrieval

### Community 11 - "MDAgent: Role Specialization & Reflexion Evaluator Loop"
Cohesion: 0.40
Nodes (4): 1. Multi-Agent Role Specialization, 2. Reflexion Error Feedback Loop, MDAgent: Role Specialization & Reflexion Evaluator Loop, Static Pre-Flight Rules Evaluated

### Community 13 - "Liu et al. (2026): Lifelong Agent Memory for Materials Scientists"
Cohesion: 0.40
Nodes (4): 1. Core Problem: The Decay of Operational Experience, 2. Lifelong Memory Architecture, 3. The Retrieve-Plan-Act-Reflect-Update Lifecycle, Liu et al. (2026): Lifelong Agent Memory for Materials Scientists

### Community 14 - "GENIUS (2026): Autonomous Design & Execution of Simulation Protocols"
Cohesion: 0.40
Nodes (4): 1. Core Architecture & Scientific Motivation, 2. Two-Stage Automated Error Handling (AEH), 3. Best Practices for Protocol Design, GENIUS (2026): Autonomous Design & Execution of Simulation Protocols

### Community 15 - "MatSciAgent (2025): Modular Multi-Task Materials Science Agents"
Cohesion: 0.50
Nodes (3): 1. Modular Multi-Agent Architecture, 2. Key Methodological Lessons, MatSciAgent (2025): Modular Multi-Task Materials Science Agents

### Community 16 - "Mi et al. (2025): Computer Systems Insights for LLM Agents"
Cohesion: 0.50
Nodes (3): 1. The von Neumann Analogy for LLM Agents, 2. Core Systems Principles Applied to Scientific Agents, Mi et al. (2025): Computer Systems Insights for LLM Agents

### Community 17 - "Simthesizer (2026): Agent-Driven Workload Simulation & Serving"
Cohesion: 0.50
Nodes (3): 1. Core Problem & Concept, 2. Key Methodological Lessons for Scientific Research Skills, Simthesizer (2026): Agent-Driven Workload Simulation & Serving

### Community 26 - "3. Targeted Functional Enhancements for Global Deployment"
Cohesion: 0.17
Nodes (11): 1. Executive Vision, 2. Four-Tier Memory & Systems Hierarchy (Mi et al. & Liu et al.), 3. Targeted Functional Enhancements for Global Deployment, 4. Implementation Roadmap & Phased Execution, Blueprint: Global Architecture & Continuous Improvement Plan, Milestone 1: Lifelong Continuous Memory & Skill Crystallization (Liu et al.), Milestone 2: Two-Stage Automated Error Handling & Protocol Generation (GENIUS), Milestone 3: Modular Multi-Task Tool Routing (MatSciAgent) (+3 more)

### Community 27 - "FactsStore"
Cohesion: 0.31
Nodes (4): FactsStore, Any, Records an empirical fact, failure warning, or boundary condition into lifelong…, Retrieves matching facts and warnings before launching expensive workflows.

### Community 28 - "SkillCrystallizer"
Cohesion: 0.32
Nodes (4): Any, Finds crystallized skills and procedures matching a natural language query or…, Crystallizes an operational procedure into persistent memory and appends to…, SkillCrystallizer

### Community 29 - "Sol27LC Benchmark Platinum Study Report a769b1"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study Report a769b1, Verified Claims & Provenance Audit

### Community 30 - "Sol27LC Benchmark Platinum Study Report Unique"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study Report Unique, Verified Claims & Provenance Audit

### Community 31 - "Donella Meadows (2008): Thinking in Systems Applied to Scientific Agents"
Cohesion: 0.40
Nodes (4): 1. Core Systems Principles Applied to AI Scientific Agents, 2. Springing the Archetypal System Traps in Scientific LLMs, 3. Top Leverage Points for Scientific Autonomous Systems, Donella Meadows (2008): Thinking in Systems Applied to Scientific Agents

### Community 32 - "GraphifyBridge"
Cohesion: 0.33
Nodes (4): GraphifyBridge, Any, Regenerates knowledge documents and runs `graphify update .`, Creates an interconnected Markdown summary linking all Notes, Reports,…

### Community 37 - "PHOTH-Graphene Comprehensive Convergence Benchmarks & Supercell Scaling"
Cohesion: 0.50
Nodes (3): 1. Executive Summary, 2. Supercell Transferability Rules (NotebookLM Grounded), PHOTH-Graphene Comprehensive Convergence Benchmarks & Supercell Scaling

### Community 40 - "GitController"
Cohesion: 0.24
Nodes (8): CompletedProcess, GitController, Any, Creates an atomic Git commit snapshot linking the workspace state to active…, Evaluates whether a simulation setup is strictly reproducible from Git., Helper to run git commands in the base directory., Checks if base_dir is inside an active git repository., Retrieves current git repository state for scientific audit trails.

### Community 41 - "Sol27LC Benchmark Platinum Study Report 18a8ee"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study Report 18a8ee, Verified Claims & Provenance Audit

### Community 43 - "Sol27LC Benchmark Platinum Study Report 965f17"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study Report 965f17, Verified Claims & Provenance Audit

### Community 44 - "Sol27LC Benchmark Platinum Study Report a1f321"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study Report a1f321, Verified Claims & Provenance Audit

### Community 45 - "Multi-Cluster Distributed Execution & Baseline Benchmarks for Monolayer CrCl3"
Cohesion: 0.40
Nodes (4): 1. Overview, 2. Converged Benchmarks & Artifact Provenance, 3. Hubbard U Dual Benchmark, Multi-Cluster Distributed Execution & Baseline Benchmarks for Monolayer CrCl3

## Knowledge Gaps
- **64 isolated node(s):** `1. Overview`, `2. Converged Benchmarks & Artifact Provenance`, `3. Hubbard U Dual Benchmark`, `1. Executive Summary`, `2. Supercell Transferability Rules (NotebookLM Grounded)` (+59 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 168 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TestScientificResearchLog` connect `TestScientificResearchLog` to `__init__.py`, `CanvasStore`, `GraphifyBridge`, `CheckpointManager`, `HistoricalMemoryStore`, `ScientificEvaluator`, `GitController`, `FactsStore`, `SkillCrystallizer`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `CanvasStore` connect `CanvasStore` to `__init__.py`, `GitController`, `TestScientificResearchLog`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `GitController` connect `GitController` to `__init__.py`, `CanvasStore`, `TestScientificResearchLog`, `CheckpointManager`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `TestScientificResearchLog` (e.g. with `CanvasStore` and `CheckpointManager`) actually correct?**
  _`TestScientificResearchLog` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CanvasStore` (e.g. with `main()` and `GitController`) actually correct?**
  _`CanvasStore` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `GitController` (e.g. with `main()` and `CanvasStore`) actually correct?**
  _`GitController` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CheckpointManager` (e.g. with `main()` and `GitController`) actually correct?**
  _`CheckpointManager` has 4 INFERRED edges - model-reasoned connections that need verification._