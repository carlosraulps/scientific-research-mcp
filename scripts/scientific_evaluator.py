#!/usr/bin/env python3
"""
================================================================================
Scientific Script Evaluator, Decision Ladder & Convergence Diagnostic Engine
================================================================================
Implements:
  1. MDAgent Evaluator & Reflexion Pre-Flight: Static verification & scoring (1-10)
     with structured point deductions and suggestions for VASP, QE, LAMMPS, ORCA.
     Enforces Ponytail zero-redundancy and Slurm topology rules.
  2. Lee & Rondinelli 8-Rule Decision Ladder & DREAMS Convergence Diagnostics:
     Diagnoses SCF, ionic, or electronic errors (charge sloshing, active drift,
     level shifting) and prescribes targeted parameter interventions.
  3. Auditable Decision Trail: Appends decisions to logs/decisions.csv and EVIDENCE.md.
================================================================================
"""

import os
import sys
import re
import csv
import json
import datetime
from typing import Dict, Any, List, Optional, Tuple


class ScientificEvaluator:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.logs_dir = os.path.join(self.base_dir, "logs")
        self.decisions_csv = os.path.join(self.logs_dir, "decisions.csv")
        self.evidence_md = os.path.join(self.base_dir, "EVIDENCE.md")

        os.makedirs(self.logs_dir, exist_ok=True)
        self._init_decision_csv()

    def _init_decision_csv(self):
        if not os.path.exists(self.decisions_csv):
            with open(self.decisions_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "run_id", "step_name", "rule_id",
                    "hypothesis", "intervention", "outcome", "evidence_ref"
                ])

    # -------------------------------------------------------------------------
    # 1. MDAGENT PRE-FLIGHT SCRIPT EVALUATOR
    # -------------------------------------------------------------------------
    def evaluate_script(
        self,
        calc_type: str,
        script_content: str,
        formula_or_system: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Scores a simulation script (1-10) and flags redundant, dangerous, or unphysical tags.
        """
        score = 10.0
        deductions = []
        suggestions = []
        c_type = calc_type.lower()

        # VASP INCAR Evaluator
        if "vasp" in c_type or "incar" in c_type:
            # Ponytail Rule 1: Never redefine VASP defaults
            redundant_defaults = {
                r"\bALGO\s*=\s*Normal\b": "ALGO = Normal is VASP default; remove redundant definition.",
                r"\bLDAUTYPE\s*=\s*2\b": "LDAUTYPE = 2 (Dudarev) is VASP default; remove redundant definition.",
                r"\bLDAUJ\s*=\s*0(\.0)?\s+0(\.0)?\b": "LDAUJ = 0 is VASP default; remove redundant definition.",
                r"\bLWAVE\s*=\s*\.TRUE\.\b": "LWAVE = .TRUE. is VASP default; prune unless explicitly overriding.",
                r"\bLCHARG\s*=\s*\.TRUE\.\b": "LCHARG = .TRUE. is VASP default; prune unless explicitly overriding.",
                r"\bSYSTEM\s*=": "SYSTEM tag is obsolete metadata creating unnecessary text bloat.",
                r"\bPOTIM\s*=\s*0\.5\b": "POTIM = 0.5 is VASP default for IBRION=2; remove redundancy."
            }
            for pattern, msg in redundant_defaults.items():
                if re.search(pattern, script_content, re.IGNORECASE):
                    score -= 0.5
                    deductions.append(f"Ponytail VASP Redundancy: {msg}")
                    suggestions.append(f"Prune matching line: '{pattern}'")

            # Check IBRION & ISIF redundancy
            if re.search(r"\bIBRION\s*=\s*2\b", script_content, re.IGNORECASE):
                if re.search(r"\bISIF\s*=\s*2\b", script_content, re.IGNORECASE):
                    score -= 0.5
                    deductions.append("Ponytail Redundancy: ISIF=2 is native default when IBRION=2.")
                    suggestions.append("Remove 'ISIF = 2' from INCAR.")

            # Check unnecessary analysis overhead tags
            if re.search(r"\bNEDOS\s*=", script_content, re.IGNORECASE) or re.search(r"\bLORBIT\s*=", script_content, re.IGNORECASE):
                score -= 1.0
                deductions.append("I/O Overhead: NEDOS/LORBIT generate heavy DOSCAR/PROCAR files; omit unless plotting DOS.")
                suggestions.append("Prune NEDOS and LORBIT for relaxation or total energy calculations.")

            # Check precision & cutoff
            if not re.search(r"\bENCUT\s*=", script_content, re.IGNORECASE):
                score -= 2.0
                deductions.append("Missing Critical Parameter: ENCUT is not explicitly specified; default from POTCAR may under-converge.")
                suggestions.append("Explicitly set ENCUT based on ENMAX * 1.3 or convergence test.")

            # Check parallelization topology (NCORE/KPAR)
            if not re.search(r"\bNCORE\s*=", script_content, re.IGNORECASE) and not re.search(r"\bNPAR\s*=", script_content, re.IGNORECASE):
                score -= 0.5
                deductions.append("HPC Sizing: Neither NCORE nor NPAR is set; default may suffer severe MPI contention.")
                suggestions.append("Add NCORE = 4 (or divisor of socket core count) for optimal parallel scaling.")

        # LAMMPS Script Evaluator
        elif "lammps" in c_type:
            # Check timestep
            ts_match = re.search(r"\btimestep\s+([\d\.]+)", script_content, re.IGNORECASE)
            if ts_match:
                ts_val = float(ts_match.group(1))
                if ts_val > 1.0 and formula_or_system and any(h in formula_or_system for h in ["H", "water", "protein", "organic"]):
                    score -= 2.0
                    deductions.append(f"Unphysical Timestep: Timestep {ts_val} fs is dangerously large for hydrogenous systems (max 1.0 fs).")
                    suggestions.append("Reduce timestep to 0.5 - 1.0 fs to avoid bond-stretching explosion.")
            else:
                score -= 1.0
                deductions.append("Missing Timestep: 'timestep' directive not found.")

            # Check thermo and dump frequency
            if not re.search(r"\bthermo\s+\d+", script_content, re.IGNORECASE):
                score -= 1.0
                deductions.append("Missing Monitoring: 'thermo' output frequency is not declared.")

        # Quantum ESPRESSO (.pwi) Evaluator
        elif "qe" in c_type or "pw" in c_type:
            if not re.search(r"\becutwfc\s*=", script_content, re.IGNORECASE):
                score -= 2.5
                deductions.append("Missing Wavefunction Cutoff: 'ecutwfc' must be explicitly declared.")
            if not re.search(r"\bconv_thr\s*=", script_content, re.IGNORECASE):
                score -= 1.0
                deductions.append("Missing SCF Convergence Threshold: 'conv_thr' not declared.")

        score = max(0.0, min(10.0, round(score, 1)))
        passed = score >= 7.0

        return {
            "calc_type": calc_type,
            "score": score,
            "passed": passed,
            "deductions": deductions,
            "suggestions": suggestions,
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 2. 8-RULE DECISION LADDER & CONVERGENCE DIAGNOSTIC
    # -------------------------------------------------------------------------
    def diagnose_convergence(
        self,
        engine: str,
        input_content: str = "",
        output_content: str = "",
        error_log: str = "",
        iteration_count: int = 1
    ) -> Dict[str, Any]:
        """
        Executes the hierarchical 8-Rule Decision Ladder and Convergence Agent diagnostics.
        """
        if iteration_count >= 8:
            return {
                "rule_triggered": "BUDGET_EXHAUSTED",
                "diagnosis": f"The 8-attempt recovery budget has been exhausted (iteration {iteration_count}). Recurring failures indicate an improper model/active space or physical unfeasibility.",
                "recommended_actions": ["Terminate automated retry loop", "Preserve all logs and output artifacts", "Escalate to human review with structured diagnostics"],
                "should_terminate": True,
                "isError": False
            }

        eng = engine.lower()
        combined_text = f"{output_content}\n{error_log}"

        # Rule A: Infrastructure / Slurm Scheduler Failure
        if any(term in combined_text for term in [
            "CANCELLED AT", "DUE TO TIME LIMIT", "OUT OF MEMORY", "oom-killer",
            "SIGKILL", "slurmstepd: error:", "Bus error", "Segmentation fault"
        ]):
            return {
                "rule_triggered": "Rule A (Infrastructure / Hardware Failure)",
                "diagnosis": "Job terminated prematurely due to SLURM walltime expiry, node memory exhaustion, or hardware SIGKILL.",
                "recommended_actions": [
                    "Check node memory per core; downsize core count to allocate more RAM per MPI task.",
                    "Size job with micro-batch checkpointing (3h walltime) rather than monolithic execution.",
                    "Verify node interconnect and scratch disk quotas."
                ],
                "parameters_to_modify": {"walltime": "03:00:00", "memory_per_cpu": "higher"},
                "should_terminate": False,
                "isError": False
            }

        # Rule B: Standard SCF Non-Convergence
        if any(term in combined_text for term in [
            "SCF NOT CONVERGED", "convergence not achieved", "ELECTRONIC RELAXATION NOT CONVERGED",
            "not converged after", "dE failed to reach threshold", "charge sloshing"
        ]):
            remedies = []
            param_mods = {}
            if "vasp" in eng:
                remedies.append("Reduce electronic mixing parameter AMIX from 0.4 to 0.2 to suppress charge sloshing.")
                remedies.append("Increase electronic step limit NELM from 60 to 120.")
                remedies.append("If metallic, ensure ISMEAR = 1 or 2 with SIGMA = 0.1 - 0.2.")
                param_mods = {"AMIX": 0.2, "NELM": 120, "BMIX": 0.0001}
            elif "qe" in eng:
                remedies.append("Reduce mixing_beta from 0.7 down to 0.3.")
                remedies.append("Switch mixing_mode to 'local-TF'.")
                remedies.append("Increase electron_maxstep to 200.")
                param_mods = {"mixing_beta": 0.3, "mixing_mode": "local-TF", "electron_maxstep": 200}
            else:
                remedies.append("Damp DIIS mixing and extend maximum SCF cycles.")

            return {
                "rule_triggered": "Rule B (Standard SCF Non-Convergence)",
                "diagnosis": "Electronic ground state self-consistent field failed to converge within maximum allowed cycles due to charge sloshing or narrow energy gaps.",
                "recommended_actions": remedies,
                "parameters_to_modify": param_mods,
                "should_terminate": False,
                "isError": False
            }

        # Rule C: CASSCF Non-Convergence (ORCA / Multireference)
        if any(term in combined_text for term in ["CASSCF did not converge", "Orbital gradient norm too large", "CASSCF_MAXITER"]):
            return {
                "rule_triggered": "Rule C (CASSCF Non-Convergence)",
                "diagnosis": "Multiconfigurational orbital gradient failed to converge in active space optimization.",
                "recommended_actions": [
                    "Introduce orbital level-shifting to separate active and external orbitals.",
                    "Switch to quasi-Newton orbital update or increase CASSCF maxiter.",
                    "Inspect active orbital occupations (NOON) for near-zero or near-2 values."
                ],
                "parameters_to_modify": {"LevelShift": 0.5, "MaxIter": 100},
                "should_terminate": False,
                "isError": False
            }

        # Rule D: Wrong Electronic State / Active Orbital Drift
        if any(term in combined_text for term in ["Active orbital drifted", "NOON out of expected range", "wrong state selected", "symmetry mismatch"]):
            return {
                "rule_triggered": "Rule D (Incorrect Electronic State / Active Drift)",
                "diagnosis": "The wavefunction converged to an undesired local minimum or excited root with active orbitals drifting into virtual space.",
                "recommended_actions": [
                    "Perform constrained orbital rotations preserving spatial irreducible representation (irrep) symmetry.",
                    "Re-order orbitals using localized initial guesses (e.g. Pipek-Mezey or Foster-Boys).",
                    "Enforce strict state-averaging (SA-CASSCF) over degenerate or near-degenerate states."
                ],
                "parameters_to_modify": {"RotateOrbitals": True, "StateAveraging": True},
                "should_terminate": False,
                "isError": False
            }

        # Rule G: Rydberg / Diffuse State Contamination
        if any(term in combined_text for term in ["diffuse exponent", "Rydberg contamination", "unphysical diffuse orbital"]):
            return {
                "rule_triggered": "Rule G (Rydberg / Diffuse State Contamination)",
                "diagnosis": "Calculated excitation involves diffuse basis functions rather than targeted valence active space.",
                "recommended_actions": [
                    "Inspect Gaussian exponents and exclude ultra-diffuse basis functions from valence active space.",
                    "Expand state roots to separate low-lying valence excitations from continuum Rydberg onset."
                ],
                "parameters_to_modify": {"ExcludeDiffuse": True},
                "should_terminate": False,
                "isError": False
            }

        # Check for confirmed convergence (Rule H)
        if any(term in combined_text for term in [
            "reached required accuracy", "General timing and accounting",
            "JOB FINISHED", "ORCA TERMINATED NORMALLY", "Total CPU time"
        ]):
            return {
                "rule_triggered": "Rule H (Verified Successful Convergence)",
                "diagnosis": "Calculation completed successfully with all convergence criteria satisfied.",
                "recommended_actions": ["Extract ground-state physical observables", "Register output artifact to Canvas"],
                "parameters_to_modify": {},
                "should_terminate": False,
                "isError": False
            }

        # Fallback General Diagnostic
        return {
            "rule_triggered": "Unclassified Calculation Behavior",
            "diagnosis": "Calculation exited without explicit error signatures but without verified convergence markers.",
            "recommended_actions": ["Inspect output file tail", "Verify input geometry and coordinate integrity"],
            "parameters_to_modify": {},
            "should_terminate": False,
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 3. AUDITABLE DECISION LOGGING
    # -------------------------------------------------------------------------
    def log_decision(
        self,
        run_id: str,
        step_name: str,
        hypothesis: str,
        intervention: str,
        outcome: str,
        rule_id: str = "Rule B",
        evidence_ref: str = ""
    ) -> Dict[str, Any]:
        """
        Appends an entry to logs/decisions.csv and updates EVIDENCE.md.
        """
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # 1. Append to CSV
        with open(self.decisions_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                now_iso, run_id, step_name, rule_id,
                hypothesis, intervention, outcome, evidence_ref
            ])

        # 2. Append to EVIDENCE.md
        if not os.path.exists(self.evidence_md):
            with open(self.evidence_md, "w", encoding="utf-8") as f:
                f.write("# Scientific Research Evidence & Decision Log\n\nAuditable record of all procedural decisions, theoretical justifications, and parameter interventions.\n\n---\n\n")

        evidence_entry = f"""### [{now_iso}] Decision: {step_name} (`{run_id}`)
- **Triggered Rule**: {rule_id}
- **Hypothesis**: {hypothesis}
- **Intervention**: {intervention}
- **Observed Outcome**: {outcome}
- **Evidence / Artifact Reference**: `{evidence_ref}`

---
"""
        with open(self.evidence_md, "a", encoding="utf-8") as f:
            f.write(evidence_entry)

        return {
            "status": "LOGGED",
            "run_id": run_id,
            "step_name": step_name,
            "rule_id": rule_id,
            "decisions_csv": self.decisions_csv,
            "isError": False
        }
