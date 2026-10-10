---
title: "2D Carbon Explorer Crystallographic Architecture & Scalability Standard"
version: 1
created_at: "2026-10-10T02:54:17.917537+00:00"
tags: ["2D_carbon", "crystallography", "wallpaper_groups", "thermodynamics", "biphenylene"]
references: []
---

# 2D Carbon Explorer: Crystallographic Architecture & Database Scalability Standard

## 1. Structural Representation & Standardization
- **2D Wallpaper Symmetry**: Mapped 3D layer space groups (with c-axis vacuum >= 15 Å) to International 2D wallpaper groups (plane groups 1–17). Graphene ($h6_1$) maps to $p6mm$ (#17), Biphenylene ($r4^1_6^1_8^1$) maps to $pmm$ (#6), Phagraphene maps to $pmg$ (#7), and Cmmm Graphene maps to $cmm$ (#9).
- **Interactive Symmetry Overlay**: Projected onto 2D ball-and-stick lattice with rotation centers ($C_6, C_4, C_3, C_2$), mirror lines ($m$), and glide lines ($g$).
- **Multi-Cell CIF Generation**: Supported native exports of Primitive Standard, Conventional Standard, and 2×2 Supercell geometries with clean symmetry preservation using pymatgen `CifWriter`.

## 2. Thermodynamic Stability Anchoring
- **Ground-State Reference**: Anchored at pristine graphene ($h6_1$, $\Delta E = 0.000$ eV/atom).
- **Synthesis Benchmark**: Anchored at the experimentally synthesized biphenylene network ($\Delta E \approx 0.456$ eV/atom, Fan et al., Science 372, 852, 2021).
- **Regime Partitioning**: Structures with $\Delta E \le 0.456$ eV/atom fall in the synthetically feasible window, while those exceeding 0.456 eV/atom require kinetic trapping / bottom-up synthesis.

## 3. Database Scalability & Optimization
- **Catalog Schema**: Enriched with 2D wallpaper symbols, plane group numbers, point groups, in-plane symmetry elements, and offset vs biphenylene.
- **Client Performance**: In-memory caching with Flask-Caching, Plotly vector trace bundling (single C-C bond segment trace), and Times New Roman academic typography.
