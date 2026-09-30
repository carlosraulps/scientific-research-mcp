---
name: xcrysden-visualizer
description: Use when visualizing Fermi surfaces (BXSF), 2D charge density topological contours, Brillouin zones, or automating XCrySDen headlessly via TCL scripting with background whitening.
---

# XCrySDen Visualizer Skill

## Overview
Automates **XCrySDen** across X11 and headless environments. Features a programmatic **TCL Scripting Engine** for 2D charge density topological contour slicing, 3D isosurfaces, and Fermi surface extraction, paired with an automated **Publication Background Whitening Pipeline** that converts default black OpenGL viewports into crisp, publication-ready white graphics.

## Key Capabilities & Scientific Mechanisms

### 1. Headless TCL Scripting Automation
XCrySDen can be driven headlessly with zero interactive mouse clicks via:
```bash
xcrysden <flag> <file> --script render_script.tcl
```
The skill automatically translates input parameters into clean TCL routines handling rotation, zoom, 2D slice planes, and viewport frame dumping.

### 2. 2D Charge Density Difference (CDD) Planar Contours
- Computes and slices 2D cross-sections across planes ($xy$, $xz$, $yz$) at arbitrary fractional positions (e.g. basal plane $z = 0.50$ for 2D materials like PHOTH-graphene).
- Configurable contour line counts (default: 35) with diverging colormaps (Blue-White-Red, Rainbow) for clear topological charge transfer visualization.

### 3. Publication Background Whitening Pipeline (`postprocess_image.py`)
- **Problem**: XCrySDen defaults to an unprintable solid black background (`#000000`).
- **Solution**: Automated post-processing remaps dark background pixels to pure `#FFFFFF` with fringe antialiasing to prevent jagged dark halos around atomic bonds, labels, and contour lines, followed by automated border whitespace trimming.

### 4. Headless HPC Cluster Support (`xvfb-run`)
- If running on headless compute nodes without an active X server (`DISPLAY`), execution is wrapped automatically in `xvfb-run -a -s "-screen 0 2400x1800x24"`.

### 5. Reproducible TCL Script Export
- Allows generating and exporting standalone `.tcl` scripts (`--export-script <path.tcl>`) for manual inspection or batch execution on remote HPC supercomputers.

---

## Quick Reference

| **Snapshot structure with white background** | `xcrysden-snapshot POSCAR -o ./figures/struc.png` |
| **Auto-Detect 2D Sheet & Contour Slice** | `xcrysden-slice density.xsf --target sheet -p xy -o ./figures/slice_sheet.png` |
| **Auto-Detect Adsorbate & Contour Slice** | `xcrysden-slice density.xsf --target adsorbate -p xy -o ./figures/slice_ads.png` |
| **2D Density Contour ($xy$ basal plane)** | `xcrysden-snapshot density.cube --slice-2d --plane xy --plane-pos 0.50 -o ./figures/slice_xy.png` |
| **3D Isosurface snapshot** | `xcrysden-snapshot density.cube --isovalue 0.05 -o ./figures/iso.png` |
| **Export headless TCL script** | `xcrysden-snapshot POSCAR --export-script render.tcl` |
| **Visualize Fermi Surface (BXSF)** | `xcrysden-snapshot fermi.bxsf --keep-open` |
| **Post-process existing black image** | `python <script_dir>/postprocess_image.py raw.png -o white.png` |

---

## Script Options & Arguments

The underlying scripts are located at:
- `skills/xcrysden-visualizer/scripts/xcrysden_auto.py` (wrapped globally in `~/.local/bin/xcrysden-snapshot`)
- `skills/xcrysden-visualizer/scripts/postprocess_image.py` (background whitening and antialiasing pipeline)

- `input`: Path to input file (`POSCAR`, `structure.cif`, `file.xsf`, `bands.bxsf`, `density.cube`, `pw.in`, `pw.out`).
- `--output`, `-o`: Output image path (defaults to `<stem>_xcrysden.png`).
- `--view`, `-v`: `a`, `b`, `c`, or `iso` (default: `c`).
- `--mode`, `-m`: `BallStick`, `SpaceFill`, or `Wireframe` (default: `BallStick`).
- `--slice-2d`: Enables 2D planar contour slicing of volumetric data.
- `--plane`: `xy`, `xz`, or `yz` (default: `xy`).
- `--plane-pos`: Fractional coordinate along normal axis for 2D slice (default: `0.50`).
- `--contours`: Number of contour lines (default: `35`).
- `--isovalue`: 3D isosurface cutoff level.
- `--no-white-bg`: Retains default black background instead of inverting to pure white.
- `--width`: Output width in pixels (default: `2400`).
- `--height`: Output height in pixels (default: `1800`).
- `--export-script`: Saves the generated TCL script to specified file path.
- `--timeout`: Maximum seconds to wait for rendering (default: `15.0s`).
- `--keep-open`: Keeps the interactive GUI open for manual exploration.

---

## Common Pitfalls & Solutions

1. **`DISPLAY not set`**: When running on remote clusters, ensure `xvfb` is installed or run with `--export-script` to prepare scripts locally.
2. **Scratch space conflict**: If multiple concurrent instances clash on `/tmp/xc_*`, the script uses unique process IDs (`os.getpid()`) to guarantee isolation.
3. **Format conversion**: Non-native files (POSCAR, CIF, XYZ) are converted automatically to XSF via ASE before dispatch.
