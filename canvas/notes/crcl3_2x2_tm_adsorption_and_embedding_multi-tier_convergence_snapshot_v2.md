---
title: "CrCl3 2x2 TM Adsorption and Embedding Multi-Tier Convergence Snapshot"
version: 2
created_at: "2026-10-05T10:16:39.592103+00:00"
tags: ["crcl3", "hpc", "server_info", "convergence", "u_all329", "co_fe_ni"]
references: ["22e6c873"]
---

# CrCl3 2x2 TM Adsorption and Embedding Multi-Tier Convergence Snapshot (October 5, 2026 - 07:15 BRT)

## 1. Major Convergence Breakthroughs in the +U_all Suite (U_Cr = 3.29 eV & U_TM = 3.29 eV)
Three complete pairs of clean and hydrogen-adsorbed systems have now fully converged:

1. **Co (adsorbed) [100% Converged Pair]**:
   - Clean (Carbono Job 167938): $E_0 = -150.58281$ eV ($M_{\text{tot}} = 27.00\ \mu_{\mathrm{B}}$, Step 55)
   - With H (Carbono): $E_0 = -154.15985$ eV ($M_{\text{tot}} = 28.00\ \mu_{\mathrm{B}}$, Step 16)
   - Adsorption thermodynamics: $\Delta E = -3.57704$ eV $\implies E_{\text{ads}} = -0.19134$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +0.065\text{ eV}}$!
   - **Conclusion:** Surface-adsorbed Co firmly retains its **optimal Sabatier catalytic sweet spot** ($|\Delta G_{\text{H}^*}| \le 0.15$ eV) across all 3 methodological tiers ($+0.18$ eV in vdW, $-0.07$ eV in $+U_{\text{Cr}}$, $+0.065$ eV in $+U_{\text{all}}$).

2. **Co (embedded) [100% Converged Pair]**:
   - Clean (Carbono): $E_0 = -152.31146$ eV ($M_{\text{tot}} = 29.00\ \mu_{\mathrm{B}}$, Step 27)
   - With H (Carbono Job 167939): $E_0 = -154.56415$ eV ($M_{\text{tot}} = 28.00\ \mu_{\mathrm{B}}$, Step 54)
   - Adsorption thermodynamics: $\Delta E = -2.25269$ eV $\implies E_{\text{ads}} = +1.13301$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +1.389\text{ eV}}$!
   - **Conclusion:** Near-perfect agreement with Tier 2 ($+U_{\text{Cr}}$: $+1.375$ eV, $\Delta = 14$ meV), rigorously confirming that octahedral 6-fold coordination deactivates the Co active site.

3. **Fe (embedded) [100% Converged Pair]**:
   - Clean (Carbono): $E_0 = -153.79065$ eV ($M_{\text{tot}} = 30.00\ \mu_{\mathrm{B}}$, Step 8)
   - With H (Carbono): $E_0 = -155.61036$ eV ($M_{\text{tot}} = 29.00\ \mu_{\mathrm{B}}$, Step 28)
   - Adsorption thermodynamics: $\Delta E = -1.81971$ eV $\implies E_{\text{ads}} = +1.56599$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +1.822\text{ eV}}$!

4. **Ni (adsorbed) + H [Single Milestone Converged]**:
   - With H (Huk Job 8053): Reached required accuracy at Step 13, $E_0 = -152.74034$ eV ($M_{\text{tot}} = 25.00\ \mu_{\mathrm{B}}$).

5. **Fe (adsorbed) clean [Single Milestone Converged]**:
   - Clean (Huk): Reached required accuracy at Step 6, $E_0 = -153.94703$ eV ($M_{\text{tot}} = 30.00\ \mu_{\mathrm{B}}$).

## 2. In-Flight Calculations Status
- **Huk (`ssh huk`)**:
  - `Fe_ads_H_Uall` (Job 8051 on `huk124`, 28 cores): RUNNING for 15h 02m at Ionic Step 28 ($E_0 = -155.65943$ eV, $\text{mag} = 29.00\ \mu_{\mathrm{B}}$).
  - `Ni_ads_c_Uall` (Job 8052 on `huk125`, 28 cores): RUNNING for 15h 02m at Ionic Step 12 ($E_0 = -149.74240$ eV, $\text{mag} = 24.00\ \mu_{\mathrm{B}}$).
- **Carbono (`ssh carbono`)**:
  - `Ni_emb_c_Uall` (Job 167940 on `n01`, 32 cores): RUNNING for 3h 45m at Ionic Step 15 ($E_0 = -150.78748$ eV, $\text{mag} = 28.00\ \mu_{\mathrm{B}}$, $dE \approx -1$ meV).
  - `Ni_emb_H_Uall` (Job 167941 on `n06`, 32 cores): RUNNING for 1h 13m at Ionic Step 2 ($E_0 = -153.35822$ eV, $\text{mag} = 27.00\ \mu_{\mathrm{B}}$).

## 3. Provenance & Artifacts
- Master figure `crcl3_tm_abs_vs_emb_multitier.png` (.pdf) updated with 3 solid bars for converged pairs and pushed to Git `master` (Commit `4083988`).
