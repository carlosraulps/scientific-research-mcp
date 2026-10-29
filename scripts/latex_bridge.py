#!/usr/bin/env python3
"""
Bridge for LaTeX & Beamer Template Management in SciResearch.
Provides programmatic access to template scaffolding, compilation (XeLaTeX / pdfLaTeX),
automatic Biber bibliography resolution, and PNG previews.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
LATEX_SKILL_DIR = BASE_DIR / "skills" / "latex-template"
LATEX_SCRIPTS_DIR = LATEX_SKILL_DIR / "scripts"

if str(LATEX_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(LATEX_SCRIPTS_DIR))

import latex_manager as lm


class LaTeXBridge:
    """Manages LaTeX document templates, scaffolding, compilation, and rendering."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = Path(base_dir) if base_dir else BASE_DIR
        self.templates_dir = LATEX_SKILL_DIR / "templates"

    def list_templates(self) -> Dict[str, Any]:
        """Lists all registered LaTeX document and presentation templates."""
        catalog = lm.load_catalog()
        return {
            "templates": catalog,
            "count": len(catalog)
        }

    def scaffold_report(
        self,
        destination: str,
        template: str = "latex-report",
        title: Optional[str] = None,
        author: Optional[str] = None,
        institute: Optional[str] = None,
        doctype: str = "Experimental Lab Report",
        compile_pdf: bool = False,
        force: bool = False
    ) -> Dict[str, Any]:
        """Scaffolds a new experimental report or paper from a template."""
        dest_path = Path(destination).resolve()
        
        args = type("Args", (), {
            "destination": str(dest_path),
            "template": template,
            "title": title or "Investigation of Electronic Structure and Transport in Novel 2D Allotropes",
            "author": author or "Research Group",
            "institute": institute or "Universidade Federal do ABC (UFABC)",
            "doctype": doctype,
            "theme": "dark",
            "subtitle": "",
            "project": "",
            "logo": None,
            "compile": compile_pdf,
            "force": force
        })()

        try:
            lm.new_project(args)
            
            created_files = [str(p.relative_to(dest_path)) for p in dest_path.rglob("*") if p.is_file()]
            target_tex = dest_path / ("template.tex" if (dest_path / "template.tex").exists() else "main.tex")
            target_pdf = dest_path / f"{target_tex.stem}.pdf"

            res = {
                "success": True,
                "destination": str(dest_path),
                "template": template,
                "starter_file": str(target_tex),
                "files_created": created_files,
                "compiled": compile_pdf and target_pdf.exists(),
                "pdf_path": str(target_pdf) if target_pdf.exists() else None
            }
            return res
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "destination": str(dest_path)
            }

    def compile_document(
        self,
        tex_path: str,
        compiler: Optional[str] = None,
        passes: Optional[int] = None,
        clean_aux: bool = True,
        preview: bool = False
    ) -> Dict[str, Any]:
        """Compiles a .tex file with automatic multi-pass, Biber resolution, and aux pruning."""
        path = Path(tex_path).resolve()
        if not path.exists():
            return {"success": False, "error": f"File not found: {tex_path}"}

        args = type("Args", (), {
            "file": str(path),
            "compiler": compiler,
            "passes": passes,
            "clean": clean_aux,
            "preview": preview
        })()

        try:
            lm.compile_file(args)
            pdf_path = path.parent / f"{path.stem}.pdf"
            if pdf_path.exists():
                preview_png = path.parent / f"{path.stem}_preview-1.png"
                return {
                    "success": True,
                    "pdf_path": str(pdf_path),
                    "size_kb": round(pdf_path.stat().st_size / 1024, 1),
                    "preview_png": str(preview_png) if preview_png.exists() else None
                }
            else:
                return {"success": False, "error": "PDF was not generated."}
        except SystemExit as se:
            return {"success": False, "error": f"Compilation terminated with exit code {se.code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def preview_document(
        self,
        tex_path: str,
        page: int = 1,
        dpi: int = 150
    ) -> Dict[str, Any]:
        """Renders a specific page of a compiled LaTeX document as a high-resolution PNG."""
        path = Path(tex_path).resolve()
        args = type("Args", (), {
            "file": str(path),
            "page": page,
            "dpi": dpi
        })()

        try:
            lm.preview_file(args)
            generated = list(path.parent.glob(f"{path.stem}_page{page}*.png"))
            if generated:
                return {
                    "success": True,
                    "page": page,
                    "dpi": dpi,
                    "preview_image": str(generated[0])
                }
            return {"success": False, "error": f"Preview image for page {page} not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
