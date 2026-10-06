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
        # Clean up any malformed empty statements
        cur.execute("DELETE FROM facts WHERE statement IS NULL OR TRIM(statement) = ''")
        conn.commit()

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
            ),
            (
                "trap", "Bader FFT Grid Origin & Wyckoff Symmetry Splitting",
                "Cartesian FFT grid discretization (NGX, NGY, NGZ) cutting across mirror planes introduces artificial charge splitting (~0.14 e) between symmetry-equivalent atoms. In planar systems like PHOTH-graphene (Pmm2), paired Wyckoff sites (e.g. C2(2) and C2(3)) appear slightly split in raw ACF.dat due to origin alignment.",
                "Group atomic basins into symmetry-inequivalent Wyckoff orbits (C_sub^(super)), average paired basins, and use Henkelman flux-weighted grid interpolation (bader -b weight) to prevent false claims of physical symmetry breaking.",
                1.0, "PHOTH-Graphene Guide (Primo et al., 2026)", now_iso, now_iso
            ),
            (
                "boundary_condition", "Scientific Animation Rendering (Zero-Dilation Rule)",
                "Using bbox_inches='tight' in matplotlib savefig dynamically recalculates the bounding box on each frame based on shifting tick labels or annotations, causing frame dilation jitter, pulsing borders, and video artifacting.",
                "Zero-Dilation Rule: Fix figure dimensions explicitly (e.g. figsize=(7, 4.2), dpi=200) without bbox_inches='tight'. Use explicit subplots_adjust or gridspec margins across all frames.",
                1.0, "PHOTH-Graphene Guide (Primo et al., 2026)", now_iso, now_iso
            ),
            (
                "empirical_rule", "Volumetric Charge Density Processing (Zero-Bloat Protocol)",
                "Downloading full 3D volumetric datasets (CHGCAR, LOCPOT, ELFCAR >30 MB to GBs each) over SSH for 2D visualization causes network saturation and disk bloat.",
                "Zero-Bloat Remote Slicing Protocol: Extract 2D compact planar slices (e.g., at invariant sheet height z = 0.50, <500 KB binary) directly on the cluster before transferring locally.",
                1.0, "PHOTH-Graphene Guide (Primo et al., 2026)", now_iso, now_iso
            ),
            (
                "empirical_rule", "Bader Net Charge Definition (PAW Core vs Valence)",
                "Net atomic Bader charge requires subtracting valence electron count from ionic core charge: q = Z_core - Q_Bader. For Carbon with PAW potentials (frozen 1s2 core), Z_core = 4.0 e. For Hydrogen, Z_core = 1.0 e. Omitting the core offset inverts polarity or confuses total valence with charge transfer.",
                "Compute q_C = 4.0 - Q_Bader(C) and q_H = 1.0 - Q_Bader(H). Verify neutral baseline Q_Bader = 4.0 e (q_C = 0.00 e).",
                1.0, "PHOTH-Graphene Guide / Henkelman Group (2026)", now_iso, now_iso
            ),
            (
                "trap", "Slurm HPC Walltime & Ghost Jobs Prevention",
                "Submitting monolithic 5-day walltime allocations (--time=5-00:00:00) blocks opportunistic backfill harvesting, severely inflates queue wait times (T_wait), and can create ghost/orphan allocations holding resources if compute processes die or hang.",
                "Micro-batch iterative workflows into 3-4 hour jobs with SIGUSR1 checkpoint traps (#SBATCH --signal=B:USR1@300) and automated CONTCAR resubmission; run periodic slurm-ghost-watchdog audits.",
                1.0, "Slurm Pre-Flight & HPC Watchdog Protocol (2026)", now_iso, now_iso
            )
        ]

        for s in seeds:
            cur.execute("SELECT id FROM facts WHERE material_or_system = ? OR statement LIKE ?", (s[1], f"%{s[2][:40]}%"))
            row = cur.fetchone()
            if not row:
                cur.execute("""
                    INSERT INTO facts (category, material_or_system, statement, remediation, confidence, source_ref, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, s)

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
