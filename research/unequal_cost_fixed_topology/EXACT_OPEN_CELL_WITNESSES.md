# Exact Interior Witnesses in Eleven Strictly Positive Cells

The current strictly positive frontier contains 83 labeled cells. The exact
checker `exact_open_cell_witnesses.py` supplies strict rational interior
instances in eleven of those cells for which **every** cost-feasible routing
has maximum upper deviation greater than one. The certificates do not solve
any cell; they provide rigorous lower bounds and exact targets for upper-bound
work.

| Cell | Minimal feasible sets | Exact lower witness | Decimal |
| --- | --- | ---: | ---: |
| F042 | 12, 13, 23 | `1111291/1000000` | 1.1112910000 |
| F045 | 12, 13, 23, 14, 24 | `2173363/2000000` | 1.0866815000 |
| F047 | 12, 13, 23, 14, 34 | `26854219/25000000` | 1.0741687600 |
| F049 | 12, 13, 23, 24, 34 | `1350435821/1250000000` | 1.0803486568 |
| F055 | 12, 13, 14, 34 | `5509335803/5000000000` | 1.1018671606 |
| F060 | 12, 23, 14, 24 | `28085483/25000000` | 1.1234193200 |
| F061 | 12, 23, 14, 24, 34 | `88144229/80000000` | 1.1018028625 |
| F125 | 123, 124, 134, 234 | `51/50` | 1.0200000000 |
| F126 | 123, 124, 234 | `5151/5000` | 1.0302000000 |
| F129 | 123, 134, 234 | `638/625` | 1.0208000000 |
| F143 | 124, 134, 234 | `251517/250000` | 1.0060680000 |

For each instance the checker verifies with exact rational arithmetic that:

1. `k_i > 0`, `0 <= p_i <= 1`, `0 < d_i <= 1`, and `max d_i = 1`;
2. the threshold inequalities realize exactly the named labeled family, with a
   positive strict losing margin;
3. every feasible cheap set is enumerated; and
4. all five trunk and four positive private-arc deviations are checked.

The strongest current certificate is F060:

```text
k = (1667/5000, 417/1250, 1/10000, 3329/10000)
p = (2577/10000, 4867/10000, 3/10000, 2563/10000)
d = (1, 1859/2500, 9957/10000, 1999/2000)
exact minimum feasible maximum deviation = 28085483/25000000
```

The strict losing margin is `13/5000000`, so the point is genuinely inside
the F060 threshold cell rather than merely on its boundary.

None of the eleven certificates exceeds the every-pair value

`L = (299 - 41*sqrt(41))/32 ≈ 1.139747070789`.

The earlier F042 certificate `423/400` has been strengthened to
`1111291/1000000`. Numerical scouting was used only to locate candidate
points; every value retained here is re-encoded and verified exactly.
