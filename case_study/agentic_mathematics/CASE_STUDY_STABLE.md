# Agentic mathematics under exact verification

## A four-terminal planar unsplittable-flow case study

- **Author:** Matthew Protti
- **Date:** 28 July 2026
- **Stable research version:** `v0.1.0`, commit
  `087204eda4cc490cb59dd1988d7383c406288d2e`, released 23 July 2026
- **Document boundary:** Stable-only process account; no successor theorem is
  incorporated
- **Review status:** Public, exact, reproducible, and unrefereed. No external
  human mathematical review has been requested or documented.

No institutional affiliation, sponsorship, or institutional ownership is
asserted.

## Summary

This case study describes a human-directed agentic mathematics project that
produced a public, exactly checkable research package for a four-terminal
planar single-source unsplittable-flow problem.

An AI research agent performed substantial construction search, symbolic
derivation, proof development, verifier development, adversarial critique, and
manuscript drafting. A second, role-separated AI context challenged the
builder's work. Matthew Protti selected and framed the problem, directed the
inquiry, evaluated proposed constructions, identified a consequential
cost-normalization error, required exact and adversarial checks, narrowed the
claims, decided the public evidence threshold, and accepted responsibility for
the release. A later Codex execution session separately re-encoded important
computational checks and supported release verification.

The stable release contains three carefully separated mathematical outcomes:

1. an attained finite certificate with ratio

   $$
   \frac{335}{294}=1.139455782312\ldots;
   $$

2. a planar lower-bound family converging to

   $$
   L=\frac{299-41\sqrt{41}}{32}
   =1.139747070789\ldots;
   $$

3. an exact supremum equal to \(L\) only within the explicitly restricted
   fixed-topology, equal-full-cost, two-cheap-choice model.

The first claim is exhaustively checked over all 16 unsplittable routings and
all 13 arcs using exact arithmetic. The package also contains symbolic checks,
representative mutation tests, deterministic reference outputs, and a
separately written AI-assisted implementation. The human-readable manuscript
remains authoritative. The software is strong corroborating evidence, but it
does not establish novelty, validate claims outside its specification, or
replace independent mathematical review.

## Scientific context

The project arose from a broader conversation about recurring structures in
mathematical breakthroughs and questions that might be tractable in a
human-directed, model-assisted loop. Dmitry Rybin's public counterexample of
22 July 2026 was the direct catalyst for applying that inquiry to
cost-constrained single-source unsplittable flow. Rybin's contribution is prior
and distinct.

Across 22–23 July, the human–builder–critic loop moved from that catalyst
through construction search, normalization repair, exact enumeration,
claim-scope repair, manuscript hardening, and authorized public release.

The research was released on 23 July 2026. OpenAI's exploratory field report
on agentic scientific computing appeared on 28 July. The SSUF work was not
developed in response to that report. The later comparison revealed a
methodological resemblance: agents can contribute substantial implementation
and reasoning work when humans define the scientific object, design external
acceptance targets, adjudicate discrepancies, limit the public claim, and
remain responsible for stewardship.

## Problem or opportunity

The target combined mathematical uncertainty with unusually strong
checkability. A candidate obstruction could be encoded as a small explicit
graph, and the key finite property could be tested over every routing and every
arc using exact arithmetic. At the same time, moving from one certificate to a
limiting family and then to a sharp theorem required human mathematical
judgment about quantifiers, model boundaries, and proof.

This made the problem suitable for a high-agency research loop. Agents could
search, derive, encode, and attack candidates quickly, while acceptance could
be tied to stronger evidence than an agent's own assessment: an explicit
theorem, graph and cost data, all routings, all arcs, symbolic identities,
invalid mutations, and immutable public artifacts.

## Project scope

### Exact theorem and claim boundaries

The stable theorem concerns the graph, demands, capacities, and cost model
specified in the `v0.1.0` paper and data files. The release supports only the
claims stated in that version.

It does not establish:

- the exact unrestricted planar constant;
- global four-terminal optimality;
- arbitrary-cost optimality on the fixed graph;
- applicability to other routing models without a new proof;
- exhaustive novelty clearance;
- independent human verification; or
- peer review or journal acceptance.

The restricted-model sharpness result is not a global-optimality result.
Successor-release claims are outside this case study and must be evaluated from
their own statement, proof, data, and validation package.

### Novelty posture

Targeted searches conducted on 23 July 2026 found no exact public match for the
released support pattern and constants. Those searches cannot rule out private,
unindexed, differently worded, or simultaneous work. The release therefore
makes no claim of exhaustive novelty clearance or priority over all related
work.

## The agentic research loop

The effective loop was:

1. the human research director framed the target and evidence threshold;
2. the builder agent searched, derived, encoded, and drafted;
3. exact checks compared the proposal with explicit acceptance conditions;
4. a role-separated critic attacked the claim, specification, proof, and code;
5. the human adjudicated discrepancies and required repair, narrowing, or
   rejection; and
6. the cycle repeated until the public claim matched the evidence.

During the core stable research, Matthew confirms that he worked with two
role-separated AI contexts: builder and adversarial critic. Codex later
provided a separate execution context for computational reconstruction,
stress-testing, packaging repair, and release checks.

Role separation reduced some single-context failure risk. It did not make the
critic independent of the model ecosystem, and it did not convert AI review
into human refereeing.

## Human role and responsibility

Matthew:

- selected and framed the research problem;
- chose which variants merited investigation;
- required exact arithmetic, all-routing enumeration, all-arc checking,
  mutation tests, and adversarial review;
- challenged whether intermediate results justified broader conclusions;
- detected and required repair of a material cost-normalization error;
- separated finite certificates, limiting families, restricted sharpness, and
  unrestricted claims;
- decided the public wording and nonclaims;
- authorized the stable release; and
- accepts responsibility for the released work and its correction.

The AI systems are not named as authors. Human authorship does not imply that
the AI contribution was merely clerical; the substantial contribution is
disclosed so readers can evaluate the process and its correlated-error risks.

## Validation and evidence

### Evidence hierarchy

The project uses the following hierarchy:

1. self-contained human-readable mathematical proof;
2. exact finite certificates and exhaustive enumeration for finite claims;
3. exact symbolic or algebraic corroboration;
4. deliberately scoped secondary implementations and mutation tests;
5. role-separated AI-assisted adversarial-review records; and
6. explicit human adjudication and release responsibility.

Fluent exposition, agent confidence, a successful numerical search, and a
passing text-regression check are not accepted as proofs.

### Proof versus computation

The verifier can establish that the encoded finite instance has the claimed
properties. It cannot by itself prove that the encoding is the intended
mathematical object, establish the analytic limiting argument, or clear
novelty. Those responsibilities remain in the specification, proof, public
data, and human adjudication.

The finite certificate permits unusually strong checking:

- four commodities give \(2^4=16\) unsplittable route choices;
- every routing can be reconstructed explicitly;
- every one of the 13 arcs can be checked;
- costs and overloads can be evaluated with exact integers or rationals; and
- deliberately invalid mutations can test whether a checker rejects nearby
  false instances.

### Correlated-error controls

Because agents helped create both proof and code, passing code could share a
mistaken assumption with the mathematical draft. The project therefore added:

- explicit graph and path data;
- all-routing and all-arc checking;
- a clean-room AI-assisted reimplementation, accurately labelled as
  computational corroboration;
- symbolic identities;
- representative invalid mutations;
- deterministic reference outputs;
- a manifest of public files; and
- immutable tagged artifacts.

These measures reduce selected failure modes. They do not create independent
human verification.

### What remains dependent on human mathematical judgment

Executable checks do not decide whether the theorem asks the right scientific
question, whether every intended hypothesis has been encoded, whether an
analytic limiting argument is complete, or whether the novelty search has
found all relevant work. Those questions require mathematical reading,
comparison with the literature, claim adjudication, and responsibility for any
correction.

## Reproduce the stable checks

The canonical object is the immutable `v0.1.0` tag. From a new clone:

```bash
git clone https://github.com/matthewprotti/planar-ssuf-four-terminal-bound.git
cd planar-ssuf-four-terminal-bound
git checkout v0.1.0
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r verification/requirements.txt
python scripts/verify_all.py
python scripts/manifest.py
python scripts/release_preflight.py --public
```

The expected full-verification output is `FULL VERIFICATION PASS`. In the
stable release, the manifest checks 26 files and the public package-hygiene
preflight checks 27 files. A successful replay is reproducibility evidence,
not independent human proof review.

The stable release records these public asset hashes:

- paper PDF:
  `d9efdadb25eb176a64dbd186f95d78e2a00b83c9a07b752b1a58c0f4d93b690d`;
- source archive:
  `746fa1a07006ade6ec22ac3fca83370afe359d001b045bccecaefa80cb11a4de`;
- release checksum sidecar:
  `0c9ee78ed8a92fc4a3d28f4cfb40be7cee7ac325d8e073acd314b56c90a92be5`.

Reproducers should compare against the tagged release, not an untagged working
copy.

## Mathematical outcome

### Attained finite certificate

The stable construction has four demands with maximum demand \(294\). Each
commodity has a cheap path and an expensive path on a compact planar acyclic
graph. The cost model is calibrated so a cost-nonincreasing unsplittable
routing must choose a sufficient number of cheap paths. Exact enumeration of
all 16 routings shows that the smallest possible maximum upper overload is
\(335\). Hence the attained normalized ratio is

$$
\frac{335}{294}.
$$

The certificate is finite and directly inspectable. It is not merely a sampled
optimization result.

### Limiting planar lower bound

A rational parameter family yields feasible instances whose ratios converge to

$$
L=\frac{299-41\sqrt{41}}{32}.
$$

This proves that the unrestricted planar constant is at least \(L\). It does
not prove that the unrestricted constant equals \(L\).

### Restricted-model sharpness

Within the fixed-topology equal-full-cost, two-cheap-choice model explicitly
defined in the paper, the analytic upper argument matches the limiting family.
Therefore \(L\) is the exact supremum in that restricted model. The qualifiers
are part of the theorem.

## Obstacles and failure modes

### Cost normalization

An early construction did not correctly implement the intended equal
full-choice cost logic. Matthew detected the discrepancy during adversarial
review. The repair placed costs on private expensive-path arcs and normalized
them so every full expensive choice had the intended cost. Exact cost checks
and a cost mutation were added.

### Quantifier and scope repair

Intermediate computational evidence supported a promising lower bound, but
did not justify global optimality. The final release separates:

- one attained finite certificate;
- one limiting planar lower-bound family; and
- one exact result in a restricted model.

### Graph and path repair

The public artifact was revised so the graph, paths, and arc contributions are
explicit rather than inferred from prose. This makes all-routing reconstruction
and external reimplementation possible.

### Selected-arc versus all-arc checking

Checking only the most visibly congested arcs could miss a violation
elsewhere. The verifier was strengthened to evaluate every arc for every
routing.

### Review terminology

A role-separated AI critic can find real defects, but “reviewer” as a
functional role must not be mistaken for an independent human referee. The
accurate description is role-separated AI-assisted adversarial review.

## Lessons and reflections

### Safe autonomy rises with checkability

The finite certificate supported unusually high agent autonomy in search and
implementation because acceptance could be tied to a small, exact, externally
inspectable object. This is a methodological heuristic, not a theorem about AI
reliability.

### Exact code can verify the wrong specification

Exact arithmetic prevents floating-point ambiguity; it does not guarantee that
the encoded graph, costs, or theorem match the intended problem. Specification
review and explicit data remain essential.

### Corrections are evidence

The cost-normalization and scope corrections reveal where the process was
fragile and which controls mattered. A case study that reported only the final
success would hide the strongest process evidence.

### Role separation helps without creating independence

Builder and critic roles can expose different mistakes. Shared model families,
overlapping specifications, and common context still create correlated failure
risks. Independent human mathematical review remains a separate evidence
class.

### Public reproducibility can replace private-process disclosure

Readers do not need private prompts or complete conversation transcripts to
inspect the released claim. The proof, graph data, exact certificate,
verifiers, mutations, hashes, and version history provide the relevant public
evidence.

### The OpenAI report is a comparator, not validation

OpenAI's July 2026 field report describes researchers shifting effort toward
specification, verification, orchestration, and stewardship when agents can
work against strong acceptance targets. The SSUF process independently showed
that pattern in original mathematics. The comparison does not validate the
theorem, and no causal relationship, sponsorship, review, or endorsement is
claimed.

## Long-term stewardship

Matthew Protti is the named author and release steward. The maintenance
commitment is to:

- preserve immutable tags;
- accept precise objections and reproduction reports;
- distinguish theorem, software, documentation, and packaging defects;
- publish an erratum or new version rather than rewrite a release; and
- keep later extensions separate from the stable claim.

Reporting guidance appears in [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Current external-review status

The evidence classes are:

- public proof and exact data: documented;
- exact finite enumeration: documented;
- symbolic and mutation checks: documented;
- author review and release decision: documented;
- role-separated AI-assisted adversarial review: documented;
- independent human reproduction: not documented;
- expert human proof review: not documented; and
- formal peer review: not documented.

No external human mathematical review has been requested or documented.
Internal preparation alone would not constitute review evidence. Any future
record should identify the reviewed version, date, scope, materials,
objections, dispositions, and outcome, with permission for public attribution.

## Public artifacts

The stable record consists of:

- the immutable
  [`v0.1.0` tag](https://github.com/matthewprotti/planar-ssuf-four-terminal-bound/tree/v0.1.0);
- the stable paper PDF and TeX source under `paper/`;
- explicit instance data under `data/`;
- exact and symbolic checks under `verification/`;
- deterministic expected outputs;
- mutation tests;
- `SHA256SUMS.txt`;
- `PRIORITY_DISCLOSURE.md`;
- `AI_USE_AND_PROVENANCE.md`; and
- `LIMITATIONS.md`.

The GitHub release's server-recorded publication time is the deliberate
canonical public timestamp. Earlier private repository events are not
presented as public priority.

Private prompts and conversation transcripts are not required to reproduce the
released claims and are deliberately excluded.

## Author-contribution and AI-use statement

Matthew Protti contributed conceptualization, problem selection, methodology,
research direction, validation design, adversarial review, error detection,
claim adjudication, project administration, writing review and editing, the
public-release decision, and responsibility for the released claims.

GPT-5.6 Pro contributed construction search, symbolic derivation, proof
development, verifier development, adversarial critique, and manuscript
drafting. Two role-separated AI agent contexts were used during the core
research and review process. Codex later contributed separate computational
reconstruction, stress testing, package repair, and release verification.

AI systems are not authors. The named human author accepts responsibility for
the released claims and corrections.

## References

1. Matthew Protti, *A Four-Terminal Planar Lower Bound and a Sharp Equal-Cost
   Gadget for Cost-Preserving Unsplittable-Flow Rounding*, `v0.1.0`,
   23 July 2026.
2. Dmitry Rybin, public counterexample disclosed 22 July 2026; see the stable
   paper for the exact citation and scope.
3. OpenAI, *Scientific computing in the age of agentic AI: an exploratory
   field report*, 28 July 2026:
   https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf

## Version boundary

This case study is tied to the immutable `v0.1.0` release. It does not add a
theorem, modify a release asset, incorporate successor-release mathematics, or
claim external review. Any future case study revision should state its exact
scope and version history.
