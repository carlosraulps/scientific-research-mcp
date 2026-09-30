---
name: latex-template
description: Production-grade LaTeX and Beamer template management, scaffolding, multi-pass XeLaTeX compilation with automatic auxiliary cleanup, PNG slide previews, and institutional UFABC grayscale branding. Use when creating scientific presentations (beamer), papers, theses, or registering new LaTeX templates.
---

# LaTeX & Beamer Template Skill (`latex-template` / `beamer-template`)

A modular system for creating, managing, and compiling publication-grade LaTeX documents and Beamer presentations with institutional branding and automatic build workflows.

## Features & Capabilities

1. **Nordic Beamer Presentation Theme (`beamer-nord`)**:
   - Modern Nordic palette (Polar Night dark mode & Snow Storm light mode).
   - High-contrast, transparent alpha-channel **UFABC grayscale insignia** in the bottom-right corner of the title slide:
     - `logo-ufabc-light.png`: High-luminance silver/frost monochrome optimized for dark themes (`#2E3440`).
     - `logo-ufabc-dark.png`: Deep charcoal slate monochrome optimized for light themes.
   - Rich typography with Libertinus math & fontspec, custom colored blocks (`block`, `alertblock`, `exampleblock`), two-column layouts, and mathematical macros (`\circled`, `siunitx`, `diffcoeff`).
2. **Instant Scaffolding**:
   - Generate complete presentation folders ready to compile with one command.
3. **Automated Multi-Pass Compiler & Aux Cleaner**:
   - Compiles with XeLaTeX (`xelatex -interaction=nonstopmode`).
   - Multi-pass resolution for table of contents, bookmarks, and cross-references.
   - Automatically purges `.aux`, `.log`, `.nav`, `.snm`, `.toc`, `.vrb`, `.out` files unless `--keep-aux` is requested.
4. **Slide Previewing**:
   - Headless PNG rendering of any slide using `pdftoppm`.
5. **Template Extensibility**:
   - Register any future LaTeX template (e.g., RevTeX articles, UFABC theses, posters) with `latex-template add`.

---

## Quick Reference CLI

Both `latex-template` and `beamer-template` are installed in `~/.local/bin/` (available system-wide in PATH):

### 1. Scaffold a New Presentation
```bash
# Dark theme (default)
beamer-template new my_talk \
  --title "Quantum Confinement in Halide Perovskites" \
  --author "Research Group" \
  --institute "Universidade Federal do ABC (UFABC)" \
  --compile

# Light theme
beamer-template new my_light_talk \
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
