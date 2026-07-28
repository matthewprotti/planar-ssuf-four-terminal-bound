# Completed Adversarial Proof-Only Review Brief — RB-003 v4

**Status:** completed. This was the attack brief used for the second-round
hostile proof-only review of v4. The resulting report is
`ADVERSARIAL_PROOF_ONLY_REVIEW_RB003_V4.md`; the proof-integrated response is
`ADVERSARIAL_PROOF_ONLY_REVIEW_RESPONSE_RB003_V5.md`. The original attack list
is retained below for auditability.

The brief asked the reviewer to attempt to falsify the claim

\[
\beta_G^{(2\mathrm{sc})}=17/8
\]

under the exact model in `TWO_SCENARIO_GLOBAL_CONSTANT.md`: an unsplittable
routing must **not increase** either scenario cost relative to the fractional
routing. Equality is not required.

Priority attacks:

1. Re-derive equation (4) from the graph-native cost definition and verify that
   the full-demand route-cost differences contain the demand factors in the
   stated way.
2. Reconstruct the graph and all C/E paths from the paper; check that the path
   table has exactly the intended routes and that every positive private-arc
   deviation is at most `d_max`.
3. Re-derive all four singleton-E trunk maxima in equation (13).
4. Attack the two-colour blocked-hypergraph matching lemma, especially strict
   inequalities, singleton hyperedges, and the union-of-colours step.
5. Attack Lemma 2 in its generalized `c_i in [0,1]` form. Check both choices
   `c_i=d_i` and `c_i=1` and all boundary cases of the one-knapsack LP.
6. Check that the `|A|=4` and `|A|=3` blocker-graph reductions exhaust actual
   shared-baseline instances; do not use the abstract 11,175-pair census as a
   substitute for this proof.
7. Re-optimize the central and outer star-triangle envelopes without using the
   supplied allocation argument.
8. Attack Corollary RB-003a. In particular, verify that equality at `17/8`
   forces `Delta=3/4`, `h_u=1`, `d_u=q_u=1`, and then contradicts normalized
   blocking of singleton `u`.
9. Reconstruct the rational lower sequence and the `epsilon=1/1000` graph
   certificate. Confirm that feasible unsplittable costs are below—not equal
   to—the fractional budgets.
10. Search numerically for instances above `17/8`, including ill-conditioned
    weights and baselines near zero or one. Treat this only as supporting
    evidence.
11. Check that all contextual comparisons with `L` are explicitly non-causal
    and that no sequential-algorithm claim is inferred from the theorem.
12. Check manifest authentication before and after replay and confirm that the
    frozen replay report is itself hashed.

A counterexample should include exact or high-precision values for `d`, `p`,
both scenario vectors, the best budget-respecting routing, and its witness arc.
