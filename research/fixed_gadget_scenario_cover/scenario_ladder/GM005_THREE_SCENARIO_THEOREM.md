# GM-005 — Three Positive Scenarios on the Fixed Four-Terminal Gadget

**Version:** R2-v2 proof repair, 2026-08-01  
**Status:** proof repaired; frozen fresh R2 v2 `ACCEPT_AS_STATED`  
**Scope:** exactly three strictly positive E-minus-C scenario vectors, weak
scenario-wise cost nonincrease, positive demands, and the fixed graph in
`MODEL_SPEC_GM005.md`.

## Theorem GM-005

Let \(\beta_G^{(3,+)}\) denote the normalized additive upper arc-deviation
supremum on the fixed gadget with exactly three positive scenarios. Then

\[
\boxed{\beta_G^{(3,+)}=3}.
\]

Every finite legal instance has value strictly below three. Hence the
supremum is not attained. The same supremum is approached by rational data.

## 1. A singleton-assignment lemma

Normalize \(d_{\max}=1\), and put

\[
h_i=d_iq_i,\qquad H=\sum_i h_i.
\]

The all-C routing is always feasible and has exact value \(H\).

### Lemma 1

If every singleton E-set is blocked by at least one of the three scenarios,
then

\[
H<3.
\]

### Proof

First split off \(q=(0,0,0,0)\). Then the fractional flow is already the
all-C unsplittable routing and has value zero.

Assume now that \(q\ne0\). Since every coordinate of every scenario vector is
positive,

\[
B_j:=k^{(j)}\cdot q>0
\qquad(j=1,2,3).
\]

Normalize

\[
w^{(j)}:=\frac{k^{(j)}}{B_j},
\qquad
w^{(j)}\cdot q=1.
\]

Assign each singleton \(\{i\}\) to one scenario that blocks it, and let
\(G_j\) be the indices assigned to scenario \(j\). Blocking is strict, so

\[
w_i^{(j)}>1\qquad(i\in G_j).
\]

If the assigned group has positive \(h\)-mass, then

\[
\sum_{i\in G_j}h_i
<
\sum_{i\in G_j}h_iw_i^{(j)}
\le
\sum_iq_iw_i^{(j)}
=1,
\tag{1}
\]

where \(h_i=d_iq_i\le q_i\). If the group is empty or has zero
\(h\)-mass, its contribution is simply \(0<1\). Summing the three strict
group bounds gives \(H<3\). \(\square\)

## 2. Equality collapse for a feasible singleton

### Lemma 2

If a singleton E-set \(\{r\}\) is feasible, then the instance has a feasible
routing of value strictly below three.

### Proof

Route terminal \(r\) on E and the other three terminals on C. On a trunk arc,
positive deviation can come from at most those three C-routed terminals, each
by at most one. The E-routed terminal contributes nonpositively on its
difference support. Every positive private-arc deviation is at most one.
Thus this singleton route has value at most three.

If its value is below three, the conclusion is immediate. Suppose instead
that its value equals three. A private arc cannot witness equality. On a trunk
arc there are at most three positive summands, each at most one, together with
at most one nonpositive summand. Equality therefore forces

\[
h_i=d_iq_i=1
\qquad(i\ne r).
\tag{2}
\]

Because \(d_i\le1\) and \(q_i\le1\), equation (2) gives

\[
d_i=q_i=1
\qquad(i\ne r).
\tag{3}
\]

Now take the complementary triple E-set

\[
T=[4]\setminus\{r\}.
\]

For every scenario \(j\), weak feasibility and (3) give

\[
\begin{aligned}
k^{(j)}(T)
&=\sum_{i\ne r}k_i^{(j)}\\
&=\sum_{i\ne r}q_i k_i^{(j)}\\
&\le \sum_iq_i k_i^{(j)}
=k^{(j)}\cdot q.
\end{aligned}
\tag{4}
\]

Hence \(T\) is feasible in all three scenarios. In this routing the three
E-routed terminals have

\[
\ell_i=d_i(1-q_i)=0
\qquad(i\ne r).
\]

Only the single C-routed terminal \(r\) can contribute positively on a trunk,
and that contribution is at most \(h_r\le1\). Positive private deviations are
also at most one. Thus \(T\) has route value at most one, and in particular
strictly below three. \(\square\)

## 3. Strict finite upper bound

For any finite instance, either every singleton is blocked or some singleton
is feasible.

- In the first case, Lemma 1 gives a feasible all-C route of value \(H<3\).
- In the second case, Lemma 2 gives a feasible route of value below three.

Therefore every finite legal three-scenario instance satisfies

\[
\boxed{t<3}.
\tag{5}
\]

This proves both the universal upper bound and nonattainment.

## 4. Exact rational lower sequence

For an integer \(n\ge2\), take unit demands and

\[
q_i=1-\frac1n
\qquad(i=1,2,3,4).
\]

Use three positive scenario vectors, heavy respectively on terminals 1, 2,
and 3:

\[
(3n,1,1,1),\qquad
(1,3n,1,1),\qquad
(1,1,3n,1).
\tag{6}
\]

Every scenario budget equals

\[
(3n+3)\left(1-\frac1n\right)
=3n-\frac3n
<3n.
\tag{7}
\]

Thus an E-set containing terminal 1, 2, or 3 is blocked by the corresponding
heavy scenario. Conversely, the empty set is trivially feasible, and
\(\{4\}\) has scenario weight one while
\(3n-3/n>1\) for \(n\ge2\). Hence the common feasible E-sets are exactly

\[
\varnothing
\quad\text{and}\quad
\{4\}.
\tag{8}
\]

The route \(\{4\}\) has exact value

\[
3\left(1-\frac1n\right),
\tag{9}
\]

witnessed on trunk arc \(a_2\), where terminals 1, 2, and 3 contribute and
terminal 4 has no C-minus-E support. No trunk can exceed the sum of those
three positive C contributions, and every positive private deviation is at
most one, which is strictly smaller than (9). The all-C route has the larger
value \(4(1-1/n)\). Therefore the finite instance value is exactly (9), and

\[
3\left(1-\frac1n\right)\longrightarrow3.
\tag{10}
\]

Combining (5) and (10) proves the theorem.

At \(n=4\), the exact finite value is

\[
\frac94>\frac{17}{8},
\]

but this comparison is optional and is not used in the proof of GM-005.

## 5. Evidence and nonclaim boundary

- The proof uses only the fixed support identities, positivity, and weak
  scenario feasibility.
- The all-thirteen-arc bound used above is proved explicitly in
  `TRUNK_PRIVATE_ARC_ENVELOPE.md` and reconstructed by
  `reproduction/verify_arc_envelope.py`.
- It does not use the scenario-cover atlas, SC-006, the bounded-heterogeneity
  curve, GM-006, GM-008, or GM-009.
- It proves a fixed-gadget positive-scenario theorem, not an unrestricted
  planar SSUF result.
- The frozen fresh R2-v2 review accepted this repaired theorem as stated. That
  internal AI-assisted disposition is not external human review, journal peer
  review, or publication clearance.
