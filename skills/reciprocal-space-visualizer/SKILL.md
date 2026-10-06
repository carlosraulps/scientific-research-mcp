---
name: reciprocal-space-visualizer
description: Use when constructing, analyzing, or rendering 3D first Brillouin zones, Wigner-Seitz reciprocal cells, SeeK-path standardized k-vector paths, 2D monolayer hexagonal/rectangular projections, or generating VASP KPOINTS band structures.
---

# 🌐 Reciprocal Space & Brillouin Zone Visualizer Skill

## Overview
Automates the construction, high-symmetry path identification, and publication-grade rendering of **Reciprocal Space & 3D Brillouin Zones** for crystalline materials and 2D monolayers. Based on exact Voronoi Dirichlet tessellation of reciprocal lattices, SeeK-path crystallographic standardization (HPKOT protocol), and Physical Review/Nature styling.

---

## 🚀 Key Capabilities

1. **Exact 1st Brillouin Zone Geometry**:
   - Calculates reciprocal lattice vectors $\mathbf{b}_i = 2\pi \frac{\mathbf{a}_j \times \mathbf{a}_k}{\mathbf{a}_i \cdot (\mathbf{a}_j \times \mathbf{a}_k)}$.
   - Computes the exact Wigner-Seitz cell via Voronoi polyhedron tessellation of reciprocal lattice points.
   - Depth-tested 3D wireframe rendering (solid forward edges, dashed rear hidden edges).

2. **SeeK-path Crystallographic Standardization**:
   - Automated identification of space group, bravais lattice, and standardized high-symmetry $k$-points ($\Gamma, \mathrm{K}, \mathrm{M}, \mathrm{X}, \mathrm{W}, \mathrm{L}, \mathrm{Z}, \mathrm{U}$, etc.).
   - Automatic generation of continuous high-symmetry $k$-paths for electronic band structure calculations.
   - Exports ready-to-run VASP `KPOINTS` (Line-mode).

3. **2D Material Protocol (Hexagonal / Rectangular Layers)**:
   - Identifies non-periodic vacuum directions ($c$-axis).
   - Generates pure 2D planar cross-sections ($k_z = 0$) or 3D hexagonal prisms with transparent shading.
   - Highlights $K - \Gamma - M - K$ contours for graphene, TMDs, and trihalides ($\mathrm{CrCl}_3$).

4. **Publication Visual Styling**:
   - Translucent irreducible Brillouin zone (IBZ) wedge / prism shading.
   - Reciprocal basis vectors ($\mathbf{b}_1, \mathbf{b}_2, \mathbf{b}_3$) with 3D directional arrowheads.
   - Collision-free LaTeX STIX typography for high-symmetry labels.

---

## ⚡ CLI Usage

The primary visualizer `bz-visualizer` (or `bz_visualizer.py`) is directly executable:

```bash
# 1. Standard 3D Brillouin Zone from VASP POSCAR
bz-visualizer POSCAR -o brillouin_zone.png

# 2. 2D Monolayer with translucent prism shading and k-path
bz-visualizer POSCAR --is-2d --shade-wedge -o monolayer_bz.png --elev 22 --azim 38

# 3. Custom camera orientation and resolution
bz-visualizer POSCAR -o figure_prb.png --elev 30 --azim 45 --dpi 600

# 4. Generate VASP KPOINTS band structure file alongside figure
bz-visualizer POSCAR --export-kpoints KPOINTS_band --kpoints-density 40
```

---

## 🐍 Python API Reference

```python
from skills.reciprocal_space_visualizer.scripts.bz_visualizer import (
    parse_poscar_lattice,
    compute_reciprocal_lattice,
    get_brillouin_zone_facets,
    render_brillouin_zone
)

# 1. Load real lattice
lattice = parse_poscar_lattice("POSCAR")

# 2. Get reciprocal vectors
b_matrix = compute_reciprocal_lattice(lattice)

# 3. Extract facets
facets = get_brillouin_zone_facets(b_matrix)

# 4. Render publication figure
fig, ax = render_brillouin_zone(
    lattice=lattice,
    facets=facets,
    is_2d=True,
    output_path="figures/brillouin_zone.png"
)
```
