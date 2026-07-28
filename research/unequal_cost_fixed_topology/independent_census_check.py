#!/usr/bin/env python3
"""Clean-room replay of the four-label threshold-family census.

This file does not import ``threshold_family_census.py``.  It enumerates
monotone truth tables directly and searches every integer quota from zero to
the total weight, then independently replays every stored witness and trade.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
N = 4
SUBSETS = tuple(range(1 << N))


def stable_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def family_from_bits(bits: int) -> frozenset[int]:
    return frozenset(mask for mask in SUBSETS if bits & (1 << mask))


def is_monotone_truth_table(bits: int) -> bool:
    for mask in SUBSETS:
        if not bits & (1 << mask):
            continue
        for index in range(N):
            if not mask & (1 << index):
                if not bits & (1 << (mask | (1 << index))):
                    return False
    return True


def subset_weight(mask: int, weights: Sequence[int]) -> int:
    return sum(weights[index] for index in range(N) if mask & (1 << index))


def threshold_family(weights: Sequence[int], quota: int) -> frozenset[int]:
    return frozenset(mask for mask in SUBSETS if subset_weight(mask, weights) >= quota)


def subset_of(left: int, right: int) -> bool:
    return left & right == left


def minimal_members(family: Iterable[int]) -> tuple[int, ...]:
    items = frozenset(family)
    return tuple(
        sorted(
            mask
            for mask in items
            if not any(other != mask and subset_of(other, mask) for other in items)
        )
    )


def parse_subset(name: str) -> int:
    if name == "∅":
        return 0
    result = 0
    for character in name:
        result |= 1 << (int(character) - 1)
    return result


def incidence_sum(left: int, right: int) -> tuple[int, ...]:
    return tuple(
        int(bool(left & (1 << index))) + int(bool(right & (1 << index)))
        for index in range(N)
    )


def find_trade(positive: frozenset[int]) -> tuple[int, int, int, int] | None:
    negative = frozenset(SUBSETS) - positive
    positive_pairs: dict[tuple[int, ...], tuple[int, int]] = {}
    for left, right in itertools.combinations_with_replacement(sorted(positive), 2):
        positive_pairs.setdefault(incidence_sum(left, right), (left, right))
    for left, right in itertools.combinations_with_replacement(sorted(negative), 2):
        key = incidence_sum(left, right)
        if key in positive_pairs:
            pos_left, pos_right = positive_pairs[key]
            return pos_left, pos_right, left, right
    return None


def permute_subset(mask: int, permutation: Sequence[int]) -> int:
    result = 0
    for old, new in enumerate(permutation):
        if mask & (1 << old):
            result |= 1 << new
    return result


def orbit_key(family: frozenset[int]) -> tuple[int, ...]:
    return min(
        tuple(sorted(permute_subset(mask, permutation) for mask in family))
        for permutation in itertools.permutations(range(N))
    )


def main() -> None:
    payload = json.loads((HERE / "threshold_family_census.json").read_text(encoding="utf-8"))
    unhashed = dict(payload)
    content_hash = unhashed.pop("content_sha256")
    assert content_hash == stable_hash(unhashed)

    monotone = tuple(
        family_from_bits(bits)
        for bits in range(1 << len(SUBSETS))
        if is_monotone_truth_table(bits)
    )
    assert len(monotone) == 168 and len(set(monotone)) == 168

    found: dict[frozenset[int], tuple[tuple[int, ...], int]] = {}
    cumulative = []
    for bound in range(1, 5):
        for weights in itertools.product(range(1, bound + 1), repeat=N):
            if max(weights) != bound:
                continue
            for quota in range(sum(weights) + 1):
                found.setdefault(threshold_family(weights, quota), (weights, quota))
        cumulative.append(len(found))
    assert cumulative == [5, 53, 121, 149]

    excluded = tuple(family for family in monotone if family not in found)
    empty = tuple(family for family in excluded if not family)
    nonthreshold = tuple(family for family in excluded if family)
    assert len(empty) == 1 and len(nonthreshold) == 18
    independent_trades = {family: find_trade(family) for family in nonthreshold}
    assert all(trade is not None for trade in independent_trades.values())

    rows_by_family = {}
    rows_by_id = {}
    for row in payload["realizable_families"]:
        family = family_from_bits(int(row["family_bitmask_hex"], 16))
        weights = tuple(row["integer_weights"])
        quota = row["integer_threshold"]
        assert threshold_family(weights, quota) == family
        assert all(weight > 0 for weight in weights)
        assert max(weights) <= 4
        assert [parse_subset(item) for item in row["minimal_feasible_sets"]] == list(
            minimal_members(family)
        )
        rows_by_family[family] = row
        rows_by_id[row["id"]] = row
    assert set(rows_by_family) == set(found)
    assert len(rows_by_id) == 149

    stored_nonthreshold = set()
    for row in payload["nonthreshold_trade_certificates"]:
        family = family_from_bits(int(row["family_bitmask_hex"], 16))
        positive = [parse_subset(item) for item in row["positive_trade_sets"]]
        negative = [parse_subset(item) for item in row["negative_trade_sets"]]
        assert all(item in family for item in positive)
        assert all(item not in family for item in negative)
        assert incidence_sum(*positive) == incidence_sum(*negative)
        assert tuple(row["common_incidence_sum"]) == incidence_sum(*positive)
        stored_nonthreshold.add(family)
    assert stored_nonthreshold == set(nonthreshold)

    every_pair = frozenset(mask for mask in SUBSETS if mask.bit_count() >= 2)
    singleton = tuple(family for family in found if any((1 << i) in family for i in range(N)))
    no_singleton = tuple(family for family in found if not any((1 << i) in family for i in range(N)))
    remaining = tuple(family for family in no_singleton if family != every_pair)
    assert len(singleton) == 54
    assert len(remaining) == 94
    assert len({orbit_key(family) for family in found}) == 26
    assert len({orbit_key(family) for family in remaining}) == 15

    candidate_families = {
        family_from_bits(int(rows_by_id[family_id]["family_bitmask_hex"], 16))
        for family_id in payload["unequal_candidate_family_ids"]
    }
    assert candidate_families == set(remaining)

    result = {
        "status": "PASS",
        "method": "clean-room; no imports from threshold_family_census.py",
        "all_monotone_families": len(monotone),
        "positive_threshold_families": len(found),
        "cumulative_weight_bounds": cumulative,
        "nonempty_nonthreshold_families": len(nonthreshold),
        "independently_found_two_trades": len(independent_trades),
        "realizable_orbits": len({orbit_key(family) for family in found}),
        "remaining_labeled_cells": len(remaining),
        "remaining_arbitrary_label_orbits": len({orbit_key(family) for family in remaining}),
    }
    output = HERE / "independent_census_results.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
