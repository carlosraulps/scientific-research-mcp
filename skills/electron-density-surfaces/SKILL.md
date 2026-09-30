---
name: electron-density-surfaces
description: Use when analyzing or visualizing 3D electron density isosurfaces (CHGCAR, LOCPOT, ELFCAR, Cube), generating 2D topological contour maps, extracting marching cubes meshes, or calculating planar electrostatic potentials and work functions.
---

# Electron Density & Molecular Surfaces Skill

## Overview
Comprehensive analysis and visualization toolkit for electronic structure, molecular orbitals, crystalline electron density localization, and electrostatic potentials (VASP `CHGCAR`, `LOCPOT`, `ELFCAR`, `PARCHG`, Gaussian `.cube`). Combines 3D polygonal isosurface extraction via `skimage.measure.marching_cubes`, 2D topological gradient/Laplacian mapping, planar-averaged work function calculation, and direct export to Wavefront `.obj`, interactive 3D HTML, VESTA, and XCrySDen.

## When to Use
- **Trigger**: Extracting 3D isosurfaces of charge density $\rho(\mathbf{r})$, ELF (Electron Localization Function), or molecular orbitals.
- **Trigger**: Exporting 3D surface meshes (`.obj`) to Blender for publication-quality ray-tracing.
- **Trigger**: Plotting 2D topological charge density slices with gradient vectors ($\nabla \rho$) or Laplacians ($\nabla^2 \rho$) to analyze bonding character (QTAIM / Bader attractors).
- **Trigger**: Calculating planar-averaged electrostatic potential $\overline{V}(z)$ from `LOCPOT` to determine the vacuum level $V_{\text{vac}}$ and surface work function $\Phi = V_{\text{vac}} - E_{\text{F}}$.
- **When NOT to use**:
  - Simple structure snapshots without volumetric grids (use [ovito-snapshot](../ovito-snapshot/SKILL.md) or [vesta-automation](../vesta-automation/SKILL.md)).
  - Band structures without real-space grids (extract eigenvalues directly).

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **Extract 3D Isosurface (OBJ & HTML)** | `density-analyzer CHGCAR -i 0.05 --obj surf.obj --html surf.html` |
| **2D Topological Slice ($xy$ at $z=0.5$)** | `density-analyzer CHGCAR --slice-plane xy --slice-pos 0.5 --slice-out slice_xy.png` |
| **2D Density Laplacian ($\nabla^2 \rho$)** | `density-analyzer CHGCAR --slice-plane xy --slice-out laplacian.png --laplacian` |
| **Planar Average Potential & Work Function** | `density-analyzer LOCPOT --planar-potential pot.png --fermi-energy -2.35` |
| **Analyze Gaussian Cube File** | `density-analyzer orbital.cube -i 0.02 --html orbital.html` |
| **Direct script execution** | `uv run --with scikit-image --with scipy --with matplotlib --with plotly python <script_path>/density_analyzer.py CHGCAR` |

## Script Options & Arguments

The underlying script is located at:
`skills/electron-density-surfaces/scripts/density_analyzer.py` (and wrapped in `~/.local/bin/density-analyzer`).

- `input`: Path to volumetric data file (`CHGCAR`, `LOCPOT`, `ELFCAR`, `PARCHG`, or `.cube`).
- `--isovalue`, `-i`: Threshold value for isosurface extraction (default: `0.05`). Typical ranges:
  - Total charge density (`CHGCAR`): `0.02` – `0.10 e/Å³`.
  - Electron Localization Function (`ELFCAR`): `0.70` – `0.85` (covalent/lone pair basins).
  - Molecular Orbitals (`.cube`): `0.01` – `0.05`.
- `--obj`: Output Wavefront `.obj` file path for 3D meshes (importable into Blender).
- `--html`: Output standalone interactive 3D HTML plot (powered by Plotly).
- `--slice-plane`: Crystallographic slice plane (`xy`, `xz`, or `yz`).
- `--slice-pos`: Fractional coordinate along normal axis ($0.0$ to $1.0$, default: $0.5$).
- `--slice-out`: Output path for 2D contour slice image (PNG).
- `--laplacian`: Toggle 2D Laplacian calculation ($\nabla^2 \rho$). Negative values (blue) denote electron accumulation (covalent sharing); positive values (red) denote electron depletion (ionic/closed-shell cores).
- `--no-gradient`: Hide gradient vector quiver arrows ($\nabla \rho$).
- `--planar-potential`: Output path for planar average electrostatic potential plot along $z$.
- `--fermi-energy`: Fermi energy ($E_{\text{F}}$ in eV) to annotate the work function $\Phi = V_{\text{vac}} - E_{\text{F}}$.

## Common Pitfalls & Solutions

1. **Isosurface appears empty or covers entire cell**: Check the units. VASP stores raw grid data multiplied by cell volume $\Omega$; `density_analyzer` handles volume scaling, but selecting an appropriate isovalue is essential. Start with `-i 0.05` for valence density.
2. **Missing atoms in 2D slice**: Atoms located more than $1.2\text{ Å}$ from the chosen slice plane are automatically culled to keep the topological section clean and uncluttered.
3. **Vacuum level identification**: In slab calculations with asymmetric surfaces or dipole corrections (`LDIPOL = .TRUE.`), inspect both vacuum regions to ensure asymptotic flatness.
