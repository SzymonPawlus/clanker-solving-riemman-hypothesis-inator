# 2026-08-23 — n16 tomography certification (worker T2, issue #97)

Lane: I1's shortlist #1, the 6-direction dodecagonal-norm relaxation. T1 was assigned it and
died before writing anything (both its directories were empty); everything here is fresh.

## Order of events (honest sequence)

1. Read I1's round-3 README and `dodeca.py`; re-derived the six projection forms by hand from
   the chart (each expansion checked; they match I1's), the cos15 loss bound, and the sandwich
   `t*a_n <= M6(n) <= a_n` — the sandwich is new here and became the main control device.
2. Paper observation before any code: the unit lattice steps (1,0),(0,1),(1,1),(1,-1) are
   parallel to the six projection directions, so dod = Euclid on them and T_k lattices compress
   by exactly cos15. That answers I1's "check early: is M6(15) < 4?" question by construction
   (M6(15) <= 4*cos15 = 3.8637 < 4) and pins M6(4), M6(5), M6(10), M6(15) to ~1e-5 brackets.
   It also handed me B&C controls whose right answers (sqrt3*cos15, 2*cos15) are NOT in the
   Euclidean table — a pipeline that just reproduces a_4 = sqrt3 fails them, which is the
   control-trap fix the assignment demanded.
3. Wrote `attacks/n16-tomography/KILL-CRITERION.md` with fixed gates and caps BEFORE computing:
   K1 = exact 16-witness below 1+2sqrt3; K2 = n=10 gate 600 s / 300k nodes, n=15 gate,
   extrapolation > 1e9 nodes at n=16; K3 = sandwich/ceiling tripwires as bug detectors.
4. Wrote `experiments/packing-n16-tomography/tomography.py`: exact Q(sqrt3) witness checker,
   rational certification thresholds r_f <= t/w_f (proved exactly; note the true thresholds live
   in Q(sqrt2,sqrt3), so going rational also fixes a small error in I1's "leaves in Q(sqrt3)"
   line), disjunctive branch-and-cut with sort-symmetry rows and an exact rational Farkas
   check at every pruned leaf (box-absorption trick so no exact dual equality is needed).
5. Controls: all passed, including the two-sided B&C brackets at n=4 (3037 nodes) and n=5
   (8821 nodes), hex-cheat rejection, and independent re-verification of I1's 449/100 witness.
6. Gate: n=10 at a = 2.888 (0.34% below the closed-form transition 3t) hit TIME_CAP at
   269,741 nodes, max depth 15/45 pairs. **K2 fired.** Caps not raised; n=16 not attempted.
   Both pre-registered extrapolations (per-n: ~1.1e9; per-pair: ~5e16 nodes at n=16) are at or
   past I1's 1e9 gate; measured 450 certified nodes/s makes 1e9 nodes >= 26 days on 1 core.
7. One post-kill computation on the K1/ceiling side (not a re-scope of K2): my independent
   12-restart search at a = 4485/1000 found a config that passed the exact true-t check —
   **M6(16) <= 4.485**, tightening I1's exact ceiling 4.49. Exactly above the record
   ((4.485-1)^2 = 12.145 > 12), so K1 still does not fire. Ceiling profit now +0.021 max.

## Verdict

Certification strategy (naive disjunctive B&C) dead at this effort; relaxation alive with
M6(16) numerically in (4.48, 4.485], still above 1+2sqrt3. Nothing certified above the record.

## Post-mortem mechanism (sketch)

The dod metric is flat along its own six directions: pairs with |dv| >= 2t/sqrt3 are satisfied
regardless of du, so near-threshold feasible sets contain whole-row translational continua in
three directions. The Farkas tree must carve away volume, not points — that, not the corner
defect that killed P4–P6 (this relaxation keeps the container exactly), is why the tree
explodes. Revival would need to turn the row degeneracy into combinatorics (condition on the
v-multiset pattern and certify patterns by 1-D interval arguments) rather than add nodes.

## Least sure of

The 2-point growth extrapolation (n=4,5 only completed) is quantitatively weak — but the kill
does not rest on it alone: the n=10 gate timeout is a direct measurement. Of the exact
machinery, the step to review hardest is the Farkas box-absorption argument in
`_exact_farkas` (README "delicate" §1).

## Loose ends for the board

- The lattice-compression fact pins M6(n) = cos15 * a_n on lattice-like n; if anyone wants the
  value-vs-k curve (I1's k=12 suggestion), the same fact gives cos(7.5) compression for k=12
  lattices immediately — no search needed for the lattice part.
- Background jobs: none left running (both spawned tasks completed; verified before finishing).
