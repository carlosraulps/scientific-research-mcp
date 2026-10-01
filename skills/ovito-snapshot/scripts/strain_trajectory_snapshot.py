#!/usr/bin/env python3
"""
================================================================================
OVITO Strain Sweep & Trajectory Series Renderer (strain_trajectory_snapshot.py)
================================================================================
Renders a sequence of strained crystal structures or MD trajectory frames with:
1. Locked Global Viewport (FOV & Camera): Ensures zero frame-dilation or zoom jumps
   between strain states (e.g. -3% to +3%).
2. Unified Global Bader Net Charge Scale: Preserves a single, fixed colorbar range
   across all strain steps so color shifts reflect true electronic redistribution.
3. 2D-Carbon Calibrated Presets: Atomic sphere radius 0.38 A (C), 0.24 A (adsorbate H),
   bond cylinder 0.14 A, and C-C cutoff 1.70 A.
4. Publication Frame Sequence Output: Emits uniformly sized PNGs ready for
   the zero-dilation animation protocol.
================================================================================
"""

import argparse
import glob
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np

# Sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from publication_colorbar import generate_publication_colorbar
from render_ovito import VALENCE_ELECTRONS, parse_bader_charges


def extract_strain_percentage(filename: str) -> float:
    """Extracts numerical strain percentage from filename like POSCAR_strain_-2.5% or eps_0.03."""
    m = re.search(r"[-+]?\d*\.?\d+(?:%)?", filename)
    if m:
        val = m.group(0).rstrip("%")
        try:
            return float(val)
        except ValueError:
            pass
    return 0.0


def render_strain_series(
    structure_files: List[Union[str, Path]],
    output_dir: Union[str, Path] = "./strain_frames",
    bader_files: Optional[List[Union[str, Path]]] = None,
    net_charge: bool = True,
    view: str = "c",
    preset: str = "2d-carbon",
    width: int = 1920,
    height: int = 1080,
    renderer_type: str = "standard",
) -> List[Path]:
    """
    Renders a series of structures with identical camera FOV and unified color scaling.
    """
    import ovito
    from ovito.io import import_file
    from ovito.modifiers import CreateBondsModifier
    from ovito.vis import CoordinateTripodOverlay, Viewport

    out_path = Path(output_dir).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.mkdir(parents=True, exist_ok=True)

    sorted_files = sorted(structure_files, key=lambda p: extract_strain_percentage(Path(p).name))
    print(f"[ovito-strain] Processing {len(sorted_files)} structures in series...")

    # Step 1: Pre-calculate global charge bounds if Bader files are provided
    global_cmin, global_cmax = -0.30, 0.30
    all_net_charges = {}
    if bader_files:
        all_vals = []
        for s_file, b_file in zip(sorted_files, bader_files):
            b_path = Path(b_file)
            if b_path.exists():
                raw = parse_bader_charges(b_path)
                if raw:
                    try:
                        from ase.io import read as ase_read
                        atoms = ase_read(str(s_file))
                        syms = atoms.get_chemical_symbols()
                        net_q = [round(VALENCE_ELECTRONS.get(syms[i] if i < len(syms) else "C", 4.0) - q, 4) for i, q in enumerate(raw)]
                    except Exception:
                        net_q = [round(4.0 - q, 4) for q in raw]
                    all_net_charges[str(Path(s_file).resolve())] = net_q
                    all_vals.extend(net_q)
        if all_vals:
            max_abs = max(abs(min(all_vals)), abs(max(all_vals)))
            global_cmin = -round(max_abs, 2)
            global_cmax = round(max_abs, 2)
            print(f"[ovito-strain] Determined global unified net charge range: [{global_cmin:+.2f}, {global_cmax:+.2f}] e")

    # Step 2: Determine locked camera FOV using the first or central structure
    ref_file = sorted_files[len(sorted_files) // 2]
    ref_pipeline = import_file(str(ref_file))
    ref_data = ref_pipeline.compute()
    ref_box = ref_data.cell[...]
    # Calculate appropriate FOV with 15% margin
    max_extent = max(np.linalg.norm(ref_box[0, :3]), np.linalg.norm(ref_box[1, :3]))
    locked_fov = float(max_extent * 1.15)
    print(f"[ovito-strain] Locked camera FOV across all frames: {locked_fov:.2f} Angstroms")

    # Step 3: Render each structure with locked viewport
    rendered_frames = []
    camera_configs = {
        "a": ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
        "b": ((0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        "c": ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
        "iso": ((1.2, 1.5, 1.0), (0.0, 0.0, 1.0)),
    }
    cdir, cup = camera_configs.get(view.lower(), camera_configs["c"])

    ovito_renderer = None
    if renderer_type.lower() == "tachyon":
        try:
            from ovito.vis import TachyonRenderer
            ovito_renderer = TachyonRenderer(ambient_occlusion=True, shadows=True, antialiasing=True)
        except Exception:
            pass

    for idx, s_path in enumerate(sorted_files):
        s_file = Path(s_path).resolve()
        pipeline = import_file(str(s_file))

        # Bond modifiers (calibrated 2D carbon: 1.70 A)
        cutoff = 1.70 if preset.lower() == "2d-carbon" else 2.80
        pipeline.modifiers.append(CreateBondsModifier(cutoff=cutoff))

        # Distinct radii: C = 0.38 A, H = 0.24 A
        def apply_radii(frame, data):
            try:
                from ase.io import read as ase_read
                syms = ase_read(str(s_file)).get_chemical_symbols()
                radii = [0.24 if (i < len(syms) and syms[i] == "H") else 0.38 for i in range(data.particles.count)]
            except Exception:
                radii = [0.38] * data.particles.count
            data.particles_.create_property("Radius", data=radii)
            if data.particles.bonds:
                data.particles.bonds.vis.width = 0.14
        pipeline.modifiers.append(apply_radii)

        # Bader net charge modifier with locked range
        if str(s_file) in all_net_charges:
            net_q_vals = all_net_charges[str(s_file)]
            def assign_charge(frame, data):
                data.particles_.create_property("Charge", data=net_q_vals[:data.particles.count])
            pipeline.modifiers.append(assign_charge)

            from ovito.modifiers import ColorCodingModifier
            color_mod = ColorCodingModifier(
                property="Charge",
                gradient=ColorCodingModifier.BlueWhiteRed(),
                start_value=global_cmin,
                end_value=global_cmax,
            )
            pipeline.modifiers.append(color_mod)

        pipeline.add_to_scene()

        vp = Viewport(type=Viewport.Type.Ortho)
        vp.camera_dir = cdir
        vp.camera_up = cup
        vp.fov = locked_fov

        # Safe padded coordinate tripod
        tripod = CoordinateTripodOverlay(size=0.075, offset_x=0.06, offset_y=0.06)
        vp.overlays.append(tripod)

        frame_out = out_path / f"frame_{idx:03d}_{s_file.stem}.png"
        vp.render_image(
            filename=str(frame_out),
            size=(width, height),
            background=(1.0, 1.0, 1.0),
            renderer=ovito_renderer,
        )
        rendered_frames.append(frame_out)
        print(f"[{idx+1}/{len(sorted_files)}] Rendered locked frame: {frame_out.name}")

    # Generate unified standalone colorbar
    if all_net_charges:
        cbar_path = out_path / "unified_publication_colorbar.png"
        generate_publication_colorbar(
            vmin=global_cmin,
            vmax=global_cmax,
            output_path=cbar_path,
            label=r"Net Bader Charge $\Delta Q = Z_{\mathrm{valence}} - Q_{\mathrm{bader}}\ (e)$",
        )
        print(f"🎨 Generated unified STIX publication colorbar: {cbar_path}")

    print(f"✨ Successfully rendered {len(rendered_frames)} uniform strain frames in: {out_path}")
    return rendered_frames


def main():
    parser = argparse.ArgumentParser(
        description="Render strain series / trajectories in OVITO with locked FOV & zero-dilation"
    )
    parser.add_argument("pattern", help="Glob pattern or directory containing structure files (e.g. './strain_poscars/POSCAR*')")
    parser.add_argument("-o", "--output-dir", default="./strain_frames", help="Output directory for frame sequence")
    parser.add_argument("-v", "--view", choices=["a", "b", "c", "iso"], default="c", help="Crystallographic view (default: c)")
    parser.add_argument("--bader-pattern", help="Optional glob pattern for corresponding ACF.dat files")
    parser.add_argument("--preset", default="2d-carbon", choices=["2d-carbon", "ball-stick"], help="Styling preset (default: 2d-carbon)")
    parser.add_argument("--width", type=int, default=1920, help="Frame width in px (default: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="Frame height in px (default: 1080)")
    parser.add_argument("--renderer", choices=["standard", "tachyon"], default="standard", help="Renderer type")

    args = parser.parse_args()

    if os.path.isdir(args.pattern):
        files = sorted(glob.glob(os.path.join(args.pattern, "POSCAR*")) or glob.glob(os.path.join(args.pattern, "*.vasp")))
    else:
        files = sorted(glob.glob(args.pattern))

    if not files:
        print(f"Error: No files matched pattern '{args.pattern}'", file=sys.stderr)
        sys.exit(1)

    bader_files = None
    if args.bader_pattern:
        bader_files = sorted(glob.glob(args.bader_pattern))

    render_strain_series(
        structure_files=files,
        output_dir=args.output_dir,
        bader_files=bader_files,
        view=args.view,
        preset=args.preset,
        width=args.width,
        height=args.height,
        renderer_type=args.renderer,
    )


if __name__ == "__main__":
    main()
