#!/usr/bin/env python3
"""
================================================================================
VESTA Project & Style (.vesta / .vstd) Generator
================================================================================
Generates programmatic VESTA project files with:
1. Strict boundary containment ('Bound = 0') preventing periodic 800-atom spillover.
2. Standardized crystallographic orientation matrices (LMATRIX for a, b, c, iso).
3. Dual-isosurface definitions for Charge Density Difference (CDD) calculations
   (e.g., accumulation yellow/gold, depletion cyan/blue, opacity control).
================================================================================
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


# Standard Crystallographic Orientation Matrices (LMATRIX in VESTA format)
# Formatted as 4 rows of 4 floats, plus scaling parameters
ORIENTATION_MATRICES = {
    # View along c-axis (looking down onto xy plane, a-horizontal, b-vertical)
    "c": [
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
    # View along a-axis (looking down onto yz plane, b-horizontal, c-vertical)
    "a": [
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000",
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
    # View along b-axis (looking down onto xz plane, c-horizontal, a-vertical)
    "b": [
        " 0.000000  0.000000  1.000000  0.000000",
        " 1.000000  0.000000  0.000000  0.000000",
        " 0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
    # Isometric 3D perspective
    "iso": [
        " 0.707107 -0.408248  0.577350  0.000000",
        " 0.707107  0.408248 -0.577350  0.000000",
        " 0.000000  0.816497  0.577350  0.000000",
        " 0.000000  0.000000  0.000000  1.000000",
        " 0.000000  0.000000  0.000000",
    ],
}


def build_sbond_block(
    element_pairs: Optional[List[Tuple[str, str, float, float]]] = None,
    bound_mode: int = 0,
) -> str:
    """
    Builds the SBOND section for VESTA.
    Token 7 ('Bound') controls periodic boundary expansion:
      0 = Do not search atoms beyond the boundary (ELIMINATES 800-ATOM BUG).
      1 = Search atoms beyond boundary.
      2 = Recursive search across periodic boundaries.
    """
    default_pairs = [
        ("C", "C", 0.0, 1.85),
        ("C", "H", 0.0, 1.25),
        ("N", "C", 0.0, 1.70),
        ("O", "C", 0.0, 1.60),
        ("H", "O", 0.0, 1.15),
        ("Pt", "Pt", 0.0, 3.10),
        ("Pt", "H", 0.0, 2.00),
        ("Fe", "Cl", 0.0, 2.60),
        ("Co", "Cl", 0.0, 2.60),
        ("Ni", "Cl", 0.0, 2.60),
        ("Cr", "Cl", 0.0, 2.60),
        ("Mo", "S", 0.0, 2.65),
    ]
    pairs = element_pairs if element_pairs else default_pairs

    lines = ["SBOND"]
    for idx, (e1, e2, d_min, d_max) in enumerate(pairs, start=1):
        # Format: ID Elem1 Elem2 Min_Dist Max_Dist Flag Bound Search Poly Color ...
        lines.append(
            f"  {idx:<3} {e1:<4} {e2:<4} {d_min:8.5f} {d_max:8.5f}  0  {bound_mode}  1  0  1  0.250  2.000 127 127 127"
        )
    lines.append("  0 0 0 0")
    return "\n".join(lines)


def build_cdd_isosurface_block(
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    pos_color: Tuple[int, int, int] = (255, 200, 0),     # Yellow / Gold
    neg_color: Tuple[int, int, int] = (0, 180, 255),     # Cyan / Sky Blue
    opacity: float = 0.75,
) -> str:
    """
    Builds the ISURF and SURFC blocks for dual positive/negative isosurface rendering
    of Charge Density Difference (CDD) data.
    """
    lines = [
        "ISURF",
        f"  1  {pos_level:10.6f}  1",
        f"  2  {neg_level:10.6f}  1",
        "  0",
        "SURFC",
        f"  1  {pos_color[0]:3} {pos_color[1]:3} {pos_color[2]:3}  {int(opacity * 255):3}  0",
        f"  2  {neg_color[0]:3} {neg_color[1]:3} {neg_color[2]:3}  {int(opacity * 255):3}  0",
        "  0",
    ]
    return "\n".join(lines)


def generate_vesta_project(
    data_file: Union[str, Path],
    output_vesta_path: Union[str, Path],
    view: str = "c",
    bound_mode: int = 0,
    cdd_mode: bool = False,
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    boundary_range: Tuple[float, float, float, float, float, float] = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0),
    title: Optional[str] = None,
) -> Path:
    """
    Creates an authentic, lightweight .vesta project wrapper that references
    an input geometry or volumetric dataset.
    
    Args:
        data_file: Path to underlying structure (.vasp, POSCAR, .cif) or volumetric file (.cube, CHGCAR, cdd.vasp).
        output_vesta_path: Destination .vesta project file.
        view: Crystallographic orientation ('a', 'b', 'c', or 'iso').
        bound_mode: 0 = strictly isolate primitive unit cell (no boundary search), 1 = search beyond.
        cdd_mode: If True, adds dual-surface accumulation/depletion isosurfaces.
        pos_level: Positive CDD isosurface level.
        neg_level: Negative CDD isosurface level.
        boundary_range: (xmin, xmax, ymin, ymax, zmin, zmax) unit cell bounds.
        title: Project title.
    """
    data_path = Path(data_file).resolve()
    out_path = Path(output_vesta_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    proj_title = title or data_path.stem
    v = view.lower() if view.lower() in ORIENTATION_MATRICES else "c"
    matrix_lines = ORIENTATION_MATRICES[v]

    x0, x1, y0, y1, z0, z1 = boundary_range

    content = [
        "#VESTA_FORMAT_VERSION 3.5.4",
        "",
        "CRYSTAL",
        "",
        "TITLE",
        f"{proj_title}",
        "",
        "IMPORT_STRUCTURE",
        f"{data_path}",
        "",
        "LORIENT",
        "-1   0   0   0   0",
        " 1.000000  0.000000  0.000000  1.000000  0.000000  0.000000",
        " 0.000000  0.000000  1.000000  0.000000  0.000000  1.000000",
        "LMATRIX",
        *matrix_lines,
        "",
        "BOUND",
        f"{x0:.4f} {x1:.4f} {y0:.4f} {y1:.4f} {z0:.4f} {z1:.4f}",
        "  0   0   0   0  0",
        "",
        "QCORIG",
        "        0         0         0",
        "",
        build_sbond_block(bound_mode=bound_mode),
        "",
    ]

    if cdd_mode:
        content.append(build_cdd_isosurface_block(pos_level=pos_level, neg_level=neg_level))
        content.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content) + "\n")

    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate VESTA project files with strict boundary control.")
    parser.add_argument("input", help="Path to input crystal or volumetric data file")
    parser.add_argument("--output", "-o", required=True, help="Destination .vesta file")
    parser.add_argument("--view", "-v", choices=["a", "b", "c", "iso"], default="c", help="Orientation view")
    parser.add_argument("--bound", type=int, default=0, help="Boundary mode (0=contain within unit cell, default: 0)")
    parser.add_argument("--cdd", action="store_true", help="Include dual CDD isosurfaces")
    parser.add_argument("--pos-level", type=float, default=0.005, help="Positive isosurface cutoff")
    parser.add_argument("--neg-level", type=float, default=-0.005, help="Negative isosurface cutoff")
    args = parser.parse_args()

    out = generate_vesta_project(
        data_file=args.input,
        output_vesta_path=args.output,
        view=args.view,
        bound_mode=args.bound,
        cdd_mode=args.cdd,
        pos_level=args.pos_level,
        neg_level=args.neg_level,
    )
    print(f"[+] Successfully generated VESTA project: {out}")
