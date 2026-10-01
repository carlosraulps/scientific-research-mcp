#!/usr/bin/env python3
"""
================================================================================
Automated VESTA 3D Charge Density Difference (CDD) Renderer (vesta_cdd.py)
================================================================================
One-command production of publication-quality 3D Charge Density Difference graphics:
1. Automatically configures dual isosurfaces:
   - Accumulation (\\Delta\\rho > 0): Gold / Yellow (#f1c40f, [241, 196, 15])
   - Depletion (\\Delta\\rho < 0): Cyan / Sky Blue (#00b4d8, [0, 180, 216])
   - Calibrated 60% opacity (alpha=0.60) for clear core atom visibility.
2. Injects Bound = 0 and SEARCH_BOUNDARY = 0 into the .vesta project wrapper.
3. Renders headlessly with VESTA native CLI (-export_img scale=<N>) with xvfb fallback.
4. Auto-trims uniform white border margins to 30px padding.
================================================================================
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, Union
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_vstd import extract_species_from_structure, generate_vesta_project_content
from vesta_auto import find_vesta_binary


def trim_whitespace(img_path: Path, padding: int = 30) -> None:
    """Trims uniform border whitespace down to padding pixels."""
    try:
        img = Image.open(img_path).convert("RGBA")
        arr = np.array(img)
        # Check against pure white or transparent
        diff = np.abs(arr[:, :, :3].astype(np.int32) - 255)
        is_content = np.any(diff > 15, axis=2)
        if not np.any(is_content):
            return
        coords = np.argwhere(is_content)
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        H, W = arr.shape[:2]
        x0 = max(0, x0 - padding)
        y0 = max(0, y0 - padding)
        x1 = min(W, x1 + padding)
        y1 = min(H, y1 + padding)
        cropped = img.crop((x0, y0, x1, y1))
        cropped.save(img_path)
    except Exception as e:
        print(f"[vesta-cdd] Warning during autotrim: {e}", file=sys.stderr)


def render_cdd(
    cdd_file: Union[str, Path],
    output_image: Optional[Union[str, Path]] = None,
    view: str = "c",
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    opacity: float = 0.60,
    scale: int = 2,
    timeout: float = 15.0,
) -> Optional[Path]:
    """
    Renders 3D Charge Density Difference headlessly using VESTA.
    """
    cdd_path = Path(cdd_file).resolve()
    if not cdd_path.exists():
        print(f"Error: CDD input file not found: {cdd_path}", file=sys.stderr)
        return None

    vesta_bin = find_vesta_binary()
    if not vesta_bin:
        print("Error: VESTA binary not found on system PATH.", file=sys.stderr)
        return None

    out_img = Path(output_image).resolve() if output_image else cdd_path.parent / f"{cdd_path.stem}_cdd_{view}.png"
    out_img.parent.mkdir(parents=True, exist_ok=True)
    if out_img.exists():
        out_img.unlink()

    # Step 1: Detect species and generate temporary .vesta project
    species = extract_species_from_structure(cdd_path)
    temp_vesta = cdd_path.parent / f".temp_cdd_{view}.vesta"
    content = generate_vesta_project_content(
        data_file_path=cdd_path,
        species=species,
        view=view,
        bound_mode=0,
        search_boundary=0,
        cdd_mode=True,
        pos_level=pos_level,
        neg_level=neg_level,
        opacity=opacity,
        title=f"CDD_{cdd_path.stem}",
    )
    temp_vesta.write_text(content, encoding="utf-8")

    # Step 2: Build native CLI export command
    cmd = [vesta_bin, "-open", str(temp_vesta), "-export_img", f"scale={scale}", str(out_img)]

    env = os.environ.copy()
    run_cmd = cmd
    if sys.platform.startswith("linux") and not env.get("DISPLAY"):
        xvfb = shutil.which("xvfb-run")
        if xvfb:
            run_cmd = [xvfb, "-a", "-s", "-screen 0 3840x2160x24"] + cmd
        else:
            print("Warning: DISPLAY is not set and xvfb-run is missing. Render may fail.", file=sys.stderr)

    print(f"[vesta-cdd] Rendering view '{view}' (Scale={scale}, pos={pos_level}, neg={neg_level})...")
    proc = subprocess.Popen(run_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)

    start_time = time.time()
    success = False
    try:
        while time.time() - start_time < timeout:
            if out_img.exists() and out_img.stat().st_size > 2000:
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
        # Cleanup temporary .vesta file
        if temp_vesta.exists():
            temp_vesta.unlink()

    if success and out_img.exists():
        trim_whitespace(out_img, padding=30)
        print(f"🎉 3D CDD Render Complete: {out_img} ({out_img.stat().st_size / 1024:.1f} KB)")
        return out_img
    else:
        print(f"❌ Failed to render CDD image within {timeout}s timeout.", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Headless 3D Charge Density Difference (CDD) Renderer for VESTA"
    )
    parser.add_argument("input", help="Input CDD volumetric file (cdd.vasp, CHGCAR, cdd.cube)")
    parser.add_argument("-o", "--output", help="Output PNG image path")
    parser.add_argument("-v", "--view", choices=["a", "b", "c", "iso"], default="c", help="Crystallographic view (default: c)")
    parser.add_argument("--pos-level", type=float, default=0.005, help="Positive cutoff for accumulation (gold/yellow, default: 0.005)")
    parser.add_argument("--neg-level", type=float, default=-0.005, help="Negative cutoff for depletion (cyan/sky blue, default: -0.005)")
    parser.add_argument("--opacity", type=float, default=0.60, help="Isosurface opacity (default: 0.60)")
    parser.add_argument("--scale", "-s", type=int, default=2, help="Resolution scale: 1=1080p, 2=4K, 3=600DPI (default: 2)")
    parser.add_argument("--timeout", type=float, default=15.0, help="Max wait timeout in seconds")

    args = parser.parse_args()
    render_cdd(
        cdd_file=args.input,
        output_image=args.output,
        view=args.view,
        pos_level=args.pos_level,
        neg_level=args.neg_level,
        opacity=args.opacity,
        scale=args.scale,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
