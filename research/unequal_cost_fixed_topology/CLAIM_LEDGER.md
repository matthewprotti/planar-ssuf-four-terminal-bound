# Claim Ledger — Unequal-Cost Fixed-Topology SSUF

Last updated: 24 July 2026, adversarial revision 2

| ID | Claim | Status | Evidence | Boundary / next gate |
| --- | --- | --- | --- | --- |
| UC-001 | If \(k_i=e_i^{\mathrm{cost}}-b_i>0\), a C set \(S\) is cost feasible exactly when \(k(S)\ge k\cdot p\). | Proved algebraic reduction | `EVERY_PAIR_CELL_THEOREM.md` | Zero/negative differences are excluded. |
| UC-002 | Every positive threshold family with threshold in \([0,\sum_i k_i]\) is realizable by valid cheap fractions. | Proved converse | uniform \(p_i=\tau/\sum_jk_j\) | Discrete feasibility only; not an optimizer. |
| UC-003 | Exactly 149 of the 168 labeled monotone four-label families are positive threshold families. | Exact finite census, clean-room reproduced | generator and independent checker | Classical threshold-game classification may overlap; no novelty claim. |
| UC-004 | Every realizable family has some positive integer witness with maximum weight at most 4. | Exact finite existence certificate | 149 stored rows, independently replayed | Not canonical, unique, minimum-sum, or claimed optimal. |
| UC-005 | Each of 18 nonempty nonthreshold families has an exact two-trade; the empty family is impossible. | Exact certificates, clean-room reproduced | census JSON and independent checker | Four-label statement only. |
| UC-006 | Any family containing a singleton has an available routing with maximum upper deviation at most 1. | Proved fixed-topology lemma | `FIXED_TOPOLOGY_APPENDIX.md` | Exact optimum not identified. |
| UC-007 | Every pair feasible and no singleton feasible imply \(1<\sum_i p_i\le2\). | Proved scalar lemma | `EVERY_PAIR_CELL_THEOREM.md` | Paired-coordinate sorting only; no graph symmetry. |
| UC-008 | The exact supremum on the arbitrary-positive-difference every-pair/no-singleton cell is \(L\). | Self-contained unrefereed theorem; symbolically reconstructed | local topology appendix, fixed-support lemma, theorem, symbolic checker | External mathematical peer review still required. |
| UC-009 | After UC-006 and UC-008, 94 labeled cells in 15 arbitrary-label orbits remain. | Exact classification, clean-room reproduced | census and symbolic automorphism check | All 94 labelings remain formal units. |
| UC-020 | Every remaining cell has supremum at most \(L\). | Open main conjecture | None | Counterexample above \(L\) remains possible. |
| UC-021 | Arbitrary positive full-route cost differences do not improve the fixed-topology supremum. | Open flagship target | Equivalent to resolving remaining cells | Not claimed. |
| UC-030 | One remaining cell yields a larger exact algebraic lower bound. | Open alternative target | Numerical scouting is discovery-only | No certified candidate. |

## Standing nonclaims

The branch does not supersede `v0.1.0`, prove global topology sharpness or the
unrestricted planar constant, or claim novelty, peer review, or independent
human verification.
