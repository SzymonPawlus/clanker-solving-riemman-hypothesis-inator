# Kill-criteria — fixed before any computation

Attack: raise the lower bound on $a_{16}$ (separation 1, triangle side $a$) above the repo's
current $5\sqrt3/2 = 4.330127$, by exhibiting a **15-piece covering of $T_a$ with every piece of
diameter strictly $< 1$**, exactly certified.

Author: `claude` (N1), 2026-08-22. Written **before** running anything.

## The mechanism (so the criteria are about the right quantity)

If $T_a$ is covered by 15 sets each of diameter $< 1$, then 16 points at pairwise distance
$\ge 1$ cannot fit in $T_a$ (pigeonhole: two points in one piece would be $< 1$ apart, and the
problem's separation is **non-strict**, so "diameter $\le 1$" is *not* enough — see §1 of the
write-up). Hence $a_{16} \ge a$. The bound reported is $a_{16} \ge a^\star$ where $a^\star$ is the
supremum of side lengths for which such a covering is exhibited.

## Criteria

**K1 (primary, no-improvement).** If the best exactly certified $a^\star$ from the whole session
is $\le 5\sqrt3/2 = 4.3301270$, the attack has produced nothing: record the measurement, mark the
approach `refuted` for this piece budget, and stop. No re-scoping to a different $n$.

**K2 (diminishing returns).** If the float optimiser's best max-diameter $D$ at the reference side
$a_0$ implies $a_0/D < 4.3518$ (i.e. under $+0.5\%$ on the lattice, which is the size of the gain
the same optimiser produced at $N=28$ in `eo-covering-construct` §3), then the power-diagram /
convex-partition family has nothing structurally new here at $N=15$; stop searching, certify what
there is, and report the measurement as the finding.

**K3 (sanity / §7 tripwire).** Melissen–Schuur (1995) give an explicit 16-point packing with
$a_{16} \le 4.62476$. Any covering claiming $a^\star > 4.62476$ is **wrong** — the likely causes,
in order, are a piece of diameter marginally over 1 accepted by a non-strict test, a gap in the
union that the area identity failed to catch, or an $a$-vs-$s$ normalisation slip. On such an
output: stop, do not report a bound, report it to the manager as a candidate defect per
`../../../../RULES.md` §7.

**K4 (area ceiling).** A piece of diameter $<1$ has area $< 3\sqrt3/8$ *if* the hexagonal bound is
the truth (it is asserted, not cited, in `eo-covering-construct` §5.3), and the corner pieces have
area $\le \pi/6$ (proved). With 3 corner + $E \ge 9$ edge + interior pieces this caps
$\frac{\sqrt3}{4}a^2 \le 3\cdot\frac{\pi}{6} + 9\cdot 0.6095 + 3\cdot\frac{3\sqrt3}{8}$, i.e.
$a \lesssim 4.5603$. If the search stalls within $1\%$ of that ceiling, stop — the remaining gap
is the joint-infeasibility of the per-piece ceilings (`eo-covering-construct` §4), not something a
longer run fixes.

**Budget.** One hour of compute (`RULES.md` §6.6), checkpointed to disk.

## What is *not* a kill

Failing to reach the packing bound 4.62476 is expected and is not a kill: the covering route is
known (same file, §3) to sit below the truth. Any exactly certified $a^\star > 4.3301270$ is a
genuine improvement to an open case and is the intended deliverable.
