#!/usr/bin/env python3
"""
================================================================================
Chargemol DDEC6 Population Analysis Suite (chargemol-ddec6)
================================================================================
Prepares, executes, and parses DDEC6 (Density Derived Electrostatic and Chemical)
net atomic charges, atomic spin moments, and atomic bond orders (ABO).
Compatible with VASP (AECCAR0, AECCAR2, CHGCAR) and Chargemol analysis.
================================================================================
"""

import os
import sys
import argparse
import json
import numpy as np

try:
    from pymatgen.command_line.chargemol_caller import ChargemolAnalysis
    HAS_PYMATGEN_CHARGEMOL = True
except ImportError:
    HAS_PYMATGEN_CHARGEMOL = False


def generate_job_control(output_dir=".", net_charge=0.0, periodicity=(True, True, True),
                         atomic_densities_dir="/opt/chargemol/atomic_densities/",
                         input_filename="CHGCAR_sum", charge_type="DDEC6", compute_bo=True):
    """Generates standard Chargemol job_control.txt file."""
    p_strs = [".true." if p else ".false." for p in periodicity]
    bo_str = ".true." if compute_bo else ".false."

    content = f"""<net charge>
{net_charge:.4f}
</net charge>

<periodicity along A, B, and C vectors>
{p_strs[0]}
{p_strs[1]}
{p_strs[2]}
</periodicity along A, B, and C vectors>

<atomic densities directory complete path>
{atomic_densities_dir}
</atomic densities directory complete path>

<input filename>
{input_filename}
</input filename>

<charge type>
{charge_type}
</charge type>

<compute BOs>
{bo_str}
</compute BOs>
"""
    job_file = os.path.join(output_dir, "job_control.txt")
    with open(job_file, "w") as f:
        f.write(content)
    return job_file


def sum_aeccar_files(aeccar0="AECCAR0", aeccar2="AECCAR2", output="CHGCAR_sum"):
    """
    Sums AECCAR0 (core) and AECCAR2 (valence) volumetric charge densities
    natively without requiring external Perl scripts.
    """
    if not (os.path.isfile(aeccar0) and os.path.isfile(aeccar2)):
        raise FileNotFoundError(f"Missing {aeccar0} or {aeccar2} in current directory.")

    print(f"[*] Summing {aeccar0} (core) and {aeccar2} (valence)...")
    with open(aeccar0, "r") as f0, open(aeccar2, "r") as f2, open(output, "w") as out:
        # Copy header from AECCAR0 until grid dimensions
        header_lines = []
        for _ in range(8):
            l0 = f0.readline()
            _ = f2.readline()
            out.write(l0)

        # Parse grid dimensions (NGX NGY NGZ)
        grid_line0 = f0.readline()
        grid_line2 = f2.readline()
        out.write(grid_line0)
        ngx, ngy, ngz = [int(x) for x in grid_line0.split()[:3]]
        n_points = ngx * ngy * ngz

        # Stream and sum density grid points
        count = 0
        while count < n_points:
            l0 = f0.readline()
            l2 = f2.readline()
            if not l0 or not l2:
                break
            vals0 = [float(x) for x in l0.split()]
            vals2 = [float(x) for x in l2.split()]
            summed = [v0 + v2 for v0, v2 in zip(vals0, vals2)]
            out.write(" " + " ".join(f"{s:18.11E}" for s in summed) + "\n")
            count += len(summed)

    print(f"[✓] Created summed charge density: {output}")
    return output


def parse_ddec6_charges(xyz_file="DDEC6_even_tempered_net_atomic_charges.xyz"):
    """Parses net atomic charges and dipole moments from DDEC6 output."""
    if not os.path.isfile(xyz_file):
        raise FileNotFoundError(f"Chargemol output '{xyz_file}' not found.")

    with open(xyz_file, "r") as f:
        num_atoms = int(f.readline().strip())
        comment = f.readline().strip()

        atoms = []
        for i in range(num_atoms):
            parts = f.readline().split()
            sym = parts[0]
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            net_charge = float(parts[4])
            dipole_z = float(parts[5]) if len(parts) > 5 else 0.0
            atoms.append({
                "index": i,
                "element": sym,
                "coords": [x, y, z],
                "net_charge": net_charge,
                "dipole_z": dipole_z
            })

    return {
        "num_atoms": num_atoms,
        "atoms": atoms,
        "total_charge": sum(a["net_charge"] for a in atoms)
    }


def parse_bond_orders(bo_file="DDEC6_even_tempered_atomic_bond_orders.xyz"):
    """Parses pairwise bond orders and total sum of bond orders (SBO)."""
    if not os.path.isfile(bo_file):
        return None

    bond_data = []
    with open(bo_file, "r") as f:
        lines = f.readlines()

    current_atom = None
    for line in lines:
        if "The sum of bond orders (SBO) for atom" in line:
            parts = line.split()
            idx = int(parts[7])
            sbo = float(parts[-1])
            current_atom = {"atom_index": idx, "sbo": sbo, "bonds": []}
            bond_data.append(current_atom)
        elif "Bonded to atom" in line and current_atom is not None:
            parts = line.split()
            target_idx = int(parts[3])
            bo_val = float(parts[-1])
            current_atom["bonds"].append({"target_index": target_idx, "bond_order": bo_val})

    return bond_data


def main():
    parser = argparse.ArgumentParser(description="Chargemol DDEC6 Population & Bond Order Analysis")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Setup
    p_setup = subparsers.add_parser("setup", help="Generate job_control.txt for Chargemol")
    p_setup.add_argument("-d", "--dir", default=".", help="Directory to create job_control.txt")
    p_setup.add_argument("-q", "--charge", type=float, default=0.0, help="Total system net charge")
    p_setup.add_argument("--is-2d", action="store_true", help="Set z-periodicity to false for 2D slab/monolayer")
    p_setup.add_argument("--densities-dir", default="/opt/chargemol/atomic_densities/", help="Path to atomic_densities folder")
    p_setup.add_argument("-i", "--input", default="CHGCAR_sum", help="Input density filename")

    # Sum AECCARs
    p_sum = subparsers.add_parser("chgsum", help="Sum AECCAR0 and AECCAR2 into CHGCAR_sum")
    p_sum.add_argument("--aeccar0", default="AECCAR0", help="Core density file")
    p_sum.add_argument("--aeccar2", default="AECCAR2", help="Valence density file")
    p_sum.add_argument("-o", "--output", default="CHGCAR_sum", help="Summed output file")

    # Parse
    p_parse = subparsers.add_parser("parse", help="Parse DDEC6 net atomic charges and bond orders")
    p_parse.add_argument("-c", "--charges", default="DDEC6_even_tempered_net_atomic_charges.xyz", help="Charges xyz file")
    p_parse.add_argument("-b", "--bonds", default="DDEC6_even_tempered_atomic_bond_orders.xyz", help="Bond orders xyz file")
    p_parse.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.command == "setup":
        periodicity = (True, True, False) if args.is_2d else (True, True, True)
        f = generate_job_control(output_dir=args.dir, net_charge=args.charge,
                                 periodicity=periodicity, atomic_densities_dir=args.densities_dir,
                                 input_filename=args.input)
        print(f"[✓] Created {f}")
    elif args.command == "chgsum":
        sum_aeccar_files(args.aeccar0, args.aeccar2, args.output)
    elif args.command == "parse":
        charges = parse_ddec6_charges(args.charges)
        bonds = parse_bond_orders(args.bonds)
        if args.json:
            out_data = {"charges": charges, "bonds": bonds}
            print(json.dumps(out_data, indent=2))
        else:
            print("\n" + "=" * 60)
            print(f" DDEC6 Net Atomic Charges (Total atoms: {charges['num_atoms']})")
            print(f" System Net Charge: {charges['total_charge']:.4f} e")
            print("=" * 60)
            print(f"{'Idx':>4} | {'Elem':^6} | {'Net Charge (e)':^16} | {'Dipole Z (a.u.)':^16}")
            print("-" * 60)
            for at in charges["atoms"]:
                print(f"{at['index']:>4} | {at['element']:^6} | {at['net_charge']:^16.4f} | {at['dipole_z']:^16.4f}")
            print("=" * 60)
            if bonds:
                print("\n" + "=" * 60)
                print(" Top Atomic Bond Orders (Sum of Bond Orders)")
                print("=" * 60)
                for b in bonds[:10]:
                    print(f" Atom {b['atom_index']:>3} | SBO = {b['sbo']:.3f} | Bonds: {len(b['bonds'])}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
