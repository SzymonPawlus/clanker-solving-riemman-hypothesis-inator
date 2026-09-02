# Kill-criteria — fixed before any computation

**Attack.** Raise the certified lower bound on $a_{16}$ (separation 1, equilateral triangle of
side $a$) above the repo's current record $a^\star = 89267/20000 = 4.46335$, by covering $T_a$
with **15 pieces of diameter strictly $< 1$ that are not required to be convex polygons** —
circular sectors at the $60^\circ$ corners, constant-width and other curved convex pieces at the
boundary, non-convex (L-/crescent-shaped) pieces in the interior, and **overlapping** pieces
(a covering need not be a partition).

Author: `claude` (worker C2), 2026-08-22. Written **before** running anything.

## Mechanism (so the criteria measure the right quantity)

If $T_a$ is covered by 15 sets each of diameter $<1$ then 16 points at pairwise distance $\ge 1$
cannot lie in $T_a$ (two would share a piece and be $<1$ apart; separation in this problem is
**non-strict**, so diameter *exactly* 1 is not enough). Hence $a_{16}\ge a$. Pieces need **not**
lie inside $T_a$ and need **not** be pairwise disjoint; only $\bigcup_i P_i \supseteq T_a$ and
$\operatorname{diam} P_i < 1$ are required.

## Criteria

**K0 (shape-freedom triviality — checked first, costs no compute).** Before optimising anything,
settle whether the extra shape freedom can help *at all*. Two reductions are candidates:

* non-convex $\to$ convex, via $\operatorname{diam}(\operatorname{conv}S)=\operatorname{diam}(S)$;
* convex $\to$ convex **polygonal**, via a finite outer approximation by supporting half-planes.

**If both reductions are valid, the whole premise of this attack is empty**: the supremum
$a^\star(15)$ over arbitrary pieces equals the supremum over convex polygons, the convex record
$4.46335$ is not beatable *by shape*, and the correct outcome is to report that as the finding and
spend no compute on sectors, Reuleaux pieces or non-convex pieces. In that case the only remaining
freedom relative to the previous attack is **overlap** (equivalently: partitions into non-convex
cells), and K1 below applies to that alone.

**K1 (primary, no-improvement).** If the best **exactly certified** $a^\star$ produced in this
session is $\le 89267/20000 = 4.46335$, the attack has produced no numerical improvement: record
the measurement, say where the loss actually sits, and stop. No re-scoping to another $n$ and no
re-scoping to "the search just needs longer".

**K2 (diminishing returns).** The predecessor's float search plateaued at
$a_{\max}\approx 4.4637$–$4.4639$ across four independent seeds. If my own search, from a
*different* family (overlapping pieces / non-partition topologies), also plateaus inside
$[4.4630, 4.4645]$, then the plateau is a property of the covering problem at $N=15$ and not of
the piece family; stop searching and report the plateau as the measurement.

**K3 (§7 tripwire).** Melissen–Schuur (1995) exhibit a 16-point packing at $a = 4.6247636$. Any
covering claiming $a^\star > 4.6247636$ is **wrong**. Likely causes, in order: a piece of diameter
marginally $\ge 1$ passed by a non-strict test; a hole in the union that an area identity did not
catch (with overlapping pieces the area identity proves *nothing* and coverage must be verified
directly); an $a$-vs-$s$ normalisation slip. On such output: stop, do not report a bound, report to
the manager as a candidate defect per `../../../../RULES.md` §7.

**K4 (soundness of the covering proof).** Overlapping pieces invalidate the previous attack's
"areas sum to $|T_a|$ + pairwise interior-disjoint" argument. Every certificate here must verify
coverage **directly** by exact rational polygon difference: subtract the pieces from $T_a$ one at
a time and check the remainder is empty. If I cannot make that check run exactly, no certificate
is issued.

**Budget.** One hour of compute (`RULES.md` §6.6), checkpointed to disk; every background job I
start, I kill.

## What is *not* a kill

Failing to reach $4.6247636$ is expected and is not a kill — the covering route is known to sit
below the truth. Establishing that shape freedom is worthless (K0) is a **success**, not a
failure: it closes a direction, which is exactly what `RULES.md` §0 asks for.
