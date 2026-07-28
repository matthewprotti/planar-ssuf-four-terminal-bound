# Four-Terminal Census Reconciliation

## Ambient partition

The ambient objects are all **168 labeled monotone families** of subsets of
`{1,2,3,4}`. They partition exactly as

\[
149\text{ positive threshold}
+18\text{ nonempty nonthreshold}
+1\text{ empty impossible family}
=168.
\]

The empty family is impossible in the SSUF reduction because
\(\tau=k\cdot p\le\sum_i k_i\), so the full cheap set is always feasible.

## Search partition inside the 149 realizable families

\[
54\text{ feasible-singleton families}
+1\text{ every-pair/no-singleton family}
+94\text{ remaining families}
=149.
\]

- The 54 singleton families have a routing with maximum upper deviation at most
  1.
- The one every-pair/no-singleton family has exact supremum \(L\) under the
  positive-difference assumptions.
- The 94 remaining labeled families form the historical initial optimization
  remainder after UC-006/008. Later theorems reduce this set.

## Two distinct group actions

### Arbitrary-label action

The full symmetric group \(S_4\) acts by permuting the four abstract terminal
labels in a threshold family. Under this action:

- the 149 realizable families form 26 orbits;
- the 94 remaining families form 15 orbits.

`threshold_family_census.json` records every orbit representative, every member
family ID, orbit size, and stabilizer size, with

\[
|\operatorname{orbit}|\,|\operatorname{stabilizer}|=24.
\]

These orbits organize search only.

### Fixed-graph automorphism action

The directed fixed topology preserves source, trunk vertices, and terminal
roles. Its role-preserving automorphism group is the identity. Therefore an
arbitrary terminal-label permutation is not automatically an objective
symmetry.

At the initial stage every one of the 94 labeled cells was a formal
optimization unit unless a separate objective-preserving transformation was
proved. The later reductions are labelwise theorems, not an assumption that
orbit members have equal objective values.

## Forward reduction after the original census partition

The original machine census remains

`149 = 54 singleton + 1 every-pair + 94 initial remainder`.

UC-013 is a later analytic reduction inside the 94-cell remainder. It eliminates
exactly five labeled no-pair cells:

- the full-set-only family; and
- the four families with exactly one feasible triple.

Those five cells form two complete abstract-label orbits, so the sequential
orbit count at the 89-cell stage is 13 rather than 15.

The verified sequence is:

| Stage | Labeled cells | Abstract-label search orbits | Role |
| --- | ---: | ---: | --- |
| after UC-006/008 | 94 | 15 | historical initial remainder |
| after UC-013 | 89 | 13 | historical intermediate remainder |
| after UC-017 | 83 | 12 | historical intermediate remainder |
| after UC-023 | **79** | **11** | current open frontier |

UC-017 resolves all 11 single-generator cells, six of them beyond the five
already covered by UC-013. UC-023 then resolves the four pure three-pair
clique cells. `census_reconciliation_check.py` reconstructs these four stages
from the minimal generators, checks each count and orbit count, and emits all
79 current labeled IDs.

This does not retroactively change the original census JSON field
`cells_remaining_after_every_pair_theorem`; it records an additional theorem
applied after that stage.
