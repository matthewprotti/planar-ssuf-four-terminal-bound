# The proper hat-guessing number of `K5-e`

> **Public research disclosure v0.1 (2 September 2026)**  
> **Status:** theorem proved in the manuscript and executable package; independent review pending.

## Result

Let `K5-e` be the complete graph on five vertices with one edge removed. Then

\[
\boxed{\mathrm{HG}_{P}(K_5-e)=8}.
\]

This resolves the five-vertex instance of the `K_n-e` problem posed in *Hat guessing with proper colorings* (Adriaensen et al., arXiv:2603.04909v4).

The upper bound is the general inequality

\[
\mathrm{HG}_{P}(G)\le |V(G)|+\chi(G)-1.
\]

The lower bound uses an explicit construction over `F_2^3`. Two nonadjacent twin players cover part of every proper coloring. The residual-coloring/local-view incidence graph has left degree three and right degree at most three, so Hall's theorem supplies consistent guesses for the three clique players.

## Trusted proof core

The conceptual proof reduces to:

1. seven explicit choices of `delta(U)` for the seven two-dimensional subspaces of `F_2^3`;
2. 42 direct evaluations showing that seven maps `phi_w` are fixed-point-free permutations; and
3. a degree-count proof of Hall's condition.

The compact verifier reconstructs a residual saturating matching and the complete 6,720-entry strategy, then checks all 8,400 proper eight-colorings. Those computations are redundant verification layers rather than premises of the conceptual proof.

## Verify

Only the Python standard library is required:

```bash
python3 code/verify_k5e_fano_hall.py \
  certificates/K5_e_q8_fano_delta.json
```

## Files

- `preprint/proper_hat_guessing_K5_minus_e_v0.1.pdf` - review-pending manuscript.
- `preprint/proper_hat_guessing_K5_minus_e_v0.1.tex` - LaTeX source.
- `THEOREM.md` - self-contained theorem proof in Markdown.
- `GENERAL_KNE_REDUCTION.md` - reusable twin-completion lemma for `K_n-e`.
- `AI_USE_AND_PROVENANCE.md` - contribution and AI-use disclosure.
- `REVIEW_REQUEST.md` - compact independent-review checklist.
- `NOVELTY_SEARCH_20260902.md` - same-day targeted landscape search record.
- `code/verify_k5e_fano_hall.py` - dependency-free constructor/verifier.
- `certificates/K5_e_q8_fano_delta.json` - seven-entry compact certificate.
- `release/HGP_K5E_PUBLIC_DISCLOSURE_20260902_v0.1.zip` - complete frozen disclosure.

## Scope

This release proves only the exact value for `K5-e` and a general sufficient twin-completion lemma. It does **not** solve the full `K_n-e` family, determine `HG_P(C5)`, claim peer review, or claim exhaustive novelty clearance.

## Citation

Until an archival DOI is assigned, cite the exact public commit containing this versioned disclosure.