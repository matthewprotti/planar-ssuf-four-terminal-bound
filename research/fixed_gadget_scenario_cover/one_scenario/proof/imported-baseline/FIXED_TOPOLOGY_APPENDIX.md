# Fixed Topology and Deviation Formulas

This appendix makes the follow-on unequal-cost package auditable without
opening the released manuscript.

## Directed graph

The vertices are

\[
\{s,v_1,v_2,v_3,v_4,v_5,t_1,t_2,t_3,t_4\}.
\]

The five trunk arcs are

\[
a_j=(v_{j-1},v_j)\qquad(1\le j\le5),\quad v_0=s.
\]

The remaining arcs are

\[
(s,t_1),(v_3,t_1),(s,t_2),(v_5,t_2),
(v_1,t_3),(v_5,t_3),(v_2,t_4),(v_4,t_4).
\]

Every terminal has exactly two source-terminal paths:

\[
\begin{aligned}
P^{\mathrm E}_1&=(s,t_1),
&P^{\mathrm C}_1&=(s,v_1,v_2,v_3,t_1),\\
P^{\mathrm E}_2&=(s,t_2),
&P^{\mathrm C}_2&=(s,v_1,v_2,v_3,v_4,v_5,t_2),\\
P^{\mathrm E}_3&=(s,v_1,t_3),
&P^{\mathrm C}_3&=(s,v_1,v_2,v_3,v_4,v_5,t_3),\\
P^{\mathrm E}_4&=(s,v_1,v_2,t_4),
&P^{\mathrm C}_4&=(s,v_1,v_2,v_3,v_4,t_4).
\end{aligned}
\]

Here E and C retain the historical names “expensive” and “cheap.” In the
unequal-cost reduction, only the positive full-demand cost differences between
these routes matter.

`MASTER_OBJECTIVE_AND_COST_REALIZATION.md` defines the common objective
\(\Phi(k,p,d)\) for positive, signed, and zero route-cost differences. It also
records the path-private construction that realizes every such difference
vector using nonnegative, commodity-independent arc costs. In particular,
signed \(k_i\) are physical E-minus-C route-cost differences, not negative arc
costs.

## Trunk difference supports

The arcs added to terminal \(i\)'s route when switching from E to C are

\[
\begin{aligned}
I_1&=\{a_1,a_2,a_3\},\\
I_2&=\{a_1,a_2,a_3,a_4,a_5\},\\
I_3&=\{a_2,a_3,a_4,a_5\},\\
I_4&=\{a_3,a_4\}.
\end{aligned}
\]

Let \(d_i\in(0,1]\), let \(p_i\in[0,1]\) be the fractional C fraction, and
write

\[
\ell_i=d_ip_i,
\qquad
e_i=d_i(1-p_i).
\]

For a cheap set \(S\), terminal \(i\)'s contribution to the deviation on a
trunk arc in \(I_i\) is

\[
\begin{cases}
e_i,&i\in S,\\
-\ell_i,&i\notin S.
\end{cases}
\]

It contributes zero on trunk arcs outside \(I_i\).

## Private terminal arcs

On an arc unique to the C route, terminal \(i\)'s deviation is \(e_i\) when
cheap and \(-\ell_i\) when expensive. On an arc unique to the E route, the
signs reverse. Therefore every positive private-arc deviation is at most

\[
\max\{e_i,\ell_i\}\le d_i\le1.
\]

Since

\[
L=\frac{299-41\sqrt{41}}{32}>\frac98>1,
\]

private arcs cannot obstruct an upper bound of \(L\); only the trunk maxima
need the longer argument.

## Exact pair maxima on the trunk

When precisely terminals \(i,j\) are cheap, let \(M_{ij}\) be the maximum of
the five trunk deviations. Direct substitution into the four supports gives

\[
\begin{array}{c@{\qquad}c}
\{i,j\}&M_{ij}\\
\hline
\{1,2\}&e_1+e_2\\
\{1,3\}&e_1+e_3-\ell_2\\
\{1,4\}&\max\{e_1-\ell_2,\ e_1+e_4-\ell_2-\ell_3\}\\
\{2,3\}&e_2+e_3\\
\{2,4\}&\max\{e_2-\ell_1,\ e_2+e_4-\ell_3\}\\
\{3,4\}&e_3+e_4-\ell_2.
\end{array}
\]

`symbolic_every_pair_check.py` reconstructs all five arc expressions for every
pair and checks that these maxima are both dominating and attained.

## Three-cheap trunk maxima

For later no-pair analysis, the exactly-three-cheap trunk maxima are:

| Cheap set | Missing terminal | Maximum trunk deviation |
| --- | ---: | --- |
| 234 | 1 | `e2+e3+e4` |
| 134 | 2 | `e1+e3+e4-l2` |
| 124 | 3 | `max(e1+e2, e1+e2+e4-l3)` |
| 123 | 4 | `e1+e2+e3` |

The all-cheap routing has trunk maximum at most `e1+e2+e3+e4`.
These identities are direct substitutions from the four fixed supports. They are
used only as upper bounds in UC-013 and are checked by exact rational witness
enumeration in UC-014.
