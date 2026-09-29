# MatSciAgent (2025): Modular Multi-Task Materials Science Agents
**Reference**: A. Chaudhari, J. Ock, A. B. Farimani, *Modular large language model agents for multi-task computational materials science*, Communications Materials (Nature Portfolio) 7:131 (2025).

---

## 1. Modular Multi-Agent Architecture
MatSciAgent decomposes materials science tasks into specialized autonomous subagents coordinated by a central orchestrator:

```
                      [ User Query ]
                            │
                            ▼
              ┌───────────────────────────┐
              │     Master Orchestrator   │
              │  (Intent & Task Routing)  │
              └─────────────┬─────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Data Agent   │     │ Generative   │     │ Simulation   │
│ - MatWeb     │     │ Structure    │     │ Agent        │
│ - MatProj    │     │ Agent        │     │ - LAMMPS     │
│ - OQMD/ICSD  │     │ - Crystal Gen│     │ - Continuum  │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## 2. Key Methodological Lessons

1. **Decoupled Tool Abstraction**:
   - Rather than loading dozens of disparate APIs into a single agent prompt, tools are segmented into domain clusters (Data Retrieval, Crystal Construction, Thermodynamic Simulation, Mechanics).
2. **Deterministic Parameter Extraction**:
   - Extraction of physical parameters (e.g. density, Young's modulus, lattice parameters) is validated against schema filters, achieving 100% extraction consistency across repeated stochastic LLM runs.
3. **Generative Structure Fallback**:
   - When a requested compound is absent from established databases (Materials Project, MatWeb), the framework gracefully routes to a crystal structure generator rather than failing or hallucinating coordinates.
