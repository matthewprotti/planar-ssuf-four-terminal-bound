#!/usr/bin/env python3
"""Validate SSUF census, independent results, claim IDs, and dependency pin."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def readme_ids(text: str) -> list[str]:
    return re.findall(r"^### (UC-\d{3})\b", text, flags=re.MULTILINE)


def ledger_ids(text: str) -> list[str]:
    return re.findall(r"^\| (UC-\d{3}) \|", text, flags=re.MULTILINE)


def main() -> None:
    ids_readme = readme_ids((HERE / "README.md").read_text(encoding="utf-8"))
    ids_ledger = ledger_ids((HERE / "CLAIM_LEDGER.md").read_text(encoding="utf-8"))
    if len(ids_readme) != len(set(ids_readme)) or len(ids_ledger) != len(set(ids_ledger)):
        raise ValueError("duplicate claim ID")
    if set(ids_readme) != set(ids_ledger):
        raise ValueError(f"README/ledger claim mismatch: {ids_readme} vs {ids_ledger}")

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

    mutated = json.loads(json.dumps(census))
    mutated["counts"]["realizable_positive_threshold_families"] = 150
    if mutated["counts"] == expected:
        raise AssertionError("count mutation was not applied")

    for filename in ("independent_census_results.json", "symbolic_every_pair_results.json"):
        result = json.loads((HERE / filename).read_text(encoding="utf-8"))
        if result.get("status") != "PASS":
            raise ValueError(f"non-PASS result: {filename}")

    dependency = json.loads((HERE / "DEPENDENCY_MANIFEST.json").read_text(encoding="utf-8"))
    if dependency["dependency_status"] != "provenance_only":
        raise ValueError("released proof must not remain an unexpanded dependency")
    for local_file in dependency["local_self_containment"]:
        if not (HERE / local_file).is_file():
            raise ValueError(f"missing local theorem component: {local_file}")

    print("PASS: census hash/counts, independent results, claim IDs, and dependency pin agree")


if __name__ == "__main__":
    main()
