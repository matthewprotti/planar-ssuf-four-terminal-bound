# Second-Round Hostile Proof-Only Referee Report — RB-003 v4

**Manuscript:** *The Exact Two-Scenario Cost-Nonincrease Supremum on the Four-Terminal Gadget*  
**Version reviewed:** `SSUF_July_2026_TrackB_Global_17_8_v4_Major_Revision.zip`  
**Archive SHA-256:** `34590ce7f66b222672c0ad47ea4f9a0f204f542281a42979aa46ff9953603c2f`  
**Scope:** hostile proof-only review, with the v3 major-revision findings treated as integrated rather than reopened.

## Referee disposition

**Recommendation: accept subject to minor proof revision.**

I found no counterexample and no remaining theorem-level gap in the four requested pressure points:

1. Lemma 1, including strict inequalities and the passage from one colour to two;
2. Lemma 2 in its generalized `c_i in [0,1]` form;
3. the actual shared-baseline `|A|=3` exhaustion; and
4. the equality chain proving non-attainment.

The v3 publication blockers have been repaired. The upper-bound proof now closes, and the non-attainment corollary is valid. I would not send the manuscript back to discovery or numerical search. I would require five local edits before circulation because two current phrases state more—or the opposite—of what the proof establishes.

The mathematical verdict below treats the computational package as non-probative. I authenticated the archive and manifest only to identify the reviewed version.

---

## 1. Lemma 1 survives the hostile review

For a fixed scenario `j`, let `E_j` be the assigned blocked singletons and pairs, and let

\[
\ell_i^{(j)}:=\sum_{T\in E_j:\,i\in T}\lambda_T.
\]

If the colour class carries nonzero weight, every positively weighted `T` has
`w^(j)(T)>1`, so

\[
\sum_{T\in E_j}\lambda_T
<\sum_{T\in E_j}\lambda_Tw^{(j)}(T)
=\sum_iw_i^{(j)}\ell_i^{(j)}
\le\sum_iw_i^{(j)}h_i
\le\sum_iw_i^{(j)}q_i
=1.
\]

Every step is valid:

- the first inequality is strict because at least one positive `lambda_T` is multiplied by a strictly larger-than-one blocker weight;
- the reindexing is exact for singletons and pairs alike;
- the vertex-load hypothesis gives `ell_i^(j) <= h_i`;
- `h_i=d_iq_i <= q_i` follows from the normalization `d_max=1`; and
- scenario normalization gives `sum_i q_i w_i^(j)=1`.

If the colour class is empty, its total is zero and is still strictly below one. Thus the exception “unless all `lambda_T` vanish” is unnecessary.

For the two-colour consequence, the earlier assignment partitions each blocked set into one colour. Given any global fractional matching with vertex loads at most `h_i`, its restriction to either colour also has vertex loads at most `h_i`. Hence each colour contributes less than one and the global total is less than two. This remains true when one colour is empty.

The three matching constructions in §6.1 are all legal:

- `|A|=0`: singleton weight `h_i` at every vertex;
- `|A|=1`: singleton weight `h_i` at the three non-omittable vertices; and
- `|A|=2`: singleton weights on the two non-omittable vertices plus `min(h_r,h_s)` on the blocked pair `{r,s}`.

Their total weights are respectively `H`, at least `H-Delta=t`, and at least `H-Delta=t`, so each contradicts the strict two-colour bound when `t>2`.

### Required edit 1

The heading at manuscript line 390 is reversed. The argument proves

> **At least three individually omittable terminals**

not “At most two individually omittable terminals.” The displayed conclusion `|A|>=3` is correct.

### Recommended edit 2

State the two-colour consequence as a formal corollary rather than the sentence “Thus every fractional matching in the union...”. A paste-ready version is:

> Assign every blocked singleton and pair to one scenario that blocks it. If `lambda_T` is any weighting of the assigned sets satisfying `sum_{T contains i} lambda_T <= h_i` for every vertex, then, after restricting `lambda` to each scenario, Lemma 1 gives total weight below one in each colour. Consequently `sum_T lambda_T<2`.

This removes any ambiguity about coloured copies or double counting.

---

## 2. The generalized one-knapsack lemma is correct

Let

\[
P=\left\{z\in[0,1]^T:\sum_{i\in T}w_i z_i\le1\right\},
\qquad |T|=3.
\]

The restricted baseline vector `q_T` belongs to `P` because the omitted terms in
`sum_i q_iw_i=1` are nonnegative.

A linear objective has an optimum at a vertex of `P`. At a vertex:

- if the knapsack inequality is slack, all three coordinates must be at box bounds;
- if it is tight, at least two independent box constraints must also be active, so at most one coordinate is fractional.

Thus an extreme optimum has at most one fractional coordinate. Because every pair in `T` is blocked, two coordinates cannot both equal one: that would have knapsack weight greater than one. Therefore the integral part contains at most one selected item. With `0<=c_i<=1`, that item contributes at most one, and the possible fractional item contributes at most one. Hence the optimum is at most two, and so

\[
\sum_{i\in T}c_iq_i\le2.
\]

Both applications are legitimate after `d_max=1`:

- `c_i=d_i` lies in `[0,1]` and gives `sum_{i in T}d_iq_i<=2`;
- `c_i=1` gives `sum_{i in T}q_i<=2`.

The proof covers all boundary cases: inactive knapsack, an overweight individual item, zero-profit items, zero baseline coordinates, and degeneracy of the optimum face.

In fact, strict pair blocking implies the optimum is strictly below two for every finite instance: if there is one integral selected item, any second nonzero extreme coordinate must be genuinely fractional. The manuscript does not need this strengthening, and retaining the closed bound `<=2` is harmless.

### Required edit 3

The sentence at manuscript lines 356–358 is overbroad when read literally. Equation (15) applies only when the complement `T` satisfies Lemma 2’s hypothesis—one scenario blocks every pair of `T`. Replace it with:

> If a feasible singleton E-set `{r}` has complement `T`, **and one scenario blocks every pair in `T`**, then (15) shows that routing `r` on E has positive trunk deviation at most two; private deviations remain at most one.

The later applications in §§6.2–6.3 already supply exactly this hypothesis, so this is a statement repair, not a repair of the argument.

### Recommended edit 4

For full self-containment, add the one-sentence active-constraint argument above after “at most one fractional coordinate.” The current statement is standard and correct, but the paper otherwise aims to prove every finite reduction internally.

---

## 3. The `|A|=3` exhaustion is valid for actual shared-baseline instances

Assume `t>2`. Then no E-pair is feasible, so every pair is blocked by at least one of the two actual normalized scenario vectors sharing the same baseline `q`.

Let `u` be the unique vertex outside `A`. Since `{u}` is not jointly feasible, some scenario—call it scenario 1—has

\[
w_u^{(1)}>1.
\]

All weights are positive, so scenario 1 blocks every pair `{u,a}` with `a in A`.

Now exclude the easy case in which one scenario contains a blocked triangle whose complementary vertex belongs to `A`. Under that exclusion, scenario 1 cannot block an internal edge `{a,b}` of `A`: together with its already-blocked edges `{u,a}` and `{u,b}`, this would form the forbidden monochromatic triangle `{u,a,b}`, whose complement is the third vertex of `A`.

Therefore scenario 1 has no blocked edge internal to `A`. Since every internal pair of `A` must nevertheless be blocked by at least one scenario, scenario 2 blocks all three internal pairs. This is exactly the hypothesis needed for Lemma 2 with `T=A`, yielding

\[
\sum_{i\in A}q_i\le2.
\]

This is a direct argument about the two realized weight vectors and their common `q`; the abstract 11,175-pair census is neither used nor needed.

### Required edit 5

The phrase “the only remaining pattern is” should describe a **forced core**, not necessarily both complete blocker graphs. What is proved is:

- scenario 1’s blocked-pair graph is exactly the star centred at `u`; and
- scenario 2 contains the triangle on `A`.

The argument does not exclude scenario 2 from blocking one additional edge incident with `u`; two such additional incident edges would create one of the excluded triangles. No later inequality requires the absence of that possible extra edge.

A precise replacement is:

> Up to exchanging scenarios, the forced blocker core is as follows: scenario 1 blocks `{u}` and all three pairs incident with `u`, and blocks no pair internal to `A`; scenario 2 blocks all three pairs internal to `A`. Possible additional incident edges in scenario 2 are irrelevant to the argument.

This prevents readers from mistaking the reduction for an exact two-graph classification while preserving the proof verbatim.

---

## 4. The non-attainment equality chain is sound

Suppose a finite instance attained `t=17/8`. All cases other than the central star-triangle branch have already been bounded by two, so the instance must lie in the central branch with `1/2<=Delta<=1`.

Equation (22) gives

\[
\frac{17}{8}=t
\le \frac{17}{8}-2\left(\Delta-\frac34\right)^2,
\]

hence

\[
\Delta=\frac34,
\qquad
H=t+\Delta=\frac{23}{8}.
\]

Let `a,b` be the two outer vertices in `A`, `c` the central vertex in `A`, and `u` the central non-omittable vertex. At `Delta=3/4`, the complete equality chain is

\[
\frac{23}{8}=H
=h_u+h_a+h_b+h_c
\le
1+\min\{q_a,\tfrac34\}
 +\min\{q_b,\tfrac34\}
 +\tfrac34 q_c
\le
\frac{23}{8}.
\]

Therefore equality holds throughout. In particular the first component bound is tight:

\[
h_u=1.
\]

Since `h_u=d_uq_u` and `0<d_u<=1`, `0<=q_u<=1`, this forces

\[
d_u=q_u=1.
\]

Because `u` is not individually omittable, some scenario has `w_u^(j)>1`. But its normalization then gives

\[
1=\sum_iq_iw_i^{(j)}
\ge q_uw_u^{(j)}
=w_u^{(j)}>1,
\]

which is impossible.

There is no omitted equality branch:

- `Delta<=1/2` gives `t<=2`;
- `Delta>=1` gives `t<=2`;
- the outer non-omittable branch gives `t<=2`; and
- in the central branch the quadratic has a unique maximizer at `Delta=3/4`.

### Recommended edit 6

At manuscript line 550, replace “Equality in the bound (20) then requires `h_u=1`” with “Equality throughout (20)–(22) then requires `h_u=1`,” preferably displaying the sandwich above. Equation (20) alone does not state that its right-hand side is tight; the combination with the exact envelope does.

This is expository tightening only. The current conclusion is mathematically correct.

---

## Integrated assessment of v4

The major-revision response has done what it needed to do:

- cost non-increase is now derived correctly from graph-native costs;
- the theorem is self-contained;
- the generalized unit-profit step is present;
- the analytic upper bound no longer relies on the abstract pattern census;
- the lower family is correctly described as an extremizing sequence; and
- non-attainment is proved rather than merely asserted.

The four requested proof pressure points withstand adversarial review. The remaining edits are local:

1. reverse the erroneous §6.1 heading;
2. formalize the two-colour corollary to Lemma 1;
3. restore Lemma 2’s hypothesis in the sentence applying equation (15);
4. describe the `|A|=3` result as a forced star-triangle core rather than necessarily exact blocker graphs; and
5. make the equality-throughout step explicit in the non-attainment proof.

Subject to those edits, I would sign off on the mathematical claim

\[
\boxed{\beta_G^{(2\mathrm{sc})}=17/8}
\]

as proved for the stated fixed graph and model, with `17/8` a non-attained supremum.
