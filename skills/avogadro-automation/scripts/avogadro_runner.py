#!/home/cr/.local/share/mamba/envs/vasp-env/bin/python
"""
================================================================================
Avogadro 2 & OpenBabel Molecular Modeling Automation Suite
================================================================================
Provides headless molecular generation, 3D conformer optimization (UFF/MMFF94),
adsorbate placement/grafting onto 2D slabs/clusters, format conversion
(SMILES, PDB, MOL2, XYZ, POSCAR), and interactive Avogadro 2 launch.
================================================================================
"""

import os
import sys
import argparse
import subprocess
import numpy as np

try:
    from openbabel import pybel
    import openbabel as ob
    HAS_PYBEL = True
except ImportError:
    HAS_PYBEL = False

try:
    from pymatgen.core import Structure, Molecule
    HAS_PYMATGEN = True
except ImportError:
    HAS_PYMATGEN = False


def build_molecule_from_smiles(smiles: str, output_path: str, forcefield="mmff94", steps=500):
    """Builds 3D optimized molecular coordinates from SMILES string."""
    if not HAS_PYBEL:
        raise RuntimeError("OpenBabel/pybel required for SMILES 3D conversion.")
    
    mol = pybel.readstring("smi", smiles)
    mol.addh()
    mol.make3D(forcefield=forcefield, steps=steps)
    mol.localopt(forcefield=forcefield, steps=steps)
    
    ext = os.path.splitext(output_path)[1].lstrip(".").lower()
    if not ext:
        ext = "xyz"
        output_path += ".xyz"
    
    mol.write(ext, output_path, overwrite=True)
    return output_path


def convert_format(input_path: str, output_path: str):
    """Converts molecular or crystallographic file between chemical formats."""
    in_ext = os.path.splitext(input_path)[1].lstrip(".").lower()
    out_ext = os.path.splitext(output_path)[1].lstrip(".").lower()

    if HAS_PYBEL:
        mol = next(pybel.readfile(in_ext, input_path))
        mol.write(out_ext, output_path, overwrite=True)
        return output_path
    else:
        # Fallback to obabel CLI
        cmd = ["obabel", f"-i{in_ext}", input_path, f"-o{out_ext}", "-O", output_path]
        subprocess.run(cmd, check=True)
        return output_path


def graft_molecule_on_slab(slab_poscar: str, mol_file: str, site_index: int, 
                           distance=2.1, output_poscar="GRAFTED_POSCAR"):
    """
    Grafts an adsorbate molecule on top of a specified slab atom site
    along the surface normal (+z direction).
    """
    with open(slab_poscar, "r") as f:
        slab_lines = [l.strip() for l in f if l.strip()]

    scale = float(slab_lines[1])
    lattice = np.array([[float(x) * scale for x in slab_lines[i].split()[:3]] for i in range(2, 5)])
    species = slab_lines[5].split()
    counts = [int(c) for c in slab_lines[6].split()]

    slab_elements = []
    for sp, cnt in zip(species, counts):
        slab_elements.extend([sp] * cnt)

    coord_type = slab_lines[7].lower()
    is_direct = "direct" in coord_type or coord_type.startswith("d")

    slab_coords = []
    for i in range(8, 8 + len(slab_elements)):
        slab_coords.append([float(x) for x in slab_lines[i].split()[:3]])
    slab_coords = np.array(slab_coords)
    if is_direct:
        slab_cart = slab_coords @ lattice
    else:
        slab_cart = slab_coords * scale

    target_site = slab_cart[site_index]

    # Read molecule
    mol_ext = os.path.splitext(mol_file)[1].lstrip(".").lower()
    mol = next(pybel.readfile(mol_ext, mol_file))
    mol_elems = [ob.GetSymbol(atom.atomicnum) for atom in mol.atoms]
    mol_coords = np.array([atom.coords for atom in mol.atoms])

    # Center molecule and shift bottom-most atom to distance above target site
    min_z_idx = np.argmin(mol_coords[:, 2])
    anchor_pt = mol_coords[min_z_idx]
    shifted_mol = mol_coords - anchor_pt
    shifted_mol[:, 0] += target_site[0]
    shifted_mol[:, 1] += target_site[1]
    shifted_mol[:, 2] += target_site[2] + distance

    # Combine elements and coordinates
    combined_elems = slab_elements + mol_elems
    combined_cart = np.vstack([slab_cart, shifted_mol])

    # Convert back to fractional
    inv_lat = np.linalg.inv(lattice)
    combined_frac = combined_cart @ inv_lat

    # Group by species
    unique_species = []
    for el in combined_elems:
        if el not in unique_species:
            unique_species.append(el)

    grouped_counts = []
    grouped_frac = []
    for sp in unique_species:
        idx_list = [i for i, el in enumerate(combined_elems) if el == sp]
        grouped_counts.append(len(idx_list))
        grouped_frac.extend(combined_frac[idx_list])

    # Write POSCAR
    with open(output_poscar, "w") as f:
        f.write(f"Grafted {os.path.basename(mol_file)} on site {site_index}\n")
        f.write("1.0\n")
        for row in lattice:
            f.write(f"  {row[0]:15.8f} {row[1]:15.8f} {row[2]:15.8f}\n")
        f.write("  " + "  ".join(unique_species) + "\n")
        f.write("  " + "  ".join(str(c) for c in grouped_counts) + "\n")
        f.write("Direct\n")
        for pt in grouped_frac:
            # Wrap within [0, 1) except z if desired
            f.write(f"  {pt[0]%1.0:15.8f} {pt[1]%1.0:15.8f} {pt[2]:15.8f}\n")

    return output_poscar


def launch_avogadro(file_path=None, headless=False):
    """Launches Avogadro 2 AppImage."""
    cmd = ["avogadro"]
    if file_path:
        cmd.append(file_path)
    
    if headless:
        cmd = ["xvfb-run", "-a"] + cmd
    
    subprocess.Popen(cmd)


def main():
    parser = argparse.ArgumentParser(description="Avogadro 2 & OpenBabel Automation Suite")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Build SMILES
    p_build = subparsers.add_parser("build", help="Build 3D molecule from SMILES")
    p_build.add_argument("smiles", help="SMILES string (e.g. 'CC(=O)O')")
    p_build.add_argument("-o", "--output", default="molecule.xyz", help="Output file path (.xyz, .mol, .pdb)")
    p_build.add_argument("--ff", default="mmff94", choices=["uff", "mmff94", "gaff"], help="Forcefield")
    p_build.add_argument("--steps", type=int, default=500, help="Optimization steps")

    # Convert
    p_conv = subparsers.add_parser("convert", help="Convert between molecular file formats")
    p_conv.add_argument("input", help="Input file path")
    p_conv.add_argument("output", help="Output file path")

    # Graft
    p_graft = subparsers.add_parser("graft", help="Graft molecule onto slab POSCAR")
    p_graft.add_argument("--slab", required=True, help="Slab POSCAR file")
    p_graft.add_argument("--molecule", required=True, help="Adsorbate molecule file")
    p_graft.add_argument("--site", type=int, required=True, help="0-based atom index in slab to adsorb over")
    p_graft.add_argument("--distance", type=float, default=2.1, help="Adsorption height in Angstroms")
    p_graft.add_argument("-o", "--output", default="GRAFTED_POSCAR", help="Output POSCAR file")

    # Launch GUI
    p_gui = subparsers.add_parser("gui", help="Launch Avogadro 2 desktop interface")
    p_gui.add_argument("file", nargs="?", help="Optional file to open in Avogadro")

    args = parser.parse_args()

    if args.command == "build":
        out = build_molecule_from_smiles(args.smiles, args.output, forcefield=args.ff, steps=args.steps)
        print(f"[✓] Built 3D molecule: {out}")
    elif args.command == "convert":
        out = convert_format(args.input, args.output)
        print(f"[✓] Converted {args.input} -> {out}")
    elif args.command == "graft":
        out = graft_molecule_on_slab(args.slab, args.molecule, args.site, distance=args.distance, output_poscar=args.output)
        print(f"[✓] Grafted adsorbate: {out}")
    elif args.command == "gui":
        launch_avogadro(args.file)
        print("[*] Launched Avogadro 2.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
