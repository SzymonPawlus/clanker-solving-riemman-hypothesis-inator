# Kill-criteria — occupancy exhaustion (covering with slack) for $n = 16$

**Written before any computation** (repo `RULES.md` §6.2). Worker O2, `claude`, 2026-08-22,
branch `claude/circle-packing-subagents-9yg5gt`, issue #97.

## The mechanism being tried

Cover $T_a$ (closed equilateral triangle of side $a$, separation-1 normalisation as in
[`../n16-covering-2/`](../n16-covering-2/)) by $N \ge 16$ convex pieces each of diameter
**strictly** $< 1$ (exact rational comparison). Any 16 points at pairwise distance $\ge 1$ then
occupy 16 *distinct* pieces; enumerate the $\binom{N}{16}$ occupancy patterns and refute each
by (a) pair pruning — two occupied pieces with exact max mutual distance $< 1$; (b) capacity
pruning — $k$ occupied pieces inside an equilateral triangle of side $< a_k$, using only
`cited` $a_k$ with $k \le 15$; (c) recursive refinement — split occupied pieces, branch on which
sub-cell holds the point, re-prune. If every pattern is refuted, $a_{16} \ge a$.

**Circularity guard.** No property of $n = 16$ is an input. The capacity table is hard-capped at
index 15 by a named constant in the code (`CAP_MAX_INDEX`); the value $4.6247636$ appears only as
a comparison target. Controls at $n = m$ cap the table at $m - 1$ for the same reason.

## Criteria

**K0 (validation gate — do not point the machinery at the open case before this).** The engine
must, at $n \in \{4, 6, 10\}$: (i) certify $a_n \ge a$ for an $a$ about 3–5 % below the known
$a_n$, and (ii) **fail to certify** (report surviving patterns, not a proof) at an $a$ just above
$a_n$ where an explicit packing exists. If (i) fails for two of the three controls after
reasonable per-control effort ($\le 10$ min compute total for all controls), or (ii) ever
produces a false refutation, the engine is untrustworthy: stop, report the failure, run nothing
at $n = 16$.

**K1 (no-improvement).** The record is $a_{16} \ge 1 + 2\sqrt3 = 4.46410\ldots$
([`../n16-covering-2/`](../n16-covering-2/), `sketch`). If by the end of the compute budget no
$a > 1 + 2\sqrt3$ is exactly certified, the lane has not beaten the record. Record honestly how
far the refutation got at each probed $a$ (patterns refuted / total, refinement depth reached,
what the surviving nodes look like), mark the wall, stop. No re-scoping to another $n$ or
another claim to survive falsification.

**K2 (cost wall).** The BnB resolution heuristic (from `experiments/circle-packing-bnb/`,
re-derived here): closing at side $a$ requires refuting phantom configurations with pairwise
distances $\ge 1 - \delta$, $\delta \approx 1 - a/a_{16}^{\text{true}}$, which needs cells of
diameter $O(\delta)$ — depth $\log_2(1/\delta)$ per piece. If a probe run's checkpoint shows the
surviving-node frontier still growing at half that probe's time cap, kill that probe at its cap
and do not extend it; the projected cost is the finding.

**K3 (§7 tripwire).** Melissen–Schuur's explicit 16-point packing sits at $4.6247636$
(`numerical`). Any exact certification at $a \ge 4.62$ is presumed to be a bug — likeliest: a
non-strict comparison accepted as strict, a capacity index off by one, a cover verifier that
missed a hole, or the pattern enumerator skipping patterns. Stop immediately, label the output a
candidate defect, report to the manager per repo `RULES.md` §7. Do not write "record" anywhere.

**Budget.** $\le 45$ min wall-clock compute, at most 1 core for any long run, every long run
time-capped in advance and checkpointed to `experiments/packing-n16-occupancy/out/` (a run
killed with nothing on disk produced nothing). All background jobs killed by this worker.

## What is *not* a kill

- A probe at $a > 1+2\sqrt3$ that times out with surviving patterns is the *expected* outcome
  (the wall is real); it kills the probe, not the write-up. The deliverable is the measured
  refutation frontier and the reproducible machinery.
- Controls passing only at 3–5 % below $a_n$ (not 0.5 %) is expected: the cost diverges as
  $a \uparrow a_n$; that divergence is part of what is being measured.
