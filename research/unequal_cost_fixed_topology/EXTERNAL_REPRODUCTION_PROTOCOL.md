# External Clean-Environment Reproduction Protocol

This protocol is ready for a third party. Completing it is external work; the
branch claims only deterministic internal replay.

## Record to return

- repository and exact detached commit SHA;
- operating system, architecture, Python version, SymPy version, and mpmath version;
- dependency-install transcript;
- clean-worktree checks before and after replay;
- whether network access was disabled during replay;
- replay exit code;
- SHA-256 of `artifact_manifest.json` and `round2_replay_report.json`;
- all failed, skipped, or manually altered steps; and
- reviewer identity or pseudonymous signing key, if they choose.

## Commands

```bash
git clone https://github.com/matthewprotti/planar-ssuf-four-terminal-bound.git
cd planar-ssuf-four-terminal-bound
git checkout --detach <PINNED_SSUF_COMMIT>
test -z "$(git status --porcelain)"
cd research/unequal_cost_fixed_topology
python -m pip install -r requirements-replay.txt
python round2_replay.py
sha256sum artifact_manifest.json round2_replay_report.json
test -z "$(git -C ../.. status --porcelain)"
```

Expected exit code: `0`. The replay needs no network after dependency
installation. For a stricter offline run, prepare and hash a local wheelhouse,
then install with `--no-index --find-links` before disabling network access.

A successful run may be described as external reproduction of the deterministic
finite and algebraic replay at the pinned commit. It is not independent human
verification of the written inequalities, novelty clearance, or acceptance of
the remaining 83-cell conjecture.
