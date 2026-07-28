# Agentic Research Validation Protocol

## Purpose

This protocol states how agent-generated mathematical and scientific-computing
work is converted into a claim that a human author may responsibly release. It
is a research-governance record, not a theorem and not a product specification.

The core rule is:

> Agent output becomes release evidence only after it is translated into an
> externally checkable claim, tested against a declared acceptance target, and
> adjudicated by a named human responsible for publication.

## 1. Claim before implementation

Every workstream begins with a claim record containing:

- the exact mathematical object or software behavior;
- the quantified domain;
- the objective or acceptance metric;
- explicit nonclaims;
- the evidence required for acceptance; and
- the person responsible for the final decision.

A numerical pattern, attractive construction, or confident narrative is not a
claim record.

## 2. Match autonomy to verifiability

Agent autonomy may increase only as the task becomes easier to verify
externally.

High-autonomy examples:

- exhaustive enumeration over a stated finite universe;
- byte-identical regeneration;
- exact rational arithmetic;
- a known-answer synthetic fixture;
- a proof assistant kernel check; or
- a predeclared regression suite with unambiguous outputs.

Lower-autonomy examples:

- interpreting an unfamiliar theorem;
- deciding whether a proof case split is exhaustive;
- claiming novelty;
- choosing a commercial or safety interpretation; or
- determining whether a plausible result is scientifically meaningful.

## 3. Evidence classes

Every reported result is labelled as one of:

1. **Human proof** - a self-contained argument intended to establish the claim.
2. **Exact finite certificate** - finite data plus exhaustive verification.
3. **Exact algebraic corroboration** - symbolic or rational checks of stated
   identities.
4. **Regression evidence** - tests that detect specified implementation drift.
5. **Numerical exploration** - search evidence used to generate hypotheses.
6. **Adversarial review** - a structured attempt to break a stated claim.
7. **Human adjudication** - the decision that the evidence supports release.

No weaker class is silently promoted into a stronger one.

## 4. Staged research loop

The default loop is:

1. formalize the object and acceptance target;
2. enumerate or search only the smallest useful domain;
3. export an exact witness or counterexample;
4. reconstruct the witness without relying on the search implementation;
5. derive a human-readable proof when a general claim is made;
6. write mutations aimed at the most likely failure modes;
7. obtain a hostile review with a bounded attack brief;
8. respond issue by issue;
9. replay from a clean environment; and
10. require named human sign-off.

The first implementation is a hypothesis generator. The last mile - edge cases,
quantifiers, proof closure, exact semantics, packaging, and maintenance - is
part of the scientific work, not post-processing.

## 5. Role separation

The same model family may be used in multiple roles, but the roles must be
recorded separately:

- **proposer:** searches for constructions or proof ideas;
- **implementer:** writes code or formal artifacts;
- **checker:** re-encodes the stated object and runs exact checks;
- **attacker:** seeks counterexamples, missing branches, or scope errors;
- **editor:** improves exposition without changing claims; and
- **human adjudicator:** determines what is accepted and released.

Separate model sessions reduce correlated implementation errors but do not
create independent human peer review.

## 6. Checker requirements

A checker must state:

- its input object;
- what it recomputes rather than trusts;
- arithmetic domain and dependency versions;
- every shared assumption with the constructor;
- generated outputs and expected hashes;
- negative mutations it rejects; and
- what it does not prove.

Where practical, supplied outputs are authenticated before execution and
regenerated outputs are compared byte for byte afterward.

## 7. Adversarial-review rules

An adversarial review must return one of:

- an exact counterexample;
- a proved correction;
- a replayed pass with explicit scope;
- an unresolved obligation with a minimal reproducer; or
- a statement that the evidence supplied was insufficient.

Generic confidence scores are not dispositions.

A review response must preserve the original issue identifier, state the exact
change, identify the evidence class, and list residual limitations.

## 8. Publication gate

Public release requires:

- final theorem and nonclaim ledger;
- self-contained proof for analytic claims;
- exact replay of finite claims;
- final human cold read;
- targeted literature and priority sweep;
- AI-use and intervention record;
- checker-assurance statement;
- immutable version and manifest;
- correction and maintenance policy; and
- explicit human authorization.

## 9. Post-release stewardship

A public result remains an object requiring maintenance. Confirmed defects are
not hidden by changing an immutable tag. They are recorded through an issue,
erratum, and new version when material. Reproduction failures are triaged as
scientific defects, environment failures, documentation defects, or unsupported
use.

## 10. Relation to contemporary agentic-science practice

OpenAI's 28 July 2026 exploratory field report describes recurring use of
external references, staged validation, human adjudication, and long-term
stewardship in agent-assisted scientific computing. This protocol was developed
through the SSUF and finite-Horn work and is consistent with those themes. The
report is context, not validation or endorsement of this project.
