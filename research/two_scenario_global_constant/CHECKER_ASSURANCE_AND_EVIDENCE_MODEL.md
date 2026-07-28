# Checker Assurance and Evidence Model - RB-003

## Principle

A checker proves only the proposition encoded by its inputs, arithmetic, and
acceptance conditions. Passing software does not by itself prove that the
encoded proposition is the right theorem.

## Authoritative evidence

The authoritative general result is the human-readable proof in
`TWO_SCENARIO_GLOBAL_CONSTANT.md` and the typeset paper.

The exact finite certificate is established by exhaustive graph-native
enumeration. The remaining programs are corroborating or regression evidence
unless stated otherwise.

## Primary exact verifier

`verify_two_scenario_global_constant.py`:

- reconstructs the fixed graph and its C/E path supports;
- checks the two positive cost-difference scenarios;
- derives scenario budgets from the shared fractional baseline;
- enumerates all 16 unsplittable routings;
- evaluates all 13 arc deviations exactly;
- identifies the feasible C-family;
- verifies the `1061/500` finite optimum and scaled deviation `8488`;
- generates the threshold-recognition registry; and
- writes deterministic JSON/CSV artifacts.

This proves the concrete finite statement for the encoded graph and inputs. It
does not prove the analytic global upper bound `17/8`.

## Threshold-recognition registry

The finite four-label registry exactly partitions the 168 downsets into:

- 149 positive scalar-threshold families with explicit integer witnesses;
- 18 nonempty nonthreshold families with exact two-trade certificates; and
- one empty family, inadmissible because the full set is feasible.

This is a finite combinatorial classification. It is not claimed as a novel
classification of threshold/simple games, and it is not the proof of the
shared-baseline analytic theorem.

## Secondary code path

`secondary_regression_check.py` uses a separately written code path and a
different finite lower parameter. It reduces some copy-and-paste risk, but it
shares:

- the same graph support matrix;
- the blocker framework;
- the lower-family ansatz; and
- the broad threshold-generation strategy.

It is therefore described as secondary regression, not independent derivation.

## Proof-text regression

`proof_review_integration_check.py` confirms that required proof repairs remain
present and superseded formulations remain absent. It is useful against
editorial regression. It has no mathematical authority over whether those
sentences are true.

## Envelope and pattern-pair regressions

The denominator-grid envelope check evaluates the proved analytic expressions
on a finite grid. It is not continuous optimization.

The 11,175 unordered pairs of scalar threshold patterns form an abstract
blocker census. Arbitrary pattern pairs need not share a common fractional
baseline, so the census is not a shared-baseline realization theorem.

## Mutation model

Mutations target:

- graph and path transcription;
- scenario/budget semantics;
- fraction orientation;
- finite objective values;
- feasible-family identity;
- non-attainment wording;
- missing proof-review repairs; and
- manifest or generated-artifact drift.

Passing the mutation set means only that the named corruptions are detected.
It does not imply completeness against all possible implementation errors.

## Authentication and replay

`replay.py`:

1. authenticates all package artifacts against `MANIFEST.sha256` before
   execution;
2. runs the proof-text, primary, and secondary checks;
3. regenerates deterministic outputs; and
4. authenticates the package again.

The root release manifest additionally binds the repository-level source and
checked PDFs.

## Trusted assumptions

The release still trusts:

- the stated graph and model are the intended scientific object;
- Python's integer and rational semantics are correctly implemented;
- the analytic proof is read and judged by humans;
- the committed source corresponds to the public claim; and
- the release infrastructure and Git hosting service behave as documented.

## Nonclaims

The checker package does not establish:

- novelty or priority;
- formal peer review;
- proof-assistant kernel verification;
- safety or correctness of a Compliance Health product;
- regulatory or legal correctness;
- customer performance; or
- an exact theorem outside the stated fixed-graph two-scenario model.
