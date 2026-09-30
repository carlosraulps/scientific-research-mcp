---
name: blender-crystal-render
description: Use when generating publication-quality, photorealistic 3D ray-traced figures of crystal structures (POSCAR, CIF, XYZ) with ball-and-stick, polyhedra, studio lighting, depth of field, or Cycles/Eevee materials.
---

# Blender Crystal Render Skill

## Overview
Headless, publication-quality 3D crystal structure ray-tracing powered by Blender 5.2. Parses crystal coordinates (POSCAR, CIF, XYZ), builds 3D atoms with realistic PBR materials and CPK colors, constructs nearest-neighbor bonds and unit cell wireframes, configures 3-point studio lighting, and renders publication-ready figures using EEVEE or CYCLES.

## When to Use
- **Trigger**: Creating high-impact publication figures, journal table-of-contents graphics (TOC), or presentation slides.
- **Trigger**: Requiring true ray-traced global illumination, depth of field, specular highlights, and soft shadows.
- **Trigger**: Headless rendering without launching a desktop GUI.
- **When NOT to use**:
  - Quick, sub-second screening of hundreds of structures (use [ovito-snapshot](../ovito-snapshot/SKILL.md)).
  - Interactive manual polyhedra manipulation or live crystal editing (use [vesta-automation](../vesta-automation/SKILL.md)).
  - Fermi surface / Brillouin zone analysis (use [xcrysden-visualizer](../xcrysden-visualizer/SKILL.md)).

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **All views ($a, b, c, \text{iso}$)** | `blender-render POSCAR -o ./figures` |
| **Isometric studio render** | `blender-render POSCAR -v iso -o ./figures` |
| **Photorealistic Cycles ray-tracing** | `blender-render POSCAR --engine cycles --samples 128` |
| **Orthographic crystallographic projection** | `blender-render POSCAR -v c --ortho` |
| **Transparent background (for slides/papers)** | `blender-render POSCAR --transparent` |
| **High resolution (4K UHD)** | `blender-render POSCAR --width 3840 --height 2160` |
| **Custom bond cutoff & atom scale** | `blender-render POSCAR --bond-cutoff 3.2 --scale-atoms 1.2` |

## Script Options & Arguments

The underlying script is located at:
`skills/blender-crystal-render/scripts/render_blender.py` (and wrapped in `~/.local/bin/blender-render`).

- `input`: Path to input crystal structure (`POSCAR`, `structure.cif`, `molecule.xyz`).
- `--view`, `-v`: `a`, `b`, `c`, `iso`, or `all` (default: `all`).
- `--output-dir`, `-o`: Directory to store the output PNG files.
- `--prefix`, `-p`: File prefix (defaults to input file stem).
- `--engine`: `eevee` (rapid high-quality rendering, default) or `cycles` (physically-based path tracing).
- `--samples`: Sampling rate for Cycles path tracing (default: 64).
- `--bond-cutoff`: Cutoff distance in Ångströms for bond generation (default: 2.8 Å).
- `--bond-radius`: Cylinder thickness for bonds (default: 0.08 Å).
- `--scale-atoms`: Multiplier for atomic sphere radii (default: 1.0).
- `--no-bonds`: Disable bond cylinder rendering.
- `--no-cell`: Hide the unit cell wireframe box.
- `--ortho`: Enable orthographic camera projection for $a, b, c$ axes.
- `--transparent`: Render with transparent alpha channel for seamless integration into papers.

## Common Pitfalls & Solutions

1. **Cycles render is slow**: For quick drafts, stick to `--engine eevee` (completes in ~3-4s). For final submission graphics, switch to `--engine cycles`.
2. **Atoms appear too large/small**: Adjust `--scale-atoms` (e.g., `--scale-atoms 0.8` for dense lattices or spacefill).
3. **No bonds visible**: Increase `--bond-cutoff` (e.g. `--bond-cutoff 3.5` for extended coordination complexes).
