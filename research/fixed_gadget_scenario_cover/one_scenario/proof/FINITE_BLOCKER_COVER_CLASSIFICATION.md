# Exact Four-Label Blocker-Cover Classification

This appendix supplies the finite classification used in Section 6 of `GLOBAL_ARBITRARY_ONE_SCENARIO_THEOREM.md`.

## 1. Setup

Let `V` be the feasible E-singletons and let `G` be the graph on `V` whose edges are the feasible E-pairs. There is no feasible E-triple. For positive weights `w_i`,

\[
ij\in E(G)\iff w_i+w_j\le1.
\]

After sorting the vertex weights, neighborhoods are nested. Thus `G` is a threshold graph. On at most four vertices this excludes induced `P4`, `C4`, and `2K2`.

The minimal blocker hypergraph consists of:

- every singleton outside `V`;
- every missing edge inside `V`; and
- every triangle of `G`.

For a blocker hypergraph `B`, the cover polyhedron is

\[
P(B)=\{y\ge0:y(T)\ge1\text{ for every }T\in B\}.
\]

The two-stage choice in the main theorem—first minimize `q·y`, then `sum(y)`, then take an extreme point of that face—is coordinatewise undominated. Thus only coordinatewise-undominated extreme covers need be classified. Every extreme cover lies in `[0,1]^4`.

## 2. Canonical table

Labels are chosen canonically within each graph row. “Fractional vertices” lists every nonintegral undominated extreme cover; the remaining undominated vertices are integral.

| `|V|` | Feasible edges | Minimal blockers | Fractional undominated extreme covers |
| ---: | --- | --- | --- |
| 0 | none | `1,2,3,4` | none |
| 1 | none on `V={1}` | `2,3,4` | none |
| 2 | none on `V={1,2}` | `12,3,4` | none |
| 2 | `12` | `3,4` | none |
| 3 | none on `V={1,2,3}`, blocked `4` | `12,13,23,4` | `(1/2,1/2,1/2,1)` |
| 3 | `12`, blocked `4` | `13,23,4` | none |
| 3 | `12,13`, blocked `4` | `23,4` | none |
| 3 | `12,13,23`, blocked `4` | `123,4` | none |
| 4 | none | `12,13,14,23,24,34` | `(1/2,1/2,1/2,1/2)` |
| 4 | `12` | `13,14,23,24,34` | `(1/2,1/2,1/2,1/2)` |
| 4 | `12,13` | `23,14,24,34` | `(1/2,1/2,1/2,1/2)` |
| 4 | star `12,13,14` | `23,24,34` | `(0,1/2,1/2,1/2)` |
| 4 | triangle `12,13,23`, isolated `4` | `123,14,24,34` | `(1/3,1/3,1/3,2/3)` |
| 4 | paw `12,13,14,23` | `123,24,34` | `(0,1/2,1/2,1/2)` |
| 4 | `K4-34` | `123,124,34` | `(0,1/2,1/2,1/2)` and `(1/2,0,1/2,1/2)` |
| 4 | `K4` | `123,124,134,234` | separated all-pairs row |

The table contains all possible threshold graphs:

- for three vertices: 0, 1, 2, or 3 edges, with the two-edge graph necessarily a path;
- for four vertices: 0, 1, or 2 edges; at three edges either a star or a triangle; then the unique threshold forms at four and five edges; and `K4`.

A two-edge matching cannot occur because if two disjoint pairs are feasible, the two lighter endpoints are also feasible as a pair and create an additional edge. The same nested-neighborhood property excludes `P4` and `C4` at the remaining edge counts.

## 3. Direct cover calculations

The nonintegral rows can be checked without invoking the full threshold-family census.

### Three feasible vertices, no edges

The constraints are

\[
y_4\ge1,
\quad y_1+y_2\ge1,
\quad y_1+y_3\ge1,
\quad y_2+y_3\ge1.
\]

The only nonintegral undominated vertex is

\[
(1/2,1/2,1/2,1).
\]

### Four vertices with zero, one, or two feasible edges

The minimal two-element blockers form a connected nonbipartite graph. Solving four independent tight edge constraints gives the unique nonintegral undominated vertex

\[
(1/2,1/2,1/2,1/2).
\]

For the canonical two-edge row, the constraints are `23,14,24,34`; the unique fractional solution of all four equalities is again all-half.

### Feasible star

The blockers are the three leaf-pairs `23,24,34`. Their fractional vertex-cover polytope has the unique nonintegral undominated vertex

\[
(0,1/2,1/2,1/2).
\]

### Feasible triangle and isolated vertex

The constraints are

\[
y_1+y_2+y_3\ge1,
\quad y_i+y_4\ge1\ (i=1,2,3).
\]

Making all four tight gives

\[
y_1=y_2=y_3=1/3,
\qquad y_4=2/3.
\]

All other undominated extreme covers are integral.

### Four-edge paw

The constraints are

\[
y_1+y_2+y_3\ge1,
\quad y_2+y_4\ge1,
\quad y_3+y_4\ge1.
\]

The only nonintegral undominated extreme cover is

\[
(0,1/2,1/2,1/2).
\]

The outside vertex `1` is adjacent in the feasible graph to all three half-covered vertices.

### Five-edge graph

For `K4-34`, the constraints are

\[
y_1+y_2+y_3\ge1,
\quad y_1+y_2+y_4\ge1,
\quad y_3+y_4\ge1.
\]

The nonintegral undominated covers are

\[
(0,1/2,1/2,1/2),
\qquad
(1/2,0,1/2,1/2).
\]

In the first, vertex `1` is universal in the feasible graph; in the second, vertex `2` is universal. Thus each half-covered triple has all three complementary two-C routes required by Lemma 2.

## 4. Exact executable check

`reproduction/verify_global_one_scenario_theorem.py` performs two independent finite checks:

1. it constructs the 16 canonical blocker hypergraphs above and enumerates every cover vertex from all four-constraint active sets using exact rational arithmetic; and
2. it regenerates all 149 positive four-label threshold downsets from their small integer witnesses, selects the 95 with no feasible E-triple, and verifies that every nonintegral undominated cover maps to one of the canonical rows.

The first path proves the displayed finite table without using family IDs. The second path cross-checks that no positive weighted-threshold family was omitted.
