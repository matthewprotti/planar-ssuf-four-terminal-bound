#!/usr/bin/env python3
"""Deterministic guard for the RB-003 second-round proof revisions.

This is a text-integrity regression. It confirms that the local edits required
or recommended by the hostile proof-only referee are present and superseded
formulations are absent. It is not an independent proof of RB-003.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    root = Path(__file__).resolve().parent
    manuscript_path = root / "TWO_SCENARIO_GLOBAL_CONSTANT.md"
    manuscript = manuscript_path.read_text(encoding="utf-8")
    flat = normalize(manuscript)

    required_exact = {
        "signoff_candidate_status": "**Status:** proof-integrated sign-off candidate",
        "correct_A_heading": "### 6.1 At least three individually omittable terminals",
        "empty_colour_handled": "If all \\(\\lambda_T\\) vanish, the conclusion is immediate.",
        "forced_core_language": "Up to exchanging scenarios, the forced blocker core is:",
        "possible_extra_incident_edge": "The triangle scenario may also block one additional pair incident with `u`;",
        "equality_throughout": "Equality throughout (20)--(22) gives",
    }
    required_normalized = {
        "formal_two_colour_assignment": (
            "Assign every blocked singleton and pair to one scenario that blocks it."
        ),
        "formal_two_colour_restriction": (
            "then its restriction to either scenario satisfies the same vertex-load bounds."
        ),
        "lemma2_application_hypothesis": (
            "If a feasible singleton E-set \\(\\{r\\}\\) has complement `T`, and one scenario "
            "blocks every pair in `T`, then (15) shows"
        ),
        "knapsack_active_constraints": (
            "if the knapsack inequality is slack, all coordinates of an extreme point are at "
            "box bounds; if it is tight, at least two independent box constraints must also be active."
        ),
        "extra_edge_irrelevance": (
            "The triangle scenario may also block one additional pair incident with `u`; this does not affect the argument."
        ),
        "nonattainment_tightness": (
            "Hence every inequality in this chain is tight, in particular \\(h_u=1\\)."
        ),
    }
    forbidden = {
        "reversed_A_heading": "### 6.1 At most two individually omittable terminals",
        "informal_union_sentence": (
            "Thus every fractional matching in the union of the two assigned blocker hypergraphs has total weight below two."
        ),
        "overbroad_lemma2_application": (
            "If a feasible singleton E-set \\(\\{r\\}\\) has complement `T`, then (15) shows"
        ),
        "overstated_exact_pattern": "Up to exchanging scenarios, the only remaining pattern is:",
        "underjustified_nonattainment": "Equality in the bound (20) then requires",
    }

    missing_exact = [
        name for name, phrase in required_exact.items() if phrase not in manuscript
    ]
    missing_normalized = [
        name for name, phrase in required_normalized.items() if normalize(phrase) not in flat
    ]
    present_forbidden = [
        name for name, phrase in forbidden.items() if normalize(phrase) in flat
    ]

    assert not missing_exact, f"missing exact proof-review edits: {missing_exact}"
    assert not missing_normalized, (
        f"missing normalized proof-review edits: {missing_normalized}"
    )
    assert not present_forbidden, (
        f"superseded proof formulations remain: {present_forbidden}"
    )

    cross_documents = {
        "CLAIM_LEDGER.md": ("forced", "star-triangle", "not an exact classification"),
        "EXECUTIVE_SUMMARY.md": ("forced", "star-triangle", "may also block one additional"),
        "COMMERCIAL_INTERPRETATION.md": ("forced", "star-triangle", "extra restriction is irrelevant"),
    }
    cross_passed: list[str] = []
    for filename, phrases in cross_documents.items():
        text = (root / filename).read_text(encoding="utf-8").lower()
        for phrase in phrases:
            assert phrase.lower() in text, f"{filename} missing scope phrase: {phrase}"
        cross_passed.append(filename)

    review = (root / "ADVERSARIAL_PROOF_ONLY_REVIEW_RB003_V4.md").read_text(
        encoding="utf-8"
    ).lower()
    assert "accept subject to minor proof revision" in review
    assert "no remaining theorem-level gap" in review

    response = (
        root / "ADVERSARIAL_PROOF_ONLY_REVIEW_RESPONSE_RB003_V5.md"
    ).read_text(encoding="utf-8")
    assert "One-to-one revision matrix" in response
    assert "No numerical" in response or "No theorem constant" in response

    payload = {
        "schema": "ssuf-rb003-proof-review-integration-v2",
        "status": (
            "deterministic text-integrity guard; confirms second-round local "
            "proof edits and cross-document scope; not an independent proof"
        ),
        "manuscript": manuscript_path.name,
        "required_exact_checks_passed": sorted(required_exact),
        "required_normalized_checks_passed": sorted(required_normalized),
        "forbidden_formulations_absent": sorted(forbidden),
        "cross_document_scope_checks_passed": sorted(cross_passed),
        "review_disposition_confirmed": "accept subject to minor proof revision",
        "result": "PASS",
    }
    output = root / "PROOF_REVIEW_INTEGRATION_REPORT.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("PASS: all second-round proof revisions are present in the v5 theorem.")
    print("PASS: every superseded formulation identified by the referee is absent.")
    print("PASS: claim, executive, and commercial documents preserve forced-core scope.")
    print(f"WROTE: {output}")


if __name__ == "__main__":
    main()
