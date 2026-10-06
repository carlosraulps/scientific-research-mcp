# 🔮 Computational Science Skills Roadmap: Future Architecture & Extensions

> **Document Status**: Living Architectural Roadmap  
> **Repository**: `/home/cr/simulations/scientific-research`  
> **Framework Compatibility**: DREAMS, TRITONDFT, MDCrow, MDAgent, Rosetta  
> **Target System**: Antigravity CLI / Gemini Multi-Agent System (`sciresearch`)

---

## 📌 Executive Summary

This roadmap establishes the technical specifications, architectural designs, input/output data contracts, and integration milestones for computational science and quantum chemistry skills deferred from active sprints or slated for future implementation.

Skills are organized into:
1. **Deferred Sprint Candidates** (Explicitly held per user instructions):
   - **Skill 5**: `lobster-cohp-bonding` (Crystal Orbital Hamilton Populations & Chemical Bonding)
   - **Skill 8**: `boltztrap2-transport` (Semiclassical Thermoelectric & Electronic Transport)
2. **Next-Generation Frontier Skills**:
   - **Skill 9**: `wannier90-berri-topological` (Berry Curvature & Anomalous Transport)
   - **Skill 10**: `phonopy-vibrational-thermo` (Harmonic Phonon Dispersions & Free Energy)
   - **Skill 11**: `phono3py-anharmonic-lattice-thermal` (Lattice Thermal Conductivity $\kappa_{\mathrm{ph}}$)
   - **Skill 12**: `vasp-vtst-reaction-kinetics` (CI-NEB, Saddle Points & Catalytic Kinetics)
   - **Skill 13**: `ai-ml-interatomic-potentials` (Universal MLIPs: MACE, CHGNet, SevenNet)
   - **Skill 14**: `multireference-openmolcas-caspt2` (CASSCF/CASPT2 Multi-Reference Chemistry)
   - **Skill 15**: `superconducting-migdal-eliashberg` (Electron-Phonon Coupling & $T_c$)

---

## 1. Deferred Sprint Candidates

### 1.1 Skill 5: `lobster-cohp-bonding`
- **Core Domain**: Quantum Chemical Bonding Analysis in Periodic Solids
- **Underlying Engine**: LOBSTER (Local Orbital Basis Suite Towards Electronic-Structure Reconstruction) v5.1.0+
- **Physical Formulation**:
  Projects delocalized Kohn-Sham Bloch wavefunctions $|\psi_{n\mathbf{k}}\rangle$ from plane-wave DFT onto localized atom-centered basis sets (Bunge/Slater-type orbitals):
  $$\mathrm{COHP}_{ij}(E) = -\sum_{n\mathbf{k}} w_\mathbf{k} H_{i\mathbf{k}, j\mathbf{k}} \operatorname{Re}\left[c_{in\mathbf{k}}^* c_{jn\mathbf{k}}\right] \delta(E - \varepsilon_{n\mathbf{k}})$$
  Where $H_{i\mathbf{k}, j\mathbf{k}}$ is the Hamiltonian matrix element and $c_{in\mathbf{k}}$ are expansion coefficients.
- **Key Descriptors Computed**:
  - **-COHP($E$)**: Crystal Orbital Hamilton Population (positive = bonding, negative = antibonding).
  - **ICOHP**: Integrated Crystal Orbital Hamilton Population up to $E_{\text{F}}$ (correlates with covalent bond strength).
  - **COOP / COBI**: Crystal Orbital Overlap / Bond Index.
  - **Mulliken / Löwdin Net Atomic Charges**.
- **Required DFT Pre-Flight Protocol**:
  ```ini
  # INCAR modifications for VASP + LOBSTER
  ISYM = -1               # Symmetry must be turned off for unconstrained projection
  NSW = 0                 # Static SCF calculation
  LWAVE = .TRUE.          # Essential: writes WAVECAR with plane-wave coefficients
  NBANDS = <computed>     # Must exceed sum of basis functions from lobsterin
  ```
- **Execution & Analysis Pipeline**:
  1. Auto-generate `lobsterin` by inspecting POSCAR and choosing optimal basis sets (`pbeVaspFit2015`).
  2. Execute `lobster` binary headlessly.
  3. Extract pairwise ICOHP values from `ICOHPLIST.lobster` and identify dominant bonding interactions.
  4. Render publication-grade multi-panel -COHP plots ($E - E_{\text{F}}$ on vertical axis, inverted convention where bonding is right/positive).

---

### 1.2 Skill 8: `boltztrap2-transport`
- **Core Domain**: Semiclassical Electronic & Thermoelectric Transport Properties
- **Underlying Engine**: BoltzTraP2 (Boltzmann Transport Properties 2)
- **Physical Formulation**:
  Solves the linearized Boltzmann transport equation under the Constant Relaxation Time Approximation (CRTA) and Rigid Band Approximation (RBA):
  $$\sigma_{\alpha\beta}(T, \mu) = \frac{1}{\Omega} \int \Sigma_{\alpha\beta}(E) \left(-\frac{\partial f_0}{\partial E}\right) dE$$
  $$S_{\alpha\beta}(T, \mu) = \frac{1}{e T \Omega \sigma_{\alpha\beta}} \int \Sigma_{\alpha\beta}(E) (E - \mu) \left(-\frac{\partial f_0}{\partial E}\right) dE$$
  Where $\Sigma_{\alpha\beta}(E) = e^2 \sum_n \int \frac{d\mathbf{k}}{8\pi^3} v_{n\alpha}(\mathbf{k}) v_{n\beta}(\mathbf{k}) \tau_{n\mathbf{k}} \delta(E - E_n(\mathbf{k}))$ is the transport distribution tensor.
- **Key Descriptors Computed**:
  - Seebeck coefficient $S(T, \mu)$ ($\mu\mathrm{V/K}$)
  - Electrical conductivity tensor $\sigma/\tau$ ($\Omega^{-1}\mathrm{m}^{-1}\mathrm{s}^{-1}$)
  - Electronic thermal conductivity $\kappa_0/\tau$ ($\mathrm{W}\cdot\mathrm{m}^{-1}\mathrm{K}^{-1}\mathrm{s}^{-1}$)
  - Power Factor $\mathrm{PF}/\tau = S^2 \sigma / \tau$
  - Hall coefficient $R_{\mathrm{H}}$ and carrier concentration-dependent figures of merit $zT$
- **Required DFT Pre-Flight Protocol**:
  - Extremely dense uniform $k$-mesh ($N_k \ge 30 \times 30 \times 30$ for 3D bulk, or high $k$-density $\ge 50\text{ \AA}^{-1}$).
  - Static SCF calculation generating high-precision `vasprun.xml` or `EIGENVAL`.
- **Planned Tooling**:
  - `bt2_interpolate`: B-spline smoothed Fourier interpolation of DFT band energies.
  - `bt2_transport`: Slices across chemical potential $\mu \in [-2, +2]\text{ eV}$ and temperature $T \in [100, 1000]\text{ K}$.
  - Heatmap generation for optimum doping concentration ($n$-type vs $p$-type).

---

## 2. Next-Generation Computational Skills

### 2.1 Skill 9: `wannier90-berri-topological`
- **Domain**: Maximally Localized Wannier Functions (MLWFs), Berry Curvature, and Anomalous Transport.
- **Workflow**:
  - Interface VASP `LWANNIER90 = .TRUE.` with `Wannier90` v3.1+.
  - Automated initial projections selection (using atom-centered orbitals or selected bands).
  - Band disentanglement and spread minimization ($\Omega = \Omega_{\mathrm{I}} + \widetilde{\Omega}$).
  - WannierBerri post-processing: Berry curvature vector fields $\mathbf{\Omega}(\mathbf{k})$, Anomalous Hall Conductivity (AHC) $\sigma_{xy}$, Spin Hall Conductivity (SHC), and Anomalous Nernst effect.
  - Surface green function calculations for Fermi arc surface states via `WannierTools`.

### 2.2 Skill 10: `phonopy-vibrational-thermo`
- **Domain**: Harmonic Lattice Dynamics, Phonon Dispersions, and Thermodynamic Functions.
- **Workflow**:
  - Supercell generation ($2\times2\times2$, $3\times3\times3$) with finite atomic displacements ($0.01\text{ \AA}$).
  - VASP force evaluation (`NSW=0`, high energy precision `EDIFF = 1E-8`).
  - Force constant matrix calculation and acoustic sum rule (ASR) symmetry enforcement.
  - Phonon dispersion curves along SeeK-path high-symmetry routes, identifying imaginary frequencies (dynamic instability).
  - Vibrational partition function integration: Free energy $F(T)$, Entropy $S(T)$, and constant-volume heat capacity $C_v(T)$.

### 2.3 Skill 11: `phono3py-anharmonic-lattice-thermal`
- **Domain**: Anharmonic Lattice Dynamics and Phonon Thermal Conductivity ($\kappa_{\mathrm{ph}}$).
- **Workflow**:
  - Generation of 3rd-order force constant displacement supercells.
  - Evaluation of 3-phonon scattering matrix elements and relaxation times $\tau_\lambda$.
  - Solution of the linearized phonon Boltzmann transport equation (RTA and self-consistent direct solver).
  - Directional lattice thermal conductivity tensor $\kappa_{xx}, \kappa_{yy}, \kappa_{zz}$ vs temperature ($10\text{ K} - 1200\text{ K}$).

### 2.4 Skill 12: `vasp-vtst-reaction-kinetics`
- **Domain**: Chemical Reaction Pathways, Transition State Theory, and Catalytic Kinetics.
- **Workflow**:
  - VTST linear/IDPP interpolation between reactant and product states (`nebmake.pl`).
  - Climbing-Image Nudged Elastic Band (CI-NEB) with variable spring constants.
  - Dimer method and Lanczos saddle-point searches.
  - Vibrational frequency calculation at saddle point (confirming exactly 1 imaginary frequency along reaction coordinate).
  - Harmonic transition state theory (hTST) barrier $\Delta G^\ddagger$ and Eyring reaction rate constant $k(T)$.

### 2.5 Skill 13: `ai-ml-interatomic-potentials`
- **Domain**: Foundation Machine Learning Interatomic Potentials (MLIPs).
- **Supported Architectures**: MACE (Higher-order equivariant message passing), CHGNet (Crystal Hamiltonian Graph Neural Network), SevenNet, and M3GNet.
- **Workflow**:
  - Zero-shot crystal relaxation of complex supercells ($>1000$ atoms) in seconds prior to DFT refinement.
  - High-throughput screening of defect migration barriers and finite-temperature molecular dynamics (ASE interface).
  - Automatic uncertainty quantification to detect out-of-distribution structures requiring DFT recalibration.

### 2.6 Skill 14: `multireference-openmolcas-caspt2`
- **Domain**: Strongly Correlated Molecular Systems & Non-Dynamical Electron Correlation.
- **Underlying Engine**: OpenMolcas / PySCF.
- **Workflow**:
  - Automated Active Space selection (AVAS / DMET) for transition metal complexes, open-shell diradicals, and actinide complexes.
  - Complete Active Space Self-Consistent Field (CASSCF) orbital optimization.
  - Multi-State Second-Order Perturbation Theory (MS-CASPT2 / NEVPT2) for dynamic correlation.
  - Spin-orbit coupling (RASSI-SO) and magnetic anisotropy parameters ($D, E$).

### 2.7 Skill 15: `superconducting-migdal-eliashberg`
- **Domain**: Phonon-Mediated Conventional Superconductivity.
- **Underlying Engine**: EPW (Electron-Phonon Wannier) / Quantum ESPRESSO.
- **Workflow**:
  - Electron-phonon matrix elements $g_{mn\nu}(\mathbf{k}, \mathbf{q})$ interpolated via Wannier functions.
  - Eliashberg spectral function calculation: $\alpha^2 F(\omega) = \frac{1}{2\pi N(\varepsilon_{\mathrm{F}})} \sum_{\mathbf{q}\nu} \frac{\gamma_{\mathbf{q}\nu}}{\omega_{\mathbf{q}\nu}} \delta(\omega - \omega_{\mathbf{q}\nu})$.
  - Total coupling constant $\lambda = 2 \int \frac{\alpha^2 F(\omega)}{\omega} d\omega$ and logarithmic average frequency $\omega_{\mathrm{log}}$.
  - Superconducting critical temperature $T_c$ via Allen-Dynes equation with Coulomb pseudopotential $\mu^* \in [0.10, 0.14]$.

---

## 3. Architecture & Dependency Matrix

| Skill ID | Skill Name | Primary Packages | HPC Requirements | Complexity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Skill 5** | `lobster-cohp-bonding` | LOBSTER, pymatgen | Single node (32 cores, 64 GB RAM) | Moderate | **Deferred (Roadmap)** |
| **Skill 8** | `boltztrap2-transport` | BoltzTraP2, spglib, scipy | 16–32 cores (high memory for dense k) | Moderate | **Deferred (Roadmap)** |
| **Skill 9** | `wannier90-berri-topological` | Wannier90, WannierBerri | 32–64 cores (MPI enabled) | High | Planned |
| **Skill 10** | `phonopy-vibrational-thermo` | phonopy, seekpath | Cluster batch (10–50 supercells) | High | Planned |
| **Skill 11** | `phono3py-anharmonic-lattice-thermal` | phono3py, OpenMP/MPI | Multi-node cluster (heavy 3rd order) | Very High | Planned |
| **Skill 12** | `vasp-vtst-reaction-kinetics` | VTST tools, ase | Multi-node (e.g. 8–16 images parallel) | High | Planned |
| **Skill 13** | `ai-ml-interatomic-potentials` | mace-torch, chgnet, ase | GPU node (CUDA / PyTorch) | Moderate | Planned |
| **Skill 14** | `multireference-openmolcas-caspt2` | OpenMolcas, PySCF | Large-memory node (>128 GB RAM) | Very High | Planned |
| **Skill 15** | `superconducting-migdal-eliashberg` | EPW, QE, Wannier90 | Massive MPI cluster (>128 cores) | Very High | Planned |

---

## 4. Lifelong Memory Integration

When any of the above skills are promoted to active implementation:
1. Initialize folder at `skills/<skill_name>/` with valid Antigravity YAML frontmatter in `SKILL.md`.
2. Provide verified Python CLI wrappers in `skills/<skill_name>/scripts/`.
3. Symlink into `~/.gemini/config/skills/<skill_name>` for global multi-agent discovery.
4. Record baseline convergence facts and failure traps into `facts_memory.db` via `sciresearch facts`.
5. Update AST knowledge graph using `graphify update .`.
