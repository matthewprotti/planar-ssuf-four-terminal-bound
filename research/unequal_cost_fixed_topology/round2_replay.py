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
                "remaining_labeled_cells": 94,
                "realizable_arbitrary_label_orbits": 26,
                "remaining_arbitrary_label_orbits": 15,
            },
            "commands": results,
            "generated_output_sha256": output_hashes,
            "limitations": [
                "UC-008 is proved in the human-readable local theorem; software is corroboration.",
                "Zero and negative route-cost differences are outside the theorem domain.",
                "The 94 remaining labeled cells and their boundaries remain open.",
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
