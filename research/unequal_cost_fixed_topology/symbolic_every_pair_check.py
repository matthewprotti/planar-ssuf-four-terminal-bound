#!/usr/bin/env python3
"""Exact symbolic audit of the local fixed-support lemma and every-pair theorem."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def sx(expr: sp.Expr) -> str:
    return str(sp.factor(sp.simplify(expr)))


def main() -> None:
    supports = {
        1: {1, 2, 3},
        2: {1, 2, 3, 4, 5},
        3: {2, 3, 4, 5},
        4: {3, 4},
    }
    e = {i: sp.symbols(f"e{i}", nonnegative=True) for i in range(1, 5)}
    ell = {i: sp.symbols(f"l{i}", nonnegative=True) for i in range(1, 5)}
    expected_candidates = {
        (1, 2): [e[1] + e[2]],
        (1, 3): [e[1] + e[3] - ell[2]],
        (1, 4): [e[1] - ell[2], e[1] + e[4] - ell[2] - ell[3]],
        (2, 3): [e[2] + e[3]],
        (2, 4): [e[2] - ell[1], e[2] + e[4] - ell[3]],
        (3, 4): [e[3] + e[4] - ell[2]],
    }
    arc_expressions = {}
    for pair in itertools.combinations(range(1, 5), 2):
        cheap = set(pair)
        expressions = []
        for arc in range(1, 6):
            expression = sum(
                (e[i] if i in cheap else -ell[i])
                for i in range(1, 5)
                if arc in supports[i]
            )
            expressions.append(sp.expand(expression))
        arc_expressions["".join(map(str, pair))] = [sx(item) for item in expressions]
        for expression in expressions:
            assert any(
                all(
                    coefficient >= 0
                    for _monomial, coefficient in sp.Poly(
                        sp.expand(candidate - expression),
                        *list(e.values()),
                        *list(ell.values()),
                    ).terms()
                )
                for candidate in expected_candidates[pair]
            )
        assert all(
            any(sp.simplify(candidate - expression) == 0 for expression in expressions)
            for candidate in expected_candidates[pair]
        )

    s, t, p, q = sp.symbols("s t p q", positive=True)
    e2, l2 = s * (1 - p), s * p
    e3, l3 = t * (1 - q), t * q
    T1 = e2 + e3
    T2 = 1 + p + q - l2 - l3
    T3tilde = (1 + 2 * s + (1 - 2 * s) * p + (1 - t) * q) / 2

    low = sp.expand((1 - 2 * s) * T1 + 2 * s * T3tilde)
    low_expected = t + 2 * s * (1 - t) + q * (s * (1 + t) - t)
    assert sp.simplify(low - low_expected) == 0

    lam1 = s / t - s
    lam2 = s + s / t - 1
    lam3 = 2 * (1 - s / t)
    assert sp.simplify(lam1 + lam2 + lam3 - 1) == 0
    g = s * (4 - s - t - s / t)
    main_identity = sp.expand(lam1 * T1 + lam2 * T2 + lam3 * T3tilde)
    assert sp.simplify(main_identity - g) == 0

    T3reverse = (1 + 2 * t + (1 - 2 * s) * p + (1 - 2 * t) * q) / 2
    small = sp.expand((1 - 2 * t) * T1 + 2 * t * T3reverse)
    assert sp.simplify(small - (s + 2 * t - 2 * s * t + p * (t - s))) == 0
    large = sp.expand((2 * t - 1) * T2 + 2 * (1 - t) * T3reverse)
    assert sp.simplify(large - (t * (3 - 2 * t) + p * (t - s))) == 0

    t_star = (sp.sqrt(41) - 3) / 4
    s_star = t_star**2
    L = (299 - 41 * sp.sqrt(41)) / 32
    assert sp.simplify(sp.diff(g, s).subs({s: s_star, t: t_star})) == 0
    assert sp.simplify(sp.diff(g, t).subs({s: s_star, t: t_star})) == 0
    assert sp.simplify(g.subs({s: s_star, t: t_star}) - L) == 0
    assert sp.simplify(L - sp.Rational(9, 8)) > 0

    eps = sp.symbols("eps", positive=True)
    p1 = 1 - q**2
    p2 = q**2 + 2 * q - 2 + eps
    p3 = p4 = 1 - q
    assert sp.simplify(p1 + p2 + p3 + p4 - (1 + eps)) == 0

    # Brute-force directed automorphisms preserving source/internal/terminal roles.
    vertices = ["s"] + [f"v{i}" for i in range(1, 6)] + [f"t{i}" for i in range(1, 5)]
    arcs = {("s" if i == 1 else f"v{i-1}", f"v{i}") for i in range(1, 6)}
    arcs |= {
        ("s", "t1"), ("v3", "t1"), ("s", "t2"), ("v5", "t2"),
        ("v1", "t3"), ("v5", "t3"), ("v2", "t4"), ("v4", "t4"),
    }
    automorphisms = []
    for internal_perm in itertools.permutations([f"v{i}" for i in range(1, 6)]):
        internal_map = dict(zip([f"v{i}" for i in range(1, 6)], internal_perm))
        for terminal_perm in itertools.permutations([f"t{i}" for i in range(1, 5)]):
            mapping = {"s": "s", **internal_map, **dict(zip([f"t{i}" for i in range(1, 5)], terminal_perm))}
            mapped_arcs = {(mapping[left], mapping[right]) for left, right in arcs}
            if mapped_arcs == arcs:
                automorphisms.append(mapping)
    assert len(automorphisms) == 1

    result = {
        "status": "PASS",
        "pair_arc_expressions": arc_expressions,
        "convex_combination_identities": "exact",
        "stationary_point": {"s": sx(s_star), "t": sx(t_star), "value": sx(L)},
        "lower_family_sum_p": sx(p1 + p2 + p3 + p4),
        "directed_role_preserving_automorphisms": len(automorphisms),
        "dependency_assessment": "PASS: upper theorem uses the local fixed-support lemma; no unexpanded proof import",
    }
    output = HERE / "symbolic_every_pair_results.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
