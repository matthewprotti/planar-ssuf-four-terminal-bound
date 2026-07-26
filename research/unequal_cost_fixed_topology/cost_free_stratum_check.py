#!/usr/bin/env python3
"""Exact checks for the identically-zero cost-difference theorem UC-019."""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
from pathlib import Path

SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)
BOUND = Q(4, 5)


def route_deviations(mask: int, d: tuple[Q, ...], p: tuple[Q, ...]) -> tuple[Q, ...]:
    ell = tuple(d[i] * p[i] for i in range(4))
    e = tuple(d[i] * (1 - p[i]) for i in range(4))
    values: list[Q] = []
    for arc in range(5):
        values.append(
            sum(
                (
                    e[i] if mask & (1 << i) else -ell[i]
                    for i in range(4)
                    if arc in SUPPORTS[i]
                ),
                Q(0),
            )
        )
    # Each route choice has one terminal-private positive deviation: e_i for C,
    # ell_i for E. Negative private deviations are irrelevant to the upper-only
    # maximum and need not be included separately.
    values.extend(e[i] if mask & (1 << i) else ell[i] for i in range(4))
    return tuple(values)


def route_max(mask: int, d: tuple[Q, ...], p: tuple[Q, ...]) -> Q:
    return max(route_deviations(mask, d, p))


def constructive_mask(d: tuple[Q, ...], p: tuple[Q, ...]) -> int:
    ell = tuple(d[i] * p[i] for i in range(4))
    return sum(1 << i for i in range(4) if ell[i] > BOUND)


def main() -> None:
    # Exact matching lower instance.
    d = (Q(1),) * 4
    p = (BOUND,) * 4
    route_values = [route_max(mask, d, p) for mask in range(16)]
    assert min(route_values) == BOUND
    assert route_values[15] == BOUND
    assert all(value >= BOUND for value in route_values)

    # Exact rational-grid regression for the constructive upper rule. This does
    # not replace the proof, but it attacks threshold/equality edge cases.
    p_grid = tuple(Q(i, 5) for i in range(6))
    d_grid = tuple(Q(i, 5) for i in range(1, 6))
    checked = 0
    equality_cases = 0
    for d_values in itertools.product(d_grid, repeat=4):
        if max(d_values) != 1:
            continue
        for p_values in itertools.product(p_grid, repeat=4):
            mask = constructive_mask(d_values, p_values)
            maximum = route_max(mask, d_values, p_values)
            assert maximum <= BOUND
            checked += 1
            equality_cases += int(maximum == BOUND)

    result = {
        "status": "PASS",
        "exact_value": "4/5",
        "lower_instance_route_values": [str(value) for value in route_values],
        "constructive_rule": "choose C iff d_i*p_i > 4/5; choose E otherwise",
        "exact_grid_cases": checked,
        "exact_grid_equality_cases": equality_cases,
        "p_grid": [str(value) for value in p_grid],
        "d_grid": [str(value) for value in d_grid],
        "evidence_class": "human theorem plus exact finite rational-grid corroboration",
    }
    target = Path(__file__).with_name("cost_free_stratum_results.json")
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: all 16 lower-instance routes have maximum deviation at least 4/5")
    print("PASS: the all-C route attains 4/5 on the symmetric lower instance")
    print(f"PASS: constructive upper routing is <=4/5 on {checked} exact grid cases")
    print(f"WROTE: {target}")


if __name__ == "__main__":
    main()
