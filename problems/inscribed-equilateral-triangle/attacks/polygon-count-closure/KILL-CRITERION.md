# Kill-criterion — `polygon-count-closure`

**Written before any computation in this lane**, per repo [`RULES.md`](../../../../RULES.md) §6.2
and this problem's [`RULES.md`](../../RULES.md). Provenance paragraph below says exactly what had
and had not happened when this file was written, because a kill-criterion written after the
answer is known is worthless.

## Provenance — what had happened when this was written

Written **after** reading, and **before** running a single line of code in this lane:

- repo [`RULES.md`](../../../../RULES.md) §0, §3, §7 and the problem
  [`RULES.md`](../../RULES.md) in full;
- [`../../README.md`](../../README.md), including its provenance warning;
- the four attack READMEs named in the brief:
  [`../exceptional-set-polygons/`](../exceptional-set-polygons/README.md),
  [`../exceptional-pair-rigidity/`](../exceptional-pair-rigidity/README.md),
  [`../half-density-obstruction/`](../half-density-obstruction/README.md),
  [`../convex-vertex-criterion/`](../convex-vertex-criterion/README.md);
- the signature list of the committed exact decider
  `experiments/inscribed-triangle-polygons/geom.py` (read-only for this lane).

What had **also** already happened, and it matters: the paper-and-pencil part of §3 of the
README (the *ancestor lemma* — that on a radially monotone tree all directions at one radius lie
in an arc of width `< 60°`) and the *design* of the thin-tree counterexample search were worked
out in my head before this file was written. So this file is pre-registration of the **search and
its verdict rule**, not of the algebra. That is the same honest caveat
[`../half-density-obstruction/KILL-CRITERION.md`](../half-density-obstruction/KILL-CRITERION.md)
records for itself, and it is stated here rather than smoothed over.

## The question this lane owns

> Can a simple polygon have **three** exceptional vertices, given that at most two of them can be
> wedge-type?

Equivalently: close `|E(P)| <= 2` for simple polygons, or find precisely why it does not close.

## Pre-registered predictions

Recorded before running anything, so that they can be scored rather than retrofitted.

| # | Prediction | Confidence |
|---|---|---|
| P1 | My independently written exact decider reproduces all four controls (equilateral, 30-30-120, unit square, the 17-gon spiral witness) on the first or second attempt. | high |
| P2 | The *thin-tree* reduction is sound: for a tree `T` with three leaves, all pairwise direction separations at each radius bounded away from `60°`, a thin enough simple polygon around `T` has all three tips exceptional. | medium |
| P3 | The three arc conditions (one per tip) are **not** simultaneously satisfiable for a straight-armed 3-leaf tree ("Y"), and the obstruction will be visible as a numerically robust barrier rather than a near miss. | medium-low — this is the prediction I most expect to be wrong |
| P4 | `|E(P)| <= 2` will **not** be closed by this lane. | high |

## Kill criteria — what stops which activity

**K1 (validation gate).** If my from-scratch decider disagrees with the committed decider on any
control, or with the hand-checked `30`-`30`-`120` answer, **stop and fix the decider**; no search
result computed before the gate passes may be reported. Five checkers have failed in this session
against zero mathematical errors of that kind; the decider is the prime suspect for any anomaly.

**K2 (the extraordinary-claim trip-wire).** If a polygon appears to have **three** exceptional
vertices, that contradicts the provisional Meyerson bound and I must, per repo `RULES.md` §7 and
this problem's `RULES.md`:
1. report it as "this appears to show", never as a result;
2. re-decide it with the committed decider, with my own decider, and **by hand** on at least one
   of the three vertices;
3. name the step I least trust, in this order of prior likelihood: (a) my own error, (b) a
   misreading of the criterion, (c) a wrong provisional citation;
4. not merge, not announce, and flag for both humans.
A three-exceptional polygon that survives only my own code is **not** reportable as anything but
a suspicion.

**K3 (the search is exhausted, not the question).** If the straight-armed Y search finds the three
conditions jointly satisfiable, prediction P3 is dead and the arc/ancestor lemma cannot by itself
close the count: **stop trying to close the count with it** and report that instead.

**K4 (the search is infeasible and I cannot say why).** If the Y search finds no feasible
configuration but I cannot identify a mechanism, the honest output is "search found none,
mechanism unknown". I must **not** upgrade that to a theorem, and must **not** re-scope the lane
to make the numerics look like a proof.

**K5 (proof self-audit).** Any argument I write that would close `|E(P)| <= 2` must be run against
three witnesses before it is written up: the `30`-`30`-`120` triangle (two exceptional points must
survive), the 17-gon spiral witness of `exceptional-set-polygons` §7 (a *non-wedge* exceptional
point must survive), and the pentagon `C2` of `exceptional-pair-rigidity` §7.3 (a mixed pair must
survive). An argument that kills any of those is broken, not a breakthrough.

**K6 (square test, §3.2).** Any argument here must be replayed with `90°` for `60°`. If it
survives verbatim it proves the square peg problem and is therefore wrong. Note honestly that
square peg *is* known for polygons, so a transfer is not automatically an error — but it is an
alarm that must be explained, not waved through.

**K7 (compute budget).** One hour unattended (`RULES.md` §6.6). Checkpoint partial results; kill
my own background jobs; report partial results rather than nothing.

**K8 (no self-granted status).** Nothing in this lane may be labelled above `sketch` or
`numerical`, nothing goes in `results/`, and Meyerson is a consistency check on output only, never
a premise. If I catch myself using "at most two" as an input, the argument is circular and dies.

## What would count as success

In decreasing order of value:

1. A proof that `|E(P)| <= 2` for simple polygons, with the regularity budget stated and every
   re-derived dependency written out (would be `sketch`, awaiting cross-family review).
2. An exact simple polygon with three exceptional vertices, surviving K2 in full.
3. A precise, checkable account of the obstruction: what replaces the metric (diameter) argument
   for non-wedge points, and exactly which joint hypothesis on three exceptional points is not
   available.

Outcome 3 is the expected one, and per repo `RULES.md` §0 a clearly documented failure is a
success and is reported as one.
