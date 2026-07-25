# Scalar Lemmas for the No-Pair Region

Let `K=sum k_i`, `tau=k·p`, and `q_i=1-p_i`. Then

`R := K-tau = k·q`.

The triple missing terminal `i` is feasible exactly when `R >= k_i`.

## Lemma UC-012: no feasible pair forces `sum p_i > 2`

If every two-element cheap set is infeasible, then `tau` is larger than the sum
of the two largest weights. If `sum p_i <= 2`, the maximum of `k·p` over
`p in [0,1]^4` with that fixed sum is obtained by filling the two largest
coordinates first, so `k·p` is at most the sum of the two largest weights. This
is a contradiction. Therefore `sum p_i > 2`.

Equivalently, `sum q_i < 2` throughout the strict no-pair region.

## Lemma UC-013: full-set-only and one-triple cells have value at most one

If no triple is feasible, then `R < min_i k_i`. Hence

`min_i k_i * sum q_i <= k·q = R < min_i k_i`,

so `sum q_i < 1`. The all-cheap routing has every positive trunk deviation at
most `sum d_i q_i <= sum q_i < 1`, while every private deviation is at most one. Hence its maximum upper deviation is at most one.

If exactly one triple is feasible, say the triple missing `i`, then
`k_i <= R < k_j` for all `j != i`. Thus

`R = k_i q_i + sum_{j != i} k_j q_j
   > R * sum_{j != i} q_j`,

where the omitted nonnegative term `k_i q_i` only strengthens the inequality.
Therefore `sum_{j != i} q_j < 1`. Routing that feasible triple cheaply has each
positive trunk deviation at most `sum_{j != i} d_j q_j < 1`; private deviations
are at most one. Hence its maximum upper deviation is at most one.

Consequently five of the 94 cells are now analytically bounded by one: the
full-set-only cell and the four cells with exactly one feasible triple. The
positive-difference search remainder falls from 94 to **89 labeled cells**.

The argument does not cover cells with two, three, or four feasible triples, nor
cells with feasible pairs.
