"""
Site Pyramidalization & Circular Zoom Annotator for Scientific Publications.
Generates publication-ready figures featuring:
1. High-resolution circular site zoom-ins with antialiased borders.
2. Shaded 3D coordination polyhedra (tetrahedral pyramidalization).
3. Geometric bond angle arcs (theta_1, theta_2, theta_3) and POAV1 pyramidalization angles.
4. Macro-to-micro curved leader callout arrows.
5. Continuous scalar property mapping (Delta G_ads, Bader charge) with publication colorbars.
6. Multi-panel composite layouts (Panels a, b, e-j) matching Nature/Science standards.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc, Circle, ConnectionPatch, Polygon
from matplotlib.collections import PatchCollection, PolyCollection
import numpy as np

# Ensure scripts directory is in sys.path
_cur_dir = Path(__file__).parent.resolve()
if str(_cur_dir) not in sys.path:
    sys.path.insert(0, str(_cur_dir))

# Import geometry engine
from geometry import (
    SiteGeometry,
    analyze_site_geometry,
    auto_detect_sites,
    compute_poav1,
    export_geometry_report,
)

# Import publication styling from publication-figure-formatter if available
_pub_style_dir = _cur_dir.parent.parent / "publication-figure-formatter" / "scripts"
if _pub_style_dir.exists() and str(_pub_style_dir) not in sys.path:
    sys.path.insert(0, str(_pub_style_dir))

try:
    from style_config import set_publication_style
    from vesta_colors import get_vesta_color, VESTA_ELEMENTS
except ImportError:
    # Fallback styling if isolated
    def set_publication_style(font_size=11, **kwargs):
        plt.rcParams.update({
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": font_size,
        })
    def get_vesta_color(sym):
        colors = {"C": "#2A9D8F", "H": "#F4F4F9", "O": "#E63946", "N": "#457B9D", "Fe": "#E76F51"}
        return colors.get(sym, "#888888")


# Atomic display radii for ball-and-stick rendering (in Angstroms)
ELEMENT_RADII = {
    "H": 0.28, "C": 0.42, "N": 0.40, "O": 0.38, "F": 0.35,
    "P": 0.45, "S": 0.45, "Cl": 0.45, "Fe": 0.52, "Co": 0.50,
    "Ni": 0.50, "Cu": 0.50, "Zn": 0.50, "Pt": 0.55, "Au": 0.55,
}


def load_structure(filepath: Union[str, Path]) -> Tuple[np.ndarray, List[str], Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Loads atomic structure from POSCAR, CIF, or XYZ.
    Returns (positions, symbols, cell, pbc).
    """
    path = Path(filepath).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Structure file not found: {path}")

    # Try ASE first if available
    try:
        from ase.io import read
        atoms = read(str(path))
        return atoms.get_positions(), list(atoms.get_chemical_symbols()), atoms.get_cell()[:], atoms.get_pbc()
    except Exception:
        pass

    # Built-in fallback POSCAR parser
    positions = []
    symbols = []
    cell = np.eye(3)
    pbc = np.array([True, True, True])

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # POSCAR format
    scale = float(lines[1].split()[0])
    cell[0] = [float(x) * scale for x in lines[2].split()[:3]]
    cell[1] = [float(x) * scale for x in lines[3].split()[:3]]
    cell[2] = [float(x) * scale for x in lines[4].split()[:3]]

    species = lines[5].split()
    counts = [int(x) for x in lines[6].split()]

    idx = 7
    coord_type = lines[idx].lower()
    if coord_type.startswith("s"):  # Selective dynamics
        idx += 1
        coord_type = lines[idx].lower()
    is_direct = coord_type.startswith("d") or coord_type.startswith("f")
    idx += 1

    total_atoms = sum(counts)
    for sp, cnt in zip(species, counts):
        for _ in range(cnt):
            parts = [float(x) for x in lines[idx].split()[:3]]
            if is_direct:
                # Direct to Cartesian
                pos = parts[0] * cell[0] + parts[1] * cell[1] + parts[2] * cell[2]
            else:
                pos = np.array(parts) * scale
            positions.append(pos)
            symbols.append(sp)
            idx += 1

    return np.array(positions), symbols, cell, pbc


def rotate_3d(coords: np.ndarray, elev: float = 0.0, azim: float = 0.0) -> np.ndarray:
    """Applies elevation and azimuth rotations to 3D coordinates."""
    if abs(elev) < 1e-4 and abs(azim) < 1e-4:
        return np.copy(coords)
    phi = np.radians(elev)
    theta = np.radians(azim)

    # Rz (azimuth)
    Rz = np.array([
        [np.cos(theta), -np.sin(theta), 0.0],
        [np.sin(theta),  np.cos(theta), 0.0],
        [0.0,            0.0,           1.0],
    ])
    # Rx (elevation)
    Rx = np.array([
        [1.0, 0.0,          0.0],
        [0.0, np.cos(phi), -np.sin(phi)],
        [0.0, np.sin(phi),  np.cos(phi)],
    ])
    R = np.dot(Rx, Rz)
    return np.dot(coords, R.T)


def find_bonds(
    positions: np.ndarray,
    symbols: List[str],
    cutoff_factor: float = 1.15,
) -> List[Tuple[int, int]]:
    """
    Identifies covalent bonds between atoms with strict pair-specific cutoffs
    to prevent spurious diagonal bonds in 4-membered and 8-membered rings.
    """
    pair_max_distances = {
        ("C", "C"): 1.62,
        ("C", "H"): 1.25,
        ("H", "C"): 1.25,
        ("O", "H"): 1.15,
        ("H", "O"): 1.15,
        ("N", "H"): 1.15,
        ("H", "N"): 1.15,
        ("H", "H"): 0.85,
    }
    cov_radii = {
        "H": 0.31, "C": 0.76, "N": 0.74, "O": 0.71, "F": 0.71,
        "P": 1.05, "S": 1.02, "Cl": 0.99, "Fe": 1.24, "Co": 1.25,
    }
    bonds = []
    n = len(positions)
    for i in range(n):
        s_i = symbols[i]
        for j in range(i + 1, n):
            s_j = symbols[j]
            pair_key = (s_i, s_j)
            if pair_key in pair_max_distances:
                max_d = pair_max_distances[pair_key]
            else:
                r_i = cov_radii.get(s_i, 0.76)
                r_j = cov_radii.get(s_j, 0.76)
                max_d = (r_i + r_j) * cutoff_factor

            dist = np.linalg.norm(positions[i] - positions[j])
            if 0.4 < dist <= max_d:
                bonds.append((i, j))
    return bonds


# Publication-grade colors for catalytic and materials figures
PUBLICATION_PALETTE = {
    "C": "#26828E",     # Deep publication sea-teal (Nature Catalysis / ACS style)
    "H": "#FFFFFF",     # Pure white with crisp outline
    "O": "#D62728",     # Deep crimson red
    "N": "#1F77B4",     # Rich cobalt blue
    "Fe": "#E65100",    # Deep iron amber
    "Pt": "#4A148C",    # Noble platinum purple
}


def draw_structure_2d(
    ax: plt.Axes,
    positions: np.ndarray,
    symbols: List[str],
    bonds: Optional[List[Tuple[int, int]]] = None,
    color_override: Optional[Dict[int, str]] = None,
    scalar_values: Optional[np.ndarray] = None,
    cmap_name: str = "coolwarm",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    clip_circle: Optional[Tuple[float, float, float]] = None,
    scale_factor: float = 1.0,
    elev: float = 0.0,
    azim: float = 0.0,
    atom_alpha: float = 1.0,
    bond_color: str = "#2B2B2B",
    bond_width: float = 2.0,
    mask_hydrogens_in_scalar: bool = True,
) -> mpl.cm.ScalarMappable:
    """
    Renders atoms and bonds on a Matplotlib axes with depth sorting and optional circular clipping.
    """
    coords_rot = rotate_3d(positions, elev=elev, azim=azim)
    n_atoms = len(positions)

    if bonds is None:
        bonds = find_bonds(positions, symbols)

    # Scalar colormap setup
    mappable = None
    scalar_colors = {}
    if scalar_values is not None:
        if vmin is None:
            vmin = float(np.min(scalar_values))
        if vmax is None:
            vmax = float(np.max(scalar_values))
        norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        cmap = plt.get_cmap(cmap_name)
        mappable = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
        for i in range(n_atoms):
            if mask_hydrogens_in_scalar and symbols[i] == "H":
                scalar_colors[i] = "#FFFFFF"
            else:
                scalar_colors[i] = cmap(norm(scalar_values[i]))

    # Circular clipping patch if requested
    clip_patch = None
    if clip_circle is not None:
        cx, cy, cr = clip_circle
        clip_patch = Circle((cx, cy), cr, transform=ax.transData)

    # Sort elements by z depth for correct rendering overlap
    z_depths = coords_rot[:, 2]

    # Draw bonds
    for i, j in bonds:
        p1 = coords_rot[i]
        p2 = coords_rot[j]
        line = ax.plot(
            [p1[0], p2[0]], [p1[1], p2[1]],
            color=bond_color, lw=bond_width, solid_capstyle="round",
            zorder=1 + min(p1[2], p2[2]) * 0.01,
        )[0]
        if clip_patch is not None:
            line.set_clip_path(clip_patch)

    # Draw atoms
    sorted_atom_indices = np.argsort(z_depths)
    for idx in sorted_atom_indices:
        p = coords_rot[idx]
        sym = symbols[idx]
        r_disp = ELEMENT_RADII.get(sym, 0.40) * scale_factor

        # Determine color
        if color_override and idx in color_override:
            c = color_override[idx]
        elif scalar_values is not None:
            c = scalar_colors[idx]
        else:
            c = PUBLICATION_PALETTE.get(sym, get_vesta_color(sym))

        edge_c = "#444444" if sym == "H" else "#1A1A1A"
        edge_lw = 0.9 if sym == "H" else 1.1

        circle = Circle(
            (p[0], p[1]), r_disp,
            facecolor=c, edgecolor=edge_c, linewidth=edge_lw,
            alpha=atom_alpha, zorder=2 + p[2] * 0.01,
        )
        if clip_patch is not None:
            circle.set_clip_path(clip_patch)
        ax.add_patch(circle)
    return mappable



def draw_pyramid_polyhedron(
    ax: plt.Axes,
    base_coords_rot: np.ndarray,
    apex_coord_rot: np.ndarray,
    face_color: str = "#2979FF",
    edge_color: str = "#0D47A1",
    alpha: float = 0.45,
    edge_width: float = 1.6,
    clip_patch: Optional[patches.Patch] = None,
):
    """
    Renders the shaded tetrahedral coordination polyhedron (base triangle + 3 side facets)
    projected in 2D with depth sorting.
    """
    b0, b1, b2 = base_coords_rot[0], base_coords_rot[1], base_coords_rot[2]
    ap = apex_coord_rot

    # 4 triangular facets of the tetrahedron
    facets = [
        [b0, b1, b2],      # Base triangle
        [b0, b1, ap],      # Side face 1
        [b1, b2, ap],      # Side face 2
        [b2, b0, ap],      # Side face 3
    ]

    # Sort facets by average z depth
    facet_depths = [np.mean([pt[2] for pt in f]) for f in facets]
    sorted_order = np.argsort(facet_depths)

    for f_idx in sorted_order:
        pts = facets[f_idx]
        poly_pts = np.array([[pt[0], pt[1]] for pt in pts])
        poly = Polygon(
            poly_pts, closed=True,
            facecolor=face_color, edgecolor=edge_color,
            linewidth=edge_width, alpha=alpha,
            zorder=3 + facet_depths[f_idx] * 0.01,
        )
        if clip_patch is not None:
            poly.set_clip_path(clip_patch)
        ax.add_patch(poly)


def draw_bond_angle_arcs(
    ax: plt.Axes,
    site_coord_rot: np.ndarray,
    neighbor_coords_rot: np.ndarray,
    angles_deg: List[float],
    arc_radius: float = 0.65,
    arc_color: str = "#E53935",
    text_color: str = "#D32F2F",
    font_size: int = 9,
    clip_patch: Optional[patches.Patch] = None,
):
    """
    Draws red circular arcs indicating bond angles theta_1, theta_2, theta_3
    between the 3 neighbors, with bold red mathematical labels.
    """
    s = site_coord_rot[:2]
    u_list = []
    angles_polar = []

    for nb in neighbor_coords_rot:
        v = nb[:2] - s
        norm_v = np.linalg.norm(v)
        if norm_v < 1e-4:
            continue
        u = v / norm_v
        u_list.append(u)
        ang = np.degrees(np.arctan2(u[1], u[0])) % 360.0
        angles_polar.append(ang)

    if len(angles_polar) < 3:
        return

    # Sort neighbor vectors angularly
    ang_sort = np.argsort(angles_polar)
    sorted_angles = [angles_polar[i] for i in ang_sort]

    # Label sequence: theta_1, theta_2, theta_3
    label_names = [r"$\theta_1$", r"$\theta_2$", r"$\theta_3$"]

    for k in range(3):
        a_start = sorted_angles[k]
        a_end = sorted_angles[(k + 1) % 3]
        if a_end < a_start:
            a_end += 360.0
        span = a_end - a_start
        if span > 180.0:
            # Take the acute angle between adjacent bonds
            a_start, a_end = a_end, a_start + 360.0
            span = a_end - a_start

        # Draw Arc
        arc = Arc(
            (s[0], s[1]),
            width=2 * arc_radius,
            height=2 * arc_radius,
            angle=0.0,
            theta1=a_start,
            theta2=a_end,
            color=arc_color,
            lw=1.4,
            zorder=5,
        )
        if clip_patch is not None:
            arc.set_clip_path(clip_patch)
        ax.add_patch(arc)

        # Place label at arc midpoint
        mid_ang = np.radians(a_start + span * 0.5)
        r_text = arc_radius * 1.45
        tx = s[0] + r_text * np.cos(mid_ang)
        ty = s[1] + r_text * np.sin(mid_ang)
        txt = ax.text(
            tx, ty, label_names[k],
            color=text_color, fontsize=font_size, fontweight="bold",
            ha="center", va="center", zorder=6,
        )
        if clip_patch is not None:
            txt.set_clip_path(clip_patch)


def extract_local_cluster(
    positions: np.ndarray,
    symbols: List[str],
    site_idx: int,
    radius: float = 4.8,
    out_dir: Union[str, Path] = "/tmp/site_clusters",
) -> Tuple[str, List[int]]:
    """Carves out a cluster around site_idx and saves a clean VASP file."""
    out_p = Path(out_dir).resolve()
    out_p.mkdir(parents=True, exist_ok=True)
    site_pos = positions[site_idx]
    dists = np.linalg.norm(positions - site_pos, axis=1)
    mask = dists <= radius
    indices = np.where(mask)[0].tolist()

    sub_pos = positions[indices] - site_pos + np.array([10.0, 10.0, 10.0])
    sub_syms = [symbols[i] for i in indices]

    vasp_file = out_p / f"cluster_site_{site_idx}.vasp"
    with open(vasp_file, "w") as f:
        f.write(f"Cluster around site {symbols[site_idx]}{site_idx} radius {radius:.1f}A\n")
        f.write("1.0\n")
        f.write(" 20.00000000   0.00000000   0.00000000\n")
        f.write("  0.00000000  20.00000000   0.00000000\n")
        f.write("  0.00000000   0.00000000  20.00000000\n")
        elem_order = []
        elem_counts = {}
        for s in sub_syms:
            if s not in elem_counts:
                elem_order.append(s)
                elem_counts[s] = 0
            elem_counts[s] += 1
        f.write(" " + "   ".join(elem_order) + "\n")
        f.write(" " + "   ".join(str(elem_counts[s]) for s in elem_order) + "\n")
        f.write("Cartesian\n")
        for s in elem_order:
            for idx_local, sym in enumerate(sub_syms):
                if sym == s:
                    p = sub_pos[idx_local]
                    f.write(f" {p[0]:15.8f} {p[1]:15.8f} {p[2]:15.8f}\n")

    return str(vasp_file), indices


def render_ovito_cluster(
    vasp_path: str,
    view: str = "c",
    particle_radius: float = 0.38,
    bond_width: float = 0.16,
    out_dir: str = "/tmp/ovito_site_renders",
) -> Optional[str]:
    """Renders 3D cluster using headless OVITO."""
    import subprocess
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    stem = Path(vasp_path).stem
    out_file = Path(out_dir) / f"{stem}_view_{view}.png"
    cmd = [
        "ovito-snapshot", vasp_path,
        "-v", view,
        "--particle-radius", str(particle_radius),
        "--bond-width", str(bond_width),
        "--no-tripod",
        "--no-cell",
        "--background", "white",
        "-o", out_dir,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if out_file.exists():
            return str(out_file)
    except Exception:
        pass
    return None


def render_vesta_cluster(
    vasp_path: str,
    view: str = "c",
    out_dir: str = "/tmp/vesta_site_renders",
) -> Optional[str]:
    """Renders 3D cluster using desktop VESTA automation on X11."""
    import subprocess
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    stem = Path(vasp_path).stem
    out_file = Path(out_dir) / f"{stem}_vesta_view_{view}.png"
    cmd = [
        "vesta-snapshot", vasp_path,
        "-v", view,
        "-o", out_dir,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if out_file.exists():
            return str(out_file)
    except Exception:
        pass
    return None


def get_circular_masked_image(
    image_path: str,
    target_size: Optional[int] = None,
):
    """Crops center square from rendered image and applies an antialiased circular mask."""
    try:
        from PIL import Image, ImageDraw
        img = Image.open(image_path).convert("RGBA")
        w, h = img.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        cropped = img.crop((left, top, left + side, top + side))
        if target_size:
            cropped = cropped.resize((target_size, target_size), Image.Resampling.LANCZOS)
            side = target_size

        scale = 2
        mask = Image.new("L", (side * scale, side * scale), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, side * scale - 1, side * scale - 1), fill=255)
        mask = mask.resize((side, side), Image.Resampling.LANCZOS)

        masked_img = Image.new("RGBA", (side, side), (255, 255, 255, 0))
        masked_img.paste(cropped, (0, 0), mask=mask)
        return masked_img
    except Exception:
        return None


def render_circular_site_zoom(
    positions: np.ndarray,
    symbols: List[str],
    site_idx: int,
    output_path: Union[str, Path],
    radius_zoom: float = 4.8,
    draw_polyhedron: bool = True,
    draw_arcs: bool = False,
    elev: float = 15.0,
    azim: float = -30.0,
    panel_title: Optional[str] = None,
    backend: str = "native",
    cell: Optional[np.ndarray] = None,
    pbc: Optional[np.ndarray] = None,
    dpi: int = 300,
):
    """
    Renders an isolated circular zoom panel for a designated active site.
    Supports backends: 'native' (pure Matplotlib vector), 'ovito' (headless 3D), 'vesta' (desktop VESTA).
    """
    set_publication_style(font_size=11)
    fig, ax = plt.subplots(figsize=(4.0, 4.0), dpi=dpi)
    ax.set_aspect("equal")
    ax.axis("off")

    geom = analyze_site_geometry(positions, symbols, site_idx, cell=cell, pbc=pbc)
    site_pos = geom.site_position

    cx, cy, cr = 0.0, 0.0, radius_zoom
    clip_circle = (cx, cy, cr)
    clip_patch = Circle((cx, cy), cr, transform=ax.transData)

    # Dispatch Rendering Backend
    rendered_external = False
    if backend in ["ovito", "vesta"]:
        vasp_cluster, _ = extract_local_cluster(positions, symbols, site_idx, radius=radius_zoom)
        img_file = None
        if backend == "ovito":
            img_file = render_ovito_cluster(vasp_cluster, view="c")
        elif backend == "vesta":
            img_file = render_vesta_cluster(vasp_cluster, view="c")

        if img_file and Path(img_file).exists():
            masked_img = get_circular_masked_image(img_file)
            if masked_img is not None:
                ax.imshow(masked_img, extent=[-cr, cr, -cr, cr], origin="upper", zorder=1)
                rendered_external = True

    # Fallback to Native Vector Engine if external backend wasn't used or failed
    if not rendered_external:
        dists = np.linalg.norm(positions - site_pos, axis=1)
        local_mask = dists <= (radius_zoom + 0.5)
        local_indices = np.where(local_mask)[0]

        local_pos = positions[local_indices] - site_pos
        local_syms = [symbols[i] for i in local_indices]
        old_to_new = {old: new for new, old in enumerate(local_indices)}
        new_site_idx = old_to_new[site_idx]
        local_bonds = find_bonds(local_pos, local_syms)

        draw_structure_2d(
            ax, local_pos, local_syms,
            bonds=local_bonds,
            clip_circle=clip_circle,
            elev=elev, azim=azim,
            scale_factor=1.1,
        )

        local_pos_rot = rotate_3d(local_pos, elev=elev, azim=azim)

        # Draw Polyhedron if requested
        if draw_polyhedron and len(geom.neighbor_indices) == 3:
            nb_rot = [local_pos_rot[old_to_new[nb]] for nb in geom.neighbor_indices if nb in old_to_new]
            if len(nb_rot) == 3:
                if geom.adsorbate_index is not None and geom.adsorbate_index in old_to_new:
                    apex_rot = local_pos_rot[old_to_new[geom.adsorbate_index]]
                else:
                    apex_rot = local_pos_rot[new_site_idx]

                draw_pyramid_polyhedron(
                    ax, np.array(nb_rot), apex_rot,
                    face_color="#2979FF", edge_color="#0D47A1",
                    alpha=0.50, clip_patch=clip_patch,
                )

        # Draw Angle Arcs if requested
        if draw_arcs and len(geom.neighbor_indices) == 3:
            nb_rot = [local_pos_rot[old_to_new[nb]] for nb in geom.neighbor_indices if nb in old_to_new]
            if len(nb_rot) == 3:
                site_rot = local_pos_rot[new_site_idx]
                draw_bond_angle_arcs(
                    ax, site_rot, np.array(nb_rot),
                    angles_deg=geom.bond_angles_deg,
                    clip_patch=clip_patch,
                )

    # Draw Crisp Circular Border Outline
    border_circle = Circle(
        (cx, cy), cr,
        facecolor="none", edgecolor="#111111", linewidth=2.0,
        zorder=10,
    )
    ax.add_patch(border_circle)

    # Panel title (e.g. "e) S1")
    if panel_title:
        ax.text(
            -cr * 0.95, cr * 1.08, panel_title,
            fontsize=13, fontweight="bold", ha="left", va="bottom",
        )

    pad = cr * 1.18
    ax.set_xlim(-pad, pad)
    ax.set_ylim(-pad, pad)

    out_p = Path(output_path).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_p, dpi=dpi, bbox_inches="tight", transparent=False)
    plt.close(fig)
    return str(out_p)


def render_full_composite_figure(
    structure_path: Union[str, Path],
    site_dict: Dict[str, int],  # e.g. {"S1": 17, "S2": 25, ...}
    property_csv_path: Optional[Union[str, Path]] = None,
    property_col: str = "dG_ads_eV",
    colorbar_label: str = r"$\Delta G_{\mathrm{ads}}\ (\mathrm{eV})$",
    output_path: Union[str, Path] = "composite_site_pyramidalization.png",
    active_pyramid_site: str = "S6",
    backend: str = "native",
    radius_zoom: float = 4.8,
    dpi: int = 300,
):
    """
    Renders a complete, publication-ready multi-panel figure matching Panels a, b, and e-j:
    - Panel a: Macro structure color-coded by scalar property (Delta G_ads) with colorbar,
      dashed boundary box, and site labels S1-S6.
    - Panel b: Perspective macro view of the substrate, with red angle arcs around active site,
      curved leader arrow, and circular zoom inset displaying the shaded pyramidalization tetrahedron!
    - Panels e-j: Circular zoom panels for designated sites S1 through S6.
    """
    set_publication_style(font_size=11)
    positions, symbols, cell, pbc = load_structure(structure_path)

    # Read property data if provided
    scalar_values = None
    if property_csv_path is not None and Path(property_csv_path).exists():
        import pandas as pd
        df = pd.read_csv(property_csv_path)
        col = property_col if property_col in df.columns else df.columns[1]
        scalar_dict = dict(zip(df["atom_index"].astype(int), df[col].astype(float)))
        scalar_values = np.array([scalar_dict.get(i, 0.0) for i in range(len(positions))])

    # Canvas Setup: 2 Main panels (a, b) on left, 6 circular zooms (e-j) on right
    fig = plt.figure(figsize=(13.0, 7.5), dpi=dpi)

    gs = fig.add_gridspec(
        6, 12,
        left=0.04, right=0.98, top=0.95, bottom=0.05,
        wspace=0.35, hspace=0.35,
    )

    # -------------------------------------------------------------
    # PANEL A: Macro Property Map (Delta G_ads)
    # -------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0:3, 0:7])
    ax_a.set_aspect("equal")
    ax_a.axis("off")
    ax_a.text(0.01, 0.98, "a)", transform=ax_a.transAxes, fontsize=15, fontweight="bold", va="top")

    bonds = find_bonds(positions, symbols)
    mappable = draw_structure_2d(
        ax_a, positions, symbols,
        bonds=bonds,
        scalar_values=scalar_values,
        cmap_name="coolwarm",
        vmin=-1.2, vmax=1.2,
        scale_factor=0.9,
    )

    # Dashed bounding box
    min_x, max_x = np.min(positions[:, 0]) - 1.0, np.max(positions[:, 0]) + 1.0
    min_y, max_y = np.min(positions[:, 1]) - 1.0, np.max(positions[:, 1]) + 1.0
    rect = patches.Rectangle(
        (min_x, min_y), max_x - min_x, max_y - min_y,
        fill=False, edgecolor="#777777", linestyle="--", linewidth=1.2,
    )
    ax_a.add_patch(rect)

    # Site labels S1 - S6 in distinct publication colors
    site_colors = {
        "S1": "#880E4F", "S2": "#827717", "S3": "#0D47A1",
        "S4": "#4A148C", "S5": "#1B5E20", "S6": "#BF360C",
    }
    for name, s_idx in site_dict.items():
        if s_idx < len(positions):
            p = positions[s_idx]
            c = site_colors.get(name, "#111111")
            ax_a.text(
                p[0] + 0.35, p[1] - 0.25, name,
                fontsize=9.5, fontweight="bold", color=c, zorder=12,
            )

    ax_a.set_xlim(min_x - 0.8, max_x + 0.8)
    ax_a.set_ylim(min_y - 0.8, max_y + 0.8)

    # Add Colorbar for Panel a
    if mappable is not None:
        cax = ax_a.inset_axes([-0.09, 0.15, 0.025, 0.70])
        cbar = fig.colorbar(mappable, cax=cax, orientation="vertical")
        cbar.set_label(colorbar_label, fontsize=10.5)
        cbar.ax.tick_params(labelsize=9)

    # -------------------------------------------------------------
    # PANEL B: Perspective Macro View with Pyramidalization Callout
    # -------------------------------------------------------------
    ax_b = fig.add_subplot(gs[3:6, 0:7])
    ax_b.set_aspect("equal")
    ax_b.axis("off")
    ax_b.text(0.01, 0.98, "b)", transform=ax_b.transAxes, fontsize=15, fontweight="bold", va="top")

    macro_elev, macro_azim = 0.0, 0.0
    coords_macro = rotate_3d(positions, elev=macro_elev, azim=macro_azim)

    draw_structure_2d(
        ax_b, positions, symbols,
        bonds=bonds,
        elev=macro_elev, azim=macro_azim,
        scale_factor=0.9,
    )

    pyramid_idx = site_dict.get(active_pyramid_site, 0)
    p_site = coords_macro[pyramid_idx]

    r_target = 1.3
    target_circle = Circle(
        (p_site[0], p_site[1]), r_target,
        facecolor="none", edgecolor="#222222", linewidth=1.4, zorder=8,
    )
    ax_b.add_patch(target_circle)

    geom_active = analyze_site_geometry(positions, symbols, pyramid_idx, cell=cell, pbc=pbc)
    if len(geom_active.neighbor_indices) == 3:
        nb_coords = np.array([coords_macro[i] for i in geom_active.neighbor_indices])
        draw_bond_angle_arcs(
            ax_b, p_site, nb_coords,
            angles_deg=geom_active.bond_angles_deg,
            arc_radius=0.75, font_size=8.5,
        )

    # Inset Axes for Magnified Pyramidalization Zoom (Tetrahedron)
    ax_inset = ax_b.inset_axes([0.64, 0.28, 0.42, 0.72])
    ax_inset.set_aspect("equal")
    ax_inset.axis("off")

    inset_elev, inset_azim = 20.0, -35.0
    r_inset_zoom = 4.2
    dists_site = np.linalg.norm(positions - geom_active.site_position, axis=1)
    inset_mask = dists_site <= (r_inset_zoom + 0.5)
    inset_indices = np.where(inset_mask)[0]

    inset_pos = positions[inset_indices] - geom_active.site_position
    inset_syms = [symbols[i] for i in inset_indices]
    inset_bonds = find_bonds(inset_pos, inset_syms)

    inset_clip = Circle((0, 0), r_inset_zoom, transform=ax_inset.transData)

    draw_structure_2d(
        ax_inset, inset_pos, inset_syms,
        bonds=inset_bonds,
        clip_circle=(0, 0, r_inset_zoom),
        elev=inset_elev, azim=inset_azim,
        scale_factor=1.1,
    )

    inset_map = {old: new for new, old in enumerate(inset_indices)}
    inset_rot = rotate_3d(inset_pos, elev=inset_elev, azim=inset_azim)
    nb_rot = [inset_rot[inset_map[i]] for i in geom_active.neighbor_indices if i in inset_map]

    if len(nb_rot) == 3:
        if geom_active.adsorbate_index is not None and geom_active.adsorbate_index in inset_map:
            apex_rot = inset_rot[inset_map[geom_active.adsorbate_index]]
        else:
            apex_rot = inset_rot[inset_map[pyramid_idx]]

        draw_pyramid_polyhedron(
            ax_inset, np.array(nb_rot), apex_rot,
            face_color="#2979FF", edge_color="#0D47A1",
            alpha=0.55, clip_patch=inset_clip,
        )

    inset_border = Circle(
        (0, 0), r_inset_zoom,
        facecolor="none", edgecolor="#111111", linewidth=2.0, zorder=10,
    )
    ax_inset.add_patch(inset_border)
    pad_in = r_inset_zoom * 1.05
    ax_inset.set_xlim(-pad_in, pad_in)
    ax_inset.set_ylim(-pad_in, pad_in)

    # Curved Callout Arrow
    con = ConnectionPatch(
        xyA=(p_site[0] + r_target * 0.707, p_site[1] + r_target * 0.707),
        coordsA=ax_b.transData,
        xyB=(0.0, 0.5),
        coordsB=ax_inset.transAxes,
        arrowstyle="->,head_width=0.35,head_length=0.6",
        connectionstyle="arc3,rad=-0.28",
        shrinkA=3, shrinkB=6,
        lw=1.6, color="#111111", zorder=20,
    )
    ax_b.add_artist(con)

    ax_b.set_xlim(min_x - 0.8, max_x + 0.8)
    ax_b.set_ylim(min_y - 0.8, max_y + 0.8)

    # -------------------------------------------------------------
    # PANELS E - J: Circular Zoom Grid for S1 - S6
    # -------------------------------------------------------------
    site_names = ["S1", "S2", "S3", "S4", "S5", "S6"]
    panel_letters = ["e)", "f)", "g)", "h)", "i)", "j)"]

    grid_locs = [
        (0, 7),  # e) S1
        (2, 7),  # f) S2
        (4, 7),  # g) S3
        (0, 9),  # h) S4
        (2, 9),  # i) S5
        (4, 9),  # j) S6
    ]

    for k, (s_name, letter) in enumerate(zip(site_names, panel_letters)):
        if s_name not in site_dict:
            continue
        curr_idx = site_dict[s_name]
        r_start, c_start = grid_locs[k]
        ax_zoom = fig.add_subplot(gs[r_start:r_start + 2, c_start:c_start + 2])
        ax_zoom.set_aspect("equal")
        ax_zoom.axis("off")

        # External 3D Backend Support (OVITO / VESTA)
        rendered_external = False
        if backend in ["ovito", "vesta"]:
            vasp_sub, _ = extract_local_cluster(positions, symbols, curr_idx, radius=radius_zoom)
            img_sub = None
            if backend == "ovito":
                img_sub = render_ovito_cluster(vasp_sub, view="c")
            elif backend == "vesta":
                img_sub = render_vesta_cluster(vasp_sub, view="c")

            if img_sub and Path(img_sub).exists():
                masked_sub = get_circular_masked_image(img_sub)
                if masked_sub is not None:
                    ax_zoom.imshow(masked_sub, extent=[-radius_zoom, radius_zoom, -radius_zoom, radius_zoom], origin="upper", zorder=1)
                    rendered_external = True

        if not rendered_external:
            g_site = analyze_site_geometry(positions, symbols, curr_idx, cell=cell, pbc=pbc)
            dists_k = np.linalg.norm(positions - g_site.site_position, axis=1)
            k_mask = dists_k <= (radius_zoom + 0.5)
            k_indices = np.where(k_mask)[0]

            k_pos = positions[k_indices] - g_site.site_position
            k_syms = [symbols[i] for i in k_indices]
            k_bonds = find_bonds(k_pos, k_syms)

            draw_structure_2d(
                ax_zoom, k_pos, k_syms,
                bonds=k_bonds,
                clip_circle=(0, 0, radius_zoom),
                elev=5.0, azim=-15.0,
                scale_factor=1.05,
            )

        circ_border = Circle(
            (0, 0), radius_zoom,
            facecolor="none", edgecolor="#111111", linewidth=1.8, zorder=10,
        )
        ax_zoom.add_patch(circ_border)

        ax_zoom.text(
            -radius_zoom * 0.95, radius_zoom * 1.08,
            f"{letter} {s_name}",
            fontsize=12, fontweight="bold", ha="left", va="bottom",
        )

        pad_k = radius_zoom * 1.15
        ax_zoom.set_xlim(-pad_k, pad_k)
        ax_zoom.set_ylim(-pad_k, pad_k)

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_file, dpi=dpi, bbox_inches="tight")
    pdf_file = out_file.with_suffix(".pdf")
    plt.savefig(pdf_file, bbox_inches="tight")
    plt.close(fig)

    return str(out_file), str(pdf_file)


def main():
    parser = argparse.ArgumentParser(
        description="Site Pyramidalization & Circular Zoom Annotator for Publications",
    )
    parser.add_argument("input", help="Structure file (POSCAR, CIF, XYZ)")
    parser.add_argument("--site", "-s", type=int, help="Single active site index (0-based or 1-based)")
    parser.add_argument("--sites", type=str, help="Comma-separated sites (e.g. '17,25,30' or 'S1:17,S2:25,S3:30,S4:35,S5:28,S6:29')")
    parser.add_argument("--auto-sites", action="store_true", help="Automatically detect top catalytic/adsorption sites")
    parser.add_argument("--auto-mode", choices=["all", "adsorbate", "strain"], default="all", help="Auto-detection mode (default: 'all')")
    parser.add_argument("--top-n", type=int, default=6, help="Number of sites to auto-detect (default: 6)")
    parser.add_argument("--backend", choices=["native", "ovito", "vesta"], default="native", help="Visualizer backend for circular snapshots")
    parser.add_argument("--radius", "-r", type=float, default=4.8, help="Zoom circle radius in Angstroms (default: 4.8)")
    parser.add_argument("--polyhedron", action="store_true", help="Draw shaded coordination tetrahedron")
    parser.add_argument("--arcs", action="store_true", help="Draw red bond angle arcs (theta_1, theta_2, theta_3)")
    parser.add_argument("--elev", type=float, default=15.0, help="Camera elevation angle in degrees")
    parser.add_argument("--azim", type=float, default=-30.0, help="Camera azimuth angle in degrees")
    parser.add_argument("--property-csv", type=str, help="Path to CSV containing per-atom scalar values")
    parser.add_argument("--property-col", type=str, default="dG_ads_eV", help="Column name in property CSV")
    parser.add_argument("--colorbar-label", type=str, default=r"$\Delta G_{\mathrm{ads}}\ (\mathrm{eV})$", help="Colorbar label (supports LaTeX)")
    parser.add_argument("--composite", action="store_true", help="Generate full multi-panel publication composite figure")
    parser.add_argument("--pyramid-site", type=str, default="S6", help="Site name to feature with pyramid callout in composite mode")
    parser.add_argument("--output-dir", "-o", default="./figures", help="Directory to save output figures")
    parser.add_argument("--prefix", "-p", default="site_zoom", help="Output filename prefix")
    parser.add_argument("--dpi", type=int, default=300, help="Figure resolution DPI (default: 300)")

    args = parser.parse_args()

    positions, symbols, cell, pbc = load_structure(args.input)
    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Site Selection & Auto-Detection
    site_dict = {}
    if args.sites:
        items = args.sites.split(",")
        for item in items:
            item = item.strip()
            if ":" in item:
                k, v = item.split(":")
                site_dict[k.strip()] = int(v.strip())
            else:
                idx = int(item)
                site_dict[f"S{len(site_dict)+1}"] = idx
    elif args.site is not None:
        site_dict["S1"] = args.site
    else:
        # Default to automated site detection
        site_dict = auto_detect_sites(
            positions, symbols, cell=cell, pbc=pbc,
            mode=args.auto_mode, top_n=args.top_n,
        )
        print(f"[+] Automatically identified {len(site_dict)} top active sites ({args.auto_mode} mode): {site_dict}")

    # Optimal Geometric Calculations
    site_geometries = []
    print("=" * 82)
    print(f" SITE PYRAMIDALIZATION & COORDINATION GEOMETRY ANALYSIS (POAV1) [Backend: {args.backend}]")
    print("=" * 82)
    print(f"{'Site':<6} {'Idx':<6} {'Sym':<4} {'Neighbors':<14} {'Angles (deg)':<22} {'theta_p':<10} {'Height':<8} {'Vol (A^3)':<8}")
    print("-" * 82)

    for s_name, s_idx in site_dict.items():
        if s_idx >= len(positions):
            continue
        geom = analyze_site_geometry(positions, symbols, s_idx, cell=cell, pbc=pbc)
        site_geometries.append(geom)
        nb_str = ",".join([f"{symbols[i]}{i}" for i in geom.neighbor_indices])
        ang_str = f"[{geom.bond_angles_deg[0]:.1f}, {geom.bond_angles_deg[1]:.1f}, {geom.bond_angles_deg[2]:.1f}]"
        print(f"{s_name:<6} {s_idx:<6} {geom.site_symbol:<4} {nb_str:<14} {ang_str:<22} {geom.poav1_theta_p_deg:>6.2f}° {geom.puckering_height_ang:>6.3f}Å {geom.polyhedron_volume_ang3:>7.4f}")
    print("=" * 82)

    # Save Structured Optimal Geometry Reports (JSON + CSV)
    json_path = out_dir / f"{args.prefix}_analysis_report.json"
    csv_path = out_dir / f"{args.prefix}_analysis_report.csv"
    export_geometry_report(site_geometries, str(json_path), str(csv_path))
    print(f"\n[+] Optimal geometry analysis reports generated:")
    print(f"    JSON: {json_path}")
    print(f"    CSV:  {csv_path}")

    # 1. Full Multi-Panel Composite Mode
    if args.composite:
        composite_path = out_dir / f"{args.prefix}_composite.png"
        png_p, pdf_p = render_full_composite_figure(
            structure_path=args.input,
            site_dict=site_dict,
            property_csv_path=args.property_csv,
            property_col=args.property_col,
            colorbar_label=args.colorbar_label,
            output_path=composite_path,
            active_pyramid_site=args.pyramid_site,
            backend=args.backend,
            radius_zoom=args.radius,
            dpi=args.dpi,
        )
        print(f"\n[+] Publication composite figure successfully generated:")
        print(f"    PNG: {png_p}")
        print(f"    PDF: {pdf_p}")

    # 2. Individual Site Circular Zoom Insets
    for s_name, s_idx in site_dict.items():
        if s_idx >= len(positions):
            continue
        site_out = out_dir / f"{args.prefix}_{s_name}.png"
        p = render_circular_site_zoom(
            positions=positions,
            symbols=symbols,
            site_idx=s_idx,
            output_path=site_out,
            radius_zoom=args.radius,
            draw_polyhedron=args.polyhedron,
            draw_arcs=args.arcs,
            elev=args.elev,
            azim=args.azim,
            panel_title=f"{s_name}",
            backend=args.backend,
            cell=cell,
            pbc=pbc,
            dpi=args.dpi,
        )
        print(f"[+] Circular zoom snapshot saved: {p}")


if __name__ == "__main__":
    main()

