---
title: "Distributed Execution and Converged Benchmarks for Monolayer CrCl3"
version: 1
created_at: "2026-09-29T17:58:06.019443+00:00"
tags: ["crcl3", "dft_plus_u", "co_embedded", "her_catalysis", "provenance"]
references: ["6aba240c", "67595469"]
---

# Multi-Cluster Distributed Execution & Baseline Benchmarks for Monolayer CrCl3

## 1. Overview
Calculations for monolayer CrCl3 and single-atom transition metal substitutions (Co, Fe, Ni) were executed across distributed infrastructure:
- **Carbono Cluster**: Co-embedded two-phase pipeline (Job 165535 on node gn01) achieved complete convergence in Phase 1 (PBE+D3 BJ) and Phase 2 (+U, U=3.29 eV).
- **Huk Cluster**: Fe-embedded pipeline running on node huk120 (Job 7953, Phase 1 converged; Phase 2 in progress) and huk121 (Job 7954).
- **Local Arch Workstation**: Ni-embedded pipeline running locally across 16 Zen 3 cores (Jobs 190 and 191).

## 2. Converged Benchmarks & Artifact Provenance
- Artifact `6aba240c`: Co-embedded pristine monolayer Cr7CoCl24 converged to E0 = -152.68359 eV, with total magnetic moment M = 28.14 mu_B across 60 ionic relaxation steps.
- Artifact `67595469`: Pristine 2x2 CrCl3 + H* Site 1 (Top-Cl) ground state converged to E0 = -149.76937 eV, yielding binding energy Delta_E = -2.4655 eV, adsorption energy E_ads = 0.9145 eV, and HER free energy descriptor Delta_G_H* = +1.155 eV.

## 3. Hubbard U Dual Benchmark
The Hubbard U = 3.29 eV applied on Cr 3d manifolds was independently cross-validated:
1. Structural observable matching a(U) = a_exp = 6.056 A (Webster 2018; Luo 2020) yielding U* = 3.29 eV.
2. Cococcioni linear response ab initio fixed point yielding U_scf = 3.26 eV (L->inf asymptotic limit 3.27 eV, 2x2 supercell 3.32 eV).
The agreement within 0.03 eV (< 1%) confirms physical fidelity without empirical fitting.
