#!/usr/bin/env python3
"""Exact rational interior lower-bound witnesses for selected open SSUF cells.

These witnesses do not solve a cell.  They prove that several remaining cells
have value strictly greater than one, so a universal singleton-style <=1 bound
cannot eliminate the entire 94-cell remainder.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCS = ("a1", "a2", "a3", "a4", "a5")
SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)

# k, p, d.  All coordinates are exact rationals and max(d)=1.
WITNESSES = {
    "F126": {
        "k": (Q(1, 5), Q(2, 5), Q(1, 5), Q(1, 5)),
        "p": (Q(17, 100), Q(99, 100), Q(19, 25), Q(3, 25)),
        "d": (Q(99, 100), Q(93, 100), Q(83, 100), Q(1)),
    },
    "F125": {
        "k": (Q(1, 4), Q(1, 4), Q(1, 4), Q(1, 4)),
        "p": (Q(1, 4), Q(11, 20), Q(1, 4), Q(1)),
        "d": (Q(1), Q(3, 5), Q(1), Q(17, 20)),
    },
    "F042": {
        "k": (Q(3, 10), Q(3, 10), Q(3, 10), Q(3, 20)),
        "p": (Q(3, 10), Q(9, 20), Q(3, 10), Q(19, 20)),
        "d": (Q(1), Q(13, 20), Q(1), Q(13, 20)),
    },
    "F129": {
        "k": (Q(1, 5), Q(1, 5), Q(2, 5), Q(1, 5)),
        "p": (Q(7, 25), Q(17, 25), Q(1), Q(3, 50)),
        "d": (Q(1), Q(47, 50), Q(31, 50), Q(1)),
    },
    "F143": {
        "k": (Q(1, 5), Q(1, 5), Q(1, 5), Q(2, 5)),
        "p": (Q(171, 500), Q(237, 500), Q(63, 250), Q(121, 125)),
        "d": (Q(123, 125), Q(87, 100), Q(1), Q(359, 500)),
    },
}


def family_from_bitmask(value: str) -> frozenset[int]:
    bitmask = int(value, 16)
    return frozenset(mask for mask in range(16) if bitmask & (1 << mask))


def subset_weight(mask: int, weights: tuple[Q, ...]) -> Q:
    return sum((weights[i] for i in range(4) if mask & (1 << i)), Q(0))


def route_deviations(mask: int, d: tuple[Q, ...], p: tuple[Q, ...]) -> dict[str, Q]:
    e = tuple(d[i] * (1 - p[i]) for i in range(4))
    ell = tuple(d[i] * p[i] for i in range(4))
    result: dict[str, Q] = {}
    for arc_index, arc in enumerate(ARCS):
        result[arc] = sum(
            (
                e[i] if mask & (1 << i) else -ell[i]
                for i in range(4)
                if arc_index in SUPPORTS[i]
            ),
            Q(0),
        )
    for i in range(4):
        result[f"private_t{i + 1}"] = e[i] if mask & (1 << i) else ell[i]
    return result


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def mask_text(mask: int) -> str:
    return "∅" if mask == 0 else "".join(str(i + 1) for i in range(4) if mask & (1 << i))


def main() -> None:
    census = json.loads((HERE / "threshold_family_census.json").read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in census["realizable_families"]}
    output = []
    for family_id, raw in WITNESSES.items():
        row = rows[family_id]
        expected = family_from_bitmask(row["family_bitmask_hex"])
        k = raw["k"]
        p = raw["p"]
        d = raw["d"]
        assert all(value > 0 for value in k)
        assert all(Q(0) <= value <= Q(1) for value in p)
        assert all(Q(0) < value <= Q(1) for value in d) and max(d) == 1
        tau = sum((k[i] * p[i] for i in range(4)), Q(0))
        actual = frozenset(mask for mask in range(16) if subset_weight(mask, k) >= tau)
        assert actual == expected
        losing_max = max(subset_weight(mask, k) for mask in range(16) if mask not in actual)
        winning_min = min(subset_weight(mask, k) for mask in actual)
        assert losing_max < tau <= winning_min

        routes = []
        for mask in sorted(actual):
            deviations = route_deviations(mask, d, p)
            maximum = max(deviations.values())
            witness_arcs = sorted(name for name, value in deviations.items() if value == maximum)
            routes.append(
                {
                    "cheap_set": mask_text(mask),
                    "maximum_upper_deviation": qtext(maximum),
                    "witness_arcs": witness_arcs,
                }
            )
        optimum = min(Q(item["maximum_upper_deviation"]) for item in routes)
        assert optimum > 1
        output.append(
            {
                "family_id": family_id,
                "minimal_feasible_sets": row["minimal_feasible_sets"],
                "k": [qtext(value) for value in k],
                "p": [qtext(value) for value in p],
                "d": [qtext(value) for value in d],
                "tau": qtext(tau),
                "strict_losing_margin": qtext(tau - losing_max),
                "winning_slack": qtext(winning_min - tau),
                "exact_minimum_maximum_deviation": qtext(optimum),
                "routes": routes,
            }
        )
        print(f"PASS: {family_id} has exact interior lower witness {qtext(optimum)} > 1")

    target = HERE / "exact_open_cell_witnesses.json"
    target.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {target}")


if __name__ == "__main__":
    main()
