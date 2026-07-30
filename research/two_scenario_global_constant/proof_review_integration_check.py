#!/usr/bin/env python3
"""Deterministic guard for the RB-003 proof and provenance revisions.

This is a text-integrity regression. It confirms that the local edits required
or recommended by the role-separated AI-assisted proof critic are present,
that superseded formulations are absent, and that the public package does not
misclassify model critique as external human review. It is not an independent
proof of RB-003.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    root = Path(__file__).resolve().parent
    repository_root = root.parent.parent
    manuscript_path = root / "TWO_SCENARIO_GLOBAL_CONSTANT.md"
    manuscript = manuscript_path.read_text(encoding="utf-8")
    flat = normalize(manuscript)

    required_exact = {
        "released_status": "**Status:** public unrefereed theorem package",
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

    provenance_documents = {
        "TWO_SCENARIO_GLOBAL_CONSTANT.md": (
            "role-separated",
            "AI-assisted",
            "not external human mathematical review",
        ),
        "README.md": (
            "role-separated",
            "AI-assisted",
            "No external human mathematical review",
        ),
        "CLAIM_LEDGER.md": (
            "role-separated",
            "AI-assisted",
            "no external human mathematical review",
        ),
        "EXECUTIVE_SUMMARY.md": (
            "role-separated",
            "AI-assisted",
            "No external human mathematical review",
        ),
        "COMMERCIAL_INTERPRETATION.md": (
            "role-separated",
            "AI-assisted",
            "No external human mathematical review",
        ),
        "AI_CONTRIBUTION_AND_INTERVENTION_RECORD.md": (
            "External human mathematical review",
            "none requested or documented",
        ),
    }
    provenance_passed: list[str] = []
    for filename, phrases in provenance_documents.items():
        text = (root / filename).read_text(encoding="utf-8").lower()
        for phrase in phrases:
            assert phrase.lower() in text, (
                f"{filename} missing provenance phrase: {phrase}"
            )
        provenance_passed.append(filename)

    public_status_files = (
        "TWO_SCENARIO_GLOBAL_CONSTANT.md",
        "README.md",
        "CLAIM_LEDGER.md",
        "EXECUTIVE_SUMMARY.md",
        "COMMERCIAL_INTERPRETATION.md",
        "BASELINE_CONTEXT_AND_DEPENDENCIES.md",
        "AI_CONTRIBUTION_AND_INTERVENTION_RECORD.md",
        "ADVERSARIAL_PROOF_ONLY_REVIEW_RESPONSE_RB003_V5.md",
        "FINAL_CIRCULATION_CHECKLIST.md",
        "FINAL_SIGNOFF_REVIEW_BRIEF.md",
    )
    misleading_phrases = (
        "proof-integrated sign-off candidate",
        "external referee",
        "external supporting evidence",
        "re-signed by",
        "re-authenticated",
        "review_revision_guard.py",
        "await final external signoff",
    )
    for filename in public_status_files:
        text = (root / filename).read_text(encoding="utf-8").lower()
        for phrase in misleading_phrases:
            assert phrase not in text, (
                f"{filename} retains misleading review-status phrase: {phrase}"
            )

    paper_md = repository_root / "paper" / "rb003_two_scenario_note_v2.md"
    paper_tex = repository_root / "paper" / "rb003_two_scenario_note_v2.tex"
    for path in (paper_md, paper_tex):
        text = path.read_text(encoding="utf-8").lower()
        for phrase in (
            "revision 2",
            "role-separated ai-assisted model critiques",
            "no external human mathematical review is documented",
        ):
            assert phrase in text, f"{path.name} missing provenance phrase: {phrase}"

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
        "schema": "ssuf-rb003-proof-review-integration-v3",
        "status": (
            "deterministic text-integrity guard; confirms second-round local "
            "proof edits, cross-document scope, and AI-review provenance; not "
            "an independent proof"
        ),
        "manuscript": manuscript_path.name,
        "required_exact_checks_passed": sorted(required_exact),
        "required_normalized_checks_passed": sorted(required_normalized),
        "forbidden_formulations_absent": sorted(forbidden),
        "cross_document_scope_checks_passed": sorted(cross_passed),
        "provenance_documents_checked": sorted(provenance_passed),
        "misleading_review_status_phrases_absent": sorted(misleading_phrases),
        "paper_revision_checked": paper_md.name,
        "review_disposition_confirmed": "accept subject to minor proof revision",
        "result": "PASS",
    }
    output = root / "PROOF_REVIEW_INTEGRATION_REPORT.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("PASS: all second-round proof revisions are present in the v5 theorem.")
    print("PASS: every superseded formulation identified by the AI-assisted critic is absent.")
    print("PASS: claim, executive, and commercial documents preserve forced-core scope.")
    print("PASS: public status documents distinguish AI-assisted critique from external human review.")
    print(f"WROTE: {output.name}")


if __name__ == "__main__":
    main()
