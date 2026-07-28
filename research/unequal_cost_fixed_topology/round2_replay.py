#!/usr/bin/env python3
"""Replay the SSUF round-two checks without mutating the source checkout.

The committed report is a canonical, host-independent result.  Host details and
command-stream hashes belong only in an explicitly requested external
attestation.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import platform
import shutil
import subprocess
import sys
import tempfile
from types import ModuleType
from typing import Any, Iterator

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CANONICAL_REPORT = HERE / "round2_replay_report.json"

GENERATED_OUTPUTS = {
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
}

COMMANDS = (
    ("build_artifact_manifest.py", ("--check",)),
    ("threshold_family_census.py", ()),
    ("independent_census_check.py", ()),
    ("census_reconciliation_check.py", ()),
    ("symbolic_every_pair_check.py", ()),
    ("exact_algebra_audit.py", ()),
    ("release_family_equivalence_check.py", ()),
    ("generate_witness_examples.py", ()),
    ("exact_open_cell_witnesses.py", ()),
    ("signed_difference_census.py", ()),
    ("signed_single_generator_check.py", ()),
    ("nonpositive_difference_check.py", ()),
    ("nonpositive_difference_grid_check.py", ()),
    ("cost_free_stratum_check.py", ()),
    ("positive_three_pair_clique_check.py", ()),
    ("validate_artifacts.py", ()),
)


def digest(path: Path) -> str:
    """Return the SHA-256 digest of a file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    """Serialize a canonical report with stable key order and line endings."""

    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _strings(key)
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def assert_canonical_report_is_portable(
    report: dict[str, Any], temporary_root: Path | None = None
) -> None:
    """Reject host paths and interpreter paths in canonical replay results."""

    forbidden_fragments = {str(Path(sys.executable).resolve())}
    if temporary_root is not None:
        forbidden_fragments.add(str(temporary_root.resolve()))

    for value in _strings(report):
        if PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute():
            raise AssertionError(f"absolute path in canonical report: {value!r}")
        if any(fragment and fragment in value for fragment in forbidden_fragments):
            raise AssertionError(f"host-specific path in canonical report: {value!r}")


def _load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def research_deliverables() -> list[Path]:
    """Return research files that the repository manifest must carry."""

    manifest_module = _load_module(ROOT / "scripts" / "manifest.py", "ssuf_manifest")
    return [
        path
        for path in manifest_module.deliverables()
        if path.is_relative_to(HERE)
    ]


def verify_release_membership() -> dict[str, int]:
    """Verify the root manifest and archive input contain all research files."""

    manifest_module = _load_module(
        ROOT / "scripts" / "manifest.py", "ssuf_manifest_check"
    )
    expected_lines = manifest_module.MANIFEST.read_text(encoding="utf-8").splitlines()
    actual_lines = manifest_module.rendered_lines()
    if expected_lines != actual_lines:
        raise SystemExit(
            "repository SHA256SUMS.txt is stale; run scripts/manifest.py --write"
        )

    archive_module = _load_module(
        ROOT / "scripts" / "build_release.py", "ssuf_build_release_check"
    )
    archived = {
        path.relative_to(ROOT).as_posix() for path in archive_module.manifest_paths()
    }
    required = {
        path.relative_to(ROOT).as_posix() for path in research_deliverables()
    }
    missing = sorted(required - archived)
    if missing:
        raise SystemExit(
            "release archive input omits research files: " + ", ".join(missing)
        )
    return {
        "research_files_in_repository_manifest": len(required),
        "research_files_in_archive_input": len(required),
    }


def git_status() -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.splitlines()


def assert_repo_clean(stage: str) -> None:
    status = git_status()
    if status:
        details = "\n".join(status)
        raise SystemExit(f"source checkout is not clean {stage}:\n{details}")


def _require_runtime() -> tuple[str, str]:
    if sys.version_info < (3, 11):
        raise SystemExit("SSUF replay requires Python 3.11 or later")

    import mpmath
    import sympy

    sympy_version = sympy.__version__
    mpmath_version = mpmath.__version__
    if sympy_version != "1.14.0" or mpmath_version != "1.3.0":
        raise SystemExit(
            "SSUF replay requires sympy==1.14.0 and mpmath==1.3.0; "
            f"found sympy=={sympy_version}, mpmath=={mpmath_version}"
        )
    return sympy_version, mpmath_version


def _read_json(work: Path, name: str) -> Any:
    return json.loads((work / name).read_text(encoding="utf-8"))


def _validate_exact_results(work: Path) -> None:
    from fractions import Fraction

    census = _read_json(work, "threshold_family_census.json")
    reconciliation = _read_json(work, "census_reconciliation_results.json")
    if census["counts"]["all_labeled_monotone_families"] != 168:
        raise AssertionError("unexpected monotone-family count")
    if census["counts"]["realizable_positive_threshold_families"] != 149:
        raise AssertionError("unexpected positive-threshold count")
    if census["counts"]["nonempty_nonthreshold_families"] != 18:
        raise AssertionError("unexpected nonthreshold count")
    if census["counts"]["cells_remaining_after_every_pair_theorem"] != 94:
        raise AssertionError("unexpected initial remaining-cell count")
    if reconciliation["search_partition"]["feasible_singleton"] != 54:
        raise AssertionError("unexpected feasible-singleton count")
    if len(reconciliation["all_realizable_orbits"]) != 26:
        raise AssertionError("unexpected realizable-orbit count")
    if len(reconciliation["remaining_orbits"]) != 15:
        raise AssertionError("unexpected initial remaining-orbit count")

    exact_witnesses = _read_json(work, "exact_open_cell_witnesses.json")
    if len(exact_witnesses) != 11:
        raise AssertionError("unexpected exact-witness count")
    if not all(
        Fraction(row["exact_minimum_maximum_deviation"]) > 1
        for row in exact_witnesses
    ):
        raise AssertionError("an exact witness does not lie strictly above one")

    signed = _read_json(work, "signed_difference_census.json")
    single_generator = _read_json(work, "signed_single_generator_results.json")
    nonpositive = _read_json(work, "nonpositive_difference_results.json")
    nonpositive_grid = _read_json(work, "nonpositive_difference_grid_results.json")
    cost_free = _read_json(work, "cost_free_stratum_results.json")
    clique = _read_json(work, "positive_three_pair_clique_results.json")

    if signed["unique_signed_unate_threshold_families"] != 1881:
        raise AssertionError("unexpected signed-family count")
    if signed["upward_closed_original_coordinate_families"] != 149:
        raise AssertionError("unexpected upward-closed-family count")
    if single_generator["nonzero_signed_representations"] != 176:
        raise AssertionError("unexpected nonzero single-generator count")
    if nonpositive["value_one_sign_zero_strata"] != 73:
        raise AssertionError("unexpected value-one stratum count")
    if nonpositive["chain_sign_zero_strata"] != 6:
        raise AssertionError("unexpected chain-stratum count")
    if nonpositive_grid["sign_zero_patterns"] != 79:
        raise AssertionError("unexpected nonpositive sign-pattern count")
    if nonpositive_grid["exact_grid_cases"] != 31_995:
        raise AssertionError("unexpected nonpositive grid-case count")
    if cost_free["exact_value"] != "4/5" or cost_free["exact_grid_cases"] <= 0:
        raise AssertionError("unexpected cost-free result")
    if clique["positive_frontier_after"] != 79:
        raise AssertionError("unexpected current positive frontier")
    if clique["abstract_orbits_after"] != 11:
        raise AssertionError("unexpected current abstract-orbit frontier")


def _build_canonical_report(
    work: Path, commands: list[dict[str, Any]]
) -> dict[str, Any]:
    _validate_exact_results(work)
    output_hashes = {
        name: digest(work / name)
        for name in sorted(GENERATED_OUTPUTS)
        if (work / name).exists()
    }
    if set(output_hashes) != GENERATED_OUTPUTS:
        missing = sorted(GENERATED_OUTPUTS - set(output_hashes))
        raise AssertionError("replay did not generate: " + ", ".join(missing))

    report: dict[str, Any] = {
        "schema_version": "ssuf-round2-canonical-replay-v0.2",
        "status": "PASS",
        "evidence_class": "deterministic internal exact finite and algebraic replay",
        "network_required": False,
        "expected_exit_code": 0,
        "required_runtime": {
            "python": ">=3.11",
            "sympy": "==1.14.0",
            "mpmath": "==1.3.0",
        },
        "canonicalization": {
            "encoding": "UTF-8",
            "line_endings": "LF",
            "json_keys": "sorted",
            "host_metadata_included": False,
            "command_stream_hashes_included": False,
        },
        "artifact_manifest_sha256": digest(work / "artifact_manifest.json"),
        "release_membership": {
            "manifest_and_archive_input_required": True,
            "research_file_count": len(research_deliverables()),
        },
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
            "positive_three_pair_clique_cells_resolved_by_UC_023": 4,
            "remaining_positive_labeled_cells": 79,
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
        "commands": commands,
        "generated_output_sha256": output_hashes,
        "attestation_policy": {
            "canonical": False,
            "external_path_required": True,
            "purpose": "optional host and command-stream diagnostics only",
        },
        "limitations": [
            "UC-008 is proved in the human-readable local theorem; "
            "software is corroboration.",
            "The non-all-positive objective theorem is human-readable; "
            "finite grids and exact identities are corroboration.",
            "The identically-zero cost-difference theorem is fixed-topology only; "
            "finite-grid checks are corroboration.",
            "The 79 remaining strictly positive labeled cells and their "
            "boundaries remain open.",
            "The release-family extraction is pinned and compared but was "
            "transcribed from TeX by a human.",
            "No external clean-environment reproduction is claimed by the "
            "canonical report alone.",
        ],
    }
    return report


def run_replay(
    temporary_parent: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run the full replay in a disposable copy and return two report classes."""

    sympy_version, mpmath_version = _require_runtime()
    if temporary_parent is not None:
        temporary_parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix="ssuf-r2-", dir=temporary_parent
    ) as raw_directory:
        temporary_root = Path(raw_directory)
        work = temporary_root / "unequal_cost_fixed_topology"
        shutil.copytree(
            HERE,
            work,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                "*.pyc",
                *GENERATED_OUTPUTS,
                CANONICAL_REPORT.name,
                "round2_replay_attestation*.json",
            ),
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

        canonical_commands: list[dict[str, Any]] = []
        diagnostic_commands: list[dict[str, Any]] = []
        for program, arguments in COMMANDS:
            command = [sys.executable, program, *arguments]
            completed = subprocess.run(
                command,
                cwd=work,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            canonical_commands.append(
                {
                    "program": "python",
                    "arguments": [program, *arguments],
                    "exit_code": completed.returncode,
                }
            )
            diagnostic_commands.append(
                {
                    "program": str(Path(sys.executable).resolve()),
                    "arguments": [program, *arguments],
                    "exit_code": completed.returncode,
                    "stdout_sha256": hashlib.sha256(
                        completed.stdout.encode("utf-8")
                    ).hexdigest(),
                    "stderr_sha256": hashlib.sha256(
                        completed.stderr.encode("utf-8")
                    ).hexdigest(),
                }
            )
            if completed.returncode:
                print(completed.stdout)
                print(completed.stderr, file=sys.stderr)
                raise SystemExit(completed.returncode)

        canonical = _build_canonical_report(work, canonical_commands)
        assert_canonical_report_is_portable(canonical, temporary_root)
        canonical_sha256 = hashlib.sha256(canonical_bytes(canonical)).hexdigest()
        attestation = {
            "schema_version": "ssuf-round2-ephemeral-attestation-v0.1",
            "noncanonical": True,
            "must_not_be_committed": True,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "canonical_report_sha256": canonical_sha256,
            "temporary_root": str(temporary_root.resolve()),
            "host": {
                "executable": str(Path(sys.executable).resolve()),
                "python_version": platform.python_version(),
                "implementation": platform.python_implementation(),
                "platform": platform.platform(),
                "sympy_version": sympy_version,
                "mpmath_version": mpmath_version,
            },
            "commands": diagnostic_commands,
        }
        return canonical, attestation


def _external_attestation_path(raw_path: str) -> Path:
    path = Path(raw_path).expanduser().resolve()
    if path.is_relative_to(ROOT):
        raise SystemExit("attestation path must be outside the source repository")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="check the deterministic SSUF round-two replay"
    )
    parser.add_argument(
        "--write-canonical",
        action="store_true",
        help="maintainer-only: replace the committed canonical report",
    )
    parser.add_argument(
        "--attestation",
        metavar="PATH",
        help="write noncanonical host diagnostics outside the repository",
    )
    parser.add_argument(
        "--skip-git-clean-check",
        action="store_true",
        help="maintainer-only: allow replay while preparing a commit",
    )
    parser.add_argument(
        "--skip-release-membership-check",
        action="store_true",
        help="maintainer-only: defer root manifest/archive membership validation",
    )
    args = parser.parse_args()

    if args.write_canonical and not (
        args.skip_git_clean_check and args.skip_release_membership_check
    ):
        raise SystemExit(
            "--write-canonical requires --skip-git-clean-check and "
            "--skip-release-membership-check"
        )
    if args.skip_release_membership_check and not args.write_canonical:
        raise SystemExit(
            "--skip-release-membership-check is valid only with --write-canonical"
        )
    attestation_path = (
        _external_attestation_path(args.attestation) if args.attestation else None
    )
    if not args.skip_git_clean_check:
        assert_repo_clean("before replay")
    if not args.skip_release_membership_check:
        membership = verify_release_membership()
        print(
            "RELEASE MEMBERSHIP PASS: "
            f"{membership['research_files_in_repository_manifest']} research files"
        )

    canonical, attestation = run_replay()
    rendered = canonical_bytes(canonical)
    canonical_sha256 = hashlib.sha256(rendered).hexdigest()

    if args.write_canonical:
        CANONICAL_REPORT.write_bytes(rendered)
        print(f"WROTE CANONICAL: {CANONICAL_REPORT}")
    else:
        if not CANONICAL_REPORT.exists():
            raise SystemExit(
                "canonical replay report is missing; a maintainer must generate it"
            )
        committed = CANONICAL_REPORT.read_bytes()
        if committed != rendered:
            raise SystemExit(
                "canonical replay report differs: "
                f"committed={hashlib.sha256(committed).hexdigest()} "
                f"replayed={canonical_sha256}; a maintainer may regenerate with "
                "--write-canonical --skip-git-clean-check "
                "--skip-release-membership-check"
            )

    if attestation_path is not None:
        attestation_path.parent.mkdir(parents=True, exist_ok=True)
        attestation_path.write_bytes(canonical_bytes(attestation))
        print(f"WROTE NONCANONICAL ATTESTATION: {attestation_path}")

    if not args.skip_git_clean_check:
        assert_repo_clean("after replay")
    print(f"ROUND-TWO REPLAY PASS: canonical_sha256={canonical_sha256}")


if __name__ == "__main__":
    main()
