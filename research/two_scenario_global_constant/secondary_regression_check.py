#!/usr/bin/env python3
"""Secondary regression code path for RB-003.

This script does not import the primary verifier, but it is not an independent
mathematical derivation: it shares the support matrix, blocker framework, and
lower-family ansatz. It scans all Boolean set families, certifies the 18
nonthreshold exclusions by exact two-trades, uses epsilon=1/137 for a second
finite instance, and checks the supplied analytic envelopes on a finite grid.
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

N = 4
ALL = tuple(range(16))
FULL = 15
# Rows are terminals 1..4; columns are trunk arcs a1..a5.
SUPPORT = (
    (1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1),
    (0, 1, 1, 1, 1),
    (0, 0, 1, 1, 0),
)


def weight(mask: int, vector: tuple[int, ...]) -> int:
    total = 0
    for i in range(N):
        if mask & (1 << i):
            total += vector[i]
    return total


def is_downset(truth: int) -> bool:
    for mask in ALL:
        if not (truth & (1 << mask)):
            continue
        sub = mask
        while True:
            if not (truth & (1 << sub)):
                return False
            if sub == 0:
                break
            sub = (sub - 1) & mask
    return True


def truth_from_family(family: set[int] | frozenset[int]) -> int:
    return sum(1 << mask for mask in family)


def family_from_truth(truth: int) -> frozenset[int]:
    return frozenset(mask for mask in ALL if truth & (1 << mask))


def incidence_sum(left: int, right: int) -> tuple[int, ...]:
    return tuple(
        int(bool(left & (1 << i))) + int(bool(right & (1 << i)))
        for i in range(N)
    )


def two_trade_for_truth(truth: int) -> tuple[int, int, int, int]:
    feasible = family_from_truth(truth)
    infeasible = frozenset(ALL) - feasible
    feasible_by_incidence: dict[tuple[int, ...], tuple[int, int]] = {}
    for left, right in combinations_with_replacement(sorted(feasible), 2):
        feasible_by_incidence.setdefault(incidence_sum(left, right), (left, right))
    for left, right in combinations_with_replacement(sorted(infeasible), 2):
        key = incidence_sum(left, right)
        if key in feasible_by_incidence:
            a, b = feasible_by_incidence[key]
            return a, b, left, right
    raise AssertionError("missing two-trade contradiction")


def scalar_patterns() -> tuple[set[int], dict[str, int]]:
    patterns: set[int] = set()
    for vector in product(range(1, 5), repeat=N):
        for capacity in range(sum(vector) + 1):
            family = frozenset(mask for mask in ALL if weight(mask, vector) <= capacity)
            patterns.add(truth_from_family(family))

    downsets = {truth for truth in range(1 << 16) if is_downset(truth)}
    assert len(downsets) == 168
    represented = downsets & patterns
    excluded = downsets - represented
    empty_truth = 0
    nonthreshold = excluded - {empty_truth}
    assert len(represented) == 149
    assert len(nonthreshold) == 18
    assert excluded == nonthreshold | {empty_truth}
    assert all(truth & 1 for truth in represented)

    for truth in nonthreshold:
        a, b, c, d = two_trade_for_truth(truth)
        assert incidence_sum(a, b) == incidence_sum(c, d)
        family = family_from_truth(truth)
        assert a in family and b in family and c not in family and d not in family

    return represented, {
        "all_downsets": len(downsets),
        "represented": len(represented),
        "nonthreshold_with_two_trades": len(nonthreshold),
        "empty_inadmissible": 1,
    }


def blocked_edges(truth: int) -> set[frozenset[int]]:
    result: set[frozenset[int]] = set()
    for i, j in combinations(range(N), 2):
        mask = (1 << i) | (1 << j)
        if not (truth & (1 << mask)):
            result.add(frozenset((i, j)))
    return result


def triangles(edges: set[frozenset[int]]) -> list[frozenset[int]]:
    result: list[frozenset[int]] = []
    for triple in combinations(range(N), 3):
        if all(frozenset(pair) in edges for pair in combinations(triple, 2)):
            result.append(frozenset(triple))
    return result


def classify_pattern_pairs(patterns: set[int]) -> Counter[str]:
    ordered = sorted(patterns)
    counts: Counter[str] = Counter()
    no_pair_truths: set[int] = set()
    for left, right in combinations_with_replacement(ordered, 2):
        robust = left & right
        pair_available = any(
            robust & (1 << ((1 << i) | (1 << j)))
            for i, j in combinations(range(N), 2)
        )
        if pair_available:
            counts["pair"] += 1
            continue
        no_pair_truths.add(robust)
        A = {i for i in range(N) if robust & (1 << (1 << i))}
        if len(A) <= 2:
            counts[f"matching_{len(A)}"] += 1
            continue
        e1 = blocked_edges(left)
        e2 = blocked_edges(right)
        tri1 = triangles(e1)
        tri2 = triangles(e2)
        if len(A) == 4:
            assert tri1 or tri2
            counts["triangle_4"] += 1
            continue
        u = next(i for i in range(N) if i not in A)
        useful = any(
            next(i for i in range(N) if i not in tri) in A
            for tri in tri1 + tri2
        )
        if useful:
            counts["triangle_3"] += 1
            continue
        # In the exceptional case, one truth table omits singleton u and all
        # supersets containing it, while the other omits all A-pairs.
        exceptional = False
        for star, triangle in ((left, right), (right, left)):
            if star & (1 << (1 << u)):
                continue
            if not all(
                star & (1 << ((1 << i) | (1 << j)))
                for i, j in combinations(sorted(A), 2)
            ):
                continue
            if not all(
                not (triangle & (1 << ((1 << i) | (1 << j))))
                for i, j in combinations(sorted(A), 2)
            ):
                continue
            exceptional = True
        assert exceptional
        counts["star_triangle_central" if u in (1, 2) else "star_triangle_outer"] += 1

    assert sum(counts.values()) == 11175
    assert len(no_pair_truths) == 16
    return counts


def c_route_value(
    c_mask: int,
    p: tuple[Fraction, ...],
    q: tuple[Fraction, ...],
    d: tuple[Fraction, ...],
) -> Fraction:
    trunk: list[Fraction] = []
    for column in range(5):
        value = Fraction(0)
        for i in range(N):
            if not SUPPORT[i][column]:
                continue
            if c_mask & (1 << i):
                value += d[i] * q[i]
            else:
                value -= d[i] * p[i]
        trunk.append(value)
    private: list[Fraction] = []
    for i in range(N):
        private.append(d[i] * (q[i] if c_mask & (1 << i) else p[i]))
    return max(trunk + private)


def secondary_lower_instance() -> dict[str, object]:
    n = 137
    eps = Fraction(1, n)
    q = (
        Fraction(3, 4) - eps,
        Fraction(1) - eps,
        Fraction(1, 2),
        Fraction(3, 4) - eps,
    )
    p = tuple(1 - value for value in q)
    d = (Fraction(1), Fraction(1), Fraction(3, 4), Fraction(1))
    k1 = (1, 3 * n, 1, 1)
    k2 = (n, 1, n, n)
    budget1 = sum(Fraction(k1[i]) * q[i] for i in range(N))
    budget2 = sum(Fraction(k2[i]) * q[i] for i in range(N))

    feasible: dict[int, Fraction] = {}
    feasible_cost_pairs: set[tuple[Fraction, Fraction]] = set()
    for c_mask in ALL:
        e_mask = FULL ^ c_mask
        cost1 = Fraction(weight(e_mask, k1))
        cost2 = Fraction(weight(e_mask, k2))
        ok1 = cost1 <= budget1
        ok2 = cost2 <= budget2
        if ok1 and ok2:
            feasible[c_mask] = c_route_value(c_mask, p, q, d)
            feasible_cost_pairs.add((cost1, cost2))

    assert set(feasible) == {7, 11, 14, 15}
    expected = Fraction(17, 8) - Fraction(3, n)
    assert min(feasible.values()) == expected == Fraction(2305, 1096)
    assert expected > 2
    assert feasible[11] == expected
    assert feasible[7] == feasible[14] == Fraction(17, 8) - Fraction(2, n)
    assert feasible[15] == Fraction(23, 8) - Fraction(3, n)

    # Directly verify the established one-scenario representation of F126.
    canonical = (1, 2, 1, 1)
    target = frozenset(mask for mask in ALL if weight(mask, canonical) >= 4)
    assert target == frozenset(feasible)
    assert all(cost1 != budget1 and cost2 != budget2 for cost1, cost2 in feasible_cost_pairs)

    return {
        "epsilon": f"1/{n}",
        "finite_value": f"{expected.numerator}/{expected.denominator}",
        "finite_decimal": float(expected),
        "feasible_C_masks": sorted(feasible),
        "scenario_1_budget": str(budget1),
        "scenario_2_budget": str(budget2),
        "mutation_beta_le_2_falsified": True,
        "feasibility_semantics": "scenario cost <= fractional budget; equality not required",
        "feasible_unsplittable_cost_pairs": [
            [str(left), str(right)] for left, right in sorted(feasible_cost_pairs)
        ],
        "any_budget_equality": False,
    }


def envelope_grid_regression() -> dict[str, object]:
    denominator = 16
    central_max = Fraction(-10)
    outer_max = Fraction(-10)
    central_arg = None
    outer_arg = None
    for delta_num in range(denominator + 1):
        delta = Fraction(delta_num, denominator)
        central_envelope = (
            1 + 3 * delta
            if delta <= Fraction(1, 2)
            else 1 + 4 * delta - 2 * delta * delta
        )
        outer_envelope = 1 + 3 * delta - delta * delta
        for qa_num, qb_num, qc_num in product(range(denominator + 1), repeat=3):
            if qa_num + qb_num + qc_num > 2 * denominator:
                continue
            qa = Fraction(qa_num, denominator)
            qb = Fraction(qb_num, denominator)
            qc = Fraction(qc_num, denominator)
            central_H = 1 + min(qa, delta) + min(qb, delta) + delta * qc
            outer_H = 1 + min(qa, delta) + delta * (qb + qc)
            assert central_H <= central_envelope
            assert outer_H <= outer_envelope
            central_t = central_H - delta
            outer_t = outer_H - delta
            if central_t > central_max:
                central_max = central_t
                central_arg = (delta, qa, qb, qc)
            if outer_t > outer_max:
                outer_max = outer_t
                outer_arg = (delta, qa, qb, qc)
    assert central_max == Fraction(17, 8)
    assert central_arg is not None and central_arg[0] == Fraction(3, 4)
    assert outer_max == 2
    return {
        "interpretation": "finite grid regression against the analytic envelopes; not continuous optimization",
        "denominator": denominator,
        "central_grid_maximum": str(central_max),
        "central_first_argmax": [str(value) for value in central_arg],
        "outer_grid_maximum": str(outer_max),
        "outer_first_argmax": [str(value) for value in outer_arg],
    }


def main() -> None:
    directory = Path(__file__).resolve().parent
    patterns, recognition = scalar_patterns()
    counts = classify_pattern_pairs(patterns)
    lower = secondary_lower_instance()
    grid = envelope_grid_regression()
    payload = {
        "schema": "ssuf-two-scenario-global-secondary-regression-v2",
        "status": (
            "secondary exact regression code path; shares the support matrix, "
            "blocker framework, and lower ansatz; not an independent derivation"
        ),
        "threshold_recognition": recognition,
        "positive_scalar_threshold_truth_tables": len(patterns),
        "abstract_unordered_pattern_pairs": 11175,
        "abstract_pair_census_limitation": "pattern pairs need not share one baseline q",
        "case_counts": dict(sorted(counts.items())),
        "secondary_lower_instance": lower,
        "analytic_envelope_grid_regression": grid,
    }
    output = directory / "secondary_regression_report.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("PASS: scanned all 65,536 Boolean set families and found 168 downsets.")
    print("PASS: reconstructed 149 threshold downsets and certified all 18 exclusions by exact two-trades.")
    print("PASS: classified all 11,175 abstract pattern pairs as a regression check.")
    print("PASS: a second exact lower instance (epsilon=1/137) has value 2305/1096 > 2.")
    print("PASS: support-matrix enumeration gives intrinsic feasible C masks 7,11,14,15.")
    print("PASS: denominator-16 grid regression reaches 17/8 only in the supplied central envelope.")
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
