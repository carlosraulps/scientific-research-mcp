---
name: avogadro-automation
description: Use when building, modifying, or converting 3D molecular structures (SMILES, PDB, MOL2, SDF, XYZ, POSCAR), performing force-field geometry optimization (UFF, MMFF94), grafting adsorbates onto periodic slabs, or launching Avogadro 2 GUI/headless sessions.
---

# 🧬 Avogadro 2 & OpenBabel Molecular Modeling Skill

## Overview
Automates **Avogadro 2** (v2.0.0 AppImage) and **OpenBabel** (v3.1) for molecular generation, force-field geometry optimization, coordinate format transformations, adsorbate grafting on periodic substrates, and interactive GUI inspection.

---

## 🚀 Key Capabilities

1. **3D Molecular Coordinate Synthesis from SMILES**:
   - Converts 1D SMILES / InChI representations into 3D Cartesian coordinates.
   - Automatically adds hydrogens and builds realistic valence geometry.
   - Minimizes conformational energy using MMFF94, UFF, or GAFF force fields.

2. **Heterogeneous Adsorbate Grafting Protocol**:
   - Automatically attaches molecules onto specific catalytic or crystal surface sites.
   - Aligns the adsorbate along the surface normal vector ($+z$ direction).
   - Enforces adjustable adsorption clearance distances ($d \approx 1.8 - 2.5\text{ \AA}$) and outputs valid VASP `POSCAR` formats.

3. **Multi-Format Interoperability**:
   - Bi-directional translation across quantum chemistry (ORCA, Gaussian, Q-Chem, Turbomole) and solid-state formats (POSCAR, CIF, XYZ, PDB, MOL2, SDF).

4. **Avogadro 2 Desktop & Virtual Desktop Control**:
   - Launches interactive desktop visualization sessions for manual inspection.
   - Supports off-screen headless rendering via `xvfb-run` on remote HPC nodes.

---

## ⚡ CLI Usage

```bash
# 1. Generate 3D optimized coordinates from SMILES string
avogadro-runner build "CC(=O)O" -o acetic_acid.xyz --ff mmff94

# 2. Convert format (e.g. CIF to XYZ or PDB to POSCAR)
avogadro-runner convert structure.cif structure.xyz

# 3. Graft an adsorbate molecule on a 2D slab site (atom index 0, height 2.1 Angstroms)
avogadro-runner graft --slab POSCAR_slab --molecule water.xyz --site 0 --distance 2.1 -o GRAFTED_POSCAR

# 4. Launch interactive Avogadro 2 window
avogadro-runner gui molecule.xyz
```

---

## 🐍 Python API Reference

```python
from skills.avogadro_automation.scripts.avogadro_runner import (
    build_molecule_from_smiles,
    convert_format,
    graft_molecule_on_slab,
    launch_avogadro
)

# 1. Synthesize molecule
xyz_file = build_molecule_from_smiles("C1=CC=CC=C1", "benzene.xyz", forcefield="mmff94")

# 2. Graft on catalytic substrate
poscar = graft_molecule_on_slab(
    slab_poscar="POSCAR",
    mol_file="benzene.xyz",
    site_index=12,
    distance=2.2,
    output_poscar="BENZENE_ON_SLAB.vasp"
)
```
