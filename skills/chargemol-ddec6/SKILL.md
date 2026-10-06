---
name: chargemol-ddec6
description: Use when setting up, executing, or parsing Chargemol DDEC6 population analysis, net atomic charges, atomic spin moments, and atomic bond orders (ABO) from VASP all-electron charge densities (AECCAR0, AECCAR2, CHGCAR).
---

# ⚛️ Chargemol DDEC6 Population & Bond Order Analysis Skill

## Overview
Automates the preparation, charge density integration, and output post-processing for **Chargemol DDEC6** (Density Derived Electrostatic and Chemical charge partitioning, version 6). Calculates conformationally insensitive net atomic charges ($q_i$), atomic dipoles/quadrupoles, atomic spin moments, and quantitative atomic bond orders (ABO) from DFT all-electron charge densities.

---

## 🚀 Key Capabilities

1. **Automated `job_control.txt` Synthesis**:
   - Auto-configures boundary periodicity: 3D bulk ($x, y, z = \text{true}$) vs 2D slabs/monolayers ($x, y = \text{true}, z = \text{false}$).
   - Sets total net charge and paths to non-interacting spherical reference atomic densities.

2. **Native All-Electron Density Summation (`chgsum`)**:
   - High-throughput streaming summation of VASP core density (`AECCAR0`) and valence density (`AECCAR2`) into `CHGCAR_sum`.
   - Eliminates dependence on external unmaintained Perl scripts while preserving high numerical precision.

3. **VASP Pre-Flight Protocol**:
   To generate required inputs for Chargemol in VASP `INCAR`:
   ```ini
   LCHARG = .TRUE.
   LAECHG = .TRUE.   # Writes AECCAR0 (core) and AECCAR2 (valence)
   NSW = 0           # Static single-point calculation
   ```

4. **Structured Parsing & Property Extraction**:
   - Extracts net atomic charges, dipole vectors, and quadrupole tensors from `DDEC6_even_tempered_net_atomic_charges.xyz`.
   - Extracts pairwise bond orders and sum of bond orders (SBO) from `DDEC6_even_tempered_atomic_bond_orders.xyz`.
   - Exports clean JSON and formatted tabular summaries.

---

## ⚡ CLI Usage

```bash
# 1. Sum VASP all-electron densities (AECCAR0 + AECCAR2 -> CHGCAR_sum)
chargemol-ddec6 chgsum --aeccar0 AECCAR0 --aeccar2 AECCAR2 -o CHGCAR_sum

# 2. Generate job_control.txt for a 2D monolayer
chargemol-ddec6 setup --is-2d -i CHGCAR_sum -q 0.0

# 3. Parse Chargemol DDEC6 output charges and bond orders
chargemol-ddec6 parse -c DDEC6_even_tempered_net_atomic_charges.xyz -b DDEC6_even_tempered_atomic_bond_orders.xyz

# 4. Export structured JSON for downstream analysis
chargemol-ddec6 parse --json > charges_and_bonds.json
```

---

## 🐍 Python API Reference

```python
from skills.chargemol_ddec6.scripts.chargemol_ddec6 import (
    generate_job_control,
    sum_aeccar_files,
    parse_ddec6_charges,
    parse_bond_orders
)

# 1. Sum densities
sum_aeccar_files("AECCAR0", "AECCAR2", "CHGCAR_sum")

# 2. Write job_control.txt
generate_job_control(periodicity=(True, True, False), input_filename="CHGCAR_sum")

# 3. Parse output
results = parse_ddec6_charges("DDEC6_even_tempered_net_atomic_charges.xyz")
print("Total charge:", results["total_charge"])
```
