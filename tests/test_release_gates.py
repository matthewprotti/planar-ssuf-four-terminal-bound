#!/usr/bin/env python3
"""Integration tests for release identity and archive completeness gates."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest


SOURCE_ROOT = Path(__file__).resolve().parent.parent
CURRENT_VERSION = "0.3.0"


class ReleaseGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="ssuf-release-gates-")
        self.base = Path(self.temporary.name)
        self.repo = self.base / "repo"
        shutil.copytree(
            SOURCE_ROOT,
            self.repo,
            ignore=shutil.ignore_patterns(
                ".git",
                ".venv",
                "__pycache__",
                "build",
                "dist",
                "*.pyc",
            ),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_repo(self, *command: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            list(command),
            cwd=self.repo,
            check=False,
            capture_output=True,
            text=True,
        )
        if check and result.returncode != 0:
            self.fail(
                f"command failed ({result.returncode}): {' '.join(command)}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def initialize_git(self, tag: str) -> None:
        self.run_repo("git", "init", "--initial-branch=main")
        self.run_repo("git", "config", "user.name", "Release Gate Test")
        self.run_repo("git", "config", "user.email", "release-gate@example.invalid")
        self.run_repo("git", "add", ".")
        self.run_repo("git", "commit", "-m", "test fixture")
        self.run_repo("git", "tag", tag)

    def test_candidate_rejects_unmanifested_deliverable(self) -> None:
        (self.repo / "UNMANIFESTED.txt").write_text("must fail\n", encoding="utf-8")
        result = self.run_repo(
            sys.executable,
            "scripts/build_release.py",
            "--mode",
            "candidate",
            "--version",
            "0.3.1-dev",
            "--output-dir",
            os.fspath(self.base / "candidate-output"),
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("manifest verification failed", result.stdout + result.stderr)

    def test_public_build_rejects_tag_cff_mismatch(self) -> None:
        self.initialize_git("v9.9.9")
        result = self.run_repo(
            sys.executable,
            "scripts/build_release.py",
            "--mode",
            "public",
            "--output-dir",
            os.fspath(self.base / "public-output"),
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            f"public build requires exact tag v{CURRENT_VERSION}",
            result.stdout + result.stderr,
        )

    def test_candidate_rejects_final_version(self) -> None:
        result = self.run_repo(
            sys.executable,
            "scripts/build_release.py",
            "--mode",
            "candidate",
            "--version",
            CURRENT_VERSION,
            "--output-dir",
            os.fspath(self.base / "candidate-output"),
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("visible prerelease suffix", result.stdout + result.stderr)

    def test_public_build_rejects_prerelease_cff_version(self) -> None:
        cff_path = self.repo / "CITATION.cff"
        cff = cff_path.read_text(encoding="utf-8")
        cff_path.write_text(
            cff.replace('version: "0.3.0"', 'version: "0.3.1-rc1"'),
            encoding="utf-8",
        )
        self.run_repo(sys.executable, "scripts/manifest.py", "--write")
        self.initialize_git("v0.3.1-rc1")
        result = self.run_repo(
            sys.executable,
            "scripts/build_release.py",
            "--mode",
            "public",
            "--output-dir",
            os.fspath(self.base / "public-output"),
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("public versions must be final", result.stdout + result.stderr)

    def test_candidate_builds_exact_manifest_membership(self) -> None:
        candidate_version = "0.3.1-dev"
        self.run_repo(
            sys.executable,
            "scripts/release_preflight.py",
            "--candidate-version",
            candidate_version,
        )

        output = self.base / "candidate-output"
        self.run_repo(
            sys.executable,
            "scripts/build_release.py",
            "--mode",
            "candidate",
            "--version",
            candidate_version,
            "--output-dir",
            os.fspath(output),
        )
        manifest_paths = [
            line.split("  ", 1)[1]
            for line in (self.repo / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        ]
        prefix = f"planar-ssuf-four-terminal-bound-v{candidate_version}"
        expected = sorted(
            [
                f"{prefix}/SHA256SUMS.txt",
                *[f"{prefix}/{relative}" for relative in manifest_paths],
            ]
        )
        archive_path = output / f"ssuf-four-terminal-v{candidate_version}-source.tar.gz"
        with tarfile.open(archive_path, "r:gz") as archive:
            self.assertEqual([member.name for member in archive.getmembers()], expected)

        asset_manifest = (output / "SHA256SUMS.txt").read_text(encoding="utf-8")
        self.assertIn("ssuf_four_terminal_note_v5.pdf", asset_manifest)
        self.assertIn("rb003_two_scenario_note_v2.pdf", asset_manifest)
        self.assertIn("ssuf_fixed_gadget_scenario_cover_synopsis.pdf", asset_manifest)

    def test_candidate_rejects_nonempty_output_directory(self) -> None:
        output = self.base / "candidate-output"
        output.mkdir()
        (output / "preexisting.txt").write_text("preserve me\n", encoding="utf-8")
        result = self.run_repo(
            sys.executable,
            "scripts/build_release.py",
            "--mode",
            "candidate",
            "--version",
            "0.3.1-dev",
            "--output-dir",
            os.fspath(output),
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("output directory must be empty", result.stdout + result.stderr)
        self.assertEqual((output / "preexisting.txt").read_text(encoding="utf-8"), "preserve me\n")

    def test_v030_public_metadata_and_scope_gate(self) -> None:
        self.run_repo(sys.executable, "release/v0.3.0/verify_public_release.py")

    def test_v030_public_metadata_rejects_author_placeholder(self) -> None:
        synopsis = self.repo / "paper" / "ssuf_fixed_gadget_scenario_cover_synopsis.tex"
        synopsis.write_text(
            synopsis.read_text(encoding="utf-8").replace(
                r"\author{Matthew Protti}",
                r"\author{Author line intentionally withheld}",
            ),
            encoding="utf-8",
        )
        result = self.run_repo(
            sys.executable,
            "release/v0.3.0/verify_public_release.py",
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("synopsis publication token is missing", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
