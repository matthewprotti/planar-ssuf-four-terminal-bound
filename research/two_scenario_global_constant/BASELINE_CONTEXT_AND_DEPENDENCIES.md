# Baseline Context and Dependency Map

This file separates facts used in the proof of RB-003 from contextual facts
used only for comparison or naming.

## Public fixed-topology release

The public repository is:

`matthewprotti/planar-ssuf-four-terminal-bound`

The immutable public disclosure commit is:

`087204eda4cc490cb59dd1988d7383c406288d2e`

In the restricted equal-full-route-cost, all-pairs-feasible fixed-topology
regime, that release proves the exact supremum

\[
L=\frac{299-41\sqrt{41}}{32}.
\]

RB-003 uses `L` only as a contextual arithmetic benchmark. The proof of the
upper or lower bound `17/8` does not depend on the proof of `L`.

## Follow-on one-scenario census

The follow-on fixed-topology research baseline used for the established family
ordering is commit:

`d24a3df8ebe63158cb9a8087699272dbf50642eb`

Its exact four-label census partitions the 168 monotone families as:

- 149 positive scalar-threshold families;
- 18 nonempty nonthreshold families; and
- one empty family, inadmissible because the full C-set / empty E-set is always
  feasible.

The v5 package regenerates this finite partition in the E-set
orientation: it supplies an explicit positive threshold witness for each of
the 149 represented downsets and an exact two-trade contradiction for each of
the 18 excluded nonempty downsets.

## The label `F126`

The label is not intrinsic. In the established ordering, `F126` is the upward
C-family whose minimal feasible sets are

\[
123,\quad124,\quad234.
\]

Equivalently, its feasible E-sets are

\[
\varnothing,\quad\{1\},\quad\{3\},\quad\{4\}.
\]

RB-003 states this family intrinsically, so the theorem does not depend on the
historical ID or ordering.

## Earlier two-scenario results

A prior Track B package established that every nonempty four-label monotone
family is representable by at most two positive scenarios on a shared uniform
baseline (allowing baseline zero for the all-subsets endpoint), and that the 18
newly accessible nonthreshold cells have exact fixed-topology value 2.

Those results provide research context, but they are not used in the proof of
the global upper bound `17/8`. The global theorem classifies actual
shared-baseline scenario vectors directly through the blocker argument.

## Review dependency status

The second-round hostile proof-only report on v4 is included verbatim as
`ADVERSARIAL_PROOF_ONLY_REVIEW_RB003_V4.md`. It is external supporting evidence,
not a premise of the proof. The v5 theorem integrates every local edit requested
or recommended in that report. The v5 archive itself has not yet been
re-signed by the reviewer.

## Dependency summary

The proof of RB-003 depends only on:

1. the graph and C/E path table reproduced in
   `TWO_SCENARIO_GLOBAL_CONSTANT.md`;
2. elementary linear-cost algebra;
3. the two-colour fractional-matching lemma;
4. the one-knapsack pair-blocking lemma; and
5. the explicit star-triangle optimization and rational lower sequence.

The values `L`, `149/18/1`, and the name `F126` are contextual and naming
information, not hidden proof dependencies.
