#!/usr/bin/env python3
"""Authenticate every controlling source listed in FULL_PROOF_REVIEW_MAP.md."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "research" / "fixed_gadget_scenario_cover" / "FULL_PROOF_REVIEW_MAP.md"
ROW = re.compile(
    r"^\|[^|]+\| `(?P<path>[^`]+)` \| (?P<lines>[0-9]+) \| "
    r"`(?P<sha>[0-9a-f]{64})` \|"
)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    require(MAP.is_file(), "full-proof review map is missing")
    rows = []
    for line in MAP.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match:
            rows.append(match.groupdict())
    require(len(rows) == 8, f"expected 8 controlling-source rows, observed {len(rows)}")

    for row in rows:
        path = (MAP.parent / row["path"]).resolve()
        require(path.is_relative_to(ROOT), f"proof-map path escapes repository: {path}")
        require(path.is_file() and not path.is_symlink(), f"missing or unsafe proof source: {path}")
        observed_lines = len(path.read_text(encoding="utf-8").splitlines())
        require(
            observed_lines == int(row["lines"]),
            f"line-count mismatch for {path}: {observed_lines} != {row['lines']}",
        )
        observed_sha = digest(path)
        require(
            observed_sha == row["sha"],
            f"SHA-256 mismatch for {path}: {observed_sha} != {row['sha']}",
        )

    print(f"PASS: authenticated {len(rows)} controlling analytic sources from the full-proof map")


if __name__ == "__main__":
    main()
