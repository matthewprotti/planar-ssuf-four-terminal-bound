# Exact Interior Witnesses in Five Previously Open Cells

The 94-cell remainder cannot all be eliminated by extending the feasible-
singleton bound `<= 1`. The exact checker `exact_open_cell_witnesses.py` gives
strict interior rational instances in five cells for which **every** cost-
feasible routing has maximum upper deviation greater than one.

| Cell | Minimal feasible sets | Exact lower witness |
| --- | --- | ---: |
| F126 | 123, 124, 234 | 5151/5000 = 1.0302 |
| F125 | all four triples | 51/50 = 1.02 |
| F042 | 12, 13, 23 | 423/400 = 1.0575 |
| F129 | 123, 134, 234 | 638/625 = 1.0208 |
| F143 | 124, 134, 234 | 251517/250000 = 1.006068 |

For each instance the script verifies with exact rational arithmetic that:

1. `k_i > 0`, `0 <= p_i <= 1`, `0 < d_i <= 1`, and `max d_i = 1`;
2. the threshold inequalities realize exactly the named labeled family, with a
   positive strict losing margin;
3. every feasible cheap set is enumerated; and
4. all five trunk and four positive private-arc deviations are checked.

These are lower bounds for individual cells, not cell optima. In particular,
none exceeds the every-pair value

`L = (299 - 41*sqrt(41))/32 ≈ 1.139747070789`.
