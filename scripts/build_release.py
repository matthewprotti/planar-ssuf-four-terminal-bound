#!/usr/bin/env python3
"""Build a deterministic source archive and release-asset checksum file."""

from __future__ import annotations

import gzip
import hashlib
from pathlib import Path
import shutil
import tarfile


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
MANIFEST = ROOT / "SHA256SUMS.txt"
VERSION = "0.1.0"
PREFIX = f"planar-ssuf-four-terminal-bound-v{VERSION}"
ARCHIVE = DIST / f"ssuf-four-terminal-v{VERSION}-source.tar.gz"
PDF = ROOT / "paper" / "ssuf_four_terminal_note_v5.pdf"
DIST_PDF = DIST / PDF.name
EPOCH = 1_784_846_040


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
        _digest, relative = line.split("  ", 1)
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"manifest entry is missing, non-file, or symlinked: {relative}")
        paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix())


def add_file(archive: tarfile.TarFile, path: Path) -> None:
    relative = path.relative_to(ROOT).as_posix()
    data = path.read_bytes()
    info = tarfile.TarInfo(f"{PREFIX}/{relative}")
    info.size = len(data)
    info.mtime = EPOCH
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    import io

    archive.addfile(info, io.BytesIO(data))


def validate_archive(paths: list[Path]) -> None:
    expected = {f"{PREFIX}/{path.relative_to(ROOT).as_posix()}" for path in paths}
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        members = archive.getmembers()
        actual = {member.name for member in members}
        if actual != expected:
            raise SystemExit("archive membership differs from the manifest")
        for member in members:
            if not member.isfile() or member.issym() or member.islnk():
                raise SystemExit(f"unsafe archive member: {member.name}")
            if member.uid != 0 or member.gid != 0 or member.mtime != EPOCH:
                raise SystemExit(f"non-normalized archive metadata: {member.name}")


def main() -> None:
    paths = manifest_paths()
    DIST.mkdir(exist_ok=True)
    with ARCHIVE.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in paths:
                    add_file(archive, path)
    validate_archive(paths)

    shutil.copyfile(PDF, DIST_PDF)
    assets = (ARCHIVE, DIST_PDF)
    checksums = "\n".join(f"{sha256(path)}  {path.name}" for path in assets) + "\n"
    (DIST / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8")
    print(f"RELEASE ARCHIVE PASS: {ARCHIVE.name} ({len(paths)} files)")
    print(checksums, end="")


if __name__ == "__main__":
    main()
