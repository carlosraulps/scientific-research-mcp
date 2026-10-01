#!/usr/bin/env python3
"""
================================================================================
VESTA Style & Project Generator (generate_vstd.py)
================================================================================
Solves the infamous 800-atom periodic boundary spillover bug in VESTA:
1. Automated Element Pair & Bond Detection: Inspects input POSCAR, CONTCAR, CIF,
   or XSF and extracts chemical species to generate comprehensive SBOND rules.
2. Strict Boundary Containment ('Bound = 0', 'SEARCH_BOUNDARY 0'):
   Eliminates duplicate ghost atoms reaching across cell boundaries.
3. Dual Isosurface CDD Automation: Standardizes 3D Charge Density Difference
   visualization with accumulation (Gold/Yellow #f1c40f) and depletion
   (Cyan/Sky Blue #00b4d8) at calibrated 60% opacity (alpha=0.60).
4. Dual Format Output: Emits standalone .vstd style files (for VESTA -style)
   or complete .vesta project wrappers.
================================================================================
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Standard covalent radius lookup (in Angstroms) for automatic cutoff estimation
COVALENT_RADII = {
    "H": 0.31, "He": 0.28, "Li": 1.28, "Be": 0.96, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66,
    "F": 0.57, "Ne": 0.58, "Na": 1.66, "Mg": 1.41, "Al": 1.21, "Si": 1.11, "P": 1.07, "S": 1.05,
    "Cl": 1.02, "Ar": 1.06, "K": 2.03, "Ca": 1.76, "Sc": 1.70, "Ti": 1.60, "V": 1.53, "Cr": 1.39,
    "Mn": 1.39, "Fe": 1.32, "Co": 1.26, "Ni": 1.24, "Cu": 1.32, "Zn": 1.22, "Ga": 1.22, "Ge": 1.20,
    "As": 1.19, "Se": 1.20, "Br": 1.20, "Kr": 1.16, "Rb": 2.20, "Sr": 1.95, "Y": 1.90, "Zr": 1.75,
    "Nb": 1.64, "Mo": 1.54, "Tc": 1.47, "Ru": 1.46, "Rh": 1.42, "Pd": 1.39, "Ag": 1.45, "Cd": 1.44,
    "In": 1.42, "Sn": 1.39, "Sb": 1.39, "Te": 1.38, "I": 1.39, "Xe": 1.40, "Cs": 2.44, "Ba": 2.15,
    "Pt": 1.36, "Au": 1.36, "Pb": 1.46, "Bi": 1.48
}

# Standard VESTA Element RGB colors (matched from elements.ini)
ELEMENT_COLORS = {
    "H": (255, 255, 255), "C": (144, 144, 144), "N": (48, 80, 248), "O": (255, 13, 13),
    "F": (144, 224, 80), "P": (255, 128, 0), "S": (255, 255, 48), "Cl": (31, 240, 31),
    "Fe": (224, 102, 51), "Co": (0, 102, 255), "Ni": (80, 208, 80), "Cr": (138, 153, 199),
    "Pt": (208, 208, 224), "Au": (255, 209, 35), "Cu": (200, 115, 51), "Mo": (84, 181, 181),
}

# Standard Crystallographic Orientation Matrices (LMATRIX in VESTA format)
ORIENTATION_MATRICES = {
    "c": [
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
    "a": [
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
    "b": [
        " 0.000000  0.000000  1.000000  0.000000",
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
    "iso": [
        " 0.707107 -0.408248  0.577350  0.000000",
        " 0.707107  0.408248 -0.577350  0.000000",
        " 0.000000  0.816497  0.577350  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
}


def extract_species_from_structure(file_path: Path) -> List[str]:
    """
    Extracts unique chemical elements from POSCAR, CONTCAR, CIF, or XSF file.
    """
    elements = []
    try:
        from ase.io import read as ase_read
        atoms = ase_read(str(file_path))
        for sym in atoms.get_chemical_symbols():
            if sym not in elements:
                elements.append(sym)
        return elements
    except Exception:
        pass

    # Fallback POSCAR parser
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip()]
        if len(lines) >= 6:
            line5 = lines[5].split()
            if not line5[0].isdigit():
                return line5
            # VASP 4 format: check comment
            first_line = lines[0].split()
            return [x for x in first_line if x.isalpha()]
    except Exception:
        pass

    return ["C", "H"]


def estimate_bond_cutoffs(e1: str, e2: str) -> float:
    """
    Calculates physically realistic bond cutoff: (r1 + r2) * 1.25.
    Special overrides for 2D carbon lattices (e.g. C-C = 1.70 A).
    """
    if {e1, e2} == {"C"}:
        return 1.70  # Captures up to 1.52 A, avoids diagonal 5/6/8-ring artifacts
    if {e1, e2} == {"C", "H"}:
        return 1.25
    if {e1, e2} == {"N", "C"}:
        return 1.65
    if {e1, e2} == {"O", "C"}:
        return 1.60
    r1 = COVALENT_RADII.get(e1, 1.20)
    r2 = COVALENT_RADII.get(e2, 1.20)
    return round((r1 + r2) * 1.25, 2)


def build_sbond_section(
    species: List[str],
    bound_mode: int = 0,
    search_boundary: int = 0,
    max_cutoff_override: Optional[float] = None,
) -> str:
    """
    Generates the SBOND block with strict Bound = 0 and SEARCH_BOUNDARY = 0.
    Format:
    SBOND
      idx  e1  e2  d_min  d_max  flag  bound_mode  search_boundary  poly  color ...
    """
    lines = ["SBOND"]
    idx = 1
    # Generate all pairs (including self-pairs)
    for i, e1 in enumerate(species):
        for e2 in species[i:]:
            d_max = max_cutoff_override or estimate_bond_cutoffs(e1, e2)
            # Bound = 0 -> "Do not search atoms beyond boundary"
            # Search = 0 -> "Do not search boundary"
            lines.append(
                f"  {idx:<3} {e1:<4} {e2:<4}  0.00000  {d_max:7.5f}  0  {bound_mode}  {search_boundary}  0  1  0.250  2.000 127 127 127"
            )
            idx += 1
    lines.append("  0 0 0 0")
    return "\n".join(lines)


def build_cdd_isosurface_section(
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    pos_color: Tuple[int, int, int] = (241, 196, 15),    # Gold / Yellow (#f1c40f)
    neg_color: Tuple[int, int, int] = (0, 180, 216),    # Cyan / Sky Blue (#00b4d8)
    opacity: float = 0.60,                              # 60% standard opacity
) -> str:
    """
    Constructs ISURF and SURFC blocks for dual positive/negative Charge Density Difference (CDD).
    """
    alpha_byte = int(opacity * 255)
    lines = [
        "ISURF",
        f"  1  {pos_level:10.6f}  1",
        f"  2  {neg_level:10.6f}  1",
        "  0",
        "SURFC",
        f"  1  {pos_color[0]:3} {pos_color[1]:3} {pos_color[2]:3}  {alpha_byte:3}  0",
        f"  2  {neg_color[0]:3} {neg_color[1]:3} {neg_color[2]:3}  {alpha_byte:3}  0",
        "  0",
    ]
    return "\n".join(lines)


def generate_vstd_content(
    species: List[str],
    bound_mode: int = 0,
    search_boundary: int = 0,
    cdd_mode: bool = False,
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    opacity: float = 0.60,
) -> str:
    """
    Creates a clean .vstd style configuration.
    """
    sections = [
        "# VESTA Style Definition File (auto-generated)",
        "# Enforces strict primitive cell boundary containment: Bound = 0, SEARCH_BOUNDARY = 0",
        "",
        build_sbond_section(species, bound_mode, search_boundary),
    ]
    if cdd_mode:
        sections.append("")
        sections.append(build_cdd_isosurface_section(pos_level, neg_level, opacity=opacity))
    return "\n".join(sections) + "\n"


def generate_vesta_project_content(
    data_file_path: Path,
    species: List[str],
    view: str = "c",
    bound_mode: int = 0,
    search_boundary: int = 0,
    cdd_mode: bool = False,
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    opacity: float = 0.60,
    title: Optional[str] = None,
) -> str:
    """
    Creates an authentic, lightweight .vesta project file referencing an external structure/grid file.
    """
    proj_title = title or data_file_path.stem
    matrix_lines = ORIENTATION_MATRICES.get(view, ORIENTATION_MATRICES["c"])

    sections = [
        "#VESTA_FORMAT_VERSION 3.5.0",
        "",
        "TITLE",
        f"{proj_title}",
        "",
        "IMPORT_STRUCTURE",
        f"{data_file_path.name}",
        "",
        "LMATRIX",
        "\n".join(matrix_lines),
        "",
        build_sbond_section(species, bound_mode, search_boundary),
        "",
        "BOUND",
        "  0.000000  1.000000  0.000000  1.000000  0.000000  1.000000",
        "  0  0  0  0",
        "",
        "STYLE",
        "MODEL  1",        # Ball and stick
        "SURF   1",        # Smooth surface shading
        "SECT   0",
        "",
    ]

    if cdd_mode:
        sections.append(build_cdd_isosurface_section(pos_level, neg_level, opacity=opacity))
        sections.append("")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(
        description="Generate VESTA .vstd style files or .vesta project wrappers with Bound=0"
    )
    parser.add_argument("input", help="Input structure file (POSCAR, CONTCAR, CIF, cdd.vasp, CHGCAR)")
    parser.add_argument("-o", "--output", help="Output .vstd or .vesta file path")
    parser.add_argument("-v", "--view", choices=["a", "b", "c", "iso"], default="c", help="Orientation matrix (for .vesta)")
    parser.add_argument("--format", choices=["vstd", "vesta", "auto"], default="auto", help="Output format")
    parser.add_argument("--bound", type=int, default=0, choices=[0, 1, 2], help="Bound mode: 0=isolate cell, 2=recursive periodic search")
    parser.add_argument("--search-boundary", type=int, default=0, choices=[0, 1], help="Search boundary mode")
    parser.add_argument("--cdd", action="store_true", help="Enable Charge Density Difference (CDD) dual isosurfaces")
    parser.add_argument("--pos-level", type=float, default=0.005, help="Positive CDD cutoff (accumulation, gold)")
    parser.add_argument("--neg-level", type=float, default=-0.005, help="Negative CDD cutoff (depletion, cyan)")
    parser.add_argument("--opacity", type=float, default=0.60, help="Isosurface opacity (0.0 - 1.0, default 0.60)")
    parser.add_argument("--species", nargs="+", help="Explicit chemical species list (overrides auto-detection)")
    parser.add_argument("--bond-cutoff", type=float, help="Universal bond cutoff override in Angstroms")

    args = parser.parse_args()
    in_path = Path(args.input).resolve()
    if not in_path.exists():
        print(f"Error: Input file does not exist: {in_path}", file=sys.stderr)
        sys.exit(1)

    # Determine species
    species = args.species or extract_species_from_structure(in_path)
    print(f"[vstd-gen] Detected species in {in_path.name}: {', '.join(species)}")

    # Determine format
    out_format = args.format
    if out_format == "auto":
        if args.output:
            out_format = "vstd" if args.output.endswith(".vstd") else "vesta"
        else:
            out_format = "vesta"

    out_file = args.output
    if not out_file:
        out_file = in_path.parent / f"{in_path.stem}.{out_format}"
    else:
        out_file = Path(out_file).resolve()

    if out_format == "vstd":
        content = generate_vstd_content(
            species=species,
            bound_mode=args.bound,
            search_boundary=args.search_boundary,
            cdd_mode=args.cdd,
            pos_level=args.pos_level,
            neg_level=args.neg_level,
            opacity=args.opacity,
        )
    else:
        content = generate_vesta_project_content(
            data_file_path=in_path,
            species=species,
            view=args.view,
            bound_mode=args.bound,
            search_boundary=args.search_boundary,
            cdd_mode=args.cdd,
            pos_level=args.pos_level,
            neg_level=args.neg_level,
            opacity=args.opacity,
        )

    out_file.write_text(content, encoding="utf-8")
    print(f"✅ Generated {out_format.upper()} configuration: {out_file}")


if __name__ == "__main__":
    main()
