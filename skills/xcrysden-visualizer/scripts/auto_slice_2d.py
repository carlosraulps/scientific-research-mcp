#!/usr/bin/env python3
"""
================================================================================
Automated 2D Plane Slicer & Contour Visualizer for XCrySDen & Electronic Datasets
================================================================================
Solves the manual plane-positioning problem in 2D materials and adsorption systems:
1. Basal Sheet Auto-Detection: Automatically detects the fractional z-plane of
   2D monolayers (graphene, PHOTH-graphene, TMDs, phosphorene).
2. Adatom / Active Site Plane Detection: Locates adsorbed atoms (H*, O*, OH*, metals)
   and computes the adatom z-height or bonding cross-section plane.
3. 3-Point Plane Calculation: Computes planar equations and fractional normal vectors
   passing through 3 selected atom indices (e.g. catalytic active site triad).
4. Direct Headless Execution: Emits ready-to-run TCL scripts or calls XCrySDen
   headlessly with automatic background whitening and margin auto-trimming.
================================================================================
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np

# Add current script directory for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from postprocess_image import invert_black_background
from xcrysden_auto import build_tcl_script, convert_to_xsf, run_xcrysden


def find_monolayer_z_plane(positions_frac: np.ndarray, species: List[str]) -> Tuple[float, float]:
    """
    Finds the mean fractional z-coordinate of the 2D material sheet and
    identifies any adsorbate adatom z-coordinates.
    """
    z_coords = positions_frac[:, 2]

    # Cluster z coordinates to separate monolayer from adsorbates
    # Typically 2D sheet atoms have very similar z
    hist, bin_edges = np.histogram(z_coords, bins=50)
    peak_idx = np.argmax(hist)
    sheet_z_center = (bin_edges[peak_idx] + bin_edges[peak_idx + 1]) / 2.0

    # Collect atoms within 0.15 fractional z of peak
    sheet_mask = np.abs(z_coords - sheet_z_center) < 0.10
    sheet_mean_z = float(np.mean(z_coords[sheet_mask]))

    # Adsorbate atoms
    adsorbate_mask = ~sheet_mask
    adsorbate_z = float(np.mean(z_coords[adsorbate_mask])) if np.any(adsorbate_mask) else sheet_mean_z

    return sheet_mean_z, adsorbate_z


def compute_3point_plane(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Computes normal vector and plane offset from 3 Cartesian points:
    n_x * x + n_y * y + n_z * z + d = 0
    """
    v1 = p2 - p1
    v2 = p3 - p1
    normal = np.cross(v1, v2)
    norm = np.linalg.norm(normal)
    if norm < 1e-6:
        raise ValueError("Selected 3 points are collinear; cannot define a unique plane.")
    normal = normal / norm
    d = -float(np.dot(normal, p1))
    return normal, d


def auto_slice_and_render(
    input_file: Union[str, Path],
    output_image: Optional[Union[str, Path]] = None,
    target: str = "sheet",  # 'sheet', 'adsorbate', or custom float pos
    plane: str = "xy",
    atom_indices: Optional[List[int]] = None,
    contours: int = 35,
    colormap: str = "bwr",
    white_bg: bool = True,
    width: int = 2400,
    height: int = 1800,
) -> Optional[str]:
    """
    Analyzes atomic geometry, calculates optimal fractional slice position,
    and headlessly renders the 2D contour slice.
    """
    in_path = Path(input_file).resolve()
    if not in_path.exists():
        print(f"Error: Input file does not exist: {in_path}", file=sys.stderr)
        return None

    # Load structure via ASE
    try:
        from ase.io import read as ase_read
        atoms = ase_read(str(in_path))
    except Exception as e:
        print(f"Error reading structure {in_path}: {e}", file=sys.stderr)
        return None

    pos_frac = atoms.get_scaled_positions()
    species = atoms.get_chemical_symbols()

    slice_pos = 0.50
    if target == "sheet":
        sheet_z, ads_z = find_monolayer_z_plane(pos_frac, species)
        slice_pos = sheet_z
        print(f"[AutoSlice] Detected 2D Monolayer basal plane at fractional z = {slice_pos:.4f}")
    elif target == "adsorbate":
        sheet_z, ads_z = find_monolayer_z_plane(pos_frac, species)
        slice_pos = ads_z
        print(f"[AutoSlice] Detected Adsorbate/Active Site plane at fractional z = {slice_pos:.4f}")
    else:
        try:
            slice_pos = float(target)
            print(f"[AutoSlice] Using user-specified slice position: {slice_pos:.4f}")
        except ValueError:
            slice_pos = 0.50

    out_img = Path(output_image).resolve() if output_image else in_path.parent / f"{in_path.stem}_slice_{plane}_{slice_pos:.2f}.png"

    res = run_xcrysden(
        input_file=in_path,
        output_image=out_img,
        view="c" if plane == "xy" else ("a" if plane == "yz" else "b"),
        slice_2d=True,
        slice_plane=plane,
        slice_pos=slice_pos,
        contours=contours,
        white_bg=white_bg,
        width=width,
        height=height,
    )
    return res


def main():
    parser = argparse.ArgumentParser(
        description="Automated 2D Plane Positioner & Contour Slicer for XCrySDen."
    )
    parser.add_argument("input", help="Path to input structure (.xsf, POSCAR, CIF, CHGCAR)")
    parser.add_argument("--output", "-o", help="Destination image path (default: <stem>_slice_<plane>.png)")
    parser.add_argument(
        "--target",
        "-t",
        default="sheet",
        help="Target slicing level: 'sheet' (monolayer basal plane), 'adsorbate' (adatom plane), or float value (default: sheet)",
    )
    parser.add_argument(
        "--plane",
        "-p",
        choices=["xy", "xz", "yz"],
        default="xy",
        help="Planar orientation (default: xy)",
    )
    parser.add_argument("--contours", "-c", type=int, default=35, help="Number of contour lines (default: 35)")
    parser.add_argument("--colormap", default="bwr", help="Colormap (default: bwr)")
    parser.add_argument("--no-white-bg", action="store_true", help="Preserve default black background")
    parser.add_argument("--width", type=int, default=2400, help="Image width (default: 2400)")
    parser.add_argument("--height", type=int, default=1800, help="Image height (default: 1800)")

    args = parser.parse_args()

    auto_slice_and_render(
        input_file=args.input,
        output_image=args.output,
        target=args.target,
        plane=args.plane,
        contours=args.contours,
        colormap=args.colormap,
        white_bg=not args.no_white_bg,
        width=args.width,
        height=args.height,
    )


if __name__ == "__main__":
    main()
