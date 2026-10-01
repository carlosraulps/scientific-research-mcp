#!/usr/bin/env python3
"""
================================================================================
Automated Headless 2D CDD Planar Contour Visualizer for XCrySDen (xcrysden_cdd.py)
================================================================================
Executes headless 2D Charge Density Difference (CDD) planar contour mapping:
1. Translates volumetric data (cdd.vasp, structure.xsf, density.cube) into XSF format.
2. Emits standardized TCL headless scripting routines:
   - Sets BallStick display mode, view c (looking down z), and zoom 1.2.
   - Slices 2D contours through basal plane (default z=0.50) with 35 isolines and BWR colormap.
   - Dumps offscreen framebuffer.
3. Automatically inverts black background to publication white with edge-blending
   antialiasing and crops uniform whitespace margins down to 30px padding.
================================================================================
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional, Union

# Sibling script imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from postprocess_image import invert_black_background
from xcrysden_auto import convert_to_xsf, find_xcrysden_binary


def build_cdd_tcl_script(
    xsf_path: Path,
    output_png: Path,
    plane: str = "xy",
    coord: float = 0.50,
    isolines: int = 35,
    colormap: str = "bwr",
    zoom: float = 1.2,
    view: str = "c",
) -> str:
    """
    Constructs the headless TCL script for 2D planar contour extraction.
    """
    tcl_lines = [
        f"scripting::open --xsf \"{xsf_path}\"",
        "scripting::display_mode BallStick",
        f"scripting::zoom {zoom}",
        f"scripting::view {view}",
        f"scripting::slice2d --plane {plane} --coord {coord:0.4f} --isoline {isolines} --colormap {colormap}",
        f"scripting::dump_frame \"{output_png}\"",
        "scripting::exit",
        "",
    ]
    return "\n".join(tcl_lines)


def run_cdd_slice(
    input_file: Union[str, Path],
    output_file: Optional[Union[str, Path]] = None,
    plane: str = "xy",
    coord: float = 0.50,
    isolines: int = 35,
    colormap: str = "bwr",
    zoom: float = 1.2,
    view: str = "c",
    timeout: float = 18.0,
    export_script: Optional[Union[str, Path]] = None,
) -> Optional[Path]:
    """
    Renders 2D CDD planar contour headlessly through XCrySDen and whitens the background.
    """
    in_path = Path(input_file).resolve()
    if not in_path.exists():
        print(f"Error: Input file does not exist: {in_path}", file=sys.stderr)
        return None

    xc_bin = find_xcrysden_binary()
    if not xc_bin:
        print("Error: XCrySDen binary not found on system PATH.", file=sys.stderr)
        return None

    out_final = Path(output_file).resolve() if output_file else in_path.parent / f"{in_path.stem}_2d_cdd_{plane}.png"
    out_final.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="xc_cdd_") as tmpdir:
        tmp_dir = Path(tmpdir)
        # Convert to XSF if necessary
        if in_path.suffix.lower() == ".xsf":
            xsf_path = in_path
        else:
            xsf_path = tmp_dir / f"{in_path.stem}.xsf"
            print(f"[xcrysden-cdd] Converting {in_path.name} to XSF format...")
            convert_to_xsf(in_path, xsf_path)

        raw_png = tmp_dir / "raw_frame.png"
        tcl_path = tmp_dir / "render_2d_cdd.tcl"
        tcl_content = build_cdd_tcl_script(
            xsf_path=xsf_path,
            output_png=raw_png,
            plane=plane,
            coord=coord,
            isolines=isolines,
            colormap=colormap,
            zoom=zoom,
            view=view,
        )
        tcl_path.write_text(tcl_content, encoding="utf-8")

        if export_script:
            shutil.copy2(tcl_path, Path(export_script).resolve())
            print(f"📝 Exported TCL script: {export_script}")

        # Headless command execution
        cmd = [xc_bin, "--xsf", str(xsf_path), "--script", str(tcl_path)]
        env = os.environ.copy()
        run_cmd = cmd
        if sys.platform.startswith("linux") and not env.get("DISPLAY"):
            xvfb = shutil.which("xvfb-run")
            if xvfb:
                run_cmd = [xvfb, "-a", "-s", "-screen 0 2400x1800x24"] + cmd
            else:
                print("Warning: DISPLAY is not set and xvfb-run is missing. Render may fail.", file=sys.stderr)

        print(f"[xcrysden-cdd] Executing headless 2D CDD slicing (plane={plane}, coord={coord}, isolines={isolines})...")
        proc = subprocess.Popen(run_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)

        start_time = time.time()
        success = False
        try:
            while time.time() - start_time < timeout:
                if raw_png.exists() and raw_png.stat().st_size > 1500:
                    success = True
                    break
                time.sleep(0.4)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=1.0)

        if success and raw_png.exists():
            # Apply Publication Background Whitening Pipeline
            print(f"[xcrysden-cdd] Whitening background & applying fringe antialiasing...")
            invert_black_background(
                input_image=raw_png,
                output_image=out_final,
                dark_threshold=25,
                blend_width=35,
                trim_borders=True,
                border_padding=30,
            )
            print(f"🎉 2D CDD Planar Contour Complete: {out_final} ({out_final.stat().st_size / 1024:.1f} KB)")
            return out_final
        else:
            print(f"❌ Failed to extract 2D CDD frame within {timeout}s timeout.", file=sys.stderr)
            return None


def main():
    parser = argparse.ArgumentParser(
        description="Headless 2D Charge Density Difference (CDD) Planar Contour Visualizer for XCrySDen"
    )
    parser.add_argument("input", help="Input volumetric file (cdd.vasp, density.xsf, CHGCAR, .cube)")
    parser.add_argument("-o", "--output", help="Output PNG file path")
    parser.add_argument("--plane", choices=["xy", "xz", "yz"], default="xy", help="Slice plane (default: xy)")
    parser.add_argument("--coord", type=float, default=0.50, help="Fractional normal coordinate of slice (default: 0.50)")
    parser.add_argument("--isolines", type=int, default=35, help="Number of contour lines (default: 35)")
    parser.add_argument("--colormap", default="bwr", help="Contour colormap (bwr, rainbow, etc.)")
    parser.add_argument("--zoom", type=float, default=1.2, help="Camera zoom level (default: 1.2)")
    parser.add_argument("-v", "--view", choices=["a", "b", "c", "iso"], default="c", help="View orientation (default: c)")
    parser.add_argument("--export-script", help="Save the generated TCL script for manual inspection")
    parser.add_argument("--timeout", type=float, default=18.0, help="Max wait timeout in seconds")

    args = parser.parse_args()
    run_cdd_slice(
        input_file=args.input,
        output_file=args.output,
        plane=args.plane,
        coord=args.coord,
        isolines=args.isolines,
        colormap=args.colormap,
        zoom=args.zoom,
        view=args.view,
        timeout=args.timeout,
        export_script=args.export_script,
    )


if __name__ == "__main__":
    main()
