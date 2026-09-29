---
title: "PHOTH-Graphene DFT & MD Convergence Benchmarks and Supercell Scaling Report"
version: 1
created_at: "2026-09-29T19:14:46.740736+00:00"
tags: ["dft", "photh-graphene", "convergence", "supercell", "lammps", "reaxff", "hpc"]
references: []
---

# PHOTH-Graphene Comprehensive Convergence Benchmarks & Supercell Scaling

## 1. Executive Summary
- **System**: Monolayer PHOTH-Graphene (Orthorhombic C10 unit cell, containing 4-, 8-, and hexagonal carbon rings).
- **HPC Execution**: Dispatched to Huk cluster (`huk128`, 24 physical cores Intel Xeon Gold, 126 GB RAM) in partition `normal`.
- **DFT Ground State**: ENCUT converged at 500 eV (< 1 meV/atom window); K-points converged at 6x11x1 anisotropic Monkhorst-Pack grid.
- **Supercell Energy Stability**:
  - $1\times 1\times 1$ (10 atoms): $E_0 = -86.7731$ eV ($-8.6773$ eV/atom)
  - $2\times 2\times 1$ (40 atoms): $E_0 = -347.1378$ eV ($-8.6785$ eV/atom, $\Delta E = 1.1$ meV/atom)
  - $3\times 3\times 1$ (90 atoms): $E_0 = -780.8784$ eV ($-8.6764$ eV/atom, $\Delta E = 0.9$ meV/atom)

## 2. Supercell Transferability Rules (NotebookLM Grounded)
1. **ENCUT is Strictly Transferable**: Plane-wave cutoff is an atomic/pseudopotential core augmentation requirement. Converged value on the unit cell transfers without modification to any supercell size.
2. **K-Points Fold Inversely**: BZ volume contracts by $1/(N_x N_y N_z)$. The sampling grid must be scaled as $k_i' = \lceil k_i / N_i \rceil$. Full parametric sweeps on supercells are redundant.
3. **MD Parameters are Size-Invariant**: Timestep $\Delta t = 0.25 - 0.50$ fs and thermostat damping $T_{\text{damp}} \approx 100 \times \Delta t$ depend on local potential stiffness (ReaxFF C-C bonds) and do not scale with supercell size.
4. **2D Physical Constraints**: Systems require $L \ge 20$ Å ($4\times 4$ or larger) to capture out-of-plane acoustic ZA flexural modes ($\omega \propto q^2$) without periodic truncation distortion.
