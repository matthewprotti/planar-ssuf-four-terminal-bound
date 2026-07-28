#!/usr/bin/env python3
"""Exact census for nonzero signed route-cost differences on four labels.

A negative difference is handled by complementing that terminal's binary route
coordinate.  This classifies cost-feasible set systems only; the SSUF overload
objective must also flip the corresponding path-difference orientation.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def family(row: dict) -> frozenset[int]:
    bitmask = int(row["family_bitmask_hex"], 16)
    return frozenset(mask for mask in range(16) if bitmask & (1 << mask))


def bitmask(value: frozenset[int]) -> str:
    result = 0
    for mask in value:
        result |= 1 << mask
    return hex(result)


def is_upward_closed(value: frozenset[int]) -> bool:
    return all(
        not ((small & large) == small and small in value and large not in value)
        for small in range(16)
        for large in range(16)
    )


def main() -> None:
    census = json.loads((HERE / "threshold_family_census.json").read_text(encoding="utf-8"))
    representations: dict[frozenset[int], list[dict[str, object]]] = {}
    for row in census["realizable_families"]:
        positive_family = family(row)
        for negative_mask in range(16):
            signed_family = frozenset(
                selected for selected in range(16) if (selected ^ negative_mask) in positive_family
            )
            representations.setdefault(signed_family, []).append(
                {
                    "positive_family_id": row["id"],
                    "negative_coordinate_mask": hex(negative_mask),
                    "negative_coordinates": [
                        index + 1 for index in range(4) if negative_mask & (1 << index)
                    ],
                    "integer_absolute_weights": row["integer_weights"],
                    "transformed_integer_threshold": row["integer_threshold"],
                }
            )

    rows = []
    for index, (signed_family, reps) in enumerate(
        sorted(representations.items(), key=lambda item: bitmask(item[0])), start=1
    ):
        rows.append(
            {
                "id": f"S{index:04d}",
                "family_bitmask_hex": bitmask(signed_family),
                "number_of_feasible_sets": len(signed_family),
                "upward_closed_in_original_cheap_coordinates": is_upward_closed(signed_family),
                "number_of_signed_representations": len(reps),
                "representations": reps,
            }
        )

    summary = {
        "scope": "four labels; every route-cost difference nonzero; feasibility classification only",
        "positive_threshold_families": len(census["realizable_families"]),
        "sign_patterns": 16,
        "raw_positive_family_sign_pairs": len(census["realizable_families"]) * 16,
        "unique_signed_unate_threshold_families": len(rows),
        "upward_closed_original_coordinate_families": sum(
            row["upward_closed_in_original_cheap_coordinates"] for row in rows
        ),
        "representation_multiplicity": dict(
            sorted(Counter(row["number_of_signed_representations"] for row in rows).items())
        ),
        "families": rows,
    }
    assert summary["unique_signed_unate_threshold_families"] == 1881
    assert summary["upward_closed_original_coordinate_families"] == 149
    output = HERE / "signed_difference_census.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: 149 positive threshold families x 16 sign patterns")
    print("PASS: 1881 unique nonzero signed/unate threshold families")
    print("PASS: exactly 149 remain upward closed in the original cheap coordinates")
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
