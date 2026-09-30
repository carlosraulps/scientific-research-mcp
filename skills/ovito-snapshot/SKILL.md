---
name: ovito-snapshot
description: Use when needing headless, high-throughput, scriptable 2D/3D snapshots or animations of atomic structures (POSCAR, CONTCAR, CIF, XYZ, LAMMPS) along crystallographic axes (a, b, c, isometric) with publication colorbars.
---

# OVITO Snapshot Skill

## Overview
Headless, high-throughput crystal structure and trajectory rendering using the OVITO Python API. Renders publication-grade orthographic or perspective images along crystallographic axes ($a$, $b$, $c$, isometric) in seconds with calibrated 2D material presets, padded coordinate tripods (preventing label clipping), and decoupled Matplotlib-rendered STIX/Times New Roman publication colorbars.

## Key Capabilities & Scientific Mechanisms

### 1. Padded Coordinate Tripod Overlay
- **Problem**: Default OVITO viewport tripods position origin coordinates at $(0, 0)$, clipping axis arrow labels (specifically $-x$ and $-z$) against image borders.
- **Solution**: Enforces minimum safe margin offsets (`offset_x >= 0.05`, `offset_y >= 0.05`, default: `(0.06, 0.06)`, `size = 0.075`), guaranteeing clean, unclipped axis indicators across all projection ratios.

### 2. Calibrated 2D Material & Carbon Presets (`--preset`)
- `--preset 2d-carbon` (calibrated for graphene, PHOTH-graphene, BCN, graphyne):
  - Atomic sphere radius: `0.38 Å`
  - Bond cylinder radius: `0.14 Å`
  - Bond cutoff: `1.70 Å` (captures C-C single and conjugated bonds up to $1.52$ Å while strictly eliminating spurious diagonal bonds across 5-, 6-, and 8-membered rings).
- `--preset ball-stick`: Standard ball-and-stick (`r = 0.40 Å`, `w = 0.15 Å`, `cutoff = 2.80 Å`).
- `--preset spacefill`: Van der Waals spacefilling representation.
- `--preset wireframe`: Thin bond wireframe representation (`r = 0.10 Å`, `w = 0.08 Å`).

### 3. Decoupled Typography & Publication Colorbars (`publication_colorbar.py`)
- **Problem**: Internal OpenGL bitmap fonts produce blocky, unscalable text that cannot render LaTeX math equations.
- **Solution**: Generates publication-quality vector (`.pdf`) and raster (`.png`) colorbars using Matplotlib with:
  - STIX mathematical typography ($Q_{\mathrm{net}} = Z_{\mathrm{valence}} - Q_{\mathrm{bader}}\ (e)$)
  - Times New Roman serif font family
  - Clean decimal ticks (`-0.30`, `-0.15`, `0.00`, `+0.15`, `+0.30`)
  - Qualitative annotations: `"Electron Acceptor"` (blue) at top and `"Electron Donor"` (red) at bottom.
  - Option to composite colorbars directly onto crystal snapshots horizontally (`--composite-colorbar`).

### 4. Physical Net Bader Charge Mapping (`--net-charge`)
- Automatically deduces element types via ASE and converts Henkelman raw valence electron counts into physical net atomic charges:
  $$\Delta Q = Z_{\mathrm{valence}} - Q_{\mathrm{bader}}$$
  centered cleanly around zero.

### 5. CPU Raytracing & Path-Tracing Renderers (`--renderer`)
- `--renderer standard`: Fast OpenGL/offscreen rasterizer for batch runs.
- `--renderer tachyon`: Headless software raytracer with ambient occlusion (`ambient_occlusion=True`), soft contact shadows beneath atoms and bond cylinders, and multisample antialiasing. Runs headlessly on any CPU without X11 or GPU!
- `--renderer ospray`: Intel OSPRay photorealistic path-tracer with direct lighting, ambient sky illumination, principled specular highlights, and real-time CPU denoising.

### 6. Nature-Grade Physical Scale Bar (`--scale-bar`)
- Automatically calculates the exact physical magnification from the orthographic camera's field of view (`vp.fov` in Ångströms):
  $$\text{Scale (px/Å)} = \frac{\text{Height}}{\text{FOV}}$$
- Injects a high-contrast physical scale bar (e.g., 5 Å, 10 Å, 1 nm) in Times New Roman / STIX typography directly onto crystallographic projections ($a, b, c$).

### 7. Automated Whitespace Trimming (`--autotrim`)
- Crops excess uniform margins down to a calibrated padding border (30 px) for seamless journal layout insertion.

### 8. 3D Atomic Vector Overlays (`--vectors-file`)
- Renders forces, displacement vectors, or magnetic moments as 3D arrows emanating from atomic coordinates using `ovito.vis.VectorVis`.

---

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **All views ($a, b, c, \text{iso}$)** | `ovito-snapshot POSCAR -o ./figures` |
| **2D Carbon preset (PHOTH-graphene)** | `ovito-snapshot POSCAR -v c --preset 2d-carbon -o ./figures` |
| **View along $c$-axis (xy plane)** | `ovito-snapshot POSCAR -v c -o ./figures` |
| **View along $a$-axis (yz plane)** | `ovito-snapshot POSCAR -v a -o ./figures` |
| **Supercell expansion ($2\times 2\times 2$)** | `ovito-snapshot POSCAR --supercell 2 2 2` |
| **High resolution (4K UHD)** | `ovito-snapshot POSCAR --width 3840 --height 2160` |
| **CPU Raytracing (Tachyon + Shadows)** | `ovito-snapshot POSCAR --renderer tachyon --autotrim -o ./figures` |
| **Path-Tracing (Intel OSPRay)** | `ovito-snapshot POSCAR --renderer ospray -v iso -o ./figures` |
| **Physical Scale Bar (5 Å on 2D sheet)** | `ovito-snapshot POSCAR -v c --scale-bar 5.0 --autotrim -o ./figures` |
| **Atomic Vector Overlay (Forces/Moments)** | `ovito-snapshot POSCAR --vectors-file forces.dat --vector-scale 1.5 -v c` |
| **Bader Net Charge with STIX Colorbar** | `ovito-snapshot POSCAR --bader-file ACF.dat --net-charge --publish-colorbar -v c` |
| **Composite Snapshot + Publication Colorbar** | `ovito-snapshot POSCAR --bader-file ACF.dat --net-charge --composite-colorbar -v c` |
| **Generate Standalone STIX Colorbar** | `python <script_dir>/publication_colorbar.py --vmin -0.25 --vmax 0.25 -o colorbar.png` |

---

## Script Options & Arguments

The underlying scripts are located at:
- `skills/ovito-snapshot/scripts/render_ovito.py` (wrapped globally in `~/.local/bin/ovito-snapshot`)
- `skills/ovito-snapshot/scripts/publication_colorbar.py` (standalone STIX colorbar generator & compositor)

- `input`: Path to input crystal/trajectory file (`POSCAR`, `CONTCAR`, `structure.cif`, `dump.lammpstrj`).
- `--view`, `-v`: `a`, `b`, `c`, `iso`, or `all` (default: `all`).
- `--output-dir`, `-o`: Directory to store output PNG files.
- `--prefix`, `-p`: File prefix (defaults to input file stem).
- `--preset`: `2d-carbon`, `ball-stick`, `spacefill`, `wireframe`.
- `--supercell NX NY NZ`: Expand periodic boundaries by integers along $a, b, c$.
- `--bond-cutoff`: Cutoff distance in Ångströms for bond generation (default: 3.0 Å; 1.7 Å in 2d-carbon).
- `--particle-radius`: Multiplier for atomic sphere radii.
- `--bond-width`: Multiplier for cylinder bond width.
- `--polyhedra`: Enable coordination polyhedra generation.
- `--no-tripod`: Hide the coordinate axes tripod overlay.
- `--tripod-offset X Y`: Padded margin offset for tripod (default: `0.06 0.06`, min `0.05`).
- `--tripod-size`: Normalized size of tripod (default: `0.075`).
- `--projection`: `ortho` (orthographic, default for crystal axes) or `perspective`.
- `--background`: `white`, `black`, `gray`, or `transparent`.
- `--bader-file`: Path to Henkelman Bader `ACF.dat` or column file.
- `--net-charge`: Automatically calculates net charge $\Delta Q = Z_{\mathrm{val}} - Q_{\mathrm{bader}}$.
- `--charge-range MIN MAX`: Set explicit bounds for the diverging color scale (e.g. `--charge-range -0.25 0.25`).
- `--bader-colormap`: Diverging colormap gradient (`BlueWhiteRed`, `Viridis`, `Magma`).
- `--publish-colorbar`: Exports a standalone Matplotlib STIX publication colorbar (PDF and PNG).
- `--composite-colorbar`: Horizontally composites the publication colorbar directly onto the rendered crystal image.
- `--colorbar-label`: Custom LaTeX label (default: `$Q_{\mathrm{net}}\ (e)$`).
- `--no-cell`: Hide the unit cell wireframe box.

---

## Common Pitfalls & Solutions

1. **Axis label clipped at border**: Always keep `--tripod-offset` at or above `0.05 0.05` (the script enforces this by default).
2. **False diagonal bonds in 2D rings**: Use `--preset 2d-carbon` which limits bond cutoff to $1.70$ Å, connecting carbon rings cleanly without diagonal bridging.
3. **Typography clipping in OpenGL overlays**: Use `--composite-colorbar` or `--publish-colorbar` to replace low-resolution OpenGL bitmap text with vector STIX and Times New Roman fonts.
