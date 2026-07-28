# v0.2.0 - Exact two-scenario fixed-gadget supremum

**Release date:** 28 July 2026

## Main result

This release adds RB-003:

$$
\boxed{\beta_G^{(2\mathrm{sc})}=\frac{17}{8}=2.125}
$$

for the released four-terminal planar acyclic gadget under two simultaneous
positive scenario-wise cost-nonincrease constraints.

The value is a non-attained supremum. A rational extremizing sequence has
intrinsic feasible C-family

$$
\uparrow\{123,124,234\}.
$$

A finite exact certificate at `epsilon = 1/1000` has normalized objective
`1061/500 = 2.122`; after integer scaling, every route respecting both scenario
budgets has upper deviation at least `8488` with maximum demand `4000`.

## Model semantics

A route is feasible when it does not increase either scenario cost:

$$
C_j(y)\le C_j(x),\qquad j=1,2.
$$

Equality is not required. The objective is normalized additive upper arc
deviation, not a multiplicative total-cost or capacity ratio.

## Review history

The theorem package underwent two hostile review rounds. The second proof-only
review found no theorem-level gap and recommended acceptance after local proof
revisions. The final source integrates those revisions, including:

- explicit two-colour matching logic;
- the generalized one-knapsack lemma and unit-profit consequence;
- the exact shared-baseline `|A|=3` star-triangle core;
- the full non-attainment equality chain; and
- corrected scope and commercial language.

This remains unrefereed research, not formal peer review.

## Reproducibility additions

- self-contained RB-003 paper and proof package;
- exact 16-routing graph-native certificate;
- exact threshold-recognition registry (`149 + 18 + 1 = 168`);
- deterministic replay authenticated before and after execution;
- proof-text regression and mutation guards;
- updated deterministic release tooling and manifests;
- explicit checker-assurance, AI-contribution, validation, and stewardship
  records.

## Agentic-science context

The release records the division between human scientific responsibility and
agent implementation/reasoning work. It adopts externally checkable acceptance
targets, staged validation, explicit adjudication, and maintenance ownership.
OpenAI's 28 July 2026 field report on agentic scientific computing is cited as
contemporaneous methodological context only; it is not evidence for or an
endorsement of RB-003.

## Preserved boundaries

- The immutable `v0.1.0` tag and assets are unchanged.
- No open-source or open-content license is granted.
- No institutional ownership, sponsorship, or affiliation is asserted.
- No private Compliance Health product code, rule library, customer data, or
  uncleared product brand is included.
- The arbitrary one-scenario fixed-graph constant, many-scenario extension,
  and bounded-heterogeneity function remain open.
