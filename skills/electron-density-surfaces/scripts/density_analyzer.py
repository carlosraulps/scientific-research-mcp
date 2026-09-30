#!/usr/bin/env python3
"""
Electron Density, Molecular Surfaces & 2D Topological Analysis Toolkit.
Supports 3D marching cubes isosurface extraction, 2D topological slices,
Laplacian/gradient fields, planar potential averaging, and visualizer export.
"""

import argparse
import math
import os
import sys
from pathlib import Path
import numpy as np


def parse_chgcar(file_path):
    """Parse VASP CHGCAR / LOCPOT / ELFCAR volumetric file."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    comment = lines[0].strip()
    scale = float(lines[1].strip())
    lattice = np.array([[float(x) for x in lines[i].split()] for i in range(2, 5)]) * scale

    line5 = lines[5].split()
    if line5[0].isdigit():
        species = ["X"] * len(line5)
        counts = [int(x) for x in line5]
        idx = 6
    else:
        species = line5
        counts = [int(x) for x in lines[6].split()]
        idx = 7

    if lines[idx].strip().lower().startswith("s"):
        idx += 1
    coord_type = lines[idx].strip().lower()
    idx += 1

    total_atoms = sum(counts)
    atom_types = []
    coords = []
    for sp, cnt in zip(species, counts):
        for _ in range(cnt):
            atom_types.append(sp)
            coords.append([float(x) for x in lines[idx].split()[:3]])
            idx += 1

    coords = np.array(coords)
    if coord_type.startswith("d"):
        cart_coords = coords @ lattice
    else:
        cart_coords = coords * scale

    # Find blank line before grid dimensions
    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    grid_dims = [int(x) for x in lines[idx].split()]
    idx += 1
    nx, ny, nz = grid_dims
    total_voxels = nx * ny * nz

    data = []
    while idx < len(lines) and len(data) < total_voxels:
        line = lines[idx].strip()
        if line:
            data.extend([float(x) for x in line.split()])
        idx += 1

    volume_grid = np.array(data[:total_voxels]).reshape((nz, ny, nx)).transpose(2, 1, 0)
    # Unit cell volume
    vol = np.abs(np.linalg.det(lattice))

    return {
        "lattice": lattice,
        "species": atom_types,
        "positions": cart_coords,
        "fractional_positions": coords,
        "grid": grid_dims,
        "data": volume_grid,
        "volume": vol,
    }


def parse_cube(file_path):
    """Parse Gaussian Cube file format."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Lines 1-2: comments
    # Line 3: natoms, origin_x, origin_y, origin_z
    l3 = lines[2].split()
    natoms = int(l3[0])
    origin = np.array([float(x) for x in l3[1:4]])

    # Lines 4-6: grid steps
    l4 = lines[3].split()
    nx = int(l4[0])
    v_a = np.array([float(x) for x in l4[1:4]])

    l5 = lines[4].split()
    ny = int(l5[0])
    v_b = np.array([float(x) for x in l5[1:4]])

    l6 = lines[5].split()
    nz = int(l6[0])
    v_c = np.array([float(x) for x in l6[1:4]])

    lattice = np.array([nx * v_a, ny * v_b, nz * v_c])

    atom_types = []
    positions = []
    idx = 6
    for _ in range(abs(natoms)):
        parts = lines[idx].split()
        atomic_num = int(parts[0])
        pos = [float(x) for x in parts[2:5]]
        atom_types.append(str(atomic_num))
        positions.append(pos)
        idx += 1

    positions = np.array(positions)
    # Convert Bohr to Angstrom if necessary (standard cube is in Bohr: 0.529177)
    # Note: Cube files are commonly in atomic units
    total_voxels = abs(nx * ny * nz)
    data = []
    while idx < len(lines) and len(data) < total_voxels:
        line = lines[idx].strip()
        if line:
            data.extend([float(x) for x in line.split()])
        idx += 1

    volume_grid = np.array(data[:total_voxels]).reshape((abs(nx), abs(ny), abs(nz)))
    vol = np.abs(np.linalg.det(lattice))

    return {
        "lattice": lattice,
        "species": atom_types,
        "positions": positions,
        "grid": [abs(nx), abs(ny), abs(nz)],
        "data": volume_grid,
        "volume": vol,
    }


def extract_3d_isosurface(density_data, isovalue, output_obj=None, output_html=None):
    """
    Extract 3D polygonal isosurface using skimage.measure.marching_cubes
    and export to OBJ and interactive Plotly HTML.
    """
    import skimage.measure

    grid = density_data["data"]
    lattice = density_data["lattice"]
    nx, ny, nz = density_data["grid"]

    v_min, v_max = float(np.min(grid)), float(np.max(grid))
    if isovalue <= v_min or isovalue >= v_max:
        print(f"Warning: Requested isovalue {isovalue} is outside data range [{v_min:.4f}, {v_max:.4f}]. Adjusting to midpoint.", file=sys.stderr)
        isovalue = v_min + 0.3 * (v_max - v_min)

    # Voxel transform matrix
    spacing = (1.0 / nx, 1.0 / ny, 1.0 / nz)

    # Marching cubes
    verts, faces, normals, values = skimage.measure.marching_cubes(
        grid, level=isovalue, spacing=spacing
    )

    # Convert fractional vertex coordinates to Cartesian coordinates (Angstroms)
    cart_verts = verts @ lattice

    # Save to Wavefront OBJ format
    if output_obj:
        obj_path = Path(output_obj).resolve()
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        with open(obj_path, "w") as f:
            f.write(f"# 3D Isosurface (isovalue={isovalue})\n")
            f.write(f"# Vertices: {len(cart_verts)}, Faces: {len(faces)}\n")
            for v in cart_verts:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            for n in normals:
                f.write(f"vn {n[0]:.6f} {n[1]:.6f} {n[2]:.6f}\n")
            for face in faces:
                # 1-indexed for OBJ
                f.write(f"f {face[0]+1}//{face[0]+1} {face[1]+1}//{face[1]+1} {face[2]+1}//{face[2]+1}\n")
        print(f"Exported 3D Isosurface OBJ: {obj_path} ({len(cart_verts)} vertices, {len(faces)} faces)")

    # Save interactive 3D HTML using Plotly
    if output_html:
        try:
            import plotly.graph_objects as go

            fig = go.Figure()

            # Add Isosurface Mesh
            fig.add_trace(go.Mesh3d(
                x=cart_verts[:, 0],
                y=cart_verts[:, 1],
                z=cart_verts[:, 2],
                i=faces[:, 0],
                j=faces[:, 1],
                k=faces[:, 2],
                opacity=0.6,
                color="deepskyblue",
                name=f"Isosurface ({isovalue})",
            ))

            # Add Atoms as 3D Scatter
            positions = density_data["positions"]
            species = density_data["species"]
            fig.add_trace(go.Scatter3d(
                x=positions[:, 0],
                y=positions[:, 1],
                z=positions[:, 2],
                mode="markers+text",
                marker=dict(size=8, color="firebrick"),
                text=species,
                name="Atoms",
            ))

            # Unit cell bounding lines
            corners = np.array([
                [0,0,0], [1,0,0], [1,1,0], [0,1,0],
                [0,0,1], [1,0,1], [1,1,1], [0,1,1]
            ]) @ lattice

            edges = [
                (0,1), (1,2), (2,3), (3,0),
                (4,5), (5,6), (6,7), (7,4),
                (0,4), (1,5), (2,6), (3,7)
            ]
            for p1, p2 in edges:
                fig.add_trace(go.Scatter3d(
                    x=[corners[p1, 0], corners[p2, 0]],
                    y=[corners[p1, 1], corners[p2, 1]],
                    z=[corners[p1, 2], corners[p2, 2]],
                    mode="lines",
                    line=dict(color="black", width=2),
                    showlegend=False,
                ))

            fig.update_layout(
                title=f"3D Electron Density Isosurface (Isovalue = {isovalue})",
                scene=dict(
                    xaxis_title="X (Å)",
                    yaxis_title="Y (Å)",
                    zaxis_title="Z (Å)",
                    aspectmode="data",
                ),
                margin=dict(l=0, r=0, b=0, t=40),
            )

            html_path = Path(output_html).resolve()
            html_path.parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(str(html_path))
            print(f"Exported interactive 3D HTML: {html_path}")
        except Exception as e:
            print(f"Warning: Could not export Plotly HTML: {e}", file=sys.stderr)

    return cart_verts, faces


def generate_2d_slice(
    density_data,
    plane: str = "xy",
    slice_pos: float = 0.5,
    output_image: str = "density_slice.png",
    show_gradient: bool = True,
    show_laplacian: bool = False,
):
    """
    Generate 2D topological mapping across a crystallographic slice.
    Includes filled contours, gradient vector field (charge flow attractors),
    and 2D Laplacian of electron density (covalent vs ionic bonding).
    """
    import matplotlib.pyplot as plt

    # Apply Times New Roman publication styling
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.edgecolor": "#222222",
        "axes.linewidth": 1.2,
    })

    grid = density_data["data"]
    lattice = density_data["lattice"]
    nx, ny, nz = density_data["grid"]

    if plane.lower() == "xy":
        # Slice at z = slice_pos
        k = int(round(slice_pos * (nz - 1)))
        slice_2d = grid[:, :, k].T
        x_dim = np.linalg.norm(lattice[0])
        y_dim = np.linalg.norm(lattice[1])
        x_label, y_label = r"$x\ \mathrm{(Å)}$", r"$y\ \mathrm{(Å)}$"
        plane_title = f"(001) Plane at $z = {slice_pos:.2f}$"
    elif plane.lower() == "xz":
        # Slice at y = slice_pos
        j = int(round(slice_pos * (ny - 1)))
        slice_2d = grid[:, j, :].T
        x_dim = np.linalg.norm(lattice[0])
        y_dim = np.linalg.norm(lattice[2])
        x_label, y_label = r"$x\ \mathrm{(Å)}$", r"$z\ \mathrm{(Å)}$"
        plane_title = f"(010) Plane at $y = {slice_pos:.2f}$"
    else:  # yz
        # Slice at x = slice_pos
        i = int(round(slice_pos * (nx - 1)))
        slice_2d = grid[i, :, :].T
        x_dim = np.linalg.norm(lattice[1])
        y_dim = np.linalg.norm(lattice[2])
        x_label, y_label = r"$y\ \mathrm{(Å)}$", r"$z\ \mathrm{(Å)}$"
        plane_title = f"(100) Plane at $x = {slice_pos:.2f}$"

    X = np.linspace(0, x_dim, slice_2d.shape[1])
    Y = np.linspace(0, y_dim, slice_2d.shape[0])
    XX, YY = np.meshgrid(X, Y)

    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

    if show_laplacian:
        # Calculate numerical Laplacian: d2/dx2 + d2/dy2
        laplacian_2d = np.gradient(np.gradient(slice_2d, axis=0), axis=0) + \
                       np.gradient(np.gradient(slice_2d, axis=1), axis=1)
        # Symmetrical colormap around zero
        lim = np.percentile(np.abs(laplacian_2d), 95)
        cp = ax.contourf(XX, YY, laplacian_2d, levels=40, cmap="RdBu_r", vmin=-lim, vmax=lim)
        cbar = fig.colorbar(cp, ax=ax)
        cbar.set_label(r"$\nabla^2 \rho(\mathbf{r})\ \mathrm{(e/Å^5)}$ (Blue: Concentration, Red: Depletion)")
    else:
        # Standard density contour
        cp = ax.contourf(XX, YY, slice_2d, levels=40, cmap="viridis")
        ax.contour(XX, YY, slice_2d, levels=10, colors="black", linewidths=0.5, alpha=0.5)
        cbar = fig.colorbar(cp, ax=ax)
        cbar.set_label(r"Electron Density $\rho(\mathbf{r})\ \mathrm{(e/Å^3)}$")

    # Add gradient vectors (QTAIM charge concentration attractors)
    if show_gradient:
        gy, gx = np.gradient(slice_2d)
        step = max(slice_2d.shape[0] // 20, 1)
        ax.quiver(
            XX[::step, ::step],
            YY[::step, ::step],
            gx[::step, ::step],
            gy[::step, ::step],
            color="white",
            alpha=0.6,
            scale=None,
        )

    # Project atoms near the slice plane
    positions = density_data["positions"]
    species = density_data["species"]
    for sp, pos in zip(species, positions):
        # Check proximity to slice plane
        if plane.lower() == "xy":
            dist = abs(pos[2] - slice_pos * np.linalg.norm(lattice[2]))
            p_x, p_y = pos[0], pos[1]
        elif plane.lower() == "xz":
            dist = abs(pos[1] - slice_pos * np.linalg.norm(lattice[1]))
            p_x, p_y = pos[0], pos[2]
        else:
            dist = abs(pos[0] - slice_pos * np.linalg.norm(lattice[0]))
            p_x, p_y = pos[1], pos[2]

        if dist < 1.2:  # within 1.2 Å of the plane
            ax.scatter(p_x, p_y, color="crimson", s=90, edgecolors="white", linewidth=1.2, zorder=5)
            ax.text(p_x + 0.1, p_y + 0.1, sp, color="white", fontsize=11, fontweight="bold", zorder=6)

    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    ax.set_title(f"Topological Electron Density Map: {plane_title}", fontsize=14, pad=10)
    ax.set_aspect("equal")

    out_path = Path(output_image).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(str(out_path), dpi=300)
    plt.close()
    print(f"Saved 2D Topological Slice: {out_path}")
    return str(out_path)


def compute_planar_potential(density_data, output_image: str = "planar_potential.png", fermi_energy: float = None):
    """
    Compute planar-averaged electrostatic potential along z-axis.
    Used for vacuum level identification, dipole corrections, and work function calculation.
    """
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.edgecolor": "#222222",
        "axes.linewidth": 1.2,
    })

    grid = density_data["data"]
    lattice = density_data["lattice"]
    nx, ny, nz = density_data["grid"]

    # Average over x and y dimensions
    v_planar = np.mean(grid, axis=(0, 1))
    z_len = np.linalg.norm(lattice[2])
    z_coords = np.linspace(0, z_len, nz)

    # Identify vacuum level (maximum in asymptotic region)
    v_vac = np.max(v_planar)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(z_coords, v_planar, color="#1f77b4", linewidth=2.0, label=r"Planar Average $\overline{V}(z)$")
    ax.axhline(v_vac, color="red", linestyle="--", linewidth=1.5, label=f"Vacuum Level $V_{{\\mathrm{{vac}}}} = {v_vac:.2f}\\ \\mathrm{{eV}}$")

    if fermi_energy is not None:
        ax.axhline(fermi_energy, color="green", linestyle=":", linewidth=1.5, label=f"Fermi Level $E_{{\\mathrm{{F}}}} = {fermi_energy:.2f}\\ \\mathrm{{eV}}$")
        work_func = v_vac - fermi_energy
        ax.annotate(
            rf"$\Phi = V_{{\mathrm{{vac}}}} - E_{{\mathrm{{F}}}} = {work_func:.2f}\ \mathrm{{eV}}$",
            xy=(z_len * 0.5, (v_vac + fermi_energy) / 2),
            xytext=(z_len * 0.55, (v_vac + fermi_energy) / 2 + 0.5),
            arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=6),
            fontsize=12,
            fontweight="bold",
        )

    ax.set_xlabel(r"Position along $z$-axis (Å)", fontsize=13)
    ax.set_ylabel(r"Electrostatic Potential (eV)", fontsize=13)
    ax.set_title(r"Planar-Averaged Electrostatic Potential $\overline{V}(z)$", fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="best", frameon=True)

    out_path = Path(output_image).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(str(out_path), dpi=300)
    plt.close()
    print(f"Saved Planar Potential Plot: {out_path} (Vacuum Level = {v_vac:.3f} eV)")
    return str(out_path), v_vac


def export_to_xsf(density_data, output_xsf: str):
    """
    Export volumetric data and atomic coordinates to XCrySDen / VESTA compatible XSF format.
    Includes 3D DATAGRID block for direct isosurface and 2D contour rendering.
    """
    out_path = Path(output_xsf).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lat = density_data["lattice"]
    species = density_data["species"]
    pos = density_data["positions"]
    grid = density_data["data"]
    nx, ny, nz = density_data["grid"]

    with open(out_path, "w") as f:
        f.write("CRYSTAL\nPRIMVEC\n")
        for row in lat:
            f.write(f"  {row[0]:12.6f} {row[1]:12.6f} {row[2]:12.6f}\n")
        f.write(f"PRIMCOORD\n{len(species)} 1\n")
        for sp, p in zip(species, pos):
            f.write(f"  {sp}  {p[0]:12.6f} {p[1]:12.6f} {p[2]:12.6f}\n")
        f.write("BEGIN_BLOCK_DATAGRID_3D\n3D_charge_density\nBEGIN_DATAGRID_3D_density\n")
        f.write(f"{nx} {ny} {nz}\n0.0 0.0 0.0\n")
        for row in lat:
            f.write(f"  {row[0]:12.6f} {row[1]:12.6f} {row[2]:12.6f}\n")

        flat = grid.transpose(2, 1, 0).flatten()
        count = 0
        for v in flat:
            f.write(f"{v:12.6f} ")
            count += 1
            if count % 6 == 0:
                f.write("\n")
        if count % 6 != 0:
            f.write("\n")
        f.write("END_DATAGRID_3D\nEND_BLOCK_DATAGRID_3D\n")

    print(f"Exported XCrySDen/VESTA 3D Datagrid XSF: {out_path}")
    return str(out_path)


def main():
    parser = argparse.ArgumentParser(
        description="Electron Density, Molecular Surfaces, and 2D Topological Analysis Toolkit."
    )
    parser.add_argument("input", help="Path to volumetric file (CHGCAR, LOCPOT, ELFCAR, or .cube)")
    parser.add_argument("--isovalue", "-i", type=float, default=0.05, help="Isovalue for 3D isosurface (default: 0.05)")
    parser.add_argument("--obj", help="Path to export 3D surface mesh in Wavefront OBJ format")
    parser.add_argument("--html", help="Path to export interactive 3D surface in HTML format")
    parser.add_argument("--slice-plane", choices=["xy", "xz", "yz"], default="xy", help="2D slice plane (default: xy)")
    parser.add_argument("--slice-pos", type=float, default=0.5, help="Fractional position along normal axis (0.0 - 1.0, default: 0.5)")
    parser.add_argument("--slice-out", help="Path to save 2D slice contour plot PNG")
    parser.add_argument("--laplacian", action="store_true", help="Plot 2D Laplacian of density (covalent vs ionic topology)")
    parser.add_argument("--no-gradient", action="store_true", help="Disable gradient flow arrows on 2D slice")
    parser.add_argument("--planar-potential", help="Path to save 1D planar-averaged potential plot (from LOCPOT)")
    parser.add_argument("--fermi-energy", type=float, help="Fermi level in eV for work function calculation")
    parser.add_argument("--export-xsf", help="Export volumetric data to XCrySDen / VESTA compatible XSF with 3D datagrid")

    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: File does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing volumetric file: {input_path.name}...")
    if input_path.suffix.lower() == ".cube":
        density_data = parse_cube(input_path)
    else:
        density_data = parse_chgcar(input_path)

    print(f"Grid: {density_data['grid']}, Unit Cell Volume: {density_data['volume']:.2f} Å³")

    # Export XSF
    if args.export_xsf:
        export_to_xsf(density_data, args.export_xsf)

    # 3D Isosurface
    if args.obj or args.html or (not args.slice_out and not args.planar_potential and not args.export_xsf):
        obj_file = args.obj or f"{input_path.stem}_iso.obj"
        html_file = args.html or f"{input_path.stem}_iso.html"
        extract_3d_isosurface(density_data, isovalue=args.isovalue, output_obj=obj_file, output_html=html_file)

    # 2D Slice
    if args.slice_out:
        generate_2d_slice(
            density_data,
            plane=args.slice_plane,
            slice_pos=args.slice_pos,
            output_image=args.slice_out,
            show_gradient=not args.no_gradient,
            show_laplacian=args.laplacian,
        )

    # Planar Potential
    if args.planar_potential:
        compute_planar_potential(
            density_data,
            output_image=args.planar_potential,
            fermi_energy=args.fermi_energy,
        )


if __name__ == "__main__":
    main()
