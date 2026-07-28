# Stewardship and Maintenance - RB-003

## Steward

Matthew Protti is the human release steward and repository maintainer for
`v0.2.0`.

This identifies responsibility for triage and versioning. It is not a service
level agreement and does not assert legal ownership.

## Maintenance objectives

The maintainer will use reasonable efforts to preserve:

- installable and runnable verification instructions;
- deterministic checked artifacts;
- clear theorem and nonclaim boundaries;
- attribution to prior and concurrent work;
- an auditable correction history; and
- immutable released tags.

## Reporting a problem

Useful reports include:

- a concrete routing, parameter set, or inequality that violates the theorem;
- a missing proof branch;
- a verifier disagreement with a minimal reproducer;
- a clean-environment replay failure;
- an omitted or overlapping prior result; or
- an attribution or provenance correction.

Reports should identify the exact tag, commit, file, command, environment, and
observed versus expected result where applicable.

## Triage classes

1. **Theorem-critical:** counterexample or proof gap affecting RB-003.
2. **Certificate-critical:** finite verifier or data defect.
3. **Reproducibility:** clean-environment or deterministic-build failure.
4. **Editorial:** notation, citation, accessibility, or explanation defect.
5. **Scope request:** desired extension beyond the released model.

Scope requests are not defects in the released theorem.

## Correction policy

Released tags and attached assets are immutable. A confirmed defect will be
handled by:

1. opening or preserving a public issue;
2. publishing a concise technical assessment;
3. adding an erratum when the stated theorem remains valid but exposition or
   artifacts require correction; and
4. issuing a new semantic version when a released claim, proof, certificate, or
   public package materially changes.

No correction will be presented as though it existed in the earlier immutable
release.

## Relationship to upstream and adjacent work

The project will preserve explicit credit to Dmitry Rybin and formal citations
to the relevant SSUF literature. Where overlapping work is identified, the
maintainer will update the related-work record rather than claim exclusivity.

The public SSUF repository is independent from private Compliance Health
repositories. The release does not transfer product stewardship, brand rights,
rule-content responsibility, or customer-data obligations to this project.

## Longevity boundary

No perpetual maintenance promise is made. If active stewardship ends, the
repository should retain a final status note identifying the last supported
release and inviting a clearly named successor maintainer rather than silently
appearing maintained.
