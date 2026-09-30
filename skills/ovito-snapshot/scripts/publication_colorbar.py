#!/usr/bin/env python3
"""
================================================================================
Publication-Grade Colorbar Generator & Image Compositor (STIX & Times New Roman)
================================================================================
Decouples scientific typography from internal OpenGL rendering.
Generates publication-quality colorbars using Matplotlib with:
1. STIX mathematical formatting and Times New Roman typography.
2. Diverging Blue-White-Red or sequential colormaps.
3. Formatted decimal ticks (e.g., -0.30, -0.15, 0.00, +0.15, +0.30).
4. Qualitative physical callouts ("Electron Acceptor" in blue, "Electron Donor" in red).
5. Seamless side-by-side compositing onto rendered crystal snapshots.
================================================================================
"""

import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from PIL import Image


def generate_publication_colorbar(
    output_path: Union[str, Path],
    vmin: float = -0.30,
    vmax: float = 0.30,
    colormap: str = "coolwarm",
    label: str = r"$Q_{\mathrm{net}}\ (e)$",
    tick_count: int = 5,
    top_annotation: Optional[str] = "Electron Acceptor",
    bottom_annotation: Optional[str] = "Electron Donor",
    orientation: str = "vertical",
    dpi: int = 300,
    figsize: Tuple[float, float] = (1.5, 4.5),
) -> Path:
    """
    Renders a standalone publication-quality vector and raster colorbar.
    """
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 11

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Normalize colormap
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = plt.get_cmap(colormap)

    cb = fig.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap=cmap),
        cax=ax,
        orientation=orientation,
    )

    cb.set_label(label, fontsize=12, labelpad=10)

    # Clean decimal ticks
    ticks = np.linspace(vmin, vmax, tick_count)
    cb.set_ticks(ticks)
    cb.set_ticklabels([f"{t:+.2f}" if abs(t) > 1e-4 else "0.00" for t in ticks])
    cb.ax.tick_params(labelsize=10, width=1.0, length=4)

    # Qualitative physical annotations
    if orientation == "vertical":
        if top_annotation:
            ax.text(
                0.5, 1.05, top_annotation,
                transform=ax.transAxes,
                ha="center", va="bottom",
                fontsize=9.5, fontweight="bold",
                color="#1b4f72"  # Deep blue
            )
        if bottom_annotation:
            ax.text(
                0.5, -0.05, bottom_annotation,
                transform=ax.transAxes,
                ha="center", va="top",
                fontsize=9.5, fontweight="bold",
                color="#78281f"  # Deep red
            )

    plt.tight_layout()
    plt.savefig(out_file, bbox_inches="tight", transparent=True, dpi=dpi)
    pdf_out = out_file.with_suffix(".pdf")
    plt.savefig(pdf_out, bbox_inches="tight", transparent=True)
    plt.close()

    print(f"[Colorbar] Saved publication colorbar: {out_file} (and {pdf_out})")
    return out_file


def composite_image_with_colorbar(
    crystal_image_path: Union[str, Path],
    colorbar_image_path: Union[str, Path],
    output_composite_path: Union[str, Path],
    margin_spacing: int = 40,
) -> Path:
    """
    Horizontally composites an OVITO crystal snapshot with the publication colorbar.
    """
    c_img = Image.open(crystal_image_path).convert("RGBA")
    cb_img = Image.open(colorbar_image_path).convert("RGBA")

    # Scale colorbar to match crystal image height proportionally
    target_cb_height = int(c_img.height * 0.85)
    cb_aspect = cb_img.width / cb_img.height
    new_cb_width = max(1, int(target_cb_height * cb_aspect))
    cb_resized = cb_img.resize((new_cb_width, target_cb_height), Image.Resampling.LANCZOS)

    # Canvas width: crystal + margin + colorbar
    tot_width = c_img.width + margin_spacing + new_cb_width + 40
    tot_height = c_img.height

    composite = Image.new("RGBA", (tot_width, tot_height), (255, 255, 255, 255))
    composite.paste(c_img, (0, 0), c_img)

    # Center colorbar vertically on the right margin
    cb_y = (tot_height - target_cb_height) // 2
    cb_x = c_img.width + margin_spacing
    composite.paste(cb_resized, (cb_x, cb_y), cb_resized)

    out_comp = Path(output_composite_path).resolve()
    composite.save(out_comp, format="PNG")
    print(f"[Composite] Saved combined figure with colorbar: {out_comp} ({composite.width}x{composite.height})")
    return out_comp


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate publication STIX colorbars and composite onto crystal figures.")
    parser.add_argument("--output", "-o", default="colorbar.png", help="Output path for colorbar")
    parser.add_argument("--vmin", type=float, default=-0.30, help="Minimum value")
    parser.add_argument("--vmax", type=float, default=0.30, help="Maximum value")
    parser.add_argument("--cmap", default="coolwarm", help="Matplotlib colormap name")
    parser.add_argument("--label", default=r"$Q_{\mathrm{net}}\ (e)$", help="Colorbar LaTeX label")
    parser.add_argument("--composite", help="Crystal image path to composite with")
    parser.add_argument("--out-composite", default="figure_with_colorbar.png", help="Composite output path")
    args = parser.parse_args()

    cb_p = generate_publication_colorbar(
        output_path=args.output,
        vmin=args.vmin,
        vmax=args.vmax,
        colormap=args.cmap,
        label=args.label,
    )
    if args.composite:
        composite_image_with_colorbar(args.composite, cb_p, args.out_composite)
