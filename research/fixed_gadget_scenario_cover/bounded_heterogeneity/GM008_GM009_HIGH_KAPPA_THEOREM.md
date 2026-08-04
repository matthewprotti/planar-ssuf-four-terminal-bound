# Bounded-Heterogeneity Two-Scenario Draft — Scope-Repaired Revision

**Status:** private proof draft, repaired after a second proof-only review. The
prior constructive revision stated equation (10) without its necessary
\(t>2\) hypothesis; an exact legal counterexample shows that unconditional
statement is false. The proof now separates the already-settled \(t\le2\)
case before deriving (10). A fresh dependency-complete R2 v3 review accepted
GM-008, GM-009, and the packet `ACCEPT_AS_STATED`. That internal AI-assisted
disposition is not external human review or authority for public release.

For \(\kappa\ge1\), impose in each positive scenario

\[
\frac{\max_i k_i^{(j)}}{\min_i k_i^{(j)}}\le\kappa.
\]

Let \(\beta_G^{(2\mathrm{sc})}(\kappa)\) be the resulting fixed-gadget
supremum.

## Candidate branch and threshold

For \(\kappa>2\), define

\[
Q_\kappa=\frac{\kappa(\kappa-2)}{\kappa^2-1},
\qquad
S_\kappa=\frac{\kappa(2\kappa-1)}{\kappa^2-1},
\]

and

\[
F(\kappa)
=Q_\kappa+\frac{(1+S_\kappa)^2}{8}
=\frac{17\kappa^4-22\kappa^3-13\kappa^2+18\kappa+1}
       {8(\kappa-1)^2(\kappa+1)^2}.
\]

Let \(\kappa_0\) be the unique real root above \(2\) of

\[
P(\kappa)=\kappa^4-22\kappa^3+19\kappa^2+18\kappa-15.
\]

Equivalently, it is the largest real root. Numerically,

\[
\kappa_0=21.058780922898283\ldots,
\qquad F(\kappa_0)=2.
\]

The identity

\[
F(\kappa)-2
=\frac{P(\kappa)}{8(\kappa-1)^2(\kappa+1)^2}
\tag{1}
\]

shows that \(F(\kappa)\ge2\) exactly for
\(\kappa\ge\kappa_0\) in the range \(\kappa>2\).

## Sharpened draft theorem and open-region sandwich

The draft tail theorem is

\[
\boxed{
\beta_G^{(2\mathrm{sc})}(\kappa)=F(\kappa)
\quad\text{for }\kappa\ge\kappa_0.
}
\tag{2}
\]

The same argument gives additional information below the tail:

\[
\boxed{
\beta_G^{(2\mathrm{sc})}(\kappa)\le2
\quad\text{for }1\le\kappa\le\kappa_0.
}
\tag{3}
\]

The released equal-weight one-scenario construction may be duplicated as the
two scenarios, so

\[
\beta_G^{(2\mathrm{sc})}(\kappa)\ge L
:=\frac{299-41\sqrt{41}}{32}
\qquad(\kappa\ge1).
\tag{4}
\]

The star-triangle sequence below also gives
\(\beta_G^{(2\mathrm{sc})}(\kappa)\ge F(\kappa)\) for every
\(\kappa>2\). For \(1\le\kappa\le2\), (3)-(4) give the simpler bracket
\(L\le\beta_G^{(2\mathrm{sc})}(\kappa)\le2\). For the unresolved middle
interval, the sharper sandwich is

\[
\boxed{
\max\{L,F(\kappa)\}
\le\beta_G^{(2\mathrm{sc})}(\kappa)
\le2
\qquad(2<\kappa<\kappa_0).
}
\tag{5}
\]

The function \(F\) is strictly increasing for \(\kappa\ge2\), because

\[
F'(\kappa)
=\frac{11\kappa^4-21\kappa^3+6\kappa^2+11\kappa-9}
       {4(\kappa-1)^3(\kappa+1)^3}>0.
\tag{6}
\]

Indeed, for \(\kappa\ge2\), the numerator is
\(\kappa^3(11\kappa-21)+6\kappa^2+11\kappa-9>0\). Also

\[
\lim_{\kappa\to\infty}F(\kappa)=\frac{17}{8}.
\]

## Dependency on the released RB-003 reduction

Normalize \(d_{\max}=1\). The released RB-003 proof shows that every branch
other than the **central star-triangle branch** has value at most \(2\). Thus
only that branch needs a bounded-heterogeneity refinement when studying a
value above two. The exact imported model definitions, singleton-route
formulas, and branch statement used here are reproduced in
`MODEL_AND_RB003_DEPENDENCY_SPEC.md`; no stronger RB-003 conclusion is used.

Let \(u\in\{2,3\}\) be the unique non-omittable central terminal, let
\(A=[4]\setminus\{u\}\), and put

\[
q=q_u,
\qquad
S=\sum_{i\in A}q_i,
\qquad
\Delta=H-t.
\]

The set \(A\) consists of two outer terminals and one remaining central
terminal.

## Refined star and triangle constraints

### Star constraint

The star scenario blocks singleton \(\{u\}\). If \(m\) is its minimum
weight, then \(k_u\le\kappa m\), every A-weight is at least \(m\), and

\[
k_u(1-q)>
\sum_{i\in A}k_iq_i
\ge mS
\ge\frac{k_u}{\kappa}S.
\]

Therefore

\[
S<\kappa(1-q). \tag{7}
\]

### Triangle constraint

In the triangle scenario, order the three A-weights as
\(a_1\le a_2\le a_3\), and let the outside weight be \(b\). Since every
A-pair is blocked, its budget \(B\) satisfies

\[
B<a_1+a_2.
\]

If \(S\le1\), then \(S\le 2-q/\kappa\); equality could occur only at
\(\kappa=q=S=1\), which is incompatible with the strict star bound (7). Thus
the combined constraints already give the desired strict inequality. If
\(S>1\), fractional-knapsack minimization fills the cheapest coordinate first
and then allocates all further mass at marginal cost at least \(a_2\). (When
\(S>2\), any mass forced onto the third coordinate only strengthens the same
lower bound.) Consequently,

\[
\sum_{i\in A}a_iq_i\ge a_1+a_2(S-1).
\]

Using \(B=bq+\sum_{i\in A}a_iq_i<a_1+a_2\), we obtain

\[
bq+a_2(S-1)<a_2,
\qquad
S<2-\frac{b}{a_2}q.
\]

The heterogeneity bound gives \(a_2\le\kappa b\), hence

\[
S<2-\frac q\kappa. \tag{8}
\]

Combining (7)-(8),

\[
S<B_\kappa(q)
:=\min\left\{\kappa(1-q),\,2-\frac q\kappa\right\}.
\tag{9}
\]

## Exact allocation envelope

Let \(x,y\) be the two outer A-coordinates and \(z\) the remaining central
A-coordinate, so \(x+y+z=S\).

If \(t\le2\), the target bound \(t\le\max\{2,F(\kappa)\}\) is immediate, so
assume for the rest of this branch that \(t>2\). For either feasible outer
singleton \(i\), its private deviations are at most one and every trunk
deviation is at most \(H-h_i\). Thus its complete route value is at most
\(\max\{1,H-h_i\}\). Because every feasible route has value at least
\(t>2\), the value-one branch cannot control, and hence \(t\le H-h_i\), so
\(h_i\le\Delta\); together with \(h_i\le q_i\), this gives
\(h_i\le\min\{q_i,\Delta\}\).

For the remaining central singleton, write \(z=q_z\). If \(z\) is terminal
2, its singleton route has trunk maximum \(H-d_z\). If \(z\) is terminal 3,
its trunk maximum is

\[
\max\{h_1+h_2,\ H-d_z\}\le\max\{2,\ H-d_z\},
\]

because each normalized contribution is at most one. Private deviations are
also at most one. Since this feasible singleton route must have value at least
\(t>2\), both cases force \(H-d_z\ge t\), hence
\(d_z\le\Delta\) and \(h_z=d_z z\le\Delta z\). Finally
\(h_u=d_uq\le q\). Summing these four bounds gives

\[
H\le q+\min\{x,\Delta\}+\min\{y,\Delta\}+\Delta z.
\tag{10}
\]

The all-C route is feasible. Under the standing assumption \(t>2\), its
private deviations cannot determine its value, so its trunk value \(H\)
satisfies \(H\ge t\) and \(\Delta\ge0\). Also
\(H\le q+S<3\) by \(d_i\le1\) and (8), so \(t>2\) implies
\(\Delta<1\). Thus define

\[
\Phi_\Delta(S)
:=\max_{\substack{0\le x,y,z\le1\\x+y+z=S}}
\left(\min\{x,\Delta\}+\min\{y,\Delta\}+\Delta z\right).
\]

Allocating mass first to the two outer coordinates and then to the central
coordinate gives the exact piecewise envelope

\[
\Phi_\Delta(S)=
\begin{cases}
S,
&0\le S\le2\Delta,\\[1mm]
2\Delta+\Delta(S-2\Delta),
&2\Delta\le S\le2\Delta+1,\\[1mm]
3\Delta,
&2\Delta+1\le S\le3.
\end{cases}
\tag{11}
\]

Since \(t=H-\Delta\), the first regime gives

\[
t\le q+S-\Delta\le q+\frac S2<2,
\]

using \(q\le1\) and \(S<2\). The third regime gives

\[
t\le q+2\Delta\le q+S-1
<1+q\left(1-\frac1\kappa\right)\le2,
\]

where (8) was used. Thus only the middle regime can support a value above
two. There,

\[
t\le q+\Delta+\Delta S-2\Delta^2
\le q+\frac{(1+S)^2}{8},
\tag{12}
\]

with equality in the quadratic maximization at

\[
\Delta=\frac{1+S}{4}.
\]

The standing \(t>2\) reduction already gave \(0\le\Delta<1\), so no
additional \(\Delta\)-regime is missing.

### Why the \(t>2\) guard is essential

The star-triangle blocker pattern alone does **not** imply (10). Take

\[
\kappa=\frac{21}{10},\qquad
q=\left(\frac3{10},\frac1{20},\frac9{50},\frac12\right),\qquad
d=\left(\frac25,\frac4{25},\frac25,1\right),
\]

with scenarios

\[
k^{(1)}=\left(1,\frac{21}{10},1,1\right),\qquad
k^{(2)}=\left(\frac{21}{10},1,\frac{21}{10},\frac{21}{10}\right).
\]

The common feasible E-sets are exactly
\(\varnothing,\{1\},\{3\},\{4\}\), with route values

\[
\frac7{10},\quad\frac{29}{50},\quad\frac12,\quad\frac12.
\]

Hence \(t=1/2\), \(H=7/10\), and \(\Delta=1/5\), whereas the right-hand
side of (10) is only

\[
\frac1{20}+\frac15+\frac15+\frac15\frac9{50}
=\frac{243}{500}<\frac{350}{500}=H.
\]

This counterexample lies entirely in the \(t\le2\) branch, where the desired
global upper bound is already immediate. It therefore invalidates only the
unconditional wording, not the repaired tail argument.

## One-dimensional maximization

Define

\[
g_\kappa(q)
=q+\frac{(1+B_\kappa(q))^2}{8},
\qquad 0\le q\le1.
\tag{13}
\]

For \(1\le\kappa\le2\), one has
\(B_\kappa(q)=\kappa(1-q)\) throughout \([0,1]\). The resulting quadratic is
convex, so its maximum occurs at an endpoint; both endpoint values are at
most \(9/8\). Thus

\[
\max_{q\in[0,1]}g_\kappa(q)=\frac98
\qquad(1\le\kappa\le2).
\tag{14}
\]

For \(\kappa>2\), the two bounds in (9) intersect at

\[
q=Q_\kappa,
\qquad S=S_\kappa.
\]

On \([0,Q_\kappa]\), the active bound is
\(2-q/\kappa\), and

\[
\frac{d}{dq}
\left[q+\frac{(3-q/\kappa)^2}{8}\right]
=1-\frac{3-q/\kappa}{4\kappa}>0.
\]

On \([Q_\kappa,1]\), the active bound is \(\kappa(1-q)\); the resulting
quadratic is convex, so its maximum is at \(Q_\kappa\) or \(1\). The value at
\(1\) is \(9/8\), while the value at the intersection is \(F(\kappa)\).
By (6), \(F(\kappa)>F(2)=9/8\) for \(\kappa>2\). Therefore

\[
\max_{q\in[0,1]}g_\kappa(q)=F(\kappa)
\qquad(\kappa>2).
\tag{15}
\]

In the middle regime, the right-hand side of (12) is strictly increasing in
\(S\), while (9) is strict. Therefore every instance in the standing
\(t>2\) branch satisfies

\[
t<g_\kappa(q).
\]

For \(1\le\kappa\le2\), (14) makes \(t>2\) impossible. For
\(2<\kappa\le\kappa_0\), (15) and \(F(\kappa)\le2\) again make
\(t>2\) impossible. For \(\kappa\ge\kappa_0\), either \(t\le2\le
F(\kappa)\), or the standing branch gives \(t<F(\kappa)\). Consequently,
for \(\kappa>2\),

\[
\beta_G^{(2\mathrm{sc})}(\kappa)
\le\max\{2,F(\kappa)\},
\]

while (14) gives the upper bound two for \(1\le\kappa\le2\). Together with
the noncentral RB-003 bound, this proves (2)-(3) after the matching lower
sequence below is included.

## Matching strict sequence

Fix \(\kappa>2\) and choose

\[
0<\varepsilon<S_\kappa-1.
\tag{16}
\]

Set

\[
q_2=Q_\kappa,
\qquad
S=S_\kappa-\varepsilon,
\qquad
\Delta=\frac{1+S}{4},
\]

\[
q_1=q_4=\Delta,
\qquad
q_3=\frac{S-1}{2},
\qquad
d=(1,1,\Delta,1).
\tag{17}
\]

Because \(1<S<S_\kappa<2\), all coordinates satisfy the required positivity
and box constraints. Use

\[
k^{(1)}=(1,\kappa,1,1),
\qquad
k^{(2)}=(\kappa,1,\kappa,\kappa).
\tag{18}
\]

Both heterogeneity ratios equal \(\kappa\). The exact scenario budgets are

\[
B_1=\kappa Q_\kappa+S=\kappa-\varepsilon,
\qquad
B_2=Q_\kappa+\kappa S=2\kappa-\kappa\varepsilon.
\tag{19}
\]

Since \(0<\varepsilon<S_\kappa-1<1\), scenario 1 permits the three A-singletons
but blocks every set containing terminal 2, while scenario 2 permits the three
A-singletons but blocks every A-pair. Hence the common feasible E-sets are
exactly

\[
\varnothing,\quad\{1\},\quad\{3\},\quad\{4\}.
\tag{20}
\]

Put

\[
V_{\kappa,\varepsilon}
:=Q_\kappa+\frac{(1+S)^2}{8}.
\]

Direct evaluation on the thirteen graph arcs gives

\[
\operatorname{val}(\{1\})
=\operatorname{val}(\{3\})
=\operatorname{val}(\{4\})
=V_{\kappa,\varepsilon},
\]

while the all-C route has value

\[
V_{\kappa,\varepsilon}+\Delta.
\]

Therefore the exact finite instance value is

\[
V_{\kappa,\varepsilon}
=F(\kappa)-\frac{1+S_\kappa}{4}\varepsilon
 +\frac{\varepsilon^2}{8}
\longrightarrow F(\kappa).
\tag{21}
\]

When \(\kappa\) and \(\varepsilon\) are rational, all data are rational. For
arbitrary real \(\kappa>2\), (17)-(21) give a strict real sequence.

The accompanying verifier checks this construction over the **entire** stated
parameter range, not only at sampled anchors. It substitutes
\(\kappa=2+a\) and
\(\varepsilon=(S_\kappa-1)/(1+b)\) with \(a,b>0\), then verifies that each
claimed route maximum dominates every one of the thirteen arc deviations by
an exact rational function whose numerator and denominator have nonnegative
coefficients in \(a,b\). Rational anchors are retained only as readable
regression examples.

For \(\kappa>\kappa_0\), the value \(F(\kappa)>2\) cannot be attained by a
finite instance: attaining the unique maximum in (15) would force equality in
the strict star and triangle bounds (7)-(8). The endpoint
\(\kappa=\kappa_0\) has exact supremum two; this argument does not separately
classify all possible finite equality cases at that endpoint.

## What remains open

The exact curve on

\[
1\le\kappa<\kappa_0
\]

is still open. The revised proof narrows the task to deciding where the value
lies inside (5), together with the corresponding lower interval for
\(1\le\kappa\le2\). In particular, it remains unknown whether only the
equal-weight one-scenario branch and the star-triangle branch are active, or
whether another two-scenario family intervenes.
