#!/usr/bin/env python3
"""Separate clean-room checks for the four-terminal SSUF v0.1.0 release.

This audit intentionally does not import any module from the supplied bundle.
It uses NetworkX to discover graph properties and paths, exact Fraction
arithmetic for the finite certificate, SymPy for a separately encoded symbolic
check, and deterministic randomized stress tests for the restricted model.
It is computational corroboration, not independent human review, and the
randomized checks are not a proof.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import math
import random

import networkx as nx
import sympy as sp


SOURCE = "s"
VERTICES = ("s", "v1", "v2", "v3", "v4", "v5", "t1", "t2", "t3", "t4")
TERMINALS = ("t1", "t2", "t3", "t4")
TRUNK = (
    ("s", "v1"),
    ("v1", "v2"),
    ("v2", "v3"),
    ("v3", "v4"),
    ("v4", "v5"),
)
ARCS = TRUNK + (
    ("s", "t1"),
    ("v3", "t1"),
    ("s", "t2"),
    ("v5", "t2"),
    ("v1", "t3"),
    ("v5", "t3"),
    ("v2", "t4"),
    ("v4", "t4"),
)
CHARGED = {
    "t1": ("s", "t1"),
    "t2": ("s", "t2"),
    "t3": ("v1", "t3"),
    "t4": ("v2", "t4"),
}


def arc_path(vertices: list[str]) -> tuple[tuple[str, str], ...]:
    return tuple(zip(vertices[:-1], vertices[1:], strict=True))


def discover_paths(graph: nx.DiGraph) -> dict[str, dict[str, tuple[tuple[str, str], ...]]]:
    result: dict[str, dict[str, tuple[tuple[str, str], ...]]] = {}
    for terminal in TERMINALS:
        vertex_paths = list(nx.all_simple_paths(graph, SOURCE, terminal))
        assert len(vertex_paths) == 2, (terminal, vertex_paths)
        paths = [arc_path(path) for path in vertex_paths]
        expensive = [path for path in paths if CHARGED[terminal] in path]
        cheap = [path for path in paths if CHARGED[terminal] not in path]
        assert len(expensive) == len(cheap) == 1
        result[terminal] = {"E": expensive[0], "C": cheap[0]}
    return result


def loads_for_amounts(
    paths: dict[str, dict[str, tuple[tuple[str, str], ...]]],
    amounts: dict[tuple[str, str], Fraction],
) -> dict[tuple[str, str], Fraction]:
    loads = {arc: Fraction(0) for arc in ARCS}
    for (terminal, choice), amount in amounts.items():
        for arc in paths[terminal][choice]:
            loads[arc] += amount
    return loads


def finite_certificate(paths: dict[str, dict[str, tuple[tuple[str, str], ...]]]) -> None:
    demands = {"t1": 294, "t2": 216, "t3": 252, "t4": 294}
    cheap = {"t1": 78, "t2": 97, "t3": 36, "t4": 42}
    cost = {arc: 0 for arc in ARCS}
    cost.update(
        {
            ("s", "t1"): 36,
            ("s", "t2"): 49,
            ("v1", "t3"): 42,
            ("v2", "t4"): 36,
        }
    )

    fractional_amounts: dict[tuple[str, str], Fraction] = {}
    for terminal in TERMINALS:
        fractional_amounts[(terminal, "C")] = Fraction(cheap[terminal])
        fractional_amounts[(terminal, "E")] = Fraction(demands[terminal] - cheap[terminal])
    x = loads_for_amounts(paths, fractional_amounts)
    x_cost = sum(Fraction(cost[arc]) * x[arc] for arc in ARCS)
    assert x_cost == 31_751
    assert tuple(x[arc] for arc in TRUNK) == (721, 505, 253, 175, 133)

    rows: list[tuple[str, int, int, tuple[str, str]]] = []
    for choices in product(("E", "C"), repeat=4):
        amounts = {
            (terminal, choice): Fraction(demands[terminal])
            for terminal, choice in zip(TERMINALS, choices, strict=True)
        }
        y = loads_for_amounts(paths, amounts)
        route_cost = sum(Fraction(cost[arc]) * y[arc] for arc in ARCS)
        delta = {arc: y[arc] - x[arc] for arc in ARCS}
        witness = max(ARCS, key=lambda arc: delta[arc])
        rows.append(("".join(choices), int(route_cost), int(delta[witness]), witness))

    feasible = [row for row in rows if row[1] <= x_cost]
    assert len(feasible) == 11
    assert min(row[2] for row in feasible) == 335
    assert sorted(row[0] for row in feasible if row[2] == 335) == [
        "CCEE",
        "CECE",
        "CEEC",
        "ECCE",
        "ECEC",
    ]
    assert Fraction(335, 294) > Fraction(9, 8)


def symbolic_family(paths: dict[str, dict[str, tuple[tuple[str, str], ...]]]) -> None:
    supports: dict[int, frozenset[int]] = {}
    for i, terminal in enumerate(TERMINALS, start=1):
        cheap_arcs = set(paths[terminal]["C"])
        expensive_arcs = set(paths[terminal]["E"])
        supports[i] = frozenset(
            index
            for index, arc in enumerate(TRUNK, start=1)
            if int(arc in cheap_arcs) - int(arc in expensive_arcs) == 1
        )
    assert supports == {
        1: frozenset({1, 2, 3}),
        2: frozenset({1, 2, 3, 4, 5}),
        3: frozenset({2, 3, 4, 5}),
        4: frozenset({3, 4}),
    }

    q, epsilon = sp.symbols("q epsilon", positive=True)
    demands = (sp.Integer(1), q**2, q, sp.Integer(1))
    cheap_fractions = (
        1 - q**2,
        q**2 + 2 * q - 2 + epsilon,
        1 - q,
        1 - q,
    )
    assert sp.simplify(sum(cheap_fractions) - (1 + epsilon)) == 0

    def deviation(cheap_set: frozenset[int], trunk_index: int) -> sp.Expr:
        value = sp.Integer(0)
        for i in range(1, 5):
            if trunk_index not in supports[i]:
                continue
            d = demands[i - 1]
            p = cheap_fractions[i - 1]
            value += d * (1 - p) if i in cheap_set else -d * p
        return sp.factor(value)

    target = q**2 * (4 - q**2 - 2 * q - epsilon)
    witnesses = {
        frozenset({1, 2}): 1,
        frozenset({1, 3}): 2,
        frozenset({1, 4}): 3,
        frozenset({2, 3}): 5,
        frozenset({2, 4}): 4,
        frozenset({3, 4}): 4,
    }
    for cheap_set, trunk_index in witnesses.items():
        expected = target
        if cheap_set == frozenset({3, 4}):
            expected += q - q**2
        assert sp.simplify(deviation(cheap_set, trunk_index) - expected) == 0

    limiting = sp.expand(target.subs(epsilon, 0))
    q_star = (sp.sqrt(41) - 3) / 4
    radical = (299 - 41 * sp.sqrt(41)) / 32
    assert sp.simplify(sp.diff(limiting, q).subs(q, q_star)) == 0
    assert sp.simplify(limiting.subs(q, q_star) - radical) == 0


def objective(
    paths: dict[str, dict[str, tuple[tuple[str, str], ...]]],
    demands: tuple[float, float, float, float],
    cheap_fractions: tuple[float, float, float, float],
) -> float:
    x = {arc: 0.0 for arc in ARCS}
    for terminal, demand, fraction in zip(
        TERMINALS, demands, cheap_fractions, strict=True
    ):
        for arc in paths[terminal]["C"]:
            x[arc] += demand * fraction
        for arc in paths[terminal]["E"]:
            x[arc] += demand * (1 - fraction)
    best = math.inf
    for choices in product(("E", "C"), repeat=4):
        if choices.count("C") < 2:
            continue
        y = {arc: 0.0 for arc in ARCS}
        for terminal, choice, demand in zip(
            TERMINALS, choices, demands, strict=True
        ):
            for arc in paths[terminal][choice]:
                y[arc] += demand
        worst = max(y[arc] - x[arc] for arc in ARCS)
        best = min(best, worst)
    return best


def restricted_model_stress(
    paths: dict[str, dict[str, tuple[tuple[str, str], ...]]]
) -> None:
    radical = (299 - 41 * math.sqrt(41)) / 32
    q_star = (math.sqrt(41) - 3) / 4
    epsilon = 1e-9
    family_demands = (1.0, q_star**2, q_star, 1.0)
    family_p = (
        1 - q_star**2,
        q_star**2 + 2 * q_star - 2 + epsilon,
        1 - q_star,
        1 - q_star,
    )
    family_value = objective(paths, family_demands, family_p)
    assert abs(family_value - (radical - q_star**2 * epsilon)) < 5e-12

    rng = random.Random(20260723)
    observed = -math.inf
    for sample in range(200_000):
        if sample % 2:
            demands = (1.0, rng.random(), rng.random(), 1.0)
        else:
            raw = [0.02 + 0.98 * rng.random() for _ in range(4)]
            raw[rng.randrange(4)] = 1.0
            demands = tuple(raw)

        weights = [rng.expovariate(1.0) for _ in range(4)]
        boundary = [weight / sum(weights) for weight in weights]
        room = [1 - value for value in boundary]
        epsilon_sum = min(0.5 * rng.random(), sum(room))
        additions = [0.0] * 4
        remaining = epsilon_sum
        for index in rng.sample(range(4), 4):
            add = min(room[index], remaining * rng.random())
            additions[index] = add
            remaining -= add
        for index in range(4):
            if remaining <= 0:
                break
            add = min(room[index] - additions[index], remaining)
            additions[index] += add
            remaining -= add
        cheap_fractions = tuple(
            boundary[index] + additions[index] for index in range(4)
        )
        assert 1 - 1e-12 <= sum(cheap_fractions) <= 2 + 1e-12
        value = objective(paths, demands, cheap_fractions)
        observed = max(observed, value)
        assert value <= radical + 2e-12, (
            sample,
            demands,
            cheap_fractions,
            value,
            radical,
        )
    print(f"restricted stress maximum across 200000 samples: {observed:.12f}")
    print(f"limiting family check: {family_value:.12f} < {radical:.12f}")


def main() -> None:
    graph = nx.DiGraph()
    graph.add_nodes_from(VERTICES)
    graph.add_edges_from(ARCS)
    assert nx.is_directed_acyclic_graph(graph)
    assert nx.is_weakly_connected(graph)
    planar, _embedding = nx.check_planarity(graph.to_undirected(), counterexample=True)
    assert planar

    branch_sets = (
        {"s", "t1", "t2"},
        {"v1", "v2", "t3", "t4"},
        {"v3", "v4"},
        {"v5"},
    )
    undirected = graph.to_undirected()
    for branch in branch_sets:
        assert nx.is_connected(undirected.subgraph(branch))
    for i in range(4):
        for j in range(i + 1, 4):
            assert any(
                undirected.has_edge(u, v)
                for u in branch_sets[i]
                for v in branch_sets[j]
            )

    paths = discover_paths(graph)
    finite_certificate(paths)
    symbolic_family(paths)
    restricted_model_stress(paths)
    print("SEPARATE CLEAN-ROOM CROSS-CHECK PASS")


if __name__ == "__main__":
    main()
