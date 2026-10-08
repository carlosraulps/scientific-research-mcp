---
name: sciresearch
description: >-
  Scientific research logging, persistent shared memory, append-only provenance registry,
  MDCrow checkpoint tracking, TRITONDFT historical memory with symmetry-first retrieval,
  Liu et al. lifelong facts/traps memory, procedural skill crystallization, GENIUS multi-step
  protocol validation, Rosetta dual verification (functional vs scientific validity), MDAgent
  reflexion evaluator, Lee & Rondinelli 8-rule decision ladder, and seamless Graphify knowledge
  graph synchronization for DFT, MD, and multireference quantum chemistry.
---

# 🔬 Scientific Research Log & Persistent Shared Memory Superpower

Welcome to the **Scientific Research Log & Shared Memory Engine**. Grounded in 12 foundational research frameworks across autonomous LLM scientific agents and systems thinking (**DREAMS**, **TRITONDFT**, **MDCrow**, **MDAgent**, **Lee & Rondinelli**, **Liu et al.**, **GENIUS**, **MatSciAgent**, **Mi et al.**, **Simthesizer**, **Rosetta**, and **Meadows**), this framework provides persistent shared memory, append-only provenance tracking, simulation checkpointing, historical parameter retrieval, lifelong failure trap recording, procedural skill crystallization, and dual verification, integrated seamlessly with the local **Graphify** knowledge graph.

---

## 🏛️ Theoretical Foundations & Literature Architecture

| Framework | Literature Citation | Core Scientific Mechanism Implemented |
| :--- | :--- | :--- |
| **DREAMS** | Z. Wang et al., *arXiv:2507.14267* (2026) | **Centralized Shared Canvas** (Notes, Artifacts, Reports), **Append-Only Provenance Registry** (immutable 8-character hash IDs, DAG tracking, anti-laundering gates), and **Convergence Agent**. |
| **MDCrow** | Q. Campbell et al., *ML:ST* 7, 025037 (2026) | **Checkpoint-Based Memory**: Unique run directories (`/runs/<run_id>/`), serialized manifests (`checkpoints/<run_id>.json`), trajectory & parameter registries, session resumption without re-running setup. |
| **TRITONDFT** | Z. Hu et al., *arXiv:2603.03372* (2026) | **Historical Memory Mechanism**: Decoupled $\theta_{phy}$ (physical settings) & $\theta_{hpc}$ (HPC topology), **Symmetry-First Retrieval** (space group $\rightarrow$ crystal system $\rightarrow$ composition), Pareto accuracy tiers (<1, <10, <20 meV/atom). |
| **MDAgent** | Z. Shi et al., *Sci. Rep.* 15, 92337 (2025) | **Role Specialization** (Manager/Planner/Worker/Evaluator) & **Reflexion Error Loop**; static script evaluation (1-10 scoring) with structured deductions. |
| **Lee & Rondinelli** | V. C. Lee & J. M. Rondinelli, *arXiv:2609.13357* (2026) | **Context Partitioning** (`CLAUDE.md`, `TASK.md`, `EVIDENCE.md`, `/logs/decisions.csv`), **8-Rule Decision Ladder** (Rules A–H), and an **8-attempt recovery budget**. |
| **Liu et al.** | S. Liu et al., *arXiv:2608.11224* (2026) | **Lifelong Agent Memory**: Unified Memory Subsystem separating **Facts/Traps Store**, **Procedural Skills Store**, and **Links**, with cross-session continuous learning and `save_to_skill`. |
| **GENIUS** | M. Soleymanibrojeni et al., *Nat. Commun. Mater.* 7:115 (2026) | **Autonomous Protocol Design**: Two-Stage Automated Error Handling (**AEH Stage 1** static constraints vs. **AEH Stage 2** dynamic runtime convergence recovery). |
| **MatSciAgent** | A. Chaudhari et al., *Nat. Commun. Mater.* 7:131 (2025) | **Modular Multi-Task Architecture**: Domain-specific tool clusters (Data Retrieval, Structure Generation, Continuum Mechanics, and Molecular Dynamics) with deterministic extraction. |
| **Mi et al.** | Y. Mi et al., *arXiv:2504.04485* (2025) | **Computer Systems Memory Hierarchy**: Von Neumann mapping (Registers/L1 context $\rightarrow$ L2/L3 working memory $\rightarrow$ RAM database $\rightarrow$ Secondary storage knowledge graph) & context virtualization. |
| **Simthesizer** | W. Kim et al., *arXiv:2608.24650* (2026) | **Workload Simulation & Profiling**: Synthetic trace simulation estimating node-hours, disk I/O, and token budgets prior to cluster submission. |
| **Rosetta** | K. Sankaralingam, *arXiv:2609.19376* (2026) | **The Scientific Constitution**: Prohibits circular reasoning, enforces calibration-as-overlay, and establishes **Dual Verification** separating functional correctness from scientific validity. |
| **Meadows** | D. H. Meadows, *Thinking in Systems* (2008) | **Systems Leverage Points**: Balancing convergence loops, reinforcing lifelong memory accumulation, springing the "Rule Beating" and "Drift to Low Performance" system traps. |
| **Microsoft AI4Science** | AI4Science Team, *arXiv:2311.07361* (2023) | **Physical Geometry Sanity Guard**: Prevents POSCAR coordinate hallucinations, atomic overlaps (<0.8 Å), unphysical short bonds (<1.0 Å), and volume inversions. |
| **LLM4SR** | Z. Luo et al., *ACM Comput. Surv.* (2025) | **Hypothesis Discovery & Feedback**: 4-stage research loop, Novelty/Validity/Clarity/Feasibility multi-criteria feedback, and multi-inspiration association (LMI). |
| **HKUST Autonomy** | T. Zheng et al., *arXiv:2505.13259* (2025) | **Three-Tier Autonomy Taxonomy**: Progression from Level 1 (Tool) to Level 2 (Analyst) to Level 3 (Autonomous Scientist) navigating full-cycle scientific inquiry. |
| **SDE Benchmark** | Z. Song, C. Duan, H. Kulik et al., *arXiv:2512.15567* (2026) | **Closed-Loop Discovery Harness (`sde-harness`)**: Multi-round hypothesis testing against simulation oracles, anti-saturation sentinel preventing ungrounded linguistic loops. |
| **AI Engineering** | C. Huyen, *O'Reilly Media* (2025) | **Defense-in-Depth AI Architecture**: 5-step application framework, component-level evaluations, strict input/output guardrails, and hierarchical prompt/memory caching. |

---

## ⚡ Quick CLI Commands

The unified `sciresearch` utility is available directly on PATH:

```bash
# 1. Inspect Canvas stores (all, notes, artifacts, reports)
sciresearch inspect --store all

# 2. Audit complete upstream DAG provenance of any artifact or claim
sciresearch audit <artifact_id>

# 3. Query TRITONDFT Historical Memory for similar material parameters
sciresearch memory --formula Pt --space-group Fm-3m --crystal-system Cubic --tier high_precision

# 4. Search Liu et al. Lifelong Facts, Traps & Boundary Conditions
sciresearch facts --query "sloshing"
sciresearch facts --category trap --system "Pt(111)"

# 5. Search Crystallized Procedural Skills
sciresearch skills "charge sloshing"

# 6. Score simulation input script against Ponytail zero-redundancy and physical rules
sciresearch eval INCAR --engine vasp

# 7. Compose input file using Ponytail Delta Composer (anti-regeneration standard)
sciresearch compose --base base_templates/vasp/INCAR.base --set NSW=0 ISMEAR=-5 NEDOS=2001 LORBIT=11 --output 01_pristine/dos/INCAR

# 8. Rosetta Dual Verification (Functional Correctness + Scientific Validity)
sciresearch verify INCAR --domain dft

# 9. Structure Sanity Guard (Prevent coordinate hallucinations & atomic overlaps)
sciresearch guard-structure POSCAR

# 10. Multi-Dimensional Hypothesis Evaluation (Novelty, Validity, Clarity, Feasibility)
sciresearch eval-hypothesis "We hypothesize PHOTH-graphene band gap tuning with VASP..."

# 11. SDE Closed-Loop Discovery Verification (Multi-Round state & anti-saturation sentinel)
sciresearch sde-verify photh_project 1 "Hypothesis text..." --oracle --metric 1.25

# 8. List resumable simulation runs and checkpoints
sciresearch runs --status RUNNING

# 9. Synchronize Knowledge Map and update Graphify knowledge graph
sciresearch sync

# 10. Wyckoff symmetry orbit Bader standardization & PAW core offset
sciresearch bader-standardize ACF.dat --z-core 4.0 --element C

# 11. Zero-bloat remote extraction of 2D density slice (<500 KB)
sciresearch slice-2d CHGCAR --plane xy --z-slice 0.50 -o slice_z0.50.npz

# 12. Validate animation frames against the Zero-Dilation Rule
sciresearch validate-anim ./frames/frame_*.png

# 13. Quantify electronic strain descriptors across 2D states
sciresearch strain-metrics strain_electronic_metrics.csv

# 14. Audit scientific payload against Chip Huyen Defense-in-Depth Guardrails
sciresearch guardrail --stage input --file INCAR --domain vasp

# 15. Run isolated Component-Level evaluation across all agent modules
sciresearch test-components

# 16. Two-tier exact & semantic cache query / storage
sciresearch cache set --key pt111_her --text "Pt(111) HER free energy" --val '{"delta_G": -0.09}' --namespace her
sciresearch cache get --key pt111_her --namespace her
```

---

## 🔌 Model Context Protocol (MCP) Tool Suite (34 Tools)

The skill exposes 34 dedicated tools via the `sciresearch` MCP server (`sciresearch-mcp`):

### 1. DREAMS Shared Canvas & Provenance Store
* `canvas_register_artifact(producing_tool, value, arguments, rationales, sources, declared_context, sensitive_params)`:
  Registers an immutable tool output with an 8-character hash ID (`result_id`). Enforces anti-laundering rules: verifies referenced source IDs exist, prevents fake math/identity laundering, and validates declared scientific context.
* `audit_provenance_chain(result_id)`:
  Traverses upstream DAG dependencies to prove that every reported claim traces back to machine-verified simulation outputs.
* `canvas_write_note(title, content, tags, references)`:
  Creates or appends to a version-controlled, append-only note in `canvas/notes/`. Validates that all cited references exist in the artifact registry.
* `canvas_create_report(title, objective, executive_summary, findings, claims_with_provenance, author)`:
  Generates an audited scientific report in `canvas/reports/`. Audits all claims against the DAG. Once verified, the report becomes permanently immutable.
* `canvas_inspect(store)`:
  Lists available keys across Notes, Artifacts, and Reports.
* `canvas_read(store, key_or_id)`:
  Reads an item from Notes, Artifacts, or Reports.

### 2. MDCrow Checkpoint & Session Memory
* `checkpoint_save_run(run_id, prompt_summary, agent_trace, parameter_registry, file_paths, figures, metrics, status)`:
  Saves or updates a simulation checkpoint in `checkpoints/<run_id>.json` and initializes `/runs/<run_id>/`.
* `checkpoint_resume_run(run_id)`:
  Reloads context summaries, parameter dictionaries, and verified files to resume an interrupted or completed run.
* `checkpoint_list_runs(status_filter, query)`:
  Lists all simulation runs with status and text filtering.

### 3. TRITONDFT Historical Memory
* `memory_store_calculation(system_name, formula, space_group, crystal_system, volume, electron_count, theta_phy, theta_hpc, accuracy_tier, converged_energy, notes)`:
  Stores converged physical settings ($\theta_{phy}$) and HPC geometry ($\theta_{hpc}$) in SQLite database.
* `memory_retrieve_similar(formula, space_group, crystal_system, volume, electron_count, accuracy_tier, top_k)`:
  Uses symmetry-first two-stage retrieval to recommend Pareto-optimal starting settings for new materials.

### 4. Liu et al. Lifelong Memory & Skill Crystallization
* `memory_save_fact(category, material_or_system, statement, remediation, confidence, source_ref)`:
  Records an empirical fact, boundary condition, or failure trap into lifelong memory that persists across models.
* `memory_search_facts(query, category, material_or_system)`:
  Retrieves relevant facts, operational traps, and failure warnings prior to calculation execution.
* `skill_save_procedure(skill_name, description, trigger_conditions, procedure_code, validation_criteria)`:
  Crystallizes a verified error recovery or workflow into a permanent, reusable procedure synced with `SKILL.md`.
* `skill_search_procedures(query)`:
  Searches crystallized procedural skills matching an error signature or task.

### 5. GENIUS Protocol Engine & Rosetta Dual Verification
* `protocol_validate_multistep(workflow_name, steps, engine)`:
  AEH Stage 1 pre-flight validation of multi-step protocols for topological ordering and parameter invariance (functional, pseudopotentials).
* `verifier_dual_audit(code_or_spec, scientific_domain, claims, literature_overlays)`:
  Rosetta dual verification independently auditing Functional Correctness (syntax, execution) and Scientific Validity (Scientific Constitution, non-circularity, calibration-as-overlay).

### 6. MDAgent & Lee & Rondinelli Diagnostics
* `evaluator_score_input(calc_type, script_content, formula_or_system)`:
  Scores simulation scripts (1-10), checks Ponytail zero-redundancy rules, verifies timestep limits, and suggests optimizations.
* `diagnose_convergence_failure(engine, input_content, output_content, error_log, iteration_count)`:
  Applies the 8-Rule Decision Ladder and Convergence Agent rules to diagnose failures and recommend parameter modifications. Bounded by an 8-attempt recovery budget.
* `log_decision(run_id, step_name, hypothesis, intervention, outcome, rule_id, evidence_ref)`:
  Appends an entry to `logs/decisions.csv` and updates `EVIDENCE.md`.

### 7. Scientific Git Version Controller & Reproducibility Locking
* `git_snapshot_state(message, run_id, artifact_id, report_title, tag_report, push)`:
  Creates an atomic Git commit snapshot linking the workspace state (code, inputs, logs) to an active simulation Run ID, Artifact ID, or sealed Report. Optionally creates annotated Git tags.
* `git_provenance_status(target_files)`:
  Inspects Git repository state (commit hash, branch, dirty files) to assess simulation reproducibility and provenance locking.

### 8. Graphify Knowledge Graph Bridge
* `graphify_sync_knowledge()`:
  Generates `docs/KNOWLEDGE_MAP.md` cross-linking all research deliverables and executes `graphify update .` to keep the local graph current.

### 9. Scientific Visualization & Crystallographic Analysis
* `standardize_wyckoff_bader_charges(bader_data, wyckoff_mapping, z_core, tolerance, element)`:
  Standardizes Bader populations into crystallographic Wyckoff symmetry orbits ($\mathrm{C}_{\text{sub}}^{(\text{super})}$), applies PAW core charge offset ($q = Z_{\text{core}} - Q_{\text{Bader}}$), and diagnoses numerical Cartesian FFT grid splitting artifacts vs physical symmetry breaking.
* `extract_compact_2d_slice(source_path, output_path, z_slice, plane)`:
  Zero-Bloat Remote Slicing: Extracts 2D planar density cross sections at invariant crystallographic coordinates (e.g. $z = 0.50$ cutting through 2D sheet nuclei) from gigabyte-scale volumetric files (CHGCAR/LOCPOT/ELFCAR), compressing down to $<500\text{ KB}$ for lightweight transfer.
* `validate_animation_geometry(frame_paths, target_resolution)`:
  Zero-Dilation Rule Validator: Audits multi-frame scientific animation sequences to ensure 100% uniform pixel geometry ($W \times H$), detecting and preventing frame dilation jitter caused by `matplotlib` `bbox_inches="tight"`.
* `quantify_electronic_strain_metrics(band_data, reference_efermi)`:
  Quantifies electronic strain descriptors ($E_g$, $\Delta E_{\text{F}}(\varepsilon)$, $v_{\text{F}}$, $\Delta k_{\text{Dirac}}$, $p_z\text{ purity}$) across strained 2D allotropes, extracting chemical potential shifts and HER electrocatalytic electron injection mechanisms.

### 10. Chip Huyen AI Engineering Defense-in-Depth Suite (Chapters 3, 4, 10)
* `guardrails_audit_pipeline(stage, payload, domain, iteration_count, expected_metrics)`:
  Tri-stage defense-in-depth guardrail engine. Enforces credential non-disclosure (`.env`, private API keys), blocks monolithic 5-day Slurm walltimes, verifies AMD EPYC socket divisors (16, 32, 64, 128 cores), checks 8-attempt recovery limits, and confirms ground-state physics anchors (`reached required accuracy`, `E0=`).
* `evaluate_system_components(component_name)`:
  Isolated component-level evaluation benchmark suite. Runs automated unit tests on each registered agent module and generates a latency, error rate, and health scorecard (100% pass rate target).
* `cache_query(query_key, query_text, namespace, min_similarity)`:
  Hierarchical two-tier cache retrieval. Performs SHA-256 exact matching with semantic fallback (token set Jaccard similarity $\ge 0.85$) to eliminate redundant simulation queries and LLM token costs.
* `cache_store_entry(query_key, query_text, value, namespace, ttl_seconds)`:
  Stores expensive calculation manifests and verified physical properties in persistent SQLite cache with TTL expiration and LRU tracking.

---

## 📂 File-Based Context Structure

```
/home/cr/simulations/scientific-research/
├── CLAUDE.md                    # System policies, decision ladder, operational limits
├── TASK.md                      # Active execution loop tracking and subtask state
├── EVIDENCE.md                  # Theoretical justifications, literature benchmarks
├── SKILL.md                      # Unified skill definition & MCP tool documentation
├── canvas/
│   ├── notes/                   # Version-controlled append-only working notes
│   ├── artifacts/               # Immutable 8-character hashed tool outputs
│   └── reports/                 # Sealed immutable scientific reports
├── runs/<run_id>/               # Isolated input/output directories per simulation
├── checkpoints/<run_id>.json    # Resumable session state manifests
├── memory/
│   ├── historical_memory.db     # SQLite database for TRITONDFT parameters
│   ├── facts_memory.db          # SQLite database for Liu et al. facts & traps
│   └── skills_memory.db         # SQLite database for crystallized skills
├── logs/
│   ├── decisions.csv            # Tabular append-only audit trail
│   ├── results.csv              # Machine-readable verified physical values
│   └── artifacts_registry.json  # Master index of artifact DAG
├── skills/                      # Modular domain-specific agent skills
│   ├── reciprocal-space-visualizer/  # 3D Brillouin Zone, SeeK-path, k-paths, Wigner-Seitz
│   ├── povray-crystal-raytracer/     # POV-Ray 3.7 studio raytracing & realistic shadows
│   ├── avogadro-automation/          # Avogadro 2 & OpenBabel molecular builder & grafting
│   ├── pyprocar-electronic-suite/    # Fat bands, spin texture (Sx,Sy,Sz), band unfolding
│   ├── chargemol-ddec6/              # DDEC6 net atomic charges & atomic bond orders
│   ├── ifermi-surface-topology/      # 3D Fermi surfaces & Fermi velocity vector fields
│   ├── blender-crystal-render/       # Photorealistic ray-traced Blender crystal scenes
│   ├── electron-density-surfaces/    # CHGCAR/LOCPOT isosurfaces & 2D topological slices
│   ├── latex-template/               # Production LaTeX & Beamer presentation templates
│   ├── ovito-snapshot/               # Headless high-throughput structural snapshots
│   ├── publication-figure-formatter/ # Times New Roman & STIX publication figure styling
│   ├── site-pyramidalization-zoom/   # Polyhedral zoom insets & Haddon POAV1 pyramidalization
│   ├── vesta-automation/             # Headless VASTA CLI with Bound=0 spillover fix
│   └── xcrysden-visualizer/          # Fermi surfaces (BXSF) & Brillouin zone rendering
├── FUTURE_SKILLS_ROADMAP.md     # Architecture for deferred (LOBSTER, BoltzTraP2) & next-gen skills
└── graphify-out/                # Graphify persistent knowledge graph
```

---

## 🛠️ Specialized Subskills Ecosystem

All subskills in `skills/` are symlinked to `~/.gemini/config/skills/` and exposed directly across Antigravity CLI and multi-agent sessions:

| Skill | Primary CLI Utility | Core Scientific Function |
| :--- | :--- | :--- |
| **`reciprocal-space-visualizer`** | `bz-visualizer` | 3D Brillouin Zone Voronoi cells, SeeK-path standardization, 2D monolayers, VASP KPOINTS. |
| **`povray-crystal-raytracer`** | `povray-crystal-render` | Studio 3-point lighting, ground shadow receiver, metallic/dielectric materials via POV-Ray 3.7. |
| **`avogadro-automation`** | `avogadro-runner` | 3D molecular builder (SMILES), UFF/MMFF94 geometry optimization, slab adsorbate grafting. |
| **`pyprocar-electronic-suite`** | `pyprocar-suite` | Fat bands, $S_x, S_y, S_z$ spin texture, supercell band unfolding onto primitive BZ. |
| **`chargemol-ddec6`** | `chargemol-ddec6` | DDEC6 net atomic charges, atomic spin moments, pairwise atomic bond orders from VASP AECCARs. |
| **`ifermi-surface-topology`** | `ifermi-surface` | 3D Fermi surfaces in Wigner-Seitz cells, Fermi velocity $\mathbf{v}_{\mathrm{F}}$ vector fields, 2D Fermi slices. |
| **`vesta-automation`** | `generate-vstd` | Clean boundary rules (`Bound=0`), headless offscreen export, multi-view CDD isosurfaces. |
| **`publication-figure-formatter`**| `format-pub-fig` | Times New Roman typography, STIX math, collision-free annotations, journal aspect ratios. |
| **`electron-density-surfaces`** | `extract-slice-2d` | CHGCAR 3D isosurfaces, compact 2D slices ($<500\text{ KB}$), Bader Wyckoff standardization. |
| **`blender-crystal-render`** | `render-blender-crystal`| Cycles raytracing, glass/metal shaders, depth-of-field, studio softbox lighting. |

> **Deferred Candidates & Future Roadmap**: See [`FUTURE_SKILLS_ROADMAP.md`](file:///home/cr/simulations/scientific-research/FUTURE_SKILLS_ROADMAP.md) for specifications on **Skill 5** (`lobster-cohp-bonding`), **Skill 8** (`boltztrap2-transport`), and upcoming topological/vibrational skills (WannierBerri, Phonopy, Phono3py, VTST-NEB, universal MLIPs).



### Learned Skill: `test_charge_sloshing_fix`
- **Description**: Remedies severe charge sloshing on metallic slab surfaces
- **Trigger**: SCF non-convergence with oscillating dE
- **Validation**: Automated schema verification
```python
def fix_sloshing(incar):
    incar['AMIX'] = 0.2
    return incar
```


### Learned Skill: ``
- **Description**: Multi-view 3D Charge Density Difference (CDD) publication suite. Renders a, b, c, iso, and edge-on views of CDD volumetric files using VESTA headless CLI with dual isosurfaces (Gold accumulation, Cyan depletion at 60% opacity). Applies dynamic feature cropping, Layer Separation Protocol for badge compositing, and assembles unified multi-panel publication figure with Times New Roman typography.
- **Trigger**: 
- **Validation**: Automated schema verification
```python

```

### Learned Skill: `ponytail_delta_composition`
- **Description**: Declarative input delta composition and grounded self-documentation across simulation stages for VASP, SIESTA, and LAMMPS.
- **Trigger**: Transitioning from structural relaxation to static, DOS, bands, adsorption, or MD.
- **Validation**: Ponytail zero-redundancy passes, every mutated line annotated with rationale, no baseline drift.
```python
sciresearch compose --base base_templates/vasp/INCAR.base --set NSW=0 ISMEAR=-5 NEDOS=2001 LORBIT=11 --output 01_pristine/dos/INCAR
```
