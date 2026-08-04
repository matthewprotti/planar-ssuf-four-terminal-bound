#!/usr/bin/env python3
"""Generate exact certificates for the four-terminal SSUF scenario-cover atlas.

Floating-point linear programming is used only to propose active constraints.
Every retained LP result is certified by exact rational primal/dual witnesses.
The output is deterministic and contains enough information for the separate
stdlib verifier to reconstruct all finite claims without invoking SciPy.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from scipy.optimize import linprog
import sympy as sp

HERE = Path(__file__).resolve().parent
OUT = HERE / "SCENARIO_COVER_ATLAS_RESULTS.json"

N = 4
SUBSETS = tuple(range(1 << N))
FULL_MASK = (1 << N) - 1
SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)

P = (Q(251, 1000), Q(1, 1000), Q(1, 2), Q(251, 1000))
D = (Q(1), Q(1), Q(3, 4), Q(1))


class VerificationFailure(RuntimeError):
    """Raised when an exact certificate cannot be established."""


def require(condition: object, message: object) -> None:
    if condition is True or condition is sp.true:
        return
    try:
        if bool(condition):
            return
    except TypeError:
        pass
    raise VerificationFailure(str(message))


def dot(left: Sequence[Q], right: Sequence[Q]) -> Q:
    return sum((x * y for x, y in zip(left, right, strict=True)), Q(0))


def mat_vec(matrix: Sequence[Sequence[Q]], vector: Sequence[Q]) -> tuple[Q, ...]:
    return tuple(dot(row, vector) for row in matrix)


def transpose(matrix: Sequence[Sequence[Q]]) -> tuple[tuple[Q, ...], ...]:
    if not matrix:
        return tuple()
    return tuple(tuple(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0])))


def fstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Q:
    return Q(str(value))


def subset_name(mask: int) -> str:
    return "".join(str(i + 1) for i in range(N) if mask & (1 << i)) or "empty"


def members(mask: int) -> tuple[int, ...]:
    return tuple(i for i in range(N) if mask & (1 << i))


def is_subset(left: int, right: int) -> bool:
    return left & right == left


def is_downset(family_mask: int) -> bool:
    for item in SUBSETS:
        if not (family_mask & (1 << item)):
            continue
        sub = item
        while True:
            if not (family_mask & (1 << sub)):
                return False
            if sub == 0:
                break
            sub = (sub - 1) & item
    return True


def maximal_members(family_mask: int) -> tuple[int, ...]:
    items = [item for item in SUBSETS if family_mask & (1 << item)]
    return tuple(
        item
        for item in items
        if not any(item != other and is_subset(item, other) for other in items)
    )


def minimal_nonmembers(family_mask: int) -> tuple[int, ...]:
    items = [item for item in SUBSETS if not (family_mask & (1 << item))]
    return tuple(
        item
        for item in items
        if not any(item != other and is_subset(other, item) for other in items)
    )


def displacement(mask: int, p: Sequence[Q]) -> tuple[Q, ...]:
    return tuple(Q(1 if mask & (1 << i) else 0) - p[i] for i in range(N))


def route_deviations(mask: int, p: Sequence[Q], d: Sequence[Q]) -> tuple[Q, ...]:
    trunk = tuple(
        sum(
            (
                d[i] * (Q(1 if mask & (1 << i) else 0) - p[i])
                for i in range(N)
                if arc_index in SUPPORTS[i]
            ),
            Q(0),
        )
        for arc_index in range(5)
    )

    private: list[Q] = []
    for i in range(N):
        q_i = Q(1) - p[i]
        if mask & (1 << i):
            private.extend((-d[i] * q_i, d[i] * q_i))
        else:
            private.extend((d[i] * p[i], -d[i] * p[i]))
    return trunk + tuple(private)


def route_value(mask: int, p: Sequence[Q], d: Sequence[Q]) -> Q:
    return max(route_deviations(mask, p, d))


def exact_linear_solve(matrix: Sequence[Sequence[Q]], rhs: Sequence[Q]) -> tuple[Q, ...] | None:
    if not matrix:
        return tuple()
    size = len(matrix)
    if len(rhs) != size or any(len(row) != size for row in matrix):
        return None

    augmented = [list(row) + [rhs[index]] for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column] != 0),
            None,
        )
        if pivot is None:
            return None
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]

        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            augmented[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    augmented[row], augmented[column], strict=True
                )
            ]

    return tuple(augmented[row][-1] for row in range(size))


def objective(vector: Sequence[Q], c: Sequence[Q]) -> Q:
    return dot(vector, c)


def verify_max_lp_certificate(
    *,
    G: Sequence[Sequence[Q]],
    h: Sequence[Q],
    E: Sequence[Sequence[Q]],
    f: Sequence[Q],
    c: Sequence[Q],
    primal: Sequence[Q],
    active: Sequence[int],
    dual_active: Sequence[Q],
    dual_equalities: Sequence[Q],
) -> Q:
    require(len(primal) == len(c), "primal dimension mismatch")
    require(len(active) == len(dual_active), "dual support mismatch")
    require(len(E) == len(f) == len(dual_equalities), "equality dual mismatch")

    for row, bound in zip(G, h, strict=True):
        require(dot(row, primal) <= bound, ("primal inequality failure", row, bound, primal))
    for row, bound in zip(E, f, strict=True):
        require(dot(row, primal) == bound, ("primal equality failure", row, bound, primal))
    require(all(value >= 0 for value in dual_active), "negative dual multiplier")

    dual_lhs = [Q(0) for _ in c]
    for row_index, multiplier in zip(active, dual_active, strict=True):
        for j, coefficient in enumerate(G[row_index]):
            dual_lhs[j] += multiplier * coefficient
    for row, multiplier in zip(E, dual_equalities, strict=True):
        for j, coefficient in enumerate(row):
            dual_lhs[j] += multiplier * coefficient
    require(tuple(dual_lhs) == tuple(c), ("dual equality failure", dual_lhs, c))

    primal_value = objective(primal, c)
    dual_value = sum((h[index] * value for index, value in zip(active, dual_active, strict=True)), Q(0))
    dual_value += sum((bound * value for bound, value in zip(f, dual_equalities, strict=True)), Q(0))
    require(primal_value == dual_value, ("strong duality failure", primal_value, dual_value))
    return primal_value


def normalized_fraction_key(values: Sequence[Q]) -> tuple[tuple[int, int], ...]:
    """Primitive deterministic representation for a rational vector."""

    return tuple((value.numerator, value.denominator) for value in values)


def canonical_certificate_at_value(
    *,
    G: Sequence[Sequence[Q]],
    h: Sequence[Q],
    E: Sequence[Sequence[Q]],
    f: Sequence[Q],
    c: Sequence[Q],
    value: Q,
    label: str,
) -> dict[str, object]:
    """Select the lexicographically least normalized exact optimal certificate.

    The floating solver has already proposed an exactly verified optimum value.
    Canonical selection below is entirely rational and independent of its basis.
    Variable order is the order in c and constraint order is the order in G.
    The primal key is the vector of reduced (numerator, denominator) pairs.
    For that primal, the dual key is active row indices followed by the reduced
    active and equality multiplier vectors.
    """

    n = len(c)
    equality_count = len(E)
    active_needed = n - equality_count
    anchor_needed = active_needed - 1
    require(anchor_needed >= 0, (label, "objective is overdetermined"))

    primal_by_key: dict[tuple[tuple[int, int], ...], tuple[Q, ...]] = {}
    for anchor in combinations(range(len(G)), anchor_needed):
        matrix = list(E) + [list(c)] + [G[index] for index in anchor]
        rhs = list(f) + [value] + [h[index] for index in anchor]
        primal = exact_linear_solve(matrix, rhs)
        if primal is None:
            continue
        if any(dot(row, primal) > bound for row, bound in zip(G, h, strict=True)):
            continue
        if any(dot(row, primal) != bound for row, bound in zip(E, f, strict=True)):
            continue
        if objective(primal, c) != value:
            continue
        primal_by_key.setdefault(normalized_fraction_key(primal), primal)

    require(primal_by_key, f"no exact canonical optimal primal found for {label}")
    primal_key = min(primal_by_key)
    primal = primal_by_key[primal_key]
    tight = tuple(
        index
        for index, (row, bound) in enumerate(zip(G, h, strict=True))
        if dot(row, primal) == bound
    )

    dual_candidates: list[
        tuple[
            tuple[object, ...],
            tuple[int, ...],
            tuple[Q, ...],
            tuple[Q, ...],
        ]
    ] = []
    for active in combinations(tight, active_needed):
        dual_matrix = [
            [G[index][variable] for index in active]
            + [row[variable] for row in E]
            for variable in range(n)
        ]
        dual = exact_linear_solve(dual_matrix, c)
        if dual is None:
            continue
        dual_active = dual[:active_needed]
        dual_equalities = dual[active_needed:]
        if any(multiplier < 0 for multiplier in dual_active):
            continue
        try:
            verified_value = verify_max_lp_certificate(
                G=G,
                h=h,
                E=E,
                f=f,
                c=c,
                primal=primal,
                active=active,
                dual_active=dual_active,
                dual_equalities=dual_equalities,
            )
        except VerificationFailure:
            continue
        require(verified_value == value, (label, verified_value, value))
        key: tuple[object, ...] = (
            tuple(active),
            normalized_fraction_key(dual_active),
            normalized_fraction_key(dual_equalities),
        )
        dual_candidates.append(
            (key, tuple(active), tuple(dual_active), tuple(dual_equalities))
        )

    require(dual_candidates, f"no exact canonical optimal dual found for {label}")
    _, active, dual_active, dual_equalities = min(
        dual_candidates, key=lambda item: item[0]
    )
    return {
        "primal": [fstr(item) for item in primal],
        "active_indices": list(active),
        "dual_active": [fstr(item) for item in dual_active],
        "dual_equalities": [fstr(item) for item in dual_equalities],
        "objective": fstr(value),
    }


def solve_max_lp_exact(
    *,
    G: Sequence[Sequence[Q]],
    h: Sequence[Q],
    E: Sequence[Sequence[Q]],
    f: Sequence[Q],
    c: Sequence[Q],
    label: str,
    canonical: bool = True,
) -> dict[str, object]:
    n = len(c)
    eq_rank = len(E)
    active_needed = n - eq_rank
    require(active_needed >= 0, "too many equalities")

    result = linprog(
        c=[-float(value) for value in c],
        A_ub=np.array([[float(value) for value in row] for row in G], dtype=float) if G else None,
        b_ub=np.array([float(value) for value in h], dtype=float) if h else None,
        A_eq=np.array([[float(value) for value in row] for row in E], dtype=float) if E else None,
        b_eq=np.array([float(value) for value in f], dtype=float) if f else None,
        bounds=[(None, None)] * n,
        method="highs",
    )
    require(result.success, (label, result.message))

    slacks = []
    for row, bound in zip(G, h, strict=True):
        slacks.append(float(bound) - sum(float(value) * proposal for value, proposal in zip(row, result.x, strict=True)))

    candidate_rows = [index for index, slack in enumerate(slacks) if abs(slack) <= 1e-7]
    pools: list[Sequence[int]] = [candidate_rows]
    near_rows = [index for index, slack in enumerate(slacks) if abs(slack) <= 1e-5]
    if set(near_rows) != set(candidate_rows):
        pools.append(near_rows)
    pools.append(tuple(range(len(G))))

    seen: set[tuple[int, ...]] = set()
    for pool in pools:
        if len(pool) < active_needed:
            continue
        for active_tuple in combinations(pool, active_needed):
            if active_tuple in seen:
                continue
            seen.add(active_tuple)
            primal_matrix = list(E) + [G[index] for index in active_tuple]
            primal_rhs = list(f) + [h[index] for index in active_tuple]
            primal = exact_linear_solve(primal_matrix, primal_rhs)
            if primal is None:
                continue

            dual_matrix: list[list[Q]] = []
            for variable in range(n):
                dual_matrix.append(
                    [G[index][variable] for index in active_tuple]
                    + [row[variable] for row in E]
                )
            dual = exact_linear_solve(dual_matrix, c)
            if dual is None:
                continue
            dual_active = dual[:active_needed]
            dual_equalities = dual[active_needed:]
            try:
                value = verify_max_lp_certificate(
                    G=G,
                    h=h,
                    E=E,
                    f=f,
                    c=c,
                    primal=primal,
                    active=active_tuple,
                    dual_active=dual_active,
                    dual_equalities=dual_equalities,
                )
            except VerificationFailure:
                continue
            if canonical:
                return canonical_certificate_at_value(
                    G=G,
                    h=h,
                    E=E,
                    f=f,
                    c=c,
                    value=value,
                    label=label,
                )
            return {
                "primal": [fstr(item) for item in primal],
                "active_indices": list(active_tuple),
                "dual_active": [fstr(item) for item in dual_active],
                "dual_equalities": [fstr(item) for item in dual_equalities],
                "objective": fstr(value),
            }

    raise VerificationFailure(f"no exact primal-dual certificate found for {label}")


def margin_lp(family_mask: int, p: Sequence[Q], kappa: Q | None = None) -> tuple[list[list[Q]], list[Q], list[list[Q]], list[Q], list[Q], list[str]]:
    # x=(k1,k2,k3,k4,rho), maximize rho, sum k_i=1.
    G: list[list[Q]] = []
    h: list[Q] = []
    labels: list[str] = []

    for i in range(N):
        row = [Q(0)] * 5
        row[i] = Q(-1)
        row[4] = Q(1)
        G.append(row)
        h.append(Q(0))
        labels.append(f"positive_margin_t{i + 1}")

    for mask in SUBSETS:
        v = displacement(mask, p)
        if family_mask & (1 << mask):
            # bad: k.v <= -rho
            G.append(list(v) + [Q(1)])
            h.append(Q(0))
            labels.append(f"bad_{subset_name(mask)}")
        else:
            # accepted/tied: k.v >= 0
            G.append([Q(-value) for value in v] + [Q(0)])
            h.append(Q(0))
            labels.append(f"good_{subset_name(mask)}")

    if kappa is not None:
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                row = [Q(0)] * 5
                row[i] = Q(1)
                row[j] = -kappa
                G.append(row)
                h.append(Q(0))
                labels.append(f"ratio_t{i + 1}_over_t{j + 1}")

    E = [[Q(1), Q(1), Q(1), Q(1), Q(0)]]
    f = [Q(1)]
    c = [Q(0), Q(0), Q(0), Q(0), Q(1)]
    return G, h, E, f, c, labels


def kappa_lp(family_mask: int, p: Sequence[Q]) -> tuple[list[list[Q]], list[Q], list[list[Q]], list[Q], list[Q], list[str]]:
    # x=(k1,k2,k3,k4,K), maximize -K, with min k_i >=1.
    G: list[list[Q]] = []
    h: list[Q] = []
    labels: list[str] = []

    for i in range(N):
        row = [Q(0)] * 5
        row[i] = Q(-1)
        G.append(row)
        h.append(Q(-1))
        labels.append(f"lower_t{i + 1}")

        row = [Q(0)] * 5
        row[i] = Q(1)
        row[4] = Q(-1)
        G.append(row)
        h.append(Q(0))
        labels.append(f"upper_t{i + 1}")

    for mask in SUBSETS:
        v = displacement(mask, p)
        if family_mask & (1 << mask):
            G.append(list(v) + [Q(0)])
            h.append(Q(0))
            labels.append(f"bad_closure_{subset_name(mask)}")
        else:
            G.append([Q(-value) for value in v] + [Q(0)])
            h.append(Q(0))
            labels.append(f"good_{subset_name(mask)}")

    E: list[list[Q]] = []
    f: list[Q] = []
    c = [Q(0), Q(0), Q(0), Q(0), Q(-1)]
    return G, h, E, f, c, labels


def attach_labels(certificate: dict[str, object], labels: Sequence[str]) -> dict[str, object]:
    out = deepcopy(certificate)
    out["active_labels"] = [labels[index] for index in out["active_indices"]]  # type: ignore[index]
    return out


def good_feasibility_lp(family_mask: int, p: Sequence[Q]) -> tuple[list[list[Q]], list[Q], list[list[Q]], list[Q], list[Q], list[str]]:
    # x=(k1,k2,k3,k4,z), maximize -z over the nonnegative simplex.
    # z=0 exactly when some nonnegative normalized k accepts every non-bad set.
    G: list[list[Q]] = []
    h: list[Q] = []
    labels: list[str] = []
    for i in range(N):
        row = [Q(0)] * 5
        row[i] = Q(-1)
        G.append(row)
        h.append(Q(0))
        labels.append(f"nonnegative_t{i + 1}")
    row = [Q(0)] * 5
    row[4] = Q(-1)
    G.append(row)
    h.append(Q(0))
    labels.append("nonnegative_slack")
    for mask in SUBSETS:
        if family_mask & (1 << mask):
            continue
        v = displacement(mask, p)
        # k.v >= -z, equivalently -k.v-z <= 0.
        G.append([Q(-value) for value in v] + [Q(-1)])
        h.append(Q(0))
        labels.append(f"relaxed_good_{subset_name(mask)}")
    E = [[Q(1), Q(1), Q(1), Q(1), Q(0)]]
    f = [Q(1)]
    c = [Q(0), Q(0), Q(0), Q(0), Q(-1)]
    return G, h, E, f, c, labels


def exact_pattern_record(
    family_mask: int,
    p: Sequence[Q],
    *,
    canonical_certificates: bool = True,
) -> dict[str, object]:
    G0, h0, E0, f0, c0, labels0 = good_feasibility_lp(family_mask, p)
    good_cert = solve_max_lp_exact(
        G=G0,
        h=h0,
        E=E0,
        f=f0,
        c=c0,
        label=f"good-feasibility {family_mask:#06x}",
        canonical=canonical_certificates,
    )
    good_cert = attach_labels(good_cert, labels0)
    minimum_slack = -parse_fraction(good_cert["objective"])
    require(minimum_slack >= 0, (family_mask, minimum_slack))

    record: dict[str, object] = {
        "mask_hex": f"0x{family_mask:04x}",
        "maximal_bad_sets": [subset_name(mask) for mask in maximal_members(family_mask)],
        "minimal_accepted_sets": [subset_name(mask) for mask in minimal_nonmembers(family_mask)],
        "good_feasibility_certificate": good_cert,
        "minimum_good_slack": fstr(minimum_slack),
        "realizable": False,
    }
    if minimum_slack > 0:
        record["infeasibility_reason"] = "no nonnegative normalized normal accepts every declared good set"
        return record

    G, h, E, f, c, labels = margin_lp(family_mask, p)
    margin_cert = solve_max_lp_exact(
        G=G,
        h=h,
        E=E,
        f=f,
        c=c,
        label=f"margin {family_mask:#06x}",
        canonical=canonical_certificates,
    )
    margin_cert = attach_labels(margin_cert, labels)
    margin = parse_fraction(margin_cert["objective"])
    realizable = margin > 0
    record["margin_certificate"] = margin_cert
    record["realizable"] = realizable
    if not realizable:
        record["infeasibility_reason"] = "accepted-set cone exists only on a zero bad/positivity margin boundary"
        return record

    Gk, hk, Ek, fk, ck, klabels = kappa_lp(family_mask, p)
    kappa_cert = solve_max_lp_exact(
        G=Gk,
        h=hk,
        E=Ek,
        f=fk,
        c=ck,
        label=f"kappa {family_mask:#06x}",
        canonical=canonical_certificates,
    )
    kappa_cert = attach_labels(kappa_cert, klabels)
    kappa = -parse_fraction(kappa_cert["objective"])
    require(kappa >= 1, (family_mask, kappa))

    Ga, ha, Ea, fa, ca, alabels = margin_lp(family_mask, p, kappa=kappa)
    attained_cert = solve_max_lp_exact(
        G=Ga,
        h=ha,
        E=Ea,
        f=fa,
        c=ca,
        label=f"attainment {family_mask:#06x}",
        canonical=canonical_certificates,
    )
    attained_cert = attach_labels(attained_cert, alabels)
    attained_margin = parse_fraction(attained_cert["objective"])

    record.update(
        {
            "kappa_infimum": fstr(kappa),
            "kappa_certificate": kappa_cert,
            "attained_at_infimum": attained_margin > 0,
            "attainment_certificate": attained_cert,
        }
    )
    return record

def available_pattern(record: dict[str, object], kappa: Q, *, right_limit: bool = False) -> bool:
    if not record["realizable"]:
        return False
    threshold = parse_fraction(record["kappa_infimum"])
    if kappa > threshold:
        return True
    if kappa < threshold:
        return False
    if right_limit:
        return True
    return bool(record["attained_at_infimum"])


def union_cover_dp(pattern_masks: Sequence[int], max_scenarios: int) -> tuple[list[int], list[tuple[int, ...] | None]]:
    size = 1 << 16
    inf = max_scenarios + 1
    distance = [inf] * size
    witness: list[tuple[int, ...] | None] = [None] * size
    distance[0] = 0
    witness[0] = tuple()

    frontier = {0}
    for step in range(1, max_scenarios + 1):
        new_frontier: set[int] = set()
        for union_mask in frontier:
            previous = witness[union_mask]
            require(previous is not None, "missing predecessor")
            for pattern in pattern_masks:
                merged = union_mask | pattern
                if distance[merged] > step:
                    distance[merged] = step
                    witness[merged] = previous + (pattern,)
                    new_frontier.add(merged)
        frontier = new_frontier
    return distance, witness


def best_cover_for_target(
    target: int,
    pattern_masks: Sequence[int],
    max_scenarios: int,
) -> tuple[int | None, tuple[int, ...] | None]:
    distance, witnesses = union_cover_dp(pattern_masks, max_scenarios)
    best: tuple[int, tuple[int, ...]] | None = None
    for union_mask, count in enumerate(distance):
        if count > max_scenarios or target & ~union_mask:
            continue
        witness = witnesses[union_mask]
        require(witness is not None, "cover distance lacks witness")
        if best is None or count < best[0] or (count == best[0] and witness < best[1]):
            best = (count, witness)
    if best is None:
        return None, None
    return best


def cover_number_distribution(pattern_masks: Sequence[int]) -> tuple[dict[str, int], dict[int, tuple[int, ...] | None]]:
    distance, witnesses = union_cover_dp(pattern_masks, 4)
    sup_distance = distance[:]
    sup_witness = witnesses[:]
    for bit in range(16):
        for mask in range((1 << 16) - 1, -1, -1):
            if mask & (1 << bit):
                continue
            larger = mask | (1 << bit)
            if sup_distance[larger] < sup_distance[mask]:
                sup_distance[mask] = sup_distance[larger]
                sup_witness[mask] = sup_witness[larger]

    counter: Counter[str] = Counter()
    by_downset: dict[int, tuple[int, ...] | None] = {}
    for mask in range(1 << 16):
        if not is_downset(mask):
            continue
        if sup_distance[mask] <= 4:
            counter[str(sup_distance[mask])] += 1
            by_downset[mask] = sup_witness[mask]
        else:
            counter["impossible"] += 1
            by_downset[mask] = None
    return dict(sorted(counter.items())), by_downset


def target_below(value: Q, route_values: dict[int, Q]) -> int:
    return sum(1 << mask for mask, route in route_values.items() if route < value)


def robust_value_at_kappa(
    *,
    records: Sequence[dict[str, object]],
    route_values: dict[int, Q],
    kappa: Q,
    scenarios: int,
    right_limit: bool = False,
) -> tuple[Q, tuple[int, ...]]:
    patterns = [
        int(str(record["mask_hex"]), 16)
        for record in records
        if available_pattern(record, kappa, right_limit=right_limit)
    ]
    levels = sorted(set(route_values.values()))
    best_value = levels[0]
    best_witness: tuple[int, ...] = tuple()
    for level in levels:
        target = target_below(level, route_values)
        count, witness = best_cover_for_target(target, patterns, scenarios)
        if count is not None:
            best_value = level
            require(witness is not None, "missing robust cover witness")
            best_witness = witness
    return best_value, best_witness


def phase_checks(records: Sequence[dict[str, object]], route_values: dict[int, Q]) -> dict[str, object]:
    A = Q(1498, 501)
    B = Q(998)
    C = Q(1998)
    D3 = Q(1249, 252)
    E3 = Q(1248, 251)

    probes = {
        "one": Q(1),
        "inside_A": (Q(1) + A) / 2,
        "at_A": A,
        "after_A": (A + D3) / 2,
        "at_D3": D3,
        "after_D3": (D3 + E3) / 2,
        "at_E3": E3,
        "after_E3": (E3 + B) / 2,
        "at_B": B,
        "after_B": (B + C) / 2,
        "at_C": C,
        "after_C": C + Q(1),
    }

    values: dict[str, dict[str, object]] = {}
    for name, kappa in probes.items():
        row: dict[str, object] = {"kappa": fstr(kappa)}
        for scenarios in (1, 2, 3, 4):
            value, witness = robust_value_at_kappa(
                records=records,
                route_values=route_values,
                kappa=kappa,
                scenarios=scenarios,
            )
            row[f"m{scenarios}_value"] = fstr(value)
            row[f"m{scenarios}_cover"] = [f"0x{mask:04x}" for mask in witness]
        values[name] = row

    expected_m2 = {
        "one": Q(561, 500),
        "inside_A": Q(561, 500),
        "at_A": Q(561, 500),
        "after_A": Q(1123, 1000),
        "at_B": Q(1123, 1000),
        "after_B": Q(234, 125),
        "at_C": Q(234, 125),
        "after_C": Q(1061, 500),
    }
    expected_m3 = {
        "one": Q(561, 500),
        "inside_A": Q(561, 500),
        "at_A": Q(561, 500),
        "after_A": Q(1123, 1000),
        "at_D3": Q(1123, 1000),
        "after_D3": Q(687, 500),
        "at_E3": Q(687, 500),
        "after_E3": Q(234, 125),
        "at_C": Q(234, 125),
        "after_C": Q(2123, 1000),
    }
    expected_m4 = {
        "one": Q(561, 500),
        "inside_A": Q(561, 500),
        "at_A": Q(561, 500),
        "after_A": Q(1123, 1000),
        "at_D3": Q(1123, 1000),
        "after_D3": Q(234, 125),
        "at_C": Q(234, 125),
        "after_C": Q(359, 125),
    }
    for name, expected in expected_m2.items():
        require(parse_fraction(values[name]["m2_value"]) == expected, ("m2 phase", name, values[name], expected))
    for name, expected in expected_m3.items():
        require(parse_fraction(values[name]["m3_value"]) == expected, ("m3 phase", name, values[name], expected))
    for name, expected in expected_m4.items():
        require(parse_fraction(values[name]["m4_value"]) == expected, ("m4 phase", name, values[name], expected))

    return {
        "breakpoints": {
            "A": fstr(A),
            "B": fstr(B),
            "C": fstr(C),
            "D3": fstr(D3),
            "E3": fstr(E3),
        },
        "probes": values,
        "m2_piecewise": [
            {"kappa": f"1 <= kappa <= {fstr(A)}", "value": fstr(Q(561, 500))},
            {"kappa": f"{fstr(A)} < kappa <= {fstr(B)}", "value": fstr(Q(1123, 1000))},
            {"kappa": f"{fstr(B)} < kappa <= {fstr(C)}", "value": fstr(Q(234, 125))},
            {"kappa": f"{fstr(C)} < kappa", "value": fstr(Q(1061, 500))},
        ],
        "m3_piecewise": [
            {"kappa": f"1 <= kappa <= {fstr(A)}", "value": fstr(Q(561, 500))},
            {"kappa": f"{fstr(A)} < kappa <= {fstr(D3)}", "value": fstr(Q(1123, 1000))},
            {"kappa": f"{fstr(D3)} < kappa <= {fstr(E3)}", "value": fstr(Q(687, 500))},
            {"kappa": f"{fstr(E3)} < kappa <= {fstr(C)}", "value": fstr(Q(234, 125))},
            {"kappa": f"{fstr(C)} < kappa", "value": fstr(Q(2123, 1000))},
        ],
        "m4_piecewise": [
            {"kappa": f"1 <= kappa <= {fstr(A)}", "value": fstr(Q(561, 500))},
            {"kappa": f"{fstr(A)} < kappa <= {fstr(D3)}", "value": fstr(Q(1123, 1000))},
            {"kappa": f"{fstr(D3)} < kappa <= {fstr(C)}", "value": fstr(Q(234, 125))},
            {"kappa": f"{fstr(C)} < kappa", "value": fstr(Q(359, 125))},
        ],
    }


def scenario_bad_mask(weights: Sequence[Q], p: Sequence[Q]) -> int:
    threshold = dot(weights, p)
    return sum(
        1 << mask
        for mask in SUBSETS
        if sum((weights[i] for i in members(mask)), Q(0)) < threshold
    )


def common_feasible_sets(scenarios: Sequence[Sequence[Q]], p: Sequence[Q]) -> tuple[int, ...]:
    return tuple(
        mask
        for mask in SUBSETS
        if all(dot(weights, displacement(mask, p)) >= 0 for weights in scenarios)
    )


def finite_witness_checks(route_values: dict[int, Q]) -> dict[str, object]:
    original = ((Q(1), Q(3000), Q(1), Q(1)), (Q(1000), Q(1), Q(1000), Q(1000)))
    improved = ((Q(1), Q(1999), Q(1), Q(1)), (Q(500), Q(1), Q(500), Q(500)))
    expected = (0b0111, 0b1011, 0b1110, 0b1111)
    original_feasible = common_feasible_sets(original, P)
    improved_feasible = common_feasible_sets(improved, P)
    require(original_feasible == expected, original_feasible)
    require(improved_feasible == expected, improved_feasible)
    optimum = min(route_values[mask] for mask in improved_feasible)
    require(optimum == Q(1061, 500), optimum)

    center_mask = scenario_bad_mask(improved[0], P)
    triangle_mask = scenario_bad_mask(improved[1], P)
    require(center_mask == 0x3333, f"center mask {center_mask:#06x}")
    require(triangle_mask == 0x055F, f"triangle mask {triangle_mask:#06x}")

    return {
        "original_scenarios": [[fstr(value) for value in row] for row in original],
        "improved_integer_scenarios": [[fstr(value) for value in row] for row in improved],
        "original_max_condition_number": "3000",
        "improved_max_condition_number": "1999",
        "common_feasible_C_sets": [subset_name(mask) for mask in improved_feasible],
        "exact_objective": fstr(optimum),
        "center_bad_mask": f"0x{center_mask:04x}",
        "triangle_bad_mask": f"0x{triangle_mask:04x}",
        "center_kappa_infimum": "1998",
        "triangle_kappa_infimum": "999/2",
    }


def symbolic_checks() -> dict[str, object]:
    kappa, epsilon = sp.symbols("kappa epsilon", positive=True)
    Qk = kappa * (kappa - 2) / (kappa**2 - 1)
    Sk = kappa * (2 * kappa - 1) / (kappa**2 - 1)
    require(sp.simplify(Sk - kappa * (1 - Qk)) == 0, "central cover boundary identity")
    require(sp.simplify(Sk - (2 - Qk / kappa)) == 0, "outer-pair cover boundary identity")

    Fk = sp.simplify(Qk + (1 + Sk) ** 2 / 8)
    expected_F = (17 * kappa**4 - 22 * kappa**3 - 13 * kappa**2 + 18 * kappa + 1) / (8 * (kappa**2 - 1) ** 2)
    require(sp.simplify(Fk - expected_F) == 0, "F(kappa) recovery identity")

    kappa_star = 2 * (1 - epsilon) / epsilon
    center_budget = (1 + 2 * epsilon) + epsilon * kappa_star
    require(sp.simplify(center_budget - 3) == 0, "center triple boundary")
    triangle_star = (1 - epsilon) / (2 * epsilon)
    triangle_budget = (1 + 2 * epsilon) * triangle_star + epsilon
    require(sp.simplify(triangle_budget - (1 + triangle_star)) == 0, "central pair boundary")
    require(sp.simplify(kappa_star - 4 * triangle_star) == 0, "four-to-one bottleneck identity")

    lower_branch = sp.Rational(17, 8) - 6 / (kappa + 2)
    require(sp.simplify((sp.Rational(17, 8) - 3 * (2 / (kappa + 2))) - lower_branch) == 0, "lower branch")

    epsilon_samples = [Q(1, 1000), Q(1, 100), Q(1, 50), Q(1, 20), Q(1, 10)]
    sample_rows = []
    for eps in epsilon_samples:
        p = (Q(1, 4) + eps, eps, Q(1, 2), Q(1, 4) + eps)
        center = Q(2) * (Q(1) - eps) / eps
        triangle = (Q(1) - eps) / (Q(2) * eps)
        require(center == Q(4) * triangle, (eps, center, triangle))
        sample_rows.append(
            {
                "epsilon": fstr(eps),
                "center_infimum": fstr(center),
                "triangle_infimum": fstr(triangle),
                "predicted_two_scenario_bottleneck": fstr(center),
                "p": [fstr(value) for value in p],
            }
        )

    return {
        "Q_kappa": str(sp.factor(Qk)),
        "S_kappa": str(sp.factor(Sk)),
        "F_kappa": str(sp.factor(Fk)),
        "star_cover_kappa_infimum": str(sp.factor(kappa_star)),
        "triangle_cover_kappa_infimum": str(sp.factor(triangle_star)),
        "cover_derived_lower_branch_for_kappa_gt_6": str(sp.factor(lower_branch)),
        "exact_epsilon_samples": sample_rows,
    }


def content_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    downsets = tuple(mask for mask in range(1 << 16) if is_downset(mask))
    require(len(downsets) == 168, len(downsets))

    route_values = {mask: route_value(mask, P, D) for mask in SUBSETS}
    expected_route_values = {
        0: Q(3, 8), 4: Q(3, 8), 1: Q(749, 1000), 8: Q(749, 1000),
        2: Q(999, 1000), 9: Q(561, 500), 5: Q(1123, 1000), 12: Q(1123, 1000),
        10: Q(1373, 1000), 6: Q(687, 500), 3: Q(437, 250), 13: Q(234, 125),
        11: Q(1061, 500), 7: Q(2123, 1000), 14: Q(2123, 1000), 15: Q(359, 125),
    }
    require(route_values == expected_route_values, route_values)

    records = [exact_pattern_record(mask, P) for mask in downsets]
    realizable_records = [record for record in records if record["realizable"]]
    require(len(realizable_records) == 59, len(realizable_records))
    pattern_masks = [int(str(record["mask_hex"]), 16) for record in realizable_records]

    distribution, downset_witnesses = cover_number_distribution(pattern_masks)
    require(distribution == {"0": 1, "1": 61, "2": 91, "3": 13, "4": 1, "impossible": 1}, distribution)
    four_needed = [mask for mask, witness in downset_witnesses.items() if witness is not None and len(witness) == 4]
    impossible = [mask for mask, witness in downset_witnesses.items() if witness is None]
    require(four_needed == [0x7FFF], four_needed)
    require(impossible == [0xFFFF], impossible)

    unrestricted: dict[str, object] = {}
    for scenarios in (1, 2, 3, 4):
        value, witness = robust_value_at_kappa(
            records=records,
            route_values=route_values,
            kappa=Q(10**9),
            scenarios=scenarios,
            right_limit=True,
        )
        unrestricted[str(scenarios)] = {
            "value": fstr(value),
            "cover": [f"0x{mask:04x}" for mask in witness],
        }
    require(parse_fraction(unrestricted["1"]["value"]) == Q(561, 500), unrestricted)
    require(parse_fraction(unrestricted["2"]["value"]) == Q(1061, 500), unrestricted)
    require(parse_fraction(unrestricted["3"]["value"]) == Q(2123, 1000), unrestricted)
    require(parse_fraction(unrestricted["4"]["value"]) == Q(359, 125), unrestricted)

    finite_witness = finite_witness_checks(route_values)
    phases = phase_checks(records, route_values)
    symbolic = symbolic_checks()

    kappa_levels = sorted(
        {parse_fraction(record["kappa_infimum"]) for record in realizable_records}
    )
    require(len(kappa_levels) == 32, len(kappa_levels))

    payload: dict[str, object] = {
        "schema": "ssuf-scenario-cover-atlas-v1",
        "date": "2026-08-01",
        "status": "private exact research package; no public repository change",
        "orientation": {
            "route_encoding": "mask S is the C-set",
            "displacement": "v_S = 1_S - p",
            "scenario_acceptance": "k dot v_S >= 0",
            "scenario_elimination": "k dot v_S < 0",
            "threshold_semantics": "routes with M(S) < t must be covered to force objective at least t",
        },
        "fixed_instance": {
            "p": [fstr(value) for value in P],
            "d": [fstr(value) for value in D],
            "route_values": {
                subset_name(mask): fstr(route_values[mask]) for mask in SUBSETS
            },
        },
        "atlas_summary": {
            "downsets": len(downsets),
            "realizable_positive_scenario_losing_patterns": len(realizable_records),
            "distinct_kappa_infima": len(kappa_levels),
            "cover_number_distribution_over_all_downsets": distribution,
            "unique_four_scenario_downset": "0x7fff (all proper C-sets)",
            "unique_impossible_downset": "0xffff (all C-sets, including all-C)",
        },
        "unrestricted_fixed_instance_values": unrestricted,
        "finite_witness": finite_witness,
        "bounded_phase_diagrams": phases,
        "symbolic_cover_recovery": symbolic,
        "patterns": records,
    }
    payload["content_sha256"] = content_hash(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("PASS exact route table for the epsilon=1/1000 RB-003 family member")
    print("PASS exact primal-dual classification of 168 downsets; 59 positive-normal losing patterns")
    print("PASS exact scenario-cover distribution: 1, 61, 91, 13, 1, 1")
    print("PASS exact unrestricted fixed-instance ladder: 561/500, 1061/500, 2123/1000, 359/125")
    print("PASS exact bounded-kappa phase diagrams for two, three, and four scenarios")
    print("PASS improved integer two-scenario witness with maximum condition number 1999")
    print("PASS symbolic recovery of Q_kappa, S_kappa, F(kappa), and the star-cover threshold")
    print(f"WROTE {OUT.name}")
    print(f"CONTENT_SHA256 {payload['content_sha256']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}")
        raise
