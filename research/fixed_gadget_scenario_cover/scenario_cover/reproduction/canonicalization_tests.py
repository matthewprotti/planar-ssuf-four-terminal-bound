#!/usr/bin/env python3
"""Regression tests for environment-independent exact LP certificates."""

from __future__ import annotations

from fractions import Fraction as Q
import json

from scenario_cover_atlas import (
    canonical_certificate_at_value,
    parse_fraction,
    require,
    verify_max_lp_certificate,
)


def main() -> None:
    # Maximize x+y over the unit simplex.  The full optimal edge has objective
    # one, and the endpoint bases (1,0) and (0,1) are both valid exact solver
    # proposals.  Canonical selection must ignore which endpoint was proposed.
    G = [
        [Q(1), Q(0)],
        [Q(0), Q(1)],
        [Q(1), Q(1)],
        [Q(-1), Q(0)],
        [Q(0), Q(-1)],
    ]
    h = [Q(1), Q(1), Q(1), Q(0), Q(0)]
    E: list[list[Q]] = []
    f: list[Q] = []
    c = [Q(1), Q(1)]

    left_value = verify_max_lp_certificate(
        G=G,
        h=h,
        E=E,
        f=f,
        c=c,
        primal=[Q(1), Q(0)],
        active=[0, 2],
        dual_active=[Q(0), Q(1)],
        dual_equalities=[],
    )
    right_value = verify_max_lp_certificate(
        G=G,
        h=h,
        E=E,
        f=f,
        c=c,
        primal=[Q(0), Q(1)],
        active=[1, 2],
        dual_active=[Q(0), Q(1)],
        dual_equalities=[],
    )
    require(left_value == right_value == Q(1), "alternative exact optima")

    from_left = canonical_certificate_at_value(
        G=G, h=h, E=E, f=f, c=c, value=left_value, label="toy-left"
    )
    from_right = canonical_certificate_at_value(
        G=G, h=h, E=E, f=f, c=c, value=right_value, label="toy-right"
    )
    require(from_left == from_right, "proposal-dependent canonical certificate")
    require(from_left["primal"] == ["0", "1"], from_left)
    require(from_left["active_indices"] == [1, 2], from_left)
    require(parse_fraction(from_left["objective"]) == Q(1), from_left)

    encoded = json.dumps(from_left, sort_keys=True, separators=(",", ":"))
    require("." not in encoded, "floating-point token in canonical certificate")
    print("PASS alternative exact proposal bases canonicalize identically")
    print(encoded)


if __name__ == "__main__":
    main()
