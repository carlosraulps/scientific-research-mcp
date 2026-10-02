---
title: "authentic_vesta_cdd_3d_orbital_animation_v1"
version: 1
created_at: "2026-10-02T20:40:59.533517+00:00"
tags: ["cdd", "vesta", "isosurface", "animation", "photh-graphene"]
references: []
---

# Authentic VESTA Headless CLI 3D CDD Isosurface Animation

## Executive Summary
Generated high-definition 3D orbital animation of the Charge Density Difference ($\Delta\rho(\mathbf{r})$) for hydrogen chemisorption on PHOTH-graphene using VESTA's native headless CLI (`-export_img scale=2`).

## Key Advancements
1. **Zero Unit Cell Wireframe Artifacts**:
   - Identified that unit cell boundary lines can be suppressed in VESTA by setting `UCOLP 0 0 0.000 255 255 255` in `/home/cr/.VESTA/style/default.ini`.
   - Completely eliminated wireframe line cuts through the molecular orbitals and substrate atoms.
2. **Smooth 360-Degree Continuous Orbital Orbit**:
   - Synthesized 36 rotation frames ($10^\circ$ azimuthal increments) orbiting around the normal perspective axis.
   - Captured real VESTA glossy ball-and-stick carbon lattice and dual translucent isosurfaces:
     * Cyan ($\Delta\rho > 0$, $+0.005\ e/\mathrm{\AA}^3$): Charge accumulation at chemisorbed H and C-C bridge.
     * Yellow ($\Delta\rho < 0$, $-0.005\ e/\mathrm{\AA}^3$): Charge depletion along the active carbon rehybridized orbital.
3. **Publication Typography**:
   - Enforced TrueType Times New Roman and STIX mathematical glyphs in matplotlib compositing with standardized legend pill box.

## Output Files
- `06_charge_density_analysis/figures_cdd/anim_cdd_3d_vesta_orbital.gif`
- `06_charge_density_analysis/figures_cdd/anim_cdd_3d_orbital_rotation.gif`
