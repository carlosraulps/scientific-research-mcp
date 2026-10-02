---
name: xcrysden-visualizer
description: Use when visualizing Fermi surfaces (BXSF), 2D charge density topological contours, Brillouin zones, or automating XCrySDen headlessly via TCL scripting with background whitening.
---

# XCrySDen Visualizer Skill

## Overview
Automates **XCrySDen** across X11 and headless environments. Features a programmatic **TCL Scripting Engine** for 2D charge density topological contour slicing, 3D isosurfaces, and Fermi surface extraction, paired with an automated **Publication Background Whitening Pipeline** that converts default black OpenGL viewports into crisp, publication-ready white graphics with fringe antialiasing and uniform 30 px padding.

## ⚠️ 3D Volumetric CDD Deprecation Notice

> [!WARNING]
> **XCrySDen is NOT recommended for 3D volumetric Charge Density Difference (CDD) isosurface rendering.** Empirical testing on PHOTH-graphene and adsorbate systems reveals three critical failure modes:
> 1. **Dark Haloing Artifacts**: XCrySDen's legacy OpenGL pipeline produces persistent dark halo fringes around 3D isosurfaces that cannot be eliminated by background whitening post-processing.
> 2. **Poor Anti-Aliasing**: The fixed-pipeline rasterizer produces jagged isosurface edges with no MSAA support, unacceptable for publication-quality 3D renders.
> 3. **Xvfb Segfaults**: Headless 3D isosurface rendering via `xvfb-run` triggers intermittent segfaults in the GLX context on certain Mesa drivers.
>
> **Use instead:**
> - **3D CDD Isosurfaces**: `vesta-cdd` (VESTA automation skill) or OVITO with Tachyon ray tracer
> - **2D CDD Planar Contours**: XCrySDen remains the **best tool** for 2D topological contour slicing via `xcrysden-cdd`

---

## Key Capabilities & Scientific Protocols

### 1. Headless TCL Scripting Architecture
XCrySDen can be driven headlessly with zero interactive mouse clicks via:
```bash
xcrysden <flag> <file> --script render_script.tcl
```
The skill automatically translates input parameters into clean TCL routines handling rotation, zoom, 2D slice planes, and viewport frame dumping.

### 2. 2D Charge Density Difference (CDD) Planar Contours (`xcrysden-cdd`)
- Slices 2D cross-sections across planes ($xy$, $xz$, $yz$) at arbitrary fractional positions (e.g. basal plane $z = 0.50$ for 2D materials like PHOTH-graphene).
- Standardized headless script protocol:
  ```tcl
  scripting::open --xsf structure.xsf
  scripting::display_mode BallStick
  scripting::zoom 1.2
  scripting::view c
  scripting::slice2d --plane xy --coord 0.50 --isoline 35 --colormap bwr
  scripting::dump_frame frame_cdd.png
  scripting::exit
  ```
- Divides electron accumulation and depletion with 35 contour isolines using diverging colormaps (Blue-White-Red `bwr`).

### 3. Publication Background Whitening Pipeline (`postprocess_image.py`)
- **Problem**: XCrySDen defaults to an unprintable solid black background (`#000000`).
- **Solution**: Automated post-processing remaps dark background pixels to pure `#FFFFFF`:
  - **Fringe Antialiasing**: Smoothly blends transitional edge pixels into the white background, preventing dark jagged halos around atomic bonds, labels, and contour isolines.
  - **Clean Margin Trimming**: Automatically trims redundant border whitespace down to a clean **30 px padding**.

### 4. Headless HPC Cluster Support (`xvfb-run`)
- If running on headless compute nodes without an active X server (`DISPLAY`), execution is wrapped automatically in `xvfb-run -a -s "-screen 0 2400x1800x24"`.

---

## Quick Reference CLI

| Action | CLI Command |
| :--- | :--- |
| **Snapshot structure with white background** | `xcrysden-snapshot POSCAR -o ./figures/struc.png` |
| **One-command 2D CDD Basal Slice ($xy$)** | `xcrysden-cdd cdd.vasp --coord 0.50 --isolines 35 -o ./figures/cdd_xy.png` |
| **Auto-Detect 2D Sheet & Contour Slice** | `xcrysden-slice density.xsf --target sheet -p xy -o ./figures/slice_sheet.png` |
| **Auto-Detect Adsorbate & Contour Slice** | `xcrysden-slice density.xsf --target adsorbate -p xy -o ./figures/slice_ads.png` |
| **3D Isosurface snapshot** | `xcrysden-snapshot density.cube --isovalue 0.05 -o ./figures/iso.png` |
| **Export headless TCL script** | `xcrysden-cdd cdd.vasp --export-script render_2d_cdd.tcl` |
| **Visualize Fermi Surface (BXSF)** | `xcrysden-snapshot fermi.bxsf --keep-open` |
| **Post-process existing black image** | `python <script_dir>/postprocess_image.py raw.png --padding 30 -o white.png` |

---

## Script Architecture & CLI Binaries

Installed globally in `~/.local/bin/`:
- `xcrysden-snapshot` -> `skills/xcrysden-visualizer/scripts/xcrysden_auto.py`
- `xcrysden-cdd` -> `skills/xcrysden-visualizer/scripts/xcrysden_cdd.py`
- `xcrysden-slice` -> `skills/xcrysden-visualizer/scripts/auto_slice_2d.py`
- `postprocess_image.py` -> Background whitening & 30px padding pipeline

### Common Options:
- `input`: Path to input file (`POSCAR`, `structure.cif`, `file.xsf`, `bands.bxsf`, `density.cube`, `cdd.vasp`).
- `--output`, `-o`: Output image path.
- `--plane`: `xy`, `xz`, or `yz` (default: `xy`).
- `--coord`: Fractional coordinate along normal axis for 2D slice (default: `0.50`).
- `--isolines`: Number of contour lines (default: `35`).
- `--colormap`: Colormap name (default: `bwr`).
- `--padding`: Uniform border whitespace padding in pixels (default: `30`).
- `--export-script`: Saves the generated TCL script to specified file path.
- `--timeout`: Maximum seconds to wait for rendering (default: `18.0s`).
