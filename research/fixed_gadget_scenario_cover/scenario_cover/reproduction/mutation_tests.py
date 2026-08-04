#!/usr/bin/env python3
"""Mutation-resistance checks for the independent scenario-cover verifier."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from verify_scenario_cover_results import VerificationFailure, verify_payload

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "SCENARIO_COVER_ATLAS_RESULTS.json"


def stable_hash(payload: dict[str, object]) -> str:
    copy = dict(payload)
    copy.pop("content_sha256", None)
    return hashlib.sha256(
        json.dumps(copy, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def seal(payload: dict[str, object]) -> None:
    payload["content_sha256"] = stable_hash(payload)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def expect_rejection(name: str, payload: dict[str, object]) -> str:
    seal(payload)
    try:
        verify_payload(payload, verbose=False)
    except VerificationFailure as exc:
        return f"PASS {name}: {exc}"
    raise RuntimeError(f"mutation survived: {name}")


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    messages: list[str] = []

    mutated = deepcopy(source)
    mutated["fixed_instance"]["route_values"]["124"] = "999"  # type: ignore[index]
    messages.append(expect_rejection("route-value corruption", mutated))

    mutated = deepcopy(source)
    realized = next(record for record in mutated["patterns"] if record["realizable"])  # type: ignore[index]
    realized["kappa_certificate"]["objective"] = "-999999"  # type: ignore[index]
    messages.append(expect_rejection("LP-objective corruption", mutated))

    mutated = deepcopy(source)
    mutated["patterns"].pop()  # type: ignore[index]
    messages.append(expect_rejection("pattern deletion", mutated))

    mutated = deepcopy(source)
    mutated["bounded_phase_diagrams"]["probes"]["after_C"]["m2_value"] = "1"  # type: ignore[index]
    messages.append(expect_rejection("phase-diagram corruption", mutated))

    for message in messages:
        print(message)
    require(len(messages) == 4, "mutation count")
    print("ALL FOUR MUTATIONS REJECTED")


if __name__ == "__main__":
    main()
