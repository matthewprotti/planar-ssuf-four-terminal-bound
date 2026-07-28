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
route-cost, all-pairs-feasible regime. This directory studies full-demand route-cost differences on the same topology.
The unresolved optimization frontier is now entirely in the strictly positive
lane; signed and zero strata are treated separately below.

The first adversarial referee independently reproduced the complete finite
census and reconstructed the every-pair theorem, but required the theorem to be
self-contained. The second-round revision made that dependency local and auditable. This forward pass adds new exact reductions and witnesses without declaring referee acceptance.

## One master objective

`MASTER_OBJECTIVE_AND_COST_REALIZATION.md` defines the common normalized
fixed-topology objective

\[
\Phi(k,p,d)
=
\frac1{d_{\max}}
\min_{\substack{z\in\{0,1\}^4\\k\cdot(z-p)\ge0}}
\max_a\Delta_a(z;p,d).
\]

Every exact-value statement in this directory uses this same \(\Phi\).
Moreover, every signed vector \(k\) used by the optimization is realized on
the fixed graph by nonnegative, commodity-independent arc costs: charge only
the path-private terminal arc on the E route when \(k_i\ge0\), and only the
corresponding C-route arc when \(k_i<0\). This establishes physical legality;
it is not an optimizer or global-sharpness claim.

## Cost-difference reduction

Let \(b_i\) and \(e_i^{\mathrm{cost}}\) be terminal \(i\)'s full-demand C- and
E-route costs under the arc-cost vector, and put

\[
k_i=e_i^{\mathrm{cost}}-b_i.
\]

For fractional C fraction \(p_i\) and unsplittable C set \(S\), common baselines
cancel and

\[
C(S)\le C(x)
\quad\Longleftrightarrow\quad
k(S)\ge k\cdot p.
\]

Thus feasible C sets form a positive weighted-threshold family when \(k_i>0\)
for every \(i\). Negative coordinates become positive after an oriented
coordinate complement at the feasibility level, while zero coordinates are
genuine boundaries. UC-018 solves \(\Phi\) on every non-all-positive nonzero
sign/zero stratum, and UC-019 solves the all-zero stratum.

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
- 94 labeled cells remained after the original singleton/every-pair reduction.

The 94 cells form 15 orbits under arbitrary relabeling, but the directed fixed
graph has only the identity role-preserving automorphism. They are formal
optimization units. UC-013 eliminates five no-pair cells, UC-017 resolves all
11 single-generator positive cells (six beyond UC-013), and UC-023 resolves
four positive three-pair clique cells. The current strictly positive frontier
is therefore **79 labeled cells in 11 abstract-label search orbits**.

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

### UC-009 — initial 94-cell census remainder

After UC-006 and UC-008, 94 labeled cells initially remained in 15 arbitrary-label orbits.
The orbit count is not an objective-symmetry reduction.

### UC-010 — release-family equivalence

The local lower family matches the pinned release extraction componentwise.

### UC-011 — exact algebra corroboration

Two exact arithmetic paths corroborate the local identities used in UC-008.

### UC-012 — no-pair scalar lemma

No feasible pair forces `sum p_i>2`.

### UC-013 — five no-pair cells are at most one

The full-only and four exactly-one-triple cells have value at most one, reducing
the positive remainder from 94 to 89.

### UC-014 — exact interior witnesses above one

Ten current strictly positive open cells have exact rational interior lower
witnesses above one. The strongest current certificate is F060 at
`28085483/25000000 = 1.12341932`; every retained point has a positive strict
losing margin and has been checked on every feasible route and every arc.
F042's earlier certificate remains historical evidence, but UC-023 now solves
that cell, so it is absent from the current atlas and count.

### UC-015 — signed nonzero feasibility census

There are 1,881 unique labeled unate threshold families across nonzero sign
patterns.

### UC-016 — zero boundary of the solved cell

The solved every-pair/no-singleton cell has no zero-difference point in its
nonnegative closure.


### UC-017 — signed single-generator value one

Every sign-oriented threshold cell with one minimal generator of size at least
two has exact value one. This covers 176 nonzero sign/generator regimes and
zeros outside the generator. In the strictly positive lane it resolves all 11
single-generator cells and produced the historical 89-to-83 reduction; after
UC-023, the current frontier is 79 cells.

### UC-018 — all non-all-positive strata are below `L`

Every nonzero sign/zero stratum outside the strictly all-positive lane has exact
value one or `9/8`. The `9/8` cases are precisely the three-positive chain
placements with terminal 2, 3, or 4 nonpositive. Since `9/8<L`, no signed or
zero-boundary stratum can improve the released value.

### UC-019 — exact cost-free value `4/5`

When every cost difference is zero, all routes are feasible and the exact value
is `4/5`. The upper routing chooses C exactly when `d_i p_i>4/5`; every chosen
C terminal then contributes less than `1/5` on the trunk, while every E terminal
has private deviation at most `4/5`. The symmetric `p_i=4/5`, unit-demand
instance gives the matching lower bound.

### UC-023 — exact positive three-pair clique cells

If the three pair generators are exactly the pairs of one terminal triple, the
cell has exact value `9/8` when the omitted terminal is 2, 3, or 4 and exact
value one when it is terminal 1. This resolves four more positive cells and one
full abstract-label orbit.

### UC-020 — all 79 remaining positive cells are bounded by \(L\)

Open main conjecture for the 79 remaining strictly positive cells.

### UC-021 — a remaining positive cell exceeds `L`

Open alternative: an exact witness above `L` in one of the 79 remaining strictly positive cells.

### UC-022 — arbitrary signed/zero reduction

Any fixed-topology obstruction above `L` must now lie in the 79 strictly
positive cells. All other nonzero sign/zero strata are at most `9/8`, and the
all-zero stratum has exact value `4/5`.

### UC-030 — structural replacement for cellwise optimization

Open target; numerical scouting alone cannot establish it.

## Run the complete gate

```bash
cd research/unequal_cost_fixed_topology
python round2_replay.py
python replay_determinism_test.py
```

Both commands are check-only by default. Generated JSON result files are
created in disposable copies, and the replay byte-compares their deterministic
summary with the committed `round2_replay_report.json`. The two-root test also
checks the root SHA-256 manifest and deterministic source-archive membership.
`artifact_manifest.json` hashes the committed research sources and records the
exact released provenance pin. See `REPRODUCIBILITY.md` for the canonical versus
noncanonical attestation boundary.

## Nonclaims

This branch does not prove global arbitrary-cost fixed-topology sharpness,
four-terminal optimality, the exact unrestricted planar constant, novelty,
independent human verification, or peer review. It does not alter the immutable
release.


## Forward-pass mathematical advances

### No-pair reduction

`NO_PAIR_SCALAR_LEMMAS.md` proves that no feasible pair forces
`sum p_i > 2`. It also proves that the full-set-only cell and the four cells
with exactly one feasible triple have value at most 1. The unresolved positive-
difference remainder is therefore reduced from 94 to **89 labeled cells**.

### Exact lower-witness atlas inside the positive frontier

`exact_open_cell_witnesses.py` now gives strict rational interior certificates
in ten current open labeled cells. The strongest are

- F060: `28085483/25000000 = 1.12341932`;
- F055: `5509335803/5000000000 = 1.1018671606`;
- F061: `88144229/80000000 = 1.1018028625`.

Seven further current exact certificates are recorded in
`EXACT_OPEN_CELL_WITNESSES.md` and `exact_open_cell_witnesses.json`. These are
cell lower bounds rather than optima; all remain below `L`. The F060 point has
strict losing margin `13/5000000`, so it lies inside the named cell rather than
only on its closure. F042's earlier `1111291/1000000` certificate is retained
there as historical evidence, outside the generated current atlas, because
UC-023 proves the exact F042 cell value `9/8`.

### Nonzero signed differences

`SIGNED_DIFFERENCE_REDUCTION.md` proves that complementing every negative-cost
coordinate converts cost feasibility to a positive threshold family. The exact
four-label census contains **1,881 unique labeled unate threshold families**
across all nonzero sign patterns. This is a feasibility classification only:
the physical path-difference objective must also be sign-oriented.

### Zero boundary of the solved cell

`ZERO_BOUNDARY_EVERY_PAIR.md` proves that the every-pair/no-singleton cell cannot
contain a zero cost-difference coordinate in its nonnegative closure. Thus the
exact value `L` already covers that cell's complete nonnegative closure.


### Positive three-pair clique theorem

`POSITIVE_THREE_PAIR_CLIQUE_THEOREM.md` resolves the four cells generated by all
three pairs of a fixed terminal triple. Three chain placements have exact value
`9/8`; the nested placement has exact value one. The open strictly positive
frontier is therefore **79 labeled cells in 11 abstract-label orbits**.

## Current frontier

The main positive-difference question is now 79 labeled cells, not 94. The
non-all-positive signed/zero objective is fully solved: the all-zero stratum has
exact value `4/5`, and no such stratum can exceed `L`.


### Signed single-generator theorem

`SIGNED_SINGLE_GENERATOR_THEOREM.md` proves exact value one for every unique
oriented-generator stratum and supplies exact checks for 176 sign-pattern/
generator regimes.

### Complete non-all-positive theorem

`NONPOSITIVE_DIFFERENCE_THEOREM.md` classifies all 79 nonzero, non-all-positive
sign/zero patterns: six chain placements have value `9/8`, and the other 73
have value one. A structurally separate finite grid checks 31,995 exact rational
cases.

### Cost-free stratum

`COST_FREE_STRATUM.md` proves the exact value `beta_0=4/5`.
