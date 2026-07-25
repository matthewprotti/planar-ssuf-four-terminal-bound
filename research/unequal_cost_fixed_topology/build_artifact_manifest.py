#!/usr/bin/env python3
"""Build or check the committed manifest for unequal-cost research sources."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "artifact_manifest.json"
EXCLUDED = {
    "artifact_manifest.json",
    "threshold_family_census.json",
    "independent_census_results.json",
    "symbolic_every_pair_results.json",
}


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload() -> dict:
    files = {
        path.name: file_hash(path)
        for path in sorted(HERE.iterdir())
        if path.is_file()
        and path.name not in EXCLUDED
        and not path.name.startswith(".")
        and path.suffix in {".py", ".md", ".json"}
    }
    dependency = json.loads((HERE / "DEPENDENCY_MANIFEST.json").read_text(encoding="utf-8"))
    return {
        "schema_version": "ssuf-unequal-cost-artifact-manifest-v0.2",
        "scope": "committed unequal_cost_fixed_topology research sources",
        "files": files,
        "released_provenance": dependency["released_provenance"],
        "dependency_status": dependency["dependency_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current = payload()
    if args.check:
        stored = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if stored != current:
            raise SystemExit("artifact manifest is stale")
        print("PASS: artifact manifest is current")
        return
    OUTPUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUTPUT}")


if __name__ == "__main__":
    main()
