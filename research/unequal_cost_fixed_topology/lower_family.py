"""Machine-readable local definition of the every-pair lower family."""

from __future__ import annotations

CANONICAL_LOWER_FAMILY = {
    "parameters": {
        "q_domain": "sqrt(3)-1 < q < 1",
        "epsilon_domain": "0 < epsilon < 3-2*q-q^2",
    },
    "demands": ["1", "q^2", "q", "1"],
    "cheap_fractions": [
        "1-q^2",
        "q^2+2*q-2+epsilon",
        "1-q",
        "1-q",
    ],
    "positive_route_cost_differences": ["1", "1", "1", "1"],
    "sum_cheap_fractions": "1+epsilon",
    "witness_lower_bound": "q^2*(4-q^2-2*q-epsilon)",
    "limiting_function": "q^2*(4-q^2-2*q)",
    "maximizer": "(sqrt(41)-3)/4",
    "limiting_value": "(299-41*sqrt(41))/32",
}
