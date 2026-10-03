"""
3D Volumetric Animation Engine for creating publication-quality CDD animations:
1. Biaxial strain breathing cycles (morphing between strain states)
2. 360° orbital rotation GIFs around a fixed structure
"""
import argparse
import os
import glob
from pathlib import Path
from PIL import Image
import numpy as np
from typing import List, Optional

def render_rotation_gif(
    structure_images: List[str],
    output_path: str,
    fps: int = 15,
    duration_per_frame: int = 67,  # ms, ~15 fps
    boomerang: bool = True,
):
    """Compose pre-rendered rotation frames into a smooth GIF."""
    if not structure_images:
        print("No images found for rotation gif.")
        return

    # Expand any glob patterns if passed as strings rather than shell expanded
    expanded_images = []
    for p in structure_images:
        if '*' in p or '?' in p:
            expanded_images.extend(glob.glob(p))
        else:
            expanded_images.append(p)
    
    frames = [Image.open(p).convert('RGBA') for p in sorted(expanded_images)]
    if boomerang and len(frames) > 2:
        frames = frames + frames[-2:0:-1]  # Reverse without duplicating endpoints
    
    if not frames:
        print("No images loaded.")
        return

    # Save GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_per_frame,
        loop=0,
        optimize=True,
    )
    print(f"Saved rotation GIF to {output_path}")

def crossfade(img1: Image.Image, img2: Image.Image, alpha: float) -> Image.Image:
    """Blend two PIL images with alpha crossfade."""
    a1 = np.array(img1, dtype=np.float32)
    a2 = np.array(img2, dtype=np.float32)
    blended = (1.0 - alpha) * a1 + alpha * a2
    return Image.fromarray(blended.astype(np.uint8))

def render_strain_breathing(
    frame_dirs: List[str],
    output_path: str,
    view: str = 'c',
    hold_frames: int = 3,  # Hold each strain state for N frames
    transition_frames: int = 5,  # Cross-fade between states
    fps: int = 10,
):
    """Create strain breathing cycle animation.
    
    Uses comfortable pacing from Zero-Dilation Rule:
    - 800ms per static slide (data-light)
    - 1200ms per data-heavy panel
    - 1000ms transitions
    """
    if not frame_dirs:
        print("No directories provided for strain breathing.")
        return

    images = []
    for d in frame_dirs:
        # Check for image based on view, fallback to any png
        patterns = [f"*{view}*.png", "*.png"]
        img_path = None
        for p in patterns:
            found = glob.glob(os.path.join(d, p))
            if found:
                img_path = sorted(found)[0]
                break
        
        if img_path and os.path.exists(img_path):
            images.append(Image.open(img_path).convert('RGBA'))
        else:
            print(f"Warning: No valid images found in {d}")
            
    if len(images) < 2:
        print("Not enough images found to animate breathing cycle.")
        return

    frames = []
    # Loop over the sequence and morph
    for i in range(len(images)):
        img1 = images[i]
        img2 = images[(i + 1) % len(images)]
        
        # Hold frames
        for _ in range(hold_frames):
            frames.append(img1)
            
        # Transition frames
        for j in range(1, transition_frames + 1):
            alpha = j / float(transition_frames + 1)
            frames.append(crossfade(img1, img2, alpha))
            
    duration_per_frame = int(1000 / fps)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_per_frame,
        loop=0,
        optimize=True,
    )
    print(f"Saved breathing GIF to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="3D Volumetric Animation Engine for CDD")
    parser.add_argument('--mode', choices=['rotation', 'breathing'], required=True, help="Animation mode")
    parser.add_argument('--frames', nargs='+', help="Input frame images (for rotation mode)")
    parser.add_argument('--dirs', nargs='+', help="Input frame directories (for breathing mode)")
    parser.add_argument('--output', required=True, help="Output GIF path")
    parser.add_argument('--fps', type=int, default=15, help="Frames per second")
    parser.add_argument('--boomerang', action='store_true', help="Forward + reverse for seamless loop")
    parser.add_argument('--view', default='c', help="View angle for breathing mode")
    
    args = parser.parse_args()
    
    if args.mode == 'rotation':
        if not args.frames:
            parser.error("--frames required for rotation mode")
        render_rotation_gif(args.frames, args.output, fps=args.fps, boomerang=args.boomerang)
    elif args.mode == 'breathing':
        if not args.dirs:
            parser.error("--dirs required for breathing mode")
        render_strain_breathing(args.dirs, args.output, view=args.view, fps=args.fps)

if __name__ == '__main__':
    main()
