#!/usr/bin/env python3
"""Exact symbolic reconstruction and algebra checks for SC-006."""

from __future__ import annotations

import sympy as sp


e = sp.symbols("epsilon", real=True)
kappa = sp.symbols("kappa", real=True)
k1, k2, k3, k4 = sp.symbols("k1 k2 k3 k4", positive=True)
ks = (k1, k2, k3, k4)

ZERO = sp.Integer(0)
ONE = sp.Integer(1)
EIGHTH = sp.Rational(1, 8)

a = sp.Rational(1, 4) + e
p = (a, e, sp.Rational(1, 2), a)
d = (ONE, ONE, sp.Rational(3, 4), ONE)
supports = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)


def require(condition: object, message: str) -> None:
    if condition is True or condition is sp.true:
        return
    try:
        if bool(condition):
            return
    except TypeError:
        pass
    raise AssertionError(message)


def is_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def affine_endpoints(expr: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    expr = sp.cancel(sp.together(expr))
    numerator, denominator = sp.fraction(expr)
    require(not denominator.has(e), f"epsilon-dependent denominator: {expr}")
    poly = sp.Poly(sp.expand(numerator), e)
    require(poly.degree() <= 1, f"non-affine expression: {expr}")
    left = sp.simplify(expr.subs(e, 0))
    right = sp.simplify(expr.subs(e, EIGHTH))
    return left, right


def nonnegative_closed(expr: sp.Expr, label: str) -> None:
    left, right = affine_endpoints(expr)
    require(left >= 0 and right >= 0,
            f"{label}: negative endpoint for {sp.factor(expr)}: {left}, {right}")


def positive_open(expr: sp.Expr, label: str) -> None:
    expr = sp.factor(expr)
    nonnegative_closed(expr, label)
    require(not is_zero(expr), f"{label}: identically zero")


def route_deviations(mask: int) -> tuple[sp.Expr, ...]:
    trunk: list[sp.Expr] = []
    for arc in range(5):
        value = ZERO
        for i in range(4):
            if arc in supports[i]:
                choice = ONE if mask & (1 << i) else ZERO
                value += d[i] * (choice - p[i])
        trunk.append(sp.expand(value))

    private: list[sp.Expr] = []
    for i in range(4):
        q_i = ONE - p[i]
        if mask & (1 << i):
            private.extend((-d[i] * q_i, d[i] * q_i))
        else:
            private.extend((d[i] * p[i], -d[i] * p[i]))
    return tuple(sp.expand(value) for value in trunk + private)


# Masks use bit i for terminal i+1.
M = {
    0: sp.Rational(3, 8),
    1: sp.Rational(3, 4) - e,
    2: ONE - e,
    3: sp.Rational(7, 4) - 2 * e,
    4: sp.Rational(3, 8),
    5: sp.Rational(9, 8) - 2 * e,
    6: sp.Rational(11, 8) - e,
    7: sp.Rational(17, 8) - 2 * e,
    8: sp.Rational(3, 4) - e,
    9: sp.Rational(9, 8) - 3 * e,
    10: sp.Rational(11, 8) - 2 * e,
    11: sp.Rational(17, 8) - 3 * e,
    12: sp.Rational(9, 8) - 2 * e,
    13: sp.Rational(15, 8) - 3 * e,
    14: sp.Rational(17, 8) - 2 * e,
    15: sp.Rational(23, 8) - 3 * e,
}

# Reconstruct every maximum from all 13 arc deviations.
for mask in range(16):
    deviations = route_deviations(mask)
    require(len(deviations) == 13, f"route {mask}: wrong arc count")
    require(any(is_zero(M[mask] - value) for value in deviations),
            f"route {mask}: proposed maximum is not attained")
    for index, value in enumerate(deviations):
        nonnegative_closed(M[mask] - value,
                           f"route {mask}, arc deviation {index}")

r0 = sp.Rational(9, 8) - 3 * e
r1 = sp.Rational(9, 8) - 2 * e
r2 = sp.Rational(15, 8) - 3 * e
r3 = sp.Rational(17, 8) - 3 * e

# Verify the claimed unique nontrivial route-order crossing in the open interval.
require(is_zero(M[2] - M[9] - 2 * (e - sp.Rational(1, 16))),
        "route 2 / route 14 crossing identity")
interior_crossings: list[tuple[int, int, sp.Expr]] = []
for left in range(16):
    for right in range(left + 1, 16):
        diff = sp.expand(M[left] - M[right])
        if is_zero(diff):
            continue
        poly = sp.Poly(diff, e)
        require(poly.degree() <= 1, f"non-affine route comparison {left},{right}")
        if poly.degree() == 1:
            root = sp.simplify(-poly.nth(0) / poly.nth(1))
            if bool(root > 0 and root < EIGHTH):
                interior_crossings.append((left, right, root))
require(interior_crossings == [(2, 9, sp.Rational(1, 16))],
        f"unexpected route crossings: {interior_crossings}")

# Every route below r0 is empty or a singleton; 14 equals r0.
require(is_zero(M[9] - r0), "14 does not equal r0")
for mask in range(16):
    if mask.bit_count() >= 2 and mask != 9:
        positive_open(M[mask] - r0, f"route {mask} above r0")

# Exact route filtrations for the next three levels.
below_r1 = {0, 1, 2, 4, 8, 9}
equal_r1 = {5, 12}
for mask in range(16):
    if mask in below_r1:
        positive_open(r1 - M[mask], f"route {mask} below r1")
    elif mask in equal_r1:
        require(is_zero(M[mask] - r1), f"route {mask} not equal r1")
    else:
        positive_open(M[mask] - r1, f"route {mask} above r1")

for mask in range(16):
    if mask.bit_count() <= 2:
        positive_open(r2 - M[mask], f"route {mask} below r2")
    elif mask == 13:  # 134
        require(is_zero(M[mask] - r2), "134 not equal r2")
    else:
        positive_open(M[mask] - r2, f"route {mask} above r2")

for mask in range(16):
    if mask.bit_count() <= 2 or mask == 13:
        positive_open(r3 - M[mask], f"route {mask} below r3")
    elif mask == 11:  # 124
        require(is_zero(M[mask] - r3), "124 not equal r3")
    else:
        positive_open(M[mask] - r3, f"route {mask} above r3")

A = (3 - 4 * e) / (1 + 2 * e)
B = 1 / e - 2
C = 2 / e - 2

require(is_zero(A - 1 - 2 * (1 - 3 * e) / (1 + 2 * e)),
        "A-1 identity")
require(is_zero(B - A - (1 - 3 * e) / (e * (1 + 2 * e))),
        "B-A identity")
require(is_zero(C - B - 1 / e), "C-B identity")

T = a * (k1 + k4) + e * k2 + sp.Rational(1, 2) * k3

# Equal scenario threshold and coverage.
T_equal = sp.expand(T.subs({k1: 1, k2: 1, k3: 1, k4: 1}))
require(is_zero(T_equal - (1 + 3 * e)), "equal-scenario threshold")
positive_open(T_equal - 1, "equal scenario eliminates singletons")
positive_open(2 - T_equal, "equal scenario accepts pairs")

# Explicit construction identities.
T_A = sp.expand(T.subs({k1: 1, k2: kappa, k3: kappa, k4: 1}) - 2)
require(is_zero(T_A - (sp.Rational(1, 2) + e) * (kappa - A)),
        "A construction identity")

T_triangle_pair = sp.expand(T.subs({k1: 1, k2: kappa, k3: 1, k4: 1}) - 2)
require(is_zero(T_triangle_pair - e * (kappa - B)),
        "B triangle identity")

T_triangle_triple = sp.expand(T.subs({k1: 1, k2: kappa, k3: 1, k4: 1}) - 3)
require(is_zero(T_triangle_triple - e * (kappa - C)),
        "C triangle identity")

T_star_pair = sp.expand(
    T.subs({k1: kappa, k2: 1, k3: kappa, k4: kappa}) - (1 + kappa)
)
require(is_zero(T_star_pair - (2 * e * kappa + e - 1)),
        "star construction identity")
require(is_zero(B - (1 - e) / (2 * e) - (1 - 3 * e) / (2 * e)),
        "star threshold comparison")

# Constants in the A and C upper bounds.
require(is_zero(2 * (sp.Rational(3, 4) - e)
                    - (sp.Rational(1, 2) + e) * A),
        "A obstruction constant")
require(is_zero(2 * (sp.Rational(3, 4) - e)
                    + sp.Rational(1, 2) - e * C),
        "C obstruction constant")

# The middle two-outer-pair lemma, reconstructed from the losing gaps.
def set_weight(mask: int) -> sp.Expr:
    return sum((ks[i] for i in range(4) if mask & (1 << i)), ZERO)

outer_pair_masks = (5, 9, 12)  # 13, 14, 34
expected_rhs = {
    (5, 9): (sp.Rational(3, 2) - 2 * e) * k1
            + (sp.Rational(1, 2) - 2 * e) * k4,
    (5, 12): (sp.Rational(1, 2) - 2 * e) * (k1 + k4) + k3,
    (9, 12): (sp.Rational(1, 2) - 2 * e) * k1
             + (sp.Rational(3, 2) - 2 * e) * k4,
}
for i in range(3):
    for j in range(i + 1, 3):
        pair = (outer_pair_masks[i], outer_pair_masks[j])
        gap_sum = sp.expand((T - set_weight(pair[0])) + (T - set_weight(pair[1])))
        rhs = expected_rhs[pair]
        require(is_zero(gap_sum - (2 * e * k2 - rhs)),
                f"outer-pair sum identity {pair}")
        coeffs = [sp.expand(rhs).coeff(variable) for variable in (k1, k3, k4)]
        for index, coefficient in enumerate(coeffs):
            nonnegative_closed(coefficient, f"outer-pair coefficient {pair} #{index}")
        require(is_zero(sum(coeffs, ZERO) - (2 - 4 * e)),
                f"outer-pair coefficient sum {pair}")

# Final unrestricted obstruction.
both_triples = sp.expand(
    (T - set_weight(13)) +  # 134
    (T - set_weight(11))    # 124
)
expected_both = (
    (-sp.Rational(3, 2) + 2 * e) * (k1 + k4)
    + (2 * e - 1) * k2
)
require(is_zero(both_triples - expected_both),
        "two-triple impossibility identity")
positive_open(sp.Rational(3, 2) - 2 * e,
              "two-triple negative outer coefficient magnitude")
positive_open(1 - 2 * e,
              "two-triple negative center coefficient magnitude")

# Coefficient comparisons used to show that eliminating 134 forces k2>T,
# and eliminating 124 forces k3>T.
positive_open((1 - e) - e, "1-e > epsilon")
positive_open((sp.Rational(3, 4) - e) - a,
              "3/4-epsilon > 1/4+epsilon")

print("PASS: reconstructed all 16 route maxima on 13 arcs")
print("PASS: verified the r0, r1, r2, r3 route filtrations")
print("PASS: verified A, B, C construction and obstruction identities")
print("PASS: verified all three two-outer-pair certificates")
print("PASS: verified the final 134/124/23 obstruction identities")
