# From Automation to Autonomy: LLMs in Scientific Discovery
**Reference**: Tianshi Zheng, Zheye Deng, Hong Ting Tsang, Weiqi Wang, Jiaxin Bai, Zihao Wang, Yangqiu Song, *From Automation to Autonomy: A Survey on Large Language Models in Scientific Discovery*, Department of Computer Science and Engineering, HKUST / arXiv:2505.13259v1 (2025).

---

## 1. Executive Summary & The Three-Tier Autonomy Taxonomy
The HKUST survey charts the paradigm shift of Large Language Models in scientific inquiry from static, human-directed scripting helpers toward fully autonomous exploratory agents. The authors establish a foundational three-level taxonomy of scientific AI autonomy:

```
+-----------------------------------------------------------------------------------------+
|                               THREE LEVELS OF AUTONOMY                                  |
+-------------------+--------------------+-----------------------+------------------------+
| Dimension         | Level 1: Tool      | Level 2: Analyst      | Level 3: Scientist     |
+-------------------+--------------------+-----------------------+------------------------+
| Primary Role      | Task Automation    | Data Modeling &       | Open Exploratory &     |
|                   | Tool               | Analytical Agent      | Discovery Agent        |
+-------------------+--------------------+-----------------------+------------------------+
| Human Role        | Task Allocation &  | Problem Definition &  | Minimal Oversight /    |
|                   | Direct Control     | Output Validation     | Strategic Guidance     |
+-------------------+--------------------+-----------------------+------------------------+
| Task Scope        | Explicitly Defined | Goal-Oriented         | Open-Ended & Evolving  |
|                   | (Single Step)      | (Multi-Step Sub-task) | (Full Research Cycle)  |
+-------------------+--------------------+-----------------------+------------------------+
| Agentic Workflow  | Simple & Static    | Advanced Interactive  | Strategic, Iterative,  |
|                   | (Script / Regex)   | (ReAct, Code Gen)     | Multi-Agent Debate     |
+-------------------+--------------------+-----------------------+------------------------+
```

---

## 2. Mapping to the Six Stages of the Scientific Method
Anchoring autonomous agents into the classical epistemological cycle (Popper 1935, Kuhn 1962):

```
       [Stage 1: Observation & Problem Definition]
                         |
                         v
       [Stage 2: Hypothesis Development & Search]
                         |
                         v
       [Stage 3: Experimentation & Data Collection]  <---+
                         |                                |  Autonomous
                         v                                |  Self-Refining
       [Stage 4: Data Analysis & Interpretation]         |  Iterative
                         |                                |  Cycle
                         v                                |
       [Stage 5: Drawing Conclusions & Verification]     |
                         |                                |
                         v                                |
       [Stage 6: Iteration & Strategic Refinement] ------+
```

### Stage Breakdown & Agent Specializations:
1. **Observation & Problem Definition**: Academic graph navigation, literature synthesis, paper-to-table automated extraction, and anomaly identification.
2. **Hypothesis Development**: LLM-assisted brainstorming, agentic tree-search over chemical/physical spaces, and multi-inspiration cross-pollination.
3. **Experimentation & Data Collection**: Automated workflow design, scientific code generation (DFT, MD, quantum chemistry), and robot/HPC execution.
4. **Data Analysis & Interpretation**: Tabular and chart reasoning, symbolic regression (e.g. PySR, LLM-SR), and physical equation discovery from trajectory data.
5. **Drawing Conclusions**: Automated claim verification, replication auditing, peer-review generation, and epistemic confidence scoring.
6. **Iteration & Strategic Refinement**: Monte-Carlo Tree Search (MC-NEST), explanation-refining theorem proving, and Bayesian experimental redirection.

---

## 3. Key Findings on Autonomous Scientific Reasoning
- **Data Analytics Bottleneck**: The survey notes that on realistic scientific analytics benchmarks (BLADE, DiscoveryBench), unaugmented LLMs struggle significantly with multi-table tabular reasoning and complex data modeling. Agentic frameworks (e.g., DS-Agent) that combine case-based reasoning and memory clusters are essential.
- **Symbolic Regression as Physical Discovery**: Bridging LLM semantic intuition with symbolic mathematics (LLM-SR) enables discovery of governing differential equations and constitutive laws directly from noisy simulation outputs.
- **Deep Transparency vs. Superficial Explainability**: Standard post-hoc Explainable AI (XAI) is insufficient for scientific rigor. Level 3 systems require **verifiable internal reasoning** where every intermediate claim is explicitly tethered to physical laws or deterministic computational artifacts.

---

## 4. Unresolved Frontier Challenges
1. **End-to-End Closed Discovery Cycles**: Moving beyond single-shot optimization into multi-generation research programs where the agent autonomously defines follow-up studies based on unexpected physical anomalies.
2. **Robotic & Supercomputing Embodiment**: Seamless bridging between language reasoning and live HPC queue telemetry, SLURM batch execution, and laboratory hardware.
3. **Continual Learning Without Catastrophic Forgetting**: Maintaining persistent episodic and procedural memories across multi-month computational campaigns.

---

## 5. Direct Architectural Blueprint for `sciresearch`
- **Promote `sciresearch` to Level 3 Autonomy**: Equip the tool suite with closed-loop iteration protocols allowing autonomous progression from hypothesis definition to SLURM execution, result parsing, and next-step refinement.
- **Verifiable Claim Ledger**: Institutionalize the distinction between speculative agent commentary and mathematically/empirically verified physical facts in SQLite persistent memory.
