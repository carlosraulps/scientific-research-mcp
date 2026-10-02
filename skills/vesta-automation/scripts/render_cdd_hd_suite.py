#!/usr/bin/env python3
"""
Multi-view CDD publication suite that renders multiple crystallographic projections 
of charge density difference automatically.

This script processes VASP volumetric files (CHGCAR, PARCHG, LOCPOT) and renders
views along crystallographic axes as well as isometric and edge-on views.
"""
import argparse
import sys
import os
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Union

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageChops

# Ensure we can run headlessly
if not os.environ.get('DISPLAY'):
    os.environ['DISPLAY'] = ':99'
    # Start Xvfb if not running? We'll assume the user uses xvfb-run or we fallback to headless backends
    import matplotlib
    matplotlib.use('Agg')

# Attempt to import vesta_cdd if it exists
try:
    import vesta_cdd
except ImportError:
    # Define a stub if not present in the environment for testing
    class vesta_cdd_stub:
        @staticmethod
        def render_cdd(*args, **kwargs) -> str:
            output = kwargs.get('output_path', 'dummy.png')
            img = Image.new('RGBA', (800, 800), (255, 255, 255, 255))
            img.save(output)
            return output
    vesta_cdd = vesta_cdd_stub()

# Import publication style
try:
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "publication-figure-formatter" / "scripts"))
    import style_config
except ImportError:
    style_config = None

def dynamic_feature_crop(img_path: str) -> None:
    """
    Non-destructive border inpainting (white border cleanup without touching structural features).
    Uses PIL to crop out surrounding white space.

    Args:
        img_path (str): The absolute or relative path to the image to be cropped.
    """
    img = Image.open(img_path).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)
        # Add a small padding
        padding = 20
        new_size = (img.width + 2*padding, img.height + 2*padding)
        new_img = Image.new("RGBA", new_size, (255, 255, 255, 255))
        new_img.paste(img, (padding, padding))
        new_img.save(img_path)

def render_cdd_suite(
    cdd_file: str,
    output_dir: Optional[str] = None,
    views: Tuple[str, ...] = ('a', 'b', 'c', 'iso'),
    pos_level: float = 0.005,
    neg_level: float = -0.005,
    opacity: float = 0.60,
    scale: float = 2.0,
    compose_panel: bool = True,
    panel_output: Optional[str] = None,
    figsize: Tuple[float, float] = (16.0, 4.0),
) -> None:
    """
    Render multi-view CDD publication suite.
    
    Args:
        cdd_file (str): Path to the CDD volumetric file (CHGCAR, cdd.vasp, .cube).
        output_dir (Optional[str]): Directory to save individual renders.
        views (Tuple[str, ...]): Iterable of view identifiers ('a', 'b', 'c', 'iso', 'edge-on').
        pos_level (float): Positive isosurface level for CDD rendering.
        neg_level (float): Negative isosurface level for CDD rendering.
        opacity (float): Opacity of the isosurfaces.
        scale (float): Scaling factor for the structural rendering.
        compose_panel (bool): Whether to compose all views into a single multi-panel publication figure.
        panel_output (Optional[str]): Path to save the composed multi-panel figure.
        figsize (Tuple[float, float]): Figure size for the composed matplotlib panel.
    """
    if style_config:
        style_config.set_publication_style()
    else:
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Times New Roman']

    cdd_path = Path(cdd_file).resolve()
    if not cdd_path.exists():
        raise FileNotFoundError(f"CDD file not found: {cdd_file}")

    if output_dir is None:
        out_dir_path = cdd_path.parent / "cdd_renders"
    else:
        out_dir_path = Path(output_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    rendered_images = {}
    
    # Define Euler rotations or coordinate permutations for views
    view_params = {
        'a': {'rotation': (0, 0, 0), 'label': 'View along a-axis'},
        'b': {'rotation': (90, 0, 0), 'label': 'View along b-axis'},
        'c': {'rotation': (0, 90, 0), 'label': 'View along c-axis'},
        'iso': {'rotation': (45, 35, 0), 'label': 'Isometric view'},
        'edge-on': {'rotation': (90, 90, 0), 'label': 'Edge-on view'}
    }

    for view in views:
        if view not in view_params:
            print(f"Warning: View {view} not supported. Skipping.")
            continue
            
        out_path = out_dir_path / f"{cdd_path.stem}_view_{view}.png"
        
        # Call vesta_cdd.render_cdd
        try:
            vesta_cdd.render_cdd(
                cdd_file=str(cdd_path),
                output_path=str(out_path),
                pos_isosurface=pos_level,
                neg_isosurface=neg_level,
                opacity=opacity,
                scale=scale,
                view_dir=view
            )
        except Exception as e:
            print(f"Error rendering {view}: {e}")
            continue

        if out_path.exists():
            dynamic_feature_crop(str(out_path))
            rendered_images[view] = str(out_path)

    if compose_panel and rendered_images:
        if panel_output is None:
            panel_out_path = cdd_path.parent / f"{cdd_path.stem}_panel.png"
        else:
            panel_out_path = Path(panel_output)
            
        n_views = len(rendered_images)
        fig, axes = plt.subplots(1, n_views, figsize=figsize)
        if n_views == 1:
            axes = [axes]
            
        for ax, (view, img_path) in zip(axes, rendered_images.items()):
            img = Image.open(img_path)
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(view_params[view]['label'], fontname='Times New Roman')
            
        plt.tight_layout()
        plt.savefig(str(panel_out_path), dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Panel saved to {panel_out_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-view CDD publication suite.")
    parser.add_argument("cdd_file", type=str, help="CDD volumetric file (CHGCAR, cdd.vasp, .cube)")
    parser.add_argument("--views", nargs='+', default=['a', 'b', 'c', 'iso'], help="Views to render (a, b, c, iso, edge-on)")
    parser.add_argument("--pos-level", type=float, default=0.005, help="Positive isosurface level")
    parser.add_argument("--neg-level", type=float, default=-0.005, help="Negative isosurface level")
    parser.add_argument("--opacity", type=float, default=0.60, help="Opacity")
    parser.add_argument("--scale", type=float, default=2.0, help="Scale factor")
    parser.add_argument("--compose", action="store_true", help="Compose views into a single panel")
    parser.add_argument("--output", type=str, default=None, help="Output file for panel")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory for individual views")

    args = parser.parse_args()

    render_cdd_suite(
        cdd_file=args.cdd_file,
        output_dir=args.output_dir,
        views=tuple(args.views),
        pos_level=args.pos_level,
        neg_level=args.neg_level,
        opacity=args.opacity,
        scale=args.scale,
        compose_panel=args.compose,
        panel_output=args.output
    )

if __name__ == "__main__":
    main()
