#!/usr/bin/env python3
"""Build a deterministic public or candidate/dev release package."""

from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path
import shutil
import tarfile

from manifest import check_manifest
from release_metadata import release_version


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "SHA256SUMS.txt"
PDFS = (
    ROOT / "paper" / "ssuf_four_terminal_note_v5.pdf",
    ROOT / "paper" / "rb003_two_scenario_note_v1.pdf",
)
EPOCH = 1_785_261_600


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def manifest_paths() -> list[Path]:
    if not MANIFEST.exists():
        raise SystemExit("SHA256SUMS.txt is missing; run scripts/manifest.py --write")
    paths = [MANIFEST]
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        try:
            _digest, relative = line.split("  ", 1)
        except ValueError as error:
            raise SystemExit(f"malformed manifest entry: {line!r}") from error
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"manifest entry is missing, non-file, or symlinked: {relative}")
        paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix())


def add_file(archive: tarfile.TarFile, path: Path, *, prefix: str) -> None:
    relative = path.relative_to(ROOT).as_posix()
    data = path.read_bytes()
    info = tarfile.TarInfo(f"{prefix}/{relative}")
    info.size = len(data)
    info.mtime = EPOCH
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    import io

    archive.addfile(info, io.BytesIO(data))


def validate_archive(archive_path: Path, paths: list[Path], *, prefix: str) -> None:
    expected = [f"{prefix}/{path.relative_to(ROOT).as_posix()}" for path in paths]
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        actual = [member.name for member in members]
        if actual != expected:
            raise SystemExit("archive membership differs from the manifest")
        for member in members:
            if not member.isfile() or member.issym() or member.islnk():
                raise SystemExit(f"unsafe archive member: {member.name}")
            if member.uid != 0 or member.gid != 0 or member.mtime != EPOCH:
                raise SystemExit(f"non-normalized archive metadata: {member.name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        required=True,
        choices=("public", "candidate"),
        help="public requires an exact CFF-matching tag; candidate requires --version",
    )
    parser.add_argument(
        "--version",
        help="visibly non-final version for candidate mode, such as 0.2.0-dev",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "dist",
        help="directory for generated assets (default: repository dist/)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    version = release_version(ROOT, mode=args.mode, candidate_version=args.version)
    prefix = f"planar-ssuf-four-terminal-bound-v{version}"
    output_dir = args.output_dir.resolve()
    archive_path = output_dir / f"ssuf-four-terminal-v{version}-source.tar.gz"

    check_manifest()
    paths = manifest_paths()
    output_dir.mkdir(parents=True, exist_ok=True)
    with archive_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in paths:
                    add_file(archive, path, prefix=prefix)
    validate_archive(archive_path, paths, prefix=prefix)

    copied_pdfs: list[Path] = []
    for pdf in PDFS:
        if not pdf.is_file() or pdf.stat().st_size <= 100_000:
            raise SystemExit(f"checked PDF is missing or implausibly small: {pdf}")
        output_pdf = output_dir / pdf.name
        shutil.copyfile(pdf, output_pdf)
        copied_pdfs.append(output_pdf)

    assets = (archive_path, *copied_pdfs)
    checksums = "\n".join(f"{sha256(path)}  {path.name}" for path in assets) + "\n"
    (output_dir / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8")
    print(
        f"RELEASE ARCHIVE PASS [{args.mode}]: "
        f"{archive_path.name} ({len(paths)} files)"
    )
    print(checksums, end="")


if __name__ == "__main__":
    main()
