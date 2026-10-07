# VASPKIT Technical Reference & VASP INCAR Recipes

## 1. Input / Output File Mapping by Task

### A. Band Structure Calculations
- **Prerequisite VASP Run**:
  1. Standard SCF calculation (`ICHARG=2`, dense k-mesh).
  2. Non-SCF band calculation (`ICHARG=11`, `LORBIT=11`, line-mode `KPOINTS` from Task 102/103).
- **VASP Input/Output Files Required**:
  - `POSCAR` (structure)
  - `KPOINTS` (line-mode k-path)
  - `EIGENVAL` (eigenvalues at each k-point)
  - `PROCAR` (required for projected/fat bands, Task 212)
  - `OUTCAR` (Fermi energy $E_{\mathrm{F}}$ and reciprocal lattice)
- **VASPKIT Outputs**:
  - `BAND.dat`: 2-column or multi-column $(k, E - E_{\mathrm{F}})$ for each band curve.
  - `KLABELS`: High-symmetry points coordinates and labels along the path.
  - `BAND_GAP`: Summary file recording direct/indirect band gap and VBM/CBM values.
  - `PBAND_*.dat`: Orbital/element-projected fat band data.

---

### B. Density of States (DOS) Calculations
- **Prerequisite VASP Run**:
  - Static run with fine k-mesh, `LORBIT=11`, `NEDOS=2001`, `EMIN` and `EMAX` configured.
- **VASP Files Required**:
  - `DOSCAR`
  - `OUTCAR`
  - `POSCAR`
- **VASPKIT Outputs**:
  - `TDOS.dat`: Total DOS ($E - E_{\mathrm{F}}$, $\text{DOS}_{\mathrm{up}}$, $\text{DOS}_{\mathrm{down}}$).
  - `PDOS_<element>.dat`: Element-resolved projected DOS.
  - `PDOS_<element>_<orbital>.dat`: Orbital-resolved projected DOS ($s, p_x, p_y, p_z, d_{xy}, d_{yz}, d_{z^2}, d_{xz}, d_{x^2-y^2}$).

---

### C. Mechanical & Elastic Properties
- **Prerequisite VASP Run**:
  - Finite strain method (`ISIF=3`, `IBRION=6`, `NFREE=2`, `POTIM=0.015`).
- **VASP Files Required**:
  - `OUTCAR` containing the elastic stiffness tensor (`TOTAL ELASTIC MODULI (kBar)`).
  - `POSCAR`.
- **VASPKIT Outputs**:
  - `ELASTIC_TENSOR`: Parsed stiffness and compliance matrices.
  - 2D: $C_{11}, C_{22}, C_{12}, C_{66}\ (\mathrm{N/m})$, Young's modulus, Poisson's ratio, Born stability audit.
  - 3D: Voigt, Reuss, and VRH average bulk ($B$) and shear ($G$) moduli, Young's modulus ($E$), Poisson's ratio ($\nu$), Pugh ratio ($B/G$), Cauchy pressure.

---

### D. Work Function & Electrostatic Potential
- **Prerequisite VASP Run**:
  - Slab calculation with dipole correction (`LVTOT=.TRUE.`, `LVHAR=.TRUE.`, `LDIPOL=.TRUE.`, `IDIPOL=3`).
- **VASP Files Required**:
  - `LOCPOT` (local potential grid).
  - `OUTCAR` (for Fermi energy).
- **VASPKIT Outputs**:
  - `PLANAR_AVERAGE.dat`: $z$-coordinate vs. planar-averaged potential $\overline{V}(z)$.
  - Vacuum plateau identification ($V_{\mathrm{vac}}$) and work function $\Phi = V_{\mathrm{vac}} - E_{\mathrm{F}}$.

---

## 2. Recommended VASP INCAR Settings for VASPKIT Workflows

### Band Structure INCAR (Non-SCF step)
```ini
System   = Band Structure Calculation
ISTART   = 1
ICHARG   = 11
PREC     = Accurate
ENCUT    = 520
NELM     = 100
EDIFF    = 1E-7
ISMEAR   = 0
SIGMA    = 0.05
LORBIT   = 11
LREAL    = .FALSE.
LWAVE    = .FALSE.
LCHARG   = .FALSE.
```

### High-Resolution DOS INCAR
```ini
System   = High-Resolution DOS
ISTART   = 1
ICHARG   = 11
PREC     = Accurate
ENCUT    = 520
NEDOS    = 2001
ISMEAR   = -5          # Tetrahedron method with Bloechl corrections for semiconductors/insulators
# ISMEAR = 0, SIGMA = 0.03 for metals or 2D materials
LORBIT   = 11
```

### Elastic Constants INCAR (Finite Differences)
```ini
System   = Elastic Tensor Calculation
PREC     = Accurate
ENCUT    = 600         # High cutoff recommended for strain derivatives
EDIFF    = 1E-8
IBRION   = 6           # Finite differences with symmetry
ISIF     = 3           # Relax ions and calculate strain derivatives
NFREE    = 2
POTIM    = 0.015       # Strain step
ISMEAR   = 0
SIGMA    = 0.05
```
