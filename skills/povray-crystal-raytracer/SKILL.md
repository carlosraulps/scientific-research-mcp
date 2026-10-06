---
name: povray-crystal-raytracer
description: Use when generating publication-quality, photorealistic 3D ray-traced figures of crystal structures (POSCAR, CIF, XYZ) with studio lighting, realistic depth shadows, metallic/dielectric materials, and ball-and-stick representations using POV-Ray 3.7.
---

# 💎 POV-Ray Crystal Raytracer Skill

## Overview
Automates **POV-Ray 3.7** for high-resolution, photorealistic 3D ray tracing of periodic crystal lattices, slabs, molecules, and defect geometries. Implements physically grounded materials (metallic finishes for transition metals, dielectric finishes with specular highlights for non-metals), 3-point studio lighting, ground shadow receiver planes, and unit cell bounding wireframes.

---

## 🚀 Key Capabilities

1. **Photorealistic Ray Tracing Engine**:
   - Uses POV-Ray 3.7 headless rendering with adaptive anti-aliasing (`+A0.1 +J +Q9`).
   - Generates soft shadows, ambient occlusion, and Fresnel edge reflections.
   - Independent of X11 displays (renders directly on headless HPC compute nodes).

2. **Automated Scene Synthesis**:
   - Converts standard VASP `POSCAR` / `.vasp`, `CIF`, or `XYZ` files directly into `.pov` scene descriptions.
   - Auto-computes bounding boxes, geometric centers, optimal camera focal distances, and field-of-view angles.
   - Dynamic bond detection based on covalent radii and coordination thresholds.
   - Bicolor split cylinders for heterogeneous chemical bonds.

3. **Material & Lighting Protocol**:
   - **Key Light**: High-intensity warm-white studio light ($45^\circ$ azimuth, $60^\circ$ elevation).
   - **Fill Light**: Cool ambient fill light to eliminate harsh shadows.
   - **Rim Light**: Backlight providing edge separation from the background.
   - **Shadow Receiver Plane**: Renders a subtle ground plane capturing realistic contact shadows.
   - **Elemental Finishes**: Specular highlights for organic atoms (C, H, O, N, Cl) vs metallic luster for transition metals (Fe, Co, Ni, Pt, Au, Cr).

---

## ⚡ CLI Usage

```bash
# 1. Basic ray-traced render from POSCAR (default 2400x1800)
povray-crystal-render POSCAR -o crystal_3d.png

# 2. Ultra-HD print-quality render (4K resolution)
povray-crystal-render POSCAR -o crystal_4k.png --width 3840 --height 2160 --ball-scale 0.50

# 3. Export standalone .pov scene for custom editing
povray-crystal-render POSCAR --pov-out scene.pov -o render.png

# 4. Render without unit cell wireframe or ground plane
povray-crystal-render POSCAR -o molecule_floating.png --no-cell --no-ground
```

---

## 🐍 Python API Reference

```python
from skills.povray_crystal_raytracer.scripts.povray_crystal_render import (
    parse_poscar,
    compute_bonds,
    generate_pov_scene,
    render_povray
)

# 1. Parse lattice and coordinates
lattice, elements, cart_coords = parse_poscar("POSCAR")

# 2. Compute bonds
bonds = compute_bonds(elements, cart_coords, lattice)

# 3. Generate POV-Ray scene description
scene_code = generate_pov_scene(
    lattice=lattice,
    elements=elements,
    cart_coords=cart_coords,
    bonds=bonds,
    ball_scale=0.45,
    bond_radius=0.10
)

# 4. Save and raytrace
with open("scene.pov", "w") as f:
    f.write(scene_code)

render_povray("scene.pov", "output.png", width=2400, height=1800)
```
