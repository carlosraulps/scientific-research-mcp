---
name: ovito-snapshot
description: Use when needing headless, high-throughput, scriptable 2D/3D snapshots or animations of atomic structures (POSCAR, CONTCAR, CIF, XYZ, LAMMPS) along crystallographic axes (a, b, c, isometric) without a GUI.
---

# OVITO Snapshot Skill

## Overview
Headless, high-throughput crystal structure and trajectory rendering using the OVITO Python API. Renders high-resolution orthographic or perspective images along crystallographic axes ($a$, $b$, $c$, isometric) in seconds with zero GUI overhead or display requirements.

## When to Use
- **Trigger**: Need quick, automated, high-resolution snapshots of atomic structures (POSCAR, CONTCAR, CIF, XYZ, LAMMPS).
- **Trigger**: Batch processing dozens or hundreds of relaxed geometries or MD trajectory frames.
- **Trigger**: Headless cluster environments or remote servers without active X11/Wayland desktop displays.
- **When NOT to use**:
  - Interactive GUI editing or manual bond manipulation (use [vesta-automation](../vesta-automation/SKILL.md)).
  - Photorealistic, ray-traced publication covers with complex depth of field and PBR materials (use [blender-crystal-render](../blender-crystal-render/SKILL.md)).
  - Fermi surface / Brillouin zone k-path analysis (use [xcrysden-visualizer](../xcrysden-visualizer/SKILL.md)).

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **All views ($a, b, c, \text{iso}$)** | `ovito-snapshot POSCAR -o ./figures` |
| **View along $c$-axis (xy plane)** | `ovito-snapshot POSCAR -v c -o ./figures` |
| **View along $a$-axis (yz plane)** | `ovito-snapshot POSCAR -v a -o ./figures` |
| **Supercell expansion ($2\times 2\times 2$)** | `ovito-snapshot POSCAR --supercell 2 2 2` |
| **Polyhedral matching** | `ovito-snapshot POSCAR --polyhedra` |
| **High resolution (4K UHD)** | `ovito-snapshot POSCAR --width 3840 --height 2160` |
| **Bader charge color coding (Blue-Red)** | `ovito-snapshot POSCAR --bader-file ACF.dat -v iso` |
| **Bader with explicit range & legend** | `ovito-snapshot POSCAR --bader-file ACF.dat --charge-range -2.5 2.5` |
| **Direct script execution** | `uv run --with ovito --with ase python <script_path>/render_ovito.py POSCAR` |

## Script Options & Arguments

The underlying script is located at:
`skills/ovito-snapshot/scripts/render_ovito.py` (and wrapped in `~/.local/bin/ovito-snapshot`).

- `input`: Path to input crystal/trajectory file (`POSCAR`, `CONTCAR`, `structure.cif`, `dump.lammpstrj`).
- `--view`, `-v`: `a`, `b`, `c`, `iso`, or `all` (default: `all`).
- `--output-dir`, `-o`: Directory to store the output PNG files.
- `--prefix`, `-p`: File prefix (defaults to input file stem).
- `--supercell NX NY NZ`: Expand periodic boundaries by integers along $a, b, c$.
- `--bond-cutoff`: Cutoff distance in Ångströms for bond generation (default: 3.0 Å).
- `--no-bonds`: Disable bond cylinder rendering (render spacefill/balls only).
- `--polyhedra`: Enable coordination polyhedra generation.
- `--no-tripod`: Hide the coordinate axes tripod overlay.
- `--projection`: `ortho` (orthographic, default for crystal axes) or `perspective`.
- `--background`: `white`, `black`, `gray`, or `transparent`.
- `--bader-file`: Path to Henkelman Bader `ACF.dat` or charge column to color-code atoms.
- `--charge-range MIN MAX`: Set explicit bounds for the diverging color scale (e.g. `--charge-range -2.5 2.5`).
- `--bader-colormap`: Diverging colormap gradient (`BlueWhiteRed`, `Viridis`, `Magma`). Automatically adds a floating `ColorLegendOverlay`.

## Common Pitfalls & Solutions

1. **Atoms appear disconnected**: Increase `--bond-cutoff` (e.g. `--bond-cutoff 3.5` for large ionic radii).
2. **Atoms overlap heavily**: Disable bonds (`--no-bonds`) or decrease bond cutoff.
3. **Missing module errors**: Run via `ovito-snapshot` or `uv run --with ovito --with ase python render_ovito.py`.
