---
name: site-pyramidalization-zoom
description: Use when creating publication-ready multi-panel scientific figures featuring circular zoom insets, coordination polyhedra (tetrahedral pyramidalization), Haddon POAV1 angle calculations, curved leader callouts, and atomic property colormaps.
---

# Site Pyramidalization & Circular Zoom Annotator

## Overview
Generates publication-quality scientific illustrations and multi-panel figures for 2D materials, heterogeneous catalysis, surface adsorption, and stereochemistry. Replicates and surpasses top-tier journal aesthetics (Nature, ACS, Science) by automating:
1. **Circular Site Zoom Insets**: High-resolution circular cutouts centered at local adsorption/reaction sites ($S_1, S_2, \dots$) with crisp antialiased borders.
2. **Pyramidalization Coordination Polyhedra**: Shaded 3D translucent tetrahedra visualising local $sp^2 \rightarrow sp^3$ rehybridization and out-of-plane puckering.
3. **Rigorous Geometric Analysis**: Exact Haddon POAV1 ($\pi$-orbital axis vector) pyramidalization angles ($\theta_p$), inter-bond angles ($\theta_1, \theta_2, \theta_3$), puckering heights ($\Delta h$), and coordination volumes.
4. **Macro-to-Micro Callouts**: Curved Bezier leader arrows connecting parent structures to local zoomed insets.
5. **Continuous Scalar Property Mapping**: Element-wise color coding (adsorption free energy $\Delta G_{\text{ads}}$, Bader charges, or magnetic moments) with formatted vertical colorbars.
6. **Multi-Panel Scientific Layouts**: Assembles composite figures (Panels a, b, and e–j) formatted with Times New Roman typography and STIX mathematical notation.
7. **Multi-Visualizer Backend Integration**: Seamlessly dispatches cluster renders through `native` (Matplotlib vector), `ovito` (headless 3D ray-traced), or `vesta` (desktop VESTA GUI on X11).
8. **Automated Optimal Calculations & Reporting**: Auto-detects top catalytic sites by strain or adsorbate binding, and exports structured reports (`analysis_report.json` and `analysis_report.csv`).

---

## When to Use
- **Trigger**: The user requests zoomed circular snapshots of active sites, coordination polyhedra, or pyramidalization angle calculations.
- **Trigger**: Preparing composite multi-panel figures (e.g. macro property map + 3D overview with leader arrows + grid of local site circular zooms).
- **Trigger**: Analyzing local puckering, $sp^2/sp^3$ rehybridization, or active site coordination in graphene, 2D carbons, transition metal dichalcogenides, MOFs, or clusters.
- **Trigger**: Automating multi-backend rendering with VESTA or OVITO.

---

## Quick Reference

| Action | CLI Command |
| :--- | :--- |
| **Fully Automated Workflow (Auto-sites + Composite + Reports)** | `site-zoom POSCAR --auto-sites --composite -o ./figures` |
| **Composite with $\Delta G_{\text{ads}}$ Colormap** | `site-zoom POSCAR --sites "S1:17,S2:25,S3:30,S4:35,S5:28,S6:29" --property-csv dG_ads.csv --colorbar-label "$\Delta G_{\mathrm{ads}}\ (\mathrm{eV})$" --composite` |
| **OVITO 3D Headless Backend** | `site-zoom POSCAR --site 29 --backend ovito --polyhedron --arcs -o ./figures` |
| **VESTA X11 Backend** | `site-zoom POSCAR --site 29 --backend vesta --polyhedron --arcs -o ./figures` |
| **Single Site Zoom with 3D Pyramid & Arcs** | `site-zoom POSCAR --site 29 --polyhedron --arcs --elev 20 --azim -35 -o ./figures` |
| **Custom Zoom Radius (e.g. 5.5 Å)** | `site-zoom POSCAR --site 29 --radius 5.5 --polyhedron` |
| **Generate Benchmark Demo Structure** | `python skills/site-pyramidalization-zoom/scripts/generate_demo_structure.py` |

---

## Physical Background: Haddon's POAV1 Pyramidalization

In planar $sp^2$ networks (graphene, biphenylene, pristine aromatics), atoms have 3 coplanar bonds ($\theta_1 = \theta_2 = \theta_3 = 120^\circ$) and the $\pi$-orbital is orthogonal to all three $\sigma$ bonds ($\theta_{\sigma\pi} = 90^\circ$).

When an adatom (e.g., H, OH, O, or metal) adsorbs, local $sp^2 \rightarrow sp^3$ rehybridization puckers the central atom out of plane.

### 1. Vector Formulation
Given three unit bond vectors $\vec{u}_1, \vec{u}_2, \vec{u}_3$ from the central atom to its three framework neighbors:
$$\vec{w} = (\vec{u}_1 \times \vec{u}_2) + (\vec{u}_2 \times \vec{u}_3) + (\vec{u}_3 \times \vec{u}_1)$$
The unit $\pi$-orbital axis vector is:
$$\vec{v}_{\pi} = \frac{\vec{w}}{\|\vec{w}\|}$$
The angle $\theta_{\sigma\pi}$ between the $\pi$-orbital and each $\sigma$-bond is:
$$\cos \theta_{\sigma\pi} = \vec{v}_{\pi} \cdot \vec{u}_1 = \frac{\det([\vec{u}_1, \vec{u}_2, \vec{u}_3])}{\|\vec{w}\|}$$
The **Haddon Pyramidalization Angle** $\theta_p$ is defined as:
$$\theta_p = \theta_{\sigma\pi} - 90^\circ$$

- **Ideal planar $sp^2$**: $\theta_{\sigma\pi} = 90.00^\circ \implies \theta_p = 0.00^\circ$
- **Ideal tetrahedral $sp^3$**: $\theta_{\sigma\pi} = 109.47^\circ \implies \theta_p = 19.47^\circ$

### 2. Coordination Polyhedron
The shaded tetrahedron comprises 4 vertices:
- **Base Triangle**: Formed by the 3 nearest framework neighbors ($B_1, B_2, B_3$).
- **Apex**: The active puckered atom ($A$) or the capping adsorbate ($X$, e.g. H).
- **Out-of-Plane Puckering Height ($\Delta h$)**: Distance of $A$ from the plane $(B_1, B_2, B_3)$.
- **Coordination Volume ($V_{\text{tet}}$)**: Volume enclosed by the tetrahedron:
  $$V_{\text{tet}} = \frac{1}{6} \left| (\vec{r}_1 - \vec{r}_0) \cdot ((\vec{r}_2 - \vec{r}_0) \times (\vec{r}_3 - \vec{r}_0)) \right|$$

---

## Options & Arguments

- `input`: Path to atomic structure (`POSCAR`, `CONTCAR`, `structure.cif`, `molecule.xyz`).
- `--site`, `-s`: Single active site index (0-based or 1-based).
- `--sites`: Comma-separated named sites, e.g. `'S1:17,S2:25,S3:30,S4:35,S5:28,S6:29'` or `'17,25,30'`.
- `--auto-sites`: Automatically detect top active sites (enabled by default when `--sites` or `--site` are omitted).
- `--auto-mode`: Auto-detection ranking strategy: `all` (adsorbate-bound + strain), `adsorbate`, or `strain` (highest $\theta_p$).
- `--top-n`: Number of active sites to auto-detect (default: `6`).
- `--backend`: Visualizer engine for circular snapshots: `native` (vector Matplotlib), `ovito` (headless 3D), `vesta` (desktop VESTA GUI).
- `--radius`, `-r`: Zoom cutoff radius in Ångströms (default: `4.8`).
- `--polyhedron`: Enable shaded blue coordination tetrahedron.
- `--arcs`: Enable red circular angle arcs ($\theta_1, \theta_2, \theta_3$).
- `--elev`: Camera elevation angle in degrees (default: `15.0`).
- `--azim`: Camera azimuth angle in degrees (default: `-30.0`).
- `--property-csv`: CSV file mapping atom indices to scalar properties (e.g. `atom_index,dG_ads_eV`).
- `--property-col`: Target column in the CSV (default: `dG_ads_eV`).
- `--colorbar-label`: Colorbar title (supports LaTeX math, e.g. `$\Delta G_{\mathrm{ads}}\ (\mathrm{eV})$`).
- `--composite`: Render the complete multi-panel figure (Panel a: property map, Panel b: 3D macro + callout + pyramid inset, Panels e-j: circular zooms).
- `--pyramid-site`: Designated site name for the 3D pyramid inset in composite mode (default: `S6`).

---

## Publication Typography & Figure Standards

All figures and animated GIF loops generated under this skill MUST strictly adhere to:
1. **Font Family**: Times New Roman typography (`font.family: serif`, `font.serif: ["Times New Roman", "DejaVu Serif"]`, `mathtext.fontset: "stix"`).
2. **Mathematical Notation**: Rigorous LaTeX STIX math formatting with proper roman text prefixes (`\mathrm{}`) for elements, units, and chemical species (e.g., $\Delta z_{\mathrm{buckle}}$, $d(\mathrm{C-H})$, $\theta_p(\mathrm{POAV1})$, $\Delta G_{\mathrm{H}^*}$).
3. **Centered Titles**: All figure and GIF animation titles must be horizontally centered (`ha="center"`, `x = width / 2`).
4. **Seamless Reversible Loops**: In dynamic chemisorption cycles, reaction coordinates must smoothly ping-pong from $0 \rightarrow 1 \rightarrow 0$ using harmonic/smoothstep weighting $\lambda(\tau) = \frac{1 - \cos(\tau)}{2}$ so $\lambda'(0) = \lambda'(2\pi) = 0$, guaranteeing zero velocity jumps at loop seams.

- `--output-dir`, `-o`: Directory to save generated PNG and PDF files.
- `--prefix`, `-p`: File prefix (default: `site_zoom`).
- `--dpi`: Figure resolution (default: `300`).
