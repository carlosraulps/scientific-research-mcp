# AI Engineering: Architecture, Guardrails & Evaluation for Foundation Model Systems
**Reference**: Chip Huyen, *AI Engineering: Building Applications with Foundation Models*, O'Reilly Media (2025). ISBN: 978-1-098-16630-4.

---

## 1. Executive Summary & The AI Engineering Paradigm
Chip Huyen formalizes the transition from ad-hoc prompting and exploratory machine learning engineering to rigorous, production-grade **AI Engineering**. As foundation models become ubiquitous cognitive components, building reliable, cost-effective, and safe applications demands disciplined architectural patterns, comprehensive multi-tier evaluation, and defense-in-depth engineering.

```
       +-------------------------------------------------------------+
       |             THE 5-STEP AI ENGINEERING ARCHITECTURE          |
       +-------------------------------------------------------------+
       | Step 1: Context Enhancement (RAG, Caching, Graph Grounding) |
       |                               |                             |
       |                               v                             |
       | Step 2: Input & Output Guardrails (Schema, Pydantic, Safety)|
       |                               |                             |
       |                               v                             |
       | Step 3: Model Router & Gateway (Cost, Latency, Capability)  |
       |                               |                             |
       |                               v                             |
       | Step 4: Multi-Tier Caching (Prompt Cache, Semantic Cache)   |
       |                               |                             |
       |                               v                             |
       | Step 5: Agentic Execution (Plan-and-Execute, ReAct, Memory) |
       +-------------------------------------------------------------+
```

---

## 2. Rigorous Evaluation Methodology (Chapters 3 & 4)
Evaluating AI applications cannot rely on subjective "vibe checks" or single-metric benchmarks.

### The 3-Step Evaluation Pipeline:
1. **Component-Level Evaluation**:
   - Break complex agent pipelines into isolated components (retriever, parser, planner, code generator, verifier) and benchmark each independently.
   - Example: Evaluate whether the retrieval engine returns the correct pseudopotential before evaluating whether the simulation input file succeeds.
2. **Evaluation Guidelines & Gold Standards**:
   - Establish explicit, unambiguous rubrics for functional correctness, physical validity, and structural compliance.
3. **Multi-Faceted Metrics**:
   - **Exact Evaluation**: Deterministic schema validation, AST parsing, syntax execution.
   - **Functional Correctness**: Unit testing and simulation execution (pass/fail against external solvers).
   - **AI-as-a-Judge**: Employed strictly with explicit rubric anchoring, comparative ranking (Elo/Bradley-Terry), and position-bias mitigation.

---

## 3. Defense-in-Depth Guardrails (Chapter 10, Step 2)
Scientific AI systems require strict boundary validation to prevent silent data corruption:
- **Input Guardrails**:
  - Semantic sanitization, schema constraints, and format pre-validation (e.g. verifying POSCAR fractional coordinates fall within $[0, 1)$).
- **Execution Guardrails**:
  - Sandboxed execution, timeout limits, and resource budgeting before invoking heavy HPC or external CLI commands.
- **Output Guardrails**:
  - Deterministic post-processing, regex/JSON Schema validation, and physical consistency filters (e.g. ensuring energy convergence flags are strictly checked via anchors like `"End of run"` rather than generic strings).

---

## 4. Agent Architecture, Memory & Planning (Chapter 6)
- **Agent Failure Modes**:
  - Infinite loops, tool-calling hallucinations, plan divergence, and context window pollution.
- **Structured Planning**:
  - Plan-and-Execute architectures outperforming pure step-by-step ReAct on long-horizon, deterministic tasks.
  - Periodic plan re-evaluation against intermediate evidence.
- **Hierarchical Memory**:
  - **Short-Term Memory**: Ephemeral conversation buffer and working state.
  - **Long-Term Memory**: Structured episodic logs, factual databases (vector stores, SQLite), and procedural skills retrieved via semantic similarity and domain indices.

---

## 5. Architectural Blueprint for `sciresearch`
Based on Huyen's engineering principles:
1. **Input/Output Schema Enforcement**:
   All `sciresearch` tool parameters and JSON outputs must use strict typed validation (e.g., Pydantic models with clear error explanations).
2. **Component-Level Health Checks**:
   Add automated self-testing verifying individual MCP tools (canvas registry, provenance audit, ponytail delta composer, memory retrieval) in isolation.
3. **Hierarchical Caching**:
   Cache heavy queries and external tool invocations to minimize token overhead and latency during iterative refinement loops.
4. **Defensive Error Handling**:
   Ensure all simulation failures provide rich, actionable diagnostic context (traceback, physical interpretation, proposed fix) to avoid repeated agent stalls.
