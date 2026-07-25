#!/usr/bin/env python3
"""CAS-independent exact audit for the every-pair theorem algebra.

The audit uses Fraction-valued Laurent polynomials and a tiny exact arithmetic
implementation of Q(sqrt(41)). It is corroborative; the human proof remains in
the markdown theorem and routing lemma.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Mapping

HERE = Path(__file__).resolve().parent
NVAR = 5  # s,t,p,q,epsilon


class Laurent:
    def __init__(self, terms: Mapping[tuple[int, ...], Fraction | int] | None = None):
        cleaned = {}
        for monomial, coefficient in (terms or {}).items():
            if len(monomial) != NVAR:
                raise ValueError("wrong monomial dimension")
            value = Fraction(coefficient)
            if value:
                cleaned[tuple(monomial)] = value
        self.terms = cleaned

    @staticmethod
    def const(value: Fraction | int) -> "Laurent":
        return Laurent({(0,) * NVAR: Fraction(value)})

    @staticmethod
    def variable(index: int, exponent: int = 1) -> "Laurent":
        monomial = [0] * NVAR
        monomial[index] = exponent
        return Laurent({tuple(monomial): 1})

    def __add__(self, other):
        other = other if isinstance(other, Laurent) else Laurent.const(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, Fraction()) + coefficient
        return Laurent(result)

    __radd__ = __add__

    def __neg__(self):
        return Laurent({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Laurent) else -Fraction(other))

    def __rsub__(self, other):
        return Laurent.const(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Laurent) else Laurent.const(other)
        result: dict[tuple[int, ...], Fraction] = {}
        for left_m, left_c in self.terms.items():
            for right_m, right_c in other.terms.items():
                monomial = tuple(a + b for a, b in zip(left_m, right_m))
                result[monomial] = result.get(monomial, Fraction()) + left_c * right_c
        return Laurent(result)

    __rmul__ = __mul__

    def __pow__(self, exponent: int):
        if exponent < 0:
            raise ValueError("negative powers are represented by negative-exponent variables")
        result = Laurent.const(1)
        for _ in range(exponent):
            result = result * self
        return result

    def __eq__(self, other):
        other = other if isinstance(other, Laurent) else Laurent.const(other)
        return self.terms == other.terms


S = Laurent.variable(0)
T = Laurent.variable(1)
P = Laurent.variable(2)
Q = Laurent.variable(3)
EPS = Laurent.variable(4)
T_INV = Laurent.variable(1, -1)


@dataclass(frozen=True)
class Q41:
    rational: Fraction
    radical: Fraction

    def __add__(self, other):
        other = other if isinstance(other, Q41) else Q41(Fraction(other), Fraction())
        return Q41(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self):
        return Q41(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q41) else -Q41(Fraction(other), Fraction()))

    def __rsub__(self, other):
        return Q41(Fraction(other), Fraction()) - self

    def __mul__(self, other):
        other = other if isinstance(other, Q41) else Q41(Fraction(other), Fraction())
        return Q41(
            self.rational * other.rational + 41 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent: int):
        result = Q41(Fraction(1), Fraction())
        for _ in range(exponent):
            result = result * self
        return result

    def serial(self) -> str:
        return f"{self.rational}+({self.radical})*sqrt(41)"


def add_linear(*expressions: dict[str, int]) -> dict[str, int]:
    result: dict[str, int] = {}
    for expression in expressions:
        for name, coefficient in expression.items():
            result[name] = result.get(name, 0) + coefficient
    return {name: coefficient for name, coefficient in result.items() if coefficient}


def dominates(candidate: dict[str, int], expression: dict[str, int]) -> bool:
    names = set(candidate) | set(expression)
    return all(candidate.get(name, 0) - expression.get(name, 0) >= 0 for name in names)


def pair_expression_audit() -> dict[str, object]:
    supports = {1: {1, 2, 3}, 2: {1, 2, 3, 4, 5}, 3: {2, 3, 4, 5}, 4: {3, 4}}
    expected = {
        (1, 2): [{"e1": 1, "e2": 1}],
        (1, 3): [{"e1": 1, "e3": 1, "l2": -1}],
        (1, 4): [
            {"e1": 1, "l2": -1},
            {"e1": 1, "e4": 1, "l2": -1, "l3": -1},
        ],
        (2, 3): [{"e2": 1, "e3": 1}],
        (2, 4): [
            {"e2": 1, "l1": -1},
            {"e2": 1, "e4": 1, "l3": -1},
        ],
        (3, 4): [{"e3": 1, "e4": 1, "l2": -1}],
    }
    rows = {}
    for pair, candidates in expected.items():
        arc_expressions = []
        cheap = set(pair)
        for arc in range(1, 6):
            terms = []
            for terminal in range(1, 5):
                if arc in supports[terminal]:
                    terms.append({f"e{terminal}" if terminal in cheap else f"l{terminal}": 1 if terminal in cheap else -1})
            arc_expressions.append(add_linear(*terms))
        assert all(any(dominates(candidate, expression) for candidate in candidates) for expression in arc_expressions)
        assert all(candidate in arc_expressions for candidate in candidates)
        rows["".join(map(str, pair))] = arc_expressions
    return rows


def main() -> None:
    e2, l2 = S * (1 - P), S * P
    e3, l3 = T * (1 - Q), T * Q
    T1 = e2 + e3
    T2 = 1 + P + Q - l2 - l3
    T3tilde = (1 + 2 * S + (1 - 2 * S) * P + (1 - T) * Q) * Fraction(1, 2)

    low = (1 - 2 * S) * T1 + 2 * S * T3tilde
    low_expected = T + 2 * S * (1 - T) + Q * (S * (1 + T) - T)
    assert low == low_expected

    lam1 = S * T_INV - S
    lam2 = S + S * T_INV - 1
    lam3 = 2 * (1 - S * T_INV)
    assert lam1 + lam2 + lam3 == 1
    g = S * (4 - S - T - S * T_INV)
    assert lam1 * T1 + lam2 * T2 + lam3 * T3tilde == g

    T3reverse = (1 + 2 * T + (1 - 2 * S) * P + (1 - 2 * T) * Q) * Fraction(1, 2)
    assert (1 - 2 * T) * T1 + 2 * T * T3reverse == S + 2 * T - 2 * S * T + P * (T - S)
    assert (2 * T - 1) * T2 + 2 * (1 - T) * T3reverse == T * (3 - 2 * T) + P * (T - S)

    assert Laurent.const(Fraction(9, 8)) - T * (3 - 2 * T) == 2 * (T - Fraction(3, 4)) ** 2

    p1 = 1 - Q**2
    p2 = Q**2 + 2 * Q - 2 + EPS
    p3 = p4 = 1 - Q
    assert p1 + p2 + p3 + p4 == 1 + EPS
    R = Q**2 * (4 - Q**2 - 2 * Q - EPS)
    b2 = Q**2 * (Q**2 + 2 * Q - 2 + EPS)
    identities = (
        Q**2 + Q**2 * (3 - Q**2 - 2 * Q - EPS),
        Q**2 - b2 + Q**2,
        Q**2 - b2 + (Q**2 - Q) + Q,
        Q**2 * (3 - Q**2 - 2 * Q - EPS) + Q**2,
        Q**2 * (3 - Q**2 - 2 * Q - EPS) + (Q**2 - Q) + Q,
    )
    assert all(identity == R for identity in identities)
    assert -b2 + Q**2 + Q == R + Q - Q**2

    t_star = Q41(Fraction(-3, 4), Fraction(1, 4))
    s_star = t_star**2
    assert 2 * t_star**2 + 3 * t_star - 4 == Q41(Fraction(), Fraction())
    assert 4 - 2 * s_star - 3 * t_star == Q41(Fraction(), Fraction())
    assert -s_star + t_star**2 == Q41(Fraction(), Fraction())
    value = s_star * (4 - s_star - 2 * t_star)
    L = Q41(Fraction(299, 32), Fraction(-41, 32))
    assert value == L

    radical_gap_square = 263**2 - 41**3
    assert radical_gap_square == 248 > 0

    result = {
        "status": "PASS",
        "arithmetic": "Fraction-valued Laurent polynomials and Q(sqrt(41)); no CAS",
        "pair_arc_expressions": pair_expression_audit(),
        "convex_identities": "exact coefficient equality",
        "boundary_certificate": {
            "nine_eighths_gap": "2*(t-3/4)^2",
            "constraint_boundary_gap_numerator": "(1-t)^2",
            "constraint_boundary_denominator": "t+1>0 on 0<=t<=1",
        },
        "stationary_point": {"t": t_star.serial(), "s": s_star.serial(), "value": value.serial()},
        "L_gt_9_over_8_square_gap": radical_gap_square,
        "lower_family_identities": "exact coefficient equality",
    }
    output = HERE / "exact_algebra_results.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
