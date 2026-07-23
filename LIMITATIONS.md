# Status and limitations

## Mathematical scope

- The value `(299 - 41*sqrt(41))/32` is a lower bound for the unrestricted
  planar constant and a sharp value only for the explicitly defined
  equal-full-cost, two-cheap-choice model on the fixed topology.
- The result does not establish global four-terminal optimality, fixed-graph
  optimality under unequal full-route costs, or the exact unrestricted
  planar constant.
- The document is an unrefereed research disclosure, not a peer-reviewed
  paper.

## Verification scope

- Exact enumeration proves the finite statement for the encoded graph and
  data.
- Symbolic scripts corroborate the displayed identities and optimization.
- Mutation tests show that representative corruptions are rejected; they are
  not exhaustive tests of every possible implementation error.
- The separate clean-room implementation was prepared with AI assistance.
  It reduces shared-code risk but is not independent human verification.
- Randomized stress testing of the restricted model is corroborative only;
  the manuscript's analytic argument is the proof.

## Novelty scope

Targeted searches conducted on 23 July 2026 found no exact public match for
the support pattern, finite ratio, radical in this setting, or restricted
theorem. The searches cannot rule out private, unindexed, differently worded,
or simultaneous work. No claim of exhaustive novelty clearance is made.

## Release controls

The public `v0.1.0` release preserves the following controls:

1. the deliberate no-license status remains explicit, with no ownership or
   affiliation claim introduced;
2. the final public-release diff, PDF, hashes, and repository visibility were
   checked before publication;
3. publication followed explicit authorization.

No mathematical defect is currently known in the stated claims. This means
only that the completed review passes found none.
