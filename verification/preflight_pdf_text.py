#!/usr/bin/env python3
"""Preflight checks for the revision-5 source and rendered PDF."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "paper" / "ssuf_four_terminal_note_v5.tex"
PDF = ROOT / "paper" / "ssuf_four_terminal_note_v5.pdf"


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

    require(tex_path.exists(), "LaTeX source is missing")
    require(
        pdf_path.exists() and pdf_path.stat().st_size > 100_000,
        "PDF is missing or implausibly small",
    )
    require(shutil.which("pdftotext") is not None, "pdftotext is required for PDF preflight")
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
        r"q=\frac67",
        r"\varepsilon=\frac1{10584}",
        r"\apl\ge\frac{335}{294}",
        r"\beta_G^{\mathrm{eq},2}",
        r"\beta_{G,\Q}^{\mathrm{eq},2}",
        r"\frac{299-41\sqrt{41}}{32}",
        r"\overline{\mathcal D}",
        r"\crefname{lemma}{lemma}{lemmas}",
    )
    for token in required_tex:
        require(token in tex, f"required LaTeX token is missing: {token}")

    forbidden_source = (
        r"256/225",
        r"q=\frac{13}{15}",
        r"\varepsilon=\frac{29}{38025}",
        "authorship and priority " "to be determined",
        "[FULL " "LEGAL NAME]",
        "[GITHUB-" "OWNER]",
    )
    for token in forbidden_source:
        require(token not in tex, f"obsolete or placeholder source remains: {token}")

    required_pdf_text = (
        "Matthew Protti",
        "335/294",
        "10584",
        "Sharpness within an equal-full-cost two-cheap model",
        "A finite integer certificate: 335/294",
        "Research provenance and contemporaneous context",
    )
    for token in required_pdf_text:
        require(token in text, f"required PDF text is missing: {token}")

    for token in ("256/225", "38025", "authorship and priority " "to be determined"):
        require(token not in text, f"obsolete value or placeholder remains in PDF text: {token}")

    print("PASS: revision-5 source contains the intended theorem data and scope.")
    print("PASS: obsolete certificate values and authorship placeholders are absent.")
    print("PASS: extracted PDF text contains the finite, sharpness, and provenance sections.")


if __name__ == "__main__":
    main()
