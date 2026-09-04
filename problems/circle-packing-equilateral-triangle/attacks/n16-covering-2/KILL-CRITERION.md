# Kill-criteria — fixed before any computation

Attack: **beat** the repo's current certified lower bound $a_{16} \ge 89267/20000 = 4.46335$
(attack [`../n16-covering/`](../n16-covering/)) by exhibiting a **15-piece covering of $T_a$
with every piece of diameter strictly $< 1$**, exactly certified over $\mathbb{Q}$.

Author: `claude` (worker C1), 2026-08-22. Written **before** running anything.

## Mechanism (so the criteria measure the right quantity)

If $T_a$ is covered by 15 sets each of diameter $<1$, then 16 points at pairwise distance
$\ge 1$ cannot fit in $T_a$ (pigeonhole; the problem's separation is **non-strict**, so
"diameter $\le 1$" would *not* suffice). Hence $a_{16} \ge a$. Scale invariance: a subdivision
of the unit triangle $T_1$ with max piece diameter $D$ certifies $a^\star = 1/D$.

## Criteria

**K1 (primary, no-improvement).** If the best **exactly certified** $a^\star$ of this session is
$\le 89267/20000 = 4.46335$, the attack has produced nothing new. Record the measurement, say
where the optimiser plateaued and why, mark this lane exhausted for the 15-convex-piece family,
and stop. No re-scoping to a different $n$, no re-scoping to a different piece budget.

**K2 (diminishing returns).** If two consecutive optimisation phases of $\ge 20$ min wall clock
each improve the best *float* $a_{\max}$ by less than $2\times10^{-4}$ in total, stop searching,
freeze the exact certificate, and report the measurement as the finding.

**K3 (§7 tripwire — the one that matters).** Melissen–Schuur (1995) give an explicit 16-point
packing at $a = 4.6247636\ldots$. **Any covering claiming $a^\star > 4.6247636$ is wrong**, and a
covering *approaching* it means $n=16$ would be solved, which is an extraordinary claim. So:
- $a^\star > 4.6247636$: stop immediately, report no bound, report a candidate defect to the
  manager per `RULES.md` §7. Likely causes, in order: a piece with squared diameter $\ge 1$
  accepted by a non-strict comparison; a hole in the union that the area identity missed
  (overlap + hole of equal area); an $a$-vs-$s$ normalisation slip; a float leaking into a
  conclusion.
- $a^\star > 4.60$ (within $0.025$ of the ceiling): treat as a **candidate, not a result**.
  Rebuild the checker from scratch a third time, re-verify, and report to the manager as a
  candidate. Do not write "solved" anywhere.

**K4 (structural ceiling).** The per-piece area ceilings (corner $\le \pi/6$, generic
$\le 3\sqrt3/8$) cap this family. If the search stalls within $0.5\%$ of the ceiling implied by
the realised piece classification, stop: what remains is joint infeasibility of the per-piece
ceilings, not something a longer run fixes.

**Budget.** $\le 3$ h wall clock of compute, checkpointed. **An exact certificate is frozen at
every improvement**, never only at the end. All background jobs are killed by this worker.

## What is *not* a kill

Failing to reach $4.6247636$ is expected: a 15-piece covering cannot be tight, because the pieces
must be truncated at the boundary of $T_a$ and truncation wastes area. Any exactly certified
$a^\star > 4.46335$ is the intended deliverable.

---

## Amendment, 2026-08-22 (during the run, from the manager/verifier — recorded, not retro-fitted)

Two corrections arrived after the criteria above were fixed. They are appended rather than
edited in, so the record shows what was decided when.

1. **K4 is downgraded from a wall to a heuristic.** The per-piece figure $3\sqrt3/8=0.649519$ is
   what a *hexagonal partition achieves*; it is **not** a proved cap on the area a diameter-1
   piece may contribute. The isodiametric cap is the disk, $\pi/4=0.785398$. So the implied
   "ceiling" near $4.5603$ **is not a theorem**, and K4 must not fire as if it were: a certificate
   above $4.5603$ contradicts nothing proved and must not be discarded as obviously buggy. The
   only hard wall stays K3 at $4.6247636$ (a published packing). K4 survives only as a
   diagnostic — "the search has stopped moving near the hexagonal heuristic" — never as a reason
   to reject a verified certificate.

2. **Target raised, and every certificate must be dilated.** A certificate at side $a$ whose exact
   max squared diameter is $\Delta<1$ dilates about the chart origin by any rational
   $\mu<1/\sqrt\Delta$: squared distances and areas scale by $\mu^2$, convexity, containment and
   disjointness are preserved. So the covering exists for **every** rational $a'<a/\sqrt\Delta$,
   hence $a_{16}\ge a/\sqrt{\Delta}$. Slack left in the diameter is free bound thrown away.
   Applying this to the standing certificate ($\Delta=(49999/50000)^2$) gives
   $a_{16}\ge 446335/99998=4.46343926878\ldots$, so **K1's threshold is raised to
   $446335/99998$**: the session produces nothing unless it certifies strictly more than that.
