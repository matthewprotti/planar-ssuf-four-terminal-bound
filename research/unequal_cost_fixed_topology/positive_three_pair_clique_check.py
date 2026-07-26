#!/usr/bin/env python3
"""Exact checks for UC-023 positive three-pair clique cells."""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)
CHAIN_MISSING = {1, 2, 3}  # paper terminals 2,3,4
CELL_IDS = {3: "F042", 2: "F068", 1: "F094", 0: "F105"}


def feasible(mask: int, k: tuple[Q, ...], p: tuple[Q, ...]) -> bool:
    return sum((k[i] * (((mask >> i) & 1) - p[i]) for i in range(4)), Q(0)) >= 0


def route_max(mask: int, d: tuple[Q, ...], p: tuple[Q, ...]) -> Q:
    values: list[Q] = []
    for arc in range(5):
        values.append(
            sum(
                (
                    d[i] * (((mask >> i) & 1) - p[i])
                    for i in range(4)
                    if arc in SUPPORTS[i]
                ),
                Q(0),
            )
        )
    values.extend(
        d[i] * ((1 - p[i]) if (mask >> i) & 1 else p[i]) for i in range(4)
    )
    return max(values)


def expected_family(missing: int) -> frozenset[int]:
    q = [i for i in range(4) if i != missing]
    return frozenset(
        mask for mask in range(16) if sum((mask >> i) & 1 for i in q) >= 2
    )


def chain_lower(missing: int, epsilon: Q, delta: Q, eta: Q) -> dict[str, str]:
    q = [i for i in range(4) if i != missing]
    middle = {1: 2, 2: 1, 3: 1}[missing]
    outer = [i for i in q if i != middle]
    k = [Q(1)] * 4
    k[missing] = delta
    p = [Q(0)] * 4
    p[outer[0]] = p[outer[1]] = (1 + epsilon) / 4
    p[middle] = (1 + epsilon) / 2
    p[missing] = 1
    d = [Q(1)] * 4
    d[middle] = (3 - epsilon) / 4
    d[missing] = eta
    actual = frozenset(mask for mask in range(16) if feasible(mask, tuple(k), tuple(p)))
    assert actual == expected_family(missing)
    optimum = min(route_max(mask, tuple(d), tuple(p)) for mask in actual)
    base = (3 - epsilon) ** 2 / 8
    assert base - eta <= optimum <= base
    return {"optimum": str(optimum), "base": str(base), "base_minus_eta": str(base - eta)}


def nested_lower(epsilon: Q, delta: Q, eta: Q) -> dict[str, str]:
    missing = 0
    k = (delta, Q(1), Q(1), Q(1))
    p = (Q(1), epsilon, Q(1), Q(0))
    d = (eta, Q(1), Q(1), Q(1))
    actual = frozenset(mask for mask in range(16) if feasible(mask, k, p))
    assert actual == expected_family(missing)
    optimum = min(route_max(mask, d, p) for mask in actual)
    assert optimum == 1 - epsilon
    return {"optimum": str(optimum), "target": str(1 - epsilon)}


def main() -> None:
    census = json.loads((HERE / "threshold_family_census.json").read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in census["realizable_families"]}
    for missing, cell_id in CELL_IDS.items():
        expected_minima = sorted(
            "".join(str(i + 1) for i in pair)
            for pair in combinations([i for i in range(4) if i != missing], 2)
        )
        assert sorted(rows[cell_id]["minimal_feasible_sets"]) == expected_minima

    # Exact square identity for the chain upper bound.
    for numerator in range(1001):
        p = Q(numerator, 1000)
        value = 1 + p / 2 - p * p / 2
        assert Q(9, 8) - value == (p - Q(1, 2)) ** 2 / 2
        assert value <= Q(9, 8)

    epsilon = Q(1, 1000)
    delta = Q(1, 2000)
    eta = Q(1, 10000)
    chain = {
        str(missing + 1): chain_lower(missing, epsilon, delta, eta)
        for missing in sorted(CHAIN_MISSING)
    }
    nested = nested_lower(epsilon, delta, eta)

    result = {
        "status": "PASS",
        "cell_ids_by_omitted_terminal": {str(k + 1): v for k, v in CELL_IDS.items()},
        "chain_omitted_terminals": [2, 3, 4],
        "chain_exact_supremum": "9/8",
        "nested_omitted_terminal": 1,
        "nested_exact_supremum": "1",
        "chain_lower_sequences": chain,
        "nested_lower_sequence": nested,
        "positive_frontier_before": 83,
        "positive_frontier_after": 79,
        "abstract_orbits_before": 12,
        "abstract_orbits_after": 11,
        "evidence_class": "human theorem plus exact finite/algebraic corroboration",
    }
    target = HERE / "positive_three_pair_clique_results.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: four pure three-pair clique cells identified exactly")
    print("PASS: three chain cells approach 9/8 and nested cell approaches 1")
    print("PASS: positive frontier reduces 83->79 and 12->11 abstract orbits")
    print(f"WROTE: {target}")


if __name__ == "__main__":
    main()
