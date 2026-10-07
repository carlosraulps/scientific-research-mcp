#!/home/cr/.local/share/mamba/envs/vasp-env/bin/python
"""
================================================================================
Publication-Grade 3D Brillouin Zone Visualizer (bz-visualizer)
================================================================================
Constructs the exact 1st Brillouin Zone (Wigner-Seitz cell of reciprocal lattice)
via Voronoi tessellation for any crystal structure (POSCAR, CIF, or lattice params).
Renders:
  - Outer BZ wireframe with depth-tested solid front and dashed rear edges
  - Reciprocal basis vectors (b1, b2, b3) with 3D arrow heads
  - High-symmetry k-points (Gamma, M, K, A, L, H, etc.) with LaTeX STIX math labels
  - Highlighted high-symmetry paths and translucent shaded irreducible prisms/wedges
  - Publication formatting matching Physical Review, Nature, and ACS standards
================================================================================
"""

import os
import sys
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Voronoi

try:
    import seekpath
    HAS_SEEKPATH = True
except ImportError:
    HAS_SEEKPATH = False

try:
    from pymatgen.core import Structure
    HAS_PYMATGEN = True
except ImportError:
    HAS_PYMATGEN = False

# Publication font styling
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "figure.dpi": 300
})


def parse_poscar_lattice(file_path: str) -> np.ndarray:
    """Extracts 3x3 lattice vector matrix from VASP POSCAR."""
    with open(file_path, "r") as f:
        _ = f.readline()  # comment
        scale = float(f.readline().strip())
        lattice = []
        for _ in range(3):
            lattice.append([float(x) * scale for x in f.readline().split()[:3]])
    return np.array(lattice)


def compute_reciprocal_lattice(lattice: np.ndarray) -> np.ndarray:
    """Computes reciprocal lattice vectors B = 2*pi * (A^-1)^T."""
    return 2.0 * np.pi * np.linalg.inv(lattice).T


def compute_brillouin_zone_voronoi(b_matrix: np.ndarray) -> tuple:
    """
    Computes 1st Brillouin Zone as the Voronoi cell around origin (0,0,0)
    in a 3x3x3 reciprocal lattice grid.
    Returns: (vertices, edges_set, faces_list)
    """
    b1, b2, b3 = b_matrix[0], b_matrix[1], b_matrix[2]
    points = []
    for h in [-1, 0, 1]:
        for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
                points.append(h * b1 + k * b2 + l * b3)
    points = np.array(points)

    origin_idx = 13  # (0, 0, 0)
    vor = Voronoi(points)
    origin_region = vor.point_region[origin_idx]
    bz_verts = vor.vertices[vor.regions[origin_region]]

    bz_edges = set()
    bz_faces = []
    for (p1, p2), ridge in zip(vor.ridge_points, vor.ridge_vertices):
        if p1 == origin_idx or p2 == origin_idx:
            if all(v >= 0 for v in ridge):
                face_pts = [vor.vertices[v] for v in ridge]
                bz_faces.append(face_pts)
                for i in range(len(ridge)):
                    e = tuple(sorted([ridge[i], ridge[(i + 1) % len(ridge)]]))
                    bz_edges.add(e)

    return bz_verts, bz_edges, bz_faces, vor


def render_brillouin_zone(
    lattice: np.ndarray,
    output_path: str = "brillouin_zone.png",
    elev: float = 22,
    azim: float = -78,
    crystal_type: str = "hexagonal",
    highlight_prism: bool = True,
    panel_label: str = "(e)",
    color_accent: str = "#1850b8",
    color_fill: str = "#4c78d4"
) -> str:
    """Renders 3D publication-quality Brillouin zone figure."""
    # Compute reciprocal lattice vectors
    B = compute_reciprocal_lattice(lattice)
    b1, b2, b3 = B[0], B[1], B[2]

    # Detect crystal system or use parameter
    lengths = [np.linalg.norm(lattice[i]) for i in range(3)]
    angles = [
        np.degrees(np.arccos(np.dot(lattice[1], lattice[2]) / (lengths[1] * lengths[2]))),
        np.degrees(np.arccos(np.dot(lattice[0], lattice[2]) / (lengths[0] * lengths[2]))),
        np.degrees(np.arccos(np.dot(lattice[0], lattice[1]) / (lengths[0] * lengths[1]))),
    ]
    is_orthorhombic = crystal_type.lower() in ["orthorhombic", "ortho"] or (
        np.allclose(angles, 90.0, atol=1.5) and not np.isclose(lengths[0], lengths[1], atol=0.05)
    )

    if crystal_type.lower() in ["hexagonal", "hex", "trigonal"]:
        b_mag = np.linalg.norm(b1)
        b3_mag = np.linalg.norm(b3)
        b1 = b_mag * np.array([-np.cos(np.radians(30)), -np.sin(np.radians(30)), 0.0])
        b2 = b_mag * np.array([ np.cos(np.radians(30)), -np.sin(np.radians(30)), 0.0])
        b3 = np.array([0.0, 0.0, b3_mag])
        B = np.array([b1, b2, b3])

    bz_verts, bz_edges, bz_faces, vor = compute_brillouin_zone_voronoi(B)

    gamma = np.array([0.0, 0.0, 0.0])

    if is_orthorhombic:
        b1_mag = np.linalg.norm(b1)
        b2_mag = np.linalg.norm(b2)
        b3_mag = np.linalg.norm(b3)
        kx = b1_mag / 2.0
        ky = b2_mag / 2.0
        kz = b3_mag / 2.0

        prism_vertices = {
            "\\Gamma": gamma,
            "X": np.array([kx, 0.0, 0.0]),
            "S": np.array([kx, ky, 0.0]),
            "Y": np.array([0.0, ky, 0.0]),
            "Z": np.array([0.0, 0.0, kz]),
            "U": np.array([kx, 0.0, kz]),
            "R": np.array([kx, ky, kz]),
            "T": np.array([0.0, ky, kz]),
        }
        X_pt, S_pt, Y_pt = prism_vertices["X"], prism_vertices["S"], prism_vertices["Y"]
        Z_pt, U_pt, R_pt, T_pt = prism_vertices["Z"], prism_vertices["U"], prism_vertices["R"], prism_vertices["T"]

        prism_faces = [
            [gamma, X_pt, S_pt, Y_pt],
            [Z_pt, U_pt, R_pt, T_pt],
            [gamma, X_pt, U_pt, Z_pt],
            [X_pt, S_pt, R_pt, U_pt],
            [S_pt, Y_pt, T_pt, R_pt],
            [Y_pt, gamma, Z_pt, T_pt],
        ]
        prism_edges = [
            (gamma, X_pt), (X_pt, S_pt), (S_pt, Y_pt), (Y_pt, gamma),
            (Z_pt, U_pt), (U_pt, R_pt), (R_pt, T_pt), (T_pt, Z_pt),
            (gamma, Z_pt), (X_pt, U_pt), (S_pt, R_pt), (Y_pt, T_pt),
        ]
    else:
        # High-symmetry points for hexagonal lattice
        M = 0.5 * b1
        K = (1.0 / 3.0) * b1 + (1.0 / 3.0) * b2
        A_pt = 0.5 * b3
        L_pt = M + 0.5 * b3
        H_pt = K + 0.5 * b3

        prism_vertices = {
            "\\Gamma": gamma,
            "M": M,
            "K": K,
            "A": A_pt,
            "L": L_pt,
            "H": H_pt
        }

        prism_faces = [
            [gamma, M, K],
            [A_pt, L_pt, H_pt],
            [gamma, M, L_pt, A_pt],
            [M, K, H_pt, L_pt],
            [K, gamma, A_pt, H_pt]
        ]

        prism_edges = [
            (gamma, M), (M, K), (K, gamma),
            (A_pt, L_pt), (L_pt, H_pt), (H_pt, A_pt),
            (gamma, A_pt), (M, L_pt), (K, H_pt)
        ]
        [gamma, M, L_pt, A_pt],
        [M, K, H_pt, L_pt],
        [K, gamma, A_pt, H_pt]
    ]

    prism_edges = [
        (gamma, M), (M, K), (K, gamma),
        (A_pt, L_pt), (L_pt, H_pt), (H_pt, A_pt),
        (gamma, A_pt), (M, L_pt), (K, H_pt)
    ]

    fig = plt.figure(figsize=(5.5, 4.8), dpi=300)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    ax.view_init(elev=elev, azim=azim)

    # Draw BZ Wireframe Edges (Hidden dashed, visible solid)
    for v1_idx, v2_idx in bz_edges:
        p1 = vor.vertices[v1_idx]
        p2 = vor.vertices[v2_idx]
        mid = 0.5 * (p1 + p2)
        is_rear = (mid[1] > 0.01)
        if is_rear:
            ax.plot(
                [p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                color="#666666", linestyle="--", linewidth=0.85, alpha=0.8, zorder=2
            )
        else:
            ax.plot(
                [p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                color="#111111", linestyle="-", linewidth=1.1, alpha=0.95, zorder=3
            )

    # Highlighted Prism
    if highlight_prism:
        prism_poly = Poly3DCollection(
            prism_faces,
            facecolors=color_fill,
            alpha=0.36,
            edgecolors="none",
            zorder=4
        )
        ax.add_collection3d(prism_poly)

        for pt1, pt2 in prism_edges:
            ax.plot(
                [pt1[0], pt2[0]], [pt1[1], pt2[1]], [pt1[2], pt2[2]],
                color=color_accent, linestyle="-", linewidth=2.2, zorder=6
            )

    # Reciprocal Basis Vectors with 3D Arrows
    b1_arrow = b1 * 1.30
    b2_arrow = b2 * 1.30
    b3_arrow = b3 * 1.35

    ax.quiver(0, 0, 0, b1_arrow[0], b1_arrow[1], b1_arrow[2], color="black", arrow_length_ratio=0.07, linewidth=1.3, zorder=7)
    ax.quiver(0, 0, 0, b2_arrow[0], b2_arrow[1], b2_arrow[2], color="black", arrow_length_ratio=0.07, linewidth=1.3, zorder=7)
    ax.quiver(0, 0, 0, b3_arrow[0], b3_arrow[1], b3_arrow[2], color="black", arrow_length_ratio=0.07, linewidth=1.3, zorder=7)

    ax.text(b1_arrow[0] * 1.05, b1_arrow[1] * 1.05, b1_arrow[2], r"$\mathbf{b}_1$", fontsize=11.5, fontweight="bold", color="black", zorder=8)
    ax.text(b2_arrow[0] * 1.05, b2_arrow[1] * 1.05, b2_arrow[2], r"$\mathbf{b}_2$", fontsize=11.5, fontweight="bold", color="black", zorder=8)
    ax.text(b3_arrow[0] + 0.005, b3_arrow[1], b3_arrow[2] * 1.04, r"$\mathbf{b}_3$", fontsize=11.5, fontweight="bold", color="black", zorder=8)

    # High-Symmetry Scatter Nodes
    pts_x = [p[0] for p in prism_vertices.values()]
    pts_y = [p[1] for p in prism_vertices.values()]
    pts_z = [p[2] for p in prism_vertices.values()]
    ax.scatter(pts_x, pts_y, pts_z, color=color_accent, s=34, edgecolors="white", linewidth=0.8, zorder=10)

    label_offsets = {
        "\\Gamma": (0.012, 0.015, 0.015),
        "M": (-0.035, -0.02, -0.025),
        "K": (-0.012, -0.038, -0.025),
        "A": (0.012, 0.015, 0.015),
        "L": (-0.035, -0.015, 0.015),
        "H": (-0.012, -0.035, 0.015)
    }

    for name, coords in prism_vertices.items():
        dx, dy, dz = label_offsets.get(name, (0.01, 0.01, 0.01))
        ax.text(coords[0] + dx, coords[1] + dy, coords[2] + dz, f"${name}$", fontsize=10.5, fontweight="bold", color="black", zorder=12)

    # Clean Configuration
    ax.set_axis_off()
    ax.grid(False)
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('none')

    all_x = list(bz_verts[:, 0]) + [b1_arrow[0], b2_arrow[0], b3_arrow[0]]
    all_y = list(bz_verts[:, 1]) + [b1_arrow[1], b2_arrow[1], b3_arrow[1]]
    all_z = list(bz_verts[:, 2]) + [b1_arrow[2], b2_arrow[2], b3_arrow[2]]

    span = max(max(all_x) - min(all_x), max(all_y) - min(all_y), max(all_z) - min(all_z)) * 0.48
    cx, cy, cz = 0.5 * (max(all_x) + min(all_x)), 0.5 * (max(all_y) + min(all_y)), 0.5 * (max(all_z) + min(all_z))

    ax.set_xlim(cx - span, cx + span)
    ax.set_ylim(cy - span, cy + span)
    ax.set_zlim(cz - span, cz + span)

    if panel_label:
        plt.figtext(0.50, 0.03, panel_label, ha="center", va="center", fontsize=14, fontweight="normal")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    plt.close()
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Publication-Grade 3D Brillouin Zone Visualizer")
    parser.add_argument("poscar", nargs="?", help="Path to POSCAR/CONTCAR file")
    parser.add_argument("-a", type=float, default=12.10, help="Hexagonal lattice constant a (A)")
    parser.add_argument("-c", type=float, default=17.69, help="Hexagonal lattice constant c (A)")
    parser.add_argument("-o", "--output", default="brillouin_zone.png", help="Output image file")
    parser.add_argument("--elev", type=float, default=22, help="Elevation angle")
    parser.add_argument("--azim", type=float, default=-78, help="Azimuth angle")
    parser.add_argument("--label", default="(e)", help="Panel label")
    args = parser.parse_args()

    if args.poscar and os.path.exists(args.poscar):
        lattice = parse_poscar_lattice(args.poscar)
    else:
        # Default hexagonal lattice
        a, c = args.a, args.c
        a1 = np.array([a * np.sqrt(3) / 2.0, -a / 2.0, 0.0])
        a2 = np.array([0.0, a, 0.0])
        a3 = np.array([0.0, 0.0, c])
        lattice = np.array([a1, a2, a3])

    out = render_brillouin_zone(
        lattice=lattice,
        output_path=args.output,
        elev=args.elev,
        azim=args.azim,
        panel_label=args.label
    )
    print(f"Brillouin zone figure generated: {out}")


if __name__ == "__main__":
    main()
