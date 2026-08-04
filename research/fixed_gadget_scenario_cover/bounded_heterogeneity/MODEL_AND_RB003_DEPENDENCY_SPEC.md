# Model and RB-003 Dependency Specification

**Purpose.** This file makes explicit the model and the exact imported branch
statement used by the repaired bounded-heterogeneity draft. It is included so
that equation (10) and the scope of NG-005 can be reviewed without guessing at
unstated hypotheses.

This is a dependency specification, not a replacement for reviewing the pinned
RB-003 proof itself.

## 1. Pinned sources

### RB-003 theorem package

- repository: `matthewprotti/planar-ssuf-four-terminal-bound`
- review snapshot commit:
  `102988d5f4025b2ae081aea7fbed0e16fcc7de2a`
- theorem file:
  `research/two_scenario_global_constant/TWO_SCENARIO_GLOBAL_CONSTANT.md`
- Git blob SHA reported by the GitHub connector:
  `d272487f606f4653380636a551ea30ca4642d27f`
- contextual dependency file:
  `research/two_scenario_global_constant/BASELINE_CONTEXT_AND_DEPENDENCIES.md`

The theorem file states the cost-nonincreasing two-scenario value

\[
\beta_G^{(2\mathrm{sc})}=\frac{17}{8},
\]

and contains the branch reduction reproduced in Section 5 below.

### One-scenario census baseline

- source commit:
  `aaa472492d72e4c567d699eface450e376caece2`
- package path:
  `research/unequal_cost_fixed_topology/`
- `artifact_manifest.json` Git blob SHA:
  `1c694e11f36eca0dda5ea66eeebae12bb0ac78d1`
- pinned `round2_replay_report.json` SHA-256:
  `4b4bca57dcb8c194838f19058d55aa57a2aa1f6c677783dc52df992ca979f53c`
- pinned `threshold_family_census.py` SHA-256:
  `d7db08b7bcc11592a96e17bfca4b6605bcec1143b8752d8de30e195f3e5d6747`
- pinned `exact_open_cell_witnesses.py` SHA-256:
  `0bccef952e62551d55e8eeb35d56faad8e76088a0b97b9b6a0b28b94d2bd83e3`

The complete census source tree is not duplicated in this review archive.
Therefore claims imported from that baseline remain conditional on the pinned
commit and digest. The numerical scout generator and the original next-gap
verifier supplied in the handoff are included under `source_inputs/`.

## 2. Graph and designated paths

The directed graph has source `s`, trunk vertices `v1,...,v5`, terminals
`t1,...,t4`, and trunk arcs

\[
a_1=sv_1,\quad a_2=v_1v_2,\quad a_3=v_2v_3,\quad
 a_4=v_3v_4,\quad a_5=v_4v_5.
\]

The terminal-private arcs are

\[
e_1=st_1,\ c_1=v_3t_1,\ e_2=st_2,\ c_2=v_5t_2,
\]

\[
e_3=v_1t_3,\ c_3=v_5t_3,\ e_4=v_2t_4,\ c_4=v_4t_4.
\]

Each terminal has exactly two designated paths:

| terminal | `E_i` | `C_i` |
| ---: | --- | --- |
| 1 | `e1` | `a1 a2 a3 c1` |
| 2 | `e2` | `a1 a2 a3 a4 a5 c2` |
| 3 | `a1 e3` | `a1 a2 a3 a4 a5 c3` |
| 4 | `a1 a2 e4` | `a1 a2 a3 a4 c4` |

The verifier re-encodes this path table graph-natively and independently by
support sets, then compares the two orientations on every routing.

## 3. Fractions, costs, and feasible E-sets

Terminal `i` has demand \(d_i>0\). The fractional flow sends fraction
\(q_i\in[0,1]\) on `E_i` and fraction \(1-q_i\) on `C_i`.

For scenario `j`, let

\[
k_i^{(j)}
=d_i\bigl(\operatorname{cost}_j(E_i)-
          \operatorname{cost}_j(C_i)\bigr)>0.
\]

An unsplittable routing is represented by its E-set
\(R\subseteq[4]\). Scenario-wise cost nonincrease is exactly

\[
k^{(j)}(R)\le k^{(j)}\!\cdot q
\qquad\text{for every scenario }j.
\tag{D1}
\]

No equality of fractional and unsplittable scenario costs is required.
Every positive difference vector is graph-realizable by placing the
corresponding cost on private E-only arcs.

Normalize

\[
d_{\max}=1,
\qquad h_i=d_iq_i,
\qquad \ell_i=d_i(1-q_i),
\qquad H=\sum_i h_i.
\tag{D2}
\]

For an instance, let

\[
t=\min_{R\text{ satisfying (D1)}}
   \max_{a\in\mathcal A(G)}\bigl(y^R(a)-x(a)\bigr).
\tag{D3}
\]

## 4. Arc-deviation identities used by the new proofs

The C-minus-E trunk supports are

\[
I_1=\{a_1,a_2,a_3\},\qquad
I_2=\{a_1,a_2,a_3,a_4,a_5\},
\]

\[
I_3=\{a_2,a_3,a_4,a_5\},\qquad
I_4=\{a_3,a_4\}.
\tag{D4}
\]

For E-set `R`, the deviation on trunk arc `a` is

\[
\sum_{i\notin R:\ a\in I_i}h_i
-
\sum_{i\in R:\ a\in I_i}\ell_i.
\tag{D5}
\]

Every positive private-arc deviation is at most \(d_i\le1\).
The all-C routing has trunk maximum exactly \(H\), attained on \(a_3\).

When singleton E-set \(\{r\}\) is feasible, direct evaluation gives the
following maximum trunk deviations:

\[
\begin{array}{c|c}
r&\text{maximum trunk deviation}\\
\hline
1&H-h_1\\
2&H-d_2\\
3&\max\{h_1+h_2,\ H-d_3\}\\
4&H-h_4.
\end{array}
\tag{D6}
\]

These identities are the missing hypotheses behind the repaired derivation of
equation (10). In particular, they imply the required coordinate bounds only
under the standing assumption \(t>2\).

## 5. Exact RB-003 branch reduction imported by the bounded proof

The repaired bounded proof imports the following implication from RB-003:

> Assume a legal two-scenario instance has \(t>2\). Then no E-pair is feasible.
> At least three singleton E-sets are feasible. The all-four-singleton branch
> has value at most two. Hence exactly three singletons are feasible; let `u`
> be the unique non-omittable terminal. Up to swapping scenarios, one scenario
> supplies a blocker star centred at `u`, and the other blocks all three pairs
> inside \(A=[4]\setminus\{u\}\). If `u` is an outer terminal (`1` or `4`),
> the branch has value at most two. Thus any value above two lies in the
> **central star-triangle branch**, with \(u\in\{2,3\}\).

In that central branch, `A` contains two outer terminals and one central
terminal. The bounded proof additionally uses:

- the star scenario strictly blocks singleton \(\{u\}\);
- the triangle scenario strictly blocks every pair in `A`;
- each singleton in `A` is feasible under both scenarios; and
- equations (D2)-(D6).

No unconditional inequality of the form (10) is imported. The exact
counterexample in the repaired draft shows that such an unconditional claim
would be false.

## 6. Orientation warning

The RB-003 and many-scenario material uses `q` as the **E-path fraction** and
labels a routing by its **E-set**. The one-scenario census and F064 discussion
use `p` as the **C-path fraction** and label a routing by its **C-set**. They
are related by

\[
p_i=1-q_i,
\qquad C=[4]\setminus R.
\]

The v2 verifier checks both orientations against the graph path table.

## 7. Review consequence

With this specification in the archive, the scope of the bounded proof is no
longer implicit. A full release decision still requires checking the imported
branch reduction against the pinned RB-003 source rather than treating this
summary as an independent proof of RB-003.
