#!/usr/bin/env python3
"""
VESTA GUI Automation & Multi-Axis Crystal Capture for X11.
Automates window launching, crystallographic axis alignment (a, b, c), and window capture.
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def automate_vesta(
    input_file: str,
    view: str = "all",
    output_dir: str = ".",
    output_prefix: str = None,
    timeout: float = 4.0,
    keep_open: bool = False,
):
    import pyautogui
    from Xlib import display, X

    display_env = os.environ.get("DISPLAY")
    if not display_env:
        print("Error: DISPLAY environment variable is not set. VESTA requires an active X11 display.", file=sys.stderr)
        sys.exit(1)

    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    prefix = output_prefix or input_path.stem

    print(f"Launching VESTA with structure: {input_path.name}...")
    proc = subprocess.Popen(["vesta", str(input_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    rendered_files = []

    try:
        d = display.Display()
        root = d.screen().root

        target_window = None
        start_time = time.time()

        # Poll for the VESTA window with matching title or class
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
        print(f"Located VESTA Window: 0x{target_window.id:x} ({geom.width}x{geom.height})")

        # Raise and focus window
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
                # VESTA hotkeys 'a', 'b', 'c' orient perpendicular to axes
                pyautogui.press(v)
                time.sleep(0.4)

            out_file = out_dir / f"{prefix}_vesta_view_{v}.png"
            subprocess.run(["import", "-window", hex(target_window.id), str(out_file)], check=True)
            print(f"Saved: {out_file} (view={v})")
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
            print("VESTA process cleanly terminated.")

    return rendered_files


def main():
    parser = argparse.ArgumentParser(
        description="Automate VESTA GUI on X11 to align and capture crystal structures."
    )
    parser.add_argument("input", help="Path to input crystal file (POSCAR, CIF, XSF, etc.)")
    parser.add_argument(
        "--view",
        "-v",
        choices=["a", "b", "c", "all"],
        default="all",
        help="View orientation along crystal axis (a, b, c, or all; default: all)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Output directory for captured PNGs (default: current directory)",
    )
    parser.add_argument("--prefix", "-p", help="Output file prefix (default: input file stem)")
    parser.add_argument(
        "--timeout",
        type=float,
        default=4.0,
        help="Timeout in seconds to wait for VESTA window to initialize (default: 4.0)",
    )
    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep the VESTA GUI open after taking snapshots",
    )

    args = parser.parse_args()

    automate_vesta(
        input_file=args.input,
        view=args.view,
        output_dir=args.output_dir,
        output_prefix=args.prefix,
        timeout=args.timeout,
        keep_open=args.keep_open,
    )


if __name__ == "__main__":
    main()
