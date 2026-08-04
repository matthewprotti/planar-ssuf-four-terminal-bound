#!/usr/bin/env python3
"""Exact and audit checks for the scope-repaired SSUF next-gap package.

The Markdown proofs remain authoritative. This verifier deliberately avoids
Python ``assert`` statements, so running with ``python -O`` does not remove the
checks. It verifies exact finite constructions, symbolic identities, a full-
parameter positivity certificate for the bounded lower sequence, the full
F064 delta interval, and the stated limitations of the numerical scout.
"""
from __future__ import annotations
import ast
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Iterable, Sequence
import sympy as sp
HERE = Path(__file__).resolve().parent
# The public candidate carries one immutable scout payload beside this verifier.
# Keeping a single canonical path prevents a replay from depending on the layout
# of the private review packet from which the verifier was derived.
SOURCE = HERE
N = 4
FULL_MASK = (1 << N) - 1
SUBSETS = tuple(range(1 << N))
Arc = tuple[str, str]
TRUNK: tuple[Arc, ...] = (('s', 'v1'), ('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4'), ('v4', 'v5'))
PRIVATE: tuple[Arc, ...] = (('s', 't1'), ('v3', 't1'), ('s', 't2'), ('v5', 't2'), ('v1', 't3'), ('v5', 't3'), ('v2', 't4'), ('v4', 't4'))
ARCS = TRUNK + PRIVATE
TERMINALS = ('t1', 't2', 't3', 't4')
PATHS: dict[str, dict[str, tuple[Arc, ...]]] = {'t1': {'E': (('s', 't1'),), 'C': (('s', 'v1'), ('v1', 'v2'), ('v2', 'v3'), ('v3', 't1'))}, 't2': {'E': (('s', 't2'),), 'C': TRUNK + (('v5', 't2'),)}, 't3': {'E': (('s', 'v1'), ('v1', 't3')), 'C': TRUNK + (('v5', 't3'),)}, 't4': {'E': (('s', 'v1'), ('v1', 'v2'), ('v2', 't4')), 'C': (('s', 'v1'), ('v1', 'v2'), ('v2', 'v3'), ('v3', 'v4'), ('v4', 't4'))}}
SUPPORTS: tuple[frozenset[int], ...] = (frozenset({0, 1, 2}), frozenset({0, 1, 2, 3, 4}), frozenset({1, 2, 3, 4}), frozenset({2, 3}))


class VerificationFailure(RuntimeError):
    """Raised when an exact or audit check fails."""


def require(condition: object, message: object) -> None:
    """Require a concrete truth value without relying on Python assertions."""
    if condition is True or condition is sp.true:
        return
    try:
        if bool(condition):
            return
    except TypeError:
        pass
    raise VerificationFailure(str(message))


def require_equal(actual: object, expected: object, message: str) -> None:
    if isinstance(actual, sp.Basic) or isinstance(expected, sp.Basic):
        require(sp.simplify(actual - expected) == 0, f"{message}: {actual!r} != {expected!r}")
    else:
        require(actual == expected, f"{message}: {actual!r} != {expected!r}")


def require_nonnegative(expr: object, message: str) -> None:
    value = sp.simplify(expr)
    require(value == 0 or value.is_nonnegative is True, f"{message}: not proved nonnegative: {value}")


def require_positive(expr: object, message: str) -> None:
    value = sp.simplify(expr)
    require(value.is_positive is True, f"{message}: not proved positive: {value}")

def subset_weight(mask: int, weights: Sequence) -> object:
    return sum((weights[i] for i in range(N) if mask & 1 << i), 0)

def feasible_e_masks(q: Sequence, scenarios: Sequence[Sequence]) -> tuple[int, ...]:
    budgets = tuple((sum((k[i] * q[i] for i in range(N))) for k in scenarios))
    return tuple((mask for mask in SUBSETS if all((subset_weight(mask, k) <= budget for k, budget in zip(scenarios, budgets)))))

def fractional_load(q: Sequence, d: Sequence) -> dict[Arc, object]:
    load = {arc: 0 for arc in ARCS}
    for i, terminal in enumerate(TERMINALS):
        for arc in PATHS[terminal]['C']:
            load[arc] += d[i] * (1 - q[i])
        for arc in PATHS[terminal]['E']:
            load[arc] += d[i] * q[i]
    return load

def routing_load(e_mask: int, d: Sequence) -> dict[Arc, object]:
    load = {arc: 0 for arc in ARCS}
    for i, terminal in enumerate(TERMINALS):
        choice = 'E' if e_mask & 1 << i else 'C'
        for arc in PATHS[terminal][choice]:
            load[arc] += d[i]
    return load

def route_deviations(e_mask: int, q: Sequence, d: Sequence) -> tuple[object, ...]:
    x = fractional_load(q, d)
    y = routing_load(e_mask, d)
    return tuple((sp.simplify(y[arc] - x[arc]) for arc in ARCS))

def exact_max(values: Iterable[object]) -> object:
    values = tuple((sp.simplify(value) for value in values))
    candidate = max(values, key=lambda value: float(sp.N(value, 60)))
    for value in values:
        difference = sp.simplify(candidate - value)
        require(difference.is_nonnegative is True or difference == 0, (candidate, value, difference))
    return sp.simplify(candidate)

def route_value(e_mask: int, q: Sequence, d: Sequence) -> object:
    return exact_max(route_deviations(e_mask, q, d))

def instance_value(q: Sequence, d: Sequence, scenarios: Sequence[Sequence]) -> object:
    return exact_max((-route_value(mask, q, d) for mask in feasible_e_masks(q, scenarios))) * -1

def support_formula_deviations(e_mask: int, q: Sequence, d: Sequence) -> tuple[object, ...]:
    h = tuple((d[i] * q[i] for i in range(N)))
    ell = tuple((d[i] * (1 - q[i]) for i in range(N)))
    trunk = tuple((sum((-ell[i] if e_mask & 1 << i else h[i] for i in range(N) if arc_index in SUPPORTS[i])) for arc_index in range(5)))
    private = tuple((ell[i] if e_mask & 1 << i else h[i] for i in range(N)))
    return tuple((sp.simplify(value) for value in trunk + private))

def check_orientation_crosscheck() -> None:
    anchors = (((Q(1, 4), Q(1, 2), Q(3, 4), Q(2, 3)), (Q(1), Q(3, 4), Q(2, 5), Q(1))), ((Q(0), Q(2, 5), Q(1), Q(1, 3)), (Q(4, 5), Q(1), Q(2, 3), Q(1, 2))))
    for q, d in anchors:
        for mask in SUBSETS:
            graph = route_deviations(mask, q, d)
            support = support_formula_deviations(mask, q, d)
            require(graph[:5] == support[:5], 'assertion from source line 157')
            require(exact_max(graph[5:]) == exact_max(support[5:]), 'assertion from source line 160')
            require(exact_max(graph) == exact_max(support), 'assertion from source line 161')

def check_three_scenario_sequence() -> None:
    for n in (4, 5, 10, 100):
        q = (Q(n - 1, n),) * 4
        d = (Q(1),) * 4
        scenarios = tuple((tuple((Q(3 * n) if i == heavy else Q(1) for i in range(N))) for heavy in range(3)))
        require(feasible_e_masks(q, scenarios) == (0, 1 << 3), 'assertion from source line 172')
        require(route_value(0, q, d) == Q(4 * (n - 1), n), 'assertion from source line 173')
        require(route_value(1 << 3, q, d) == Q(3 * (n - 1), n), 'assertion from source line 174')
        require(instance_value(q, d, scenarios) == Q(3 * (n - 1), n), 'assertion from source line 175')
    require(Q(9, 4) > Q(17, 8), 'assertion from source line 176')

def check_four_scenario_sequence() -> None:
    for n in (2, 4, 10, 100):
        q = (Q(n - 1, n),) * 4
        d = (Q(1),) * 4
        scenarios = tuple((tuple((Q(3 * n) if i == heavy else Q(1) for i in range(N))) for heavy in range(4)))
        require(feasible_e_masks(q, scenarios) == (0,), 'assertion from source line 187')
        require(route_value(0, q, d) == Q(4 * (n - 1), n), 'assertion from source line 188')
        require(instance_value(q, d, scenarios) == Q(4 * (n - 1), n), 'assertion from source line 189')

def bounded_tail_parameters(kappa: Q, epsilon: Q):
    require(kappa > 2 and epsilon > 0, 'assertion from source line 193')
    q_u = kappa * (kappa - 2) / (kappa * kappa - 1)
    s_star = kappa * (2 * kappa - 1) / (kappa * kappa - 1)
    require(epsilon < s_star - 1, 'assertion from source line 196')
    s = s_star - epsilon
    delta = (1 + s) / 4
    q = (delta, q_u, (s - 1) / 2, delta)
    d = (Q(1), Q(1), delta, Q(1))
    scenarios = ((Q(1), kappa, Q(1), Q(1)), (kappa, Q(1), kappa, kappa))
    value = q_u + (1 + s) * (1 + s) / 8
    return (q, d, scenarios, value, s_star, delta)

def check_bounded_tail_rational_anchors() -> None:
    anchors = ((Q(5), Q(1, 100)), (Q(22), Q(1, 1000)), (Q(30), Q(1, 2000)), (Q(100), Q(1, 5000)))
    for kappa, epsilon in anchors:
        q, d, scenarios, expected, s_star, delta = bounded_tail_parameters(kappa, epsilon)
        require(all((Q(0) < value < Q(1) for value in q)), 'assertion from source line 218')
        require(max(d) == 1 and all((Q(0) < value <= Q(1) for value in d)), 'assertion from source line 219')
        for scenario in scenarios:
            require(max(scenario) / min(scenario) == kappa, 'assertion from source line 221')
        budget_1 = sum((scenarios[0][i] * q[i] for i in range(N)))
        budget_2 = sum((scenarios[1][i] * q[i] for i in range(N)))
        require(budget_1 == kappa - epsilon, 'assertion from source line 224')
        require(budget_2 == 2 * kappa - kappa * epsilon, 'assertion from source line 225')
        require(feasible_e_masks(q, scenarios) == (0, 1, 4, 8), 'assertion from source line 226')
        require(route_value(1, q, d) == expected, 'assertion from source line 227')
        require(route_value(4, q, d) == expected, 'assertion from source line 228')
        require(route_value(8, q, d) == expected, 'assertion from source line 229')
        require(route_value(0, q, d) == expected + delta, 'assertion from source line 230')
        require(instance_value(q, d, scenarios) == expected, 'assertion from source line 231')
        limiting = q[1] + (1 + s_star) ** 2 / 8
        require(sp.simplify(expected - (limiting - (1 + s_star) * epsilon / 4 + epsilon ** 2 / 8)) == 0, 'assertion from source line 233')

def check_symbolic_tail_algebra() -> None:
    k = sp.symbols('k', positive=True)
    q = k * (k - 2) / (k ** 2 - 1)
    s = k * (2 * k - 1) / (k ** 2 - 1)
    formula = sp.factor(q + (1 + s) ** 2 / 8)
    expected = (17 * k ** 4 - 22 * k ** 3 - 13 * k ** 2 + 18 * k + 1) / (8 * (k - 1) ** 2 * (k + 1) ** 2)
    require(sp.simplify(formula - expected) == 0, 'assertion from source line 246')
    threshold = sp.Poly(k ** 4 - 22 * k ** 3 + 19 * k ** 2 + 18 * k - 15, k)
    require(sp.factor(formula - 2) == threshold.as_expr() / (8 * (k - 1) ** 2 * (k + 1) ** 2), 'assertion from source line 248')
    require(threshold.count_roots(2, sp.oo) == 1, 'assertion from source line 251')
    lower = sp.Rational(210587809228982, 10 ** 13)
    upper = sp.Rational(210587809228983, 10 ** 13)
    require(threshold.count_roots(lower, upper) == 1, 'assertion from source line 254')
    require(threshold.count_roots(upper, sp.oo) == 0, 'assertion from source line 255')
    derivative = sp.factor(sp.diff(formula, k))
    expected_derivative = (11 * k ** 4 - 21 * k ** 3 + 6 * k ** 2 + 11 * k - 9) / (4 * (k - 1) ** 3 * (k + 1) ** 3)
    require(sp.simplify(derivative - expected_derivative) == 0, 'assertion from source line 260')
    require(sp.simplify(formula.subs(k, 2) - sp.Rational(9, 8)) == 0, 'assertion from source line 261')
    require(sp.limit(formula, k, sp.oo) == sp.Rational(17, 8), 'assertion from source line 262')

def feasible_c_family(weights: Sequence, threshold: object) -> tuple[int, ...]:
    return tuple((mask for mask in SUBSETS if subset_weight(mask, weights) >= threshold))

def c_route_value(c_mask: int, p: Sequence, d: Sequence) -> object:
    q = tuple((1 - value for value in p))
    return route_value(FULL_MASK ^ c_mask, q, d)

def check_f064_algebraic_sequence() -> None:
    root2 = sp.sqrt(2)
    delta = sp.Rational(1, 100)
    weights = (sp.Integer(1), sp.Integer(2), sp.Integer(1), sp.Integer(1))
    p = (1 / root2 + delta, (root2 - 1) / 2, 2 - root2, 1 - 1 / root2)
    d = (sp.Integer(1), sp.Integer(1), 1 / root2, sp.Integer(1))
    threshold = sp.simplify(sum((weights[i] * p[i] for i in range(N))))
    require(threshold == 2 + delta, 'assertion from source line 286')
    target_family = (3, 6, 7, 10, 11, 13, 14, 15)
    require(feasible_c_family(weights, threshold) == target_family, 'assertion from source line 288')
    c = sp.Rational(5, 2) - root2
    expected = {3: c - delta, 6: c, 7: sp.Rational(7, 2) - 3 * root2 / 2 - delta, 10: c, 11: sp.Rational(7, 2) - 3 * root2 / 2 - delta, 13: c - delta, 14: sp.Rational(5, 2) - root2 / 2, 15: sp.Rational(7, 2) - root2 - delta}
    for mask, value in expected.items():
        require(sp.simplify(c_route_value(mask, p, d) - value) == 0, 'assertion from source line 301')
    require(exact_max((-value for value in expected.values())) * -1 == c - delta, 'assertion from source line 302')

def check_numerical_scout_integrity() -> None:
    path = HERE / 'one_scenario_numerical_scout.json'
    if not path.exists():
        raise FileNotFoundError(f'missing numerical artifact: {path}')
    payload = json.loads(path.read_text(encoding='utf-8'))
    results = payload['results']
    values = [row['best']['value'] for row in results]
    require(len(results) == payload['frontier_cells'] == 79, 'assertion from source line 312')
    require(abs(max(values) - payload['maximum_scout_value']) < 1e-15, 'assertion from source line 313')
    require(payload['cells_above_9_over_8_by_more_than_1e_6'] == [], 'assertion from source line 314')
    require(sum((value > 1.1249 for value in values)) == 21, 'assertion from source line 315')
    require(sum((value > 1.000001 for value in values)) == 24, 'assertion from source line 316')
    require(sum((value > 1.12 for value in values)) == 23, 'assertion from source line 317')
    require(sum((not row['best']['success'] for row in results)) == 7, 'assertion from source line 318')
    f064 = next((row for row in results if row['family_id'] == 'F064'))
    require(abs(f064['best']['value'] - float(sp.Rational(5, 2) - sp.sqrt(2))) < 1e-08, 'assertion from source line 320')


def check_no_assert_statements() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    assert_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    require(len(assert_nodes) == 0, f"verifier contains {len(assert_nodes)} removable assert statements")


def check_equation10_scope_counterexample() -> None:
    kappa = Q(21, 10)
    q = (Q(3, 10), Q(1, 20), Q(9, 50), Q(1, 2))
    d = (Q(2, 5), Q(4, 25), Q(2, 5), Q(1))
    scenarios = (
        (Q(1), kappa, Q(1), Q(1)),
        (kappa, Q(1), kappa, kappa),
    )
    require(feasible_e_masks(q, scenarios) == (0, 1, 4, 8), "scope counterexample has wrong feasible family")
    expected_values = (Q(7, 10), Q(29, 50), Q(1, 2), Q(1, 2))
    actual_values = tuple(route_value(mask, q, d) for mask in (0, 1, 4, 8))
    require(actual_values == expected_values, f"scope counterexample route table changed: {actual_values}")
    h_total = sum(q[i] * d[i] for i in range(N))
    t = instance_value(q, d, scenarios)
    delta = h_total - t
    rhs = q[1] + min(q[0], delta) + min(q[3], delta) + delta * q[2]
    require_equal(h_total, Q(7, 10), "scope counterexample H")
    require_equal(t, Q(1, 2), "scope counterexample t")
    require_equal(delta, Q(1, 5), "scope counterexample Delta")
    require_equal(rhs, Q(243, 500), "scope counterexample equation (10) RHS")
    require_equal(h_total - rhs, Q(107, 500), "scope counterexample gap")
    require(t <= 2, "scope counterexample should lie in the already-settled t<=2 branch")


def polynomial_coefficient_certificate(expr: object, variables: tuple[sp.Symbol, ...], message: str) -> None:
    rational = sp.cancel(sp.together(expr))
    numerator, denominator = sp.fraction(rational)
    p_num = sp.Poly(sp.expand(numerator), *variables)
    p_den = sp.Poly(sp.expand(denominator), *variables)
    if p_den.LC().is_negative is True:
        p_num = -p_num
        p_den = -p_den
    for coefficient in p_num.coeffs():
        require_nonnegative(coefficient, f"{message} numerator coefficient")
    for coefficient in p_den.coeffs():
        require_nonnegative(coefficient, f"{message} denominator coefficient")
    origin = p_den.eval({variable: 0 for variable in variables})
    require_positive(origin, f"{message} denominator at origin")


def check_symbolic_tail_positivity() -> None:
    k = sp.symbols("k", positive=True)
    q = k * (k - 2) / (k**2 - 1)
    s_star = k * (2 * k - 1) / (k**2 - 1)
    formula = sp.factor(q + (1 + s_star) ** 2 / 8)
    derivative_numerator = 11 * k**4 - 21 * k**3 + 6 * k**2 + 11 * k - 9
    expected_derivative = derivative_numerator / (4 * (k - 1) ** 3 * (k + 1) ** 3)
    require_equal(sp.factor(sp.diff(formula, k)), expected_derivative, "derivative formula")
    x = sp.symbols("x", nonnegative=True)
    shifted = sp.Poly(sp.expand(derivative_numerator.subs(k, x + 2)), x)
    require(shifted.all_coeffs() == [11, 67, 144, 135, 45], "unexpected shifted derivative numerator")
    require(all(coefficient > 0 for coefficient in shifted.all_coeffs()), "derivative positivity certificate failed")


def check_symbolic_bounded_construction_full_range() -> None:
    # Parameterization of every kappa>2 and 0<epsilon<S_kappa-1:
    # kappa=2+a and epsilon=(S_kappa-1)/(1+b), with a,b>0.
    a, b = sp.symbols("a b", nonnegative=True)
    kappa = 2 + a
    q_u = kappa * (kappa - 2) / (kappa**2 - 1)
    s_star = kappa * (2 * kappa - 1) / (kappa**2 - 1)
    epsilon_max = s_star - 1
    epsilon = epsilon_max / (1 + b)
    s_value = s_star - epsilon
    delta = (1 + s_value) / 4
    q = (delta, q_u, (s_value - 1) / 2, delta)
    d = (sp.Integer(1), sp.Integer(1), delta, sp.Integer(1))
    scenario_1 = (sp.Integer(1), kappa, sp.Integer(1), sp.Integer(1))
    scenario_2 = (kappa, sp.Integer(1), kappa, kappa)
    budget_1 = sum(scenario_1[i] * q[i] for i in range(N))
    budget_2 = sum(scenario_2[i] * q[i] for i in range(N))
    require_equal(budget_1, kappa - epsilon, "full-range scenario 1 budget")
    require_equal(budget_2, 2 * kappa - kappa * epsilon, "full-range scenario 2 budget")

    expressions = {
        "q_u": q_u,
        "1-q_u": 1 - q_u,
        "q_3": q[2],
        "1-q_3": 1 - q[2],
        "delta": delta,
        "1-delta": 1 - delta,
        "scenario1 singleton slack": budget_1 - 1,
        "scenario1 heavy block": kappa - budget_1,
        "scenario2 singleton slack": budget_2 - kappa,
        "scenario2 pair block": 2 * kappa - budget_2,
    }
    for name, expression in expressions.items():
        polynomial_coefficient_certificate(expression, (a, b), name)
        require(sp.simplify(expression) != 0, f"{name} vanished identically")

    value = sp.factor(q_u + (1 + s_value) ** 2 / 8)
    route_targets = {0: value + delta, 1: value, 4: value, 8: value}
    equality_arcs = {0: 2, 1: 3, 4: 2, 8: 1}
    for mask, target in route_targets.items():
        deviations = route_deviations(mask, q, d)
        require_equal(deviations[equality_arcs[mask]], target, f"full-range route {mask} equality arc")
        for arc_index, deviation in enumerate(deviations):
            polynomial_coefficient_certificate(
                target - deviation,
                (a, b),
                f"full-range route {mask}, arc {arc_index}",
            )

    limiting = sp.factor(q_u + (1 + s_star) ** 2 / 8)
    require_equal(
        value,
        limiting - (1 + s_star) * epsilon / 4 + epsilon**2 / 8,
        "full-range convergence identity",
    )


def c_route_deviations(c_mask: int, p: Sequence, d: Sequence) -> tuple[object, ...]:
    q = tuple(1 - value for value in p)
    return route_deviations(FULL_MASK ^ c_mask, q, d)


def check_f064_full_delta_interval() -> None:
    root2 = sp.sqrt(2)
    delta = sp.symbols("delta", real=True)
    delta_max = 1 - 1 / root2
    require_positive(delta_max, "F064 delta upper bound")
    weights = (sp.Integer(1), sp.Integer(2), sp.Integer(1), sp.Integer(1))
    p = (
        1 / root2 + delta,
        (root2 - 1) / 2,
        2 - root2,
        1 - 1 / root2,
    )
    d = (sp.Integer(1), sp.Integer(1), 1 / root2, sp.Integer(1))
    threshold = sp.simplify(sum(weights[i] * p[i] for i in range(N)))
    require_equal(threshold, 2 + delta, "F064 threshold")
    target_family = (3, 6, 7, 10, 11, 13, 14, 15)
    integer_weight_family = tuple(mask for mask in SUBSETS if subset_weight(mask, weights) >= 3)
    require(integer_weight_family == target_family, "F064 integer-weight family changed")

    c = sp.Rational(5, 2) - root2
    expected = {
        3: c - delta,
        6: c,
        7: sp.Rational(7, 2) - 3 * root2 / 2 - delta,
        10: c,
        11: sp.Rational(7, 2) - 3 * root2 / 2 - delta,
        13: c - delta,
        14: sp.Rational(5, 2) - root2 / 2,
        15: sp.Rational(7, 2) - root2 - delta,
    }
    for mask, target in expected.items():
        deviations = c_route_deviations(mask, p, d)
        equality_found = False
        for arc_index, deviation in enumerate(deviations):
            difference = sp.expand(target - deviation)
            require(sp.Poly(difference, delta).degree() <= 1, f"F064 route {mask}, arc {arc_index} is not affine")
            require_nonnegative(difference.subs(delta, 0), f"F064 route {mask}, arc {arc_index} at delta=0")
            require_nonnegative(
                difference.subs(delta, delta_max),
                f"F064 route {mask}, arc {arc_index} at delta upper endpoint",
            )
            if sp.simplify(difference) == 0:
                equality_found = True
        require(equality_found, f"F064 route {mask} has no arc attaining the claimed maximum")

    finite_value = c - delta
    for mask, target in expected.items():
        difference = sp.expand(target - finite_value)
        require_nonnegative(difference.subs(delta, 0), f"F064 minimum comparison {mask} at delta=0")
        require_nonnegative(
            difference.subs(delta, delta_max),
            f"F064 minimum comparison {mask} at delta upper endpoint",
        )
    require_equal(expected[3], finite_value, "F064 attaining route 12")
    require_equal(expected[13], finite_value, "F064 attaining route 134")


def parse_terminal_set(label: str) -> int:
    mask = 0
    for character in label:
        terminal = int(character)
        require(1 <= terminal <= 4, f"invalid terminal label {label!r}")
        mask |= 1 << (terminal - 1)
    return mask


def upward_family(minimal_sets: Sequence[str]) -> tuple[int, ...]:
    minima = tuple(parse_terminal_set(label) for label in minimal_sets)
    return tuple(mask for mask in SUBSETS if any(mask & minimum == minimum for minimum in minima))


def scout_subset_weight(mask: int, weights: Sequence[float]) -> float:
    return float(sum(weights[i] for i in range(N) if mask & (1 << i)))


def scout_route_value(c_mask: int, p: Sequence[float], d: Sequence[float]) -> float:
    e = [d[i] * (1 - p[i]) for i in range(N)]
    ell = [d[i] * p[i] for i in range(N)]
    trunk = [
        sum(
            e[i] if c_mask & (1 << i) else -ell[i]
            for i in range(N)
            if arc in SUPPORTS[i]
        )
        for arc in range(5)
    ]
    private = [e[i] if c_mask & (1 << i) else ell[i] for i in range(N)]
    return float(max(trunk + private))


def scout_objective(family: Sequence[int], p: Sequence[float], d: Sequence[float]) -> float:
    return min(scout_route_value(mask, p, d) for mask in family)


def check_numerical_scout_audit() -> None:
    path = SOURCE / "one_scenario_numerical_scout.json"
    require(path.exists(), f"missing numerical artifact: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = payload["results"]
    require(len(results) == payload["frontier_cells"] == 79, "numerical artifact cell count")
    values = [row["best"]["value"] for row in results]
    require(abs(max(values) - payload["maximum_scout_value"]) < 1e-15, "numerical maximum summary mismatch")
    require(payload["cells_above_9_over_8_by_more_than_1e_6"] == [], "unexpected scout value above 9/8 tolerance")
    require(sum(value > 1.1249 for value in values) == 21, "high cluster count mismatch")
    require(sum(value > 1.000001 for value in values) == 24, "nontrivial cell count mismatch")
    require(sum(value > 1.12 for value in values) == 23, ">1.12 count mismatch")
    require(sum(not row["best"]["success"] for row in results) == 7, "solver non-success count mismatch")

    margin = float(payload["requested_strict_losing_margin"])
    negative_constraint_count = 0
    literal_family_mismatch_ids: list[str] = []
    high_cluster_mismatch_count = 0
    max_objective_error = 0.0
    max_constraint_error = 0.0
    for row in results:
        best = row["best"]
        k = best["k"]
        p_values = best["p"]
        d_values = best["d"]
        family = upward_family(row["minimal_feasible_sets"])
        losing = tuple(mask for mask in SUBSETS if mask not in family)
        tau = float(sum(k[i] * p_values[i] for i in range(N)))
        constraints = [scout_subset_weight(mask, k) - tau for mask in family]
        constraints.extend(tau - scout_subset_weight(mask, k) - margin for mask in losing)
        recomputed_constraint = min(constraints)
        recomputed_objective = scout_objective(family, p_values, d_values)
        max_objective_error = max(max_objective_error, abs(recomputed_objective - best["value"]))
        max_constraint_error = max(max_constraint_error, abs(recomputed_constraint - best["minimum_constraint"]))
        if best["minimum_constraint"] < 0:
            negative_constraint_count += 1
        induced = tuple(mask for mask in SUBSETS if scout_subset_weight(mask, k) >= tau)
        if induced != family:
            literal_family_mismatch_ids.append(row["family_id"])
            if best["value"] > 1.1249:
                high_cluster_mismatch_count += 1
        require(best["minimum_constraint"] >= -2e-7, f"stored candidate outside generator acceptance tolerance: {row['family_id']}")

    require(max_objective_error <= 5e-15, f"stored objective recomputation error {max_objective_error}")
    require(max_constraint_error <= 5e-15, f"stored constraint recomputation error {max_constraint_error}")
    require(negative_constraint_count == 68, f"negative minimum_constraint count {negative_constraint_count}")
    expected_mismatches = [
        "F050", "F053", "F055", "F060", "F065", "F067", "F070", "F073", "F087", "F088",
        "F090", "F095", "F100", "F103", "F108", "F117", "F120", "F138", "F141",
    ]
    require(literal_family_mismatch_ids == expected_mismatches, f"literal family mismatch IDs changed: {literal_family_mismatch_ids}")
    require(high_cluster_mismatch_count == 6, f"high-cluster mismatch count {high_cluster_mismatch_count}")
    f064 = next(row for row in results if row["family_id"] == "F064")
    require(abs(f064["best"]["value"] - float(sp.Rational(5, 2) - sp.sqrt(2))) < 1e-8, "F064 numerical target mismatch")

def main() -> None:
    check_no_assert_statements()
    print("PASS: verifier contains no optimization-removable assert statements")
    check_orientation_crosscheck()
    print("PASS: graph-native and independent support-formula orientations agree")
    check_three_scenario_sequence()
    print("PASS: exact three-scenario route table; n=4 gives 9/4 > 17/8")
    check_four_scenario_sequence()
    print("PASS: exact four-scenario only-all-C sequence tends to 4")
    check_equation10_scope_counterexample()
    print("PASS: exact equation-(10) scope counterexample; the t>2 guard is necessary")
    check_bounded_tail_rational_anchors()
    print("PASS: bounded-tail exact rational anchor route tables")
    check_symbolic_tail_algebra()
    check_symbolic_tail_positivity()
    print("PASS: symbolic F(kappa), derivative positivity, root isolation, and 17/8 limit")
    check_symbolic_bounded_construction_full_range()
    print("PASS: bounded lower family and all 13-arc route maxima over the full parameter range")
    check_f064_full_delta_interval()
    print("PASS: exact F064 family and route maxima over the full stated delta interval")
    check_numerical_scout_audit()
    print("PASS: all scout objectives recompute; 68 negative constraints and 19 literal family mismatches are recorded limitations")


if __name__ == "__main__":
    main()
