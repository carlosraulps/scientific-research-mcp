# AI Engineering: Architecture, Multi-Agent Systems, Guardrails & Evaluation for Foundation Model Systems
**Reference**: Chip Huyen, *AI Engineering: Building Applications with Foundation Models*, O'Reilly Media (2025). 535 pages. ISBN: 978-1-098-16630-4.

---

## 1. Executive Summary & The AI Engineering Paradigm

Chip Huyen establishes the formal discipline of **AI Engineering**: the systematic process of building, deploying, and maintaining production-grade applications powered by readily available foundation models (LLMs and LMMs). As foundation models lower the barriers to entry for software creation, the central engineering challenge shifts from model training to **architectural composition, context engineering, defense-in-depth guardrails, and rigorous multi-tier evaluation**.

### The Three Paradigms Compared:
| Dimension | Traditional Full-Stack Engineering | Traditional Machine Learning Engineering (MLE) | AI Engineering (AIE) |
| :--- | :--- | :--- | :--- |
| **Core Abstraction** | Deterministic algorithms, relational databases, business logic | Statistical models trained on curated tabular/structured datasets | Probabilistic foundation models adapted via context, prompting, and tools |
| **Development Lifecycle** | Waterfall / Agile sprint cycles, exact unit tests | Feature engineering, gradient descent, loss curve optimization | Context construction (RAG), prompt iteration, tool routing, evaluation rubrics |
| **Failure Modes** | Syntax errors, logic bugs, deadlocks, infrastructure crashes | Overfitting, data drift, vanishing gradients, concept drift | Hallucinations, tool call parameter errors, prompt injections, reasoning plateaus |
| **Verification Basis** | 100% deterministic assertion suites | Statistical validation sets (AUC, F1, RMSE) | Exact evaluation, functional simulation execution, and calibrated AI-as-a-Judge |

---

## 2. The 5-Step AI Engineering Architecture (Chapter 10)

Production AI applications require an end-to-end defense-in-depth architecture to guarantee reliability, low latency, and cost containment:

```
       +-------------------------------------------------------------------------------+
       |                     THE 5-STEP AI ENGINEERING ARCHITECTURE                    |
       +-------------------------------------------------------------------------------+
       | Step 1: Context Enhancement (RAG, Knowledge Graphs, Caching, Slicing)         |
       |                                      |                                        |
       |                                      v                                        |
       | Step 2: Input & Output Guardrails (PII/Secret Masking, Schema, Physics Bounds)|
       |                                      |                                        |
       |                                      v                                        |
       | Step 3: Model Router & Gateway (Intent Classification, Tiered Model Dispatch) |
       |                                      |                                        |
       |                                      v                                        |
       | Step 4: Multi-Tier Caching (Exact SHA-256 Cache, Semantic Jaccard/Embedding)  |
       |                                      |                                        |
       |                                      v                                        |
       | Step 5: Agent Patterns & Control Flows (Decoupled Planning, ReAct, Reflexion) |
       +-------------------------------------------------------------------------------+
```

### Detailed Architectural Breakdown:
1. **Step 1: Enhance Context**:
   - Context construction acts as feature engineering for foundation models.
   - Encompasses document retrieval (dense embeddings, BM25, hybrid search), structured database execution (SQL/SQLite), and remote zero-bloat volumetric slicing (e.g. 2D CHGCAR slices $<500\text{ KB}$).
2. **Step 2: Put in Guardrails**:
   - **Input Guardrails**: Credential isolation (redacting API keys, private tokens, certificates), prompt injection defenses, physical parameter range checks (e.g. positive cutoff energies, fractional coordinate boundaries $[0, 1)$).
   - **Execution Guardrails**: Hard runtime budgets (maximum 8 recovery attempts per Lee & Rondinelli), micro-batch walltime enforcement (capping Slurm jobs at 3h-4h to harvest backfill openings), memory consumption monitors.
   - **Output Guardrails**: Detection of empty or malformatted responses, ground-state physics anchors (`reached required accuracy`, `E0=`), catastrophic SCF divergence warnings (`BRMIX`, `POSCAR fatal error`).
3. **Step 3: Add Model Router and Gateway**:
   - **Router**: Intent classifiers route incoming queries to the optimal tool or model tier (e.g., routing trivial arithmetic to a Python calculator, geometry checks to `StructureSanityGuard`, and expensive multireference CASSCF to specialized agents).
   - **Gateway**: Centralized abstraction layer managing rate limits, fallback retries, secret key isolation, and token budget analytics.
4. **Step 4: Reduce Latency with Caches**:
   - **Exact Caching**: SHA-256 hash matching on identical keys and arguments; stores exact simulation outputs in SQLite with TTL.
   - **Semantic Caching**: Reuses cached answers for semantically equivalent queries using token set Jaccard similarity and character n-gram matching ($\ge 0.85$ threshold).
   - **Inference Caching**: KV-caching and prompt caching for shared system prompts and large reference catalogs.
5. **Step 5: Add Agent Patterns**:
   - Interleaves tool execution, conditional branching (`if-else`), looping (`while`/`for`), and multi-agent delegation.
   - Introduces write actions (e.g. launching HPC calculations, writing files, git commits) with strict sandboxing and human-in-the-loop gates.

---

## 3. Multi-Agent Systems, Planning & Tool Use (Chapter 6)

### A. What is an Agent?
An agent is characterized by its **environment** and the **set of actions** it can perform. By itself, a foundation model can only generate text or tokens; external tools make an agent vastly more capable by enabling read-only perception (retrievers, file readers) and write actions (code execution, file generation, job dispatch).

### B. Decoupled Planning vs. Execution (The 3-Component Multi-Agent Triad)
Chip Huyen emphasizes that coupling planning and execution in a single prompt risks runaway execution, infinite loops, and massive resource waste. To ensure robustness:
```
   [User Request] 
         │
         ▼
  +──────────────+         Plan          +────────────────+
  | PLANNER      | ────────────────────> | VALIDATOR      |
  | AGENT        | <──────────────────── | AGENT          |
  +──────────────+      (Critique/       +────────────────+
                        Regenerate)              │
                                                 │ Validated Plan
                                                 ▼
                                         +────────────────+
                                         | WORKER /       |
                                         | EXECUTOR AGENT |
                                         +────────────────+
```
- **Planner Agent**: Decomposes high-level goals into manageable subtasks and generates a structured plan.
- **Validator Agent**: Audits the plan before any execution begins (checks tool availability, verifies parameter types, enforces step budgets).
- **Executor Agent**: Calls external tools and executes individual actions sequentially or in parallel.
- **Because most agentic workflows are sufficiently complex to involve multiple specialized components, most production agents are fundamentally multi-agent systems.**

### C. Planning Granularity & Hierarchical Planning
- Detailed plans are hard to generate in advance because subsequent tool parameters often depend on previous tool outputs.
- High-level plans are easier to formulate but harder for a worker to execute blindly.
- **Hierarchical Planning**: Formulate a high-level strategic roadmap first (e.g., relaxation $\rightarrow$ static SCF $\rightarrow$ band structure $\rightarrow$ Bader analysis), then invoke localized sub-planners for each stage to resolve exact parameters dynamically.

### D. Control Flow Topologies
1. **Sequential**: Step A $\rightarrow$ Step B $\rightarrow$ Step C.
2. **Parallel**: Executes independent subtasks simultaneously (e.g. testing $k$-mesh convergence across multiple densities concurrently), significantly reducing latency.
3. **Conditional (`if-else`)**: Branches execution based on runtime observations (e.g., if band gap $> 0$, run hybrid HSE06; if metallic, enforce Methfessel-Paxton smearing).
4. **Iterative (`while`/`for`)**: Loops until physical convergence criteria are met, strictly bounded by a recovery budget (maximum 8 attempts) to prevent infinite loops.

### E. Reflection and Error Correction (ReAct vs. Reflexion)
- **ReAct** (Yao et al., 2022): Interleaves Thought, Action, and Observation at every micro-step.
- **Reflexion** (Shinn et al., 2023): Separates the Actor from an independent Evaluator and a Self-Reflection module. Upon failure, the Evaluator computes a score and failure diagnosis, the Self-Reflection module reasons over the error, and the Actor generates a revised trajectory.

### F. Tool Inventory Management
- More tools expand capabilities but increase cognitive load, context token costs, and tool selection errors.
- Literature trajectories: Toolformer (5 tools), Chameleon (13 tools), Gorilla (1,645 APIs).
- **Ablation Studies**: Regularly evaluate agent performance with individual tools removed; prune redundant or confusing tools.
- **Explicit Parameter Schemas**: Tool definitions must declare typed parameters, descriptions, and required constraints to prevent hallucinated argument values.

### G. Memory Systems
1. **Internal Knowledge**: Frozen model weights from pre-training.
2. **Short-Term Memory**: In-context conversation history, ephemeral working scratchpads, and active tool call outputs.
3. **Long-Term Memory**: External persistent databases (SQLite tables for TRITONDFT parameters, Liu et al. facts and traps, crystallized procedural skills, and DREAMS provenance registries).

---

## 4. Rigorous Evaluation Methodology (Chapters 3 & 4)

AI application evaluation must never rely on subjective "vibe checks". Chip Huyen formalizes a multi-tier evaluation framework:

### A. The Three Tiers of Evaluation
1. **Exact Evaluation**:
   - Deterministic schema matching, JSON parsing, regex anchoring, and AST syntax validation.
2. **Functional Correctness**:
   - Unit testing, script execution, and simulation oracle verification (pass/fail against external compilers, VASP/SIESTA/LAMMPS engines).
3. **AI-as-a-Judge**:
   - Employed for open-ended generation (hypotheses, reasoning explanations) strictly with:
     * Explicit, granular rubrics (e.g. 4-dimension Novelty/Validity/Clarity/Feasibility scoring).
     * Comparative evaluation (Elo / Bradley-Terry model pairing) to mitigate scoring drift.
     * Position-bias and length-bias mitigation.

### B. Component-Level vs. System-Level Evaluation
- **End-to-End Evaluation**: Testing only the final output masks which internal module caused a failure.
- **Component-Level Evaluation**: Isolates each component (retriever, parser, planner, code generator, verifier) and benchmarks its accuracy, latency, and error rate independently.
- Ensures fast root-cause isolation and prevents regressions when swapping sub-models or tools.

---

## 5. Defense-in-Depth Guardrails (Chapter 10, Step 2)

| Guardrail Tier | Target Failure Mode | Concrete Implementation Mechanism |
| :--- | :--- | :--- |
| **Input Guardrails** | Secret exposure, credential leakage, prompt injection, invalid parameters | Regex pattern scanners for API keys/tokens; Pydantic schema validation; POSCAR coordinate bounds $[0, 1)$; Slurm 5-day walltime rejection. |
| **Execution Guardrails** | Runaway loops, infinite reasoning, zombie processes, quota overruns | Lee & Rondinelli 8-attempt recovery budget; walltime limits; AMD EPYC core divisor enforcement (16, 32, 64, 128 cores); Carbono 384-core cap check. |
| **Output Guardrails** | Hallucinated convergence, unphysical energies, malformatted JSON | Ground-state physics anchor scanners (`reached required accuracy`, `E0=`); energy magnitude and finiteness audits ($|\Delta E| < 10^5\text{ eV}$); JSON schema validation. |

---

## 6. Observability & User Feedback Flywheels (Chapter 10)

### A. Core DevOps / AIOps Observability Metrics
- **MTTD (Mean Time to Detection)**: Latency between an agent error or convergence failure and the system's automated detection.
- **MTTR (Mean Time to Resolution)**: Time required for the agent's reflection loop to diagnose the failure, apply a parameter intervention, and resume execution.
- **CFR (Change Failure Rate)**: Percentage of simulation input mutations or code modifications that fail to run or diverge.

### B. Conversational User Feedback Loops
- **Explicit Feedback**: Direct user ratings (thumbs up/down, scalar satisfaction scores).
- **Implicit Conversational Feedback**: Extracted organically from follow-up user messages (e.g., user requesting corrections, re-running with modified constraints, or accepting deliverables).
- **Flywheel**: Feedback is captured in lifelong memory stores (Facts & Traps Store), crystallizing into verified procedural skills that prevent future regressions.

---

## 7. Direct Architectural Mapping to `sciresearch` MCP Ecosystem

| Chip Huyen AI Engineering Principle | Existing / Upgraded `sciresearch` Subsystem | Concrete MCP Tool / Module |
| :--- | :--- | :--- |
| **Context Enhancement (Step 1)** | DREAMS Shared Canvas & Volumetric Slicing | `canvas_register_artifact`, `extract_compact_2d_slice` |
| **Tri-Stage Guardrails (Step 2)** | Defense-in-Depth Guardrails Engine | `guardrails_audit_pipeline` (`scripts/guardrails_engine.py`) |
| **Model Router & Gateway (Step 3)** | SDE Discovery Harness & Intent Routing | `sde_verify_loop`, `evaluator_score_hypothesis` |
| **Hierarchical Caching (Step 4)** | Two-Tier Exact & Semantic Cache Store | `cache_query`, `cache_store_entry` (`scripts/cache_store.py`) |
| **Decoupled Multi-Agent Planning (Step 5)** | Plan-Validator-Executor Architecture | `protocol_validate_multistep`, `evaluator_score_input` |
| **Component-Level Evaluation (Ch. 3 & 4)** | Isolated Component Benchmark Suite | `evaluate_system_components` (`scripts/component_evaluator.py`) |
| **Reflexion Actor-Critic Loops (Ch. 6)** | MDAgent Reflexion & 8-Rule Decision Ladder | `diagnose_convergence_failure`, `log_decision` |
| **Three-Tier Memory Hierarchy (Ch. 6)** | TRITONDFT + Liu et al. Persistent Memory | `memory_store_calculation`, `memory_save_fact`, `skill_save_procedure` |
| **Conversational Feedback Flywheel (Ch. 10)** | Lifelong Facts & Procedural Skill Crystallization| `skill_crystallizer.py`, `facts_store.py` |
