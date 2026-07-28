# Targeted Literature and Novelty Matrix - RB-003

**Search date:** 28 July 2026  
**Status:** good-faith targeted search, not exhaustive novelty clearance

## RB-003 claim being positioned

On one specified four-terminal planar acyclic graph, require a single
unsplittable routing to satisfy two positive scenario-wise cost-nonincrease
constraints relative to a given fractional routing. For normalized additive
upper arc deviation, the exact non-attained supremum is `17/8`.

## Closest research areas

| Area | Representative source | Relationship | Distinction from RB-003 |
| --- | --- | --- | --- |
| Planar cost-preserving SSUF rounding | Traub, Vargas Koch, Zenklusen, *Mathematical Programming* (2026), DOI `10.1007/s10107-026-02365-x` | Establishes a planar upper bound with one cost vector | RB-003 fixes one gadget, imposes two simultaneous nonincrease constraints, and solves the exact extremal value for that model |
| Series-parallel unsplittable multiflows | Majthoub Almoghrabi, Skutella, Warode, *Mathematical Programming* (2026), DOI `10.1007/s10107-026-02392-8` | Strong integrality/decomposition on series-parallel digraphs | The released gadget lies outside that positive class; RB-003 is a two-scenario fixed-gadget obstruction |
| Classical single-source unsplittable flow | Dinitz, Garg, Goemans, *Combinatorica* 19 (1999), DOI `10.1007/s004930050043` | Foundational one-source rounding framework | Does not state the RB-003 two-scenario exact fixed-gadget theorem |
| Arc-wise lower and upper discrepancy | Morell and Skutella, *Mathematical Programming* 192 (2022), DOI `10.1007/s10107-021-01704-4` | Simultaneous load bounds rather than multiple cost budgets | Different constraints and objective |
| Multicriteria/QoS unsplittable flow | Applied traffic-engineering formulations with several path metrics | Shows that multiple constraints occur in applications | Typically solves capacity/QoS routing instances; not rounding a fixed fractional flow while preserving two linear scenario costs, and not the exact `17/8` gadget theorem |
| Robust/reroutable flow | Robust and failure-scenario flow literature | Uses scenarios or contingencies | Usually concerns demand uncertainty, edge failure, recourse, or max-flow feasibility rather than simultaneous cost nonincrease against one fractional baseline |
| Threshold and simple-game dimension | Classical weighted-game/threshold-function literature | Intersections of two positive thresholds can represent nonthreshold monotone families | RB-003 does not claim that general representation theory as novel; its contribution is the shared-baseline SSUF coupling and exact overload analysis |

## Search result

Targeted searches did not locate an indexed paper stating the exact RB-003
formulation, the central star-triangle proof, the non-attained `17/8`
supremum, or the `1061/500` finite certificate on this graph.

This absence is weak evidence only. It cannot exclude:

- private or unpublished work;
- differently described multicriteria formulations;
- unindexed conference material;
- concurrent work after Rybin's disclosure; or
- a general theorem that specializes to RB-003 without using its terminology.

## Safe novelty wording

Use:

> A targeted search found no indexed match for the exact fixed-gadget
> two-scenario formulation or the value `17/8`; priority and overlap checks
> remain open to correction.

Do not use “first,” “unique,” or “novel” without additional expert and
bibliographic review.
