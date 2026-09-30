"""
Geometric and Pyramidalization Analysis Engine.
Calculates Haddon POAV1 (Pi-Orbital Axis Vector) pyramidalization angles,
inter-bond angles, puckering heights, coordination polyhedra, and local site metrics.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
import numpy as np


@dataclass
class SiteGeometry:
    site_index: int
    site_symbol: str
    site_position: np.ndarray
    neighbor_indices: List[int]
    neighbor_symbols: List[str]
    neighbor_positions: List[np.ndarray]
    adsorbate_index: Optional[int]
    adsorbate_symbol: Optional[str]
    adsorbate_position: Optional[np.ndarray]
    bond_lengths: List[float]  # d(A - B_i) in Å
    adsorbate_bond_length: Optional[float]  # d(A - X) in Å
    bond_angles_deg: List[float]  # [theta_1(B2-A-B3), theta_2(B3-A-B1), theta_3(B1-A-B2)]
    average_bond_angle_deg: float
    adsorbate_angles_deg: List[float]  # [angle(X-A-B1), angle(X-A-B2), angle(X-A-B3)]
    poav1_theta_p_deg: float  # Haddon pyramidalization angle: theta_sigma_pi - 90 deg
    poav1_theta_sp_deg: float  # theta_sigma_pi
    poav1_axis_vector: np.ndarray  # Unit vector along the pi-orbital axis
    puckering_height_ang: float  # Out-of-plane distance of A from B1-B2-B3 base plane
    base_plane_normal: np.ndarray  # Unit normal to B1-B2-B3 plane
    base_area_ang2: float  # Area of B1-B2-B3 triangle
    polyhedron_volume_ang3: float  # Volume of tetrahedron A-B1-B2-B3


def compute_poav1(
    u1: np.ndarray,
    u2: np.ndarray,
    u3: np.ndarray,
) -> Tuple[float, float, np.ndarray]:
    """
    Computes Haddon's POAV1 (Pi-Orbital Axis Vector) pyramidalization angle.
    Reference: R. C. Haddon, J. Am. Chem. Soc. 1986, 108, 2837-2842.

    Parameters:
        u1, u2, u3: 3D unit vectors along the three bonds originating from central atom.

    Returns:
        (theta_p_deg, theta_sigma_pi_deg, v_pi_unit_vector)
        - For ideal planar sp2: theta_p = 0.0 deg, theta_sp = 90.0 deg
        - For ideal tetrahedral sp3: theta_p = 19.471 deg, theta_sp = 109.471 deg
    """
    u1 = u1 / np.linalg.norm(u1)
    u2 = u2 / np.linalg.norm(u2)
    u3 = u3 / np.linalg.norm(u3)

    # Reciprocal-like dual vector perpendicular to the bond projections
    w = np.cross(u1, u2) + np.cross(u2, u3) + np.cross(u3, u1)
    norm_w = np.linalg.norm(w)
    if norm_w < 1e-12:
        return 0.0, 90.0, np.zeros(3)

    v_pi = w / norm_w

    # Scalar triple product det([u1, u2, u3])
    det = float(np.dot(u1, np.cross(u2, u3)))

    # cos(theta_sigma_pi)
    cos_theta_sp = det / norm_w
    cos_theta_sp = float(np.clip(cos_theta_sp, -1.0, 1.0))

    # Angle between pi-axis and sigma bonds
    theta_sp_deg = float(np.degrees(np.arccos(abs(cos_theta_sp))))
    theta_p_deg = 90.0 - theta_sp_deg

    return theta_p_deg, theta_sp_deg, v_pi


def get_minimum_image_vector(
    v: np.ndarray,
    cell: Optional[np.ndarray],
    pbc: Optional[np.ndarray],
) -> np.ndarray:
    """Applies minimum image convention for periodic boundary conditions if cell is given."""
    if cell is None or pbc is None or not np.any(pbc):
        return v
    inv_cell = np.linalg.pinv(cell)
    s = np.dot(v, inv_cell)
    for i in range(3):
        if pbc[i]:
            s[i] -= np.round(s[i])
    return np.dot(s, cell)


def analyze_site_geometry(
    positions: np.ndarray,
    symbols: List[str],
    site_idx: int,
    neighbor_indices: Optional[List[int]] = None,
    adsorbate_idx: Optional[int] = None,
    cell: Optional[np.ndarray] = None,
    pbc: Optional[np.ndarray] = None,
    bond_cutoff: float = 2.0,
) -> SiteGeometry:
    """
    Analyzes local geometry of a catalytic/adsorption site.

    If neighbor_indices is None, finds the 3 nearest non-adsorbate neighbors.
    If adsorbate_idx is None, checks if any atypical adatom (e.g. H, O, OH, metal)
    is closely bound to the site (< 1.6 Å for H, < 2.2 Å for O/others).
    """
    n_atoms = len(symbols)
    r_site = positions[site_idx]

    # Calculate distance vectors to all other atoms with MIC
    all_dists = []
    all_vecs = []
    for i in range(n_atoms):
        if i == site_idx:
            all_dists.append(np.inf)
            all_vecs.append(np.zeros(3))
            continue
        v = positions[i] - r_site
        v_mic = get_minimum_image_vector(v, cell, pbc)
        d = float(np.linalg.norm(v_mic))
        all_dists.append(d)
        all_vecs.append(v_mic)

    all_dists = np.array(all_dists)

    # 1. Identify Adsorbate if not provided
    if adsorbate_idx is None:
        # Check if there is an H within 1.4 Å or other light atom
        candidate_ads = []
        for i in range(n_atoms):
            if i == site_idx:
                continue
            if symbols[i] in ["H", "D", "T"] and all_dists[i] < 1.4:
                candidate_ads.append((all_dists[i], i))
            elif symbols[i] in ["O", "F", "Cl", "N", "S"] and all_dists[i] < 1.75:
                candidate_ads.append((all_dists[i], i))
        if candidate_ads:
            candidate_ads.sort()
            adsorbate_idx = candidate_ads[0][1]

    # 2. Identify 3 nearest framework neighbors
    if neighbor_indices is None:
        # Exclude adsorbate from framework neighbors
        ranked = np.argsort(all_dists)
        chosen = []
        for idx in ranked:
            if idx == site_idx or idx == adsorbate_idx:
                continue
            if all_dists[idx] <= bond_cutoff:
                chosen.append(idx)
            if len(chosen) == 3:
                break
        if len(chosen) < 3:
            # Fallback to closest 3 non-adsorbate atoms
            chosen = [idx for idx in ranked if idx not in [site_idx, adsorbate_idx]][:3]
        neighbor_indices = chosen

    # Extract neighbor positions and relative vectors
    r_neighbors = []
    vec_neighbors = []
    bond_lengths = []
    for idx in neighbor_indices:
        v = get_minimum_image_vector(positions[idx] - r_site, cell, pbc)
        d = float(np.linalg.norm(v))
        vec_neighbors.append(v)
        bond_lengths.append(d)
        r_neighbors.append(r_site + v)

    u = [v / np.linalg.norm(v) for v in vec_neighbors]

    # 3. Inter-bond angles:
    # theta_1 = angle(u2, u3)
    # theta_2 = angle(u3, u1)
    # theta_3 = angle(u1, u2)
    def angle_deg(v_a, v_b):
        c = np.clip(np.dot(v_a, v_b) / (np.linalg.norm(v_a) * np.linalg.norm(v_b)), -1.0, 1.0)
        return float(np.degrees(np.arccos(c)))

    theta_1 = angle_deg(u[1], u[2])
    theta_2 = angle_deg(u[2], u[0])
    theta_3 = angle_deg(u[0], u[1])
    bond_angles_deg = [theta_1, theta_2, theta_3]
    avg_bond_angle_deg = float(np.mean(bond_angles_deg))

    # 4. POAV1 pyramidalization angle
    theta_p, theta_sp, v_pi = compute_poav1(u[0], u[1], u[2])

    # 5. Base plane normal & puckering height
    v_base_1 = r_neighbors[1] - r_neighbors[0]
    v_base_2 = r_neighbors[2] - r_neighbors[0]
    cross_base = np.cross(v_base_1, v_base_2)
    norm_base = np.linalg.norm(cross_base)
    if norm_base > 1e-12:
        n_base = cross_base / norm_base
        base_area = 0.5 * norm_base
        # Out-of-plane distance of site from base plane
        puckering_h = float(abs(np.dot(r_site - r_neighbors[0], n_base)))
        # Tetrahedron volume (1/6 * base_area * 2 * height)
        tet_vol = float((1.0 / 6.0) * abs(np.dot(r_site - r_neighbors[0], cross_base)))
    else:
        n_base = np.array([0.0, 0.0, 1.0])
        base_area = 0.0
        puckering_h = 0.0
        tet_vol = 0.0

    # 6. Adsorbate metrics (if present)
    ads_pos = None
    ads_sym = None
    ads_dist = None
    ads_angles = []
    if adsorbate_idx is not None and adsorbate_idx < n_atoms:
        ads_sym = symbols[adsorbate_idx]
        v_ads = get_minimum_image_vector(positions[adsorbate_idx] - r_site, cell, pbc)
        ads_dist = float(np.linalg.norm(v_ads))
        ads_pos = r_site + v_ads
        u_ads = v_ads / ads_dist
        ads_angles = [angle_deg(u_ads, u_i) for u_i in u]

    return SiteGeometry(
        site_index=site_idx,
        site_symbol=symbols[site_idx],
        site_position=r_site,
        neighbor_indices=neighbor_indices,
        neighbor_symbols=[symbols[i] for i in neighbor_indices],
        neighbor_positions=r_neighbors,
        adsorbate_index=adsorbate_idx,
        adsorbate_symbol=ads_sym,
        adsorbate_position=ads_pos,
        bond_lengths=bond_lengths,
        adsorbate_bond_length=ads_dist,
        bond_angles_deg=bond_angles_deg,
        average_bond_angle_deg=avg_bond_angle_deg,
        adsorbate_angles_deg=ads_angles,
        poav1_theta_p_deg=theta_p,
        poav1_theta_sp_deg=theta_sp,
        poav1_axis_vector=v_pi,
        puckering_height_ang=puckering_h,
        base_plane_normal=n_base,
        base_area_ang2=base_area,
        polyhedron_volume_ang3=tet_vol,
    )


def auto_detect_sites(
    positions: np.ndarray,
    symbols: List[str],
    cell: Optional[np.ndarray] = None,
    pbc: Optional[np.ndarray] = None,
    mode: str = "strain",  # 'strain', 'adsorbate', 'all'
    top_n: int = 6,
) -> Dict[str, int]:
    """
    Automatically detects high-interest active sites:
    - 'adsorbate': Finds framework atoms with directly bound adatoms (H, O, OH, etc.).
    - 'strain': Calculates Haddon POAV1 theta_p for all 3-coordinate atoms and ranks them by strain.
    - 'all': Combines adsorbate-bound sites with highest-strain framework sites.
    """
    n_atoms = len(symbols)
    # Identify non-framework adatoms (like H, adsorbed O)
    candidate_framework = [i for i, s in enumerate(symbols) if s not in ["H", "D", "T"]]

    adsorbate_sites = []
    strain_sites = []

    for idx in candidate_framework:
        geom = analyze_site_geometry(positions, symbols, idx, cell=cell, pbc=pbc)
        if geom.adsorbate_index is not None:
            adsorbate_sites.append((geom.poav1_theta_p_deg, idx))
        if len(geom.neighbor_indices) == 3:
            strain_sites.append((geom.poav1_theta_p_deg, idx))

    # Sort descending by pyramidalization angle
    adsorbate_sites.sort(reverse=True)
    strain_sites.sort(reverse=True)

    chosen = []
    if mode == "adsorbate":
        chosen = [idx for _, idx in adsorbate_sites[:top_n]]
    elif mode == "strain":
        chosen = [idx for _, idx in strain_sites[:top_n]]
    else:  # mode == 'all'
        # Prioritize adsorbate-bound sites first, then highest-strain sites
        seen = set()
        for _, idx in adsorbate_sites:
            if idx not in seen:
                chosen.append(idx)
                seen.add(idx)
        for _, idx in strain_sites:
            if idx not in seen:
                chosen.append(idx)
                seen.add(idx)
            if len(chosen) >= top_n:
                break

    # If still not enough, take top from candidate framework
    if len(chosen) < top_n:
        for idx in candidate_framework:
            if idx not in chosen:
                chosen.append(idx)
            if len(chosen) >= top_n:
                break

    return {f"S{k+1}": idx for k, idx in enumerate(chosen[:top_n])}


def export_geometry_report(
    site_geometries: List[SiteGeometry],
    output_json_path: Optional[str] = None,
    output_csv_path: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """Exports geometric analysis results to structured JSON and CSV reports."""
    import json
    import pandas as pd

    records = []
    for g in site_geometries:
        rec = {
            "site_index": int(g.site_index),
            "site_symbol": str(g.site_symbol),
            "neighbor_indices": [int(x) for x in g.neighbor_indices],
            "neighbor_symbols": [str(x) for x in g.neighbor_symbols],
            "bond_lengths_ang": [round(float(x), 4) for x in g.bond_lengths],
            "adsorbate_index": int(g.adsorbate_index) if g.adsorbate_index is not None else None,
            "adsorbate_symbol": str(g.adsorbate_symbol) if g.adsorbate_symbol else None,
            "adsorbate_bond_length_ang": round(float(g.adsorbate_bond_length), 4) if g.adsorbate_bond_length else None,
            "bond_angles_deg": [round(float(x), 2) for x in g.bond_angles_deg],
            "average_bond_angle_deg": round(float(g.average_bond_angle_deg), 2),
            "poav1_theta_p_deg": round(float(g.poav1_theta_p_deg), 3),
            "poav1_theta_sp_deg": round(float(g.poav1_theta_sp_deg), 3),
            "puckering_height_ang": round(float(g.puckering_height_ang), 4),
            "base_area_ang2": round(float(g.base_area_ang2), 4),
            "polyhedron_volume_ang3": round(float(g.polyhedron_volume_ang3), 5),
        }
        records.append(rec)

    json_file = None
    if output_json_path:
        with open(output_json_path, "w") as f:
            json.dump(records, f, indent=2)
        json_file = output_json_path

    csv_file = None
    if output_csv_path:
        df = pd.DataFrame([{
            "site": f"S{k+1}",
            "atom_idx": r["site_index"],
            "element": r["site_symbol"],
            "theta_p_deg": r["poav1_theta_p_deg"],
            "puckering_height_ang": r["puckering_height_ang"],
            "tet_volume_ang3": r["polyhedron_volume_ang3"],
            "avg_bond_angle_deg": r["average_bond_angle_deg"],
            "adsorbate": f"{r['adsorbate_symbol']}{r['adsorbate_index']}" if r["adsorbate_symbol"] else "None",
            "adsorbate_dist_ang": r["adsorbate_bond_length_ang"],
        } for k, r in enumerate(records)])
        df.to_csv(output_csv_path, index=False)
        csv_file = output_csv_path

    return json_file, csv_file
