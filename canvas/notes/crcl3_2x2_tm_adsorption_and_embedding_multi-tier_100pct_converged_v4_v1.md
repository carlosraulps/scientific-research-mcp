---
title: "crcl3_2x2_tm_adsorption_and_embedding_multi-tier_100pct_converged_v4"
version: 1
created_at: "2026-10-07T22:08:49.379335+00:00"
tags: ["dft", "crcl3", "her", "multitier", "convergence"]
references: ["22e6c873"]
---

# CrCl3 2x2 TM Adsorption & Embedding Multi-Tier Benchmark: 100% Convergence Achieved

## Milestone Summary
The complete 3x2x3 systematic benchmark matrix across all 18 computational systems is now **100% CONVERGED** across three methodological tiers:
1. Tier 1: vdW Dispersion (PBE+D3(BJ), U = 0) [6/6 pairs complete]
2. Tier 2: Single-Site Hubbard U (PBE+D3 + U_Cr = 3.29 eV) [6/6 pairs complete]
3. Tier 3: Multi-Site Hubbard U (PBE+D3 + U_Cr = 3.29 eV & U_TM = 3.29 eV) [6/6 pairs complete]

## Tier 3 (+U_all = 3.29 eV) Final Numerical Dataset
- **Co_ads**: E_clean = -150.58281 eV, E_H* = -154.15985 eV => ΔE_ads = -0.191 eV, ΔG_H* = **+0.065 eV** (Sabatier Apex, M = 27.0 μ_B)
- **Co_emb**: E_clean = -152.31146 eV, E_H* = -154.56415 eV => ΔE_ads = +1.133 eV, ΔG_H* = **+1.389 eV** (Deactivated, M = 29.0 μ_B)
- **Fe_ads**: E_clean = -153.94703 eV, E_H* = -155.75141 eV => ΔE_ads = +1.581 eV, ΔG_H* = **+1.837 eV** (M = 30.0 μ_B)
- **Fe_emb**: E_clean = -153.79065 eV, E_H* = -155.61036 eV => ΔE_ads = +1.561 eV, ΔG_H* = **+1.822 eV** (M = 30.0 μ_B)
- **Ni_ads**: E_clean = -150.28286 eV, E_H* = -152.74034 eV => ΔE_ads = +0.928 eV, ΔG_H* = **+1.184 eV** (M = 24.0 μ_B)
- **Ni_emb**: E_clean = -150.78790 eV, E_H* = -153.40561 eV => ΔE_ads = +0.768 eV, ΔG_H* = **+1.024 eV** (M = 28.0 μ_B)

## Physical Insights
- Surface-adsorbed Cobalt remains in the optimal Sabatier window across all three tiers (+0.18 eV in vdW, -0.07 eV in +U_Cr, +0.065 eV in +U_all), demonstrating that Co_ads is an intrinsically robust, near-ideal HER electrocatalyst regardless of TM Hubbard U treatment.
- In-plane embedding consistently degrades catalytic activity for all three transition metals due to strong d-orbital coordination with the CrCl3 network.
- Figure artifact `crcl3_tm_abs_vs_emb_multitier.png` and `.pdf` regenerated and synchronized to remote master.