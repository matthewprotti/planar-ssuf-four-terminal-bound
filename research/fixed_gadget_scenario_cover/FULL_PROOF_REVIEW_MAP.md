# Full-Proof Review Map

**Candidate state:** private first-human-review derived copy, not released.  
**Purpose:** give a reviewer a direct path to every controlling analytic proof.

The PDF in `paper/ssuf_fixed_gadget_scenario_cover_synopsis.pdf` is an
integrated synopsis. It is not intended to contain every case analysis. The
complete proof sources listed below are repository payloads, not missing
external references. In any circulated reviewer package they must be exposed
as ordinary unpacked files; a nested source archive alone is not adequate
reviewer-facing presentation.

## Public/private distinction

- The immutable public `v0.2.1` corpus contains the original restricted
  one-scenario lower family and the exact two-positive-scenario theorem.
- GM-002/GM-003 is a later **private** theorem extending the one-scenario
  fixed-gadget analysis to arbitrary legally realizable route-cost
  differences. It is not the same claim as the public restricted lower family.
- GM-005, GM-006, SC-006, and GM-008/GM-009 are also private candidate claims.
- None of these fixed-gadget claims determines the unrestricted planar SSUF
  constant.

## Controlling analytic proofs

The hashes below identify this derived copy. Line counts include blank lines.

| Claim | Complete controlling source | Lines | SHA-256 | What establishes the upper/global part |
|---|---|---:|---|---|
| GM-002 / GM-003 | `one_scenario/proof/GLOBAL_ARBITRARY_ONE_SCENARIO_THEOREM.md` | 940 | `7168d598b2fbcf44ebee8a3c55a4779963e379edc3c62a93ebaed4247acf62c1` | Positive-lane blocker-cover classification plus pinned signed/zero theorems; no numerical optimizer is an upper-bound premise. |
| GM-004 / RB-003 | `../two_scenario_global_constant/TWO_SCENARIO_GLOBAL_CONSTANT.md` | 803 | `ec2d1c77abe2070877378cfce97da91ded5616646975f0013cc517c7750e7cb1` | Exhaustive analytic case reduction for exactly two positive scenarios; immutable public `v0.2.1` source. |
| GM-005 | `scenario_ladder/GM005_THREE_SCENARIO_THEOREM.md` | 248 | `dfd4e03cbf285229e863d812a17cf4422054f648abaeb266643bb3b8acebdd18` | Singleton assignment and equality collapse. |
| GM-006 | `scenario_ladder/GM006_FOUR_OR_MORE_SCENARIOS.md` | 58 | `1ecc793c6621a332cb318dcb0e74ea58ec2b537a9b28b2a48cd7d8d51a239817` | All-C ceiling, explicit lower sequence, and finite nonattainment contradiction. |
| Arc envelope used by GM-005/006 | `scenario_ladder/TRUNK_PRIVATE_ARC_ENVELOPE.md` | 97 | `c997df468fb697aa02fd04c06382840d0b3caf82d0613fc51297198518557126` | Direct signed-incidence proof over all five trunk and eight private arcs; no enumeration premise. |
| SC-000 / atlas definitions | `scenario_cover/SCENARIO_COVER_DUALITY.md` | 669 | `b23f2b376fa3b6a3081b250727b854d51963a5c2b065eac43b0bbf8fa0330d5a` | Exact open-halfspace equivalence and finite-object definitions. |
| SC-006 | `scenario_cover/SC006_CONTINUUM_THEOREM.md` | 474 | `b326dbdc663d0164eb0a2adc4d88a79294e91fbcbe98eead478017b00ae94f8d` | Analytic four-phase fixed-family proof, including every obstruction, construction, strict endpoint, and global RB-family ceiling. The finite atlas does not prove this theorem. |
| GM-008 / GM-009 | `bounded_heterogeneity/GM008_GM009_HIGH_KAPPA_THEOREM.md` | 533 | `2aced64fd851b136f88fe6f09679816b4f2d98b43380a2337104298f0f57632b` | RB-003 value-above-two reduction, strict cover inequalities, allocation envelope, one-variable maximization, matching strict construction, and quartic sign analysis. |

The relative path for GM-004 is from this directory; from the repository root
use `research/two_scenario_global_constant/TWO_SCENARIO_GLOBAL_CONSTANT.md`.

## Supporting dependencies

- GM-002/003: `one_scenario/proof/FINITE_BLOCKER_COVER_CLASSIFICATION.md`,
  `one_scenario/proof/ROUTING_ALLOCATION_DETAILS.md`, and every file under
  `one_scenario/proof/imported-baseline/`.
- GM-005/006: `scenario_ladder/MODEL_SPEC_GM005.md` and
  `scenario_ladder/TRUNK_PRIVATE_ARC_ENVELOPE.md`.
- GM-008/009: `bounded_heterogeneity/MODEL_AND_RB003_DEPENDENCY_SPEC.md` and
  the public RB-003 proof source above.
- SC-006: `scenario_cover/SCENARIO_COVER_DUALITY.md` for notation and the
  fixed-family definitions; SC-006's analytic proof is otherwise the authority
  for its phase theorem.

## Executable evidence and its boundary

| Object | Program entry point | Permitted evidentiary role |
|---|---|---|
| One-scenario theorem | `one_scenario/reproduction/verify_global_one_scenario_theorem.py` | Exact finite classification and algebraic corroboration only. |
| Thirteen-arc envelope | `scenario_ladder/reproduction/verify_arc_envelope.py` | Reconstruct all path incidences and all sixteen route formulas; the analytic lemma remains authoritative. |
| GM-005 / GM-006 | `scenario_ladder/reproduction/verify_gm005_exact.py`, `verify_scenario_ladder.py` | Exact identities, mutations, and rational lower sequences only. |
| Finite atlas | `scenario_cover/reproduction/scenario_cover_atlas.py` and verifiers | Authority for the explicitly finite RB-witness census only. |
| SC-006 | `scenario_cover/reproduction/verify_sc006_symbolic.py`, `replay_sc006_exact.py --full` | Symbolic and exact sample corroboration; not a substitute for the continuum proof. |
| GM-008 / GM-009 | `bounded_heterogeneity/verify_high_kappa.py` | Exact algebraic and branch-regression corroboration; not a substitute for the global proof. |

No finite computation, numerical search, internal review disposition, or PDF
text preflight is used as a premise for an analytic supremum or continuum
claim.

## Recommended review order

1. Read `MODEL_AND_NOTATION.md` and
   `scenario_ladder/TRUNK_PRIVATE_ARC_ENVELOPE.md`.
2. Select a claim row above and reconstruct its controlling proof without
   running the supplied code.
3. Read its listed dependencies and verify that every imported lemma has the
   same model, strict/weak convention, and scope.
4. Only then run the associated executable corroboration.
5. Report a claim-level disposition separately for GM-002/003, GM-004,
   GM-005, GM-006, SC-006, and GM-008/009. Do not infer publication readiness
   from a subset review.

The first supplied external human report reconstructed the duality and the
short GM-005/006 arguments and found no mathematical contradiction in those
portions. It did not inspect the unpacked SC-006 or GM-008/009 controlling
proofs and therefore marked those lanes unresolved. That is a scope-limited
review record, not an adverse proof finding and not a full external
reconstruction.
