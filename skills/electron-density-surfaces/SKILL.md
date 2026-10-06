---
name: electron-density-surfaces
description: Use when analyzing or visualizing 3D electron density isosurfaces (CHGCAR, LOCPOT, ELFCAR, Cube), generating 2D topological contour maps, extracting marching cubes meshes, running flux-weighted Bader charge partitioning, or calculating planar electrostatic potentials and work functions.
---

# Electron Density & Molecular Surfaces Skill

## Overview
Comprehensive analysis and visualization toolkit for electronic structure, molecular orbitals, crystalline electron density localization, electrostatic potentials (VASP `CHGCAR`, `LOCPOT`, `ELFCAR`, `PARCHG`, Gaussian `.cube`), and **flux-weighted Bader charge partitioning**. Combines 3D polygonal isosurface extraction via `skimage.measure.marching_cubes`, 2D topological gradient/Laplacian mapping, planar-averaged work function calculation, and direct export to Wavefront `.obj`, interactive 3D HTML, VESTA, and XCrySDen.

## Key Capabilities & Scientific Protocols

### 1. Bader Charge Partitioning Protocol (`bader-analyze`)
- **The Periodic Boundary Discrete Grid Artifact**:
  - **Problem**: When a covalent bond crosses the periodic unit cell boundary ($x, y, \text{or } z = 0.0 / 1.0$) — as in PHOTH-graphene's $C_1\text{--}C_6$ bond — Henkelman's default steepest-ascent algorithm partitions electron density based on discrete on-grid gradient ascent. At larger strains, infinitesimal grid mesh shifts cause boundary voxels along the zero-flux dividing surface to suddenly flip assignment from atom $C_1$ to $C_6$. This creates artificial, sudden charge jumps (e.g. from $+0.109\,e$ down to $-0.049\,e$).
  - **Mandatory Protocol**:
    1. **Enforce Flux-Weighted Interpolation**:
       ```bash
       bader CHGCAR -b weight
       ```
       The `-b weight` algorithm interpolates boundary flux surfaces, ensuring that net Bader charges vary **strictly monotonically and continuously** across applied mechanical strain.
    2. **Core Charge Reference Integration & PAW Net Charge Offset**:
       When `AECCAR0` and `AECCAR2` are present, automatically sum them via `chgsum.pl AECCAR0 AECCAR2` into `CHGCAR_total` and run:
       ```bash
       bader CHGCAR -b weight -ref CHGCAR_total
       ```
       Net atomic charge is defined by electrostatic ionic core balance ($q = Z_{\text{core}} - Q_{\text{Bader}}$). In PAW pseudopotentials with frozen $1s^2$ cores, $Z_{\text{core}} = 4.0\,e$ for Carbon and $1.0\,e$ for Hydrogen:
       $$q_{\mathrm{C}} = 4.0 - Q_{\mathrm{bader}}(\mathrm{C}), \quad q_{\mathrm{H}} = 1.0 - Q_{\mathrm{bader}}(\mathrm{H})$$
       - Neutral: $Q = 4.000\,e \implies q_{\mathrm{C}} = 0.000\,e$
       - Anionic: $Q = 4.113\,e \implies q_{\mathrm{C}} = -0.113\,e$
       - Cationic: $Q = 3.892\,e \implies q_{\mathrm{C}} = +0.108\,e$
    3. **Wyckoff Symmetry Orbit Standardization ($\mathrm{C}_{\text{subindex}}^{(\text{superscript})}$)**:
       Cartesian FFT grid discretization cutting across mirror planes creates artificial numerical splitting ($\sim 0.14\,e$) between paired sites (e.g. $C_2^{(2)}$ vs $C_2^{(3)}$).
       Always group atoms by Wyckoff symmetry orbits and compute orbit averages $\bar{q}_{\text{orbit}}$ via `sciresearch bader-standardize` to prevent claiming spurious physical symmetry breaking.
    4. **Zero-Bloat Remote Slicing Protocol**:
       Never transfer gigabyte-scale 3D volumetric datasets (`CHGCAR`, `LOCPOT`, $>30\text{ MB}$ to GBs) across SSH. Slices are extracted directly on the remote cluster at the invariant nuclear plane ($z = 0.50$ for 2D sheets):
       ```bash
       sciresearch slice-2d CHGCAR --plane xy --z-slice 0.50 -o slice_ccd_z0.50.npz
       ```
       compressing the dataset to $<500\text{ KB}$ binary/npz before local download.
    5. **Automated Toolchain**:
       The `bader-analyze` and `sciresearch bader-standardize` CLI tools execute the entire protocol automatically, outputting `bader_summary.json` and `bader_charges.csv`.

### 2. 3D Isosurface Extraction & Wavefront OBJ Export
- Extracts polygonal meshes with `skimage.measure.marching_cubes`.
- Direct export to `.obj` meshes for photorealistic studio rendering in Blender with depth of field and ambient occlusion.
- Interactive standalone 3D HTML output powered by Plotly for web inspection.

### 3. 2D Topological Slicing & Laplacian Mapping
- Extracts 2D planar density cross-sections with gradient vector field overlays ($\nabla \rho$).
- Calculates the 2D Laplacian ($\nabla^2 \rho$):
  - Negative values (blue) highlight local charge accumulation (covalent electron sharing / shared-shell bonding).
  - Positive values (red) denote charge depletion (ionic / closed-shell core localization).

### 4. Planar-Averaged Potential & Work Function
- Averages local electrostatic potential $\overline{V}(z)$ across the $xy$ unit cell plane.
- Identifies the asymptotic vacuum level $V_{\text{vac}}$ in slab geometries and calculates the surface work function:
  $$\Phi = V_{\text{vac}} - E_{\mathrm{F}}$$

### 5. Volumetric Grid Periodic Unwrapping
- **Problem**: Reactive moieties at unit cell boundaries create charge density differences (CDD) split across the periodic boundary, causing truncated 2D contour mappings.
- **Solution**: Volumetric grids are shifted via `np.roll` based on fractional shifts or auto-centered using the `max_gradient`, `max_abs`, or `centroid` of the electron density features.

---

## Quick Reference CLI

| Action | CLI Command |
| :--- | :--- |
| **Robust Flux-Weighted Bader Analysis** | `bader-analyze . --chgcar CHGCAR --poscar POSCAR` |
| **Extract 3D Isosurface (OBJ & HTML)** | `density-analyzer CHGCAR -i 0.05 --obj surf.obj --html surf.html` |
| **2D Topological Slice ($xy$ at $z=0.5$)** | `density-analyzer CHGCAR --slice-plane xy --slice-pos 0.5 --slice-out slice_xy.png` |
| **2D Density Laplacian ($\nabla^2 \rho$)** | `density-analyzer CHGCAR --slice-plane xy --slice-out laplacian.png --laplacian` |
| **Planar Potential & Work Function** | `density-analyzer LOCPOT --planar-potential pot.png --fermi-energy -2.35` |
| **Analyze Gaussian Cube File** | `density-analyzer orbital.cube -i 0.02 --html orbital.html` |
| **Unwrap Volumetric Periodic Boundary** | `volumetric-unwrap cdd.vasp --auto-center --method max_abs -o cdd_centered.vasp` |

---

## Script Architecture & CLI Binaries

Installed globally in `~/.local/bin/`:
- `bader-analyze` -> `skills/electron-density-surfaces/scripts/bader_flux_analysis.py`
- `density-analyzer` -> `skills/electron-density-surfaces/scripts/density_analyzer.py`
- `volumetric-unwrap` -> `skills/electron-density-surfaces/scripts/volumetric_unwrap.py`
- `bader` -> Henkelman Bader analysis executable
- `chgsum.pl` -> Core + valence charge density summation script
