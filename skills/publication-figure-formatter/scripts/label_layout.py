#!/usr/bin/env python3
"""
CLI Tool for Generating Collision-Free Scientific Plots with Times New Roman & STIX Math.
Supports adjustText and textalloc backends.
"""

import argparse
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from style_config import auto_adjust_labels, save_publication_figure, set_publication_style


def plot_dataset(
    data_file: str,
    output_path: str,
    engine: str = "adjustText",
    x_col: str = "x",
    y_col: str = "y",
    label_col: str = "label",
    title: str = None,
    x_label: str = None,
    y_label: str = None,
):
    import pandas as pd

    df = pd.read_csv(data_file)
    if x_col not in df.columns or y_col not in df.columns:
        print(f"Error: Columns '{x_col}' and '{y_col}' must exist in {data_file}", file=sys.stderr)
        sys.exit(1)

    set_publication_style()

    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=300)

    x = df[x_col].values
    y = df[y_col].values
    labels = df[label_col].astype(str).tolist() if label_col in df.columns else [f"P{i}" for i in range(len(x))]

    ax.scatter(x, y, color="#2b5c8f", s=50, edgecolors="white", linewidth=0.8, zorder=3)

    auto_adjust_labels(
        ax,
        x=x,
        y=y,
        labels=labels,
        engine=engine,
        text_size=10,
        draw_lines=True,
    )

    ax.set_xlabel(x_label or r"$X\ \mathrm{Coordinate}$", fontsize=12)
    ax.set_ylabel(y_label or r"$Y\ \mathrm{Coordinate}$", fontsize=12)
    if title:
        ax.set_title(title, fontsize=13, pad=10)

    ax.grid(True, linestyle="--", alpha=0.4, zorder=0)

    save_publication_figure(fig, output_path)
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Format and render collision-free scientific figures using adjustText / textalloc."
    )
    parser.add_argument("data", help="Path to CSV or TSV data file containing coordinates and labels")
    parser.add_argument("--output", "-o", default="publication_figure.png", help="Output file base path")
    parser.add_argument(
        "--engine",
        "-e",
        choices=["adjustText", "textalloc"],
        default="adjustText",
        help="Collision avoidance engine (default: adjustText)",
    )
    parser.add_argument("--x-col", default="x", help="Name of X column (default: x)")
    parser.add_argument("--y-col", default="y", help="Name of Y column (default: y)")
    parser.add_argument("--label-col", default="label", help="Name of label column (default: label)")
    parser.add_argument("--title", help="Figure title")
    parser.add_argument("--xlabel", help="X-axis label (LaTeX supported)")
    parser.add_argument("--ylabel", help="Y-axis label (LaTeX supported)")

    args = parser.parse_args()
    plot_dataset(
        data_file=args.data,
        output_path=args.output,
        engine=args.engine,
        x_col=args.x_col,
        y_col=args.y_col,
        label_col=args.label_col,
        title=args.title,
        x_label=args.xlabel,
        y_label=args.ylabel,
    )


if __name__ == "__main__":
    main()
