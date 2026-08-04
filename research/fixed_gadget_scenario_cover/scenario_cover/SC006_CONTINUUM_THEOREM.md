# SC-006 — Exact Two-Scenario \(\kappa\)-Phase on the RB Family

**Date:** 2026-08-01  
**Posture:** narrow internal theorem accepted by R3C with the nonblocking
editorial repairs applied in this derived copy; corroborated by the nonblind
R3D exact replay.  
**Scope:** the fixed four-terminal support gadget, the one-parameter RB family,
two **positive** cost-difference scenarios, and condition number at most
\(\kappa\). This note does not claim the global bounded-\(\kappa\) curve.

## 1. Setup

A routing is encoded by its C-set \(S\subseteq[4]\). Put

\[
a:=\frac14+\varepsilon,
\qquad
p_\varepsilon=\left(a,\varepsilon,\frac12,a\right),
\qquad
0<\varepsilon<\frac18,
\]

and

\[
d=\left(1,1,\frac34,1\right).
\]

The five trunk supports are

\[
P_1=\{0,1,2\},\quad
P_2=\{0,1,2,3,4\},\quad
P_3=\{1,2,3,4\},\quad
P_4=\{2,3\}.
\]

Each terminal also has its two private arcs, giving thirteen arcs in total.
For a C-set \(S\), let \(M(S;p_\varepsilon,d)\) be the maximum positive arc
deviation of the corresponding unsplittable routing from the fractional flow.

Writing \(x_i=\mathbf 1_{\{i\in S\}}\), the five trunk deviations are

\[
\begin{aligned}
D_0&=x_1+x_2-\frac14-2\varepsilon,\\
D_1&=x_1+x_2+\frac34x_3-\frac58-2\varepsilon,\\
D_2&=x_1+x_2+\frac34x_3+x_4-\frac78-3\varepsilon,\\
D_3&=x_2+\frac34x_3+x_4-\frac58-2\varepsilon,\\
D_4&=x_2+\frac34x_3-\frac38-\varepsilon.
\end{aligned}
\]

For terminal \(i\), the ordered deviations on its two private arcs are

\[
i\in S:\ \bigl(-d_i(1-p_i),\,d_i(1-p_i)\bigr),
\qquad
i\notin S:\ \bigl(d_ip_i,\,-d_ip_i\bigr).
\]

A positive cost-difference scenario is \(k=(k_1,k_2,k_3,k_4)>0\). Write

\[
T(k):=k\cdot p_\varepsilon
=a(k_1+k_4)+\varepsilon k_2+\frac12k_3.
\]

The route \(S\) is cost-nonincreasing exactly when

\[
k(S)\ge T(k),
\]

and is eliminated exactly when

\[
k(S)<T(k).
\tag{1}
\]

The condition number is

\[
\chi(k):=\frac{\max_i k_i}{\min_i k_i}.
\]

For two scenarios define

\[
\Psi_{2,\kappa}(p_\varepsilon,d)
:=
\sup_{\substack{k^{(1)},k^{(2)}>0\\
\chi(k^{(1)}),\chi(k^{(2)})\le\kappa}}
\min_{\substack{S\subseteq[4]\\
k^{(j)}(S)\ge T(k^{(j)}),\ j=1,2}}
M(S;p_\varepsilon,d).
\tag{2}
\]

The all-C route is feasible in every positive scenario, so the inner minimum
is always defined.

Set

\[
A(\varepsilon)=\frac{3-4\varepsilon}{1+2\varepsilon},\qquad
B(\varepsilon)=\frac1\varepsilon-2,\qquad
C(\varepsilon)=\frac2\varepsilon-2.
\tag{3}
\]

On \(0<\varepsilon<1/8\),

\[
1<A(\varepsilon)<B(\varepsilon)<C(\varepsilon),
\]

because

\[
A-1=\frac{2(1-3\varepsilon)}{1+2\varepsilon},\quad
B-A=\frac{1-3\varepsilon}{\varepsilon(1+2\varepsilon)},\quad
C-B=\frac1\varepsilon.
\]

## 2. Exact route table

Direct reconstruction on the five trunk arcs and eight private arcs gives:

| C-set \(S\) | \(M(S;p_\varepsilon,d)\) |
|---|---:|
| \(\varnothing,3\) | \(3/8\) |
| \(1,4\) | \(3/4-\varepsilon\) |
| \(2\) | \(1-\varepsilon\) |
| \(14\) | \(9/8-3\varepsilon\) |
| \(13,34\) | \(9/8-2\varepsilon\) |
| \(24\) | \(11/8-2\varepsilon\) |
| \(23\) | \(11/8-\varepsilon\) |
| \(12\) | \(7/4-2\varepsilon\) |
| \(134\) | \(15/8-3\varepsilon\) |
| \(124\) | \(17/8-3\varepsilon\) |
| \(123,234\) | \(17/8-2\varepsilon\) |
| \(1234\) | \(23/8-3\varepsilon\) |

The only route-order crossing inside the parameter interval is

\[
M(2)=M(14)
\quad\Longleftrightarrow\quad
\varepsilon=\frac1{16}.
\]

This crossing changes \(\mathcal G_{<r_0}\): route \(2\) is below, equal to,
or above \(r_0=M(14)\) as \(\varepsilon\) is below, equal to, or above
\(1/16\). It does not change any of the \(r_1,r_2,r_3\) filtrations used
below, and it does not affect the \(r_0\) argument because the equal scenario
eliminates every singleton throughout the interval. At the excluded endpoint
\(\varepsilon=1/8\), both collision classes are

\[
M(2)=M(13)=M(34)=\frac78,
\qquad
M(12)=M(134)=\frac32.
\]

Define

\[
r_0=\frac98-3\varepsilon,\qquad
r_1=\frac98-2\varepsilon,\qquad
r_2=\frac{15}{8}-3\varepsilon,\qquad
r_3=\frac{17}{8}-3\varepsilon.
\tag{4}
\]

The routes strictly below \(r_1\) are exactly the empty set, the four
singletons, and \(14\). The routes strictly below \(r_2\) are exactly the
sets of cardinality at most two. The routes strictly below \(r_3\) are
exactly the sets of cardinality at most two together with \(134\).

## 3. The theorem

For every \(0<\varepsilon<1/8\) and every \(\kappa\ge1\),

\[
\boxed{
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
\end{cases}}
\tag{5}
\]

The three transition points belong to the lower branch. The newly required
route ties the scenario budget at the breakpoint and is therefore feasible;
elimination in (1) is strict.

## 4. The first transition: \(A(\varepsilon)\)

### 4.1 Construction above \(A\)

The equal scenario

\[
k^{(0)}=(1,1,1,1)
\]

has threshold \(T(k^{(0)})=1+3\varepsilon\), strictly between \(1\) and
\(2\). It eliminates the empty set and every singleton. In particular, it
covers every route strictly below \(r_0\).

For

\[
k^{(A)}=(1,\kappa,\kappa,1),
\]

we have

\[
T(k^{(A)})-k^{(A)}(14)
=\left(\frac12+\varepsilon\right)
\bigl(\kappa-A(\varepsilon)\bigr).
\tag{6}
\]

Thus \(14\) is eliminated when \(\kappa>A(\varepsilon)\). The two scenarios
cover every route below \(r_1\), proving
\(\Psi_{2,\kappa}\ge r_1\) above \(A\).

### 4.2 Obstruction at and below \(A\)

Let \(m=\min_i k_i\) and suppose \(\chi(k)\le\kappa\). Then

\[
\begin{aligned}
T(k)-k(14)
&=\varepsilon k_2+\frac12k_3
-\left(\frac34-\varepsilon\right)(k_1+k_4)\\
&\le
\left(\frac12+\varepsilon\right)\kappa m
-2\left(\frac34-\varepsilon\right)m\\
&=
\left(\frac12+\varepsilon\right)
\bigl(\kappa-A(\varepsilon)\bigr)m.
\end{aligned}
\tag{7}
\]

No \(\kappa\)-bounded scenario eliminates \(14\) when \(\kappa\le A\).
Any value strictly above \(r_0=M(14)\) would require eliminating \(14\), so
the robust value is at most \(r_0\). The equal scenario gives the matching
lower bound. At \(\kappa=A\), route \(14\) ties and remains feasible.

## 5. The middle transition: \(B(\varepsilon)\)

The key step is a three-route pigeonhole argument rather than a symbolic
enumeration of all route partitions.

### 5.1 Two outer pairs force condition number \(>B\)

Call \(13,14,34\) the three outer pairs. Suppose one scenario eliminates any
two of them. Adding the two strict losing inequalities gives one of

\[
\begin{array}{c|c}
\text{eliminated pairs}&\text{consequence}\\
\hline
13,14&
2\varepsilon k_2>
\left(\frac32-2\varepsilon\right)k_1+
\left(\frac12-2\varepsilon\right)k_4\\[1mm]
13,34&
2\varepsilon k_2>
\left(\frac12-2\varepsilon\right)(k_1+k_4)+k_3\\[1mm]
14,34&
2\varepsilon k_2>
\left(\frac12-2\varepsilon\right)k_1+
\left(\frac32-2\varepsilon\right)k_4.
\end{array}
\tag{8}
\]

Every displayed coefficient is nonnegative on \(0<\varepsilon<1/8\), and
the coefficients in each row sum to \(2-4\varepsilon\). Hence

\[
2\varepsilon k_2>2(1-2\varepsilon)m,
\]

so

\[
\chi(k)\ge\frac{k_2}{m}>
\frac{1-2\varepsilon}{\varepsilon}
=B(\varepsilon).
\tag{9}
\]

Therefore a scenario of condition number at most \(B\) eliminates at most one
of the three outer pairs.

### 5.2 Upper bound through \(B\)

A value strictly above \(r_1\) requires eliminating all three routes
\(13,14,34\). Two scenarios covering three routes force one scenario, by the
pigeonhole principle, to eliminate at least two. Equation (9) rules this out
for \(\kappa\le B\). Hence \(\Psi_{2,\kappa}\le r_1\) through the
breakpoint.

### 5.3 Construction above \(B\)

Use

\[
k^\triangle=(1,\kappa,1,1),
\qquad
k^\star=(\kappa,1,\kappa,\kappa).
\tag{10}
\]

For the first scenario,

\[
T(k^\triangle)-2
=\varepsilon\bigl(\kappa-B(\varepsilon)\bigr),
\tag{11}
\]

so every outer pair is eliminated when \(\kappa>B\).

For the second scenario, each pair incident with terminal \(2\) has weight
\(1+\kappa\), while

\[
T(k^\star)-(1+\kappa)
=2\varepsilon\kappa+\varepsilon-1.
\tag{12}
\]

Moreover,

\[
B(\varepsilon)-\frac{1-\varepsilon}{2\varepsilon}
=\frac{1-3\varepsilon}{2\varepsilon}>0.
\]

Thus \(\kappa>B\) makes (12) positive, and \(k^\star\) eliminates
\(12,23,24\). The two scenarios cover every pair and, by down-closure, every
set of cardinality at most two. They force value at least \(r_2\). At
\(\kappa=B\), the outer pairs tie under \(k^\triangle\), so the new branch is
not attained.

## 6. The third transition: \(C(\varepsilon)\)

### 6.1 Obstruction at and below \(C\)

For any scenario of condition number at most \(\kappa\),

\[
\begin{aligned}
T(k)-k(134)
&=\varepsilon k_2
-\left(\frac34-\varepsilon\right)(k_1+k_4)
-\frac12k_3\\
&\le\varepsilon\kappa m-(2-2\varepsilon)m\\
&=\varepsilon\bigl(\kappa-C(\varepsilon)\bigr)m.
\end{aligned}
\tag{13}
\]

No scenario eliminates \(134\) when \(\kappa\le C\). A value strictly above
\(r_2=M(134)\) is therefore impossible.

### 6.2 Construction above \(C\)

Retain the scenarios in (10). Now

\[
T(k^\triangle)-k^\triangle(134)
=T(k^\triangle)-3
=\varepsilon\bigl(\kappa-C(\varepsilon)\bigr)>0.
\tag{14}
\]

Thus \(k^\triangle\) eliminates \(134\), as well as the outer pairs, while
\(k^\star\) eliminates the three pairs incident with terminal \(2\). Their
union covers every route below \(r_3\), proving the fourth lower branch. At
\(\kappa=C\), \(134\) ties and remains feasible.

## 7. No two positive scenarios can exceed \(r_3\)

A value strictly above \(r_3\) would require covering, among other routes,

\[
134,\qquad124,\qquad23.
\]

First, one scenario cannot eliminate both triples, because

\[
\begin{aligned}
&\bigl(T-k(134)\bigr)+\bigl(T-k(124)\bigr)\\
&\quad=
\left(-\frac32+2\varepsilon\right)(k_1+k_4)
+(2\varepsilon-1)k_2<0.
\end{aligned}
\tag{15}
\]

Second, if a scenario eliminates \(134\), then

\[
\varepsilon k_2>
\left(\frac34-\varepsilon\right)(k_1+k_4)+\frac12k_3.
\]

Since \(1-\varepsilon>\varepsilon\) and
\(3/4-\varepsilon>1/4+\varepsilon\), this implies

\[
k_2>T(k).
\tag{16}
\]

Every set containing terminal \(2\), in particular \(23\), is accepted by
that scenario.

Likewise, if a scenario eliminates \(124\), then

\[
\frac12k_3>
\left(\frac34-\varepsilon\right)(k_1+k_4)
+(1-\varepsilon)k_2
>
\left(\frac14+\varepsilon\right)(k_1+k_4)+\varepsilon k_2,
\]

so

\[
k_3>T(k).
\tag{17}
\]

That scenario also accepts \(23\).

By (15), two scenarios covering the two triples must use one scenario for
\(134\) and the other for \(124\). Equations (16) and (17) say both scenarios
then accept \(23\), leaving it uncovered. This contradiction is independent
of \(\kappa\), so \(r_3\) is the unrestricted two-scenario value throughout
the RB family.

## 8. Endpoint and scope ledger

- Losing routes use the strict inequality \(k(S)<T(k)\).
- At \(A,B,C\), the newly required route ties rather than loses.
- The parameter endpoint \(\varepsilon=1/8\) is excluded. There
  \(M(12)=M(134)\), so the route-level filtration changes.
- Positivity of all four scenario coefficients is used essentially.
- No statement is made about signed scenarios, zero coefficients, more than
  two scenarios, another support topology, or the global bounded-\(\kappa\)
  supremum.
- The proof uses scenario-cover duality but does not rely on the 168-downset
  atlas for correctness. The atlas is retained as an independent finite
  cross-check.
