# Liu et al. (2026): Lifelong Agent Memory for Materials Scientists
**Reference**: S. Liu, B. Hu, B. Ye, H. Cao, D. J. Srolovitz, T. Wen, *Harnessing agent memory to build lifelong AI partners for materials scientists*, arXiv:2608.11224v1 (2026).

---

## 1. Core Problem: The Decay of Operational Experience
In computational and experimental materials science, the most valuable asset is not a single script or model, but accumulated **research memory**:
- Which numerical parameters make phase-stability comparisons physically meaningful?
- Which structures must undergo symmetry-preserving pre-relaxation before phonon calculations?
- Which recurring calculation crashes are artifacts of charge sloshing rather than physical instability?

Today, this knowledge decays when research personnel move on, when directories are reorganized, or when LLM foundation models change. Existing agents treat the LLM as the unit of progress, losing all learned skills upon the next release.

---

## 2. Lifelong Memory Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGENT RUNTIME (ResearchAgent)                   │
│          Retrieve ──► Plan ──► Act ──► Reflect ──► Update              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        UNIFIED MEMORY SUBSYSTEM                        │
├───────────────────────────────────┬────────────────────────────────────┤
│ 1. FACTS STORE                    │ 2. SKILLS STORE                    │
│    - Empirical material properties│    - Validated simulation scripts  │
│    - Failure warnings & traps     │    - Reusable analysis workflows   │
│    - Boundary condition validity  │    - Synced with local SKILL.md    │
├───────────────────────────────────┴────────────────────────────────────┤
│ 3. LINKS & PROVENANCE GRAPH                                            │
│    - Bidirectional links between facts, skills, and execution traces   │
│    - Cross-session continuous accumulation                             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. The Retrieve-Plan-Act-Reflect-Update Lifecycle

1. **Retrieve (`search_memory` / `search_skill`)**:
   - Before launching expensive HPC jobs or parameter sweeps, query prior facts, past failure warnings, and proven scripts.
2. **Plan & Act**:
   - Execute workflows in sandboxed environments with strict timeouts and resource accounting.
3. **Reflect**:
   - Post-execution evaluation: did the simulation converge? Did it trigger known traps?
4. **Update (`save_to_memory` / `save_to_skill`)**:
   - If an error was diagnosed and resolved (e.g. through the 8-Rule Decision Ladder), crystallize the fix into a new Fact (warning) or Skill (reusable recipe).
   - Synchronize with human-readable markdown (`SKILL.md`) so human scientists and other models inherit the learned capability.
