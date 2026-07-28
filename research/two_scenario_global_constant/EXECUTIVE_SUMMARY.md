# Executive Summary — Track B Global Two-Scenario Supremum

## Mathematical result

For the fixed four-terminal planar gadget reproduced in the theorem file, the
exact worst-case normalized additive upper arc-deviation under **two
simultaneous scenario-wise cost-nonincrease constraints** is

\[
\boxed{\beta_G^{(2\mathrm{sc})}=\frac{17}{8}=2.125.}
\]

The constraint means that the unsplittable routing costs no more than the
fractional routing in either scenario. It does not require equal costs.

The value `17/8` is a supremum, not a finite maximum. No legal finite instance
attains it. Rational instances with feasible C-family

\[
\uparrow\{123,124,234\}
\]

approach it; this family is called `F126` in the earlier census.

## Review status

A second-round hostile proof-only review of v4 found no counterexample and no
remaining theorem-level gap in the two-colour matching lemma, the generalized
one-knapsack lemma, the actual shared-baseline `|A|=3` exhaustion, or the
non-attainment equality chain. Its recommendation was **accept subject to minor
proof revision**.

The v5 theorem integrates every requested and recommended local edit:

- the reversed §6.1 heading is corrected;
- the two-colour matching consequence is formalized;
- Lemma 2's pair-blocking hypothesis is restored at its application point;
- the knapsack extreme-point argument is made explicit;
- the star-triangle conclusion is stated as a forced core, allowing one
  irrelevant extra incident blocker; and
- the full equations (20)–(22) equality sandwich is displayed in the
  non-attainment proof.

This makes v5 a sign-off candidate. The revised archive itself has not yet been
re-reviewed and the work has not undergone formal journal peer review.

## Structural explanation

Any instance above value 2 contains one forced blocker core: a **central
star-triangle**.

- One scenario makes one central terminal non-omittable and therefore blocks
  every omission pair incident with it.
- The other scenario blocks every pair among the remaining three terminals.
- That second scenario may also block one additional pair incident with the
  centre; the proof and envelope do not depend on whether it does.
- The fixed graph turns the core into the scalar envelope

\[
1+3\Delta-2\Delta^2
=
\frac{17}{8}-2\left(\Delta-\frac34\right)^2.
\]

The envelope peaks at `17/8`. Exact attainment would force the non-omittable
terminal to have both demand and E-fraction equal to one, contradicting the
normalized scenario budget; hence only an extremizing sequence exists.

## Concrete finite certificate

At `epsilon=1/1000`, the package gives an exact finite instance with objective

\[
\frac{1061}{500}=2.122.
\]

After scaling demands by 4000, every routing that does not increase either
scenario cost has upper deviation at least 8488. The verifier enumerates all
16 routings and all 13 arcs.

The two fractional scenario budgets are `2998.998` and `1998.999`; feasible
unsplittable scenario costs are lower, not equal. This makes the inequality
semantics explicit.

## What the computation establishes

The graph-native enumeration exactly certifies the finite lower instance. The
package also exactly recognizes all 168 four-label downsets: 149 have positive
scalar-threshold witnesses, 18 have exact two-trade impossibility certificates,
and one is empty.

The 11,175 abstract threshold-pattern pairs and the denominator-16 envelope
grid are regression checks. They are not a shared-baseline realization proof
or continuous optimization. The secondary script is a separate code path, not
an independent mathematical derivation.

## Commercial reading — with the caveats beside it

The theorem shows that the **intersection** of two hard linear budgets can
contain a small, explainable obstruction that is invisible when each budget is
viewed only as a standalone feasible family. It motivates joint obstruction
detection and remediation analysis.

It does not prove that a particular sequential algorithm fails, nor does it
measure the marginal effect of adding a second scorecard. The previously
released value

\[
L\approx1.139747
\]

belongs to a more restricted one-scenario regime, so the arithmetic comparison
`17/8 > L` is contextual rather than causal.

The finite certificate already uses within-scenario weight ratios 3000 and
1000, and the limiting sequence requires unbounded ratios. The commercially
important next theorem is therefore the bounded-heterogeneity curve
`beta_G^(2sc)(kappa)`.
