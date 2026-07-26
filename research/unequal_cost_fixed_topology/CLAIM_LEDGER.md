# Claim Ledger — Fixed-Topology SSUF Follow-On

Last updated: 26 July 2026, remaining-limits research pass

| ID | Claim | Status / evidence class | Evidence | Boundary / next gate |
| --- | --- | --- | --- | --- |
| UC-001 | Positive cost differences reduce feasibility to `k(S)>=k·p`. | Human proof | theorem file | Zero/negative are not normalized away. |
| UC-002 | Every positive threshold family is fractionally realizable. | Human proof | census/README | Feasibility only. |
| UC-003 | 149 of 168 monotone families are positive threshold. | Exact finite census | two implementations | Four labels. |
| UC-004 | All 149 have max-weight-at-most-4 integer witnesses. | Exact finite existence | census | Not canonical. |
| UC-005 | 18 exact two-trades plus one impossible empty family. | Exact certificates | census | Four labels. |
| UC-006 | Feasible singleton implies available deviation at most 1. | Human proof | topology appendix | Fixed topology. |
| UC-007 | Every pair/no singleton implies `1<sum p<=2`. | Human proof | every-pair theorem | Positive differences. |
| UC-008 | Every-pair/no-singleton cell has exact value `L`. | Self-contained human theorem | local lemma and lower family | One cell. |
| UC-009 | Initial positive remainder is 94 labeled cells in 15 abstract orbits. | Exact census | reconciliation | Historical starting partition. |
| UC-010 | Local lower family matches pinned release extraction. | Exact comparison | equivalence checker | Provenance extraction human-created. |
| UC-011 | Exact algebra audits match local formulas. | Corroboration | two arithmetic paths | Not proof-assistant verification. |
| UC-012 | No feasible pair forces `sum p>2`. | Human scalar lemma | no-pair file | No overload conclusion alone. |
| UC-013 | Full-only and one-triple cells have value at most 1. | Human proof | no-pair file | Reduced 94→89. |
| UC-014 | Eleven strictly positive cells have exact strict interior rational lower witnesses above 1; F060 reaches `28085483/25000000`. | Exact rational certificates | witness checker and JSON | None exceeds `L`; not cell optima. |
| UC-015 | 1,881 unique nonzero signed/unate feasible families arise from oriented threshold families. | Human reduction + exact census | signed census | Feasibility classification only. |
| UC-016 | Solved every-pair cell has no zero-difference boundary point. | Human proof | zero-boundary file | Other zero strata handled by UC-018/019. |
| UC-017 | Every signed single-generator stratum with generator size at least two has exact value 1; in the positive lane this resolves 11 cells. | Human theorem + exact checks | signed single-generator files | Multiple-generator positive cells remain. |
| UC-018 | Every non-all-positive nonzero sign/zero stratum has exact value 1 or 9/8 and is strictly below `L`. | Human theorem + exact algebra/finite grids | nonpositive files | Identically zero handled only by UC-019 bounds. |
| UC-019 | Identically zero cost differences have exact value `4/5`. | Human theorem + exact lower witness and rational-grid corroboration | cost-free files | Fixed topology only. |
| UC-023 | The four pure three-pair clique cells have exact value `9/8` for omitted terminals 2/3/4 and 1 for omitted terminal 1. | Human theorem + exact checks | clique theorem/checker | Does not cover larger feasible-pair graphs. |
| UC-020 | All 79 remaining strictly positive cells are at most `L`. | Open main target | cell protocol | No exact candidate above `L`. |
| UC-021 | Some remaining strictly positive cell exceeds `L`. | Open alternative | exact interior witness required | Current witnesses are below `L`. |
| UC-022 | The unrestricted signed/zero fixed-topology optimum reduces to the 79 strictly positive cells, and the exact cost-free value `4/5`. | Human corollary from UC-018/019 | theorem ledger | Global positive frontier still open. |
| UC-030 | Structural replacement for cellwise optimization. | Open | unknown | 79 positive cells remain. |

## Standing nonclaims

No claim of global fixed-topology sharpness, four-terminal optimality, exact
unrestricted planar constant, novelty, external reproduction, independent human
verification, or peer review.
