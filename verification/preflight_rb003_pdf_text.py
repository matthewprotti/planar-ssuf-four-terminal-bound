#!/usr/bin/env python3
"""Preflight checks for the RB-003 source and rendered PDF."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "paper" / "rb003_two_scenario_note_v1.tex"
PDF = ROOT / "paper" / "rb003_two_scenario_note_v1.pdf"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex", type=Path, default=TEX)
    parser.add_argument("--pdf", type=Path, default=PDF)
    args = parser.parse_args()
    tex_path = args.tex.resolve()
    pdf_path = args.pdf.resolve()

    require(tex_path.exists(), "RB-003 LaTeX source is missing")
    require(
        pdf_path.exists() and pdf_path.stat().st_size > 100_000,
        "RB-003 PDF is missing or implausibly small",
    )
    require(shutil.which("pdftotext") is not None, "pdftotext is required")

    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    tex = tex_path.read_text(encoding="utf-8")
    text = result.stdout

    required_tex = (
        r"\author{Matthew Protti}",
        r"\boxed{\beta_G^{(2\mathrm{sc})}=\frac{17}{8}=2.125.}",
        r"\frac{1061}{500}=2.122",
        "8488",
        r"C_j(y^R)\le C_j(x)",
        "non-attained supremum",
        "Dmitry Rybin",
        "Scientific computing in the age of agentic AI",
    )
    for token in required_tex:
        require(token in tex, f"required RB-003 LaTeX token is missing: {token}")

    forbidden_source = (
        "global extremizer",
        "cost equality is required",
        "formally peer reviewed",
        "OpenAI endorsed",
        "uncleared public product brand",
    )
    for token in forbidden_source:
        require(token not in tex, f"forbidden RB-003 source claim remains: {token}")

    required_pdf_text = (
        "The Exact Two-Scenario Cost-Nonincrease Supremum",
        "Theorem RB-003",
        "17/8",
        "1061/500",
        "8488",
        "Non-attainment",
        "scenario-wise cost non-increasing",
        "Research provenance, validation, and stewardship",
        "Dmitry Rybin",
        "Scientific computing in the age of agentic AI",
    )
    for token in required_pdf_text:
        require(token in text, f"required RB-003 PDF text is missing: {token}")

    for token in ("global extremizer", "OpenAI endorsed", "uncleared public product brand"):
        require(token not in text, f"forbidden RB-003 PDF wording remains: {token}")

    print("PASS: RB-003 source contains the exact theorem, certificate, and scope.")
    print("PASS: RB-003 PDF contains the theorem, non-attainment, provenance, and stewardship sections.")


if __name__ == "__main__":
    main()
