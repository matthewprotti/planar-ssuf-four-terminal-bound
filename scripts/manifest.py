#!/usr/bin/env python3
"""Write or verify the repository SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "SHA256SUMS.txt"
EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "build", "dist"}
EXCLUDED_NAMES = {MANIFEST.name, ".DS_Store"}
EXCLUDED_SUFFIXES = {".aux", ".log", ".out", ".pyc", ".synctex.gz", ".toc"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def deliverables() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES:
            continue
        if any(path.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES):
            continue
        result.append(path)
    return sorted(result, key=lambda item: item.relative_to(ROOT).as_posix())


def rendered_lines() -> list[str]:
    return [
        f"{digest(path)}  {path.relative_to(ROOT).as_posix()}"
        for path in deliverables()
    ]


def write_manifest() -> None:
    lines = rendered_lines()
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE {MANIFEST.name}: {len(lines)} files")


def check_manifest() -> None:
    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST.name}; run with --write")
    expected = MANIFEST.read_text(encoding="utf-8").splitlines()
    actual = rendered_lines()
    if expected != actual:
        expected_set = set(expected)
        actual_set = set(actual)
        for line in sorted(expected_set - actual_set):
            print(f"MISSING/CHANGED: {line}")
        for line in sorted(actual_set - expected_set):
            print(f"NEW/CHANGED: {line}")
        raise SystemExit("manifest verification failed")
    print(f"MANIFEST PASS: {len(actual)} files")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="replace the manifest")
    args = parser.parse_args()
    if args.write:
        write_manifest()
    else:
        check_manifest()


if __name__ == "__main__":
    main()
