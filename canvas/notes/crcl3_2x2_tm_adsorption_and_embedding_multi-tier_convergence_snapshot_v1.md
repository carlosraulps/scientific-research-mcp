---
title: "CrCl3 2x2 TM Adsorption and Embedding Multi-Tier Convergence Snapshot"
version: 1
created_at: "2026-10-04T23:15:49.477487+00:00"
tags: ["crcl3", "hpc", "server_info", "convergence", "u_all329", "her"]
references: ["22e6c873"]
---

# CrCl3 2x2 TM Adsorption and Embedding Multi-Tier Convergence Snapshot (October 4, 2026 - 20:15 BRT)

## 1. Huk Cluster Live Telemetry (Active Calculations)
All 4 targeted jobs on Huk are actively computing in parallel:
- **Job 8051 (`Fe_ads_H_Uall`)** on node `huk124` (Partition: `medio`, 28 cores):
  - Elapsed walltime: 4h 07m
  - Progress: Reached Ionic Step 7 ($E_0 = -155.56348$ eV, $\text{mag} = 29.00\ \mu_{\mathrm{B}}$, $dE = -8.85\times 10^{-3}$ eV).
  - Currently computing Step 8 SCF (DAV: 6).
- **Job 8052 (`Ni_ads_c_Uall`)** on node `huk125` (Partition: `normal`, 28 cores):
  - Elapsed walltime: 4h 07m
  - Progress: Reached Ionic Step 3 ($E_0 = -149.66374$ eV, $\text{mag} = 24.00\ \mu_{\mathrm{B}}$).
  - Currently computing Step 4 SCF (DAV: 40).
- **Job 8053 (`Ni_ads_H_Uall`)** on node `huk122` (Partition: `medio`, 28 cores):
  - Elapsed walltime: 1h 42m
  - Progress: Reached Ionic Step 2 ($E_0 = -152.73595$ eV, $\text{mag} = 25.00\ \mu_{\mathrm{B}}$, $dE = -8.15\times 10^{-4}$ eV).
  - Step 3 SCF active (DAV: 10, residual $< 10^{-4}$). Very close to final force convergence ($dE < 1$ meV).
- **Job 8054 (`Fe_S2_U3`)** on node `huk126` (Partition: `normal`, 24 cores):
  - Elapsed walltime: 4h 07m
  - Progress: Reached Ionic Step 25 ($E_0 = -153.65595$ eV, $\text{mag} = 29.18\ \mu_{\mathrm{B}}$, $dE = -7.91\times 10^{-4}$ eV).

## 2. Carbono Cluster Queue Status
- **Partition `nanotubo` (32 cores each)**:
  - Job 167938 (`Co_ads_c_Uall`): PENDING (Priority)
  - Job 167939 (`Co_emb_H_Uall`): PENDING (Priority)
  - Job 167940 (`Ni_emb_c_Uall`): PENDING (Priority)
  - Job 167941 (`Ni_emb_H_Uall`): PENDING (Priority)
  - Ready for immediate dispatch as active jobs on nodes `n07, n11, n12, n14` finish their allocations.

## 3. Converged Benchmarks in the Multi-Tier Suite
- $\text{Fe}_{\text{emb}}$ ($+U_{\text{all}} = 3.29$ eV):
  - Clean: $E_0 = -153.79065$ eV
  - $\text{H}^*$: $E_0 = -155.61036$ eV
  - $\Delta E = -1.81971$ eV $\implies E_{\text{ads}} = +1.565$ eV $\implies \Delta G_{\text{H}^*} = +1.821$ eV.
- Unconverged $+U_{\text{all}}$ pairs remain cleanly staged and visually marked as running/queued with zero invented data in `crcl3_tm_abs_vs_emb_multitier.png`.
