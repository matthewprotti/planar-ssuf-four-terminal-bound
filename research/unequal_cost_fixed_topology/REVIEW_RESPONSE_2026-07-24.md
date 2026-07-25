# Response to First Adversarial Referee Report

The referee independently reproduced the census, two-trades, scalar lemma,
fixed-support identities, optimum \(L\), and trivial graph automorphism group,
but held UC-008 because the theorem imported an unpinned external reverse proof.

This revision closes the four cross-package P0 gates as follows:

| Gate | Resolution in this branch |
| --- | --- |
| UC-008 self-containment | Added `FIXED_TOPOLOGY_APPENDIX.md` and a complete local `FIXED_SUPPORT_ROUTING_LEMMA.md`; restated the lower family inside `EVERY_PAIR_CELL_THEOREM.md`. |
| Exact dependency hygiene | Added `DEPENDENCY_MANIFEST.json`; the release is now provenance-only, not an unexpanded proof dependency. |
| Independent finite replay | Added `independent_census_check.py`, which does not import the generator and searches all integer quotas. |
| Symbolic dependency audit | Added `symbolic_every_pair_check.py`, reconstructing pair maxima, convex identities, stationary point, lower-cell membership, and graph automorphisms. |

Additional P1 closures include route-cost-difference wording, a local topology
appendix, witness-existence caveats, strict-cell optimization protocol, prior-
art matrix, and artifact/claim consistency checks.
