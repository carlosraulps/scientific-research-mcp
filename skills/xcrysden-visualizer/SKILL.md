---
name: xcrysden-visualizer
description: Use when visualizing Fermi surfaces (BXSF), Brillouin zones and k-paths (pw.x, WIEN2k), 2D/3D charge density isosurfaces (XSF, Cube), or scripting XCrySDen structure plots.
---

# XCrySDen Visualizer Skill

## Overview
Automates XCrySDen on X11 for electronic structure rendering, Fermi surfaces (`.bxsf`), charge density isosurfaces (`.xsf`, `.cube`), Brillouin zones, and Quantum ESPRESSO outputs (`.pwi`, `.pwo`). Features automated file conversion via ASE and window snapshot dumping via ImageMagick.

## When to Use
- **Trigger**: Inspecting or generating snapshots of Fermi surfaces from DFT bands (`.bxsf`).
- **Trigger**: Visualizing 2D/3D electron charge density or potential contours (`.cube`, `.xsf`).
- **Trigger**: Displaying Brillouin zone shapes and high-symmetry $k$-paths for band structure calculations.
- **Trigger**: Directly loading Quantum ESPRESSO input/output files (`pw.x`).
- **When NOT to use**:
  - High-throughput headless batch rendering of geometries (use [ovito-snapshot](../ovito-snapshot/SKILL.md)).
  - Advanced manual polyhedra styling and orientation (use [vesta-automation](../vesta-automation/SKILL.md)).
  - Photorealistic journal cover ray-tracing (use [blender-crystal-render](../blender-crystal-render/SKILL.md)).

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **Snapshot structure (POSCAR/CIF)** | `xcrysden-snapshot POSCAR -o ./figures/struc.png` |
| **Visualize Fermi Surface (BXSF)** | `xcrysden-snapshot fermi.bxsf --keep-open` |
| **Visualize Charge Density (Cube)** | `xcrysden-snapshot density.cube -o ./figures/rho.png` |
| **Inspect Quantum ESPRESSO run** | `xcrysden-snapshot pw.out --keep-open` |
| **Custom window timeout** | `xcrysden-snapshot POSCAR --timeout 8.0` |
| **Direct script execution** | `uv run --with python-xlib --with pyautogui --with ase python <script_path>/xcrysden_auto.py POSCAR` |

## Script Options & Arguments

The underlying script is located at:
`skills/xcrysden-visualizer/scripts/xcrysden_auto.py` (and wrapped in `~/.local/bin/xcrysden-snapshot`).

- `input`: Path to input file (`POSCAR`, `structure.cif`, `file.xsf`, `bands.bxsf`, `density.cube`, `pw.in`, `pw.out`).
- `--output`, `-o`: Output image path (defaults to `<stem>_xcrysden.png`).
- `--timeout`: Maximum seconds to wait for XCrySDen window initialization (default: 5.0s).
- `--keep-open`: Leave the XCrySDen window open for interactive Fermi surface or isosurface manipulation.

## Common Pitfalls & Solutions

1. **`DISPLAY` not set**: XCrySDen requires an X11 environment. Ensure `DISPLAY=:0` is exported.
2. **Scratch space error**: If XCrySDen warns of scratch space conflicts, clean `/tmp/xc_*` directories.
3. **Format conversion**: POSCAR and CIF files are automatically converted to temporary XSF format using ASE before launch.
