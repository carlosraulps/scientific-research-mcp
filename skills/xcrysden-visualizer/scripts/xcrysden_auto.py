#!/usr/bin/env python3
"""
XCrySDen Automation & Visualizer Script for X11.
Supports Crystal Structures (XSF/POSCAR/CIF), Fermi Surfaces (BXSF), and Density Isosurfaces.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def convert_to_xsf(input_path: Path, output_xsf: Path):
    """Convert POSCAR or CIF to XSF format using ASE."""
    try:
        from ase.io import read, write
        atoms = read(str(input_path))
        write(str(output_xsf), atoms)
        return True
    except Exception as e:
        print(f"Warning: Could not convert {input_path} to XSF via ASE: {e}", file=sys.stderr)
        return False


def run_xcrysden(
    input_file: str,
    output_image: str = None,
    timeout: float = 4.0,
    keep_open: bool = False,
):
    import pyautogui
    from Xlib import display, X

    display_env = os.environ.get("DISPLAY")
    if not display_env:
        print("Error: DISPLAY environment variable is not set. XCrySDen requires an active X11 display.", file=sys.stderr)
        sys.exit(1)

    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    temp_xsf = None
    file_to_load = input_path
    ext = input_path.suffix.lower()

    # Determine XCrySDen input flag
    if ext in [".xsf", ".axsf"]:
        flag = "--xsf"
    elif ext == ".bxsf":
        flag = "--bxsf"
    elif ext in [".cube"]:
        flag = "--cube"
    elif ext in [".pwi", ".in"]:
        flag = "--pwi"
    elif ext in [".pwo", ".out"]:
        flag = "--pwo"
    else:
        # Convert POSCAR, CIF, XYZ to temporary XSF
        temp_xsf = Path(f"/tmp/{input_path.stem}_{os.getpid()}.xsf")
        if convert_to_xsf(input_path, temp_xsf):
            file_to_load = temp_xsf
            flag = "--xsf"
        else:
            print(f"Error: Unsupported format for XCrySDen: {input_path}", file=sys.stderr)
            sys.exit(1)

    out_file = Path(output_image).resolve() if output_image else Path(f"{input_path.stem}_xcrysden.png").resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    tcl_script = Path(f"/tmp/xc_render_{os.getpid()}.tcl")
    tcl_script.write_text(f"""
scripting::displayMode3D BallStick
scripting::zoom 25% 6
update
dumpWindow .mesa {out_file}
exit
""")

    cmd = ["xcrysden", flag, str(file_to_load), "--script", str(tcl_script)]
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Saved: {out_file}")

    if tcl_script.exists():
        tcl_script.unlink()
    if temp_xsf and temp_xsf.exists():
        temp_xsf.unlink()

    return str(out_file)


def main():
    parser = argparse.ArgumentParser(
        description="Automate XCrySDen on X11 for structures, Fermi surfaces, and charge density."
    )
    parser.add_argument("input", help="Path to input file (POSCAR, CIF, XSF, BXSF, CUBE, PWI/PWO)")
    parser.add_argument(
        "--output",
        "-o",
        help="Output PNG image path (default: <stem>_xcrysden.png)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Seconds to wait for window initialization (default: 5.0)",
    )
    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep XCrySDen GUI open after snapshot",
    )

    args = parser.parse_args()
    run_xcrysden(
        input_file=args.input,
        output_image=args.output,
        timeout=args.timeout,
        keep_open=args.keep_open,
    )


if __name__ == "__main__":
    main()
