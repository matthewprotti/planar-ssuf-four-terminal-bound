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


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="ssuf-verify-") as tmp_name:
        copied = Path(tmp_name) / "verification"
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

    print("\n=== preflight_pdf_text.py ===", flush=True)
    subprocess.run(
        [sys.executable, os.fspath(VERIFICATION / "preflight_pdf_text.py")],
        cwd=ROOT,
        check=True,
    )
    print("\nFULL VERIFICATION PASS")


if __name__ == "__main__":
    main()
