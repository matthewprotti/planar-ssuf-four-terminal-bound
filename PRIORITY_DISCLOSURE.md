# Priority disclosures and claim boundaries

## Immutable release record

### `v0.1.0`

- **Released:** 23 July 2026
- **Subject:** original one-scenario planar lower bound, finite `335/294`
  certificate, and restricted equal-cost sharpness theorem
- **Status:** public immutable GitHub release

### `v0.2.0`

- **Released:** 28 July 2026
- **Subject:** exact two-scenario fixed-gadget cost-nonincrease supremum RB-003
- **Status:** public immutable GitHub release

### `v0.2.1`

- **Released:** 30 July 2026
- **Subject:** documentation, provenance, and release-hygiene correction
- **Status:** public immutable GitHub release; no new mathematical claim or
  priority claim

For each version, the canonical public timestamp is GitHub's server-recorded
release time. Private repository events and local file timestamps are not
presented as public priority.

## Claim A - exact finite one-scenario certificate

There is a planar acyclic four-terminal single-source instance with maximum
demand `294` such that every cost-nonincreasing unsplittable routing has upper
overload at least `335`.

**Status:** exactly verified for the encoded graph and data by exhaustive
routing enumeration. This does not prove global sharpness.

## Claim B - limiting planar lower bound

For every `eta > 0`, there is a rational planar acyclic four-terminal instance
forcing upper overload greater than

$$
\left(\frac{299-41\sqrt{41}}{32}-\eta\right)d_{\max}.
$$

Consequently,

$$
\alpha_{\mathrm{pl}}\ge
\frac{299-41\sqrt{41}}{32}
=1.139747070789\ldots.
$$

**Status:** proved in the unrefereed `v0.1.0` manuscript and symbolically
corroborated.

## Claim C - restricted one-scenario sharpness

For the fixed four-terminal topology, over the explicit real
`equal-full-cost, at-least-two-cheap` model, the exact supremum is

$$
\frac{299-41\sqrt{41}}{32},
$$

and restricting data to rationals does not change the supremum.

**Status:** proved in the unrefereed `v0.1.0` manuscript. This is not arbitrary
one-scenario fixed-graph sharpness.

## Claim D - exact two-scenario fixed-gadget supremum RB-003

For the same fixed graph, one unsplittable routing must satisfy

$$
C_j(y)\le C_j(x),\qquad j=1,2,
$$

for two positive E-minus-C cost-difference scenarios. With normalized additive
upper arc deviation,

$$
\boxed{\beta_G^{(2\mathrm{sc})}=\frac{17}{8}.}
$$

The supremum is not attained by any legal finite instance. Rational instances
with feasible C-family

$$
\uparrow\{123,124,234\}
$$

approach it.

At `epsilon = 1/1000`, an exact finite certificate has value `1061/500`; after
scaling demands by `4000`, every routing satisfying both scenario budgets has
upper deviation at least `8488`.

**Status:** self-contained unrefereed proof; exact finite certificate; two
role-separated AI-assisted critique rounds; the second proof-only critic
recommended acceptance subject to local edits, which were integrated before
the human release decision. These rounds are not external human review or
formal peer review. `v0.2.1` changes this status description and package
hygiene only, not the mathematics.

## Scope and nonclaims

The releases do not claim:

- that either displayed constant is the exact unrestricted planar constant;
- global four-terminal or fixed-topology optimality outside the stated models;
- the arbitrary one-scenario fixed-graph constant;
- an unrestricted or many-scenario robust constant;
- a bounded-heterogeneity two-scenario constant;
- a sequential-algorithm lower bound;
- customer or operational performance;
- exhaustive novelty clearance;
- formal peer review or journal acceptance; or
- institutional ownership, sponsorship, or affiliation.

## Attribution and concurrent work

Dmitry Rybin's 22 July 2026 public counterexample was the direct catalyst for
this investigation and must be credited in any account of the work. Related
research is developing rapidly. The priority statement is therefore limited to
the exact public artifacts and claims in the tagged releases.
