#!/usr/bin/env python3
"""
Publication-Quality Photorealistic Crystal Structure Renderer using Blender.
Runs headlessly via Blender's Python API to generate 3D ray-traced figures.
"""

import argparse
import math
import os
import sys
from pathlib import Path

# Standard CPK Color Palette (RGBA normalized 0.0 - 1.0)
CPK_COLORS = {
    "H": (1.00, 1.00, 1.00, 1.0),
    "He": (0.85, 1.00, 1.00, 1.0),
    "Li": (0.80, 0.50, 1.00, 1.0),
    "Be": (0.76, 1.00, 0.00, 1.0),
    "B": (1.00, 0.71, 0.71, 1.0),
    "C": (0.20, 0.20, 0.20, 1.0),
    "N": (0.05, 0.05, 0.90, 1.0),
    "O": (0.90, 0.10, 0.10, 1.0),
    "F": (0.56, 0.88, 0.31, 1.0),
    "Ne": (0.70, 0.89, 0.96, 1.0),
    "Na": (0.67, 0.36, 0.95, 1.0),
    "Mg": (0.54, 1.00, 0.00, 1.0),
    "Al": (0.75, 0.65, 0.65, 1.0),
    "Si": (0.94, 0.78, 0.63, 1.0),
    "P": (1.00, 0.60, 0.00, 1.0),
    "S": (1.00, 0.90, 0.10, 1.0),
    "Cl": (0.12, 0.94, 0.12, 1.0),
    "Ar": (0.50, 0.82, 0.89, 1.0),
    "K": (0.56, 0.25, 0.84, 1.0),
    "Ca": (0.24, 1.00, 0.00, 1.0),
    "Sc": (0.90, 0.90, 0.90, 1.0),
    "Ti": (0.60, 0.60, 0.65, 1.0),
    "V": (0.65, 0.65, 0.65, 1.0),
    "Cr": (0.54, 0.60, 0.78, 1.0),
    "Mn": (0.61, 0.48, 0.78, 1.0),
    "Fe": (0.88, 0.40, 0.20, 1.0),
    "Co": (0.94, 0.56, 0.63, 1.0),
    "Ni": (0.31, 0.82, 0.31, 1.0),
    "Cu": (0.78, 0.50, 0.20, 1.0),
    "Zn": (0.49, 0.51, 0.79, 1.0),
    "Ga": (0.76, 0.56, 0.56, 1.0),
    "Ge": (0.40, 0.56, 0.56, 1.0),
    "As": (0.74, 0.50, 0.89, 1.0),
    "Se": (1.00, 0.63, 0.00, 1.0),
    "Br": (0.65, 0.16, 0.16, 1.0),
    "Rb": (0.44, 0.18, 0.69, 1.0),
    "Sr": (0.00, 1.00, 0.00, 1.0),
    "Y": (0.58, 1.00, 1.00, 1.0),
    "Zr": (0.58, 0.88, 0.88, 1.0),
    "Nb": (0.45, 0.76, 0.79, 1.0),
    "Mo": (0.33, 0.71, 0.71, 1.0),
    "Ru": (0.14, 0.56, 0.56, 1.0),
    "Rh": (0.04, 0.49, 0.55, 1.0),
    "Pd": (0.00, 0.41, 0.52, 1.0),
    "Ag": (0.75, 0.75, 0.75, 1.0),
    "Cd": (1.00, 0.85, 0.56, 1.0),
    "In": (0.65, 0.46, 0.45, 1.0),
    "Sn": (0.40, 0.50, 0.50, 1.0),
    "Sb": (0.62, 0.39, 0.71, 1.0),
    "Te": (0.83, 0.48, 0.00, 1.0),
    "I": (0.58, 0.00, 0.58, 1.0),
    "Cs": (0.35, 0.10, 0.58, 1.0),
    "Ba": (0.00, 0.79, 0.00, 1.0),
    "La": (0.44, 0.83, 1.00, 1.0),
    "Ce": (1.00, 1.00, 0.78, 1.0),
    "Pr": (0.85, 1.00, 0.78, 1.0),
    "Nd": (0.78, 1.00, 0.78, 1.0),
    "Eu": (0.38, 1.00, 0.78, 1.0),
    "Gd": (0.27, 1.00, 0.78, 1.0),
    "Tb": (0.18, 1.00, 0.78, 1.0),
    "Dy": (0.12, 1.00, 0.78, 1.0),
    "Ho": (0.00, 1.00, 0.63, 1.0),
    "Er": (0.00, 0.90, 0.47, 1.0),
    "Tm": (0.00, 0.84, 0.32, 1.0),
    "Yb": (0.00, 0.75, 0.22, 1.0),
    "Lu": (0.00, 0.67, 0.14, 1.0),
    "Hf": (0.30, 0.76, 1.00, 1.0),
    "Ta": (0.30, 0.65, 1.00, 1.0),
    "W": (0.13, 0.58, 0.84, 1.0),
    "Re": (0.15, 0.49, 0.67, 1.0),
    "Os": (0.15, 0.40, 0.59, 1.0),
    "Ir": (0.09, 0.33, 0.53, 1.0),
    "Pt": (0.82, 0.82, 0.88, 1.0),
    "Au": (1.00, 0.82, 0.14, 1.0),
    "Hg": (0.71, 0.71, 0.76, 1.0),
    "Tl": (0.65, 0.33, 0.30, 1.0),
    "Pb": (0.34, 0.35, 0.38, 1.0),
    "Bi": (0.62, 0.31, 0.71, 1.0),
    "U": (0.00, 0.56, 0.00, 1.0),
}

# Approximate covalent radii (Angstroms)
RADII = {
    "H": 0.31, "C": 0.45, "N": 0.42, "O": 0.40, "F": 0.38,
    "Si": 0.55, "P": 0.53, "S": 0.52, "Cl": 0.50,
    "Ti": 0.60, "Sr": 0.75, "Ba": 0.80, "Fe": 0.58, "Co": 0.56,
    "Ni": 0.55, "Cu": 0.55, "Zn": 0.55, "Au": 0.65, "Pt": 0.65
}


def parse_poscar(poscar_path):
    import numpy as np

    with open(poscar_path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    comment = lines[0]
    scale = float(lines[1])
    lattice = np.array([[float(x) for x in lines[i].split()] for i in range(2, 5)]) * scale

    line5 = lines[5].split()
    if line5[0].isdigit():
        # Old POSCAR without species line
        species_symbols = ["X"] * len(line5)
        counts = [int(x) for x in line5]
        idx = 6
    else:
        species_symbols = line5
        counts = [int(x) for x in lines[6].split()]
        idx = 7

    if lines[idx].lower().startswith("s"):
        idx += 1
    coord_type = lines[idx].lower()
    idx += 1

    coords = []
    atoms = []
    for sp, cnt in zip(species_symbols, counts):
        for _ in range(cnt):
            coords.append([float(x) for x in lines[idx].split()[:3]])
            atoms.append(sp)
            idx += 1

    coords = np.array(coords)
    if coord_type.startswith("d"):
        # Direct / Fractional to Cartesian
        cart_coords = coords @ lattice
    else:
        cart_coords = coords * scale

    return lattice, atoms, cart_coords


def render_crystal(args):
    import bpy
    import numpy as np

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or input_path.stem

    # Parse structure
    try:
        lattice, species, coords = parse_poscar(str(input_path))
    except Exception as e:
        # Fallback to ASE if available
        try:
            from ase.io import read
            atoms = read(str(input_path))
            lattice = np.array(atoms.get_cell())
            species = atoms.get_chemical_symbols()
            coords = np.array(atoms.get_positions())
        except Exception:
            print(f"Error parsing structure {input_path}: {e}", file=sys.stderr)
            sys.exit(1)

    # Initialize clean Blender scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    # Set render engine
    if args.engine.lower() == "cycles":
        scene.render.engine = "CYCLES"
        scene.cycles.samples = args.samples
    else:
        scene.render.engine = "BLENDER_EEVEE"

    # Material generator
    materials = {}
    for sp in set(species):
        mat = bpy.data.materials.new(name=f"mat_{sp}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            color = CPK_COLORS.get(sp, (0.7, 0.7, 0.7, 1.0))
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = 0.25
            bsdf.inputs["Metallic"].default_value = 0.1
        materials[sp] = mat

    # Add Atoms
    for sp, pos in zip(species, coords):
        r = RADII.get(sp, 0.45) * args.scale_atoms
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=tuple(pos), segments=32, ring_count=16)
        atom_obj = bpy.context.active_object
        atom_obj.name = f"atom_{sp}"
        atom_obj.data.materials.append(materials[sp])
        # Smooth shading
        bpy.ops.object.shade_smooth()

    # Add Bonds
    if not args.no_bonds:
        bond_mat = bpy.data.materials.new(name="mat_bond")
        bond_mat.use_nodes = True
        bbsdf = bond_mat.node_tree.nodes.get("Principled BSDF")
        if bbsdf:
            bbsdf.inputs["Base Color"].default_value = (0.75, 0.75, 0.75, 1.0)
            bbsdf.inputs["Roughness"].default_value = 0.3

        n_atoms = len(coords)
        for i in range(n_atoms):
            for j in range(i + 1, n_atoms):
                dist = np.linalg.norm(coords[i] - coords[j])
                if 0.5 < dist <= args.bond_cutoff:
                    # Create cylinder bond
                    mid = (coords[i] + coords[j]) / 2.0
                    diff = coords[j] - coords[i]
                    phi = math.atan2(diff[1], diff[0])
                    theta = math.acos(diff[2] / dist)

                    bpy.ops.mesh.primitive_cylinder_add(
                        radius=args.bond_radius,
                        depth=dist,
                        location=tuple(mid),
                        rotation=(0, theta, phi),
                    )
                    b_obj = bpy.context.active_object
                    b_obj.name = "bond"
                    b_obj.data.materials.append(bond_mat)
                    bpy.ops.object.shade_smooth()

    # Add Unit Cell Bounding Box
    if not args.no_cell:
        corners = np.array([
            [0,0,0], [1,0,0], [1,1,0], [0,1,0],
            [0,0,1], [1,0,1], [1,1,1], [0,1,1]
        ]) @ lattice

        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]

        curve_data = bpy.data.curves.new("unit_cell_curve", type="CURVE")
        curve_data.dimensions = "3D"
        curve_data.bevel_depth = 0.03
        curve_data.bevel_resolution = 4

        for p1, p2 in edges:
            poly = curve_data.splines.new("POLY")
            poly.points.add(1)
            poly.points[0].co = (*corners[p1], 1)
            poly.points[1].co = (*corners[p2], 1)

        cell_obj = bpy.data.objects.new("unit_cell", curve_data)
        bpy.context.collection.objects.link(cell_obj)

    # 3-Point Lighting Setup
    # Key Light (Sun)
    bpy.ops.object.light_add(type="SUN", location=(10, -10, 15))
    sun = bpy.context.active_object
    sun.data.energy = 4.5

    # Fill Light (Area)
    bpy.ops.object.light_add(type="AREA", location=(-10, -10, 8))
    fill = bpy.context.active_object
    fill.data.energy = 200.0

    # Back Light (Point)
    bpy.ops.object.light_add(type="POINT", location=(0, 15, 10))
    back = bpy.context.active_object
    back.data.energy = 100.0

    # Calculate center of mass for camera aiming
    center = coords.mean(axis=0)
    extent = np.max(np.ptp(coords, axis=0)) if len(coords) > 1 else 5.0
    dist = max(extent * 2.8, 8.0)

    # Views configuration: (camera position relative to center, rotation euler)
    camera_views = {
        "a": (center + np.array([dist, 0, 0]), (math.pi/2, 0, math.pi/2)),
        "b": (center + np.array([0, -dist, 0]), (math.pi/2, 0, 0)),
        "c": (center + np.array([0, 0, dist]), (0, 0, 0)),
        "iso": (center + np.array([dist*0.7, -dist*0.7, dist*0.6]), (1.05, 0.0, 0.785)),
    }

    views_to_render = list(camera_views.keys()) if args.view.lower() == "all" else [args.view.lower()]

    # Render configurations
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height

    if args.transparent:
        scene.render.film_transparent = True

    rendered_files = []

    for v in views_to_render:
        if v not in camera_views:
            continue
        cam_pos, cam_rot = camera_views[v]

        # Add or update camera
        bpy.ops.object.camera_add(location=tuple(cam_pos), rotation=cam_rot)
        cam = bpy.context.active_object
        scene.camera = cam

        if args.ortho and v != "iso":
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = extent * 1.5
        else:
            cam.data.type = "PERSP"

        out_file = out_dir / f"{prefix}_blender_{v}.png"
        scene.render.filepath = str(out_file)

        print(f"Rendering view {v} ({args.width}x{args.height}, engine={scene.render.engine})...")
        bpy.ops.render.render(write_still=True)
        print(f"Saved: {out_file}")
        rendered_files.append(str(out_file))

        # Remove camera for next iteration
        bpy.data.objects.remove(cam, do_unlink=True)

    return rendered_files


def main():
    # Detect if run via `blender -b -P script.py -- [args]`
    raw_args = sys.argv
    if "--" in raw_args:
        cli_args = raw_args[raw_args.index("--") + 1:]
    else:
        cli_args = raw_args[1:]

    parser = argparse.ArgumentParser(
        description="Publication-Quality Crystal Structure Ray-Tracer using Blender 5.2."
    )
    parser.add_argument("input", help="Path to input crystal structure (POSCAR, CIF, XYZ)")
    parser.add_argument(
        "--view",
        "-v",
        choices=["a", "b", "c", "iso", "all"],
        default="all",
        help="View angle along crystal axes (a, b, c, iso, or all; default: all)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=".",
        help="Output directory for generated PNG images",
    )
    parser.add_argument("--prefix", "-p", help="Output file prefix (default: input file stem)")
    parser.add_argument("--width", type=int, default=1920, help="Image width in pixels (default: 1920)")
    parser.add_argument("--height", type=int, default=1080, help="Image height in pixels (default: 1080)")
    parser.add_argument(
        "--engine",
        choices=["eevee", "cycles"],
        default="eevee",
        help="Blender render engine (eevee for fast rendering, cycles for ray-tracing; default: eevee)",
    )
    parser.add_argument("--samples", type=int, default=64, help="Render samples for Cycles (default: 64)")
    parser.add_argument("--bond-cutoff", type=float, default=2.8, help="Bond cutoff distance in Angstroms (default: 2.8)")
    parser.add_argument("--bond-radius", type=float, default=0.08, help="Bond cylinder radius (default: 0.08)")
    parser.add_argument("--scale-atoms", type=float, default=1.0, help="Scale factor for atomic radii (default: 1.0)")
    parser.add_argument("--no-bonds", action="store_true", help="Disable bond rendering")
    parser.add_argument("--no-cell", action="store_true", help="Disable unit cell wireframe")
    parser.add_argument("--ortho", action="store_true", help="Use orthographic camera projection for a, b, c axes")
    parser.add_argument("--transparent", action="store_true", help="Render with transparent alpha background")

    args = parser.parse_args(cli_args)
    render_crystal(args)


if __name__ == "__main__":
    main()
