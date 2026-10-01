#!/usr/bin/env python3
"""
================================================================================
XCrySDen Publication Image Post-Processing & Background Whitening Pipeline
================================================================================
Transforms raw XCrySDen OpenGL screen dumps and renders into Nature/PRB publication standards:
1. Background Whitening: Inverts or remaps default black (#000000) backgrounds
   to pure white (#FFFFFF) while strictly preserving atomic colors, bond cylinders,
   and 2D contour color fidelity.
2. Soft Antialiasing & Fringe Correction: Blends dark boundary edge pixels smoothly
   into the white background to eliminate jagged black halos around atoms and contours.
3. Automated Canvas Bounding Box Trimming: Crops redundant whitespace padding.
================================================================================
"""

import sys
from pathlib import Path
from typing import Optional, Union
import numpy as np
from PIL import Image


def invert_black_background(
    input_image: Union[str, Path],
    output_image: Optional[Union[str, Path]] = None,
    dark_threshold: int = 25,
    blend_width: int = 35,
    trim_borders: bool = True,
    border_padding: int = 30,
) -> Path:
    """
    Remaps dark/black backgrounds to pure white with smooth fringe antialiasing.
    
    Args:
        input_image: Path to input image file (PNG, JPG, PPM).
        output_image: Destination path (defaults to overwrite or <stem>_white.png).
        dark_threshold: Maximum RGB value considered solid background (0-255).
        blend_width: Soft gradient transition width for edge antialiasing.
        trim_borders: Whether to crop uniform outer margins.
        border_padding: Pixels of padding to retain around trimmed content.
        
    Returns:
        Path to processed output image.
    """
    in_path = Path(input_image).resolve()
    if not in_path.exists():
        raise FileNotFoundError(f"Input image not found: {in_path}")

    out_path = Path(output_image).resolve() if output_image else in_path.parent / f"{in_path.stem}_white.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.open(in_path).convert("RGBA")
    arr = np.array(img, dtype=np.float32)

    # Calculate brightness / max channel
    rgb = arr[:, :, :3]
    max_rgb = np.max(rgb, axis=2)

    # 1. Pure dark background mask
    is_pure_dark = max_rgb <= dark_threshold
    
    # 2. Fringe transition zone for antialiased edge smoothing
    is_transition = (max_rgb > dark_threshold) & (max_rgb <= (dark_threshold + blend_width))

    # Initialize output RGB array
    out_rgb = rgb.copy()

    # Set solid background to pure white
    out_rgb[is_pure_dark] = [255.0, 255.0, 255.0]

    # Smoothly blend boundary edge pixels towards white
    if np.any(is_transition):
        # alpha goes from 0.0 (near background) to 1.0 (pure foreground)
        t_alpha = (max_rgb[is_transition] - dark_threshold) / float(blend_width)
        t_alpha = np.clip(t_alpha, 0.0, 1.0)[:, np.newaxis]

        original_colors = rgb[is_transition]
        # Invert the dark component while keeping hue
        boosted_colors = 255.0 - (255.0 - original_colors) * (1.0 - t_alpha * 0.5)
        out_rgb[is_transition] = boosted_colors

    out_arr = np.clip(out_rgb, 0.0, 255.0).astype(np.uint8)
    alpha_chan = np.full((arr.shape[0], arr.shape[1], 1), 255, dtype=np.uint8)
    result_img = Image.fromarray(np.concatenate([out_arr, alpha_chan], axis=2), mode="RGBA")

    # 3. Auto-crop whitespace margins
    if trim_borders:
        # Convert to grayscale to locate non-white content
        gray = np.mean(out_arr, axis=2)
        non_white = np.where(gray < 250)
        if len(non_white[0]) > 0 and len(non_white[1]) > 0:
            ymin, ymax = non_white[0].min(), non_white[0].max()
            xmin, xmax = non_white[1].min(), non_white[1].max()

            h, w = gray.shape
            ymin = max(0, ymin - border_padding)
            ymax = min(h, ymax + border_padding)
            xmin = max(0, xmin - border_padding)
            xmax = min(w, xmax + border_padding)

            result_img = result_img.crop((xmin, ymin, xmax, ymax))

    result_img.save(out_path, format="PNG")
    print(f"[Post-Process] White background image saved: {out_path} ({result_img.size[0]}x{result_img.size[1]})")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Remap black XCrySDen backgrounds to pure publication white.")
    parser.add_argument("input", help="Path to input image file")
    parser.add_argument("--output", "-o", help="Path to output white-background image")
    parser.add_argument("--threshold", type=int, default=25, help="Dark threshold (default: 25)")
    parser.add_argument("--padding", type=int, default=30, help="Border padding pixels (default: 30)")
    parser.add_argument("--no-trim", action="store_true", help="Disable automatic border trimming")
    args = parser.parse_args()

    invert_black_background(
        input_image=args.input,
        output_image=args.output,
        dark_threshold=args.threshold,
        trim_borders=not args.no_trim,
        border_padding=args.padding,
    )
