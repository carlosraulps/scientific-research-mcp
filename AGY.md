# 🔬 AGY Autonomous Scientific Research Operating Standard (AGY.md)
**Frameworks**: Lee & Rondinelli (2026), DREAMS (2026), TRITONDFT (2026), MDCrow (2026), Ponytail Protocol, Graphify.
**Target Agent**: Antigravity CLI / AGY 2.0 Autonomous Scientist
**Applies To**: Density Functional Theory (VASP, SIESTA, QE) and Molecular Dynamics (LAMMPS)

---

## 1. Core Operational Policies & Non-Negotiables

### 1. Zero Hallucinated or Laundered Data
- Every reported numerical parameter, cutoff, or physical claim **MUST** cite a verifiable 8-character DREAMS artifact hash (`#b7703ad6`) or a literature source.
- Sensitive convergence parameters (`ENCUT`, `kpoints`, `MeshCutoff`, `timestep`, `smearing`) must be sourced from an upstream convergence benchmark in `00_convergence/` or TRITONDFT historical memory.

### 2. The Ponytail Zero-Redundancy Principle
- **Never redefine built-in engine defaults**:
  - In **VASP**: Do not specify `ALGO = Normal`, `ISIF = 2` when `IBRION = 2`, `LDAUTYPE = 2`, `LDAUJ = 0 0`, `LWAVE = .TRUE.`, `LCHARG = .TRUE.`, `SYSTEM`, or `POTIM = 0.5`.
  - In **SIESTA**: Do not redefine default PAO energy shifts or default diagonalizers unless overriding.
  - In **LAMMPS**: Do not repeat force-field definitions or static fixes across run stages.
- **Prune I/O Bloat**: Do not request `NEDOS` or `LORBIT` during ionic relaxations (`NSW > 0`).

### 3. Declarative Input Delta Composition (Anti-Regeneration Rule)
- **STRICT PROHIBITION**: Autonomous agents must **NEVER** re-generate entire multi-page input files (`INCAR`, `.fdf`, `in.lammps`) from scratch when transitioning between simulation stages. Full rewriting introduces stochastic token sampling drift, alters precision settings, and breaks git diff readability.
- **MANDATORY MECHANISM**: All progressive calculations must be composed using the **Ponytail Delta Composer**:
  ```bash
  ponytail-compose --base base_templates/vasp/INCAR.base \
                   --delta delta.json \
                   --output 01_pristine/01_04_dos/INCAR \
                   --engine vasp
  ```
  Or directly via `sciresearch compose`:
  ```bash
  sciresearch compose --base base_templates/vasp/INCAR.base \
                      --set NSW=0 ISMEAR=-5 NEDOS=2001 LORBIT=11 \
                      --output 01_pristine/01_04_dos/INCAR
  ```

### 4. Self-Documenting Tag Standard & NotebookLM Grounding
- Every mutated or non-trivial configuration tag must contain an inline rationale formatted as:
  ```text
  TAG = VALUE  # [Grounding:Source] Physical rationale
  ```
- **NotebookLM Grounding Engine**:
  - For DFT parameters (smearing, mixing, U values, van der Waals, k-point density): Query the local NotebookLM `dft-documentation` library.
  - For MD parameters (timesteps, thermostat damping `Tdamp`, barostat damping `Pdamp`, neighbor skins): Query the local NotebookLM `md-documentation` library.
  - Prefix comments with the grounded source tag (e.g., `[NotebookLM:dft-doc:Sloshing]`, `[NotebookLM:md-doc:Tdamp]`, `[DREAMS:artifact_id]`).

---

## 2. Hybrid 2-Tier Directory Standard (Filesystem + Zettelkasten DAG)

To prevent the **Branching Explosion Trap** (excessive 8-level deep directories) and the **HPC Clutter Trap** (unsearchable hash-only directories), all projects must follow the **Hybrid 2-Tier Standard**:

```
project_root/
├── 00_convergence/                     # Tier 0: Parameter validation & sweeps
│   ├── encut_sweep/                    #   Semantic slug
│   └── kpoints_sweep/
├── 01_pristine/                        # Tier 1: Baseline ground states
│   ├── relax/                          #   Relaxation (POSCAR, INCAR, CONTCAR)
│   ├── static_charge/                  #   Electronic charge density (CHGCAR, LOCPOT)
│   ├── bands/                          #   Band structure (BAND.dat, band_structure.pdf)
│   └── dos/                            #   Density of states (TDOS.dat, PDOS_*.dat)
├── 02_strained/                        # Tier 2: Systematic perturbations & response
│   ├── biaxial_m04/                    #   -4% biaxial compression
│   ├── biaxial_p04/                    #   +4% biaxial tension
│   ├── uniaxial_x_m04/
│   └── uniaxial_y_p04/
├── 03_functionalized/                  # Tier 3: Chemistry, defects, catalysis
│   ├── her_site_top/
│   └── her_site_bridge/
├── 04_dynamics/                        # Tier 4: Finite temperature & stability
│   ├── nvt_300k/
│   └── npt_300k/
├── 05_publication_figures/             # Tier 5: Publication-grade deliverables
│   ├── fig1_crystal_structure.pdf
│   └── fig2_coupled_band_pdos.pdf
├── base_templates/                     # Canonical project immutable templates
│   ├── vasp/INCAR.base
│   ├── siesta/template.fdf.base
│   └── lammps/system.lammps.base
└── logs/                               # Zettelkasten DAG Memory Registry
    ├── artifacts_registry.json         # DREAMS: immutable IDs, DAG parents, sources
    ├── notes_index.json                # Slip-Box notes & literature links
    └── decisions.csv                   # 8-rule decision audit trail
```

### Directory Navigation Rules:
1. **Maximum Nesting Depth**: Directories must never be nested deeper than **2 tiers** (`<tier_number>_<category>/<semantic_slug>/`).
2. **Multi-Parameter Branching**: Branch variations (such as strain percentages or adsorption sites) must reside as siblings within the tier directory.
3. **Zettelkasten DAG Metadata**: The relationship between stages (e.g. `02_strained/biaxial_m04` depends on `01_pristine/relax/CONTCAR`) is recorded in `logs/artifacts_registry.json` and `docs/KNOWLEDGE_MAP.md` via immutable parent IDs.

---

## 3. Seamless Graphify Knowledge Graph Synchronization

The workspace is continuously indexed into a semantic knowledge graph (`graphify-out/graph.json`):
- Run `sciresearch sync` to re-generate `docs/KNOWLEDGE_MAP.md` and trigger Graphify synchronization.
- All calculation directories, base templates, canvas notes, and verified reports are automatically linked using typed wikilinks:
  - `[[template:INCAR.base]]`
  - `[[calculation:01_pristine/relax]]`
  - `[[note:pt_bulk_convergence_discussion]]`
  - `[[artifact:b7703ad6]]`

---

## 4. The 8-Rule Decision Ladder & Recovery Budget

When a simulation encounters an error or SCF non-convergence:
- **Rule A (Infrastructure / Hardware Failure)**: SLURM walltime, node OOM, or SIGKILL $\rightarrow$ adjust core density, RAM per task, or micro-batch walltime.
- **Rule B (Standard SCF Non-Convergence)**: Charge sloshing or narrow band gaps $\rightarrow$ reduce mixing (`AMIX`/`mixing_beta`/`DM.MixingWeight`) to 0.04 - 0.2, increase max cycles, increase smearing for metals.
- **Rule C (CASSCF / Active Orbital Non-Convergence)**: Orbital gradient $\rightarrow$ apply level shifting, quasi-Newton orbital update.
- **Rule D (Active Orbital Drift / Symmetry Mismatch)**: Active space drifted into virtual space $\rightarrow$ inspect NOON, swap active orbitals, enforce irrep symmetry.
- **Rule E (Incomplete Correlation Space)**: Least-occupied active NOONs deviate from zero $\rightarrow$ expand root window or correlated pairs.
- **Rule F (Literature Precedent Conflict)**: Flag for human inspection; verify spin contamination $\langle S^2 \rangle$.
- **Rule G (Rydberg / Diffuse Contamination)**: Exclude ultra-diffuse basis functions from valence active space.
- **Rule H (Confirmed Successful Convergence)**: Extract ground-state observables, register artifact to Canvas.

---

## 5. Git Version Control Policy

- **Strict Master Branch Rule**: Always operate on `master` branch (never `main`) for all git branches, commits, and remote pushes.
- **Atomic Scientific Snapshots**: Use Conventional Commits (`feat(skills):`, `chore(templates):`, `fix(convergence):`).
