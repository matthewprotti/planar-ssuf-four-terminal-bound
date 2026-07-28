# Master Fixed-Topology Objective and Arc-Cost Realization

This file fixes one notation for every exact-value statement in the unequal-
cost work package. It is a definition and an elementary realization lemma, not
a new global sharpness theorem.

## Physical two-route data

For terminal \(i\), let \(P_i^{\mathrm C}\) and \(P_i^{\mathrm E}\) be the two
paths in `FIXED_TOPOLOGY_APPENDIX.md`. Let

\[
d_i>0,\qquad p_i\in[0,1],\qquad d_{\max}:=\max_i d_i,
\]

where the fractional flow sends \(d_ip_i\) on \(P_i^{\mathrm C}\) and
\(d_i(1-p_i)\) on \(P_i^{\mathrm E}\). For
\(z\in\{0,1\}^4\), \(z_i=1\) means that the unsplittable routing uses
\(P_i^{\mathrm C}\).

Given one nonnegative, commodity-independent per-unit arc-cost vector \(c\),
define the full-demand route-cost difference

\[
k_i
:=
d_i\left(
\sum_{a\in P_i^{\mathrm E}}c(a)
-
\sum_{a\in P_i^{\mathrm C}}c(a)
\right).
\]

The unsplittable routing is cost-nonincreasing relative to the fractional flow
exactly when

\[
\sum_i k_i(z_i-p_i)\ge0. \tag{1}
\]

For an arc \(a\), its upper load deviation is

\[
\Delta_a(z;p,d)
:=
\sum_i d_i(z_i-p_i)
\left(
\mathbf 1_{a\in P_i^{\mathrm C}}
-
\mathbf 1_{a\in P_i^{\mathrm E}}
\right). \tag{2}
\]

## Master objective

The normalized fixed-topology objective is

\[
\boxed{
\Phi(k,p,d)
:=
\frac1{d_{\max}}
\min_{\substack{z\in\{0,1\}^4\\
                 k\cdot(z-p)\ge0}}
\max_{a\in A}\Delta_a(z;p,d).
} \tag{3}
\]

The feasible set in (3) is never empty: choose the cheaper physical route in
each nonzero coordinate and either route in a zero coordinate. The research
files usually normalize \(d_{\max}=1\), in which case the denominator
disappears.

For a fixed positive threshold family \(\mathcal F\), “the value of the cell”
means

\[
\sup\left\{
\Phi(k,p,d):
k_i>0,\quad
\{z:k\cdot(z-p)\ge0\}=\mathcal F,\quad
d_i>0
\right\}. \tag{4}
\]

For a fixed sign/zero pattern \(\sigma\), “the value of the stratum” means the
same supremum with \(\operatorname{sign}(k)=\sigma\). Rational-value statements
restrict \(k,p,d\) to rational data. Thus UC-017, UC-018, UC-019, and UC-023
all optimize the same physical quantity; only their parameter domains differ.

## Nonnegative arc-cost realization lemma

Every vector \(k\in\mathbb R^4\) used in (3) is realizable by legal
nonnegative, commodity-independent arc costs on the fixed graph.

Each \(P_i^{\mathrm C}\) and \(P_i^{\mathrm E}\) has a terminal arc used by no
other candidate path. In terminal order, the C-private arcs are

\[
(v_3,t_1),\ (v_5,t_2),\ (v_5,t_3),\ (v_4,t_4),
\]

and the E-private arcs are

\[
(s,t_1),\ (s,t_2),\ (v_1,t_3),\ (v_2,t_4).
\]

Set every other arc cost to zero. On terminal \(i\)'s two private terminal
arcs set

\[
c_i^{\mathrm E}=\frac{\max\{k_i,0\}}{d_i},
\qquad
c_i^{\mathrm C}=\frac{\max\{-k_i,0\}}{d_i}. \tag{5}
\]

All costs in (5) are nonnegative and are attached to arcs, not commodities.
Because the chosen terminal arcs are path-private, the resulting full-demand
E-minus-C difference is

\[
d_i(c_i^{\mathrm E}-c_i^{\mathrm C})=k_i.
\]

If \(k,p,d\) are rational, so are the constructed arc costs. This establishes
physical legality of the signed and zero-coordinate parameterizations. It
does not identify an optimizer, prove any cell value, or turn an arbitrary
terminal-label permutation into an objective symmetry.

## Scope

The master objective is restricted to the fixed graph and its two paths per
terminal. The current proved results leave 79 strictly positive labeled cells
in 11 abstract-label search orbits open. The orbit quotient is not a graph-
symmetry reduction.
