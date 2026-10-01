#!/usr/bin/env python3
"""
================================================================================
Publication Animation & Multi-Frame Composer (animation_composer.py)
================================================================================
Enforces the Zero-Dilation Rule and Comfortable Animation Pacing for scientific
strain sweeps, reaction paths, and trajectory oscillations:
1. The Zero-Dilation Rule:
   - Validates that 100% of input frames possess identical pixel dimensions (W x H).
   - Prevents jittering caused by Matplotlib's bbox_inches='tight'.
   - Pads or resizes any mismatched frames to exact reference canvas dimensions.
2. Comfortable Animation Pacing:
   - Intermediate transition frames: 800 ms per frame.
   - Extrema hold frames (e.g. -3% and +3% maximum strain): 1200 ms hold.
   - Pristine / Equilibrium hold frames (0% strain): 1000 ms hold.
3. High-Fidelity Palette Optimization:
   - Quantizes frames with adaptive color palettes, preserving crisp Times New Roman /
     STIX text and smooth colormap gradients without dithering grain.
4. Smooth Cyclic Looping:
   - Supports forward-backward ping-pong oscillations (e.g. 0% -> +3% -> 0% -> -3% -> 0%).
================================================================================
"""

import argparse
import glob
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union
import numpy as np
from PIL import Image


def parse_numeric_label(filename: str) -> float:
    """Extracts numerical parameter (e.g., strain -3.0%, angle 15.5) for natural sorting."""
    m = re.search(r"[-+]?\d*\.?\d+", filename)
    return float(m.group(0)) if m else 0.0


def validate_and_normalize_frames(
    image_paths: List[Path],
    pad_background: Tuple[int, int, int, int] = (255, 255, 255, 255),
) -> List[Image.Image]:
    """
    Enforces the Zero-Dilation Rule: ensures every single frame matches the exact
    maximum canvas dimensions (W x H) without cropping content.
    """
    opened = [Image.open(p).convert("RGBA") for p in image_paths]
    widths = [img.width for img in opened]
    heights = [img.height for img in opened]

    target_w = max(widths)
    target_h = max(heights)

    is_uniform = all(w == target_w and h == target_h for w, h in zip(widths, heights))
    if is_uniform:
        print(f"[Zero-Dilation] All {len(opened)} frames have identical dimensions: {target_w}x{target_h} px. Perfect!")
        return opened

    print(f"[Zero-Dilation] Warning: Frame dimension variance detected (W: {min(widths)}-{target_w}, H: {min(heights)}-{target_h}).")
    print(f"[Zero-Dilation] Normalizing all frames to fixed canvas: {target_w}x{target_h} px...")

    normalized = []
    for idx, img in enumerate(opened):
        if img.width == target_w and img.height == target_h:
            normalized.append(img)
            continue
        # Create centered canvas
        canvas = Image.new("RGBA", (target_w, target_h), pad_background)
        ox = (target_w - img.width) // 2
        oy = (target_h - img.height) // 2
        canvas.paste(img, (ox, oy), mask=img)
        normalized.append(canvas)

    return normalized


def build_ping_pong_sequence(frames: List[Image.Image], filenames: List[str]) -> Tuple[List[Image.Image], List[str]]:
    """
    Constructs an oscillating cycle: A -> B -> C -> B -> A.
    Avoids duplicating the turning endpoints.
    """
    if len(frames) <= 2:
        return frames, filenames
    forward = frames
    backward = frames[-2:0:-1]
    f_names = filenames
    b_names = filenames[-2:0:-1]
    return forward + backward, f_names + b_names


def calculate_frame_durations(
    filenames: List[str],
    intermediate_ms: int = 800,
    extrema_ms: int = 1200,
    pristine_ms: int = 1000,
) -> List[int]:
    """
    Calculates pacing per frame: 800 ms standard, 1200 ms for extrema, 1000 ms for 0%.
    """
    durations = []
    # Identify values to find extrema and 0%
    nums = [parse_numeric_label(name) for name in filenames]
    min_val = min(nums) if nums else 0.0
    max_val = max(nums) if nums else 0.0

    for name, val in zip(filenames, nums):
        if abs(val - 0.0) < 1e-4 or "0%" in name or "pristine" in name.lower() or "eq" in name.lower():
            durations.append(pristine_ms)
        elif abs(val - min_val) < 1e-4 or abs(val - max_val) < 1e-4:
            durations.append(extrema_ms)
        else:
            durations.append(intermediate_ms)

    return durations


def compose_animation(
    image_pattern_or_files: Union[str, List[Union[str, Path]]],
    output_path: Union[str, Path] = "publication_animation.gif",
    intermediate_ms: int = 800,
    extrema_ms: int = 1200,
    pristine_ms: int = 1000,
    ping_pong: bool = False,
    sort_numeric: bool = True,
    loop: int = 0,
) -> Path:
    """
    Composes a publication-grade animated GIF obeying the Zero-Dilation Rule.
    """
    if isinstance(image_pattern_or_files, str):
        if os.path.isdir(image_pattern_or_files):
            files = sorted(Path(image_pattern_or_files).glob("*.png"))
        else:
            files = [Path(p) for p in sorted(glob.glob(image_pattern_or_files))]
    else:
        files = [Path(p) for p in image_pattern_or_files]

    if not files:
        raise FileNotFoundError(f"No image files found matching: {image_pattern_or_files}")

    if sort_numeric:
        files = sorted(files, key=lambda p: parse_numeric_label(p.name))

    print(f"[Animation] Found {len(files)} frames for animation sequence.")

    # 1. Zero-dilation validation & normalization
    frames = validate_and_normalize_frames(files)
    file_names = [f.name for f in files]

    # 2. Ping-pong cycle if requested
    if ping_pong:
        frames, file_names = build_ping_pong_sequence(frames, file_names)
        print(f"[Animation] Expanded to ping-pong cycle: {len(frames)} total frames.")

    # 3. Comfortable pacing calculation
    durations = calculate_frame_durations(
        filenames=file_names,
        intermediate_ms=intermediate_ms,
        extrema_ms=extrema_ms,
        pristine_ms=pristine_ms,
    )

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # 4. Save animated GIF with adaptive palette
    print(f"[Animation] Encoding GIF with adaptive palette quantization to: {out_file.name}...")
    rgb_frames = [f.convert("RGB") for f in frames]

    rgb_frames[0].save(
        out_file,
        save_all=True,
        append_images=rgb_frames[1:],
        duration=durations,
        loop=loop,
        optimize=True,
    )

    file_size_kb = out_file.stat().st_size / 1024
    print(f"🎉 Animation Complete: {out_file} ({file_size_kb:.1f} KB, {len(frames)} frames)")
    return out_file


def main():
    parser = argparse.ArgumentParser(
        description="Compose publication animations with the Zero-Dilation Rule & Comfortable Pacing"
    )
    parser.add_argument("frames", nargs="+", help="Input image files or glob pattern (e.g. './frames/frame_*.png')")
    parser.add_argument("-o", "--output", default="animation.gif", help="Output GIF path (default: animation.gif)")
    parser.add_argument("--intermediate-ms", type=int, default=800, help="Intermediate frame duration in ms (default: 800)")
    parser.add_argument("--extrema-ms", type=int, default=1200, help="Extrema hold duration in ms (default: 1200)")
    parser.add_argument("--pristine-ms", type=int, default=1000, help="Pristine (0%%) hold duration in ms (default: 1000)")
    parser.add_argument("--ping-pong", action="store_true", help="Loop forward then backward (0 -> +3%% -> 0 -> -3%% -> 0)")
    parser.add_argument("--no-sort", dest="sort", action="store_false", help="Do not sort frames numerically")

    args = parser.parse_args()

    # Expand any glob expressions if single string passed
    input_files = []
    for item in args.frames:
        if any(char in item for char in ["*", "?", "["]):
            matched = sorted(glob.glob(item))
            input_files.extend(matched)
        elif os.path.isdir(item):
            input_files.extend(sorted(glob.glob(os.path.join(item, "*.png"))))
        else:
            input_files.append(item)

    compose_animation(
        image_pattern_or_files=input_files,
        output_path=args.output,
        intermediate_ms=args.intermediate_ms,
        extrema_ms=args.extrema_ms,
        pristine_ms=args.pristine_ms,
        ping_pong=args.ping_pong,
        sort_numeric=args.sort,
    )


if __name__ == "__main__":
    main()
