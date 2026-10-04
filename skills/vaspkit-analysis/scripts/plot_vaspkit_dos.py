#!/usr/bin/env python3
"""
================================================================================
Publication-Grade Density of States (DOS/PDOS) Plotter for VASPKIT
================================================================================
Reads VASPKIT TDOS.dat and PDOS_*.dat outputs:
1. Native STIX math and Times New Roman typography.
2. Spin-polarized mirrored DOS (Spin-Up positive, Spin-Down negative).
3. Element and orbital projection color concordant with VESTA palettes.
4. Shaded curve areas with calibrated transparency.
5. Dual export: 300+ DPI PNG and vector PDF.
================================================================================
"""

import argparse
import glob
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np


# Standard VESTA Element Colors for concordant DOS coloring
VESTA_COLORS: Dict[str, str] = {
    "H": "#FFFFFF", "C": "#909090", "N": "#3050F8", "O": "#FF0D0D",
    "F": "#90E050", "Cl": "#1FF01F", "Br": "#A62929", "S": "#FFFF30",
    "P": "#FF8000", "Fe": "#E06633", "Co": "#F090A0", "Ni": "#50D050",
    "Cu": "#C88033", "Pt": "#D0D0E0", "Au": "#FFD123", "Mo": "#54B5B5",
    "Cr": "#8A99C7", "Ti": "#BFC2C7", "V": "#A6A6AB",
}


def set_publication_style():
    """Configures Times New Roman and STIX math typography."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.edgecolor": "#222222",
        "axes.linewidth": 1.2,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 5.0,
        "ytick.major.size": 5.0,
        "xtick.major.width": 1.2,
        "ytick.major.width": 1.2,
        "figure.autolayout": False,
        "savefig.bbox": "tight",
        "savefig.dpi": 300,
    })


def parse_dos_data(dos_file: Path) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """
    Parses VASPKIT TDOS.dat or PDOS.dat.
    Returns: energy, dos_up, dos_dw (if spin polarized).
    """
    data = []
    header_line = ""
    with open(dos_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        l = line.strip()
        if not l:
            continue
        if l.startswith("#"):
            if not header_line:
                header_line = l.upper()
            continue
        parts = l.split()
        try:
            row = [float(x) for x in parts]
            data.append(row)
        except ValueError:
            pass

    arr = np.array(data)
    if arr.ndim < 2 or arr.shape[0] == 0:
        raise ValueError(f"Empty or invalid DOS dataset in {dos_file}")

    energies = arr[:, 0]
    dos_up = arr[:, 1]
    dos_dw = None

    if arr.shape[1] >= 3:
        if "DOWN" in header_line or "DW" in header_line:
            dos_dw = arr[:, 2]
        else:
            # Check if column 2 is monotonic increasing (integrated DOS)
            col2 = arr[:, 2]
            diffs = np.diff(col2)
            if np.all(diffs >= -1e-4) and np.max(col2) > np.max(dos_up):
                dos_dw = None
            else:
                dos_dw = col2

    return energies, dos_up, dos_dw


def plot_dos(
    calc_dir: Union[str, Path] = ".",
    output_prefix: str = "density_of_states",
    energy_range: Tuple[float, float] = (-5.0, 5.0),
    include_pdos: bool = True,
    title: Optional[str] = None,
    figsize: Tuple[float, float] = (5.5, 5.0),
) -> Tuple[Path, Path]:
    """
    Plots publication-ready TDOS and PDOS from VASPKIT outputs.
    """
    c_dir = Path(calc_dir).resolve()
    tdos_path = c_dir / "TDOS.dat"
    if not tdos_path.exists():
        raise FileNotFoundError(f"TDOS.dat not found in {c_dir}")

    energies, tdos_up, tdos_dw = parse_dos_data(tdos_path)

    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    is_spin = tdos_dw is not None

    # Plot Total DOS
    ax.plot(energies, tdos_up, color="#222222", linewidth=1.3, label="Total DOS")
    ax.fill_between(energies, 0, tdos_up, color="#888888", alpha=0.25)

    if is_spin:
        ax.plot(energies, -tdos_dw, color="#222222", linewidth=1.3)
        ax.fill_between(energies, 0, -tdos_dw, color="#888888", alpha=0.25)

    # Search for PDOS files (e.g. PDOS_C.dat, PDOS_Fe.dat, etc.)
    if include_pdos:
        pdos_files = sorted(list(c_dir.glob("PDOS_*.dat")))
        for pfile in pdos_files:
            # Extract element symbol from name (e.g. PDOS_C.dat -> C)
            elem = pfile.stem.replace("PDOS_", "").split("_")[0]
            if elem in ["USER", "TOTAL"]:
                continue
            try:
                p_e, p_up, p_dw = parse_dos_data(pfile)
                color = VESTA_COLORS.get(elem, None)
                line, = ax.plot(p_e, p_up, linewidth=1.2, label=f"{elem} projected", color=color)
                if is_spin and p_dw is not None:
                    ax.plot(p_e, -p_dw, linewidth=1.2, color=line.get_color(), linestyle="--")
            except Exception:
                pass

    # Fermi level vertical dashed line
    ax.axvline(0.0, color="#d62728", linestyle="--", linewidth=1.0, alpha=0.85, label=r"$E_{\mathrm{F}}$")

    # Horizontal zero line
    ax.axhline(0.0, color="#555555", linewidth=0.8, alpha=0.7)

    ax.set_xlim(energy_range[0], energy_range[1])
    ax.set_xlabel(r"$E - E_{\mathrm{F}}\ \mathrm{(eV)}$", fontsize=13)
    ax.set_ylabel(r"$\mathrm{Density\ of\ States}\ (\mathrm{states/eV})$", fontsize=13)
    if title:
        ax.set_title(title, fontsize=13, pad=8)

    ax.legend(loc="upper right", frameon=True, fontsize=10)

    out_png = c_dir / f"{output_prefix}.png"
    out_pdf = c_dir / f"{output_prefix}.pdf"

    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()

    print(f"[VASPKIT DOS] Saved: {out_png}")
    print(f"[VASPKIT DOS] Saved: {out_pdf}")
    return out_png, out_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Plot publication-quality DOS / PDOS from VASPKIT outputs."
    )
    parser.add_argument("calc_dir", nargs="?", default=".", help="Directory containing TDOS.dat and PDOS_*.dat")
    parser.add_argument("--output", "-o", default="density_of_states", help="Output file prefix (default: density_of_states)")
    parser.add_argument(
        "--erange",
        "-e",
        nargs=2,
        type=float,
        default=[-5.0, 5.0],
        metavar=("EMIN", "EMAX"),
        help="Energy range in eV relative to Fermi level (default: -5.0 5.0)",
    )
    parser.add_argument("--no-pdos", action="store_true", help="Exclude projected DOS curves")
    parser.add_argument("--title", "-t", help="Figure title")
    args = parser.parse_args()

    plot_dos(
        calc_dir=args.calc_dir,
        output_prefix=args.output,
        energy_range=tuple(args.erange),
        include_pdos=not args.no_pdos,
        title=args.title,
    )


if __name__ == "__main__":
    main()
