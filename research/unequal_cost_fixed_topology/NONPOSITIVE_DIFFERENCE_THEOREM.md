# Every Non-All-Positive Cost-Difference Stratum Is Bounded by \(9/8\)

Let

\[
k_i=e_i^{\mathrm{cost}}-b_i
\]

be the full-demand E-minus-C route-cost difference for terminal `i`.  This file
treats every fixed sign/zero stratum for which the vector `k` is not strictly
positive in all four coordinates and is not identically zero.

The result uses the fixed path-difference supports in
`FIXED_TOPOLOGY_APPENDIX.md` and the upper-deviation convention of the research
package.

## Theorem UC-018

Fix a nonzero cost-difference vector with at least one coordinate `k_i<=0`.
Then the supremum, over the corresponding sign/zero stratum on the fixed
four-terminal topology, of the minimum cost-feasible maximum upper deviation is

\[
\begin{cases}
\dfrac98,
&\text{if exactly three coordinates are positive and the nonpositive coordinate
is terminal }2,3,\text{ or }4,\\[2mm]
1,&\text{otherwise.}
\end{cases}
\]

The same values hold after restricting the data to rationals as suprema.
Consequently every non-all-positive stratum is bounded by

\[
\frac98
<\frac{299-41\sqrt{41}}{32}=L.
\]

Thus an improvement over the released fixed-topology value `L` can occur only
in the strictly all-positive cost-difference lane.

The identically zero vector is excluded from the exact-value statement because
it is one degenerate cost-free stratum rather than a sign-oriented threshold
cell.  The standard cost-free upper bound still applies, but no separate exact
fixed-topology value is asserted here.

## 1. Remove nonpositive coordinates from the upper-bound search

Let

\[
P:=\{i:k_i>0\},\qquad N:=\{i:k_i<0\},\qquad Z:=\{i:k_i=0\}.
\]

Start from any cost-feasible routing.  Switch every terminal in `N union Z` to
its historical E route.

- If `k_i<0`, changing C to E increases the cost-feasibility left-hand side
  `sum k_i(z_i-p_i)` and therefore preserves feasibility.
- If `k_i=0`, the switch does not affect cost feasibility.
- On every trunk arc, an E-routed terminal contributes `-d_i p_i<=0`.

Hence some optimal-or-better candidate may be sought with all nonpositive
coordinates routed E.  They can be ignored when proving an upper bound on trunk
deviation; their private positive deviations are at most one.

The remaining positive coordinates must choose a subset `S subseteq P`
satisfying a positive threshold inequality

\[
k(S)\ge\theta,
\qquad
\theta:=\sum_{i\in P}k_ip_i-
       \sum_{i\in N}|k_i|p_i.
\tag{1}
\]

If `theta<=0`, choose no positive C routes and the bound is immediate.  If
`theta>0`, put

\[
\lambda:=\frac{\theta}{\sum_{i\in P}k_ip_i}\in(0,1]
\]

and replace `p_i` on `P` by `hat p_i=lambda p_i`.  This preserves the residual
threshold family because `sum k_i hat p_i=theta`.  It can only increase every
fixed route's trunk deviation: selected C contributions grow and unselected E
contributions become less negative.  It is therefore enough to analyze the
boundary relation

\[
\theta=\sum_{i\in P}k_ip_i.
\tag{2}
\]

Since at least one coordinate is nonpositive, `|P|<=3`.

## 2. Residual positive-threshold families on at most three labels

If `|P|<=2`, every nonempty upward threshold family has one of the following:

- the empty set feasible;
- a feasible singleton; or
- one unique generator of size two.

The first case uses the all-E route, the second uses the feasible-singleton
lemma, and the third uses the single-generator theorem.  Each has value at most
one.

Now let `|P|=3`.  With no feasible singleton, the minimal feasible sets can only
be:

1. one pair;
2. the full triple only;
3. exactly two of the three pairs; or
4. all three pairs.

The first two are single-generator cells and have value one.

### Two-pair lemma

Suppose the feasible pairs are `AB` and `AC`, while `BC` and all singletons are
infeasible.  Under (2), if both

\[
p_A+p_B<1,
\qquad
p_A+p_C<1,
\]

then `q_B>p_A` and `q_C>p_A`.  Infeasibility of `BC` gives

\[
k_Ap_A>k_Bq_B+k_Cq_C>p_A(k_B+k_C),
\]

so `k_A>k_B+k_C`.  Infeasibility of singleton `A` gives

\[
k_Aq_A<k_Bp_B+k_Cp_C<q_A(k_B+k_C),
\]

so `k_A<k_B+k_C`, a contradiction.  Therefore one feasible pair has

\[
q_A+q_B\le1
\quad\text{or}\quad
q_A+q_C\le1.
\]

Routing that pair C and every other terminal E gives total positive trunk
contribution at most one.  Private deviations are also at most one.

It remains only to analyze the all-three-pairs family.

## 3. Boundary reduction for the all-pairs family

All singletons infeasible and all pairs feasible imply

\[
1<\sum_{i\in P}p_i\le2.
\]

Decrease the three fractions coordinatewise to numbers with sum exactly one.
Every pair remains available in the original cost cell, while the decrease can
only increase the deviations of all three pair routings.  It suffices to prove
the upper bound on

\[
p_A+p_B+p_C=1.
\tag{3}
\]

Write

\[
e_i=d_i(1-p_i),\qquad \ell_i=d_ip_i.
\]

Positive private deviations are at most one, so only pair trunk maxima above
one matter.

## 4. Chain type: exact value \(9/8\)

When the nonpositive terminal is `2`, `3`, or `4`, the three remaining support
columns have the same chain form after naming them `A,B,C`:

\[
M_{AB}=e_A+e_B,
\qquad
M_{BC}=e_B+e_C,
\]

and

\[
M_{AC}=\max\{e_A,e_C,e_A+e_C-\ell_B\}.
\]

The concrete labelings are:

| Nonpositive terminal | `A` | `B` | `C` |
| --- | ---: | ---: | ---: |
| 2 | 1 | 3 | 4 |
| 3 | 1 | 2 | 4 |
| 4 | 1 | 2 | 3 |

Put `s=e_A+e_C`.  The smaller of the first two maxima is at most

\[
e_B+\frac{s}{2}.
\]

If `M_AC<=1`, there is nothing to prove.  Otherwise its term above one must be
`s-ell_B`, since `e_A,e_C<=1`.  Using (3),

\[
s\le(1-p_A)+(1-p_C)=1+p_B.
\]

Let `p=p_B` and `d=d_B`.  The desired minimum is therefore at most

\[
\min\left\{
\frac{1+p}{2}+d(1-p),
1+p-dp
\right\}.
\tag{4}
\]

The first expression increases in `d`; the second decreases.  Their crossing is
at

\[
d=\frac{1+p}{2},
\]

where the common value is

\[
1+\frac p2-\frac{p^2}{2}
=\frac98-\frac12\left(p-\frac12\right)^2
\le\frac98.
\]

This proves the upper bound.

For the matching lower family, choose rational `epsilon in (0,1)`, take equal
positive differences on `A,B,C`, and set

\[
p_A=p_C=\frac{1+\epsilon}{4},
\qquad
p_B=\frac{1+\epsilon}{2},
\]

\[
d_A=d_C=1,
\qquad
d_B=\frac{3-\epsilon}{4}.
\]

Give a negative omitted terminal sufficiently large magnitude and set its C
fraction to zero, so it is forced E; for a zero omitted terminal give it demand
tending to zero.  Exactly the three positive pairs and the triple are feasible.
All three pair maxima equal

\[
\frac{(3-\epsilon)^2}{8},
\]

which tends to `9/8`.  Rational data therefore attain the same supremum.

## 5. Nested type: exact value one

When terminal `1` is nonpositive, the positive terminals are `2,3,4`.  Name them
`A=2`, `B=3`, `C=4`.  Their pair maxima above one reduce to

\[
T_1=e_A+e_B,
\]

\[
T_2=e_A+e_C-\ell_B,
\qquad
T_3=e_B+e_C-\ell_A.
\]

(The full route maxima also contain `e_A`, `e_B`, or `e_C`, each at most one.)
Using (3), take the convex combination

\[
(1-p_B)T_2+p_BT_3.
\]

The coefficient of `d_A` is

\[
(1-p_B)(1-p_A)-p_Bp_A=p_C,
\]

the coefficient of `d_B` is zero, and the coefficient of `d_C` is
`1-p_C`.  Hence

\[
(1-p_B)T_2+p_BT_3=d_Ap_C+d_C(1-p_C)\le1.
\]

At least one of the two feasible special pairs has maximum deviation at most
one.  The matching lower bound follows from a signed single-generator family,
so the exact supremum is one.

## 6. Consequences

For every nonzero sign/zero stratum outside the strictly all-positive lane:

- if exactly three coordinates are positive and terminal `2`, `3`, or `4` is
  nonpositive, the exact supremum is `9/8`;
- every other such stratum has exact supremum one.

For the matching lower bound in the value-one strata, choose any nonzero
coordinate `j`. If it is the only nonzero coordinate, choose its fraction so
that cost feasibility forces its oriented value to one: `p_j=epsilon` for a
positive difference and `p_j=1-epsilon` for a negative difference. The forced
physical route has private deviation `1-epsilon`. If at least two coordinates
are nonzero, apply UC-017 with the unique oriented generator equal to the set of
all nonzero coordinates; zero coordinates lie outside the generator. Thus every
value-one stratum has rational instances approaching one.

Because

\[
263^2>41^3,
\]

we have

\[
\frac98<L.
\]

Negative and zero cost differences therefore cannot improve the fixed-topology
lower bound.  The global fixed-topology search may now be confined to the
strictly all-positive lane and its 83 unresolved labeled cells.

## Exact executable corroboration

```bash
python nonpositive_difference_check.py
```

The script checks the chain square identity, the nested convex-combination
identity, 1,022 exact rational instances of the two-pair implication, exact
negative-terminal lower families, representative zero-terminal limiting
families, all trunk/private deviations, and the strict inequality `9/8<L`.
The human inequalities above are the proof.

## Nonclaims

This theorem does not solve any of the 83 remaining strictly all-positive cells,
prove global four-terminal optimality, determine the unrestricted planar
constant, or give the exact value of the identically zero cost vector.
