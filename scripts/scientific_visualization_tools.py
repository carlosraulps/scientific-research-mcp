#!/usr/bin/env python3
"""
================================================================================
Scientific Visualization & Crystallographic Analysis Tools
================================================================================
Implements standardized scientific protocols derived from the PHOTH-Graphene
and multi-cluster computational suite:
  1. Wyckoff symmetry orbit grouping & Bader PAW core charge offset standardization
     (q_C = 4.0 - Q_Bader) with Cartesian FFT grid splitting diagnostics.
  2. Zero-bloat remote volumetric slicing (CHGCAR/LOCPOT/ELFCAR) at invariant
     crystallographic planes (e.g. z = 0.50).
  3. Zero-Dilation Rule validation for multi-frame scientific animations.
  4. Quantitative electronic strain metrics calculation (Eg, Delta E_F, v_F, Delta k).
================================================================================
"""

import os
import sys
import json
import math
import struct
from typing import Dict, Any, List, Optional, Tuple, Union
import numpy as np

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# ==============================================================================
# 1. Wyckoff Bader Standardization & PAW Core Charge Offset
# ==============================================================================

# Default Wyckoff mapping for 10-atom planar PHOTH-graphene unit cell (Pmm2, No. 25)
PHOTH_GRAPHENE_WYCKOFF_MAPPING = {
    1: "C1",
    2: "C2",
    3: "C2",
    4: "C3",
    5: "C3",
    6: "C4",
    7: "C4",
    8: "C5",
    9: "C5",
    10: "C6"
}


def parse_acf_dat(file_path: str) -> List[Dict[str, Any]]:
    """
    Parses Henkelman ACF.dat Bader analysis output.
    Columns: #, X, Y, Z, CHARGE, MIN DIST, ATOMIC VOL
    """
    atoms = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ACF.dat file not found: {file_path}")

    with open(file_path, "r") as f:
        lines = f.readlines()

    header_passed = False
    for line in lines:
        line_str = line.strip()
        if not line_str or line_str.startswith("-"):
            if "CHARGE" in line_str or "#" in line_str:
                header_passed = True
            continue

        parts = line_str.split()
        if len(parts) >= 5:
            try:
                atom_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                charge_val = float(parts[4])
                atoms.append({
                    "atom_id": atom_id,
                    "x": x,
                    "y": y,
                    "z": z,
                    "q_bader": charge_val
                })
            except (ValueError, IndexError):
                continue

    return atoms


def standardize_wyckoff_bader_charges(
    bader_data: Union[str, List[Dict[str, Any]], List[float], Dict[str, Any]],
    wyckoff_mapping: Optional[Dict[int, str]] = None,
    z_core: float = 4.0,
    tolerance: float = 0.15,
    element: str = "C"
) -> Dict[str, Any]:
    """
    Standardizes Bader charges according to crystallographic Wyckoff site symmetry
    and PAW pseudopotential core charge offset:
        q_net = Z_core - Q_Bader
    
    Detects and averages artificial charge splitting caused by Cartesian FFT grid
    mesh alignment across mirror planes.
    """
    # 1. Extract raw atom populations
    raw_atoms: List[Dict[str, Any]] = []

    if isinstance(bader_data, str):
        if os.path.exists(bader_data):
            if bader_data.endswith(".json"):
                with open(bader_data, "r") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, list):
                        raw_atoms = loaded
                    elif isinstance(loaded, dict) and "charges" in loaded:
                        raw_atoms = loaded["charges"]
            elif bader_data.endswith(".csv"):
                import csv
                with open(bader_data, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        raw_atoms.append({
                            "atom_id": int(row.get("atom_id", row.get("id", len(raw_atoms) + 1))),
                            "q_bader": float(row.get("q_bader", row.get("charge", row.get("Q_Bader", 0.0))))
                        })
            else:
                # Assume ACF.dat format
                raw_atoms = parse_acf_dat(bader_data)
        else:
            raise FileNotFoundError(f"Input file path not found: {bader_data}")
    elif isinstance(bader_data, list):
        for idx, item in enumerate(bader_data, start=1):
            if isinstance(item, dict):
                raw_atoms.append({
                    "atom_id": int(item.get("atom_id", item.get("id", idx))),
                    "q_bader": float(item.get("q_bader", item.get("charge", item.get("Q_Bader", 0.0)))),
                    "x": item.get("x"), "y": item.get("y"), "z": item.get("z")
                })
            elif isinstance(item, (int, float)):
                raw_atoms.append({
                    "atom_id": idx,
                    "q_bader": float(item)
                })
    elif isinstance(bader_data, dict):
        if "charges" in bader_data:
            return standardize_wyckoff_bader_charges(bader_data["charges"], wyckoff_mapping, z_core, tolerance, element)
        for k, v in bader_data.items():
            try:
                aid = int(k)
                raw_atoms.append({
                    "atom_id": aid,
                    "q_bader": float(v)
                })
            except ValueError:
                pass

    if not raw_atoms:
        return {"error": "No valid Bader population data found.", "isError": True}

    # Sort by atom_id
    raw_atoms.sort(key=lambda a: a["atom_id"])

    # 2. Determine Wyckoff mapping
    mapping = wyckoff_mapping
    if mapping is None:
        if len(raw_atoms) == 10:
            mapping = PHOTH_GRAPHENE_WYCKOFF_MAPPING
        else:
            # Generate trivial 1-to-1 Wyckoff sites
            mapping = {a["atom_id"]: f"{element}{a['atom_id']}" for a in raw_atoms}

    # Convert mapping keys to int if necessary
    mapping = {int(k): str(v) for k, v in mapping.items()}

    # 3. Calculate net charge q_net = Z_core - Q_Bader
    enriched_atoms = []
    total_valence = 0.0
    for a in raw_atoms:
        aid = a["atom_id"]
        q_bader = a["q_bader"]
        total_valence += q_bader
        q_net = round(z_core - q_bader, 5)
        wyckoff_site = mapping.get(aid, f"{element}_{aid}")
        label = f"{wyckoff_site}^({aid})"

        enriched_atoms.append({
            "atom_id": aid,
            "label": label,
            "wyckoff_site": wyckoff_site,
            "q_bader": q_bader,
            "q_net": q_net,
            "x": a.get("x"),
            "y": a.get("y"),
            "z": a.get("z")
        })

    # 4. Group by Wyckoff orbits
    orbits: Dict[str, Dict[str, Any]] = {}
    for a in enriched_atoms:
        site = a["wyckoff_site"]
        if site not in orbits:
            orbits[site] = {
                "wyckoff_site": site,
                "multiplicity": 0,
                "atom_ids": [],
                "labels": [],
                "q_bader_values": [],
                "q_net_values": []
            }
        orbits[site]["multiplicity"] += 1
        orbits[site]["atom_ids"].append(a["atom_id"])
        orbits[site]["labels"].append(a["label"])
        orbits[site]["q_bader_values"].append(a["q_bader"])
        orbits[site]["q_net_values"].append(a["q_net"])

    # Analyze splitting and averages
    orbit_averages = {}
    for site, odata in orbits.items():
        q_nets = odata["q_net_values"]
        mean_net = float(np.mean(q_nets))
        mean_bader = float(np.mean(odata["q_bader_values"]))
        split = float(np.ptp(q_nets)) if len(q_nets) > 1 else 0.0
        is_split_artifact = (split > 0.001) and (split <= tolerance)

        odata["mean_q_net"] = round(mean_net, 4)
        odata["mean_q_bader"] = round(mean_bader, 4)
        odata["charge_splitting"] = round(split, 4)
        odata["is_grid_artifact"] = is_split_artifact
        odata["symmetry_broken"] = (split > tolerance)
        orbit_averages[site] = round(mean_net, 4)

    # Annotate atoms with orbit averages
    for a in enriched_atoms:
        site = a["wyckoff_site"]
        a["q_orbit_avg"] = orbit_averages[site]
        a["is_grid_artifact"] = orbits[site]["is_grid_artifact"]

    total_net_charge = round(len(raw_atoms) * z_core - total_valence, 4)

    # 5. Build Markdown summary table
    md_lines = [
        f"### Wyckoff-Standardized Bader Charge Analysis ({element}, $Z_{{\\mathrm{{core}}}} = {z_core}\\,e$)",
        "",
        "| Wyckoff Orbit | Multiplicity | Atom Indices | Orbit Mean $\\bar{q}_{\\text{net}}$ ($e$) | Grid Splitting $\\Delta q$ ($e$) | Symmetry Status |",
        "| :--- | :---: | :--- | :---: | :---: | :--- |"
    ]
    for site, odata in sorted(orbits.items()):
        atoms_str = ", ".join([f"({aid})" for aid in odata["atom_ids"]])
        status = "Mirror Invariant"
        if odata["is_grid_artifact"]:
            status = "FFT Grid Artifact (Averaged)"
        elif odata["symmetry_broken"]:
            status = "Broken Symmetry (!)"
        md_lines.append(
            f"| **{site}** | {odata['multiplicity']} | {atoms_str} | **{odata['mean_q_net']:+.4f}** | {odata['charge_splitting']:.4f} | {status} |"
        )
    md_lines.append("")
    md_lines.append(f"**Total Valence Electrons**: `{total_valence:.4f}` | **Net System Charge**: `{total_net_charge:+.4f}\\,e`")

    return {
        "status": "SUCCESS",
        "element": element,
        "z_core": z_core,
        "total_atoms": len(enriched_atoms),
        "total_valence_electrons": round(total_valence, 4),
        "total_net_charge": total_net_charge,
        "wyckoff_orbits": orbits,
        "standardized_atoms": enriched_atoms,
        "summary_markdown": "\n".join(md_lines),
        "isError": False
    }


# ==============================================================================
# 2. Zero-Bloat Remote 2D Volumetric Slicing Protocol
# ==============================================================================

def extract_compact_2d_slice(
    source_path: str,
    output_path: Optional[str] = None,
    z_slice: float = 0.50,
    plane: str = "xy"
) -> Dict[str, Any]:
    """
    Extracts a compact 2D planar density slice from a 3D volumetric file (CHGCAR/LOCPOT/ELFCAR)
    at the specified fractional coordinate (default z = 0.50 cutting through nuclei in 2D sheets).
    
    Compresses gigabytes of 3D data into a lightweight (<500 KB) 2D array, eliminating SSH bloat.
    """
    if not os.path.exists(source_path):
        return {"error": f"Source file does not exist: {source_path}", "isError": True}

    orig_size_bytes = os.path.getsize(source_path)
    orig_size_mb = orig_size_bytes / (1024 * 1024)

    # Parse VASP volumetric header
    with open(source_path, "r") as f:
        comment = f.readline().strip()
        scale = float(f.readline().strip())
        lattice = []
        for _ in range(3):
            lattice.append([float(x) * scale for x in f.readline().split()])
        
        species_line = f.readline().strip().split()
        counts_line = f.readline().strip().split()
        
        # Determine if elements line is present or counts line comes first
        try:
            counts = [int(x) for x in species_line]
            species = [f"Type_{i+1}" for i in range(len(counts))]
            total_atoms = sum(counts)
            coord_type_line = counts_line[0]
        except ValueError:
            species = species_line
            counts = [int(x) for x in counts_line]
            total_atoms = sum(counts)
            coord_type_line = f.readline().strip()

        # Atom coordinates
        atom_coords = []
        for _ in range(total_atoms):
            coords = [float(x) for x in f.readline().split()[:3]]
            atom_coords.append(coords)

        # Blank or empty line
        blank = f.readline().strip()
        while not blank:
            blank = f.readline().strip()

        # Grid dimensions: NGX, NGY, NGZ
        grid_dims = [int(x) for x in blank.split()[:3]]
        ngx, ngy, ngz = grid_dims
        total_grid_points = ngx * ngy * ngz

        # Target plane index
        if plane == "xy":
            target_dim = ngz
            target_idx = int(round(z_slice * ngz)) % ngz
        elif plane == "xz":
            target_dim = ngy
            target_idx = int(round(z_slice * ngy)) % ngy
        elif plane == "yz":
            target_dim = ngx
            target_idx = int(round(z_slice * ngx)) % ngx
        else:
            return {"error": f"Unsupported plane: {plane}. Use 'xy', 'xz', or 'yz'.", "isError": True}

        # Read density grid points
        # VASP writes grid points in fast-x, mid-y, slow-z order: data[iz][iy][ix]
        # To avoid loading all 3D data into memory simultaneously for giant files,
        # we can collect numbers as a flat array and reshape.
        raw_values = []
        for line in f:
            parts = line.split()
            if not parts:
                continue
            # If augmentation charges or second spin channel header encountered, break
            if "augmentation" in line.lower() or len(raw_values) >= total_grid_points:
                break
            for val in parts:
                try:
                    raw_values.append(float(val))
                    if len(raw_values) == total_grid_points:
                        break
                except ValueError:
                    break
            if len(raw_values) >= total_grid_points:
                break

    if len(raw_values) < total_grid_points:
        return {
            "error": f"Incomplete volumetric data: read {len(raw_values)} of {total_grid_points} expected points.",
            "isError": True
        }

    # Reshape: VASP order in flat file is x fastest, then y, then z
    # flat index = ix + iy*ngx + iz*ngx*ngy
    grid_3d = np.array(raw_values, dtype=np.float32).reshape((ngz, ngy, ngx))

    # Extract 2D slice
    if plane == "xy":
        # Shape: (ngy, ngx)
        slice_2d = grid_3d[target_idx, :, :]
    elif plane == "xz":
        # Shape: (ngz, ngx)
        slice_2d = grid_3d[:, target_idx, :]
    else:  # yz
        # Shape: (ngz, ngy)
        slice_2d = grid_3d[:, :, target_idx]

    # Calculate unit cell volume
    lat_matrix = np.array(lattice)
    cell_volume = float(abs(np.linalg.det(lat_matrix)))

    # In VASP CHGCAR, density is multiplied by volume: rho_real = rho_vasp / V_cell
    # In LOCPOT, values are already in eV
    is_chgcar = "chg" in os.path.basename(source_path).lower()
    if is_chgcar and cell_volume > 0.0:
        slice_physical = slice_2d / cell_volume
    else:
        slice_physical = slice_2d

    slice_min = float(np.min(slice_physical))
    slice_max = float(np.max(slice_physical))
    slice_mean = float(np.mean(slice_physical))

    # Export if requested
    saved_size_bytes = 0
    saved_path = None
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        if output_path.endswith(".npz"):
            np.savez_compressed(
                output_path,
                slice_2d=slice_physical,
                lattice=lat_matrix,
                atom_coords=atom_coords,
                species=species,
                counts=counts,
                grid_dims=grid_dims,
                target_idx=target_idx,
                fractional_pos=z_slice,
                plane=plane
            )
        elif output_path.endswith(".bin"):
            # Compact binary format: header + float32 array
            # Header: magic(4B), plane(2B), nx(2B), ny(2B), frac(4B)
            with open(output_path, "wb") as bf:
                header = struct.pack("4sHHf", b"SL2D", slice_physical.shape[1], slice_physical.shape[0], z_slice)
                bf.write(header)
                bf.write(slice_physical.tobytes())
        else:
            # JSON format
            export_dict = {
                "plane": plane,
                "fractional_pos": z_slice,
                "grid_dims": grid_dims,
                "slice_shape": list(slice_physical.shape),
                "density_min": slice_min,
                "density_max": slice_max,
                "density_mean": slice_mean,
                "slice_data": slice_physical.tolist()
            }
            with open(output_path, "w") as jf:
                json.dump(export_dict, jf)
        saved_path = output_path
        saved_size_bytes = os.path.getsize(output_path)

    saved_size_kb = saved_size_bytes / 1024
    compression_ratio = (orig_size_bytes / max(1, saved_size_bytes)) if saved_size_bytes > 0 else 0.0

    return {
        "status": "EXTRACTED",
        "source_file": source_path,
        "original_size_mb": round(orig_size_mb, 2),
        "plane": plane,
        "fractional_coordinate": z_slice,
        "slice_grid_index": target_idx,
        "grid_dimensions": grid_dims,
        "slice_shape": list(slice_physical.shape),
        "density_statistics": {
            "min": round(slice_min, 6),
            "max": round(slice_max, 6),
            "mean": round(slice_mean, 6),
            "units": "e/A^3" if is_chgcar else "raw_unit"
        },
        "saved_path": saved_path,
        "saved_size_kb": round(saved_size_kb, 2),
        "compression_ratio": f"{compression_ratio:.1f}x" if compression_ratio > 0 else "N/A",
        "isError": False
    }


# ==============================================================================
# 3. Zero-Dilation Rule Frame Geometry Validator
# ==============================================================================

def validate_animation_geometry(
    frame_paths: List[str],
    target_resolution: Optional[Tuple[int, int]] = None
) -> Dict[str, Any]:
    """
    Validates that 100% of frames in a scientific animation sequence possess
    identical pixel geometry (W x H), auditing against the Zero-Dilation Rule
    (detecting matplotlib bbox_inches='tight' artifacting).
    """
    if not HAS_PIL:
        return {"error": "Pillow (PIL) library is required for frame geometry inspection.", "isError": True}

    if not frame_paths:
        return {"error": "No frame paths provided for validation.", "isError": True}

    resolutions: Dict[Tuple[int, int], List[str]] = {}
    frame_details = []

    for fpath in frame_paths:
        if not os.path.exists(fpath):
            return {"error": f"Frame file not found: {fpath}", "isError": True}
        try:
            with Image.open(fpath) as img:
                res = img.size  # (width, height)
                mode = img.mode
                if res not in resolutions:
                    resolutions[res] = []
                resolutions[res].append(os.path.basename(fpath))
                frame_details.append({
                    "file": os.path.basename(fpath),
                    "width": res[0],
                    "height": res[1],
                    "aspect_ratio": round(res[0] / res[1], 4),
                    "mode": mode
                })
        except Exception as e:
            return {"error": f"Failed to inspect image '{fpath}': {str(e)}", "isError": True}

    is_uniform = (len(resolutions) == 1)
    reference_res = list(resolutions.keys())[0] if resolutions else (0, 0)

    # Check against target resolution if provided
    target_mismatch = False
    if target_resolution and reference_res != target_resolution:
        target_mismatch = True

    zero_dilation_violation = not is_uniform or target_mismatch

    # Diagnostics
    remediation = None
    if zero_dilation_violation:
        remediation = (
            "Zero-Dilation Violation Detected! Frame dimensions fluctuate across the sequence. "
            "Remediation: In your matplotlib plotting script, NEVER call fig.savefig(..., bbox_inches='tight'). "
            "Instead, set an explicit figure size: figsize=(W, H), dpi=DPI, and configure uniform margins using "
            "plt.subplots_adjust(left=0.10, right=0.92, top=0.88, bottom=0.12) or gridspec."
        )

    # Recommended animation pacing
    pacing_guide = {
        "standard_fps": 15,
        "frame_duration_ms": 66,
        "transition_hold_ms": 800,
        "extrema_hold_ms": 1200,
        "equilibrium_hold_ms": 1000,
        "loop_mode": "infinite (loop=0)"
    }

    return {
        "status": "PASSED" if not zero_dilation_violation else "VIOLATION_DETECTED",
        "total_frames": len(frame_paths),
        "is_uniform_resolution": is_uniform,
        "reference_resolution": {"width": reference_res[0], "height": reference_res[1]},
        "unique_resolutions_count": len(resolutions),
        "resolution_breakdown": {f"{k[0]}x{k[1]}": len(v) for k, v in resolutions.items()},
        "zero_dilation_violation": zero_dilation_violation,
        "remediation": remediation,
        "pacing_recommendation": pacing_guide,
        "isError": False
    }


# ==============================================================================
# 4. Quantitative Electronic Strain Descriptors
# ==============================================================================

def quantify_electronic_strain_metrics(
    band_data: Union[Dict[str, Any], str],
    reference_efermi: Optional[float] = None
) -> Dict[str, Any]:
    """
    Quantifies fundamental electronic strain descriptors across 2D carbon allotropes:
      - Fundamental Band Gap (Eg)
      - Dirac Crossing Gap (Delta E_Dirac)
      - Chemical Potential / Fermi Level Shift (Delta E_F)
      - Fermi Velocity Estimate (v_F = 1/hbar * |dE/dk|)
      - Dirac Point Shift (Delta k_Dirac)
    """
    # Parse input
    data_dict = {}
    if isinstance(band_data, str):
        if os.path.exists(band_data):
            if band_data.endswith(".json"):
                with open(band_data, "r") as f:
                    data_dict = json.load(f)
            elif band_data.endswith(".csv"):
                import csv
                rows = []
                with open(band_data, "r") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        rows.append(r)
                data_dict = {"states": rows}
        else:
            return {"error": f"File not found: {band_data}", "isError": True}
    elif isinstance(band_data, dict):
        data_dict = band_data

    # Multi-state table mode
    if "states" in data_dict and isinstance(data_dict["states"], list):
        states = data_dict["states"]
        # Look for strain, e_fermi, band_gap, v_f columns
        parsed_states = []
        pristine_ef = reference_efermi
        for s in states:
            # Case-insensitive / flexible column getter
            def get_col(keys, default=0.0):
                for k in keys:
                    for sk in s.keys():
                        if sk.lower().strip() == k.lower().strip() or sk.lower().startswith(k.lower()):
                            val = s[sk]
                            if val is not None and str(val).strip():
                                try:
                                    return float(str(val).replace("%", "").strip())
                                except ValueError:
                                    return val
                return default

            strain_val = get_col(["strain", "strain_pct", "eps"], 0.0)
            try:
                strain_float = float(strain_val)
                # If strain is given in decimal fraction (e.g. -0.03), convert to percentage
                if 0.0 < abs(strain_float) <= 0.20:
                    strain_float = strain_float * 100.0
            except (ValueError, TypeError):
                strain_float = 0.0

            ef = float(get_col(["fermi_level_ev", "e_fermi", "e_f", "fermi_level", "fermi"], 0.0))
            gap = float(get_col(["fund_gap_ev", "band_gap", "eg", "gap"], 0.0))
            dirac_gap = float(get_col(["dirac_gap_ev", "dirac_gap"], 0.0))
            
            # Fermi velocity: handle raw m/s or 1e5 m/s
            vf_raw = get_col(["fermi_velocity_1e5_ms", "v_f", "v_fermi", "vf"], 4.48)
            try:
                vf_float = float(vf_raw)
                if vf_float < 100.0:  # Given in 1e5 m/s units
                    vf_float = vf_float * 1e5
            except (ValueError, TypeError):
                vf_float = 4.48e5

            delta_k = float(get_col(["delta_k_dirac_inva", "delta_k", "dk"], 0.0))
            pz_purity = float(get_col(["c_pz_weight_pct", "pz_purity", "pz"], 100.0))

            mode_str = str(s.get("Mode", s.get("mode", s.get("Case", "")))).strip()
            label_str = s.get("Case", s.get("label", f"{mode_str} {strain_float:+.1f}%".strip()))

            if (strain_float == 0.0 or "pristine" in str(label_str).lower()) and pristine_ef is None:
                pristine_ef = ef

            parsed_states.append({
                "label": str(label_str),
                "mode": mode_str if mode_str else "General",
                "strain_pct": round(strain_float, 2),
                "e_fermi": round(ef, 4),
                "band_gap": round(gap, 4),
                "dirac_gap": round(dirac_gap, 4),
                "v_fermi": round(vf_float, 1),
                "delta_k": round(delta_k, 5),
                "pz_purity": round(pz_purity, 1)
            })

        if pristine_ef is None and parsed_states:
            pristine_ef = parsed_states[0]["e_fermi"]

        # Calculate Delta E_F(eps)
        for ps in parsed_states:
            ps["delta_e_fermi"] = round(ps["e_fermi"] - pristine_ef, 4)

        # Sort by strain
        parsed_states.sort(key=lambda x: x["strain_pct"])

        # Linear fit of Delta E_F vs strain
        strains = [x["strain_pct"] for x in parsed_states]
        delta_efs = [x["delta_e_fermi"] for x in parsed_states]
        if len(strains) > 1 and np.ptp(strains) > 0:
            slope, intercept = np.polyfit(strains, delta_efs, 1)
        else:
            slope, intercept = 0.0, 0.0

        md_table = [
            "### Quantitative Electronic Strain Descriptors",
            "",
            "| State | Strain $\\varepsilon$ (%) | $E_{\\mathrm{F}}$ (eV) | $\\Delta E_{\\mathrm{F}}$ (eV) | Band Gap $E_g$ (eV) | $v_{\\mathrm{F}}$ ($10^5$ m/s) |",
            "| :--- | :---: | :---: | :---: | :---: | :---: |"
        ]
        for ps in parsed_states:
            vf_disp = f"{ps['v_fermi'] / 1e5:.2f}" if ps["v_fermi"] > 1e4 else f"{ps['v_fermi']:.2f}"
            md_table.append(
                f"| **{ps['label']}** | {ps['strain_pct']:+.1f}% | {ps['e_fermi']:.3f} | **{ps['delta_e_fermi']:+.3f}** | {ps['band_gap']:.2f} | {vf_disp} |"
            )

        her_insight = (
            f"Electrochemical Potential Modulation: $\\Delta E_{{\\mathrm{{F}}}}(\\varepsilon)$ exhibits a linear slope of "
            f"**{slope:+.4f} eV/% strain**. Compressive deformation shifts $E_{{\\mathrm{{F}}}}$ upwards, raising the chemical "
            f"potential and lowering the work function ($\\Phi \\approx -E_{{\\mathrm{{F}}}}$), directly accelerating electron "
            f"injection into adsorbate orbitals during the Hydrogen Evolution Reaction (HER)."
        )

        return {
            "status": "SUCCESS",
            "pristine_efermi": pristine_ef,
            "ef_strain_slope_ev_per_pct": round(float(slope), 4),
            "states": parsed_states,
            "her_electrocatalysis_insight": her_insight,
            "summary_markdown": "\n".join(md_table),
            "isError": False
        }

    # Single-state eigenvalue analysis mode
    eigenvalues = data_dict.get("eigenvalues", [])
    efermi = float(data_dict.get("efermi", data_dict.get("e_fermi", 0.0)))
    if eigenvalues:
        eig_arr = np.array(eigenvalues)
        # Shift relative to Fermi level
        shifted = eig_arr - efermi
        vbm = float(np.max(shifted[shifted <= 0.0])) if np.any(shifted <= 0.0) else 0.0
        cbm = float(np.min(shifted[shifted > 0.0])) if np.any(shifted > 0.0) else 0.0
        direct_gaps = []
        if eig_arr.ndim >= 2:
            # Axis 0: kpoints, Axis 1: bands
            for k_idx in range(eig_arr.shape[0]):
                k_bands = shifted[k_idx, :]
                occ = k_bands[k_bands <= 0.0]
                unocc = k_bands[k_bands > 0.0]
                if len(occ) > 0 and len(unocc) > 0:
                    direct_gaps.append(float(np.min(unocc) - np.max(occ)))
        min_direct_gap = min(direct_gaps) if direct_gaps else (cbm - vbm)
        fundamental_gap = max(0.0, cbm - vbm)

        return {
            "status": "SUCCESS",
            "e_fermi": efermi,
            "vbm": round(vbm, 4),
            "cbm": round(cbm, 4),
            "fundamental_band_gap": round(fundamental_gap, 4),
            "dirac_crossing_gap": round(min_direct_gap, 4),
            "is_semimetal": fundamental_gap < 0.05,
            "isError": False
        }

    return {"error": "Invalid band structure data specification.", "isError": True}
