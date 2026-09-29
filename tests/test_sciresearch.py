#!/usr/bin/env python3
"""
Unit tests for Scientific Research Log Skill & MCP Engine (21 Tools).
"""

import os
import sys
import json
import uuid
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from canvas_store import CanvasStore
from checkpoint_manager import CheckpointManager
from historical_memory import HistoricalMemoryStore
from scientific_evaluator import ScientificEvaluator
from graphify_bridge import GraphifyBridge
from facts_store import FactsStore
from skill_crystallizer import SkillCrystallizer
from dual_verifier import DualVerifier
from protocol_engine import ProtocolEngine
from git_controller import GitController


class TestScientificResearchLog(unittest.TestCase):
    def setUp(self):
        self.canvas = CanvasStore(BASE_DIR)
        self.checkpoints = CheckpointManager(BASE_DIR)
        self.memory = HistoricalMemoryStore(BASE_DIR)
        self.evaluator = ScientificEvaluator(BASE_DIR)
        self.graphify = GraphifyBridge(BASE_DIR)
        self.facts = FactsStore(BASE_DIR)
        self.skills = SkillCrystallizer(BASE_DIR)
        self.verifier = DualVerifier(BASE_DIR)
        self.protocols = ProtocolEngine(BASE_DIR)
        self.git = GitController(BASE_DIR)

    def test_01_anti_laundering_short_context(self):
        res = self.canvas.register_artifact(
            producing_tool="dft_relax",
            value=-154.2,
            arguments={"encut": 520},
            rationales={},
            sources={},
            declared_context="Too short"
        )
        self.assertTrue(res.get("isError"))
        self.assertIn("Anti-Laundering Violation", res.get("error", ""))

    def test_02_anti_laundering_trivial_math(self):
        res = self.canvas.register_artifact(
            producing_tool="math_eval",
            value=520.0,
            arguments={"expression": "x0 * 1.0"},
            rationales={},
            sources={},
            declared_context="Characterizing energy cutoff via identity product."
        )
        self.assertTrue(res.get("isError"))
        self.assertIn("Trivial identity expression", res.get("error", ""))

    def test_03_valid_artifact_and_audit(self):
        res1 = self.canvas.register_artifact(
            producing_tool="dft_cutoff_sweep",
            value={"converged_encut": 520, "energy_diff_mev": 0.4},
            arguments={"encut_range": [400, 450, 500, 520, 600]},
            rationales={"encut": "Convergence sweep to Delta E < 1 meV/atom"},
            sources={},
            declared_context="Initial kinetic energy cutoff sweep for FCC Platinum bulk."
        )
        self.assertFalse(res1.get("isError"))
        art1_id = res1["result_id"]

        res2 = self.canvas.register_artifact(
            producing_tool="dft_equilibrium_volume",
            value={"a0": 3.924, "e0": -6.048},
            arguments={"encut": 520, "kpoints": [12, 12, 12]},
            rationales={
                "encut": "Sourced from prior convergence sweep",
                "kpoints": "Monkhorst-Pack 12x12x12 grid standard for metallic FCC Pt"
            },
            sources={"encut": art1_id},
            declared_context="Equation of state volume relaxation for FCC Platinum."
        )
        self.assertFalse(res2.get("isError"))
        art2_id = res2["result_id"]

        audit = self.canvas.audit_provenance_chain(art2_id)
        self.assertFalse(audit.get("isError"))
        self.assertEqual(audit["total_ancestors"], 1)
        ancestor_ids = [a["result_id"] for a in audit["provenance_chain"]]
        self.assertIn(art1_id, ancestor_ids)

        return art1_id, art2_id

    def test_04_notes_and_reports(self):
        art1_id, art2_id = self.test_03_valid_artifact_and_audit()

        note_res = self.canvas.write_note(
            title="Pt Bulk Convergence Discussion",
            content="Plane-wave cutoff test converged at 520 eV with delta E below 1 meV/atom.",
            tags=["dft", "pt", "convergence"],
            references=[art1_id]
        )
        self.assertFalse(note_res.get("isError"))
        self.assertGreaterEqual(note_res["version"], 1)

        unique_tag = uuid.uuid4().hex[:6]
        rep_res = self.canvas.create_report(
            title=f"Sol27LC Benchmark Platinum Study Report {unique_tag}",
            objective="Reproduce expert-level equilibrium lattice constant for Pt bulk.",
            executive_summary="Calculated lattice constant a0 = 3.924 A within 0.2% of experiment.",
            findings=[
                {"title": "Equilibrium Parameter", "description": "Obtained via Birch-Murnaghan EOS fit.", "data": {"a0": 3.924}}
            ],
            claims_with_provenance=[
                {"claim": "Lattice constant converges to 3.924 A at 520 eV cutoff", "artifact_id": art2_id}
            ]
        )
        self.assertFalse(rep_res.get("isError"))
        self.assertEqual(rep_res["claims_verified"], 1)

    def test_05_checkpoints(self):
        run_id = self.checkpoints.generate_run_id("test_md")
        save_res = self.checkpoints.save_run(
            run_id=run_id,
            prompt_summary="Equilibrate solvated protein in NPT ensemble at 300K.",
            parameter_registry={"timestep": 1.0, "temperature": 300, "ensemble": "NPT"},
            status="RUNNING"
        )
        self.assertFalse(save_res.get("isError"))

        resume_res = self.checkpoints.resume_run(run_id)
        self.assertFalse(resume_res.get("isError"))
        self.assertEqual(resume_res["checkpoint"]["status"], "RUNNING")
        self.assertEqual(resume_res["checkpoint"]["parameter_registry"]["temperature"], 300)

    def test_06_historical_memory_symmetry_retrieval(self):
        ret = self.memory.retrieve_similar(
            formula="Pt",
            space_group="Fm-3m",
            crystal_system="Cubic",
            volume=60.0,
            accuracy_tier="high_precision"
        )
        self.assertFalse(ret.get("isError"))
        self.assertGreater(len(ret["recommendations"]), 0)
        top = ret["recommendations"][0]
        self.assertEqual(top["space_group"], "Fm-3m")
        self.assertIn("encut", top["theta_phy"])

    def test_07_evaluator_script_scoring(self):
        bad_incar = """
ALGO = Normal
ISIF = 2
IBRION = 2
LDAUTYPE = 2
SYSTEM = Bad Test
"""
        eval_res = self.evaluator.evaluate_script("vasp", bad_incar)
        self.assertFalse(eval_res.get("isError"))
        self.assertLess(eval_res["score"], 10.0)
        self.assertTrue(len(eval_res["deductions"]) >= 2)

    def test_08_decision_ladder_diagnostics(self):
        diag = self.evaluator.diagnose_convergence(
            engine="vasp",
            output_content="SCF NOT CONVERGED dE failed to reach threshold",
            error_log=""
        )
        self.assertFalse(diag.get("isError"))
        self.assertIn("Rule B", diag["rule_triggered"])
        self.assertIn("AMIX", diag["parameters_to_modify"])

    def test_09_facts_and_traps_memory(self):
        # Search seeded traps
        res = self.facts.search_facts(material_or_system="Pt(111)")
        self.assertFalse(res.get("isError"))
        self.assertGreater(res["total_matches"], 0)
        self.assertIn("dipole", res["facts"][0]["statement"].lower())

        # Save new fact
        save_res = self.facts.save_fact(
            category="trap",
            material_or_system="TiO2 Anatase",
            statement="Requires +U on Ti 3d orbitals to localize polaron states.",
            remediation="Set LDAUU = 4.2 for Ti.",
            source_ref="Test Benchmark"
        )
        self.assertFalse(save_res.get("isError"))

    def test_10_skill_crystallization(self):
        res = self.skills.save_procedure(
            skill_name="test_charge_sloshing_fix",
            description="Remedies severe charge sloshing on metallic slab surfaces",
            trigger_conditions="SCF non-convergence with oscillating dE",
            procedure_code="def fix_sloshing(incar):\n    incar['AMIX'] = 0.2\n    return incar"
        )
        self.assertFalse(res.get("isError"))

        search_res = self.skills.search_procedures("charge sloshing")
        self.assertFalse(search_res.get("isError"))
        self.assertGreater(search_res["total_matches"], 0)

    def test_11_rosetta_dual_verification(self):
        # Spec with circularity violation
        bad_spec = """
def calculate_bandgap():
    # Fit directly to experimental target
    target_energy = 1.42
    return target_energy
"""
        verif = self.verifier.audit_dual_verification(bad_spec, "dft")
        self.assertTrue(verif.get("isError"))
        self.assertFalse(verif["scientific_validity"]["passed"])
        self.assertTrue(len(verif["scientific_validity"]["constitution_violations"]) > 0)

    def test_12_genius_protocol_validation(self):
        # Incompatible functional study
        mismatched_steps = [
            {"name": "relax", "type": "relax", "parameters": {"functional": "PBE", "encut": 520}},
            {"name": "bands", "type": "band_structure", "parameters": {"functional": "SCAN", "encut": 520}}
        ]
        proto = self.protocols.validate_multistep_protocol("mismatched_test", mismatched_steps)
        self.assertTrue(proto.get("isError"))
        self.assertFalse(proto["passed_aeh_stage1"])
        self.assertTrue(any("Invariance Violation" in iss for iss in proto["issues"]))

    def test_13_git_controller(self):
        status = self.git.get_status()
        self.assertIn("is_git_repo", status)
        self.assertIn("is_dirty", status)
        self.assertIn("modified_files", status)

        repro = self.git.verify_reproducibility()
        self.assertIn("reproducible", repro)
        self.assertIn("score", repro)


if __name__ == "__main__":
    unittest.main()
