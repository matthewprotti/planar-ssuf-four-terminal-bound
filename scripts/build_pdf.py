#!/usr/bin/env python3
"""Build all checked manuscripts in temporary directories."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Manuscript:
    tex: Path
    pdf: Path
    source_date_epoch: str
    preflight: Path


MANUSCRIPTS = (
    Manuscript(
        tex=ROOT / "paper" / "ssuf_four_terminal_note_v5.tex",
        pdf=ROOT / "paper" / "ssuf_four_terminal_note_v5.pdf",
        source_date_epoch="1784846040",  # Immutable v0.1.0 build epoch.
        preflight=ROOT / "verification" / "preflight_pdf_text.py",
    ),
    Manuscript(
        tex=ROOT / "paper" / "rb003_two_scenario_note_v2.tex",
        pdf=ROOT / "paper" / "rb003_two_scenario_note_v2.pdf",
        source_date_epoch="1785434400",  # Fixed v0.2.1 build epoch.
        preflight=ROOT / "verification" / "preflight_rb003_pdf_text.py",
    ),
)


def run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, env=env, check=True)


def build(manuscript: Manuscript) -> None:
    if not manuscript.tex.exists():
        raise SystemExit(f"missing source: {manuscript.tex}")

    env = os.environ.copy()
    env.update(
        {
            "SOURCE_DATE_EPOCH": manuscript.source_date_epoch,
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
                    str(manuscript.tex),
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
                str(manuscript.tex),
            ]
            run(command, cwd=ROOT, env=env)
            run(command, cwd=ROOT, env=env)
        else:
            raise SystemExit("install Tectonic or a TeX distribution providing pdflatex")

        built = tmp / manuscript.pdf.name
        if not built.exists() or built.stat().st_size <= 100_000:
            raise SystemExit(f"rendered PDF is missing or implausibly small: {built}")
        if shutil.which("pdfinfo"):
            run(["pdfinfo", str(built)], cwd=ROOT, env=env)
        run(
            [
                os.fspath(Path(os.sys.executable)),
                os.fspath(manuscript.preflight),
                "--tex",
                os.fspath(manuscript.tex),
                "--pdf",
                os.fspath(built),
            ],
            cwd=ROOT,
            env=env,
        )
        shutil.copyfile(built, manuscript.pdf)

    print(f"PDF BUILD PASS: {manuscript.pdf.relative_to(ROOT)}")


def main() -> None:
    for manuscript in MANUSCRIPTS:
        build(manuscript)


if __name__ == "__main__":
    main()
