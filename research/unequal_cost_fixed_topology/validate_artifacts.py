#!/usr/bin/env python3
"""Validate SSUF counts, claim IDs, provenance pins, and replay artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
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
    readme_ids = re.findall(r"^### (UC-\d{3})\b", (HERE / "README.md").read_text(encoding="utf-8"), flags=re.MULTILINE)
    for label, ids in (("claim", claim_ids), ("theorem", theorem_ids), ("README", readme_ids)):
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate {label} ID")
    required_core = {f"UC-{value:03d}" for value in range(1, 20)}
    if not required_core.issubset(set(theorem_ids)):
        raise ValueError(f"theorem ledger missing core IDs: {sorted(required_core - set(theorem_ids))}")
    if set(claim_ids) != set(theorem_ids) or set(theorem_ids) != set(readme_ids):
        raise ValueError(
            f"UC claim IDs differ: README={readme_ids}, claims={claim_ids}, theorems={theorem_ids}"
        )

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
        "signed_single_generator_results.json",
        "nonpositive_difference_results.json",
        "nonpositive_difference_grid_results.json",
        "cost_free_stratum_results.json",
        "positive_three_pair_clique_results.json",
    )
    for filename in results:
        result = json.loads((HERE / filename).read_text(encoding="utf-8"))
        if result.get("status") != "PASS":
            raise ValueError(f"non-PASS result: {filename}")

    reconciliation = json.loads(
        (HERE / "census_reconciliation_results.json").read_text(encoding="utf-8")
    )
    expected_stages = [
        {
            "stage": "after_UC_006_and_UC_008",
            "status": "historical_initial_remainder",
            "labeled_cells": 94,
            "abstract_label_orbits": 15,
        },
        {
            "stage": "after_UC_013",
            "status": "historical_intermediate_remainder",
            "labeled_cells": 89,
            "abstract_label_orbits": 13,
        },
        {
            "stage": "after_UC_017",
            "status": "historical_intermediate_remainder",
            "labeled_cells": 83,
            "abstract_label_orbits": 12,
        },
        {
            "stage": "after_UC_023",
            "status": "current_open_frontier",
            "labeled_cells": 79,
            "abstract_label_orbits": 11,
        },
    ]
    if reconciliation["frontier_stages"] != expected_stages:
        raise ValueError("positive-frontier stage history changed")
    current_frontier = set(reconciliation["current_frontier_family_ids"])
    if len(current_frontier) != 79 or len(reconciliation["current_frontier_orbits"]) != 11:
        raise ValueError("current 79-cell/11-orbit frontier changed")
    resolved_ids = reconciliation["resolved_family_ids"]
    if len(resolved_ids["UC_013"]) != 5:
        raise ValueError("UC-013 resolved-family list changed")
    if (
        len(resolved_ids["UC_017_all_single_generator"]) != 11
        or len(resolved_ids["UC_017_new_beyond_UC_013"]) != 6
    ):
        raise ValueError("UC-017 resolved-family lists changed")
    if resolved_ids["UC_023"] != ["F042", "F068", "F094", "F105"]:
        raise ValueError("UC-023 resolved-family list changed")
    if current_frontier & set(resolved_ids["UC_017_all_single_generator"] + resolved_ids["UC_023"]):
        raise ValueError("a proved resolved family remains in the current frontier")

    exact_witnesses = json.loads((HERE / "exact_open_cell_witnesses.json").read_text(encoding="utf-8"))
    witness_ids = [row["family_id"] for row in exact_witnesses]
    if len(exact_witnesses) != 10 or len(witness_ids) != len(set(witness_ids)):
        raise ValueError("expected ten distinct current open-cell witnesses")
    if "F042" in witness_ids:
        raise ValueError("solved historical cell F042 remains in the current witness atlas")
    if not set(witness_ids).issubset(current_frontier):
        raise ValueError("a current witness is outside the reconciled 79-cell frontier")
    if not all(Fraction(row["exact_minimum_maximum_deviation"]) > 1 for row in exact_witnesses):
        raise ValueError("an exact open-cell witness is not greater than one")
    signed = json.loads((HERE / "signed_difference_census.json").read_text(encoding="utf-8"))
    if signed["unique_signed_unate_threshold_families"] != 1881:
        raise ValueError("signed-family census changed")
    if signed["upward_closed_original_coordinate_families"] != 149:
        raise ValueError("positive-family subset of signed census changed")
    single_generator = json.loads((HERE / "signed_single_generator_results.json").read_text(encoding="utf-8"))
    if single_generator["nonzero_signed_representations"] != 176:
        raise ValueError("signed single-generator regime count changed")
    nonpositive = json.loads((HERE / "nonpositive_difference_results.json").read_text(encoding="utf-8"))
    if (nonpositive["value_one_sign_zero_strata"], nonpositive["chain_sign_zero_strata"]) != (73, 6):
        raise ValueError("non-all-positive stratum classification changed")
    grid = json.loads((HERE / "nonpositive_difference_grid_results.json").read_text(encoding="utf-8"))
    if (grid["sign_zero_patterns"], grid["exact_grid_cases"]) != (79, 31995):
        raise ValueError("nonpositive finite-grid declaration changed")
    cost_free = json.loads((HERE / "cost_free_stratum_results.json").read_text(encoding="utf-8"))
    if cost_free["exact_value"] != "4/5" or cost_free["exact_grid_cases"] <= 0:
        raise ValueError("cost-free exact-value artifact changed")
    clique = json.loads((HERE / "positive_three_pair_clique_results.json").read_text(encoding="utf-8"))
    if (clique["positive_frontier_after"], clique["abstract_orbits_after"]) != (79, 11):
        raise ValueError("three-pair clique frontier reduction changed")

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

    master = (HERE / "MASTER_OBJECTIVE_AND_COST_REALIZATION.md").read_text(encoding="utf-8")
    for required_text in (
        r"\Phi(k,p,d)",
        "nonnegative, commodity-independent",
        r"c_i^{\mathrm E}=\frac{\max\{k_i,0\}}{d_i}",
    ):
        if required_text not in master:
            raise ValueError(f"master objective/realization text missing: {required_text}")

    scope = (HERE / "POSITIVE_DIFFERENCE_SCOPE.md").read_text(encoding="utf-8")
    if "genuine restriction" not in scope or "without-loss-of-generality" not in scope:
        raise ValueError("positive-difference restriction is not explicit")
    if "89" not in (HERE / "NO_PAIR_SCALAR_LEMMAS.md").read_text(encoding="utf-8"):
        raise ValueError("historical no-pair reduction is not recorded")
    if "83" not in (HERE / "SIGNED_SINGLE_GENERATOR_THEOREM.md").read_text(encoding="utf-8"):
        raise ValueError("historical 83-cell UC-017 stage is not recorded")
    if "9/8" not in (HERE / "NONPOSITIVE_DIFFERENCE_THEOREM.md").read_text(encoding="utf-8"):
        raise ValueError("non-all-positive theorem is not recorded")
    if "1,881" not in (HERE / "SIGNED_DIFFERENCE_REDUCTION.md").read_text(encoding="utf-8"):
        raise ValueError("signed census statement is not recorded")

    print(
        "PASS: theorem IDs, staged frontier, current witnesses, orbit tables, "
        "result artifacts, master objective, and provenance pin agree"
    )


if __name__ == "__main__":
    main()
