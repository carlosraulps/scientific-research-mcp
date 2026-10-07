#!/home/cr/.local/share/mamba/envs/vasp-env/bin/python
"""
================================================================================
PyProcar Electronic Structure Suite (pyprocar-suite)
================================================================================
Comprehensive post-processing of VASP PROCAR and OUTCAR files:
- Fat bands & orbital-projected band structures
- Spin texture (Sx, Sy, Sz) across reciprocal space
- Supercell band unfolding onto primitive Brillouin zones
- Direct & indirect band gap extraction
================================================================================
"""

import os
import sys
import argparse
import pyprocar


def run_bands(code="vasp", dirname=".", atoms=None, orbitals=None, 
              spins=None, mode="parametric", outname="fat_bands.png", 
              elimit=None, fermi=None):
    """Generates projected fat bands or parametric orbital band structure."""
    kwargs = {
        "code": code,
        "dirname": dirname,
        "mode": mode,
        "savefig": outname
    }
    if atoms is not None:
        kwargs["atoms"] = [int(a) for a in atoms.split(",")]
    if orbitals is not None:
        kwargs["orbitals"] = [int(o) for o in orbitals.split(",")]
    if spins is not None:
        kwargs["spins"] = [int(s) for s in spins.split(",")]
    if elimit is not None:
        kwargs["elimit"] = [float(x) for x in elimit.split(",")]
    if fermi is not None:
        kwargs["fermi"] = float(fermi)

    print(f"[*] Plotting band structure with pyprocar (mode={mode})...")
    pyprocar.bandsplot(**kwargs)
    print(f"[✓] Generated band structure plot: {outname}")


def run_spin_texture(code="vasp", dirname=".", spin_component="z", 
                     outname="spin_texture.png", elimit=None):
    """Plots spin texture along band structure or 2D Fermi surface."""
    # Spin projections in PROCAR: 1=Sx, 2=Sy, 3=Sz
    spin_map = {"x": [1], "y": [2], "z": [3]}
    spins = spin_map.get(spin_component.lower(), [3])

    kwargs = {
        "code": code,
        "dirname": dirname,
        "mode": "spin",
        "spins": spins,
        "savefig": outname
    }
    if elimit is not None:
        kwargs["elimit"] = [float(x) for x in elimit.split(",")]

    print(f"[*] Plotting S_{spin_component} spin texture...")
    pyprocar.bandsplot(**kwargs)
    print(f"[✓] Generated spin texture plot: {outname}")


def run_unfold(code="vasp", dirname=".", supercell_matrix="2,0,0,0,2,0,0,0,1", 
               outname="unfolded_bands.png", elimit=None):
    """Unfolds supercell electronic band structure into primitive Brillouin zone."""
    mat_vals = [float(x) for x in supercell_matrix.split(",")]
    if len(mat_vals) == 9:
        matrix = [mat_vals[0:3], mat_vals[3:6], mat_vals[6:9]]
    else:
        raise ValueError("Supercell matrix must contain 9 comma-separated values (3x3).")

    kwargs = {
        "code": code,
        "dirname": dirname,
        "supercell_matrix": matrix,
        "savefig": outname
    }
    if elimit is not None:
        kwargs["elimit"] = [float(x) for x in elimit.split(",")]

    print(f"[*] Unfolding supercell bands using matrix {matrix}...")
    pyprocar.unfold(**kwargs)
    print(f"[✓] Generated unfolded band plot: {outname}")


def run_bandgap(code="vasp", dirname="."):
    """Extracts electronic band gap, VBM, CBM, and transition type."""
    print(f"[*] Analyzing band gap in directory '{dirname}'...")
    gap_info = pyprocar.bandgap(code=code, dirname=dirname)
    print(f"[✓] Band Gap Analysis:\n{gap_info}")


def main():
    parser = argparse.ArgumentParser(description="PyProcar Electronic Structure Suite")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to execute")

    # Bands
    p_bands = subparsers.add_parser("bands", help="Plot projected or fat bands")
    p_bands.add_argument("-d", "--dir", default=".", help="Directory containing PROCAR/OUTCAR")
    p_bands.add_argument("-a", "--atoms", help="Comma-separated list of atom indices (0-based or 1-based per code)")
    p_bands.add_argument("-o", "--orbitals", help="Comma-separated orbital indices (e.g. 0 for s, 1..3 for p, 4..8 for d)")
    p_bands.add_argument("-s", "--spins", help="Comma-separated spin channels (e.g. 0, 1)")
    p_bands.add_argument("-m", "--mode", default="parametric", choices=["plain", "parametric", "scatter", "atomic"], help="Plotting mode")
    p_bands.add_argument("-e", "--elimit", help="Energy limits 'Emin,Emax' relative to Fermi level (e.g. '-4,4')")
    p_bands.add_argument("-f", "--fermi", help="Manual Fermi energy override")
    p_bands.add_argument("--out", default="fat_bands.png", help="Output figure filename")

    # Spin Texture
    p_spin = subparsers.add_parser("spin", help="Plot spin texture (Sx, Sy, Sz)")
    p_spin.add_argument("-d", "--dir", default=".", help="Directory containing PROCAR/OUTCAR")
    p_spin.add_argument("-c", "--component", default="z", choices=["x", "y", "z"], help="Spin component (x, y, or z)")
    p_spin.add_argument("-e", "--elimit", help="Energy window 'Emin,Emax' (e.g. '-3,3')")
    p_spin.add_argument("--out", default="spin_texture.png", help="Output figure filename")

    # Unfold
    p_unfold = subparsers.add_parser("unfold", help="Unfold supercell band structure")
    p_unfold.add_argument("-d", "--dir", default=".", help="Directory containing PROCAR/POSCAR")
    p_unfold.add_argument("-m", "--matrix", default="2,0,0,0,2,0,0,0,1", help="3x3 supercell expansion matrix as 9 comma-separated floats")
    p_unfold.add_argument("-e", "--elimit", help="Energy window 'Emin,Emax'")
    p_unfold.add_argument("--out", default="unfolded_bands.png", help="Output figure filename")

    # Bandgap
    p_gap = subparsers.add_parser("gap", help="Calculate band gap from PROCAR")
    p_gap.add_argument("-d", "--dir", default=".", help="Directory containing PROCAR/OUTCAR")

    args = parser.parse_args()

    if args.command == "bands":
        run_bands(dirname=args.dir, atoms=args.atoms, orbitals=args.orbitals, 
                  spins=args.spins, mode=args.mode, outname=args.out, 
                  elimit=args.elimit, fermi=args.fermi)
    elif args.command == "spin":
        run_spin_texture(dirname=args.dir, spin_component=args.component, 
                         outname=args.out, elimit=args.elimit)
    elif args.command == "unfold":
        run_unfold(dirname=args.dir, supercell_matrix=args.matrix, 
                   outname=args.out, elimit=args.elimit)
    elif args.command == "gap":
        run_bandgap(dirname=args.dir)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
