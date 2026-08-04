# Adversarial Mathematical Review Record

## SSUF fixed-gadget review packet, RC1-HR1 reseal v2

**Reviewer:** OpenAI GPT-5.6 Pro, private reviewer ID `OAI-SSUF-AR-2026-08-03-01`  
**Reviewer type:** AI mathematical reviewer; this record is not external human peer review  
**Review date:** 2026-08-03 (America/Edmonton)  
**Candidate:** private `v0.3.0-rc1-hr1`, packaging reseal v2  
**Packet reviewed:** `SSUF_HUMAN_MATHEMATICAL_REVIEW_PACKET_RC1_HR1_RESEALED_2026-08-03_v2.zip`  
**Authenticated packet SHA-256:** `8ac50ee0eae5ba9b40c11d9f1d84fb016a7f4501dcf0da5255f6bee8310783cb`

## 1. Executive disposition

### Mathematical conclusion

I found **no mathematical contradiction or claim-defeating gap** in the reviewed fixed-gadget corpus. In particular, I did not find an orientation error, strict-versus-weak feasibility error, omitted branch in the stated case reductions, false extremizing-family calculation, invalid endpoint assignment, or misuse of a finite computation as proof of a global or continuum claim.

The following claim lanes are dispositioned `ACCEPT_AS_STATED`:

| Claim lane | Disposition |
|---|---|
| GM-002 / GM-003 - arbitrary legal one-scenario fixed-gadget supremum and positive-cell bound | `ACCEPT_AS_STATED` |
| GM-004 / RB-003 - exactly two positive scenarios, supremum `17/8`, nonattained | `ACCEPT_AS_STATED` |
| GM-005 - exactly three positive scenarios, supremum `3`, nonattained | `ACCEPT_AS_STATED` |
| GM-006 - four or more positive scenarios, supremum `4`, nonattained | `ACCEPT_AS_STATED` |
| SC-000 / SC-001--003 - scenario-cover duality and the fixed finite atlas | `ACCEPT_AS_STATED` |
| SC-006 - exact four-phase two-scenario curve on the fixed RB family | `ACCEPT_AS_STATED` |
| GM-008 / GM-009 - bounded-heterogeneity upper bounds and exact high-`kappa` tail | `ACCEPT_AS_STATED` |

### Integrated disposition

**Integrated mathematical manuscript and handoff: `ACCEPT_WITH_EDITORIAL_REPAIRS`.**

The qualification is driven by three nonmathematical findings: two flattened-package entry points do not run from the delivered ZIP, a reviewer-facing scope reference is left inside the canonical TAR rather than exposed in the flat layer, and the notation for the two-positive-scenario constant drifts between `beta_G^(2,+)` and `beta_G^(2sc)`. None changes a theorem statement after context is reconstructed, and none undermines the proofs.

### Confidence statement

Confidence is high for the precise fixed-gadget claims reviewed here. This is still an adversarial reading and exact-computation cross-check, not a formal proof-assistant certification. The conclusions do not extend beyond the explicit gadget, path set, positivity class, scenario count, or heterogeneity range stated in the packet.

## 2. Independence and conflict statement

I have no personal, financial, institutional, authorship, or publication interest in the candidate. No outside party was contacted, and no external source was used to repair or supplement a missing private-document premise.

I cannot certify that a general-purpose model had no training-data exposure to public antecedents. Operationally, this review used only the supplied ZIP, its embedded canonical source archive, and computations written or executed during this pass. I had no reviewer identity or prior-report information beyond what the packet itself disclosed.

## 3. Authentication and corpus integrity

1. The ZIP SHA-256 independently recomputed to
   `8ac50ee0eae5ba9b40c11d9f1d84fb016a7f4501dcf0da5255f6bee8310783cb`, exactly matching the adjacent sidecar.
2. Extraction was performed only after rejecting absolute paths, parent traversal, and link members.
3. All 71 entries in the packet's `MANIFEST.sha256` passed.
4. All four payloads authenticated by `06_CANONICAL_SOURCE_ARCHIVE/SHA256SUMS.txt` passed.
5. The synopsis PDF exposed in `01_SYNOPSIS/` is byte-identical to the canonical-archive copy.
6. The eight controlling proof files match the line counts and SHA-256 values recorded in `FULL_PROOF_REVIEW_MAP.md`.
7. Every exposed controlling proof and listed analytic dependency checked in the flat layer is byte-identical to its counterpart in the canonical source TAR.
8. The 12-page synopsis PDF was rendered to images and visually inspected; notation and page geometry displayed normally. The canonical PDF preflight later reported that all 12 pages stayed within their media boxes.

## 4. Method

The review followed the packet's evidence rule: reconstruct the analytic argument first, then run its supplied program within the stated evidence boundary.

The common model was reconstructed independently from the path table. With E-set `R`, E fractions `q_i`, demands `d_i`, `h_i=d_i q_i`, and `ell_i=d_i(1-q_i)`, the four C-minus-E trunk supports are

- `I1={a1,a2,a3}`;
- `I2={a1,a2,a3,a4,a5}`;
- `I3={a2,a3,a4,a5}`;
- `I4={a3,a4}`.

Thus the trunk deviation is

`Delta_a(R) = sum_{i notin R, a in I_i} h_i - sum_{i in R, a in I_i} ell_i`,

and each positive private-arc deviation is either `h_i` or `ell_i`. This yields

`M(R) <= max(1, sum_{i notin R} h_i) <= max(1,4-|R|)`,

while the all-C route has exact value `H=sum_i h_i` on `a3`. This support/orientation layer was checked before any theorem-specific reasoning because nearly every headline constant depends on it.

For the finite objects, I treated the stored certificates and the regeneration program as separate witnesses. I also wrote a fresh independent script that does not import the packet's verifier code. It reconstructs all 13 arc deviations, enumerates the threshold-graph blocker covers, recomputes the downset cover dynamic program, and checks the high-heterogeneity formulas symbolically and at exact rational instances.

## 5. Findings

### `OAI-SSUF-AR-2026-08-03-01-F01` - flattened top-level verifier entry points are not runnable

**Severity:** Moderate  
**Category:** Reproducibility / packaging  
**Mathematical impact:** None observed  
**Disposition impact:** Integrated packet requires repair

`05_REPRODUCTION/verify_all.py` sets

- `ROOT` to the flat packet root,
- `VERIFICATION = ROOT / "verification"`,
- `RB003 = ROOT / "research" / ...`, and
- `FIXED_GADGET = ROOT / "research" / ...`.

Those repository-layout directories are absent from the flattened packet. Direct execution exits with `FileNotFoundError` for the missing `verification` directory.

Likewise, `05_REPRODUCTION/verify_fixed_gadget_proof_map.py` looks for
`ROOT/research/fixed_gadget_scenario_cover/FULL_PROOF_REVIEW_MAP.md`, while the delivered file is under `02_PROOF_MAP/`. It exits with `RuntimeError: full-proof review map is missing`.

This is confirmed to be a flat-layer wiring defect rather than a verifier or mathematical defect: after safely extracting the canonical source TAR, the native proof-map authenticator passed, and the canonical `scripts/verify_all.py` completed with `FULL VERIFICATION PASS`.

**Smallest repair:** add packet-specific entry points whose paths target `02_PROOF_MAP/`, `03_CONTROLLING_PROOFS/`, and the lane directories under `05_REPRODUCTION/`; then add a packaging smoke test that extracts the final ZIP into an empty directory and runs both top-level commands.

### `OAI-SSUF-AR-2026-08-03-01-F02` - reviewer-facing navigation is not completely self-contained

**Severity:** Low  
**Category:** Exposition / packaging  
**Mathematical impact:** None observed

`02_PROOF_MAP/DEPENDENCY_MAP.md` references
`scenario_cover/R3B_V2_REPRODUCTION_SCOPE.md`, but that file is not exposed in the flattened packet. It is present inside the canonical source TAR. The GM-004 proof similarly references the noncontrolling `BASELINE_CONTEXT_AND_DEPENDENCIES.md` and its graph SVG, which are source-archive-only.

All dependencies needed to reconstruct the reviewed analytic proofs were available, so this did not block the review. Still, the flat navigation layer should either expose these referenced files or explicitly label each reference as “canonical source archive only.” The R3B scope file is the clearest candidate for exposure because it appears as its own row in the dependency map.

### `OAI-SSUF-AR-2026-08-03-01-F03` - two-scenario notation drifts across the integrated corpus

**Severity:** Low  
**Category:** Editorial / notation  
**Mathematical impact:** None observed

The global notation document uses `beta_G^(m,+)(kappa)`, and the claim ledger states GM-008 with `beta_G^(2,+)(kappa)`. GM-004 and GM-008/009 use `beta_G^(2sc)(kappa)`. Most visibly, `SCENARIO_COVER_DUALITY.md` defines the local quantity as `beta_G^(2,+)(kappa)` and ten lines later states its corollary using `beta_G^(2sc)(kappa)`.

Context makes the intended object clear: exactly two coordinatewise strictly positive scenarios, each with condition number at most `kappa`. The symbols should nevertheless be normalized, ideally to the general convention `beta_G^(m,+)(kappa)` with `m=2`.

### Mathematical findings

No mathematical finding was opened. I found no exact counterexample, failed inequality, unhandled endpoint, or unresolved imported lemma in the selected lanes.

## 6. Claim-by-claim reconstruction

### 6.1 GM-002 / GM-003 - one arbitrary legal scenario

**Claim reconstructed:** the fixed-gadget supremum over one legally realizable nonnegative arc-cost scenario is

`L = (299 - 41 sqrt(41))/32 = 1.139747070789...`,

and every other strictly positive threshold cell is at most `9/8`.

**Positive lane.** For strictly positive differences, normalizing by `B=k dot q` gives positive weights `w_i=k_i/B` with `sum q_i w_i=1`; feasible E-sets are exactly the positive threshold downset `w(R)<=1`. A feasible E-triple immediately yields a route of value at most one. If every E-pair is feasible, the complementary all-C-pairs/no-C-singleton cell invokes the fixed-support lemma and has exact supremum `L`.

In the remaining branch, minimal infeasible E-sets form a blocker hypergraph. The strict inequality `w(T)>1` yields a fractional matching optimum strictly below one. LP duality supplies a blocker cover `y` with `q dot y<1`. The secondary `sum y_i` tie-break makes the selected extreme cover coordinatewise undominated. Integral covers directly produce a feasible route of value at most one.

I independently enumerated the threshold-graph cases on up to four labels. The isomorphism counts are `1,1,2,4,8`, totaling the 16 rows in the appendix. Exact active-set enumeration reproduced every nonintegral undominated cover listed there. The separated `K4` row contains the expected fractional covers and is correctly sent to the already-solved all-pairs theorem.

The four graph-specific routing lemmas then match the fractional cover types: a half-cover on three labels, the all-half cover with total E mass at most two, exactly three feasible singletons with no feasible edge, and a feasible triangle with an isolated singleton. I checked their reductions, monotonicity scalings, label cases, convex combinations, and boundary maxima. Each gives at most `9/8`.

**Signed and zero strata.** The private-arc realization lemma legally realizes every signed vector using nonnegative commodity-independent arc costs. Routing all nonpositive coordinates E reduces the remaining search to a positive threshold family on at most three labels. The single-generator, two-pair, all-pairs chain/nested, and cost-free arguments give at most `9/8`, with the zero vector exactly `4/5`. These bounds are strictly below `L`.

**Independent algebra:** for `f(q)=q^2(4-q^2-2q)`, the admissible stationary point is `q*=(sqrt(41)-3)/4`; exact substitution gives `f(q*)=L` and a negative second derivative. The fresh blocker-cover enumeration and the supplied one-scenario suites both passed.

**Disposition:** `ACCEPT_AS_STATED`. GM-002 is correctly phrased as a supremum-only statement; no finite attainment conclusion is inferred.

### 6.2 GM-004 / RB-003 - exactly two positive scenarios

A feasible E-pair gives a complementary two-C route of value at most two, so a value above two requires every E-pair to be blocked by at least one scenario. The two-colour fractional-matching lemma forces at least three singletons to be commonly feasible.

If all four singletons are feasible, a triangle-free blocked-pair graph for one scenario is a subgraph of a star; two stars cannot cover `K4`, so one scenario contains a blocked triangle and the complementary feasible singleton has value at most two. If exactly three singletons are feasible, the blocker core is forced to be a star at the unique non-omittable terminal plus a triangle on the other three terminals.

When the non-omittable terminal is central, the exact allocation envelope is

- `H <= 1+3 Delta` for `0<=Delta<=1/2`;
- `H <= 1+4 Delta-2 Delta^2` for `1/2<=Delta<=1`.

Therefore

`t=H-Delta <= 17/8 - 2(Delta-3/4)^2 <=17/8`.

The outer non-omittable branch is at most two. Equality at `17/8` would force `Delta=3/4` and `h_u=1`, hence `q_u=d_u=1`, contradicting strict blocking of singleton `u`; thus the supremum is not attained.

For rational `0<epsilon<1/4`, the stated star-triangle family has common feasible E-sets exactly `empty,{1},{3},{4}` and exact objective `17/8-3 epsilon`. I independently recomputed all four route values at four rational epsilon values, including `1/1000`.

**Disposition:** `ACCEPT_AS_STATED`.

### 6.3 GM-005 - exactly three positive scenarios

If every singleton E-set is blocked, assign each singleton to a blocking scenario. After normalizing each scenario, every assigned group's `h`-mass is strictly below one, so `H<3` and the all-C route has value below three.

If a singleton `{r}` is feasible, its route value is at most three. Equality would force `d_i=q_i=1` for all `i != r`; the complementary E-triple is then weakly feasible in every scenario and has value at most one. Hence every finite legal instance has value strictly below three.

The rational lower family with unit demands, `q_i=1-1/n`, and three scenarios heavy on terminals 1, 2, and 3 has common feasible E-sets exactly `empty` and `{4}`. The latter has exact value `3(1-1/n)`, approaching three. Fresh exact checks at `n=2,3,4,7,101` and the supplied replay through `n=1000` passed.

**Disposition:** `ACCEPT_AS_STATED`.

### 6.4 GM-006 - four or more positive scenarios

The all-C route gives the universal upper bound `H<=4`. Four heavy-coordinate scenarios make all-C the unique common feasible routing and give exact value `4(1-1/n)`, approaching four. Duplicating scenarios preserves the construction for any `m>4`.

Finite equality at four would require `d_i=q_i=1` for every terminal. The full E-set would then tie every scenario budget and have zero deviation, contradicting an instance value of four. Exact lower-family checks passed.

**Disposition:** `ACCEPT_AS_STATED`.

### 6.5 SC-000 / SC-001--003 - duality and the fixed finite atlas

For a C-set `S`, let `v_S=1_S-p`. A positive scenario accepts `S` exactly when `k dot v_S>=0` and eliminates it exactly when `k dot v_S<0`. Therefore a target `t` is forced exactly when all routes with `M(S)<t` are covered by the union of the scenarios' strict losing downsets. This proves the scenario-cover equivalence directly.

The closure-to-strictness lemma is valid: after normalizing positive normals by `min k_i=1`, a weak boundary minimizer can be mixed with a strict realizer, preserving the condition bound and approaching the weak infimum. It does not falsely claim endpoint attainment.

For the fixed rational RB witness, I independently enumerated all `2^16` set families and recovered exactly 168 downsets. Reading the 59 stored realizable positive-normal masks, a fresh union-cover dynamic program reproduced the distribution

`0:1, 1:61, 2:91, 3:13, 4:1, impossible:1`

and the unrestricted fixed-instance ladder

- one scenario: `561/500`;
- two scenarios: `1061/500`;
- three scenarios: `2123/1000`;
- four scenarios: `359/125`.

The full atlas regenerated byte-identically and its exact certificates and mutation tests passed.

**Disposition:** `ACCEPT_AS_STATED`.

### 6.6 SC-006 - continuum phase theorem on the fixed RB family

Using

`p_epsilon=(1/4+epsilon, epsilon, 1/2, 1/4+epsilon)` and `d=(1,1,3/4,1)`,

I reconstructed all five trunk and eight private deviations. For every one of the 16 C-sets, the stated affine route value dominates all 13 deviations throughout `0<=epsilon<=1/8` and is attained by at least one arc. This independently confirms the route table and its only interior crossing at `epsilon=1/16`.

The three condition thresholds are

- `A=(3-4 epsilon)/(1+2 epsilon)`;
- `B=1/epsilon-2`;
- `C=2/epsilon-2`.

The first obstruction proves route `14` cannot be eliminated at or below `A`. The middle pigeonhole argument shows that one bounded scenario eliminating two of `13,14,34` must have condition number strictly greater than `B`. The third obstruction proves `134` cannot be eliminated at or below `C`. The displayed equal, triangle, and star scenarios realize the successive upper branches strictly above those thresholds.

The unrestricted ceiling is also valid: one scenario cannot eliminate both `134` and `124`; any scenario eliminating either triple necessarily accepts `23`. Two scenarios therefore cannot cover all three required routes. The transition points correctly belong to the lower branch because the newly required route ties the budget and weak feasibility preserves it.

The resulting four phases are exactly

- `9/8-3 epsilon` for `1<=kappa<=A`;
- `9/8-2 epsilon` for `A<kappa<=B`;
- `15/8-3 epsilon` for `B<kappa<=C`;
- `17/8-3 epsilon` for `C<kappa`.

The supplied symbolic verifier, full exact replay at 13 epsilon values, and strictness/endpoint mutation tests passed.

**Disposition:** `ACCEPT_AS_STATED`.

### 6.7 GM-008 / GM-009 - bounded heterogeneity and exact high-`kappa` tail

The proof correctly imports only the RB-003 reduction needed in a value-above-two branch: every noncentral branch is already at most two. In the central star-triangle branch, with non-omittable central E fraction `q` and total remaining E mass `S`, strict blocking gives

`S < min{kappa(1-q), 2-q/kappa}`.

The star inequality follows from blocking the central singleton. The triangle inequality follows from exact fractional-knapsack minimization under blocked A-pairs and the condition-number bound.

Under the necessary guard `t>2`, the feasible singleton route formulas imply the exact allocation bound

`H <= q + min{x,Delta} + min{y,Delta} + Delta z`,

where `x,y` are outer E fractions, `z` is the remaining central E fraction, and `Delta=H-t`. The packet correctly records a legal counterexample showing this inequality is false without the `t>2` guard.

The first and third allocation regimes force `t<2`. In the middle regime,

`t <= q + (1+S)^2/8`.

Maximizing over the strict star/triangle bound yields

`Q_kappa=kappa(kappa-2)/(kappa^2-1)`,

`S_kappa=kappa(2kappa-1)/(kappa^2-1)`,

and

`F(kappa)=Q_kappa+(1+S_kappa)^2/8`.

I independently verified

`F(kappa)-2 = P(kappa)/[8(kappa-1)^2(kappa+1)^2]`,

with `P(kappa)=kappa^4-22kappa^3+19kappa^2+18kappa-15`, the stated derivative formula and positivity for `kappa>=2`, and exactly one real root above two:

`kappa_0=21.058780922898283...`.

The strict lower sequence has common feasible E-sets exactly `empty,{1},{3},{4}`. Fresh exact checks at six rational kappa values, from `21/10` through `30`, reproduced the three equal singleton route values, the larger all-C value, and convergence to `F(kappa)`.

Consequently the proof supports

- `beta<=2` for `1<=kappa<=kappa_0`;
- `beta<=max{2,F(kappa)}` for `kappa>2`;
- `beta=F(kappa)` for `kappa>=kappa_0`.

The exact curve below `kappa_0` remains explicitly open, as it should.

**Disposition:** `ACCEPT_AS_STATED`.

## 7. Integrated consistency checks

The integrated synopsis, proof map, and controlling sources use the same fixed graph, two designated paths per terminal, normalization `max d_i=1`, and weak feasibility / strict blocking convention. C-set and E-set orientations are complementary and remain algebraically consistent across the lanes.

Cross-lane numerical and limiting checks are coherent:

- `9/8 < L < 17/8 < 3 < 4` where applicable to their distinct cells/scenario counts;
- the fixed atlas values stay below the corresponding global fixed-gadget suprema;
- the SC-006 unrestricted fixed-family branch tends to `17/8` as `epsilon` tends to zero;
- the high-`kappa` global tail tends to `17/8` as `kappa` tends to infinity;
- GM-005's finite `n=4` instance gives `9/4`, above the two-scenario constant but below the three-scenario supremum;
- endpoint ties are consistently treated as feasible throughout.

The scope ledger is conservative. The packet does not convert a fixed-instance atlas into a global theorem, SC-006 into the global bounded-heterogeneity curve, or the fixed-gadget ladder into an unrestricted planar constant.

## 8. Computations run

### Packet-level

- recomputed ZIP SHA-256 and compared it with the sidecar;
- validated all 71 internal manifest entries;
- validated the canonical source TAR and all three adjacent PDFs;
- authenticated all eight controlling proof hashes and line counts;
- compared flat controlling proofs and dependencies with canonical-source copies;
- rendered and inspected the 12-page synopsis PDF.

### Supplied lane-level programs

All completed successfully when invoked from their included lane directories:

- `verify_global_one_scenario_theorem.py`;
- `symbolic_every_pair_check.py`;
- `verify_arc_envelope.py`;
- `verify_gm005_exact.py`;
- `mutation_tests_gm005.py`;
- `verify_scenario_ladder.py`;
- `verify_high_kappa.py`;
- `verify_scenario_cover_results.py` before and after regeneration;
- `canonicalization_tests.py`;
- `mutation_tests.py`;
- `scenario_cover_atlas.py`;
- `verify_sc006_symbolic.py`;
- `replay_sc006_exact.py --full`;
- `mutation_tests_sc006.py`.

The regenerated `SCENARIO_COVER_ATLAS_RESULTS.json` was byte-identical to the committed copy.

### Fresh independent program

`ssuf_independent_adversarial_checks.py`, written during this review without importing packet verifier code, passed all of the following:

- symbolic domination and witnesses for all 16 SC-006 route values over the whole epsilon interval;
- exact RB-003 feasible family and lower-route values at four rational epsilon values;
- exact GM-005/006 lower families at five values of `n`;
- high-`kappa` rational identity, derivative, root count, and six exact lower-family samples;
- exhaustive threshold-graph blocker-cover classification;
- independent 168-downset count, 59-pattern cover DP, cover-number distribution, and fixed-instance ladder;
- exact one-scenario stationary point and value `L`.

### Canonical native-layout replay

After safe extraction of the embedded source TAR, the native `scripts/verify_all.py` completed with `FULL VERIFICATION PASS`. This included the base one-scenario certificate regeneration, fixed-gadget suites, byte-identical atlas regeneration, deterministic RB-003 replay, source/provenance checks, and all PDF text/geometry preflights.

### Environment

The review execution environment was:

- Python `3.13.5`;
- SymPy `1.14.0`;
- NumPy `2.3.5`;
- SciPy `1.17.0`;
- NetworkX `3.6.1`.

The packet pins NetworkX `3.5`; that exact wheel was not available from the execution environment's package index. Every other pinned Python package matched, all exact outputs regenerated, and the full suite passed under NetworkX `3.6.1`. This version variance is disclosed rather than treated as exact environment reproduction.

## 9. Files read

The review included:

- `00_READ_ME_FIRST.md`, the reseal note, package scope, review prompt, claim ledger, dependency map, limitations, model/notation, and full-proof map;
- the rendered synopsis PDF and its source-level scope statements;
- all eight controlling analytic proof files for GM-002/003, GM-004, GM-005, GM-006, the shared arc envelope, SC-000, SC-006, and GM-008/009;
- all listed one-scenario imported-baseline dependencies, the finite blocker-cover classification, routing allocation details, the GM-005 model specification, and the bounded-heterogeneity dependency specification;
- all included reproduction programs relevant to the selected lanes;
- the canonical source equivalents needed to authenticate the flat copies and run the native verification suite.

## 10. Not reviewed or not certified

This review does **not** determine or certify:

- novelty, priority, literature completeness, citation overlap, or independence from prior art;
- the unrestricted planar SSUF constant or topology-wide sharpness;
- the exact bounded-heterogeneity curve below `kappa_0`;
- the unclaimed F064 matching upper bound;
- authorship, acknowledgements, licensing, rights, release authority, or publication readiness;
- journal-level exposition quality beyond the specific findings above;
- an external human-review status;
- any theorem for signed or zero-coordinate multi-scenario vectors not expressly claimed;
- any graph or designated-path system other than the fixed 13-arc four-terminal gadget.

## 11. Final record

**Claim-level mathematical result:** all reviewed lanes `ACCEPT_AS_STATED`.  
**Integrated result:** `ACCEPT_WITH_EDITORIAL_REPAIRS`.  
**Blocking mathematical objections:** none found.  
**Required repairs before recirculating this exact handoff ZIP:** repair the two flat top-level runners, expose or qualify the R3B scope reference, and normalize two-scenario notation.

---

Private review record. This document does not authorize publication, attribution, external contact, repository mutation, release, or reuse beyond the sender's separate permission.
