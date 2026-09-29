#!/usr/bin/env python3
"""
================================================================================
TRITONDFT Historical Memory & Symmetry-First Retrieval Engine
================================================================================
Stores and retrieves physical parameters (θ_phy: k-points, cutoff energy, smearing)
and HPC execution settings (θ_hpc: cores, nodes, kpar, ncore, walltime) from
successfully converged calculations using two-stage symmetry-first retrieval:
  1. High-level symmetry filtering (space group, crystal system)
  2. Multi-feature similarity ranking (elemental composition, volume, electrons)
Categorizes recommendations across Pareto accuracy tiers (<1, <10, <20 meV/atom).
================================================================================
"""

import os
import sys
import json
import sqlite3
import datetime
from typing import Dict, Any, List, Optional, Tuple


class HistoricalMemoryStore:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.memory_dir = os.path.join(self.base_dir, "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        self.db_path = os.path.join(self.memory_dir, "historical_memory.db")
        self._init_db()
        self._seed_reference_calculations()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historical_calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                system_name TEXT NOT NULL,
                formula TEXT NOT NULL,
                space_group TEXT,
                crystal_system TEXT,
                volume REAL,
                electron_count REAL,
                theta_phy TEXT NOT NULL,
                theta_hpc TEXT NOT NULL,
                accuracy_tier TEXT NOT NULL,
                converged_energy REAL,
                notes TEXT,
                created_at TEXT NOT NULL
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sg ON historical_calculations(space_group)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_cs ON historical_calculations(crystal_system)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tier ON historical_calculations(accuracy_tier)")
        conn.commit()
        conn.close()

    def _seed_reference_calculations(self):
        """Seeds curated reference calculations if the database is newly initialized."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM historical_calculations")
        count = cur.fetchone()[0]
        if count == 0:
            now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            seeds = [
                # FCC Transition Metal (Pt bulk - Sol27LC)
                (
                    "Pt_bulk_fcc", "Pt", "Fm-3m", "Cubic", 60.38, 10.0,
                    json.dumps({
                        "encut": 520, "kpoints": [12, 12, 12], "ismear": 1, "sigma": 0.1,
                        "potcar": "Pt", "ediff": 1e-6, "ibrion": 2, "isif": 3
                    }),
                    json.dumps({"nodes": 1, "cores": 32, "ncore": 4, "kpar": 2, "time": "02:00:00"}),
                    "high_precision", -6.048, "Converged fcc Pt bulk lattice parameter 3.924 A", now_iso
                ),
                # BCC Transition Metal (Fe bulk ferromagnetic)
                (
                    "Fe_bulk_bcc_fm", "Fe", "Im-3m", "Cubic", 24.1, 8.0,
                    json.dumps({
                        "encut": 500, "kpoints": [14, 14, 14], "ismear": 1, "sigma": 0.1,
                        "ispin": 2, "magmom": [2.2, 2.2], "ediff": 1e-6
                    }),
                    json.dumps({"nodes": 1, "cores": 32, "ncore": 4, "kpar": 2, "time": "02:00:00"}),
                    "high_precision", -8.254, "BCC Iron ground state with 2.22 mu_B spin moment", now_iso
                ),
                # Semiconductor Diamond/Zincblende (Si bulk)
                (
                    "Si_bulk_diamond", "Si", "Fd-3m", "Cubic", 40.89, 8.0,
                    json.dumps({
                        "encut": 450, "kpoints": [8, 8, 8], "ismear": 0, "sigma": 0.05,
                        "ediff": 1e-6, "isif": 3
                    }),
                    json.dumps({"nodes": 1, "cores": 16, "ncore": 4, "kpar": 1, "time": "01:00:00"}),
                    "standard", -5.421, "Silicon diamond cubic equilibrium volume", now_iso
                ),
                # Hexagonal 2D / Surface Slab (Pt(111) 4-layer slab)
                (
                    "Pt_111_slab_4L", "Pt16", "P3m1", "Hexagonal", 280.5, 160.0,
                    json.dumps({
                        "encut": 450, "kpoints": [6, 6, 1], "ismear": 1, "sigma": 0.1,
                        "ediff": 1e-5, "ediffg": -0.02, "dipol": [0, 0, 1]
                    }),
                    json.dumps({"nodes": 1, "cores": 64, "ncore": 4, "kpar": 4, "time": "04:00:00"}),
                    "high_precision", -94.85, "4-layer Pt(111) surface slab with vacuum 15 A", now_iso
                ),
                # Transition Metal Oxide Perovskite (SrTiO3)
                (
                    "SrTiO3_perovskite", "SrTiO3", "Pm-3m", "Cubic", 59.8, 40.0,
                    json.dumps({
                        "encut": 600, "kpoints": [8, 8, 8], "ismear": 0, "sigma": 0.05,
                        "ediff": 1e-6, "ldau": False
                    }),
                    json.dumps({"nodes": 1, "cores": 32, "ncore": 4, "kpar": 2, "time": "03:00:00"}),
                    "high_precision", -40.12, "Non-magnetic cubic SrTiO3 perovskite", now_iso
                )
            ]
            cur.executemany("""
                INSERT INTO historical_calculations
                (system_name, formula, space_group, crystal_system, volume, electron_count, theta_phy, theta_hpc, accuracy_tier, converged_energy, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, seeds)
            conn.commit()
        conn.close()

    def store_calculation(
        self,
        system_name: str,
        formula: str,
        space_group: Optional[str],
        crystal_system: Optional[str],
        volume: Optional[float],
        electron_count: Optional[float],
        theta_phy: Dict[str, Any],
        theta_hpc: Dict[str, Any],
        accuracy_tier: str = "standard",
        converged_energy: Optional[float] = None,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Stores physical and computational settings from a converged calculation.
        """
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO historical_calculations
            (system_name, formula, space_group, crystal_system, volume, electron_count, theta_phy, theta_hpc, accuracy_tier, converged_energy, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            system_name,
            formula,
            space_group,
            crystal_system,
            volume,
            electron_count,
            json.dumps(theta_phy),
            json.dumps(theta_hpc),
            accuracy_tier.lower(),
            converged_energy,
            notes,
            now_iso
        ))
        row_id = cur.lastrowid
        conn.commit()
        conn.close()

        return {
            "status": "STORED",
            "entry_id": row_id,
            "system_name": system_name,
            "accuracy_tier": accuracy_tier,
            "isError": False
        }

    def retrieve_similar(
        self,
        formula: Optional[str] = None,
        space_group: Optional[str] = None,
        crystal_system: Optional[str] = None,
        volume: Optional[float] = None,
        electron_count: Optional[float] = None,
        accuracy_tier: Optional[str] = None,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Two-stage retrieval:
          1. Symmetry filtering (space group / crystal system)
          2. Multi-feature similarity ranking (volume, electron count, formula)
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        query_sql = "SELECT id, system_name, formula, space_group, crystal_system, volume, electron_count, theta_phy, theta_hpc, accuracy_tier, converged_energy, notes FROM historical_calculations WHERE 1=1"
        params = []

        # Stage 1: Symmetry filter if provided
        if space_group:
            query_sql += " AND (space_group = ? OR space_group IS NULL)"
            params.append(space_group)
        elif crystal_system:
            query_sql += " AND (crystal_system = ? OR crystal_system IS NULL)"
            params.append(crystal_system)

        if accuracy_tier:
            query_sql += " AND accuracy_tier = ?"
            params.append(accuracy_tier.lower())

        cur.execute(query_sql, params)
        rows = cur.fetchall()

        # If zero matches on space group, fall back to broader crystal system or all
        if not rows and space_group and crystal_system:
            cur.execute("""
                SELECT id, system_name, formula, space_group, crystal_system, volume, electron_count, theta_phy, theta_hpc, accuracy_tier, converged_energy, notes
                FROM historical_calculations WHERE crystal_system = ?
            """, (crystal_system,))
            rows = cur.fetchall()

        if not rows:
            cur.execute("SELECT id, system_name, formula, space_group, crystal_system, volume, electron_count, theta_phy, theta_hpc, accuracy_tier, converged_energy, notes FROM historical_calculations LIMIT 10")
            rows = cur.fetchall()

        conn.close()

        # Stage 2: Feature scoring
        scored_candidates = []
        for r in rows:
            score = 0.0
            r_sg, r_cs, r_vol, r_elec, r_form = r[3], r[4], r[5], r[6], r[2]

            # Exact space group match
            if space_group and r_sg and r_sg.lower() == space_group.lower():
                score += 50.0
            # Crystal system match
            if crystal_system and r_cs and r_cs.lower() == crystal_system.lower():
                score += 25.0
            # Formula match
            if formula and r_form and formula.lower() in r_form.lower():
                score += 30.0
            # Volume similarity
            if volume and r_vol and volume > 0:
                rel_diff = abs(volume - r_vol) / max(volume, r_vol)
                score += max(0.0, 15.0 * (1.0 - rel_diff))
            # Electron count similarity
            if electron_count and r_elec and electron_count > 0:
                rel_diff = abs(electron_count - r_elec) / max(electron_count, r_elec)
                score += max(0.0, 15.0 * (1.0 - rel_diff))

            scored_candidates.append({
                "id": r[0],
                "system_name": r[1],
                "formula": r[2],
                "space_group": r[3],
                "crystal_system": r[4],
                "volume": r[5],
                "electron_count": r[6],
                "theta_phy": json.loads(r[7]),
                "theta_hpc": json.loads(r[8]),
                "accuracy_tier": r[9],
                "converged_energy": r[10],
                "notes": r[11],
                "similarity_score": round(score, 2)
            })

        scored_candidates.sort(key=lambda x: x["similarity_score"], reverse=True)
        top_matches = scored_candidates[:top_k]

        return {
            "query": {
                "formula": formula,
                "space_group": space_group,
                "crystal_system": crystal_system,
                "volume": volume,
                "electron_count": electron_count,
                "accuracy_tier": accuracy_tier
            },
            "total_evaluated": len(scored_candidates),
            "recommendations": top_matches,
            "isError": False
        }
