# Four-terminal planar unsplittable-flow rounding

> **Latest release line: `v0.2.0` (28 July 2026).**
>
> Canonical public versions are the immutable GitHub tags and releases. At an
> untagged commit, repository files are working copies. This is an unrefereed
> research package whose claims, proofs, exact data, and executable checks are
> provided for scrutiny and reproducibility.

## What this repository contains

The repository studies cost-constrained single-source unsplittable-flow
rounding on one compact planar acyclic four-terminal graph.

It now contains two distinct result lines that must not be conflated:

1. the original one-scenario planar lower-bound disclosure (`v0.1.0`); and
2. the exact fixed-gadget two-scenario cost-nonincrease theorem added in
   `v0.2.0`.

The second result does not replace or strengthen the unrestricted planar lower
bound directly. It defines a richer fixed-gadget model with two simultaneous
cost budgets and determines that model's exact normalized additive upper
arc-deviation supremum.

## Results at a glance

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
are not treated as proofs. The RB-003 proof survived two hostile review rounds;
the second proof-only referee found no theorem-level gap and recommended
acceptance after local edits, which are integrated. This is not formal journal
peer review.

## Agentic research method and stewardship

The development process is documented rather than hidden. Matthew Protti
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
- [`research/two_scenario_global_constant/AGENTIC_RESEARCH_VALIDATION_PROTOCOL.md`](research/two_scenario_global_constant/AGENTIC_RESEARCH_VALIDATION_PROTOCOL.md);
- [`research/two_scenario_global_constant/AI_CONTRIBUTION_AND_INTERVENTION_RECORD.md`](research/two_scenario_global_constant/AI_CONTRIBUTION_AND_INTERVENTION_RECORD.md);
- [`research/two_scenario_global_constant/CHECKER_ASSURANCE_AND_EVIDENCE_MODEL.md`](research/two_scenario_global_constant/CHECKER_ASSURANCE_AND_EVIDENCE_MODEL.md); and
- [`research/two_scenario_global_constant/STEWARDSHIP_AND_MAINTENANCE.md`](research/two_scenario_global_constant/STEWARDSHIP_AND_MAINTENANCE.md).

The July 28, 2026 OpenAI field report on agentic scientific computing is cited
as contemporaneous methodological context, not as verification, endorsement,
or evidence for the theorem.

## Where to start

- Read the RB-003 paper:
  [`paper/rb003_two_scenario_note_v1.pdf`](paper/rb003_two_scenario_note_v1.pdf).
- Read the original one-scenario paper:
  [`paper/ssuf_four_terminal_note_v5.pdf`](paper/ssuf_four_terminal_note_v5.pdf).
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

## Rebuild the manuscripts

The checked PDFs are built with Tectonic 0.16.9. Poppler's `pdftotext` is used
for text preflight checks.

```bash
python scripts/build_pdf.py
python verification/preflight_pdf_text.py
python verification/preflight_rb003_pdf_text.py
```

## Repository map

- [`paper/`](paper/): both paper sources and checked PDFs.
- [`verification/`](verification/): original exact and symbolic checks plus
  PDF preflight scripts.
- [`research/two_scenario_global_constant/`](research/two_scenario_global_constant/):
  RB-003 proof, review history, exact certificate, replay, and research
  governance records.
- [`scripts/`](scripts/): verification, PDF, manifest, and deterministic
  release tooling.
- [`AI_USE_AND_PROVENANCE.md`](AI_USE_AND_PROVENANCE.md): contribution and
  responsibility record.
- [`LICENSING.md`](LICENSING.md): deliberate no-license status.

## Context and novelty

Dmitry Rybin's public counterexample of 22 July 2026 was the direct catalyst
for this investigation and is credited in both papers and the provenance
record.

Targeted literature and public-code searches found no indexed match for the
exact RB-003 fixed-gadget two-scenario formulation or the value `17/8`. That is
a good-faith search result, not exhaustive novelty clearance. The surrounding
literature includes planar cost-preserving SSUF rounding, series-parallel
integrality, multicriteria/QoS unsplittable-flow models, robust and reroutable
flows, and classical threshold/simple-game representation theory. See the
RB-003 literature matrix for the precise distinctions.

## Publication, authorship, and rights

Matthew Protti is the named human author and release maintainer. Authorship is
not a representation of legal ownership. No institutional affiliation,
sponsorship, or institutional ownership is asserted.

This repository deliberately grants no open-source or open-content license.
See [`LICENSING.md`](LICENSING.md).
