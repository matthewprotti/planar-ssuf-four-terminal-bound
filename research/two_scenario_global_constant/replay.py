#!/usr/bin/env python3
"""Complete deterministic replay for the RB-003 v5 proof-integrated package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(path: Path, *args: str) -> None:
    command = [sys.executable, str(path), *args]
    print(f"\n$ {' '.join(command)}", flush=True)
    subprocess.run(command, check=True)


def main() -> None:
    root = Path(__file__).resolve().parent

    run(root / "build_manifest.py", "--check")
    run(root / "proof_review_integration_check.py")
    run(root / "verify_two_scenario_global_constant.py")
    run(root / "secondary_regression_check.py")

    proof_integration = json.loads(
        (root / "PROOF_REVIEW_INTEGRATION_REPORT.json").read_text(encoding="utf-8")
    )
    certificate = json.loads(
        (root / "two_scenario_17_8_certificate.json").read_text(encoding="utf-8")
    )
    recognition = json.loads(
        (root / "threshold_recognition_report.json").read_text(encoding="utf-8")
    )
    census = json.loads(
        (root / "two_scenario_case_census.json").read_text(encoding="utf-8")
    )
    secondary = json.loads(
        (root / "secondary_regression_report.json").read_text(encoding="utf-8")
    )
    nonattainment = json.loads(
        (root / "nonattainment_logic_report.json").read_text(encoding="utf-8")
    )

    assert proof_integration["result"] == "PASS"
    assert len(proof_integration["required_exact_checks_passed"]) == 6
    assert len(proof_integration["required_normalized_checks_passed"]) == 6
    assert len(proof_integration["forbidden_formulations_absent"]) == 5
    assert len(proof_integration["cross_document_scope_checks_passed"]) == 3

    assert certificate["feasibility_semantics"].startswith("for each scenario")
    assert certificate["finite_minimum_max_upper_deviation"] == "1061/500"
    assert certificate["limiting_supremum"] == "17/8"
    assert certificate["global_supremum_attained_by_any_finite_legal_instance"] is False
    assert certificate["intrinsic_family"] == "upward closure of {123,124,234}"
    assert certificate["integer_scaling"]["unavoidable_upper_deviation"] == 8488
    assert certificate["any_feasible_route_equal_to_fractional_budget"] is False

    assert recognition["all_downsets"] == 168
    assert recognition["positive_scalar_threshold_downsets"] == 149
    assert recognition["nonempty_nonthreshold_downsets"] == 18
    assert len(recognition["nonthreshold_two_trade_certificates"]) == 18

    assert census["unordered_pattern_pairs"] == 11175
    assert census["unique_no_pair_robust_families"] == 16
    assert "need not admit a common baseline" in census["interpretation"]

    assert secondary["secondary_lower_instance"]["finite_value"] == "2305/1096"
    grid = secondary["analytic_envelope_grid_regression"]
    assert grid["central_grid_maximum"] == "17/8"
    assert grid["outer_grid_maximum"] == "2"
    assert "not continuous optimization" in grid["interpretation"]
    assert secondary["threshold_recognition"]["nonthreshold_with_two_trades"] == 18

    assert nonattainment["equality_delta"] == "3/4"
    assert nonattainment["required_h_u"] == "1"
    assert nonattainment["conclusion"].endswith("legal finite instance")

    run(root / "build_manifest.py", "--check")
    print(
        "\nCOMPLETE PASS: RB-003 v5 authenticated before replay, proof-review "
        "edits checked, regenerated deterministically, and authenticated again."
    )


if __name__ == "__main__":
    main()
