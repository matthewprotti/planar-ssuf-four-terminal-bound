# Response to Second-Round AI-Assisted Hostile Proof-Only Critique — RB-003 v4 to v5

**Classification note:** The critic was a role-separated AI model context, not
an external human mathematical reviewer. This historical response records the
pre-release proof-repair loop. The v5 package was subsequently released after
human adjudication in `v0.2.0`.

## Disposition

The AI-assisted critic reported no counterexample and no remaining theorem-level gap in
the four requested proof pressure points. The formal recommendation was:

> accept subject to minor proof revision.

The report identified five circulation edits, together with the additional
active-constraint and zero-weight proof-hygiene clarifications. All are
incorporated in the v5 theorem file. No numerical
constant, finite certificate, feasible family, or theorem scope changed.

The v5 archive incorporated the proof repairs and was subsequently released
after Matthew Protti's human adjudication. No external human mathematical
review has been requested or documented, and the work has not been peer
reviewed. `v0.2.1` corrects this status and provenance language only.

## One-to-one revision matrix

| Review item | Disposition | v5 revision |
| --- | --- | --- |
| Required edit 1 — §6.1 heading stated the opposite of the proved conclusion. | Accepted. | Heading changed to **“At least three individually omittable terminals.”** The proof already concluded `|A|>=3`; no argument changed. |
| Recommended edit 2 — formalize the two-colour consequence of Lemma 1. | Accepted. | Added an explicit global weighting statement: assign each blocker to one blocking scenario, restrict the weighting to each colour, apply Lemma 1 to each restriction, and sum to obtain total weight `<2`. Empty colour classes are covered. |
| Required edit 3 — equation (15) was applied without restating Lemma 2's pair-blocking hypothesis. | Accepted. | The sentence now requires that one scenario block every pair in the complementary three-set `T` before invoking (15). Later applications already satisfy this condition. |
| Recommended edit 4 — make the one-knapsack extreme-point claim self-contained. | Accepted. | Added the active-constraint argument: with slack knapsack all coordinates of an extreme point are at box bounds; with tight knapsack at least two independent box constraints are active, leaving at most one fractional coordinate. |
| Required edit 5 — “the only remaining pattern” overstated the `|A|=3` reduction. | Accepted. | Replaced by a **forced blocker core** statement. Scenario 1 blocks `u`, all three incident pairs, and no internal pair of `A`; scenario 2 blocks all three pairs within `A`. The theorem now explicitly allows scenario 2 to block one additional incident pair and explains why it is irrelevant. |
| Recommended edit 6 — the non-attainment proof jumped from equation (20) to `h_u=1`. | Accepted. | Displayed the full equality sandwich at `Delta=3/4` from equations (20)–(22), then inferred that every inequality is tight and hence `h_u=1`. |
| Lemma 1 zero-weight wording — the former exception was unnecessary. | Accepted. | Lemma 1 now states `<1` unconditionally and treats the all-zero weighting as immediate before applying the strict blocker inequality. |

## Mathematical claims unchanged

The proof-integrated manuscript retains:

1. the exact fixed-graph two-scenario cost-nonincrease supremum
   \[
   \beta_G^{(2\mathrm{sc})}=17/8;
   \]
2. non-attainment by every legal finite instance;
3. the rational extremizing sequence with intrinsic feasible C-family
   `upward_closure{123,124,234}`;
4. the exact `epsilon=1/1000` finite value `1061/500`; and
5. the scaled unavoidable upper deviation 8488.

The role-separated v4 AI-assisted critic specifically confirmed the strict two-colour matching argument,
the generalized unit-profit knapsack lemma, the actual shared-baseline
`|A|=3` exhaustion, both star-triangle envelopes, and the non-attainment
equality chain. The v5 revisions alter only how those already-valid steps are
stated and connected.

## Package-level hardening

The v5 package also:

- includes the AI-assisted critic report verbatim;
- adds `proof_review_integration_check.py`, which asserts the required formulations are
  present and the superseded formulations are absent;
- runs that guard inside `replay.py` after package authentication;
- updates the claim ledger to describe a forced blocker core rather than an
  exact pair of blocker graphs;
- updates the executive and commercial documents to preserve the same
  distinction; and
- retains the first-round major-revision response and completed attack brief as
  historical audit artifacts.

## Residual limitations

Nothing in the second-round review changes the established limitations:

- `17/8` is a non-attained supremum;
- the theorem is fixed-topology and two-scenario;
- feasibility means cost non-increase, not equality;
- the finite certificate is highly ill-conditioned;
- the 11,175 abstract pattern-pair census is regression evidence, not a
  shared-baseline proof; and
- the secondary implementation is not an independent mathematical derivation.

## Author-side recommendation

This historical recommendation was superseded by the completed authenticated
replay and Matthew Protti's human release decision for `v0.2.0`. External human
review remains a separate future evidence class and must be documented as such.
No further discovery or numerical search is implied by the `v0.2.1`
provenance correction.
