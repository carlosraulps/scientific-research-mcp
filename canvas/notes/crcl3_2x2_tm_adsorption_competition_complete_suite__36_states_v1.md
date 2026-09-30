---
title: "CrCl3 2x2 TM Adsorption Competition Complete Suite (36 States)"
version: 1
created_at: "2026-09-30T20:29:41.320345+00:00"
tags: ["crcl3", "tm_adsorption", "dft_plus_u", "vdw_d3", "fe", "co", "ni", "her"]
references: []
---

# Transition Metal Adsorption Competition Suite on CrCl3 (2x2) Monolayer - 100% Completed

All 36/36 states across Co, Ni, and Fe adsorption on 2x2 CrCl3 monolayers have been fully relaxed, calculated, and cross-verified.

### Key Results Summary:
1. **Fe Adsorption (Ground State: Site 1 / Top-Cl)**:
   - Pure PBE: E_bind = -5.617 eV
   - PBE+D3: E_bind = -6.809 eV
   - PBE+D3+U (U_Cr = 3.29 eV):
     - S1 (Top-Cl): E_bind = -7.531 eV (Ground State)
     - S2 (Hollow): E_bind = -6.126 eV (+1.405 eV penalty)
     - S3 (Top-Cr): E_bind = -5.628 eV (+1.902 eV penalty)

2. **Ni Adsorption (Ground State: Site 2 / Hollow)**:
   - Pure PBE: E_bind = -3.791 eV
   - PBE+D3: E_bind = -4.204 eV
   - PBE+D3+U:
     - S1 (Top-Cl): E_bind = -3.421 eV (+0.951 eV penalty)
     - S2 (Hollow): E_bind = -4.372 eV (Ground State)
     - S3 (Top-Cr): E_bind = -3.448 eV (+0.924 eV penalty)

3. **Co Adsorption**:
   - PBE+D3: S2 (Hollow) ground state (E_bind = -5.060 eV)
   - PBE+D3+U: S1 (Top-Cl) ground state (E_bind = -5.143 eV), with S2 competing at -5.042 eV (+0.101 eV penalty).

### Updated Publication Figures:
- `crcl3-newcals/postprosseing/tm_site_competition_multipanel.png` (.pdf)
- `crcl3-newcals/postprosseing/tm_site_preference_barchart.png` (.pdf)
All plots adhere to GEMINI.md publication plotting zero-overlap policy with adaptive headroom and smart pedestals.
