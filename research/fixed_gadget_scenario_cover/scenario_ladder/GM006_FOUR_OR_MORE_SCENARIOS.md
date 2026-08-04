# GM-006 - Four or More Positive Scenarios

Status: private RC1 derived proof. The theorem content is extracted from the
GM-006 section accepted at claim level in the frozen original R2 review. The
obsolete GM-005 section of that historical source is deliberately excluded;
GM-005 is controlled by its separate versioned repair.

## Theorem

On the fixed four-terminal gadget, with weak scenario-wise cost nonincrease
and exactly `m >= 4` coordinatewise strictly positive E-minus-C scenario
vectors,

`beta_G^(m,+) = 4`.

Every finite legal instance has value strictly below four, so the supremum is
not attained. Rational instances approach four.

## Proof

Normalize `0 < d_i <= 1` and `max_i d_i = 1`. Put `h_i = d_i q_i` and
`H = sum_i h_i`. The all-C E-set is empty, hence is feasible in every positive
scenario, and its maximum positive deviation is `H <= 4`. Therefore every
instance has value at most four.

This is a bound over all thirteen arcs, not only the trunk. The exact
trunk/private envelope in `TRUNK_PRIVATE_ARC_ENVELOPE.md` gives

`M(R) <= max(1, sum_{i not in R} h_i)`.

For the all-C route, equality with `H` is witnessed on the common trunk arc
`a3`; every positive private deviation is at most one. No finite enumeration
is used for this upper bound.

For the matching lower sequence, take an integer `n >= 2`, unit demands, and
`q_i = 1 - 1/n` for all four terminals. Use four scenarios. Scenario `i` has
weight `3n` on terminal `i` and weight one on each other terminal. Its
fractional budget is

`(3n + 3)(1 - 1/n) = 3n - 3/n < 3n`.

Every nonempty E-set contains some terminal `i` and is blocked by scenario
`i`. Thus all-C is the unique common feasible routing and has value

`4(1 - 1/n)`,

which tends to four. For `m > 4`, duplicate any of the four positive
scenarios; distinctness is not part of the model and the common feasible
family is unchanged.

Finally, suppose a finite instance had value four. Because all-C is feasible
and has value `H <= 4`, equality would force `d_i q_i = 1` for every terminal,
hence `d_i = q_i = 1`. The full E-set would then be feasible in every scenario
at equality with the fractional budget and would have zero deviation. This is
a contradiction. Therefore four is not attained.

The argument is fixed-gadget and positive-scenario only. It does not establish
a signed/zero extension or any topology-wide constant.
