#!/usr/bin/env python3
"""Exact rational SC-006 replay against the complete 168-downset atlas."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q

from scenario_cover_atlas import (
    D,
    SUBSETS,
    exact_pattern_record,
    is_downset,
    robust_value_at_kappa,
    route_value,
)

def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


QUICK = (Q(1, 1000), Q(1, 16), Q(1, 10))
FULL = (
    Q(1, 10000),
    Q(1, 1000),
    Q(1, 257),
    Q(1, 100),
    Q(1, 50),
    Q(1, 17),
    Q(1, 16),
    Q(17, 256),
    Q(3, 40),
    Q(1, 20),
    Q(1, 10),
    Q(7, 64),
    Q(31, 250),
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    samples = FULL if args.full else QUICK

    downsets = tuple(mask for mask in range(1 << 16) if is_downset(mask))
    require(len(downsets) == 168, ("downset count", len(downsets)))

    for epsilon in samples:
        p = (
            Q(1, 4) + epsilon,
            epsilon,
            Q(1, 2),
            Q(1, 4) + epsilon,
        )
        route_values = {mask: route_value(mask, p, D) for mask in SUBSETS}
        # SC-006 consumes only exact realizability, kappa thresholds, endpoint
        # attainment, and robust values. Canonical certificate serialization is
        # separately checked for the fixed atlas and would add no evidence here.
        # Disabling it preserves the accepted R3D computation while keeping the
        # continuum replay practical in clean release environments.
        records = [
            exact_pattern_record(mask, p, canonical_certificates=False)
            for mask in downsets
        ]

        A = (Q(3) - Q(4) * epsilon) / (Q(1) + Q(2) * epsilon)
        B = Q(1) / epsilon - Q(2)
        C = Q(2) / epsilon - Q(2)
        expected = (
            Q(9, 8) - Q(3) * epsilon,
            Q(9, 8) - Q(2) * epsilon,
            Q(15, 8) - Q(3) * epsilon,
            Q(17, 8) - Q(3) * epsilon,
        )
        probes = (
            (Q(1), expected[0]),
            (A, expected[0]),
            ((A + B) / 2, expected[1]),
            (B, expected[1]),
            ((B + C) / 2, expected[2]),
            (C, expected[2]),
            (C + Q(1), expected[3]),
        )

        for kappa, target in probes:
            value, _ = robust_value_at_kappa(
                records=records,
                route_values=route_values,
                kappa=kappa,
                scenarios=2,
            )
            require(value == target, (epsilon, kappa, value, target))

        print(
            f"PASS epsilon={epsilon}: "
            f"A={A}, B={B}, C={C}, exact four-phase probes"
        )


if __name__ == "__main__":
    main()
