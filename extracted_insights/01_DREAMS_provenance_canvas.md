# DREAMS: Shared Canvas & Append-Only Provenance Registry
**Reference**: Z. Wang et al., *DREAMS: Density Functional Theory Based Research Engine for Agentic Materials Simulation*, arXiv:2507.14267v2 (2026).

---

## 1. Core Architecture & Scientific Motivation
Autonomous LLM agents applied to physical simulations (DFT, MD) frequently suffer from:
1. **Context Loss**: Critical input parameters or intermediate energies fade from context across long workflows.
2. **Verification Gaming**: Agents craft plausible-sounding explanations or alter physical parameters without justified provenance.
3. **Data Laundering & Fabrication**: Agents report numbers that never originated from actual simulation tool outputs, or pass inputs through identity operations to forge provenance.

DREAMS resolves these failure modes through two central constructs:
- **Centralized Shared Canvas**: Persistent shared memory divided into 3 specialized stores (Notes, Artifacts, Reports).
- **Multi-Tier Safety Guard & Append-Only Provenance Graph**: Every value used in a calculation or reported finding must reference a machine-verified producing tool call.

---

## 2. Canvas Three-Store Topology

```
+-------------------------------------------------------------------------+
|                              SHARED CANVAS                              |
+-------------------------------------------------------------------------+
| 1. NOTES (Working Documents)                                            |
|    - Free-form markdown logs for agent day-to-day bookkeeping.          |
|    - Append-only & version-controlled (editing creates v2, v3...).       |
|    - Cites artifact IDs; unknown IDs cause rejection of note.           |
+-------------------------------------------------------------------------+
| 2. ARTIFACTS (Append-Only Provenance Registry)                          |
|    - Every tool output receives an immutable 8-character hash ID.       |
|    - Stores producing tool, output value, arguments, declared context.  |
|    - Per-parameter rationales and per-parameter source IDs.             |
|    - Machine-verified Directed Acyclic Graph (DAG).                     |
+-------------------------------------------------------------------------+
| 3. REPORTS (Verified Scientific Findings)                               |
|    - High-level structured research deliverables.                       |
|    - Audited at generation time by a Report Judge against the DAG.      |
|    - Once verified and sealed, reports become completely IMMUTABLE.     |
+-------------------------------------------------------------------------+
```

---

## 3. Strict Provenance Rules (Anti-Laundering Gates)

1. **Rule R1 (Output Sourcing)**:
   - Sensitive simulation parameters (e.g., `ecutwfc`, `kpoints`, `encut`, `functional`, `smearing`) must cite a valid upstream artifact `result_id` from a convergence sweep or reference benchmark.
   - Generic boilerplate rationales ("standard setting", "default practice") are rejected.

2. **Rule R1-dotted (No Input Parameter Laundering)**:
   - An agent cannot reference an arbitrary input parameter of a previous call (`<id>.<parameter>`) to claim verified provenance unless that input was part of an explicit characterization test.

3. **Rule R1-no-source (Explicit Sub-Study Isolation)**:
   - Holding a sensitive parameter fixed without an output source is allowed *only* during an explicit sub-study (e.g., holding `ecutwfc` fixed while sweeping `kspacing`), requiring explicit declaration in the call's `declared_context`.

4. **Trivial Math & Identity Rejection**:
   - Math operations like `x * 1.0`, `x + 0`, or superficial string echoes cannot be used to generate a new artifact ID to launder data.

5. **Downstream Invalidation**:
   - If an upstream artifact is regenerated or adjusted, all downstream artifacts depending on it are marked dirty or invalid, necessitating re-execution.

---

## 4. Convergence Agent Patterns for DFT
When self-consistent field (SCF) or geometry optimization fails, DREAMS dispatches a dedicated **Convergence Agent** child agent to isolate diagnostics from the primary planning loop:
- **Energy cutoff (`ecutwfc`/`ENCUT`)**: Increment by 5-10 Ry for ultrasoft/PAW potentials with transition metals.
- **Smearing width (`degauss`/`SIGMA`)**: Increase for metallic or narrow-gap systems (e.g. 0.02 to 0.03 Ry) to ensure smooth Fermi surface integration.
- **Charge sloshing (`mixing_beta`/`AMIX`)**: Reduce from 0.7 down to 0.2–0.3; switch `mixing_mode` to `local-TF` for stubborn surface adsorption systems.
- **Step limits (`electron_maxstep`/`NELM`)**: Extend up to 200–300 if energy difference $\Delta E$ is monotonically decreasing.
- **Symmetry breaking (`starting_magnetization`/`MAGMOM`)**: Initialize small magnetic moments (0.1–0.5 $\mu_B$) on transition metal sites.
