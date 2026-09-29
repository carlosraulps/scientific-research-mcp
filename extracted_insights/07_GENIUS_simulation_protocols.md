# GENIUS (2026): Autonomous Design & Execution of Simulation Protocols
**Reference**: M. Soleymanibrojeni, R. Aydin, D. Guedes-Sobrinho, A. C. Dias, M. J. Piotrowski, W. Wenzel, C. R. C. Rêgo, *GENIUS: an agentic AI framework for autonomous design and execution of simulation protocols*, Communications Materials (Nature Portfolio) 7:115 (2026).

---

## 1. Core Architecture & Scientific Motivation
Setting up multi-step first-principles workflows (e.g. self-consistent field, geometry relaxation, band structures, vibrational frequencies) requires translating high-level user intent into verified, constraint-compatible input protocols.

GENIUS introduces an end-to-end framework combining:
1. **Smart Knowledge Graph**: Encodes software parameters, physical relationships, and operational constraints (e.g., Quantum ESPRESSO, VASP).
2. **Autonomous Protocol Synthesizer**: Converts natural language intent into structured simulation workflows.
3. **Automated Error Handling (AEH) Loop**: Two distinct stages of verification.

---

## 2. Two-Stage Automated Error Handling (AEH)

```
        [ Natural Language Scientific Request ]
                          │
                          ▼
            [ Protocol Design via LLM ]
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│ STAGE 1: Static Pre-Flight Validation (Error 1)     │
│ - Schema check against Smart Knowledge Graph        │
│ - Incompatible parameter pair detection             │
│ - Missing pseudopotentials / PAW verification       │
│ - K-point sampling density sanity bounds            │
└─────────────────────────┬───────────────────────────┘
                          │
                  Passes Stage 1?
                   ├── No ──► [ Prompt LLM with Graph Constraint Fix ]
                   │
                   ▼ (Yes)
┌─────────────────────────────────────────────────────┐
│ HPC Job Dispatch & Execution                        │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│ STAGE 2: Dynamic Runtime Diagnosis (Error 2)        │
│ - Detects SCF divergence, ionic crashes, walltime   │
│ - Re-queries knowledge graph for targeted remedies  │
│ - Submits corrected protocol iteratively            │
└─────────────────────────────────────────────────────┘
```

---

## 3. Best Practices for Protocol Design
- **Topological Input Ordering**: Dependencies between workflow stages (e.g., SCF wavefunctions $\rightarrow$ Non-SCF dense k-mesh $\rightarrow$ Band plotting) must be represented as a DAG.
- **Explicit Invariance Checks**: Ensure pseudopotentials match throughout all calculation stages in a single study (e.g., never mix scalar-relativistic and fully relativistic pseudopotentials between bulk and surface runs).
