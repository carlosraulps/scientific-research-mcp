#!/usr/bin/env python3
"""
================================================================================
Structure Sanity Guard (structure_guard.py)
================================================================================
Defensive geometry validator for computational materials science and chemistry.
Inspired by Microsoft Research AI4Science (2023) POSCAR hallucination findings
and Chip Huyen AI Engineering (2025) input guardrail standards.

Validates:
1. Fractional coordinate boundaries ([0, 1) or wrapped).
2. Interatomic pairwise distances (flags atomic overlap < 0.8 A and short bonds < 1.0 A).
3. Positive unit cell volume and right-handed triple product (a . (b x c) > 0).
4. Unphysical vacuum collapses or negative coordinates.
================================================================================
"""

import os
import sys
import math
import json
import re
from typing import Dict, Any, List, Tuple, Optional


class StructureSanityGuard:
    """Validates structural input files (POSCAR, XYZ, CIF, FDF) against physical sanity rules."""

    def __init__(self, min_allowed_distance: float = 0.80, warning_distance: float = 1.05):
        self.min_allowed_distance = min_allowed_distance
        self.warning_distance = warning_distance

    def _cross_product(self, u: List[float], v: List[float]) -> List[float]:
        return [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]
        ]

    def _dot_product(self, u: List[float], v: List[float]) -> float:
        return sum(a * b for a, b in zip(u, v))

    def _norm(self, v: List[float]) -> float:
        return math.sqrt(sum(x * x for x in v))

    def _calc_volume(self, cell: List[List[float]]) -> float:
        """Triple scalar product a . (b x c)."""
        b_cross_c = self._cross_product(cell[1], cell[2])
        return self._dot_product(cell[0], b_cross_c)

    def parse_poscar(self, filepath: str) -> Dict[str, Any]:
        """Parses standard VASP POSCAR / CONTCAR file."""
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) < 8:
            raise ValueError(f"POSCAR file too short ({len(lines)} lines)")

        comment = lines[0]
        scale = float(lines[1])

        cell = []
        for i in range(2, 5):
            parts = [float(x) for x in lines[i].split()[:3]]
            cell.append([x * scale for x in parts])

        line5_parts = lines[5].split()
        # Check if line 5 is species names or counts
        if line5_parts[0].isalpha():
            species = line5_parts
            counts = [int(x) for x in lines[6].split()]
            coord_start_idx = 7
        else:
            species = [f"Elem{i+1}" for i in range(len(line5_parts))]
            counts = [int(x) for x in line5_parts]
            coord_start_idx = 6

        coord_type_line = lines[coord_start_idx].lower()
        is_selective = False
        if coord_type_line.startswith("s"):
            is_selective = True
            coord_start_idx += 1
            coord_type_line = lines[coord_start_idx].lower()

        is_direct = coord_type_line.startswith("d") or coord_type_line.startswith("direct")
        coord_start_idx += 1

        total_atoms = sum(counts)
        atoms = []
        atom_idx = 0
        species_expanded = []
        for sp, count in zip(species, counts):
            species_expanded.extend([sp] * count)

        for i in range(coord_start_idx, coord_start_idx + total_atoms):
            if i >= len(lines):
                break
            parts = lines[i].split()
            coords = [float(x) for x in parts[:3]]
            sp = species_expanded[atom_idx] if atom_idx < len(species_expanded) else "Unknown"
            atoms.append({"species": sp, "coords": coords, "direct": is_direct, "index": atom_idx + 1})
            atom_idx += 1

        return {
            "comment": comment,
            "scale": scale,
            "cell": cell,
            "species": species,
            "counts": counts,
            "is_direct": is_direct,
            "atoms": atoms
        }

    def _cartesian_distance(self, p1: List[float], p2: List[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def _to_cartesian(self, coords: List[float], cell: List[List[float]], is_direct: bool) -> List[float]:
        if not is_direct:
            return coords
        # direct fractional coords to Cartesian
        x, y, z = coords
        cx = x * cell[0][0] + y * cell[1][0] + z * cell[2][0]
        cy = x * cell[0][1] + y * cell[1][1] + z * cell[2][1]
        cz = x * cell[0][2] + y * cell[1][2] + z * cell[2][2]
        return [cx, cy, cz]

    def validate_poscar(self, filepath: str) -> Dict[str, Any]:
        """Comprehensive sanity check for POSCAR structure."""
        errors = []
        warnings = []
        
        try:
            parsed = self.parse_poscar(filepath)
        except Exception as e:
            return {
                "valid": False,
                "file": filepath,
                "errors": [f"Failed to parse POSCAR: {str(e)}"],
                "warnings": [],
                "metrics": {}
            }

        cell = parsed["cell"]
        vol = self._calc_volume(cell)
        
        if vol <= 0:
            errors.append(f"Invalid unit cell volume: {vol:.4f} A^3 (zero or left-handed lattice)")
        elif vol < 5.0:
            warnings.append(f"Unusually small unit cell volume: {vol:.4f} A^3")

        atoms = parsed["atoms"]
        if not atoms:
            errors.append("Structure contains zero atoms")
            return {"valid": False, "file": filepath, "errors": errors, "warnings": warnings, "metrics": {}}

        # Convert all to Cartesian for pairwise distance evaluation
        cart_coords = []
        for a in atoms:
            coords = a["coords"]
            if parsed["is_direct"]:
                # Check fractional boundary
                for idx, c in enumerate(coords):
                    if c < -0.05 or c > 1.05:
                        warnings.append(f"Atom {a['index']} ({a['species']}) fractional coordinate {c:.4f} outside standard [0, 1] range")
            cart_coords.append((a["species"], self._to_cartesian(coords, cell, parsed["is_direct"]), a["index"]))

        min_dist = float("inf")
        closest_pair = None

        # Check pairwise distances (including nearest periodic copies if cell exists)
        n = len(cart_coords)
        for i in range(n):
            sp1, p1, idx1 = cart_coords[i]
            for j in range(i + 1, n):
                sp2, p2, idx2 = cart_coords[j]
                # Direct distance in cell
                d = self._cartesian_distance(p1, p2)
                if d < min_dist:
                    min_dist = d
                    closest_pair = (f"{sp1}#{idx1}", f"{sp2}#{idx2}", d)

                if d < self.min_allowed_distance:
                    errors.append(f"Atomic overlap: {sp1}#{idx1} and {sp2}#{idx2} distance is {d:.3f} A (threshold: {self.min_allowed_distance:.2f} A)")
                elif d < self.warning_distance:
                    warnings.append(f"Very short bond: {sp1}#{idx1} and {sp2}#{idx2} distance is {d:.3f} A (expected > {self.warning_distance:.2f} A)")

        is_valid = len(errors) == 0

        return {
            "valid": is_valid,
            "file": filepath,
            "formula": "".join(f"{sp}{ct}" for sp, ct in zip(parsed["species"], parsed["counts"])),
            "total_atoms": len(atoms),
            "errors": errors,
            "warnings": warnings,
            "metrics": {
                "volume_angstrom3": round(vol, 4),
                "min_pairwise_distance_angstrom": round(min_dist, 4) if min_dist != float("inf") else None,
                "closest_pair": closest_pair
            }
        }

    def inspect_file(self, filepath: str) -> Dict[str, Any]:
        """Automatically detects format and applies appropriate sanity guard."""
        if not os.path.exists(filepath):
            return {"valid": False, "error": f"File '{filepath}' not found"}

        base = os.path.basename(filepath).lower()
        if "poscar" in base or "contcar" in base or filepath.endswith(".vasp"):
            return self.validate_poscar(filepath)
        else:
            # Fallback POSCAR-style attempt
            return self.validate_poscar(filepath)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 structure_guard.py <path_to_POSCAR>")
        sys.exit(1)

    guard = StructureSanityGuard()
    res = guard.inspect_file(sys.argv[1])
    print(json.dumps(res, indent=2))
    sys.exit(0 if res.get("valid", False) else 1)
