# Reproducibility Record — Positive-Difference Fixed-Topology SSUF

This is a deterministic **internal replay record**, not a claim that an
external party has reproduced the result.

## Repository identity

- Repository: `matthewprotti/planar-ssuf-four-terminal-bound`
- Base commit: `087204eda4cc490cb59dd1988d7383c406288d2e`
- Reviewed implementation commit: `e3becc5e36a20dcf152f17fa350b4110b9e0eb3b`
- Research directory: `research/unequal_cost_fixed_topology`
- Original public release used only as provenance: `v0.1.0`
- Released TeX pin: `paper/ssuf_four_terminal_note_v5.tex`, SHA-256
  `3b9c5963ad2da2cbaa99621202e5b50ad3c2525f2bb5f6fdf7f649568c3e1154`

## Clean clone

```bash
git clone https://github.com/matthewprotti/planar-ssuf-four-terminal-bound.git
cd planar-ssuf-four-terminal-bound
git checkout --detach e3becc5e36a20dcf152f17fa350b4110b9e0eb3b
test -z "$(git status --porcelain)"
python -m venv .venv
. .venv/bin/activate
python -m pip install -r research/unequal_cost_fixed_topology/requirements-replay.txt
python research/unequal_cost_fixed_topology/round2_replay.py
```

Expected exit code: `0`.

## Environment and dependency boundary

- Replay platform: Ubuntu 24.04 GitHub-hosted runner.
- CPython: `3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0]`.
- SymPy: `1.14.0`.
- mpmath: `1.3.0`.
- Container digest: none supplied; exact Python dependencies and committed
  source hashes are pinned instead.
- Network during mathematical replay: **not required**. The replay consumes
  only committed files; the installation step may require package-index access
  unless dependencies are already cached.
- Known platform sensitivity: temporary directory names appear only in captured
  stdout tails, not in mathematical output hashes.

## One-command replay stages

`round2_replay.py` copies the research directory to a disposable directory and:

1. verifies the committed source manifest;
2. regenerates the 168-family threshold census;
3. runs the separately written census checker;
4. reconciles the 168=149+18+1 and 149=54+1+94 partitions and all orbit sizes;
5. runs the pinned SymPy identity audit;
6. runs the CAS-independent rational/Laurent/\(\mathbb Q(\sqrt{41})\) audit;
7. compares the local lower-family definition with the pinned release
   extraction without reading the released paper at runtime;
8. generates human-readable witnesses; and
9. validates theorem IDs, counts, partitions, group actions, result schemas,
   and provenance pins.

## Expected identities

- Artifact manifest SHA-256:
  `0981594f69a8d8048b44b7c92dc1a456ceb0df95950405ffe0b3ec87b40e8215`.
- Workflow replay run: `30140273295`.
- Workflow result: every step completed successfully; the resulting
  implementation commit is the reviewed commit above.
- Generated output SHA-256 values:
  - census reconciliation: `0db74d10fa656e47ace23173d40a1df0f0b68b97d4e7ea291d8199bbc4367264`;
  - exact no-CAS algebra: `877dd3621b1dee96bb74953643daccd8242dbed9f7d50b0d54b2930aed4ffc30`;
  - separate census: `6a6e83e2d076933264f8417430493f5ccbdbf5a5aca1238e0f2398c96431ce3b`;
  - release-family comparison: `d534f47a0c23c3ed35f2ab9531ac257ace23fda001d0946e3226b59d3286c91e`;
  - SymPy audit: `7c5b7e3c09e72fe266ff778833025c3bf96a7697b8bf667baad39785e5727145`;
  - threshold census: `8c2ebf27e5aeacf1a29bfa9ea306fda542e73627c4acd812cbf54407c3dfbb9e`;
  - witness examples: `122595ef2e2a64bfbbed8adb985aa8ba45744d9dfd8d4cc1682ac0357fcbd643`.

## Production-boundary check

The implementation diff from the base commit is restricted to
`research/unequal_cost_fixed_topology/`. The temporary workflow that performed
the replay removed itself before the implementation commit. No released paper,
released verifier, package dependency, build path, or deployment configuration
is modified by that implementation commit.

## Unsuccessful or excluded checks

- Zero and negative route-cost differences are outside the theorem domain and
  are not normalized away.
- The 94 remaining labeled cells and their boundaries are not optimized.
- SymPy does not establish unstated sign or branch conditions; those remain in
  the human proof and are mirrored by exact gap identities where stated.
- The pinned lower-family extraction is compared exactly but was transcribed
  from the released TeX by a human.
- No external clean-environment reproduction has yet been recorded.

## Forward-pass commands

The one-command replay now additionally runs:

```bash
python exact_open_cell_witnesses.py
python signed_difference_census.py
```

Both use exact integer/rational set arithmetic and require no network. The signed
census classifies feasibility systems only; it does not replay a signed-objective
optimization theorem.
