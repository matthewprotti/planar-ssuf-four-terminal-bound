#!/usr/bin/env python3
"""Exact structural corroboration for the thirteen-arc envelope lemma.

The analytic proof is TRUNK_PRIVATE_ARC_ENVELOPE.md. This checker rebuilds the
two paths for each terminal, verifies every signed incidence coefficient for
all sixteen E-set routings, and tests the resulting envelope on a rational
grid. It is not a proof assistant.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import product


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
SUPPORTS = tuple((C_PATHS[i] - E_PATHS[i]) & frozenset(TRUNK) for i in range(N))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def fractional_loads(d: tuple[Q, ...], q: tuple[Q, ...]) -> dict[str, Q]:
    loads = {arc: Q(0) for arc in ARCS}
    for i in range(N):
        for arc in E_PATHS[i]:
            loads[arc] += d[i] * q[i]
        for arc in C_PATHS[i]:
            loads[arc] += d[i] * (1 - q[i])
    return loads


def route_loads(mask: int, d: tuple[Q, ...]) -> dict[str, Q]:
    loads = {arc: Q(0) for arc in ARCS}
    for i in range(N):
        path = E_PATHS[i] if mask & (1 << i) else C_PATHS[i]
        for arc in path:
            loads[arc] += d[i]
    return loads


def direct_deviations(mask: int, d: tuple[Q, ...], q: tuple[Q, ...]) -> dict[str, Q]:
    fractional = fractional_loads(d, q)
    routed = route_loads(mask, d)
    return {arc: routed[arc] - fractional[arc] for arc in ARCS}


def formula_deviation(
    arc: str, mask: int, d: tuple[Q, ...], q: tuple[Q, ...]
) -> Q:
    total = Q(0)
    for i in range(N):
        on_e = bool(mask & (1 << i))
        path = E_PATHS[i] if on_e else C_PATHS[i]
        fractional_coefficient = q[i] * (arc in E_PATHS[i]) + (1 - q[i]) * (
            arc in C_PATHS[i]
        )
        total += d[i] * (Q(arc in path) - fractional_coefficient)
    return total


def main() -> None:
    require(all("a3" in support for support in SUPPORTS), "a3 is not common")
    structural_rows = 0
    for mask in range(1 << N):
        for arc in ARCS:
            for terminal in range(N):
                on_e = bool(mask & (1 << terminal))
                c_minus_e = int(arc in C_PATHS[terminal]) - int(
                    arc in E_PATHS[terminal]
                )
                if arc in TRUNK:
                    require(
                        c_minus_e == int(arc in SUPPORTS[terminal]),
                        "trunk support coefficient mismatch",
                    )
                    expected_orientation = -c_minus_e if on_e else c_minus_e
                    require(
                        expected_orientation in (-1, 0, 1),
                        "invalid signed trunk orientation",
                    )
                else:
                    users = sum(
                        int(arc in E_PATHS[i] or arc in C_PATHS[i]) for i in range(N)
                    )
                    require(users == 1, "private arc is not terminal-private")
                structural_rows += 1

    q_values = (Q(0), Q(1, 2), Q(1))
    d_values = (Q(1, 2), Q(1))
    grid_instances = 0
    route_rows = 0
    for q in product(q_values, repeat=N):
        for d in product(d_values, repeat=N):
            if max(d) != 1:
                continue
            grid_instances += 1
            h = tuple(d[i] * q[i] for i in range(N))
            for mask in range(1 << N):
                direct = direct_deviations(mask, d, q)
                for arc in ARCS:
                    require(
                        direct[arc] == formula_deviation(arc, mask, d, q),
                        f"path/formula mismatch at mask={mask}, arc={arc}",
                    )
                c_mass = sum((h[i] for i in range(N) if not mask & (1 << i)), Q(0))
                maximum = max((Q(0), *direct.values()))
                require(maximum <= max(Q(1), c_mass), "thirteen-arc envelope failed")
                if mask == 0:
                    require(maximum == sum(h, Q(0)), "all-C exact identity failed")
                route_rows += 1

    print("PASS: rebuilt all 13 path-incidence rows and 16 routings")
    print(f"PASS: checked {structural_rows} signed structural coefficients")
    print(
        f"PASS: checked the exact envelope on {grid_instances} normalized grid instances "
        f"and {route_rows} routing rows"
    )
    print("PASS: all-C value is exactly H on every tested instance")
    print("EVIDENCE BOUNDARY: exact corroboration; analytic lemma remains authoritative")


if __name__ == "__main__":
    main()
