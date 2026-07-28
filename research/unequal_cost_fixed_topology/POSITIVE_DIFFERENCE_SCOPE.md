# Positive Route-Cost-Difference Scope

For terminal \(i\), let \(b_i\) and \(e_i\) be the full-demand costs of its
chosen cheap and expensive routes, and put

\[
k_i=e_i-b_i.
\]

This workstream assumes

\[
k_i>0\qquad(i=1,2,3,4).
\]

The assumption is a genuine restriction for the positive-threshold cell
program, not a without-loss-of-generality normalization.

- Positive differences make cost-feasible cheap sets upward closed and yield a
  positive weighted-threshold family.
- Zero differences are boundary/closure cases that may collapse strict
  inequalities or make a terminal cost-neutral.
- Negative differences destroy the same upward-closed interpretation in the
  original C coordinates. `SIGNED_DIFFERENCE_REDUCTION.md` gives a coordinate
  complement for feasibility, but it is not an objective-preserving reduction
  to the positive case.

Accordingly, titles, theorem statements, and conclusions use “positive
differences” for this lane. The original 94-cell and intermediate 83-cell
counts are historical stages; after UC-013, UC-017, and UC-023, the current
positive-difference program contains 79 labeled cells in 11 abstract-label
orbits.

Subsequent theorems do address the excluded domains for the same master
objective \(\Phi\): UC-018 solves every non-all-positive nonzero sign/zero
stratum, and UC-019 solves the all-zero stratum. Those results do not make
positivity without loss of generality for UC-001, UC-008, or the positive-cell
census.
