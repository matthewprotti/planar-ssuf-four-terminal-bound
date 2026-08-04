# Scenario-Cover Duality for the Four-Terminal SSUF Gadget

**Status:** internally AI-reviewed structural theorem plus an exact finite
atlas. The five nonblocking R3A repairs are applied in this derived RC1 copy.
The narrow fixed-RB-family continuum theorem in §9 was reviewed separately in
R3C and replayed nonblind in R3D.

Matthew's completed no-error mathematical review covered only the immutable
public v0.2.1 corpus. It did not cover this scenario-cover mathematics or
its reproduction.

## 1. Orientation and notation

A routing is encoded by its **C-set**

\[
S\subseteq[4],
\]

where terminal \(i\) uses its C path exactly when \(i\in S\). Let
\(p_i\in[0,1]\) be the fractional C fraction and write

\[
v_S:=\mathbf 1_S-p\in\mathbb R^4.
\]

Let \(k_i\) be the full-demand E-minus-C route-cost difference for terminal
\(i\). For the positive-cost lane considered here, \(k_i>0\). The difference
between the unsplittable route cost and the fractional route cost is

\[
c(y^S)-c(x)=k\cdot p-k(S)=-k\cdot v_S.
\]

Therefore \(S\) is cost-nonincreasing in scenario \(k\) exactly when

\[
\boxed{k\cdot v_S\ge 0.}
\tag{1}
\]

### Fixed-support legality and a sign check

This orientation is imported from commit
aaa472492d72e4c567d699eface450e376caece2, specifically
research/unequal_cost_fixed_topology/MASTER_OBJECTIVE_AND_COST_REALIZATION.md
and the fixed paths in
research/unequal_cost_fixed_topology/FIXED_TOPOLOGY_APPENDIX.md. There,
\[
k_i=d_i\bigl(c(P_i^{\mathrm E})-c(P_i^{\mathrm C})\bigr),
\]
so direct subtraction gives
\[
c(y^S)-c(x)=k\cdot p-k(S)=-k\cdot v_S.
\]

Every positive normal used here is physically legal on the fixed graph. The
demands satisfy \(d_i>0\). The terminal-private arcs are:

| terminal | E-private arc | C-private arc |
|---:|---|---|
| 1 | \((s,t_1)\) | \((v_3,t_1)\) |
| 2 | \((s,t_2)\) | \((v_5,t_2)\) |
| 3 | \((v_1,t_3)\) | \((v_5,t_3)\) |
| 4 | \((v_2,t_4)\) | \((v_4,t_4)\) |

Put cost \(k_i/d_i\) on terminal \(i\)'s E-private arc, put zero cost on its
C-private arc and every other arc, and obtain the full-demand E-minus-C
difference \(k_i\). The constructed arc costs are nonnegative and
commodity-independent; rational \(k,d\) give rational costs.

For an exact sign check at (8), take \(k=(1,1999,1,1)\). Then
\[
k\cdot p=\frac{3001}{1000}.
\]
For \(S=134\), \(k(S)=3\), hence
\[
k\cdot v_{134}=-\frac1{1000}<0
\quad\text{and}\quad
c(y^{134})-c(x)=\frac1{1000}>0.
\]
Thus C-set \(134\) is correctly eliminated, while every C-set containing
terminal 2 is feasible. This checks both the E-minus-C sign and the
positive-normal realization against an exact package witness.

Define the route's maximum positive arc deviation by

\[
M(S;p,d).
\]

The accompanying checker reconstructs this value on all five trunk arcs and
all eight private arcs.

## 2. Losing downsets and low-deviation routes

For one positive scenario, define its losing or eliminated family

\[
\mathcal B(k;p)
:=\{S\subseteq[4]:k\cdot v_S<0\}.
\tag{2}
\]

Because \(k>0\), \(\mathcal B(k;p)\) is a downset: if \(T\subseteq S\) and
\(S\in\mathcal B(k;p)\), then

\[
k(T)\le k(S)<k\cdot p,
\]

so \(T\in\mathcal B(k;p)\).

For a deviation threshold \(t\), define

\[
\mathcal G_{<t}(p,d)
:=\{S\subseteq[4]:M(S;p,d)<t\}.
\tag{3}
\]

The strict inequality is deliberate. It removes endpoint ambiguity: to force
the best common feasible route to have value at least \(t\), every route of
value **strictly below** \(t\) must be eliminated.

## 3. SC-000 — exact scenario-cover duality

Let \(k^{(1)},\ldots,k^{(m)}>0\) be \(m\) cost scenarios, and let

\[
\mathcal F(p;k^{(1)},\ldots,k^{(m)})
:=\{S:k^{(j)}\cdot v_S\ge0\text{ for every }j\}
\]

be their common cost-nonincreasing routing family. Define

\[
\Phi(p,d;k^{(1)},\ldots,k^{(m)})
:=\min_{S\in\mathcal F}M(S;p,d).
\]

This minimum is well-defined. The all-C C-set \([4]\) has displacement
\(v_{[4]}=\mathbf1-p\ge0\), so it lies in \(\mathcal F\) for every positive
scenario.

Then, for every real threshold \(t\),

\[
\boxed{
\Phi(p,d;k^{(1)},\ldots,k^{(m)})\ge t
\iff
\mathcal G_{<t}(p,d)
\subseteq
\bigcup_{j=1}^m\mathcal B(k^{(j)};p).
}
\tag{4}
\]

### Proof

The left side says that no common feasible routing has deviation below \(t\).
By (1), a route fails common feasibility exactly when at least one scenario has
negative dot product with its displacement. Thus every route in
\(\mathcal G_{<t}\) must lie in at least one losing family, which is precisely
the right side. The reverse implication is the same argument read backward.
\(\square\)

This equivalence is elementary, but it changes the research object. Multiple
cost scenarios are no longer primarily a family of cost inequalities. They are
a restricted cover of the low-deviation displacement configuration by open
homogeneous halfspaces.

## 4. Restricted cover number and the robust value

For \(\kappa\ge1\), let

\[
\mathcal K_\kappa
:=\left\{k\in\mathbb R^4_{>0}:
\frac{\max_i k_i}{\min_i k_i}\le\kappa\right\}.
\]

For a routing family \(\mathcal A\), define its restricted scenario-cover
number

\[
\tau_{\kappa,p}(\mathcal A)
:=\min\left\{m:
\mathcal A\subseteq\bigcup_{j=1}^m\mathcal B(k^{(j)};p),
\ k^{(j)}\in\mathcal K_\kappa
\right\}.
\tag{5}
\]

Use \(\tau_{\kappa,p}(\varnothing)=0\); if no such cover exists, its value is
\(+\infty\). The notation \(\kappa=\infty\) means unrestricted positive
normals. A result for exactly \(m\) scenarios also gives an at-most-\(m\)
cover, and conversely a smaller cover may be padded to exactly \(m\) by
duplicating a positive scenario. Distinctness is not required.

Let \(\mathcal R(p,d)=\{M(S;p,d):S\subseteq[4]\}\) be the finite set of route
values. The best value that \(m\) \(\kappa\)-bounded scenarios can force at a
fixed \((p,d)\) is

\[
\boxed{
\Psi_{m,\kappa}(p,d)
=
\max\left\{r\in\mathcal R(p,d):
\tau_{\kappa,p}(\mathcal G_{<r}(p,d))\le m
\right\}.
}
\tag{6}
\]

Equation (6) is the finite optimization form of the duality.

### Partition form

For a finite target family \(\mathcal A\), let \(\kappa_1(\mathcal U;p)\) be
the infimum condition number of one positive scenario that eliminates every
route in \(\mathcal U\). Define \(\kappa_2(\mathcal A;p)\) as the infimum
condition-number cap for a two-scenario cover. Then

\[
\kappa_2(\mathcal A;p)
=
\min_{\mathcal U\subseteq\mathcal A}
\max\bigl\{
\kappa_1(\mathcal U;p),
\kappa_1(\mathcal A\setminus\mathcal U;p)
\bigr\}.
\tag{7}
\]

Indeed, any two-scenario cover assigns each covered route to one scenario that
eliminates it; conversely, any partition and two corresponding normals give a
cover. For a twelve-route target, (7) has only \(2^{12}=4096\) labelled
assignments before symmetry. The separately reviewed fixed-RB-family phase
theorem is recorded in §9.

### Closure-to-strictness lemma

Let \(\mathcal U,\mathcal V\) be disjoint finite route families. Assume there
exists a strict positive realizer \(k^{\mathrm s}>0\) satisfying
\[
k^{\mathrm s}\cdot v_S<0\quad(S\in\mathcal U),
\qquad
k^{\mathrm s}\cdot v_T\ge0\quad(T\in\mathcal V).
\]
Here \(\mathcal U\) lists routes required to be eliminated and
\(\mathcal V\) lists any routes required to remain accepted. Normalize
positive normals by \(\min_i k_i=1\). In the weak closed problem replace the
first inequalities by \(k\cdot v_S\le0\), retain the accepted-route
inequalities, and minimize \(K=\max_i k_i\).

The feasible sublevel set below the value of any fixed feasible normal is
closed and contained in a box \([1,K_0]^4\), so a weak optimizer \(k^0\)
exists and realizes a minimum \(\kappa_*\). For \(0<\lambda\le1\), put
\[
k^\lambda=(1-\lambda)k^0+\lambda k^{\mathrm s}.
\]
Both endpoints are positive, every accepted-route dot product remains
nonnegative, and every losing-route dot product is strict because it is a
convex combination of a weakly negative and a strictly negative number.
Condition number is continuous on the positive orthant, so
\[
\operatorname{cond}(k^\lambda)
\longrightarrow
\operatorname{cond}(k^0)=\kappa_*
\qquad(\lambda\downarrow0).
\]
Therefore the weak minimum equals the strict infimum, and a strict realizer
exists in \(\mathcal K_\kappa\) for every \(\kappa>\kappa_*\). Availability
at \(\kappa_*\) is not implied by the weak optimizer; it holds exactly when
the strict system has a realizer at that cap.

If no strict realizer exists, the strict threshold is \(+\infty\). For an
empty elimination target use \(\kappa_1(\varnothing;p)=1\), attained. For an
exact losing-pattern threshold take
\(\mathcal V=2^{[4]}\setminus\mathcal U\); for the cover-only thresholds in
(7), take \(\mathcal V=\varnothing\). Thus a minimizing partition in (7)
gives an actual two-scenario cover for every larger \(\kappa\); availability
at equality requires strict endpoint realizers for both parts.

## 5. Relation to the marginal convex-hull theorem

The candidate one-scenario marginal theorem asserts

\[
p\in\operatorname{conv}\{\mathbf1_S:M(S;p,d)\le L\}.
\]

Equivalently,

\[
0\in\operatorname{conv}\{v_S:M(S;p,d)\le L\}.
\]

Therefore no single linear functional—positive, signed, or otherwise—can be
negative on every \(L\)-good displacement. This explains the one-scenario
averaging proof.

Two open halfspaces can cover a finite vector set whose convex hull contains
the origin. Thus the one-scenario convex-hull invariant is not expected to
control two scenarios by itself. The restricted cover number in (5) is the
next invariant.

## 6. SC-001 to SC-003 — exact finite atlas at the RB-003 witness

Take

\[
p=\left(\frac{251}{1000},\frac1{1000},\frac12,\frac{251}{1000}\right),
\qquad
 d=\left(1,1,\frac34,1\right).
\tag{8}
\]

The exact route levels are:

| C-set(s) | Exact value |
|---|---:|
| \(\varnothing,3\) | \(3/8\) |
| \(1,4\) | \(749/1000\) |
| \(2\) | \(999/1000\) |
| \(14\) | \(561/500\) |
| \(13,34\) | \(1123/1000\) |
| \(24\) | \(1373/1000\) |
| \(23\) | \(687/500\) |
| \(12\) | \(437/250\) |
| \(134\) | \(234/125\) |
| \(124\) | \(1061/500\) |
| \(123,234\) | \(2123/1000\) |
| \(1234\) | \(359/125\) |

The exact atlas establishes:

- the four-cube has 168 downsets;
- exactly 59 are losing families of a positive scenario at this \(p\);
- those 59 patterns have 32 distinct condition-number infima; and
- over all 168 downsets, the minimum scenario-cover counts are

\[
\begin{array}{c|rrrrrr}
\text{cover count}&0&1&2&3&4&\text{impossible}\\\hline
\text{downsets}&1&61&91&13&1&1.
\end{array}
\tag{9}
\]

The unique downset requiring four scenarios is the family of all proper
C-sets. The unique impossible downset is the full cube: the all-C routing can
never be eliminated by a positive scenario.

With unrestricted positive normals, the fixed point's exact robust ladder is

\[
\begin{array}{c|cccc}
m&1&2&3&4\\\hline
\Psi_{m,\infty}(p,d)
&561/500&1061/500&2123/1000&359/125.
\end{array}
\tag{10}
\]

These are fixed-instance values, not the global \(m\)-scenario suprema.

### Exact two-scenario heterogeneity phase

Set

\[
A=\frac{1498}{501},\qquad B=998,\qquad C=1998.
\]

Then the exact two-scenario phase diagram at (8) is

\[
\boxed{
\Psi_{2,\kappa}(p,d)=
\begin{cases}
561/500,&1\le\kappa\le A,\\
1123/1000,&A<\kappa\le B,\\
234/125,&B<\kappa\le C,\\
1061/500,&C<\kappa.
\end{cases}}
\tag{11}
\]

All three transitions are open on the new-regime side because the relevant
route eliminations are strict. The exact endpoint LPs have zero elimination
margin.

The package also records exact three- and four-scenario phase diagrams at the
same fixed point.

## 7. SC-004 — exact star-triangle cover threshold

For

\[
p_\varepsilon
=\left(\frac14+\varepsilon,\varepsilon,\frac12,
\frac14+\varepsilon\right),
\qquad
 d=\left(1,1,\frac34,1\right),
\qquad 0<\varepsilon<\frac14,
\tag{12}
\]

consider the joint feasible family

\[
\{123,124,234,1234\}.
\tag{13}
\]

The exact infimum condition number for a two-scenario realization of (13) is

\[
\boxed{
\kappa_\star(\varepsilon)
=\frac{2(1-\varepsilon)}{\varepsilon}.
}
\tag{14}
\]

It is not attained.

### Lower bound

Any realization of (13) must eliminate C-set \(134\) in at least one scenario.
For any positive normal \(k\),

\[
p_\varepsilon\cdot k-k(134)
=
\varepsilon k_2
-\left(\frac34-\varepsilon\right)(k_1+k_4)
-\frac12 k_3.
\]

If \(134\) is eliminated, the right side is positive. With
\(m=\min_i k_i\), this implies

\[
\varepsilon k_2>2(1-\varepsilon)m,
\]

and hence

\[
\frac{\max_i k_i}{\min_i k_i}
>\frac{2(1-\varepsilon)}{\varepsilon}.
\]

### Matching construction

Take

\[
k^{\mathrm c}=(1,r,1,1),
\qquad
r>\frac{2(1-\varepsilon)}{\varepsilon},
\tag{15}
\]

and

\[
k^{\triangle}=(s,1,s,s),
\qquad
s>\frac{1-\varepsilon}{2\varepsilon}.
\tag{16}
\]

The first scenario eliminates exactly the C-sets not containing terminal 2.
The second eliminates the empty set, the singletons, and the three pairs
incident to terminal 2. Their union leaves exactly (13). Since the threshold
in (15) is four times
the threshold in (16), the central scenario is the bottleneck. Equality only
ties C-set \(134\), so (14) is an unattained infimum.

At \(\varepsilon=1/1000\), the infima are

\[
1998
\quad\text{and}\quad
\frac{999}{2}.
\]

The simple integer scenarios

\[
(1,1999,1,1),
\qquad
(500,1,500,500)
\tag{17}
\]

produce the same feasible family and the exact objective \(1061/500\). They
reduce the maximum integer condition number of the earlier finite witness from
3000 to 1999.

Define the global fixed-gadget quantity locally by

\[
\beta_G^{(2,+)}(\kappa)
:=\sup_{\substack{p\in[0,1]^4,\ 0<d_i\le1\\\max_i d_i=1}}
\Psi_{2,\kappa}(p,d),
\]

where each of the two scenarios is coordinatewise strictly positive and has
condition number at most \(\kappa\). A direct corollary is the clean family
lower bound

\[
\beta_G^{(2\mathrm{sc})}(\kappa)
\ge
\frac{17}{8}-\frac{6}{\kappa+2},
\qquad \kappa>6,
\tag{18}
\]

interpreted supremally along \(\varepsilon\downarrow2/(\kappa+2)\). This is a
structural cover-derived bound, not claimed to improve the strongest existing
bounded-tail lower construction.

## 8. SC-005 — the old bounded-tail parameters from cover boundaries

Switch to the E-set orientation used in the bounded two-scenario draft. Let
\(Q\) be the central terminal's E fraction and let \(S\) be the total E
fraction of the three outer terminals.

For the center-heavy normal \((1,\kappa,1,1)\), the fractional budget is

\[
\kappa Q+S.
\]

The central singleton E-set lies on its blocking boundary when

\[
\kappa=\kappa Q+S,
\quad\text{or}\quad
S=\kappa(1-Q).
\tag{19}
\]

For the outer-heavy normal \((\kappa,1,\kappa,\kappa)\), the budget is

\[
Q+\kappa S.
\]

An outer E-pair lies on its blocking boundary when

\[
2\kappa=Q+\kappa S,
\quad\text{or}\quad
S=2-\frac Q\kappa.
\tag{20}
\]

Intersecting (19) and (20) gives

\[
\boxed{
Q_\kappa=\frac{\kappa(\kappa-2)}{\kappa^2-1},
\qquad
S_\kappa=\frac{\kappa(2\kappa-1)}{\kappa^2-1}.
}
\tag{21}
\]

Thus the parameters in the existing high-\(\kappa\) proof are not mysterious
optimization artifacts: they are the intersection of the two extremal
restricted halfspace-cover boundaries.

Substitution into the existing overload envelope gives

\[
F(\kappa)
=Q_\kappa+\frac{(1+S_\kappa)^2}{8}
=\frac{17\kappa^4-22\kappa^3-13\kappa^2+18\kappa+1}
{8(\kappa^2-1)^2}.
\tag{22}
\]

This is an exact algebraic recovery and conceptual reinterpretation. It does
not extend the already stated scope of the bounded-tail theorem by itself.

## 9. SC-006 — exact symbolic phase along the fixed RB family

For \(0<\varepsilon<1/8\), define

\[
A(\varepsilon)=\frac{3-4\varepsilon}{1+2\varepsilon},
\qquad
B(\varepsilon)=\frac1\varepsilon-2,
\qquad
C(\varepsilon)=\frac2\varepsilon-2.
\]

For the fixed four-terminal RB support, exactly two strictly positive
cost-difference scenarios, and condition number at most \(\kappa\), the
separately reviewed SC-006 theorem establishes

\[
\Psi_{2,\kappa}(p_\varepsilon,d)=
\begin{cases}
\frac98-3\varepsilon,
&1\le\kappa\le A(\varepsilon),\\[2mm]
\frac98-2\varepsilon,
&A(\varepsilon)<\kappa\le B(\varepsilon),\\[2mm]
\frac{15}{8}-3\varepsilon,
&B(\varepsilon)<\kappa\le C(\varepsilon),\\[2mm]
\frac{17}{8}-3\varepsilon,
&C(\varepsilon)<\kappa.
\end{cases}
\tag{23}
\]

Each transition point belongs to the lower branch because elimination is
strict and the newly required route ties the scenario budget at equality.
The focused theorem note proves the four branches analytically using the
route filtration, explicit constructions, and matching obstructions at
\(A,B,C\), including the condition-number-unrestricted fixed-family ceiling.

R3C accepted the theorem with three nonblocking presentation/integration
repairs, all applied in the derived focused note and this minimal integration
copy. R3D independently replayed the supplied exact computations, including
an off-registry rational parameter; it was deliberately nonblind and is
corroboration rather than the continuum proof. Neither review turns (23) into
a global bounded-\(\kappa\), different-topology, signed, zero-coordinate, or
multi-scenario result. The later R3B v2 lane separately reconstructed the
fixed finite atlas under technical answer isolation. It did not reproduce the
continuum theorem. Its preserved comparison label is
`SEMANTIC_MATHEMATICAL_MATCH / STRICT_CERTIFICATE_PAYLOAD_IDENTITY_FAIL`.

## 10. Evidence boundary

The package proves and checks:

- the exact duality (4);
- the exact fixed-point route table;
- all 168 downset LP classifications by rational primal-dual certificates;
- the 59-pattern and 32-threshold census;
- the cover-number distribution;
- the fixed-point unrestricted and bounded-\(\kappa\) phases;
- the improved finite two-scenario witness;
- the general star-triangle infimum (14); and
- the algebraic recovery (21)–(22); and
- the exact fixed-RB-family two-positive-scenario continuum phase (23),
  accepted in the separate R3C review.

It does not establish:

- independent adversarial acceptance of the global marginal theorem;
- the full global bounded-\(\kappa\) middle curve;
- the global \(m=3\) value \(3\) or global \(m\ge4\) value \(4\), which belong
  to separate imported private drafts;
- a stronger unrestricted planar SSUF constant;
- novelty, priority, peer review, or formal-proof-assistant verification.

The fixed-instance three- and four-scenario values in this package are not the
global constants \(3\) and \(4\). Those global statements remain separate
private proof drafts with their own review lane.
