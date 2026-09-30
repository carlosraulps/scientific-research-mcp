#!/usr/bin/env python3
"""
LaTeX & Beamer Template Manager & Scaffolder
Supports quick presentation scaffolding, template registration, multi-pass XeLaTeX/pdfLaTeX
compilation, auxiliary file pruning, and PNG preview rendering.
"""

import sys
import os
import shutil
import argparse
import subprocess
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_CATALOG_FILE = SKILL_DIR / "templates" / "templates.json"
DEFAULT_BEAMER_THEME_DIR = SKILL_DIR / "beamer-theme"

def load_catalog():
    if TEMPLATES_CATALOG_FILE.exists():
        try:
            with open(TEMPLATES_CATALOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Default fallback catalog
    return {
        "beamer-nord": {
            "name": "beamer-nord",
            "description": "Nordic Beamer presentation theme (sthlmNord) with UFABC grayscale branding, dark/light modes, and math macros",
            "type": "beamer",
            "compiler": "xelatex",
            "path": str(DEFAULT_BEAMER_THEME_DIR),
            "starter": "demo_ufabc_presentation.tex"
        }
    }

def save_catalog(catalog):
    TEMPLATES_CATALOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TEMPLATES_CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

def list_templates(args):
    catalog = load_catalog()
    print("\n📦 Registered LaTeX / Beamer Templates:")
    print("=" * 70)
    for key, data in catalog.items():
        print(f"  • \033[1;36m{key}\033[0m ({data.get('type', 'general')}) [Compiler: {data.get('compiler', 'xelatex')}]")
        print(f"    Description: {data.get('description', 'No description')}")
        print(f"    Source Path: {data.get('path', 'Unknown')}\n")
    print("=" * 70)

def add_template(args):
    src = Path(args.path).resolve()
    if not src.exists():
        print(f"❌ Error: Source directory does not exist: {src}")
        sys.exit(1)
    
    catalog = load_catalog()
    name = args.name.strip().lower()
    dest_dir = SKILL_DIR / "templates" / name

    if dest_dir.exists() and not args.force:
        print(f"❌ Error: Template '{name}' already exists in registry. Use --force to overwrite.")
        sys.exit(1)

    print(f"📂 Registering template '{name}' from {src}...")
    shutil.copytree(src, dest_dir, dirs_exist_ok=True)

    catalog[name] = {
        "name": name,
        "description": args.desc or f"Custom {name} template",
        "type": args.type,
        "compiler": args.compiler,
        "path": str(dest_dir),
        "starter": args.starter or ("main.tex" if (dest_dir / "main.tex").exists() else "template.tex")
    }
    save_catalog(catalog)
    print(f"✅ Template '{name}' registered successfully.")

def new_project(args):
    catalog = load_catalog()
    template_name = getattr(args, "template", "beamer-nord")
    
    if template_name not in catalog:
        print(f"❌ Error: Template '{template_name}' not found. Available: {list(catalog.keys())}")
        sys.exit(1)

    tmpl_info = catalog[template_name]
    src_dir = Path(tmpl_info["path"])
    out_dir = Path(args.destination).resolve()

    if out_dir.exists() and any(out_dir.iterdir()) and not args.force:
        print(f"❌ Error: Target directory '{out_dir}' exists and is not empty. Use --force to proceed.")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"🚀 Scaffolding new presentation in: {out_dir}")

    # Files to copy for beamer-nord
    if template_name == "beamer-nord":
        # Copy core style files and assets
        for sty in src_dir.glob("*.sty"):
            shutil.copy2(sty, out_dir / sty.name)
        if (src_dir / "mhoRef.bib").exists():
            shutil.copy2(src_dir / "mhoRef.bib", out_dir / "mhoRef.bib")

        # Copy assets directory (including UFABC logos)
        assets_src = src_dir / "assets"
        assets_dst = out_dir / "assets"
        if assets_src.exists():
            shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)

        mode = getattr(args, "theme", "dark")
        title = getattr(args, "title", "Computational Materials Physics & DFT")
        subtitle = getattr(args, "subtitle", "Research Progress and Electronic Structure Modeling")
        author = getattr(args, "author", "Research Group")
        institute = getattr(args, "institute", "Universidade Federal do ABC (UFABC)")
        project = getattr(args, "project", "Advanced Ab Initio Simulations")
        
        # Choose logo variant based on mode
        logo = "logo-ufabc-light" if mode == "dark" else "logo-ufabc-dark"
        if getattr(args, "logo", None):
            logo = args.logo

        theme_mode_str = "\\usetheme{sthlmnord}" if mode == "dark" else "\\usetheme[mode=light]{sthlmnord}"

        main_tex_content = f"""\\documentclass[aspectratio=169, sectionpages, codemintedoverleaf, bibref]{{beamer}}

% Bibliography File
\\newcommand{{\\bibfilename}}{{mhoRef.bib}}

% Choose Theme: {mode.capitalize()} mode
{theme_mode_str}

\\usepackage{{lipsum}}

% Image File Paths
\\graphicspath{{{{./assets/}},{{./images/}}}}

% Document Information
\\title{{{title}}}
\\subtitle{{{subtitle}}}
\\newcommand{{\\titleAuthor}}{{Presenter}}
\\author{{{author}}}
\\newcommand{{\\titleInstitute}}{{Institution}}
\\institute{{{institute}}}
\\newcommand{{\\titleMiscI}}{{Project}}
\\newcommand{{\\descMiscI}}{{{project}}}
\\newcommand{{\\titleMiscII}}{{Date}}
\\newcommand{{\\descMiscII}}{{\\today}}
\\date{{\\today}}

% Grayscale High-Contrast Logo for {mode.capitalize()} Theme
\\titlegraphic{{{logo}}}

\\hypersetup{{
  colorlinks=false,
  linkcolor={{nordNine}},
  citecolor={{nordNine}},
  urlcolor={{nordNine}}
}}

\\begin{{document}}

% Title Slide
\\titlepage

% Table of Contents
\\begin{{frame}}{{Outline}}
  \\tableofcontents
\\end{{frame}}

\\section{{Introduction and Methodology}}

\\begin{{frame}}{{Density Functional Theory and Materials Simulation}}
  \\begin{{columns}}[T]
    \\begin{{column}}{{0.48\\textwidth}}
      \\begin{{block}}{{Kohn-Sham Equations}}
        Self-consistent single-particle formulation:
        \\[
          \\left[ -\\frac{{1}}{{2}}\\nabla^2 + V_{{\\text{{ext}}}}(\\mathbf{{r}}) + V_{{\\text{{H}}}}(\\mathbf{{r}}) + V_{{\\text{{xc}}}}(\\mathbf{{r}}) \\right] \\psi_i(\\mathbf{{r}}) = \\varepsilon_i \\psi_i(\\mathbf{{r}})
        \\]
      \\end{{block}}
      \\begin{{itemize}}
        \\item Projected Augmented Wave (PAW) method
        \\item Generalized Gradient Approximation (PBE)
        \\item On-site Coulomb interaction (+U)
      \\end{{itemize}}
    \\end{{column}}

    \\begin{{column}}{{0.48\\textwidth}}
      \\begin{{exampleblock}}{{Simulation Protocol}}
        \\begin{{itemize}}
          \\item Geometry relaxation ($F_{{\\text{{max}}}} < 0.01\\,\\text{{eV/\\AA}}$)
          \\item Electronic convergence ($10^{{-6}}\\,\\text{{eV}}$)
          \\item Micro-batch Slurm execution on HPC clusters
        \\end{{itemize}}
      \\end{{exampleblock}}
      \\vspace{{1em}}
      \\centering
      {{\\small \\textcolor{{nordEight}}{{\\textbf{{{institute}}}}}}}
    \\end{{column}}
  \\end{{columns}}
\\end{{frame}}

\\section{{Summary and Outlook}}

\\begin{{frame}}{{Conclusions and Outlook}}
  \\begin{{alertblock}}{{Key Milestones}}
    \\begin{{itemize}}
      \\item Integrated custom Nord Beamer theme with UFABC insignia.
      \\item High-contrast grayscale vector-aligned branding on title slide.
      \\item Ready for conference presentations, seminars, and defenses.
    \\end{{itemize}}
  \\end{{alertblock}}
  \\vfill
  \\centering
  {{\\Large \\textbf{{\\textcolor{{nordEight}}{{Thank you for your attention!}}}}}}\\\\[1em]
  {{\\small Questions and Discussion}}
\\end{{frame}}

\\end{{document}}
"""
        target_tex = out_dir / "presentation.tex"
        with open(target_tex, "w", encoding="utf-8") as f:
            f.write(main_tex_content)
        print(f"📝 Created starter presentation: {target_tex}")

    else:
        # Generic copy of template
        for item in src_dir.iterdir():
            if item.name.startswith("."):
                continue
            if item.is_dir():
                shutil.copytree(item, out_dir / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, out_dir / item.name)
        target_tex = out_dir / tmpl_info.get("starter", "template.tex")

    print(f"✨ Scaffold complete!")
    print(f"👉 To compile, run:")
    print(f"   beamer-template compile {target_tex.name} (inside {out_dir})")
    
    if args.compile:
        compile_file(argparse.Namespace(
            file=str(target_tex),
            compiler=tmpl_info.get("compiler", "xelatex"),
            clean=True,
            preview=False
        ))

def clean_auxiliary(tex_path):
    tex_path = Path(tex_path).resolve()
    stem = tex_path.stem
    parent = tex_path.parent
    extensions = [".aux", ".bbl", ".blg", ".log", ".nav", ".out", ".snm", ".toc", ".vrb", ".run.xml", "-blx.bib"]
    deleted = 0
    for ext in extensions:
        aux_file = parent / f"{stem}{ext}"
        if aux_file.exists():
            aux_file.unlink()
            deleted += 1
    return deleted

def compile_file(args):
    tex_path = Path(args.file).resolve()
    if not tex_path.exists():
        print(f"❌ Error: File not found: {tex_path}")
        sys.exit(1)

    workdir = tex_path.parent
    compiler = getattr(args, "compiler", "xelatex")
    passes = getattr(args, "passes", 2)
    clean = getattr(args, "clean", True)
    preview = getattr(args, "preview", False)

    print(f"⚙️  Compiling {tex_path.name} with {compiler} ({passes} passes)...")
    
    for p in range(1, passes + 1):
        cmd = [compiler, "-interaction=nonstopmode", tex_path.name]
        res = subprocess.run(cmd, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if res.returncode != 0:
            print(f"❌ Compilation failed at pass {p}:")
            lines = res.stdout.splitlines()
            for line in lines[-25:]:
                print(f"   {line}")
            sys.exit(res.returncode)
        print(f"   ✓ Pass {p}/{passes} successful")

    pdf_file = workdir / f"{tex_path.stem}.pdf"
    if pdf_file.exists():
        pdf_size_kb = pdf_file.stat().st_size / 1024
        print(f"🎉 Build Succeeded: {pdf_file} ({pdf_size_kb:.1f} KB)")
        
        if clean:
            n_cleaned = clean_auxiliary(tex_path)
            print(f"🧹 Cleaned {n_cleaned} auxiliary files.")

        if preview:
            preview_png = workdir / f"{tex_path.stem}_preview"
            cmd_preview = ["pdftoppm", "-png", "-r", "150", "-f", "1", "-l", "1", str(pdf_file), str(preview_png)]
            subprocess.run(cmd_preview, check=True)
            print(f"🖼️ Title slide preview generated: {preview_png}-1.png")
    else:
        print("❌ Warning: PDF file was not created.")

def preview_file(args):
    tex_path = Path(args.file).resolve()
    pdf_file = tex_path.parent / f"{tex_path.stem}.pdf"
    if not pdf_file.exists():
        print(f"Compiling {tex_path} first...")
        compile_file(argparse.Namespace(
            file=str(tex_path),
            compiler=getattr(args, "compiler", "xelatex"),
            passes=2,
            clean=True,
            preview=False
        ))
    
    page = getattr(args, "page", 1)
    dpi = getattr(args, "dpi", 150)
    out_prefix = tex_path.parent / f"{tex_path.stem}_page{page}"
    cmd = ["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page), str(pdf_file), str(out_prefix)]
    subprocess.run(cmd, check=True)
    generated = list(tex_path.parent.glob(f"{out_prefix.name}*.png"))
    if generated:
        print(f"🖼️ Preview rendered: {generated[0]}")
    else:
        print("❌ Failed to render preview image.")

def main():
    parser = argparse.ArgumentParser(
        description="LaTeX & Beamer Template Manager (beamer-template / latex-template)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: list
    parser_list = subparsers.add_parser("list", help="List registered templates")
    parser_list.set_defaults(func=list_templates)

    # Subcommand: add
    parser_add = subparsers.add_parser("add", help="Register a new template")
    parser_add.add_argument("name", help="Template name (e.g., revtex-article, thesis-ufabc)")
    parser_add.add_argument("path", help="Directory path containing the template")
    parser_add.add_argument("--desc", help="Short description of the template")
    parser_add.add_argument("--type", default="article", choices=["beamer", "article", "thesis", "poster", "letter"])
    parser_add.add_argument("--compiler", default="xelatex", choices=["xelatex", "pdflatex", "lualatex"])
    parser_add.add_argument("--starter", help="Main starter .tex file name")
    parser_add.add_argument("--force", action="store_true", help="Overwrite existing template in registry")
    parser_add.set_defaults(func=add_template)

    # Subcommand: new
    parser_new = subparsers.add_parser("new", help="Scaffold a new project from a template")
    parser_new.add_argument("destination", help="Target project directory")
    parser_new.add_argument("--template", default="beamer-nord", help="Template name to use")
    parser_new.add_argument("--theme", choices=["dark", "light"], default="dark", help="Color theme (for beamer-nord)")
    parser_new.add_argument("--title", default="Computational Materials Physics & DFT", help="Presentation / document title")
    parser_new.add_argument("--subtitle", default="Research Progress and Electronic Structure Modeling", help="Subtitle")
    parser_new.add_argument("--author", default="Research Group", help="Author name")
    parser_new.add_argument("--institute", default="Universidade Federal do ABC (UFABC)", help="Institute name")
    parser_new.add_argument("--project", default="Advanced Ab Initio Simulations", help="Course or project name")
    parser_new.add_argument("--logo", help="Custom logo graphic name or path")
    parser_new.add_argument("--compile", action="store_true", help="Compile immediately after scaffolding")
    parser_new.add_argument("--force", action="store_true", help="Overwrite existing destination directory")
    parser_new.set_defaults(func=new_project)

    # Subcommand: compile
    parser_compile = subparsers.add_parser("compile", help="Compile a .tex file with automatic multi-pass and cleanup")
    parser_compile.add_argument("file", help="Path to .tex file")
    parser_compile.add_argument("--compiler", default="xelatex", choices=["xelatex", "pdflatex", "lualatex"])
    parser_compile.add_argument("--passes", type=int, default=2, help="Number of compilation passes")
    parser_compile.add_argument("--keep-aux", dest="clean", action="store_false", help="Keep auxiliary files (.aux, .toc, etc.)")
    parser_compile.add_argument("--preview", action="store_true", help="Also generate PNG preview of title slide")
    parser_compile.set_defaults(func=compile_file)

    # Subcommand: preview
    parser_preview = subparsers.add_parser("preview", help="Render a page of a compiled presentation to PNG")
    parser_preview.add_argument("file", help="Path to .tex file")
    parser_preview.add_argument("--page", type=int, default=1, help="Page number to render (default: 1)")
    parser_preview.add_argument("--dpi", type=int, default=150, help="Resolution DPI (default: 150)")
    parser_preview.set_defaults(func=preview_file)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
