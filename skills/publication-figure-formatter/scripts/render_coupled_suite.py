#!/usr/bin/env python3
"""
================================================================================
Coupled Band Structure + PDOS Publication Suite (render_coupled_suite.py)
================================================================================
Implements the standardized coupled Band Structure + Projected DOS architecture:
1. Coupled Shared-Y Coordinate:
   - fig, (ax_band, ax_dos, ax_cbar) = plt.subplots(..., sharey=True, width_ratios=[1.6, 1.0, 0.04])
   - Uninterrupted horizontal Fermi level dashed line: ax.axhline(0.0, color="#d9534f", ls="--", lw=1.0)
     linking band extrema directly into PDOS van Hove singularities.
2. Fixed Dedicated Colorbar Axis:
   - Allocates an explicit third subplot for the colorbar, preventing dynamic width shrinkage.
3. Header Clearance & Overlap Prevention:
   - Line 1 (Mode Title): y = 0.955, fontsize = 12.0, weight="bold"
   - Line 2 (Parameters \\varepsilon, a, b, \\Delta Q): y = 0.895, fontsize = 10.5
   - Subplot top margin: top = 0.81 (leaves ~25-point clearance above subplot headers '(a)', '(b)').
4. VESTA Element Color Concordance:
   - Integrates orbital and element colors matching the 3D crystal structure representation.
5. Times New Roman / STIX Typography & Dual Vector/Raster Export.
================================================================================
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np

# Sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from style_config import get_vesta_color, save_publication_figure, set_publication_style


def render_coupled_band_dos(
    band_kpoints: np.ndarray,
    band_energies: np.ndarray,              # Shape (num_bands, num_kpoints)
    dos_energies: np.ndarray,
    pdos_dict: Dict[str, np.ndarray],       # e.g. {"C $2p_z$": array, "C $sp^2$": array}
    kpoint_labels: List[Tuple[float, str]], # [(0.0, r"$\Gamma$"), (1.2, r"$\mathrm{M}$"), ...]
    output_prefix: Union[str, Path] = "coupled_band_dos",
    title_line1: str = "PHOTH-Graphene: Electronic Band Structure & Density of States",
    title_line2: str = r"Pristine Monolayer ($\varepsilon = 0\%$, $a = 2.46\,\mathrm{\AA}$, Direct Gap = $0.00\,\mathrm{eV}$)",
    e_fermi: float = 0.0,
    energy_window: Tuple[float, float] = (-4.0, 4.0),
    band_weights: Optional[np.ndarray] = None, # For fat-band projection
    cbar_label: str = r"Orbital Weight $|c_{n\mathbf{k}}|^2$",
) -> Tuple[Path, Path]:
    """
    Renders the coupled Band Structure + PDOS multi-panel layout with strict clearance rules.
    """
    import matplotlib.pyplot as plt
    from matplotlib import gridspec

    set_publication_style()

    fig = plt.figure(figsize=(11.8, 5.2), dpi=300)
    # Explicit gridspec margins ensuring zero text collision
    has_cbar = band_weights is not None
    width_ratios = [1.6, 1.0, 0.04] if has_cbar else [1.6, 1.0]

    gs = gridspec.GridSpec(
        nrows=1,
        ncols=len(width_ratios),
        width_ratios=width_ratios,
        wspace=0.08,
        left=0.07,
        right=0.95,
        top=0.81,        # 25 pt vertical clearance to headers
        bottom=0.12,
    )

    ax_band = fig.add_subplot(gs[0, 0])
    ax_dos = fig.add_subplot(gs[0, 1], sharey=ax_band)

    # 1. Plot Band Structure
    num_bands = band_energies.shape[0]
    sc = None
    for b in range(num_bands):
        e_shifted = band_energies[b] - e_fermi
        if band_weights is not None:
            # Fat-band scatter overlay
            w = band_weights[b]
            ax_band.plot(band_kpoints, e_shifted, color="#555555", lw=0.6, zorder=1)
            sc = ax_band.scatter(band_kpoints, e_shifted, c=w, cmap="cividis", s=w*30 + 1, vmin=0.0, vmax=1.0, zorder=2)
        else:
            ax_band.plot(band_kpoints, e_shifted, color="#2c3e50", lw=1.2)

    # High-symmetry k-point vertical lines
    for k_val, k_lab in kpoint_labels:
        ax_band.axvline(k_val, color="#bbbbbb", ls=":", lw=0.8)

    ax_band.set_xticks([k[0] for k in kpoint_labels])
    ax_band.set_xticklabels([k[1] for k in kpoint_labels], fontsize=11)
    ax_band.set_xlim(band_kpoints[0], band_kpoints[-1])
    ax_band.set_ylim(energy_window)
    ax_band.set_ylabel(r"$E - E_{\mathrm{F}}\ \mathrm{(eV)}$", fontsize=12)

    # 2. Plot PDOS
    dos_e_shifted = dos_energies - e_fermi
    for label, pdos_curve in pdos_dict.items():
        # Match element colors from VESTA if possible
        elem = label.split()[0].strip("$")
        col = get_vesta_color(elem)
        if not col or col == "#444444":
            col = "#1f77b4" if "p" in label else "#e74c3c"
        ax_dos.plot(pdos_curve, dos_e_shifted, label=label, color=col, lw=1.3)
        ax_dos.fill_betweenx(dos_e_shifted, 0, pdos_curve, color=col, alpha=0.15)

    ax_dos.set_xlabel(r"$\mathrm{DOS}\ \mathrm{(states/eV\cdot unit\ cell)}$", fontsize=12)
    ax_dos.tick_params(labelleft=False) # Hide redundant y-ticks (shared with band)
    ax_dos.set_xlim(left=0.0)
    ax_dos.legend(loc="upper right", frameon=True, fontsize=9.5)

    # 3. Uninterrupted Shared Fermi Level across both panels
    for ax in [ax_band, ax_dos]:
        ax.axhline(0.0, color="#d9534f", ls="--", lw=1.0, zorder=3)

    # 4. Colorbar axis if fat-bands used
    if has_cbar and sc is not None:
        ax_cbar = fig.add_subplot(gs[0, 2])
        cbar = plt.colorbar(sc, cax=ax_cbar)
        cbar.set_label(cbar_label, fontsize=10.5)

    # 5. Subplot Headers (a) and (b)
    ax_band.text(0.02, 0.94, "(a) Band Dispersion", transform=ax_band.transAxes, fontsize=11, weight="bold")
    ax_dos.text(0.03, 0.94, "(b) Orbital PDOS", transform=ax_dos.transAxes, fontsize=11, weight="bold")

    # 6. Multi-line Suptitle with generous ~25-point clearance
    fig.suptitle(title_line1, y=0.955, fontsize=12.0, weight="bold")
    fig.text(0.5, 0.895, title_line2, ha="center", fontsize=10.5, color="#333333")

    # 7. Dual Export (PDF + PNG)
    out_prefix_p = Path(output_prefix).resolve()
    pdf_p, png_p = save_publication_figure(fig, out_prefix_p, dpi=300)
    plt.close(fig)

    print(f"🎉 Coupled Suite Complete:")
    print(f"   • Vector PDF: {pdf_p}")
    print(f"   • High-DPI PNG: {png_p}")
    return pdf_p, png_p


def generate_demo_suite():
    """Generates a synthetic demo coupled Band + PDOS figure."""
    k = np.linspace(0, 3.0, 150)
    k_labels = [(0.0, r"$\Gamma$"), (1.0, r"$\mathrm{K}$"), (2.0, r"$\mathrm{M}$"), (3.0, r"$\Gamma$")]

    # Synthetic bands
    bands = np.zeros((4, len(k)))
    bands[0] = -2.5 - 1.2 * np.cos(np.pi * k / 1.5)
    bands[1] = -0.5 - 0.8 * np.sin(np.pi * k / 1.0)
    bands[2] = 0.5 + 0.8 * np.sin(np.pi * k / 1.0)
    bands[3] = 2.5 + 1.2 * np.cos(np.pi * k / 1.5)

    e_dos = np.linspace(-4.0, 4.0, 200)
    pdos_c_pz = np.exp(-((e_dos + 0.5) ** 2) / 0.3) + np.exp(-((e_dos - 0.5) ** 2) / 0.3)
    pdos_c_sp2 = 0.5 * np.exp(-((e_dos + 2.5) ** 2) / 0.8) + 0.5 * np.exp(-((e_dos - 2.5) ** 2) / 0.8)

    pdos_data = {
        r"C $2p_z$ ($\pi$)": pdos_c_pz,
        r"C $sp^2$ ($\sigma$)": pdos_c_sp2,
    }

    render_coupled_band_dos(
        band_kpoints=k,
        band_energies=bands,
        dos_energies=e_dos,
        pdos_dict=pdos_data,
        kpoint_labels=k_labels,
        output_prefix="./coupled_band_dos_demo",
    )


if __name__ == "__main__":
    generate_demo_suite()
