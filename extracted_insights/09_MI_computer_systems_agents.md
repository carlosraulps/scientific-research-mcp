# Mi et al. (2025): Computer Systems Insights for LLM Agents
**Reference**: Y. Mi, Z. Gao, X. Ma, Q. Li, *Building LLM Agents by Incorporating Insights from Computer Systems*, arXiv:2504.04485v1 (2025).

---

## 1. The von Neumann Analogy for LLM Agents
Mi et al. demonstrate that LLM agent architectures parallel modern computer systems:
- **LLM Core $\approx$ CPU**: Performs reasoning, planning, and instruction execution.
- **Agent Memory Hierarchy $\approx$ Computer Memory Hierarchy**: Stratified by speed, persistence, and capacity.

```
       COMPUTER HIERARCHY                    AGENT HIERARCHY
┌───────────────────────────────┐     ┌───────────────────────────────┐
│ Registers & L1 Cache          │ ◄─► │ System Prompt & Active Scratch│
├───────────────────────────────┤     ├───────────────────────────────┤
│ L2 / L3 Cache                 │ ◄─► │ Working Memory (Task Checklist│
│                               │     │ & Session Context)            │
├───────────────────────────────┤     ├───────────────────────────────┤
│ Main Memory (RAM)             │ ◄─► │ Short-Term Stores & Checkpoint│
│                               │     │ Registries (SQLite/JSON)      │
├───────────────────────────────┤     ├───────────────────────────────┤
│ Secondary Storage (Disk/SSD)  │ ◄─► │ Long-Term Knowledge Graph     │
│                               │     │ Vector DB & Archival FS       │
└───────────────────────────────┘     └───────────────────────────────┘
```

---

## 2. Core Systems Principles Applied to Scientific Agents

1. **Context Virtualization & Paging**:
   - Just as an OS swaps pages between RAM and disk to avoid running out of physical memory, an agent must page older conversation turns and intermediate file outputs to persistent storage (`checkpoints/`, `runs/`) while retaining lightweight pointer IDs (`result_id`) in active context.
2. **Process Management & Multi-Agent IPC**:
   - Multi-agent coordination requires formal Inter-Process Communication (IPC). The Model Context Protocol (MCP) functions as the standard JSON-RPC bus.
3. **Interrupt Handling & Priority Scheduling**:
   - Long-horizon simulations require non-blocking job monitoring with interrupt signals (e.g. SLURM `SIGUSR1`, convergence thresholds) alerting the agent only upon completion or anomaly.
