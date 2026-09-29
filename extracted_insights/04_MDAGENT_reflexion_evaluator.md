# MDAgent: Role Specialization & Reflexion Evaluator Loop
**Reference**: Z. Shi et al., *A fine-tuned large language model based molecular dynamics agent for code generation to obtain material thermodynamic parameters*, Sci. Rep. 15, 92337 (2025).

---

## 1. Multi-Agent Role Specialization
MDAgent divides the scientific workflow into four specialized agents:
1. **Manager**: Interprets high-level scientific goals from natural language, assigns execution flow, and handles user interaction.
2. **Planner**: Decomposes complex thermodynamic or mechanical objectives into discrete computational steps (e.g., structure generation $\rightarrow$ equilibration $\rightarrow$ production $\rightarrow$ property extraction).
3. **Worker**: Generates the exact simulation input script (e.g., LAMMPS `in.*`, VASP `INCAR`, QE `.pwi`).
4. **Evaluator**: Rigorously audits the generated script before submission, scoring its syntax, physical correctness, and adherence to domain constraints.

---

## 2. Reflexion Error Feedback Loop

```
           [ Planner Subtask ]
                   │
                   ▼
┌──────────────────────────────────────┐
│            Worker Agent              │
│    (Generates Simulation Script)     │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│           Evaluator Agent            │
│   - Syntax and format verification   │
│   - Domain & physics sanity check    │
│   - Quantitative scoring (1-10)      │
└──────────────────┬───────────────────┘
                   │
         Score >= Threshold?
          ├── No ──────┐
          │            │ (Structured Deductions +
          ▼            │  Constructive Suggestions)
  [ Submit to Queue ]  └───────────┐
                                   ▼
                        [ Reflexion Iteration ]
```

### Static Pre-Flight Rules Evaluated
- **Time step safety**: Ensures time step does not exceed stability bounds (e.g. $\le 1.0$ fs for hydrogen-containing systems).
- **Thermostat/Barostat coupling**: Checks damping parameters (e.g., $T_{\text{damp}} \approx 100\text{ fs}$, $P_{\text{damp}} \approx 1000\text{ fs}$).
- **Ensemble consistency**: Avoids instantaneous NPT jumping without prior NVE/NVT relaxation.
- **Output frequencies**: Enforces adequate sampling for correlation functions and thermodynamic dumps.
