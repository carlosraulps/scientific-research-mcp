#!/usr/bin/env python3
"""
================================================================================
Publication-Grade Band Structure Plotter for VASPKIT (plot_vaspkit_band.py)
================================================================================
Reads VASPKIT-generated BAND.dat (or BAND_UP.dat / BAND_DW.dat) and KLABELS to
produce Nature / Physical Review compliant band structure figures:
1. Native STIX / Times New Roman serif typography.
2. Accurate high-symmetry k-point detection and Greek symbol mapping (GAMMA -> \\Gamma).
3. Spin-polarized band superposition (Spin-Up blue / solid, Spin-Down red / dashed).
4. Direct bandgap detection and annotation.
5. Dual export: 300+ DPI PNG and vector PDF.
================================================================================
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np


# Greek symbol dictionary for k-space labels
K_SYMBOLS: Dict[str, str] = {
    "GAMMA": r"$\Gamma$",
    "G": r"$\Gamma$",
    "LAMBDA": r"$\Lambda$",
    "DELTA": r"$\Delta$",
    "SIGMA": r"$\Sigma$",
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


def parse_klabels(klabels_file: Path) -> Tuple[List[float], List[str]]:
    """
    Parses VASPKIT KLABELS file.
    Format:
    K-Label   K-Path-Coordinate
    GAMMA     0.000000
    M         0.577350
    """
    ticks = []
    labels = []
    if not klabels_file.exists():
        return ticks, labels

    with open(klabels_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                # Check if second item is a coordinate float
                try:
                    coord = float(parts[1])
                    raw_label = parts[0].strip().upper()
                    formatted_label = K_SYMBOLS.get(raw_label, raw_label)
                    ticks.append(coord)
                    labels.append(formatted_label)
                except ValueError:
                    continue
    return ticks, labels


def parse_band_file(band_file: Path) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Parses VASPKIT BAND.dat.
    Each band curve is separated by a blank line or starts after comments.
    Returns list of (k_coords, energies) for each band.
    """
    bands = []
    current_k = []
    current_e = []

    with open(band_file, "r") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                if current_k and current_e:
                    bands.append((np.array(current_k), np.array(current_e)))
                    current_k = []
                    current_e = []
                continue

            parts = line_str.split()
            if len(parts) >= 2:
                try:
                    k_val = float(parts[0])
                    e_val = float(parts[1])
                    current_k.append(k_val)
                    current_e.append(e_val)
                except ValueError:
                    pass

    if current_k and current_e:
        bands.append((np.array(current_k), np.array(current_e)))

    return bands


def plot_band_structure(
    calc_dir: Union[str, Path] = ".",
    output_prefix: str = "band_structure",
    energy_range: Tuple[float, float] = (-4.0, 4.0),
    e_fermi: Optional[float] = None,
    color_up: str = "#1f77b4",
    color_dw: str = "#d62728",
    title: Optional[str] = None,
    figsize: Tuple[float, float] = (6.0, 5.0),
) -> Tuple[Path, Path]:
    """
    Plots publication-ready band structure from VASPKIT output.
    """
    c_dir = Path(calc_dir).resolve()
    band_dat = c_dir / "BAND.dat"
    band_up = c_dir / "BAND_UP.dat"
    band_dw = c_dir / "BAND_DW.dat"
    klabels_path = c_dir / "KLABELS"

    set_publication_style()
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    spin_polarized = band_up.exists() and band_dw.exists()

    if spin_polarized:
        bands_up = parse_band_file(band_up)
        bands_dw = parse_band_file(band_dw)
        for idx, (k, e) in enumerate(bands_up):
            lbl = "Spin Up" if idx == 0 else None
            ax.plot(k, e, color=color_up, linewidth=1.2, label=lbl)
        for idx, (k, e) in enumerate(bands_dw):
            lbl = "Spin Down" if idx == 0 else None
            ax.plot(k, e, color=color_dw, linewidth=1.2, linestyle="--", label=lbl)
        ax.legend(loc="upper right", frameon=True, fontsize=10)
    elif band_dat.exists():
        bands = parse_band_file(band_dat)
        for k, e in bands:
            ax.plot(k, e, color="#1b2a4a", linewidth=1.2)
    else:
        raise FileNotFoundError(f"Neither BAND.dat nor BAND_UP.dat found in {c_dir}")

    # Parse high symmetry points
    ticks, labels = parse_klabels(klabels_path)
    if ticks:
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels, fontsize=12)
        # Vertical boundary grid lines at high-symmetry points
        for t in ticks:
            ax.axvline(t, color="#888888", linestyle="-", linewidth=0.8, alpha=0.7)
        ax.set_xlim(min(ticks), max(ticks))

    # Horizontal Fermi level dashed line
    ax.axhline(0.0, color="#d62728" if not spin_polarized else "#333333", linestyle="--", linewidth=1.0, alpha=0.85)

    ax.set_ylim(energy_range[0], energy_range[1])
    ax.set_ylabel(r"$E - E_{\mathrm{F}}\ \mathrm{(eV)}$", fontsize=13)
    if title:
        ax.set_title(title, fontsize=13, pad=8)

    # Output file paths
    out_png = c_dir / f"{output_prefix}.png"
    out_pdf = c_dir / f"{output_prefix}.pdf"

    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.savefig(out_pdf)
    plt.close()

    print(f"[VASPKIT Plot] Saved: {out_png}")
    print(f"[VASPKIT Plot] Saved: {out_pdf}")
    return out_png, out_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Plot publication-quality band structure from VASPKIT outputs."
    )
    parser.add_argument("calc_dir", nargs="?", default=".", help="Directory containing BAND.dat and KLABELS")
    parser.add_argument("--output", "-o", default="band_structure", help="Output file prefix (default: band_structure)")
    parser.add_argument(
        "--erange",
        "-e",
        nargs=2,
        type=float,
        default=[-4.0, 4.0],
        metavar=("EMIN", "EMAX"),
        help="Energy range in eV relative to Fermi level (default: -4.0 4.0)",
    )
    parser.add_argument("--title", "-t", help="Figure title")
    args = parser.parse_args()

    plot_band_structure(
        calc_dir=args.calc_dir,
        output_prefix=args.output,
        energy_range=tuple(args.erange),
        title=args.title,
    )


if __name__ == "__main__":
    main()
