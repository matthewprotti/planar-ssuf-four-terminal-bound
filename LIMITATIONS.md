# Status and limitations

## Release status

- `v0.1.0` is the immutable first public disclosure dated 23 July 2026.
- `v0.2.0` adds the RB-003 two-scenario theorem and preserves the original
  release artifacts and claims.
- `v0.2.1` corrects documentation, provenance, and release hygiene. It changes
  no mathematical claim, theorem statement, constant, certificate, proof
  conclusion, or verifier result from `v0.2.0`.
- `v0.3.0` adds the fixed-gadget scenario-cover program described below.
- All three manuscripts are unrefereed research disclosures, not peer-reviewed
  journal publications.

## v0.3.0 fixed-gadget scope

The v0.3.0 release adds internally reviewed fixed-gadget results only.
Its positive-scenario ladder does not extend to signed or zero-coordinate
multi-scenario vectors. The arbitrary signed-and-zero extension is
one-scenario only. The one-scenario value is a supremum-only statement and
does not assert attainment or nonattainment.

The repaired two-scenario bounded-heterogeneity theorem gives the global
fixed-gadget upper bound `beta <= 2` for `1 <= kappa <= 2` and
`beta <= max(2,F(kappa))` for `kappa > 2`, with equality to `F` only for
`kappa >= kappa_0`. The exact curve below `kappa_0` remains open; an upper
bound by two is not an equality classification. No claim of finite attainment
for `F(kappa)` is made.

Scenario-cover atlas values are fixed-instance results. SC-006 is a narrow
fixed-family continuum theorem. Neither substitutes for a global upper proof.
The R3B v2 independent reconstruction applies only to the fixed finite atlas,
and its accurate comparison label preserves strict certificate-payload
divergence despite semantic mathematical agreement.

One scope-limited external human report is documented for the prepublication
v0.3.0 material. The supplied text does not identify the reviewer or establish
independence/conflicts. It found no contradiction in the reconstructed
portions but did not inspect the complete SC-006 or high-heterogeneity proofs.
Complete claim-by-claim external reconstruction remains open. Matthew Protti
is the named human author and release steward; AI assistance is disclosed; no
institutional affiliation is asserted; and the deliberate no-license status
continues.

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

No external human mathematical review is documented for v0.1.0 or v0.2.1.
One external human report on the prepublication v0.3.0 material was supplied on
2 August 2026. It is scope-limited: the reviewer reconstructed the duality and
short GM-005/006 arguments but did not inspect the unpacked SC-006 or
GM-008/009 proofs. The report supplies no reviewer identity or
independence/conflict declaration and is not peer review.

Internal preparation, identifying possible reviewers, or replaying the public
checks would not by itself change this status. Any future review record should
identify the exact version, date, scope, materials, objections, dispositions,
and outcome. Public attribution additionally requires the reviewer's
permission.

## Novelty scope

Targeted searches conducted on 23 and 28 July 2026 found no indexed public
match for the released support pattern and original constants, or for the exact
RB-003 fixed-gadget two-scenario formulation and value `17/8`. Targeted v0.3.0
checks covered cited primary records and the stated surrounding distinctions.
These checks cannot rule out private, unindexed, differently worded, or
simultaneous work. No claim of exhaustive novelty clearance or priority over
all related work is made.

## Agentic-workflow scope

The repository documents a human-directed, AI-assisted research workflow.
Agent output and agent self-assessment are not acceptance evidence. Claims are
accepted only through the stated proof, exact certificate, and human release
decision. The OpenAI July 28, 2026 field report is cited as contemporaneous
methodological context, not as verification or endorsement.

## Follow-on work

Open branches, pull requests, untagged commits, and draft notes are working
research, not released claims. They do not modify the mathematics or evidence
status of an immutable tag. Any follow-on result must be assessed from its own
exact statement, proof, data, verification scope, and release status.

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
found none. Matthew's separate reported no-error review covered v0.2.1 only,
and the scope-limited external report covered only the stated portions of the
prepublication v0.3.0 material.
