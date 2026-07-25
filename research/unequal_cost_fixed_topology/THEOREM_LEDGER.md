# Formal Theorem and Evidence Ledger — Positive-Difference Fixed-Topology SSUF

SSUF means **single-source unsplittable flow**. “Unequal cost” in this workstream
always means unequal **positive expensive-minus-cheap full-route cost
differences** unless a wider domain is expressly stated.

| ID | Full statement | Evidence class | Assumptions | Proof / replay location | Computation dependency / residual limitation |
| --- | --- | --- | --- | --- | --- |
| UC-001 | If terminal \(i\) has full-demand cheap-route cost \(b_i\), expensive-route cost \(e_i\), and \(k_i=e_i-b_i>0\), then a cheap set \(S\) is cost-nonincreasing iff \(k(S)\ge k\cdot p\). | Human-proved algebraic lemma | Fixed two-route topology; \(k_i>0\) | `EVERY_PAIR_CELL_THEOREM.md` “Cost-difference reduction” | Zero and negative differences are not normalized away and are excluded. |
| UC-002 | Every positive weighted-threshold family with \(0\le\tau\le\sum_i k_i\) is realizable by valid cheap fractions, e.g. uniform \(p_i=\tau/\sum_jk_j\). | Human-proved realization lemma | Positive weights; discrete feasibility family only | `README.md`; census documentation | Does not produce an overload optimizer. |
| UC-003 | There are 168 labeled monotone families on four terminals, of which exactly 149 are positive threshold families. | Exact finite machine proposition; separate reimplementation | Four labeled terminals; weak threshold feasibility | `threshold_family_census.py`; `independent_census_check.py` | Classical classification is not claimed as novel. |
| UC-004 | Every one of the 149 realizable families has at least one positive integer representation with maximum weight at most 4. | Exact finite existence proposition | Search domain certified complete for bound 4 | Same census files | Witnesses are not unique, canonical, or minimum-sum. |
| UC-005 | The remaining 18 nonempty monotone families have exact two-trade contradictions; the empty family is impossible because the full set is feasible. | Exact finite certificates | Positive weak threshold representation | Census JSON and independent checker | Two-trade discovery is finite computation. |
| UC-006 | If a singleton cheap set is feasible, a cost-feasible routing has maximum upper deviation at most 1. | Human-proved fixed-support lemma | Normalized \(d_{\max}=1\); local topology | `FIXED_TOPOLOGY_APPENDIX.md`; `README.md` | Fixed topology only. |
| UC-007 | If every pair is feasible and no singleton is feasible, then \(1<\sum_i p_i\le2\). | Human-proved scalar lemma | Paired-coordinate sorting; \(k_i>0\) | `EVERY_PAIR_CELL_THEOREM.md` “Upper bound” | Sorting is not a graph symmetry. |
| UC-008 | On the fixed topology, within the positive-difference cell where every pair is feasible and no singleton is feasible, the exact supremum is \(L=(299-41\sqrt{41})/32\). | Human-proved theorem; exact algebra corroboration | \(d_i\in(0,1]\), \(\max d_i=1\), \(p_i\in[0,1]\), all six pairs available, \(k_i>0\) | `FIXED_SUPPORT_ROUTING_LEMMA.md`; `EVERY_PAIR_CELL_THEOREM.md` | No claim for all 149 cells or for zero/negative differences. |
| UC-009 | Of the 149 threshold families, 54 contain a feasible singleton, 1 is the every-pair/no-singleton cell, and 94 remain; the 94 form 15 orbits under arbitrary-label \(S_4\). | Exact finite classification | Labeled families; arbitrary-label action only | `CENSUS_RECONCILIATION.md`; census JSON | All 94 labeled cells remain formal optimization units. |
| UC-010 | The locally restated lower family is componentwise identical to the pinned extraction from release `v0.1.0`. | Exact definition comparison plus human-auditable provenance pin | Pinned release extraction | `LOWER_FAMILY_EQUIVALENCE.md`; `release_family_equivalence_check.py` | Extraction from TeX is not reparsed at runtime. |
| UC-011 | The exact algebra audit reproduces the pair expressions, convex identities, lower-family identities, stationary point, and algebraic-number value used as corroboration for UC-008. | Exact algebraic corroboration | Rational Laurent-polynomial arithmetic and \(\mathbb Q(\sqrt{41})\); formulas stated in local theorem | `exact_algebra_audit.py`; `SYMBOLIC_TRUST_AND_ASSUMPTIONS.md` | Does not establish the human proof’s unstated logical case split or branch conditions. |
| UC-020 | Every one of the 94 remaining labeled positive-difference cells has value at most \(L\). | Open target | Exact cell/closure discipline | `CELL_OPTIMIZATION_PROTOCOL.md` | Open. |
| UC-021 | Some remaining labeled cell has an exact value exceeding \(L\). | Open alternative | Exact interior witness required | `CELL_OPTIMIZATION_PROTOCOL.md` | Open. |
| UC-030 | A structural fixed-topology or four-terminal theorem replaces cellwise optimization. | Open target | To be determined | `README.md` | Open. |

The strict-cell/closure protocol is methodology, not a theorem and not evidence
that the 94 remaining boundaries have been handled.
