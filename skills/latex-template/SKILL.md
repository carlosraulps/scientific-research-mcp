---
name: latex-template
description: Production-grade LaTeX and Beamer template management, scaffolding, multi-pass XeLaTeX compilation with automatic auxiliary cleanup, PNG slide previews, and institutional UFABC grayscale branding. Use when creating scientific presentations (beamer), papers, theses, or registering new LaTeX templates.
---

# LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`)

A modular system for creating, managing, and compiling publication-grade LaTeX documents and Beamer presentations with institutional branding and automatic build workflows.

## Features & Capabilities

1. **Experimental Lab Report & Article Template (`latex-report`)**:
   - Two-column layout based on **Tau-class (v2.6.0)**.
   - Elegant typography with **STIX2** (serif math and body), **Fira Sans** (headings, labels, tables), and **Fira Mono** (code).
   - Custom callout environments (`\begin{info}`, `\begin{note}`, `\begin{tauenv}`) with subtle rounded borders and modern color themes.
   - Superior code listings supporting both `minted` (Pygments syntax highlighting) and `listings`.
   - Built-in `biblatex` IEEE bibliography with automatic `biber` backend resolution.
   - Ready for DFT calculations, MD simulations, materials synthesis, and experimental physics/chemistry documentation.

2. **Nordic Beamer Presentation Theme (`beamer-nord`)**:
   - Modern Nordic palette (Polar Night dark mode & Snow Storm light mode).
   - High-contrast, transparent alpha-channel **UFABC grayscale insignia** in the bottom-right corner of the title slide.
   - Rich typography with Libertinus math & fontspec, custom colored blocks, two-column layouts, and mathematical macros.

3. **Instant Scaffolding & Multi-Pass Build Automation**:
   - Scaffold presentations or lab reports with a single command.
   - Automatic compiler selection (XeLaTeX for Beamer presentations, pdfLaTeX for Tau reports).
   - Multi-pass build pipeline with automatic Biber execution and auxiliary file cleanup (`.aux`, `.bbl`, `.bcf`, `.blg`, `.log`, `.toc`, etc.).
   - Headless PNG slide / document preview generation using `pdftoppm`.

---

## Quick Reference CLI

Both `latex-template` and `beamer-template` are installed in `~/.local/bin/` (available system-wide in PATH):

### 1. Scaffold a New Document or Presentation
```bash
# Experimental Lab Report (Tau-class, default)
latex-template new my_lab_report \
  --template latex-report \
  --title "Transport Dynamics in 2D Phosphorene" \
  --author "Research Group" \
  --institute "Universidade Federal do ABC (UFABC)" \
  --doctype "Experimental Lab Report" \
  --compile

# Or via the unified SciResearch CLI:
sciresearch latex-report scaffold my_lab_report --title "2D Materials" --compile

# Nordic Beamer Presentation (dark mode, default)
beamer-template new my_talk \
  --template beamer-nord \
  --title "Quantum Confinement in Halide Perovskites" \
  --author "Research Group" \
  --institute "Universidade Federal do ABC (UFABC)" \
  --compile

# Light theme presentation
beamer-template new my_light_talk \
  --template beamer-nord \
  --theme light \
  --title "Electronic Structure Methods" \
  --compile
```

### 2. Compile an Existing Document
```bash
# Multi-pass compile with automatic auxiliary cleanup
beamer-template compile presentation.tex

# Keep auxiliary files for debugging
beamer-template compile presentation.tex --keep-aux

# Compile and immediately render PNG preview of page 1
beamer-template compile presentation.tex --preview
```

### 3. Generate PNG Previews
```bash
# Render title slide (page 1) to PNG
beamer-template preview presentation.tex --page 1 --dpi 150

# Render content slide (e.g. page 3)
beamer-template preview presentation.tex --page 3
```

### 4. Manage Templates Catalog
```bash
# List all registered templates
latex-template list

# Register a new custom template directory for future use
latex-template add revtex-article /path/to/revtex/template --type article --desc "Physical Review B two-column article"
latex-template add ufabc-thesis /path/to/thesis/template --type thesis --desc "UFABC Master/PhD Thesis Dissertation template"
```

---

## Directory Architecture

```
skills/latex-template/
├── SKILL.md                          # Global skill instructions
├── scripts/
│   └── latex_manager.py              # CLI tool engine (symlinked to beamer-template & latex-template)
├── beamer-theme/                     # Nordic Beamer Theme (sthlmNord)
│   ├── beamerthemesthlmnord.sty      # Theme core definitions & title slide layout
│   ├── mhocolorthemenord.sty         # Nord color definitions
│   ├── mhomacros.sty                 # Math, units, and font macros
│   ├── mhotables.sty                 # Tabularray & table styles
│   ├── assets/                       # Image assets and institutional logos
│   │   ├── logo-ufabc-light.png      # Silver/frost UFABC insignia (for dark mode)
│   │   ├── logo-ufabc-dark.png       # Charcoal UFABC insignia (for light mode)
│   │   ├── logo-ufabc.png            # Standard grayscale transparent logo
│   │   └── nordtitlelogolight.pdf    # Default theme emblem
│   ├── demo_ufabc_presentation.tex   # Fully configured starter demo
│   └── template.tex                  # Minimal blank template
├── templates/
│   └── templates.json                # Template catalog registry
└── examples/
    └── test_presentation/            # Pre-scaffolded sample presentation
```

---

## TeX System Dependencies

The system is configured with:
- **Engine**: XeLaTeX (`/usr/bin/xelatex`)
- **Core TeX Live**: `texlive-basic`, `texlive-latex`, `texlive-xetex`, `texlive-pictures`, `texlive-fontsextra`
- **User TeX Tree (`~/texmf`)**: `siunitx`, `diffcoeff`, and scientific macros
- **Auxiliary Tools**: `pdftoppm` (Poppler) for headless PNG slide previews
