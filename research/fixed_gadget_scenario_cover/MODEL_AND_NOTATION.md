# Model and Notation

Let `G` be the fixed directed acyclic four-terminal gadget specified in
`one_scenario/proof/imported-baseline/FIXED_TOPOLOGY_APPENDIX.md`.

For each terminal `i`, let `p_i` be the fractional C share, let
`q_i = 1 - p_i` be its E share, and let `d_i` be its positive demand. Normalize

`0 < d_i <= 1` and `max_i d_i = 1`.

A routing may be encoded by its E-set `R` or its complementary C-set `S`.
With E-minus-C difference vector `k`, weak scenario-wise cost nonincrease is

`k(R) <= k dot q`,

equivalently `k dot (1_S - p) >= 0`. Blocking is strict. Equality remains
feasible.

The principal scenario classes are:

- `C_+`: coordinatewise strictly positive difference vectors;
- `C_legal`: the one-scenario vectors realizable by nonnegative,
  commodity-independent arc costs, including signed and zero strata; and
- `C_{+,kappa}`: positive vectors with the within-vector ratio
  `max_i k_i / min_i k_i <= kappa`, applied separately to every scenario.

For fixed normalized `(p,d)`, let `M_{p,d}(S)` be the exact maximum positive
arc deviation of C-set `S` and define

`G_<r(p,d) = {S : M_{p,d}(S) < r}`.

Let `tau_{kappa,p}(A)` be the least number of strictly positive losing
halfspaces of condition number at most `kappa` whose union covers `A`, with
`tau(emptyset)=0` and impossible cover value `+infinity`. The symbol
`kappa=infinity` means unrestricted positive normals. Then

`Psi_{m,kappa}(p,d) = max {r : tau_{kappa,p}(G_<r(p,d)) <= m}`

over the finite route-value set, and

`beta_G^(m,+)(kappa) = sup_{p,d} Psi_{m,kappa}(p,d)`

over the normalized fixed-gadget instance domain. Cover thresholds are
infima; strict availability at the endpoint is a separate question.

Review dispositions belong only to the cited versioned run. A claim-level
disposition need not equal the enclosing packet's top-level disposition.

