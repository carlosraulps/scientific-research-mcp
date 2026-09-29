# Rosetta (2026): Automating First-Principles Performance Modeling
**Reference**: K. Sankaralingam, *Rosetta: Automating First-Principles Performance Modeling Using Multi-Agent LLMs*, NVIDIA, arXiv:2609.19376v1 (2026).

---

## 1. Core Architectural Problem
Traditional LLM agents generate plausible-sounding calculations and performance estimates, but they frequently suffer from:
1. **Circular Reasoning**: Fitting curves to match published or expected outputs rather than deriving behavior from first principles.
2. **The Faithful-Implementation-of-a-Bad-Spec Trap**: A single verifier checks that code runs without crashes and matches the prompt, inadvertently approving unphysical or circular mathematical formulations.
3. **Implicit Parameter Drift**: Omitting binding constraints and hardware bottlenecks.

---

## 2. Four Key Rosetta Design Pillars

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. THE SCIENTIFIC CONSTITUTION (The Prime Directive)                  │
│    - Enforces derivation from primary physical/hardware parameters.    │
│    - Strict prohibition of circular curve-fitting.                     │
│    - "Calibration-as-Overlay": Literature/experimental data is strictly│
│      an external comparison overlay, never an internal derivation step.│
├────────────────────────────────────────────────────────────────────────┤
│ 2. DUAL VERIFICATION ARCHITECTURE                                      │
│    - Separates FUNCTIONAL CORRECTNESS (code execution, schemas, syntax)│
│      from SCIENTIFIC VALIDITY (equations, physical laws, bounds).      │
├────────────────────────────────────────────────────────────────────────┤
│ 3. INDEPENDENT CRITIC AGENTS IN VERIFY-REPAIR LOOPS                   │
│    - Generator agents NEVER self-verify their own output.              │
│    - Independent critic agents audit specifications and code.          │
├────────────────────────────────────────────────────────────────────────┤
│ 4. THREE STANDARDIZED ARTIFACT DELIVERABLES                            │
│    - SPECIFICATION.md: Formal mathematical and parameter derivation.   │
│    - model.py: Executable, reproducible simulation/analytical code.    │
│    - INTERPRETATION.md: Plain-English synthesis of binding constraints.│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Implications for the Global Scientific Research Engine
- **Independent Scientific Audit**: In addition to schema validation (functional correctness), every simulation parameter and convergence claim must undergo a separate scientific validity check against the Scientific Constitution.
- **Calibration-as-Overlay Guard**: Enforces the verified citations rule—experimental benchmarks appear strictly as scatter overlays for validation and are never back-propagated as simulated values.
