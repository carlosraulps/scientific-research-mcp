# TritonDFT: Historical Memory & Symmetry-First Retrieval
**Reference**: Z. Hu et al., *TritonDFT: Automating DFT with a Multi-Agent Framework*, arXiv:2603.03372v2 (2026).

---

## 1. Core Architecture & Scientific Problem
Configuring Density Functional Theory calculations from scratch requires selecting two distinct parameter spaces:
1. **Physical Parameters ($\theta_{phy}$)**: k-points grid, plane-wave cutoff energy ($E_{cut}$), smearing scheme, exchange-correlation functional, pseudopotential/PAW choices, convergence thresholds ($10^{-6}$ eV).
2. **Computational HPC Parameters ($\theta_{hpc}$)**: Core counts, node geometry, parallelization bands/plane-waves (`KPAR`, `NCORE`), walltime limits, memory allocation.

Starting every new material from unoptimized default values leads to wasted CPU hours, non-convergence, or excessive over-sampling.

---

## 2. Historical Memory Mechanism
TritonDFT records all successfully converged calculations in a structured memory store. When a new material calculation is requested, parameters are inferred via a two-stage retrieval:

```
[ New Structure Query ]
          │
          ▼
┌───────────────────────────────────────────────┐
│ Stage 1: Symmetry-First Structured Filtering │
│ - Space Group (e.g., Fm-3m, Pnma, P6_3/mmc)   │
│ - Crystal System (Cubic, Tetragonal, Hex...)  │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Stage 2: Composition & Feature Ranking        │
│ - Elemental family / transition metal presence│
│ - Total valence electron count                │
│ - Primitive unit-cell volume (Å³)             │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│ Output: Recommended Parameter Presets         │
│ - Recommended θ_phy (kpoints, encut, smearing)│
│ - Recommended θ_hpc (cores, nodes, kpar, ncore│
└───────────────────────────────────────────────┘
```

---

## 3. Pareto Accuracy-Cost Trade-Off Tiers
Historical memory organizes recommendations across 3 standardized accuracy tiers:

| Tier | Energy Tolerance ($\Delta E$) | Target Use Case | Computational Cost |
| :--- | :--- | :--- | :--- |
| **High-Precision Tier** | $\Delta E < 1\text{ meV/atom}$ | Defect energetics, subtle phase transitions, phonon spectra, adsorption energy differences | High (tight k-mesh, high cutoff) |
| **Standard Tier** | $\Delta E < 10\text{ meV/atom}$ | High-throughput screening, equilibrium lattice constants, band structure overview | Moderate (balanced parameters) |
| **Coarse Tier** | $\Delta E < 20\text{ meV/atom}$ | Initial geometric pre-relaxation, exploratory candidate filtering | Low (coarse k-mesh, minimal cutoff) |
