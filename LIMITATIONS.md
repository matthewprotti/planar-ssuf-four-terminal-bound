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

## Unreleased unequal-cost follow-on

- The follow-on work under `research/unequal_cost_fixed_topology/` is not part
  of the immutable v0.1.0 manuscript or release.
- All of its value claims use the fixed-graph, two-route objective
  \(\Phi(k,p,d)\) in `MASTER_OBJECTIVE_AND_COST_REALIZATION.md`.
- The explicit private-arc construction shows that signed route-cost
  differences are realizable with nonnegative, commodity-independent arc
  costs. It does not identify an optimizer or establish global sharpness.
- The current strictly positive open frontier is 79 labeled cells in 11
  abstract-label search orbits. The 94- and 83-cell counts are historical
  stages, and the orbit quotient is not a fixed-graph symmetry reduction.
- Ten current open cells have exact interior lower certificates above one.
  F042's older certificate remains historical evidence, but UC-023 solves that
  cell and removes it from the current atlas.
- The follow-on work does not establish the exact arbitrary-cost fixed-graph
  value, four-terminal optimality, or the unrestricted planar constant.

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
- In the follow-on work, human-readable inequalities remain the proofs.
  Census, exact-algebra, finite-grid, and witness scripts are corroboration,
  and a successful deterministic replay is not independent human review.

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

No mathematical defect is currently known in the stated v0.1.0 or follow-on
claims. This means only that the completed internal review passes found none;
the follow-on work has not been promoted to a new release.
