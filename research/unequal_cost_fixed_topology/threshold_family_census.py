#!/usr/bin/env python3
"""Exact census of four-terminal unequal-cost feasibility families.

For positive full-demand route-cost differences k_i=(E_i-C_i)>0 and fractional cheap fractions p_i,
a cheap set S is cost feasible exactly when

    sum_{i in S} k_i >= tau := sum_i k_i p_i.

Thus the feasible cheap sets form a positive weighted threshold family.  This
script classifies all labeled monotone families on four terminals using exact
integer arithmetic.  It constructs small integer witnesses for every realizable
family and two-trade impossibility certificates for every nonempty monotone
family that is not threshold.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
from typing import Iterable, Iterator

N = 4
SUBSETS = tuple(range(1 << N))
FULL = (1 << N) - 1


def is_subset(left: int, right: int) -> bool:
    return left & right == left


def subset_name(mask: int) -> str:
    if mask == 0:
        return "∅"
    return "".join(str(index + 1) for index in range(N) if mask & (1 << index))


def is_antichain(masks: Iterable[int]) -> bool:
    items = tuple(masks)
    return all(
        not (left != right and (is_subset(left, right) or is_subset(right, left)))
        for position, left in enumerate(items)
        for right in items[position + 1 :]
    )


def antichains() -> Iterator[tuple[int, ...]]:
    """Enumerate all 168 antichains of the Boolean lattice on four labels."""

    for family_bits in range(1 << len(SUBSETS)):
        candidate = tuple(mask for mask in SUBSETS if family_bits & (1 << mask))
        if is_antichain(candidate):
            yield candidate


def upward_closure(minimal_sets: Iterable[int]) -> frozenset[int]:
    minima = tuple(minimal_sets)
    return frozenset(mask for mask in SUBSETS if any(is_subset(item, mask) for item in minima))


def minimal_members(family: Iterable[int]) -> tuple[int, ...]:
    items = frozenset(family)
    return tuple(
        sorted(
            mask
            for mask in items
            if not any(other != mask and is_subset(other, mask) for other in items)
        )
    )


def subset_weight(mask: int, weights: tuple[int, ...]) -> int:
    return sum(weights[index] for index in range(N) if mask & (1 << index))


def threshold_family(weights: tuple[int, ...], threshold: int) -> frozenset[int]:
    return frozenset(mask for mask in SUBSETS if subset_weight(mask, weights) >= threshold)


def incidence_sum(left: int, right: int) -> tuple[int, ...]:
    return tuple(
        int(bool(left & (1 << index))) + int(bool(right & (1 << index)))
        for index in range(N)
    )


def find_two_trade(
    positive: frozenset[int], negative: frozenset[int]
) -> tuple[int, int, int, int]:
    """Find A,B positive and C,D negative with 1_A+1_B=1_C+1_D."""

    positive_by_incidence: dict[tuple[int, ...], tuple[int, int]] = {}
    for left, right in combinations_with_replacement(sorted(positive), 2):
        positive_by_incidence.setdefault(incidence_sum(left, right), (left, right))
    for left, right in combinations_with_replacement(sorted(negative), 2):
        incidence = incidence_sum(left, right)
        if incidence in positive_by_incidence:
            pos_left, pos_right = positive_by_incidence[incidence]
            return pos_left, pos_right, left, right
    raise AssertionError("no two-trade certificate found")


def family_bitmask(family: Iterable[int]) -> int:
    return sum(1 << mask for mask in family)


def permute_subset(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for old_label, new_label in enumerate(permutation):
        if mask & (1 << old_label):
            result |= 1 << new_label
    return result


def orbit_key(family: frozenset[int]) -> tuple[int, ...]:
    return min(
        tuple(sorted(permute_subset(mask, permutation) for mask in family))
        for permutation in permutations(range(N))
    )


def stable_sha256(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    all_monotone = tuple(upward_closure(minima) for minima in antichains())
    assert len(all_monotone) == 168
    assert len(set(all_monotone)) == 168

    witnesses: dict[frozenset[int], tuple[tuple[int, ...], int]] = {}
    count_by_weight_bound: list[dict[str, int]] = []
    for bound in range(1, 5):
        for weights in product(range(1, bound + 1), repeat=N):
            if max(weights) != bound:
                continue
            sums = sorted({subset_weight(mask, weights) for mask in SUBSETS})
            for threshold in sums:
                family = threshold_family(weights, threshold)
                witnesses.setdefault(family, (weights, threshold))
        count_by_weight_bound.append(
            {"maximum_integer_weight": bound, "distinct_families": len(witnesses)}
        )

    assert count_by_weight_bound == [
        {"maximum_integer_weight": 1, "distinct_families": 5},
        {"maximum_integer_weight": 2, "distinct_families": 53},
        {"maximum_integer_weight": 3, "distinct_families": 121},
        {"maximum_integer_weight": 4, "distinct_families": 149},
    ]
    assert len(witnesses) == 149

    nonrepresented = tuple(family for family in all_monotone if family not in witnesses)
    empty_families = tuple(family for family in nonrepresented if not family)
    nonthreshold = tuple(family for family in nonrepresented if family)
    assert len(empty_families) == 1
    assert len(nonthreshold) == 18

    every_pair_family = frozenset(mask for mask in SUBSETS if mask.bit_count() >= 2)
    assert every_pair_family in witnesses

    realizable_rows: list[dict[str, object]] = []
    family_to_id: dict[frozenset[int], str] = {}
    sorted_realizable = sorted(
        witnesses, key=lambda family: (minimal_members(family), family_bitmask(family))
    )
    for index, family in enumerate(sorted_realizable, start=1):
        weights, threshold = witnesses[family]
        assert all(weight > 0 for weight in weights)
        assert 0 <= threshold <= sum(weights)
        assert FULL in family
        assert threshold_family(weights, threshold) == family
        family_id = f"F{index:03d}"
        family_to_id[family] = family_id
        has_feasible_singleton = any((1 << label) in family for label in range(N))
        if has_feasible_singleton:
            search_status = "bounded_by_feasible_singleton_at_most_1"
        elif family == every_pair_family:
            search_status = "sharp_every_pair_cell_value_L"
        else:
            search_status = "open_unequal_cost_candidate_cell"
        realizable_rows.append(
            {
                "id": family_id,
                "family_bitmask_hex": f"0x{family_bitmask(family):04x}",
                "minimal_feasible_sets": [subset_name(mask) for mask in minimal_members(family)],
                "number_of_feasible_sets": len(family),
                "integer_weights": list(weights),
                "integer_threshold": threshold,
                "maximum_integer_weight": max(weights),
                "has_feasible_singleton": has_feasible_singleton,
                "search_status": search_status,
            }
        )

    nonthreshold_rows: list[dict[str, object]] = []
    for index, family in enumerate(
        sorted(nonthreshold, key=lambda item: (minimal_members(item), family_bitmask(item))), start=1
    ):
        negative = frozenset(SUBSETS) - family
        pos_left, pos_right, neg_left, neg_right = find_two_trade(family, negative)
        incidence = incidence_sum(pos_left, pos_right)
        assert incidence == incidence_sum(neg_left, neg_right)
        assert pos_left in family and pos_right in family
        assert neg_left in negative and neg_right in negative
        nonthreshold_rows.append(
            {
                "id": f"N{index:02d}",
                "family_bitmask_hex": f"0x{family_bitmask(family):04x}",
                "minimal_feasible_sets": [subset_name(mask) for mask in minimal_members(family)],
                "positive_trade_sets": [subset_name(pos_left), subset_name(pos_right)],
                "negative_trade_sets": [subset_name(neg_left), subset_name(neg_right)],
                "common_incidence_sum": list(incidence),
            }
        )

    orbit_count = len({orbit_key(family) for family in witnesses})
    assert orbit_count == 26

    no_singleton = tuple(
        family for family in witnesses if all((1 << index) not in family for index in range(N))
    )
    unequal_candidate_cells = tuple(
        family for family in no_singleton if family != every_pair_family
    )
    assert len(no_singleton) == 95
    assert len(unequal_candidate_cells) == 94
    unequal_candidate_orbits: dict[tuple[int, ...], frozenset[int]] = {}
    for family in sorted(
        unequal_candidate_cells,
        key=lambda item: (minimal_members(item), family_bitmask(item)),
    ):
        unequal_candidate_orbits.setdefault(orbit_key(family), family)
    assert len(unequal_candidate_orbits) == 15

    max_weight_distribution = Counter(max(weights) for weights, _ in witnesses.values())
    assert max_weight_distribution == Counter({1: 5, 2: 48, 3: 68, 4: 28})

    payload: dict[str, object] = {
        "schema_version": "ssuf-unequal-cost-threshold-census-v0.2",
        "status": "exact finite census; unrefereed research artifact; stored integer witnesses are existence certificates, not canonical representations",
        "ground_set": [1, 2, 3, 4],
        "subset_encoding": "bit i-1 denotes terminal i; family bit m denotes subset mask m",
        "counts": {
            "all_labeled_monotone_families": 168,
            "realizable_positive_threshold_families": 149,
            "nonempty_nonthreshold_families": 18,
            "empty_family_excluded_by_full_set_feasibility": 1,
            "realizable_orbits_under_all_terminal_permutations": orbit_count,
            "families_with_no_feasible_singleton": len(no_singleton),
            "cells_remaining_after_every_pair_theorem": len(unequal_candidate_cells),
            "remaining_orbits_under_all_terminal_permutations": len(
                unequal_candidate_orbits
            ),
        },
        "witness_interpretation": "for each realizable family, at least one positive integer representation with maximum weight at most four; not unique, canonical, or minimum-sum",
        "count_by_integer_weight_bound": count_by_weight_bound,
        "small_witness_max_weight_distribution": {
            str(weight): count for weight, count in sorted(max_weight_distribution.items())
        },
        "realizable_families": realizable_rows,
        "every_pair_cell": {
            "family_id": family_to_id[every_pair_family],
            "minimal_feasible_sets": [
                subset_name(mask) for mask in minimal_members(every_pair_family)
            ],
            "status": "analytic theorem gives exact supremum L on this cell",
        },
        "unequal_candidate_family_ids": [
            family_to_id[family]
            for family in sorted(
                unequal_candidate_cells,
                key=lambda item: (minimal_members(item), family_bitmask(item)),
            )
        ],
        "unequal_candidate_orbit_representatives": [
            {
                "family_id": family_to_id[family],
                "minimal_feasible_sets": [
                    subset_name(mask) for mask in minimal_members(family)
                ],
            }
            for family in unequal_candidate_orbits.values()
        ],
        "nonthreshold_trade_certificates": nonthreshold_rows,
        "empty_family_certificate": {
            "reason": "tau=sum_i k_i p_i <= sum_i k_i, so the full cheap set is always feasible",
        },
    }
    payload["content_sha256"] = stable_sha256(payload)

    output = Path(__file__).with_name("threshold_family_census.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("PASS: enumerated all 168 labeled monotone families on four terminals")
    print("PASS: constructed positive integer threshold witnesses for exactly 149 families")
    print("PASS: every witness uses weights in {1,2,3,4}")
    print("PASS: certified all 18 nonempty nonthreshold families by exact two-trades")
    print("PASS: the remaining family is empty and impossible because the full set is feasible")
    print(
        "PASS: 26 total permutation orbits; "
        "94 labeled cells in 15 orbits remain after the every-pair theorem"
    )
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
