#!/usr/bin/env python3
"""Check canonical replay identity across two unrelated temporary roots."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True

import round2_replay  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-git-clean-check",
        action="store_true",
        help="maintainer-only: allow the test while preparing a commit",
    )
    args = parser.parse_args()

    if not args.skip_git_clean_check:
        round2_replay.assert_repo_clean("before determinism test")

    membership = round2_replay.verify_release_membership()
    with tempfile.TemporaryDirectory(prefix="ssuf-replay-parent-a-") as raw_a:
        with tempfile.TemporaryDirectory(prefix="ssuf-replay-parent-b-") as raw_b:
            parent_a = Path(raw_a)
            parent_b = Path(raw_b)
            if parent_a.resolve() == parent_b.resolve():
                raise AssertionError("temporary parents must be distinct")

            report_a, _attestation_a = round2_replay.run_replay(parent_a)
            report_b, _attestation_b = round2_replay.run_replay(parent_b)
            bytes_a = round2_replay.canonical_bytes(report_a)
            bytes_b = round2_replay.canonical_bytes(report_b)

            if bytes_a != bytes_b:
                raise AssertionError(
                    "canonical replay bytes differ across temporary roots: "
                    f"a={hashlib.sha256(bytes_a).hexdigest()} "
                    f"b={hashlib.sha256(bytes_b).hexdigest()}"
                )

            forbidden = (
                str(parent_a.resolve()).encode("utf-8"),
                str(parent_b.resolve()).encode("utf-8"),
                str(Path(sys.executable).resolve()).encode("utf-8"),
            )
            if any(value in bytes_a for value in forbidden):
                raise AssertionError(
                    "canonical replay bytes contain a temporary or interpreter path"
                )

    committed = round2_replay.CANONICAL_REPORT.read_bytes()
    if committed != bytes_a:
        raise AssertionError(
            "committed canonical report differs from two-root replay: "
            f"committed={hashlib.sha256(committed).hexdigest()} "
            f"replayed={hashlib.sha256(bytes_a).hexdigest()}"
        )

    if not args.skip_git_clean_check:
        round2_replay.assert_repo_clean("after determinism test")

    print(
        "TWO-ROOT REPLAY IDENTITY PASS: "
        f"canonical_sha256={hashlib.sha256(bytes_a).hexdigest()} "
        f"research_files={membership['research_files_in_archive_input']}"
    )


if __name__ == "__main__":
    main()
