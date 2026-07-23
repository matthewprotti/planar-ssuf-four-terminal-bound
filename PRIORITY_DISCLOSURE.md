# Proposed priority disclosure

- **Candidate:** v0.1.0-rc1
- **Prepared:** 23 July 2026
- **Current status:** private and unpublished

If a public release is expressly approved, the canonical public timestamp
will be the `published_at` time recorded by GitHub for the immutable
`v0.1.0` release. Repository creation and private commit times are not
presented as public priority.

## Claim A — exact finite certificate

There is a planar acyclic four-terminal single-source instance with maximum
demand

\[
D=294
\]

such that every cost-nonincreasing unsplittable routing has upper overload at
least

\[
335=\frac{335}{294}D.
\]

The certificate uses demands `(294, 216, 252, 294)`, cheap path amounts
`(78, 97, 36, 42)`, and expensive path amounts `(216, 119, 216, 252)`.
The private expensive-arc per-unit costs are `(36, 49, 42, 36)`, so every
full expensive choice costs `10584`. The fractional cost is
`31751 = 3(10584)-1`; therefore every cost-nonincreasing unsplittable routing
uses at least two cheap paths. Exact enumeration of all 16 routings and all
13 arcs gives optimum maximum overload exactly `335`.

**Status:** exactly verified in the primary verifier and reproduced by a
separate clean-room implementation. This is computational corroboration, not
independent human review.

## Claim B — limiting planar lower bound

For every \(\eta>0\), there is a rational planar acyclic four-terminal
instance for which every cost-nonincreasing unsplittable routing overloads
some arc by more than

\[
\left(\frac{299-41\sqrt{41}}{32}-\eta\right)D.
\]

Consequently,

\[
\alpha_{\mathrm{pl}}\ge \frac{299-41\sqrt{41}}{32}
=1.139747070789\ldots.
\]

**Status:** proved in the unrefereed manuscript and checked symbolically.

## Claim C — restricted-model sharpness

For the fixed four-terminal topology defined in the manuscript, over the
explicit real equal-full-cost, two-cheap-choice model, the exact supremum is

\[
\frac{299-41\sqrt{41}}{32}.
\]

The same supremum is obtained after restricting the data to rationals.

**Status:** proved in the unrefereed manuscript, algebraically checked, and
stress-tested. The stress test is not used as proof.

## Scope and non-claims

This disclosure does **not** claim:

- that the displayed radical is the exact unrestricted planar constant;
- optimality among all four-terminal planar graphs;
- optimality on the fixed topology with arbitrary unequal full-route costs;
- exhaustive novelty clearance;
- independent human verification;
- peer review, journal acceptance, or an algorithmic lower bound stronger
  than the existential obstruction itself.

## Attribution and concurrent work

This investigation was initiated after
[Dmitry Rybin publicly announced](https://x.com/dmitryrybin1/status/2079904005652893709)
a counterexample to Goemans' cost conjecture on 22 July 2026. Related work is
developing rapidly. Any eventual public account should distinguish the
four-terminal construction here from earlier and concurrent constructions
and should preserve the limited novelty wording above.
