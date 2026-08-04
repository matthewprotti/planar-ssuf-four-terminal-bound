# Resource-Allocation Details for Lemmas 3 and 4

This appendix expands the short “efficiency” calculations in the main theorem. Every optimization below is a one-constraint linear allocation problem; no numerical optimizer is used.

## 1. Two outer caps and two central coordinates

Assume

\[
h_a\le\min\{q_a,\Delta\},
\qquad
h_b\le\min\{q_b,\Delta\},
\]

\[
h_c+h_d\le\Delta(q_c+q_d),
\qquad
q_a+q_b+q_c+q_d\le2,
\]

with \(0\le\Delta<1\). Put \(r=q_a+q_b\). Then

\[
h_a+h_b\le\min\{r,2\Delta\},
\qquad
q_c+q_d\le2-r.
\]

Therefore

\[
H\le f(r):=\min\{r,2\Delta\}+\Delta(2-r).
\]

For \(r\le2\Delta\), \(f(r)=2\Delta+(1-\Delta)r\) is increasing. For \(r\ge2\Delta\), \(f(r)=2\Delta+\Delta(2-r)\) is decreasing. Hence

\[
H\le f(2\Delta)=4\Delta-2\Delta^2.
\]

This is the allocation used in Lemma 3 and in the \(\Delta\ge1/2\) branches of Lemma 4 for blocked terminals 2 and 3.

## 2. Weighted resource with one blocked coordinate

Suppose the resource is

\[
q_a+q_b+q_c+2q_u\le2.
\]

A coordinate with contribution bound \(h_i\le q_i\) has efficiency one if its resource coefficient is one and efficiency one half if its resource coefficient is two. A coordinate with \(d_i\le\Delta\) has

\[
h_i=d_iq_i\le\Delta q_i,
\]

so its efficiency is \(\Delta\) when its resource coefficient is one.

### 2.1 Two unit-efficiency capped coordinates

If two ordinary coordinates have efficiency one up to contribution cap \(\Delta\), one ordinary coordinate has efficiency \(\Delta\), and the blocked coordinate has efficiency one half, then:

- for \(0\le\Delta\le1/2\), fill the two unit-efficiency caps and then the blocked coordinate:
  \[
  H\le2\Delta+\frac{2-2\Delta}{2}=1+\Delta;
  \]
- for \(1/2\le\Delta<1\), fill the two unit-efficiency caps and then the ordinary \(\Delta\)-efficient coordinate:
  \[
  H\le2\Delta+\Delta(2-2\Delta)=4\Delta-2\Delta^2.
  \]

This covers Lemma 4 with blocked terminal 2 or 3 in the non-\(h_1+h_2\) branch.

### 2.2 One unit-efficiency capped coordinate

If one ordinary coordinate has efficiency one up to cap \(\Delta\), two ordinary coordinates have efficiency \(\Delta\), and the blocked coordinate has efficiency one half, then:

- for \(0\le\Delta\le1/2\), fill the unit-efficiency cap and then the blocked coordinate:
  \[
  H\le\Delta+\frac{2-\Delta}{2}=1+\frac\Delta2;
  \]
- for \(1/2\le\Delta<1\), fill the unit-efficiency cap and then the two ordinary coordinates:
  \[
  H\le\Delta+\Delta(2-\Delta)=3\Delta-\Delta^2.
  \]

Subtracting \(\Delta\) gives \(t\le1\) in both branches. This covers the corresponding branches for blocked terminal 1 or 4.

## 3. Minimum resource needed to support a large sum

If

\[
h_a\le\min\{q_a,\Delta\},
\qquad
h_b\le\Delta q_b,
\]

and \(s=h_a+h_b>\Delta\), the least possible ordinary resource \(q_a+q_b\) is obtained by filling terminal \(a\) to its cap and then using terminal \(b\):

\[
q_a+q_b
\ge
\Delta+\frac{s-\Delta}{\Delta}.
\]

If terminal \(b\) instead has contribution efficiency one half under a double-weighted resource, then

\[
q_a+2q_b
\ge
\Delta+2(s-\Delta)=2s-\Delta.
\]

These are the only resource lower bounds involving division by \(\Delta\) in Lemmas 3 and 4. In every use, \(t>1\) and the preceding route inequalities imply \(\Delta>0\).
