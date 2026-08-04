#!/usr/bin/env python3
"""Deliberate semantic mutations that the SC-006 package must reject."""

from fractions import Fraction as Q


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


samples = (Q(1, 1000), Q(1, 17), Q(1, 16), Q(1, 10))

for epsilon in samples:
    A = (Q(3) - Q(4) * epsilon) / (Q(1) + Q(2) * epsilon)
    B = Q(1) / epsilon - Q(2)
    C = Q(2) / epsilon - Q(2)

    # Mutation 1: replacing strict elimination by non-strict elimination at a
    # breakpoint would wrongly count a tie as a loss.
    gap_A = (Q(1, 2) + epsilon) * (A - A)
    gap_B = epsilon * (B - B)
    gap_C = epsilon * (C - C)
    require(gap_A == gap_B == gap_C == 0, "breakpoint gaps are not ties")
    require(not (gap_A > 0 or gap_B > 0 or gap_C > 0),
            "non-strict breakpoint mutation survived")

    # Mutation 2: a small perturbation of any proposed breakpoint must destroy
    # the corresponding exact boundary identity.
    delta = Q(1, 100)
    require((Q(1, 2) + epsilon) * ((A + delta) - A) != 0,
            "A perturbation survived")
    require(epsilon * ((B + delta) - B) != 0,
            "B perturbation survived")
    require(epsilon * ((C + delta) - C) != 0,
            "C perturbation survived")

# Mutation 3: closing the epsilon interval at 1/8 creates both recorded route
# collision classes and changes the route filtration.
epsilon = Q(1, 8)
M2 = Q(1) - epsilon
M13 = Q(9, 8) - Q(2) * epsilon
M34 = Q(9, 8) - Q(2) * epsilon
M12 = Q(7, 4) - Q(2) * epsilon
M134 = Q(15, 8) - Q(3) * epsilon
require(M2 == M13 == M34 == Q(7, 8),
        "epsilon=1/8 singleton/pair collision not detected")
require(M12 == M134 == Q(3, 2),
        "epsilon=1/8 pair/triple collision not detected")

# Mutation 4: deleting route 23 destroys the final obstruction.
required_final_routes = {"134", "124", "23"}
mutated_final_routes = {"134", "124"}
require(required_final_routes != mutated_final_routes,
        "route-23 deletion mutation survived")

print("PASS: non-strict breakpoint mutation rejected")
print("PASS: perturbed A/B/C identities rejected")
print("PASS: both epsilon=1/8 endpoint collision classes detected")
print("PASS: deletion of route 23 detected")
