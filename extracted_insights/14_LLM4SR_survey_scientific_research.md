# LLM4SR: Large Language Models for Scientific Research
**Reference**: Ziming Luo, Zonglin Yang, Zexin Xu, Wei Yang, Xinya Du, *LLM4SR: A Survey on Large Language Models for Scientific Research*, ACM Computing Surveys / arXiv:2501.04306v1 (2025).

---

## 1. Executive Summary & The Four-Stage Research Cycle
The scientific research pipeline traditionally follows an inductive-deductive cycle: background acquisition, hypothesis generation, experimental design and execution, data analysis, and dissemination through peer-reviewed manuscripts. LLM4SR provides the first systematic taxonomy detailing how foundation models and agentic workflows revolutionize all four interconnected phases of modern science:

```
                  +-----------------------------------+
                  |   1. Scientific Hypothesis        |
                  |      Discovery (§2)               |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------------------------+
                  |   2. Experiment Planning &        |
                  |      Implementation (§3)          |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------------------------+
                  |   3. Scientific Paper Writing     |
                  |      & Synthesis (§4)             |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------------------------+
                  |   4. Automated Peer Reviewing     |
                  |      & Critique (§5)              |
                  +-----------------+-----------------+
                                    |
                                    +--- (Iterative Refinement / Loop)
```

---

## 2. Scientific Hypothesis Discovery: Principles & Guardrails
Historically rooted in Literature-Based Discovery (LBD; Swanson's ABC model) and inductive logic programming, modern LLM hypothesis discovery faces the core challenge of extreme inductive reasoning: generating general, valid, and novel scientific rules from observational data.

### Four Philosophical & Methodological Requirements:
1. **Consistency**: The hypothesis must not conflict with existing valid physical/empirical observations.
2. **Reality Alignment**: The hypothesis must reflect physical reality rather than synthetic artifacts or LLM fantasy.
3. **Generality**: The hypothesis must induce a general pattern applicable beyond the specific training examples.
4. **Clarity & Operational Specificity**: The hypothesis must be explicit, testable, quantitatively falsifiable, and devoid of hand-waving vagueness.

### Core Architectural Components for Autonomous Discovery (Table 1 Trajectory):
- **Inspiration Retrieval Strategy**: Moving beyond simple keyword search by querying semantic embeddings (SentenceBERT), citation graph neighbors (SciMON), and concept co-occurrence graphs (ResearchAgent, SciPIP).
- **Novelty Checker (NC)**: Iterative adversarial filtering against literature corpora to ensure the proposed relationship is genuinely novel.
- **Validity Checker (VC)**: Domain-rule verification testing physical plausibility (conservation laws, thermodynamic stability, orbital symmetry).
- **Clarity Checker (CC)**: Structural linting enforcing operational parameter definitions (exact quantities, chemical species, measurable endpoints).
- **Leverage of Multiple Inspirations (LMI)**: Decomposing complex discoveries $P(\text{hypothesis} \mid \text{background})$ into sequential inspiration associations (as established by MOOSE-Chem for high-impact chemistry and materials breakthroughs).
- **Evolutionary Algorithms (EA)**: Island-based mutation, crossover, and survival-of-the-fittest selection (FunSearch, SGA, LLM-SR) treating experimental verification as the fitness landscape.

---

## 3. Experiment Planning & Implementation: Autonomous Grounding
Transforming qualitative hypotheses into concrete simulation and laboratory protocols requires structured agent architectures characterized by **modularity** and **sound tool integration**:

1. **Hierarchical Task Decomposition**:
   - Decomposing abstract research goals into dependency graphs and executable steps (HuggingGPT, CRISPR-GPT).
   - Translating natural language intents into deterministic calculation workflows.

2. **ReAct & Multi-Agent Consensus**:
   - Iterative "Thought $\rightarrow$ Action $\rightarrow$ Observation" loops (ChemCrow, Coscientist) paired with multi-agent peer debate to resolve conflicting methodological proposals.

3. **The Necessity of Sound External Verifiers**:
   - **Crucial Finding**: LLMs cannot reliably verify their own execution plans through pure internal reasoning. Unchecked LLMs hallucinate non-physical simulation parameters (e.g. unphysical k-point grids, non-existent pseudopotentials, inverted relaxation algorithms).
   - Sound verification requires hard coupling with external deterministic solvers (ASE, VASPKIT, PyMatGen, OpenMM, SIESTA, VASP).

---

## 4. Scientific Writing & Peer Reviewing
- **Paper Generation**: Citation graph grounding, automated related work synthesis, and structured methodology writing to eliminate hallucinated literature references.
- **Automated Peer Reviewing**: Multi-criteria evaluation of submitted scientific workflows assessing methodology soundness, reproducibility, baseline completeness, and statistical rigor.

---

## 5. Direct Architectural Blueprint for `sciresearch`
Based on LLM4SR, the `sciresearch` MCP framework must incorporate:
1. **Hypothesis Evaluation Protocol (`eval_hypothesis`)**:
   A deterministic multi-dimensional scorer auditing any proposed simulation plan across **Novelty**, **Validity**, **Clarity**, and **Feasibility**.
2. **Multi-Inspiration Combiner**:
   A procedural engine combining disparate structural/computational inspirations into composite simulation protocols.
3. **Execution Guardrails**:
   Automated verification preventing premature calculation dispatch until all input parameters pass hard domain verifiers.
