# Status and limitations

## Release status

- `v0.1.0` is the immutable first public disclosure dated 23 July 2026.
- `v0.2.0` adds the RB-003 two-scenario theorem and preserves the original
  release artifacts and claims.
- `v0.2.1` corrects documentation, provenance, and release hygiene. It changes
  no mathematical claim, theorem statement, constant, certificate, proof
  conclusion, or verifier result from `v0.2.0`.
- Both papers are unrefereed research disclosures, not peer-reviewed journal
  publications.

## Original one-scenario scope

- The value `(299 - 41*sqrt(41))/32` is a lower bound for the unrestricted
  planar constant and a sharp value only for the explicitly defined
  equal-full-cost, two-cheap-choice model on the fixed topology.
- The result does not establish global four-terminal optimality, arbitrary-cost
  fixed-graph optimality, or the exact unrestricted planar constant.

## RB-003 mathematical scope

RB-003 proves

$$
\beta_G^{(2\mathrm{sc})}=17/8
$$

only for:

- the specified four-terminal planar acyclic graph;
- one routing constrained by exactly two positive E-minus-C cost-difference
  scenarios;
- scenario-wise cost non-increase `C_j(y) <= C_j(x)`, not equality; and
- additive upper arc deviation normalized by `d_max`.

The value `17/8` is a non-attained supremum. The theorem does not establish:

- the otherwise-identical arbitrary one-scenario fixed-graph constant;
- a many-scenario constant;
- an unrestricted planar two-scenario constant;
- a bounded-condition-number or bounded-heterogeneity constant;
- a multiplicative capacity-augmentation factor; or
- the performance of any sequential or joint optimization algorithm.

The extremizing sequence is ill-conditioned. The finite certificate uses
within-scenario weight ratios `3000` and `1000`, and the limiting construction
requires unbounded ratios.

## Verification scope

- The human-readable analytic proofs are authoritative.
- Exact enumeration proves the stated finite certificates for the encoded graph
  and data.
- The four-label threshold registry is an exact finite classification within
  its stated model.
- Symbolic scripts, finite grids, text-regression checks, mutation tests, and
  broad searches are corroboration or regression evidence, not substitutes for
  the proof.
- The secondary RB-003 code path shares the support matrix, blocker structure,
  and lower-family ansatz. It is not an independent mathematical derivation.
- AI-assisted hostile reviews reduce some error risks but are not independent
  human peer review.

## External human-review status

No external human mathematical review has been requested or documented for
either release. The documented author review and role-separated AI-assisted
adversarial reviews are different evidence classes and must not be described as
independent human review or peer review.

Internal preparation, identifying possible reviewers, or replaying the public
checks would not by itself change this status. Any future review record should
identify the exact version, date, scope, materials, objections, dispositions,
and outcome. Public attribution additionally requires the reviewer's
permission.

## Novelty scope

Targeted searches conducted on 23 and 28 July 2026 found no indexed public
match for the released support pattern and original constants, or for the exact
RB-003 fixed-gadget two-scenario formulation and value `17/8`. These searches
cannot rule out private, unindexed, differently worded, or simultaneous work.
No claim of exhaustive novelty clearance or priority over all related work is
made.

## Agentic-workflow scope

The repository documents a human-directed, AI-assisted research workflow.
Agent output and agent self-assessment are not acceptance evidence. Claims are
accepted only through the stated proof, exact certificate, and human release
decision. The OpenAI July 28, 2026 field report is cited as contemporaneous
methodological context, not as verification or endorsement.

## Follow-on work

Open branches, pull requests, untagged commits, and draft notes are working
research, not released claims. They do not modify the mathematics or evidence
status of either immutable tag. Any follow-on result must be assessed from its
own exact statement, proof, data, verification scope, and release status.

## Commercial interpretation

The theorem shows that two simultaneous non-increase constraints can create a
star-triangle obstruction on the fixed graph. It does not establish customer
ROI, production safety, regulatory correctness, or an algorithmic advantage.
No Compliance Health product, private rule library, customer data, or uncleared
commercial brand is part of this public research release.

## Release controls

1. The deliberate no-license status remains explicit.
2. The public package is tied to an exact semantic version and Git tag.
3. Both manuscripts, deterministic verifiers, manifests, and release archives
   are checked before publication.
4. Corrections to an immutable release must be made through an erratum or a new
   version, never by rewriting the tag.
5. Publication follows explicit human authorization.

No mathematical defect is currently known in the stated released claims. This
means only that the completed proof checks and AI-assisted critique rounds
found none; no external human mathematical review is documented.
