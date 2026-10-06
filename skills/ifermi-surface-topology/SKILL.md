---
name: ifermi-surface-topology
description: Use when constructing, analyzing, or visualizing 3D Fermi surfaces, Fermi velocity vector fields (v_F = (1/hbar) grad_k E(k)), 2D Fermi slices across high-symmetry planes, or extracting Fermi surface area and DOS(E_F) from VASP vasprun.xml files using IFermi.
---

# 🌐 IFermi 3D Fermi Surface & Topology Skill

## Overview
Automates **IFermi** (v0.3.8) for the extraction, topological analysis, and publication rendering of **3D Fermi Surfaces** from DFT outputs (`vasprun.xml`). Generates 3D isosurfaces in the Wigner-Seitz Brillouin zone, projects directional Fermi velocity vector fields ($\mathbf{v}_{\mathrm{F}}$), computes 2D Fermi surface cross-sections, and evaluates quantitative Fermi surface areas and electronic densities of states at the Fermi level $N(E_{\mathrm{F}})$.

---

## 🚀 Key Capabilities

1. **3D Wigner-Seitz Fermi Isosurfaces**:
   - Reconstructs accurate constant-energy isosurfaces at the Fermi level ($E = E_{\mathrm{F}} + \mu$).
   - Standardized Wigner-Seitz cell representation eliminating artificial periodic zone boundary cuts.
   - Separate visualization of individual bands, spin channels (spin-up vs spin-down), or composite pockets.

2. **Fermi Velocity & Spin Texture Projections**:
   - Calculates gradient-based Fermi velocity fields:
     $$\mathbf{v}_{\mathrm{F}}(\mathbf{k}) = \frac{1}{\hbar} \nabla_{\mathbf{k}} E(\mathbf{k})$$
   - Colormaps scalar speed $|\mathbf{v}_{\mathrm{F}}|$ directly onto the 3D surface mesh.
   - Renders 3D vector arrows depicting the directional flux of electronic velocity across the Brillouin zone.

3. **2D Fermi Contours & Slices**:
   - Slices through the 3D Brillouin zone along arbitrary Miller plane orientations $(j, k, l, \text{dist})$.
   - Ideal for 2D materials (e.g. graphene, $\mathrm{MoS}_2$, $\mathrm{CrCl}_3$) and quasi-2D Fermi surfaces ($k_z = 0$).

4. **Quantitative Metrics Extraction**:
   - Computes total Fermi surface area ($S_{\mathrm{F}}$ in $\text{\AA}^{-2}$).
   - Computes average Fermi velocity $\langle |\mathbf{v}_{\mathrm{F}}| \rangle$.
   - Integrates electronic density of states at the Fermi energy $g(E_{\mathrm{F}})$.

---

## ⚡ CLI Usage

```bash
# 1. Calculate quantitative Fermi surface metrics (area, velocity, DOS)
ifermi-surface info -f vasprun.xml --property velocity

# 2. Render 3D Fermi surface with Fermi velocity colormap (Matplotlib / PNG)
ifermi-surface plot -f vasprun.xml -o fermi_surface.png --property velocity --azim 45 --elev 30

# 3. Render 3D Fermi surface with directional velocity arrows
ifermi-surface plot -f vasprun.xml -o fermi_arrows.png --vectors

# 4. Extract 2D Fermi slice at kz = 0 (Miller plane: 0 0 1, dist 0)
ifermi-surface plot -f vasprun.xml -o fermi_slice_kz0.png --slice "0 0 1 0"

# 5. Interactive HTML 3D visualization using Plotly backend
ifermi-surface plot -f vasprun.xml -o fermi_surface.html -t plotly
```

---

## 🐍 Python API Reference

```python
from skills.ifermi_surface_topology.scripts.ifermi_surface import (
    run_ifermi_info,
    run_ifermi_plot
)

# 1. Quantitative inspection
run_ifermi_info("vasprun.xml", mu=0.0, prop="velocity")

# 2. Plot 3D surface
run_ifermi_plot(
    vasprun_file="vasprun.xml",
    output="fermi_surface.png",
    mu=0.0,
    prop="velocity",
    plot_type="matplotlib"
)
```
