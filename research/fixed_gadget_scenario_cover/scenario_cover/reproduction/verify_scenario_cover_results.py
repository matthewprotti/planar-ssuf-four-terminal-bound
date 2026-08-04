#!/usr/bin/env python3
"""Independent exact verifier for SCENARIO_COVER_ATLAS_RESULTS.json.

This checker does not import the generator and does not invoke NumPy, SciPy, or
SymPy. It reconstructs every rational LP, verifies all primal-dual certificates,
recomputes the route table and cover dynamic programs, and checks the reported
phase transitions.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
DEFAULT_PATH = HERE / "SCENARIO_COVER_ATLAS_RESULTS.json"

N = 4
SUBSETS = tuple(range(1 << N))
SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)
P = (Q(251, 1000), Q(1, 1000), Q(1, 2), Q(251, 1000))
D = (Q(1), Q(1), Q(3, 4), Q(1))


class VerificationFailure(RuntimeError):
    pass


def require(condition: object, message: object) -> None:
    if bool(condition):
        return
    raise VerificationFailure(str(message))


def F(value: object) -> Q:
    return Q(str(value))


def fstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def dot(left: Sequence[Q], right: Sequence[Q]) -> Q:
    return sum((x * y for x, y in zip(left, right, strict=True)), Q(0))


def subset_name(mask: int) -> str:
    return "".join(str(i + 1) for i in range(N) if mask & (1 << i)) or "empty"


def members(mask: int) -> tuple[int, ...]:
    return tuple(i for i in range(N) if mask & (1 << i))


def displacement(mask: int, p: Sequence[Q]) -> tuple[Q, ...]:
    return tuple(Q(1 if mask & (1 << i) else 0) - p[i] for i in range(N))


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
    return tuple(item for item in items if not any(item != other and is_subset(item, other) for other in items))


def minimal_nonmembers(family_mask: int) -> tuple[int, ...]:
    items = [item for item in SUBSETS if not (family_mask & (1 << item))]
    return tuple(item for item in items if not any(item != other and is_subset(other, item) for other in items))


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


def verify_max_lp_certificate(
    *,
    G: Sequence[Sequence[Q]],
    h: Sequence[Q],
    E: Sequence[Sequence[Q]],
    f: Sequence[Q],
    c: Sequence[Q],
    labels: Sequence[str],
    certificate: dict[str, object],
) -> Q:
    primal = tuple(F(value) for value in certificate["primal"])  # type: ignore[index]
    active = tuple(int(value) for value in certificate["active_indices"])  # type: ignore[index]
    dual_active = tuple(F(value) for value in certificate["dual_active"])  # type: ignore[index]
    dual_equalities = tuple(F(value) for value in certificate["dual_equalities"])  # type: ignore[index]
    require(len(primal) == len(c), "primal dimension")
    require(len(active) == len(dual_active), "dual support")
    require(len(E) == len(f) == len(dual_equalities), "dual equality length")
    require(list(certificate["active_labels"]) == [labels[index] for index in active], "active label mismatch")  # type: ignore[index]

    for row, bound in zip(G, h, strict=True):
        require(dot(row, primal) <= bound, ("primal inequality", row, bound, primal))
    for row, bound in zip(E, f, strict=True):
        require(dot(row, primal) == bound, ("primal equality", row, bound, primal))
    require(all(value >= 0 for value in dual_active), "negative dual")

    lhs = [Q(0) for _ in c]
    for index, multiplier in zip(active, dual_active, strict=True):
        for variable, coefficient in enumerate(G[index]):
            lhs[variable] += multiplier * coefficient
    for row, multiplier in zip(E, dual_equalities, strict=True):
        for variable, coefficient in enumerate(row):
            lhs[variable] += multiplier * coefficient
    require(tuple(lhs) == tuple(c), ("dual equality", lhs, c))

    primal_value = dot(primal, c)
    dual_value = sum((h[index] * multiplier for index, multiplier in zip(active, dual_active, strict=True)), Q(0))
    dual_value += sum((bound * multiplier for bound, multiplier in zip(f, dual_equalities, strict=True)), Q(0))
    require(primal_value == dual_value, ("strong duality", primal_value, dual_value))
    require(primal_value == F(certificate["objective"]), "stored objective mismatch")
    return primal_value


def good_feasibility_lp(family_mask: int, p: Sequence[Q]):
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
        G.append([Q(-value) for value in v] + [Q(-1)])
        h.append(Q(0))
        labels.append(f"relaxed_good_{subset_name(mask)}")
    E = [[Q(1), Q(1), Q(1), Q(1), Q(0)]]
    f = [Q(1)]
    c = [Q(0), Q(0), Q(0), Q(0), Q(-1)]
    return G, h, E, f, c, labels


def margin_lp(family_mask: int, p: Sequence[Q], kappa: Q | None = None):
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
            G.append(list(v) + [Q(1)])
            h.append(Q(0))
            labels.append(f"bad_{subset_name(mask)}")
        else:
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


def kappa_lp(family_mask: int, p: Sequence[Q]):
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
    return G, h, [], [], [Q(0), Q(0), Q(0), Q(0), Q(-1)], labels


def union_cover_dp(pattern_masks: Sequence[int], max_scenarios: int):
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
            require(previous is not None, "missing cover predecessor")
            for pattern in pattern_masks:
                merged = union_mask | pattern
                if distance[merged] > step:
                    distance[merged] = step
                    witness[merged] = previous + (pattern,)
                    new_frontier.add(merged)
        frontier = new_frontier
    return distance, witness


def best_cover_for_target(target: int, pattern_masks: Sequence[int], max_scenarios: int):
    distance, witness = union_cover_dp(pattern_masks, max_scenarios)
    best = None
    for union_mask, count in enumerate(distance):
        if count > max_scenarios or target & ~union_mask:
            continue
        row = witness[union_mask]
        require(row is not None, "missing cover witness")
        if best is None or count < best[0] or (count == best[0] and row < best[1]):
            best = (count, row)
    return best


def target_below(value: Q, route_values: dict[int, Q]) -> int:
    return sum(1 << mask for mask, route in route_values.items() if route < value)


def available(record: dict[str, object], kappa: Q) -> bool:
    if not record["realizable"]:
        return False
    threshold = F(record["kappa_infimum"])
    return kappa > threshold or (kappa == threshold and bool(record["attained_at_infimum"]))


def robust_value(records, route_values, kappa: Q, scenarios: int):
    patterns = [int(record["mask_hex"], 16) for record in records if available(record, kappa)]
    best_value = min(route_values.values())
    best_witness: tuple[int, ...] = tuple()
    for level in sorted(set(route_values.values())):
        result = best_cover_for_target(target_below(level, route_values), patterns, scenarios)
        if result is not None:
            best_value = level
            best_witness = result[1]
    return best_value, best_witness


def scenario_bad_mask(weights: Sequence[Q], p: Sequence[Q]) -> int:
    threshold = dot(weights, p)
    return sum(1 << mask for mask in SUBSETS if sum((weights[i] for i in members(mask)), Q(0)) < threshold)


def common_feasible(scenarios: Sequence[Sequence[Q]], p: Sequence[Q]) -> tuple[int, ...]:
    return tuple(mask for mask in SUBSETS if all(dot(weights, displacement(mask, p)) >= 0 for weights in scenarios))


def stable_hash_without_field(payload: dict[str, object]) -> str:
    copy = dict(payload)
    expected = copy.pop("content_sha256")
    encoded = json.dumps(copy, sort_keys=True, separators=(",", ":")).encode("utf-8")
    actual = hashlib.sha256(encoded).hexdigest()
    require(actual == expected, ("content hash", actual, expected))
    return actual


def verify_payload(payload: dict[str, object], *, verbose: bool = True) -> dict[str, object]:
    stable_hash_without_field(payload)
    require(payload["schema"] == "ssuf-scenario-cover-atlas-v1", "schema")
    fixed = payload["fixed_instance"]
    require(tuple(F(value) for value in fixed["p"]) == P, "p")  # type: ignore[index]
    require(tuple(F(value) for value in fixed["d"]) == D, "d")  # type: ignore[index]

    route_values = {mask: route_value(mask, P, D) for mask in SUBSETS}
    stored_routes = fixed["route_values"]  # type: ignore[index]
    require({subset_name(mask): fstr(value) for mask, value in route_values.items()} == stored_routes, "route table")

    downsets = [mask for mask in range(1 << 16) if is_downset(mask)]
    require(len(downsets) == 168, "downset count")
    records = payload["patterns"]
    require(len(records) == len(downsets), "record count")  # type: ignore[arg-type]

    realized: list[dict[str, object]] = []
    for expected_mask, record in zip(downsets, records, strict=True):  # type: ignore[arg-type]
        mask = int(record["mask_hex"], 16)
        require(mask == expected_mask, ("mask ordering", mask, expected_mask))
        require(record["maximal_bad_sets"] == [subset_name(item) for item in maximal_members(mask)], "maximal bad sets")
        require(record["minimal_accepted_sets"] == [subset_name(item) for item in minimal_nonmembers(mask)], "minimal accepted sets")

        G0, h0, E0, f0, c0, labels0 = good_feasibility_lp(mask, P)
        good_value = verify_max_lp_certificate(
            G=G0, h=h0, E=E0, f=f0, c=c0, labels=labels0,
            certificate=record["good_feasibility_certificate"],
        )
        min_slack = -good_value
        require(min_slack == F(record["minimum_good_slack"]), "good slack")

        if min_slack > 0:
            require(record["realizable"] is False, "infeasible pattern marked realized")
            continue

        G, h, E, f, c, labels = margin_lp(mask, P)
        margin = verify_max_lp_certificate(
            G=G, h=h, E=E, f=f, c=c, labels=labels,
            certificate=record["margin_certificate"],
        )
        require(bool(record["realizable"]) == (margin > 0), "realizability classification")
        if margin <= 0:
            continue

        Gk, hk, Ek, fk, ck, klabels = kappa_lp(mask, P)
        kappa_objective = verify_max_lp_certificate(
            G=Gk, h=hk, E=Ek, f=fk, c=ck, labels=klabels,
            certificate=record["kappa_certificate"],
        )
        kappa = -kappa_objective
        require(kappa == F(record["kappa_infimum"]), "kappa infimum")
        require(kappa >= 1, "kappa below one")

        Ga, ha, Ea, fa, ca, alabels = margin_lp(mask, P, kappa=kappa)
        attained_margin = verify_max_lp_certificate(
            G=Ga, h=ha, E=Ea, f=fa, c=ca, labels=alabels,
            certificate=record["attainment_certificate"],
        )
        require(bool(record["attained_at_infimum"]) == (attained_margin > 0), "attainment flag")
        realized.append(record)

    require(len(realized) == 59, len(realized))
    require(len({F(record["kappa_infimum"]) for record in realized}) == 32, "kappa level count")

    pattern_masks = [int(record["mask_hex"], 16) for record in realized]
    distance, witnesses = union_cover_dp(pattern_masks, 4)
    sup_distance = distance[:]
    for bit in range(16):
        for mask in range((1 << 16) - 1, -1, -1):
            if mask & (1 << bit):
                continue
            sup_distance[mask] = min(sup_distance[mask], sup_distance[mask | (1 << bit)])
    distribution: Counter[str] = Counter()
    four_needed = []
    impossible = []
    for mask in downsets:
        if sup_distance[mask] <= 4:
            distribution[str(sup_distance[mask])] += 1
            if sup_distance[mask] == 4:
                four_needed.append(mask)
        else:
            distribution["impossible"] += 1
            impossible.append(mask)
    expected_distribution = {"0": 1, "1": 61, "2": 91, "3": 13, "4": 1, "impossible": 1}
    require(dict(sorted(distribution.items())) == expected_distribution, distribution)
    require(four_needed == [0x7FFF], four_needed)
    require(impossible == [0xFFFF], impossible)
    require(payload["atlas_summary"]["cover_number_distribution_over_all_downsets"] == expected_distribution, "stored distribution")  # type: ignore[index]

    # Unrestricted values use all 59 patterns.
    unrestricted = payload["unrestricted_fixed_instance_values"]
    expected_unrestricted = {1: Q(561, 500), 2: Q(1061, 500), 3: Q(2123, 1000), 4: Q(359, 125)}
    for scenarios, expected in expected_unrestricted.items():
        best = min(route_values.values())
        witness = tuple()
        for level in sorted(set(route_values.values())):
            result = best_cover_for_target(target_below(level, route_values), pattern_masks, scenarios)
            if result is not None:
                best = level
                witness = result[1]
        require(best == expected, ("unrestricted", scenarios, best, expected))
        require(F(unrestricted[str(scenarios)]["value"]) == expected, "stored unrestricted value")  # type: ignore[index]
        require(unrestricted[str(scenarios)]["cover"] == [f"0x{mask:04x}" for mask in witness], "stored unrestricted cover")  # type: ignore[index]

    # Finite original and improved scenarios.
    finite = payload["finite_witness"]
    original = tuple(tuple(F(value) for value in row) for row in finite["original_scenarios"])  # type: ignore[index]
    improved = tuple(tuple(F(value) for value in row) for row in finite["improved_integer_scenarios"])  # type: ignore[index]
    expected_feasible = (0b0111, 0b1011, 0b1110, 0b1111)
    require(common_feasible(original, P) == expected_feasible, "original feasible family")
    require(common_feasible(improved, P) == expected_feasible, "improved feasible family")
    require(min(route_values[mask] for mask in expected_feasible) == Q(1061, 500), "finite objective")
    require(scenario_bad_mask(improved[0], P) == 0x3333, "center mask")
    require(scenario_bad_mask(improved[1], P) == 0x055F, "triangle mask")

    # Every stored phase probe is recomputed from exact pattern availability.
    phases = payload["bounded_phase_diagrams"]
    for probe_name, row in phases["probes"].items():  # type: ignore[index]
        kappa = F(row["kappa"])
        for scenarios in (1, 2, 3, 4):
            value, witness = robust_value(records, route_values, kappa, scenarios)
            require(F(row[f"m{scenarios}_value"]) == value, (probe_name, scenarios, value))
            require(row[f"m{scenarios}_cover"] == [f"0x{mask:04x}" for mask in witness], (probe_name, scenarios, witness))

    # Direct arithmetic checks for the general epsilon star-triangle theorem.
    for sample in payload["symbolic_cover_recovery"]["exact_epsilon_samples"]:  # type: ignore[index]
        epsilon = F(sample["epsilon"])
        center = Q(2) * (Q(1) - epsilon) / epsilon
        triangle = (Q(1) - epsilon) / (Q(2) * epsilon)
        require(F(sample["center_infimum"]) == center, "center sample")
        require(F(sample["triangle_infimum"]) == triangle, "triangle sample")
        require(center == Q(4) * triangle, "four-to-one sample")

    summary = {
        "content_sha256": payload["content_sha256"],
        "downsets": 168,
        "realizable_patterns": 59,
        "kappa_levels": 32,
        "cover_distribution": expected_distribution,
        "status": "PASS",
    }
    if verbose:
        print("PASS content hash and schema")
        print("PASS exact 16-route / 13-deviation reconstruction")
        print("PASS all rational primal-dual LP certificates")
        print("PASS 168-downset / 59-pattern / 32-kappa-level census")
        print("PASS exact cover dynamic programs and phase probes")
        print("PASS original and improved two-scenario finite certificates")
        print("PASS epsilon star-triangle arithmetic samples")
        print("ALL SCENARIO-COVER RESULTS VERIFIED")
    return summary


def main() -> None:
    payload = json.loads(DEFAULT_PATH.read_text(encoding="utf-8"))
    verify_payload(payload)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}")
        raise
