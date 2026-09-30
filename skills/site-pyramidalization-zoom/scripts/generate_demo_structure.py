"""
Demo Structure Generator for Catalytic / Adsorption Sites.
Creates a realistic 2D porous carbon / biphenylene nanoribbon structure
with non-hexagonal rings (4-, 6-, 8-membered rings), edge hydrogen passivation,
and adatoms (H) at multiple active sites (S1-S6) to benchmark pyramidalization
and circular zoom visualization.
"""

from pathlib import Path
import numpy as np


def create_porous_carbon_model(output_path: str = "demo_porous_carbon.vasp"):
    """
    Constructs a 2D porous carbon lattice (similar to the biphenylene/porous nanoribbon
    in Nature Catalysis / ACS Catalysis literature).
    Includes 6 designated active sites (S1 - S6) with puckering and an adsorbed H atom.
    """
    # Unit dimensions
    a_x = 24.0
    b_y = 14.0
    c_z = 20.0

    carbon_coords = []
    # Build a periodic/ribbon framework of 4-, 6-, and 8-membered rings
    # Backbone coordinates in xy plane at z = 10.0
    z0 = 10.0

    # Central pore boundary and surrounding rings
    # Left subunit (hexagonal and 4-8 rings)
    base_hexagons = [
        # Left wing
        (2.5, 7.0), (3.7, 7.7), (4.9, 7.0), (4.9, 5.6), (3.7, 4.9), (2.5, 5.6),
        (3.7, 9.1), (4.9, 9.8), (6.1, 9.1), (6.1, 7.7),
        (3.7, 3.5), (4.9, 2.8), (6.1, 3.5), (6.1, 4.9),
        (7.3, 9.8), (8.5, 9.1), (8.5, 7.7), (7.3, 7.0),
        (7.3, 2.8), (8.5, 3.5), (8.5, 4.9), (7.3, 5.6),
        # Middle bridge (4-8 rings with pore)
        (9.7, 9.1), (10.9, 9.1), (10.9, 7.7), (9.7, 7.7), # 4-ring top
        (9.7, 4.9), (10.9, 4.9), (10.9, 3.5), (9.7, 3.5), # 4-ring bottom
        (10.9, 6.4), (9.7, 6.4),                          # bridge atoms
        # Right wing (symmetric)
        (12.1, 9.8), (13.3, 9.1), (13.3, 7.7), (12.1, 7.0),
        (12.1, 2.8), (13.3, 3.5), (13.3, 4.9), (12.1, 5.6),
        (14.5, 9.1), (15.7, 9.8), (16.9, 9.1), (16.9, 7.7), (15.7, 7.0), (14.5, 7.7),
        (14.5, 3.5), (15.7, 2.8), (16.9, 3.5), (16.9, 4.9), (15.7, 5.6), (14.5, 4.9),
        (18.1, 7.0), (19.3, 7.7), (20.5, 7.0), (20.5, 5.6), (19.3, 4.9), (18.1, 5.6),
    ]

    # Deduplicate and sort coordinates
    seen = set()
    cleaned_c = []
    for x, y in base_hexagons:
        key = (round(x, 1), round(y, 1))
        if key not in seen:
            seen.add(key)
            cleaned_c.append(np.array([x, y, z0]))

    # Let's add designated active sites:
    # S1 (pore edge), S2 (4-ring shoulder), S3 (pore center bridge),
    # S4 (right bridge), S5 (bottom 4-ring), S6 (bottom pore edge)
    # Give site S6 out-of-plane puckering (z0 + 0.35 A) to simulate H adsorption!
    site_indices_map = {}
    positions = np.array(cleaned_c)

    # Find closest atoms to typical site coordinates:
    target_sites = {
        "S1": np.array([7.3, 7.0, z0]),
        "S2": np.array([9.7, 7.7, z0]),
        "S3": np.array([10.9, 6.4, z0]),
        "S4": np.array([12.1, 7.0, z0]),
        "S5": np.array([10.9, 3.5, z0]),
        "S6": np.array([9.7, 3.5, z0]),
    }

    site_idx_list = {}
    for name, t_pos in target_sites.items():
        dists = np.linalg.norm(positions[:, :2] - t_pos[:2], axis=1)
        best_idx = int(np.argmin(dists))
        site_idx_list[name] = best_idx

    # Apply puckering to S6 (site 5) to show sp3 pyramidalization
    s6_idx = site_idx_list["S6"]
    positions[s6_idx, 2] += 0.35  # puckered out of plane

    # Add adsorbed Hydrogen atop S6
    h_pos = np.copy(positions[s6_idx])
    h_pos[2] += 1.10  # C-H bond length ~ 1.10 A

    # Also add edge passivating hydrogens to unterminated edge carbons
    edge_h_list = []
    for i, p in enumerate(positions):
        dists = np.linalg.norm(positions[:, :2] - p[:2], axis=1)
        n_neighbors = np.sum((dists > 0.1) & (dists < 1.7))
        if n_neighbors <= 2:
            # Unterminated edge carbon -> add H
            neighbor_vecs = positions[(dists > 0.1) & (dists < 1.7)] - p
            mean_v = np.mean(neighbor_vecs[:, :2], axis=0)
            norm_v = np.linalg.norm(mean_v)
            if norm_v > 1e-4:
                out_dir = -mean_v / norm_v
                h_edge = np.array([p[0] + out_dir[0] * 1.09, p[1] + out_dir[1] * 1.09, z0])
                edge_h_list.append(h_edge)

    # Total atoms
    n_carbon = len(positions)
    all_hydrogens = [h_pos] + edge_h_list
    n_hydrogen = len(all_hydrogens)

    # Write VASP POSCAR
    out_file = Path(output_path).resolve()
    with open(out_file, "w") as f:
        f.write(f"Porous Carbon Ribbon with S1-S6 Sites and Adsorbate\n")
        f.write("1.0\n")
        f.write(f" {a_x:15.8f}   0.00000000   0.00000000\n")
        f.write(f"   0.00000000  {b_y:15.8f}   0.00000000\n")
        f.write(f"   0.00000000   0.00000000  {c_z:15.8f}\n")
        f.write(" C   H\n")
        f.write(f" {n_carbon}  {n_hydrogen}\n")
        f.write("Cartesian\n")
        for p in positions:
            f.write(f" {p[0]:15.8f} {p[1]:15.8f} {p[2]:15.8f}\n")
        for p in all_hydrogens:
            f.write(f" {p[0]:15.8f} {p[1]:15.8f} {p[2]:15.8f}\n")

    # Generate mock adsorption free energies for Panel a
    # Realistic values matching the color scale from -1.2 to +1.2 eV
    np.random.seed(42)
    dg_ads_data = []
    site_names = ["S1", "S2", "S3", "S4", "S5", "S6"]
    special_dg = {
        "S1": 0.85,
        "S2": 0.15,
        "S3": -0.72,
        "S4": -0.45,
        "S5": 0.30,
        "S6": 1.15,
    }

    for i in range(n_carbon):
        # Default distribution around 0.2 to 0.9 eV
        val = float(np.random.normal(0.4, 0.35))
        # Override special sites
        for s_name, s_idx in site_idx_list.items():
            if i == s_idx:
                val = special_dg[s_name]
        val = np.clip(val, -1.2, 1.2)
        dg_ads_data.append((i, val))

    # Save mock dG_ads.csv
    csv_file = out_file.parent / f"{out_file.stem}_dG_ads.csv"
    with open(csv_file, "w") as f:
        f.write("atom_index,dG_ads_eV\n")
        for idx, val in dg_ads_data:
            f.write(f"{idx},{val:.4f}\n")

    return str(out_file), str(csv_file), site_idx_list
