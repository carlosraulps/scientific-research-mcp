#!/usr/bin/env python3
"""
================================================================================
Headless High-Resolution Crystal & Trajectory Renderer (OVITO & ASE)
================================================================================
Generates publication-quality crystal structure snapshots and property maps:
1. Padded Coordinate Tripod: Enforces offset_x >= 0.05, offset_y >= 0.05 to
   strictly prevent axis label clipping (e.g. -x, -z labels) at image margins.
2. 2D Material & Carbon Presets: Dedicated presets ('2d-carbon', 'ball-stick',
   'spacefill', 'wireframe') calibrated for graphene, PHOTH-graphene, and TMDs.
3. Decoupled Publication Typography: Native integration with Matplotlib-driven
   STIX/Times New Roman colorbars, qualitative physical callouts, and compositing.
4. Net Bader Charge Mapping: Automatically translates raw Henkelman ACF.dat valence
   counts into physical net atomic charges (Delta Q = Z_val - Q_bader).
================================================================================
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Add current script directory for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from publication_colorbar import generate_publication_colorbar, composite_image_with_colorbar
from scale_bar_overlay import add_scale_bar, autotrim_whitespace


# Standard pseudopotential valence electron counts for common elements
VALENCE_ELECTRONS: Dict[str, float] = {
    "H": 1.0, "He": 2.0, "Li": 1.0, "Be": 2.0, "B": 3.0, "C": 4.0, "N": 5.0,
    "O": 6.0, "F": 7.0, "Ne": 8.0, "Na": 1.0, "Mg": 2.0, "Al": 3.0, "Si": 4.0,
    "P": 5.0, "S": 6.0, "Cl": 7.0, "Ar": 8.0, "K": 1.0, "Ca": 2.0, "Sc": 3.0,
    "Ti": 4.0, "V": 5.0, "Cr": 6.0, "Mn": 7.0, "Fe": 8.0, "Co": 9.0, "Ni": 10.0,
    "Cu": 11.0, "Zn": 12.0, "Ga": 3.0, "Ge": 4.0, "As": 5.0, "Se": 6.0, "Br": 7.0,
    "Mo": 6.0, "Ru": 8.0, "Rh": 9.0, "Pd": 10.0, "Ag": 11.0, "Pt": 10.0, "Au": 11.0,
}


def apply_presets(
    preset_name: Optional[str],
    particle_radius: Optional[float],
    bond_width: Optional[float],
    bond_cutoff: float,
    create_bonds: bool,
) -> Tuple[Optional[float], Optional[float], float, bool]:
    """
    Applies calibrated geometrical presets for materials visualization.
    """
    if not preset_name:
        return particle_radius, bond_width, bond_cutoff, create_bonds

    p = preset_name.lower()
    if p in ["2d-carbon", "graphene", "photh-graphene"]:
        # Optimal for 2D carbon lattices: connects C-C up to 1.52 A, strictly avoids diagonal ring artifacts
        return 0.38, 0.14, 1.70, True
    elif p in ["ball-stick", "ball_stick"]:
        return 0.40, 0.15, 2.80, True
    elif p == "spacefill":
        return 0.75, 0.00, bond_cutoff, False
    elif p == "wireframe":
        return 0.10, 0.08, bond_cutoff, True
    return particle_radius, bond_width, bond_cutoff, create_bonds


def parse_bader_charges(bader_file: Path) -> List[float]:
    """
    Parses Henkelman Bader ACF.dat or simple column files.
    """
    charges = []
    with open(bader_file, "r") as f:
        blines = [l.strip() for l in f if l.strip()]
    for bline in blines:
        parts = bline.split()
        if len(parts) >= 5 and parts[0].isdigit():
            # ACF.dat line: # X Y Z CHARGE MIN_DIST ATOMIC_VOL
            try:
                charges.append(float(parts[4]))
            except ValueError:
                pass
        elif len(parts) == 1:
            try:
                charges.append(float(parts[0]))
            except ValueError:
                pass
    return charges


def render_structure(
    input_file: Union[str, Path],
    view: str = "all",
    output_dir: Union[str, Path] = ".",
    output_prefix: Optional[str] = None,
    width: int = 1920,
    height: int = 1080,
    projection: str = "ortho",
    supercell: Optional[List[int]] = None,
    preset: Optional[str] = None,
    create_bonds: bool = True,
    bond_cutoff: float = 3.0,
    particle_radius: Optional[float] = None,
    bond_width: Optional[float] = None,
    polyhedra: bool = False,
    tripod: bool = True,
    tripod_offset: Tuple[float, float] = (0.06, 0.06),
    tripod_size: float = 0.075,
    background: str = "white",
    bader_file: Optional[Union[str, Path]] = None,
    net_charge: bool = False,
    charge_range: Optional[List[float]] = None,
    bader_colormap: str = "BlueWhiteRed",
    publish_colorbar: bool = False,
    composite_colorbar: bool = False,
    colorbar_label: Optional[str] = None,
    no_cell: bool = False,
    renderer_type: str = "standard",
    scale_bar: Optional[float] = None,
    autotrim: bool = False,
    vectors_file: Optional[Union[str, Path]] = None,
    vector_scale: float = 1.0,
    vector_width: float = 0.12,
    vector_color: Tuple[float, float, float] = (0.85, 0.15, 0.15),
) -> List[str]:
    """
    Renders high-resolution snapshots with padded tripods, raytracing (Tachyon/OSPRay),
    physical scale bars, and publication typography.
    """
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

    # Apply calibrated presets
    particle_radius, bond_width, bond_cutoff, create_bonds = apply_presets(
        preset, particle_radius, bond_width, bond_cutoff, create_bonds
    )

    pipeline = import_file(str(input_path))

    # Apply Supercell Replicate if requested
    if supercell and len(supercell) == 3:
        nx, ny, nz = [int(x) for x in supercell]
        if nx > 1 or ny > 1 or nz > 1:
            pipeline.modifiers.append(ReplicateModifier(num_x=nx, num_y=ny, num_z=nz))

    # Add Bond Modifier
    if create_bonds:
        pipeline.modifiers.append(CreateBondsModifier(cutoff=bond_cutoff))

    # Custom styling for particle radius and bond width
    if particle_radius or bond_width:
        def style_vis(frame, data):
            if particle_radius:
                data.particles_.create_property("Radius", data=[particle_radius] * data.particles.count)
            if data.particles.bonds and bond_width:
                data.particles.bonds.vis.width = bond_width
        pipeline.modifiers.append(style_vis)

    # Polyhedral analysis if requested
    if polyhedra:
        try:
            from ovito.modifiers import PolyhedralTemplateMatchingModifier
            pipeline.modifiers.append(PolyhedralTemplateMatchingModifier())
        except Exception:
            pass

    # Bader Charge Assignment & Net Charge calculation
    color_legend_overlay = None
    c_min, c_max = -0.30, 0.30
    if bader_file:
        b_path = Path(bader_file).resolve()
        if b_path.exists():
            raw_charges = parse_bader_charges(b_path)
            if raw_charges:
                final_charges = raw_charges
                if net_charge:
                    # Deduce species and calculate Delta Q = Z_val - Q_bader
                    try:
                        from ase.io import read as ase_read
                        ase_atoms = ase_read(str(input_path))
                        symbols = ase_atoms.get_chemical_symbols()
                        final_charges = []
                        for idx, q_raw in enumerate(raw_charges):
                            sym = symbols[idx] if idx < len(symbols) else "C"
                            z_val = VALENCE_ELECTRONS.get(sym, 4.0)
                            final_charges.append(round(z_val - q_raw, 4))
                    except Exception as e:
                        print(f"Warning: Could not compute net valence charges via ASE: {e}", file=sys.stderr)

                def assign_charge_prop(frame, data):
                    data.particles_.create_property("Charge", data=final_charges[:data.particles.count])
                pipeline.modifiers.append(assign_charge_prop)

                from ovito.modifiers import ColorCodingModifier
                from ovito.vis import ColorLegendOverlay

                cmap_grad = ColorCodingModifier.BlueWhiteRed()
                if bader_colormap.lower() == "viridis":
                    cmap_grad = ColorCodingModifier.Viridis()
                elif bader_colormap.lower() == "magma":
                    cmap_grad = ColorCodingModifier.Magma()

                c_min = charge_range[0] if (charge_range and len(charge_range) == 2) else min(final_charges)
                c_max = charge_range[1] if (charge_range and len(charge_range) == 2) else max(final_charges)

                color_mod = ColorCodingModifier(
                    property="Charge",
                    gradient=cmap_grad,
                    start_value=c_min,
                    end_value=c_max,
                )
                pipeline.modifiers.append(color_mod)

                # Only use internal overlay if publication colorbar is NOT requested
                if not publish_colorbar and not composite_colorbar:
                    color_legend_overlay = ColorLegendOverlay(
                        modifier=color_mod,
                        title="Net Charge (e)" if net_charge else "Bader Valence (e)",
                        ticks_enabled=True,
                    )

    # Hide simulation cell box if requested
    if no_cell:
        def hide_cell_modifier(frame, data):
            if data.cell:
                data.cell.vis.enabled = False
        pipeline.modifiers.append(hide_cell_modifier)

    # Atomic vectors (forces, magnetic moments, etc.)
    if vectors_file:
        v_path = Path(vectors_file).resolve()
        if v_path.exists():
            vec_list = []
            with open(v_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        try:
                            vec_list.append([float(parts[0]), float(parts[1]), float(parts[2])])
                        except ValueError:
                            pass
            if vec_list:
                from ovito.vis import VectorVis
                def assign_vectors_modifier(frame, data):
                    prop = data.particles_.create_property("Vector", data=vec_list[:data.particles.count])
                    prop.vis = VectorVis(
                        scaling=vector_scale,
                        width=vector_width,
                        color=vector_color,
                    )
                pipeline.modifiers.append(assign_vectors_modifier)

    pipeline.add_to_scene()

    # Configure raytracing or standard renderer
    ovito_renderer = None
    if renderer_type.lower() == "tachyon":
        try:
            from ovito.vis import TachyonRenderer
            ovito_renderer = TachyonRenderer(
                ambient_occlusion=True,
                ambient_occlusion_samples=12,
                shadows=True,
                antialiasing=True,
                antialiasing_samples=12,
            )
            print("[OVITO] Enabled Tachyon raytracing renderer (ambient occlusion + soft shadows)")
        except Exception as e:
            print(f"[OVITO] Warning: TachyonRenderer unavailable ({e}). Falling back to standard renderer.", file=sys.stderr)
    elif renderer_type.lower() == "ospray":
        try:
            from ovito.vis import OSPRayRenderer
            ovito_renderer = OSPRayRenderer(
                direct_light_enabled=True,
                ambient_light_enabled=True,
                denoising_enabled=True,
            )
            print("[OVITO] Enabled OSPRay path-tracing renderer (direct lighting + denoising)")
        except Exception as e:
            print(f"[OVITO] Warning: OSPRayRenderer unavailable ({e}). Falling back to standard renderer.", file=sys.stderr)

    bg_colors = {
        "white": (1.0, 1.0, 1.0),
        "black": (0.0, 0.0, 0.0),
        "gray": (0.2, 0.2, 0.2),
        "transparent": None,
    }
    bg = bg_colors.get(background.lower(), (1.0, 1.0, 1.0))

    camera_configs = {
        "a": ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
        "b": ((0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
        "c": ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
        "iso": ((1.2, 1.5, 1.0), (0.0, 0.0, 1.0)),
    }

    views_to_render = list(camera_configs.keys()) if view.lower() == "all" else [view.lower()]
    rendered_files = []

    # Safe padded tripod offsets (never < 0.05 to prevent clipping -x label)
    safe_ox = max(0.05, float(tripod_offset[0]))
    safe_oy = max(0.05, float(tripod_offset[1]))

    for v in views_to_render:
        if v not in camera_configs:
            continue

        cdir, cup = camera_configs[v]
        vp_type = Viewport.Type.Ortho if (projection.lower() == "ortho" and v != "iso") else Viewport.Type.Perspective
        vp = Viewport(type=vp_type)
        vp.camera_dir = cdir
        vp.camera_up = cup

        if tripod:
            t_overlay = CoordinateTripodOverlay(
                size=tripod_size,
                offset_x=safe_ox,
                offset_y=safe_oy,
            )
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
            renderer=ovito_renderer,
        )
        print(f"[OVITO] Saved: {out_file} ({width}x{height}, view={v}, proj={vp_type.name})")

        # Injected physical scale bar for orthographic views
        if scale_bar and vp_type == Viewport.Type.Ortho:
            add_scale_bar(
                image_path=out_file,
                length_angstrom=scale_bar,
                fov_angstrom=vp.fov,
                output_path=out_file,
                color="black" if background.lower() == "white" else "white",
            )
            print(f"[OVITO] Injected {scale_bar} Å scale bar onto: {out_file}")

        # Auto-trim uniform whitespace padding
        if autotrim:
            autotrim_whitespace(image_path=out_file, output_path=out_file, padding=30)

        # Generate / composite decoupled publication colorbar
        if bader_file and (publish_colorbar or composite_colorbar):
            cb_file = out_dir / f"{prefix}_colorbar.png"
            cb_label = colorbar_label or (r"$Q_{\mathrm{net}}\ (e)$" if net_charge else r"$Q_{\mathrm{valence}}\ (e)$")
            generate_publication_colorbar(
                output_path=cb_file,
                vmin=c_min,
                vmax=c_max,
                colormap="coolwarm" if bader_colormap.lower() == "bluewhitered" else bader_colormap.lower(),
                label=cb_label,
            )
            if composite_colorbar:
                comp_file = out_dir / f"{prefix}_view_{v}_composite.png"
                composite_image_with_colorbar(
                    crystal_image_path=out_file,
                    colorbar_image_path=cb_file,
                    output_composite_path=comp_file,
                )
                rendered_files.append(str(comp_file))

        rendered_files.append(str(out_file))

    return rendered_files


def main():
    parser = argparse.ArgumentParser(
        description="Headless High-Resolution Crystal Structure & Bader Charge Renderer using OVITO."
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
    parser.add_argument(
        "--preset",
        choices=["2d-carbon", "ball-stick", "spacefill", "wireframe"],
        help="Predefined material geometry presets (e.g. '2d-carbon' for clash-free graphene/PHOTH-graphene)",
    )
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
    parser.add_argument("--particle-radius", type=float, default=None, help="Atomic sphere radius in Angstroms (default: 0.38 for 2d-carbon)")
    parser.add_argument("--bond-width", type=float, default=None, help="Bond cylinder radius in Angstroms (default: 0.14 for 2d-carbon)")
    parser.add_argument("--polyhedra", action="store_true", help="Enable polyhedral template matching")
    parser.add_argument("--no-tripod", action="store_true", help="Disable coordinate tripod overlay")
    parser.add_argument(
        "--tripod-offset",
        nargs=2,
        type=float,
        default=[0.06, 0.06],
        metavar=("X", "Y"),
        help="Padded margin offset for tripod to avoid label clipping (default: 0.06 0.06)",
    )
    parser.add_argument(
        "--tripod-size",
        type=float,
        default=0.075,
        help="Normalized size of coordinate tripod (default: 0.075)",
    )
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
        "--net-charge",
        action="store_true",
        help="Calculate net charge (Delta Q = Z_val - Q_bader) centered around zero",
    )
    parser.add_argument(
        "--charge-range",
        nargs=2,
        type=float,
        metavar=("MIN", "MAX"),
        help="Explicit charge range for color mapping (e.g. --charge-range -0.25 0.25)",
    )
    parser.add_argument(
        "--bader-colormap",
        choices=["BlueWhiteRed", "Viridis", "Magma"],
        default="BlueWhiteRed",
        help="Colormap for charge coding (default: BlueWhiteRed)",
    )
    parser.add_argument(
        "--publish-colorbar",
        action="store_true",
        help="Generate standalone Matplotlib STIX/Times New Roman colorbar",
    )
    parser.add_argument(
        "--composite-colorbar",
        action="store_true",
        help="Horizontally composite publication colorbar onto the rendered crystal image",
    )
    parser.add_argument(
        "--colorbar-label",
        help="Custom LaTeX label for the publication colorbar",
    )
    parser.add_argument(
        "--no-cell",
        action="store_true",
        help="Hide simulation cell box wireframe",
    )
    parser.add_argument(
        "--renderer",
        choices=["standard", "tachyon", "ospray"],
        default="standard",
        help="Rendering backend: standard (fast offscreen), tachyon (CPU raytracing with ambient occlusion and soft shadows), or ospray (path-tracing with denoising)",
    )
    parser.add_argument(
        "--scale-bar",
        type=float,
        default=None,
        metavar="ANGSTROM",
        help="Inject physical scale bar with specified length in Angstroms (e.g. --scale-bar 5.0 for 5 Å; ortho views only)",
    )
    parser.add_argument(
        "--autotrim",
        action="store_true",
        help="Automatically crop uniform whitespace/transparent margins around rendered crystals",
    )
    parser.add_argument(
        "--vectors-file",
        help="Path to 3-column vector file (e.g. atomic forces or magnetic moments) to render 3D vector arrows on atoms",
    )
    parser.add_argument(
        "--vector-scale",
        type=float,
        default=1.0,
        help="Scaling factor for vector arrows (default: 1.0)",
    )
    parser.add_argument(
        "--vector-width",
        type=float,
        default=0.12,
        help="Cylinder diameter/width for vector arrows (default: 0.12 Å)",
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
        preset=args.preset,
        create_bonds=not args.no_bonds,
        bond_cutoff=args.bond_cutoff,
        particle_radius=args.particle_radius,
        bond_width=args.bond_width,
        polyhedra=args.polyhedra,
        tripod=not args.no_tripod,
        tripod_offset=tuple(args.tripod_offset),
        tripod_size=args.tripod_size,
        background=args.background,
        bader_file=args.bader_file,
        net_charge=args.net_charge,
        charge_range=args.charge_range,
        bader_colormap=args.bader_colormap,
        publish_colorbar=args.publish_colorbar,
        composite_colorbar=args.composite_colorbar,
        colorbar_label=args.colorbar_label,
        no_cell=args.no_cell,
        renderer_type=args.renderer,
        scale_bar=args.scale_bar,
        autotrim=args.autotrim,
        vectors_file=args.vectors_file,
        vector_scale=args.vector_scale,
        vector_width=args.vector_width,
    )


if __name__ == "__main__":
    main()
