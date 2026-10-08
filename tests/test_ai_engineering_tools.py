#!/usr/bin/env python3
"""
================================================================================
Test AI Engineering Tools (tests/test_ai_engineering_tools.py)
================================================================================
Unit tests for the new Chip Huyen 2025 AI Engineering modules:
  - GuardrailsEngine (scripts/guardrails_engine.py)
  - ComponentEvaluator (scripts/component_evaluator.py)
  - CacheStore (scripts/cache_store.py)
================================================================================
"""

import os
import sys
import unittest
import tempfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from guardrails_engine import GuardrailsEngine
from component_evaluator import ComponentEvaluator
from cache_store import CacheStore


class TestAIEngineeringTools(unittest.TestCase):

    def setUp(self):
        self.guardrails = GuardrailsEngine(BASE_DIR)
        self.evaluator = ComponentEvaluator(BASE_DIR)
        self.cache = CacheStore(BASE_DIR)

    def test_01_guardrail_credential_isolation(self):
        # Leaked key should be blocked
        leaked_payload = {
            "parameters": {"ENCUT": 520},
            "api_key": "sk-1234567890abcdef1234567890abcdef"
        }
        res = self.guardrails.audit_input(leaked_payload)
        self.assertFalse(res["passed"])
        self.assertFalse(res["sanitized"])
        self.assertTrue(any(v["guardrail"] == "credential_isolation" for v in res["violations"]))

    def test_02_guardrail_slurm_walltime_and_cores(self):
        # 5-day request should be flagged
        bad_hpc = {
            "walltime": "5-00:00:00",
            "cores": 77
        }
        res = self.guardrails.audit_input(bad_hpc)
        self.assertFalse(res["passed"])
        self.assertTrue(any(v["guardrail"] == "slurm_preflight_walltime" for v in res["violations"]))
        self.assertTrue(any(w["guardrail"] == "hpc_divisor_alignment" for w in res["warnings"]))

    def test_03_guardrail_execution_budget(self):
        # Attempt 9 exceeds budget of 8
        res = self.guardrails.audit_execution(iteration_count=9, max_budget=8)
        self.assertFalse(res["passed"])
        self.assertTrue(any(v["guardrail"] == "recovery_budget_limit" for v in res["violations"]))

        # Attempt 3 passes
        res_ok = self.guardrails.audit_execution(iteration_count=3, max_budget=8)
        self.assertTrue(res_ok["passed"])

    def test_04_guardrail_output_anchors(self):
        # Missing anchors
        res_empty = self.guardrails.audit_output("", engine="vasp")
        self.assertFalse(res_empty["passed"])

        # Catastrophic divergence
        res_div = self.guardrails.audit_output("BRMIX: very serious problems in charge mixing", engine="vasp")
        self.assertFalse(res_div["passed"])
        self.assertTrue(any(v["guardrail"] == "scf_catastrophic_divergence" for v in res_div["violations"]))

        # Converged ground state
        good_out = "reached required accuracy - stopping structural energy minimisation\nGeneral timing and accounting informations for this job"
        res_good = self.guardrails.audit_output(good_out, engine="vasp")
        self.assertTrue(res_good["passed"])
        self.assertIn("electronic_convergence", res_good["anchors_found"])

    def test_05_component_evaluator_all(self):
        summary = self.evaluator.evaluate_all()
        self.assertEqual(summary["system_health"], "HEALTHY")
        self.assertEqual(summary["pass_rate_percent"], 100.0)
        self.assertGreater(summary["total_components"], 8)

    def test_06_cache_store_exact_and_semantic(self):
        ns = "_test_ai_eng_cache"
        k = "pt111_her_barrier"
        q_orig = "Calculated hydrogen evolution reaction Gibbs free energy on Pt(111)"
        val = {"delta_g_H": -0.09, "unit": "eV"}

        self.cache.set(k, q_orig, val, namespace=ns)

        # 1. Exact hit
        hit1 = self.cache.get(k, namespace=ns)
        self.assertIsNotNone(hit1)
        self.assertEqual(hit1["hit_type"], "EXACT")
        self.assertEqual(hit1["value"]["delta_g_H"], -0.09)

        # 2. Semantic hit with reworded query
        q_reword = "Hydrogen evolution reaction free energy calculation on Pt(111)"
        hit2 = self.cache.get("different_key", query_text=q_reword, namespace=ns, min_similarity=0.60)
        self.assertIsNotNone(hit2)
        self.assertEqual(hit2["hit_type"], "SEMANTIC")
        self.assertEqual(hit2["value"]["delta_g_H"], -0.09)


if __name__ == "__main__":
    unittest.main()
