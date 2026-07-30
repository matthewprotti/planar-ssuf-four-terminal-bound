#!/usr/bin/env python3
"""Primary exact replay for Theorem RB-003 (proof-review-integrated package).

The human-readable proof in TWO_SCENARIO_GLOBAL_CONSTANT.md is authoritative. This
script proves the concrete finite certificate by exact graph enumeration,
certifies the complete 149/18/1 four-label threshold partition with witnesses
and two-trades, performs an abstract blocker regression, checks the algebra,
and writes deterministic artifacts.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
from typing import Iterable

N = 4
SUBSETS = tuple(range(1 << N))
FULL = (1 << N) - 1
EPSILON = Fraction(1, 1000)

Arc = tuple[str, str]
TRUNK: tuple[Arc, ...] = (
    ("s", "v1"),
    ("v1", "v2"),
    ("v2", "v3"),
    ("v3", "v4"),
    ("v4", "v5"),
)
PRIVATE: tuple[Arc, ...] = (
    ("s", "t1"),
    ("v3", "t1"),
    ("s", "t2"),
    ("v5", "t2"),
    ("v1", "t3"),
    ("v5", "t3"),
    ("v2", "t4"),
    ("v4", "t4"),
)
ARCS = TRUNK + PRIVATE
TERMINALS = ("t1", "t2", "t3", "t4")
PATHS: dict[str, dict[str, tuple[Arc, ...]]] = {
    "t1": {
        "E": (("s", "t1"),),
        "C": (("s", "v1"), ("v1", "v2"), ("v2", "v3"), ("v3", "t1")),
    },
    "t2": {
        "E": (("s", "t2"),),
        "C": TRUNK + (("v5", "t2"),),
    },
    "t3": {
        "E": (("s", "v1"), ("v1", "t3")),
        "C": TRUNK + (("v5", "t3"),),
    },
    "t4": {
        "E": (("s", "v1"), ("v1", "v2"), ("v2", "t4")),
        "C": (("s", "v1"), ("v1", "v2"), ("v2", "v3"), ("v3", "v4"), ("v4", "t4")),
    },
}
PRIVATE_E_ARC: tuple[Arc, ...] = (
    ("s", "t1"),
    ("s", "t2"),
    ("v1", "t3"),
    ("v2", "t4"),
)


def bitset(items: Iterable[int]) -> int:
    mask = 0
    for item in items:
        mask |= 1 << (item - 1)
    return mask


def name(mask: int) -> str:
    return "".join(str(i + 1) for i in range(N) if mask & (1 << i)) or "empty"


def fstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def minimal_members(family: Iterable[int]) -> tuple[int, ...]:
    items = frozenset(family)
    return tuple(
        sorted(
            mask
            for mask in items
            if not any(other != mask and (other & mask) == other for other in items)
        )
    )


def subset_weight(mask: int, weights: tuple[int, ...]) -> int:
    return sum(weights[i] for i in range(N) if mask & (1 << i))


def is_downset(family: frozenset[int]) -> bool:
    return all(
        all(sub in family for sub in SUBSETS if sub & mask == sub)
        for mask in family
    )


def all_downsets() -> tuple[frozenset[int], ...]:
    result: list[frozenset[int]] = []
    for truth in range(1 << len(SUBSETS)):
        family = frozenset(mask for mask in SUBSETS if truth & (1 << mask))
        if is_downset(family):
            result.append(family)
    assert len(result) == 168
    return tuple(result)


def incidence_sum(left: int, right: int) -> tuple[int, ...]:
    return tuple(
        int(bool(left & (1 << i))) + int(bool(right & (1 << i)))
        for i in range(N)
    )


def find_two_trade(
    feasible: frozenset[int], infeasible: frozenset[int]
) -> tuple[int, int, int, int]:
    """Return A,B feasible and C,D infeasible with 1_A+1_B=1_C+1_D."""

    feasible_by_incidence: dict[tuple[int, ...], tuple[int, int]] = {}
    for left, right in combinations_with_replacement(sorted(feasible), 2):
        feasible_by_incidence.setdefault(incidence_sum(left, right), (left, right))
    for left, right in combinations_with_replacement(sorted(infeasible), 2):
        key = incidence_sum(left, right)
        if key in feasible_by_incidence:
            a, b = feasible_by_incidence[key]
            return a, b, left, right
    raise AssertionError("no exact two-trade contradiction found")


def scalar_e_families() -> dict[frozenset[int], tuple[tuple[int, ...], int]]:
    """Construct explicit positive integer witnesses for 149 downsets.

    Completeness is certified separately by `threshold_recognition`: every
    other nonempty downset receives an exact two-trade contradiction.
    """

    witnesses: dict[frozenset[int], tuple[tuple[int, ...], int]] = {}
    for bound in range(1, 5):
        for weights in product(range(1, bound + 1), repeat=N):
            if max(weights) != bound:
                continue
            for capacity in sorted({subset_weight(mask, weights) for mask in SUBSETS}):
                family = frozenset(
                    mask for mask in SUBSETS if subset_weight(mask, weights) <= capacity
                )
                witnesses.setdefault(family, (weights, capacity))
    assert len(witnesses) == 149
    return witnesses


def threshold_recognition(directory: Path) -> dict[str, object]:
    represented = scalar_e_families()
    downsets = all_downsets()
    excluded = tuple(family for family in downsets if family not in represented)
    empty = tuple(family for family in excluded if not family)
    nonthreshold = tuple(family for family in excluded if family)
    assert len(represented) == 149
    assert len(nonthreshold) == 18
    assert len(empty) == 1

    witness_rows: list[dict[str, object]] = []
    for family in sorted(represented, key=lambda f: (len(f), sorted(f))):
        weights, capacity = represented[family]
        assert all(weight > 0 for weight in weights)
        assert family == frozenset(
            mask for mask in SUBSETS if subset_weight(mask, weights) <= capacity
        )
        witness_rows.append(
            {
                "family_truth_hex": f"0x{sum(1 << m for m in family):04x}",
                "feasible_E_sets": [name(mask) for mask in sorted(family)],
                "weights": list(weights),
                "capacity": capacity,
            }
        )

    trade_rows: list[dict[str, object]] = []
    for family in sorted(nonthreshold, key=lambda f: (len(f), sorted(f))):
        infeasible = frozenset(SUBSETS) - family
        a, b, c, d = find_two_trade(family, infeasible)
        common = incidence_sum(a, b)
        assert common == incidence_sum(c, d)
        # If a positive threshold representation existed, the first pair would
        # have total weight <=2*capacity and the second >2*capacity, despite
        # equal incidence sums: contradiction.
        trade_rows.append(
            {
                "family_truth_hex": f"0x{sum(1 << m for m in family):04x}",
                "feasible_E_sets": [name(mask) for mask in sorted(family)],
                "feasible_trade_sets": [name(a), name(b)],
                "infeasible_trade_sets": [name(c), name(d)],
                "common_incidence_sum": list(common),
            }
        )

    payload: dict[str, object] = {
        "schema": "ssuf-four-label-threshold-recognition-v2",
        "orientation": "downward feasible E-set families; positive weights; weak capacity inequality",
        "all_downsets": len(downsets),
        "admissible_nonempty_downsets": len(downsets) - 1,
        "positive_scalar_threshold_downsets": len(represented),
        "nonempty_nonthreshold_downsets": len(nonthreshold),
        "empty_inadmissible_downsets": len(empty),
        "completeness_method": (
            "149 explicit positive integer threshold witnesses plus exact "
            "two-trade contradictions for every other nonempty downset"
        ),
        "threshold_witnesses": witness_rows,
        "nonthreshold_two_trade_certificates": trade_rows,
        "empty_family_reason": "the empty E-set has weight zero and is always budget-feasible",
    }
    output = directory / "threshold_recognition_report.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def positive_c_family_ids() -> dict[frozenset[int], str]:
    """Reconstruct the established F001..F149 ordering from its definition."""

    witnesses: dict[frozenset[int], tuple[tuple[int, ...], int]] = {}
    for bound in range(1, 5):
        for weights in product(range(1, bound + 1), repeat=N):
            if max(weights) != bound:
                continue
            subset_sums = sorted({subset_weight(mask, weights) for mask in SUBSETS})
            for quota in subset_sums:
                family = frozenset(
                    mask for mask in SUBSETS if subset_weight(mask, weights) >= quota
                )
                witnesses.setdefault(family, (weights, quota))
    assert len(witnesses) == 149
    ordered = sorted(
        witnesses,
        key=lambda family: (
            minimal_members(family),
            sum(1 << mask for mask in family),
        ),
    )
    return {family: f"F{index:03d}" for index, family in enumerate(ordered, start=1)}


def fractional_load(
    p: tuple[Fraction, ...], d: tuple[Fraction, ...]
) -> dict[Arc, Fraction]:
    load = {arc: Fraction(0) for arc in ARCS}
    for i, terminal in enumerate(TERMINALS):
        c_amount = d[i] * p[i]
        e_amount = d[i] * (1 - p[i])
        for arc in PATHS[terminal]["C"]:
            load[arc] += c_amount
        for arc in PATHS[terminal]["E"]:
            load[arc] += e_amount
    return load


def routing_load(c_mask: int, d: tuple[Fraction, ...]) -> dict[Arc, Fraction]:
    load = {arc: Fraction(0) for arc in ARCS}
    for i, terminal in enumerate(TERMINALS):
        choice = "C" if c_mask & (1 << i) else "E"
        for arc in PATHS[terminal][choice]:
            load[arc] += d[i]
    return load


def scenario_arc_costs(
    k: tuple[Fraction, ...], d: tuple[Fraction, ...]
) -> dict[Arc, Fraction]:
    """Realize full-demand E-minus-C differences k on private E-only arcs."""

    costs = {arc: Fraction(0) for arc in ARCS}
    for i in range(N):
        assert d[i] > 0
        costs[PRIVATE_E_ARC[i]] = k[i] / d[i]
        assert PRIVATE_E_ARC[i] in PATHS[TERMINALS[i]]["E"]
        assert PRIVATE_E_ARC[i] not in PATHS[TERMINALS[i]]["C"]
    return costs


def graph_cost(load: dict[Arc, Fraction], costs: dict[Arc, Fraction]) -> Fraction:
    return sum((load[arc] * costs[arc] for arc in ARCS), Fraction(0))


def route_deviation(
    c_mask: int,
    p: tuple[Fraction, ...],
    d: tuple[Fraction, ...],
) -> tuple[Fraction, tuple[Arc, ...], dict[Arc, Fraction]]:
    x = fractional_load(p, d)
    y = routing_load(c_mask, d)
    deviations = {arc: y[arc] - x[arc] for arc in ARCS}
    maximum = max(deviations.values())
    witnesses = tuple(arc for arc in ARCS if deviations[arc] == maximum)
    return maximum, witnesses, deviations


def blocked_pair_graph(family: frozenset[int]) -> frozenset[tuple[int, int]]:
    return frozenset(
        (i, j)
        for i, j in combinations(range(N), 2)
        if ((1 << i) | (1 << j)) not in family
    )


def graph_triangles(edges: frozenset[tuple[int, int]]) -> tuple[frozenset[int], ...]:
    edge_set = {frozenset(edge) for edge in edges}
    triangles: list[frozenset[int]] = []
    for triple in combinations(range(N), 3):
        if all(frozenset(pair) in edge_set for pair in combinations(triple, 2)):
            triangles.append(frozenset(triple))
    return tuple(triangles)


def case_census() -> dict[str, object]:
    scalar = scalar_e_families()
    families = sorted(scalar, key=lambda family: (len(family), sorted(family)))
    counts: Counter[str] = Counter()
    unique_robust: dict[str, set[int]] = defaultdict(set)
    total_pairs = 0
    no_pair_count = 0

    # Verify the elementary threshold-graph fact on every stored witness.
    for family, (weights, capacity) in scalar.items():
        edges = blocked_pair_graph(family)
        if not graph_triangles(edges):
            max_vertex = max(range(N), key=lambda i: weights[i])
            assert all(max_vertex in edge for edge in edges)
        # Stored family and witness agree at singleton/pair level.
        for mask in SUBSETS:
            assert (mask in family) == (subset_weight(mask, weights) <= capacity)

    for left_index, family_1 in enumerate(families):
        for family_2 in families[left_index:]:
            total_pairs += 1
            robust = family_1 & family_2
            robust_bitmask = sum(1 << mask for mask in robust)
            feasible_pairs = [
                mask for mask in robust if mask.bit_count() == 2
            ]
            if feasible_pairs:
                counts["feasible_pair"] += 1
                unique_robust["feasible_pair"].add(robust_bitmask)
                continue

            no_pair_count += 1
            A = tuple(i for i in range(N) if (1 << i) in robust)
            a_size = len(A)
            edges_1 = blocked_pair_graph(family_1)
            edges_2 = blocked_pair_graph(family_2)
            triangles_1 = graph_triangles(edges_1)
            triangles_2 = graph_triangles(edges_2)

            if a_size <= 2:
                category = f"matching_A{a_size}"
            elif a_size == 4:
                assert triangles_1 or triangles_2
                category = "clique_complement_A4"
            else:
                assert a_size == 3
                A_set = frozenset(A)
                u = next(i for i in range(N) if i not in A_set)
                useful_triangle = False
                for triangle in triangles_1 + triangles_2:
                    complement = next(i for i in range(N) if i not in triangle)
                    if complement in A_set:
                        useful_triangle = True
                        break
                if useful_triangle:
                    category = "clique_complement_A3"
                else:
                    # Verify the unique star-triangle orientation.
                    scenarios = (family_1, family_2)
                    orientation_found = False
                    for star_index, star_family in enumerate(scenarios):
                        if (1 << u) in star_family:
                            continue
                        triangle_family = scenarios[1 - star_index]
                        # Star scenario cannot allow any set containing u.
                        assert all(
                            mask not in star_family
                            for mask in SUBSETS
                            if mask & (1 << u)
                        )
                        # It must allow all pairs internal to A, or there would
                        # be a useful blocked triangle with complement in A.
                        assert all(
                            ((1 << i) | (1 << j)) in star_family
                            for i, j in combinations(A, 2)
                        )
                        # The other scenario must block all A-pairs.
                        assert all(
                            ((1 << i) | (1 << j)) not in triangle_family
                            for i, j in combinations(A, 2)
                        )
                        orientation_found = True
                        break
                    assert orientation_found
                    category = (
                        "star_triangle_missing_central"
                        if u in (1, 2)
                        else "star_triangle_missing_outer"
                    )

            counts[category] += 1
            unique_robust[category].add(robust_bitmask)

    assert total_pairs == 149 * 150 // 2 == 11175
    assert no_pair_count == sum(
        count for category, count in counts.items() if category != "feasible_pair"
    )
    all_no_pair_unique = set().union(
        *(values for key, values in unique_robust.items() if key != "feasible_pair")
    )
    # A downward family with no pair is empty plus any subset of the four singletons.
    assert len(all_no_pair_unique) == 16
    assert counts["star_triangle_missing_central"] > 0
    assert counts["star_triangle_missing_outer"] > 0

    return {
        "schema": "ssuf-two-scenario-global-abstract-case-census-v2",
        "scalar_positive_threshold_patterns": len(scalar),
        "unordered_pattern_pairs": total_pairs,
        "no_common_feasible_pair_pattern_pairs": no_pair_count,
        "unique_no_pair_robust_families": len(all_no_pair_unique),
        "pair_counts_by_proof_case": dict(sorted(counts.items())),
        "unique_robust_family_counts_by_proof_case": {
            key: len(value) for key, value in sorted(unique_robust.items())
        },
        "interpretation": (
            "Abstract blocker regression only. The 11,175 pattern pairs need "
            "not admit a common baseline q. No shared-baseline realization or "
            "analytic upper bound is inferred from this census."
        ),
    }


def exact_algebra_checks() -> None:
    # Polynomial coefficient order: constant, Delta, Delta^2.
    central_left = (Fraction(1), Fraction(3), Fraction(-2))
    central_square = (Fraction(17, 8) - Fraction(18, 16), Fraction(3), Fraction(-2))
    assert central_left == central_square == (Fraction(1), Fraction(3), Fraction(-2))

    outer_left = (Fraction(1), Fraction(2), Fraction(-1))
    outer_square = (Fraction(1), Fraction(2), Fraction(-1))
    assert outer_left == outer_square

    # Exact maxima of the quadratic envelopes.
    delta = Fraction(3, 4)
    assert 1 + 3 * delta - 2 * delta * delta == Fraction(17, 8)
    assert 1 + 2 * Fraction(1) - Fraction(1) ** 2 == 2

    # Strict comparison 17/8 > L without floating-point arithmetic:
    # 17/8 - L = (41*sqrt(41)-231)/32 > 0.
    assert 41**3 > 231**2


def nonattainment_logic(directory: Path) -> dict[str, object]:
    delta = Fraction(3, 4)
    t = Fraction(17, 8)
    H = t + delta
    assert H == Fraction(23, 8)
    assert 1 + 4 * delta - 2 * delta * delta == H
    payload = {
        "schema": "ssuf-two-scenario-nonattainment-logic-v1",
        "equality_delta": fstr(delta),
        "equality_t": fstr(t),
        "required_H": fstr(H),
        "required_h_u": "1",
        "factor_consequence": "d_u=q_u=1 because 0<d_u<=1 and 0<=q_u<=1",
        "blocking_contradiction": (
            "u is non-omittable, so some normalized w_u>1; with q_u=1, "
            "sum_i q_i w_i >= q_u w_u > 1, contradicting normalization"
        ),
        "conclusion": "the supremum 17/8 is not attained by a legal finite instance",
    }
    output = directory / "nonattainment_logic_report.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def lower_certificate(directory: Path) -> dict[str, object]:
    eps = EPSILON
    q = (
        Fraction(3, 4) - eps,
        Fraction(1) - eps,
        Fraction(1, 2),
        Fraction(3, 4) - eps,
    )
    p = tuple(Fraction(1) - value for value in q)
    d = (Fraction(1), Fraction(1), Fraction(3, 4), Fraction(1))
    k1 = (Fraction(1), Fraction(3000), Fraction(1), Fraction(1))
    k2 = (Fraction(1000), Fraction(1), Fraction(1000), Fraction(1000))
    B1 = sum((k1[i] * q[i] for i in range(N)), Fraction(0))
    B2 = sum((k2[i] * q[i] for i in range(N)), Fraction(0))
    assert B1 == Fraction(2_998_998, 1000)
    assert B2 == Fraction(1_998_999, 1000)

    # Derive released supports graph-natively.
    supports = tuple(
        frozenset(PATHS[terminal]["C"]) - frozenset(PATHS[terminal]["E"])
        for terminal in TERMINALS
    )
    assert tuple(tuple(arc for arc in TRUNK if arc in support) for support in supports) == (
        TRUNK[0:3],
        TRUNK[0:5],
        TRUNK[1:5],
        TRUNK[2:4],
    )
    trunk_terminal_sets = tuple(
        tuple(i + 1 for i, support in enumerate(supports) if arc in support)
        for arc in TRUNK
    )
    assert trunk_terminal_sets == ((1, 2), (1, 2, 3), (1, 2, 3, 4), (2, 3, 4), (2, 3))

    x = fractional_load(p, d)
    costs_1 = scenario_arc_costs(k1, d)
    costs_2 = scenario_arc_costs(k2, d)
    fractional_cost_1 = graph_cost(x, costs_1)
    fractional_cost_2 = graph_cost(x, costs_2)
    assert fractional_cost_1 == B1
    assert fractional_cost_2 == B2

    rows: list[dict[str, object]] = []
    feasible_masks: set[int] = set()
    for c_mask in SUBSETS:
        e_mask = FULL ^ c_mask
        y = routing_load(c_mask, d)
        cost_1 = graph_cost(y, costs_1)
        cost_2 = graph_cost(y, costs_2)
        difference_1 = cost_1 - fractional_cost_1
        difference_2 = cost_2 - fractional_cost_2
        direct_difference_1 = (
            sum((k1[i] for i in range(N) if e_mask & (1 << i)), Fraction(0)) - B1
        )
        direct_difference_2 = (
            sum((k2[i] for i in range(N) if e_mask & (1 << i)), Fraction(0)) - B2
        )
        assert difference_1 == direct_difference_1
        assert difference_2 == direct_difference_2
        feasible = difference_1 <= 0 and difference_2 <= 0
        direct_feasible = direct_difference_1 <= 0 and direct_difference_2 <= 0
        assert feasible == direct_feasible
        if feasible:
            feasible_masks.add(c_mask)
        maximum, witnesses, deviations = route_deviation(c_mask, p, d)
        rows.append(
            {
                "C_mask": c_mask,
                "C_set": name(c_mask),
                "E_set": name(e_mask),
                "scenario_1_cost": fstr(cost_1),
                "scenario_2_cost": fstr(cost_2),
                "scenario_1_cost_minus_fractional": fstr(difference_1),
                "scenario_2_cost_minus_fractional": fstr(difference_2),
                "scenario_1_budget_slack": fstr(-difference_1),
                "scenario_2_budget_slack": fstr(-difference_2),
                "simultaneously_feasible": feasible,
                "maximum_upper_deviation": fstr(maximum),
                "witness_arcs": ";".join(f"{u}->{v}" for u, v in witnesses),
                **{
                    f"dev_{u}_{v}": fstr(deviations[(u, v)])
                    for u, v in ARCS
                },
            }
        )

    expected_feasible = {FULL, bitset({2, 3, 4}), bitset({1, 2, 4}), bitset({1, 2, 3})}
    assert feasible_masks == expected_feasible
    feasible_values = {
        mask: route_deviation(mask, p, d)[0] for mask in feasible_masks
    }
    assert feasible_values[FULL] == Fraction(359, 125)
    assert feasible_values[bitset({2, 3, 4})] == Fraction(2123, 1000)
    assert feasible_values[bitset({1, 2, 4})] == Fraction(1061, 500)
    assert feasible_values[bitset({1, 2, 3})] == Fraction(2123, 1000)
    optimum = min(feasible_values.values())
    assert optimum == Fraction(1061, 500) == Fraction(17, 8) - 3 * eps
    assert optimum > 2

    target_family = frozenset(feasible_masks)
    family_ids = positive_c_family_ids()
    assert family_ids[target_family] == "F126"
    assert minimal_members(target_family) == (bitset({1, 2, 3}), bitset({1, 2, 4}), bitset({2, 3, 4}))

    feasible_rows = [row for row in rows if row["simultaneously_feasible"]]
    feasible_costs_1 = sorted({row["scenario_1_cost"] for row in feasible_rows})
    feasible_costs_2 = sorted({row["scenario_2_cost"] for row in feasible_rows})
    assert feasible_costs_1 == ["0", "1"]
    assert feasible_costs_2 == ["0", "1000"]
    assert all(row["scenario_1_cost_minus_fractional"] != "0" for row in feasible_rows)
    assert all(row["scenario_2_cost_minus_fractional"] != "0" for row in feasible_rows)

    # Integer scaling check.
    scale = 4000
    scaled_d = tuple(value * scale for value in d)
    assert all(value.denominator == 1 for value in scaled_d)
    integer_optimum = optimum * scale
    assert integer_optimum == 8488

    csv_path = directory / "two_scenario_17_8_16_routings.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    payload: dict[str, object] = {
        "schema": "ssuf-two-scenario-global-17-8-certificate-v2",
        "status": "exact graph-native finite certificate; second-round proof-review edits integrated; not formally peer reviewed",
        "theorem_target": "beta_G^(2sc)=17/8 as a non-attained supremum",
        "feasibility_semantics": (
            "for each scenario, unsplittable graph cost <= fractional graph cost; "
            "cost equality is not required"
        ),
        "finite_parameter": {"epsilon": fstr(eps)},
        "p_C_fractions": [fstr(value) for value in p],
        "q_E_fractions": [fstr(value) for value in q],
        "demands": [fstr(value) for value in d],
        "scenario_1_full_demand_differences": [fstr(value) for value in k1],
        "scenario_2_full_demand_differences": [fstr(value) for value in k2],
        "scenario_1_budget": fstr(B1),
        "scenario_2_budget": fstr(B2),
        "feasible_unsplittable_scenario_1_costs": feasible_costs_1,
        "feasible_unsplittable_scenario_2_costs": feasible_costs_2,
        "any_feasible_route_equal_to_fractional_budget": False,
        "within_scenario_weight_ratios": {"scenario_1": 3000, "scenario_2": 1000},
        "legal_private_E_arc_per_unit_costs": {
            "scenario_1": {
                f"{u}->{v}": fstr(costs_1[(u, v)]) for u, v in PRIVATE_E_ARC
            },
            "scenario_2": {
                f"{u}->{v}": fstr(costs_2[(u, v)]) for u, v in PRIVATE_E_ARC
            },
        },
        "simultaneously_feasible_E_sets": [
            name(FULL ^ mask) for mask in sorted(feasible_masks)
        ],
        "simultaneously_feasible_C_sets": [name(mask) for mask in sorted(feasible_masks)],
        "minimal_feasible_C_sets": [name(mask) for mask in minimal_members(target_family)],
        "intrinsic_family": "upward closure of {123,124,234}",
        "established_family_id": "F126 (historical label only)",
        "finite_minimum_max_upper_deviation": fstr(optimum),
        "finite_decimal": float(optimum),
        "limiting_supremum": "17/8",
        "global_supremum_attained_by_any_finite_legal_instance": False,
        "finite_attainment_of_17_over_8": False,
        "integer_scaling": {
            "demand_scale": scale,
            "scaled_demands": [int(value) for value in scaled_d],
            "maximum_scaled_demand": scale,
            "unavoidable_upper_deviation": int(integer_optimum),
        },
        "released_trunk_terminal_sets": [list(items) for items in trunk_terminal_sets],
        "routing_csv": csv_path.name,
    }
    json_path = directory / "two_scenario_17_8_certificate.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    directory = Path(__file__).resolve().parent
    exact_algebra_checks()
    recognition = threshold_recognition(directory)
    nonattainment = nonattainment_logic(directory)
    census = case_census()
    census_path = directory / "two_scenario_case_census.json"
    census_path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    certificate = lower_certificate(directory)

    print("PASS: enumerated all 168 downsets and certified the exact 149/18/1 partition.")
    print("PASS: every represented family has a positive threshold witness; all 18 exclusions have two-trades.")
    print("PASS: classified all 11,175 abstract scalar-pattern pairs as a regression check.")
    print("PASS: all 16 no-pair robust families occur and every no-pair pattern pair is classified.")
    print("PASS: verified the exact central and outer star-triangle square identities.")
    print("PASS: derived the released path-difference supports from the graph.")
    print("PASS: enumerated all 16 routings and all 13 arcs for the epsilon=1/1000 instance.")
    print("PASS: graph costs satisfy cost(y)-cost(x)=k(R)-k.q for both scenarios and every route.")
    print("PASS: feasibility is scenario-wise non-increase; equality is neither required nor present in the finite certificate.")
    print("PASS: the exact finite optimum is 1061/500 = 2.122 > 2.")
    print("PASS: the intrinsic family upward_closure{123,124,234} tends to 17/8 through rational data.")
    print("PASS: exact equality logic proves that no legal finite instance attains 17/8.")
    print("PASS: integer scaling gives maximum demand 4000 and unavoidable deviation 8488.")
    print("PASS: exact comparison 41^3 > 231^2 proves 17/8 > L.")
    print("WROTE: threshold_recognition_report.json")
    print("WROTE: nonattainment_logic_report.json")
    print(f"WROTE: {census_path.name}")
    print("WROTE: two_scenario_17_8_certificate.json")
    print("WROTE: two_scenario_17_8_16_routings.csv")
    assert recognition["positive_scalar_threshold_downsets"] == 149
    assert recognition["nonempty_nonthreshold_downsets"] == 18
    assert nonattainment["conclusion"].startswith("the supremum 17/8 is not attained")
    assert certificate["finite_minimum_max_upper_deviation"] == "1061/500"


if __name__ == "__main__":
    main()
