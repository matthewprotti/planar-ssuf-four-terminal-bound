#!/usr/bin/env python3
"""Exact checks for the signed single-generator fixed-topology theorem."""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path

N = 4
FULL = (1 << N) - 1
ARCS = tuple(range(5))
SUPPORTS = (
    frozenset({0, 1, 2}),
    frozenset({0, 1, 2, 3, 4}),
    frozenset({1, 2, 3, 4}),
    frozenset({2, 3}),
)


def subsets_of_size_at_least_two():
    for size in range(2, N + 1):
        for combo in combinations(range(N), size):
            mask = sum(1 << i for i in combo)
            yield mask


def oriented(mask: int, signs: tuple[int, ...]) -> int:
    """Map historical C-route indicator z to oriented positive-threshold u."""
    result = 0
    for i, sign in enumerate(signs):
        z = bool(mask & (1 << i))
        u = z if sign > 0 else not z
        if u:
            result |= 1 << i
    return result


def subset_weight(mask: int, weights: tuple[Q, ...]) -> Q:
    return sum((weights[i] for i in range(N) if mask & (1 << i)), Q(0))


def physical_parameters(
    generator: int, signs: tuple[int, ...], epsilon: Q, delta: Q
) -> tuple[tuple[Q, ...], tuple[Q, ...], Q]:
    """Return signed k, historical-C fractions p, and oriented threshold."""
    members = [i for i in range(N) if generator & (1 << i)]
    j = members[0]
    w = tuple(Q(1) if i in members else delta for i in range(N))
    q = tuple(epsilon if i == j else Q(1) for i in range(N))
    theta = sum((w[i] * q[i] for i in range(N)), Q(0))
    k = tuple(Q(signs[i]) * w[i] for i in range(N))
    p = tuple(q[i] if signs[i] > 0 else 1 - q[i] for i in range(N))
    return k, p, theta


def cost_feasible(mask: int, k: tuple[Q, ...], p: tuple[Q, ...]) -> bool:
    return sum((k[i] * ((1 if mask & (1 << i) else 0) - p[i]) for i in range(N)), Q(0)) >= 0


def route_max(mask: int, d: tuple[Q, ...], p: tuple[Q, ...]) -> Q:
    maximum = Q(0)
    for arc in ARCS:
        deviation = sum(
            (
                d[i] * ((1 if mask & (1 << i) else 0) - p[i])
                for i in range(N)
                if arc in SUPPORTS[i]
            ),
            Q(0),
        )
        maximum = max(maximum, deviation)
    # Both routes have one private terminal arc in the fixed topology.
    for i in range(N):
        z = bool(mask & (1 << i))
        private = d[i] * ((1 - p[i]) if z else p[i])
        maximum = max(maximum, private)
    return maximum


def expected_oriented_family(generator: int) -> frozenset[int]:
    return frozenset(mask for mask in range(16) if mask & generator == generator)


def main() -> None:
    epsilon = Q(1, 1000)
    delta = Q(1, 1000)
    records = []
    representations = 0
    for generator in subsets_of_size_at_least_two():
        members = [i for i in range(N) if generator & (1 << i)]
        assert epsilon + (N - len(members)) * delta < 1
        for signs in product((-1, 1), repeat=N):
            k, p, theta = physical_parameters(generator, signs, epsilon, delta)
            w = tuple(abs(value) for value in k)
            oriented_family = frozenset(
                oriented(mask, signs) for mask in range(16) if cost_feasible(mask, k, p)
            )
            assert oriented_family == expected_oriented_family(generator)
            assert theta == sum(
                w[i] * (p[i] if signs[i] > 0 else 1 - p[i]) for i in range(N)
            )

            # The theorem's explicit feasible route: generator plus all negative
            # oriented coordinates. Convert it back to historical C choices.
            u = generator | sum(1 << i for i, sign in enumerate(signs) if sign < 0)
            z = 0
            for i, sign in enumerate(signs):
                ui = bool(u & (1 << i))
                zi = ui if sign > 0 else not ui
                if zi:
                    z |= 1 << i
            assert cost_feasible(z, k, p)

            # Matching lower witness: the first generator coordinate is forced in
            # oriented state u=1, hence its appropriate private route deviation is
            # exactly 1-epsilon under unit demand.
            j = members[0]
            d = tuple(Q(1) if i == j else Q(1, 2) for i in range(N))
            feasible = [mask for mask in range(16) if cost_feasible(mask, k, p)]
            optimum = min(route_max(mask, d, p) for mask in feasible)
            assert optimum >= 1 - epsilon
            explicit_upper = route_max(z, d, p)
            assert explicit_upper <= 1
            representations += 1
            records.append(
                {
                    "generator": [i + 1 for i in members],
                    "signs": list(signs),
                    "feasible_route_historical_C_mask": z,
                    "exact_lower_witness": str(optimum),
                    "explicit_upper_route_max": str(explicit_upper),
                }
            )

    assert representations == 11 * 16 == 176

    # Zero-coordinate boundary examples: zeros can occur only outside the
    # generator. They are cost-free and can be routed historically E to avoid
    # positive trunk deviation. The forced generator coordinate still supplies
    # the matching private-arc lower witness.
    zero_examples = 0
    for generator in subsets_of_size_at_least_two():
        outside = [i for i in range(N) if not generator & (1 << i)]
        if not outside:
            continue
        zero = outside[0]
        members = [i for i in range(N) if generator & (1 << i)]
        j = members[0]
        signs = tuple(1 for _ in range(N))
        k, p, _ = physical_parameters(generator, signs, epsilon, delta)
        k = tuple(Q(0) if i == zero else k[i] for i in range(N))
        p = tuple(Q(1, 2) if i == zero else p[i] for i in range(N))
        feasible = [mask for mask in range(16) if cost_feasible(mask, k, p)]
        assert all(mask & (1 << j) for mask in feasible)
        d = tuple(Q(1) if i == j else Q(1, 2) for i in range(N))
        assert min(route_max(mask, d, p) for mask in feasible) >= 1 - epsilon
        zero_examples += 1
    assert zero_examples == 10

    result = {
        "status": "PASS",
        "nonzero_signed_representations": representations,
        "positive_threshold_generators": 11,
        "sign_patterns": 16,
        "zero_outside_generator_examples": zero_examples,
        "epsilon": str(epsilon),
        "delta": str(delta),
        "records_sha_basis_count": len(records),
        "nonclaims": [
            "does not cover multiple-generator oriented cells",
            "does not solve arbitrary zero-coordinate strata",
            "does not imply a global signed-cost optimum",
        ],
    }
    target = Path(__file__).with_name("signed_single_generator_results.json")
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: 11 generators x 16 nonzero sign patterns = 176 exact value-one regimes")
    print("PASS: exact rational lower witnesses and explicit upper routes check on every regime")
    print("PASS: 10 representative zero-outside-generator boundary strata check")
    print(f"WROTE: {target}")


if __name__ == "__main__":
    main()
