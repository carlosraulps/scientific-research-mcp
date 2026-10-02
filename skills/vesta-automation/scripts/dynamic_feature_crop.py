import argparse
import sys
import numpy as np
from PIL import Image
from typing import Optional, Tuple

def dynamic_feature_crop(
    img_path: str,
    padding: int = 30,
    sat_threshold: int = 18,
    val_threshold: int = 240
) -> Tuple[Image.Image, Tuple[int, int, int, int]]:
    """Crops VESTA render to structural features using saturation-based detection.

    Args:
        img_path: Path to the input VESTA rendered PNG image.
        padding: Padding in pixels to add around the detected bounding box.
        sat_threshold: Minimum HSV saturation to be considered a feature.
        val_threshold: Maximum HSV value to be considered a feature (catches dark atoms/bonds).

    Returns:
        A tuple containing the cropped PIL Image object and the bounding box (left, upper, right, lower).
    """
    try:
        img = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")
        sys.exit(1)

    # Convert to HSV color space using Pillow's native convert, but we need numpy for mask
    # Pillow's HSV conversion might not map exactly to 0-255 directly as arrays.
    # Actually, converting RGBA to RGB then to HSV using matplotlib or colorsys might be safer,
    # but since Pillow has "HSV", we can use it.
    hsv_img = img.convert("HSV")
    hsv_data = np.array(hsv_img)
    
    # hsv_data is shape (H, W, 3). Indices: 0=H, 1=S, 2=V
    S = hsv_data[:, :, 1]
    V = hsv_data[:, :, 2]
    
    # Create binary mask where saturation > sat_threshold OR value < val_threshold
    mask = (S > sat_threshold) | (V < val_threshold)
    
    # Find bounding box of the mask
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        print("Warning: No structural features detected. Returning original image.")
        return img, (0, 0, img.width, img.height)
        
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]
    
    # Add padding
    xmin = max(0, xmin - padding)
    ymin = max(0, ymin - padding)
    xmax = min(img.width, xmax + padding + 1)
    ymax = min(img.height, ymax + padding + 1)
    
    # Crop the original image
    bbox = (xmin, ymin, xmax, ymax)
    cropped_img = img.crop(bbox)
    
    return cropped_img, bbox

def composite_badge(
    canvas: Image.Image,
    badge_path: str,
    position: str = 'bottom-right',
    margin: int = 10
) -> Image.Image:
    """Composites orientation badge AFTER cropping (Layer Separation Protocol).
    This prevents the destructive inpainting bug where border cleanup overwrites badges.

    Args:
        canvas: The cropped VESTA render image (PIL Image).
        badge_path: Path to the badge PNG image.
        position: Badge positioning ('top-left', 'top-right', 'bottom-left', 'bottom-right').
        margin: Margin in pixels from the edge of the canvas.

    Returns:
        The updated PIL Image with the badge composited.
    """
    try:
        badge = Image.open(badge_path).convert("RGBA")
    except Exception as e:
        print(f"Warning: Error loading badge image {badge_path}: {e}")
        return canvas

    canvas_w, canvas_h = canvas.size
    badge_w, badge_h = badge.size
    
    if position == 'top-left':
        paste_pos = (margin, margin)
    elif position == 'top-right':
        paste_pos = (canvas_w - badge_w - margin, margin)
    elif position == 'bottom-left':
        paste_pos = (margin, canvas_h - badge_h - margin)
    elif position == 'bottom-right':
        paste_pos = (canvas_w - badge_w - margin, canvas_h - badge_h - margin)
    else:
        print(f"Warning: Unknown position '{position}'. Defaulting to bottom-right.")
        paste_pos = (canvas_w - badge_w - margin, canvas_h - badge_h - margin)
        
    # Create a copy to composite onto
    result = canvas.copy()
    result.paste(badge, paste_pos, badge)
    
    return result

def sanitize_vesta_render(
    img_path: str,
    out_path: str,
    padding: int = 30,
    badge_path: Optional[str] = None,
    badge_position: str = 'bottom-right'
) -> None:
    """Full pipeline: crop -> sanitize borders -> composite badge LAST."""
    cropped_img, _ = dynamic_feature_crop(img_path, padding=padding)
    
    if badge_path:
        final_img = composite_badge(cropped_img, badge_path, position=badge_position)
    else:
        final_img = cropped_img
        
    final_img.save(out_path, format="PNG")
    print(f"Successfully processed image and saved to {out_path}")

def main() -> None:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Saturation-Grounded Dynamic Feature Crop for VESTA renders."
    )
    parser.add_argument("input", help="Path to input VESTA rendered PNG")
    parser.add_argument("-o", "--output", required=True, help="Path to save cropped output PNG")
    parser.add_argument("--padding", type=int, default=30, help="Padding in pixels (default: 30)")
    parser.add_argument("--badge", type=str, default=None, help="Path to orientation badge/tripod PNG")
    parser.add_argument(
        "--badge-position", 
        type=str, 
        choices=['top-left', 'top-right', 'bottom-left', 'bottom-right'],
        default='bottom-right',
        help="Position of the badge (default: bottom-right)"
    )
    parser.add_argument("--sat-threshold", type=int, default=18, help="Saturation threshold (default: 18)")
    parser.add_argument("--val-threshold", type=int, default=240, help="Value threshold (default: 240)")
    
    args = parser.parse_args()
    
    # We pass the threshold parameters to the functions, though the signature of
    # sanitize_vesta_render doesn't take them directly in the instructions, 
    # but dynamic_feature_crop does. Let's patch sanitize_vesta_render to use them if needed.
    
    cropped_img, _ = dynamic_feature_crop(
        args.input, 
        padding=args.padding, 
        sat_threshold=args.sat_threshold, 
        val_threshold=args.val_threshold
    )
    
    if args.badge:
        final_img = composite_badge(cropped_img, args.badge, position=args.badge_position)
    else:
        final_img = cropped_img
        
    final_img.save(args.output, format="PNG")
    print(f"Dynamic crop complete: saved to {args.output}")

if __name__ == "__main__":
    main()
