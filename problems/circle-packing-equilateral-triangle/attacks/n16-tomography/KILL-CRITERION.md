# Kill-criterion — n16 6-direction (dodecagonal-norm) tomography certification

Written **before** any computation in this lane (worker T2, 2026-08-23, issue #97).
Predecessor T1 died before writing anything; this file is fresh, not inherited.

Notation: `t = cos 15°`, `M6(n)` = least `a` admitting `n` points in the closed simplex
`{u,v >= 0, u+v <= a}` with pairwise `dod >= t` (six forms, weights `sqrt3/2` and `1/2`).
Record to beat: `1 + 2*sqrt3 = 4.4641016...` (`sketch`). I1's exact ceiling: `M6(16) <= 449/100`.

## K1 — relaxation dead vs record (inherited from I1's dodeca.py, kept verbatim)

If an **exactly verified** (Q(sqrt3) comparison) 16-point configuration exists with pairwise
`dod >= t` at some `a < 1 + 2*sqrt3` (exact check: `(a-1)^2 < 12` for rational `a`), then
`M6(16) < record` and the lane is dead permanently. Stop, write it up as `refuted`.

## K2 — certification intractable (the node-growth gate, fixed numbers)

Gate instances, all at ~0.35% relative gap below the (a priori or numerically bracketed)
transition, branch-and-cut with sort-symmetry rows:

- n=10 at rational a = 2.888  (transition = 3t = 2.89778, known a priori — see README)
- n=15 at rational a = 3.850  (transition = 4t = 3.86370, known a priori)
- n=16 at rational a = 447/100 (target; numeric transition ~4.483 per I1, not assumable)

Kill if ANY of:
- the n=10 gate run does not certify (exact Farkas at every leaf) within **600 s or 300,000
  nodes**, whichever first;
- the n=15 gate run does not certify within **900 s or 300,000 nodes**;
- log-linear extrapolation of certified node counts over n in {4, 5, 10, 15} predicts
  **> 10^9 nodes at n = 16** (I1's gate, kept);
- the n=16 run at a = 447/100 exceeds **1,200 s or 10^6 nodes** without completing.

On kill: record every measured node count and the deepest completed run, mark the lane
`refuted` for *this certification strategy* (the relaxation itself stays alive unless K1 fired),
stop. Do not re-scope mid-run; do not raise the caps after seeing partial numbers.

## K3 — self-consistency tripwires (bug detectors, fail loudly, not silently)

- Any certified lower bound `M6(n) > a` with `a > a_n` for a known `a_n` (n in 4,5,10,12,15),
  or any exact witness with `a < t*a_n`: **bug**, stop the lane, report the discrepancy.
- Any certified `M6(16) > 449/100`: contradicts I1's exact witness; **bug**, stop.
- Any certified value at or above `4.62`: possible extraordinary-claim territory AND above the
  ceiling — treat as a bug first, flag per repo RULES.md §7, do not announce.

## Controls that must pass before n=16 is attempted (two-sided, non-vacuous)

1. Exact witness M6(4) <= (rational just above sqrt3*t = 1.67303) AND branch-and-cut refuses to
   certify at a = 1.674 (witness exists there) AND certifies at a = 1.67 (< sqrt3*t).
   The target value sqrt3*cos15 is NOT in the Euclidean table — a pipeline that merely
   reproduces a_4 = sqrt3 FAILS this control.
2. Same two-sided control at n=5 around 2t = 1.93185.
3. Reverify I1's `M6(16) <= 449/100` witness with an independently written exact checker.
4. Hex-cheat rejection: the M3(4) <= 3/2 corner-cheat config must fail the dod exact check.

Success criterion (what "certified" means): exact rational Farkas certificate at every pruned
leaf, rational thresholds r_f <= t/w_f verified exactly in Q(sqrt3), rational a* with
(a*-1)^2 > 12, all controls green. Anything less is `numerical`.

Budget: 45 min wall clock, 1 core, checkpoints to `experiments/packing-n16-tomography/out/`.
