#!/usr/bin/env python3
"""Exact and regression checks for the global one-scenario fixed-gadget theorem.

The human-readable proof is authoritative.  This program verifies the finite
cover classification, graph-native route formulas, algebraic envelopes, the
F064 lower sequence, and deterministic exact/numerical regressions.

No Python ``assert`` statements are used, so ``python -O`` cannot remove checks.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path
import random
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCOUT = ROOT / "source_inputs" / "one_scenario_numerical_scout.json"

N = 4
SUBSETS = tuple(range(1 << N))
ALL = (1 << N) - 1
SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def members(mask: int) -> frozenset[int]:
    return frozenset(i for i in range(N) if mask & (1 << i))


def label_set(s: frozenset[int]) -> str:
    return "".join(str(i + 1) for i in sorted(s)) or "empty"


def downset_mask(weights: tuple[int, int, int, int], quota: int) -> int:
    out = 0
    for mask in SUBSETS:
        weight = sum(weights[i] for i in range(N) if mask & (1 << i))
        if weight <= quota:
            out |= 1 << mask
    return out


def feasible_sets(bitmask: int) -> set[frozenset[int]]:
    return {members(mask) for mask in SUBSETS if bitmask & (1 << mask)}


def minimal_blockers(bitmask: int) -> tuple[frozenset[int], ...]:
    feasible = {mask for mask in SUBSETS if bitmask & (1 << mask)}
    blockers: list[frozenset[int]] = []
    for mask in range(1, 1 << N):
        if mask in feasible:
            continue
        proper = [sub for sub in SUBSETS if sub != mask and (sub & mask) == sub]
        if all(sub in feasible for sub in proper):
            blockers.append(members(mask))
    return tuple(blockers)


def solve_square_system(
    matrix: list[list[Fraction]], rhs: list[Fraction]
) -> tuple[Fraction, ...] | None:
    m = sp.Matrix(
        [[sp.Rational(x.numerator, x.denominator) for x in row] for row in matrix]
    )
    if m.det() == 0:
        return None
    b = sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in rhs])
    solution = m.LUsolve(b)
    return tuple(Fraction(int(x.p), int(x.q)) for x in solution)


def cover_vertices(blockers: tuple[frozenset[int], ...]) -> tuple[tuple[Fraction, ...], ...]:
    """Enumerate cover-polyhedron vertices from all four active constraints."""
    constraints: list[tuple[tuple[Fraction, ...], Fraction]] = []
    for blocker in blockers:
        constraints.append(
            (
                tuple(Fraction(1 if i in blocker else 0) for i in range(N)),
                Fraction(1),
            )
        )
    for i in range(N):
        constraints.append(
            (
                tuple(Fraction(1 if i == j else 0) for j in range(N)),
                Fraction(0),
            )
        )

    vertices: set[tuple[Fraction, ...]] = set()
    for active in combinations(range(len(constraints)), N):
        matrix = [list(constraints[j][0]) for j in active]
        rhs = [constraints[j][1] for j in active]
        solution = solve_square_system(matrix, rhs)
        if solution is None:
            continue
        if all(
            sum(coeff[i] * solution[i] for i in range(N)) >= bound
            for coeff, bound in constraints
        ):
            vertices.add(solution)

    undominated: list[tuple[Fraction, ...]] = []
    for vertex in vertices:
        if any(
            other != vertex and all(other[i] <= vertex[i] for i in range(N))
            for other in vertices
        ):
            continue
        require(all(Fraction(0) <= x <= Fraction(1) for x in vertex),
                f"extreme cover coordinate outside [0,1]: {vertex}")
        undominated.append(vertex)
    return tuple(sorted(undominated))


def is_integral_cover(vertex: tuple[Fraction, ...]) -> bool:
    return all(x in (Fraction(0), Fraction(1)) for x in vertex)


def fset(*items: int) -> frozenset[int]:
    return frozenset(i - 1 for i in items)


CANONICAL_ROWS: dict[str, tuple[tuple[frozenset[int], ...], set[tuple[Fraction, ...]]]] = {
    "m0": ((fset(1), fset(2), fset(3), fset(4)), set()),
    "m1": ((fset(2), fset(3), fset(4)), set()),
    "m2e0": ((fset(1, 2), fset(3), fset(4)), set()),
    "m2e1": ((fset(3), fset(4)), set()),
    "m3e0": (
        (fset(1, 2), fset(1, 3), fset(2, 3), fset(4)),
        {(Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1))},
    ),
    "m3e1": ((fset(1, 3), fset(2, 3), fset(4)), set()),
    "m3e2": ((fset(2, 3), fset(4)), set()),
    "m3e3": ((fset(1, 2, 3), fset(4)), set()),
    "m4e0": (
        (fset(1, 2), fset(1, 3), fset(1, 4), fset(2, 3), fset(2, 4), fset(3, 4)),
        {(Fraction(1, 2),) * 4},
    ),
    "m4e1": (
        (fset(1, 3), fset(1, 4), fset(2, 3), fset(2, 4), fset(3, 4)),
        {(Fraction(1, 2),) * 4},
    ),
    "m4e2": (
        (fset(2, 3), fset(1, 4), fset(2, 4), fset(3, 4)),
        {(Fraction(1, 2),) * 4},
    ),
    "m4star": (
        (fset(2, 3), fset(2, 4), fset(3, 4)),
        {(Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))},
    ),
    "m4triangle": (
        (fset(1, 2, 3), fset(1, 4), fset(2, 4), fset(3, 4)),
        {(Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(2, 3))},
    ),
    "m4e4": (
        (fset(1, 2, 3), fset(2, 4), fset(3, 4)),
        {(Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))},
    ),
    "m4e5": (
        (fset(1, 2, 3), fset(1, 2, 4), fset(3, 4)),
        {
            (Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2)),
            (Fraction(1, 2), Fraction(0), Fraction(1, 2), Fraction(1, 2)),
        },
    ),
}


def canonical_cover_check() -> dict[str, object]:
    details: dict[str, object] = {}
    for name, (blockers, expected_fractional) in CANONICAL_ROWS.items():
        vertices = cover_vertices(blockers)
        actual_fractional = {v for v in vertices if not is_integral_cover(v)}
        require(
            actual_fractional == expected_fractional,
            f"canonical cover mismatch in {name}: {actual_fractional} != {expected_fractional}",
        )
        details[name] = {
            "blockers": [label_set(s) for s in blockers],
            "undominated_vertices": [[str(x) for x in v] for v in vertices],
        }
    return details


def graph_signature(bitmask: int) -> tuple[int, int, str]:
    sets = feasible_sets(bitmask)
    vertices = {next(iter(s)) for s in sets if len(s) == 1}
    edges = {tuple(sorted(s)) for s in sets if len(s) == 2}
    m, e = len(vertices), len(edges)
    kind = ""
    if m == 4 and e == 3:
        degrees = Counter(i for edge in edges for i in edge)
        kind = "star" if sorted(degrees.values()) == [1, 1, 1, 3] else "triangle"
    return m, e, kind


def classify_fractional_cover(
    bitmask: int, vertex: tuple[Fraction, ...]
) -> tuple[str, tuple[int, ...]]:
    m, e, kind = graph_signature(bitmask)
    sets = feasible_sets(bitmask)
    edges = {tuple(sorted(s)) for s in sets if len(s) == 2}
    nonzero = tuple(i for i, x in enumerate(vertex) if x)
    values = tuple(vertex[i] for i in nonzero)

    if m == 3 and e == 0:
        blocked = tuple(i for i in range(N) if fset(i + 1) not in sets)
        require(len(blocked) == 1, "three-singleton row must have one blocked vertex")
        u = blocked[0]
        require(vertex[u] == 1, "blocked singleton must have cover value 1")
        require(all(vertex[i] == Fraction(1, 2) for i in range(N) if i != u),
                "three-singleton fractional cover mismatch")
        return "three-singleton", (u,)

    if m == 4 and e in (0, 1, 2):
        require(vertex == (Fraction(1, 2),) * 4, "sparse four-vertex cover mismatch")
        return "all-half", tuple(range(N))

    if m == 4 and e == 3 and kind == "star":
        require(values == (Fraction(1, 2),) * 3, "star cover mismatch")
        u = next(i for i in range(N) if vertex[i] == 0)
        require(all(tuple(sorted((u, i))) in edges for i in nonzero),
                "outside star vertex must be adjacent to all half-covered vertices")
        return "triple-half", nonzero

    if m == 4 and e == 3 and kind == "triangle":
        u = next(i for i, x in enumerate(vertex) if x == Fraction(2, 3))
        require(all(vertex[i] == Fraction(1, 3) for i in range(N) if i != u),
                "triangle-isolated cover mismatch")
        return "triangle-isolated", (u,)

    if m == 4 and e in (4, 5):
        require(values == (Fraction(1, 2),) * 3, "dense triple-half cover mismatch")
        u = next(i for i in range(N) if vertex[i] == 0)
        require(all(tuple(sorted((u, i))) in edges for i in nonzero),
                "outside dense-row vertex must be universal to the half-covered triple")
        return "triple-half", nonzero

    if m == 4 and e == 6:
        return "separated-all-pairs", nonzero

    raise RuntimeError(f"unclassified fractional cover: signature={(m, e, kind)}, vertex={vertex}")


def threshold_census_crosscheck() -> dict[str, object]:
    families: dict[int, tuple[tuple[int, ...], int]] = {}
    for weights in product(range(1, 5), repeat=N):
        for quota in range(sum(weights) + 1):
            families.setdefault(downset_mask(weights, quota), (weights, quota))
    require(len(families) == 149, f"expected 149 positive threshold families, got {len(families)}")

    no_triple = 0
    signatures = Counter()
    branches = Counter()
    for bitmask in families:
        sets = feasible_sets(bitmask)
        if any(len(s) == 3 for s in sets):
            continue
        no_triple += 1
        signatures[graph_signature(bitmask)] += 1
        blockers = minimal_blockers(bitmask)
        for cover in cover_vertices(blockers):
            if is_integral_cover(cover):
                chosen = {i for i, x in enumerate(cover) if x == 1}
                complement = frozenset(set(range(N)) - chosen)
                require(complement in sets, "integral cover complement is not feasible")
            else:
                kind, data = classify_fractional_cover(bitmask, cover)
                branches[(kind, data)] += 1

    require(no_triple == 95, f"expected 95 no-E-triple families, got {no_triple}")
    expected_signatures = Counter(
        {
            (0, 0, ""): 1,
            (1, 0, ""): 4,
            (2, 0, ""): 6,
            (2, 1, ""): 6,
            (3, 0, ""): 4,
            (3, 1, ""): 12,
            (3, 2, ""): 12,
            (3, 3, ""): 4,
            (4, 0, ""): 1,
            (4, 1, ""): 6,
            (4, 2, ""): 12,
            (4, 3, "star"): 4,
            (4, 3, "triangle"): 4,
            (4, 4, ""): 12,
            (4, 5, ""): 6,
            (4, 6, ""): 1,
        }
    )
    require(signatures == expected_signatures, f"unexpected graph census: {signatures}")
    return {
        "positive_threshold_families": len(families),
        "no_E_triple_families": no_triple,
        "signatures": {str(k): v for k, v in sorted(signatures.items())},
        "fractional_branch_occurrences": sum(branches.values()),
    }


def trunk_expressions_for_cset(
    cset: frozenset[int], h: tuple[sp.Symbol, ...], ell: tuple[sp.Symbol, ...]
) -> tuple[sp.Expr, ...]:
    values: list[sp.Expr] = []
    for arc in range(5):
        value = sp.Integer(0)
        for i in range(N):
            if arc not in SUPPORTS[i]:
                continue
            value += h[i] if i in cset else -ell[i]
        values.append(sp.expand(value))
    return tuple(values)


def linear_nonnegative(expr: sp.Expr, variables: tuple[sp.Symbol, ...]) -> bool:
    poly = sp.Poly(sp.expand(expr), *variables)
    return all(coefficient >= 0 for coefficient in poly.coeffs())


def verify_max_formula(
    actual: tuple[sp.Expr, ...],
    candidates: tuple[sp.Expr, ...],
    variables: tuple[sp.Symbol, ...],
    label: str,
) -> None:
    for candidate in candidates:
        require(any(sp.simplify(candidate - expression) == 0 for expression in actual),
                f"{label}: candidate {candidate} is not attained")
    for expression in actual:
        require(any(linear_nonnegative(candidate - expression, variables) for candidate in candidates),
                f"{label}: actual arc expression {expression} is not dominated by a candidate")


def route_formula_check() -> dict[str, object]:
    h = sp.symbols("h1:5", nonnegative=True)
    ell = sp.symbols("l1:5", nonnegative=True)
    variables = tuple(h) + tuple(ell)
    H = sum(h)

    singleton = {
        "E1": (frozenset({1, 2, 3}), (H - h[0],)),
        "E2": (frozenset({0, 2, 3}), (H - h[1] - ell[1],)),
        "E3": (frozenset({0, 1, 3}), (h[0] + h[1], H - h[2] - ell[2])),
        "E4": (frozenset({0, 1, 2}), (H - h[3],)),
    }
    pairs = {
        "C12": (frozenset({0, 1}), (h[0] + h[1],)),
        "C13": (frozenset({0, 2}), (h[0] + h[2] - ell[1],)),
        "C14": (frozenset({0, 3}), (h[0] - ell[1], h[0] + h[3] - ell[1] - ell[2])),
        "C23": (frozenset({1, 2}), (h[1] + h[2],)),
        "C24": (frozenset({1, 3}), (h[1] - ell[0], h[1] + h[3] - ell[2])),
        "C34": (frozenset({2, 3}), (h[2] + h[3] - ell[1],)),
    }
    triples = {
        "C234": (frozenset({1, 2, 3}), (h[1] + h[2] + h[3],)),
        "C134": (frozenset({0, 2, 3}), (h[0] + h[2] + h[3] - ell[1],)),
        "C124": (frozenset({0, 1, 3}), (h[0] + h[1], h[0] + h[1] + h[3] - ell[2])),
        "C123": (frozenset({0, 1, 2}), (h[0] + h[1] + h[2],)),
    }

    checked: list[str] = []
    for group in (singleton, pairs, triples):
        for label, (cset, candidates) in group.items():
            actual = trunk_expressions_for_cset(cset, h, ell)
            verify_max_formula(actual, tuple(sp.expand(x) for x in candidates), variables, label)
            checked.append(label)
    return {"formulas_checked": checked}


def algebra_check() -> dict[str, str]:
    L = (sp.Integer(299) - 41 * sp.sqrt(41)) / 32
    require(bool(sp.N(L - sp.Rational(9, 8), 50) > 0), "L must exceed 9/8")

    Delta = sp.symbols("Delta", real=True)
    require(sp.expand(sp.Rational(9, 8) - (3 * Delta - 2 * Delta**2)
                      - 2 * (Delta - sp.Rational(3, 4)) ** 2) == 0,
            "Lemma 3 square identity failed")
    require(sp.expand(sp.Rational(9, 8) - Delta * (3 - 2 * Delta)
                      - 2 * (Delta - sp.Rational(3, 4)) ** 2) == 0,
            "Lemma 4 square identity failed")

    p = sp.symbols("p", real=True)
    require(sp.expand(sp.Rational(9, 8) - (1 + p / 2 - p**2 / 2)
                      - (p - sp.Rational(1, 2)) ** 2 / 2) == 0,
            "three-terminal chain identity failed")

    r = sp.symbols("r", positive=True)
    require(sp.factor(8 * r * (sp.Rational(9, 8) / r + r + r**2 - 3))
            == (2 * r - 1) * (4 * r**2 + 6 * r - 9),
            "isolated-2 small-branch factorization failed")

    a = sp.symbols("a", positive=True)
    u3 = sp.Rational(9, 4) - 2 * a + 2 * sp.sqrt(2 * a) - 3
    rr = sp.symbols("rr", positive=True)
    require(sp.simplify(u3.subs(a, rr**2 / 2) - (sp.Rational(1, 4) - (rr - 1) ** 2)) == 0,
            "isolated-3 identity failed")
    u4 = sp.Rational(13, 4) - 2 * a + 2 * sp.sqrt(a) - 3
    require(sp.simplify(u4.subs(a, rr**2) - (sp.Rational(3, 4) - 2 * (rr - sp.Rational(1, 2)) ** 2)) == 0,
            "isolated-4 identity failed")

    return {"L": str(L), "L_decimal": f"{float(L.evalf(40)):.15f}", "target": "9/8"}


def route_trunk(mask: int, q: tuple[Fraction, ...], d: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    p = tuple(Fraction(1) - q[i] for i in range(N))
    values: list[Fraction] = []
    for arc in range(5):
        value = Fraction(0)
        for i in range(N):
            if arc not in SUPPORTS[i]:
                continue
            value += -d[i] * p[i] if mask & (1 << i) else d[i] * q[i]
        values.append(value)
    return tuple(values)


def route_value(mask: int, q: tuple[Fraction, ...], d: tuple[Fraction, ...]) -> Fraction:
    p = tuple(Fraction(1) - q[i] for i in range(N))
    private = tuple(d[i] * (p[i] if mask & (1 << i) else q[i]) for i in range(N))
    return max(route_trunk(mask, q, d) + private)


def normalize_demands(raw: list[Fraction]) -> tuple[Fraction, ...]:
    maximum = max(raw)
    return tuple(x / maximum for x in raw)


def scale_q_to_resource(raw: list[Fraction], coefficients: list[int], limit: Fraction) -> tuple[Fraction, ...]:
    used = sum(Fraction(coefficients[i]) * raw[i] for i in range(N))
    if used <= limit:
        return tuple(raw)
    scale = limit / used
    return tuple(x * scale for x in raw)


def exact_targeted_regression(samples_per_branch: int = 1500, seed: int = 20260801) -> dict[str, object]:
    rng = random.Random(seed)
    target = Fraction(9, 8)
    maxima: dict[str, Fraction] = {}

    def random_data(coefficients: list[int], limit: Fraction) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
        q_raw = [Fraction(rng.randint(0, 1000), 1000) for _ in range(N)]
        q = scale_q_to_resource(q_raw, coefficients, limit)
        d_raw = [Fraction(rng.randint(1, 1000), 1000) for _ in range(N)]
        d = normalize_demands(d_raw)
        return q, d

    # Lemma 3.
    best = Fraction(0)
    for _ in range(samples_per_branch):
        q, d = random_data([1, 1, 1, 1], Fraction(2))
        value = min(route_value(1 << i, q, d) for i in range(N))
        require(value <= target, f"Lemma 3 exact sample exceeded 9/8: {value}")
        best = max(best, value)
    maxima["lemma3"] = best

    # Lemma 4, all four blocked-singleton placements.
    for u in range(N):
        best = Fraction(0)
        coeff = [1, 1, 1, 1]
        coeff[u] = 2
        masks = [1 << i for i in range(N) if i != u]
        for _ in range(samples_per_branch):
            q, d = random_data(coeff, Fraction(2))
            value = min(route_value(mask, q, d) for mask in masks)
            require(value <= target, f"Lemma 4 u={u+1} sample exceeded 9/8: {value}")
            best = max(best, value)
        maxima[f"lemma4_u{u+1}"] = best

    # Lemma 5, all four isolated placements.
    for u in range(N):
        best = Fraction(0)
        coeff = [1, 1, 1, 1]
        coeff[u] = 2
        A = [i for i in range(N) if i != u]
        masks = [(1 << i) | (1 << j) for i, j in combinations(A, 2)] + [1 << u]
        for _ in range(samples_per_branch):
            q, d = random_data(coeff, Fraction(3))
            value = min(route_value(mask, q, d) for mask in masks)
            require(value <= target, f"Lemma 5 u={u+1} sample exceeded 9/8: {value}")
            best = max(best, value)
        maxima[f"lemma5_u{u+1}"] = best

    return {key: {"fraction": str(value), "decimal": float(value)} for key, value in maxima.items()}


def f064_check() -> dict[str, str]:
    sqrt2 = sp.sqrt(2)
    delta = sp.symbols("delta", positive=True)
    delta_max = 1 - 1 / sqrt2
    p = (
        1 / sqrt2 + delta,
        (sqrt2 - 1) / 2,
        2 - sqrt2,
        1 - 1 / sqrt2,
    )
    q = tuple(sp.simplify(1 - value) for value in p)
    d = (sp.Integer(1), sp.Integer(1), 1 / sqrt2, sp.Integer(1))
    k = (sp.Integer(1), sp.Integer(2), sp.Integer(1), sp.Integer(1))
    tau = sp.simplify(sum(k[i] * p[i] for i in range(N)))
    require(sp.simplify(tau - (2 + delta)) == 0, "F064 threshold mismatch")

    feasible_c_masks = [
        mask for mask in SUBSETS
        if sum(k[i] for i in range(N) if mask & (1 << i)) >= 3
    ]
    minimal = {
        members(mask)
        for mask in feasible_c_masks
        if not any(
            members(other) < members(mask)
            for other in feasible_c_masks
        )
    }
    expected = {fset(1, 2), fset(2, 3), fset(2, 4), fset(1, 3, 4)}
    require(minimal == expected, f"F064 family mismatch: {minimal}")

    def expressions(cmask: int) -> list[sp.Expr]:
        eset = ALL ^ cmask
        values: list[sp.Expr] = []
        for arc in range(5):
            value = sp.Integer(0)
            for i in range(N):
                if arc not in SUPPORTS[i]:
                    continue
                hi = sp.simplify(d[i] * q[i])
                li = sp.simplify(d[i] * p[i])
                value += -li if eset & (1 << i) else hi
            values.append(sp.simplify(value))
        for i in range(N):
            hi = sp.simplify(d[i] * q[i])
            li = sp.simplify(d[i] * p[i])
            values.append(sp.simplify(li if eset & (1 << i) else hi))
        return values

    target = sp.Rational(5, 2) - sqrt2 - delta
    equality_found = False
    sample = {delta: sp.Rational(1, 100)}
    for mask in feasible_c_masks:
        values = expressions(mask)
        numerical = [float(sp.N(value.subs(sample), 60)) for value in values]
        witness = values[max(range(len(values)), key=lambda i: numerical[i])]
        slack = sp.simplify(witness - target)
        require(sp.simplify(slack.subs(delta, 0)) >= 0, "F064 witness fails at delta=0")
        require(sp.simplify(slack.subs(delta, delta_max)) >= 0,
                "F064 witness fails at upper endpoint")
        if mask in (0b0011, 0b1101):
            for value in values:
                upper_slack = sp.simplify(target - value)
                require(sp.simplify(upper_slack.subs(delta, 0)) >= 0,
                        "F064 equality route exceeds target at delta=0")
                require(sp.simplify(upper_slack.subs(delta, delta_max)) >= 0,
                        "F064 equality route exceeds target at upper endpoint")
            equality_found = True
    require(equality_found, "F064 equality routes were not found")
    return {
        "threshold": str(tau),
        "interval": f"0 < delta < {delta_max}",
        "finite_objective": str(target),
    }


def scout_audit() -> dict[str, object]:
    if not SCOUT.exists():
        return {"status": "not present"}
    payload = json.loads(SCOUT.read_text(encoding="utf-8"))
    rows = payload["results"]
    values = [row["best"]["value"] for row in rows]
    require(len(rows) == 79, "numerical scout must contain 79 rows")
    require(max(values) <= 9 / 8 + 1e-6, "numerical scout contains a value above tolerance")
    return {
        "cells": len(rows),
        "maximum": max(values),
        "above_1_1249": sum(value > 1.1249 for value in values),
        "evidence_role": "heuristic regression only",
    }


def main() -> None:
    report: dict[str, object] = {}
    report["canonical_cover_table"] = canonical_cover_check()
    print("PASS: independent canonical blocker-cover table")
    report["threshold_census_crosscheck"] = threshold_census_crosscheck()
    print("PASS: 149-family / 95-no-triple threshold cross-check")
    report["route_formulas"] = route_formula_check()
    print("PASS: graph-native singleton, pair, and triple route formulas")
    report["algebra"] = algebra_check()
    print("PASS: exact routing-envelope and isolated-branch algebra")
    report["targeted_exact_regression"] = exact_targeted_regression()
    print("PASS: exact rational targeted regression for Lemmas 3-5")
    report["f064"] = f064_check()
    print("PASS: F064 full-interval strict lower sequence")
    report["scout"] = scout_audit()
    if report["scout"].get("status") == "not present":
        print("SKIP: optional 79-cell numerical scout is absent; heuristic scout not checked")
    else:
        print("PASS: 79-cell numerical scout remains below 9/8 tolerance")

    output = HERE / "GLOBAL_ONE_SCENARIO_VERIFICATION_REPORT.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {output}")
    print("ALL GLOBAL ONE-SCENARIO CLOSING CHECKS PASSED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
