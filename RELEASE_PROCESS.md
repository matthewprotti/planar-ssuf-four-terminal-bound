# Release package gates

The immutable `v0.1.0` and `v0.2.0` tags and their published assets remain
canonical historical releases. Changes on `main` must never create a different
package carrying either final version. `v0.2.1` is a new immutable correction
release; it does not rewrite `v0.2.0`.

## Candidate/dev package

Use a visibly non-final version while preparing later work:

```bash
python scripts/release_preflight.py --candidate-version 0.2.1-dev
python scripts/build_release.py \
  --mode candidate \
  --version 0.2.1-dev
```

Candidate/dev mode requires a suffix such as `-dev` or `-rc1`. It checks the
complete repository manifest before creating the archive but does not require a
tag.

## Public package

Public mode derives its version from `CITATION.cff`, requires `HEAD` to carry
the exact corresponding `v<version>` tag, requires a clean worktree, verifies
the complete manifest, and constructs and inspects the archive:

```bash
python scripts/release_preflight.py --public
python scripts/build_release.py --mode public
```

The permanent CI workflow runs the complete verification on Python 3.11 and
3.12, performs the document and package build on Python 3.12, checks
candidate/dev packaging on branches, checks public packaging on tags, and
independently rebuilds the immutable `v0.1.0` assets against their published
SHA-256 values.

Release publication is deliberately separate from verification. The permanent
workflow has read-only repository permissions and never creates tags or
releases. After an explicitly authorized release PR is merged and branch CI is
green, the human release steward creates the exact annotated tag, waits for tag
CI to pass, builds the public package from that clean tag, and publishes only
those verified assets. The former one-time `v0.2.0` write-enabled publication
workflow was retired in `v0.2.1`.
