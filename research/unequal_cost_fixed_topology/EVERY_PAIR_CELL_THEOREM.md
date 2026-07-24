# The Every-Pair Unequal-Cost Cell Has Exact Value \(L\)

## Setting

Keep the fixed four-terminal topology and path-difference supports from the
released manuscript.  Normalize \(d_{\max}=1\), so
\(d_i\in(0,1]\).  Let \(p_i\in[0,1]\) be the fractional cheap fractions.
Give terminal \(i\)'s full expensive route an arbitrary cost \(k_i>0\), with
cheap-route cost zero, and define

\[
\tau:=\sum_{i=1}^4 k_ip_i.
\]

A cheap set \(S\) is cost feasible exactly when \(k(S)\ge\tau\).

Let

\[
L:=\frac{299-41\sqrt{41}}{32}.
\]

## Theorem

Suppose every two-element cheap set is cost feasible and no one-element cheap
set is cost feasible.  Then the supremum, over all such real data, of

\[
\min_{S:\,k(S)\ge\tau}
\max_{a\in A}\bigl(\operatorname{flow}_{y^S}(a)-x(a)\bigr)
\]

is exactly \(L\).

## Proof

Write

\[
r:=\sum_{i=1}^4 p_i.
\]

Relabel the costs for this numerical argument only so that

\[
k_1\le k_2\le k_3\le k_4.
\]

The relabeling is not a claimed symmetry of the fixed graph; it is used only to
bound the scalar weighted average \(k\cdot p\).

Because no singleton is feasible,

\[
k_i<\tau\qquad(i=1,2,3,4),
\]

and in particular \(\tau>k_4\).  Since \(p_i\ge0\),

\[
\tau=\sum_i k_ip_i\le k_4\sum_i p_i=k_4r.
\]

Thus \(r>1\).

Every pair is feasible, including the pair formed by the two smallest costs.
Therefore

\[
\tau\le k_1+k_2.
\]

We claim that \(r\le2\).  Suppose instead that \(r>2\).  Among all vectors
\(p\in[0,1]^4\) with coordinate sum \(r\), the dot product with sorted positive
costs is minimized by filling the cheapest coordinates first.  For
\(2<r\le3\), this gives

\[
k\cdot p\ge k_1+k_2+(r-2)k_3.
\]

For \(3<r\le4\), the exact greedy lower bound is

\[
k_1+k_2+k_3+(r-3)k_4,
\]

which is at least \(k_1+k_2+(r-2)k_3\) because
\((r-3)(k_4-k_3)\ge0\).  Hence in all cases with \(r>2\),

\[
\tau=k\cdot p
 \ge k_1+k_2+(r-2)k_3
 >k_1+k_2,
\]

contradicting feasibility of the cheapest pair.  Therefore

\[
1<r\le2.
\]

Now inspect the reverse-bound argument in the released theorem on the
equal-full-cost, two-cheap model.  After cost feasibility establishes that all
six exactly-two-cheap routings are available, the proof depends only on:

- \(d_i\in(0,1]\) and \(\max_i d_i=1\);
- \(p_i\in[0,1]\);
- \(1<\sum_i p_i\le2\);
- availability of every exactly-two-cheap routing;
- the four fixed path-difference supports.

All of those conditions hold here.  The same boundary reduction, pair-deviation
formulas, convex combinations, and optimization of

\[
g(s,t)=s\left(4-s-t-\frac{s}{t}\right)
\]

therefore produce a cost-feasible two-cheap routing whose maximum upper
deviation is at most \(L\).  This proves the upper bound.

For the lower bound, the rational family in the released manuscript has equal
full expensive-route costs, no feasible singleton, every pair feasible, and
values approaching \(L\).  Equal costs are a special case of arbitrary
positive costs.  Hence the supremum in the present cell is at least \(L\).

The two bounds agree.  ∎

## Corollary

Any unequal-cost improvement over \(L\) on the fixed topology must make at
least one two-terminal cheap set cost infeasible.  Combined with the
feasible-singleton bound, the search is confined to the 94 threshold families
identified in `threshold_family_census.json`.

## Scope

This theorem does not resolve:

- any one of the remaining 94 labeled threshold cells;
- the global arbitrary-cost fixed-topology supremum;
- a different number of terminals or a different topology;
- the unrestricted planar constant.

It is an unrefereed follow-on argument and should be attacked independently
before any public theorem claim.
