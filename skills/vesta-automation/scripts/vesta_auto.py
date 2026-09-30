#!/usr/bin/env python3
"""
================================================================================
VESTA Automation & Headless High-Resolution Renderer
================================================================================
Automates VESTA on both macOS and Linux/X11:
1. Native Terminal CLI Mode: Offscreen high-resolution rendering via
   `VESTA -open <file> [-style <style>] -export_img scale=<N> <out.png>`.
2. Periodic Boundary Spillover Fix: Automatically injects 'Bound = 0' into
   generated project/style wrappers to prevent the 800-atom duplicate explosion.
3. Dual-Isosurface Support: Native CDD (Charge Density Difference) rendering
   with custom positive/negative isosurface levels and colors.
4. Robust Process Lifecycle: Monitors output file creation and size, then
   cleanly terminates background VESTA instances.
5. Headless Server Support: Automatically falls back to `xvfb-run -a` when
   DISPLAY is not configured in Linux cluster environments.
6. Desktop GUI Automation Mode: Interactive X11 window inspection fallback
   using python-xlib and pyautogui.
================================================================================
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple, Union

# Add current script directory for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vstd_generator import generate_vesta_project


def find_vesta_binary() -> Optional[str]:
    """
    Locates the VESTA binary across macOS and Linux installations.
    CRITICAL: Resolves symlinks (os.path.realpath) so VESTA can locate
    its bundled internal resources (e.g. elements.ini).
    """
    candidates = [
        shutil.which("vesta"),
        shutil.which("VESTA"),
        "/Applications/VESTA.app/Contents/MacOS/VESTA",
        "/opt/VESTA/VESTA",
        "/usr/local/bin/vesta",
        "/usr/bin/VESTA",
        os.path.expanduser("~/opt/VESTA/VESTA"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            resolved = os.path.realpath(c)
            if os.path.exists(resolved) and os.access(resolved, os.X_OK):
                return resolved
    return None


def render_vesta_native(
    input_file: Union[str, Path],
    output_image: Union[str, Path],
    scale: int = 2,
    timeout: float = 12.0,
    style_file: Optional[Union[str, Path]] = None,
    headless: bool = True,
) -> bool:
    """
    Renders an image headlessly using VESTA's native terminal export flags.
    """
    vesta_bin = find_vesta_binary()
    if not vesta_bin:
        print("Error: VESTA binary not found on system PATH or standard directories.", file=sys.stderr)
        return False

    out_path = Path(output_image).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    cmd = [vesta_bin, "-open", str(Path(input_file).resolve())]
    if style_file and Path(style_file).exists():
        cmd.extend(["-style", str(Path(style_file).resolve())])
    cmd.extend(["-export_img", f"scale={scale}", str(out_path)])

    # Check for X11 / xvfb requirement on Linux
    env = os.environ.copy()
    run_cmd = cmd
    if sys.platform.startswith("linux") and not env.get("DISPLAY"):
        xvfb = shutil.which("xvfb-run")
        if xvfb and headless:
            run_cmd = [xvfb, "-a", "-s", "-screen 0 1920x1080x24"] + cmd
        else:
            print("Warning: DISPLAY is not set and xvfb-run is unavailable. VESTA may fail.", file=sys.stderr)

    print(f"[VESTA CLI] Launching: {' '.join(run_cmd)}")
    proc = subprocess.Popen(
        run_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )

    start_time = time.time()
    success = False

    try:
        while time.time() - start_time < timeout:
            if out_path.exists() and out_path.stat().st_size > 1000:
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

    if success:
        print(f"[VESTA CLI] Saved: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")
    else:
        print(f"[VESTA CLI] Warning: Timeout waiting for {out_path}", file=sys.stderr)

    return success


def automate_vesta_gui(
    input_file: Union[str, Path],
    view: str = "all",
    output_dir: Union[str, Path] = ".",
    output_prefix: Optional[str] = None,
    timeout: float = 6.0,
    keep_open: bool = False,
) -> List[str]:
    """
    Fallback GUI automation using X11 window introspection and pyautogui.
    """
    display_env = os.environ.get("DISPLAY")
    if not display_env:
        print("Error: DISPLAY environment variable is not set. GUI automation requires an active X11 display.", file=sys.stderr)
        sys.exit(1)

    import pyautogui
    from Xlib import display, X

    vesta_bin = find_vesta_binary() or "vesta"
    input_path = Path(input_file).resolve()
    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_prefix or input_path.stem

    print(f"[VESTA GUI] Launching VESTA with structure: {input_path.name}...")
    proc = subprocess.Popen([vesta_bin, str(input_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rendered_files = []

    try:
        d = display.Display()
        root = d.screen().root
        target_window = None
        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(0.5)
            for c in root.query_tree().children:
                try:
                    name = c.get_wm_name() or ""
                    cls = c.get_wm_class() or ()
                    geom = c.get_geometry()
                    if ("VESTA" in name or any("VESTA" in str(x) for x in cls)) and geom.width > 200:
                        target_window = c
                        break
                except Exception:
                    continue
            if target_window:
                break

        if not target_window:
            print(f"Error: Could not locate VESTA window after {timeout} seconds.", file=sys.stderr)
            sys.exit(1)

        geom = target_window.get_geometry()
        print(f"[VESTA GUI] Located Window: 0x{target_window.id:x} ({geom.width}x{geom.height})")

        try:
            target_window.set_input_focus(X.RevertToParent, X.CurrentTime)
            target_window.configure(stack_mode=X.Above)
            d.sync()
        except Exception:
            pass
        time.sleep(0.5)

        views_to_capture = ["a", "b", "c"] if view.lower() == "all" else [view.lower()]
        for v in views_to_capture:
            if v in ["a", "b", "c"]:
                pyautogui.press(v)
                time.sleep(0.4)

            out_file = out_dir / f"{prefix}_vesta_{v}.png"
            subprocess.run(["import", "-window", hex(target_window.id), str(out_file)], check=True)
            print(f"[VESTA GUI] Saved: {out_file} (view={v})")
            rendered_files.append(str(out_file))

        if keep_open:
            print("VESTA window left open for interactive inspection.")

    finally:
        if not keep_open and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()

    return rendered_files


def run_vesta_pipeline(
    input_file: Union[str, Path],
    view: str = "all",
    output_dir: Union[str, Path] = ".",
    output_prefix: Optional[str] = None,
    scale: int = 2,
    isolate_cell: bool = True,
    cdd: bool = False,
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    gui: bool = False,
    keep_open: bool = False,
    timeout: float = 12.0,
) -> List[str]:
    """
    Unified high-level rendering entry point with automatic CLI prioritization
    and primitive unit-cell boundary containment.
    """
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_prefix or input_path.stem

    # If GUI mode is explicitly requested, run GUI automation
    if gui or keep_open:
        return automate_vesta_gui(
            input_file=input_path,
            view=view,
            output_dir=out_dir,
            output_prefix=prefix,
            timeout=timeout,
            keep_open=keep_open,
        )

    # Native CLI execution (default, fast, headless)
    views_to_render = ["a", "b", "c", "iso"] if view.lower() == "all" else [view.lower()]
    rendered_files = []

    for v in views_to_render:
        out_img = out_dir / f"{prefix}_vesta_{v}.png"
        file_to_open = input_path
        temp_vesta = None

        # Solve the 800-atom spillover bug or orient via programmatic .vesta wrapper
        if isolate_cell or cdd or v in ["a", "b", "c", "iso"]:
            temp_vesta = Path(f"/tmp/vesta_wrap_{os.getpid()}_{v}.vesta")
            generate_vesta_project(
                data_file=input_path,
                output_vesta_path=temp_vesta,
                view=v,
                bound_mode=0 if isolate_cell else 1,
                cdd_mode=cdd,
                pos_level=pos_level,
                neg_level=neg_level,
            )
            file_to_open = temp_vesta

        ok = render_vesta_native(
            input_file=file_to_open,
            output_image=out_img,
            scale=scale,
            timeout=timeout,
        )

        if temp_vesta and temp_vesta.exists():
            temp_vesta.unlink()

        if ok:
            rendered_files.append(str(out_img))
        else:
            # If native CLI failed on Linux and DISPLAY is available, try GUI fallback
            if sys.platform.startswith("linux") and os.environ.get("DISPLAY"):
                print(f"[VESTA] Native export failed. Attempting GUI fallback for view {v}...", file=sys.stderr)
                gui_res = automate_vesta_gui(
                    input_file=input_path,
                    view=v,
                    output_dir=out_dir,
                    output_prefix=prefix,
                    timeout=timeout,
                )
                rendered_files.extend(gui_res)

    return rendered_files


def main():
    parser = argparse.ArgumentParser(
        description="Automate VESTA for High-Resolution, Borderless, Spillover-Free Crystal & CDD Rendering."
    )
    parser.add_argument("input", help="Path to input crystal or volumetric data file (POSCAR, CIF, XSF, CUBE, cdd.vasp)")
    parser.add_argument(
        "--view",
        "-v",
        choices=["a", "b", "c", "iso", "all"],
        default="all",
        help="View angle along crystal axis (a, b, c, iso, or all; default: all)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Output directory for generated PNG images (default: current dir)",
    )
    parser.add_argument("--prefix", "-p", help="Output file prefix (default: input file stem)")
    parser.add_argument(
        "--scale",
        "-s",
        type=int,
        default=2,
        help="Resolution scaling multiplier (e.g. scale=2 produces 4K UHD, scale=3 for 600 DPI print; default: 2)",
    )
    parser.add_argument(
        "--no-isolate",
        action="store_true",
        help="Disable automatic Bound=0 cell isolation (allow periodic bond extension)",
    )
    parser.add_argument(
        "--cdd",
        action="store_true",
        help="Enable dual-isosurface rendering for Charge Density Difference (CDD)",
    )
    parser.add_argument(
        "--pos-level",
        type=float,
        default=0.005,
        help="Positive CDD accumulation isosurface cutoff (default: 0.005)",
    )
    parser.add_argument(
        "--neg-level",
        type=float,
        default=-0.005,
        help="Negative CDD depletion isosurface cutoff (default: -0.005)",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Force interactive X11 desktop GUI automation mode instead of native CLI",
    )
    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep the VESTA GUI open for interactive inspection",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=12.0,
        help="Timeout in seconds for VESTA execution (default: 12.0s)",
    )

    args = parser.parse_args()

    results = run_vesta_pipeline(
        input_file=args.input,
        view=args.view,
        output_dir=args.output_dir,
        output_prefix=args.prefix,
        scale=args.scale,
        isolate_cell=not args.no_isolate,
        cdd=args.cdd,
        pos_level=args.pos_level,
        neg_level=args.neg_level,
        gui=args.gui,
        keep_open=args.keep_open,
        timeout=args.timeout,
    )

    print(f"\n[+] Rendered {len(results)} image(s) successfully.")


if __name__ == "__main__":
    main()
