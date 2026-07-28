# Referee Response Matrix — Round Two

The authors do not determine whether an objection is closed. “Response” below
means a change intended to address the objection. The original taxonomy is
preserved: four P0 items and six P1 items from the first report, followed by the
numbered concerns in the second report.

| Original ID | Original objection | Author response | Changed file / section | Formal claim affected | Validation evidence | Residual limitation |
| --- | --- | --- | --- | --- | --- | --- |
| P0.4 | “Make UC-008 self-contained or exactly pinned.” | Restated the graph, fixed-support routing lemma, lower family, and optimization locally; pinned release only for provenance. | `FIXED_TOPOLOGY_APPENDIX.md`; `FIXED_SUPPORT_ROUTING_LEMMA.md`; `EVERY_PAIR_CELL_THEOREM.md`; `DEPENDENCY_MANIFEST.json` | UC-006–UC-010 | `symbolic_every_pair_check.py`; `exact_algebra_audit.py`; `release_family_equivalence_check.py` | Human proof remains unrefereed; local release extraction is not a general TeX parser. |
| P1.1 | Rewrite cost reduction using \(k_i=e_i-b_i>0\) and identify excluded cases. | Positivity is stated as a genuine restriction for the positive-cell work; later UC-018/019 treat the excluded objective strata separately. | `POSITIVE_DIFFERENCE_SCOPE.md`; master objective; UC-001/018/019 | UC-001, UC-008, UC-018, UC-019 | Artifact text validation and theorem checks | The later signed results do not make positivity WLOG for the positive threshold census. |
| P1.2 | Add local topology/path-support appendix. | Added complete graph, paths, four supports, private arcs, and six pair maxima. | `FIXED_TOPOLOGY_APPENDIX.md` | UC-006, UC-008 | Symbolic pair-expression audit | Fixed topology only. |
| P1.5 | Add schemas and dependency/hash manifest. | Expanded manifest, release pin, expected replay hashes, and offline one-command replay. | `artifact_manifest.json`; `DEPENDENCY_MANIFEST.json`; `RELEASE_FAMILY_PIN.json`; replay report; `REPRODUCIBILITY.md` | All handoff claims | round-two replay; `build_artifact_manifest.py --check` | Hashes bind snapshots; they are not signatures. |
| P1.6 | Add current prior-art matrix. | Added adjacent threshold-game, trading-transform, and SSUF literature with no novelty claim. | `PRIOR_ART_AND_NOVELTY_MATRIX.md` | Novelty posture only | Human inspection | Not exhaustive novelty clearance. |
| R2-01 | P0 accounting and branch-specific items were unclear. | Preserved original P0/P1 IDs and separated second-round concerns. | This matrix; PCR companion matrix | Response accounting | Artifact validation | Referee determines adequacy. |
| R2-02 | Authors declared closure categorically. | Replaced closure language with “intended to address” and reported replay outcomes only. | response files; README; PR body | Handoff posture | Text validation | No acceptance claim. |
| R2-03 | Reproducibility block was incomplete. | Added base/implementation pins, clean-clone steps, Python/SymPy versions, network posture, exact commands, expected exit code, output/manifest hashes, and archived bundle guidance. | `REPRODUCIBILITY.md`; replay script | All machine evidence | round-two replay | External party has not yet reproduced the revised package. |
| R2-04 | Proof, finite enumeration, symbolic checks, and mutation evidence were blurred. | Classified every claim by evidence class. | `THEOREM_LEDGER.md`; `CLAIM_LEDGER.md` | UC-001–UC-011 | Ledger consistency check | Exact algebra is corroboration, not an automatic proof of inequalities. |
| R2-12 | Positivity was not proved WLOG or clearly advertised as restriction. | Advertised explicitly as a genuine restriction; renamed package/theorem scope. Later signed/zero theorems use the same physical objective without rewriting this response as a WLOG claim. | `POSITIVE_DIFFERENCE_SCOPE.md`; README; UC-001/UC-008/UC-018/UC-019 wording | UC-001, UC-008, UC-018, UC-019 | Text validation | The current positive frontier remains separate. |
| R2-13 | Principal theorem boundary was difficult to infer. | Added theorem ledger with full statements, assumptions, locations, evidence class, and residuals. | `THEOREM_LEDGER.md`; `CLAIM_LEDGER.md` | All UC claims | Ledger ID check | The current 79-cell positive conjecture remains open; 94 and 83 are historical stages. |
| R2-14 | Census units/orbits needed reconciliation. | Added explicit 168=149+18+1 and 149=54+1+94 partitions, arbitrary-label \(S_4\) action, orbit members/sizes/stabilizers, and separate graph automorphism statement. | `CENSUS_RECONCILIATION.md`; reconciliation JSON | UC-003–UC-005, UC-009 | Generator and separate census checker | Orbit quotient is not a graph-symmetry reduction. |
| R2-15 | Boundary/closure protocol was only a plan. | Labeled it methodology and enumerated which domains remain unhandled. Later exact theorems are recorded separately rather than retroactively treating the protocol as proof. | `CELL_OPTIMIZATION_PROTOCOL.md`; theorem ledger | UC-020/UC-021 | Text validation | The 79 current positive cells and their unproved boundary transfers remain open. |
| R2-16 | “Exact symbolic verification” lacked assumptions and TCB. | Pinned SymPy 1.14.0, disclosed assumptions/methods, and added a no-CAS exact algebra audit over rational Laurent polynomials and \(\mathbb Q(\sqrt{41})\). | `SYMBOLIC_TRUST_AND_ASSUMPTIONS.md`; both algebra scripts | Corroboration for UC-008 | Both exact checkers and replay | Shared formulas may still encode a human transcription error; human proof is authoritative. |
| R2-17 | Local lower-family restatement needed equivalence check. | Added machine-readable local definition, pinned release extraction, componentwise comparison, and proof-fragment checks; replay never reads the old release. | `LOWER_FAMILY_EQUIVALENCE.md`; `lower_family.py`; `RELEASE_FAMILY_PIN.json`; checker | UC-010; lower half of UC-008 | `release_family_equivalence_check.py` | Pinned extraction was human-created from the released TeX and is separately auditable. |
| R2-independence | “Independent” and “reproducible” wording was too strong. | Uses “structurally separate checker” and “deterministic internal replay”; records shared assumptions and code-generation provenance. | README; symbolic trust note; response | Handoff posture | Human inspection | No external reproduction claim. |
| R2-minor | Define acronyms, paths, versions, mutation/witness inventory, production-boundary evidence, and excluded cases. | Defined SSUF; added repository-relative paths, theorem/version ledger, witness examples, path-restricted diff statement, excluded-case table, and reproducibility record. | README; `HUMAN_READABLE_WITNESSES.md`; `REPRODUCIBILITY.md`; theorem ledger | Presentation and auditability | Manifest and path-diff check | No manuscript version beyond branch research docs is claimed. |

The companion PCR matrix maps P0.1–P0.3 and the PCR-specific second-round
concerns. P0.4 appears here because it is the SSUF cross-workstream gate.

## Forward research beyond the response matrix

Subsequent work adds UC-012–UC-023: no-pair and single-generator reductions,
exact signed/zero objective theorems, a nonnegative arc-cost realization for
the common master objective, exact lower witnesses, and the positive
three-pair-clique theorem. The staged positive remainder is
94→89→83→79 labeled cells, with 79 cells in 11 abstract-label search orbits
current. Ten current open cells retain exact interior witnesses; F042's earlier
witness is historical because UC-023 now solves that cell. These are new
research steps, not author-declared closure of referee objections.
