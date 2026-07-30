#!/usr/bin/env python3
"""Build or verify the package SHA-256 manifest.

Every regular package artifact, including the frozen replay transcript, is
hashed. MANIFEST.sha256 alone is excluded because a file cannot contain its own
stable digest.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

EXCLUDED = {"MANIFEST.sha256"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def rows(root: Path) -> list[str]:
    result: list[str] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if (
            relative in EXCLUDED
            or "__pycache__" in path.parts
            or relative.endswith(".pyc")
            or relative.endswith(".zip")
        ):
            continue
        result.append(f"{digest(path)}  {relative}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = root / "MANIFEST.sha256"
    current = rows(root)
    if args.check:
        stored = manifest.read_text(encoding="utf-8").splitlines()
        assert stored == current, "manifest mismatch"
        assert any(row.endswith("  REPLAY_REPORT.txt") for row in stored)
        print(f"PASS: authenticated {len(current)} artifact hashes in MANIFEST.sha256")
    else:
        manifest.write_text("\n".join(current) + "\n", encoding="utf-8")
        print(
            f"WROTE: {manifest.name} "
            f"({len(current)} artifacts; replay transcript included)"
        )


if __name__ == "__main__":
    main()
