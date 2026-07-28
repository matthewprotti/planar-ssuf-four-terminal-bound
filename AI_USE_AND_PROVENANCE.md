# AI use, human responsibility, and research provenance

## Origin of the project

This work grew out of a multi-week conversation between Matthew Protti and
OpenAI GPT-5.6 Pro about recurring structural patterns in mathematical
breakthroughs and the kinds of questions that might be tractable in a
human-directed, model-assisted research loop. Dmitry Rybin's public
counterexample of 22 July 2026 was the direct catalyst for applying that
conversation to cost-constrained single-source unsplittable flow.

Rybin's contribution is prior and distinct. The present repository does not
claim ownership of, priority over, or authorship of his result.

## Division of labor

### Matthew Protti

Matthew:

- selected and framed the research targets;
- decided which natural variants to pursue;
- set the requirement for exact arithmetic, exhaustive finite checks, mutation
  tests, and hostile review;
- identified and forced correction of material errors and overclaims;
- repeatedly challenged whether intermediate lower bounds were globally sharp;
- chose the final theorem scope and public wording;
- reviewed and authorized the release; and
- accepts responsibility for the manuscript and repository.

### GPT-5.6 Pro and Codex

GPT-5.6 Pro generated and developed substantial portions of:

- construction and parameter searches;
- symbolic derivations and analytic proofs;
- exact verifiers and regression checks;
- adversarial review analyses;
- manuscript and documentation drafts; and
- release-engineering plans.

Codex and other model sessions implemented or reconstructed code paths,
performed repository-level checks, and attacked proposed claims. These
model-assisted checks are not independent human verification merely because
they were run in separate sessions or code paths.

AI systems are not listed as authors. The named human author is responsible for
what is released.

## Intervention record

The development record includes several material human interventions:

- rejecting early confidence as evidence;
- correcting a cost-normalization error;
- requiring exact all-routing reconstruction;
- separating finite certificates, limiting families, restricted sharpness, and
  global claims;
- refusing to stop at the valid but nonoptimal `17/16` two-scenario lower
  certificate;
- directing the search from the 18 new nonthreshold cells to the complete
  two-scenario parameter frontier;
- requiring proof-only hostile review after the `17/8` theorem emerged;
- correcting cost non-increase versus equality language;
- adding and proving non-attainment; and
- narrowing computational and commercial claims after review.

A fuller structured account appears in
`research/two_scenario_global_constant/AI_CONTRIBUTION_AND_INTERVENTION_RECORD.md`.

## Acceptance evidence

The release does not treat model confidence or fluent exposition as evidence.
Its evidence hierarchy is:

1. self-contained human-readable proof;
2. exact finite certificates and exhaustive enumeration for finite claims;
3. exact algebraic or combinatorial corroboration;
4. deliberately scoped secondary implementations and mutation tests;
5. hostile review reports and response matrices; and
6. explicit human sign-off.

Computational artifacts are labelled according to what they actually establish.
A checker that shares assumptions with the constructor is not described as
independent proof.

## Relation to the OpenAI agentic-science field report

OpenAI published *Scientific computing in the age of agentic AI: an
exploratory field report* on 28 July 2026, after the initial SSUF release and on
the day RB-003 was being prepared for publication. The report describes a
shift in human work from implementation toward specification, validation,
orchestration, and stewardship. It also warns that agent self-assessment is
not reliable completion evidence and emphasizes external acceptance targets,
staged iteration, and clear maintenance responsibility.

Those observations closely match the workflow independently developed here.
The report is cited as contemporaneous context only. OpenAI did not review,
validate, sponsor, or endorse this theorem or release.

Official sources:

- https://openai.com/index/scientific-computing-agentic-ai/
- https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf

## Stewardship and corrections

Matthew Protti is the release steward and repository maintainer. Reproducible
counterexamples, proof objections, and verifier discrepancies are welcome
through the repository issue tracker. Immutable tags are never silently
rewritten; a confirmed defect will be documented through an issue, erratum,
and, when required, a new release.

## Private development record

Private prompts and conversation transcripts are deliberately excluded. The
public proof, explicit data, review record, and executable checks are intended
to make the released claims auditable without exposing private conversations.

## Legal and institutional boundary

Authorship does not establish legal ownership. No institutional affiliation,
sponsorship, or institutional ownership is asserted. The public SSUF research
is separate from private Compliance Health product code, rule libraries,
customer configurations, data, and operational know-how. Conceptual influence
does not by itself establish a technical or legal dependency.
