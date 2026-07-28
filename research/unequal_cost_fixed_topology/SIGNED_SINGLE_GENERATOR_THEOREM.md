# Signed Single-Generator Cells Have Exact Value One

Let `z_i=1` denote the historical C route and let `p_i` be its fractional C
proportion.  Let

\[
k_i=e_i^{\mathrm{cost}}-b_i
\]

be the full-demand E-minus-C route-cost difference.  For every nonzero
coordinate put

\[
\sigma_i=\operatorname{sign}(k_i),\qquad w_i=|k_i|,
\]

and orient the variables by

\[
(u_i,q_i)=
\begin{cases}
(z_i,p_i),&\sigma_i=+1,\\
(1-z_i,1-p_i),&\sigma_i=-1.
\end{cases}
\]

Then cost feasibility is the positive threshold condition

\[
\sum_iw_i u_i\ge\sum_iw_iq_i.
\]

All value statements below refer to the physical master objective
\(\Phi(k,p,d)\) in `MASTER_OBJECTIVE_AND_COST_REALIZATION.md`. Its private-arc
lemma realizes every signed vector here with nonnegative arc costs.

## Theorem UC-017

Suppose the oriented cost-feasible family is the upward closure of one set

\[
S\subseteq\{1,2,3,4\},\qquad |S|\ge2.
\]

Then, on the fixed four-terminal topology, the supremum of the minimum
cost-feasible maximum upper deviation is exactly

\[
1.
\]

The theorem holds for every one of the 16 fully nonzero sign patterns.  It also
continues to hold when cost differences are zero only outside `S`; those
coordinates are cost-free and may be routed on their historical E paths in the
upper-bound route.  A zero difference on a member of `S` is impossible if `S`
is genuinely a minimal threshold generator.

## Upper bound

Write

\[
K:=\sum_iw_i,\qquad
\theta:=\sum_iw_iq_i,\qquad
R:=K-\theta=\sum_iw_i(1-q_i).
\]

For every `i in S`, the oriented set `V\{i}` does not contain `S` and is
infeasible.  Hence

\[
K-w_i<\theta,
\qquad\text{so}\qquad
R<w_i.
\]

Therefore

\[
\sum_{i\in S}(1-q_i)<1. \tag{1}
\]

Choose the oriented feasible set

\[
U:=S\cup\{i:\sigma_i=-1\}.
\]

In historical route coordinates this means:

- if `i in S` and `k_i>0`, choose C;
- if `i in S` and `k_i<0`, choose E;
- if `i not in S`, choose E; and
- for a zero-cost coordinate outside `S`, also choose E.

Every terminal outside `S` then contributes nonpositively on every trunk arc.
A negative-sign member of `S` also contributes nonpositively.  Thus the only
positive trunk contributions come from positive-sign members of `S`, and their
sum is bounded by

\[
\sum_{\substack{i\in S\\\sigma_i=+1}}d_i(1-p_i)
=\sum_{\substack{i\in S\\\sigma_i=+1}}d_i(1-q_i)
\le\sum_{i\in S}(1-q_i)<1.
\]

Every positive private-arc deviation is at most `d_i<=1`.  The selected route
therefore has maximum upper deviation at most one.

## Matching lower family

Fix `j in S`.  Choose rational `epsilon,delta>0` satisfying

\[
\epsilon+(4-|S|)\delta<1.
\]

Set

\[
w_i=\begin{cases}1,&i\in S,\\ \delta,&i\notin S,\end{cases}
\qquad q_j=\epsilon,
\qquad q_i=1\quad(i\ne j).
\]

Here

\[
\theta=\sum_iw_iq_i
=|S|-1+\epsilon+(4-|S|)\delta.
\]

If an oriented set contains `S`, its weight is at least
\(|S|>\theta\). If it misses a member of `S`, its weight is at most
\(|S|-1+(4-|S|)\delta<\theta\). Thus the exact oriented feasible family is the
upward closure of `S`, including strict separation from every losing set. Set
`d_j=1`.
Every feasible oriented set contains `j`.

- If `k_j>0`, this forces historical C and gives private deviation
  `1-p_j=1-q_j=1-epsilon`.
- If `k_j<0`, it forces historical E and gives private deviation
  `p_j=1-q_j=1-epsilon`.

Hence every feasible routing has maximum upper deviation at least
`1-epsilon`.  Letting rational `epsilon` tend to zero proves the matching lower
bound.

## Consequences

1. In the all-positive lane, the 11 single-generator cells—six pair generators,
   four triple generators, and the full-set generator—have exact value one.
2. At the UC-017 stage, the positive-difference unresolved frontier falls from
   89 labeled cells to the historical **83 labeled cells**, and sequentially
   from 13 abstract-label search orbits to **12 orbits**. Measured from the
   initial post-UC-008 remainder, UC-013/017 together give 15→12 orbits.
   UC-023 then reduces the current frontier to 79 labeled cells in 11
   abstract-label search orbits.
3. Across nonzero signed differences, the theorem resolves 11 oriented
   generators for each of 16 sign patterns, i.e. 176 oriented parameter regimes.
   This is a count of sign-pattern/generator regimes, not necessarily 176
   distinct un-oriented feasible set systems.
4. Zero coordinates outside the unique generator are covered by the same
   argument: they do not affect feasibility, the upper route sends them E, and
   every feasible route still forces the selected generator coordinate used by
   the lower sequence. Other zero strata are handled by UC-018/019, not by
   UC-017 alone.

## Exact executable check

```bash
python signed_single_generator_check.py
```

The checker uses `Fraction` arithmetic to verify all 176 nonzero signed regimes,
construct the exact lower family, enumerate every physical route, check all five
trunk and private-route deviations, and test representative zero-coordinate
boundaries.

## Nonclaims

The theorem does not cover oriented families with two or more minimal
generators.  It does not solve all 1,881 signed unate feasibility systems, all
zero-coordinate strata by itself, the 79-cell current positive-difference
frontier after UC-023, or the unrestricted planar constant. The historical
83-cell count is the frontier immediately after UC-017.
