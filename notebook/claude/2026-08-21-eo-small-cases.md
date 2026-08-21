# 2026-08-21 — Prover C: reconstructing the proven Erdős–Oler cases

Role switch: literature lane closed (no egress, see `2026-08-21-eo-literature.md`), reassigned as
third prover. Write-up: `problems/circle-packing-equilateral-triangle/attacks/eo-small-cases/`;
code: `experiments/packing-eo-small-cases/check.py`.

## Result

- **k = 3 (n = 5, a < 2): proved.** Four cells of side $a/2 < 1$, each of diameter $< 1$, so at
  most one point each; 5 > 4. Three lines. The bound is attained by the $T(3)$ lattice minus its
  apex at $a = 2$, verified exactly.
- **k = 4 (n = 9, a < 3): not proved.** Stopped on my own kill-criterion. Best proved bound
  $a \ge (\sqrt{73}-3)/2 = 2.7720$, which is Oler's, not mine.
- **k = 5: not attempted**, per the plan's condition.

44 exact checks, all passing, no floats in any decision.

## The thing I actually think is worth the slot

Two exact facts, both machine-checked, both about *shape of mechanism* rather than about any
particular $n$:

**1. The pigeonhole's deficit is $\frac{(k-2)(k-3)}{2}$.** EO(k) needs a dissection into
$\Delta(k)-2$ pieces of diameter $<1$; the uniform $(k-1)$-fold subdivision gives $(k-1)^2$. The
difference is $\le 0$ **iff $k \le 3$**. So the method is not "weak for large k" — it is exactly
sufficient at $k=3$ and off by 1, 3, 6, **10**, 15 at $k = 4,5,6,7,8$. At $k = 7$ a pigeonhole
argument starts ten pieces short.

**2. Oler must be beaten by exactly one point, for every k.** Oler's RHS at $a = k-1$ is exactly
$\Delta(k)$ — an exact rational identity, checked for all $k$ in range. So as $a \to (k-1)^-$ Oler
permits $\Delta(k)-1$ and EO needs $\Delta(k)-2$: the required gain is **1**, independent of $k$,
while the gap measured in side length collapses like $2/(2k+1)$ (0.298 at $k=3$, 0.135 at $k=7$).

The second is the one I want the other two provers to internalise. At $k = 7$ Oler is within 0.135
of the target and that reads as nearly there; it is the *same single point* as at $k = 3$, where
the side-length gap is more than twice as big. **Measure progress in points, never in side
length.** And a mechanism whose yield scales with $k$ — boundary length, area, anything
$k$-dependent — is the wrong shape: it will be hopeless at $k=7$ or will prove something false at
$k=3$. The one structure with the right signature is the three corners, which agrees with
`attacks/oler-slack-analysis/` §3 measuring stage-2 loss as exactly 1 at every $n = \Delta(k)-1$
it checked.

## Where k = 4 died, precisely

Not for lack of effort but for a reason I can state. Four decompositions, all landing on capacity
exactly 9 where 8 is needed:

| three rows | 5+3+1 | bottom row + top sub-triangle (side $2h<2$) | 5+4 | rows 1–2 + top cell | 8+1 | uniform 9 cells | 1×9 |

and I built **exact witnesses** at $a = 2.7$ showing the two non-trivial rows really do hold 5 and
3. So this is a refutation, not a failure to try: any partition-and-sum argument is capped at
$\Delta(k)-1$. The two witnesses are individually valid and jointly infeasible — closest cross pair
at squared distance exactly 1/16. **The missing unit is an interaction term between regions, which
is exactly what a partition discards.**

Generalising from partitions to covers does not help either, and I can say why: a cover by $N$
sets of diameter $<1$ needs $N \ge n^*(a) = \max\{n : a_n < a\}$, and at $a \to (k-1)^-$ that is
exactly $\Delta(k)-2$. **The dissection must be an optimal covering with zero slack.** At $k=3$ the
optimum is 4 and the trivial subdivision hits it, which is why the proof is three lines. At $k=4$
it would have to be 8; the best construction I found (three corner sectors — the maximal
diameter-1 sets at a 60° corner — plus three edge Reuleaux triangles) covers the whole boundary
with 6 and leaves three gaps pairwise 1.098 apart. 6+3 = 9 again.

**Honest limit, and I want it on the record:** that last argument is a proof only in the regime
where each edge is met by exactly three pieces. I have **not** shown 8 pieces are impossible. If
$T_3$ admits a cover by 8 sets of diameter $\le 1$, EO(4) falls out immediately by scaling. That is
a clean, self-contained open question I am leaving behind rather than pretending to have closed.

## Discipline notes

- I stated the kill-criterion before starting and it is in the write-up with its outcome. It fired
  on k = 4 and I stopped instead of re-scoping (repo `RULES.md` §6.3). The temptation to keep
  pushing on k = 4 was real; the four-decompositions-all-give-9 pattern is what convinced me the
  shortfall was structural rather than effort-shaped.
- Everything is `sketch` or `numerical`. §7's prior does not bite here — these are *known* results
  and I said so in the first paragraph of the write-up — but that cuts both ways: proving a known
  theorem is no evidence my proof is right, so k = 3 stays `sketch` and is not assumable, including
  by me.
- A pleasant free consequence: the subdivision lemma re-proves Oler's triangular case
  $a_{\Delta(k)} = k-1$ for $k \le 4$ without Oler, since $\Delta(k) > (k-1)^2$ exactly there. The
  repo now has a self-contained proof of $n = 3, 6, 10$, which previously rested entirely on the
  Oler paper.
- One thing I got wrong mid-flight and caught: I first wrote the gap-point separation as
  $45/4 - 6\sqrt3$; it is $9 - \tfrac{9\sqrt3}{2}$. Both round to nothing near each other (0.858 vs
  1.206) and the wrong one would have destroyed the argument, since it needs to exceed 1. Now
  asserted exactly in the checker rather than typeset from a scratch calculation.
