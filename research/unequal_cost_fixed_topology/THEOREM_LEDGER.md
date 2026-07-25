# Formal Theorem and Evidence Ledger — Fixed-Topology SSUF

SSUF means **single-source unsplittable flow**.

| ID | Full statement | Evidence class | Assumptions | Proof / replay location | Residual limitation |
| --- | --- | --- | --- | --- | --- |
| UC-001 | With full-demand route-cost difference `k_i=expensive_i-cheap_i>0`, a cheap set `S` is cost feasible iff `k(S)>=k·p`. | Human algebraic proof | Fixed two-route topology; positive differences | `EVERY_PAIR_CELL_THEOREM.md` | Zero/negative not normalized away. |
| UC-002 | Every positive threshold family with threshold in `[0,sum k_i]` is realizable by valid fractions. | Human realization lemma | Feasibility level only | README/census | Not an overload optimizer. |
| UC-003 | Exactly 149 of 168 labeled monotone four-label families are positive threshold families. | Exact finite proposition; separate implementation | Four labels | census scripts | Classical classification not claimed novel. |
| UC-004 | Each realizable family has a positive integer representation with maximum weight at most 4. | Exact finite existence proposition | Enumerated witness search | census JSON | Not canonical/minimum. |
| UC-005 | The other 18 nonempty monotone families have exact two-trade contradictions; the empty family is impossible. | Exact finite certificates | Positive weak threshold | census | Four-label only. |
| UC-006 | A feasible singleton gives an available routing with maximum upper deviation at most 1. | Human fixed-support lemma | `d_max=1` | topology appendix | Fixed topology only. |
| UC-007 | Every pair feasible and no singleton feasible imply `1<sum p_i<=2`. | Human scalar lemma | `k_i>0` | every-pair theorem | Sorting is scalar only. |
| UC-008 | The positive-difference every-pair/no-singleton cell has exact supremum `L=(299-41sqrt(41))/32`. | Human theorem; exact algebra corroboration | Fixed topology and cell conditions | local routing lemma/theorem | Does not solve other cells. |
| UC-009 | `149=54+1+94`: singleton cells, solved every-pair cell, and 94 initial remainder; 15 abstract-label orbits in the remainder. | Exact finite classification | Abstract `S4` action only | reconciliation | Graph automorphism is identity; labels remain formal. |
| UC-010 | Local lower family equals the pinned release extraction componentwise. | Exact definition comparison | Pinned extraction | equivalence checker | Human-created extraction. |
| UC-011 | Exact algebra audits reproduce the formulas used to corroborate UC-008. | Exact algebraic corroboration | Declared assumptions | algebra audits | Human proof remains authoritative. |
| UC-012 | If no pair is feasible, then `sum p_i>2` (equivalently `sum q_i<2`). | Human scalar proof | Positive differences | `NO_PAIR_SCALAR_LEMMAS.md` | Does not by itself bound overload. |
| UC-013 | The full-set-only cell and four exactly-one-triple cells have value at most 1. | Human fixed-topology proof | Positive differences; no feasible pair | same file | Two-or-more-triple and pair cells not covered. |
| UC-014 | Five named strict interior cells have exact rational lower witnesses greater than 1. | Exact finite rational certificates | Named labeled cells | `EXACT_OPEN_CELL_WITNESSES.md`; exact checker | Lower bounds only, not optima. |
| UC-015 | Every nonzero signed-difference feasible family is a coordinate complement of a positive threshold family; on four labels there are exactly 1,881 unique labeled unate threshold families. | Human reduction plus exact finite census | All `k_i!=0`; feasibility only | `SIGNED_DIFFERENCE_REDUCTION.md`; signed census | Objective orientations also flip; no signed optimum result. |
| UC-016 | The nonnegative closure of the solved every-pair/no-singleton cell contains no zero coordinate, so UC-008 already covers that closure. | Human scalar proof | `k_i>=0`, not all zero, same cell | `ZERO_BOUNDARY_EVERY_PAIR.md` | Other zero-boundary cells open. |
| UC-020 | Every one of the **89** remaining labeled positive-difference cells has value at most `L`. | Open target | After UC-013 reduction | optimization protocol | Open. |
| UC-021 | Some remaining cell has value exceeding `L`. | Open alternative | Exact interior witness needed | optimization protocol | Current exact witnesses exceed 1 but not L. |
| UC-022 | The 1,881 signed nonzero cells can be structurally reduced or optimized under sign-oriented supports. | Open extension | Signed objective required | signed reduction | Open. |
| UC-030 | A structural theorem replaces cellwise optimization. | Open target | To be determined | README | Open. |
