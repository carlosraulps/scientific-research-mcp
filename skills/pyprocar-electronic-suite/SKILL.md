---
name: pyprocar-electronic-suite
description: Use when analyzing electronic structure from VASP PROCAR and OUTCAR files, including orbitally projected fat bands, spin texture (Sx, Sy, Sz) for Rashba/topological states, supercell band unfolding onto primitive Brillouin zones, and direct/indirect band gap extraction.
---

# ⚡ PyProcar Electronic Structure Suite Skill

## Overview
Automates post-processing of electronic eigenstates and wavefunctions using **PyProcar** (v6.5.0). Specializes in orbitally projected fat bands, full spin texture mapping ($S_x, S_y, S_z$), supercell band unfolding for dopants and defective lattices, and direct/indirect band gap determination.

---

## 🚀 Key Capabilities

1. **Orbitally Projected Fat Bands**:
   - Decomposes Bloch state wavefunctions into atomic site contributions ($i$) and orbital channels ($s, p_x, p_y, p_z, d_{xy}, d_{yz}, d_{z^2}, d_{xz}, d_{x^2-y^2}$).
   - Generates parametric colormapped bands, scatter fat bands, and multi-element overlay plots.

2. **Spin Texture Mapping**:
   - Parses non-collinear spin-orbit coupling (SOC) wavefunctions (`LNONCOLLINEAR = .TRUE.`, `LSORBIT = .TRUE.`).
   - Resolves expectations values of Pauli spin matrices $\langle \sigma_x \rangle$, $\langle \sigma_y \rangle$, $\langle \sigma_z \rangle$.
   - Visualizes Rashba spin splitting and helical spin textures around Dirac cones and high-symmetry points.

3. **Supercell Band Unfolding**:
   - Unfolds folded bands from large supercells ($2\times2$, $3\times3$, $4\times4$) back into the primitive Brillouin zone using spectral weight projection:
     $$A(\mathbf{k}, E) = \sum_J |\langle \mathbf{k} | K_J \rangle|^2 \delta(E - E_J)$$
   - Essential for resolving effective band dispersion in defective, alloyed, or doped systems.

4. **Band Gap & Transition Analysis**:
   - Automatically detects valence band maximum (VBM) and conduction band minimum (CBM).
   - Identifies whether the fundamental gap is direct or indirect, reporting exact $k$-point coordinates.

---

## ⚡ CLI Usage

The suite provides the unified `pyprocar-suite` utility:

```bash
# 1. Plot fat bands for specific atom and d-orbitals in energy range [-3, +3] eV
pyprocar-suite bands -d ./calc -a "0,1" -o "4,5,6,7,8" -e "-3,3" --out cr_d_bands.png

# 2. Plot Sz spin texture
pyprocar-suite spin -d ./calc -c z -e "-2,2" --out sz_texture.png

# 3. Unfold 2x2x1 supercell band structure onto primitive unit cell
pyprocar-suite unfold -d ./calc -m "2,0,0,0,2,0,0,0,1" -e "-4,4" --out unfolded.png

# 4. Extract fundamental band gap
pyprocar-suite gap -d ./calc
```

---

## 🐍 Python API Reference

```python
from skills.pyprocar_electronic_suite.scripts.pyprocar_suite import (
    run_bands,
    run_spin_texture,
    run_unfold,
    run_bandgap
)

# 1. Fat bands
run_bands(dirname="./vasp_calc", atoms="0,1", orbitals="4,5,6,7,8", elimit="-3,3", outname="fat_bands.png")

# 2. Spin texture
run_spin_texture(dirname="./vasp_calc", spin_component="z", outname="spin_z.png")

# 3. Supercell unfolding
run_unfold(dirname="./vasp_calc", supercell_matrix="2,0,0,0,2,0,0,0,1", outname="unfolded.png")
```
