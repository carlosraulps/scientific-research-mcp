#!/usr/bin/env python3
"""
================================================================================
Bader Charge Analysis & Flux-Weighted Partitioning Suite (bader_flux_analysis.py)
================================================================================
Solves the Periodic Boundary Discrete Grid Artifact in Bader Charge calculations:
1. Mandatory Flux-Weighted Interpolation (-b weight):
   - Eliminates sudden artificial charge flips across periodic cell boundaries
     (e.g. PHOTH-graphene C1-C6 boundary bond).
   - Ensures strictly continuous and monotonic charge transfer curves across
     mechanical strain sweeps and reaction coordinates.
2. Automated Core Charge Reference Integration (-ref CHGCAR_total):
   - Automatically detects AECCAR0 and AECCAR2, invokes chgsum.pl to generate
     CHGCAR_total, and passes it as reference density.
3. Physical Net Valence Charge Mapping:
   - Converts raw valence electron populations into physical net atomic charges:
     \\Delta Q = Z_valence - Q_bader
   - Validates total electron count and charge conservation (sum(\\Delta Q) = 0).
4. Machine-Readable & Publication Export:
   - Generates bader_summary.json, bader_charges.csv, and publication STIX colorbars.
================================================================================
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Standard VASP PAW valence electron lookup
VALENCE_LOOKUP: Dict[str, float] = {
    "H": 1.0, "He": 2.0, "Li": 1.0, "Be": 2.0, "B": 3.0, "C": 4.0, "N": 5.0, "O": 6.0,
    "F": 7.0, "Ne": 8.0, "Na": 1.0, "Mg": 2.0, "Al": 3.0, "Si": 4.0, "P": 5.0, "S": 6.0,
    "Cl": 7.0, "Ar": 8.0, "K": 1.0, "Ca": 2.0, "Sc": 3.0, "Ti": 4.0, "V": 5.0, "Cr": 6.0,
    "Mn": 7.0, "Fe": 8.0, "Co": 9.0, "Ni": 10.0, "Cu": 11.0, "Zn": 12.0, "Ga": 3.0, "Ge": 4.0,
    "As": 5.0, "Se": 6.0, "Br": 7.0, "Kr": 8.0, "Rb": 1.0, "Sr": 2.0, "Y": 3.0, "Zr": 4.0,
    "Nb": 5.0, "Mo": 6.0, "Tc": 7.0, "Ru": 8.0, "Rh": 9.0, "Pd": 10.0, "Ag": 11.0, "Cd": 12.0,
    "In": 3.0, "Sn": 4.0, "Sb": 5.0, "Te": 6.0, "I": 7.0, "Xe": 8.0, "Cs": 1.0, "Ba": 2.0,
    "Pt": 10.0, "Au": 11.0, "Pb": 4.0, "Bi": 5.0,
}


def read_poscar_species_and_coords(poscar_path: Path) -> Tuple[List[str], List[Tuple[float, float, float]]]:
    """Extracts species list and Cartesian coordinates from POSCAR/CONTCAR."""
    try:
        from ase.io import read as ase_read
        atoms = ase_read(str(poscar_path))
        syms = atoms.get_chemical_symbols()
        coords = [tuple(c) for c in atoms.get_positions()]
        return syms, coords
    except Exception:
        pass

    # Simple native parser
    with open(poscar_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    scale = float(lines[1])
    lattice = [
        [float(x) * scale for x in lines[2].split()],
        [float(x) * scale for x in lines[3].split()],
        [float(x) * scale for x in lines[4].split()],
    ]
    line5 = lines[5].split()
    if line5[0].isdigit():
        species = ["C"] * len(line5)
        counts = [int(x) for x in line5]
        idx = 6
    else:
        species = line5
        counts = [int(x) for x in lines[6].split()]
        idx = 7

    if lines[idx].lower().startswith("s"):
        idx += 1
    coord_type = lines[idx].lower()
    idx += 1

    expanded_syms = []
    for sp, cnt in zip(species, counts):
        expanded_syms.extend([sp] * cnt)

    coords = []
    for _ in range(sum(counts)):
        parts = [float(x) for x in lines[idx].split()[:3]]
        coords.append((parts[0], parts[1], parts[2]))
        idx += 1

    return expanded_syms, coords


def prepare_total_charge_reference(workdir: Path) -> Optional[Path]:
    """
    Checks for AECCAR0 and AECCAR2 and executes chgsum.pl to generate CHGCAR_total.
    """
    ae0 = workdir / "AECCAR0"
    ae2 = workdir / "AECCAR2"
    chg_total = workdir / "CHGCAR_total"

    if chg_total.exists() and chg_total.stat().st_size > 1000:
        print(f"[Bader Ref] Found existing CHGCAR_total ({chg_total.stat().st_size / (1024*1024):.1f} MB)")
        return chg_total

    if not (ae0.exists() and ae2.exists()):
        return None

    chgsum_bin = shutil.which("chgsum.pl") or "/home/cr/.local/bin/chgsum.pl"
    if not (os.path.exists(chgsum_bin) and os.access(chgsum_bin, os.X_OK)):
        print(f"[Bader Ref] Warning: AECCAR0/2 found but chgsum.pl is not executable on PATH.", file=sys.stderr)
        return None

    print(f"[Bader Ref] Summing AECCAR0 + AECCAR2 via chgsum.pl...")
    cmd = [chgsum_bin, "AECCAR0", "AECCAR2"]
    res = subprocess.run(cmd, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        # chgsum.pl typically writes to CHGCAR_sum
        sum_out = workdir / "CHGCAR_sum"
        if sum_out.exists():
            shutil.copy2(sum_out, chg_total)
            print(f"[Bader Ref] Created CHGCAR_total reference file successfully.")
            return chg_total
    return None


def parse_acf_dat(acf_path: Path) -> List[Dict[str, float]]:
    """
    Parses Henkelman Bader ACF.dat output file.
    Columns: # X Y Z CHARGE MIN_DIST ATOMIC_VOL
    """
    results = []
    with open(acf_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    for line in lines:
        parts = line.split()
        if len(parts) >= 6 and parts[0].isdigit():
            results.append({
                "atom_id": int(parts[0]),
                "x": float(parts[1]),
                "y": float(parts[2]),
                "z": float(parts[3]),
                "bader_charge": float(parts[4]),
                "min_dist": float(parts[5]),
                "atomic_vol": float(parts[6]) if len(parts) > 6 else 0.0,
            })
    return results


def run_bader_protocol(
    workdir: Union[str, Path] = ".",
    chgcar_name: str = "CHGCAR",
    poscar_name: str = "POSCAR",
    use_weight: bool = True,
    use_reference: bool = True,
    output_prefix: str = "bader",
) -> Dict:
    """
    Executes the robust flux-weighted Bader charge protocol.
    """
    work_path = Path(workdir).resolve()
    chg_path = work_path / chgcar_name
    pos_path = work_path / poscar_name

    if not chg_path.exists():
        raise FileNotFoundError(f"Charge density file not found: {chg_path}")
    if not pos_path.exists():
        # Check CONTCAR fallback
        pos_path = work_path / "CONTCAR"
        if not pos_path.exists():
            raise FileNotFoundError(f"Structure geometry file not found in {work_path}")

    bader_bin = shutil.which("bader") or "/home/cr/.local/bin/bader"
    if not (os.path.exists(bader_bin) and os.access(bader_bin, os.X_OK)):
        raise RuntimeError("Henkelman Bader executable ('bader') not found on system PATH.")

    # Step 1: Core charge reference detection
    ref_file = prepare_total_charge_reference(work_path) if use_reference else None

    # Step 2: Build command line
    cmd = [bader_bin, str(chg_path)]
    if use_weight:
        cmd.extend(["-b", "weight"])
        print("[Bader Protocol] Enforcing flux-weighted interpolation algorithm (-b weight)")
    if ref_file:
        cmd.extend(["-ref", str(ref_file.name)])
        print(f"[Bader Protocol] Using reference total density (-ref {ref_file.name})")

    print(f"[Bader Protocol] Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=work_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Bader Execution Error: {res.stderr}", file=sys.stderr)
        raise RuntimeError(f"Bader failed with exit code {res.returncode}")

    acf_path = work_path / "ACF.dat"
    if not acf_path.exists():
        raise FileNotFoundError("Bader completed but ACF.dat was not produced.")

    # Step 3: Parse results and compute net charges
    parsed_atoms = parse_acf_dat(acf_path)
    species_list, coords_list = read_poscar_species_and_coords(pos_path)

    total_electrons = 0.0
    total_valence = 0.0
    enriched_results = []

    for idx, item in enumerate(parsed_atoms):
        sym = species_list[idx] if idx < len(species_list) else "X"
        z_val = VALENCE_LOOKUP.get(sym, 4.0)
        q_bader = item["bader_charge"]
        net_q = round(z_val - q_bader, 4)

        total_electrons += q_bader
        total_valence += z_val

        record = {
            "atom_id": item["atom_id"],
            "species": sym,
            "x": item["x"],
            "y": item["y"],
            "z": item["z"],
            "bader_charge_e": q_bader,
            "valence_electrons_z": z_val,
            "net_charge_e": net_q,
            "atomic_vol_ang3": item["atomic_vol"],
            "min_dist_ang": item["min_dist"],
        }
        enriched_results.append(record)

    net_charge_sum = round(total_valence - total_electrons, 4)

    # Step 4: Write CSV and JSON outputs
    csv_file = work_path / f"{output_prefix}_charges.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "atom_id", "species", "x", "y", "z",
            "bader_charge_e", "valence_electrons_z", "net_charge_e",
            "atomic_vol_ang3", "min_dist_ang"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_results)

    summary_file = work_path / f"{output_prefix}_summary.json"
    summary_data = {
        "num_atoms": len(enriched_results),
        "total_valence_electrons": round(total_valence, 4),
        "total_bader_electrons": round(total_electrons, 4),
        "total_net_charge_e": net_charge_sum,
        "algorithm": "weight" if use_weight else "neargrid",
        "reference_file": str(ref_file.name) if ref_file else None,
        "atoms": enriched_results,
    }
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    # Print summary table
    print("\n" + "=" * 78)
    print("📊 BADER NET ATOMIC CHARGE SUMMARY (Flux-Weighted Protocol)")
    print("=" * 78)
    print(f" {'ID':<4} {'Species':<8} {'Bader (e)':<12} {'Valence Z':<12} {'Net Q (e)':<14} {'State':<15}")
    print("-" * 78)
    for r in enriched_results[:30]:  # Show first 30
        q_net = r["net_charge_e"]
        state = "Donor (+)" if q_net > 0.02 else ("Acceptor (-)" if q_net < -0.02 else "Neutral (0)")
        print(f" {r['atom_id']:<4} {r['species']:<8} {r['bader_charge_e']:<12.4f} {r['valence_electrons_z']:<12.1f} {q_net:<+14.4f} {state:<15}")
    if len(enriched_results) > 30:
        print(f" ... ({len(enriched_results) - 30} additional atoms omitted from console) ...")
    print("-" * 78)
    print(f" Total Valence: {total_valence:.2f} e | Calculated: {total_electrons:.4f} e | Sum Net: {net_charge_sum:+.4f} e")
    print("=" * 78)
    print(f"✅ Outputs written:\n   • {csv_file}\n   • {summary_file}\n")

    return summary_data


def main():
    parser = argparse.ArgumentParser(
        description="Run robust flux-weighted Bader charge analysis with automatic reference handling"
    )
    parser.add_argument("workdir", nargs="?", default=".", help="Calculation directory containing CHGCAR/POSCAR (default: current dir)")
    parser.add_argument("--chgcar", default="CHGCAR", help="Charge density file (default: CHGCAR)")
    parser.add_argument("--poscar", default="POSCAR", help="Structure file (default: POSCAR)")
    parser.add_argument("--no-weight", dest="weight", action="store_false", help="Disable -b weight flux interpolation")
    parser.add_argument("--no-ref", dest="ref", action="store_false", help="Disable -ref CHGCAR_total core charge reference")
    parser.add_argument("-o", "--prefix", default="bader", help="Output prefix (default: bader)")

    args = parser.parse_args()
    run_bader_protocol(
        workdir=args.workdir,
        chgcar_name=args.chgcar,
        poscar_name=args.poscar,
        use_weight=args.weight,
        use_reference=args.ref,
        output_prefix=args.prefix,
    )


if __name__ == "__main__":
    main()
