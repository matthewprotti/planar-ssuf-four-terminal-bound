# First Adversarial Review Brief — Unequal-Cost Fixed Topology

## Review posture

Treat UC-001 through UC-009 as false until reconstructed from the fixed graph,
released definitions, and files in this directory.  Do not rely on the
narrative of how the claims were found.

## Required attacks

### A. Cost reduction

1. Re-derive the fractional and unsplittable costs from arc costs, not abstract
   path labels.
2. Check both directions of
   \(C(S)\le C(x)\iff k(S)\ge k\cdot p\).
3. Attack zero, negative, unequal, scaled, and demand-dependent cost cases; state
   exactly where positivity is used.
4. Verify the converse threshold realization and identify what it does not say
   about optimizing \(p\).

### B. Census completeness

1. Independently enumerate all 168 antichains/upward families on four labels.
2. Reconstruct all 149 threshold witnesses without importing the constructor's
   family list.
3. Check that searching thresholds only at subset sums is complete.
4. Validate every recorded family bitmask, minimum antichain, weight vector, and
   threshold.
5. Determine whether a witness with weight above 4 could represent one of the
   19 excluded families despite the finite search.

### C. Nonthreshold certificates

1. For each two-trade, verify membership signs and equality of incidence sums.
2. Re-derive the threshold contradiction, including strictness for infeasible
   sets.
3. Check duplicate-set trades and degenerate incidence vectors.
4. Confirm the empty family is the only excluded family not covered by a
   two-trade and that the full set must be feasible.

### D. Feasible-singleton lemma

1. Compute every trunk and terminal-private deviation for a singleton-cheap
   routing.
2. Look for a positive contribution from an expensive terminal exceeding one.
3. Verify the normalization \(d_{\max}=1\) is applied correctly.

### E. Every-pair theorem

1. Reconstruct the deductions \(\sum p_i>1\) and \(\sum p_i\le2\).
2. Attack the cheapest-coordinates argument for \(2<r\le3\) and
   \(3<r\le4\).
3. Check that sorting costs is only a scalar argument and does not silently
   relabel the fixed topology.
4. Identify every line of the released restricted-model reverse proof that
   might still depend on equal full-route costs.
5. Verify that all private-arc deviations are covered when the released proof is
   reused.
6. Reconstruct the lower-bound inclusion of the equal-cost family in this cell.

### F. Reduced search space

1. Independently classify the 54 singleton families, the one every-pair cell,
   and the 94 remaining cells.
2. Verify the count of 15 permutation orbits.
3. Do not treat an arbitrary terminal permutation as a symmetry of the overload
   objective unless an accompanying graph/arc automorphism is proved.

### G. Novelty and concurrent work

Search unequal-cost SSUF rounding, weighted threshold Boolean functions,
trade robustness, four-variable threshold-function classifications, and fixed-
topology discrepancy optimization.  Similar terminology or a classical count
must be separated from any genuinely new SSUF consequence.

## Admissible outcomes

- exact counterexample;
- corrected proof with named dependency;
- independent census and certificate replay;
- independently reconstructed PASS with precise scope;
- unresolved obligation tied to a claim-ledger ID.

“Looks right,” numerical agreement, and generic confidence scores are not
review outcomes.
