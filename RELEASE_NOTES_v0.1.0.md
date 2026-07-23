# v0.1.0 — immutable research disclosure

This release publishes the manuscript, exact finite certificate, symbolic
checks, and reproducibility materials for the four-terminal construction.

## Included claims

- Exact finite certificate: `335/294`, verified over all 16 routings and all
  13 arcs.
- Limiting lower-bound family:
  `(299 - 41*sqrt(41))/32 = 1.139747070789...`.
- Restricted sharpness theorem for the fixed real equal-full-cost,
  two-cheap-choice model, with the same supremum for rational data.

## Verification

- exact primary verifier and exhaustive routing table;
- symbolic family and restricted-optimality checks;
- representative mutation tests;
- separate clean-room graph, finite, symbolic, and deterministic stress
  cross-check;
- PDF text preflight, secret scan, manifest verification, and visual review.

The separate implementation is AI-assisted computational corroboration, not
independent human review. The manuscript is unrefereed.

## Research provenance

The work grew out of a multi-week conversation between Matthew Protti and
OpenAI GPT-5.6 Pro about similarities among mathematical breakthroughs and
the kinds of difficult problems AI systems might help with. GPT-5.6 Pro did
most of the active mathematical heavy lifting; Matthew framed and directed
the inquiry, challenged the work, required exact verification, chose the
scope of the claims, and accepts responsibility for the release. The private
conversation transcript is not included.

## Immutable assets

- `ssuf-four-terminal-v0.1.0-source.tar.gz`;
- `ssuf_four_terminal_note_v5.pdf`;
- `SHA256SUMS.txt`.

Later corrections would be issued as new versioned releases. Once the
repository's immutable-release setting applies to a release, its tag and
assets must not be altered.
