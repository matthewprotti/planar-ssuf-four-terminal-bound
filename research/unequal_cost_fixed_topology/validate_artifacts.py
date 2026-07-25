#!/usr/bin/env python3
"""Validate SSUF counts, claim IDs, provenance pins, and replay artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def ledger_ids(path: str) -> list[str]:
    return re.findall(r"^\| (UC-\d{3}) \|", (HERE / path).read_text(encoding="utf-8"), flags=re.MULTILINE)


def main() -> None:
    claim_ids = ledger_ids("CLAIM_LEDGER.md")
    theorem_ids = ledger_ids("THEOREM_LEDGER.md")
    for label, ids in (("claim", claim_ids), ("theorem", theorem_ids)):
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate {label} ID")
    required_core = {f"UC-{value:03d}" for value in range(1, 12)}
    if not required_core.issubset(set(theorem_ids)):
        raise ValueError(f"theorem ledger missing core IDs: {sorted(required_core - set(theorem_ids))}")
    if not set(claim_ids).issubset(set(theorem_ids) | {"UC-021", "UC-030"}):
        raise ValueError("claim ledger contains unexplained IDs")

    census = json.loads((HERE / "threshold_family_census.json").read_text(encoding="utf-8"))
    unhashed = dict(census)
    stored = unhashed.pop("content_sha256")
    if stored != stable_hash(unhashed):
        raise ValueError("census content hash mismatch")
    expected = {
        "all_labeled_monotone_families": 168,
        "realizable_positive_threshold_families": 149,
        "nonempty_nonthreshold_families": 18,
        "empty_family_excluded_by_full_set_feasibility": 1,
        "realizable_orbits_under_all_terminal_permutations": 26,
        "families_with_no_feasible_singleton": 95,
        "cells_remaining_after_every_pair_theorem": 94,
        "remaining_orbits_under_all_terminal_permutations": 15,
    }
    if census["counts"] != expected:
        raise ValueError(f"unexpected census counts: {census['counts']}")

    results = (
        "independent_census_results.json",
        "symbolic_every_pair_results.json",
        "exact_algebra_results.json",
        "release_family_equivalence_results.json",
        "census_reconciliation_results.json",
        "witness_examples.json",
    )
    for filename in results:
        result = json.loads((HERE / filename).read_text(encoding="utf-8"))
        if result.get("status") != "PASS":
            raise ValueError(f"non-PASS result: {filename}")

    reconciliation = json.loads(
        (HERE / "census_reconciliation_results.json").read_text(encoding="utf-8")
    )
    if reconciliation["ambient_partition"] != {
        "positive_threshold": 149,
        "nonempty_nonthreshold": 18,
        "empty_impossible": 1,
        "total": 168,
    }:
        raise ValueError("ambient partition mismatch")
    if reconciliation["search_partition"] != {
        "feasible_singleton": 54,
        "every_pair_no_singleton": 1,
        "remaining_labeled_cells": 94,
        "total_positive_threshold": 149,
    }:
        raise ValueError("search partition mismatch")
    for orbit_row in reconciliation["all_realizable_orbits"] + reconciliation["remaining_orbits"]:
        if orbit_row["orbit_size"] * orbit_row["stabilizer_size"] != 24:
            raise ValueError("orbit-stabilizer mismatch")

    dependency = json.loads((HERE / "DEPENDENCY_MANIFEST.json").read_text(encoding="utf-8"))
    if dependency["dependency_status"] != "provenance_only":
        raise ValueError("released proof must not remain an unexpanded dependency")
    for local_file in dependency["local_self_containment"]:
        if not (HERE / local_file).is_file():
            raise ValueError(f"missing local theorem component: {local_file}")

    scope = (HERE / "POSITIVE_DIFFERENCE_SCOPE.md").read_text(encoding="utf-8")
    if "genuine restriction" not in scope or "without-loss-of-generality" not in scope:
        raise ValueError("positive-difference restriction is not explicit")

    print("PASS: theorem IDs, census partitions, orbit tables, result artifacts, and provenance pin agree")


if __name__ == "__main__":
    main()
