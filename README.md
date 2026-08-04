# Four-terminal planar unsplittable-flow rounding

> **Latest release line: `v0.2.1` (30 July 2026).**
>
> Canonical public versions are the immutable GitHub tags and releases. At an
> untagged commit, repository files are working copies. This is an unrefereed
> research package whose claims, proofs, exact data, and executable checks are
> provided for scrutiny and reproducibility.
>
> **External human-review status:** One external human report on the private
> candidate was supplied on 2 August 2026. The supplied text does not identify
> the reviewer or document independence/conflicts. It reconstructed the
> duality and short three-/many-scenario arguments and found no contradiction,
> but it did not inspect the unpacked SC-006 or high-heterogeneity companion
> proofs. It is therefore recorded as scope-limited review, not full acceptance
> or peer review.
>
> `v0.2.1` is a documentation, provenance, and release-hygiene correction.
> It changes no mathematical claim, theorem statement, constant, certificate,
> proof conclusion, or verifier result from `v0.2.0`.

## Private follow-on candidate

This working branch contains a private `v0.3.0-rc1` candidate under
[`research/fixed_gadget_scenario_cover/`](research/fixed_gadget_scenario_cover/).
It integrates the arbitrary legal one-scenario theorem, the positive
scenario-count ladder, scenario-cover duality and exact atlas, the narrow
SC-006 fixed-family phase, and the repaired high-heterogeneity tail.

The immutable public `v0.2.1` release remains the public baseline. The new
material is internally AI-reviewed and has received one scope-limited external
human report. It has not received a complete independent human reconstruction,
peer review, formal proof-assistant verification, novelty clearance,
authorship/licensing clearance, publication approval, or release approval.
Every new global optimization is restricted to the released fixed gadget; the
global bounded-heterogeneity middle interval remains open. See the candidate
[`claim ledger`](research/fixed_gadget_scenario_cover/CLAIM_LEDGER.md) and
[`limitations`](research/fixed_gadget_scenario_cover/LIMITATIONS_AND_OPEN_PROBLEMS.md).
Reviewers should begin with the
[`full-proof map`](research/fixed_gadget_scenario_cover/FULL_PROOF_REVIEW_MAP.md),
which identifies every controlling analytic proof, dependency, hash, and
executable-evidence boundary.

## What this repository contains

The repository studies cost-constrained single-source unsplittable-flow
rounding on one compact planar acyclic four-terminal graph.

The immutable public release contains two distinct result lines that must not
be conflated:

1. the original one-scenario planar lower-bound disclosure (`v0.1.0`); and
2. the exact fixed-gadget two-scenario cost-nonincrease theorem added in
   `v0.2.0` and carried forward unchanged in `v0.2.1`.

The second result does not replace or strengthen the unrestricted planar lower
bound directly. It defines a richer fixed-gadget model with two simultaneous
cost budgets and determines that model's exact normalized additive upper
arc-deviation supremum.

Open branches, pull requests, and untagged drafts are follow-on working
materials. They do not alter either tagged release or extend its proved claims.

## Released results at a glance

### A. Original one-scenario planar disclosure (`v0.1.0`)

There is an attained integer certificate with maximum demand `294` for which
every cost-nonincreasing unsplittable routing has upper overload at least
`335`:

$$
\frac{335}{294}=1.139455782312\ldots.
$$

A rational family also proves

$$
\alpha_{\mathrm{pl}}\ge
L:=\frac{299-41\sqrt{41}}{32}
=1.139747070789\ldots,
$$

and the same value is the exact supremum in the explicitly restricted
fixed-topology equal-full-cost, two-cheap-choice model.

### B. Exact two-scenario fixed-gadget theorem (`v0.2.0`)

For the same fixed graph, require one unsplittable routing to be no more
expensive than the fractional routing under **each of two positive cost
scenarios**. With additive upper arc deviation normalized by the largest
individual demand,

$$
\boxed{\beta_G^{(2\mathrm{sc})}=\frac{17}{8}=2.125.}
$$

The value is a **non-attained supremum**. Rational instances whose feasible
C-family is

$$
\uparrow\{123,124,234\}
$$

approach it. At `epsilon = 1/1000`, the exact finite objective is

$$
\frac{1061}{500}=2.122,
$$

and after scaling demands by `4000`, every routing respecting both scenario
budgets has upper deviation at least `8488`.

This theorem is restricted to:

- the displayed fixed graph;
- exactly two positive E-minus-C cost-difference vectors;
- scenario-wise cost **non-increase**, not equality; and
- normalized additive upper arc deviation.

It does not determine the unrestricted planar constant, the arbitrary
one-scenario fixed-graph constant, a many-scenario constant, or the
bounded-heterogeneity variant.

## Evidence hierarchy

The human-readable proofs are authoritative. The programs serve narrower
roles:

- exact finite enumeration;
- symbolic and algebraic corroboration;
- finite threshold recognition;
- deterministic regression testing;
- mutation testing; and
- release reproducibility.

Agent confidence, a passing text-regression check, and a broad numerical search
are not treated as proofs. The RB-003 proof survived two AI-assisted hostile
review rounds; the second role-separated proof-only critic found no
theorem-level gap and recommended acceptance after local edits, which are
integrated. This is neither independent human review nor formal journal peer
review.

## Agentic research method and stewardship

For the immutable `v0.2.1` corpus, the development process is documented rather
than hidden. Matthew Protti
selected and directed the research program, set the claim and validation
standards, repeatedly challenged proposed conclusions, required exact and
adversarial checking, approved the final scope, and accepts responsibility for
the release. GPT-5.6 Pro generated and developed substantial portions of the
construction, proof, verification code, review analysis, and manuscript.
Separate model sessions and Codex code paths reduced shared-error risk but are
not independent human verification.

The release protocol follows four rules:

1. specify the claim before accepting implementation output;
2. require externally checkable acceptance targets wherever possible;
3. separate proposal, verification, and human adjudication; and
4. identify who will maintain, correct, and version the result after release.

See:

- [`AI_USE_AND_PROVENANCE.md`](AI_USE_AND_PROVENANCE.md);
- the stable-only
  [`agentic-mathematics case study`](case_study/agentic_mathematics/);
- [`research/two_scenario_global_constant/AGENTIC_RESEARCH_VALIDATION_PROTOCOL.md`](research/two_scenario_global_constant/AGENTIC_RESEARCH_VALIDATION_PROTOCOL.md);
- [`research/two_scenario_global_constant/AI_CONTRIBUTION_AND_INTERVENTION_RECORD.md`](research/two_scenario_global_constant/AI_CONTRIBUTION_AND_INTERVENTION_RECORD.md);
- [`research/two_scenario_global_constant/CHECKER_ASSURANCE_AND_EVIDENCE_MODEL.md`](research/two_scenario_global_constant/CHECKER_ASSURANCE_AND_EVIDENCE_MODEL.md); and
- [`research/two_scenario_global_constant/STEWARDSHIP_AND_MAINTENANCE.md`](research/two_scenario_global_constant/STEWARDSHIP_AND_MAINTENANCE.md).

The July 28, 2026 OpenAI field report on agentic scientific computing is cited
as contemporaneous methodological context, not as verification, endorsement,
evidence for the theorem, or an influence on the July 22–23 stable work.

## Where to start

- Read the private candidate synopsis:
  [`paper/ssuf_fixed_gadget_scenario_cover_synopsis.pdf`](paper/ssuf_fixed_gadget_scenario_cover_synopsis.pdf).
- Read the RB-003 paper:
  [`paper/rb003_two_scenario_note_v2.pdf`](paper/rb003_two_scenario_note_v2.pdf).
- Read the original one-scenario paper:
  [`paper/ssuf_four_terminal_note_v5.pdf`](paper/ssuf_four_terminal_note_v5.pdf).
- Read the stable-only account of the human-directed, AI-assisted workflow:
  [`case_study/agentic_mathematics/CASE_STUDY_STABLE.md`](case_study/agentic_mathematics/CASE_STUDY_STABLE.md).
- Read the complete RB-003 proof package:
  [`research/two_scenario_global_constant/`](research/two_scenario_global_constant/).
- See [`PRIORITY_DISCLOSURE.md`](PRIORITY_DISCLOSURE.md) for the released
  claims and nonclaims.
- See [`LIMITATIONS.md`](LIMITATIONS.md) for mathematical, computational,
  novelty, and review boundaries.

## Reproduce the checks

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r verification/requirements.txt
python scripts/verify_all.py
```

The RB-003 package itself uses Python 3.11 or later and no third-party
packages:

```bash
python research/two_scenario_global_constant/replay.py
```

The replay authenticates the package before execution, checks that the
proof-review repairs remain present, regenerates the exact JSON/CSV artifacts,
and authenticates the package again.

## Report an objection or reproduction failure

Use [`CONTRIBUTING.md`](CONTRIBUTING.md) to report a counterexample, proof or
code correction, reproduction failure, prior-art lead, or proposed extension.
Reports should identify the exact version or commit and distinguish theorem
objections from implementation or documentation issues. Opening an issue or
running the checks does not constitute independent peer review.

## Rebuild the manuscripts

The checked PDFs are built with Tectonic 0.16.9. Poppler's `pdftotext` is used
for text preflight checks.

```bash
python scripts/build_pdf.py
python scripts/build_pdf.py --only-cached
python verification/preflight_pdf_text.py
python verification/preflight_rb003_pdf_text.py
python verification/preflight_fixed_gadget_pdf_text.py
```

## Repository map

- [`paper/`](paper/): the released paper sources and checked PDFs plus the
  private candidate synopsis.
- [`verification/`](verification/): original exact and symbolic checks plus
  PDF preflight scripts.
- [`research/two_scenario_global_constant/`](research/two_scenario_global_constant/):
  RB-003 proof, review history, exact certificate, replay, and research
  governance records.
- [`research/fixed_gadget_scenario_cover/`](research/fixed_gadget_scenario_cover/):
  private follow-on theorem program, exact atlas, companion proofs, and review
  boundary records; its `FULL_PROOF_REVIEW_MAP.md` is the reviewer entry point.
- [`scripts/`](scripts/): verification, PDF, manifest, and deterministic
  release tooling.
- [`case_study/agentic_mathematics/`](case_study/agentic_mathematics/):
  stable-only account of the original agentic research workflow.
- [`AI_USE_AND_PROVENANCE.md`](AI_USE_AND_PROVENANCE.md): contribution and
  responsibility record.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): objection, correction, reproduction,
  prior-art, and extension reporting protocol.
- [`LICENSING.md`](LICENSING.md): deliberate no-license status.

## Context and novelty

Dmitry Rybin's public counterexample of 22 July 2026 was the direct catalyst
for the released investigation and is credited in both released papers and the
provenance record.

Targeted literature and public-code searches found no indexed match for the
exact RB-003 fixed-gadget two-scenario formulation or the value `17/8`. That is
a good-faith search result, not exhaustive novelty clearance. The surrounding
literature includes planar cost-preserving SSUF rounding, series-parallel
integrality, multicriteria/QoS unsplittable-flow models, robust and reroutable
flows, and classical threshold/simple-game representation theory. See the
RB-003 literature matrix for the precise distinctions.

Those search statements describe the released `v0.2.1` record. Related-work,
chronology, and overlap language for the new candidate remains provisional
pending the separate neutral audit.

## Publication, authorship, and rights

Matthew Protti is the named human author and release maintainer for the
immutable `v0.2.1` corpus. The candidate synopsis deliberately withholds its
author line until authorship, contribution, acknowledgement, and rights
language are settled. Authorship is not a representation of legal ownership.
No institutional affiliation, sponsorship, or institutional ownership is
asserted.

This repository deliberately grants no open-source or open-content license.
See [`LICENSING.md`](LICENSING.md).


## v0.3.0 fixed-gadget scenario-cover release

The v0.3.0 candidate consolidates the exact fixed-gadget scenario-count
ladder, the scenario-cover atlas, SC-006, and the high-heterogeneity tail.
See [`release/v0.3.0/RELEASE_NOTES.md`](release/v0.3.0/RELEASE_NOTES.md),
[`release/v0.3.0/FINAL_SCOPE_LEDGER.md`](release/v0.3.0/FINAL_SCOPE_LEDGER.md),
and [`review_evidence/v0.3.0/README.md`](review_evidence/v0.3.0/README.md).

This is an unrefereed research release with exact certificates, deterministic
replay, disclosed blind-reproduction evidence, and claim-scoped adversarial
human/AI-assisted review. It is not represented as conventional journal peer review.
