#!/usr/bin/env python3
"""
================================================================================
Liu et al. Lifelong Facts & Traps Memory Subsystem
================================================================================
Stores empirical knowledge about the physical world, computational traps,
and boundary conditions that must persist across sessions, projects, and
foundation model migrations.
================================================================================
"""

import os
import sys
import json
import sqlite3
import datetime
from typing import Dict, Any, List, Optional


class FactsStore:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.memory_dir = os.path.join(self.base_dir, "memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        self.db_path = os.path.join(self.memory_dir, "facts_memory.db")
        self._init_db()
        self._seed_reference_traps()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,          -- 'trap', 'empirical_rule', 'boundary_condition', 'benchmark'
                material_or_system TEXT NOT NULL,
                statement TEXT NOT NULL,
                remediation TEXT,
                confidence REAL DEFAULT 1.0,
                source_ref TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_cat ON facts(category)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_mat ON facts(material_or_system)")
        conn.commit()
        conn.close()

    def _seed_reference_traps(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM facts")
        count = cur.fetchone()[0]
        if count == 0:
            now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            seeds = [
                (
                    "trap", "Pt(111) CO adsorption",
                    "CO adsorption on Pt(111) surface slabs requires dipole correction along the z-axis (LDIPOL = .TRUE., IDIPOL = 3 in VASP) and a minimum vacuum spacing of 15 A to prevent spurious slab-slab dipole interactions.",
                    "Set LDIPOL = .TRUE., IDIPOL = 3, and verify vacuum length >= 15 A.",
                    1.0, "DREAMS (Wang et al., 2026)", now_iso, now_iso
                ),
                (
                    "trap", "Magnetic Iron (BCC Fe)",
                    "Default non-spin-polarized initialization in transition metals fails to break symmetry, leading to an unphysical non-magnetic ground state.",
                    "Set ISPIN = 2 and MAGMOM = 2.2 for each Fe atom in INCAR.",
                    1.0, "TRITONDFT (Hu et al., 2026)", now_iso, now_iso
                ),
                (
                    "trap", "Perovskite SrTiO3",
                    "Standard PBE functional underestimates band gap (~1.8 eV vs. experimental 3.25 eV) and can mischaracterize octahedral tilting without tight k-mesh.",
                    "Use HSE06 hybrid functional or calibrated DFT+U for band edge alignment.",
                    0.95, "Materials Project / QUESTDB", now_iso, now_iso
                ),
                (
                    "boundary_condition", "Hydrogenous MD Simulations",
                    "Molecular dynamics timesteps exceeding 1.0 fs cause high-frequency O-H or C-H bond stretching instabilities and numerical explosion.",
                    "Cap timestep at 0.5 - 1.0 fs, or apply SHAKE / RATTLE bond constraints.",
                    1.0, "MDCrow / MDAgent (Shi et al., 2025)", now_iso, now_iso
                ),
                (
                    "empirical_rule", "Transition Metal Adsorption (Charge Sloshing)",
                    "High default mixing parameters (AMIX > 0.4 or mixing_beta > 0.5) trigger persistent SCF charge sloshing oscillations on narrow-gap metallic surfaces.",
                    "Reduce AMIX to 0.2 (VASP) or mixing_beta to 0.3 with local-TF (Quantum ESPRESSO).",
                    1.0, "DREAMS (Wang et al., 2026)", now_iso, now_iso
                )
            ]
            cur.executemany("""
                INSERT INTO facts (category, material_or_system, statement, remediation, confidence, source_ref, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, seeds)
            conn.commit()
        conn.close()

    def save_fact(
        self,
        category: str,
        material_or_system: str,
        statement: str,
        remediation: Optional[str] = None,
        confidence: float = 1.0,
        source_ref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Records an empirical fact, failure warning, or boundary condition into lifelong memory.
        """
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO facts (category, material_or_system, statement, remediation, confidence, source_ref, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (category, material_or_system, statement, remediation, confidence, source_ref, now_iso, now_iso))
        fact_id = cur.lastrowid
        conn.commit()
        conn.close()

        return {
            "status": "STORED",
            "fact_id": fact_id,
            "category": category,
            "material_or_system": material_or_system,
            "isError": False
        }

    def search_facts(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        material_or_system: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves matching facts and warnings before launching expensive workflows.
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        sql = "SELECT id, category, material_or_system, statement, remediation, confidence, source_ref, created_at FROM facts WHERE 1=1"
        params = []

        if category:
            sql += " AND category = ?"
            params.append(category)

        if material_or_system:
            sql += " AND (LOWER(material_or_system) LIKE ? OR LOWER(material_or_system) LIKE ?)"
            params.append(f"%{material_or_system.lower()}%")
            params.append(f"%{material_or_system.lower().replace(' ', '')}%")

        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()

        results = []
        for r in rows:
            entry = {
                "id": r[0],
                "category": r[1],
                "material_or_system": r[2],
                "statement": r[3],
                "remediation": r[4],
                "confidence": r[5],
                "source_ref": r[6],
                "created_at": r[7]
            }
            if query:
                q_lower = query.lower()
                combined = f"{r[1]} {r[2]} {r[3]} {r[4] or ''}".lower()
                if q_lower not in combined:
                    continue
            results.append(entry)

        return {
            "query": query,
            "category": category,
            "material_or_system": material_or_system,
            "total_matches": len(results),
            "facts": results,
            "isError": False
        }
