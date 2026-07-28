#!/usr/bin/env python3
"""Check local lower-family data against the pinned release extraction.

The check runs using only files in this research directory. It does not read or
import the released manuscript at runtime. The release file/hash remains a
human-auditable provenance pin for the extracted canonical data.
"""

from __future__ import annotations

import json
from pathlib import Path

from lower_family import CANONICAL_LOWER_FAMILY

HERE = Path(__file__).resolve().parent


def main() -> None:
    pin = json.loads((HERE / "RELEASE_FAMILY_PIN.json").read_text(encoding="utf-8"))
    dependency = json.loads((HERE / "DEPENDENCY_MANIFEST.json").read_text(encoding="utf-8"))
    assert pin["canonical_family"] == CANONICAL_LOWER_FAMILY
    for key, value in dependency["released_provenance"].items():
        assert pin["release_provenance"].get(key) == value

    theorem = (HERE / "EVERY_PAIR_CELL_THEOREM.md").read_text(encoding="utf-8")
    required_fragments = (
        "(d_1,d_2,d_3,d_4)=(1,q^2,q,1)",
        "(1-q^2,\\ q^2+2q-2+\\varepsilon,\\ 1-q,\\ 1-q)",
        "R(q,\\varepsilon)=q^2(4-q^2-2q-\\varepsilon)",
        "q_* =\\frac{\\sqrt{41}-3}{4}",
        "\\frac{299-41\\sqrt{41}}{32}",
    )
    missing = [fragment for fragment in required_fragments if fragment not in theorem]
    if missing:
        raise ValueError(f"local theorem no longer contains pinned lower-family formulas: {missing}")

    result = {
        "status": "PASS",
        "comparison": "local machine-readable definition equals pinned release extraction",
        "runtime_release_file_access": False,
        "release_commit": pin["release_provenance"]["commit"],
        "release_tex_sha256": pin["release_provenance"]["release_manifest_sha256"],
        "residual_limitation": "the extraction from the pinned TeX is human-auditable rather than reparsed at runtime",
    }
    output = HERE / "release_family_equivalence_results.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
