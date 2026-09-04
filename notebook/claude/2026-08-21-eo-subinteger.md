# 2026-08-21 — sub-integer refinement of the corner-occupancy relaxation (worker W4)

Task: take the one gap Prover E named in its own write-up
(`attacks/eo-corner-squeeze/` §7 — "the thresholds are integers, and a finer partition … could in
principle be infeasible where mine is feasible") and find out whether it is real.

Attack dir: `problems/circle-packing-equilateral-triangle/attacks/eo-subinteger-relaxation/`
Code: `experiments/packing-eo-subinteger/`

## Answer

**The gap is real, and it is not enough.**

- Integer thresholds at $k=4$: LP bound $9 = n$. Break-even, reproducing the predecessor exactly.
- Sub-integer thresholds ($a/3$, $a/6$) at $k=4$: LP bound $8 < 9$. **Decides** Erdős–Oler at
  $k=4$, with a four-piece cover valid uniformly for every $a<3$ and containing no $d(n)$ value.
- $k=5$ ($M$ up to 9), $k=6$ ($M$ up to 6): back to break-even, LP $=\lfloor\mathrm{Oler}(a)\rfloor
  = n$. K1 met at $k=5$. The $k=5$ bisection returns $a^{*}(5) = a_0(5)$: the refined family, 81
  cells and 1918 boxes, reproduces Oler exactly and adds nothing.
- $k=7$ recorded but not used as a decision procedure: LP $= 27 = \lfloor\mathrm{Oler}\rfloor$,
  i.e. break-even, exactly as the efficiency argument predicted before it was run.

So a refinement crossed break-even for the first time in this project — and the crossing point is
between $k=4$ and $k=5$, which is exactly where it stops being useful.

## The thing worth keeping

The whole $k=4$ certificate is four lines and needs no computation:

> Put $t=a/3<1$. The three corner triangles $\Delta_V(t)$ have diameter $<1$ (one point each);
> what is left, $\{u_A,u_B,u_C \ge t\}$, is a **regular hexagon of side $t$**, so its circumradius
> is $t<1$, so it holds at most 5 (six points in a disk of radius $<1$ would have two within an
> angular gap of $60°$, hence closer than the radius). $3+5=8<9$.

At the nearest *integer* threshold $t=1$ both capacities jump (3 and 6) and the same cover gives
15. That single jump is the whole content of "integer thresholds are too coarse".

## Two errors of mine, both caught by controls I had written first

1. **Degenerate regions.** `capacity` returned 1 for any region whose polygon had fewer than 3
   vertices. A corner box can degenerate to a **segment**, and a segment of length $\ell$ holds
   $1+\lfloor\ell\rfloor$ points. K3 found it immediately: 198 violations counting the $T(7)$
   lattice against every box. This is the dangerous direction — a capacity that is too *small*
   manufactures infeasibility, which at $k=7$ would have read as a solved open problem.
2. **Dropping the per-cell constraints.** I filtered out every box whose capacity was not below
   its cell count "as vacuous". That removes the singleton constraints, leaves the LP variables
   unbounded, and made the covering dual infeasible. Correct test:
   $\mathrm{cap}(R) \ge \sum_{c \subseteq R}\mathrm{cap}(c)$.

Neither would have been caught by re-reading the code; both fell out of running the thing on cases
whose answer is known. That is the second time this week the same discipline has paid.

## Structural reading (why it stops)

For a partition into pieces of capacity $c_i$, the average "efficiency" $\mathrm{area}/c$ must
reach $\mathrm{area}(T_{k-1})/(T(k)-2) = 0.433, 0.487, 0.533, 0.570, 0.600$ at $k=3..7$. The best
periodic pattern the capacity toolkit supports (hexagons of side just under 1, capacity 5, with
the two small triangles per hexagon that any three-line arrangement forces) sits at $0.495$; the
best single piece is $0.520$. So $k=3,4$ are reachable and $k \ge 5$ is not, and the requirement
climbs quadratically. Equivalently: for $k \ge 5$ the best partition bound is *worse* than plain
Oler on the whole triangle, so the refinement stops contributing anything at all.

## Bookkeeping

- No git commands were run; no PR, no issue comment (worker restriction).
- Files created: the attack dir, `experiments/packing-eo-subinteger/**`, this journal file.
- Lemma P of `../eo-corner-squeeze/` §3 re-derived and exactly verified for $k \le 12$; correct,
  and break-even at $a = k-1$ exactly as its author says. Same-family, so no status change.
