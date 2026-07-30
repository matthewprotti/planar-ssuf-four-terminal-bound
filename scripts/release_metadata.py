#!/usr/bin/env python3
"""Read and validate release identity from CFF metadata and Git."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess


VERSION_PATTERN = re.compile(
    r"^(?P<base>0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?P<suffix>-[0-9A-Za-z][0-9A-Za-z.-]*|\+[0-9A-Za-z][0-9A-Za-z.-]*)?$"
)
CFF_VERSION_PATTERN = re.compile(
    r"""(?m)^version:\s*(?:"(?P<double>[^"]+)"|'(?P<single>[^']+)'|(?P<plain>\S+))\s*$"""
)


def cff_version(root: Path) -> str:
    cff_path = root / "CITATION.cff"
    if not cff_path.is_file():
        raise SystemExit("CITATION.cff is missing")
    match = CFF_VERSION_PATTERN.search(cff_path.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit("CITATION.cff has no unambiguous top-level version")
    version = next(value for value in match.groupdict().values() if value is not None)
    validate_version(version)
    return version


def validate_version(
    version: str,
    *,
    candidate: bool = False,
    public: bool = False,
) -> None:
    match = VERSION_PATTERN.fullmatch(version)
    if not match:
        raise SystemExit(f"invalid release version: {version!r}")
    suffix = match.group("suffix")
    if candidate and (not suffix or not suffix.startswith("-")):
        raise SystemExit(
            "candidate/dev versions must have a visible prerelease suffix "
            "(for example, 0.2.1-dev or 0.2.1-rc1)"
        )
    if public and suffix:
        raise SystemExit(
            "public versions must be final semantic versions without "
            "prerelease or build suffixes"
        )


def git_output(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown Git error"
        raise SystemExit(f"Git release-identity check failed: {detail}")
    return result.stdout.strip()


def require_public_identity(root: Path) -> str:
    version = cff_version(root)
    validate_version(version, public=True)
    expected_tag = f"v{version}"
    exact_tags = set(git_output(root, "tag", "--points-at", "HEAD").splitlines())
    if expected_tag not in exact_tags:
        rendered = ", ".join(sorted(exact_tags)) if exact_tags else "none"
        raise SystemExit(
            f"public build requires exact tag {expected_tag}; tags at HEAD: {rendered}"
        )
    dirty = git_output(root, "status", "--porcelain", "--untracked-files=all")
    if dirty:
        raise SystemExit("public build requires a clean Git worktree")
    return version


def release_version(root: Path, *, mode: str, candidate_version: str | None) -> str:
    if mode == "public":
        if candidate_version is not None:
            raise SystemExit("--version is not allowed in public mode; CITATION.cff is authoritative")
        return require_public_identity(root)
    if mode == "candidate":
        if candidate_version is None:
            raise SystemExit("candidate mode requires --version")
        validate_version(candidate_version, candidate=True)
        return candidate_version
    raise SystemExit(f"unknown build mode: {mode}")
