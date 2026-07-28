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


def orbit_count(families: tuple[frozenset[int], ...]) -> int:
    return len({census.orbit_key(family) for family in families})


def is_uc_013_cell(family: frozenset[int]) -> bool:
    minima = census.minimal_members(family)
    return len(minima) == 1 and minima[0].bit_count() >= 3


def is_uc_017_single_generator_cell(family: frozenset[int]) -> bool:
    minima = census.minimal_members(family)
    return len(minima) == 1 and minima[0].bit_count() >= 2


def is_uc_023_three_pair_clique_cell(family: frozenset[int]) -> bool:
    minima = census.minimal_members(family)
    return (
        len(minima) == 3
        and all(mask.bit_count() == 2 for mask in minima)
        and (minima[0] | minima[1] | minima[2]).bit_count() == 3
    )


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

    uc_013 = tuple(family for family in remaining if is_uc_013_cell(family))
    after_uc_013 = tuple(family for family in remaining if family not in uc_013)
    all_uc_017 = tuple(
        family
        for family in remaining
        if is_uc_017_single_generator_cell(family)
    )
    new_uc_017 = tuple(family for family in all_uc_017 if family not in uc_013)
    after_uc_017 = tuple(
        family for family in remaining if family not in all_uc_017
    )
    uc_023 = tuple(
        family
        for family in after_uc_017
        if is_uc_023_three_pair_clique_cell(family)
    )
    after_uc_023 = tuple(family for family in after_uc_017 if family not in uc_023)

    assert len(uc_013) == 5
    assert len(after_uc_013) == 89
    assert len(all_uc_017) == 11
    assert len(new_uc_017) == 6
    assert len(after_uc_017) == 83
    assert len(uc_023) == 4
    assert len(after_uc_023) == 79
    assert set(uc_013).issubset(all_uc_017)
    assert set(new_uc_017) == set(all_uc_017) - set(uc_013)
    assert not set(all_uc_017) & set(uc_023)
    assert set(remaining) == set(all_uc_017) | set(uc_023) | set(after_uc_023)
    assert (
        orbit_count(remaining),
        orbit_count(after_uc_013),
        orbit_count(after_uc_017),
        orbit_count(after_uc_023),
    ) == (15, 13, 12, 11)

    current_representatives: dict[tuple[int, ...], frozenset[int]] = {}
    for family in sorted(after_uc_023, key=lambda item: family_ids[item]):
        current_representatives.setdefault(census.orbit_key(family), family)
    assert all(
        orbit(family).issubset(set(after_uc_023))
        for family in current_representatives.values()
    )

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
        "frontier_stages": [
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
        ],
        "resolved_family_ids": {
            "UC_013": sorted(family_ids[family] for family in uc_013),
            "UC_017_all_single_generator": sorted(
                family_ids[family] for family in all_uc_017
            ),
            "UC_017_new_beyond_UC_013": sorted(
                family_ids[family] for family in new_uc_017
            ),
            "UC_023": sorted(family_ids[family] for family in uc_023),
        },
        "current_frontier_family_ids": sorted(
            family_ids[family] for family in after_uc_023
        ),
        "current_frontier_orbits": [
            row(family, family_ids)
            for family in current_representatives.values()
        ],
        "formal_optimization_units": (
            "79 current labeled cells after UC-023; the 94-cell and 83-cell "
            "counts are historical stages"
        ),
    }
    output = HERE / "census_reconciliation_results.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
