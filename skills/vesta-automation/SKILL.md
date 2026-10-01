---
name: vesta-automation
description: Use when generating authentic VESTA-rendered crystal projections, 3D charge density difference (CDD) isosurfaces, or automating VESTA via native terminal CLI or X11 GUI.
---

# VESTA Automation & Headless High-Resolution Skill

## Overview
Automates **VESTA** (Visualization for Electronic and STructural Analysis) across macOS and Linux/X11. Prioritizes VESTA's native headless terminal export interface (`-export_img scale=<N>`) for rapid, borderless, publication-quality graphics up to 600 DPI, while solving the infamous periodic boundary spillover bug (`Bound = 0`). Also features full X11 desktop GUI automation fallback for interactive inspection.

## Key Technical Solutions & Protocols

### 1. The Periodic Boundary Spillover Bug & Clean Boundary Rules (`Bound = 0`)
- **Problem**: When loading a `POSCAR` or volumetric `CHGCAR` into VESTA via default settings, VESTA's bond search engine defaults to `Bound = 2` (recursive periodic boundary search). Any bond crossing the periodic cell boundary iteratively draws atoms in neighboring cells, populating hundreds of duplicate ghost atoms that clutter the viewport and distort visual presentation.
- **Root Solution**:
  1. In CLI/Headless execution: Generate a clean `.vstd` style or `.vesta` project wrapper enforcing:
     ```ini
     # In .vstd / .vesta style configuration
     BOUND_MODE 0
     SEARCH_BOUNDARY 0
     ```
  2. The `generate-vstd` tool automatically inspects the input POSCAR, determines all chemical species present, computes physically realistic bond cutoff thresholds (e.g. C-C $1.70\text{ \AA}$ avoiding ring diagonals, C-H $1.25\text{ \AA}$), and auto-injects `Bound = 0` and `SEARCH_BOUNDARY = 0`.
  3. Load the style dynamically along with the crystal data:
     ```bash
     VESTA -open crystal.vasp -style cleanup_rules.vstd -export_img scale=2 output_image.png
     ```

### 2. Native Terminal CLI Flags & Offscreen Export
- **Command Syntax**:
  ```bash
  VESTA -open <input_file> [-style <rules.vstd>] -export_img scale=<N> <output_image.png>
  ```
- **Scale Multipliers**:
  - `scale=1`: Standard screen resolution ($1920 \times 1080$).
  - `scale=2`: 4K Ultra-HD presentation quality ($3840 \times 2160$).
  - `scale=3`: 600 DPI print quality for journal submissions.
- **Headless X11 Server Fallback**:
  On remote HPC compute nodes without an active `$DISPLAY`, the scripts automatically wrap execution in:
  ```bash
  xvfb-run -a -s "-screen 0 3840x2160x24" VESTA -open crystal.vasp -export_img scale=2 output.png
  ```

### 3. Dual Isosurface CDD Automation (`vesta-cdd`)
- Automatically generates dual positive/negative accumulation and depletion isosurfaces:
  - **Accumulation ($\Delta\rho > 0$)**: Gold / Yellow (`#f1c40f`, `[241, 196, 15]`)
  - **Depletion ($\Delta\rho < 0$)**: Cyan / Sky Blue (`#00b4d8`, `[0, 180, 216]`)
  - **Opacity**: Calibrated to 60% (`alpha=0.60`) to keep internal atomic coordinates and bonding networks visible.
- Execution is completely headless with automatic border whitespace trimming down to a clean 30 px padding.

---

## Quick Reference CLI

| Action | CLI Command |
| :--- | :--- |
| **All views ($a, b, c, \text{iso}$) at 4K** | `vesta-snapshot POSCAR -o ./figures` |
| **View along $c$-axis (xy plane)** | `vesta-snapshot POSCAR -v c -o ./figures` |
| **View along $a$-axis (yz plane)** | `vesta-snapshot POSCAR -v a -o ./figures` |
| **Publication 600 DPI print scale** | `vesta-snapshot POSCAR -s 3 -o ./figures` |
| **One-command 3D CDD Rendering** | `vesta-cdd cdd.vasp -v c --pos-level 0.005 --neg-level -0.005` |
| **Generate clean Bound=0 .vstd style** | `generate-vstd POSCAR -o clean_rules.vstd --format vstd` |
| **Generate complete .vesta wrapper** | `generate-vstd POSCAR -o project.vesta -v c --bound 0` |
| **Batch Render Directory + Gallery** | `vesta-batch ./relax_steps/ -v c -o ./gallery --pattern "POSCAR*"` |
| **Interactive GUI mode on X11** | `vesta-snapshot POSCAR --gui --keep-open` |

---

## Script Architecture & CLI Binaries

Installed globally in `~/.local/bin/`:
- `vesta-snapshot` -> `skills/vesta-automation/scripts/vesta_auto.py`
- `generate-vstd` -> `skills/vesta-automation/scripts/generate_vstd.py`
- `vesta-cdd` -> `skills/vesta-automation/scripts/vesta_cdd.py`
- `vesta-batch` -> `skills/vesta-automation/scripts/batch_vesta_render.py`

### Common Options:
- `input`: Path to input crystal structure (`POSCAR`, `CONTCAR`, `structure.cif`, `file.xsf`) or volumetric dataset (`CHGCAR`, `cdd.vasp`, `LOCPOT`, `.cube`).
- `--view`, `-v`: `a`, `b`, `c`, `iso`, or `all` (default: `all`).
- `--scale`, `-s`: Integer resolution scale multiplier (default: `2`).
- `--bound`: `0` (isolate cell, default), `1` (search beyond), `2` (recursive periodic search).
- `--pos-level`: Positive CDD isosurface cutoff (default: `0.005`).
- `--neg-level`: Negative CDD isosurface cutoff (default: `-0.005`).
- `--opacity`: Surface opacity between 0.0 and 1.0 (default: `0.60`).
- `--timeout`: Maximum seconds to wait for render completion (default: `15.0s`).

---

## Common Pitfalls & Solutions

1. **`The file (/usr/local/bin/elements.ini) was not opened`**: Occurs when VESTA is invoked via an unresolved symlink. The scripts resolve symlinks (`os.path.realpath`) to locate bundled application resources.
2. **Periodic duplicate explosion**: Occurs when `Bound = 2` is used with bonding search across cell faces. Enforce `Bound = 0` and `SEARCH_BOUNDARY = 0` with `generate-vstd`.
3. **Headless Linux environments without X11**: Automatically wraps calls in `xvfb-run -a -s "-screen 0 3840x2160x24"`.
