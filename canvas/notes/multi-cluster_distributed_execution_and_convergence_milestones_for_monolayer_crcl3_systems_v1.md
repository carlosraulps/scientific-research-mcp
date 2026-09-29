---
title: "Multi-Cluster Distributed Execution and Convergence Milestones for Monolayer CrCl3 Systems"
version: 1
created_at: "2026-09-29T20:14:01.684736+00:00"
tags: ["crcl3", "her", "dft_plus_u", "co_fe_ni", "convergence", "hpc"]
references: ["6aba240c", "67595469", "9721a455", "a765b3ed"]
---

# Multi-Cluster Distributed Execution and Convergence Milestones for Monolayer CrCl3 Systems

## 1. Executive Status
This note records the live multi-cluster convergence state across Carbono, Huk, and Arch for single-atom embedded transition metal (Co, Fe, Ni) monolayer CrCl3 systems:

- **Co-Embedded Clean (Cr8CoCl24)**: Fully converged under PBE+D3(BJ)+U (U_Cr = 3.29 eV) in Carbono metano on node gn01 (Artifact 6aba240c) at E0 = -152.68359 eV, M_tot = 28.1422 mu_B.
- **Ni-Embedded Clean (Cr8NiCl24)**: Phase 1 (PBE+D3) converged in 8 ionic steps on Carbono node n04 (Job 165245, Artifact 9721a455) at E0 = -165.48960 eV, M_tot = 24.0000 mu_B. Phase 2 (+U) actively calculating in-allocation.
- **Co-Embedded + H (Cr8CoCl24H)**: Reached Step 12 in Phase 2 (+U) on n12 at E0 = -154.69642 eV (Artifact a765b3ed), while sister job 165536 on gn01 is calculating under a 24h allocation.
- **Fe-Embedded Clean (Cr8FeCl24)**: Actively calculating Phase 2 (+U) on Huk (huk120, Job 7953) using DecisionCouncil-approved RMM-DIIS (ALGO = Fast) at Step 3 (E0 = -153.9947 eV).
- **Fe-Embedded + H (Cr8FeCl24H)**: Down to F_max = 0.0423 eV/A at Step 13 on Carbono n11 (Job 165244), within 2-3 steps of Phase 1 convergence.

## 2. Infrastructure & Algorithmic Acceleration Opportunities
- Carbono partition `etileno` features node `gn04` with 64 idle CPUs and 24h walltime. This provides an immediate opportunity to dispatch the advanced Step 12 checkpoint of Co+H for sub-30 minute completion.
- RMM-DIIS (`ALGO = Fast`) combined with `NELMIN = 4` and `POTIM = 0.25` provides a ~3x speedup per ionic step for pre-converged Phase 2 runs, demonstrated on Huk huk120.