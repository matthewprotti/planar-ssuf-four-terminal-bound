# Exact Trunk and Private-Arc Envelope

**Status:** analytic fixed-gadget lemma, added in the first-human-review
derived copy on 2 August 2026.  
**Scope:** all sixteen designated routings on the fixed thirteen-arc gadget;
arbitrary normalized demands and fractional route shares.  
**Purpose:** make explicit the arc bound used by GM-005 and GM-006. This lemma
does not use a finite atlas or numerical optimization.

## Model

Let (R\subseteq[4]) be the set of terminals routed on their E paths. Normalize
(d_{\max}=1), so (0<d_i\le1), and let terminal (i) send fractional share
(q_i\in[0,1]) on E. Put

\[
h_i=d_iq_i,\qquad \ell_i=d_i(1-q_i).
\tag{1}
\]

The C-minus-E trunk supports are

\[
I_1=\{a_1,a_2,a_3\},\quad
I_2=\{a_1,a_2,a_3,a_4,a_5\},
\]

\[
I_3=\{a_2,a_3,a_4,a_5\},\quad
I_4=\{a_3,a_4\}.
\tag{2}
\]

## Lemma

For every trunk arc (a), the unsplittable-minus-fractional deviation is

\[
\Delta_a(R)=
\sum_{\substack{i\notin R\\a\in I_i}}h_i
-
\sum_{\substack{i\in R\\a\in I_i}}\ell_i.
\tag{3}
\]

Consequently,

\[
\Delta_a(R)
\le
\sum_{\substack{i\notin R\\a\in I_i}}h_i
\le
\sum_{i\notin R}h_i
\le 4-|R|.
\tag{4}
\]

Every positive private-arc deviation is either (h_i) on the C-private arc
when (i\notin R), or (\ell_i) on the E-private arc when (i\in R). It is
therefore at most (d_i\le1).

Hence the normalized maximum positive deviation over all thirteen arcs obeys

\[
M(R)\le \max\left\{1,\sum_{i\notin R}h_i\right\}
\le \max\{1,4-|R|\}.
\tag{5}
\]

In particular:

- a singleton E-set has value at most (3);
- an E-triple has value at most (1); and
- the all-C route has exact value (H=\sum_i h_i), witnessed on (a_3),
  because all four supports contain (a_3).

## Proof

Switching terminal (i) from its fractional split to C adds (d_iq_i=h_i)
on every arc of (I_i); switching it to E subtracts
(d_i(1-q_i)=\ell_i) there. Summing these signed contributions gives (3).
Dropping the nonpositive second sum and using (h_i\le d_i\le1) gives (4).

Each terminal has its own two private arcs, used by no other terminal. The
private-arc statement follows by the same one-terminal calculation, so taking
the maximum of the trunk and private bounds proves (5). For (R=\varnothing),
equation (3) on (a_3) is (\sum_i h_i=H); no trunk deviation exceeds (H)
and no private positive deviation exceeds its corresponding (h_i\le H).
Thus the all-C value is exactly (H). \(\square\)

## Evidence boundary

The proof above is the authority. The companion program
`reproduction/verify_arc_envelope.py` reconstructs the path-incidence vectors,
checks the signed coefficient identity on every trunk and private arc for all
sixteen routings, and exercises (5) on an exact rational grid. It is
corroboration, not a proof assistant and not external review.
