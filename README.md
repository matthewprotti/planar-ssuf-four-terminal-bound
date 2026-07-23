# A four-terminal planar lower bound for cost-preserving unsplittable-flow rounding

> **Unpublished private release candidate — v0.1.0-rc1 — 23 July 2026**
>
> This repository is currently a private provenance record. It is not yet a
> public priority disclosure and has not been peer reviewed.

This project studies the planar cost-preserving additive-congestion constant
for single-source unsplittable-flow rounding. The manuscript proves:

1. an attained exact finite certificate
   \[
   \frac{335}{294}=1.139455782312\ldots;
   \]
2. a rational family yielding
   \[
   \alpha_{\mathrm{pl}}\ge
   L:=\frac{299-41\sqrt{41}}{32}
   =1.139747070789\ldots;
   \]
3. that the same value \(L\) is sharp for a precisely defined,
   fixed-topology, equal-full-cost, two-cheap-choice model.

The third item is a restricted-model result. It is not a claim that \(L\) is
the exact unrestricted planar constant, is optimal among all four-terminal
planar instances, or remains sharp when full expensive-route costs may be
unequal.

## Verification

The finite certificate is checked by exact arithmetic over all 16
unsplittable routings and all 13 arcs. The supplied verification suite also
checks the graph, embedding certificate, path structure, flow conservation,
cost forcing, symbolic family, radical optimization, restricted-model
identities, and representative failure mutations.

`verification/independent_crosscheck.py` is a separate clean-room
implementation prepared in a different Codex execution context. It discovers
the graph properties and paths with NetworkX, re-encodes the exact and
symbolic checks, and runs deterministic stress tests. It is useful
corroboration, but it is not an independent human review and its randomized
stress test is not a proof.

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r verification/requirements.txt
python scripts/verify_all.py
```

Expected headline values include:

- fractional cost `31751`;
- three-expensive-choice cost `31752`;
- 11 cost-feasible routings out of 16;
- exact minimum maximum overload `335`;
- maximum demand `294`;
- finite ratio `335/294`;
- restricted-model value
  `(299 - 41*sqrt(41))/32 = 1.139747070789...`.

The manuscript is intended to be human-checkable without software. The
software is corroborating evidence, not a substitute for proof.

## Repository contents

- [`paper/ssuf_four_terminal_note_v5.pdf`](paper/ssuf_four_terminal_note_v5.pdf):
  current unrefereed manuscript.
- [`paper/ssuf_four_terminal_note_v5.tex`](paper/ssuf_four_terminal_note_v5.tex):
  LaTeX source.
- [`verification/`](verification/): exact verifiers, exhaustive routing table,
  separate cross-check, mutation tests, and machine-readable output.
- [`scripts/`](scripts/): one-command verification, PDF build, manifest, and
  deterministic release-archive tooling.
- [`PRIORITY_DISCLOSURE.md`](PRIORITY_DISCLOSURE.md): concise statement of the
  proposed public claims and non-claims.
- [`LIMITATIONS.md`](LIMITATIONS.md): scope, review, novelty, and reproducibility
  limitations.
- [`AI_USE_AND_PROVENANCE.md`](AI_USE_AND_PROVENANCE.md): detailed AI-use
  disclosure and chronology.
- [`LICENSING.md`](LICENSING.md): the deliberate no-license status of this
  release candidate.

## Build the manuscript

The checked PDF was built with Tectonic 0.16.9. Poppler's `pdftotext` is used
for text preflight checks.

```bash
python scripts/build_pdf.py
python verification/preflight_pdf_text.py
```

`scripts/build_pdf.py` writes temporary TeX products outside the source tree
and then replaces only the checked PDF. It also supports `pdflatex` when
Tectonic is unavailable.

## Novelty and contemporaneous context

The work began after
[Dmitry Rybin's public post of 22 July 2026](https://x.com/dmitryrybin1/status/2079904005652893709)
announcing a counterexample to Goemans' cost conjecture. Targeted web, paper,
and public-GitHub searches performed on 23 July 2026 did not locate the exact
four-terminal support pattern, the `335/294` certificate, the displayed
radical in this setting, or the restricted-model theorem. That is a
good-faith search result, not exhaustive novelty clearance and not a claim
against private, unindexed, or concurrent work.

The current planar upper-bound reference is the 2026 journal article
[Single-source unsplittable flows in planar and bounded-genus graphs](https://doi.org/10.1007/s10107-026-02365-x).
The graph used here lies outside the series-parallel positive class treated
in [Integer and unsplittable multiflows in series-parallel digraphs](https://doi.org/10.1007/s10107-026-02392-8).

## Publication and citation

Repository creation and private commits provide private provenance, not a
public priority date. If publication is approved, the canonical public
timestamp will be the server-recorded `published_at` time of a new immutable
GitHub release. No tag or release has been created yet.

Please do not cite the moving private candidate. After publication, cite the
immutable `v0.1.0` release and its exact commit.

## Author

Matthew Protti

No institutional affiliation or intellectual-property ownership claim is
asserted in this release candidate. See [`LICENSING.md`](LICENSING.md).
