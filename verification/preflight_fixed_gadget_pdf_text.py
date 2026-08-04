#!/usr/bin/env python3
"""Text and page-geometry preflight for the fixed-gadget synopsis."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "paper" / "ssuf_fixed_gadget_scenario_cover_synopsis.tex"
PDF = ROOT / "paper" / "ssuf_fixed_gadget_scenario_cover_synopsis.pdf"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run(*command: str) -> str:
    result = subprocess.run(
        list(command),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex", type=Path, default=TEX)
    parser.add_argument("--pdf", type=Path, default=PDF)
    args = parser.parse_args()
    tex_path = args.tex.resolve()
    pdf_path = args.pdf.resolve()

    require(tex_path.is_file(), "fixed-gadget LaTeX source is missing")
    require(
        pdf_path.is_file() and pdf_path.stat().st_size > 100_000,
        "fixed-gadget PDF is missing or implausibly small",
    )
    for command in ("pdfinfo", "pdftotext"):
        require(shutil.which(command) is not None, f"{command} is required")

    tex = tex_path.read_text(encoding="utf-8")
    text = run("pdftotext", "-layout", str(pdf_path), "-")
    info = run("pdfinfo", str(pdf_path))

    required_tex = (
        r"\author{Author line intentionally withheld pending final approval}",
        r"\beta_G^{(m,+)}=",
        r"\beta_G^{(3,+)}=3",
        r"\beta_G^{(m,+)}=4",
        r"\max\{L,F(\kappa)\}\le\beta_G^{(2,+)}(\kappa)\le2",
        "Integrated technical synopsis with companion proofs",
        "scope-limited external criticism",
        "TRUNK_PRIVATE_ARC_ENVELOPE.md",
        "FULL_PROOF_REVIEW_MAP.md",
        "R4 v6",
    )
    for token in required_tex:
        require(token in tex, f"required fixed-gadget LaTeX token is missing: {token}")

    forbidden_source = (
        "source import pending",
        "R4 v6 pending",
        "formally peer reviewed",
        "OpenAI endorsed",
        "global SSUF conjecture",
        "[FULL " "LEGAL NAME]",
        "[GITHUB-" "OWNER]",
    )
    for token in forbidden_source:
        require(token not in tex, f"forbidden fixed-gadget source wording remains: {token}")

    required_pdf_text = (
        "Scenario-Cover Geometry for a Four-Terminal",
        "private RC1 human-review repair",
        "The fixed-gadget scenario-count ladder",
        "High-heterogeneity global tail",
        "Scenario-cover duality",
        "Complete proof map and computation boundary",
        "R4 v6",
        "scope-limited external criticism",
    )
    for token in required_pdf_text:
        require(token in text, f"required fixed-gadget PDF text is missing: {token}")

    require("Pages:" in info, "pdfinfo did not report a page count")
    pages_match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", info)
    require(pages_match is not None and int(pages_match.group(1)) >= 8, "unexpected synopsis page count")
    require("Page size:" in info and "pts" in info, "pdfinfo did not report page geometry")

    # Poppler's bbox mode emits one page bounding box per page. Bounds outside
    # the media box are a strong signal of clipped or off-page content.
    bbox = subprocess.run(
        ["pdftotext", "-bbox", str(pdf_path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout
    page_boxes = re.findall(
        r'<page width="([0-9.]+)" height="([0-9.]+)">(.*?)</page>',
        bbox,
        flags=re.DOTALL,
    )
    require(len(page_boxes) == int(pages_match.group(1)), "bbox page count differs from pdfinfo")
    for page_number, (width_text, height_text, body) in enumerate(page_boxes, start=1):
        width = float(width_text)
        height = float(height_text)
        for name, value_text in re.findall(r'(xMin|yMin|xMax|yMax)="(-?[0-9.]+)"', body):
            value = float(value_text)
            lower, upper = (0.0, width) if name.startswith("x") else (0.0, height)
            require(
                lower - 0.1 <= value <= upper + 0.1,
                f"page {page_number} has {name}={value} outside media bounds",
            )

    print("PASS: fixed-gadget source contains the scoped theorem ladder and review posture.")
    print("PASS: extracted PDF text contains every substantive synopsis section.")
    print(f"PASS: Poppler geometry stayed within the media boxes on {len(page_boxes)} pages.")


if __name__ == "__main__":
    main()
