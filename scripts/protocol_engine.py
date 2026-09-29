#!/usr/bin/env python3
"""
================================================================================
GENIUS Protocol Engine & Two-Stage Automated Error Handling (AEH)
================================================================================
Validates multi-step first-principles and molecular dynamics simulation
protocols across stages, enforcing topological ordering, parameter invariance
(e.g., pseudopotential / functional consistency), and static pre-flight rules.
================================================================================
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional


class ProtocolEngine:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir

    def validate_multistep_protocol(
        self,
        workflow_name: str,
        steps: List[Dict[str, Any]],
        engine: str = "vasp"
    ) -> Dict[str, Any]:
        """
        AEH Stage 1: Static verification of multi-step simulation protocols.
        """
        issues = []
        warnings = []
        eng = engine.lower()

        if not steps or len(steps) == 0:
            return {"error": "Workflow contains no steps.", "isError": True}

        # 1. Check topological ordering for standard DFT workflows
        step_types = [s.get("type", "").lower() for s in steps]

        if "band_structure" in step_types and "scf" not in step_types and "relax" not in step_types:
            issues.append("Topological Violation: 'band_structure' step requires a preceding converged 'scf' or 'relax' step.")

        if "phonons" in step_types and "relax" not in step_types:
            warnings.append("Recommendation: 'phonons' calculation should be preceded by strict force relaxation (EDIFFG <= -0.01 eV/A).")

        # 2. Check parameter invariance across steps (GENIUS rule)
        functionals = set()
        pseudopotentials = set()
        cutoffs = []

        for idx, step in enumerate(steps, 1):
            s_name = step.get("name", f"step_{idx}")
            params = step.get("parameters", {})

            if "functional" in params:
                functionals.add(params["functional"].upper())
            if "potcar" in params or "pseudopotential" in params:
                pp = params.get("potcar") or params.get("pseudopotential")
                pseudopotentials.add(str(pp))
            if "encut" in params or "ecutwfc" in params:
                cutoffs.append(params.get("encut") or params.get("ecutwfc"))

        if len(functionals) > 1:
            issues.append(f"Invariance Violation: Mismatched exchange-correlation functionals across steps in the same study: {list(functionals)}")

        if len(pseudopotentials) > 1:
            issues.append(f"Invariance Violation: Inconsistent pseudopotential definitions across steps: {list(pseudopotentials)}")

        # 3. Check cutoff stability
        if len(cutoffs) > 1 and len(set(cutoffs)) > 1:
            warnings.append(f"Cutoff variation across steps: {cutoffs}. Ensure consistent plane-wave basis to prevent Pulay stress artifacts.")

        passed = len(issues) == 0

        return {
            "workflow_name": workflow_name,
            "engine": engine,
            "total_steps": len(steps),
            "passed_aeh_stage1": passed,
            "issues": issues,
            "warnings": warnings,
            "isError": not passed
        }
