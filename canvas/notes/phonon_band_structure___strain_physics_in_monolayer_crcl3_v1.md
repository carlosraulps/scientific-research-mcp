---
title: "Phonon Band Structure & Strain Physics in Monolayer CrCl3"
version: 1
created_at: "2026-10-04T11:47:46.182509+00:00"
tags: ["phonons", "strain", "CrCl3", "phonopy", "VASP"]
references: []
---

# Phonon Dispersion & Strain Engineering in Monolayer CrCl3

## 1. Phonopy Workflow Architecture: Base vs Consequential Calculations
1. **Base Equilibrium Relaxation:**
   - Primitive unit cell (Cr2Cl6) relaxed to ultratight force tolerance: `EDIFF = 1E-8 eV`, `EDIFFG = -0.001 eV/Å`, `PREC = Accurate`.
   - Produces the unperturbed equilibrium reference structure (`CONTCAR`).
2. **Supercell Generation & Finite Displacements:**
   - `phonopy -d --dim="3 3 1"` generates `SPOSCAR` (supercell with no displacements) and consequential displacement supercells (`POSCAR-001`, `POSCAR-002`, etc., typically displacement amplitude delta = 0.01 Å).
3. **Consequential Force Calculations:**
   - Single-point static SCF on each displaced supercell (`NSW = 0`, `IBRION = -1`, `EDIFF = 1E-8 eV`).
   - Symmetries reduce the number of independent displacements.
4. **Dynamical Matrix & Dispersion:**
   - Forces compiled via `phonopy -f disp-001/vasprun.xml disp-002/vasprun.xml ...` into `FORCE_SETS`.
   - `phonopy -p band.conf` diagonalizes the dynamical matrix D(q) across Gamma-M-K-Gamma.

## 2. Strain Effects on 2D Phonon Modes & Dynamical Stability
- **Flexural Acoustic Branch (ZA):** In 2D membranes, out-of-plane acoustic phonons exhibit quadratic dispersion omega(q) ~ B q^2 due to translational/rotational symmetry in vacuum.
- **Compressive Strain (epsilon < 0):** Induces negative mode stiffness for out-of-plane vibrations, driving omega^2 < 0 (imaginary/negative frequencies near Gamma) - the signature of Euler buckling instability.
- **Tensile Strain (epsilon > 0):** Linearizes the ZA branch near Gamma (introducing effective membrane tension) and globally softens in-plane acoustic (LA, TA) and optical phonon branches (red-shift).
- **Critical Threshold:** Beyond critical tensile strain (~6-8%), optical phonon softenings at zone boundaries (K or M) trigger structural phase transitions or bond rupture.

## 3. Electrocatalytic Connection (HER):
- Phonon density of states g(omega) integrates to Zero-Point Energy (EZPE = 0.5 \sum hbar omega) and vibrational entropy (TS_vib). Local modes around adsorbed H* shift Delta G_H* by +0.18 to +0.26 eV, directly dictating the volcano overpotential.