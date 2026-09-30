#!/usr/bin/env python3
"""
================================================================================
Physical Scale Bar Overlay & Margin Auto-Trimmer for Crystal Visualizations
================================================================================
Enforces Nature / Phys. Rev. publication standards:
1. Physical Scale Bar: Exact world-coordinate scale bar (e.g. 5 Å, 1 nm)
   calculated from Viewport FOV in orthographic projections.
2. Publication Typography: STIX / Times New Roman serif font with clean
   high-contrast backing box.
3. Whitespace Auto-Trimming: Trims excess canvas background to a calibrated
   padding margin (default: 30 px).
================================================================================
"""

import sys
from pathlib import Path
from typing import Optional, Tuple, Union
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def autotrim_whitespace(
    image_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    padding: int = 30,
    tolerance: int = 15,
) -> Path:
    """
    Trims excess uniform background (white, black, or transparent) while
    preserving a clean publication padding border.
    """
    in_p = Path(image_path).resolve()
    out_p = Path(output_path).resolve() if output_path else in_p

    img = Image.open(in_p).convert("RGBA")
    arr = np.array(img)

    # Determine background from corner pixels
    corners = np.vstack([
        arr[0, 0],
        arr[0, -1],
        arr[-1, 0],
        arr[-1, -1],
    ])
    mean_corner = np.mean(corners, axis=0)

    # Check if background is transparent or colored
    if mean_corner[3] < 50:
        # Transparent background
        mask = arr[:, :, 3] > 30
    else:
        # Distance from background color
        diff = np.abs(arr[:, :, :3] - mean_corner[:3])
        mask = np.any(diff > tolerance, axis=2)

    coords = np.argwhere(mask)
    if coords.size == 0:
        # All background, return original
        return out_p

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    # Add padding clamped to image bounds
    H, W = arr.shape[:2]
    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(W, x1 + padding)
    y1 = min(H, y1 + padding)

    cropped = img.crop((x0, y0, x1, y1))
    cropped.save(out_p)
    return out_p


def add_scale_bar(
    image_path: Union[str, Path],
    length_angstrom: float,
    fov_angstrom: float,
    output_path: Optional[Union[str, Path]] = None,
    position: str = "lower-right",
    unit_label: Optional[str] = None,
    bar_thickness_pt: int = 6,
    font_size_pt: int = 18,
    margin_px: int = 50,
    color: str = "black",
    background_box: bool = True,
) -> Path:
    """
    Calculates and draws an authentic physical scale bar onto an orthographic
    crystal projection image.

    Args:
        image_path: Path to rendered PNG image.
        length_angstrom: Physical length of scale bar in Angstroms (e.g. 5.0).
        fov_angstrom: Viewport vertical field of view (height) in Angstroms.
        output_path: Output PNG path (overwrites image_path if None).
        position: 'lower-right', 'lower-left', 'upper-right', or 'upper-left'.
        unit_label: Custom text (e.g. "5 Å" or "0.5 nm"). If None, automatically formatted.
        bar_thickness_pt: Line thickness in points.
        font_size_pt: Font size for label text.
        margin_px: Offset from image borders in pixels.
        color: 'black' or 'white'.
        background_box: If True, draws a translucent high-contrast pill behind scale bar.
    """
    in_p = Path(image_path).resolve()
    out_p = Path(output_path).resolve() if output_path else in_p

    img = Image.open(in_p).convert("RGBA")
    W, H = img.size

    # In Ovito ortho view: 1 Angstrom = H / fov_angstrom pixels
    px_per_angstrom = H / fov_angstrom
    bar_px = int(round(length_angstrom * px_per_angstrom))

    # Fallback/clamp if bar is too long or too short
    bar_px = max(10, min(bar_px, W - 2 * margin_px))

    if unit_label is None:
        if length_angstrom >= 10.0 and length_angstrom % 10.0 == 0:
            nm = length_angstrom / 10.0
            unit_label = f"{nm:.0f} nm"
        elif length_angstrom == int(length_angstrom):
            unit_label = f"{int(length_angstrom)} Å"
        else:
            unit_label = f"{length_angstrom:.1f} Å"

    # Load serif font with fallbacks
    font = None
    serif_candidates = [
        "/Library/Fonts/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSerif-Bold.ttf",
    ]
    for c in serif_candidates:
        if Path(c).exists():
            try:
                font = ImageFont.truetype(c, size=font_size_pt)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)
    # Measure text bounding box
    bbox = draw.textbbox((0, 0), unit_label, font=font)
    t_w = bbox[2] - bbox[0]
    t_h = bbox[3] - bbox[1]

    # Calculate placement
    content_w = max(bar_px, t_w)
    total_h = bar_thickness_pt + 8 + t_h

    if "right" in position:
        x_start = W - margin_px - content_w
    else:
        x_start = margin_px

    if "lower" in position:
        y_start = H - margin_px - total_h
    else:
        y_start = margin_px

    # Align bar and text centered relative to content_w
    bar_x0 = x_start + (content_w - bar_px) // 2
    bar_x1 = bar_x0 + bar_px
    bar_y0 = y_start + t_h + 8
    bar_y1 = bar_y0 + bar_thickness_pt

    text_x = x_start + (content_w - t_w) // 2
    text_y = y_start

    ink_color = (0, 0, 0, 255) if color == "black" else (255, 255, 255, 255)
    box_bg = (255, 255, 255, 215) if color == "black" else (0, 0, 0, 200)

    if background_box:
        pad_x = 18
        pad_y = 12
        box_coords = [
            x_start - pad_x,
            y_start - pad_y,
            x_start + content_w + pad_x,
            y_start + total_h + pad_y,
        ]
        # Draw translucent rounded rectangle
        draw.rounded_rectangle(box_coords, radius=8, fill=box_bg)

    # Draw label and scale line
    draw.text((text_x, text_y), unit_label, font=font, fill=ink_color)
    draw.rectangle([bar_x0, bar_y0, bar_x1, bar_y1], fill=ink_color)

    img.save(out_p)
    return out_p


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Apply scale bar and auto-trimming to crystal images.")
    parser.add_argument("image", help="Input image file")
    parser.add_argument("--scale-bar", "-s", type=float, help="Length in Angstroms (e.g. 5.0 for 5 Å)")
    parser.add_argument("--fov", "-f", type=float, help="Viewport FOV height in Angstroms")
    parser.add_argument("--trim", "-t", action="store_true", help="Auto-trim whitespace margins")
    parser.add_argument("--output", "-o", help="Output image file")
    args = parser.parse_args()

    out = Path(args.output) if args.output else Path(args.image)
    if args.trim:
        autotrim_whitespace(args.image, out)
    if args.scale_bar and args.fov:
        add_scale_bar(out, length_angstrom=args.scale_bar, fov_angstrom=args.fov, output_path=out)
    print(f"Processed: {out}")
