# Commercial Interpretation — The Joint-Budget Star-Triangle Obstruction

## The defensible one-sentence claim

On the fixed four-choice routing structure, two simultaneous requirements that
the discrete solution **not increase either linear scenario cost** can support
an unavoidable normalized additive deviation approaching

\[
\boxed{17/8=2.125}.
\]

This is a supremum approached by increasingly uneven scorecard weights; it is
not a finite maximum and not a total-cost multiplier.

## The mechanism in plain language

The hard pattern contains a forced **star-triangle blocker core**:

1. One budget effectively pins one central item: it cannot be omitted even by
   itself.
2. A second budget allows any one of the other three items to be omitted, but
   disallows omitting any two together.
3. The three individually admissible repairs therefore remain mutually
   incompatible in pairs.
4. The second budget may also block one additional pair involving the pinned
   item; that extra restriction is irrelevant to the certified envelope.
5. On this graph, balancing the core repairs drives the additive deviation
   toward `17/8`.

“Central” is graph-structural. The two central terminal supports cross five and
four trunk arcs respectively—so each crosses **at least four** trunk arcs.

## Review status

Two role-separated AI-assisted critique rounds were performed; they are not
external human mathematical review. The second proof-only critic found no
theorem-level gap and recommended acceptance subject to minor proof revision.
The proof-integrated v5 package incorporates all identified local edits,
including the distinction between a forced blocker core and an exact
classification of both blocker graphs. It was released after human
adjudication in `v0.2.0`. No external human mathematical review is documented,
and the work has not been peer reviewed. `v0.2.1` changes this description and
release hygiene only, not the mathematics.

## What a product could expose

A proof-pack or remediation UI could identify:

- the pinned central item;
- the three individually admissible omissions;
- the pairwise incompatibilities created by the other budget;
- the certified additive-deviation bound for the modeled instance; and
- candidate interventions that break either the star or the triangle.

In a compliance setting, the objects might be credentials, documents, roles,
or remediation actions. One control can make a particular item effectively
mandatory, while another permits any single exception among three alternatives
but not two exceptions together.

That is commercially interpretable because the output is a small conflict
certificate rather than a generic “infeasible” or “high risk” flag.

## What the theorem does **not** yet justify

The theorem does not establish that optimizing scorecards sequentially is
suboptimal. It proves a geometric obstruction in their joint feasible region;
a sequential-algorithm claim requires a separately defined algorithm and an
approximation or counterexample analysis.

It also does not show that adding a second scorecard raises the constant by
86.44%. The released benchmark

\[
L=\frac{299-41\sqrt{41}}{32}\approx1.139747
\]

comes from a restricted one-scenario model, while the new theorem ranges over
two arbitrary positive difference vectors. The arithmetic comparison is true,
but it changes more than one modeling assumption.

## The important conditioning caveat

At `epsilon=1/1000`, the exact finite certificate uses scenario weight ratios
of 3000 and 1000. In the extremizing sequence those ratios diverge. Real
customer scorecards may be much better conditioned.

The natural commercial theorem is therefore

\[
\beta_G^{(2\mathrm{sc})}(\kappa),
\qquad
\frac{\max_i k_i^{(j)}}{\min_i k_i^{(j)}}\le\kappa.
\]

That curve would answer the customer-facing question:

> How large can the certified joint-budget deviation become when no
> requirement is weighted more than `kappa` times another within either
> scorecard?

The unrestricted value `17/8` is the exact ceiling; the bounded-heterogeneity
curve determines how quickly realistic systems approach it.
