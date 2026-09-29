# Scientific Research Agent: System Policies & Operational Boundaries
**Reference**: Lee & Rondinelli, arXiv:2609.13357 (2026); DREAMS, arXiv:2507.14267 (2026).

---

## 1. Core Operating Policies & Non-Negotiables

1. **Zero Hallucinated or Laundered Data**:
   - Every reported numerical value, parameter recommendation, or finding MUST reference an immutable 8-character artifact ID in the DREAMS registry.
   - Sourced sensitive parameters (`ecutwfc`, `kpoints`, `encut`, `smearing`) must cite a valid upstream artifact from a convergence test.

2. **Ponytail VASP Zero-Redundancy Principle**:
   - Never write tags that VASP already sets by default (`ALGO = Normal`, `ISIF = 2` when `IBRION = 2`, `LDAUTYPE = 2`, `LDAUJ = 0 0`, `LWAVE = .TRUE.`, `LCHARG = .TRUE.`, `SYSTEM`, `POTIM = 0.5`).
   - Prune unnecessary I/O overhead tags (`NEDOS`, `LORBIT`) unless plotting density of states.
   - Align MPI core geometry with node socket divisors (`NCORE = 4` or `16`).

3. **MDCrow Resumption Standard**:
   - Long-horizon simulations MUST be initialized with a unique `Run ID` and checkpoint directory.
   - All trajectories, logs, and output coordinates must be registered in the file path registry.

4. **The 8-Attempt Recovery Budget**:
   - When encountering non-convergence or calculation failure, traverse the 8-Rule Decision Ladder (Rules A through H).
   - If a calculation fails after 8 interventions, terminate the automatic retry loop, log full diagnostics to `logs/decisions.csv`, and seal the state for human review.

---

## 2. Decision Ladder Diagnostic Rules (Rules A–H)

- **Rule A (Infrastructure / Hardware Failure)**: SLURM walltime, node OOM, or SIGKILL $\rightarrow$ adjust core density, RAM per task, or micro-batch walltime.
- **Rule B (Standard SCF Non-Convergence)**: Charge sloshing or narrow band gaps $\rightarrow$ reduce `mixing_beta`/`AMIX` to 0.2, increase max cycles, increase smearing for metals.
- **Rule C (CASSCF / Active Orbital Non-Convergence)**: Orbital gradient $\rightarrow$ apply level shifting, quasi-Newton orbital update.
- **Rule D (Active Orbital Drift / Symmetry Mismatch)**: Active space drifted into virtual space $\rightarrow$ inspect NOON, swap active orbitals, enforce irrep symmetry.
- **Rule E (Incomplete Correlation Space)**: Least-occupied active NOONs deviate from zero $\rightarrow$ expand root window or correlated pairs.
- **Rule F (Literature Precedent Conflict)**: Flag for human inspection; verify spin contamination $\langle S^2 \rangle$.
- **Rule G (Rydberg / Diffuse Contamination)**: Exclude ultra-diffuse basis functions from valence active space.
- **Rule H (Confirmed Successful Convergence)**: Extract ground-state observables, register artifact to Canvas.
