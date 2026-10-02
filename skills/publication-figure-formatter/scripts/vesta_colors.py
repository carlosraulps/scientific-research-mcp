"""
VESTA Element Color Palette & Colorblind-Accessible Scientific Color Schemes.
Provides exact concordance between VESTA crystal structure renderings
and element-projected DOS/band structure plots, plus Okabe-Ito and Tol colorblind palettes.
"""

from typing import Dict, List, Tuple, Union
import matplotlib as mpl
from cycler import cycler

# ---------------------------------------------------------------------------
# 1. Okabe-Ito Colorblind-Friendly Categorical Palette (JFly / Nature Methods)
# ---------------------------------------------------------------------------
OKABE_ITO = {
    "orange": "#E69F00",
    "sky_blue": "#56B4E9",
    "bluish_green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "black": "#000000",
}
OKABE_ITO_LIST = list(OKABE_ITO.values())

# Paul Tol's Bright & Muted Palettes
TOL_BRIGHT = ["#4477AA", "#66CCEE", "#228833", "#CCBB44", "#EE6677", "#AA3377", "#BBBBBB"]
TOL_MUTED = ["#CC6677", "#332288", "#DDCC77", "#117733", "#88CCEE", "#882255", "#44AA99", "#999933", "#AA4499"]

# Recommended Colorblind-Safe Continuous Colormaps
COLORBLIND_SEQUENTIAL = ["cividis", "viridis", "plasma", "inferno", "magma"]
COLORBLIND_DIVERGING = ["coolwarm", "RdBu_r", "PRGn", "PuOr"]

# ---------------------------------------------------------------------------
# 1b. Standardized CDD Isosurface Color Constants
# ---------------------------------------------------------------------------
CDD_COLORS = {
    "accumulation": {"hex": "#f1c40f", "rgb": (0.945, 0.769, 0.059), "rgb255": (241, 196, 15), "label": r"$\Delta\rho > 0$ (accumulation)"},
    "depletion":    {"hex": "#00b4d8", "rgb": (0.000, 0.706, 0.847), "rgb255": (0, 180, 216),   "label": r"$\Delta\rho < 0$ (depletion)"},
    "opacity":      0.60,
}

# ---------------------------------------------------------------------------
# 1c. Continuous Bader Charge Colormap Utility
# ---------------------------------------------------------------------------
def bader_charge_colormap(charges, cmap_name="RdBu_r", vmin=None, vmax=None):
    """Map Bader net charges to RGBA colors using a diverging colormap.

    Args:
        charges: Array-like of net atomic charges (ΔQ = Z_val - Q_bader).
        cmap_name: Matplotlib colormap name (default: 'RdBu_r', red=positive, blue=negative).
        vmin, vmax: Symmetric limits. If None, uses max(|charges|) for symmetric scale.

    Returns:
        List of hex color strings, one per atom.
    """
    import numpy as np
    charges = np.asarray(charges, dtype=float)
    if vmin is None or vmax is None:
        limit = max(abs(charges.min()), abs(charges.max()), 0.01)
        vmin, vmax = -limit, limit
    cmap = mpl.colormaps.get_cmap(cmap_name)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    return [mpl.colors.to_hex(cmap(norm(q))) for q in charges]

# ---------------------------------------------------------------------------
# 2. VESTA Standard Element Colors & Radii (Extracted from /opt/VESTA/elements.ini)
# ---------------------------------------------------------------------------
VESTA_ELEMENTS = {
    "H":  {"z": 1,  "rgb": (1.000, 0.800, 0.800), "hex": "#FFCCCC", "r_cov": 0.46, "r_vdw": 1.20},
    "He": {"z": 2,  "rgb": (0.989, 0.913, 0.811), "hex": "#FCE9CF", "r_cov": 1.22, "r_vdw": 1.40},
    "Li": {"z": 3,  "rgb": (0.527, 0.880, 0.457), "hex": "#87E075", "r_cov": 1.57, "r_vdw": 1.40},
    "Be": {"z": 4,  "rgb": (0.371, 0.846, 0.483), "hex": "#5FD87B", "r_cov": 1.12, "r_vdw": 1.40},
    "B":  {"z": 5,  "rgb": (0.125, 0.636, 0.059), "hex": "#20A20F", "r_cov": 0.81, "r_vdw": 1.40},
    "C":  {"z": 6,  "rgb": (0.504, 0.287, 0.162), "hex": "#814929", "r_cov": 0.77, "r_vdw": 1.70},
    "N":  {"z": 7,  "rgb": (0.691, 0.729, 0.903), "hex": "#B0BAE6", "r_cov": 0.74, "r_vdw": 1.55},
    "O":  {"z": 8,  "rgb": (1.000, 0.013, 0.000), "hex": "#FF0300", "r_cov": 0.74, "r_vdw": 1.52},
    "F":  {"z": 9,  "rgb": (0.691, 0.729, 0.903), "hex": "#B0BAE6", "r_cov": 0.72, "r_vdw": 1.47},
    "Ne": {"z": 10, "rgb": (1.000, 0.218, 0.710), "hex": "#FF37B5", "r_cov": 1.60, "r_vdw": 1.54},
    "Na": {"z": 11, "rgb": (0.980, 0.866, 0.238), "hex": "#FADD3D", "r_cov": 1.91, "r_vdw": 1.54},
    "Mg": {"z": 12, "rgb": (0.988, 0.485, 0.085), "hex": "#FC7C16", "r_cov": 1.60, "r_vdw": 1.54},
    "Al": {"z": 13, "rgb": (0.507, 0.701, 0.841), "hex": "#82B3D7", "r_cov": 1.43, "r_vdw": 1.54},
    "Si": {"z": 14, "rgb": (0.106, 0.232, 0.981), "hex": "#1B3BFA", "r_cov": 1.18, "r_vdw": 2.10},
    "P":  {"z": 15, "rgb": (0.756, 0.613, 0.764), "hex": "#C19CC3", "r_cov": 1.10, "r_vdw": 1.80},
    "S":  {"z": 16, "rgb": (1.000, 0.981, 0.000), "hex": "#FFFA00", "r_cov": 1.04, "r_vdw": 1.80},
    "Cl": {"z": 17, "rgb": (0.196, 0.988, 0.012), "hex": "#32FC03", "r_cov": 0.99, "r_vdw": 1.75},
    "Ar": {"z": 18, "rgb": (0.813, 0.997, 0.771), "hex": "#D0FEC5", "r_cov": 1.92, "r_vdw": 1.88},
    "K":  {"z": 19, "rgb": (0.633, 0.133, 0.969), "hex": "#A122F7", "r_cov": 2.35, "r_vdw": 1.88},
    "Ca": {"z": 20, "rgb": (0.356, 0.589, 0.745), "hex": "#5B96BE", "r_cov": 1.97, "r_vdw": 1.88},
    "Sc": {"z": 21, "rgb": (0.712, 0.389, 0.673), "hex": "#B663AC", "r_cov": 1.64, "r_vdw": 1.88},
    "Ti": {"z": 22, "rgb": (0.472, 0.794, 1.000), "hex": "#78CAFF", "r_cov": 1.47, "r_vdw": 1.88},
    "V":  {"z": 23, "rgb": (0.900, 0.100, 0.000), "hex": "#E61A00", "r_cov": 1.35, "r_vdw": 1.88},
    "Cr": {"z": 24, "rgb": (0.000, 0.000, 0.620), "hex": "#00009E", "r_cov": 1.29, "r_vdw": 1.88},
    "Mn": {"z": 25, "rgb": (0.661, 0.034, 0.620), "hex": "#A9099E", "r_cov": 1.37, "r_vdw": 1.88},
    "Fe": {"z": 26, "rgb": (0.711, 0.447, 0.001), "hex": "#B57200", "r_cov": 1.26, "r_vdw": 1.88},
    "Co": {"z": 27, "rgb": (0.000, 0.000, 0.687), "hex": "#0000AF", "r_cov": 1.25, "r_vdw": 1.88},
    "Ni": {"z": 28, "rgb": (0.720, 0.736, 0.743), "hex": "#B8BCBE", "r_cov": 1.25, "r_vdw": 1.88},
    "Cu": {"z": 29, "rgb": (0.134, 0.280, 0.866), "hex": "#2247DD", "r_cov": 1.28, "r_vdw": 1.88},
    "Zn": {"z": 30, "rgb": (0.561, 0.564, 0.508), "hex": "#8F9082", "r_cov": 1.37, "r_vdw": 1.88},
    "Ga": {"z": 31, "rgb": (0.623, 0.893, 0.455), "hex": "#9FE474", "r_cov": 1.53, "r_vdw": 1.88},
    "Ge": {"z": 32, "rgb": (0.496, 0.435, 0.652), "hex": "#7E6FA6", "r_cov": 1.22, "r_vdw": 1.88},
    "As": {"z": 33, "rgb": (0.458, 0.817, 0.342), "hex": "#75D057", "r_cov": 1.21, "r_vdw": 1.85},
    "Se": {"z": 34, "rgb": (0.604, 0.939, 0.061), "hex": "#9AEE10", "r_cov": 1.04, "r_vdw": 1.90},
    "Br": {"z": 35, "rgb": (0.496, 0.193, 0.011), "hex": "#7F3103", "r_cov": 1.14, "r_vdw": 1.85},
    "Kr": {"z": 36, "rgb": (0.981, 0.758, 0.954), "hex": "#FAC1F3", "r_cov": 1.98, "r_vdw": 2.02},
    "Rb": {"z": 37, "rgb": (1.000, 0.000, 0.600), "hex": "#FF0099", "r_cov": 2.50, "r_vdw": 2.02},
    "Sr": {"z": 38, "rgb": (0.000, 1.000, 0.153), "hex": "#00FF27", "r_cov": 2.15, "r_vdw": 2.02},
    "Y":  {"z": 39, "rgb": (0.403, 0.597, 0.558), "hex": "#67988E", "r_cov": 1.82, "r_vdw": 2.02},
    "Zr": {"z": 40, "rgb": (0.835, 0.463, 0.334), "hex": "#D57655", "r_cov": 1.60, "r_vdw": 2.02},
    "Nb": {"z": 41, "rgb": (0.584, 0.819, 0.672), "hex": "#95D1AB", "r_cov": 1.47, "r_vdw": 2.02},
    "Mo": {"z": 42, "rgb": (0.287, 0.457, 0.864), "hex": "#4975DC", "r_cov": 1.40, "r_vdw": 2.02},
    "Ru": {"z": 44, "rgb": (0.134, 0.669, 0.697), "hex": "#22ABB2", "r_cov": 1.34, "r_vdw": 2.02},
    "Rh": {"z": 45, "rgb": (0.040, 0.490, 0.550), "hex": "#0A7D8C", "r_cov": 1.34, "r_vdw": 2.02},
    "Pd": {"z": 46, "rgb": (0.000, 0.410, 0.520), "hex": "#006885", "r_cov": 1.37, "r_vdw": 2.02},
    "Ag": {"z": 47, "rgb": (0.750, 0.750, 0.750), "hex": "#BFBFBF", "r_cov": 1.44, "r_vdw": 2.02},
    "Cd": {"z": 48, "rgb": (1.000, 0.850, 0.560), "hex": "#FFD98F", "r_cov": 1.52, "r_vdw": 2.02},
    "In": {"z": 49, "rgb": (0.650, 0.460, 0.450), "hex": "#A67573", "r_cov": 1.50, "r_vdw": 2.02},
    "Sn": {"z": 50, "rgb": (0.400, 0.500, 0.500), "hex": "#668080", "r_cov": 1.40, "r_vdw": 2.02},
    "Sb": {"z": 51, "rgb": (0.620, 0.390, 0.710), "hex": "#9E63B5", "r_cov": 1.41, "r_vdw": 2.00},
    "Te": {"z": 52, "rgb": (0.830, 0.480, 0.000), "hex": "#D47A00", "r_cov": 1.37, "r_vdw": 2.00},
    "I":  {"z": 53, "rgb": (0.580, 0.000, 0.580), "hex": "#940094", "r_cov": 1.33, "r_vdw": 2.00},
    "Cs": {"z": 55, "rgb": (0.350, 0.100, 0.580), "hex": "#591A94", "r_cov": 2.70, "r_vdw": 2.10},
    "Ba": {"z": 56, "rgb": (0.000, 0.790, 0.000), "hex": "#00C900", "r_cov": 2.24, "r_vdw": 2.10},
    "La": {"z": 57, "rgb": (0.440, 0.830, 1.000), "hex": "#70D4FF", "r_cov": 1.95, "r_vdw": 2.10},
    "Ce": {"z": 58, "rgb": (1.000, 1.000, 0.780), "hex": "#FFFFC7", "r_cov": 1.85, "r_vdw": 2.10},
    "Pt": {"z": 78, "rgb": (0.820, 0.820, 0.880), "hex": "#D1D1E0", "r_cov": 1.36, "r_vdw": 2.10},
    "Au": {"z": 79, "rgb": (1.000, 0.820, 0.140), "hex": "#FFD124", "r_cov": 1.44, "r_vdw": 2.10},
    "Hg": {"z": 80, "rgb": (0.710, 0.710, 0.760), "hex": "#B5B5C2", "r_cov": 1.49, "r_vdw": 2.10},
    "Pb": {"z": 82, "rgb": (0.340, 0.350, 0.380), "hex": "#575961", "r_cov": 1.46, "r_vdw": 2.10},
    "Bi": {"z": 83, "rgb": (0.620, 0.310, 0.710), "hex": "#9E4FB5", "r_cov": 1.51, "r_vdw": 2.10},
}


def get_vesta_color(symbol: str, format: str = "hex") -> Union[str, Tuple[float, float, float]]:
    """
    Get the exact VESTA color for a given chemical element.

    Parameters:
    - symbol: Chemical element symbol (e.g., 'Ti', 'Sr', 'O', 'Fe')
    - format: 'hex' (default) or 'rgb' (normalized 0.0-1.0)
    """
    sym = symbol.strip().capitalize()
    el_data = VESTA_ELEMENTS.get(sym)
    if not el_data:
        # Fallback to dark gray
        return "#444444" if format == "hex" else (0.27, 0.27, 0.27)
    return el_data["hex"] if format == "hex" else el_data["rgb"]


def get_element_cycler(elements: List[str]) -> mpl.cycler:
    """
    Create a Matplotlib cycler configured with the exact VESTA element colors.
    Useful for element-projected DOS or band structure line plots.
    """
    colors = [get_vesta_color(el, format="hex") for el in elements]
    return cycler(color=colors)


def get_element_palette(elements: List[str]) -> Dict[str, str]:
    """
    Return a dictionary mapping element symbol -> VESTA hex color.
    """
    return {el: get_vesta_color(el, format="hex") for el in elements}
