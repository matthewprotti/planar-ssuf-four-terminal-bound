#!/usr/bin/env python3
"""Run the complete SSUF round-two replay in a disposable copied directory."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
GENERATED = {
    "threshold_family_census.json",
    "independent_census_results.json",
    "symbolic_every_pair_results.json",
    "exact_algebra_results.json",
    "release_family_equivalence_results.json",
    "census_reconciliation_results.json",
    "witness_examples.json",
    "exact_open_cell_witnesses.json",
    "signed_difference_census.json",
    "signed_single_generator_results.json",
    "nonpositive_difference_results.json",
    "nonpositive_difference_grid_results.json",
    "cost_free_stratum_results.json",
    "positive_three_pair_clique_results.json",
    "round2_replay_report.json",
}
COMMANDS = [
    [sys.executable, "build_artifact_manifest.py", "--check"],
    [sys.executable, "threshold_family_census.py"],
    [sys.executable, "independent_census_check.py"],
    [sys.executable, "census_reconciliation_check.py"],
    [sys.executable, "symbolic_every_pair_check.py"],
    [sys.executable, "exact_algebra_audit.py"],
    [sys.executable, "release_family_equivalence_check.py"],
    [sys.executable, "generate_witness_examples.py"],
    [sys.executable, "exact_open_cell_witnesses.py"],
    [sys.executable, "signed_difference_census.py"],
    [sys.executable, "signed_single_generator_check.py"],
    [sys.executable, "nonpositive_difference_check.py"],
    [sys.executable, "nonpositive_difference_grid_check.py"],
    [sys.executable, "cost_free_stratum_check.py"],
    [sys.executable, "positive_three_pair_clique_check.py"],
    [sys.executable, "validate_artifacts.py"],
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("SSUF replay requires Python 3.11 or later")

    with tempfile.TemporaryDirectory(prefix="ssuf-r2-") as raw:
        work = Path(raw) / "unequal_cost_fixed_topology"
        shutil.copytree(
            HERE,
            work,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", *GENERATED),
        )
        env = os.environ.copy()
        env.update(
            {
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONHASHSEED": "0",
                "NO_PROXY": "*",
                "no_proxy": "*",
            }
        )
        results = []
        for command in COMMANDS:
            completed = subprocess.run(
                command,
                cwd=work,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            results.append(
                {
                    "command": command,
                    "exit_code": completed.returncode,
                    "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
                    "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest(),
                    "stdout_tail": completed.stdout.splitlines()[-8:],
                    "stderr_tail": completed.stderr.splitlines()[-8:],
                }
            )
            if completed.returncode:
                print(completed.stdout)
                print(completed.stderr, file=sys.stderr)
                raise SystemExit(completed.returncode)

        census = json.loads((work / "threshold_family_census.json").read_text())
        reconciliation = json.loads(
            (work / "census_reconciliation_results.json").read_text()
        )
        assert census["counts"]["all_labeled_monotone_families"] == 168
        assert census["counts"]["realizable_positive_threshold_families"] == 149
        assert census["counts"]["nonempty_nonthreshold_families"] == 18
        assert census["counts"]["cells_remaining_after_every_pair_theorem"] == 94
        assert reconciliation["search_partition"]["feasible_singleton"] == 54
        assert len(reconciliation["all_realizable_orbits"]) == 26
        assert len(reconciliation["remaining_orbits"]) == 15
        exact_witnesses = json.loads((work / "exact_open_cell_witnesses.json").read_text())
        assert len(exact_witnesses) == 11
        assert all(__import__("fractions").Fraction(row["exact_minimum_maximum_deviation"]) > 1 for row in exact_witnesses)
        signed = json.loads((work / "signed_difference_census.json").read_text())
        assert signed["unique_signed_unate_threshold_families"] == 1881
        assert signed["upward_closed_original_coordinate_families"] == 149
        single_generator = json.loads((work / "signed_single_generator_results.json").read_text())
        nonpositive = json.loads((work / "nonpositive_difference_results.json").read_text())
        nonpositive_grid = json.loads((work / "nonpositive_difference_grid_results.json").read_text())
        cost_free = json.loads((work / "cost_free_stratum_results.json").read_text())
        clique = json.loads((work / "positive_three_pair_clique_results.json").read_text())
        assert single_generator["nonzero_signed_representations"] == 176
        assert nonpositive["value_one_sign_zero_strata"] == 73
        assert nonpositive["chain_sign_zero_strata"] == 6
        assert nonpositive_grid["sign_zero_patterns"] == 79
        assert nonpositive_grid["exact_grid_cases"] == 31995
        assert cost_free["exact_value"] == "4/5"
        assert cost_free["exact_grid_cases"] > 0
        assert clique["positive_frontier_after"] == 79 and clique["abstract_orbits_after"] == 11

        output_hashes = {
            name: digest(work / name)
            for name in sorted(GENERATED - {"round2_replay_report.json"})
            if (work / name).exists()
        }
        report = {
            "status": "PASS",
            "evidence_class": "deterministic internal exact finite and algebraic replay",
            "python": sys.version,
            "sympy_version": __import__("sympy").__version__,
            "network_required": False,
            "expected_exit_code": 0,
            "artifact_manifest_sha256": digest(work / "artifact_manifest.json"),
            "counts": {
                "monotone_families": 168,
                "positive_threshold_families": 149,
                "nonempty_nonthreshold_families": 18,
                "empty_impossible_families": 1,
                "feasible_singleton_families": 54,
                "every_pair_no_singleton_families": 1,
                "initial_remaining_labeled_cells": 94,
                "no_pair_cells_eliminated_by_UC_013": 5,
                "single_generator_positive_cells_resolved_by_UC_017": 11,
                "new_single_generator_cells_beyond_UC_013": 6,
                "remaining_positive_labeled_cells": 79,
                "positive_three_pair_clique_cells_resolved_by_UC_023": 4,
                "exact_above_one_witness_cells": 11,
                "nonzero_signed_unate_feasibility_families": 1881,
                "realizable_arbitrary_label_orbits": 26,
                "initial_remaining_arbitrary_label_orbits": 15,
                "remaining_positive_arbitrary_label_orbits": 11,
                "nonallpositive_nonzero_sign_zero_strata": 79,
                "nonallpositive_value_one_strata": 73,
                "nonallpositive_value_9_over_8_strata": 6,
                "identically_zero_value_4_over_5_strata": 1,
            },
            "commands": results,
            "generated_output_sha256": output_hashes,
            "limitations": [
                "UC-008 is proved in the human-readable local theorem; software is corroboration.",
                "The non-all-positive objective theorem is human-readable; finite grids and exact identities are corroboration.",
                "The identically-zero cost-difference theorem is fixed-topology only; finite-grid checks are corroboration.",
                "The 79 remaining strictly positive labeled cells and their boundaries remain open.",
                "The release-family extraction is pinned and compared but was transcribed from TeX by a human.",
                "No external clean-environment reproduction is claimed.",
            ],
        }

    output = HERE / "round2_replay_report.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
