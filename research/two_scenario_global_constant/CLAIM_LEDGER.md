# Claim Ledger — Track B Global Two-Scenario Supremum

**Review status.** Two role-separated AI-assisted critique rounds were
performed; no external human mathematical review is documented. The second
proof-only critic reported no remaining theorem-level gap and recommended
acceptance subject to minor proof revision. This v5 package incorporates all
required and recommended local edits and was released after human adjudication
in `v0.2.0`. `v0.2.1` corrects provenance and release hygiene only.

| ID | Claim | Evidence class | Scope / limitation |
| --- | --- | --- | --- |
| RB-001 | Every nonempty four-label monotone family is realizable by at most two positive scenarios on a shared uniform baseline, allowing baseline zero for the all-subsets endpoint. | Prior exact finite theorem; contextual here. | Feasibility classification only; not used in RB-003 upper proof. |
| RB-002 | Each of the 18 two-scenario-only nonthreshold cells has exact fixed-topology value 2. | Prior human support proof and exact certificates; contextual here. | Does not determine the global two-scenario parameter constant. |
| RB-003 | Under two scenario-wise cost-nonincrease constraints, the fixed-graph normalized additive upper-deviation supremum is exactly `17/8`. | Self-contained human-readable blocker/matching/knapsack/star-triangle proof plus rational lower sequence; role-separated AI-assisted proof-only critique found no theorem-level gap after the listed local edits. | Fixed graph, two positive E-minus-C difference vectors, upper-deviation objective; no external human mathematical review is documented. |
| RB-003a | No legal finite instance attains `17/8`. | Human-readable equality-case contradiction using the full equations (20)–(22) equality sandwich, `h_u=1`, and normalized scenario budget. | Establishes non-attainment, not a quantitative convergence rate. |
| RB-004 | Any actual shared-baseline instance above 2 contains a forced star-triangle blocker core with the non-omittable terminal in graph role 2 or 3. The triangle scenario may also block one additional incident pair without affecting the proof. | Human-readable shared-baseline case proof. | Forced-core reduction, not an exact classification of both complete blocker graphs. The 11,175 abstract pair census is regression only. |
| RB-005 | At `epsilon=1/1000`, the lower instance has exact objective `1061/500`; after demand scaling by 4000, unavoidable upper deviation is 8488. | Exact graph-native enumeration of 16 routes and 13 arcs. | Finite certificate approaches but cannot attain `17/8`. |
| RB-006 | `17/8 > L`. | Exact arithmetic comparison `41^3 > 231^2`. | Contextual comparison to a restricted one-scenario benchmark, not a marginal effect estimate. |
| RB-007 | Exactly 149 of the 167 admissible nonempty four-label downsets are positive scalar-threshold families; the other 18 have exact two-trade contradictions. | Exact finite enumeration with witnesses and impossibility certificates. | Four labels only. |
| RB-008 | The secondary code path reproduces the finite certificate, threshold counts, abstract case counts, and envelope-grid values. | Regression implementation. | Not an independent mathematical derivation; shares the support matrix, blocker framework, and lower ansatz. |
| RB-009 | The v5 theorem text contains all second-round local proof edits and excludes the superseded formulations identified by the AI-assisted critic. | Deterministic text guard plus line-level revision map. | Editorial/proof-hygiene assurance only; not mathematical evidence for RB-003. |
