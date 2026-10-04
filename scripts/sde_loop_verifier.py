#!/usr/bin/env python3
"""
================================================================================
SDE Closed-Loop Verifier (sde_loop_verifier.py)
================================================================================
Implements closed-loop discovery verification based on the SDE benchmark
(Song, Duan, Kulik et al., 2026) and HKUST Level 3 Autonomous Scientist framework.

Formalizes:
1. Hypothesis Proposal -> Simulation Oracle -> Observation -> Iterative Selection.
2. Anti-Saturation Sentinel: Flags reasoning compute plateau if an agent loops
   in natural language without invoking external deterministic solvers.
3. Generational Lineage: Tracks iteration history, fitness progression, and state.
================================================================================
"""

import os
import sys
import json
import time
from typing import Dict, Any, List, Optional
try:
    from hypothesis_evaluator import HypothesisEvaluator
    from structure_guard import StructureSanityGuard
except ImportError:
    from scripts.hypothesis_evaluator import HypothesisEvaluator
    from scripts.structure_guard import StructureSanityGuard


class SDELoopVerifier:
    """Verifies and orchestrates multi-round closed discovery loop steps."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.state_file = os.path.join(self.base_dir, "runs", "discovery_loop_state.json")
        self.hypothesis_evaluator = HypothesisEvaluator(self.base_dir)
        self.structure_guard = StructureSanityGuard()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"current_project": None, "rounds": [], "active_lineage": []}

    def _save_state(self, state: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def verify_discovery_step(
        self,
        project_name: str,
        round_index: int,
        hypothesis_text: str,
        structure_file: Optional[str] = None,
        observed_metric: Optional[float] = None,
        oracle_called: bool = False,
        target_metric_goal: Optional[float] = None
    ) -> Dict[str, Any]:
        """Audits a discovery iteration step and returns next-action guidance."""
        state = self._load_state()
        if state.get("current_project") != project_name:
            state = {"current_project": project_name, "rounds": [], "active_lineage": []}

        # 1. Audit Hypothesis
        hypo_res = self.hypothesis_evaluator.evaluate_hypothesis(hypothesis_text)

        # 2. Audit Structure if supplied
        struct_res = None
        if structure_file and os.path.exists(structure_file):
            struct_res = self.structure_guard.inspect_file(structure_file)

        # 3. Anti-Saturation Check (SDE 2026: pure LLM reasoning plateaus without external oracles)
        consecutive_unverified = 0
        if not oracle_called:
            for prior_round in reversed(state["rounds"]):
                if not prior_round.get("oracle_called", False):
                    consecutive_unverified += 1
                else:
                    break
            consecutive_unverified += 1

        saturation_warning = None
        if consecutive_unverified >= 3:
            saturation_warning = (
                f"REASONING PLATEAU DETECTED: {consecutive_unverified} consecutive rounds executed without external "
                "numerical or computational simulation oracle. In accordance with SDE (2026), pure linguistic reasoning "
                "saturates. Must invoke ASE/VASPKIT/SIESTA/LAMMPS oracle to ground further progress."
            )

        # 4. Assess Fitness & Progress
        fitness_delta = None
        if observed_metric is not None and len(state["rounds"]) > 0:
            last_metric = state["rounds"][-1].get("observed_metric")
            if last_metric is not None:
                fitness_delta = round(observed_metric - last_metric, 4)

        # Determine Recommendation
        recommendation = "DISPATCH_ORACLE"
        if not hypo_res["passed"]:
            recommendation = "REFINE_HYPOTHESIS"
        elif struct_res and not struct_res["valid"]:
            recommendation = "REPAIR_STRUCTURE"
        elif saturation_warning:
            recommendation = "FORCE_ORACLE_EXECUTION"
        elif target_metric_goal is not None and observed_metric is not None:
            if abs(observed_metric - target_metric_goal) < 0.05:
                recommendation = "CONVERGED_GOAL_REACHED"
            else:
                recommendation = "ITERATE_NEXT_GENERATION"
        elif oracle_called and observed_metric is not None:
            recommendation = "EVALUATE_AND_BRANCH"

        round_entry = {
            "round_index": round_index,
            "timestamp": time.time(),
            "hypothesis": hypothesis_text,
            "hypothesis_score": hypo_res["total_score"],
            "hypothesis_passed": hypo_res["passed"],
            "structure_valid": struct_res["valid"] if struct_res else None,
            "oracle_called": oracle_called,
            "observed_metric": observed_metric,
            "fitness_delta": fitness_delta,
            "recommendation": recommendation
        }

        state["rounds"].append(round_entry)
        self._save_state(state)

        return {
            "project_name": project_name,
            "round_index": round_index,
            "recommendation": recommendation,
            "hypothesis_audit": hypo_res,
            "structure_audit": struct_res,
            "consecutive_unverified_rounds": consecutive_unverified,
            "saturation_warning": saturation_warning,
            "fitness_delta": fitness_delta,
            "total_rounds_logged": len(state["rounds"])
        }

    def reset_project(self, project_name: str) -> None:
        state = {"current_project": project_name, "rounds": [], "active_lineage": []}
        self._save_state(state)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 sde_loop_verifier.py <project_name> <round_index> '<hypothesis_text>'")
        sys.exit(1)

    verifier = SDELoopVerifier()
    res = verifier.verify_discovery_step(
        project_name=sys.argv[1],
        round_index=int(sys.argv[2]),
        hypothesis_text=sys.argv[3]
    )
    print(json.dumps(res, indent=2))
