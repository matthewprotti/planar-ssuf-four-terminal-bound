#!/usr/bin/env python3
"""Deliberate semantic mutations for the GM-005 repair."""

from fractions import Fraction as Q

import verify_gm005_exact as gm


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


# Mutation 1: replacing weak feasibility by strict feasibility loses a required tie.
q = (Q(1), Q(1), Q(1), Q(0))
weights = (Q(1), Q(1), Q(1), Q(1))
triple = 0b0111
budget = gm.scenario_budget(weights, q)
require(gm.route_weight(triple, weights) == budget == 3, "tie fixture changed")
require(gm.route_weight(triple, weights) <= budget, "weak feasibility tie rejected")
require(not (gm.route_weight(triple, weights) < budget), "strict-feasibility mutation survived")

# Mutation 2: q=0 must be split off before normalization.
zero_q = (Q(0),) * 4
require(gm.scenario_budget(weights, zero_q) == 0, "zero-q budget changed")
require(gm.route_value(0, (Q(1),) * 4, zero_q) == 0, "zero-q all-C route must match fractional flow")

# Mutation 3: scenario positivity is part of the theorem domain.
try:
    gm.validate_positive_scenario((Q(1), Q(1), Q(0), Q(1)))
except RuntimeError:
    pass
else:
    raise RuntimeError("zero-coordinate scenario mutation was accepted")

# Mutation 4: the exact trunk support table is load-bearing.
mutated_supports = list(gm.EXPECTED_SUPPORTS)
mutated_supports[2] = frozenset(set(mutated_supports[2]) - {"a4"})
observed = tuple(frozenset((gm.C_PATHS[i] - gm.E_PATHS[i]) & set(gm.TRUNK)) for i in range(4))
require(tuple(mutated_supports) != observed, "support-deletion mutation survived")

# Mutation 5: weakening the heavy entry from 3n to 3(n-1) destroys strict blocking.
n = 7
q_n = tuple(Q(n - 1, n) for _ in range(4))
mutated = (Q(3 * (n - 1)), Q(1), Q(1), Q(1))
require(gm.route_weight(0b0001, mutated) == gm.scenario_budget(mutated, q_n),
        "mutated heavy singleton should tie the budget")
require(gm.route_weight(0b0001, mutated) <= gm.scenario_budget(mutated, q_n),
        "mutated heavy singleton unexpectedly blocked")

# Mutation 6: the old weak branch really can contain a singleton route of value 3.
d = (Q(1),) * 4
scenarios = (weights, weights, weights)
require(gm.is_feasible(0b1000, q, scenarios), "singleton 4 fixture infeasible")
require(gm.route_value(0b1000, d, q) == 3, "singleton 4 no longer hits 3")
require(gm.is_feasible(0b0111, q, scenarios), "repair triple infeasible")
require(gm.route_value(0b0111, d, q) == 0, "repair triple no longer collapses equality")

# Mutation 7: no finite member of the approaching sequence may equal 3.
for n in range(2, 101):
    require(Q(3 * (n - 1), n) < 3, f"finite lower member attained 3 at n={n}")

print("PASS: strict-feasibility mutation rejected")
print("PASS: q=0 normalization endpoint exposed and handled")
print("PASS: nonpositive scenario mutation rejected")
print("PASS: trunk-support deletion rejected")
print("PASS: weakened-heavy-entry mutation loses strict blocking")
print("PASS: old singleton-equality gap is repaired by the complementary triple")
print("PASS: every tested finite lower-sequence member remains strictly below 3")
print("ALL GM-005 MUTATION TESTS PASSED")
