#!/usr/bin/env python3
"""Symbolic audit of the parametric four-terminal SSUF family.

Requires SymPy.  Path incidences and trunk difference supports are derived
from the directed graph in verify_concrete_instance.py; the six overload
formulas are not supplied as input.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import sympy as sp

from verify_concrete_instance import DEFAULT_INSTANCE, Arc

DATA = DEFAULT_INSTANCE
q, eps = sp.symbols("q eps", positive=True)


def adjacency() -> dict[str, tuple[str, ...]]:
    out: dict[str, list[str]] = {v: [] for v in DATA.vertices}
    for u, v in DATA.arcs:
        out[u].append(v)
    return {u: tuple(vs) for u, vs in out.items()}


def enumerate_paths(target: str) -> tuple[tuple[Arc, ...], ...]:
    adj = adjacency()
    result: list[tuple[Arc, ...]] = []

    def dfs(u: str, visited: frozenset[str], path: tuple[Arc, ...]) -> None:
        if u == target:
            result.append(path)
            return
        for v in adj[u]:
            if v not in visited:
                dfs(v, visited | {v}, path + ((u, v),))

    dfs(DATA.source, frozenset({DATA.source}), tuple())
    return tuple(result)


def classify_paths() -> dict[int, dict[str, tuple[Arc, ...]]]:
    classified: dict[int, dict[str, tuple[Arc, ...]]] = {}
    for index, terminal in enumerate(DATA.terminals, start=1):
        paths = enumerate_paths(terminal)
        if len(paths) != 2:
            raise AssertionError((terminal, paths))
        charged = DATA.charged_expensive_arc[terminal]
        expensive = [path for path in paths if charged in path]
        cheap = [path for path in paths if charged not in path]
        if len(expensive) != 1 or len(cheap) != 1:
            raise AssertionError((terminal, expensive, cheap))
        classified[index] = {"E": expensive[0], "C": cheap[0]}
    return classified


PATHS = classify_paths()
TRUNK_INDEX = {arc: j + 1 for j, arc in enumerate(DATA.trunk)}
SUPPORTS: dict[int, frozenset[int]] = {}
for i in range(1, 5):
    cheap = set(PATHS[i]["C"])
    expensive = set(PATHS[i]["E"])
    diff = []
    for arc, index in TRUNK_INDEX.items():
        incidence_difference = int(arc in cheap) - int(arc in expensive)
        if incidence_difference not in (0, 1):
            raise AssertionError((i, arc, incidence_difference))
        if incidence_difference == 1:
            diff.append(index)
    SUPPORTS[i] = frozenset(diff)

assert SUPPORTS == {
    1: frozenset({1, 2, 3}),
    2: frozenset({1, 2, 3, 4, 5}),
    3: frozenset({2, 3, 4, 5}),
    4: frozenset({3, 4}),
}

# Demands and fractional cheap fractions.
d = {1: sp.Integer(1), 2: q**2, 3: q, 4: sp.Integer(1)}
p = {
    1: 1 - q**2,
    2: q**2 + 2*q - 2 + eps,
    3: 1 - q,
    4: 1 - q,
}


def trunk_deviation(cheap_set: frozenset[int], trunk_index: int) -> sp.Expr:
    value = sp.Integer(0)
    for i in range(1, 5):
        if trunk_index not in SUPPORTS[i]:
            continue
        value += d[i] * (1 - p[i]) if i in cheap_set else -d[i] * p[i]
    return sp.factor(value)


assert sp.simplify(sum(p.values()) - (1 + eps)) == 0
assert sp.simplify(sum(1 - p[i] for i in range(1, 5)) - (3 - eps)) == 0

R = sp.factor(q**2 * (4 - q**2 - 2*q - eps))
witnesses = {
    frozenset({1, 2}): 1,
    frozenset({1, 3}): 2,
    frozenset({1, 4}): 3,
    frozenset({2, 3}): 5,
    frozenset({2, 4}): 4,
    frozenset({3, 4}): 4,
}
for cheap_pair, arc_index in witnesses.items():
    actual = trunk_deviation(cheap_pair, arc_index)
    expected = R if cheap_pair != frozenset({3, 4}) else R + q - q**2
    assert sp.simplify(actual - expected) == 0, (cheap_pair, arc_index, actual, expected)

# Derive every trunk expression for auditability.
all_pair_expressions = {
    tuple(sorted(pair)): tuple(trunk_deviation(frozenset(pair), j) for j in range(1, 6))
    for pair in combinations(range(1, 5), 2)
}

f = sp.expand(R.subs(eps, 0))
f_prime = sp.factor(sp.diff(f, q))
q_star = (sp.sqrt(41) - 3) / 4
L = (sp.Integer(299) - 41 * sp.sqrt(41)) / 32

assert sp.simplify(f_prime - 2*q*(4 - 3*q - 2*q**2)) == 0
assert sp.simplify(4 - 3*q_star - 2*q_star**2) == 0
assert sp.simplify(f.subs(q, q_star) - L) == 0

# Exact audit of the 335/294 finite certificate.
q0 = sp.Rational(6, 7)
eps0 = sp.Rational(1, 10584)
scale = sp.Integer(294)
assert sp.simplify(
    eps0 - (sp.Rational(97, 216) - (q0**2 + 2*q0 - 2))
) == 0

scaled_demands = [sp.simplify(scale * d[i].subs(q, q0)) for i in range(1, 5)]
scaled_cheap = [
    sp.simplify(scale * d[i].subs(q, q0) * p[i].subs({q: q0, eps: eps0}))
    for i in range(1, 5)
]
scaled_expensive = [scaled_demands[i] - scaled_cheap[i] for i in range(4)]
scaled_R = sp.simplify(scale * R.subs({q: q0, eps: eps0}))

assert scaled_demands == [294, 216, 252, 294]
assert scaled_cheap == [78, 97, 36, 42]
assert scaled_expensive == [216, 119, 216, 252]
assert scaled_R == 335

def main() -> None:
    print("PASS: reconstructed both paths for each terminal from the directed graph.")
    print(f"PASS: derived trunk difference supports {SUPPORTS}.")
    print("PASS: cheap fractions sum to 1 + epsilon.")
    print("PASS: fractional cost is 3 - epsilon under per-unit expensive-path cost 1/d_i.")
    print("PASS: all six pair witness identities were derived from graph incidences.")
    for pair, expressions in all_pair_expressions.items():
        print(f"  pair {pair}: {expressions}")
    print(f"R(q, epsilon) = {R}")
    print(f"f'(q) = {f_prime}")
    print(f"q_* = {q_star}")
    print(f"f(q_*) = {L} = {sp.N(L, 16)}")
    print("PASS: q=6/7, epsilon=1/10584 scales to the 335/294 integer certificate.")


if __name__ == "__main__":
    main()
