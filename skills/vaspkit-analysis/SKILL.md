---
name: vaspkit-analysis
description: Use when generating high-symmetry k-paths (2D/3D/HSE06), post-processing electronic band structures, plotting TDOS/PDOS, calculating 2D/3D elastic constants and moduli, extracting work functions, or automating VASPKIT workflows non-interactively.
---

# VASPKIT Analysis & Automation Skill

## Overview
Automates **VASPKIT** (the premier pre- and post-processing toolkit for VASP) across macOS and Linux HPC clusters. Provides programmatic, non-interactive execution for generating high-symmetry k-paths (2D monolayers, 3D bulk, and HSE06 hybrid functionals), extracting band structures and direct/indirect band gaps, decomposing total and orbital-projected DOS, computing 2D/3D elastic tensors and mechanical stability criteria, and evaluating work functions.

---

## Key Capabilities & Scientific Workflows

### 1. High-Symmetry K-Path Generation
- **2D Materials (`--kpath-2d` / Task 103)**:
  - Generates recommended SeeK-path / Bradley-Cracknell k-paths for monolayers and heterostructures (e.g. $\Gamma - M - K - \Gamma$ for hexagonal lattices, or $\Gamma - X - S - Y - \Gamma$ for rectangular/orthorhombic systems like PHOTH-graphene).
  - Automatically isolates the $k_z = 0$ reciprocal plane, preventing spurious out-of-plane dispersion.
  - Outputs `KPOINTS`, `KLABELS`, and `HIGH_SYMMETRY_POINTS`.
- **3D Bulk Crystals (`--kpath-3d` / Task 102)**:
  - Standardizes the primitive unit cell (`PRIMCELL.vasp`) and builds standard crystallographic k-paths.
- **HSE06 Hybrid Functional K-Mesh (Task 108)**:
  - Merges regular self-consistent k-mesh with zero-weight line-mode k-points into a single `KPOINTS` file for single-shot hybrid functional band structures.

### 2. Electronic Band Structure Post-Processing (`--band` / Task 211)
- Automatically extracts eigenvalues from `EIGENVAL`, shifts energy relative to Fermi level ($E - E_{\mathrm{F}}$), and outputs `BAND.dat` and `KLABELS`.
- Computes band gap ($E_g$), flags Direct vs. Indirect nature, and locates VBM and CBM coordinates in $k$-space.
- Native integration with [`plot_vaspkit_band.py`](file:///Users/apple/Research/abc/scientific-research-mcp/skills/vaspkit-analysis/scripts/plot_vaspkit_band.py):
  - Times New Roman & STIX math typography ($E - E_{\mathrm{F}}\ (\mathrm{eV})$).
  - High-symmetry vertical boundary lines with Greek symbol translation ($\text{GAMMA} \rightarrow \Gamma$).
  - Simultaneous Spin-Up (solid blue) and Spin-Down (dashed red) superposition.
  - Dual export to 300+ DPI PNG and vector PDF.

### 3. Density of States (DOS/PDOS) (`--dos` / Tasks 111 & 112)
- Extracts Total DOS (`TDOS.dat`) and Projected DOS (`PDOS_*.dat` per element and orbital).
- Native integration with [`plot_vaspkit_dos.py`](file:///Users/apple/Research/abc/scientific-research-mcp/skills/vaspkit-analysis/scripts/plot_vaspkit_dos.py):
  - Area-shaded curves with calibrated opacity.
  - VESTA element color mapping (concordant with crystal structure figures).
  - Symmetric spin-polarized view ($\text{DOS}_{\mathrm{up}} > 0, \text{DOS}_{\mathrm{down}} < 0$).

### 4. Mechanical & Elastic Constants (`--elastic-2d` / `--elastic-3d`)
- **2D Materials (Task 201)**:
  - Calculates in-plane stiffness tensor components: $C_{11}, C_{22}, C_{12}, C_{66}\ (\mathrm{N/m})$.
  - Evaluates directional 2D Young's Modulus ($Y_x, Y_y$) and in-plane Poisson's ratio ($\nu_{xy}, \nu_{yx}$).
  - Verifies Born mechanical stability criteria for 2D sheets ($C_{11}C_{22} - C_{12}^2 > 0$ and $C_{66} > 0$).
- **3D Bulk Crystals (Task 202)**:
  - Computes Voigt-Reuss-Hill bulk modulus ($B_{\mathrm{VRH}}$) and shear modulus ($G_{\mathrm{VRH}}$).
  - Evaluates Pugh's ductility ratio ($B/G > 1.75$ indicates ductile behavior; $< 1.75$ indicates brittle).
  - Computes Cauchy pressure ($C_{12} - C_{44}$) and universal elastic anisotropy index $A^U$.

### 5. Work Function & Electrostatic Potentials (`--work-function` / Task 426)
- Reads `LOCPOT`, computes planar average along the surface normal $z$, identifies asymptotic vacuum plateau ($V_{\mathrm{vac}}$), and evaluates the work function:
  $$\Phi = V_{\mathrm{vac}} - E_{\mathrm{F}}$$

---

## Quick Reference

| Scientific Task | CLI Command | Key Outputs |
| :--- | :--- | :--- |
| **Generate 2D Monolayer K-Path** | `vaspkit-auto --kpath-2d` | `KPOINTS`, `KLABELS` |
| **Generate 3D Bulk K-Path** | `vaspkit-auto --kpath-3d` | `KPOINTS`, `PRIMCELL.vasp` |
| **Extract & Plot Band Structure** | `vaspkit-auto --band` | `BAND.dat`, `band_structure.png/pdf` |
| **Extract & Plot TDOS + PDOS** | `vaspkit-auto --dos` | `TDOS.dat`, `density_of_states.png/pdf` |
| **2D Elastic Constants & Moduli** | `vaspkit-auto --elastic-2d` | $C_{ij}$, Young's modulus, Poisson's ratio |
| **3D Elastic Constants (VRH)** | `vaspkit-auto --elastic-3d` | $B_{\mathrm{VRH}}, G_{\mathrm{VRH}}, E$, Pugh ratio |
| **Extract Work Function** | `vaspkit-auto --work-function` | $V_{\mathrm{vac}}, E_{\mathrm{F}}, \Phi\ (\mathrm{eV})$ |
| **Raw VASPKIT Task Execution** | `vaspkit-auto --task 108` | Direct stdin pipe execution |
| **Plot Existing Band Data** | `plot-vaspkit-band --erange -3 3` | Publication vector band plot |
| **Plot Existing DOS Data** | `plot-vaspkit-dos --erange -4 4` | Publication vector DOS plot |

---

## Standard Task Number Reference

| Task Code | Category | Purpose |
| :---: | :--- | :--- |
| **101** | K-Points | Monkhorst-Pack or $\Gamma$-centered k-mesh generation |
| **102 / 303** | K-Points | High-symmetry k-path for 3D bulk structures (303 in modern CLI) |
| **103 / 302** | K-Points | High-symmetry k-path for 2D monolayers/slabs (302 in modern CLI) |
| **108** | K-Points | Hybrid functional (HSE06) band k-mesh generator |
| **111** | DOS | Total Density of States (`TDOS.dat`) |
| **112** | DOS | Projected Density of States (`PDOS_*.dat`) |
| **201** | Elastic | 2D elastic constants ($C_{11}, C_{22}, C_{12}, C_{66}$) |
| **202** | Elastic | 3D elastic constants & Voigt-Reuss-Hill moduli |
| **211** | Bands | Electronic band structure & band gap extraction |
| **212** | Bands | Projected (fat) band structure |
| **251** | Transport | Carrier effective mass ($m^*$) parabolic fitting |
| **302** | K-Points | 2D Structure K-Path (modern CLI mode) |
| **303** | K-Points | 3D Bulk Structure K-Path (modern CLI mode) |
| **311** | Charge | Planar-averaged charge density or electrostatic potential |
| **313** | Charge | 3D Charge Density Difference ($\Delta\rho$) |
| **426** | Surface | Work function calculation ($\Phi = V_{\mathrm{vac}} - E_{\mathrm{F}}$) |
| **501** | Optical | Linear optical absorption, reflectivity, and dielectric tensor |
| **602** | Symmetry | Find Primitive Cell (`PRIMCELL.vasp`) |
| **603** | Symmetry | Find Standard Conventional Cell |

---

## Python API Integration

```python
from vaspkit_auto import (
    generate_kpath_2d,
    extract_band_structure,
    extract_dos,
    calculate_elastic_constants,
    calculate_work_function,
)

# 1. Generate k-path for 2D sheet
kpath_info = generate_kpath_2d(calc_dir="./monolayer")
print(f"KPOINTS created: {kpath_info['kpoints']}")

# 2. Post-process band calculation and auto-plot
band_info = extract_band_structure(calc_dir="./band_calc", plot=True)
print(f"Band gap: {band_info['band_gap_eV']} eV ({band_info['gap_type']})")
print(f"Plot saved: {band_info['plots']['pdf']}")

# 3. Compute 2D elastic properties
elastic_info = calculate_elastic_constants(calc_dir="./strain_calc", dim="2D")
print(f"In-plane stiffness C11: {elastic_info['C11_N_m']} N/m")
```

---

## Common Pitfalls & Solutions

1. **`arch -x86_64` on Apple Silicon Macs**:
   VASPKIT official precompiled binaries for macOS are x86_64 Mach-O binaries. `vaspkit_auto.py` automatically detects Apple Silicon arm64 environments and executes via macOS Rosetta 2 (`arch -x86_64 vaspkit`).
2. **Missing `~/.vaspkit` Configuration**:
   On initial launch, VASPKIT creates a default `~/.vaspkit` configuration file in the user home directory. Default symmetry tolerances (`SYMMETRY_TOLERANCE = 1E-5`) and plotting defaults can be customized there.
3. **Collinear points in 2D K-Path**:
   Ensure vacuum spacing along the $z$-axis is at least 12–15 Å in the `POSCAR` before calling Task 103 so VASPKIT correctly classifies the geometry as a 2D periodic slab.
