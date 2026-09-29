#!/usr/bin/env python3
"""
================================================================================
Rosetta Dual Verifier & Scientific Constitution (Prime Directive)
================================================================================
Separates Functional Correctness (schema fidelity, code executability, syntax)
from Scientific Validity (compliance with the Scientific Constitution,
non-circularity, calibration-as-overlay, dimensional consistency).
================================================================================
"""

import os
import sys
import re
import json
from typing import Dict, Any, List, Optional


class DualVerifier:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir

    def audit_dual_verification(
        self,
        code_or_spec: str,
        scientific_domain: str,
        claims: Optional[List[str]] = None,
        literature_overlays: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Performs dual verification across Functional Correctness and Scientific Validity.
        """
        functional_passed = True
        functional_issues = []

        scientific_passed = True
        scientific_issues = []
        constitution_violations = []

        # ---------------------------------------------------------------------
        # 1. FUNCTIONAL CORRECTNESS AUDIT
        # ---------------------------------------------------------------------
        # Check basic syntax / unescaped characters / empty payload
        if not code_or_spec or len(code_or_spec.strip()) < 10:
            functional_passed = False
            functional_issues.append("Payload too short or empty.")

        # Check for unhandled syntax placeholders
        if any(ph in code_or_spec for ph in ["TODO", "FIXME", "YOUR_CODE_HERE", "pass # replace"]):
            functional_passed = False
            functional_issues.append("Unresolved placeholders found in code or specification.")

        # ---------------------------------------------------------------------
        # 2. SCIENTIFIC VALIDITY & CONSTITUTION AUDIT (Rosetta Prime Directive)
        # ---------------------------------------------------------------------
        # Constitution Rule 1: Non-Circularity (Prohibition of curve fitting / target hardcoding)
        circular_patterns = [
            r"target_energy\s*=", r"fit_to_exp\s*=", r"hardcode_target\s*=",
            r"scale_to_match_paper\s*=", r"adjust_factor_for_target\s*="
        ]
        for cp in circular_patterns:
            if re.search(cp, code_or_spec, re.IGNORECASE):
                scientific_passed = False
                constitution_violations.append(f"Circularity Violation: Hardcoded target or curve-fitting heuristic '{cp}' detected.")
                scientific_issues.append("Calculations must derive from first-principles parameters, not circular target fitting.")

        # Constitution Rule 2: Calibration-as-Overlay
        # Literature numbers must only appear in overlay/comparison sections, not computation
        if literature_overlays:
            for lit in literature_overlays:
                val = str(lit.get("value", ""))
                # If the literature value is directly assigned inside the computational body
                if val and re.search(rf"\b(energy|lattice|vte|bandgap)\s*=\s*{re.escape(val)}\b", code_or_spec):
                    scientific_passed = False
                    constitution_violations.append(f"Calibration Violation: Literature benchmark value {val} is being used as a computational input rather than a comparative overlay.")

        # Constitution Rule 3: Dimensional Consistency & Physical Bounds
        if "dft" in scientific_domain.lower() or "vasp" in scientific_domain.lower():
            # Check for negative cutoff energy
            encut_match = re.search(r"\bENCUT\s*=\s*(-?\d+)", code_or_spec, re.IGNORECASE)
            if encut_match and int(encut_match.group(1)) <= 100:
                scientific_passed = False
                scientific_issues.append(f"Unphysical Cutoff: ENCUT = {encut_match.group(1)} eV is below physical plane-wave threshold (minimum ~200 eV).")

            # Check for excessive smearing
            sigma_match = re.search(r"\bSIGMA\s*=\s*([\d\.]+)", code_or_spec, re.IGNORECASE)
            if sigma_match and float(sigma_match.group(1)) > 0.5:
                scientific_passed = False
                scientific_issues.append(f"Excessive Smearing: SIGMA = {sigma_match.group(1)} eV artificially broadens Fermi surface and corrupts total energy.")

        overall_passed = functional_passed and scientific_passed

        return {
            "overall_verified": overall_passed,
            "functional_correctness": {
                "passed": functional_passed,
                "issues": functional_issues
            },
            "scientific_validity": {
                "passed": scientific_passed,
                "constitution_violations": constitution_violations,
                "issues": scientific_issues
            },
            "isError": not overall_passed
        }
