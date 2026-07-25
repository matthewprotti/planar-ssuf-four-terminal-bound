#!/usr/bin/env python3
"""Generate representative finite census witnesses for human inspection."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    census = json.loads((HERE / "threshold_family_census.json").read_text(encoding="utf-8"))
    reconciliation = json.loads(
        (HERE / "census_reconciliation_results.json").read_text(encoding="utf-8")
    )
    by_id = {row["id"]: row for row in census["realizable_families"]}
    every_id = census["every_pair_cell"]["family_id"]
    open_id = census["unequal_candidate_family_ids"][0]
    payload = {
        "status": "PASS",
        "ambient_partition": reconciliation["ambient_partition"],
        "realizable_partition": reconciliation["search_partition"],
        "every_pair_positive_threshold_witness": by_id[every_id],
        "one_remaining_labeled_cell": by_id[open_id],
        "one_nonthreshold_two_trade": census["nonthreshold_trade_certificates"][0],
        "empty_family_obstruction": census["empty_family_certificate"],
        "interpretation": "examples only; complete data remain in threshold_family_census.json",
    }
    output = HERE / "witness_examples.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
