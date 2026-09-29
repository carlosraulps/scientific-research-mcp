# Lee & Rondinelli: File-Based Context Architecture & The Decision Ladder
**Reference**: V. C. Lee and J. M. Rondinelli, *Can Autonomous LLM Agents Execute Multireference Quantum Chemistry Calculations?*, arXiv:2609.13357v1 (2026).

---

## 1. Context Separation Architecture
To prevent degradation as workflows grow over hundreds of tool calls, operational context is partitioned across three core files:

| File | Purpose | Access Pattern |
| :--- | :--- | :--- |
| **`CLAUDE.md`** | System context, operational boundaries, permitted execution modes, safety constraints. | Read once at session initialization. |
| **`TASK.md`** | Active execution state, subtask checklist, step counter, current hypothesis, and next action. | Read and updated at every iteration loop. |
| **`EVIDENCE.md`** | Auxiliary theoretical knowledge store, literature benchmarks, rule rationales, and past justification notes. | Queried on demand during diagnosis or parameter selection. |

### Supplementary Execution Artifacts
- **`/runs/<run_id>/`**: Isolated working directory for raw inputs and outputs.
- **`/logs/decisions.csv`**: Tabular append-only audit trail logging every step, hypothesis, intervention, and outcome.
- **`/logs/results.csv`**: Machine-readable verified physical values and convergence metrics.

---

## 2. The 8-Rule Decision Ladder (Rules A–H)
When a calculation terminates or produces suspect electronic states, the agent traverses a hierarchical ladder rather than guessing:

```
[ Calculation Finished or Errored ]
                │
                ▼
 Rule A: Infrastructure / SLURM Failure?
    └── Yes ──► Check walltime, memory, node health, resubmit.
    └── No  ──▼
 Rule B: Standard SCF Non-Convergence?
    └── Yes ──► Damp mixing, adjust DIIS, increase max iterations.
    └── No  ──▼
 Rule C: Multi-Configurational (CASSCF) Non-Convergence?
    └── Yes ──► Inspect orbital gradient, apply level shift, quasi-Newton update.
    └── No  ──▼
 Rule D: Convergence to Wrong Electronic State (Active Drift)?
    └── Yes ──► Inspect NOON (Natural Orbital Occupation Numbers), swap orbitals,
                enforce irrep symmetry, freeze core/valence boundaries.
    └── No  ──▼
 Rule E: Incomplete Correlation Space / Root Truncation?
    └── Yes ──► Expand active space roots, include correlated pairs.
    └── No  ──▼
 Rule F: Significant Disagreement with Literature Precedent?
    └── Yes ──► Flag for human review; inspect spin contamination (<S^2>).
    └── No  ──▼
 Rule G: Rydberg / Diffuse State Contamination?
    └── Yes ──► Check Gaussian exponents, expand diffuse basis functions.
    └── No  ──▼
 Rule H: Fully Validated & Verified Convergence!
    └── Proceed to publish artifact and log result.
```

### The 8-Attempt Budget Rule
Each calculation is bounded by an **8-attempt recovery budget**. If a calculation fails 8 successive interventions, the agent terminates and logs a structured failure report with full diagnostics rather than spinning indefinitely.
