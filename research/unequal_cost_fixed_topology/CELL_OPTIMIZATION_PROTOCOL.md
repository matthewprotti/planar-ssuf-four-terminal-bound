# Protocol for the Remaining 83 Strictly Positive Threshold Cells

Each positive threshold cell is defined by

\[
k(S)\ge k\cdot p\quad(S\in\mathcal F),
\qquad
k(S)<k\cdot p\quad(S\notin\mathcal F),
\]

with \(k_i>0\), \(p_i\in[0,1]\), \(d_i\in(0,1]\), and
\(\max_i d_i=1\).

## Normalization

Use \(\sum_i k_i=1\). Encode strict losing constraints with a margin
\(\delta>0\):

\[
k(S)\le k\cdot p-\delta.
\]

A numerical candidate with \(\delta\approx0\) is a boundary signal, not an
interior witness.

## Cell versus closure

Track separately:

1. the strict cell;
2. its closure, where some losing sets may become feasible; and
3. the larger boundary feasibility family.

Adding feasible routings can only help the minimizing router, so a closure may
be an upper relaxation when this monotonic direction is proved. A boundary
maximizer is not automatically a lower-bound witness for the strict cell.
Lower bounds require an exact interior point or an explicit strict sequence.

## Demand boundary

Do not silently replace \(d_i>0\) by \(d_i\ge0\). If a closure optimizer has a
zero demand, prove approximation from the positive domain or label the result
as a closure bound only.

## Label discipline

Arbitrary-label permutation orbits may organize scouting, but the fixed graph
has no nontrivial role-preserving automorphism. Certify every labeled cell or
prove an objective-preserving transformation for the specific labels involved.

## Evidence standard

Floating-point optimization may identify active regimes. Every reported result
must be replaced by exact rational/algebraic data, exact feasibility margins,
and a symbolic upper or lower certificate.

## Forward-pass priority order

After UC-013 and UC-017, skip the five bounded no-pair cells and all 11 single-generator cells; retain 83
labeled positive-difference cells. Exact witnesses in F126, F125, F042, F129,
and F143 show that some surviving cells exceed one; these are priority cells for
upper-bound analysis, not evidence of an improvement over `L`.

For nonzero signed differences, the analogous feasibility universe has 1,881
labeled unate threshold families. Signed optimization must attach the coordinate
sign mask to the objective and may not quotient it away using the positive
family alone.
