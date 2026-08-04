# The Global Arbitrary One-Scenario Constant on the Four-Terminal SSUF Gadget

**Status:** proof-complete private theorem; frozen R1-v2 claim-level
`ACCEPT_AS_STATED`, with packet-level editorial repairs recorded in the derived
candidate.  
**Date:** 1 August 2026.  
**Scope:** the fixed directed four-terminal gadget and its two designated paths per terminal. This document does **not** claim the unrestricted planar SSUF constant.

Matthew's completed no-error mathematical review covered only the immutable public `v0.2.1` corpus. It did not cover this private theorem.

The R1-v2 disposition is internal and AI-assisted. It is not external human
review, journal peer review, proof-assistant verification, or publication
clearance.

## 1. Main result

Let

\[
L:=\frac{299-41\sqrt{41}}{32}
  =1.139747070789\ldots .
\]

For one nonnegative, commodity-independent arc-cost scenario, arbitrary positive demands, and arbitrary fractional proportions on the fixed gadget, let \(\Phi\) be the normalized minimum, over cost-nonincreasing unsplittable routings, of the maximum upper arc-load deviation.

### Theorem OS-001

\[
\boxed{
\sup \Phi=L.
}
\]

The same supremum is obtained after restricting all input data to rational numbers.

The theorem asserts a supremum approached by rational instances. It does not assert that a maximizing legal instance exists, and no separate attainment or nonattainment theorem is claimed here.

More strongly, in the strictly positive full-demand E-minus-C cost-difference lane:

1. the complementary all-C-pairs/no-C-singleton cell has exact supremum \(L\); and
2. every other positive threshold cell has value at most
   \[
   \boxed{\frac98}.
   \]

Since \(9/8<L\), arbitrary one-scenario route costs do not improve the released fixed-gadget lower family.

## 2. Model and imported results

Normalize \(d_{\max}=1\), so \(0<d_i\le1\). Terminal \(i\) sends fractional proportion \(p_i\in[0,1]\) on its C path and

\[
q_i:=1-p_i
\]

on its E path. Put

\[
h_i:=d_iq_i,
\qquad
\ell_i:=d_ip_i=d_i-h_i,
\qquad
H:=\sum_{i=1}^4h_i.
\tag{1}
\]

The proof imports three results from the pinned fixed-topology package:

- the complementary all-C-pairs/no-C-singleton positive cell has exact supremum \(L\);
- every nonzero cost-difference stratum that is not strictly all-positive has value at most \(9/8\); and
- the identically zero cost-difference stratum has exact value \(4/5\).

The new argument below is self-contained about the positive-lane reduction, blocker-cover duality, the finite four-label cover classification, and every graph-specific routing inequality used to bound the remaining cells.

## 3. Fixed support formulas

The trunk-difference supports are

\[
I_1=\{a_1,a_2,a_3\},
\quad
I_2=\{a_1,a_2,a_3,a_4,a_5\},
\]

\[
I_3=\{a_2,a_3,a_4,a_5\},
\quad
I_4=\{a_3,a_4\}.
\tag{2}
\]

If terminal \(i\) is routed C, it contributes \(h_i\) on every arc in \(I_i\); if it is routed E, it contributes \(-\ell_i\). Every positive private-arc deviation is at most \(d_i\le1\). Consequently, only trunk deviations above one require analysis.

We will use the following exact trunk maxima.

### 3.1 One E choice

If only terminal \(r\) is routed E, the C-set is \([4]\setminus\{r\}\), and the trunk maximum is

\[
\begin{array}{c|c}
 r & M^{E}_r\\
\hline
1&H-h_1,\\
2&H-d_2,\\
3&\max\{h_1+h_2,\ H-d_3\},\\
4&H-h_4.
\end{array}
\tag{3}
\]

### 3.2 Exactly two C choices

For C-set \(S\),

\[
\begin{array}{c|c}
S&M^C_S\\
\hline
12&h_1+h_2,\\
13&h_1+h_3-\ell_2,\\
14&\max\{h_1-\ell_2,\ h_1+h_4-\ell_2-\ell_3\},\\
23&h_2+h_3,\\
24&\max\{h_2-\ell_1,\ h_2+h_4-\ell_3\},\\
34&h_3+h_4-\ell_2.
\end{array}
\tag{4}
\]

### 3.3 Exactly three C choices

\[
\begin{array}{c|c}
S&M^C_S\\
\hline
234&h_2+h_3+h_4,\\
134&h_1+h_3+h_4-\ell_2,\\
124&\max\{h_1+h_2,\ h_1+h_2+h_4-\ell_3\},\\
123&h_1+h_2+h_3.
\end{array}
\tag{5}
\]

All formulas follow by direct substitution into (2).

## 4. E-side normalization

Assume first that all four full-demand E-minus-C cost differences are strictly positive:

\[
k_i>0.
\]

Represent an unsplittable routing by its E-set \(R\subseteq[4]\). Cost non-increase is equivalent to

\[
k(R)\le k\cdot q.
\tag{6}
\]

If \(q=0\), the fractional flow is already the all-C unsplittable route and has value zero. Otherwise put

\[
B:=k\cdot q>0,
\qquad
w_i:=\frac{k_i}{B}.
\]

Then

\[
\sum_iq_iw_i=1,
\tag{7}
\]

and

\[
R\text{ is feasible}
\quad\Longleftrightarrow\quad
w(R)\le1.
\tag{8}
\]

Thus the feasible E-sets form a positive weighted-threshold downset.

If an E-triple is feasible, its complementary C-set is a singleton. Only that one C terminal can contribute positively on the trunk, so the route value is at most one. Hence we may assume that no E-triple is feasible.

If all six E-pairs are feasible, then all six complementary C-pairs are feasible, while no complementary C-singleton is feasible. This is the previously solved all-C-pairs/no-C-singleton cell and has value at most \(L\).

It remains to prove:

> If no E-triple is feasible and at least one E-pair is blocked, then some feasible route has value at most \(9/8\).

## 5. Blocker matching and blocker cover

Let \(\mathcal B\) be the inclusion-minimal infeasible E-sets. Every \(T\in\mathcal B\) satisfies

\[
w(T)>1.
\tag{9}
\]

### Lemma 1 — one-scenario blocker matching

For nonnegative coefficients \(\lambda_T\) satisfying

\[
\sum_{T\ni i}\lambda_T\le q_i
\qquad(i=1,2,3,4),
\tag{10}
\]

we have

\[
\sum_{T\in\mathcal B}\lambda_T<1.
\tag{11}
\]

**Proof.** If all \(\lambda_T\) vanish, the conclusion is immediate. Otherwise,

\[
\sum_T\lambda_T
<
\sum_T\lambda_Tw(T)
=
\sum_iw_i\sum_{T\ni i}\lambda_T
\le
\sum_iw_iq_i
=1.
\]

\(\square\)

The matching polytope in (10) is compact, so its maximum is attained and is strictly below one. By finite LP duality, the blocker-cover problem

\[
\min\left\{
q\cdot y:
 y_i\ge0,
\quad
\sum_{i\in T}y_i\ge1\ (T\in\mathcal B)
\right\}
\tag{12}
\]

has an optimal value strictly below one. Among the \(q\)-optimal covers, first minimize \(\sum_i y_i\), and then choose an extreme point of this secondary optimal face. The secondary minimum is attained because \(y\ge0\) makes its bounded sublevel sets compact. This selected point is coordinatewise undominated: if another feasible cover \(y'\le y\) differed in some coordinate, nonnegativity of \(q\) and \(q\)-optimality would force \(q\cdot y'=q\cdot y\), while \(\sum_i y'_i<\sum_i y_i\), contradicting the secondary choice. Because the secondary optimal set is a face of the pointed cover polyhedron, its extreme points are extreme covers. Every extreme cover has \(y_i\le1\): if \(y_i>1\), no blocker constraint containing \(i\) is tight, and \(y_i\) can be perturbed in both directions, contradicting extremality.

If the selected cover is integral, let

\[
Y:=\{i:y_i=1\},
\qquad
R:=[4]\setminus Y.
\]

Since \(Y\) meets every minimal blocker, \(R\) contains no minimal blocker and is feasible. On each trunk arc, only the C-routed terminals in \(Y\) can contribute positively, so

\[
\max_a\bigl(y^R(a)-x(a)\bigr)
\le
\max\left\{1,\sum_{i\in Y}h_i\right\}
\le
\max\left\{1,\sum_{i\in Y}q_i\right\}
=1,
\tag{13}
\]

because \(q\cdot y<1\). Thus only nonintegral extreme covers remain.

## 6. Exact four-label cover classification

Let

\[
V:=\{i:w_i\le1\}
\]

be the feasible E-singletons, and let \(G\) be the graph on \(V\) with

\[
ij\in E(G)
\quad\Longleftrightarrow\quad
w_i+w_j\le1.
\tag{14}
\]

After sorting the weights, the neighborhoods are nested. Equivalently, \(G\) is a threshold graph. On at most four vertices, the possible graphs are therefore the familiar finite list obtained by excluding induced \(P_4\), \(C_4\), and \(2K_2\).

Because no E-triple is feasible, the minimal blockers are exactly:

1. blocked singleton vertices \(i\notin V\);
2. missing edges among vertices of \(V\); and
3. three-vertex cliques of \(G\).

Solving the resulting four-variable cover systems gives the following complete list of nonintegral, coordinatewise-undominated extreme covers, up to relabeling. The complete graph \(K_4\) is separated because it is the established all-pairs cell.

| Feasible-singleton graph | Nonintegral extreme cover | Consequence of \(q\cdot y<1\) |
| --- | --- | --- |
| three feasible vertices, no edges; blocked vertex \(u\) | \(y_u=1\), \(y_i=1/2\) for \(i\ne u\) | \(2q_u+\sum_{i\ne u}q_i<2\) |
| four vertices with 0, 1, or 2 edges | \(y_i=1/2\) for all \(i\) | \(\sum_iq_i<2\) |
| feasible star with centre \(u\) and leaf set \(T\) | \(y_i=1/2\) on \(T\), zero at \(u\) | \(q(T)<2\) |
| feasible triangle on \(A=[4]\setminus\{u\}\), isolated \(u\) | \(y_u=2/3\), \(y_i=1/3\) on \(A\) | \(2q_u+q(A)<3\) |
| four-edge threshold graph | \(y_i=1/2\) on a triple \(T\) whose outside vertex is adjacent to all of \(T\) | \(q(T)<2\) |
| five-edge threshold graph | one of two half-covers on a triple \(T\), again with a universal outside vertex | \(q(T)<2\) |

Every other threshold-graph row has only integral undominated extreme covers. A full canonical table, including all 16 singleton/edge signatures and every minimal blocker, is supplied in `FINITE_BLOCKER_COVER_CLASSIFICATION.md`. The companion exact checker independently enumerates all active sets of each cover polyhedron and also cross-checks the classification against all 149 positive four-label threshold downsets.

We now prove the four routing statements corresponding to the four cover inequalities.

## 7. Half-cover on a three-terminal set

### Lemma 2 — three-terminal pair bound

Let \(T\) be a three-terminal set and route the fourth terminal E. Suppose all three exactly-two-C routes on \(T\) are feasible and

\[
q(T)\le2.
\tag{15}
\]

Then one of those three routes has maximum upper deviation at most \(9/8\). If the omitted terminal is terminal 1, the bound improves to one.

**Proof.** Since \(p(T)=3-q(T)\ge1\), replace \(p_i\) on \(T\) by

\[
\widehat p_i:=\frac{p_i}{p(T)}.
\]

The new fractions sum to one and satisfy \(\widehat p_i\le p_i\). For each fixed two-C route, decreasing the selected C fractions increases its positive C contributions, while decreasing the one unselected E fraction makes its negative contribution less negative. Thus every trunk deviation weakly increases. It is enough to prove the bound for \(p(T)=1\). The outside E terminal contributes nonpositively on the trunk and at most one on a private arc.

If the omitted terminal is 2, 3, or 4, the three remaining support columns have chain form. Name them \(A,B,C\), put \(p=p_B\), and let \(V_{AB},V_{AC},V_{BC}\) denote the actual maximum upper deviations of the three corresponding routes. Define the conservative trunk envelopes

\[
\overline M_{AB}:=h_A+h_B,
\qquad
\overline M_{BC}:=h_B+h_C,
\]

\[
\overline M_{AC}:=\max\{h_A,h_C,h_A+h_C-\ell_B\}.
\]

After dropping the outside E terminal's nonpositive trunk contribution and
retaining the private-arc bound one, (4) gives
\[
V_{XY}\le\max\{1,\overline M_{XY}\}
\qquad(XY\in\{AB,AC,BC\}).
\]
It therefore suffices to prove that at least one of the three envelopes is at
most \(9/8\).

Let \(s=h_A+h_C\). Then

\[
\min\{\overline M_{AB},\overline M_{BC}\}
\le h_B+\frac s2.
\]

If \(\overline M_{AC}\le1\), then \(V_{AC}\le1\), and we are done. Otherwise its term above one is \(s-\ell_B\), since \(h_A,h_C\le1\). Because \(p_A+p_B+p_C=1\),

\[
s\le(1-p_A)+(1-p_C)=1+p.
\]

Writing \(d=d_B\), the envelope bounds give

\[
\min\{\overline M_{AB},\overline M_{AC},\overline M_{BC}\}
\le
\min\left\{
\frac{1+p}{2}+d(1-p),
\ 1+p-dp
\right\}.
\]

The first expression increases in \(d\), the second decreases, and their crossing is at \(d=(1+p)/2\). Hence

\[
\min\{\overline M_{AB},\overline M_{AC},\overline M_{BC}\}
\le
1+\frac p2-\frac{p^2}{2}
=
\frac98-\frac12\left(p-\frac12\right)^2
\le\frac98.
\tag{16}
\]

Hence the corresponding actual route has value at most
\(\max\{1,\overline M_{XY}\}\le9/8\).

If terminal 1 is omitted, the remaining supports are nested. For terminals
\(A=2,B=3,C=4\), the actual values of two of the three routes are bounded
respectively by
\(\max\{1,T_2\}\) and \(\max\{1,T_3\}\), where

\[
T_2=h_A+h_C-\ell_B,
\qquad
T_3=h_B+h_C-\ell_A.
\]

Since \(p_A+p_B+p_C=1\),

\[
(1-p_B)T_2+p_BT_3
=d_Ap_C+d_C(1-p_C)
\le1.
\tag{17}
\]

Thus at least one of those two routes is at most one. \(\square\)

In the star, four-edge, and five-edge rows of Section 6, the vertex outside the half-covered triple is adjacent to all three vertices of the triple. Its three feasible incident E-edges are precisely the complements of the three required two-C routes, so Lemma 2 applies.

## 8. Four feasible E-singletons with total E mass at most two

### Lemma 3

If all four E-singletons are feasible and

\[
Q:=\sum_iq_i\le2,
\tag{18}
\]

then one singleton-E route has value at most \(9/8\).

**Proof.** Private deviations are at most one. Suppose the minimum of the four trunk maxima in (3) is \(t>1\), and set

\[
\Delta:=H-t.
\]

Every singleton trunk maximum is at most \(H\), so \(\Delta\ge0\). Since \(H\le Q\le2\) and \(t>1\), we have \(\Delta<1\). Routes 1, 2, and 4 give

\[
h_1\le\Delta,
\qquad
d_2\le\Delta,
\qquad h_4\le\Delta.
\tag{19}
\]

For route 3, either

\[
H-d_3\ge t
\quad\Longrightarrow\quad
d_3\le\Delta,
\tag{20}
\]

or

\[
s:=h_1+h_2\ge t.
\tag{21}
\]

In branch (20),

\[
h_1\le\min\{q_1,\Delta\},
\quad
h_4\le\min\{q_4,\Delta\},
\quad
h_2+h_3\le\Delta(q_2+q_3).
\]

For \(r=q_1+q_4\),

\[
H
\le
\min\{r,2\Delta\}+\Delta(2-r)
\le
4\Delta-2\Delta^2.
\]

Therefore

\[
t=H-\Delta
\le3\Delta-2\Delta^2
=
\frac98-2\left(\Delta-\frac34\right)^2
\le\frac98.
\tag{22}
\]

In branch (21), \(\Delta>0\). Since \(h_1\le\min\{q_1,\Delta\}\) and \(h_2\le\Delta q_2\), supporting \(s>\Delta\) requires

\[
q_1+q_2
\ge
\Delta+\frac{s-\Delta}{\Delta}.
\tag{23}
\]

Also

\[
q_3+q_4\ge h_3+h_4=H-s=t+\Delta-s.
\]

Because \(s\ge t\) and \(0<\Delta<1\),

\[
2\ge Q
\ge
2\Delta-1+\frac t\Delta,
\]

so

\[
t\le\Delta(3-2\Delta)
=
\frac98-2\left(\Delta-\frac34\right)^2
\le\frac98.
\]

\(\square\)

Lemma 3 resolves the all-half cover for every four-vertex graph with zero, one, or two feasible E-edges.

## 9. Exactly three feasible E-singletons and no feasible E-edge

Let \(u\) be the blocked singleton. The fractional cover from Section 6 gives

\[
2q_u+\sum_{i\ne u}q_i\le2.
\tag{24}
\]

### Lemma 4

Under (24), one of the three feasible singleton-E routes has value at most \(9/8\).

**Proof.** Let \(t>1\) be the minimum of the three available singleton trunk maxima, and put \(\Delta=H-t\). Since (24) implies \(\sum_iq_i\le2\), we again have \(0\le\Delta<1\). We use (3) and retain the weighted resource in (24).

### Case 1: \(u=2\)

Routes 1 and 4 give \(h_1,h_4\le\Delta\).

If route 3 is large through \(H-d_3\), then \(d_3\le\Delta\). The contribution efficiencies per unit of the weighted resource \(q_1+q_3+q_4+2q_2\) are: one on terminals 1 and 4 until their caps \(\Delta\), \(\Delta\) on terminal 3, and \(1/2\) on terminal 2. Hence

\[
H\le
\begin{cases}
1+\Delta,&0\le\Delta\le1/2,\\[1mm]
4\Delta-2\Delta^2,&1/2\le\Delta<1.
\end{cases}
\]

Thus \(t=H-\Delta\le9/8\).

If route 3 is large through \(s=h_1+h_2\ge t\), supporting \(s\) requires

\[
q_1+2q_2\ge\Delta+2(s-\Delta)=2s-\Delta.
\]

The remaining coordinates satisfy \(q_3+q_4\ge H-s\). Therefore the weighted resource is at least

\[
2s-\Delta+H-s=s+t\ge2t>2,
\]

contradicting (24).

### Case 2: \(u=3\)

Routes 1, 2, and 4 give

\[
h_1,h_4,d_2\le\Delta.
\]

The resource is \(q_1+q_2+q_4+2q_3\le2\). The same efficiency calculation as in Case 1 yields

\[
H\le
\begin{cases}
1+\Delta,&0\le\Delta\le1/2,\\[1mm]
4\Delta-2\Delta^2,&1/2\le\Delta<1,
\end{cases}
\]

and hence \(t\le9/8\).

### Case 3: \(u=4\)

Routes 1 and 2 give \(h_1\le\Delta\) and \(d_2\le\Delta\).

If route 3 is large through \(H-d_3\), then \(d_3\le\Delta\). Under \(q_1+q_2+q_3+2q_4\le2\), terminal 1 has unit efficiency until cap \(\Delta\), terminals 2 and 3 have efficiency \(\Delta\), and terminal 4 has efficiency \(1/2\). Thus

\[
H\le
\begin{cases}
\displaystyle \Delta+\frac{2-\Delta}{2},&0\le\Delta\le1/2,\\[3mm]
\Delta+\Delta(2-\Delta),&1/2\le\Delta<1.
\end{cases}
\]

Both branches give \(t\le1\).

Otherwise put \(s=h_1+h_2\ge t\). As in (23),

\[
q_1+q_2
\ge
\Delta+\frac{s-\Delta}{\Delta}.
\]

Also \(q_3+2q_4\ge h_3+h_4=H-s\). Hence

\[
2\ge2\Delta-1+\frac t\Delta,
\]

which gives \(t\le\Delta(3-2\Delta)\le9/8\).

### Case 4: \(u=1\)

Routes 2 and 4 give \(d_2\le\Delta\) and \(h_4\le\Delta\).

If route 3 is large through \(H-d_3\), the same efficiency calculation as the first branch of Case 3 gives \(t\le1\).

Finally suppose \(s=h_1+h_2\ge t\). If \(\Delta\le1/2\), terminals 1 and 2 each produce at most one half-unit of \(s\) per unit of weighted resource, so

\[
2q_1+q_2\ge2s>2,
\]

impossible. If \(\Delta\ge1/2\), terminal 2 is the more efficient coordinate and is filled first. Since \(q_2\le1\),

\[
2q_1+q_2\ge1+2(s-\Delta).
\]

The remaining coordinates require \(q_3+q_4\ge H-s\), so the total resource is at least

\[
1+2(s-\Delta)+H-s
=1+s+t-\Delta
\ge1+2t-\Delta
>2,
\]

again impossible.

This completes all four labeled placements. \(\square\)

All other graphs on three feasible singleton vertices have only integral cover branches and were already resolved by (13).

## 10. Feasible E-triangle and isolated singleton

Let \(A=[4]\setminus\{u\}\). Assume all four E-singletons are feasible, the three E-edges inside \(A\) are feasible, and all three E-edges incident with \(u\) are blocked. The fractional cover gives

\[
2q_u+q(A)\le3.
\tag{25}
\]

The available complementary C-routes include the three pairs \(\{u,i\}\), \(i\in A\), and the triple \(A\).

### Lemma 5

Under (25), one of those four routes has value at most \(9/8\).

**Proof.** Suppose the contrary. Private deviations are at most one, so all four displayed trunk maxima exceed \(9/8\). Let \(t>9/8\) be their minimum and put

\[
a:=t-h_u.
\]

Since \(h_u\le1\), \(a>1/8\). Each displayed pair route chooses C only for \(u\) and one other terminal, so its trunk maximum is at most \(h_u+1\); hence \(t\le h_u+1\) and

\[
\frac18<a\le1.
\tag{26}
\]

We treat the four labeled placements directly.

### Case 1: \(u=1\)

From the C12, C13, and C14 formulas in (4),

\[
h_2\ge a,
\qquad
h_3\ge a+\ell_2,
\qquad
h_4\ge a+\ell_2+\ell_3.
\]

Put

\[
A_0:=a+\ell_2,
\qquad
D_0:=A_0+\ell_3.
\]

Then

\[
q_1\ge t-a,
\qquad
q_2\ge\frac a{A_0},
\qquad
q_3\ge\frac{A_0}{D_0},
\qquad
q_4\ge D_0.
\]

AM-GM gives

\[
2q_1+q_2+q_3+q_4
\ge
2(t-a)+3a^{1/3}.
\]

At \(t=9/8\), the right side is

\[
\frac94-2a+3a^{1/3}>3
\qquad(1/8\le a\le1).
\]

Indeed, with \(r=a^{1/3}\in[1/2,1]\), the difference from three is \(3r-2r^3-3/4\), a concave function whose endpoint values are \(1/2\) and \(1/4\). This contradicts (25).

### Case 2: \(u=3\)

The C13, C23, and C34 routes give

\[
h_2\ge a,
\qquad
h_1,h_4\ge a+\ell_2.
\]

With \(D_0=a+\ell_2\),

\[
2q_3+q_1+q_2+q_4
\ge
2(t-a)+2D_0+\frac a{D_0}
\ge
2(t-a)+2\sqrt{2a}.
\]

At \(t=9/8\), this is at least three on \([1/8,1]\), because with \(r=\sqrt{2a}\),

\[
\frac94-2a+2\sqrt{2a}-3
=
\frac14-(r-1)^2
\ge0.
\]

Equality at the displayed \(t=9/8\) bound can occur only at \(a=1/8\). Because the actual \(t\) is strictly larger than \(9/8\), the preceding lower bound is then strictly larger than three. Again (25) is contradicted.

### Case 3: \(u=4\)

The C14, C24, and C34 routes force

\[
h_1\ge a+\ell_2+\ell_3,
\qquad
h_2\ge a+\ell_3,
\qquad
h_3\ge a+\ell_2.
\]

Let \(D_0=a+\ell_2+\ell_3\). Then

\[
q_1+q_2+q_3
\ge
1+D_0+\frac a{D_0}.
\]

Consequently

\[
2q_4+q_1+q_2+q_3
\ge
2(t-a)+1+2\sqrt a.
\]

At \(t=9/8\), the difference from three is

\[
\frac14-2a+2\sqrt a
=
\frac34-2\left(\sqrt a-\frac12\right)^2
>0
\]

after using \(1/8\le a\le1\). This contradicts (25).

### Case 4: \(u=2\)

The C12, C23, and C24 routes give

\[
h_1\ge a,
\qquad
h_3\ge a,
\qquad
h_4\ge a+\ell_3.
\]

The C134 route gives

\[
h_1+h_3+h_4\ge a+d_2.
\]

Put \(D=d_2\). Since \(h_2=t-a\),

\[
q_2=\frac{t-a}{D},
\qquad
t-a\le D\le1.
\]

The other three coordinates satisfy both

\[
q_1+q_3+q_4\ge a+2\sqrt a
\]

and

\[
q_1+q_3+q_4\ge a+D.
\]

Therefore

\[
2q_2+q_1+q_3+q_4
\ge
\frac{2(t-a)}D+a+\max\{2\sqrt a,D\}.
\tag{27}
\]

It remains to show that the right side of (27) is at least three at \(t=9/8\).

- If \(D\ge2\sqrt a\), then \(a\le1/4\). The function
  \[
  \frac{2(9/8-a)}D+D
  \]
  decreases on \(D\le1\), so (27) is at least
  \[
  2(9/8-a)+a+1=\frac{13}{4}-a\ge3.
  \]
- If \(D\le2\sqrt a\) and \(a\le1/4\), write \(r=\sqrt a\le1/2\). Taking the largest allowed \(D\) gives the lower bound
  \[
  \frac{9}{8r}+r+r^2.
  \]
  Its difference from three, multiplied by \(8r>0\), factors as
  \[
  (2r-1)(4r^2+6r-9)\ge0
  \qquad\left(\frac1{2\sqrt2}\le r\le\frac12\right).
  \]
- If \(D\le2\sqrt a\) and \(a\ge1/4\), use \(D\le1\) to obtain
  \[
  \frac94-a+2\sqrt a.
  \]
  With \(r=\sqrt a\in[1/2,1]\), its difference from three is
  \[
  \frac14-(r-1)^2\ge0.
  \]

Because \(D>0\) and the actual \(t\) is strictly greater than \(9/8\), the
right-hand side of (27) is strictly larger than its \(t=9/8\) value and hence
strictly larger than three. Therefore
\(2q_2+q_1+q_3+q_4>3\), contradicting (25).

All four placements are impossible, proving the lemma. \(\square\)

The F064 family belongs to the isolated-terminal-2 placement. Its exact lower sequence approaching \(5/2-\sqrt2\) remains valid, but a matching cell-specific upper bound is not needed here and is not claimed.

## 11. Completion of the positive lane

Take any strictly positive one-scenario instance.

1. If an E-triple is feasible, a complementary C-singleton route has value at most one.
2. If no E-triple is feasible and every E-pair is feasible, the established all-C-pairs/no-C-singleton theorem gives value at most \(L\).
3. Otherwise apply Lemma 1 and choose the coordinatewise-undominated optimal blocker cover selected by the two-stage tie-break in Section 5.
   - An integral cover gives value at most one by (13).
   - The three-feasible-singleton no-edge cover is handled by Lemma 4.
   - The all-half cover is handled by Lemma 3.
   - A half-cover on a triple is handled by Lemma 2.
   - The triangle-isolated cover is handled by Lemma 5.

The classification in Section 6 is exhaustive. Hence every strictly positive cell other than the all-pairs cell has value at most \(9/8\).

## 12. Global conclusion

The imported signed/zero results give

\[
\Phi\le\frac98
\]

for every nonzero cost-difference vector that is not strictly positive, and \(\Phi=4/5\) when the difference vector is zero. The positive lane is at most \(L\), and the released equal-full-cost all-pairs sequence approaches \(L\) through rational instances. Therefore

\[
\boxed{
\sup\Phi
=
\frac{299-41\sqrt{41}}{32}.
}
\]

This resolves the former UC-020 conjecture and rules out UC-021 on the fixed four-terminal gadget.

## 13. Scope and evidence posture

The theorem is about one scenario on this fixed graph and these designated path pairs. It does not determine the unrestricted planar SSUF constant.

The human proof above is authoritative. The companion computations serve only to:

- reproduce the finite blocker-cover classification exactly;
- independently regenerate the 149 positive threshold families as a cross-check;
- reconstruct all graph-native route formulas;
- check the univariate algebra used in Lemmas 2–5;
- verify the F064 strict lower sequence; and
- run targeted numerical attempts to find a counterexample.

No numerical optimization is used as an upper-bound premise.
