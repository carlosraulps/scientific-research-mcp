#!/usr/bin/env python3
"""
vmd_volumetric.py - Headless 3D Volumetric Isosurface Rendering via VMD and Tachyon.

Part of the SciResearch / VMD-Automation Skill Suite.
Renders volumetric datasets (VASP CHGCAR/LOCPOT, Gaussian Cube, OpenDX, CCP4)
with dual isosurfaces (accumulation & depletion or positive/negative potentials)
overlaid on ball-and-stick crystal frameworks, rendered headlessly via Tachyon.
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

VMD_BIN_DEFAULT = "/home/cr/computational-materials-suite/bin/vmd"
TACHYON_BIN_DEFAULT = "/home/cr/computational-materials-suite/vmd/tachyon_LINUXAMD64"

VIEW_ROTATIONS = {
    "c": "",
    "a": "rotate y by -90",
    "b": "rotate x by 90",
    "iso": "rotate y by -45\nrotate x by 35.264"
}


def detect_vol_type(path: str) -> str:
    base = os.path.basename(path).lower()
    if base.startswith("chgcar") or base.startswith("locpot") or base.startswith("parchg"):
        return "CHGCAR"
    if path.endswith(".cube"):
        return "cube"
    if path.endswith(".dx"):
        return "dx"
    if path.endswith(".ccp4"):
        return "ccp4"
    if path.endswith(".xsf"):
        return "xsf"
    return "CHGCAR"


def main():
    parser = argparse.ArgumentParser(
        description="VMD-Volumetric: Headless 3D Isosurface Raytracer for Densities & Potentials",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("volumetric_file", help="Volumetric grid file (CHGCAR, LOCPOT, Cube, DX, XSF)")
    parser.add_argument("-o", "--output", default="./isosurface.png", help="Output image file")
    parser.add_argument("-v", "--view", choices=["c", "a", "b", "iso"], default="iso", help="Projection view")
    parser.add_argument("--isoval", type=float, default=0.005, help="Isosurface cutoff value")
    parser.add_argument("--dual", action="store_true", default=True, help="Render dual +/- isosurfaces (CDD mode)")
    parser.add_argument("--single", dest="dual", action="store_false", help="Render single positive isosurface")
    parser.add_argument("--pos-color", default="yellow", help="Positive isosurface color (yellow, gold, red)")
    parser.add_argument("--neg-color", default="cyan", help="Negative isosurface color (cyan, blue)")
    parser.add_argument("--pos-mat", default="AOShiny", help="Positive isosurface material (AOShiny, Transparent, Glass)")
    parser.add_argument("--neg-mat", default="AOShiny", help="Negative isosurface material (AOShiny, Transparent, Glass)")
    parser.add_argument("--pbc-box", action="store_true", default=True, help="Draw unit cell boundary box")
    parser.add_argument("--width", type=int, default=1920, help="Output width in pixels")
    parser.add_argument("--height", type=int, default=1080, help="Output height in pixels")
    parser.add_argument("--ao", type=float, default=0.7, help="Tachyon ambient occlusion skylight factor")
    parser.add_argument("--samples", type=int, default=12, help="Anti-aliasing rays per pixel")
    parser.add_argument("--bg", choices=["white", "black"], default="white", help="Display background color")
    parser.add_argument("--vmd-bin", default=VMD_BIN_DEFAULT, help="Path to vmd executable")
    parser.add_argument("--tachyon-bin", default=TACHYON_BIN_DEFAULT, help="Path to tachyon executable")

    args = parser.parse_args()

    if not os.path.exists(args.volumetric_file):
        sys.stderr.write(f"Error: File not found: {args.volumetric_file}\n")
        sys.exit(1)

    file_type = detect_vol_type(args.volumetric_file)

    with tempfile.TemporaryDirectory() as tmpdir:
        tcl_script = os.path.join(tmpdir, "vol.tcl")
        tach_dat = os.path.join(tmpdir, "scene.dat")
        tach_bmp = os.path.join(tmpdir, "scene.bmp")

        tcl = []
        tcl.append("package require pbctools")
        tcl.append(f"mol new {{{os.path.abspath(args.volumetric_file)}}} type {file_type} waitfor all")
        tcl.append("mol delrep 0 top")

        # Rep 0: Atomic framework (CPK)
        tcl.append("mol representation CPK 0.40 0.15 28 28")
        tcl.append("mol color Element")
        tcl.append("mol selection all")
        tcl.append("mol material AOShiny")
        tcl.append("mol addrep top")

        # Rep 1: Positive Isosurface
        tcl.append(f"mol representation Isosurface {args.isoval} 0 2 0")
        tcl.append(f"mol color ColorID 4")  # Yellow
        tcl.append(f"mol material {args.pos_mat}")
        tcl.append("mol addrep top")

        # Rep 2: Negative Isosurface (if dual)
        if args.dual:
            neg_val = -abs(args.isoval)
            tcl.append(f"mol representation Isosurface {neg_val} 0 2 0")
            tcl.append(f"mol color ColorID 0")  # Blue / Cyan
            tcl.append(f"mol material {args.neg_mat}")
            tcl.append("mol addrep top")

        if args.pbc_box:
            tcl.append("pbc box -color black -width 2.0")

        tcl.append("display projection Orthographic")
        tcl.append(f"color Display Background {args.bg}")
        tcl.append("axes location Off")
        tcl.append("display resetview")

        rot = VIEW_ROTATIONS.get(args.view, "")
        if rot:
            tcl.append(rot)

        tcl.append(f"render Tachyon {{{tach_dat}}}")
        tcl.append("exit")

        with open(tcl_script, "w") as f:
            f.write("\n".join(tcl) + "\n")

        vmd_cmd = [args.vmd_bin, "-dispdev", "text", "-e", tcl_script]
        v_res = subprocess.run(vmd_cmd, capture_output=True, text=True)
        if not os.path.exists(tach_dat):
            sys.stderr.write(f"VMD Error generating volumetric scene:\n{v_res.stderr}\n")
            sys.exit(1)

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
        t_res = subprocess.run(tach_cmd, capture_output=True, text=True)
        if not os.path.exists(tach_bmp):
            sys.stderr.write(f"Tachyon Error:\n{t_res.stderr}\n")
            sys.exit(1)

        os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
        if HAS_PIL:
            im = Image.open(tach_bmp)
            out_ext = os.path.splitext(args.output)[1].lower()
            if out_ext in [".jpg", ".jpeg"]:
                im.convert("RGB").save(args.output, quality=95)
            elif out_ext == ".pdf":
                im.convert("RGB").save(args.output, "PDF", resolution=300.0)
            else:
                im.save(args.output, "PNG")
        else:
            shutil.copy(tach_bmp, args.output)

        print(f"✨ [VMD-Volumetric] 3D Isosurface rendered successfully: {args.output}")


if __name__ == "__main__":
    main()
