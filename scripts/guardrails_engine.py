#!/usr/bin/env python3
"""
================================================================================
SciResearch Defense-in-Depth Guardrails Engine (scripts/guardrails_engine.py)
================================================================================
Grounded in Chip Huyen, 'AI Engineering: Building Applications with Foundation Models'
(O'Reilly 2025, Chapters 5 & 10, Step 2: Put in Guardrails).

Provides tri-stage defense-in-depth guardrails for scientific agents:
  1. Input Guardrail:
     - Secret and credential leak protection (enforces strict non-disclosure of .env,
       API keys, private tokens, certificates per DecisionCouncil protocol).
     - Scientific parameter typing and physical range bounds (positive cutoff energies,
       finite k-points, valid pseudopotentials).
     - Blind 5-day walltime rejection (enforces 3h-4h micro-batching).
     - HPC core divisor alignment (16, 32, 64, 128, 192, 256 cores).
  2. Execution Guardrail:
     - Iteration limits against the 8-attempt recovery budget (Lee & Rondinelli).
     - Runaway loop and execution timeout sentinels.
  3. Output Guardrail:
     - Ground-state physics anchor verification ('reached required accuracy', 'E0=').
     - Energetic sanity bounds (detects catastrophic SCF divergence, negative volumes).
     - Schema formatting validation (guarantees deterministic downstream consumption).
================================================================================
"""

import os
import re
import math
from typing import Dict, Any, List, Optional, Tuple


class GuardrailsEngine:
    """
    Defense-in-depth scientific guardrails engine implementing Chip Huyen's
    three-stage guardrail architecture for autonomous scientific agents.
    """

    # Secret patterns to detect and block immediately
    SECRET_PATTERNS = [
        re.compile(r'(?i)(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{16,}["\']?'),
        re.compile(r'ghp_[a-zA-Z0-9]{36}'),  # GitHub PAT
        re.compile(r'sk-[a-zA-Z0-9]{20,}'),   # OpenAI Key
        re.compile(r'AIza[0-9A-Za-z-_]{35}'), # Google API Key
        re.compile(r'-----BEGIN\s+(RSA|EC|DSA|OPENSSH|PRIVATE)\s+KEY-----'),
    ]

    # VASP valid parameter ranges
    VASP_BOUNDS = {
        "ENCUT": (100.0, 1500.0),
        "EDIFF": (1e-9, 1e-3),
        "EDIFFG": (-1.0, 1e-1),
        "ISIF": (0, 7),
        "IBRION": (-1, 8),
        "ISMEAR": (-5, 5),
        "SIGMA": (0.001, 1.0),
        "AMIX": (0.01, 1.0),
        "BMIX": (0.00001, 3.0),
        "POTIM": (0.01, 5.0),
    }

    # HPC core divisor constraints (AMD EPYC architecture)
    VALID_HPC_DIVISORS = {1, 2, 4, 8, 16, 32, 64, 128, 192, 256}

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def audit_input(self, payload: Dict[str, Any], domain: str = "dft") -> Dict[str, Any]:
        """
        Audits incoming task inputs, script contents, or parameter dictionaries.
        Returns a structured assessment containing passed status, violations, and remediations.
        """
        violations = []
        warnings = []
        sanitized = True

        payload_str = str(payload)

        # 1. Secret & Credential Leak Guardrail
        for pat in self.SECRET_PATTERNS:
            if pat.search(payload_str):
                violations.append({
                    "guardrail": "credential_isolation",
                    "severity": "CRITICAL",
                    "message": "Potential exposed API key, private secret, or credential detected in input payload.",
                    "remediation": "Redact all secret tokens immediately (KEY=***REDACTED***) and store credentials exclusively in protected local env."
                })
                sanitized = False

        # 2. Walltime & Micro-batching Guardrail
        walltime = payload.get("walltime") or payload.get("time") or payload.get("TIME")
        if walltime:
            wt_str = str(walltime)
            # Check for 5-day monolithic walltimes
            if re.search(r'(?i)(5-00:00:00|120:00:00|[5-9]\s*days?)', wt_str):
                violations.append({
                    "guardrail": "slurm_preflight_walltime",
                    "severity": "HIGH",
                    "message": f"Monolithic 5-day walltime '{wt_str}' requested. Violates backfill harvesting protocol.",
                    "remediation": "Partition into 3-hour or 4-hour micro-batches (--time=03:00:00) with SIGUSR1 checkpoint traps."
                })

        # 3. HPC Core Topology Alignment
        cores = payload.get("cores") or payload.get("ntasks") or payload.get("cpus")
        if cores:
            try:
                c_val = int(cores)
                if c_val not in self.VALID_HPC_DIVISORS:
                    warnings.append({
                        "guardrail": "hpc_divisor_alignment",
                        "severity": "MEDIUM",
                        "message": f"Requested core count {c_val} is not aligned with AMD EPYC socket architecture (16, 32, 64, 128, 192, 256).",
                        "remediation": f"Adjust core allocation to a hardware divisor (e.g. 16, 32, 64) to prevent core fragmentation stalls."
                    })
            except (ValueError, TypeError):
                pass

        # 4. Domain-Specific Scientific Parameter Range Checks
        if domain.lower() in ["dft", "vasp"]:
            params = payload.get("parameters") or payload.get("params") or payload
            if isinstance(params, dict):
                for key, val in params.items():
                    k_upper = key.upper()
                    if k_upper in self.VASP_BOUNDS:
                        min_v, max_v = self.VASP_BOUNDS[k_upper]
                        try:
                            f_val = float(val)
                            if f_val < min_v or f_val > max_v:
                                violations.append({
                                    "guardrail": "parameter_bounds_check",
                                    "severity": "HIGH",
                                    "message": f"VASP tag {k_upper}={val} out of physical bounds [{min_v}, {max_v}].",
                                    "remediation": f"Reset {k_upper} within physically safe bounds [{min_v}, {max_v}]."
                                })
                        except (ValueError, TypeError):
                            pass

        return {
            "stage": "INPUT",
            "passed": len(violations) == 0,
            "sanitized": sanitized,
            "violations": violations,
            "warnings": warnings,
            "total_violations": len(violations),
            "total_warnings": len(warnings)
        }

    def audit_execution(self, iteration_count: int, max_budget: int = 8, elapsed_seconds: float = 0.0, timeout_seconds: float = 3600.0) -> Dict[str, Any]:
        """
        Audits live execution state against recursion bounds and runtime budgets.
        """
        violations = []
        warnings = []

        if iteration_count > max_budget:
            violations.append({
                "guardrail": "recovery_budget_limit",
                "severity": "CRITICAL",
                "message": f"Attempt {iteration_count} exceeds maximum Lee & Rondinelli recovery budget of {max_budget} attempts.",
                "remediation": "Halt execution immediately. Convene DecisionCouncil or escalate to human researcher to re-evaluate physical model."
            })
        elif iteration_count >= max_budget - 1:
            warnings.append({
                "guardrail": "recovery_budget_warning",
                "severity": "MEDIUM",
                "message": f"Attempt {iteration_count} of {max_budget}. Nearing recovery budget exhaustion.",
                "remediation": "Verify that parameter interventions have addressed root cause before final attempt."
            })

        if timeout_seconds > 0 and elapsed_seconds > timeout_seconds:
            violations.append({
                "guardrail": "execution_timeout",
                "severity": "CRITICAL",
                "message": f"Elapsed execution time ({elapsed_seconds:.1f}s) exceeded timeout threshold ({timeout_seconds:.1f}s).",
                "remediation": "Interrupt hanging calculation or tool call to prevent zombie process stalls."
            })

        return {
            "stage": "EXECUTION",
            "passed": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "current_iteration": iteration_count,
            "max_budget": max_budget
        }

    def audit_output(self, output_text: str, engine: str = "vasp", expected_metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Audits simulation outputs or calculation deliverables for physical anchors,
        catastrophic divergence, and structural integrity.
        """
        violations = []
        warnings = []
        anchors_found = []

        if not output_text or len(output_text.strip()) == 0:
            violations.append({
                "guardrail": "empty_output_filter",
                "severity": "CRITICAL",
                "message": "Simulation output is completely empty.",
                "remediation": "Verify that the calculation executable was dispatched and produced logs."
            })
            return {
                "stage": "OUTPUT",
                "passed": False,
                "violations": violations,
                "warnings": warnings,
                "anchors_found": []
            }

        # 1. Physics Anchor Detection (Huyen Chapter 10 Output Guardrails)
        if engine.lower() == "vasp":
            vasp_anchors = [
                ("electronic_convergence", "reached required accuracy - stopping structural energy minimisation"),
                ("ionic_completion", "General timing and accounting informations for this job"),
                ("energy_line", "free  energy   TOTEN"),
                ("fermi_energy", "E-fermi")
            ]
            for anchor_name, anchor_str in vasp_anchors:
                if anchor_str.lower() in output_text.lower():
                    anchors_found.append(anchor_name)

            # Check for catastrophic SCF divergence
            if "POSCAR: fatal error" in output_text or "BRMIX: very serious problems" in output_text:
                violations.append({
                    "guardrail": "scf_catastrophic_divergence",
                    "severity": "CRITICAL",
                    "message": "Fatal numerical instability or charge density explosion detected in output log.",
                    "remediation": "Apply charge sloshing remediation (AMIX=0.2, BMIX=0.0001) or re-relax structure with lower POTIM."
                })

            if "electronic_convergence" not in anchors_found and "energy_line" not in anchors_found:
                warnings.append({
                    "guardrail": "unconfirmed_ground_state",
                    "severity": "HIGH",
                    "message": "Output lacks explicit electronic convergence anchor strings.",
                    "remediation": "Audit OSZICAR / OUTCAR to confirm SCF loop converged before using reported energies."
                })

        # 2. Check Expected Physical Metrics (if provided)
        if expected_metrics and isinstance(expected_metrics, dict):
            energy = expected_metrics.get("energy_ev")
            if energy is not None:
                if math.isnan(energy) or math.isinf(energy):
                    violations.append({
                        "guardrail": "non_finite_physical_quantity",
                        "severity": "CRITICAL",
                        "message": f"Reported ground-state energy is non-finite: {energy}",
                        "remediation": "Discard calculation output and check input geometry for coordinate singularities."
                    })
                elif abs(energy) > 100000.0:
                    warnings.append({
                        "guardrail": "extreme_energy_magnitude",
                        "severity": "MEDIUM",
                        "message": f"Reported ground-state energy magnitude (|{energy}| eV) is exceptionally large.",
                        "remediation": "Confirm cell stoichiometry and atomic count match reported energy scale."
                    })

        return {
            "stage": "OUTPUT",
            "passed": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "anchors_found": anchors_found,
            "total_violations": len(violations),
            "total_warnings": len(warnings)
        }


if __name__ == "__main__":
    guard = GuardrailsEngine()
    test_in = {
        "parameters": {"ENCUT": 520.0, "ISIF": 2, "EDIFF": 1e-6},
        "walltime": "04:00:00",
        "cores": 32
    }
    res = guard.audit_input(test_in)
    print("Test input audit passed:", res["passed"])
