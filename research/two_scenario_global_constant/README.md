# SSUF Track B — Exact Two-Scenario Cost-Nonincrease Supremum

This v5 theorem package was first released in `v0.2.0` and is carried forward
mathematically unchanged in the `v0.2.1` provenance and release-hygiene
correction. It proves

\[
\beta_G^{(2\mathrm{sc})}=\frac{17}{8}
\]

on the reproduced four-terminal fixed planar gadget.

The feasibility condition is **scenario-wise cost non-increase**:

\[
C_j(y)\le C_j(x)
\qquad(j=1,2).
\]

It is not an equality condition. The value `17/8` is a non-attained supremum;
rational instances in the intrinsic family
`upward_closure{123,124,234}` approach it.

## Review status

The two documented hostile-review rounds were role-separated AI-assisted model
critiques, not external human mathematical review. The second proof-only critic
found no counterexample and no remaining theorem-level gap in the four
requested pressure points, and recommended **accept subject to minor proof
revision**. This package incorporates all five required local edits and both
recommended proof-hygiene tightenings from that critique. Matthew Protti then
made the human release decision for `v0.2.0`.

No external human mathematical review has been requested or documented. The
package has not undergone formal journal peer review. `v0.2.1` corrects this
status and provenance description; it does not change the mathematics.

## Review-integrated edits

The canonical theorem file now:

1. titles §6.1 **“At least three individually omittable terminals”**;
2. formalizes the two-colour consequence of Lemma 1;
3. restores Lemma 2's pair-blocking hypothesis at the application of equation
   (15);
4. includes the active-constraint proof that a box-constrained one-knapsack
   vertex has at most one fractional coordinate;
5. describes the `|A|=3` result as a **forced star-triangle blocker core** and
   allows the irrelevant possible extra incident edge; and
6. displays the full equations (20)–(22) equality sandwich in the
   non-attainment proof.

The all-zero weighting case in Lemma 1 is also handled explicitly.

## Reproduce

Requires Python 3.11 or later and no third-party packages.

```bash
python replay.py
```

The replay:

1. authenticates the package **as received** against `MANIFEST.sha256`;
2. runs `proof_review_integration_check.py` to confirm every requested proof
   edit remains present and every superseded formulation remains absent;
3. regenerates the deterministic JSON/CSV artifacts with the primary and
   secondary code paths; and
4. authenticates the package again to verify byte-identical regeneration.

`REPLAY_REPORT.txt` is a frozen transcript and is included in the manifest.
Only `MANIFEST.sha256` is excluded from its own hash list.

## Evidence hierarchy

The self-contained human-readable proof in `TWO_SCENARIO_GLOBAL_CONSTANT.md` is
authoritative.

The second-round proof-only critique is an AI-assisted adversarial record and
is included verbatim as generated, but it is not external human evidence, part
of the proof, or journal peer review. The proof-integration checker is a
text-regression guard, not mathematical evidence.

The exact graph enumeration proves the concrete finite lower certificate. The
four-label witness/two-trade registry is an exact finite classification. The
11,175 pattern-pair census and denominator-16 envelope grid are regression
checks only:

- abstract pattern pairs need not share one baseline `q`;
- the envelope grid is not continuous optimization; and
- the secondary script is a separate code path, not an independent
  mathematical derivation.

## Main files

- `TWO_SCENARIO_GLOBAL_CONSTANT.md` — canonical self-contained theorem and
  proof with the second-round edits integrated.
- `ADVERSARIAL_PROOF_ONLY_REVIEW_RB003_V4.md` — verbatim second-round
  AI-assisted proof-only critique on v4.
- `ADVERSARIAL_PROOF_ONLY_REVIEW_RESPONSE_RB003_V5.md` — one-to-one response
  and revision map.
- `FINAL_SIGNOFF_REVIEW_BRIEF.md` — historical pre-release AI-assisted
  verification brief for v5.
- `FINAL_CIRCULATION_CHECKLIST.md` — completed release and correction record.
- `proof_review_integration_check.py` — deterministic proof-text regression
  guard.
- `PROOF_REVIEW_INTEGRATION_REPORT.json` — generated integration report; not
  proof.
- `released_four_terminal_gadget.svg` — graph figure reproduced in the paper.
- `BASELINE_CONTEXT_AND_DEPENDENCIES.md` — baseline, census, naming, and review
  dependency context.
- `EXECUTIVE_SUMMARY.md` — conservative executive account and review status.
- `COMMERCIAL_INTERPRETATION.md` — commercial reading with scope and
  conditioning caveats.
- `ADVERSARIAL_REVIEW_RESPONSE_2026-07-28.md` — historical response to the
  earlier major-revision review.
- `ADVERSARIAL_REVIEW_BRIEF.md` — completed v4 proof-only attack brief retained
  for auditability.
- `verify_two_scenario_global_constant.py` — primary exact verifier and finite
  recognition registry.
- `secondary_regression_check.py` — secondary regression code path.
- `threshold_recognition_report.json` — 149 witnesses, 18 two-trades, and the
  empty-family disposition.
- `two_scenario_17_8_certificate.json` — generated finite certificate.
- `two_scenario_17_8_16_routings.csv` — all 16 concrete routings and arc
  deviations.
- `two_scenario_case_census.json` — abstract blocker-case regression.
- `CLAIM_LEDGER.md` — exact claims, evidence classes, and limitations.
