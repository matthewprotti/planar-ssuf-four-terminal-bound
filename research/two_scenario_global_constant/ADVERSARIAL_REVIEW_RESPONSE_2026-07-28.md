# First-Round Response to Adversarial Review — RB-003 Major Revision (Historical)

**Historical status.** This file records the response that produced v4. The
subsequent second-round proof-only report is included as
`ADVERSARIAL_PROOF_ONLY_REVIEW_RB003_V4.md`; its local revisions are mapped in
`ADVERSARIAL_PROOF_ONLY_REVIEW_RESPONSE_RB003_V5.md` and integrated into v5.

## Disposition

The review found no counterexample to the central supremum claim but identified
publication-blocking language, one omitted proof step, self-containment gaps,
and overstatements about computation and commercial interpretation. All are
accepted. The v4 package treats RB-003 as a major revision rather than a
cosmetic edit.

## 1. Feasibility semantics: accepted and corrected

The model now defines per-scenario arc costs and derives

\[
C_j(y^R)-C_j(x)=k^{(j)}(R)-k^{(j)}\cdot q.
\]

A routing is feasible when

\[
C_j(y^R)\le C_j(x)
\]

for both scenarios. The paper consistently calls this “scenario-wise cost
non-increase” or “respecting both scenario budgets.” Equality is not required.

The finite certificate now records the fractional budgets and the actual
unsplittable costs. At `epsilon=1/1000`, feasible unsplittable costs are `0 or
1` in scenario 1 and `0 or 1000` in scenario 2, strictly below the fractional
budgets `2998.998` and `1998.999`.

## 2. No finite global extremizer: accepted and promoted to a corollary

The phrase “global extremizer” has been removed. The theorem now states an
exact non-attained supremum.

A new Corollary RB-003a proves non-attainment. Equality at `17/8` would force
the central star-triangle branch, `Delta=3/4`, and `h_u=1`. Since
`h_u=d_u q_u` with both factors at most one, this forces `d_u=q_u=1`. But the
non-omittable terminal `u` is blocked by some normalized scenario, so
`w_u>1`; normalization would then give

\[
1=\sum_iq_iw_i\ge q_uw_u>1,
\]

a contradiction.

The lower construction is therefore described as a rational extremizing
sequence in the intrinsic family `upward_closure{123,124,234}` (`F126` only as
historical nomenclature).

## 3. Missing unit-profit step: accepted and repaired

The one-knapsack lemma is now stated for every profit vector
`c_i in [0,1]`. It yields both required consequences:

\[
\sum_{i\in T}d_iq_i\le2
\]

by choosing `c_i=d_i`, and

\[
\sum_{i\in T}q_i\le2
\]

by choosing `c_i=1`.

Equation (16) is no longer presented as an unsupported special case of the
weighted inequality.

## 4. Self-containment: accepted and repaired

The theorem now contains:

- the full vertex and arc set;
- a rendered graph figure;
- the complete C/E path table;
- formal definitions of `x(a)` and `y^R(a)`;
- a derivation of the scenario cost inequalities;
- the five trunk supports and terminal-incidence sets;
- an intrinsic definition of the extremizing family; and
- a dependency appendix distinguishing proof dependencies from context.

`BASELINE_CONTEXT_AND_DEPENDENCIES.md` identifies the public release commit,
the follow-on census commit, the restricted benchmark `L`, the `149/18/1`
partition, and the historical `F126` name. None is a hidden dependency of the
RB-003 proof.

## 5. Computational claims: accepted and narrowed

The package no longer calls its two scripts independent mathematical
derivations. The second is now a **secondary regression implementation**.

The primary finite census has been strengthened:

- all 168 downsets are enumerated;
- 149 receive explicit positive integer threshold witnesses;
- all 18 excluded nonempty downsets receive exact two-trade impossibility
  certificates; and
- the remaining downset is the empty inadmissible family.

The 11,175 unordered threshold-pattern pairs are explicitly labeled an
**abstract blocker regression**. They need not admit one shared baseline `q`
and are not used to prove the analytic upper bound.

The denominator-16 calculation is labeled an **envelope grid regression**. It
checks grid points against the analytic envelope; it is not continuous
optimization.

The replay now authenticates the received artifacts against the SHA-256
manifest **before** regenerating outputs and checks them again afterward.
`REPLAY_REPORT.txt` is included in the manifest; only the manifest itself is
excluded from its own hash list.

## 6. Commercial claims: accepted and narrowed

The commercial document no longer says that a second scorecard “raises” the
constant by 86.44%, and no longer recommends against sequential optimization as
a theorem consequence.

The corrected interpretation is:

- the joint feasible region of two non-increase constraints can support a
  star-triangle obstruction approaching `17/8`;
- this motivates joint obstruction detection;
- it does not compare a defined sequential algorithm with a joint algorithm;
- `17/8 > L` is an arithmetic comparison across different model classes, not a
  causal estimate of adding one control; and
- the finite certificate uses weight ratios 3000 and 1000, with unbounded ratios
  in the limiting sequence.

The central-support wording is corrected from “cross four trunk arcs” to
“cross at least four trunk arcs”; the two sizes are five and four.

## 7. Mathematical disposition after revision

The following remain the central claims:

1. the exact fixed-graph two-scenario cost-nonincrease supremum is `17/8`;
2. the supremum is not attained by any finite legal instance;
3. a rational sequence in the intrinsic family
   `upward_closure{123,124,234}` approaches it;
4. the concrete `epsilon=1/1000` certificate has exact value `1061/500` and
   scaled unavoidable deviation 8488; and
5. the proof's only branch above two is the central star-triangle.

The v4 package remained a theorem draft pending the second-round hostile proof-only review and formal publication work. That second-round review is included separately in the v5 package.

## 8. External adversarial evidence retained as external evidence

The reviewer additionally reported an independent linear-feasibility
recognition of all 168 downsets and a 2.8-million-instance broad and targeted
numerical search, including ill-conditioned vectors and baselines near zero or
one, with no point above `17/8`. Those results are recorded as supporting
adversarial evidence. They are not reproduced by this package and are not used
as proof.
