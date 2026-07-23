#!/usr/bin/env python3
"""Build the manuscript in a temporary directory and install the checked PDF."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "paper" / "ssuf_four_terminal_note_v5.tex"
PDF = ROOT / "paper" / "ssuf_four_terminal_note_v5.pdf"
SOURCE_DATE_EPOCH = "1784846040"  # Fixed v0.1.0 build epoch.


def run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, env=env, check=True)


def main() -> None:
    if not TEX.exists():
        raise SystemExit(f"missing source: {TEX}")

    env = os.environ.copy()
    env.update(
        {
            "SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH,
            "FORCE_SOURCE_DATE": "1",
            "TZ": "UTC",
        }
    )

    with tempfile.TemporaryDirectory(prefix="ssuf-pdf-") as tmp_name:
        tmp = Path(tmp_name)
        if shutil.which("tectonic"):
            run(
                [
                    "tectonic",
                    "--untrusted",
                    "--outdir",
                    str(tmp),
                    str(TEX),
                ],
                cwd=ROOT,
                env=env,
            )
        elif shutil.which("pdflatex"):
            command = [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={tmp}",
                str(TEX),
            ]
            run(command, cwd=ROOT, env=env)
            run(command, cwd=ROOT, env=env)
        else:
            raise SystemExit("install Tectonic or a TeX distribution providing pdflatex")

        built = tmp / PDF.name
        if not built.exists() or built.stat().st_size <= 100_000:
            raise SystemExit("rendered PDF is missing or implausibly small")
        if shutil.which("pdfinfo"):
            run(["pdfinfo", str(built)], cwd=ROOT, env=env)
        run(
            [
                os.fspath(Path(os.sys.executable)),
                os.fspath(ROOT / "verification" / "preflight_pdf_text.py"),
                "--tex",
                os.fspath(TEX),
                "--pdf",
                os.fspath(built),
            ],
            cwd=ROOT,
            env=env,
        )
        shutil.copyfile(built, PDF)

    print(f"PDF BUILD PASS: {PDF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
