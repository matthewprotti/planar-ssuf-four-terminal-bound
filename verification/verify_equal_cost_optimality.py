#!/usr/bin/env python3
"""Symbolic audit of the restricted fixed-topology optimality theorem.

Requires SymPy.  This script checks the exact pair-max formulas, the
convex-combination identities used in every case, and the calculus leading to
(299 - 41*sqrt(41))/32.
"""

from __future__ import annotations

from itertools import combinations
import sympy as sp

from verify_symbolic_family import SUPPORTS

# General fractional cheap and expensive amounts.
l = {i: sp.symbols(f"ell{i}", nonnegative=True) for i in range(1, 5)}
e = {i: sp.symbols(f"e{i}", nonnegative=True) for i in range(1, 5)}


def deviations(pair: frozenset[int]) -> tuple[sp.Expr, ...]:
    result = []
    for arc in range(1, 6):
        value = sp.Integer(0)
        for i in range(1, 5):
            if arc in SUPPORTS[i]:
                value += e[i] if i in pair else -l[i]
        result.append(sp.expand(value))
    return tuple(result)


PAIR_DEV = {
    tuple(pair): deviations(frozenset(pair))
    for pair in combinations(range(1, 5), 2)
}

# Exact maximum candidates and dominance decompositions.
M12 = e[1] + e[2]
assert tuple(sp.expand(M12 - z) for z in PAIR_DEV[(1, 2)]) == (
    0, l[3], l[3] + l[4], e[1] + l[3] + l[4], e[1] + l[3]
)

M13 = e[1] + e[3] - l[2]
assert tuple(sp.expand(M13 - z) for z in PAIR_DEV[(1, 3)]) == (
    e[3], 0, l[4], e[1] + l[4], e[1]
)

M23 = e[2] + e[3]
assert tuple(sp.expand(M23 - z) for z in PAIR_DEV[(2, 3)]) == (
    e[3] + l[1], l[1], l[1] + l[4], l[4], 0
)

M34 = e[3] + e[4] - l[2]
assert tuple(sp.expand(M34 - z) for z in PAIR_DEV[(3, 4)]) == (
    e[3] + e[4] + l[1], e[4] + l[1], l[1], 0, e[4]
)

A14 = e[1] - l[2]
B14 = e[1] + e[4] - l[2] - l[3]
assert sp.expand(A14 - PAIR_DEV[(1, 4)][0]) == 0
assert sp.expand(A14 - PAIR_DEV[(1, 4)][1]) == l[3]
assert sp.expand(B14 - PAIR_DEV[(1, 4)][2]) == 0
assert sp.expand(B14 - PAIR_DEV[(1, 4)][3]) == e[1]
assert sp.expand(A14 - PAIR_DEV[(1, 4)][4]) == e[1] + l[3]

A24 = e[2] - l[1]
B24 = e[2] + e[4] - l[3]
assert sp.expand(A24 - PAIR_DEV[(2, 4)][0]) == 0
assert sp.expand(A24 - PAIR_DEV[(2, 4)][1]) == l[3]
assert sp.expand(B24 - PAIR_DEV[(2, 4)][2]) == l[1]
assert sp.expand(B24 - PAIR_DEV[(2, 4)][3]) == 0
assert sp.expand(B24 - PAIR_DEV[(2, 4)][4]) == e[4]
assert sp.expand(B14 - A14) == e[4] - l[3]
assert sp.expand(B24 - A24) == e[4] - l[3] + l[1]

# Reduced four-variable proof.
s, t, p, q = sp.symbols("s t p q", positive=True)
T1 = s*(1-p) + t*(1-q)
T2 = 1 + (1-s)*p + (1-t)*q
T3_upper = (1 + 2*s + (1-2*s)*p + (1-t)*q) / 2
T3_lower_region = (1 + 2*t + (1-2*s)*p + (1-2*t)*q) / 2

# Region t >= s and s + s/t <= 1.
identity_low = sp.factor((1-2*s)*T1 + 2*s*T3_upper)
assert sp.simplify(
    identity_low - (t + 2*s*(1-t) + q*(s*(1+t)-t))
) == 0

# Region t >= s and s + s/t >= 1.
lambda1 = s/t - s
lambda2 = s + s/t - 1
lambda3 = 2*(1-s/t)
assert sp.simplify(lambda1 + lambda2 + lambda3 - 1) == 0
g = sp.factor(s*(4-s-t-s/t))
assert sp.simplify(lambda1*T1 + lambda2*T2 + lambda3*T3_upper - g) == 0

# Region t <= s, split at t=1/2.
assert sp.simplify(
    (1-2*t)*T1 + 2*t*T3_lower_region
    - (s + 2*t - 2*s*t + p*(t-s))
) == 0
assert sp.simplify(
    (2*t-1)*T2 + 2*(1-t)*T3_lower_region
    - (t*(3-2*t) + p*(t-s))
) == 0

# Interior and boundary calculus for g.
g_s = sp.factor(sp.diff(g, s))
g_t = sp.factor(sp.diff(g, t))
assert sp.simplify(g_s - (4-t-2*s-2*s/t)) == 0
assert sp.simplify(g_t - s*(s/t**2-1)) == 0

q_star = (sp.sqrt(41)-3)/4
L = (sp.Integer(299)-41*sp.sqrt(41))/32
assert sp.simplify(2*q_star**2 + 3*q_star - 4) == 0
assert sp.simplify(g.subs({s: q_star**2, t: q_star}) - L) == 0

hessian = sp.hessian(g, (s, t)).subs({s: q_star**2, t: q_star})
assert sp.N(hessian.trace(), 30) < 0
assert sp.N(hessian.det(), 30) > 0

assert sp.simplify(g.subs(s, t) - t*(3-2*t)) == 0
assert sp.simplify(g.subs(t, 1) - s*(3-2*s)) == 0
assert sp.simplify(g.subs(s, t/(t+1)) - t*(3-t)/(t+1)) == 0
assert sp.simplify(t*(3-2*t) - (sp.Rational(9, 8) - 2*(t-sp.Rational(3,4))**2)) == 0
assert sp.simplify(t*(3-t)/(t+1) - (1 - (t-1)**2/(t+1))) == 0
assert 263**2 - 41**3 == 248  # proves L > 9/8 after squaring positive sides

print("PASS: general pair-max formulas were derived from the graph supports.")
print("PASS: dominance identities justify all six piecewise maxima.")
print("PASS: all convex-combination cancellations in the upper-bound proof hold.")
print(f"g(s,t) = {g}")
print(f"partial_s g = {g_s}")
print(f"partial_t g = {g_t}")
print(f"q_* = {q_star}")
print(f"g(q_*^2,q_*) = {L} = {sp.N(L, 16)}")
print("PASS: all boundary formulas are at most 9/8 or 1, and L > 9/8.")
