#!/usr/bin/env python3
"""Check public-package hygiene and report intentional publication blockers."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from manifest import check_manifest
from release_metadata import cff_version, require_public_identity, validate_version


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
    "/" "Users/",
    ".codex/" "attachments/",
    "pasted-" "text.txt",
    "authorship and priority " "to be determined",
)
STALE_RELEASE_MARKERS = (
    "v0.1.0-" "rc1",
    "private, " "unpublished",
    "private and " "unpublished",
    "release " "candidate",
    "dra" "ft release notes",
    "proposed " "priority disclosure",
    "proposed " "immutable",
    "potential " "public release",
    "if publication " "is approved",
    "if a public release " "is expressly approved",
    "does not yet establish " "a public priority date",
    "no tag or " "release has been created",
    "moving private " "candidate",
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
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--public",
        action="store_true",
        help="require public metadata, exact CFF-matching tag, and a valid archive",
    )
    mode.add_argument(
        "--candidate-version",
        help="check candidate/dev packaging using a visibly non-final version",
    )
    args = parser.parse_args()
    failures: list[str] = []

    # Hygiene cannot pass while new or changed deliverables are omitted.
    check_manifest()

    for path in files():
        relative = path.relative_to(ROOT)
        if path.name in FORBIDDEN_NAMES:
            failures.append(f"internal review file present: {relative}")
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        controls = sorted(
            {
                ord(character)
                for character in text
                if ord(character) < 32 and character not in "\t\n\r"
            }
        )
        if controls:
            failures.append(f"C0 control characters in {relative}: {controls}")
        for token in FORBIDDEN_TEXT:
            if token in text:
                failures.append(f"forbidden placeholder/private path in {relative}: {token}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f"possible secret in {relative}: {pattern.pattern}")

    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if args.public:
        version = cff_version(ROOT)
        for path in files():
            if path.resolve() == Path(__file__).resolve():
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            for marker in STALE_RELEASE_MARKERS:
                if marker in text:
                    failures.append(
                        f"stale pre-publication language in {path.relative_to(ROOT)}: {marker}"
                    )
        if "date-released:" not in cff:
            failures.append(f"CITATION.cff is not finalized as dated version {version}")
        if re.search(r"(?m)^license:", cff):
            failures.append("CITATION.cff asserts a license despite the deliberate no-license status")
        licensing = (ROOT / "LICENSING.md").read_text(encoding="utf-8")
        normalized_licensing = " ".join(licensing.split())
        if "grants no open-source or open-content license" not in normalized_licensing:
            failures.append("LICENSING.md does not state the deliberate no-license status")

        try:
            require_public_identity(ROOT)
        except SystemExit as error:
            failures.append(str(error))
    elif args.candidate_version:
        try:
            validate_version(args.candidate_version, candidate=True)
        except SystemExit as error:
            failures.append(str(error))

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit("release preflight failed")

    print(f"PACKAGE HYGIENE PASS: {len(files())} files scanned")
    print("PASS: no institutional affiliation or operative license is asserted.")
    if args.public or args.candidate_version:
        build_mode = "public" if args.public else "candidate"
        command = [
            sys.executable,
            os.fspath(ROOT / "scripts" / "build_release.py"),
            "--mode",
            build_mode,
        ]
        if args.candidate_version:
            command.extend(["--version", args.candidate_version])
        with tempfile.TemporaryDirectory(prefix="ssuf-package-preflight-") as tmp_name:
            command.extend(["--output-dir", tmp_name])
            subprocess.run(command, cwd=ROOT, check=True)
        print(f"{build_mode.upper()} ARCHIVE PREFLIGHT PASS")
    else:
        print("BASELINE PREFLIGHT PASS")


if __name__ == "__main__":
    main()
