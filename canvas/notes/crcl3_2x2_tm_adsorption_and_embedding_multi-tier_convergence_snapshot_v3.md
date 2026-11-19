---
title: "CrCl3 2x2 TM Adsorption and Embedding Multi-Tier Convergence Snapshot"
version: 3
created_at: "2026-10-06T00:00:58.845752+00:00"
tags: ["crcl3", "hpc", "server_info", "convergence", "u_all329", "co_fe_ni"]
references: ["22e6c873"]
---

# CrCl3 2x2 TM Adsorption and Embedding Multi-Tier Convergence Snapshot (October 5, 2026 - 21:00 BRT)

## 1. Major Milestone: 5 Out of 6 Pairs Fully Converged in Tier 3 (+U_all = 3.29 eV)
Five complete pairs of clean and hydrogen-adsorbed systems have now fully reached ground-state convergence:

1. **Co (adsorbed) [100% Converged Pair]**:
   - Clean: $E_0 = -150.58281$ eV ($M_{\text{tot}} = 27.00\ \mu_{\mathrm{B}}$)
   - With H: $E_0 = -154.15985$ eV ($M_{\text{tot}} = 28.00\ \mu_{\mathrm{B}}$)
   - $\Delta E = -3.57704$ eV $\implies E_{\text{ads}} = -0.191$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +0.065\text{ eV}}$ (**Sabatier Sweet Spot!**)

2. **Co (embedded) [100% Converged Pair]**:
   - Clean: $E_0 = -152.31146$ eV ($M_{\text{tot}} = 29.00\ \mu_{\mathrm{B}}$)
   - With H: $E_0 = -154.56415$ eV ($M_{\text{tot}} = 28.00\ \mu_{\mathrm{B}}$)
   - $\Delta E = -2.25269$ eV $\implies E_{\text{ads}} = +1.133$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +1.389\text{ eV}}$ (Deactivated)

3. **Fe (adsorbed) [100% Converged Pair]**:
   - Clean: $E_0 = -153.94703$ eV ($M_{\text{tot}} = 30.00\ \mu_{\mathrm{B}}$)
   - With H (Huk Job 8051, Step 54): $E_0 = -155.75141$ eV ($M_{\text{tot}} = 29.00\ \mu_{\mathrm{B}}$)
   - $\Delta E = -1.80438$ eV $\implies E_{\text{ads}} = +1.581$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +1.837\text{ eV}}$
   - $E_{\text{bind}} = -6.643$ eV

4. **Fe (embedded) [100% Converged Pair]**:
   - Clean: $E_0 = -153.79065$ eV ($M_{\text{tot}} = 30.00\ \mu_{\mathrm{B}}$)
   - With H: $E_0 = -155.61036$ eV ($M_{\text{tot}} = 29.00\ \mu_{\mathrm{B}}$)
   - $\Delta E = -1.81971$ eV $\implies E_{\text{ads}} = +1.566$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +1.822\text{ eV}}$ (Deactivated)
   - $E_{\text{bind}} = -6.487$ eV

5. **Ni (embedded) [100% Converged Pair]**:
   - Clean (Carbono Job 167940, Step 16): $E_0 = -150.78790$ eV ($M_{\text{tot}} = 28.00\ \mu_{\mathrm{B}}$)
   - With H (Carbono Job 167941, Step 19): $E_0 = -153.40561$ eV ($M_{\text{tot}} = 27.00\ \mu_{\mathrm{B}}$)
   - $\Delta E = -2.61771$ eV $\implies E_{\text{ads}} = +0.768$ eV $\implies \mathbf{\Delta G_{\text{H}^*} = +1.024\text{ eV}}$ (Deactivated)
   - $E_{\text{bind}} = -3.484$ eV

6. **Ni (adsorbed) [In-Flight Final Phase]**:
   - With H: Fully converged on Huk ($E_0 = -152.74034$ eV, $M_{\text{tot}} = 25.00\ \mu_{\mathrm{B}}$)
   - Clean: Actively calculating in Job 8073 on Huk (`huk125`) and queued in Job 169656 on Carbono (`nanotubo`).

## 2. Remote Synchronization & Version Control
- All changes from other computers pulled cleanly with zero conflicts (`master` branch).
- Publication figures `crcl3_tm_abs_vs_emb_multitier.png` (.pdf) regenerated and pushed to GitHub `origin/master` (Commit `ed80b29`).
