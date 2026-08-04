# Candidate derivation notes

This subtree is a private release-candidate derivation from authenticated,
immutable sources. `SOURCE_PROVENANCE.json` records source and candidate hashes.
The repository does not carry raw reviewer prompts, model transcripts, private
run logs, or review ZIPs.

The substantive proof imports are unchanged except where the claim ledger
already authorized a derived editorial copy:

- R1 N001/N002 terminology was made conservative without changing the theorem.
- Python `assert` checks that disappear under `-O` were replaced with explicit
  runtime checks; packet-layout output writes and private paths were removed.
- GM-005 received candidate status metadata after its frozen R2 v2 acceptance.
- GM-006 was extracted from the authenticated many-scenario source as a
  standalone companion proof, without importing obsolete GM-005 reasoning.
- GM-008/009 received the R2 v3 status and the accepted nonblocking exposition
  clarification in the `t>2` branch.
- The scenario-cover proof received the five R3A nonblocking model/convention
  repairs and the exact narrow R3B v2 result label.
- The SC-006 theorem and canonical exact atlas are byte-identical to their
  controlling accepted sources.
- The integrated SC-006 replay explicitly requests noncanonical certificates,
  reproducing the accepted R3D computation. Canonical serialization is tested
  separately for the fixed atlas and is not part of the SC-006 claim.
- The first external human report is recorded with its exact raw-text hash and
  scope limitation; reviewer identity and independence are not inferred.
- `FULL_PROOF_REVIEW_MAP.md` makes every controlling analytic proof directly
  discoverable and separates it from finite corroboration.
- `TRUNK_PRIVATE_ARC_ENVELOPE.md` now states the all-thirteen-arc inequality
  used by GM-005/006, and `verify_arc_envelope.py` reconstructs it exactly.
- The stale final GM-005 sentence was corrected to agree with the already
  frozen R2-v2 acceptance recorded in that file's header.
- The one-scenario status banner was updated to the already frozen R1-v2
  disposition; the proof body and theorem statement are unchanged.
- The Nikolenko related-work metadata and dates were checked against the two
  primary Zenodo records dated 30 and 31 July 2026.

These transformations do not widen any theorem. The integrated manuscript is a
synopsis that points to the complete companion proofs; it is not a replacement
for them. The first external report is scope-limited and does not constitute a
full external review of the integrated candidate.
