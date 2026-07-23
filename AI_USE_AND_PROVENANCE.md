# AI use and provenance

## Human role and responsibility

Matthew Protti selected and framed the research problem, directed the
investigation, evaluated candidate constructions, identified a
cost-normalization error, required repeated adversarial review, exact
verification, mutation testing, and a separate reimplementation, and
determined the scope and wording of the proposed claims.

The named human author reviewed the released claims and accepts
responsibility for the manuscript and repository. AI systems are not listed
as authors.

## AI contribution

OpenAI GPT-5.6 Pro was used as a substantive research tool for candidate
construction, symbolic derivation, proof development, exact-verifier
development, adversarial review, and manuscript drafting.

Separate model sessions were used to challenge and reconstruct key steps. A
Codex execution session then performed a further clean-room computational
cross-check from the stated graph and numerical data, repaired the public
packaging, and ran release checks. These are separate AI-assisted checks, not
independent human verification or peer review.

Private prompts and conversation transcripts are deliberately excluded from
the release. The public-facing proof, explicit data, and executable verifiers
are intended to make the claims auditable without exposing that development
record.

## Development chronology

- **22 July 2026:** Dmitry Rybin publicly announced a counterexample to
  Goemans' cost conjecture. The present investigation began later that day.
- **22–23 July 2026:** the four-terminal construction, exact finite
  certificates, limiting family, and restricted-model sharpness argument were
  developed through a human-directed model and verification loop.
- **23 July 2026:** adversarial passes repaired cost normalization,
  quantifiers, graph definition, limiting arguments, all-arc verification,
  and exposition. The `335/294` certificate was reconstructed with exact
  enumeration in a separate implementation. A further clean-room program
  separately encoded the released data and reproduced the central
  computational checks.
- **Private repository record:** the repository was created privately at
  GitHub's server-recorded time. This is private provenance, not a public
  priority claim.
- **Potential public release:** if expressly approved, its canonical public
  timestamp will be the immutable GitHub release's server-recorded
  `published_at` value.

## Limits of the record

The mathematical document is unrefereed. The verification programs strongly
reduce transcription and finite-enumeration risk but do not establish
novelty, replace human peer review, or prove statements beyond their encoded
scope.
