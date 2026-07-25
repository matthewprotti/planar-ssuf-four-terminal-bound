# Unequal-Cost Fixed-Topology SSUF Research Work Package

**Status:** adversarial revision on a follow-on research branch. The immutable
`v0.1.0` disclosure is unchanged.

**Started:** 24 July 2026  
**Adversarial revision:** 24 July 2026

## Purpose

The released paper proves

\[
L=\frac{299-41\sqrt{41}}{32}
\]

is the exact supremum on the fixed four-terminal topology in the equal full-
route-cost, all-pairs-feasible regime. This directory studies arbitrary
**positive full-demand route-cost differences** on the same topology.

The first adversarial referee independently reproduced the complete finite
census and reconstructed the every-pair theorem, but required the theorem to be
self-contained. This revision closes that dependency gap and adds clean-room
and symbolic replays.

## Cost-difference reduction

Let \(b_i\) and \(e_i^{\mathrm{cost}}\) be terminal \(i\)'s full-demand C- and
E-route costs under the arc-cost vector, and assume

\[
k_i=e_i^{\mathrm{cost}}-b_i>0.
\]

For fractional C fraction \(p_i\) and unsplittable C set \(S\), common baselines
cancel and

\[
C(S)\le C(x)
\quad\Longleftrightarrow\quad
k(S)\ge k\cdot p.
\]

Thus feasible C sets form a positive weighted-threshold family. Zero
differences require separate weak-degeneracy handling; negative differences
are not upward monotone and are outside this branch.

Conversely, any positive threshold family with
\(0\le\tau\le\sum_i k_i\) can be realized at the discrete feasibility level by
setting every \(p_i=\tau/\sum_jk_j\). This does not identify an optimizer within
that cell.

## Exact four-label census

`threshold_family_census.py` enumerates all 168 labeled monotone families on
four labels and gives:

- 149 positive threshold families;
- a positive integer witness with maximum weight at most 4 for each;
- 18 nonempty nonthreshold families, each with an exact two-trade;
- one impossible empty family; and
- 26 arbitrary-label permutation orbits among the realizable families.

The weight bound is an existence result, not a claim that the stored witness is
unique, minimum-sum, or canonical. `independent_census_check.py` reconstructs
the classification without importing the generator and searches every integer
quota from zero through the total weight.

## Fixed-topology lemmas

`FIXED_TOPOLOGY_APPENDIX.md` restates the graph, paths, four trunk supports,
private-arc bounds, and six exact pair maxima.

A feasible singleton gives a routing with maximum upper deviation at most one:
route only that terminal on C. It is the only possible positive contributor on
its trunk support, while all positive private-arc deviations are at most
\(d_i\le1\).

`FIXED_SUPPORT_ROUTING_LEMMA.md` proves, without any cost assumption, that if

\[
1<\sum_i p_i\le2
\]

and all six exactly-two-cheap routings are available, one of them has maximum
upper deviation at most \(L\).

## Every-pair theorem

If every pair is feasible and no singleton is feasible, sorting the paired
coordinates \((k_i,p_i)\) for the scalar calculation gives

\[
1<\sum_i p_i\le2.
\]

The local fixed-support lemma supplies the upper bound. The equal positive-
difference family is restated inside `EVERY_PAIR_CELL_THEOREM.md` and approaches
\(L\), giving the lower bound. Hence the exact supremum on this full unequal-
cost cell remains \(L\).

The theorem no longer imports an unexpanded released proof. Release `v0.1.0`
is pinned only as provenance in `DEPENDENCY_MANIFEST.json`.

## Reduced search space

Among the 149 positive threshold families:

- 54 contain a feasible singleton and have value at most one;
- one no-singleton/every-pair family has exact supremum \(L\); and
- 94 labeled cells remain possible locations of an improvement.

The 94 cells form 15 orbits under arbitrary relabeling, but the directed fixed
graph has only the identity role-preserving automorphism. All 94 labeled cells
remain formal optimization units.

Strict losing inequalities make these open cells. Future optimization must
separate the strict cell, its closure, and boundary families, and must separate
positive demand from a zero-demand closure. See `CELL_OPTIMIZATION_PROTOCOL.md`.

## Claim map

### UC-001 — positive route-cost-difference threshold reduction

Cost feasibility is exactly a positive weighted-threshold inequality when every
full-demand E-minus-C difference is positive.

### UC-002 — discrete converse realization

Every positive threshold family in the admissible threshold interval has valid
cheap fractions; this is not an optimizer claim.

### UC-003 — exact 168/149 census

Exactly 149 of the 168 labeled monotone four-label families are positive
threshold families.

### UC-004 — small integer witness existence

Each realizable family has at least one positive integer representation with
maximum weight at most four.

### UC-005 — exact exclusions

All 18 nonempty excluded families have exact two-trade contradictions, and the
empty family is impossible because the full C set is always feasible.

### UC-006 — feasible-singleton bound

Any cell containing a singleton has an available routing with maximum upper
deviation at most one.

### UC-007 — every-pair scalar lemma

Every-pair feasibility plus singleton infeasibility implies
\(1<\sum_i p_i\le2\).

### UC-008 — exact value of the every-pair cell

The self-contained fixed-support lemma and lower family prove exact supremum
\(L\) for arbitrary positive route-cost differences in this cell.

### UC-009 — 94 labeled cells remain

After UC-006 and UC-008, 94 labeled cells in 15 arbitrary-label orbits remain.
The orbit count is not an objective-symmetry reduction.

### UC-020 — all remaining cells are bounded by \(L\)

Open main conjecture.

### UC-021 — arbitrary positive differences do not improve the topology

Open flagship target, equivalent to resolving the remaining cells.

### UC-030 — a remaining cell yields a larger exact obstruction

Open alternative target; numerical scouting alone cannot establish it.

## Run the complete gate

```bash
cd research/unequal_cost_fixed_topology
python threshold_family_census.py
python independent_census_check.py
python symbolic_every_pair_check.py
python validate_artifacts.py
python build_artifact_manifest.py --check
```

Generated JSON result files are ignored by Git. `artifact_manifest.json` hashes
the committed research sources and records the exact released provenance pin.

## Nonclaims

This branch does not prove global arbitrary-cost fixed-topology sharpness,
four-terminal optimality, the exact unrestricted planar constant, novelty,
independent human verification, or peer review. It does not alter the immutable
release.
