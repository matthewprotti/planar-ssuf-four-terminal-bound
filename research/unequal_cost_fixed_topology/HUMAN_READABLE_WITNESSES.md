# Human-Readable Census Witnesses

Run `python generate_witness_examples.py` to regenerate
`witness_examples.json`.

## Positive threshold example: every pair, no singleton

The census stores the exact family whose minimal feasible sets are all six
pairs. Equal positive weights with threshold two realize it. This is the cell
treated by UC-008.

## Remaining labeled cell example

The generated file selects the first stable labeled ID from the 94-cell list
and records its exact integer weights, threshold, and minimal feasible sets. It
is still a formal optimization unit on the fixed graph; membership in an
arbitrary-label orbit is only a search aid.

## Nonthreshold example

The generated file includes one exact two-trade. In the canonical first case,
positive sets `{1,3}` and `{2,4}` and negative sets `{2,3}` and `{1,4}` have
identical incidence sum

\[
\mathbf 1_{13}+\mathbf 1_{24}
=\mathbf 1_{23}+\mathbf 1_{14}
=(1,1,1,1).
\]

A threshold representation would force the same total weight to be both at
least and below twice the quota.

## Empty-family obstruction

The empty family is not an SSUF feasibility family because the full cheap set
has weight \(\sum_i k_i\ge k\cdot p=\tau\).
