#!/usr/bin/env python3
"""Build all checked manuscripts in temporary directories."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
TOOLCHAIN = ROOT / "verification" / "document-toolchain.json"


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
    Manuscript(
        tex=ROOT / "paper" / "ssuf_fixed_gadget_scenario_cover_synopsis.tex",
        pdf=ROOT / "paper" / "ssuf_fixed_gadget_scenario_cover_synopsis.pdf",
        source_date_epoch="1785672000",  # Fixed v0.3.0 reproducible build epoch.
        preflight=ROOT / "verification" / "preflight_fixed_gadget_pdf_text.py",
    ),
)


def run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, env=env, check=True)


def toolchain() -> dict[str, object]:
    if not TOOLCHAIN.is_file():
        raise SystemExit(f"missing document toolchain lock: {TOOLCHAIN}")
    payload = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    if payload.get("schema") != "ssuf-document-toolchain-v1":
        raise SystemExit("unsupported document toolchain lock schema")
    return payload


def require_toolchain(payload: dict[str, object]) -> tuple[str, str, str]:
    tectonic = payload["tectonic"]
    if not isinstance(tectonic, dict):
        raise SystemExit("malformed Tectonic toolchain lock")
    expected_version = str(tectonic["version"])
    bundle_url = str(tectonic["bundle_url"])
    bundle_hash = str(tectonic["bundle_content_sha256"])
    if not re.fullmatch(r"[0-9a-f]{64}", bundle_hash):
        raise SystemExit("malformed locked Tectonic bundle content hash")
    executable = shutil.which("tectonic")
    if executable is None:
        raise SystemExit(f"Tectonic {expected_version} is required")
    result = subprocess.run(
        [executable, "--version"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    actual = result.stdout.strip()
    if actual != f"Tectonic {expected_version}":
        raise SystemExit(
            f"Tectonic version mismatch: expected {expected_version}, observed {actual!r}"
        )
    for command in ("pdfinfo", "pdftotext"):
        if shutil.which(command) is None:
            raise SystemExit(f"Poppler command {command} is required")
    print(
        f"DOCUMENT TOOLCHAIN PASS: Tectonic {expected_version}; "
        f"bundle content {bundle_hash}"
    )
    return executable, bundle_url, bundle_hash


def tectonic_url_cache_name(url: str) -> str:
    return "".join(
        character
        if character.isalnum() or character in "._-"
        else f",{ord(character)},"
        for character in url
    )


def require_bundle_resolution(bundle_url: str, expected_hash: str) -> None:
    roots: list[Path] = []
    explicit = os.environ.get("TECTONIC_CACHE_DIR")
    if explicit:
        roots.append(Path(explicit))
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        roots.append(Path(xdg) / "Tectonic")
    roots.extend(
        (
            Path.home() / "Library" / "Caches" / "Tectonic",
            Path.home() / ".cache" / "Tectonic",
            Path.home() / ".cache" / "tectonic",
        )
    )
    cache_name = tectonic_url_cache_name(bundle_url)
    for root in dict.fromkeys(roots):
        mapping = root / "bundles" / "hashes" / cache_name
        index = root / "bundles" / "data" / f"{expected_hash}.index"
        data = root / "bundles" / "data" / expected_hash
        if not mapping.is_file():
            continue
        observed = mapping.read_text(encoding="utf-8").strip()
        if observed != expected_hash:
            raise SystemExit(
                f"Tectonic bundle resolution mismatch: expected {expected_hash}, observed {observed}"
            )
        if not index.is_file() or not data.is_dir():
            raise SystemExit("locked Tectonic bundle cache is incomplete")
        print(f"TECTONIC BUNDLE RESOLUTION PASS: {expected_hash}")
        return
    raise SystemExit("could not authenticate the resolved Tectonic bundle cache")


def build(
    manuscript: Manuscript,
    *,
    tectonic: str,
    bundle_url: str,
    bundle_hash: str,
    only_cached: bool,
) -> None:
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
        command = [
            tectonic,
            "--untrusted",
            "--bundle",
            bundle_url,
            "--outdir",
            str(tmp),
        ]
        if only_cached:
            command.append("--only-cached")
        command.append(str(manuscript.tex))
        run(command, cwd=ROOT, env=env)
        require_bundle_resolution(bundle_url, bundle_hash)

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only-cached",
        action="store_true",
        help="forbid network access and use only the locked bundle already in the Tectonic cache",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tectonic, bundle_url, bundle_hash = require_toolchain(toolchain())
    for manuscript in MANUSCRIPTS:
        build(
            manuscript,
            tectonic=tectonic,
            bundle_url=bundle_url,
            bundle_hash=bundle_hash,
            only_cached=args.only_cached,
        )


if __name__ == "__main__":
    main()
