"""
Scientific Publication Plotting & Typography Configuration.
Enforces Times New Roman serif typography, STIX math rendering,
and collision-free label allocation via adjustText and textalloc.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np

# Ensure module directory is in sys.path for robust global imports
_scripts_dir = str(Path(__file__).parent.resolve())
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# Import VESTA color palette and Colorblind standards
from vesta_colors import (
    COLORBLIND_DIVERGING,
    COLORBLIND_SEQUENTIAL,
    OKABE_ITO,
    OKABE_ITO_LIST,
    TOL_BRIGHT,
    TOL_MUTED,
    VESTA_ELEMENTS,
    get_element_cycler,
    get_element_palette,
    get_vesta_color,
)


def set_publication_style(
    font_size: int = 11,
    tick_size: int = 10,
    label_size: int = 12,
    title_size: int = 13,
    linewidth: float = 1.2,
):
    """
    Apply mandatory scientific typography and formatting standards:
    - Times New Roman with robust cross-platform serif fallbacks
    - STIX math fontset matching Nature, Phys. Rev., and ACS standards
    - Inward ticks and clean axes spines
    """
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": [
            "Times New Roman",
            "Nimbus Roman",
            "Liberation Serif",
            "STIXGeneral",
            "DejaVu Serif",
        ],
        "mathtext.fontset": "stix",
        "font.size": font_size,
        "axes.labelsize": label_size,
        "axes.titlesize": title_size,
        "xtick.labelsize": tick_size,
        "ytick.labelsize": tick_size,
        "legend.fontsize": font_size,
        "axes.linewidth": linewidth,
        "axes.edgecolor": "#222222",
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 4.5,
        "ytick.major.size": 4.5,
        "xtick.major.width": linewidth,
        "ytick.major.width": linewidth,
        "figure.autolayout": False,
        "savefig.bbox": "tight",
        "savefig.dpi": 300,
    })


def auto_adjust_labels(
    ax,
    x: Union[List[float], np.ndarray],
    y: Union[List[float], np.ndarray],
    labels: List[str],
    engine: str = "adjustText",
    text_size: int = 10,
    draw_lines: bool = True,
    line_color: str = "#555555",
    line_width: float = 0.8,
    **kwargs,
):
    """
    Allocate non-overlapping text labels using adjustText or textalloc.

    Parameters:
    - ax: Matplotlib axes object
    - x, y: Data coordinates for target points
    - labels: Text strings (supports LaTeX r"$...$")
    - engine: 'adjustText' (force-directed) or 'textalloc' (bounding-box allocation)
    - text_size: Font size for labels
    - draw_lines: Draw leader lines / arrows to points
    - line_color: Leader line color
    """
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    if engine.lower() == "textalloc":
        import textalloc as ta

        ta.allocate(
            ax,
            x_arr,
            y_arr,
            labels,
            x_scatter=x_arr,
            y_scatter=y_arr,
            textsize=text_size,
            draw_lines=draw_lines,
            linecolor=line_color,
            linewidth=line_width,
            **kwargs,
        )
    else:
        from adjustText import adjust_text

        texts = [
            ax.text(x_arr[i], y_arr[i], labels[i], fontsize=text_size)
            for i in range(len(labels))
        ]
        arrowprops = (
            dict(arrowstyle="->", color=line_color, lw=line_width)
            if draw_lines
            else None
        )
        adjust_text(
            texts,
            arrowprops=arrowprops,
            ax=ax,
            **kwargs,
        )


def save_publication_figure(fig, output_path: str, dpi: int = 300):
    """
    Dual-format exporter: saves both 300 DPI PNG and vector PDF.
    """
    from pathlib import Path

    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    base = out.parent / out.stem
    png_path = base.with_suffix(".png")
    pdf_path = base.with_suffix(".pdf")

    fig.savefig(str(png_path), dpi=dpi, bbox_inches="tight")
    fig.savefig(str(pdf_path), bbox_inches="tight")
    print(f"Saved publication figures:\n  Raster: {png_path}\n  Vector: {pdf_path}")
    return str(png_path), str(pdf_path)
