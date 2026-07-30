# Contributing objections, corrections, and reproductions

This repository welcomes precise scrutiny of its released claims and
artifacts. The most useful first step is a focused issue tied to an exact
version or commit.

## Rights and submission boundary

The repository deliberately has no operative open-source or open-content
license. See [`LICENSING.md`](LICENSING.md). Viewing the public materials,
opening an issue, or receiving a response does not grant rights beyond those
provided by law.

Use the issue tracker before submitting code or manuscript changes. Do not
submit a pull request containing code, proof text, data, or other third-party
material unless the maintainer requests it and the authorship, provenance, and
submission rights are clear.

## What to report

Reports are welcome in five categories:

1. a mathematical counterexample or proof objection;
2. a verifier, data, build, packaging, or documentation defect;
3. an exact reproduction result or reproduction failure;
4. a prior-art or attribution lead; or
5. a clearly separated proposed extension.

For adversarial mathematical review, the
[`adversarial-review` issue template](.github/ISSUE_TEMPLATE/adversarial-review.md)
provides a useful starting structure.

## Minimum report

Please include:

- the exact tag, release, or commit;
- the precise theorem, lemma, file, command, or artifact at issue;
- the smallest concrete objection or reproduction case;
- exact input data and arithmetic where relevant;
- environment and commands for a computational discrepancy;
- expected and observed results; and
- the provenance and redistribution status of any attached data or code.

Distinguish a theorem objection from a software, manuscript, documentation, or
packaging issue. For a suspected counterexample, show that it satisfies every
hypothesis and state exactly which conclusion fails.

## Reproduction reports

A useful reproduction report records:

- operating system and architecture;
- Python and dependency versions;
- the checked-out tag or commit;
- commands run without material omission;
- complete pass/fail status; and
- any changed files or hashes after execution.

A successful replay is valuable reproducibility evidence. It is not, by
itself, independent proof review or peer review.

## Corrections and immutable releases

Released tags and assets are not silently rewritten. A confirmed defect will
be classified by scope and addressed through a public issue, erratum, or new
version as appropriate. A correction to one result line does not automatically
alter another result line.

## Prior art and extensions

For prior art, provide a stable citation or link and explain the closest
matching formulation, hypotheses, and conclusion. A proposed extension should
state which released assumptions it changes and must not be presented as
already proved by the existing package.

## Privacy and review terminology

Do not post private prompts, private correspondence, personal contact details,
confidential information, credentials, or customer data. Do not attribute a
reviewer or quote private feedback without permission.

An issue, pull request, automated check, or AI-assisted critique is not
described as independent human review or formal peer review.
