# Unequal-Cost Fixed-Topology SSUF Research Work Package

**Status:** exact first-pass reduction and census on a research branch; the
immutable `v0.1.0` disclosure is unchanged.

**Started:** 24 July 2026

## Purpose

The released paper proves that

\[
L=\frac{299-41\sqrt{41}}{32}=1.139747070789\ldots
\]

is the exact supremum on the fixed four-terminal topology when every full
expensive choice has the same cost and cost feasibility forces at least two
cheap choices.  It deliberately leaves open the same topology with arbitrary
positive full expensive-route costs.

This directory begins that unequal-cost program with:

1. an exact reduction of cost feasibility to positive weighted threshold
   families on four labels;
2. a complete certificate census of those families;
3. an analytic theorem showing that unequal costs do not improve the value on
   the entire “every pair feasible, no singleton feasible” cell;
4. a reduced list of 94 labeled candidate cells, in 15 permutation orbits, on
   which any improvement must occur.

No claim is made yet about the unrestricted unequal-cost optimum.

## 1. Threshold-family reduction

Normalize demands so that \(0<d_i\le1\) and \(d_{\max}=1\).  Let
\(p_i\in[0,1]\) be terminal \(i\)'s fractional cheap fraction.  Give terminal
\(i\)'s full expensive route an arbitrary positive cost \(k_i\), while its
cheap route has cost zero.

The fractional cost is

\[
C(x)=\sum_{i=1}^4 k_i(1-p_i).
\]

If \(S\subseteq[4]\) is the set of terminals routed cheaply, the unsplittable
cost is

\[
C(S)=\sum_{i\notin S}k_i.
\]

Therefore

\[
C(S)\le C(x)
\quad\Longleftrightarrow\quad
\sum_{i\in S}k_i\ge \tau,
\qquad
\tau:=\sum_{i=1}^4 k_ip_i.
\]

Thus the cost-feasible cheap sets are exactly a positive weighted threshold
family

\[
\mathcal F(k,\tau)
 =\left\{S\subseteq[4]:k(S)\ge\tau\right\}.
\]

Conversely, every positive weighted threshold family with
\(0\le\tau\le\sum_i k_i\) occurs for valid cheap fractions: set

\[
p_1=p_2=p_3=p_4=\frac{\tau}{\sum_i k_i}.
\]

This converse concerns the realizability of the discrete feasibility family.
For optimization, the actual \(p_i\)'s remain coupled to \(k\) through
\(k\cdot p=\tau\).

## 2. Exact four-label census

`threshold_family_census.py` enumerates all 168 labeled monotone families on
four terminals, using antichains of the Boolean lattice.  It then:

- constructs positive integer threshold witnesses for exactly 149 families;
- proves that every realizable family has a witness with all weights at most 4;
- gives an exact two-trade impossibility certificate for each of the 18
  nonempty monotone families that is not threshold;
- excludes the remaining empty family because the full cheap set is always
  cost feasible;
- identifies 26 terminal-permutation orbits among all realizable families.

For a two-trade certificate, feasible sets \(A,B\) and infeasible sets \(C,D\)
have equal summed incidence vectors:

\[
\mathbf 1_A+\mathbf 1_B=\mathbf 1_C+\mathbf 1_D.
\]

Any threshold representation would imply

\[
k(A)+k(B)\ge2\tau
\quad\text{and}\quad
k(C)+k(D)<2\tau,
\]

but equal incidence makes the two left sides identical.  This is an exact
nonrepresentability proof, not a failure to find larger weights.

The machine-readable artifact `threshold_family_census.json` records all 149
witnesses, all 18 two-trades, stable family identifiers, and search status.

## 3. First analytic theorem: the every-pair cell remains sharp at \(L\)

### Theorem

On the released fixed topology, suppose full expensive-route costs are arbitrary
positive numbers, every two-terminal cheap set is cost feasible, and no
singleton cheap set is cost feasible.  Then the exact supremum of the minimum
maximum upper overload is

\[
L=\frac{299-41\sqrt{41}}{32}.
\]

### Proof summary

Let \(r=\sum_i p_i\), order the full costs as
\(k_1\le k_2\le k_3\le k_4\), and put \(\tau=k\cdot p\).

No singleton is feasible, so

\[
\tau>\max_i k_i.
\]

Since \(\tau\le k_4r\), this gives \(r>1\).

Every pair is feasible, in particular the pair with the two smallest costs, so

\[
\tau\le k_1+k_2.
\]

If \(r>2\), the minimum possible value of \(k\cdot p\) over
\(p\in[0,1]^4\) with coordinate sum \(r\) is obtained by filling the cheapest
coordinates first.  Hence

\[
\tau=k\cdot p
 \ge k_1+k_2+(r-2)k_3
 >k_1+k_2,
\]

with the same lower bound remaining valid when \(r>3\).  This contradicts pair
feasibility.  Therefore

\[
1<\sum_i p_i\le2.
\]

The reverse-bound proof in the released restricted-model theorem uses the cost
assumption only to know that all six exactly-two-cheap routings are feasible;
its analytic argument then depends on \(d\), \(p\), and
\(1<\sum_i p_i\le2\).  Those hypotheses have just been recovered, so that
proof gives an overload-at-most-\(L\) feasible pair here as well.

The released equal-full-cost family realizes this same feasibility cell and
approaches \(L\), proving the matching lower bound.

A full written proof is in `EVERY_PAIR_CELL_THEOREM.md`.

## 4. Two immediate eliminations

### A feasible singleton gives value at most one

If \(\{i\}\) is cost feasible, route only terminal \(i\) cheaply.  On every
trunk arc, only terminal \(i\) can contribute positively, by at most
\(d_i(1-p_i)\le1\); all other trunk contributions are nonpositive.  Positive
deviations on terminal-private arcs are also at most one.  Hence the routing's
maximum upper deviation is at most one.

Since \(L>1\), no family containing a feasible singleton can improve the
released lower bound.

### The every-pair family is already solved

Among the 149 threshold families:

- 54 contain a feasible singleton and have optimum at most one;
- one is the no-singleton/every-pair family and has exact supremum \(L\);
- 94 labeled families remain open.

The 94 candidates form 15 orbits under arbitrary terminal relabeling.  The
fixed topology is not fully symmetric under all such relabelings, so the
labeled cells remain the formal optimization units; the orbit list is a search
organizer, not an objective-equivalence claim.

## 5. Next theorem program

For each remaining family \(\mathcal F\):

1. retain exact threshold-cell constraints
   \[
   k(S)\ge k\cdot p\ (S\in\mathcal F),
   \qquad
   k(S)<k\cdot p\ (S\notin\mathcal F);
   \]
2. write the five trunk deviations for every feasible cheap set;
3. identify active piecewise-linear maxima and minimizing routings;
4. use numerical optimization only to conjecture active cells and algebraic
   candidates;
5. replace each candidate with a symbolic upper/lower certificate;
6. attempt a common convex-combination or dual argument across cells;
7. independently enumerate and replay every finite cell certificate.

The first global target is one of:

- prove all 94 cells have value at most \(L\), extending fixed-topology
  sharpness to arbitrary positive costs; or
- produce an exact unequal-cost instance with value greater than \(L\), then
  derive and prove its limiting family.

## Run the exact census

```bash
cd research/unequal_cost_fixed_topology
python threshold_family_census.py
```

The script deterministically rewrites `threshold_family_census.json` and fails
unless all counts, witnesses, trade certificates, family classifications, and
orbit counts agree.

## Repository and release boundary

This is follow-on research.  It does not modify the immutable `v0.1.0` release,
its manuscript, its hashes, or its released claims.  Any theorem found here
must pass a separate proof, verification, novelty, attribution, and release
process before it is presented as a public result.
