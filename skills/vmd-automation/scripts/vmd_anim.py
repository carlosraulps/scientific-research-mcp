#!/usr/bin/env python3
"""
vmd_anim.py - Headless Trajectory Animation & Video Rendering via VMD and Tachyon.

Part of the SciResearch / VMD-Automation Skill Suite.
Renders molecular dynamics trajectories (LAMMPS dump, VASP XDATCAR, DCD, XTC, XYZ)
headlessly into uniform-geometry frame sequences and encodes them into publication-grade
MP4 video or animated GIF via ffmpeg / Pillow with locked camera FOV.
"""

import os
import sys
import argparse
import subprocess
import tempfile
import glob
from pathlib import Path

try:
    from PIL import Image
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


def detect_file_type(file_path: str) -> str:
    basename = os.path.basename(file_path).lower()
    if basename.startswith("xdatcar"):
        return "XDATCAR"
    if basename.startswith("dump") or file_path.endswith(".lammpstrj") or file_path.endswith(".dump"):
        return "lammpstrj"
    if file_path.endswith(".dcd"):
        return "dcd"
    if file_path.endswith(".xtc"):
        return "xtc"
    if file_path.endswith(".trr"):
        return "trr"
    if file_path.endswith(".xyz"):
        return "xyz"
    if file_path.endswith(".pdb"):
        return "pdb"
    return "XDATCAR"


def main():
    parser = argparse.ArgumentParser(
        description="VMD-Anim: Headless MD Trajectory Animator (Tachyon Raytracing -> MP4/GIF)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("trajectory", help="Trajectory file (XDATCAR, LAMMPS dump, DCD, XTC, XYZ)")
    parser.add_argument("--topology", default=None, help="Optional topology file (POSCAR, PDB, PSF) if trajectory lacks element info")
    parser.add_argument("-o", "--output", default="trajectory.mp4", help="Output video or GIF file (.mp4, .gif)")
    parser.add_argument("-v", "--view", choices=["c", "a", "b", "iso"], default="iso", help="Camera projection axis")
    parser.add_argument("--first", type=int, default=0, help="First frame index (0-based)")
    parser.add_argument("--last", type=int, default=-1, help="Last frame index (-1 for end of trajectory)")
    parser.add_argument("--stride", type=int, default=1, help="Frame stride (skip frames)")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second in output video")
    parser.add_argument("--rep", choices=["cpk", "vdw", "licorice", "newcartoon", "quicksurf"], default="cpk")
    parser.add_argument("--pbc-box", action="store_true", help="Draw periodic boundary box")
    parser.add_argument("--width", type=int, default=1280, help="Frame width in pixels")
    parser.add_argument("--height", type=int, default=720, help="Frame height in pixels")
    parser.add_argument("--ao", type=float, default=0.6, help="Tachyon ambient occlusion skylight factor")
    parser.add_argument("--samples", type=int, default=4, help="Anti-aliasing rays per pixel for animation frames")
    parser.add_argument("--bg", choices=["white", "black"], default="white", help="Display background color")
    parser.add_argument("--vmd-bin", default=VMD_BIN_DEFAULT, help="Path to vmd executable")
    parser.add_argument("--tachyon-bin", default=TACHYON_BIN_DEFAULT, help="Path to tachyon executable")

    args = parser.parse_args()

    if not os.path.exists(args.trajectory):
        sys.stderr.write(f"Error: Trajectory file not found: {args.trajectory}\n")
        sys.exit(1)

    traj_type = detect_file_type(args.trajectory)

    with tempfile.TemporaryDirectory() as tmpdir:
        tcl_script = os.path.join(tmpdir, "anim.tcl")
        frame_dir = os.path.join(tmpdir, "frames")
        os.makedirs(frame_dir, exist_ok=True)

        # Build TCL script
        tcl = []
        tcl.append("package require pbctools")

        if args.topology and os.path.exists(args.topology):
            top_type = "POSCAR" if "poscar" in args.topology.lower() else "pdb"
            tcl.append(f"mol new {{{os.path.abspath(args.topology)}}} type {top_type} waitfor all")
            tcl.append(f"mol addfile {{{os.path.abspath(args.trajectory)}}} type {traj_type} waitfor all")
        else:
            tcl.append(f"mol new {{{os.path.abspath(args.trajectory)}}} type {traj_type} waitfor all")

        tcl.append("mol delrep 0 top")
        if args.rep == "cpk":
            tcl.append("mol representation CPK 0.45 0.18 24 24")
        elif args.rep == "vdw":
            tcl.append("mol representation VDW 0.8 24")
        elif args.rep == "licorice":
            tcl.append("mol representation Licorice 0.2 24 24")
        elif args.rep == "newcartoon":
            tcl.append("mol representation NewCartoon")
        elif args.rep == "quicksurf":
            tcl.append("mol representation QuickSurf 1.0 1.0 1.0 1.0")

        tcl.append("mol color Element")
        tcl.append("mol selection all")
        tcl.append("mol material AOShiny")
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

        # Loop over frames and export Tachyon dat files
        tcl.append(f"""
set numframes [molinfo top get numframes]
set first {args.first}
set last {args.last}
if {{$last < 0 || $last >= $numframes}} {{
    set last [expr {{$numframes - 1}}]
}}
set stride {args.stride}

puts "RENDERING_FRAMES: $first to $last with stride $stride (total in traj: $numframes)"

set frame_idx 0
for {{set i $first}} {{$i <= $last}} {{incr i $stride}} {{
    animate goto $i
    display update
    set out_dat [format "{frame_dir}/scene_%05d.dat" $frame_idx]
    render Tachyon $out_dat
    incr frame_idx
}}
puts "EXTRACTED_COUNT: $frame_idx"
exit
""")

        with open(tcl_script, "w") as f:
            f.write("\n".join(tcl))

        print(f"🎬 [VMD-Anim] Extracting trajectory frames headlessly...")
        vmd_res = subprocess.run([args.vmd_bin, "-dispdev", "text", "-e", tcl_script], capture_output=True, text=True)
        if vmd_res.returncode != 0:
            sys.stderr.write(f"VMD Error: {vmd_res.stderr}\n")

        dat_files = sorted(glob.glob(os.path.join(frame_dir, "scene_*.dat")))
        if not dat_files:
            sys.stderr.write("Error: No frame scene files were extracted.\n")
            sys.exit(1)

        print(f"🖼️ [VMD-Anim] Raytracing {len(dat_files)} frames via Tachyon (AO={args.ao}, samples={args.samples})...")
        rendered_pngs = []
        for i, dat_file in enumerate(dat_files):
            bmp_path = dat_file.replace(".dat", ".bmp")
            png_path = dat_file.replace(".dat", ".png")
            tach_cmd = [
                args.tachyon_bin,
                dat_file,
                "-fullshade",
                "-auto_skylight", str(args.ao),
                "-aasamples", str(args.samples),
                "-res", str(args.width), str(args.height),
                "-format", "BMP",
                "-o", bmp_path
            ]
            t_res = subprocess.run(tach_cmd, capture_output=True, text=True)
            if os.path.exists(bmp_path) and HAS_PIL:
                im = Image.open(bmp_path)
                im.save(png_path, "PNG")
                rendered_pngs.append(png_path)
                os.remove(bmp_path)
            if (i + 1) % 10 == 0 or (i + 1) == len(dat_files):
                print(f"   Raytraced {i + 1}/{len(dat_files)} frames...")

        if not rendered_pngs:
            sys.stderr.write("Error: Failed to raytrace animation frames.\n")
            sys.exit(1)

        # Output encoding
        out_ext = os.path.splitext(args.output)[1].lower()
        os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)

        if out_ext == ".gif":
            print(f"🎞️ [VMD-Anim] Assembling animated GIF: {args.output}")
            images = [Image.open(p) for p in rendered_pngs]
            duration_ms = int(1000 / args.fps)
            images[0].save(
                args.output,
                save_all=True,
                append_images=images[1:],
                duration=duration_ms,
                loop=0
            )
        else:
            # Default to MP4 via ffmpeg
            print(f"🎞️ [VMD-Anim] Encoding MP4 video via ffmpeg: {args.output}")
            ffmpeg_bin = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"
            input_pattern = os.path.join(frame_dir, "scene_%05d.png")
            ff_cmd = [
                ffmpeg_bin, "-y",
                "-framerate", str(args.fps),
                "-i", input_pattern,
                "-c:v", "libx264",
                "-profile:v", "high",
                "-crf", "18",
                "-pix_fmt", "yuv420p",
                args.output
            ]
            ff_res = subprocess.run(ff_cmd, capture_output=True, text=True)
            if ff_res.returncode != 0:
                sys.stderr.write(f"ffmpeg Error: {ff_res.stderr}\n")
                sys.exit(1)

        print(f"✨ [VMD-Anim] Video generated successfully: {args.output} ({len(rendered_pngs)} frames @ {args.fps} fps)")


if __name__ == "__main__":
    main()
