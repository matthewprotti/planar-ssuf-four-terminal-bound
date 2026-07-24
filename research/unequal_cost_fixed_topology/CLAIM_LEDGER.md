# Claim Ledger — Unequal-Cost Fixed-Topology SSUF

Last updated: 24 July 2026

| ID | Claim | Status | Evidence | Non-claim / next gate |
| --- | --- | --- | --- | --- |
| UC-001 | With full expensive-route costs \(k_i>0\), a cheap set \(S\) is cost feasible exactly when \(k(S)\ge k\cdot p\). | Proved algebraic reduction | `README.md` | Does not solve the continuous optimization within a threshold cell. |
| UC-002 | Every positive threshold family with threshold in \([0,\sum_i k_i]\) is realizable by valid cheap fractions. | Proved converse | Set all \(p_i=\tau/\sum_i k_i\) | The optimizing \(p\) need not be uniform. |
| UC-003 | Of the 168 labeled monotone families on four terminals, exactly 149 are realizable positive threshold families. | Exact finite census | `threshold_family_census.py`, `threshold_family_census.json` | Unrefereed; separate reimplementation pending. |
| UC-004 | Every realizable family has an integer witness with maximum weight at most 4. | Exact finite certificate | 149 recorded witness rows | This is a four-label statement only. |
| UC-005 | Each of the 18 nonempty nonthreshold families has an exact two-trade contradiction; the remaining empty family is impossible because the full set is feasible. | Exact finite certificates plus one-line proof | 18 recorded trades; empty-family certificate | Independent generator/checker pending. |
| UC-006 | Any feasibility family containing a singleton has an available routing with maximum upper deviation at most 1. | Proved lemma | `README.md` | Does not identify its exact optimum. |
| UC-007 | If every pair is feasible and no singleton is feasible, then \(1<\sum_i p_i\le2\). | Proved lemma | `EVERY_PAIR_CELL_THEOREM.md` | Depends on positive full-route costs. |
| UC-008 | The exact supremum on the arbitrary-cost every-pair/no-singleton cell is \(L=(299-41\sqrt{41})/32\). | Proved follow-on theorem, unrefereed | `EVERY_PAIR_CELL_THEOREM.md` plus released restricted-model proof/family | Requires independent reconstruction and review of the dependency on the released proof. |
| UC-009 | After UC-006 and UC-008, 94 labeled threshold cells in 15 permutation orbits remain as possible locations of an improvement over \(L\). | Exact finite classification | Census JSON statuses and orbit representatives | Permutation orbits are search organizers, not graph-objective symmetries. |
| UC-020 | Every remaining cell has supremum at most \(L\). | Open main conjecture | No proof | A counterexample above \(L\) remains possible. |
| UC-021 | Arbitrary positive full-route costs do not improve the fixed-topology supremum. | Open flagship target | Equivalent to resolving the remaining cells | Not claimed. |
| UC-030 | One remaining cell yields a larger exact algebraic lower bound. | Open alternative target | Numerical scouting is discovery-only | No candidate is currently certified. |

## Standing non-claims

This branch does not change or supersede the immutable `v0.1.0` disclosure.  It
does not prove arbitrary-cost fixed-topology sharpness, four-terminal global
optimality, the exact unrestricted planar constant, novelty, independent human
verification, or peer review.
