# Simthesizer (2026): Agent-Driven Workload Simulation & Serving
**Reference**: W. Kim, H. Choi, M. Kim, J. Cho, Y. Kim, J. Park, *Simthesizer: An Agent-Driven Simulation Framework for LLM Serving Systems*, arXiv:2608.24650v2 (2026).

---

## 1. Core Problem & Concept
Evaluating complex multi-agent workflows on real HPC clusters or production LLM deployments is cost-prohibitive and slow. Simthesizer addresses this through **agent-driven synthetic trace simulation**:
- Models the dynamic interaction graph of requests, memory lookups, and computation.
- Simulates workload throughput, token consumption, and execution latencies before committing real cluster or API resources.

---

## 2. Key Methodological Lessons for Scientific Research Skills

1. **Synthetic Cost & Latency Pre-Flight**:
   - Before executing large high-throughput screening campaigns (e.g. hundreds of DFT crystal relaxations or multi-nanosecond MD runs), simulate the execution graph, estimated node-hours, and token budgets.
2. **Workload Graph Abstraction**:
   - Model the multi-agent scientific workflow as a unified dynamic execution graph, enabling bottleneck detection (e.g. where the agent waits synchronously on cluster queues or large file I/O).
3. **Hardware-Aware Adaptive Serving**:
   - Use simulated execution traces to tune cluster parameter allocations ($\theta_{hpc}$: cores, nodes, walltime), avoiding memory spills or queue starvation.
