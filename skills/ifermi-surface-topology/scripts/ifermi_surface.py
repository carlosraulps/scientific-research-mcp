#!/home/cr/.local/share/mamba/envs/vasp-env/bin/python
"""
================================================================================
IFermi Surface & Topology Analysis Suite (ifermi-surface)
================================================================================
Generates, visualizes, and quantifies 3D Fermi surfaces and 2D Fermi slices
from DFT calculations (VASP vasprun.xml):
- 3D Fermi surface generation in Wigner-Seitz Brillouin zone
- Fermi velocity vector field projection (v_F = (1/hbar) grad_k E(k))
- 2D Fermi contour slices across high-symmetry planes
- Fermi surface area, average velocity, and DOS(E_F) quantification
================================================================================
"""

import os
import sys
import argparse
import subprocess

try:
    from ifermi.surface import FermiSurface
    from ifermi.interpolator import Interpolator
    from ifermi.plotter import FermiSlicePlotter, FermiSurfacePlotter
    from pymatgen.io.vasp.outputs import Vasprun
    HAS_IFERMI_PY = True
except ImportError:
    HAS_IFERMI_PY = False


def run_ifermi_info(vasprun_file="vasprun.xml", mu=0.0, prop="velocity"):
    """Calculates quantitative Fermi surface properties (area, v_F, DOS)."""
    cmd = [
        "ifermi", "info",
        "-f", vasprun_file,
        "-m", str(mu),
        "--property", prop,
        "--wigner"
    ]
    print(f"[*] Extracting Fermi surface metrics from '{vasprun_file}' (mu={mu})...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Error running ifermi info:\n{res.stderr}", file=sys.stderr)
        return
    print(res.stdout)


def run_ifermi_plot(vasprun_file="vasprun.xml", output="fermi_surface.png",
                    mu=0.0, prop="velocity", plot_type="matplotlib",
                    azimuth=45.0, elevation=35.0, slice_plane=None,
                    vector_arrows=False):
    """Renders 3D Fermi surface or 2D slice."""
    cmd = [
        "ifermi", "plot",
        "-f", vasprun_file,
        "-o", output,
        "-m", str(mu),
        "-t", plot_type,
        "-a", str(azimuth),
        "-e", str(elevation),
        "--wigner"
    ]

    if prop:
        cmd.extend(["--property", prop])

    if vector_arrows:
        cmd.append("--vector-property")

    if slice_plane:
        # e.g. "0 0 1 0" for kz=0 slice
        parts = slice_plane.split()
        cmd.extend(["--slice"] + parts)

    print(f"[*] Rendering Fermi surface with ifermi -> '{output}'...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Plotting error:\n{res.stderr}", file=sys.stderr)
        return
    print(f"[✓] Rendered Fermi surface: {output}")


def main():
    parser = argparse.ArgumentParser(description="IFermi Surface & Topology Analysis Suite")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Info
    p_info = subparsers.add_parser("info", help="Calculate Fermi surface area and velocity statistics")
    p_info.add_argument("-f", "--file", default="vasprun.xml", help="Input vasprun.xml file")
    p_info.add_argument("-m", "--mu", type=float, default=0.0, help="Chemical potential offset from E_F (eV)")
    p_info.add_argument("-p", "--property", default="velocity", choices=["velocity", "spin"], help="Projection property")

    # Plot
    p_plot = subparsers.add_parser("plot", help="Render 3D Fermi surface or 2D slice")
    p_plot.add_argument("-f", "--file", default="vasprun.xml", help="Input vasprun.xml file")
    p_plot.add_argument("-o", "--output", default="fermi_surface.png", help="Output figure filename")
    p_plot.add_argument("-m", "--mu", type=float, default=0.0, help="Energy offset from E_F (eV)")
    p_plot.add_argument("-p", "--property", default="velocity", choices=["velocity", "spin", "none"], help="Projection property")
    p_plot.add_argument("-t", "--type", default="matplotlib", choices=["matplotlib", "plotly", "mayavi"], help="Backend type")
    p_plot.add_argument("-a", "--azim", type=float, default=45.0, help="Azimuth viewpoint angle")
    p_plot.add_argument("-e", "--elev", type=float, default=35.0, help="Elevation viewpoint angle")
    p_plot.add_argument("--slice", help="Slice through BZ (format: 'j k l dist', e.g. '0 0 1 0' for kz=0)")
    p_plot.add_argument("--vectors", action="store_true", help="Display Fermi velocity vectors as 3D arrows")

    args = parser.parse_args()

    if args.command == "info":
        run_ifermi_info(vasprun_file=args.file, mu=args.mu, prop=args.property)
    elif args.command == "plot":
        prop = None if args.property == "none" else args.property
        run_ifermi_plot(vasprun_file=args.file, output=args.output, mu=args.mu,
                        prop=prop, plot_type=args.type, azimuth=args.azim,
                        elevation=args.elev, slice_plane=args.slice,
                        vector_arrows=args.vectors)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
