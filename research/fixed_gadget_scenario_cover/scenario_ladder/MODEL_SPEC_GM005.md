# Model Specification for GM-005

## Fixed graph and designated paths

The trunk arcs are

\[
a_1=sv_1,\quad a_2=v_1v_2,\quad a_3=v_2v_3,\quad
 a_4=v_3v_4,\quad a_5=v_4v_5.
\]

Each terminal has exactly two designated paths:

| terminal | E path | C path |
|---:|---|---|
| 1 | `e1` | `a1 a2 a3 c1` |
| 2 | `e2` | `a1 a2 a3 a4 a5 c2` |
| 3 | `a1 e3` | `a1 a2 a3 a4 a5 c3` |
| 4 | `a1 a2 e4` | `a1 a2 a3 a4 c4` |

The C-minus-E trunk supports are therefore

\[
I_1=\{a_1,a_2,a_3\},\qquad
I_2=\{a_1,a_2,a_3,a_4,a_5\},
\]

\[
I_3=\{a_2,a_3,a_4,a_5\},\qquad
I_4=\{a_3,a_4\}.
\tag{M1}
\]

In particular, all four supports contain `a3`.

## Fractional flow and normalization

Terminal `i` has demand

\[
0<d_i\le 1,\qquad \max_i d_i=1,
\]

and sends fraction `q_i` on E and `1-q_i` on C, where

\[
0\le q_i\le1.
\]

Put

\[
h_i=d_iq_i,\qquad
\ell_i=d_i(1-q_i),\qquad
H=\sum_{i=1}^4h_i.
\tag{M2}
\]

An unsplittable routing is represented by its E-set `R`. On a trunk arc `a`,
its deviation from the fractional flow is

\[
\Delta_a(R)=
\sum_{\substack{i\notin R\\a\in I_i}}h_i
-
\sum_{\substack{i\in R\\a\in I_i}}\ell_i.
\tag{M3}
\]

Every positive deviation on a terminal-private arc is at most `d_i<=1`.
The route value is the maximum positive deviation over all thirteen arcs.

Dropping the nonpositive E-routed terms in (M3) gives the exact analytic
envelope

\[
\Delta_a(R)\le \sum_{i\notin R}h_i\le 4-|R|
\]

on every trunk arc. On a private arc, the only possible positive deviation is
either (h_i) or \(\ell_i=d_i(1-q_i)\), hence at most one. Therefore

\[
M(R)\le\max\left\{1,\sum_{i\notin R}h_i\right\}.
\tag{M3a}
\]

The standalone proof is `TRUNK_PRIVATE_ARC_ENVELOPE.md`; its exact structural
corroboration is `reproduction/verify_arc_envelope.py`.

The all-C route `R=empty` is always feasible and has exact value `H`, witnessed
on `a3`.

## Three positive scenarios

There are exactly three vectors

\[
k^{(j)}\in\mathbb R_{>0}^4\qquad(j=1,2,3).
\]

An E-set `R` is feasible precisely when

\[
k^{(j)}(R):=\sum_{i\in R}k_i^{(j)}
\le
k^{(j)}\cdot q
\qquad(j=1,2,3).
\tag{M4}
\]

The inequality is weak. A set is blocked by scenario `j` only when its weight
is **strictly greater** than the fractional budget.

Let

\[
t=\min_{R\text{ feasible}}\max_a\bigl(y^R(a)-x(a)\bigr).
\tag{M5}
\]

GM-005 concerns the supremum of `t` over the stated fixed-gadget domain.
