# The Identically Zero Cost-Difference Stratum

When every full-demand route-cost difference is zero, all 16 historical
cheap/expensive route choices are cost feasible. This degenerate stratum is not
covered by the sign-oriented threshold theorem because there is no nonzero
orientation.

Normalize `d_max=1`, and write

\[
\ell_i=d_ip_i,\qquad e_i=d_i(1-p_i).
\]

Here \(\ell_i\) is terminal \(i\)'s positive private-arc deviation when its
historical E route is chosen, while \(e_i\) is its positive private-arc
and trunk contribution when its historical C route is chosen.

## Theorem UC-019

On the fixed topology, the identically zero cost-difference stratum has exact
value

\[
\boxed{\beta_0=\frac45}.
\]

## Upper bound

Define

\[
H:=\{i:\ell_i>4/5\}.
\]

Choose the historical C route exactly for terminals in \(H\), and choose the
historical E route for every other terminal. This routing is cost feasible
because all 16 routings have the same cost.

For \(i\in H\), since \(d_i\le1\),

\[
e_i=d_i-\ell_i<1-\frac45=\frac15.
\]

For \(i\notin H\),

\[
\ell_i\le\frac45.
\]

Therefore every positive private-arc deviation is at most \(4/5\): a C-chosen
terminal contributes \(e_i<1/5\), while an E-chosen terminal contributes
\(\ell_i\le4/5\).

On a trunk arc, only C-chosen terminals can contribute positively. Every such
contribution is less than \(1/5\), and there are only four terminals. Hence
on every trunk arc the positive deviation is strictly less than

\[
4\cdot\frac15=\frac45.
\]

Thus the selected routing has maximum upper deviation at most \(4/5\), proving
\(\beta_0\le4/5\).

## Lower bound

Take

\[
d_i=1,\qquad p_i=\frac45\qquad(i=1,2,3,4).
\]

If any terminal uses its historical E route, its positive private-arc deviation
is \(\ell_i=4/5\). If all four terminals use C, trunk arc \(a_3\), which belongs
to all four path-difference supports, has deviation

\[
4\left(1-\frac45\right)=\frac45.
\]

Therefore every routing has maximum upper deviation at least \(4/5\), and the
all-C routing attains exactly \(4/5\). Consequently \(\beta_0=4/5\). ∎

## Computational corroboration

`cost_free_stratum_check.py` verifies the exact 16-route lower instance and,
on a declared rational grid, checks the constructive upper routing above. The
human proof is the theorem; the finite grid is regression evidence only.
