---
name: ovito-snapshot
description: Use when needing headless, high-throughput, scriptable 2D/3D snapshots or animations of atomic structures (POSCAR, CONTCAR, CIF, XYZ, LAMMPS) along crystallographic axes (a, b, c, isometric) with publication colorbars.
---

# OVITO Snapshot Skill

## Overview
Headless, high-throughput crystal structure and trajectory rendering using the OVITO Python API. Renders publication-grade orthographic or perspective images along crystallographic axes ($a$, $b$, $c$, isometric) in seconds with calibrated 2D material presets, padded coordinate tripods (preventing label clipping), decoupled Matplotlib-rendered STIX/Times New Roman publication colorbars, and locked-FOV strain trajectory sequences.

## Key Capabilities & Scientific Protocols

### 1. Padded Coordinate Tripod Overlay
- **Problem**: Default OVITO viewport tripods position origin coordinates at $(0, 0)$, clipping axis arrow labels (specifically $-x$ and $-z$) against image borders.
- **Solution**: Enforces safe padded margin offsets (`offset_x >= 0.06`, `offset_y >= 0.06`, default: `(0.06, 0.06)`, `size = 0.075`), guaranteeing clean, unclipped axis indicators across all projection ratios.

### 2. Calibrated 2D Material & Carbon Presets (`--preset 2d-carbon`)
- Calibrated standard for graphene, PHOTH-graphene, BCN, and 2D heterostructures:
  - **Carbon sphere radius**: `0.38 Å`
  - **Adsorbate H radius**: `0.24 Å` (distinctly sized for on-top adsorbates and HER reaction intermediates)
  - **Bond cylinder radius**: `0.14 Å`
  - **C-C bond cutoff**: `1.70 Å` (captures conjugated single/double bonds up to $1.52\text{ \AA}$ while strictly eliminating spurious diagonal bonds across 5-, 6-, and 8-membered rings).
- Other available presets:
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

### 4. Locked Camera FOV & Strain Series Protocol (`ovito-strain-series`)
- When visualizing mechanical strain series ($-3\% \to +3\%$):
  - Automatically locks camera FOV to the maximum cell dimension, preventing frame-dilation or zoom jumps between frames.
  - Pre-computes a unified global net charge range $[c_{\min}, c_{\max}]$ across all strain steps so color shifts reflect true electronic redistribution.
  - Emits uniformly dimensioned frames ready for the zero-dilation animation protocol.

### 5. Physical Net Bader Charge Mapping (`--net-charge`)
- Automatically deduces element types via ASE and converts Henkelman raw valence electron counts into physical net atomic charges:
  $$\Delta Q = Z_{\mathrm{valence}} - Q_{\mathrm{bader}}$$
  centered cleanly around zero.

### 6. CPU Raytracing & Path-Tracing Renderers (`--renderer`)
- `--renderer standard`: Fast OpenGL/offscreen rasterizer for batch runs.
- `--renderer tachyon`: Headless software raytracer with ambient occlusion (`ambient_occlusion=True`), soft contact shadows beneath atoms and bond cylinders, and multisample antialiasing. Runs headlessly on any CPU without X11 or GPU!
- `--renderer ospray`: Intel OSPRay photorealistic path-tracer with direct lighting, ambient sky illumination, principled specular highlights, and real-time CPU denoising.

### 7. Nature-Grade Physical Scale Bar (`--scale-bar`)
- Automatically calculates the exact physical magnification from the orthographic camera's field of view (`vp.fov` in Ångströms):
  $$\text{Scale (px/Å)} = \frac{\text{Height}}{\text{FOV}}$$
- Injects a high-contrast physical scale bar (e.g., 5 Å, 10 Å, 1 nm) in Times New Roman / STIX typography directly onto crystallographic projections ($a, b, c$).

---

## Quick Reference CLI

| Action | CLI Command |
| :--- | :--- |
| **All views ($a, b, c, \text{iso}$)** | `ovito-snapshot POSCAR -o ./figures` |
| **2D Carbon preset (PHOTH-graphene)** | `ovito-snapshot POSCAR -v c --preset 2d-carbon -o ./figures` |
| **View along $c$-axis (xy plane)** | `ovito-snapshot POSCAR -v c -o ./figures` |
| **View along $a$-axis (yz plane)** | `ovito-snapshot POSCAR -v a -o ./figures` |
| **Supercell expansion ($2\times 2\times 2$)** | `ovito-snapshot POSCAR --supercell 2 2 2` |
| **High resolution (4K UHD)** | `ovito-snapshot POSCAR --width 3840 --height 2160` |
| **CPU Raytracing (Tachyon + Shadows)** | `ovito-snapshot POSCAR --renderer tachyon --autotrim -o ./figures` |
| **Physical Scale Bar (5 Å on 2D sheet)** | `ovito-snapshot POSCAR -v c --scale-bar 5.0 --autotrim -o ./figures` |
| **Bader Net Charge with STIX Colorbar** | `ovito-snapshot POSCAR --bader-file ACF.dat --net-charge --publish-colorbar -v c` |
| **Composite Snapshot + Publication Colorbar** | `ovito-snapshot POSCAR --bader-file ACF.dat --net-charge --composite-colorbar -v c` |
| **Strain Series with Locked FOV** | `ovito-strain-series "./strain/POSCAR_*" --bader-pattern "./strain/ACF_*" -o ./frames` |

---

## Script Architecture & CLI Binaries

Installed globally in `~/.local/bin/`:
- `ovito-snapshot` -> `skills/ovito-snapshot/scripts/render_ovito.py`
- `ovito-strain-series` -> `skills/ovito-snapshot/scripts/strain_trajectory_snapshot.py`
- `publication_colorbar.py` -> Standalone STIX colorbar generator & compositor
