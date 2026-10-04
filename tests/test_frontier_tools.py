#!/usr/bin/env python3
"""
================================================================================
Test Frontier Tools (test_frontier_tools.py)
================================================================================
Unit tests for the new literature-grounded sciresearch tools:
- StructureSanityGuard (Microsoft AI4Science 2023 & Chip Huyen 2025)
- HypothesisEvaluator (LLM4SR Luo et al. 2025 & HKUST 2025)
- SDELoopVerifier (SDE benchmark Song, Duan, Kulik et al. 2026)
================================================================================
"""

import os
import sys
import tempfile
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from structure_guard import StructureSanityGuard
from hypothesis_evaluator import HypothesisEvaluator
from sde_loop_verifier import SDELoopVerifier


def test_structure_guard_valid():
    guard = StructureSanityGuard()
    poscar_valid = """Si2 Diamond
5.43
0.0 0.5 0.5
0.5 0.0 0.5
0.5 0.5 0.0
Si
2
Direct
0.00 0.00 0.00
0.25 0.25 0.25
"""
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(poscar_valid)
        path = f.name
    try:
        res = guard.validate_poscar(path)
        assert res["valid"] is True
        assert res["total_atoms"] == 2
        assert res["metrics"]["volume_angstrom3"] > 0
        assert res["metrics"]["min_pairwise_distance_angstrom"] > 2.0
    finally:
        os.unlink(path)


def test_structure_guard_atomic_overlap():
    guard = StructureSanityGuard()
    poscar_clash = """H2 Overlap
1.0
10.0 0.0 0.0
0.0 10.0 0.0
0.0 0.0 10.0
H
2
Cartesian
0.0 0.0 0.0
0.3 0.0 0.0
"""
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write(poscar_clash)
        path = f.name
    try:
        res = guard.validate_poscar(path)
        assert res["valid"] is False
        assert any("Atomic overlap" in err for err in res["errors"])
    finally:
        os.unlink(path)


def test_hypothesis_evaluator_vague():
    evaluator = HypothesisEvaluator(BASE_DIR)
    vague_text = "We will do some calculations on carbon materials to see if they are good."
    res = evaluator.evaluate_hypothesis(vague_text)
    assert res["passed"] is False
    assert res["recommendation"] == "REFINE_HYPOTHESIS"
    assert res["breakdown"]["clarity"]["score"] < 14.0


def test_hypothesis_evaluator_rigorous():
    evaluator = HypothesisEvaluator(BASE_DIR)
    good_text = """We hypothesize that hydrogen adatom adsorption on the pentagonal ring of PHOTH-graphene (C10)
exhibits an adsorption energy of -1.45 eV using VASP with PBE+D3-BJ corrections.
Given the 2D extended lattice, Pulay mixing with AMIX=0.2 and BMIX=0.0001 is enforced to prevent charge sloshing.
The electronic band gap will be calculated using a 12x12x1 Monkhorst-Pack k-mesh and compared against pristine PHOTH-graphene."""
    res = evaluator.evaluate_hypothesis(good_text)
    assert res["passed"] is True
    assert res["total_score"] >= 80.0
    assert res["recommendation"] == "PROCEED"


def test_sde_loop_verifier_anti_saturation():
    verifier = SDELoopVerifier(BASE_DIR)
    project = "test_sde_saturation"
    verifier.reset_project(project)

    hypo = """We hypothesize that nitrogen doping at the octagonal ring of PHOTH-graphene (C10)
alters the band gap towards 1.2 eV using VASP PBE functional.
Extended 2D lattice mixing is controlled with AMIX=0.2 and BMIX=0.0001 to prevent charge sloshing.
Band structure along high-symmetry k-path will measure the resulting gap."""

    r1 = verifier.verify_discovery_step(project, 1, hypo, oracle_called=False)
    assert r1["saturation_warning"] is None

    r2 = verifier.verify_discovery_step(project, 2, hypo, oracle_called=False)
    assert r2["saturation_warning"] is None

    r3 = verifier.verify_discovery_step(project, 3, hypo, oracle_called=False)
    assert r3["saturation_warning"] is not None
    assert "REASONING PLATEAU DETECTED" in r3["saturation_warning"]
    assert r3["recommendation"] == "FORCE_ORACLE_EXECUTION"

    # Round 4 with oracle call breaks the saturation
    r4 = verifier.verify_discovery_step(
        project, 4, hypo, oracle_called=True, observed_metric=1.20, target_metric_goal=1.20
    )
    assert r4["saturation_warning"] is None
    assert r4["recommendation"] == "CONVERGED_GOAL_REACHED"
