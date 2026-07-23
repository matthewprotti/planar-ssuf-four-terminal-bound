#!/usr/bin/env python3
"""Negative tests for the concrete verifier.

Each mutation changes one claimed datum and must be rejected.  A passing test
suite demonstrates that the verifier is not merely executing its happy path.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tempfile

from verify_concrete_instance import (
    DEFAULT_INSTANCE,
    EXPECTED,
    ExpectedData,
    InstanceData,
    VerificationError,
    verify_instance,
)


def expect_failure(label: str, data: InstanceData, expected: ExpectedData = EXPECTED) -> None:
    try:
        with tempfile.TemporaryDirectory() as tmp:
            verify_instance(data=data, expected=expected, output_dir=Path(tmp))
    except VerificationError as exc:
        print(f"PASS mutation [{label}] rejected: {exc}")
        return
    raise AssertionError(f"mutation [{label}] was not rejected")


def main() -> None:
    # Baseline must pass before negative tests mean anything.
    with tempfile.TemporaryDirectory() as tmp:
        verify_instance(output_dir=Path(tmp))
    print("PASS baseline certificate accepted.")

    # 1. Change one trunk endpoint.
    arcs = list(DEFAULT_INSTANCE.arcs)
    old_arc = arcs[3]
    new_arc = ("v3", "v5")
    arcs[3] = new_arc
    trunk = list(DEFAULT_INSTANCE.trunk)
    trunk[3] = new_arc
    costs = dict(DEFAULT_INSTANCE.costs)
    costs[new_arc] = costs.pop(old_arc)
    expect_failure(
        "trunk endpoint",
        replace(DEFAULT_INSTANCE, arcs=tuple(arcs), trunk=tuple(trunk), costs=costs),
    )

    # 2. Change one fractional path amount.
    amounts = dict(DEFAULT_INSTANCE.cheap_amounts)
    amounts["t2"] += 1
    expect_failure(
        "path amount",
        replace(DEFAULT_INSTANCE, cheap_amounts=amounts),
    )

    # 3. Change one charged per-unit arc cost.
    costs = dict(DEFAULT_INSTANCE.costs)
    costs[("v1", "t3")] += 1
    expect_failure(
        "arc cost",
        replace(DEFAULT_INSTANCE, costs=costs),
    )

    # 4. Change one rotation order while preserving the neighbor set.
    rotation = dict(DEFAULT_INSTANCE.rotation)
    rotation["v3"] = ("v2", "v4", "t1")
    expect_failure(
        "rotation order",
        replace(DEFAULT_INSTANCE, rotation=rotation),
    )

    # 5. Corrupt one K4 branch set so that it overlaps another.
    branch_sets = dict(DEFAULT_INSTANCE.k4_branch_sets)
    branch_sets["D"] = frozenset({"v4"})
    expect_failure(
        "K4 branch set",
        replace(DEFAULT_INSTANCE, k4_branch_sets=branch_sets),
    )

    # 6. Change the claimed finite optimum while leaving the instance intact.
    expect_failure(
        "expected overload",
        DEFAULT_INSTANCE,
        replace(EXPECTED, min_max_overload=334, ratio=EXPECTED.ratio),
    )

    print("PASS: all six representative mutations were rejected.")


if __name__ == "__main__":
    main()
