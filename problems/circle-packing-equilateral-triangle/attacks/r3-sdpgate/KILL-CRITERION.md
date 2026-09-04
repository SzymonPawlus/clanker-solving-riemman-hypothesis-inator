# Kill-criterion for approach X (symmetry-adapted moment relaxation) — **FIRED**

**This file records the falsification of a direction. It claims no bound and no packing.**

## The criterion, as written in the triage file

From
[`../r3-approaches/README.md`](../r3-approaches/README.md), proposal **X**, verbatim:

> **Kill-criterion.** Measure the level-2 and level-3 relaxation *slack* on solved instances
> ($n = 5, 7, 8, 12$) using the dense formulation, which needs no symmetry code and runs in
> minutes. If the relaxation value is more than a few percent below the known optimum at those
> $n$, **retire the whole direction permanently** and write up the slack table — that is a
> decisive negative and a first-class outcome. Only if slack is small is the symmetry-adapted
> SDP worth building.

Round 1's approach C stated the same gate in a sharper form:

> (ii) On the calibrated small cases: if the level-2 (or affordable level-3) bound's relative
> slack against the known optimum exceeds ~1%, the hierarchy will not distinguish conjectured
> optima from nearby values at open $n$; abandon and record the slack table.

## Verdict

**Fired, by roughly two orders of magnitude on the stated threshold.** The relative slack of the
dense level-2 relaxation against the published exact $d(n)$ is **38.8–68.6 %** across
$n = 4,5,6,7,8,10,12$ — not "a few percent", and not 1 %. See
[`README.md`](./README.md) §3 for the table and §4 for the diagnosis.

The gate was applied honestly and the direction is **retired**. Nothing about SDP size was the
obstruction: the size claim that motivated re-opening the direction was re-derived here
independently and is **correct in every particular**. The relaxation is simply slack.

## What is *not* claimed

- No lower bound on $d(n)$ or $s(n)$ for any $n$ is asserted anywhere in this attack. The
  relaxation values are floating-point SDP output, hence `numerical` hypotheses about bounds,
  never bounds (problem [`../../RULES.md`](../../RULES.md) §0, repo `RULES.md` §3).
- No statement is made about levels $\ge 4$ of the hierarchy, which were not run and are far out
  of reach at $n = 16$ either way.
