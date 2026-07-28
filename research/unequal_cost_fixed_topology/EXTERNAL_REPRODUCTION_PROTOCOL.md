# External Clean-Environment Reproduction Protocol

This protocol is ready for a third party. Completing it is external work; the
branch itself claims only deterministic internal replay.

## Record to return

- repository and exact detached commit SHA;
- operating system, architecture, Python version, SymPy version, and mpmath
  version;
- dependency-install transcript;
- clean-worktree checks before and after replay;
- whether network access was disabled during replay;
- replay and two-root identity-test exit codes;
- SHA-256 of `artifact_manifest.json` and `round2_replay_report.json`;
- optional external attestation SHA-256;
- all failed, skipped, or manually altered steps; and
- reviewer identity or pseudonymous signing key, if they choose.

## Commands

Replace `<REVIEWED_COMMIT>` with the exact commit being reviewed.

```bash
git clone https://github.com/matthewprotti/planar-ssuf-four-terminal-bound.git
cd planar-ssuf-four-terminal-bound
git checkout --detach <REVIEWED_COMMIT>
git rev-parse HEAD
test -z "$(git status --porcelain --untracked-files=all)"
python -m venv .venv
. .venv/bin/activate
python -m pip install -r research/unequal_cost_fixed_topology/requirements-replay.txt
python research/unequal_cost_fixed_topology/round2_replay.py
python research/unequal_cost_fixed_topology/replay_determinism_test.py
sha256sum \
  research/unequal_cost_fixed_topology/artifact_manifest.json \
  research/unequal_cost_fixed_topology/round2_replay_report.json
test -z "$(git status --porcelain --untracked-files=all)"
```

Expected exit code: `0` for both Python checks. The replay needs no network
after dependency installation. For a stricter offline run, prepare and hash a
local wheelhouse, install with `--no-index --find-links`, and then disable
network access.

The default commands do not alter the source checkout. They verify that the
committed canonical report matches a fresh replay, that two different temporary
roots produce identical canonical bytes, and that all branch-local research
files are present in the repository manifest and deterministic source-archive
input. The reconciliation output distinguishes the historical 94-, 89-, and
83-cell stages from the current 79-cell/11-orbit frontier; the generated
open-witness atlas contains ten current cells and excludes the solved
historical F042 certificate.

## Optional noncanonical host attestation

To retain host and command-stream diagnostics, choose a path outside the clone:

```bash
attestation_file="$(mktemp "${TMPDIR:-/tmp}/ssuf-attestation.XXXXXX.json")"
python research/unequal_cost_fixed_topology/round2_replay.py \
  --attestation "$attestation_file"
sha256sum "$attestation_file"
```

The attestation is explicitly noncanonical. Its timestamp, interpreter path,
platform details, and command-stream hashes must not be compared as canonical
identity and must not be committed to the repository.

## Interpretation

A successful run may be described as external reproduction of the deterministic
finite and algebraic replay at the pinned commit. It is not independent human
verification of the written inequalities, novelty clearance, or acceptance of
the remaining 79-cell open frontier.
