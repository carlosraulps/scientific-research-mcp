# MDCrow: Checkpoint-Based Memory & Session Resumption
**Reference**: Q. Campbell et al., *MDCrow: automating molecular dynamics workflows with large language models*, Mach. Learn.: Sci. Technol. 7 (2026) 025037.

---

## 1. Core Architecture & Scientific Problem
Molecular dynamics (MD) and DFT calculations often span hours or days, requiring long-horizon execution where:
- Continuous active context windows overflow or get wiped when sessions disconnect.
- Simulations complete while the researcher is away, requiring seamless session resumption without re-running completed preparation or equilibration steps.
- Subsequent post-analysis (e.g. RMSD, radial distribution functions, diffusion coefficients, dipole autocorrelations) requires access to the exact simulation trajectory, topology, and force field parameters.

---

## 2. Checkpoint-Based Memory System

### A. Unique Checkpoint Directories & Run IDs
- Every simulation workflow generates a unique **`Run ID`** (e.g., `run_20260929_1700_md_npt`).
- Each run maintains an isolated checkpoint folder under `runs/<run_id>/` and a serialized checkpoint manifest `checkpoints/<run_id>.json`.

### B. Four Checkpoint Assets
1. **Prompt Summary**: Concise LLM-generated distillation of the initial scientific objective and constraints.
2. **Agent Trace**: Chronological log of decisions, tool calls, and execution milestones.
3. **File Path Registry**: Catalog of input coordinates (`.pdb`, `.cif`, `POSCAR`), force fields / topologies (`.prmtop`, `POTCAR`), trajectories (`.dcd`, `.xtc`, `XDATCAR`), and log outputs (`OUTCAR`, `md.log`).
4. **Figure & Artifact Log**: Extracted energy profiles, temperature/pressure convergence plots, and thermodynamic summaries.

---

## 3. Resume & Troubleshoot Lifecycle
When resuming a session:
1. The researcher or agent supplies the `Run ID` or checkpoint folder.
2. The agent reloads memory summaries, parameter dictionaries, and verified file paths.
3. If the run failed, the agent inspects the final log lines, adjusts parameters (e.g., reduces timestep from 2.0 fs to 1.0 fs, adjusts barostat coupling, or increases friction coefficient), and continues execution without repeating completed preprocessing.
4. If the run completed, the agent immediately transitions to production analysis and figure generation.
