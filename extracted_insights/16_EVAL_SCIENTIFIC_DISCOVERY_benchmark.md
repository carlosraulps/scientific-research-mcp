# Evaluating LLMs in Scientific Discovery: SDE & The Discovery Loop
**Reference**: Zhangde Song, Jieyu Lu, Yuanqi Du, Thomas M. Pruyn, Kehan Guo, Xiuzhe Luo, Yuanhao Qu, Andres M. Bran, Heather J. Kulik, Huan Sun, Seyed Mohamad Moosavi, Chenru Duan et al., *Evaluating Large Language Models in Scientific Discovery*, Deep Principle / MIT / Toronto / Cornell / arXiv:2512.15567v2 (May 2026).

---

## 1. Executive Summary & The Scientific Evaluation Crisis
Standard LLM benchmarks (GPQA, ScienceQA, MMMU, Humanity's Last Exam) probe decontextualized factual recall through single-turn multiple-choice questions. They fail to test the core drivers of actual scientific research:
- Formulating testable, falsifiable hypotheses.
- Designing and debugging non-trivial multi-step computational experiments.
- Interpreting imperfect, noisy simulation outputs.
- Strategically deciding when to branch, optimize, or abandon a research hypothesis.

To solve this, SDE introduces the **Scientific Discovery Evaluation (SDE)** framework and the open-source **`sde-harness`** across Biology, Chemistry, Materials Science, and Physics.

```
       +-------------------------------------------------------------+
       |               THE CLOSED DISCOVERY LOOP (SDE)               |
       +-------------------------------------------------------------+
       |                                                             |
       |      [1. LLM Hypothesis Space Exploration]                  |
       |             - Formulate structured candidate                |
       |                               |                             |
       |                               v                             |
       |      [2. Computational Oracle / Physical Simulator]         |
       |             - DFT / MD / ASE / RDKit / PySR                 |
       |                               |                             |
       |                               v                             |
       |      [3. Multi-Objective Observation & Metric]              |
       |             - Ground-truth property calculation             |
       |                               |                             |
       |                               v                             |
       |      [4. Selection Rule & Iterative Propagation]            |
       |             - Genetic Algorithm / MCTS / Reflexion          |
       |                               |                             |
       |                               +--- (Next Iteration)         |
       +-------------------------------------------------------------+
```

---

## 2. Key Empirical Discoveries from SDE Benchmarking

### 2.1 The General Science Illusion & The Reality Gap
- While frontier models achieve 80–90% on generic benchmarks like GPQA, their performance on scenario-grounded scientific discovery drops dramatically to **50–70%**.
- Mastery of textbook Q&A does not translate to valid scientific execution or experimental problem-solving.

### 2.2 Diminishing Returns of Scaling Reasoning Compute
- Scaling test-time reasoning tokens (e.g. from low to medium to high reasoning effort) yields **negligible accuracy gains** on hard physical and materials science scenarios:
  - Biology: $0.70 \rightarrow 0.69$
  - Chemistry: $0.53 \rightarrow 0.60$
  - Materials Science: $0.74 \rightarrow 0.75$
  - Physics: $0.58 \rightarrow 0.60$
- **Theoretical Insight**: Scientific discovery relies on physical domain constraints, numerical solvers, and experimental feedback, which cannot be generated purely from internal linguistic associations.

### 2.3 Shared Systematic Failure Modes Across Frontier Models
- Pairwise correlation of error profiles across competing frontier models (`gpt-5`, `claude-sonnet-4.5`, `deepseek-R1`, `grok-4`) exceeds **$r > 0.80$** in chemistry and physics.
- All frontier models fail on the exact same subset of hard physical problems (e.g. PXRD lattice prediction, MOF topological synthesis, transition metal complex spin-state transitions).
- **Practical Takeaway**: Naive LLM ensembling (e.g., majority voting between models) fails to heal deep scientific blind spots. Hard computational oracles are strictly necessary.

---

## 3. The Eight Grounded Discovery Projects in SDE
SDE formalizes eight end-to-end computational discovery projects evaluated via `sde-harness`:
1. **Protein Design**: Evolutionary optimization of binding affinities and structural stability.
2. **Retrosynthesis**: Multi-step retrosynthetic pathway generation using algorithmic synthesis trees.
3. **Small Molecule Optimization**: Multi-parameter lead optimization balancing QED, SA score, and binding energy.
4. **Transition Metal Complex (TMC) Optimization**: Tuning metal–ligand complexes for specific spin-state gaps and redox potentials.
5. **Crystal Design**: Autonomous 3D crystal structure generation meeting target band gaps and space groups.
6. **Symbolic Regression**: Discovering closed-form differential equations from nonlinear dynamical system trajectories.
7. **Ising Model Physics**: Parameter estimation and critical point identification in statistical mechanics.
8. **Gene Editing**: Optimizing guide RNA sequences and delivery parameters for minimal off-target cleavage.

---

## 4. Architectural Blueprint for `sciresearch`
Based on the SDE framework and `sde-harness`:
1. **Closed-Loop Simulation Harness (`sde_verify_loop`)**:
   Implement a standardized loop inside `sciresearch` that receives a candidate parameter set or material hypothesis, invokes the deterministic simulator/oracle (ASE, VASPKIT, SIESTA, LAMMPS), calculates objective fitness, and feeds structured observations back to the agent.
2. **Oracle Grounding Over Chain-of-Thought**:
   Never trust chain-of-thought derivations for numerical quantities (formation energies, lattice vectors, mixing weights). Delegate all calculations to external Python/C++ oracles.
3. **Multi-Round State Management**:
   Maintain explicit state across discovery rounds, logging parent-child relationships between successive computational generations.
