---
name: vesta-automation
description: Use when needing to automate the VESTA GUI on X11 to view, align, or capture crystal structures (POSCAR, CIF, XSF) along crystallographic directions or inspect polyhedra interactively.
---

# VESTA Automation Skill

## Overview
Automates the desktop VESTA GUI on X11 using Python window introspection (`python-xlib`), key event injection (`pyautogui`), and direct window screenshot dumping (`ImageMagick import`). Allows hands-free generation of VESTA crystal projections along $a, b, c$ axes without manually clicking the interface.

## When to Use
- **Trigger**: Need authentic VESTA-rendered images (using VESTA's native polyhedra styles, coordination boundaries, and bond coloring).
- **Trigger**: Verifying crystal structures on an active X11 desktop environment (`DISPLAY=:0`).
- **Trigger**: Automating multi-axis ($a, b, c$) screen captures from `.vasp`, `POSCAR`, `CONTCAR`, `.cif`, or `.xsf` files.
- **When NOT to use**:
  - Pure headless computing clusters without X11 or virtual framebuffer (use [ovito-snapshot](../ovito-snapshot/SKILL.md)).
  - High-end photorealistic ray-traced figures with studio illumination (use [blender-crystal-render](../blender-crystal-render/SKILL.md)).
  - Fermi surface / Brillouin zone analysis (use [xcrysden-visualizer](../xcrysden-visualizer/SKILL.md)).

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **Capture all axes ($a, b, c$)** | `vesta-snapshot POSCAR -o ./figures` |
| **Capture view along $a$-axis** | `vesta-snapshot POSCAR -v a -o ./figures` |
| **Capture view along $b$-axis** | `vesta-snapshot POSCAR -v b -o ./figures` |
| **Capture view along $c$-axis** | `vesta-snapshot POSCAR -v c -o ./figures` |
| **Keep VESTA open for inspection** | `vesta-snapshot POSCAR --keep-open` |
| **Custom window timeout** | `vesta-snapshot POSCAR --timeout 6.0` |
| **Direct script execution** | `uv run --with python-xlib --with pyautogui python <script_path>/vesta_auto.py POSCAR` |

## Script Options & Arguments

The underlying script is located at:
`skills/vesta-automation/scripts/vesta_auto.py` (and wrapped in `~/.local/bin/vesta-snapshot`).

- `input`: Path to input crystal file (`POSCAR`, `CONTCAR`, `structure.cif`, `file.xsf`).
- `--view`, `-v`: `a`, `b`, `c`, or `all` (default: `all`).
- `--output-dir`, `-o`: Directory to store the output PNG files.
- `--prefix`, `-p`: File prefix (defaults to input file stem).
- `--timeout`: Maximum seconds to wait for the VESTA window to render and register in X11 (default: 4.0s).
- `--keep-open`: Leave the VESTA GUI open after capturing images for manual interactive inspection.

## Common Pitfalls & Solutions

1. **`DISPLAY` not set**: VESTA requires an active X11 display. Ensure `export DISPLAY=:0` or use `xvfb-run` if running headlessly.
2. **Window not detected**: For very large structures (thousands of atoms), VESTA takes longer to load. Increase timeout using `--timeout 8.0`.
3. **Focus issues**: The script automatically raises and focuses the VESTA window before dispatching orientation hotkeys (`a`, `b`, `c`).
