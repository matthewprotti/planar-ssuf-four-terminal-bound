#!/usr/bin/env python3
"""Structurally separate finite-grid check for UC-018.

This is a finite consistency test, not the proof. It evaluates all 79 nonzero,
non-all-positive sign/zero patterns on a declared exact rational grid.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)


def feasible(mask, k, p):
    return sum((k[i] * ((1 if mask & (1 << i) else 0) - p[i]) for i in range(4)), Q(0)) >= 0


def route_max(mask, d, p):
    values = []
    for arc in range(5):
        values.append(
            sum(
                (
                    d[i] * ((1 if mask & (1 << i) else 0) - p[i])
                    for i in range(4)
                    if arc in SUPPORTS[i]
                ),
                Q(0),
            )
        )
    for i in range(4):
        values.append(d[i] * ((1 - p[i]) if mask & (1 << i) else p[i]))
    return max(values)


def main() -> None:
    fractions = (Q(0), Q(1, 2), Q(1))
    demand_vectors = [(Q(1),) * 4] + [
        tuple(Q(1, 2) if i == j else Q(1) for i in range(4)) for j in range(4)
    ]
    patterns = 0
    chain_patterns = 0
    value_one_patterns = 0
    cases = 0
    worst_chain = Q(0)
    worst_other = Q(0)
    for signs in product((-1, 0, 1), repeat=4):
        if signs in {(0, 0, 0, 0), (1, 1, 1, 1)}:
            continue
        patterns += 1
        positive = [i for i, sign in enumerate(signs) if sign > 0]
        nonpositive = [i for i, sign in enumerate(signs) if sign <= 0]
        chain = len(positive) == 3 and nonpositive[0] in {1, 2, 3}
        if chain:
            chain_patterns += 1
        else:
            value_one_patterns += 1
        k = tuple(Q(sign) for sign in signs)
        for p in product(fractions, repeat=4):
            feasible_routes = [mask for mask in range(16) if feasible(mask, k, p)]
            assert feasible_routes
            for d in demand_vectors:
                optimum = min(route_max(mask, d, p) for mask in feasible_routes)
                bound = Q(9, 8) if chain else Q(1)
                assert optimum <= bound, (signs, p, d, optimum, bound)
                if chain:
                    worst_chain = max(worst_chain, optimum)
                else:
                    worst_other = max(worst_other, optimum)
                cases += 1
    assert patterns == 79
    assert chain_patterns == 6
    assert value_one_patterns == 73
    result = {
        "status": "PASS",
        "sign_zero_patterns": patterns,
        "chain_value_9_over_8_patterns": chain_patterns,
        "value_one_patterns": value_one_patterns,
        "exact_grid_cases": cases,
        "fraction_grid": ["0", "1/2", "1"],
        "demand_grid": "all ones plus each one-coordinate half-demand vector",
        "largest_grid_optimum_chain": str(worst_chain),
        "largest_grid_optimum_other": str(worst_other),
        "evidence_class": "finite exact rational consistency check; human theorem is authoritative",
    }
    target = Path(__file__).with_name("nonpositive_difference_grid_results.json")
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: all 79 non-all-positive nonzero sign/zero patterns classified")
    print("PASS: 31,995 exact rational grid cases respect the claimed 1 or 9/8 bound")
    print(f"WROTE: {target}")


if __name__ == "__main__":
    main()
