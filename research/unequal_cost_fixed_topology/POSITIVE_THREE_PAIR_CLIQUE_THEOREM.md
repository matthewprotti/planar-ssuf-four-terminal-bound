# Exact Values for the Four Positive Three-Pair Clique Cells

Fix an omitted terminal `j` and let `Q` be the other three terminals. Consider
the strictly positive route-cost-difference cell whose minimal feasible C sets
are exactly the three two-element subsets of `Q`. Equivalently, a routing is
cost feasible exactly when it chooses C for at least two terminals of `Q`; the
omitted terminal may be C or E.

These are the four labeled cells `F042`, `F068`, `F094`, and `F105`.

## Theorem UC-023

The exact fixed-topology supremum of the pure three-pair clique cell is

\[
\boxed{
\begin{cases}
9/8,&j\in\{2,3,4\},\\[1mm]
1,&j=1.
\end{cases}}
\]

The same values hold over rational data as suprema. In particular all four
cells are strictly below

\[
L=\frac{299-41\sqrt{41}}{32}.
\]

## 1. The cell forces a three-terminal boundary regime

Let `k_i>0` and `tau=k·p`. Every pair contained in `Q` is feasible, every
singleton is infeasible, and every pair `{i,j}` with `i in Q` is infeasible.
Put

\[
r_Q:=\sum_{i\in Q}p_i.
\]

For each `i in Q`, infeasibility of `{i,j}` gives

\[
\tau>k_i+k_j.
\]

Since `k_j p_j<=k_j`,

\[
\sum_{h\in Q}k_hp_h=\tau-k_jp_j
>k_i+k_j(1-p_j)\ge k_i.
\]

Thus the weighted average on `Q` exceeds every individual `k_i`, which is
impossible if `r_Q<=1`. Hence

\[
r_Q>1.
\tag{1}
\]

Now sort the three weights on `Q` as `a<=b<=c`. The pair with weights `a,b` is
feasible, so

\[
\tau\le a+b.
\]

Also `sum_{Q} k_i p_i<=tau`. If `r_Q>2`, the minimum weighted sum on
`[0,1]^3` with coordinate sum `r_Q` is

\[
a+b+(r_Q-2)c>a+b,
\]

which is a contradiction. Therefore

\[
1<r_Q\le2.
\tag{2}
\]

Scale the three fractions on `Q` to

\[
\widehat p_i=p_i/r_Q,
\qquad i\in Q,
\]

so they sum to one and satisfy `hat p_i<=p_i`. For any of the three feasible
pair routings on `Q`, decreasing these fractions can only increase its trunk
deviation: selected C contributions `d_i(1-p_i)` increase and the unselected E
contribution `-d_i p_i` becomes less negative. Route terminal `j` historically
E. Its trunk contribution is nonpositive and its positive private deviation is
at most one. It is enough to prove the bound for the normalized three-terminal
problem.

## 2. Chain omissions: terminals 2, 3, or 4

When `j` is 2, 3, or 4, the three remaining path-difference supports have the
chain form described in `NONPOSITIVE_DIFFERENCE_THEOREM.md`. Naming the outer
supports `A,C` and the middle support `B`, the three pair maxima above one are

\[
M_{AB}=e_A+e_B,
\qquad
M_{BC}=e_B+e_C,
\]

\[
M_{AC}=\max\{e_A,e_C,e_A+e_C-\ell_B\}.
\]

With `p_A+p_B+p_C=1`, the convex/minimax calculation gives

\[
\min\{M_{AB},M_{AC},M_{BC}\}
\le
1+\frac{p_B}{2}-\frac{p_B^2}{2}
\le\frac98.
\]

This proves the upper bound.

For the matching lower family, choose rational `epsilon,delta,eta>0` tending to
zero. Give the three terminals in `Q` unit positive cost differences and give
terminal `j` cost difference `delta`. Set

\[
p_A=p_C=\frac{1+\epsilon}{4},
\qquad
p_B=\frac{1+\epsilon}{2},
\qquad
p_j=1,
\]

\[
d_A=d_C=1,
\qquad
d_B=\frac{3-\epsilon}{4},
\qquad
d_j=\eta.
\]

The threshold is `1+epsilon+delta`. Exactly the three pairs of `Q`, their
supersets in `Q`, and the versions with terminal `j` added are feasible. Every
feasible routing has maximum deviation at least

\[
\frac{(3-\epsilon)^2}{8}-\eta,
\]

which tends to `9/8`.

## 3. Nested omission: terminal 1

When `j=1`, the remaining terminals are `2,3,4` and have the nested form from
`NONPOSITIVE_DIFFERENCE_THEOREM.md`. After normalization, the two special pair
maxima `T_2,T_3` satisfy

\[
(1-p_3)T_2+p_3T_3
=d_2p_4+d_4(1-p_4)\le1.
\]

Thus one feasible pair has maximum upper deviation at most one.

For the matching lower sequence, take equal positive differences on terminals
`2,3,4`, a positive difference `delta` on terminal 1, and

\[
p_2=\epsilon,
\qquad p_3=1,
\qquad p_4=0,
\qquad p_1=1.
\]

The threshold is `1+epsilon+delta`, so the cell is exact. With unit demands on
terminals `2,3,4` and demand `eta` on terminal 1, every feasible routing has a
private deviation at least `1-epsilon`. Hence the supremum is one. ∎

## Consequence for the positive frontier

UC-017 reduced the strictly positive frontier to 83 labeled cells in 12
abstract-label orbits. UC-023 resolves the four-cell three-pair-clique orbit,
leaving

\[
\boxed{79\text{ labeled cells in }11\text{ abstract-label orbits}.}
\]
