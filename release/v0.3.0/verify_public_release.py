#!/usr/bin/env python3
"""Verify finalized v0.3.0 metadata, scope fences, and publication hygiene."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {".cff", ".csv", ".json", ".md", ".py", ".tex", ".txt", ".yml", ".yaml"}
EXCLUDED_DIRS = {".git", ".venv", "__pycache__", "build", "dist"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"required file is missing: {relative}")
    return path.read_text(encoding="utf-8")


def public_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and not any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts)
    ]


def main() -> None:
    readme = read("README.md")
    cff = read("CITATION.cff")
    licensing = read("LICENSING.md")
    root_notes = read("RELEASE_NOTES_v0.3.0.md")
    release_notes = read("release/v0.3.0/RELEASE_NOTES.md")
    scope = read("release/v0.3.0/FINAL_SCOPE_LEDGER.md")
    review = read("review_evidence/v0.3.0/README.md")
    research_readme = read("research/fixed_gadget_scenario_cover/README.md")
    claim_ledger = read("research/fixed_gadget_scenario_cover/CLAIM_LEDGER.md")
    proof_map = read("research/fixed_gadget_scenario_cover/FULL_PROOF_REVIEW_MAP.md")
    provenance = read("research/fixed_gadget_scenario_cover/SOURCE_PROVENANCE.json")
    synopsis = read("paper/ssuf_fixed_gadget_scenario_cover_synopsis.tex")

    for token in (
        'version: "0.3.0"',
        "date-released: 2026-08-04",
        'given-names: "Matthew"',
        'family-names: "Protti"',
        "Scenario-Cover Geometry for a Four-Terminal Planar Unsplittable-Flow Gadget",
    ):
        require(token in cff, f"final CITATION.cff token is missing: {token}")
    require(re.search(r"(?m)^license:", cff) is None, "CITATION.cff must not assert a license")
    require(
        "grants no open-source or open-content license" in " ".join(licensing.split()),
        "LICENSING.md does not preserve the deliberate no-license posture",
    )

    require("Latest release line: `v0.3.0`" in readme, "README does not identify v0.3.0")
    for token in ("fixed gadget", "not represented as conventional journal peer review"):
        require(token.lower() in readme.lower(), f"README scope token is missing: {token}")
    for token in ("bounded-", "middle region", "unrestricted planar sharpness"):
        require(token.lower() in scope.lower(), f"scope fence is missing: {token}")
    require("fixed finite atlas only" in review.lower(), "R3B scope fence is missing")
    require(
        "PUBLIC_V0_3_0_UNREFEREED_RESEARCH_RELEASE" in review,
        "review record does not carry the final release status",
    )
    require("public unrefereed `v0.3.0`" in research_readme, "research README is not finalized")
    require("public unrefereed v0.3.0 release" in claim_ledger, "claim ledger is not finalized")
    require("public unrefereed v0.3.0 derived copy" in proof_map, "proof map is not finalized")
    require(
        "PUBLIC_V0_3_0_UNREFEREED_RELEASE_FROM_REVIEWED_DERIVED_COPY" in provenance,
        "source provenance does not carry the final release state",
    )
    for token in (r"\author{Matthew Protti}", r"\date{4 August 2026}", "unrefereed research release"):
        require(token in synopsis, f"synopsis publication token is missing: {token}")

    require((ROOT / "RELEASE_NOTES_v0.3.0_CANDIDATE.md").exists() is False,
            "candidate release notes must not remain in the final tree")
    require((ROOT / "release/v0.3.0/CITATION.cff.proposed").exists() is False,
            "proposed CFF must not remain beside the final root CFF")
    for text, label, forbidden in (
        (readme, "README", ("Private follow-on candidate", "v0.3.0-rc1", "withholds its author")),
        (root_notes, "root release notes", ("Not Released", "No tag or release is authorized")),
        (release_notes, "release notes", ("release " "candidate", "PENDING_AUTHOR_APPROVAL", "External-action fence")),
        (research_readme, "research README", ("candidate, not released", "authorizes no push")),
        (claim_ledger, "claim ledger", ("Status: private RC1",)),
        (proof_map, "proof map", ("Candidate state", "not released")),
        (synopsis, "synopsis", ("Author line intentionally withheld", "Private RC1", "rights placeholder", "Before any public action")),
    ):
        for token in forbidden:
            require(token.lower() not in text.lower(), f"stale publication language in {label}: {token}")

    for path in ROOT.rglob("*"):
        require(not path.is_symlink(), f"symlink is forbidden in release payload: {path.relative_to(ROOT)}")
    for path in public_text_files():
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        controls = sorted({ord(character) for character in text if ord(character) < 32 and character not in "\t\n\r"})
        require(not controls, f"C0 control characters in {path.relative_to(ROOT)}: {controls}")
        for token in (
            "/mnt/data/",
            "/" "Users/",
            ".codex/" "attachments/",
            "pasted-" "text.txt",
        ):
            require(token not in text, f"private local path leaked in {path.relative_to(ROOT)}: {token}")

    print("PASS: finalized v0.3.0 metadata, authorship, scope, review labels, and no-license posture.")
    print("PASS: no stale publication placeholders, private local paths, control characters, or symlinks.")


if __name__ == "__main__":
    main()
