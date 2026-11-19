---
name: vmd-automation
description: Use when visualizing, raytracing, or automating analysis of molecular and periodic crystal structures (POSCAR, LAMMPS, PDB, XYZ, Cube, XDATCAR) with VMD 2.0+, headless Tachyon CPU raytracing with ambient occlusion, or batch trajectory analysis.
---

# VMD Automation Skill

## Overview
Headless, scriptable, high-fidelity crystal and molecular visualization powered by **VMD 2.0+** and the bundled **Tachyon Parallel Multiprocessor Ray Tracer**. Renders publication-grade 3D scenes with ambient occlusion, soft contact shadows, principled specular highlights, and multi-sample anti-aliasing directly from simulation files (VASP POSCAR/XDATCAR/CHGCAR, LAMMPS dump/yaml, PDB, XYZ, Cube, DX, XSF) completely offscreen without requiring an active X11 display server or GPU.

---

## Key Capabilities & Scientific Protocols

### 1. Headless Zero-X11 Tachyon Raytracing Architecture
- **Problem**: Standard VMD GUI requires an active X-Windows `$DISPLAY` and manual mouse clicks to align viewpoints, toggle representations, and export figures.
- **Solution**: Programmatically generates transient TCL scripts driving VMD in text mode (`vmd -dispdev text -e script.tcl`) to construct molecular scenes and export scene models directly to the Tachyon engine (`tachyon_LINUXAMD64`):
  - **Ambient Occlusion**: `--ao 0.7` (`-auto_skylight 0.7`) illuminates crevices and casts natural soft contact shadows under atoms and bonds.
  - **Anti-Aliasing**: `--samples 12` (`-aasamples 12`) eliminates jagged pixel edges.
  - **Full Shading**: `-fullshade` computes multi-reflection specular highlights and depth.
  - **High-DPI Output**: Arbitrary resolutions (`--width 1920 --height 1080` for 1080p, or `--width 3840 --height 2160` for 4K UHD).

### 2. Multi-Engine & Multi-Format Simulation Compatibility
Automatically detects and routes structure formats to native VMD molfile plugins:
- **VASP**:
  - `POSCAR` / `CONTCAR` (`type POSCAR`)
  - `XDATCAR` trajectories (`type XDATCAR`)
  - Volumetric charge densities (`CHGCAR`, `LOCPOT`, `PARCHG`)
  - `vasprun.xml` (`type xml`)
- **LAMMPS**:
  - Trajectory dumps (`type lammpstrj`)
  - YAML configuration files (`type lammpsyaml`)
- **Quantum Chemistry & Biology**:
  - Protein Data Bank (`.pdb`, `.ent`) and mmCIF/PDBx (`.cif`, `.pdbx`)
  - Extended XYZ (`.xyz`) and Sybyl MOL2 (`.mol2`)
  - Gaussian Cube (`.cube`) and OpenDX (`.dx`) grids
  - XCrySDen Structure Files (`.xsf`)
  - GROMACS (`.gro`, `.xtc`, `.trr`) and NAMD/CHARMM (`.dcd`)

### 3. Calibrated Scientific Presets (`--preset`)
- `--preset 2d-carbon`: Calibrated for graphene, PHOTH-graphene, BCN monolayers, and carbon allotropes.
  - Carbon sphere scale: `0.38 Å`
  - Bond cylinder radius: `0.14 Å`
  - Shading material: `AOShiny`
- `--preset perovskite`: Calibrated for halide and oxide perovskite cages ($ABX_3$).
  - Cation/Halide sphere scale: `0.65 Å`
  - Bond radius: `0.18 Å`
- `--preset biomolecule`:
  - Secondary structure ribbon: `NewCartoon`
  - Shading material: `AOShiny`
- `--preset standard`:
  - Balanced ball-and-stick: sphere scale `0.45 Å`, bond radius `0.18 Å`
- `--preset quicksurf`:
  - Smooth continuous Gaussian density surface for solvent interfaces.
- `--preset spacefill`:
  - Full Van der Waals radius spheres (`VDW`).

### 4. Crystallographic Projections & Unit Cell Boundary Boxes
- Projections along high-symmetry axes:
  - `-v c` (or `xy`): Looking down the $c$-axis onto the basal $xy$ plane (standard top view).
  - `-v a` (or `yz`): Looking down the $a$-axis onto the $yz$ plane (`rotate y by -90`).
  - `-v b` (or `xz`): Looking down the $b$-axis onto the $xz$ plane (`rotate x by 90`).
  - `-v iso`: True isometric projection ($\arcsin(1/\sqrt{3}) \approx 35.264^\circ$, `rotate y by -45; rotate x by 35.264`).
  - `-v all`: Automatically batch-renders all 4 views ($a, b, c, \text{iso}$) into an organized directory.
- **Unit Cell Box**: `--pbc-box` activates `pbctools` (`pbc box -color black -width 2.0`) to delineate lattice vectors.
- **Periodic Replicas**: `--periodic-images "+X -X +Y -Y"` seamlessly expands supercells across periodic boundaries.

### 5. Headless Trajectory Animation (`vmd-anim`)
- Iterates over molecular dynamics frames (LAMMPS dump, VASP XDATCAR, DCD).
- **Zero-Dilation Camera Locking**: Locks orthographic camera FOV and orientation across all time steps, eliminating frame jitter or jump cuts.
- Encodes output sequences directly into publication-grade **MP4 video** (via `ffmpeg` H.264 CRF 18) or **animated GIF** (via Pillow) with configurable FPS (`--fps 24`) and stride (`--stride 2`).

### 6. 3D Volumetric Isosurface Raytracing (`vmd-volumetric`)
- Renders Charge Density Difference (CDD), electrostatic potentials, or electron density from `CHGCAR`, `LOCPOT`, or `.cube` files.
- **Dual Isosurfaces**:
  - Yellow/Gold accumulation isosurface ($+\Delta\rho$, `--isoval 0.005`)
  - Cyan/Blue depletion isosurface ($-\Delta\rho$, `--isoval -0.005`)
  - Raytraced together with underlying CPK atomic framework.

### 7. Automated Publication Whitespace Trimming (`--autotrim`)
- Converts default viewports into pure publication white backgrounds (`--bg white`).
- Analyzes bounding boxes and crops redundant border margins down to a crisp, uniform 30 px padding (`--trim-padding 30`).

---

## Quick Reference CLI

| Action | CLI Command |
| :--- | :--- |
| **All views ($a, b, c, \text{iso}$)** | `vmd-render POSCAR -o ./figures/ -v all --pbc-box` |
| **Isometric 3D with Unit Cell Box** | `vmd-render POSCAR -o crystal_iso.png -v iso --pbc-box` |
| **2D Carbon preset (PHOTH-graphene)** | `vmd-render POSCAR -o graphene_c.png -v c --preset 2d-carbon` |
| **Perovskite with custom resolution** | `vmd-render POSCAR -o perovskite.png --preset perovskite --width 2560 --height 1440` |
| **High-Precision 4K UHD Raytrace** | `vmd-render POSCAR -o 4k_render.png --width 3840 --height 2160 --samples 16` |
| **Spacefill / VDW representation** | `vmd-render POSCAR -o vdw.png --rep vdw -v iso` |
| **Continuous QuickSurf surface** | `vmd-render structure.pdb -o surf.png --rep quicksurf` |
| **Biomolecule ribbon cartoon** | `vmd-render protein.pdb -o protein.png --preset biomolecule` |
| **Periodic Replicas ($2\times 2$)** | `vmd-render POSCAR -o supercell.png --periodic-images "+X +Y"` |
| **MD Trajectory to MP4 Video** | `vmd-anim XDATCAR -o md_run.mp4 --fps 30 --stride 2 -v iso --pbc-box` |
| **MD Trajectory to Animated GIF** | `vmd-anim dump.lammpstrj -o trajectory.gif --fps 15 --pbc-box` |
| **3D CDD Dual Isosurfaces** | `vmd-volumetric CHGCAR -o cdd_3d.png --isoval 0.008 -v iso` |

---

## Script Architecture & CLI Binaries

Installed globally in `~/.local/bin/` and symlinked to `skills/vmd-automation/scripts/`:
- `vmd-render` -> `skills/vmd-automation/scripts/vmd_render.py`
- `vmd-anim` -> `skills/vmd-automation/scripts/vmd_anim.py`
- `vmd-volumetric` -> `skills/vmd-automation/scripts/vmd_volumetric.py`
