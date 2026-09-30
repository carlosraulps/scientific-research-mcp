#!/usr/bin/env python3
"""
================================================================================
High-Throughput VESTA Batch Renderer & Publication Gallery Generator
================================================================================
Iterates across directories of crystal structures (POSCAR, CONTCAR, CIF, XSF),
renders offscreen high-resolution projections with strict primitive cell containment
('Bound = 0'), trims whitespace borders, and builds an interactive HTML/Markdown gallery.
================================================================================
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Union

# Add current script directory for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vesta_auto import run_vesta_pipeline


def batch_render_directory(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path] = "./vesta_gallery",
    pattern: str = "POSCAR*",
    view: str = "c",
    scale: int = 2,
    isolate_cell: bool = True,
    generate_gallery: bool = True,
) -> List[str]:
    """
    Renders all matching crystal structures in input_dir and builds a summary gallery.
    """
    in_dir = Path(input_dir).resolve()
    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(list(in_dir.glob(pattern)))
    if not files:
        # Also check common crystal extensions if pattern had no hits
        for ext in ["*.cif", "*.vasp", "*.xsf", "CONTCAR*"]:
            files.extend(sorted(list(in_dir.glob(ext))))

    if not files:
        print(f"[VESTA Batch] No matching structure files found in {in_dir}", file=sys.stderr)
        return []

    print(f"[VESTA Batch] Found {len(files)} structures to render in: {in_dir}")
    rendered_summary = []

    for idx, fpath in enumerate(files, start=1):
        if not fpath.is_file():
            continue
        print(f"[{idx}/{len(files)}] Processing: {fpath.name}")
        try:
            imgs = run_vesta_pipeline(
                input_file=fpath,
                view=view,
                output_dir=out_dir,
                output_prefix=fpath.stem,
                scale=scale,
                isolate_cell=isolate_cell,
            )
            if imgs:
                rendered_summary.append({
                    "structure": fpath.name,
                    "images": [Path(im).name for im in imgs],
                })
        except Exception as e:
            print(f"[VESTA Batch] Error rendering {fpath.name}: {e}", file=sys.stderr)

    # Build Markdown and HTML Gallery Index
    if generate_gallery and rendered_summary:
        md_path = out_dir / "GALLERY.md"
        html_path = out_dir / "index.html"

        # Write Markdown
        md_lines = [
            f"# Crystal Structure Visualization Gallery",
            f"**Total Structures**: {len(rendered_summary)} | **View**: {view} | **Engine**: VESTA CLI (Bound=0)\n",
            "| Structure | Snapshot |",
            "| :--- | :--- |",
        ]
        for item in rendered_summary:
            img_links = " ".join([f"![{im}]({im})" for im in item["images"]])
            md_lines.append(f"| **{item['structure']}** | {img_links} |")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines) + "\n")

        # Write HTML
        html_lines = [
            "<!DOCTYPE html>",
            "<html><head><meta charset='utf-8'><title>Crystal Visualization Gallery</title>",
            "<style>",
            "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #fdfdfd; color: #222; }",
            "h1 { border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }",
            ".gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 24px; margin-top: 25px; }",
            ".card { border: 1px solid #e1e4e8; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }",
            ".card-header { padding: 12px 16px; font-weight: 600; background: #f6f8fa; border-bottom: 1px solid #e1e4e8; }",
            ".card img { width: 100%; display: block; border-bottom: 1px solid #eee; }",
            "</style></head><body>",
            f"<h1>Crystal Structure Visualization Gallery</h1>",
            f"<p>Automated High-Throughput Batch Run — <strong>{len(rendered_summary)}</strong> structures processed.</p>",
            "<div class='gallery-grid'>",
        ]
        for item in rendered_summary:
            for im in item["images"]:
                html_lines.append(f"<div class='card'><div class='card-header'>{item['structure']} ({im})</div><img src='{im}' alt='{item['structure']}'></div>")
        html_lines.extend(["</div></body></html>"])

        with open(html_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html_lines) + "\n")

        print(f"[VESTA Batch] Generated HTML gallery: {html_path}")
        print(f"[VESTA Batch] Generated Markdown index: {md_path}")

    return [item["structure"] for item in rendered_summary]


def main():
    parser = argparse.ArgumentParser(
        description="High-Throughput VESTA Batch Renderer & Publication Gallery Generator."
    )
    parser.add_argument("input_dir", help="Directory containing crystal structure files")
    parser.add_argument("--output-dir", "-o", default="./vesta_gallery", help="Destination gallery directory")
    parser.add_argument("--pattern", "-p", default="POSCAR*", help="Glob pattern for structure files (default: POSCAR*)")
    parser.add_argument("--view", "-v", choices=["a", "b", "c", "iso", "all"], default="c", help="Orientation view (default: c)")
    parser.add_argument("--scale", "-s", type=int, default=2, help="Resolution multiplier (default: 2)")
    parser.add_argument("--no-isolate", action="store_true", help="Disable automatic Bound=0 unit cell containment")
    parser.add_argument("--no-gallery", action="store_true", help="Do not generate HTML/Markdown gallery files")

    args = parser.parse_args()
    batch_render_directory(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        pattern=args.pattern,
        view=args.view,
        scale=args.scale,
        isolate_cell=not args.no_isolate,
        generate_gallery=not args.no_gallery,
    )


if __name__ == "__main__":
    main()
