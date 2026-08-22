# Attack: occupancy exhaustion — covering with slack — for $n = 16$

**Claim type: OPTIMALITY / LOWER BOUND** (problem [`../../RULES.md`](../../RULES.md) §1), i.e.
$a_{16} \ge a$ in the separation-1 normalisation of [`../n16-covering-2/`](../n16-covering-2/).
Nothing here enters `results/`, and — kill-criterion outcome up front — **K1 fired: no
$a > 1+2\sqrt3$ was certified.** The record of [`../n16-covering-2/`](../n16-covering-2/) stands.
What this round delivers is a validated occupancy engine, four two-sided controls, and a
measured, quantified account of *why* the slack route stalls: the pattern count and the
per-pattern refutation cost pull in opposite directions, and at $a = 4.47$ their product is
$\sim 10^5$ seconds against a 900 s probe.

- Author: `claude`, worker **O2**, 2026-08-22, branch `claude/circle-packing-subagents-9yg5gt`,
  issue #97
- Kill-criteria, fixed before computing: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code: [`experiments/packing-n16-occupancy/`](../../../../experiments/packing-n16-occupancy/)
  — Python stdlib only for every decision; no seeds, no network
- Journal: [`notebook/claude/2026-08-22-n16-occupancy.md`](../../../../notebook/claude/2026-08-22-n16-occupancy.md)

## Status of every assertion here

| assertion | status |
|---|---|
| engine controls at $n = 4, 6, 7, 10$ pass in both directions (table below) | `numerical` (deterministic runs, reproducible one command) |
| $a_{16} \ge 43/10$ via a 15-piece cover found by the merge pass | `sketch` (mine; weaker than the standing $1+2\sqrt3$ anyway) |
| at $a = 447/100$: $N = 21$ cover verified, all $\binom{21}{16} = 20349$ patterns survive pair pruning, probe refuted only a handful in 900 s | `numerical` |
| "pair pruning alone can never beat the 15-piece family" | `sketch` — see the precise statement below; it is *not* a theorem about all covers |
| "the corner-capacity variant hits the same $1+2\sqrt3$ wall" | `sketch` — boundary-counting argument, unreviewed |
| cited $a_k$ values used in the capacity ladder ($k \le 15$) | `cited` (problem README); $a_{13}$ deliberately **omitted** rather than trusted from truncated decimals |

Nothing above is assumable, including by me (`RULES.md` §3).

## The mechanism

Cover $T_a$ by $N \ge 16$ convex pieces of diameter **strictly** $< 1$ (exact rational
comparison — separation is non-strict, so diameter exactly 1 destroys the pigeonhole). Any 16
points at pairwise distance $\ge 1$ then occupy 16 *distinct* pieces. Enumerate the
$\binom{N}{16}$ occupancy patterns and refute each:

1. **pair pruning** — two occupied pieces with exact max mutual distance $< 1$ (a max over
   vertex pairs, exact, since squared distance is convex on a product of polytopes);
2. **capacity pruning** — $k$ occupied cells all inside a lattice-aligned equilateral triangle
   (either orientation) of side $s < a_k$: then $k$ points at pairwise distance $\ge 1$ would
   sit in $T_s$ with $s < a_k$, contradicting the cited minimality of $a_k$. Subsets are
   generated heuristically (six sorted-prefix families) in floats; every firing is confirmed
   exactly before it may prune;
3. **recursive refinement** — split an occupied cell into two closed halves that cover it
   (exact clip at a rational cut), branch on which half holds the point, re-prune.

All patterns refuted $\Rightarrow$ $a_{16} \ge a$.

**Circularity guard, as a named constant.** `CAP_MAX_INDEX_FOR(n) = n - 1` in `occ.py`;
`run_occupancy` asserts it. A run at $n = 16$ may use only $a_k$, $k \le 15$; controls at
$n = m$ only $k \le m-1$. No value of $a_{16}/d(16)/s(16)$ and no property of any 16-point
packing is an input anywhere; $4.6247636$ appears once, as a *refusal threshold* (`run16.py`
refuses to run at $a \ge 4.62$, K3).

**What is delicate.**

- *Strictness*: the cover verifier requires squared diameter $< 1$ exactly; the pair prune
  requires maxdist $< 1$ exactly (points at distance exactly 1 are admissible).
- *Float discipline*: floats pre-filter which prunes to attempt and choose which cell to
  split; they can lose pruning power, never soundness. Every reported refutation is a chain
  of exact `Fraction` (or exact-vs-$p+q\sqrt{m}$) comparisons.
- *Cover verification* is by residual subtraction from first principles (repeatedly clip the
  residual regions by the piece halfplanes and keep the outside parts): no area identity, no
  disjointness assumption, overlapping pieces fine. The one bug found in this round —
  `edges_of` produced exterior halfplanes — was caught by the negative smoke test "deleting a
  piece must break the cover", which is exactly the test a reviewer should re-run first.

## Controls (K0) — all passed, both directions

Engine must certify just below a known $a_n$ and must FAIL just above it, where an explicit
packing exists. Capacity table capped at $n-1$ throughout (guard above).

| control | cover | certify at | outcome | must fail at | outcome |
|---|---|---|---|---|---|
| $n=4$ ($a_4 = \sqrt3 \approx 1.732$) | quadrisection, $N=4$ | $1.65$ | refuted, 110 nodes, depth 22 | $1.75$ | survivor $\approx$ corners $+$ centroid |
| $n=6$ ($a_6 = 2$) | 16 subcells | $1.90$ | 0 cliques survive pairs | $2.05$ | 27/422 patterns survive |
| $n=7$ ($a_7 = 1+\sqrt3 \approx 2.732$) | hex cover, $N=9$ | $2.60$ | **all 36 patterns refuted**, $\le 13547$ nodes each, 58 s | $2.80$ | 4 explicit survivors |
| $n=10$ ($a_{10} = 3$) | hex $N=9$ / fine hex $N=15$ | $2.85$ | trivial ($N=9<10$) / all 3003 patterns refuted (root capacity via $a_9$), 2.5 s | $3.05$ | budget, not certified |

The $n = 7$ control is the load-bearing one: $a \in (a_6, a_7)$ means the root capacity test
*cannot* fire (as at $n=16$ for $a > 4 = a_{14}$… for subsets; globally for $a \ge 4$), so
certification required genuine per-pattern refinement — and the must-fail direction produced
explicit survivor witnesses that look like the true 7-point packing (three corners covered,
near-lattice interior). The $n=4$ must-fail witness is the corners-plus-centroid packing to
three decimals.

## The n = 16 runs

**$a = 43/10 = 4.30$ (calibration, below the record).** The greedy exact merge pass reduced
the clipped-hexagon cover to **15 pieces** on its own, so certification is the trivial
15-piece pigeonhole — consistent with the covering family's $A_{15} \ge 1+2\sqrt3$, and a nice
incidental check that the merge machinery agrees with the covering lane, but it exercises no
occupancy machinery.

**$a = 447/100 = 4.47$ (the probe, above the record $1+2\sqrt3 = 4.46410\ldots$).**

- best cover found: $N = 21$ pieces ($t = 6/7$ hexagon lattice, offset $43/700$, merged),
  max piece diam$^2 = 48/49 < 1$, cover verified exactly;
- **all $\binom{21}{16} = 20349$ patterns survive pair pruning** — no 16-subset contains an
  incompatible pair;
- the probe refuted patterns one at a time by refinement + capacity at $\sim 30$–$60$ s per
  pattern (see `out/n16-a447_100.json` for the exact counts of its 900 s), projecting to
  $\sim 10^5$–$10^6$ s for the full exhaustion at this $N$ — two to three orders of magnitude
  over any honest single-session budget. **K1/K2 fired; the run was stopped at its cap.**

## Why the slack route stalls — the two findings worth keeping

**1. Pair pruning cannot be the engine of a record (sketch).** If a pattern dies by a pair
$(P, Q)$ with $\max_{p \in P, q \in Q}|p-q| < 1$, then since both have diameter $< 1$ every
two points of $P \cup Q$ are within $< 1$, so $\mathrm{hull}(P \cup Q)$ is a single convex
piece of diameter $< 1$ — a *merge*. More generally a clique of the incompatibility graph
merges into one piece. So a cover whose patterns all die by pairs is, up to these merges,
within one step of a $\le 15$-piece cover, the family already pinned at $1+2\sqrt3$. (This is
a structural heuristic, not a theorem quantified over all covers: no-16-clique in the
compatibility graph does not formally imply clique-cover number $\le 15$. The observed run is
consistent with it in the sharpest way: at $a = 4.47$, *zero* of the 20349 patterns died by
pairs.) All genuinely new refutation power must come from capacity subsets and refinement —
which is where the cost lives.

**2. The corner-capacity variant hits the same wall (sketch, boundary counting).** The
tempting shortcut — replace pieces near a corner by one capacity-3 region (a corner triangle
of side $c < \sqrt3 = a_4$, holding $\le 3$ points) — cannot pass $1+2\sqrt3$ either: a
cap-3 corner triangle covers $\le \sqrt3$ along each of its two sides, which is *exactly*
what the 15-cover's corner-quad-plus-edge-pentagon chain covers with the same 3 points
(both are the unit triangular lattice in disguise: $a_4 = \sqrt3$ *is* the lattice constant).
And for $a > 1+2\sqrt3$ each side's uncovered middle, of length $a - 2c > a - 2\sqrt3 > 1$,
needs two diameter-$<1$ pieces instead of one, spending the saving. Mid-side capacity regions
are strictly worse per point than diameter-$<1$ pieces ($a_{k}/\!(k\!-\!1) < 1$ of side
coverage per point for every usable $k$). Unreviewed; a reviewer should attack the implicit
claim that side coverage is the binding resource.

**3. The measured cost structure (numerical).** Pattern count and per-pattern cost trade off
through $N$: at $N = 21$, $\binom{N}{16} = 20349$ patterns at $\sim 10^{1.5}$ s each; pushing
$N$ down to 17 ($\binom{17}{16} = 17$ patterns) needs a near-optimal 16–17-piece cover of
$T_{4.47}$ (the merge pass from a hexagon lattice does not find one), and each pattern then
starts from fatter cells, i.e. deeper refinement. The BnB resolution heuristic (re-derived
from [`../../../../experiments/circle-packing-bnb/`](../../../../experiments/circle-packing-bnb/README.md))
says closing at $a$ must refute phantom near-packings at pairwise $\ge 1 - \delta$ with
$\delta \approx 1 - a/a_{16} \le 0.033$ at $a = 4.47$ — cells of diameter $\sim \delta$, 5+
levels on each of 16 cells, regardless of how the patterns are grouped. The occupancy
framing removes the bnb's choose-16-cells-of-$4^L$ explosion (my patterns are $\le 10^{4.3}$,
not $10^{14}$) but pays it back in per-pattern depth. **That is the wall, quantified.**

## What to review hardest

1. **The cover verifier** (`occ.verify_cover`): if it passed an uncovered $T_a$, everything
   downstream is vacuous. Re-run `python3 -c` smoke: delete any piece, verification must
   fail. The `edges_of` orientation bug caught in development lived exactly here.
2. **`capacity_refute` / `_cap_confirm`**: the exact re-confirmation must recompute the
   enclosure from the `Fraction` vertices (it does) and compare against $p + q\sqrt m$
   exactly (`lt_radical`); check the ladder indices against the problem README table, and
   that `cap_max_index` really is $n-1$ in every call.
3. **`split_cell`**: children must be closed and cover the parent (clip at the same rational
   `mid` with opposite inequalities). A cut that dropped a sliver would over-prune — the
   false-certification failure mode. The two-sided controls are the evidence it does not.
4. The two sketches above, which are arguments, not computations.

## Reproduce

```bash
cd experiments/packing-n16-occupancy
python3 controls.py            # all four two-sided controls, ~8 min
python3 run16.py 43 10 300     # calibration: merge finds a 15-piece cover, trivial certify
python3 run16.py 447 100 900   # the probe at a = 4.47: builds + verifies N=21 cover,
                               # enumerates 20349 patterns, refutes until the 900 s cap,
                               # checkpoints to out/n16-a447_100.json
```

Deterministic (no randomness anywhere); stdlib-only decisions; floats only as pre-filters and
heuristics. CPython 3.x, single core, exact runtimes vary with load only.

## Where a successor should start

- A **purpose-built 16–17-piece cover** (SLP minimax over a fixed combinatorial structure, as
  `packing-n16-covering-2/slp.py` did for 15) collapses the pattern count to $\le 17$; the
  entire budget then goes into a handful of deep refinements. That is the only shape of this
  lane with a chance, and it is also where finding 2 (corners) and the resolution heuristic
  say the depth will concentrate.
- Capacity subsets currently come from six sorted-prefix families; the corners of $T_a$ are
  where they fire. A smarter subset generator (connected clusters of cells) is cheap power.
- If $a_{16}$ is in truth close to $1+2\sqrt3$, *no* variant of this lane can certify past it
  cheaply — the cost divergence as $a \uparrow a_{16}$ is structural. The lane cannot tell
  you which world you are in; only an upper-bound improvement (a better packing) or a
  different lower-bound method can.
