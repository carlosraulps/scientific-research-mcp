---
name: publication-figure-formatter
description: Use when creating, styling, or formatting publication-ready scientific figures, plots, or diagrams with Times New Roman typography, STIX math equations, and collision-free label placement using adjustText or textalloc.
---

# Publication Figure Formatter Skill

## Overview
Standards and automated toolchain for generating publication-grade scientific graphics matching Physical Review, Nature, and ACS quality benchmarks. Mandates Times New Roman serif typography, native STIX math font rendering, zero text overlap via algorithmic placement (`adjustText` force-repulsion and `textalloc` bounding-box allocation), and automated dual raster/vector (`.png` and `.pdf`) export.

## When to Use
- **Trigger**: Creating scientific plots, band structures, DOS curves, reaction energy coordinates, or phase diagrams.
- **Trigger**: Crowded scatter plots or multi-line graphs where annotations/labels overlap or collide.
- **Trigger**: Preparing final graphics for journal submission requiring Times New Roman fonts and vector PDF formats.
- **When NOT to use**:
  - Headless 3D crystal rendering (use [blender-crystal-render](../blender-crystal-render/SKILL.md) or [ovito-snapshot](../ovito-snapshot/SKILL.md)).
  - Real-space 3D electron density isosurfaces (use [electron-density-surfaces](../electron-density-surfaces/SKILL.md)).

## Quick Reference

| Action | Python / CLI Pattern |
| :--- | :--- |
| **Apply Standard Styling** | `from style_config import set_publication_style; set_publication_style()` |
| **Anti-Collision (`adjustText`)** | `auto_adjust_labels(ax, x, y, labels, engine="adjustText")` |
| **Anti-Collision (`textalloc`)** | `auto_adjust_labels(ax, x, y, labels, engine="textalloc")` |
| **Dual PDF & PNG Export** | `save_publication_figure(fig, "figures/reaction_profile")` |
| **Direct CLI Format** | `format-figure data.csv -o ./fig --engine adjustText --xlabel "$E - E_{\mathrm{F}}\ \mathrm{(eV)}$"` |

## Core Principles & Typography

### 1. Typography & Mathematical Formats
- Always configure standard serif fonts with cross-platform fallbacks:
  ```python
  plt.rcParams.update({
      "font.family": "serif",
      "font.serif": ["Times New Roman", "Nimbus Roman", "Liberation Serif", "STIXGeneral", "DejaVu Serif"],
      "mathtext.fontset": "stix",
      "axes.edgecolor": "#222222",
      "axes.linewidth": 1.2,
      "xtick.direction": "in",
      "ytick.direction": "in",
  })
  ```
- **Math strings**: Always use raw LaTeX strings with explicit units:
  - $r"$\Delta G_{\mathrm{H*}}\ \mathrm{(eV)}$"$
  - $r"$\rho(\mathbf{r})\ \mathrm{(e/Å^3)}$"$
  - $r"$\mathrm{Total\ Energy}\ E - E_0\ \mathrm{(meV/atom)}$"$

### 2. Label Anti-Collision Engines

This skill embeds two state-of-the-art layout algorithms (cloned in `external/`):
- **`adjustText`** (`external/adjustText`): Uses iterative force-directed physics simulation to repel text boxes away from data points, lines, and adjacent labels, with automatic leader lines.
- **`textalloc`** (`external/textalloc`): Uses bounding-box candidate sampling and spatial partitioning to locate optimal empty voids around crowded scatter clusters.

### 3. Python Integration Pattern
```python
import matplotlib.pyplot as plt
from style_config import set_publication_style, auto_adjust_labels, save_publication_figure

set_publication_style()
fig, ax = plt.subplots(figsize=(6.5, 5))

ax.scatter(x_data, y_data, color="#1f77b4", s=40)
auto_adjust_labels(ax, x_data, y_data, labels, engine="adjustText", text_size=10)

ax.set_xlabel(r"Reaction Coordinate $\xi$", fontsize=12)
ax.set_ylabel(r"Gibbs Free Energy $\Delta G\ \mathrm{(eV)}$", fontsize=12)

save_publication_figure(fig, "figures/energy_landscape")
```

### 4. Colorblind Accessibility & Colormaps
- **Rule**: Avoid arbitrary color assignments, Rainbow, and Jet.
- **Continuous 2D Colormaps**:
  - Sequential: `cividis` (optimized for color vision deficiencies), `viridis`, `plasma`, `inferno`.
  - Diverging: `coolwarm`, `RdBu_r`, `PRGn`.
- **Categorical Data**:
  - Use the **Okabe-Ito** palette (`OKABE_ITO_LIST`) or Paul Tol's palettes (`TOL_BRIGHT`, `TOL_MUTED`) available in `style_config`.

### 5. VESTA Element Color Concordance
In solid-state physics and computational materials science, element-projected DOS (PDOS), orbital fat bands, and atomic defect levels should strictly match the color of the atoms in the crystal structure figure:
```python
from style_config import get_vesta_color, get_element_cycler

# Exact colors from /opt/VESTA/elements.ini:
ax.plot(energies, pdos_Ti, color=get_vesta_color("Ti"), label="Ti $3d$ (VESTA Sky Blue)")
ax.plot(energies, pdos_O,  color=get_vesta_color("O"),  label="O $2p$ (VESTA Red)")
ax.plot(energies, pdos_Sr, color=get_vesta_color("Sr"), label="Sr $4d$ (VESTA Green)")
```

## Common Pitfalls & Solutions

1. **LaTeX syntax error**: Do not escape math without raw strings. Always prefix with `r"..."`.
2. **Text truncated at figure margins**: Set `bbox_inches='tight'` or call `plt.tight_layout()`. `save_publication_figure` enforces this automatically.
3. **Labels outside plot bounds**: Pass `lim=500` or specify axes bounds in `adjust_text(..., ax=ax)`.
4. **Color mismatch across paper figures**: Import `get_vesta_color` so PDOS, fat bands, and scatter legends match VESTA crystal structure figures 100%.
