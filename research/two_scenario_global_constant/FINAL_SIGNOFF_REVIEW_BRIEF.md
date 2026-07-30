# Historical AI-Assisted Verification Brief — RB-003 v5

**Classification note:** This file records a pre-release brief supplied to a
role-separated AI-assisted proof critic. It is not evidence of external human
mathematical review. The edits were integrated before Matthew Protti's human
release decision for `v0.2.0`; `v0.2.1` corrects this provenance and status
wording without changing the mathematics.

## Scope

This was a narrow verification of the proof-integrated v5 archive. The
AI-assisted v4 proof-only critique found no theorem-level gap and recommended
acceptance subject to minor proof revision. The purpose was to confirm that the
requested local edits were integrated without introducing a new inconsistency.

## Integrity gate

1. Verify the external ZIP SHA-256 supplied with the archive.
2. Extract into a clean directory.
3. Run:

```bash
python replay.py
```

4. Confirm authentication succeeds before and after regeneration and that
   `proof_review_integration_check.py` passes.

## Proof-edit gate

Confirm the following exact points in `TWO_SCENARIO_GLOBAL_CONSTANT.md`:

1. §6.1 is titled **“At least three individually omittable terminals.”**
2. Lemma 1's two-colour consequence explicitly restricts a global blocker
   weighting to each scenario and obtains total weight `<2`.
3. The application of equation (15) assumes that one scenario blocks every
   pair in the complementary three-set.
4. Lemma 2 includes the active-constraint explanation for at most one
   fractional coordinate at a box-constrained one-knapsack vertex.
5. The `|A|=3` conclusion is a **forced blocker core**, not an exact
   classification of both full blocker graphs; the possible one extra incident
   edge in the triangle scenario is acknowledged as irrelevant.
6. The non-attainment proof displays the full equations (20)–(22) equality
   sandwich before inferring `h_u=1`.
7. Lemma 1 handles the all-zero weighting without an exception to its `<1`
   conclusion.

## Claim consistency gate

Confirm that the following remain unchanged and correctly scoped:

\[
\beta_G^{(2\mathrm{sc})}=17/8
\]

as a non-attained supremum for the stated fixed graph and two scenario-wise
cost-nonincrease constraints; the rational lower sequence; the exact finite
value `1061/500`; and the scaled deviation 8488.

Confirm that the executive, commercial, and claim-ledger documents use
“forced star-triangle blocker core” and do not claim:

- exact equality of fractional and unsplittable scenario costs;
- a finite maximizer at `17/8`;
- a controlled causal comparison with `L`;
- a theorem about sequential algorithms; or
- computational independence beyond what is documented.

## Historical requested disposition

Please return one of:

- **Accept:** the v4 minor-proof conditions are fully integrated and RB-003 is
  ready for a human release decision;
- **Local correction:** identify exact file, section, and replacement text; or
- **Mathematical objection:** provide the failing implication or a concrete
  counterexample under the stated cost-nonincrease model.
