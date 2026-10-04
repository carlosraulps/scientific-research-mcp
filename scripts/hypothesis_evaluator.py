#!/usr/bin/env python3
"""
================================================================================
Hypothesis Evaluator (hypothesis_evaluator.py)
================================================================================
Multi-dimensional evaluation engine for scientific hypotheses and simulation plans.
Directly grounded in LLM4SR (Luo et al., 2025) and HKUST Autonomy Survey (2025).

Evaluates across 4 core dimensions:
1. Novelty (0-25): Differentiates from existing facts/traps in lifelong memory.
2. Validity (0-25): Thermodynamic plausibility, physical laws, and empirical rules.
3. Clarity (0-25): Quantitative specificity, explicit observables, and falsifiability.
4. Feasibility (0-25): Computational tractability, engine support, convergence likelihood.
================================================================================
"""

import os
import sys
import re
import json
import sqlite3
from typing import Dict, Any, List, Optional


class HypothesisEvaluator:
    """Evaluates proposed scientific hypotheses and simulation workflows against rigorous criteria."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.base_dir, "memory", "facts_memory.db")

    def _query_similar_facts(self, text: str) -> List[Dict[str, Any]]:
        """Searches SQLite lifelong memory for existing facts or traps related to the text."""
        if not os.path.exists(self.db_path):
            return []
        
        words = [w.lower() for w in re.findall(r"\b[A-Za-z0-9_-]{3,}\b", text) if w.lower() not in {
            "the", "and", "for", "with", "this", "that", "from", "using", "calculation", "simulation", "system"
        }]
        if not words:
            return []

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        matched = []
        try:
            query = "SELECT * FROM facts"
            cursor.execute(query)
            for row in cursor.fetchall():
                row_text = f"{row['material_or_system']} {row['statement']} {row.get('remediation', '')}".lower()
                matches = sum(1 for w in words if w in row_text)
                if matches > 0:
                    matched.append({
                        "id": row["id"],
                        "category": row["category"],
                        "title": row["material_or_system"],
                        "matches": matches,
                        "description": row["statement"]
                    })
        except Exception:
            pass
        finally:
            conn.close()

        matched.sort(key=lambda x: x["matches"], reverse=True)
        return matched[:5]

    def evaluate_hypothesis(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Runs the 4-dimensional audit and returns a comprehensive scorecard."""
        context = context or {}
        text_lower = text.lower()

        # 1. NOVELTY AUDIT (0 - 25)
        # Search memory to see if this is an already solved problem or known trap
        similar_items = self._query_similar_facts(text)
        novelty_score = 25.0
        novelty_feedback = []

        if not similar_items:
            novelty_feedback.append("No identical prior calculation found in lifelong memory; hypothesis addresses an unmapped parameter space.")
        else:
            top_match = similar_items[0]
            if top_match["category"] == "trap":
                novelty_score -= 10.0
                novelty_feedback.append(f"Caution: Closely related to known fatal trap '{top_match['title']}'. Must incorporate counter-measures.")
            elif top_match["category"] == "benchmark":
                novelty_score -= 8.0
                novelty_feedback.append(f"Reference overlap with benchmark '{top_match['title']}'. Ensure original insight beyond standard reference.")
            else:
                novelty_score -= 4.0
                novelty_feedback.append(f"Builds upon related known system/rule: '{top_match['title']}'.")

        # 2. VALIDITY AUDIT (0 - 25)
        validity_score = 25.0
        validity_feedback = []

        # Check for polymer/extended systems and Pulay mixing rule
        is_extended_or_polymer = any(w in text_lower for w in ["polymer", "extended", "nanotube", "ribbon", "surface", "slab", "c2n", "photh"])
        has_pulay_or_mixing = any(w in text_lower for w in ["pulay", "mixing", "mixingweight", "dm.numberpulay", "amix", "bmix"])

        if is_extended_or_polymer and not has_pulay_or_mixing:
            validity_score -= 6.0
            validity_feedback.append("Missing charge sloshing prevention: Extended/polymer 2D systems require explicit Pulay mixing (e.g. DM.NumberPulay 5, DM.MixingWeight 0.04 in SIESTA, or AMIX/BMIX in VASP).")

        # Check for conservation/unphysical claims
        if any(w in text_lower for w in ["perpetual", "negative kelvin", "exceeds c", "zero mass"]):
            validity_score -= 20.0
            validity_feedback.append("Fatal physical invalidity: unphysical or non-conservative claim detected.")

        # Check for magnetic moment without spin polarization
        if ("magnetic" in text_lower or "ferro" in text_lower or "spin" in text_lower) and not any(w in text_lower for w in ["ispin=2", "spin-polarized", "spin polarized", "unrestricted", "spin: collinear"]):
            validity_score -= 5.0
            validity_feedback.append("Spin-state claim made without specifying spin-polarized calculation flag (e.g. ISPIN=2 or Spin.SpinPolarized).")

        if not validity_feedback:
            validity_feedback.append("Hypothesis adheres to physical conservation laws and established DFT/MD constraints.")

        # 3. CLARITY & OPERATIONAL SPECIFICITY (0 - 25)
        # Yang et al. (2025): hypotheses must be testable with concrete quantitative targets
        clarity_score = 25.0
        clarity_feedback = []

        # Check for quantitative numbers (thresholds, values, eV, Angstrom, GPa, K)
        has_units = bool(re.search(r"\b(\d+(\.\d+)?)\s*(ev|å|angstrom|gpa|k|kelvin|fs|ps|ns|mev|ry|ha)\b", text_lower))
        if not has_units:
            clarity_score -= 7.0
            clarity_feedback.append("Lacks explicit physical units (e.g. eV, Å, GPa, K, fs). Quantitative bounds are required for empirical falsifiability.")

        # Check for named target systems or chemical formulae
        has_formula = bool(re.search(r"\b[A-Z][a-z]?\d*([A-Z][a-z]?\d*)+\b", text))
        if not has_formula and not any(w in text_lower for w in ["graphene", "silicene", "phosphorene", "diamond", "perovskite", "mof"]):
            clarity_score -= 6.0
            clarity_feedback.append("No specific chemical formula or crystalline allotrope identified; hypothesis remains overly abstract.")

        # Check for concrete observable / metric
        has_metric = any(w in text_lower for w in ["band gap", "formation energy", "adsorption energy", "stress", "elastic modulus", "phonons", "dos", "work function", "bader", "charge transfer"])
        if not has_metric:
            clarity_score -= 6.0
            clarity_feedback.append("No explicit measurable observable specified (e.g. band gap, formation energy, adsorption energy, work function).")

        if not clarity_feedback:
            clarity_feedback.append("High operational clarity: contains concrete formulas, quantitative bounds, and measurable endpoints.")

        # 4. FEASIBILITY AUDIT (0 - 25)
        feasibility_score = 25.0
        feasibility_feedback = []

        # Check software engine
        has_engine = any(w in text_lower for w in ["vasp", "siesta", "lammps", "qe", "quantum espresso", "orca", "ase", "cp2k"])
        if not has_engine:
            feasibility_score -= 5.0
            feasibility_feedback.append("No computational simulation engine designated (e.g. VASP, SIESTA, LAMMPS, QE, ORCA).")

        # Check excessive k-points or box size if mentioned
        if "100x100" in text_lower or "100000 atoms" in text_lower:
            feasibility_score -= 10.0
            feasibility_feedback.append("Extreme computational cost: requested grid or atom count exceeds feasible turnaround times.")

        if not feasibility_feedback:
            feasibility_feedback.append("Feasible execution: methodology fits standard high-performance computing envelopes.")

        total_score = round(novelty_score + validity_score + clarity_score + feasibility_score, 1)
        passed = (
            total_score >= 75.0 and
            validity_score >= 18.0 and
            clarity_score >= 14.0 and
            feasibility_score >= 18.0
        )

        return {
            "total_score": total_score,
            "passed": passed,
            "breakdown": {
                "novelty": {"score": max(0.0, novelty_score), "max": 25.0, "feedback": novelty_feedback},
                "validity": {"score": max(0.0, validity_score), "max": 25.0, "feedback": validity_feedback},
                "clarity": {"score": max(0.0, clarity_score), "max": 25.0, "feedback": clarity_feedback},
                "feasibility": {"score": max(0.0, feasibility_score), "max": 25.0, "feedback": feasibility_feedback}
            },
            "recommendation": "PROCEED" if passed else "REFINE_HYPOTHESIS",
            "matched_historical_facts": similar_items
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 hypothesis_evaluator.py '<hypothesis_text>'")
        sys.exit(1)

    evaluator = HypothesisEvaluator()
    res = evaluator.evaluate_hypothesis(sys.argv[1])
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["passed"] else 1)
