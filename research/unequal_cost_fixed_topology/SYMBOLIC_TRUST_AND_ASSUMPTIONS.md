# Symbolic Audit: Trusted Components and Assumptions

The theorem is proved in `FIXED_SUPPORT_ROUTING_LEMMA.md` and
`EVERY_PAIR_CELL_THEOREM.md`. Software checks are corroboration, not a
substitute for the sign, domain, or boundary arguments in those proofs.

## SymPy audit

`symbolic_every_pair_check.py` requires:

- CPython 3.11 or later;
- SymPy exactly 1.14.0;
- exact integers, rationals, symbolic polynomials, and the algebraic number
  `sqrt(41)`.

The script verifies identities by exact expansion/simplification. It declares
positive symbols for `s,t,p,q`; pair-max dominance uses the separate assumption
that \(e_i,\ell_i\ge0\). The denominator \(t\) is positive in the theorem
region. The script does not ask a numerical sampler to establish identities.

Inequality and admissibility conclusions are not delegated to an unconstrained
simplifier. The checker verifies exact gap identities and the integer square
certificate

\[
263^2-41^3=248>0,
\]

while the human proof establishes domain signs and boundary coverage.

## CAS-independent audit

`exact_algebra_audit.py` uses only Python `Fraction`, a small Laurent-polynomial
implementation, and exact arithmetic in \(\mathbb Q(\sqrt{41})\). It checks:

- all fixed-support pair expressions;
- every convex-combination identity;
- stationary equations and value \(L\);
- boundary gap factorizations;
- the lower-family witness identities; and
- the exact square-gap certificate above.

The two programs share the stated formulas but not the algebra engine.

## What remains trusted

- the human transcription of formulas into both checkers;
- CPython integer and rational arithmetic;
- SymPy 1.14.0 for the SymPy lane;
- the theorem's human domain and sign arguments; and
- the fixed topology specification.

No second computer algebra system is claimed. The CAS-independent audit is a
separate exact implementation, not an independent human proof.
