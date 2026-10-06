---
name: publication-figure-formatter
description: Use when creating, styling, or formatting publication-ready scientific figures, plots, or diagrams with Times New Roman typography, STIX math equations, and collision-free label placement using adjustText or textalloc.
---

# Publication Figure Formatter Skill

## Overview
Standards and automated toolchain for generating publication-grade scientific graphics matching Physical Review, Nature, and ACS quality benchmarks. Mandates Times New Roman serif typography, native STIX math font rendering, zero text overlap via algorithmic placement (`adjustText` and `textalloc`), coupled Band Structure + PDOS architectures, and the Zero-Dilation Rule for scientific animations.

## Key Capabilities & Scientific Protocols

### 1. The Zero-Dilation Rule for Scientific Animations (`format-animation`)
- **Problem**: When creating multi-frame animated GIFs ($0\% \to +3\% \to 0\% \to -3\% \to 0\%$), **NEVER USE `bbox_inches="tight"`** in loop saves. Text string fluctuations (e.g. $+0.027$ vs $-0.014$) cause bounding boxes to vary by 2–10 pixels between frames, creating an unsettling visual "dilation" or frame jitter.
- **Protocol**:
  1. Fix the figure canvas explicitly: `figsize=(W, H), dpi=DPI`.
  2. Set explicit margins in `gridspec.GridSpec(left=0.06, right=0.94, top=0.81, bottom=0.12)`.
  3. Save directly without `bbox_inches="tight"`: `fig.savefig(buf, format="png", dpi=DPI)`.
  4. The `format-animation` tool validates that 100% of input frames have identical dimensions ($W \times H$) and normalizes any discrepancies.

### 2. Comfortable Animation Pacing Protocol
- Scientific inspection requires distinct pacing for extrema and equilibrium:
  - **Intermediate transition frames**: **800 ms** per frame.
  - **Extrema holds** (e.g., maximum $-3\%$ and $+3\%$ strain): **1200 ms** hold.
  - **Pristine / Equilibrium holds** ($0\%$ strain): **1000 ms** hold.
  - **Oscillation**: Ping-pong cyclic looping (`--ping-pong`) without endpoint duplication.

### 3. Header Clearance & Overlap Prevention
- When deploying multi-line figure suptitles (Title + Subtitle with parameters):
  - **Line 1 (Mode Title)**: `y = 0.955`, `fontsize = 12.0`, `weight="bold"`
  - **Line 2 (Parameters $\varepsilon, a, b, \Delta Q$)**: `y = 0.895`, `fontsize = 10.5`
  - **Subplot top margin**: `top = 0.81`
  - This leaves a generous ~25-point vertical clearance between the subtitle and the subplot headers (`(a)`, `(b)`), preventing text collisions.

### 4. Coupled Band Structure + PDOS Architecture (`render-coupled-suite`)
- **Shared Energy Axis**: `fig, (ax_band, ax_dos) = plt.subplots(..., sharey=True, gridspec_kw={"width_ratios": [1.6, 1.0], "wspace": 0.08})`.
- **Shared Fermi Level**: Plotting `ax.axhline(0.0, color="#d9534f", ls="--", lw=1.0)` on both axes produces an uninterrupted horizontal red dashed line connecting band extrema directly to PDOS van Hove singularities.
- **Dedicated Fixed Colorbar Axis**: Allocates an explicit third axis (`width_ratios=[1.6, 1.0, 0.04]`), preventing dynamic width stealing from the PDOS axis.
- **VESTA Element Color Concordance**: Maps element-projected DOS curves to the exact colors of atoms in the crystal structure figure.

### 5. Label Anti-Collision Engines
Embeds two layout algorithms (cloned in `external/`):
- **`adjustText`**: Force-directed physics repulsion with automatic leader lines.
- **`textalloc`**: Bounding-box void allocation for dense scatter clusters.

### 6. 3D Volumetric Animations (`animate-cdd`)
- **Rotation Mode**: Generates 360° orbital rotation GIFs around a fixed structure (`--mode rotation`). Supports boomerang (forward + reverse).
- **Breathing Mode**: Creates biaxial strain breathing cycles morphing between strain states with crossfading (`--mode breathing`).

### 7. Multi-View CDD Panel (`render-cdd-suite`)
- Renders Charge Density Difference panels highlighting multiple perspectives simultaneously.

### 8. TrueType Font Registration Protocol
- Ensure Times New Roman and STIX math fonts are available in the system and registered dynamically through `matplotlib.font_manager`.

### 9. Quantitative Electronic Strain Descriptors Suite
- When presenting electronic band structures under mechanical strain ($\varepsilon \in [-3\%, +3\%]$), qualitative fat band plots must be accompanied by quantitative parametric descriptors:
  - **Fundamental Band Gap $E_g$**: Insulator/semimetal verification ($E_g = 0.00\text{ eV}$ robust semimetal in PHOTH-graphene).
  - **Dirac Crossing Gap $\Delta E_{\text{Dirac}}$**: Direct gap at crossing point ($<35\text{ meV}$).
  - **Electrochemical Potential Shift $\Delta E_{\text{F}}(\varepsilon)$**: Linear shift ($\sim -0.044\text{ eV}/\%$ strain) quantifying Fermi level elevation under compression for accelerated HER electron injection.
  - **Fermi Velocity $v_{\text{F}}$**: Kinematic dispersion ($v_{\text{F}} = \frac{1}{\hbar}\|\nabla_{\mathbf{k}} E\| \approx 4.48 \times 10^5\text{ m/s}$).
  - **Frontier $p_z$ Purity**: Ratio of $2p_z$ orbital character at $E_{\text{F}}$ (100.0% pure in planar $sp^2$ states).
  - Compute automatically with `sciresearch strain-metrics <csv_or_json>`.

### 10. Programmatic Zero-Dilation Auditing
- Verify animation sequences before export using `sciresearch validate-anim <frame_glob>` to catch any inadvertent `bbox_inches="tight"` dimension jitter across frames.

---

## Quick Reference CLI

| Action | CLI Command |
| :--- | :--- |
| **Apply Standard Python Styling** | `from style_config import set_publication_style; set_publication_style()` |
| **Compose Zero-Dilation Animation** | `format-animation "./frames/frame_*.png" --ping-pong -o strain_movie.gif` |
| **Audit Zero-Dilation Compliance** | `sciresearch validate-anim ./frames/frame_*.png` |
| **Quantify Electronic Strain Descriptors** | `sciresearch strain-metrics strain_electronic_metrics.csv` |
| **Render Coupled Band + PDOS Suite** | `render-coupled-suite` |
| **Assemble Multi-Panel Figure** | `format-multipanel panel_a.png panel_b.png panel_c.png -g 1 3 -o Fig1.png` |
| **Format Single Plot with Anti-Collision** | `format-figure data.csv -o ./fig --engine adjustText --xlabel "$E - E_{\mathrm{F}}\ \mathrm{(eV)}$"` |
| **Animate 3D Volumetric Data (CDD)** | `animate-cdd --mode rotation --frames frame_*.png --output rot.gif` |

---

## Script Architecture & CLI Binaries

Installed globally in `~/.local/bin/`:
- `format-figure` -> `skills/publication-figure-formatter/scripts/label_layout.py`
- `format-multipanel` -> `skills/publication-figure-formatter/scripts/figure_panel_compositor.py`
- `format-animation` -> `skills/publication-figure-formatter/scripts/animation_composer.py`
- `render-coupled-suite` -> `skills/publication-figure-formatter/scripts/render_coupled_suite.py`
- `animate-cdd` -> `skills/publication-figure-formatter/scripts/animate_3d_cdd.py`
