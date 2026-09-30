#!/usr/bin/env python3
"""
Headless Crystal Structure & Trajectory Renderer using OVITO and ASE.
Renders high-resolution orthographic or perspective snapshots along crystallographic axes.
"""

import argparse
import os
import sys
from pathlib import Path


def render_structure(
    input_file: str,
    view: str = "all",
    output_dir: str = ".",
    output_prefix: str = None,
    width: int = 1920,
    height: int = 1080,
    projection: str = "ortho",
    supercell: list = None,
    create_bonds: bool = True,
    bond_cutoff: float = 3.0,
    particle_radius: float = None,
    bond_width: float = None,
    polyhedra: bool = False,
    tripod: bool = True,
    background: str = "white",
    bader_file: str = None,
    charge_range: list = None,
    bader_colormap: str = "BlueWhiteRed",
    no_cell: bool = False,
):
    import ovito
    from ovito.io import import_file
    from ovito.modifiers import (
        CommonNeighborAnalysisModifier,
        CreateBondsModifier,
        ReplicateModifier,
    )
    from ovito.vis import CoordinateTripodOverlay, Viewport

    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    prefix = output_prefix or input_path.stem

    pipeline = import_file(str(input_path))

    # Apply Supercell Replicate if requested
    if supercell and len(supercell) == 3:
        nx, ny, nz = [int(x) for x in supercell]
        if nx > 1 or ny > 1 or nz > 1:
            pipeline.modifiers.append(ReplicateModifier(num_x=nx, num_y=ny, num_z=nz))

    # Add Bond Modifier
    if create_bonds:
        pipeline.modifiers.append(CreateBondsModifier(cutoff=bond_cutoff))

    # Custom styling for particle radius and bond width (ball-and-stick)
    if particle_radius or bond_width:
        def style_vis(frame, data):
            if particle_radius:
                data.particles_.create_property("Radius", data=[particle_radius] * data.particles.count)
            if data.particles.bonds and bond_width:
                data.particles.bonds.vis.width = bond_width
        pipeline.modifiers.append(style_vis)

    # Add Polyhedral Analysis if requested
    if polyhedra:
        try:
            from ovito.modifiers import PolyhedralTemplateMatchingModifier
            pipeline.modifiers.append(PolyhedralTemplateMatchingModifier())
        except Exception:
            pass

    # Assign Bader charge property and color coding if requested
    color_legend_overlay = None
    if bader_file:
        bader_path = Path(bader_file).resolve()
        if bader_path.exists():
            charges = []
            with open(bader_path, "r") as f:
                blines = [l.strip() for l in f if l.strip()]
            for bline in blines:
                parts = bline.split()
                if len(parts) >= 5 and parts[0].isdigit():
                    # ACF.dat format: # X Y Z CHARGE
                    charges.append(float(parts[4]))
                elif len(parts) == 1:
                    try:
                        charges.append(float(parts[0]))
                    except ValueError:
                        pass

            if charges:
                def assign_charge_prop(frame, data):
                    data.particles_.create_property("Charge", data=charges[:data.particles.count])
                pipeline.modifiers.append(assign_charge_prop)

                from ovito.modifiers import ColorCodingModifier
                from ovito.vis import ColorLegendOverlay

                # Determine colormap gradient
                cmap_grad = ColorCodingModifier.BlueWhiteRed()
                if bader_colormap.lower() == "viridis":
                    cmap_grad = ColorCodingModifier.Viridis()
                elif bader_colormap.lower() == "magma":
                    cmap_grad = ColorCodingModifier.Magma()

                c_min = charge_range[0] if (charge_range and len(charge_range) == 2) else min(charges)
                c_max = charge_range[1] if (charge_range and len(charge_range) == 2) else max(charges)

                color_mod = ColorCodingModifier(
                    property="Charge",
                    gradient=cmap_grad,
                    start_value=c_min,
                    end_value=c_max,
                )
                pipeline.modifiers.append(color_mod)
                color_legend_overlay = ColorLegendOverlay(
                    modifier=color_mod,
                    title="Bader Charge (e)",
                    ticks_enabled=True,
                )
    # Hide simulation cell box if requested
    if no_cell:
        def hide_cell_modifier(frame, data):
            if data.cell:
                data.cell.vis.enabled = False
        pipeline.modifiers.append(hide_cell_modifier)

    pipeline.add_to_scene()

    # Configure background color
    bg_colors = {
        "white": (1.0, 1.0, 1.0),
        "black": (0.0, 0.0, 0.0),
        "gray": (0.2, 0.2, 0.2),
        "transparent": None,
    }
    bg = bg_colors.get(background.lower(), (1.0, 1.0, 1.0))

    # Define camera vectors (direction, up_vector)
    # Looking down crystallographic axes
    camera_configs = {
        "a": ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),   # View along a-axis (yz plane)
        "b": ((0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),   # View along b-axis (xz plane)
        "c": ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),   # View along c-axis (xy plane)
        "iso": ((1.2, 1.5, 1.0), (0.0, 0.0, 1.0)), # General 3D perspective
    }

    views_to_render = list(camera_configs.keys()) if view.lower() == "all" else [view.lower()]

    rendered_files = []

    for v in views_to_render:
        if v not in camera_configs:
            print(f"Warning: Unknown view '{v}'. Skipping.", file=sys.stderr)
            continue

        cdir, cup = camera_configs[v]

        vp_type = Viewport.Type.Ortho if (projection.lower() == "ortho" and v != "iso") else Viewport.Type.Perspective
        vp = Viewport(type=vp_type)
        vp.camera_dir = cdir
        vp.camera_up = cup

        if tripod:
            t_overlay = CoordinateTripodOverlay(size=0.08)
            vp.overlays.append(t_overlay)

        if color_legend_overlay:
            vp.overlays.append(color_legend_overlay)

        vp.zoom_all()

        out_name = f"{prefix}_view_{v}.png"
        out_file = out_dir / out_name

        vp.render_image(
            filename=str(out_file),
            size=(width, height),
            background=bg,
        )
        print(f"Saved: {out_file} ({width}x{height}, view={v}, proj={vp_type.name})")
        rendered_files.append(str(out_file))

    return rendered_files


def main():
    parser = argparse.ArgumentParser(
        description="Headless high-resolution crystal structure renderer using OVITO."
    )
    parser.add_argument("input", help="Path to input crystal file (POSCAR, CONTCAR, CIF, XYZ, etc.)")
    parser.add_argument(
        "--view",
        "-v",
        choices=["a", "b", "c", "iso", "all"],
        default="all",
        help="Camera orientation (a, b, c, iso, or all views; default: all)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Output directory for generated PNG images (default: current dir)",
    )
    parser.add_argument("--prefix", "-p", help="Output file prefix (default: input file stem)")
    parser.add_argument("--width", type=int, default=1920, help="Image width in pixels (default: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="Image height in pixels (default: 1080)")
    parser.add_argument(
        "--projection",
        choices=["ortho", "perspective"],
        default="ortho",
        help="Projection type (default: ortho)",
    )
    parser.add_argument(
        "--supercell",
        nargs=3,
        type=int,
        metavar=("NX", "NY", "NZ"),
        help="Replicate unit cell (e.g. --supercell 2 2 2)",
    )
    parser.add_argument("--no-bonds", action="store_true", help="Disable automatic bond creation")
    parser.add_argument("--bond-cutoff", type=float, default=3.0, help="Bond cutoff distance in Angstroms (default: 3.0)")
    parser.add_argument("--particle-radius", type=float, default=None, help="Atomic sphere radius in Angstroms (e.g. 0.38 for ball-and-stick)")
    parser.add_argument("--bond-width", type=float, default=None, help="Bond cylinder radius in Angstroms (e.g. 0.14 for ball-and-stick)")
    parser.add_argument("--polyhedra", action="store_true", help="Enable polyhedral template matching")
    parser.add_argument("--no-tripod", action="store_true", help="Disable coordinate tripod overlay")
    parser.add_argument(
        "--background",
        choices=["white", "black", "gray", "transparent"],
        default="white",
        help="Background color (default: white)",
    )
    parser.add_argument(
        "--bader-file",
        help="Path to Bader charge ACF.dat file or column file to color-code atoms",
    )
    parser.add_argument(
        "--charge-range",
        nargs=2,
        type=float,
        metavar=("MIN", "MAX"),
        help="Explicit charge range for color mapping (e.g. --charge-range -2.5 2.5)",
    )
    parser.add_argument(
        "--bader-colormap",
        choices=["BlueWhiteRed", "Viridis", "Magma"],
        default="BlueWhiteRed",
        help="Colormap for charge coding (default: BlueWhiteRed)",
    )
    parser.add_argument(
        "--no-cell",
        action="store_true",
        help="Hide simulation cell box wireframe",
    )

    args = parser.parse_args()

    render_structure(
        input_file=args.input,
        view=args.view,
        output_dir=args.output_dir,
        output_prefix=args.prefix,
        width=args.width,
        height=args.height,
        projection=args.projection,
        supercell=args.supercell,
        create_bonds=not args.no_bonds,
        bond_cutoff=args.bond_cutoff,
        particle_radius=args.particle_radius,
        bond_width=args.bond_width,
        polyhedra=args.polyhedra,
        tripod=not args.no_tripod,
        background=args.background,
        bader_file=args.bader_file,
        charge_range=args.charge_range,
        bader_colormap=args.bader_colormap,
        no_cell=args.no_cell,
    )


if __name__ == "__main__":
    main()
