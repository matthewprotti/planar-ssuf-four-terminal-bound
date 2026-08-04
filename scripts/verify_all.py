#!/usr/bin/env python3
"""Run every released verifier without modifying committed reference outputs."""

from __future__ import annotations

import filecmp
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
VERIFICATION = ROOT / "verification"
RB003 = ROOT / "research" / "two_scenario_global_constant"
FIXED_GADGET = ROOT / "research" / "fixed_gadget_scenario_cover"
PROGRAMS = (
    "verify_concrete_instance.py",
    "verify_symbolic_family.py",
    "verify_equal_cost_optimality.py",
    "mutation_tests.py",
    "independent_crosscheck.py",
)
REFERENCE_OUTPUTS = (
    "concrete_16_routings.csv",
    "concrete_verification_summary.json",
)


def run(program: Path, *arguments: str, cwd: Path) -> None:
    print(f"\n=== {program.name} ===", flush=True)
    subprocess.run(
        [sys.executable, os.fspath(program), *arguments],
        cwd=cwd,
        check=True,
    )


def verify_fixed_gadget_candidate(tmp: Path) -> None:
    copied = tmp / "fixed_gadget_scenario_cover"
    shutil.copytree(
        FIXED_GADGET,
        copied,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    one = copied / "one_scenario" / "reproduction"
    run(one / "verify_global_one_scenario_theorem.py", cwd=one)
    run(one / "symbolic_every_pair_check.py", cwd=one)

    ladder = copied / "scenario_ladder" / "reproduction"
    run(ladder / "verify_arc_envelope.py", cwd=ladder)
    run(ladder / "verify_gm005_exact.py", cwd=ladder)
    run(ladder / "mutation_tests_gm005.py", cwd=ladder)
    run(ladder / "verify_scenario_ladder.py", cwd=ladder)

    bounded = copied / "bounded_heterogeneity"
    run(bounded / "verify_high_kappa.py", cwd=bounded)

    cover = copied / "scenario_cover" / "reproduction"
    committed_atlas = (
        FIXED_GADGET
        / "scenario_cover"
        / "reproduction"
        / "SCENARIO_COVER_ATLAS_RESULTS.json"
    )
    run(cover / "verify_scenario_cover_results.py", cwd=cover)
    run(cover / "canonicalization_tests.py", cwd=cover)
    run(cover / "mutation_tests.py", cwd=cover)
    run(cover / "scenario_cover_atlas.py", cwd=cover)
    if not filecmp.cmp(
        cover / "SCENARIO_COVER_ATLAS_RESULTS.json",
        committed_atlas,
        shallow=False,
    ):
        raise SystemExit("regenerated scenario-cover atlas differs from the committed reference")
    print("PASS: regenerated scenario-cover atlas is byte-identical to the committed reference.")
    run(cover / "verify_scenario_cover_results.py", cwd=cover)
    run(cover / "verify_sc006_symbolic.py", cwd=cover)
    run(cover / "replay_sc006_exact.py", "--full", cwd=cover)
    run(cover / "mutation_tests_sc006.py", cwd=cover)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="ssuf-verify-") as tmp_name:
        tmp = Path(tmp_name)
        copied = tmp / "verification"
        shutil.copytree(
            VERIFICATION,
            copied,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        for program in PROGRAMS:
            print(f"\n=== {program} ===", flush=True)
            subprocess.run([sys.executable, program], cwd=copied, check=True)

        for name in REFERENCE_OUTPUTS:
            if not filecmp.cmp(copied / name, VERIFICATION / name, shallow=False):
                raise SystemExit(f"regenerated output differs from committed reference: {name}")
            print(f"PASS: regenerated {name} is byte-identical to the committed reference.")

        print("\n=== Fixed-gadget scenario-cover candidate ===", flush=True)
        run(
            VERIFICATION / "verify_fixed_gadget_proof_map.py",
            cwd=ROOT,
        )
        verify_fixed_gadget_candidate(tmp)

    print("\n=== RB-003 deterministic replay ===", flush=True)
    subprocess.run([sys.executable, os.fspath(RB003 / "replay.py")], cwd=RB003, check=True)

    for preflight in (
        "preflight_pdf_text.py",
        "preflight_rb003_pdf_text.py",
        "preflight_fixed_gadget_pdf_text.py",
    ):
        print(f"\n=== {preflight} ===", flush=True)
        subprocess.run(
            [sys.executable, os.fspath(VERIFICATION / preflight)],
            cwd=ROOT,
            check=True,
        )

    print("\nFULL VERIFICATION PASS")


if __name__ == "__main__":
    main()
