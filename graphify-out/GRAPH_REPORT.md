# Graph Report - scientific-research  (2026-09-30)

## Corpus Check
- 143 files · ~1,379,905 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 80 file(s) not represented in the graph (top: .tex 35, (none) 13, .csv 8)

## Summary
- 600 nodes · 845 edges · 71 communities (49 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f140276`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- cli.py
- CanvasStore
- TestScientificResearchLog
- sthlmNord BeamerTheme
- HistoricalMemoryStore
- allocate
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
- site_zoom_annotator.py
- density_analyzer.py
- Sol27LC Benchmark Platinum Study Report a769b1
- Sol27LC Benchmark Platinum Study Report Unique
- Donella Meadows (2008): Thinking in Systems Applied to Scientific Agents
- adjustText/__init__.py
- PHOTH-Graphene Comprehensive Convergence Benchmarks & Supercell Scaling
- Multi-Cluster Distributed Execution and Convergence Milestones for Monolayer CrCl3 Systems
- Sol27LC Benchmark Platinum Study Report 18a8ee
- Sol27LC Benchmark Platinum Study Report 965f17
- Sol27LC Benchmark Platinum Study Report a1f321
- Multi-Cluster Distributed Execution & Baseline Benchmarks for Monolayer CrCl3
- Blender Crystal Render Skill
- convert_to_xsf
- textalloc/README.md
- style_config.py
- adjustText - automatic label placement for `matplotlib`
- textalloc
- ScientificEvaluator
- render_structure
- generate_demo_structure.py
- vesta_auto.py
- Core Principles & Typography
- GitController
- sync_graphify.sh
- SkillCrystallizer
- scripts/__init__.py
- GraphifyBridge
- mcp_server.py
- Site Pyramidalization & Circular Zoom Annotator
- .setUp
- latex_manager.py
- FactsStore
- LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`)

## God Nodes (most connected - your core abstractions)
1. `TestScientificResearchLog` - 25 edges
2. `CanvasStore` - 20 edges
3. `GitController` - 16 edges
4. `render_circular_site_zoom()` - 16 edges
5. `render_full_composite_figure()` - 16 edges
6. `CheckpointManager` - 15 edges
7. `allocate()` - 13 edges
8. `get_non_overlapping_boxes()` - 13 edges
9. `adjust_text()` - 12 edges
10. `analyze_site_geometry()` - 12 edges

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

## Communities (71 total, 3 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.19
Nodes (8): main(), ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, Unit tests for Scientific Research Log Skill & MCP Engine (21 Tools).

### Community 1 - "CanvasStore"
Cohesion: 0.21
Nodes (8): CanvasStore, Any, Traverses upstream DAG dependencies to produce an auditable provenance tree., Creates or updates a version-controlled, append-only working note. Validates…, Creates an immutable scientific report after auditing all claims against the…, Lists available keys and metadata across canvas stores., Reads a specific item from notes, artifacts, or reports., Registers an immutable tool output artifact with anti-laundering verification.…

### Community 3 - "sthlmNord BeamerTheme"
Cohesion: 0.11
Nodes (17): Block Environments, Libertinus fonts compiled with XeLaTeX, Light and Dark Mode Available, Lists, Major Features, Mathematics, Nord Color Palette, Other Nord Beamer themes (+9 more)

### Community 4 - "HistoricalMemoryStore"
Cohesion: 0.27
Nodes (5): HistoricalMemoryStore, Any, Stores physical and computational settings from a converged calculation., Two-stage retrieval: 1. Symmetry filtering (space group / crystal system) 2.…, Seeds curated reference calculations if the database is newly initialized.

### Community 5 - "allocate"
Cohesion: 0.08
Nodes (41): Figure, RendererBase, generate_candidates(), ndarray, Generates candidate boxes Args: w (float): width of box h (float): height of…, allocate(), allocate_text(), data_to_display() (+33 more)

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

### Community 27 - "site_zoom_annotator.py"
Cohesion: 0.09
Nodes (46): Patch, ScalarMappable, analyze_site_geometry(), auto_detect_sites(), compute_poav1(), export_geometry_report(), get_minimum_image_vector(), ndarray (+38 more)

### Community 28 - "density_analyzer.py"
Cohesion: 0.19
Nodes (14): compute_planar_potential(), export_to_xsf(), extract_3d_isosurface(), generate_2d_slice(), main(), parse_chgcar(), parse_cube(), Extract 3D polygonal isosurface using skimage.measure.marching_cubes and export… (+6 more)

### Community 29 - "Sol27LC Benchmark Platinum Study Report a769b1"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study Report a769b1, Verified Claims & Provenance Audit

### Community 30 - "Sol27LC Benchmark Platinum Study Report Unique"
Cohesion: 0.33
Nodes (5): Executive Summary, Finding 1: Equilibrium Parameter, Scientific Findings & Numerical Data, Sol27LC Benchmark Platinum Study Report Unique, Verified Claims & Provenance Audit

### Community 31 - "Donella Meadows (2008): Thinking in Systems Applied to Scientific Agents"
Cohesion: 0.40
Nodes (4): 1. Core Systems Principles Applied to AI Scientific Agents, 2. Springing the Archetypal System Traps in Scientific LLMs, 3. Top Leverage Points for Scientific Autonomous Systems, Donella Meadows (2008): Thinking in Systems Applied to Scientific Agents

### Community 32 - "adjustText/__init__.py"
Cohesion: 0.12
Nodes (27): arange_multi(), overlap_intervals(), Create concatenated ranges of integers for multiple start/length. Parameters…, Take two sets of intervals and return the indices of pairs of overlapping…, adjust_text(), apply_shifts(), expand_axes_to_fit(), expand_coords() (+19 more)

### Community 37 - "PHOTH-Graphene Comprehensive Convergence Benchmarks & Supercell Scaling"
Cohesion: 0.50
Nodes (3): 1. Executive Summary, 2. Supercell Transferability Rules (NotebookLM Grounded), PHOTH-Graphene Comprehensive Convergence Benchmarks & Supercell Scaling

### Community 40 - "Multi-Cluster Distributed Execution and Convergence Milestones for Monolayer CrCl3 Systems"
Cohesion: 0.50
Nodes (3): 1. Executive Status, 2. Infrastructure & Algorithmic Acceleration Opportunities, Multi-Cluster Distributed Execution and Convergence Milestones for Monolayer CrCl3 Systems

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

### Community 48 - "Blender Crystal Render Skill"
Cohesion: 0.07
Nodes (30): Blender Crystal Render Skill, Common Pitfalls & Solutions, Overview, Quick Reference, Script Options & Arguments, When to Use, Common Pitfalls & Solutions, Electron Density & Molecular Surfaces Skill (+22 more)

### Community 49 - "convert_to_xsf"
Cohesion: 0.17
Nodes (11): main(), parse_poscar(), Publication-Quality Photorealistic Crystal Structure Renderer using Blender.…, render_crystal(), read(), convert_to_xsf(), main(), Path (+3 more)

### Community 50 - "textalloc/README.md"
Cohesion: 0.15
Nodes (12): Examples, Features, Implementation and speed, Installation, Parameters, Plotting in 3D, Plotting on images and using transforms, Quick-start (+4 more)

### Community 51 - "style_config.py"
Cohesion: 0.15
Nodes (19): cycler, main(), plot_dataset(), CLI Tool for Generating Collision-Free Scientific Plots with Times New Roman &…, auto_adjust_labels(), ndarray, Scientific Publication Plotting & Typography Configuration. Enforces Times New…, Dual-format exporter: saves both 300 DPI PNG and vector PDF. (+11 more)

### Community 52 - "adjustText - automatic label placement for `matplotlib`"
Cohesion: 0.29
Nodes (6): adjustText - automatic label placement for `matplotlib`, Brief description, Citing **adjustText**, Documentation, Getting started, Installation

### Community 55 - "ScientificEvaluator"
Cohesion: 0.27
Nodes (5): Any, Executes the hierarchical 8-Rule Decision Ladder and Convergence Agent…, Appends an entry to logs/decisions.csv and updates EVIDENCE.md., Scores a simulation script (1-10) and flags redundant, dangerous, or unphysical…, ScientificEvaluator

### Community 56 - "render_structure"
Cohesion: 0.33
Nodes (3): main(), Headless Crystal Structure & Trajectory Renderer using OVITO and ASE. Renders…, render_structure()

### Community 57 - "generate_demo_structure.py"
Cohesion: 0.50
Nodes (3): create_porous_carbon_model(), Demo Structure Generator for Catalytic / Adsorption Sites. Creates a realistic…, Constructs a 2D porous carbon lattice (similar to the biphenylene/porous…

### Community 58 - "vesta_auto.py"
Cohesion: 0.67
Nodes (3): automate_vesta(), main(), VESTA GUI Automation & Multi-Axis Crystal Capture for X11. Automates window…

### Community 59 - "Core Principles & Typography"
Cohesion: 0.18
Nodes (11): 1. Typography & Mathematical Formats, 2. Label Anti-Collision Engines, 3. Python Integration Pattern, 4. Colorblind Accessibility & Colormaps, 5. VESTA Element Color Concordance, Common Pitfalls & Solutions, Core Principles & Typography, Overview (+3 more)

### Community 60 - "GitController"
Cohesion: 0.12
Nodes (14): CompletedProcess, CheckpointManager, Any, Reloads memory summaries, trace, parameter registry, and files for an…, Lists all runs with optional status and text search filtering., Appends a discrete milestone or action to the agent trace., Saves or updates a simulation run checkpoint and its dedicated run directory., GitController (+6 more)

### Community 62 - "SkillCrystallizer"
Cohesion: 0.24
Nodes (5): Any, Finds crystallized skills and procedures matching a natural language query or…, ===============================================================================…, Crystallizes an operational procedure into persistent memory and appends to…, SkillCrystallizer

### Community 63 - "scripts/__init__.py"
Cohesion: 0.25
Nodes (5): DualVerifier, Any, ===============================================================================…, Performs dual verification across Functional Correctness and Scientific…, Scientific Research Log Skill & MCP Engine package.

### Community 64 - "GraphifyBridge"
Cohesion: 0.25
Nodes (5): GraphifyBridge, Any, Regenerates knowledge documents and runs `graphify update .`, ===============================================================================…, Creates an interconnected Markdown summary linking all Notes, Reports,…

### Community 65 - "mcp_server.py"
Cohesion: 0.25
Nodes (7): ===============================================================================…, handle_tool_call(), main(), Any, ===============================================================================…, Dispatches tool calls to the underlying engine., Simple JSON-RPC 2.0 loop over stdin/stdout for MCP clients.

### Community 66 - "Site Pyramidalization & Circular Zoom Annotator"
Cohesion: 0.22
Nodes (8): 1. Vector Formulation, 2. Coordination Polyhedron, Options & Arguments, Overview, Physical Background: Haddon's POAV1 Pyramidalization, Quick Reference, Site Pyramidalization & Circular Zoom Annotator, When to Use

### Community 67 - ".setUp"
Cohesion: 0.25
Nodes (4): ProtocolEngine, Any, ===============================================================================…, AEH Stage 1: Static verification of multi-step simulation protocols.

### Community 68 - "latex_manager.py"
Cohesion: 0.40
Nodes (10): add_template(), clean_auxiliary(), compile_file(), list_templates(), load_catalog(), main(), new_project(), preview_file() (+2 more)

### Community 69 - "FactsStore"
Cohesion: 0.31
Nodes (4): FactsStore, Any, Records an empirical fact, failure warning, or boundary condition into lifelong…, Retrieves matching facts and warnings before launching expensive workflows.

### Community 70 - "LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`)"
Cohesion: 0.20
Nodes (9): 1. Scaffold a New Presentation, 2. Compile an Existing Document, 3. Generate PNG Previews, 4. Manage Templates Catalog, Directory Architecture, Features & Capabilities, LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`), Quick Reference CLI (+1 more)

## Knowledge Gaps
- **143 isolated node(s):** `sync_graphify.sh script`, `textalloc`, `1. Overview`, `2. Converged Benchmarks & Artifact Provenance`, `3. Hubbard U Dual Benchmark` (+138 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 331 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TestScientificResearchLog` connect `TestScientificResearchLog` to `cli.py`, `CanvasStore`, `GraphifyBridge`, `.setUp`, `HistoricalMemoryStore`, `FactsStore`, `ScientificEvaluator`, `GitController`, `SkillCrystallizer`, `scripts/__init__.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `CanvasStore` connect `CanvasStore` to `cli.py`, `TestScientificResearchLog`, `.setUp`, `GitController`, `scripts/__init__.py`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `auto_adjust_labels()` connect `style_config.py` to `adjustText/__init__.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `TestScientificResearchLog` (e.g. with `CanvasStore` and `CheckpointManager`) actually correct?**
  _`TestScientificResearchLog` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CanvasStore` (e.g. with `main()` and `GitController`) actually correct?**
  _`CanvasStore` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `GitController` (e.g. with `main()` and `CanvasStore`) actually correct?**
  _`GitController` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `sync_graphify.sh script`, `textalloc`, `1. Overview` to the rest of the system?**
  _143 weakly-connected nodes found - possible documentation gaps or missing edges._