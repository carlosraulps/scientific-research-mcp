# Scientific Research Evidence & Decision Log
**Reference**: Lee & Rondinelli, arXiv:2609.13357 (2026); DREAMS, arXiv:2507.14267 (2026).

Auditable record of all procedural decisions, theoretical justifications, literature baselines, and parameter interventions.

---

## 1. Literature Benchmark References

### Sol27LC Benchmark (Lattice Constants for 27 Elemental Solids)
- **Reference**: Z. Wang et al., *DREAMS*, arXiv:2507.14267 (2026).
- **Benchmark Criteria**: Sol27LC dataset spanning FCC, BCC, HCP, and Diamond crystals.
- **Platinum Bulk (FCC)**: $a_0 = 3.924\text{ \AA}$, $E_{cut} = 520\text{ eV}$, $k\text{-mesh} = 12 \times 12 \times 12$, PBE functional.
- **Silicon Bulk (Diamond)**: $a_0 = 5.431\text{ \AA}$, $E_{cut} = 450\text{ eV}$, $k\text{-mesh} = 8 \times 8 \times 8$.

### The CO/Pt(111) Puzzle (Site Preference & Adsorption Energetics)
- **Reference**: DREAMS benchmark reproducing FCC hollow vs. top site adsorption energy difference $\Delta E_{\text{ads}}$.
- **Physical Criterion**: Comparison-set consistency: all slab calculations must share strictly identical $E_{cut}$, $k$-spacing, dipole corrections, and smearing width to preserve systematic error cancellation.

### QUESTDB Vertical Transition Energies (VTE)
- **Reference**: V. C. Lee & J. M. Rondinelli, arXiv:2609.13357 (2026).
- **Protocol**: CASSCF/SC-NEVPT2 with aug-cc-pVTZ and RIJCOSX.
- **Target Accuracy**: MAE $\le 23\text{ meV}$ when guided by the 8-Rule Decision Ladder.

---

## 2. Decision Log
*(Appended automatically by `log_decision` tool and CLI)*

### [2026-09-29T17:03:00Z] Decision: initialize_sciresearch_suite (`system_bootstrap`)
- **Triggered Rule**: Rule H (Verified Successful Convergence)
- **Hypothesis**: Unified implementation of DREAMS, MDCrow, TRITONDFT, MDAgent, and Lee & Rondinelli architectures provides complete provenance, memory, and evaluation for autonomous scientific workflows.
- **Intervention**: Deployed Canvas Store, Checkpoint Manager, Historical Memory SQLite DB, Scientific Evaluator, and Graphify Bridge.
- **Observed Outcome**: 8/8 unit tests passed; 15 MCP tools verified over JSON-RPC 2.0 stdio.
- **Evidence / Artifact Reference**: `scripts/mcp_server.py`
