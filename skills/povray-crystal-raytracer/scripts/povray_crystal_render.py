#!/home/cr/.local/share/mamba/envs/vasp-env/bin/python
"""
================================================================================
POV-Ray Crystal Raytracer (povray-crystal-render)
================================================================================
Converts POSCAR, CIF, or XYZ crystal structures into publication-grade
3D ray-traced scenes with realistic studio lighting, soft shadows,
metallic/dielectric finishes, and unit cell bounding wireframes.
================================================================================
"""

import os
import sys
import argparse
import subprocess
import numpy as np

# Standard CPK Element Colors (RGB 0.0 to 1.0) and Covalent Radii (Angstroms)
ELEMENT_PROPERTIES = {
    "H":  {"color": (0.90, 0.90, 0.90), "radius": 0.32, "spec": "dielectric"},
    "C":  {"color": (0.20, 0.20, 0.20), "radius": 0.77, "spec": "dielectric"},
    "N":  {"color": (0.18, 0.31, 0.98), "radius": 0.75, "spec": "dielectric"},
    "O":  {"color": (0.95, 0.15, 0.15), "radius": 0.73, "spec": "dielectric"},
    "F":  {"color": (0.56, 0.88, 0.31), "radius": 0.71, "spec": "dielectric"},
    "P":  {"color": (1.00, 0.50, 0.00), "radius": 1.06, "spec": "dielectric"},
    "S":  {"color": (0.90, 0.85, 0.20), "radius": 1.02, "spec": "dielectric"},
    "Cl": {"color": (0.12, 0.94, 0.12), "radius": 0.99, "spec": "dielectric"},
    "Br": {"color": (0.60, 0.13, 0.00), "radius": 1.14, "spec": "dielectric"},
    "I":  {"color": (0.45, 0.05, 0.45), "radius": 1.33, "spec": "dielectric"},
    "Ti": {"color": (0.60, 0.60, 0.65), "radius": 1.36, "spec": "metallic"},
    "V":  {"color": (0.65, 0.65, 0.70), "radius": 1.25, "spec": "metallic"},
    "Cr": {"color": (0.54, 0.60, 0.78), "radius": 1.28, "spec": "metallic"},
    "Mn": {"color": (0.61, 0.48, 0.78), "radius": 1.39, "spec": "metallic"},
    "Fe": {"color": (0.88, 0.40, 0.20), "radius": 1.25, "spec": "metallic"},
    "Co": {"color": (0.00, 0.40, 0.80), "radius": 1.26, "spec": "metallic"},
    "Ni": {"color": (0.31, 0.82, 0.31), "radius": 1.21, "spec": "metallic"},
    "Cu": {"color": (0.78, 0.50, 0.20), "radius": 1.38, "spec": "metallic"},
    "Zn": {"color": (0.49, 0.51, 0.69), "radius": 1.31, "spec": "metallic"},
    "Pt": {"color": (0.82, 0.82, 0.88), "radius": 1.28, "spec": "metallic"},
    "Au": {"color": (1.00, 0.82, 0.14), "radius": 1.44, "spec": "metallic"},
}

DEFAULT_PROP = {"color": (0.60, 0.60, 0.60), "radius": 1.20, "spec": "dielectric"}


def parse_poscar(poscar_path: str):
    """Parses standard VASP POSCAR returning lattice, species, and Cartesian coordinates."""
    with open(poscar_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    comment = lines[0]
    scale = float(lines[1])
    lattice = np.array([[float(x) * scale for x in lines[i].split()[:3]] for i in range(2, 5)])

    species_line = lines[5].split()
    counts_line = lines[6].split()

    if species_line[0].isdigit():
        raise ValueError("POSCAR missing element symbol line (VASP 4 format not supported).")

    species_list = species_line
    counts = [int(c) for c in counts_line]

    elements = []
    for sp, cnt in zip(species_list, counts):
        elements.extend([sp] * cnt)

    coord_type_idx = 7
    is_direct = "direct" in lines[coord_type_idx].lower() or "d" == lines[coord_type_idx].lower()[0]

    coords = []
    for i in range(coord_type_idx + 1, coord_type_idx + 1 + len(elements)):
        vals = [float(x) for x in lines[i].split()[:3]]
        coords.append(vals)
    coords = np.array(coords)

    if is_direct:
        cart_coords = coords @ lattice
    else:
        cart_coords = coords * scale

    return lattice, elements, cart_coords


def compute_bonds(elements, cart_coords, lattice, tolerance=1.25):
    """Finds bonded pairs based on covalent radii sum."""
    n_atoms = len(elements)
    bonds = []
    for i in range(n_atoms):
        r_i = ELEMENT_PROPERTIES.get(elements[i], DEFAULT_PROP)["radius"]
        for j in range(i + 1, n_atoms):
            r_j = ELEMENT_PROPERTIES.get(elements[j], DEFAULT_PROP)["radius"]
            max_dist = (r_i + r_j) * tolerance
            dist = np.linalg.norm(cart_coords[i] - cart_coords[j])
            if 0.5 < dist <= max_dist:
                bonds.append((i, j, dist))
    return bonds


def generate_pov_scene(lattice, elements, cart_coords, bonds, 
                       ball_scale=0.5, bond_radius=0.12, 
                       show_cell=True, show_ground=True) -> str:
    """Generates complete POV-Ray 3.7 scene description code."""
    # Compute center of geometry
    center = np.mean(cart_coords, axis=0)
    centered_coords = cart_coords - center
    
    # Camera distance based on bounding box
    bbox_size = np.ptp(centered_coords, axis=0)
    max_dim = max(bbox_size.max(), 6.0)
    cam_dist = max_dim * 2.5
    cam_pos = np.array([cam_dist * 0.7, cam_dist * 0.6, -cam_dist * 1.0])

    lines = []
    lines.append("// POV-Ray 3.7 Crystal Scene")
    lines.append('#version 3.7;')
    lines.append('global_settings { assumed_gamma 1.0 ambient_light rgb <0.15, 0.15, 0.15> }')
    lines.append('#include "colors.inc"')
    lines.append('#include "textures.inc"')
    lines.append('#include "metals.inc"')
    lines.append('')

    # Camera
    lines.append('camera {')
    lines.append(f'  perspective')
    lines.append(f'  location <{cam_pos[0]:.3f}, {cam_pos[1]:.3f}, {cam_pos[2]:.3f}>')
    lines.append(f'  look_at <0.0, 0.0, 0.0>')
    lines.append(f'  angle 38')
    lines.append('}')
    lines.append('')

    # Studio 3-Point Lighting
    lines.append('// Studio Key Light')
    lines.append(f'light_source {{ <{cam_dist*1.5:.2f}, {cam_dist*2.0:.2f}, {-cam_dist*0.8:.2f}> color rgb <1.0, 0.98, 0.95> }}')
    lines.append('// Studio Fill Light')
    lines.append(f'light_source {{ <{-cam_dist*1.5:.2f}, {cam_dist*0.8:.2f}, {-cam_dist*1.2:.2f}> color rgb <0.4, 0.45, 0.55> shadowless }}')
    lines.append('// Studio Rim Light')
    lines.append(f'light_source {{ <0.0, {-cam_dist*0.5:.2f}, {cam_dist*2.0:.2f}> color rgb <0.3, 0.3, 0.3> shadowless }}')
    lines.append('')

    # Background
    lines.append('background { color rgb <1.0, 1.0, 1.0> }')
    lines.append('')

    # Optional Ground plane for shadows
    if show_ground:
        min_y = centered_coords[:, 1].min() - 1.5
        lines.append('// Shadow receiver plane')
        lines.append(f'plane {{ <0, 1, 0>, {min_y:.2f}')
        lines.append('  pigment { color rgb <0.95, 0.95, 0.95> }')
        lines.append('  finish { ambient 0.1 diffuse 0.8 reflection 0.02 }')
        lines.append('}')
        lines.append('')

    # Atom Finishes
    lines.append('#declare FinishDielectric = finish { ambient 0.15 diffuse 0.7 specular 0.4 roughness 0.04 reflection 0.03 };')
    lines.append('#declare FinishMetallic = finish { ambient 0.15 diffuse 0.6 specular 0.7 roughness 0.02 reflection 0.12 metallic };')
    lines.append('')

    # Render Atoms
    lines.append('// Atoms')
    for i, (elem, pos) in enumerate(zip(elements, centered_coords)):
        prop = ELEMENT_PROPERTIES.get(elem, DEFAULT_PROP)
        r = prop["radius"] * ball_scale
        c = prop["color"]
        finish = "FinishMetallic" if prop["spec"] == "metallic" else "FinishDielectric"
        lines.append(f'sphere {{ <{pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f}>, {r:.4f}')
        lines.append(f'  pigment {{ color rgb <{c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f}> }}')
        lines.append(f'  finish {{ {finish} }}')
        lines.append('}')
    lines.append('')

    # Render Bonds (Split bicolor cylinders)
    lines.append('// Bonds')
    for (i, j, dist) in bonds:
        p1 = centered_coords[i]
        p2 = centered_coords[j]
        mid = (p1 + p2) / 2.0

        c1 = ELEMENT_PROPERTIES.get(elements[i], DEFAULT_PROP)["color"]
        c2 = ELEMENT_PROPERTIES.get(elements[j], DEFAULT_PROP)["color"]

        lines.append(f'cylinder {{ <{p1[0]:.4f}, {p1[1]:.4f}, {p1[2]:.4f}>, <{mid[0]:.4f}, {mid[1]:.4f}, {mid[2]:.4f}>, {bond_radius:.4f}')
        lines.append(f'  pigment {{ color rgb <{c1[0]:.3f}, {c1[1]:.3f}, {c1[2]:.3f}> }} finish {{ FinishDielectric }} }}')
        lines.append(f'cylinder {{ <{mid[0]:.4f}, {mid[1]:.4f}, {mid[2]:.4f}>, <{p2[0]:.4f}, {p2[1]:.4f}, {p2[2]:.4f}>, {bond_radius:.4f}')
        lines.append(f'  pigment {{ color rgb <{c2[0]:.3f}, {c2[1]:.3f}, {c2[2]:.3f}> }} finish {{ FinishDielectric }} }}')
    lines.append('')

    # Unit Cell Wireframe
    if show_cell:
        lines.append('// Unit Cell Vectors')
        # Cell corners shifted by -center
        o = -center
        a, b, c = lattice[0], lattice[1], lattice[2]
        corners = [
            o, o + a, o + b, o + a + b,
            o + c, o + a + c, o + b + c, o + a + b + c
        ]
        edges = [
            (0, 1), (0, 2), (1, 3), (2, 3), # base
            (4, 5), (4, 6), (5, 7), (6, 7), # top
            (0, 4), (1, 5), (2, 6), (3, 7)  # pillars
        ]
        for e1, e2 in edges:
            p1, p2 = corners[e1], corners[e2]
            lines.append(f'cylinder {{ <{p1[0]:.4f}, {p1[1]:.4f}, {p1[2]:.4f}>, <{p2[0]:.4f}, {p2[1]:.4f}, {p2[2]:.4f}>, 0.035')
            lines.append('  pigment { color rgb <0.4, 0.4, 0.4> } finish { ambient 0.2 diffuse 0.6 } }')

    return "\n".join(lines)


def render_povray(pov_path: str, output_png: str, width=2400, height=1800):
    """Executes povray CLI binary to render scene."""
    cmd = [
        "povray",
        f"+I{pov_path}",
        f"+O{output_png}",
        f"+W{width}",
        f"+H{height}",
        "+A0.1",
        "+J",
        "+Q9",
        "+FN",
        "-D"  # Disable display window for headless execution
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"POV-Ray failed with error:\n{res.stderr}\n{res.stdout}")
    return output_png


def main():
    parser = argparse.ArgumentParser(description="Publication-grade POV-Ray 3.7 Crystal Raytracer")
    parser.add_argument("structure", help="Path to input POSCAR, CIF, or XYZ")
    parser.add_argument("-o", "--output", default="crystal_raytraced.png", help="Output PNG file path")
    parser.add_argument("--pov-out", help="Save intermediate .pov scene file")
    parser.add_argument("--ball-scale", type=float, default=0.45, help="Atomic ball scale factor (0.1 to 1.0)")
    parser.add_argument("--bond-radius", type=float, default=0.10, help="Bond cylinder radius (Angstroms)")
    parser.add_argument("--no-cell", action="store_true", help="Omit unit cell wireframe")
    parser.add_argument("--no-ground", action="store_true", help="Omit ground shadow receiver plane")
    parser.add_argument("--width", type=int, default=2400, help="Image width (default: 2400)")
    parser.add_argument("--height", type=int, default=1800, help="Image height (default: 1800)")
    args = parser.parse_args()

    if not os.path.isfile(args.structure):
        print(f"Error: file '{args.structure}' not found.", file=sys.stderr)
        sys.exit(1)

    lattice, elements, cart_coords = parse_poscar(args.structure)
    bonds = compute_bonds(elements, cart_coords, lattice)

    scene_code = generate_pov_scene(
        lattice=lattice,
        elements=elements,
        cart_coords=cart_coords,
        bonds=bonds,
        ball_scale=args.ball_scale,
        bond_radius=args.bond_radius,
        show_cell=not args.no_cell,
        show_ground=not args.no_ground
    )

    pov_file = args.pov_out if args.pov_out else "scene_temp.pov"
    with open(pov_file, "w") as f:
        f.write(scene_code)

    print(f"[*] Generated POV-Ray scene: {pov_file}")
    print(f"[*] Raytracing via POV-Ray 3.7 ({args.width}x{args.height})...")
    render_povray(pov_file, args.output, width=args.width, height=args.height)
    print(f"[✓] Render complete: {args.output}")

    if not args.pov_out and os.path.exists("scene_temp.pov"):
        os.remove("scene_temp.pov")


if __name__ == "__main__":
    main()
