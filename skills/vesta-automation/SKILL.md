---
name: vesta-automation
description: Use when generating authentic VESTA-rendered crystal projections, 3D charge density difference (CDD) isosurfaces, or automating VESTA via native terminal CLI or X11 GUI.
---

# VESTA Automation & Headless High-Resolution Skill

## Overview
Automates **VESTA** (Visualization for Electronic and STructural Analysis) across macOS and Linux/X11. Prioritizes VESTA's native headless terminal export interface (`-export_img scale=<N>`) for rapid, borderless, publication-quality graphics up to 600 DPI, while solving the infamous periodic boundary spillover bug (`Bound = 0`). Also features full X11 desktop GUI automation fallback for interactive inspection.

## Key Technical Solutions & Protocols

### 1. The 800-Atom Periodic Boundary Spillover Solution (`Bound = 0`)
- **Problem**: When loading volumetric data or slab models, VESTA's bond engine defaults to `Bound = 2` (recursive periodic search). Any bond reaching across boundary faces iteratively populates neighboring cells, causing hundreds of duplicate ghost atoms to clutter the canvas.
- **Solution**: The script automatically injects `Bound = 0` ("Do not search atoms beyond boundary") into a dynamic `.vesta` project wrapper. This guarantees strict primitive unit cell containment with zero boundary artifacts.

### 2. Native Offscreen Terminal CLI Export (`-export_img`)
- Direct invocation without GUI clicks:
  ```bash
  VESTA -open <input_file> -export_img scale=2 <output_image.png>
  ```
- **Resolution Scaling**: The `scale` parameter acts as a resolution multiplier (e.g. `scale=2` outputs $3840 \times 2160$ 4K UHD; `scale=3` delivers 600 DPI journal print standards).
- **Process Lifecycle Management**: Automatically monitors output image generation and cleanly terminates the resident VESTA process.

### 3. Dual-Isosurface Charge Density Difference (CDD) Rendering
- Supports dual positive/negative accumulation and depletion isosurfaces (`--cdd`, `--pos-level`, `--neg-level`).
- Colors default to standard scientific conventions: Gold/Yellow for charge accumulation ($\Delta\rho > 0$) and Sky Blue/Cyan for charge depletion ($\Delta\rho < 0$) with calibrated opacity.

### 4. Headless Server & Virtual Framebuffer Fallback
- Automatically detects headless Linux cluster environments and wraps execution in `xvfb-run -a -s "-screen 0 1920x1080x24"` when `DISPLAY` is not configured.

---

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **All views ($a, b, c, \text{iso}$) at 4K** | `vesta-snapshot POSCAR -o ./figures` |
| **View along $c$-axis (xy plane)** | `vesta-snapshot POSCAR -v c -o ./figures` |
| **View along $a$-axis (yz plane)** | `vesta-snapshot POSCAR -v a -o ./figures` |
| **Publication 600 DPI print scale** | `vesta-snapshot POSCAR -s 3 -o ./figures` |
| **Charge Density Difference (CDD)** | `vesta-snapshot cdd.vasp --cdd --pos-level 0.005 --neg-level -0.005` |
| **Interactive GUI mode on X11** | `vesta-snapshot POSCAR --gui --keep-open` |
| **Generate standalone .vesta wrapper** | `python <script_dir>/vstd_generator.py POSCAR -o project.vesta -v c --bound 0` |

---

## Script Options & Arguments

The underlying scripts are located at:
- `skills/vesta-automation/scripts/vesta_auto.py` (wrapped globally in `~/.local/bin/vesta-snapshot`)
- `skills/vesta-automation/scripts/vstd_generator.py` (standalone `.vesta` project and style generator)

- `input`: Path to input crystal structure (`POSCAR`, `CONTCAR`, `structure.cif`, `file.xsf`) or volumetric dataset (`CHGCAR`, `cdd.vasp`, `LOCPOT`, `.cube`).
- `--view`, `-v`: `a`, `b`, `c`, `iso`, or `all` (default: `all`).
- `--output-dir`, `-o`: Directory to store output PNG images.
- `--prefix`, `-p`: File prefix (defaults to input file stem).
- `--scale`, `-s`: Integer resolution scale multiplier (default: `2`).
- `--no-isolate`: Disables automatic `Bound = 0` unit cell isolation (allows periodic bond extension).
- `--cdd`: Enables dual-surface accumulation/depletion isosurfaces for Charge Density Difference datasets.
- `--pos-level`: Positive CDD isosurface cutoff (default: `0.005`).
- `--neg-level`: Negative CDD isosurface cutoff (default: `-0.005`).
- `--gui`: Forces X11 interactive desktop GUI automation mode via `pyautogui`.
- `--keep-open`: Leaves the VESTA GUI open after taking snapshots for manual inspection.
- `--timeout`: Maximum seconds to wait for render completion (default: `12.0s`).

---

## Common Pitfalls & Solutions

1. **`The file (/usr/local/bin/elements.ini) was not opened`**: Occurs when VESTA is invoked via an unresolved symlink. `vesta_auto.py` automatically resolves symlinks (`os.path.realpath`) to locate bundled application resources.
2. **Periodic duplicate explosion**: Occurs when `Bound = 2` is used with bonding search across cell faces. Keep default `--isolate-cell` enabled to enforce `Bound = 0`.
3. **Headless Linux environments without X11**: Ensure `xvfb` is installed (`sudo apt-get install xvfb`). The script will automatically dispatch via `xvfb-run -a`.
