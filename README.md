# A four-terminal planar lower bound for cost-preserving unsplittable-flow rounding

> **Status: public research disclosure (`v0.1.0`, 23 July 2026).**
>
> This is an unrefereed research package. Its claims, proof, exact data, and
> executable verifiers are provided for scrutiny and reproducibility.

## What this is

In single-source unsplittable-flow rounding, each terminal's demand must end
up on one path instead of being split across several. This project asks how
much extra load may be unavoidable when that rounding is not allowed to
increase total cost—even on an acyclic planar graph.

The short answer is that a compact four-terminal construction already forces
a nontrivial amount of extra load. The repository contains the manuscript,
the exact finite instance, and code that checks the calculations.

## Results at a glance

The manuscript establishes three related results.

### 1. An attained finite certificate

There is an explicit integer instance with maximum demand `294` for which
every cost-nonincreasing unsplittable routing has upper overload at least
`335`. The exact ratio is

$$
\frac{335}{294}=1.139455782312\ldots
$$

### 2. A limiting planar lower bound

A rational family proves

$$
\alpha_{\mathrm{pl}}\ge
L:=\frac{299-41\sqrt{41}}{32}
=1.139747070789\ldots
$$

More precisely, for every $\eta>0$, the family contains a rational instance
requiring overload greater than $(L-\eta)d_{\max}$.

### 3. A sharp result within a restricted model

The same value $L$ is the exact supremum for the fixed topology when every
full expensive choice has equal cost and cost feasibility forces at least two
cheap choices.

The third result is intentionally narrow. It does **not** say that $L$ is the
exact unrestricted planar constant, that it is optimal among all
four-terminal planar instances, or that it remains sharp when full
expensive-route costs may be unequal.

## How this came together

This project grew out of a multi-week conversation between Matthew Protti and
OpenAI GPT-5.6 Pro about recurring structural similarities across
mathematical breakthroughs and advances in frontier language models—and,
more broadly, the kinds of hard problems AI systems might help with. Dmitry
Rybin's result became the catalyst for applying that ongoing conversation to
this unsplittable-flow question.

GPT-5.6 Pro did most of the active mathematical heavy lifting: construction
search, symbolic derivation, proof development, verifier development,
adversarial critique, and manuscript preparation. Matthew framed and steered
the investigation, evaluated the proposed constructions, conducted
adversarial critique that caught a cost-normalization error, established an
adversarial-review and adjudication loop, required exact checks, chose the
scope of the claims, and accepts responsibility for the released work.

The private conversation transcript is deliberately not included. The proof,
explicit data, and executable verifiers are intended to let readers audit the
result without it. The fuller account is in the
[AI-use and provenance note](AI_USE_AND_PROVENANCE.md).

## Where to start

- Read the
  [current manuscript](paper/ssuf_four_terminal_note_v5.pdf) for the complete
  statement and proof.
- See [the priority disclosure](PRIORITY_DISCLOSURE.md) for the
  claims and non-claims in compact form.
- Run the [verification suite](verification/) to reproduce the exact and
  symbolic checks.
- Read [the limitations](LIMITATIONS.md) for the review, novelty, and
  reproducibility boundaries.

## Check the result

The central finite certificate is small enough to check exhaustively. The
primary verifier uses exact arithmetic over all 16 unsplittable routings and
all 13 arcs. The broader suite also checks the graph and embedding
certificate, path structure, flow conservation, cost forcing, symbolic
family, radical optimization, restricted-model identities, and
representative failure mutations.

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r verification/requirements.txt
python scripts/verify_all.py
```

Some useful values to compare with the output:

| Check | Expected value |
| --- | ---: |
| Fractional cost | `31751` |
| Cost of three expensive choices | `31752` |
| Cost-feasible routings | `11` of `16` |
| Minimum possible maximum overload | `335` |
| Maximum demand | `294` |
| Finite ratio | $\frac{335}{294}$ |
| Restricted-model value | $\frac{299-41\sqrt{41}}{32}$ |

There is also a separate clean-room implementation in
[`verification/independent_crosscheck.py`](verification/independent_crosscheck.py).
It rediscovers the graph properties and paths with NetworkX, independently
re-encodes the exact and symbolic checks, and runs deterministic stress
tests. Randomized stress testing is not part of the proof.

The manuscript is designed to be checked by a person without relying on the
software. The code is corroborating evidence.

## Repository map

- [`paper/ssuf_four_terminal_note_v5.pdf`](paper/ssuf_four_terminal_note_v5.pdf):
  current unrefereed manuscript.
- [`paper/ssuf_four_terminal_note_v5.tex`](paper/ssuf_four_terminal_note_v5.tex):
  LaTeX source.
- [`verification/`](verification/): exact verifiers, exhaustive routing table,
  separate cross-check, mutation tests, and machine-readable output.
- [`scripts/`](scripts/): one-command verification, PDF build, manifest, and
  deterministic release-archive tooling.
- [`PRIORITY_DISCLOSURE.md`](PRIORITY_DISCLOSURE.md): released claims and
  non-claims.
- [`LIMITATIONS.md`](LIMITATIONS.md): mathematical, review, novelty, and
  reproducibility limits.
- [`AI_USE_AND_PROVENANCE.md`](AI_USE_AND_PROVENANCE.md): detailed AI-use
  disclosure and chronology.
- [`LICENSING.md`](LICENSING.md): the deliberate no-license status of this
  release.

## Rebuild the manuscript

The checked PDF was built with Tectonic 0.16.9. Poppler's `pdftotext` is used
for text preflight checks.

```bash
python scripts/build_pdf.py
python verification/preflight_pdf_text.py
```

The build script keeps temporary TeX products outside the source tree and
replaces only the checked PDF. It can also use `pdflatex` when Tectonic is not
available.

## Context and novelty

The specific four-terminal investigation began after
[Dmitry Rybin's public post of 22 July 2026](https://x.com/DmitryRybin1/status/2079904005652893709)
announcing a counterexample to Goemans' cost conjecture.

Targeted web, paper, and public-GitHub searches performed on 23 July 2026 did
not find the exact four-terminal support pattern, the `335/294` certificate,
the displayed radical in this setting, or the restricted-model theorem. That
is a good-faith search result, not exhaustive novelty clearance. It cannot
rule out private, unindexed, differently described, or concurrent work.

For context, the current planar upper-bound reference is the 2026 journal
article
[Single-source unsplittable flows in planar and bounded-genus graphs](https://doi.org/10.1007/s10107-026-02365-x).
The graph used here lies outside the series-parallel positive class studied
in
[Integer and unsplittable multiflows in series-parallel digraphs](https://doi.org/10.1007/s10107-026-02392-8).

## Publication and citation

The canonical public version is the immutable
[`v0.1.0` GitHub release](https://github.com/matthewprotti/planar-ssuf-four-terminal-bound/releases/tag/v0.1.0)
and its exact commit. GitHub's server-recorded `published_at` time for that
release is the canonical public timestamp.

## Author and rights

Matthew Protti

Author credit identifies the human author; it is not a claim of legal
ownership. No institutional affiliation, sponsorship, or intellectual-
property ownership is asserted. This release deliberately grants no
open-source or open-content license. See [the licensing note](LICENSING.md)
for the precise status.
