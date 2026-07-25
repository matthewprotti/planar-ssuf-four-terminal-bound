#!/usr/bin/env python3
"""Reconcile SSUF census units and materialize orbit sizes/stabilizers."""

from __future__ import annotations

import json
from itertools import permutations, product
from pathlib import Path

import threshold_family_census as census

HERE = Path(__file__).resolve().parent
PERMS = tuple(permutations(range(census.N)))


def permuted_family(family: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    return frozenset(census.permute_subset(mask, permutation) for mask in family)


def orbit(family: frozenset[int]) -> frozenset[frozenset[int]]:
    return frozenset(permuted_family(family, permutation) for permutation in PERMS)


def row(family: frozenset[int], family_ids: dict[frozenset[int], str]) -> dict[str, object]:
    members = sorted(orbit(family), key=lambda item: family_ids[item])
    stabilizer = sum(permuted_family(family, permutation) == family for permutation in PERMS)
    assert len(members) * stabilizer == 24
    return {
        "representative_id": family_ids[family],
        "representative_minimal_feasible_sets": [
            census.subset_name(mask) for mask in census.minimal_members(family)
        ],
        "member_family_ids": [family_ids[item] for item in members],
        "orbit_size": len(members),
        "stabilizer_size": stabilizer,
    }


def main() -> None:
    all_monotone = tuple(census.upward_closure(minima) for minima in census.antichains())
    witnesses: dict[frozenset[int], tuple[tuple[int, ...], int]] = {}
    for bound in range(1, 5):
        for weights in product(range(1, bound + 1), repeat=census.N):
            if max(weights) != bound:
                continue
            for threshold in sorted({census.subset_weight(mask, weights) for mask in census.SUBSETS}):
                witnesses.setdefault(census.threshold_family(weights, threshold), (weights, threshold))

    nonrepresented = tuple(family for family in all_monotone if family not in witnesses)
    nonempty_nonthreshold = tuple(family for family in nonrepresented if family)
    empty = tuple(family for family in nonrepresented if not family)
    every_pair = frozenset(mask for mask in census.SUBSETS if mask.bit_count() >= 2)
    singleton = tuple(
        family for family in witnesses if any((1 << index) in family for index in range(census.N))
    )
    remaining = tuple(
        family
        for family in witnesses
        if family not in singleton and family != every_pair
    )

    assert (len(witnesses), len(nonempty_nonthreshold), len(empty)) == (149, 18, 1)
    assert len(witnesses) + len(nonempty_nonthreshold) + len(empty) == 168
    assert (len(singleton), 1, len(remaining)) == (54, 1, 94)
    assert len(singleton) + 1 + len(remaining) == 149

    ordered = sorted(witnesses, key=lambda family: (census.minimal_members(family), census.family_bitmask(family)))
    family_ids = {family: f"F{index:03d}" for index, family in enumerate(ordered, start=1)}

    all_representatives: dict[tuple[int, ...], frozenset[int]] = {}
    for family in ordered:
        all_representatives.setdefault(census.orbit_key(family), family)
    remaining_representatives: dict[tuple[int, ...], frozenset[int]] = {}
    for family in sorted(remaining, key=lambda item: family_ids[item]):
        remaining_representatives.setdefault(census.orbit_key(family), family)
    assert len(all_representatives) == 26
    assert len(remaining_representatives) == 15

    result = {
        "status": "PASS",
        "ambient_partition": {
            "positive_threshold": 149,
            "nonempty_nonthreshold": 18,
            "empty_impossible": 1,
            "total": 168,
        },
        "search_partition": {
            "feasible_singleton": 54,
            "every_pair_no_singleton": 1,
            "remaining_labeled_cells": 94,
            "total_positive_threshold": 149,
        },
        "acting_group": "full arbitrary-label S4, order 24",
        "fixed_graph_role_preserving_automorphisms": 1,
        "all_realizable_orbits": [row(family, family_ids) for family in all_representatives.values()],
        "remaining_orbits": [row(family, family_ids) for family in remaining_representatives.values()],
        "formal_optimization_units": "all 94 labeled remaining cells",
    }
    output = HERE / "census_reconciliation_results.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
