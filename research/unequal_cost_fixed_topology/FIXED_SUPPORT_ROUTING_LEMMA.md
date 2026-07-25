# Fixed-Support Routing Lemma

Let the four trunk supports be those in `FIXED_TOPOLOGY_APPENDIX.md`. Define

\[
L:=\frac{299-41\sqrt{41}}{32}.
\]

## Lemma

For arbitrary real data

\[
d_i\in(0,1],\qquad \max_i d_i=1,
\qquad p_i\in[0,1],
\qquad 1<\sum_{i=1}^4p_i\le2,
\]

at least one exactly-two-cheap routing has maximum upper deviation, over every
arc of the fixed graph, at most \(L\).

The lemma is purely a routing statement. It assumes that all six two-cheap
routings are available; it does not use equal route costs.

## Proof

Put

\[
r:=\sum_i p_i.
\]

Replace \(p_i\) by

\[
\widehat p_i:=\frac{p_i}{r}.
\]

Then \(0\le\widehat p_i\le p_i\) and \(\sum_i\widehat p_i=1\). For a fixed
exactly-two-cheap routing, decreasing a cheap fraction increases its positive
contribution \(d_i(1-p_i)\), while decreasing an expensive fraction makes its
negative contribution \(-d_ip_i\) less negative. Thus every trunk deviation
can only increase. It is therefore enough to prove the upper bound for the
boundary data \(\widehat p\). From now on write \(p_i=\widehat p_i\), so
\(\sum_i p_i=1\), and set

\[
\ell_i=d_ip_i,
\qquad e_i=d_i(1-p_i).
\]

Positive deviations on private terminal arcs are at most \(d_i\le1<L\), so it
suffices to control the trunk maxima \(M_{ij}\) listed in the topology
appendix.

If \(e_4<\ell_3\), then

\[
M_{14}=e_1-\ell_2\le1,
\]

and the result follows. Hence assume \(e_4\ge\ell_3\). Then

\[
M_{14}=e_1+e_4-\ell_2-\ell_3,
\qquad
M_{24}=e_2+e_4-\ell_3.
\]

Because \(d_1,d_4\le1\),

\[
p_1=1-\frac{e_1}{d_1}\le1-e_1,
\qquad
p_4\le1-e_4.
\]

Using \(\sum_i p_i=1\) gives

\[
e_1+e_4\le1+p_2+p_3. \tag{1}
\]

Set

\[
s=d_2,\qquad t=d_3,\qquad p=p_2,\qquad q=p_3.
\]

Then

\[
e_2=s(1-p),\quad \ell_2=sp,
\qquad
e_3=t(1-q),\quad \ell_3=tq.
\]

Define

\[
L_0:=\min\{e_2,e_3-\ell_2\},
\qquad
R_0:=\min\{e_2-\ell_3,e_3-\ell_2\}.
\]

The smaller of \(M_{12},M_{13}\) is \(e_1+L_0\), and the smaller of
\(M_{24},M_{34}\) is \(e_4+R_0\). Together with (1),

\[
\min_{|S|=2}M_S\le\min\{T_1,T_2,T_3\}, \tag{2}
\]

where

\[
T_1=e_2+e_3,
\qquad
T_2=1+p+q-\ell_2-\ell_3,
\qquad
T_3=\frac{1+p+q+L_0+R_0}{2}.
\]

### Case 1: \(t\ge s\)

The difference between the two candidates in \(R_0\) is

\[
(e_3-\ell_2)-(e_2-\ell_3)=t-s,
\]

so \(R_0=e_2-\ell_3\). Also \(L_0=e_2\) when \(e_3\ge s\), and
\(L_0=e_3-\ell_2\) when \(e_3\le s\). Consequently

\[
T_3\le\widetilde T_3
:=\frac{1+2s+(1-2s)p+(1-t)q}{2}. \tag{3}
\]

If

\[
s+\frac{s}{t}\le1,
\]

then \(s\le1/2\), and the convex combination

\[
(1-2s)T_1+2s\widetilde T_3
=t+2s(1-t)+q\bigl(s(1+t)-t\bigr)
\]

is at most one. Indeed, the displayed condition gives
\(s\le t/(1+t)\), so the coefficient of \(q\) is nonpositive, while

\[
t+2s(1-t)
\le t+\frac{2t(1-t)}{1+t}
=\frac{t(3-t)}{1+t}
\le1.
\]

The coefficients \(1-2s\) and \(2s\) are nonnegative and sum to one, so (2)
is at most one.

Now suppose

\[
s+\frac{s}{t}\ge1.
\]

Define

\[
\lambda_1=\frac{s}{t}-s,
\qquad
\lambda_2=s+\frac{s}{t}-1,
\qquad
\lambda_3=2\left(1-\frac{s}{t}\right).
\]

These are nonnegative and sum to one. Exact cancellation gives

\[
\lambda_1T_1+\lambda_2T_2+\lambda_3\widetilde T_3
=g(s,t):=s\left(4-s-t-\frac{s}{t}\right). \tag{4}
\]

Hence (2) is at most \(g(s,t)\).

### Case 2: \(t\le s\)

Both minima defining \(L_0,R_0\) select \(e_3-\ell_2\), so

\[
T_3=\frac{1+2t+(1-2s)p+(1-2t)q}{2}.
\]

If \(t\le1/2\), then

\[
(1-2t)T_1+2tT_3
=s+2t-2st+p(t-s)\le1.
\]

If \(t\ge1/2\), then

\[
(2t-1)T_2+2(1-t)T_3
=t(3-2t)+p(t-s)\le t(3-2t)\le\frac98.
\]

Thus a value above \(9/8\) can occur only in the region

\[
0<s\le t\le1,
\qquad
s+\frac{s}{t}\ge1,
\]

where (4) applies.

### Optimization of \(g\)

Optimize on the compact set

\[
\overline{\mathcal D}
=\{(s,t):0\le s\le t\le1,\ s(t+1)\ge t\}.
\]

The only point with \(t=0\) is \((0,0)\). Define \(g(0,0)=0\); this is
continuous because \(0\le s^2/t\le s\) whenever \(0<s\le t\).

At an interior stationary point,

\[
s=t^2,
\qquad
2t^2+3t-4=0.
\]

Therefore

\[
t_* =\frac{\sqrt{41}-3}{4},
\qquad
s_*=t_*^2,
\qquad
g(s_*,t_*)=L.
\]

On the three nontrivial boundary pieces,

\[
\begin{array}{c@{\qquad}c}
s=t&g=t(3-2t)\le9/8,\\
t=1&g=s(3-2s)\le9/8,\\
s+s/t=1&g=\dfrac{t(3-t)}{t+1}\le1.
\end{array}
\]

Since \(L>9/8\), the global maximum is \(L\). Hence some exactly-two-cheap
routing has trunk maximum at most \(L\), and its private-arc deviations are at
most one. This proves the lemma. ∎

## Machine check

`symbolic_every_pair_check.py` reconstructs the five trunk expressions for all
six pairs, checks the convex-combination identities exactly, verifies the
stationary point and boundary formulas, and confirms that the directed
role-preserving automorphism group of the fixed graph is trivial.
