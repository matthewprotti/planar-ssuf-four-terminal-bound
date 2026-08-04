# Zero-Difference Boundary of the Solved Every-Pair Cell

The every-pair/no-singleton theorem was stated for `k_i>0`. Its nonnegative
closure contains no new zero-coordinate point.

Suppose `k_i>=0`, not all zero, every pair is feasible, and no singleton is
feasible. Sort the paired scalar coordinates so

`k_1 <= k_2 <= k_3 <= k_4`.

No singleton feasible gives `tau>k_4`. If some coordinate is zero, then
`k_1=0`; feasibility of the pair `{1,2}` gives

`tau <= k_1+k_2 = k_2 <= k_4`,

a contradiction. Hence every `k_i` is automatically positive.

Therefore the exact value `L` for the every-pair/no-singleton cell already
covers its entire nonnegative-difference closure. This does not address other
cells with zero differences or any negative-difference orientation.
