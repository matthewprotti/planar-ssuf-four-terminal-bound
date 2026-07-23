#!/usr/bin/env python3
"""Check public-package hygiene and report intentional publication blockers."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {".cff", ".csv", ".json", ".md", ".py", ".tex", ".txt", ".yml", ".yaml"}
EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "build", "dist"}
FORBIDDEN_NAMES = {
    "CODEX_PUBLISH_PROMPT.md",
    "NEXT_ADVERSARIAL_REVIEW_PROMPT.md",
    "NOVELTY_PRIORITY_STATUS.md",
    "RESPONSE_TO_SECOND_REVIEW.md",
}
FORBIDDEN_TEXT = (
    "[FULL " "LEGAL NAME]",
    "[GITHUB-" "OWNER]",
    "[SUR" "NAME]",
    "[GIVEN " "NAMES]",
    "/" "Users/" "matthew/.codex/attachments/",
    "pasted-" "text.txt",
    "authorship and priority " "to be determined",
)
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--public",
        action="store_true",
        help="also require completed rights/licensing and public-ready metadata",
    )
    args = parser.parse_args()
    failures: list[str] = []

    for path in files():
        relative = path.relative_to(ROOT)
        if path.name in FORBIDDEN_NAMES:
            failures.append(f"internal review file present: {relative}")
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in FORBIDDEN_TEXT:
            if token in text:
                failures.append(f"forbidden placeholder/private path in {relative}: {token}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f"possible secret in {relative}: {pattern.pattern}")

    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if args.public:
        if "Unpublished private release candidate" in readme:
            failures.append("README still marks the package private and unpublished")
        if re.search(r"(?m)^license:", cff):
            failures.append("CITATION.cff asserts a license despite the deliberate no-license status")
        licensing = (ROOT / "LICENSING.md").read_text(encoding="utf-8")
        if "grants no open-source or open-content license" not in licensing:
            failures.append("LICENSING.md does not state the deliberate no-license status")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit("release preflight failed")

    print(f"PACKAGE HYGIENE PASS: {len(files())} files scanned")
    print("PASS: no institutional affiliation or operative license is asserted.")
    if not args.public:
        print("PRIVATE-CANDIDATE PREFLIGHT PASS")


if __name__ == "__main__":
    main()
