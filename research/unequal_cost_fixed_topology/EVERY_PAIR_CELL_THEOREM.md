# The Every-Pair Unequal-Cost Cell Has Exact Value \(L\)

The value in this theorem is the common fixed-topology objective
\(\Phi(k,p,d)\) from `MASTER_OBJECTIVE_AND_COST_REALIZATION.md`.

## Cost-difference reduction

For terminal \(i\), let \(b_i\) and \(e_i^{\mathrm{cost}}\) be the full-demand
costs of its C and E routes under the underlying arc-cost vector. Assume

\[
k_i:=e_i^{\mathrm{cost}}-b_i>0.
\]

If \(p_i\) is the fractional C fraction and \(S\) is the unsplittable C set,
then

\[
\begin{aligned}
C(x)&=\sum_i\bigl(p_ib_i+(1-p_i)e_i^{\mathrm{cost}}\bigr)
=\sum_i e_i^{\mathrm{cost}}-\sum_i k_ip_i,\\
C(S)&=\sum_{i\in S}b_i+\sum_{i\notin S}e_i^{\mathrm{cost}}
=\sum_i e_i^{\mathrm{cost}}-\sum_{i\in S}k_i.
\end{aligned}
\]

Consequently

\[
C(S)\le C(x)
\quad\Longleftrightarrow\quad
k(S)\ge\tau,
\qquad
\tau:=k\cdot p.
\]

The common route-cost baseline cancels. Positivity of every \(k_i\) is what
makes the feasible family upward closed. This theorem makes no claim for zero
or negative route-cost differences; UC-018/019 treat those strata separately.

Normalize \(d_{\max}=1\), so \(d_i\in(0,1]\), and define

\[
L:=\frac{299-41\sqrt{41}}{32}.
\]

## Theorem

On the fixed topology in `FIXED_TOPOLOGY_APPENDIX.md`, suppose every two-element
C set is cost feasible and no one-element C set is cost feasible. Then the
supremum, over all real data satisfying these conditions, of

\[
\min_{S:\,k(S)\ge\tau}
\max_{a\in A}\bigl(\operatorname{flow}_{y^S}(a)-x(a)\bigr)
\]

is exactly \(L\).

## Upper bound

Write

\[
r:=\sum_i p_i.
\]

For the following scalar inequality only, reorder the paired coordinates
\((k_i,p_i)\) so that

\[
k_1\le k_2\le k_3\le k_4.
\]

This does not assert a symmetry of the fixed graph.

No singleton is feasible, so \(k_i<\tau\) for every \(i\), and in particular
\(\tau>k_4\). Since \(p_i\ge0\),

\[
\tau=k\cdot p\le k_4r,
\]

hence \(r>1\).

Every pair is feasible, including the pair with the two smallest costs, so

\[
\tau\le k_1+k_2.
\]

If \(r>2\), the dot product \(k\cdot p\) over \(p\in[0,1]^4\) with fixed sum
\(r\) is minimized by filling the cheapest paired coordinates first. For
\(2<r\le3\),

\[
k\cdot p\ge k_1+k_2+(r-2)k_3.
\]

For \(3<r\le4\), the exact greedy lower bound is

\[
k_1+k_2+k_3+(r-3)k_4,
\]

which is at least the preceding expression. Therefore \(r>2\) would imply

\[
\tau>k_1+k_2,
\]

contradicting feasibility of the cheapest pair. Thus

\[
1<\sum_i p_i\le2.
\]

All six exactly-two-cheap routings are feasible. The standalone
`FIXED_SUPPORT_ROUTING_LEMMA.md` now applies and supplies one such routing with
maximum upper deviation at most \(L\). This proves the upper bound without any
assumption that the four positive route-cost differences are equal.

## Lower bound

The lower family is restated here so the theorem is self-contained. Choose

\[
q\in(\sqrt3-1,1),
\qquad
0<\varepsilon<3-2q-q^2,
\]

and set

\[
(d_1,d_2,d_3,d_4)=(1,q^2,q,1),
\]

\[
(p_1,p_2,p_3,p_4)
=(1-q^2,\ q^2+2q-2+\varepsilon,\ 1-q,\ 1-q).
\]

Then

\[
\sum_i p_i=1+\varepsilon\in(1,2).
\]

Take equal positive differences \(k_i=1\). A set is feasible exactly when
\(|S|\ge1+\varepsilon\), hence precisely when \(|S|\ge2\). Thus the family lies
strictly in the every-pair/no-singleton cell.

Using the fixed supports, the six exactly-two-cheap routings have witness
values

\[
\begin{array}{c@{\qquad}c}
S&\text{witness lower bound}\\
\hline
\{1,2\},\{1,3\},\{1,4\},\{2,3\},\{2,4\}
&q^2(4-q^2-2q-\varepsilon),\\
\{3,4\}
&q^2(4-q^2-2q-\varepsilon)+q-q^2.
\end{array}
\]

Every routing with more than two cheap choices coordinatewise dominates a
two-cheap routing on the trunk. Hence every feasible routing overloads some arc
by at least

\[
R(q,\varepsilon)=q^2(4-q^2-2q-\varepsilon).
\]

At \(\varepsilon=0\), the function

\[
f(q)=q^2(4-q^2-2q)
\]

has its unique maximizer in the admissible interval at

\[
q_* =\frac{\sqrt{41}-3}{4},
\]

and

\[
f(q_*)=L.
\]

Rational \(q\) can approach \(q_*\), and positive rational \(\varepsilon\) can
approach zero, so values in this cell approach \(L\). This proves the matching
lower bound.

Therefore the exact supremum is \(L\). ∎

## Corollary

Any unequal-cost improvement over \(L\) on the fixed topology must make at
least one two-terminal cheap set infeasible. Combined with the feasible-
singleton lemma, this originally confined the search to the 94 labeled
threshold families identified by the exact census. Later UC-013, UC-017, and
UC-023 reductions leave the current 79-cell positive frontier.

## Release provenance

The family and analytic structure were first disclosed in immutable release
`v0.1.0`, commit
`087204eda4cc490cb59dd1988d7383c406288d2e`. This file restates every
mathematical ingredient used by the follow-on theorem; the release is provenance,
not an unexpanded proof dependency. Exact hashes are recorded in
`DEPENDENCY_MANIFEST.json`.
