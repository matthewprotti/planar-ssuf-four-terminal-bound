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

The assumption is a genuine restriction, not a without-loss-of-generality
normalization. No reorientation lemma is claimed for instances with \(k_i=0\)
or \(k_i<0\).

- Positive differences make cost-feasible cheap sets upward closed and yield a
  positive weighted-threshold family.
- Zero differences are boundary/closure cases that may collapse strict
  inequalities or make a terminal cost-neutral.
- Negative differences destroy the same upward-closed interpretation because
  choosing the nominally “cheap” route can increase the relative cost term.

Accordingly, titles, theorem statements, and conclusions use “positive
differences.” The 94-cell program concerns only the positive-difference domain.
Any future extension to zero or negative differences requires a new theorem and
new feasibility classification.
