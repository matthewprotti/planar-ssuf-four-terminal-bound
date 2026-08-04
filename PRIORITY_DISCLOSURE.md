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

### `v0.3.0`

- **Released:** 4 August 2026
- **Subject:** arbitrary/legal one-scenario fixed-gadget theorem, positive
  scenario-count ladder, scenario-cover duality and exact fixed atlas, SC-006
  fixed-family phase theorem, and the repaired high-heterogeneity tail
- **Status:** public immutable unrefereed GitHub research release

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

## Claim E - arbitrary/legal one-scenario fixed-gadget supremum

Over legal normalized one-scenario instances on the released fixed gadget,

$$
\sup\Phi=\frac{299-41\sqrt{41}}{32}.
$$

The same supremum holds after restriction to rational data and includes the
proved legally realizable signed-and-zero route-cost-difference strata. No
attainment or nonattainment assertion is made.

**Status:** complete companion proof; exact finite and symbolic corroboration;
internal AI-assisted claim review. This is not an unrestricted planar theorem.

## Claim F - positive scenario-count ladder on the fixed gadget

For coordinatewise strictly positive cost-difference scenarios,

$$
\beta_G^{(m,+)}=
\begin{cases}
\dfrac{299-41\sqrt{41}}{32},&m=1,\\[1mm]
\dfrac{17}{8},&m=2,\\[1mm]
3,&m=3,\\
4,&m\ge4.
\end{cases}
$$

The two-, three-, and four-or-more-scenario values are non-attained suprema.
The signed-and-zero extension in Claim E is not asserted for multiple
scenarios.

**Status:** complete companion proofs and narrower exact corroboration;
claim-scoped adversarial review. One supplied external human report examined
the short three-/many-scenario arguments but not every companion proof.

## Claim G - scenario-cover and fixed-family results

For a fixed normalized instance, forcing every route below a threshold is
equivalent to covering those route displacements by the scenarios' open
homogeneous halfspaces. The release includes a complete exact finite atlas at
the RB witness and the SC-006 four-phase theorem on its stated fixed RB family.

**Status:** exact finite atlas with isolated blind reconstruction; separate
analytic SC-006 proof with nonblind exact and symbolic corroboration. Neither
the atlas nor SC-006 is a global bounded-heterogeneity theorem.

## Claim H - bounded-heterogeneity high tail

For the released fixed gadget and exactly two positive scenarios, the release
proves an upper bound of `2` through `kappa_0`, exact equality to the stated
algebraic envelope `F(kappa)` for `kappa >= kappa_0`, and the accompanying
lower/upper sandwich below that threshold. The exact curve below `kappa_0`
remains open.

**Status:** complete repaired companion proof and exact algebraic
corroboration; internal AI-assisted claim review. No complete external human
reconstruction is claimed.

## Scope and nonclaims

The releases do not claim:

- that either displayed constant is the exact unrestricted planar constant;
- global four-terminal or fixed-topology optimality outside the stated models;
- a signed-or-zero multi-scenario extension;
- an unrestricted planar multi-scenario constant;
- the exact global bounded-heterogeneity curve below `kappa_0`;
- the exact F064 value `5/2 - sqrt(2)`;
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
