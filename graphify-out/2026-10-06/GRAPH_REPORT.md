# Graph Report - scientific-research  (2026-10-06)

## Corpus Check
- 186 files · ~1,406,050 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 80 file(s) not represented in the graph (top: .tex 35, (none) 13, .csv 8)

## Summary
- 866 nodes · 1245 edges · 84 communities (60 shown, 5 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9e063c62`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- mcp_server.py
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
- Key Capabilities & Scientific Protocols
- render_blender.py
- textalloc/README.md
- style_config.py
- adjustText - automatic label placement for `matplotlib`
- textalloc
- ScientificEvaluator
- render_structure
- generate_demo_structure.py
- vesta_cdd.py
- Key Capabilities & Scientific Protocols
- GitController
- sync_graphify.sh
- SkillCrystallizer
- .setUp
- GraphifyBridge
- scripts/__init__.py
- Site Pyramidalization & Circular Zoom Annotator
- auto_slice_2d.py
- latex_manager.py
- FactsStore
- LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`)
- volumetric_unwrap.py
- Transition Metal Adsorption Competition Suite on CrCl3 (2x2) Monolayer - 100% Completed
- compose_animation
- composite_panels
- run_bader_protocol
- Key Capabilities & Scientific Protocols
- PHOTH-Graphene HER Electrocatalysis & Mechanical Strain Suite
- vesta_auto.py
- animate_3d_cdd.py
- composite_badge
- photh_graphene_remote_sync_and_c5_piezo_matrix_v1.md
- Authentic VESTA Headless CLI 3D CDD Isosurface Animation
- brillouin_zone_visualizer.py

## God Nodes (most connected - your core abstractions)
1. `TestScientificResearchLog` - 25 edges
2. `CanvasStore` - 20 edges
3. `GitController` - 16 edges
4. `render_circular_site_zoom()` - 16 edges
5. `render_full_composite_figure()` - 16 edges
6. `CheckpointManager` - 15 edges
7. `main()` - 14 edges
8. `render_structure()` - 14 edges
9. `allocate()` - 13 edges
10. `get_non_overlapping_boxes()` - 13 edges

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

## Communities (84 total, 5 thin omitted)

### Community 0 - "mcp_server.py"
Cohesion: 0.14
Nodes (13): ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================…, ===============================================================================… (+5 more)

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

### Community 48 - "Key Capabilities & Scientific Protocols"
Cohesion: 0.05
Nodes (40): Blender Crystal Render Skill, Common Pitfalls & Solutions, Overview, Quick Reference, Script Options & Arguments, When to Use, 1. Padded Coordinate Tripod Overlay, 2. Calibrated 2D Material & Carbon Presets (`--preset 2d-carbon`) (+32 more)

### Community 49 - "render_blender.py"
Cohesion: 0.28
Nodes (5): main(), parse_poscar(), Publication-Quality Photorealistic Crystal Structure Renderer using Blender.…, render_crystal(), read()

### Community 50 - "textalloc/README.md"
Cohesion: 0.15
Nodes (12): Examples, Features, Implementation and speed, Installation, Parameters, Plotting in 3D, Plotting on images and using transforms, Quick-start (+4 more)

### Community 51 - "style_config.py"
Cohesion: 0.09
Nodes (30): cycler, main(), plot_dataset(), CLI Tool for Generating Collision-Free Scientific Plots with Times New Roman &…, generate_demo_suite(), ndarray, Path, Generates a synthetic demo coupled Band + PDOS figure. (+22 more)

### Community 52 - "adjustText - automatic label placement for `matplotlib`"
Cohesion: 0.29
Nodes (6): adjustText - automatic label placement for `matplotlib`, Brief description, Citing **adjustText**, Documentation, Getting started, Installation

### Community 55 - "ScientificEvaluator"
Cohesion: 0.27
Nodes (5): Any, Executes the hierarchical 8-Rule Decision Ladder and Convergence Agent…, Appends an entry to logs/decisions.csv and updates EVIDENCE.md., Scores a simulation script (1-10) and flags redundant, dangerous, or unphysical…, ScientificEvaluator

### Community 56 - "render_structure"
Cohesion: 0.08
Nodes (28): composite_image_with_colorbar(), generate_publication_colorbar(), Path, Horizontally composites an OVITO crystal snapshot with the publication colorbar., ===============================================================================…, Renders a standalone publication-quality vector and raster colorbar., apply_presets(), main() (+20 more)

### Community 57 - "generate_demo_structure.py"
Cohesion: 0.50
Nodes (3): create_porous_carbon_model(), Demo Structure Generator for Catalytic / Adsorption Sites. Creates a realistic…, Constructs a 2D porous carbon lattice (similar to the biphenylene/porous…

### Community 58 - "vesta_cdd.py"
Cohesion: 0.10
Nodes (29): build_cdd_isosurface_section(), build_sbond_section(), estimate_bond_cutoffs(), extract_species_from_structure(), generate_vesta_project_content(), generate_vstd_content(), main(), Path (+21 more)

### Community 59 - "Key Capabilities & Scientific Protocols"
Cohesion: 0.12
Nodes (15): 10. Programmatic Zero-Dilation Auditing, 1. The Zero-Dilation Rule for Scientific Animations (`format-animation`), 2. Comfortable Animation Pacing Protocol, 3. Header Clearance & Overlap Prevention, 4. Coupled Band Structure + PDOS Architecture (`render-coupled-suite`), 5. Label Anti-Collision Engines, 6. 3D Volumetric Animations (`animate-cdd`), 7. Multi-View CDD Panel (`render-cdd-suite`) (+7 more)

### Community 60 - "GitController"
Cohesion: 0.12
Nodes (14): CompletedProcess, CheckpointManager, Any, Reloads memory summaries, trace, parameter registry, and files for an…, Lists all runs with optional status and text search filtering., Appends a discrete milestone or action to the agent trace., Saves or updates a simulation run checkpoint and its dedicated run directory., GitController (+6 more)

### Community 62 - "SkillCrystallizer"
Cohesion: 0.32
Nodes (4): Any, Finds crystallized skills and procedures matching a natural language query or…, Crystallizes an operational procedure into persistent memory and appends to…, SkillCrystallizer

### Community 63 - ".setUp"
Cohesion: 0.18
Nodes (6): DualVerifier, Any, Performs dual verification across Functional Correctness and Scientific…, ProtocolEngine, Any, AEH Stage 1: Static verification of multi-step simulation protocols.

### Community 64 - "GraphifyBridge"
Cohesion: 0.33
Nodes (4): GraphifyBridge, Any, Regenerates knowledge documents and runs `graphify update .`, Creates an interconnected Markdown summary linking all Notes, Reports,…

### Community 65 - "scripts/__init__.py"
Cohesion: 0.16
Nodes (19): main(), Scientific Research Log Skill & MCP Engine package., handle_tool_call(), main(), Any, Dispatches tool calls to the underlying engine., Simple JSON-RPC 2.0 loop over stdin/stdout for MCP clients., extract_compact_2d_slice() (+11 more)

### Community 66 - "Site Pyramidalization & Circular Zoom Annotator"
Cohesion: 0.22
Nodes (8): 1. Vector Formulation, 2. Coordination Polyhedron, Options & Arguments, Overview, Physical Background: Haddon's POAV1 Pyramidalization, Quick Reference, Site Pyramidalization & Circular Zoom Annotator, When to Use

### Community 67 - "auto_slice_2d.py"
Cohesion: 0.10
Nodes (32): auto_slice_and_render(), compute_3point_plane(), find_monolayer_z_plane(), main(), ndarray, Path, ===============================================================================…, Finds the mean fractional z-coordinate of the 2D material sheet and identifies… (+24 more)

### Community 68 - "latex_manager.py"
Cohesion: 0.40
Nodes (10): add_template(), clean_auxiliary(), compile_file(), list_templates(), load_catalog(), main(), new_project(), preview_file() (+2 more)

### Community 69 - "FactsStore"
Cohesion: 0.31
Nodes (4): FactsStore, Any, Records an empirical fact, failure warning, or boundary condition into lifelong…, Retrieves matching facts and warnings before launching expensive workflows.

### Community 70 - "LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`)"
Cohesion: 0.20
Nodes (9): 1. Scaffold a New Presentation, 2. Compile an Existing Document, 3. Generate PNG Previews, 4. Manage Templates Catalog, Directory Architecture, Features & Capabilities, LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`), Quick Reference CLI (+1 more)

### Community 71 - "volumetric_unwrap.py"
Cohesion: 0.23
Nodes (15): auto_center_feature(), extract_2d_slice(), main(), plot_slice(), ndarray, Automatically detect the reactive feature and center it. Args: grid_data: 3D…, Write back the unwrapped CHGCAR with same header format., Extract a 2D slice from the 3D volumetric grid. Args: grid_data: 3D numpy array… (+7 more)

### Community 72 - "Transition Metal Adsorption Competition Suite on CrCl3 (2x2) Monolayer - 100% Completed"
Cohesion: 0.50
Nodes (3): Key Results Summary:, Transition Metal Adsorption Competition Suite on CrCl3 (2x2) Monolayer - 100% Completed, Updated Publication Figures:

### Community 73 - "compose_animation"
Cohesion: 0.21
Nodes (14): build_ping_pong_sequence(), calculate_frame_durations(), compose_animation(), main(), parse_numeric_label(), Image, Path, Composes a publication-grade animated GIF obeying the Zero-Dilation Rule. (+6 more)

### Community 74 - "composite_panels"
Cohesion: 0.23
Nodes (11): FreeTypeFont, composite_panels(), get_serif_font(), main(), Image, Path, ===============================================================================…, Trims uniform background padding from a panel while retaining specified border… (+3 more)

### Community 75 - "run_bader_protocol"
Cohesion: 0.27
Nodes (11): main(), parse_acf_dat(), prepare_total_charge_reference(), Path, Parses Henkelman Bader ACF.dat output file. Columns: # X Y Z CHARGE MIN_DIST…, Executes the robust flux-weighted Bader charge protocol., ===============================================================================…, Extracts species list and Cartesian coordinates from POSCAR/CONTCAR. (+3 more)

### Community 76 - "Key Capabilities & Scientific Protocols"
Cohesion: 0.18
Nodes (10): 1. Bader Charge Partitioning Protocol (`bader-analyze`), 2. 3D Isosurface Extraction & Wavefront OBJ Export, 3. 2D Topological Slicing & Laplacian Mapping, 4. Planar-Averaged Potential & Work Function, 5. Volumetric Grid Periodic Unwrapping, Electron Density & Molecular Surfaces Skill, Key Capabilities & Scientific Protocols, Overview (+2 more)

### Community 78 - "vesta_auto.py"
Cohesion: 0.11
Nodes (24): batch_render_directory(), main(), Path, ===============================================================================…, Renders all matching crystal structures in input_dir and builds a summary…, automate_vesta_gui(), find_vesta_binary(), main() (+16 more)

### Community 79 - "animate_3d_cdd.py"
Cohesion: 0.27
Nodes (9): crossfade(), main(), Image, 3D Volumetric Animation Engine for creating publication-quality CDD animations:…, Compose pre-rendered rotation frames into a smooth GIF., Blend two PIL images with alpha crossfade., Create strain breathing cycle animation. Uses comfortable pacing from Zero-…, render_rotation_gif() (+1 more)

### Community 80 - "composite_badge"
Cohesion: 0.36
Nodes (8): composite_badge(), dynamic_feature_crop(), main(), Image, Full pipeline: crop -> sanitize borders -> composite badge LAST., Crops VESTA render to structural features using saturation-based detection.…, Composites orientation badge AFTER cropping (Layer Separation Protocol). This…, sanitize_vesta_render()

### Community 82 - "Authentic VESTA Headless CLI 3D CDD Isosurface Animation"
Cohesion: 0.40
Nodes (4): Authentic VESTA Headless CLI 3D CDD Isosurface Animation, Executive Summary, Key Advancements, Output Files

### Community 83 - "brillouin_zone_visualizer.py"
Cohesion: 0.27
Nodes (11): compute_brillouin_zone_voronoi(), compute_reciprocal_lattice(), main(), parse_poscar_lattice(), ndarray, Renders 3D publication-quality Brillouin zone figure., ===============================================================================…, Extracts 3x3 lattice vector matrix from VASP POSCAR. (+3 more)

## Knowledge Gaps
- **168 isolated node(s):** `sync_graphify.sh script`, `textalloc`, `Executive Summary`, `Key Advancements`, `Output Files` (+163 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 469 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_structure()` connect `site_zoom_annotator.py` to `render_blender.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `read()` connect `render_blender.py` to `auto_slice_2d.py`, `site_zoom_annotator.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `convert_to_xsf()` connect `auto_slice_2d.py` to `render_blender.py`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `TestScientificResearchLog` (e.g. with `CanvasStore` and `CheckpointManager`) actually correct?**
  _`TestScientificResearchLog` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `CanvasStore` (e.g. with `main()` and `GitController`) actually correct?**
  _`CanvasStore` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `GitController` (e.g. with `main()` and `CanvasStore`) actually correct?**
  _`GitController` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `sync_graphify.sh script`, `textalloc`, `Executive Summary` to the rest of the system?**
  _168 weakly-connected nodes found - possible documentation gaps or missing edges._