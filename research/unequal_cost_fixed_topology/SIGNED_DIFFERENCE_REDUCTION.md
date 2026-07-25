# Nonzero Signed Route-Cost Differences

The positive-difference theorem does not extend automatically to negative
route-cost differences. The cost-feasibility side nevertheless has an exact
finite reduction.

Let

`k_i = expensive_i - cheap_i`

be nonzero, and let `N={i:k_i<0}`. Put `w_i=|k_i|`. For a cheap-set indicator
`z_i`, define an oriented indicator

- `z'_i=z_i` when `k_i>0`;
- `z'_i=1-z_i` when `k_i<0`.

Then

`sum_i k_i z_i >= k·p`

is equivalent to

`sum_i w_i z'_i >= w·p'`,

where `p'_i=p_i` for positive coordinates and `p'_i=1-p_i` for negative
coordinates. Thus every nonzero signed cost-feasible family is a coordinate-
complement of one of the 149 positive threshold families, and conversely.

## Exact four-label census

`signed_difference_census.py` enumerates all 149 positive families under all 16
coordinate-complement patterns. The 2,384 representations collapse to

**1,881 unique labeled unate threshold families.**

Exactly 149 are upward closed in the original cheap coordinates—the original
positive-difference families.

## Crucial limitation

This is a classification of **cost feasibility**, not an objective-preserving
reduction to the positive case. Complementing a negative coordinate swaps which
physical route is represented by the oriented `1`, reverses that terminal's
path-difference contribution, and replaces `p_i` by `1-p_i`. Future signed-cell
optimization must therefore carry both:

1. one of the 1,881 feasible set systems; and
2. the corresponding sign-oriented fixed-support objective.

Zero differences are not included. They are genuine boundary coordinates that
do not affect cost feasibility but still affect routing load, and require a
separate closure analysis.
