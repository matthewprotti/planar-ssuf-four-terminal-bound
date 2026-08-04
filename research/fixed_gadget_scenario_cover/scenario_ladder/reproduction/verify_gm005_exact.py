#!/usr/bin/env python3
"""Standard-library exact corroboration for the repaired GM-005 proof.

This script is deliberately not a proof assistant. It reconstructs the graph,
checks the exact route identities, exercises the equality-collapse mechanism,
and replays the rational lower sequence using fractions.Fraction.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
from typing import Iterable, Sequence

N = 4
TRUNK = ("a1", "a2", "a3", "a4", "a5")
PRIVATE = ("e1", "c1", "e2", "c2", "e3", "c3", "e4", "c4")
ARCS = TRUNK + PRIVATE

E_PATHS = (
    frozenset({"e1"}),
    frozenset({"e2"}),
    frozenset({"a1", "e3"}),
    frozenset({"a1", "a2", "e4"}),
)
C_PATHS = (
    frozenset({"a1", "a2", "a3", "c1"}),
    frozenset({"a1", "a2", "a3", "a4", "a5", "c2"}),
    frozenset({"a1", "a2", "a3", "a4", "a5", "c3"}),
    frozenset({"a1", "a2", "a3", "a4", "c4"}),
)
EXPECTED_SUPPORTS = (
    frozenset({"a1", "a2", "a3"}),
    frozenset({"a1", "a2", "a3", "a4", "a5"}),
    frozenset({"a2", "a3", "a4", "a5"}),
    frozenset({"a3", "a4"}),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def frac(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def validate_positive_scenario(weights: Sequence[Q]) -> None:
    require(len(weights) == N, "scenario must have four coordinates")
    require(all(weight > 0 for weight in weights), "scenario coordinates must be strictly positive")


def scenario_budget(weights: Sequence[Q], q: Sequence[Q]) -> Q:
    validate_positive_scenario(weights)
    return sum((weights[i] * q[i] for i in range(N)), Q(0))


def route_weight(mask: int, weights: Sequence[Q]) -> Q:
    return sum((weights[i] for i in range(N) if mask & (1 << i)), Q(0))


def is_feasible(mask: int, q: Sequence[Q], scenarios: Sequence[Sequence[Q]]) -> bool:
    return all(route_weight(mask, weights) <= scenario_budget(weights, q) for weights in scenarios)


def fractional_loads(d: Sequence[Q], q: Sequence[Q]) -> dict[str, Q]:
    loads = {arc: Q(0) for arc in ARCS}
    for i in range(N):
        for arc in E_PATHS[i]:
            loads[arc] += d[i] * q[i]
        for arc in C_PATHS[i]:
            loads[arc] += d[i] * (1 - q[i])
    return loads


def route_loads(mask: int, d: Sequence[Q]) -> dict[str, Q]:
    loads = {arc: Q(0) for arc in ARCS}
    for i in range(N):
        path = E_PATHS[i] if mask & (1 << i) else C_PATHS[i]
        for arc in path:
            loads[arc] += d[i]
    return loads


def deviations(mask: int, d: Sequence[Q], q: Sequence[Q]) -> dict[str, Q]:
    fractional = fractional_loads(d, q)
    routed = route_loads(mask, d)
    return {arc: routed[arc] - fractional[arc] for arc in ARCS}


def route_value(mask: int, d: Sequence[Q], q: Sequence[Q]) -> Q:
    values = deviations(mask, d, q).values()
    return max((Q(0), *values))


def trunk_max(mask: int, d: Sequence[Q], q: Sequence[Q]) -> Q:
    dev = deviations(mask, d, q)
    return max(dev[arc] for arc in TRUNK)


def instance_value(d: Sequence[Q], q: Sequence[Q], scenarios: Sequence[Sequence[Q]]) -> tuple[Q, tuple[int, ...]]:
    feasible = tuple(mask for mask in range(1 << N) if is_feasible(mask, q, scenarios))
    require(feasible, "empty feasible family")
    value = min(route_value(mask, d, q) for mask in feasible)
    return value, feasible


def support_check() -> dict[str, object]:
    observed = tuple(frozenset((C_PATHS[i] - E_PATHS[i]) & set(TRUNK)) for i in range(N))
    require(observed == EXPECTED_SUPPORTS, f"support mismatch: {observed}")
    require(all("a3" in support for support in observed), "a3 must contain all four difference supports")
    return {"supports": [sorted(support) for support in observed], "common_arc": "a3"}


def route_identity_check() -> dict[str, object]:
    q_values = (Q(0), Q(1, 2), Q(1))
    d_values = (Q(1, 2), Q(1))
    rows = 0
    for q in product(q_values, repeat=N):
        for d in product(d_values, repeat=N):
            if max(d) != 1:
                continue
            h = tuple(d[i] * q[i] for i in range(N))
            H = sum(h, Q(0))
            require(route_value(0, d, q) == H, f"all-C identity failed: d={d}, q={q}")
            expected = (
                H - h[0],
                H - d[1],
                max(h[0] + h[1], H - d[2]),
                H - h[3],
            )
            for r in range(N):
                observed = trunk_max(1 << r, d, q)
                require(observed == expected[r], f"singleton row {r+1} failed: {observed} != {expected[r]}")
                rows += 1
    return {"grid_instances": 3**4 * (2**4 - 1), "singleton_rows_checked": rows}


def assignment_cover_check() -> dict[str, object]:
    q_values = tuple(Q(i, 4) for i in range(5))
    weight_vectors = tuple(tuple(Q(x) for x in weights) for weights in product((1, 2, 3, 4), repeat=N))
    q_points = 0
    coverable = 0
    for q in product(q_values, repeat=N):
        if all(value == 0 for value in q):
            continue
        q_points += 1
        losing_masks = set()
        for weights in weight_vectors:
            budget = scenario_budget(weights, q)
            mask = 0
            for i in range(N):
                if weights[i] > budget:
                    mask |= 1 << i
            losing_masks.add(mask)
        pair_unions = {left | right for left in losing_masks for right in losing_masks}
        can_cover = any((pair_mask | third) == 0b1111 for pair_mask in pair_unions for third in losing_masks)
        if can_cover:
            coverable += 1
            require(sum(q, Q(0)) < 3, f"three scenarios covered all singletons with sum(q)>=3: {q}")
    return {
        "q_grid_points": q_points,
        "weight_vectors_per_point": len(weight_vectors),
        "three_coverable_points": coverable,
        "result": "every covered point has sum(q)<3",
    }


def equality_collapse_check() -> dict[str, object]:
    q_r_values = (Q(0), Q(1, 3), Q(2, 3), Q(1))
    d_r_values = (Q(1, 4), Q(1, 2), Q(1))
    weights_list = tuple(tuple(Q(x) for x in weights) for weights in product((1, 2, 5), repeat=N))
    scenario_checks = 0
    equality_implications = 0
    for r in range(N):
        triple = 0b1111 ^ (1 << r)
        for q_r in q_r_values:
            for d_r in d_r_values:
                q = [Q(1)] * N
                d = [Q(1)] * N
                q[r] = q_r
                d[r] = d_r
                q_t = tuple(q)
                d_t = tuple(d)
                require(route_value(triple, d_t, q_t) <= 1, f"complementary triple exceeds one: r={r+1}")
                for weights in weights_list:
                    scenario_checks += 1
                    require(route_weight(triple, weights) <= scenario_budget(weights, q_t),
                            f"complementary triple infeasible: r={r+1}, q_r={q_r}, weights={weights}")
                    singleton = 1 << r
                    if route_weight(singleton, weights) <= scenario_budget(weights, q_t) and route_value(singleton, d_t, q_t) == 3:
                        equality_implications += 1
                        require(route_value(triple, d_t, q_t) < 3, "equality collapse failed")
    require(equality_implications > 0, "no concrete equality cases exercised")
    return {
        "individual_scenario_checks": scenario_checks,
        "singleton_equality_cases_exercised": equality_implications,
        "result": "complementary triple always feasible and has value at most one",
    }


def lower_sequence_check(limit: int = 1000) -> dict[str, object]:
    anchors: dict[str, object] = {}
    for n in range(2, limit + 1):
        q = tuple(Q(n - 1, n) for _ in range(N))
        d = (Q(1),) * N
        scenarios = []
        for heavy in range(3):
            weights = [Q(1)] * N
            weights[heavy] = Q(3 * n)
            scenarios.append(tuple(weights))
        value, feasible = instance_value(d, q, tuple(scenarios))
        require(feasible == (0, 8), f"lower sequence feasible family failed at n={n}: {feasible}")
        expected = Q(3 * (n - 1), n)
        require(route_value(8, d, q) == expected, f"route 4 value failed at n={n}")
        require(value == expected, f"instance value failed at n={n}")
        require(value < 3, f"finite lower sequence attained 3 at n={n}")
        if n in (2, 4, 10, 100, limit):
            anchors[str(n)] = {"value": frac(value), "feasible_masks": list(feasible)}
    require(Q(9, 4) > Q(17, 8), "n=4 comparison failed")
    return {"n_range": [2, limit], "anchors": anchors, "n4_gt_17_8": True}


def old_gap_regression() -> dict[str, object]:
    d = (Q(1),) * N
    q = (Q(1), Q(1), Q(1), Q(0))
    ones = (Q(1),) * N
    scenarios = (ones, ones, ones)
    singleton_4 = 8
    triple_123 = 7
    require(is_feasible(singleton_4, q, scenarios), "singleton 4 should be feasible")
    require(route_value(singleton_4, d, q) == 3, "singleton 4 should have value 3")
    require(is_feasible(triple_123, q, scenarios), "complementary triple should be feasible by a tie")
    require(route_value(triple_123, d, q) == 0, "complementary triple should match the fractional flow")
    value, feasible = instance_value(d, q, scenarios)
    require(value == 0, "old-gap regression instance should have value zero")
    return {
        "q": [frac(x) for x in q],
        "singleton_4_value": "3",
        "complementary_triple_value": "0",
        "instance_value": frac(value),
        "feasible_masks": list(feasible),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()

    report = {
        "schema": "ssuf-gm005-exact-corroboration-v1",
        "arithmetic": "fractions.Fraction only",
        "support_check": support_check(),
        "route_identity_check": route_identity_check(),
        "assignment_cover_check": assignment_cover_check(),
        "equality_collapse_check": equality_collapse_check(),
        "old_gap_regression": old_gap_regression(),
        "lower_sequence_check": lower_sequence_check(),
        "evidence_boundary": "exact corroboration; not a proof assistant or substitute for proof review",
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding='utf-8', newline='\n')
    print("PASS: reconstructed the fixed graph and four C-minus-E supports")
    print("PASS: checked all-C and singleton route identities on an exact grid")
    print("PASS: checked the three-scenario singleton-cover consequence on a denominator-4 grid")
    print("PASS: checked the uniform equality-collapse mechanism for all four labels")
    print("PASS: preserved weak-feasibility ties in the old-gap regression")
    print("PASS: replayed the exact lower sequence for 2 <= n <= 1000")
    if args.output:
        print(f"WROTE: {args.output}")
    print("ALL GM-005 EXACT CORROBORATION CHECKS PASSED")


if __name__ == '__main__':
    main()
