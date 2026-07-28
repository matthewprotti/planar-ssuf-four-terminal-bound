# AI Contribution and Human Intervention Record - RB-003

## Record status

- **Release:** `v0.2.0`
- **Claim:** `RB-003`
- **Human author and release decision-maker:** Matthew Protti
- **Primary model:** OpenAI GPT-5.6 Pro
- **Implementation/repository assistance:** Codex and separate model sessions
- **Formal peer review:** none

This record describes the research process. It is not evidence for the theorem.

## Research direction set by the human

Matthew chose to pursue natural variants of the released four-terminal SSUF
gadget rather than immediately move to unrelated problems. He selected the
simultaneous two-scenario cost-nonincrease model as the principal Track B
question and required a result with commercial interpretability but precise
mathematical scope.

The decisive questions were set explicitly:

1. Which four-label monotone feasibility families can two scenarios realize?
2. What are the exact values of newly accessible families?
3. Does the two-scenario obstruction exceed the released restricted value `L`?
4. What is the global fixed-gadget two-scenario constant?

## Substantive model contributions

GPT-5.6 Pro and Codex contributed substantially to:

- representing simultaneous scenario feasibility as two positive threshold
  constraints over a shared fractional baseline;
- enumerating and classifying four-label monotone families;
- constructing early lower certificates;
- discovering that the valid `17/16` certificate was far from the unrestricted
  optimum;
- proving all 18 newly accessible nonthreshold families have value `2`;
- identifying the no-pair frontier and the central star-triangle obstruction;
- deriving the `17/8` upper envelope;
- producing the rational extremizing sequence;
- constructing the finite `1061/500` certificate;
- writing exact verifiers, regression checks, and mutation guards;
- drafting the proof, review briefs, responses, and release documentation; and
- implementing deterministic release controls.

## Material human interventions

Matthew did not accept the sequence of intermediate outputs as final.
Material interventions included:

- requesting natural variants that reused the exact finite research engine;
- insisting that Track B continue after the first feasible-family
  classification;
- explicitly reopening the valid `17/16` obstruction and asking for its exact
  cell value;
- recognizing that optimizing only the 18 newly accessible families did not
  determine the global two-scenario parameter frontier;
- directing the search to the 16 no-pair families;
- requiring commercial interpretation to be simplified without overstating
  the theorem;
- supplying hostile review reports and requiring all publication blockers to
  be repaired;
- distinguishing cost non-increase from equality;
- accepting the non-attainment correction and requiring it to be promoted to a
  formal corollary;
- rejecting overstatements of computational independence and causal commercial
  impact;
- signing off only after the second proof-only review found no theorem-level
  gap; and
- authorizing public release after a final personal review.

## Error and revision record

The development loop exposed and repaired, among other issues:

- reciprocal fraction renderings in an earlier checkpoint;
- overbroad claims about computational independence;
- ambiguous use of “cost preservation” that could be read as equality;
- an invalid inference from a demand-weighted inequality to an unweighted one;
- the mistaken phrase “global extremizer” for a non-attained supremum;
- a reversed proof-section heading;
- an overstrong exact blocker-graph classification where only a forced core was
  proved;
- an insufficiently explicit equality chain in the non-attainment proof; and
- commercial language that compared nonidentical model classes as though only
  the number of scorecards changed.

## Evidence and adjudication

The accepted theorem rests on the self-contained analytic proof. The finite
certificate is independently checkable by exhaustive enumeration of all 16
routings and 13 arcs. Model-generated reviews and code paths are supporting
adversarial and regression evidence, not the final adjudicator.

Matthew performed the final claim and release review and accepts responsibility
for publication.

## Attribution language

A defensible concise description is:

> Matthew selected and directed the research program, set the verification and
> claim standards, repeatedly challenged and revised the work, and accepts
> responsibility for the release. GPT-5.6 Pro generated and developed
> substantial portions of the mathematics, code, adversarial analysis, and
> manuscript. Exact artifacts and hostile review were used to test the result;
> separate model sessions are not represented as independent human peer review.

Dmitry Rybin's 22 July 2026 counterexample was the direct catalyst for the
research line and is credited separately.
