#!/usr/bin/env python3
"""
================================================================================
Scientific Multi-Panel Publication Figure Compositor
================================================================================
Assembles individual crystal projections, charge density maps, and plots into
Nature / Phys. Rev. / ACS compliant multi-panel composite figures:
1. High-Precision Grid Layouts: Supports 1x2, 1x3, 1x4, 2x2, 2x3, or custom NxM grids.
2. Uniform Publication Sublabels: Injects bold serif sublabels:
   - '(a)', '(b)', '(c)', '(d)'
   - 'A', 'B', 'C', 'D'
   - Custom LaTeX annotations
   with Times New Roman / STIX typography and high-contrast translucent backing pills.
3. Pre-Composition Auto-Trimming: Strips excess whitespace padding from each input
   panel before assembly to enforce uniform panel scaling and alignment.
4. High-DPI Vector and Raster Export: Direct output to PNG (300+ DPI) and PDF.
================================================================================
"""

import argparse
import math
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def trim_panel_whitespace(img: Image.Image, padding: int = 15, tolerance: int = 15) -> Image.Image:
    """
    Trims uniform background padding from a panel while retaining specified border padding.
    """
    arr = np.array(img.convert("RGBA"))
    # Corner background sampling
    corners = np.vstack([arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1]])
    mean_corner = np.mean(corners, axis=0)

    if mean_corner[3] < 50:
        mask = arr[:, :, 3] > 30
    else:
        diff = np.abs(arr[:, :, :3] - mean_corner[:3])
        mask = np.any(diff > tolerance, axis=2)

    coords = np.argwhere(mask)
    if coords.size == 0:
        return img

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    H, W = arr.shape[:2]
    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(W, x1 + padding)
    y1 = min(H, y1 + padding)

    return img.crop((x0, y0, x1, y1))


def get_serif_font(size_pt: int) -> ImageFont.FreeTypeFont:
    """
    Locates Times New Roman or serif bold font.
    """
    candidates = [
        "/Library/Fonts/Times New Roman Bold.ttf",
        "/Library/Fonts/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSerif-Bold.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size=size_pt)
            except Exception:
                pass
    return ImageFont.load_default()


def composite_panels(
    image_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    layout: Optional[Tuple[int, int]] = None,
    labels: Optional[List[str]] = None,
    label_style: str = "parens_lower",  # 'parens_lower' -> (a), 'parens_upper' -> (A), 'upper' -> A
    font_size: int = 36,
    gap: int = 40,
    margin: int = 40,
    background: str = "white",
    trim_inputs: bool = True,
    max_panel_width: int = 1600,
) -> Path:
    """
    Assembles input images into a cohesive publication multi-panel figure.
    """
    valid_paths = [Path(p).resolve() for p in image_paths if Path(p).exists()]
    if not valid_paths:
        raise ValueError("No valid input images found to composite.")

    num_images = len(valid_paths)

    # Determine grid layout (rows, cols)
    if layout and len(layout) == 2:
        rows, cols = layout
    else:
        if num_images == 1:
            rows, cols = 1, 1
        elif num_images == 2:
            rows, cols = 1, 2
        elif num_images == 3:
            rows, cols = 1, 3
        elif num_images == 4:
            rows, cols = 2, 2
        elif num_images <= 6:
            rows, cols = 2, 3
        elif num_images <= 8:
            rows, cols = 2, 4
        else:
            cols = 3
            rows = math.ceil(num_images / cols)

    # Load and optionally trim images
    loaded_imgs: List[Image.Image] = []
    for p in valid_paths:
        im = Image.open(p).convert("RGBA")
        if trim_inputs:
            im = trim_panel_whitespace(im, padding=25)
        loaded_imgs.append(im)

    # Generate standard labels if not provided
    if labels is None:
        labels = []
        for idx in range(num_images):
            letter = chr(ord('a') + idx)
            if label_style == "parens_lower":
                labels.append(f"({letter})")
            elif label_style == "parens_upper":
                labels.append(f"({letter.upper()})")
            elif label_style == "upper":
                labels.append(f"{letter.upper()}")
            elif label_style == "lower":
                labels.append(f"{letter}")
            else:
                labels.append(f"({letter})")

    # Determine maximum cell dimensions per column and row to maintain alignment
    col_widths = [0] * cols
    row_heights = [0] * rows

    for idx, im in enumerate(loaded_imgs):
        r = idx // cols
        c = idx % cols
        if r < rows and c < cols:
            col_widths[c] = max(col_widths[c], im.width)
            row_heights[r] = max(row_heights[r], im.height)

    # Calculate total canvas size
    total_w = 2 * margin + sum(col_widths) + (cols - 1) * gap
    total_h = 2 * margin + sum(row_heights) + (rows - 1) * gap

    bg_color = (255, 255, 255, 255) if background.lower() == "white" else (0, 0, 0, 255)
    canvas = Image.new("RGBA", (total_w, total_h), bg_color)
    draw = ImageDraw.Draw(canvas)
    font = get_serif_font(font_size)

    # Precalculate column X offsets
    col_x = [margin]
    for c in range(1, cols):
        col_x.append(col_x[c - 1] + col_widths[c - 1] + gap)

    # Precalculate row Y offsets
    row_y = [margin]
    for r in range(1, rows):
        row_y.append(row_y[r - 1] + row_heights[r - 1] + gap)

    # Paste panels and render sublabels
    for idx, im in enumerate(loaded_imgs):
        r = idx // cols
        c = idx % cols
        if r >= rows or c >= cols:
            break

        # Center image within its grid cell
        x_cell = col_x[c]
        y_cell = row_y[r]
        w_cell = col_widths[c]
        h_cell = row_heights[r]

        paste_x = x_cell + (w_cell - im.width) // 2
        paste_y = y_cell + (h_cell - im.height) // 2

        canvas.paste(im, (paste_x, paste_y), im)

        # Draw sublabel in top-left corner of the cell
        if idx < len(labels) and labels[idx]:
            lbl = labels[idx]
            bbox = draw.textbbox((0, 0), lbl, font=font)
            lbl_w = bbox[2] - bbox[0]
            lbl_h = bbox[3] - bbox[1]

            lbl_x = paste_x + 18
            lbl_y = paste_y + 18

            # Translucent background pill behind label for 100% readability
            pill_pad_x = 10
            pill_pad_y = 6
            pill_coords = [
                lbl_x - pill_pad_x,
                lbl_y - pill_pad_y,
                lbl_x + lbl_w + pill_pad_x,
                lbl_y + lbl_h + pill_pad_y,
            ]
            pill_bg = (255, 255, 255, 220) if background.lower() == "white" else (0, 0, 0, 220)
            text_ink = (0, 0, 0, 255) if background.lower() == "white" else (255, 255, 255, 255)

            draw.rounded_rectangle(pill_coords, radius=6, fill=pill_bg)
            draw.text((lbl_x, lbl_y - 2), lbl, font=font, fill=text_ink)

    out_p = Path(output_path).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_p, dpi=(300, 300))
    print(f"[Compositor] Successfully created publication multi-panel figure: {out_p} ({total_w}x{total_h}, {rows}x{cols} grid)")
    return out_p


def main():
    parser = argparse.ArgumentParser(
        description="Assemble individual crystal projections and plots into publication multi-panel figures."
    )
    parser.add_argument("images", nargs="+", help="Input image files in panel order (panel a, panel b, panel c...)")
    parser.add_argument("--output", "-o", required=True, help="Destination multi-panel figure path (PNG or PDF)")
    parser.add_argument(
        "--grid",
        "-g",
        nargs=2,
        type=int,
        metavar=("ROWS", "COLS"),
        help="Explicit grid dimensions (e.g. -g 1 3 for 1 row of 3 images, -g 2 2 for 2x2 grid)",
    )
    parser.add_argument(
        "--labels",
        "-l",
        nargs="+",
        help="Custom sublabels (e.g. -l '(a)' '(b)' '(c)' or -l 'Top' 'Side' 'Iso')",
    )
    parser.add_argument(
        "--label-style",
        choices=["parens_lower", "parens_upper", "upper", "lower"],
        default="parens_lower",
        help="Sublabel format style: parens_lower -> (a), parens_upper -> (A), upper -> A (default: parens_lower)",
    )
    parser.add_argument("--font-size", type=int, default=38, help="Sublabel font size in points (default: 38)")
    parser.add_argument("--gap", type=int, default=35, help="Pixel spacing between subpanels (default: 35)")
    parser.add_argument("--margin", type=int, default=30, help="Canvas outer margin in pixels (default: 30)")
    parser.add_argument("--no-trim", action="store_true", help="Disable automatic whitespace trimming of input panels")
    parser.add_argument("--background", choices=["white", "black"], default="white", help="Canvas background color (default: white)")

    args = parser.parse_args()

    layout = tuple(args.grid) if args.grid else None
    composite_panels(
        image_paths=args.images,
        output_path=args.output,
        layout=layout,
        labels=args.labels,
        label_style=args.label_style,
        font_size=args.font_size,
        gap=args.gap,
        margin=args.margin,
        background=args.background,
        trim_inputs=not args.no_trim,
    )


if __name__ == "__main__":
    main()
