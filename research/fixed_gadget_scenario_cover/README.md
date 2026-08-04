# Fixed-Gadget Scenario-Cover Program

Status: private `v0.3.0-rc1` candidate, not released.

This subtree integrates the follow-on theorem program for the same directed
planar four-terminal gadget released in `v0.2.1`. Every global optimization in
this subtree is global only over legal normalized instances on that one fixed
gadget. Nothing here determines a topology-wide or unrestricted planar SSUF
constant.

## Candidate theorem map

For coordinatewise strictly positive E-minus-C cost-difference scenarios, the
internally reviewed fixed-gadget ladder is:

| Number of scenarios | Supremum | Finite attainment posture |
|---:|---:|---|
| 1 | `(299 - 41*sqrt(41))/32` | neither attainment nor nonattainment asserted |
| 2 | `17/8` | nonattained |
| 3 | `3` | nonattained |
| 4 or more | `4` | nonattained |

The legally realizable signed-and-zero extension is proved only for one
scenario. No signed or zero-coordinate multi-scenario extension is claimed.

For exactly two positive scenarios whose coordinate condition number is at
most `kappa`, the repaired theorem proves the global fixed-gadget bounds

`beta <= 2` for `1 <= kappa <= 2`, and
`beta <= max(2, F(kappa))` for `kappa > 2`,

with exact equality to `F(kappa)` only for `kappa >= kappa_0`. The exact curve
below `kappa_0` remains open. No claim of finite attainment for `F(kappa)` is
made in this candidate.

The scenario-cover layer supplies:

- exact halfspace-cover duality for a fixed normalized instance;
- a complete exact finite atlas at the RB-003 witness;
- an exact fixed-RB-family two-scenario phase theorem, SC-006; and
- an isolated independent reconstruction of the fixed finite atlas.

Fixed-instance and fixed-family results do not replace the separate global
upper proofs.

## Evidence posture

The one-scenario, three-scenario, four-or-more-scenario, high-heterogeneity,
scenario-cover, and SC-006 lanes have distinct proof and review histories. R4
v6 accepted the 23 cross-package statement-and-scope assertions without a
finding. That is an internal AI-assisted integration review, not a new proof
review and not publication clearance.

R3B v2 independently reconstructed the fixed finite atlas under technical
answer isolation. Every tested mathematical field matched. The preserved raw
comparator result is `FAIL` because certificate serializations differ. The
accurate label is:

`SEMANTIC_MATHEMATICAL_MATCH / STRICT_CERTIFICATE_PAYLOAD_IDENTITY_FAIL`.

This is not byte-identical certificate reproduction, a continuum theorem,
external human review, peer review, formal proof-assistant verification,
novelty clearance, or release authority.

Matthew's reported no-error review applies only to the immutable public
`v0.2.1` corpus, not to the new candidate results in this subtree.

## Reading order

1. `MODEL_AND_NOTATION.md`
2. `CLAIM_LEDGER.md`
3. `FULL_PROOF_REVIEW_MAP.md`
4. the controlling proof and dependencies for the claim of interest
5. `DEPENDENCY_MAP.md`
6. `EVIDENCE_AND_REVIEW.md`
7. `SOURCE_PROVENANCE.json` and `DERIVATION_NOTES.md`
8. `LIMITATIONS_AND_OPEN_PROBLEMS.md`

The integrated manuscript in
`paper/ssuf_fixed_gadget_scenario_cover_synopsis.pdf` is a technical synopsis.
The Markdown proof artifacts in this subtree are the companion proof sources;
the synopsis is not presented as a standalone substitute for them.

The first circulated reviewer ZIP left those sources inside a nested source
archive. A supplied external human reviewer therefore assessed the synopsis
and reconstructible short arguments but did not inspect the full SC-006 or
GM-008/009 proofs. Revised review packages expose every controlling proof as an
ordinary unpacked, line-numbered file. This repairs discoverability; it does
not retroactively widen that first review's scope or convert it into an
acceptance of unexamined lanes.

## Reproduction

Install the pinned repository dependencies, then run the repository-wide
driver:

```bash
python -m pip install -r verification/requirements.txt
python scripts/verify_all.py
python -O scripts/verify_all.py
```

The programs certify their encoded finite objects and identities only. They do
not certify omitted analytic arguments, dependency correctness, theorem scope,
novelty, authorship, or rights.

## Release boundary

This candidate grants no license and authorizes no push, pull request, tag,
release, publication, submission, reviewer contact, email, or website update.
See the repository `LICENSING.md` and this subtree's publication gates.
