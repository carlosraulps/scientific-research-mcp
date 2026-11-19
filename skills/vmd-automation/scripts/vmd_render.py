#!/usr/bin/env python3
"""
vmd_render.py - Headless, High-Fidelity Scientific Rendering via VMD & Tachyon Raytracer.

Part of the SciResearch / VMD-Automation Skill Suite.
Automates VMD 2.0+ execution in text/headless mode and drives the Tachyon software raytracer
to produce publication-grade 3D renders with ambient occlusion, soft contact shadows,
and anti-aliasing without requiring an active X11 display or GPU.
"""

import os
import sys
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageChops
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Canonical suite paths
VMD_BIN_DEFAULT = "/home/cr/computational-materials-suite/bin/vmd"
TACHYON_BIN_DEFAULT = "/home/cr/computational-materials-suite/vmd/tachyon_LINUXAMD64"

# Format mapping for VMD molfile plugins
FORMAT_MAP = {
    ".poscar": "POSCAR",
    ".contcar": "POSCAR",
    ".vasp": "POSCAR",
    ".xdatcar": "XDATCAR",
    ".pdb": "pdb",
    ".ent": "pdb",
    ".cif": "pdbx",
    ".mmcif": "pdbx",
    ".pdbx": "pdbx",
    ".xyz": "xyz",
    ".mol2": "mol2",
    ".cube": "cube",
    ".dx": "dx",
    ".xsf": "xsf",
    ".dump": "lammpstrj",
    ".lammpstrj": "lammpstrj",
    ".trj": "lammpstrj",
    ".yaml": "lammpsyaml",
    ".yml": "lammpsyaml",
    ".gro": "gro",
    ".xtc": "xtc",
    ".trr": "trr",
    ".dcd": "dcd"
}

PRESETS = {
    "2d-carbon": {
        "rep": "CPK",
        "sphere_scale": 0.38,
        "bond_radius": 0.14,
        "sphere_res": 32,
        "bond_res": 32,
        "material": "AOShiny",
        "description": "Optimized for 2D carbon allotropes (graphene, PHOTH-graphene, BCN)"
    },
    "perovskite": {
        "rep": "CPK",
        "sphere_scale": 0.65,
        "bond_radius": 0.18,
        "sphere_res": 32,
        "bond_res": 32,
        "material": "AOShiny",
        "description": "Optimized for halide and oxide perovskite crystal structures"
    },
    "biomolecule": {
        "rep": "NewCartoon",
        "sphere_scale": 0.40,
        "bond_radius": 0.15,
        "sphere_res": 24,
        "bond_res": 24,
        "material": "AOShiny",
        "description": "NewCartoon ribbon for backbone with secondary structure"
    },
    "standard": {
        "rep": "CPK",
        "sphere_scale": 0.45,
        "bond_radius": 0.18,
        "sphere_res": 30,
        "bond_res": 30,
        "material": "AOShiny",
        "description": "Standard balanced ball-and-stick representation"
    },
    "quicksurf": {
        "rep": "QuickSurf",
        "sphere_scale": 1.0,
        "bond_radius": 0.5,
        "sphere_res": 1.0,
        "bond_res": 1.0,
        "material": "AOShiny",
        "description": "Smooth continuous Gaussian density surface"
    },
    "spacefill": {
        "rep": "VDW",
        "sphere_scale": 1.0,
        "bond_radius": 0.0,
        "sphere_res": 32,
        "bond_res": 32,
        "material": "AOShiny",
        "description": "Van der Waals spacefilling spheres"
    }
}

VIEW_ROTATIONS = {
    "c": "",  # Standard top view looking down z onto xy plane
    "a": "rotate y by -90",  # Looking down x onto yz plane
    "b": "rotate x by 90",   # Looking down y onto xz plane
    "iso": "rotate y by -45\nrotate x by 35.264"  # Isometric projection (arcsin(1/sqrt(3)))
}


def detect_file_type(file_path: str) -> str:
    """Detects VMD molfile type from filename or path."""
    basename = os.path.basename(file_path).lower()
    if basename.startswith("poscar") or basename.startswith("contcar"):
        return "POSCAR"
    if basename.startswith("xdatcar"):
        return "XDATCAR"
    if basename.startswith("chgcar") or basename.startswith("locpot") or basename.startswith("parchg"):
        return "CHGCAR"
    if basename.startswith("outcar"):
        return "OUTCAR"
    if basename.startswith("dump"):
        return "lammpstrj"

    _, ext = os.path.splitext(basename)
    return FORMAT_MAP.get(ext, "pdb")


def autotrim_image(img_path: str, padding: int = 30, bg_color: tuple = (255, 255, 255)):
    """Trims solid background borders around rendered image down to uniform padding."""
    if not HAS_PIL:
        return
    try:
        im = Image.open(img_path).convert("RGB")
        bg = Image.new(im.mode, im.size, bg_color)
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            left = max(0, bbox[0] - padding)
            top = max(0, bbox[1] - padding)
            right = min(im.width, bbox[2] + padding)
            bottom = min(im.height, bbox[3] + padding)
            cropped = im.crop((left, top, right, bottom))
            cropped.save(img_path)
    except Exception as e:
        sys.stderr.write(f"Warning: autotrim failed: {e}\n")


def generate_vmd_tcl(
    input_file: str,
    file_type: str,
    view: str,
    rep_type: str,
    sphere_scale: float,
    bond_radius: float,
    sphere_res: int,
    bond_res: int,
    material: str,
    color_by: str,
    pbc_box: bool,
    pbc_box_width: float,
    pbc_box_color: str,
    periodic_images: str,
    bg_color: str,
    tachyon_dat: str
) -> str:
    """Generates the VMD TCL driver script."""
    lines = []
    lines.append("package require pbctools")
    lines.append(f"mol new {{{os.path.abspath(input_file)}}} type {file_type} waitfor all")
    lines.append("mol delrep 0 top")

    # Representation
    if rep_type.upper() == "CPK":
        lines.append(f"mol representation CPK {sphere_scale} {bond_radius} {sphere_res} {bond_res}")
    elif rep_type.upper() == "VDW":
        lines.append(f"mol representation VDW {sphere_scale} {sphere_res}")
    elif rep_type.upper() == "LICORICE":
        lines.append(f"mol representation Licorice {bond_radius} {bond_res} {bond_res}")
    elif rep_type.upper() == "NEWCARTOON":
        lines.append(f"mol representation NewCartoon")
    elif rep_type.upper() == "QUICKSURF":
        lines.append(f"mol representation QuickSurf {sphere_scale} 1.0 1.0 1.0")
    elif rep_type.upper() == "LINES":
        lines.append(f"mol representation Lines {bond_radius}")
    else:
        lines.append(f"mol representation CPK {sphere_scale} {bond_radius} {sphere_res} {bond_res}")

    lines.append(f"mol color {color_by}")
    lines.append("mol selection all")
    lines.append(f"mol material {material}")
    lines.append("mol addrep top")

    # Periodic images if requested
    if periodic_images:
        lines.append(f'mol showperiodic top 0 "{periodic_images}"')
        lines.append("mol numperiodic top 0 1")

    # Unit cell boundary box
    if pbc_box:
        lines.append(f"pbc box -color {pbc_box_color} -width {pbc_box_width}")

    # Viewport setup
    lines.append("display projection Orthographic")
    lines.append(f"color Display Background {bg_color}")
    lines.append("axes location Off")
    lines.append("display resetview")

    # Camera orientation
    rot_cmds = VIEW_ROTATIONS.get(view, "")
    if rot_cmds:
        lines.append(rot_cmds)

    # Render out to Tachyon dat
    lines.append(f"render Tachyon {{{tachyon_dat}}}")
    lines.append("exit")
    return "\n".join(lines) + "\n"


def render_single_view(
    input_file: str,
    file_type: str,
    view: str,
    output_path: str,
    args: argparse.Namespace
) -> bool:
    """Executes VMD headless extraction and Tachyon raytracing for one view."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tcl_script = os.path.join(tmpdir, "render.tcl")
        tach_dat = os.path.join(tmpdir, "scene.dat")
        tach_bmp = os.path.join(tmpdir, "scene.bmp")

        tcl_content = generate_vmd_tcl(
            input_file=input_file,
            file_type=file_type,
            view=view,
            rep_type=args.rep,
            sphere_scale=args.sphere_scale,
            bond_radius=args.bond_radius,
            sphere_res=args.sphere_res,
            bond_res=args.bond_res,
            material=args.material,
            color_by=args.color_by,
            pbc_box=args.pbc_box,
            pbc_box_width=args.pbc_box_width,
            pbc_box_color=args.pbc_box_color,
            periodic_images=args.periodic_images,
            bg_color=args.bg,
            tachyon_dat=tach_dat
        )

        with open(tcl_script, "w") as f:
            f.write(tcl_content)

        # 1. Run VMD text mode
        vmd_cmd = [args.vmd_bin, "-dispdev", "text", "-e", tcl_script]
        vmd_res = subprocess.run(vmd_cmd, capture_output=True, text=True)
        if vmd_res.returncode != 0 and not os.path.exists(tach_dat):
            sys.stderr.write(f"VMD Error:\n{vmd_res.stderr}\n{vmd_res.stdout}\n")
            return False

        if not os.path.exists(tach_dat):
            sys.stderr.write(f"Failed to generate Tachyon scene file: {tach_dat}\n")
            return False

        # 2. Run Tachyon Raytracer
        tach_cmd = [
            args.tachyon_bin,
            tach_dat,
            "-fullshade",
            "-auto_skylight", str(args.ao),
            "-aasamples", str(args.samples),
            "-res", str(args.width), str(args.height),
            "-format", "BMP",
            "-o", tach_bmp
        ]
        tach_res = subprocess.run(tach_cmd, capture_output=True, text=True)
        if tach_res.returncode != 0 or not os.path.exists(tach_bmp):
            sys.stderr.write(f"Tachyon Error:\n{tach_res.stderr}\n{tach_res.stdout}\n")
            return False

        # 3. Post-process format conversion and trimming
        out_ext = os.path.splitext(output_path)[1].lower()
        if HAS_PIL:
            im = Image.open(tach_bmp)
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            if out_ext in [".jpg", ".jpeg"]:
                im.convert("RGB").save(output_path, quality=95)
            elif out_ext == ".pdf":
                im.convert("RGB").save(output_path, "PDF", resolution=300.0)
            elif out_ext == ".bmp":
                shutil.copy(tach_bmp, output_path)
            else:
                im.save(output_path, "PNG")

            if args.autotrim:
                bg_tuple = (255, 255, 255) if args.bg.lower() == "white" else (0, 0, 0)
                autotrim_image(output_path, padding=args.trim_padding, bg_color=bg_tuple)
        else:
            shutil.copy(tach_bmp, output_path)

        print(f"✨ [VMD-Tachyon] Successfully rendered ({view}-axis): {output_path}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="VMD-Render: Headless Raytraced Scientific Crystal & Molecular Visualizer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_file", help="Input structure file (POSCAR, LAMMPS, PDB, XYZ, Cube, XSF)")
    parser.add_argument("-o", "--output", default="./vmd_render.png", help="Output image file or directory")
    parser.add_argument("-v", "--view", choices=["c", "a", "b", "iso", "all"], default="iso",
                        help="Camera projection: 'c' (xy), 'a' (yz), 'b' (xz), 'iso', or 'all'")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), default="standard",
                        help="Calibrated scientific visualization preset")
    parser.add_argument("--rep", choices=["cpk", "vdw", "licorice", "newcartoon", "quicksurf", "lines"],
                        default=None, help="Graphical representation override")
    parser.add_argument("--material", default=None,
                        choices=["AOShiny", "Opaque", "Glossy", "Transparent", "Glass", "Edgy"],
                        help="Surface shader material")
    parser.add_argument("--color-by", default="Element",
                        help="Coloring method (Element, ResType, Index, Secondary Structure, Charge)")
    parser.add_argument("--sphere-scale", type=float, default=None, help="Atomic sphere scale (Å)")
    parser.add_argument("--bond-radius", type=float, default=None, help="Bond cylinder radius (Å)")
    parser.add_argument("--sphere-res", type=int, default=32, help="Sphere polygon resolution")
    parser.add_argument("--bond-res", type=int, default=32, help="Bond polygon resolution")
    parser.add_argument("--pbc-box", action="store_true", help="Draw periodic unit cell boundary box")
    parser.add_argument("--pbc-box-width", type=float, default=2.0, help="Unit cell boundary line width")
    parser.add_argument("--pbc-box-color", default="black", help="Unit cell line color")
    parser.add_argument("--periodic-images", default="",
                        help="Periodic image replicas string (e.g. '+X -X +Y -Y')")
    parser.add_argument("--type", dest="file_type", default=None,
                        help="Explicit VMD molfile type (POSCAR, pdb, xyz, lammpstrj, cube)")
    parser.add_argument("--width", type=int, default=1920, help="Output image width in pixels")
    parser.add_argument("--height", type=int, default=1080, help="Output image height in pixels")
    parser.add_argument("--ao", type=float, default=0.7, help="Tachyon ambient occlusion skylight factor")
    parser.add_argument("--samples", type=int, default=12, help="Tachyon anti-aliasing sample rays per pixel")
    parser.add_argument("--bg", choices=["white", "black"], default="white", help="Display background color")
    parser.add_argument("--autotrim", action="store_true", default=True, help="Auto-trim whitespace margins")
    parser.add_argument("--no-trim", dest="autotrim", action="store_false", help="Disable whitespace trimming")
    parser.add_argument("--trim-padding", type=int, default=30, help="Whitespace padding in pixels")
    parser.add_argument("--vmd-bin", default=VMD_BIN_DEFAULT, help="Path to vmd executable")
    parser.add_argument("--tachyon-bin", default=TACHYON_BIN_DEFAULT, help="Path to tachyon executable")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        sys.stderr.write(f"Error: Input structure file not found: {args.input_file}\n")
        sys.exit(1)

    # Resolve preset parameters
    preset_data = PRESETS[args.preset]
    if args.rep is None:
        args.rep = preset_data["rep"]
    if args.sphere_scale is None:
        args.sphere_scale = preset_data["sphere_scale"]
    if args.bond_radius is None:
        args.bond_radius = preset_data["bond_radius"]
    if args.material is None:
        args.material = preset_data["material"]

    file_type = args.file_type or detect_file_type(args.input_file)

    if args.view == "all":
        out_dir = args.output
        if out_dir.endswith(".png") or out_dir.endswith(".jpg") or out_dir.endswith(".pdf"):
            base_dir = os.path.dirname(out_dir) or "."
            stem = os.path.splitext(os.path.basename(out_dir))[0]
            ext = os.path.splitext(out_dir)[1]
        else:
            base_dir = out_dir
            stem = os.path.splitext(os.path.basename(args.input_file))[0]
            ext = ".png"

        os.makedirs(base_dir, exist_ok=True)
        views = ["a", "b", "c", "iso"]
        success = True
        for v in views:
            v_path = os.path.join(base_dir, f"{stem}_{v}{ext}")
            ok = render_single_view(args.input_file, file_type, v, v_path, args)
            if not ok:
                success = False
        sys.exit(0 if success else 1)
    else:
        output_path = args.output
        if os.path.isdir(output_path) or output_path.endswith("/"):
            stem = os.path.splitext(os.path.basename(args.input_file))[0]
            output_path = os.path.join(output_path, f"{stem}_{args.view}.png")
        ok = render_single_view(args.input_file, file_type, args.view, output_path, args)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
