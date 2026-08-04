#!/usr/bin/env python3
"""Exact finite checks for the GM-006 lower sequence and nonattainment step."""

from __future__ import annotations

from fractions import Fraction
import itertools


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check_lower_sequence() -> int:
    checked = 0
    terminals = range(4)
    for n in range(2, 1001):
        q = Fraction(n - 1, n)
        budget = Fraction(3 * n + 3) * q
        require(budget == Fraction(3 * n) - Fraction(3, n), "budget identity")
        require(budget < 3 * n, "heavy singleton must be blocked")
        scenarios = [tuple(3 * n if j == i else 1 for j in terminals) for i in terminals]
        feasible = []
        for bits in itertools.product((0, 1), repeat=4):
            ok = all(
                sum(weight[i] * bits[i] for i in terminals) <= budget
                for weight in scenarios
            )
            if ok:
                feasible.append(bits)
        require(feasible == [(0, 0, 0, 0)], f"unexpected feasible family at n={n}")
        require(4 * q < 4, "finite objective must be below four")
        checked += 1
    return checked


def check_nonattainment_collapse() -> None:
    # H=4 under 0<d_i<=1 and 0<=q_i<=1 forces every factor to one.
    grid = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1))
    for d in itertools.product(grid, repeat=4):
        for q in itertools.product((Fraction(0), *grid), repeat=4):
            if sum(d[i] * q[i] for i in range(4)) == 4:
                require(all(d[i] == q[i] == 1 for i in range(4)), "equality collapse")


def main() -> None:
    count = check_lower_sequence()
    check_nonattainment_collapse()
    print(f"PASS: GM-006 exact lower sequence for {count} values of n")
    print("PASS: GM-006 equality collapse on exact grid")


if __name__ == "__main__":
    main()

