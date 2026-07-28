# Reproducibility Record — Positive-Difference Fixed-Topology SSUF

This is a deterministic **internal replay record**, not a claim that an
external party has independently reproduced or verified the mathematics.

## Repository identity

- Repository: `matthewprotti/planar-ssuf-four-terminal-bound`
- Reviewed commit: the exact commit checked out by the reviewer
- Research directory: `research/unequal_cost_fixed_topology`
- Original public release used only as provenance: `v0.1.0`
- Released TeX pin: `paper/ssuf_four_terminal_note_v5.tex`, SHA-256
  `3b9c5963ad2da2cbaa99621202e5b50ad3c2525f2bb5f6fdf7f649568c3e1154`

Record the reviewed commit before running:

```bash
git rev-parse HEAD
```

## Clean-clone replay

Replace `<REVIEWED_COMMIT>` with the commit being reviewed.

```bash
git clone https://github.com/matthewprotti/planar-ssuf-four-terminal-bound.git
cd planar-ssuf-four-terminal-bound
git checkout --detach <REVIEWED_COMMIT>
test -z "$(git status --porcelain --untracked-files=all)"
python -m venv .venv
. .venv/bin/activate
python -m pip install -r research/unequal_cost_fixed_topology/requirements-replay.txt
python research/unequal_cost_fixed_topology/round2_replay.py
python research/unequal_cost_fixed_topology/replay_determinism_test.py
test -z "$(git status --porcelain --untracked-files=all)"
```

Both commands have expected exit code `0`. They are check-only by default:
neither command rewrites the committed canonical report or any generated result
in the source checkout.

## What the replay checks

`round2_replay.py` copies the research directory to a disposable directory and:

1. checks the committed research-source manifest;
2. runs the complete finite census, independent census, and reconciliation;
3. runs the symbolic and CAS-independent exact algebra audits;
4. compares the local lower family with the pinned release extraction;
5. generates and verifies exact open-cell witnesses;
6. runs the signed, nonpositive, grid, cost-free, and positive-clique checks;
7. validates theorem IDs, counts, partitions, group actions, schemas, and pins;
8. compares the canonical replay bytes with `round2_replay_report.json`;
9. checks that the root SHA-256 manifest is current and that every research file
   is in the deterministic source-archive input; and
10. checks the Git worktree before and after replay.

`replay_determinism_test.py` repeats the full replay below two distinct
temporary roots. It requires byte-identical canonical JSON and rejects
temporary-directory and interpreter paths in those bytes.

The replay needs no network after dependency installation. It requires Python
3.11 or later, SymPy 1.14.0, and mpmath 1.3.0.

## Canonical result and optional attestation

`round2_replay_report.json` is the committed canonical result. It contains only
deterministic commands, exact counts, source and generated-output hashes,
limitations, and fixed runtime requirements. It deliberately excludes
timestamps, operating-system details, temporary paths, interpreter paths, and
stdout/stderr hashes.

Host metadata and command-stream hashes can be recorded separately in an
explicit, noncanonical attestation. Its path must be outside the repository:

```bash
attestation_file="$(mktemp "${TMPDIR:-/tmp}/ssuf-attestation.XXXXXX.json")"
python research/unequal_cost_fixed_topology/round2_replay.py \
  --attestation "$attestation_file"
printf '%s\n' "$attestation_file"
```

The attestation is diagnostic evidence, is marked `must_not_be_committed`, and
is not part of the canonical hash identity.

## Maintainer regeneration

The normal replay never updates tracked files. After an intentional source
change, a maintainer can regenerate the two committed deterministic manifests
and canonical report in this order:

```bash
cd research/unequal_cost_fixed_topology
python build_artifact_manifest.py
python round2_replay.py \
  --write-canonical \
  --skip-git-clean-check \
  --skip-release-membership-check
cd ../..
python scripts/manifest.py --write
```

The skip flags are limited to this preparation step. Commit the intended files,
then run the clean-clone replay commands without skip flags.

## Current exact replay state

- 168 labeled monotone families;
- 149 realizable strictly positive threshold families;
- 94 labeled cells after the original singleton/every-pair reduction;
- 79 remaining strictly positive labeled cells after the proved reductions;
- 11 remaining arbitrary-label search orbits;
- 11 exact strictly-above-one interior witnesses;
- 1,881 unique signed unate threshold families;
- all non-all-positive sign/zero strata at most `9/8`; and
- the identically zero cost-difference stratum exactly `4/5`.

## Evidence boundary and nonclaims

- Human-readable theorems carry the proofs; software is corroboration.
- The 79 remaining strictly positive labeled cells and their boundaries remain
  open.
- The pinned lower-family extraction is compared exactly but was transcribed
  from the released TeX by a human.
- The theorem is fixed-topology only.
- A successful internal replay is not independent human verification, novelty
  clearance, peer review, or external clean-environment reproduction.
