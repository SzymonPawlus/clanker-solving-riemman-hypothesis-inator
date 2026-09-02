# n16 verification round 6 — adversarial audit (worker V6, agent `claude`, issue #97)

**Role:** convergent / verification. Nothing new is proposed here.

**Status ceiling, stated up front.** I am Claude. So is the manager whose work items 1–2 audit,
and so is V4, whose pass over item 3 I am duplicating. Repo `RULES.md` §5 wants a *different model
family* for independent confirmation. **I cannot grant `verified:review` to anything below, and
nothing below should be recorded as having received it.** Two Claude passes that agree are two
draws from a correlated distribution; the value of this document is the places where I *disagree*,
not the places where I nod.

Everything decided here is exact: `fractions.Fraction` throughout, integer/rational comparisons
only. No numpy, no scipy, no floats anywhere on a decision path (floats appear only in printed
decimal renderings of exactly-computed quantities).

---

## Item 1 — the manager's independent fractional checker (`experiments/packing-n16-fracverify/`)

```
checked:      (a) I reimplemented the whole of Lemma F certificate checking from scratch, with a
                  DIFFERENT algorithm for the load-bearing check (D), in
                  `experiments/packing-n16-verify-6/v6check.py`.  fracverify discharges (D) by
                  carrying (region, accumulated weight) pairs and splitting regions against
                  pieces; v6check instead builds the ARRANGEMENT of all supporting lines of all
                  piece edges plus the three lines of T_N, and evaluates the total incident weight
                  just inside every sector at every arrangement vertex, using a symbolic
                  infinitesimal (p + eps*d is in {a.x >= c} iff a.p-c > 0, or a.p-c == 0 and
                  a.d >= 0).  No sampling, no area identity, no shared code.
              (b) All three control certificates independently confirmed VALID, with the same
                  bounds: a_4 >= 108/sqrt(15841/4) = 1.716178489196, a_6 >= 126/sqrt(3969) = 2,
                  a_10 >= 189/sqrt(3969) = 3.  v6check additionally reports the exact minimum
                  incident weight over T_N: in all three it is exactly K (= 1), i.e. the coverings
                  are pointwise tight, not slack.
              (c) The exhaustiveness of fracverify's region-splitting argument -- see the two
                  proofs recorded in "Why check (D) is sound" below.  Both the early drop
                  (`acc >= K`) and the descending-weight processing order are safe, and the
                  zero-area slivers that `clip()` discards cannot hide a covering failure.
              (d) split() partitions its input: the decomposition
                  R = (R n H_1 n ... n H_m) u U_j (R n H_1 n...n H_{j-1} n H_j^c) is exact, both
                  halfplanes are kept CLOSED so the parts overlap on measure-zero sets rather than
                  losing them, and overlap is the safe direction (a doubly-listed point must clear
                  the weight bar twice).  The `if not cur: break` early exit is also safe.
              (e) The rational-vertex fix.  For `kind: "poly"` it is correct: F("107/2") is exact
                  and the polygon is used as the intersection of its edge halfplanes.  For
                  `kind: "box"` it is NOT correct -- see correction C1.  It is non-crashing rather
                  than right, exactly as the brief suspected, though on a different axis
                  (bound sign, not rational parsing).
              (f) 21 corruptions, 16 of them not in the manager's selftest.py (table below), each
                  run through both checkers.
              (g) 171,299 random integer polygons probed for the one soundness hole I could see in
                  fracverify -- a piece spec whose halfplane intersection escapes the convex hull
                  of its own vertices, which would make `sqdiam` (a max over vertices) an
                  under-estimate of the diameter of the region actually credited.  Zero escapes.
not-checked:  - The 171k-polygon probe in (g) is empirical, not a proof.  I did not prove that
                intersect(edge halfplanes) is contained in hull(vertices) for an arbitrary vertex
                list.  fracverify does not test convexity, so this is the residual soundness
                assumption in its decoder.
              - I did not audit fracverify's printing/reporting path, only its verdict path.
              - I did not re-derive Lemma F itself from scratch beyond the paragraph in "The
                lemma" below; I checked that both checkers implement the same lemma correctly.
verdict:      confirmed-with-correction
```

### The lemma, restated so the checks can be matched to it

Pieces `S_i` closed, weights `w_i >= 0`. If (i) `diam S_i < s` for all `i`, (ii)
`sum_{i : x in S_i} w_i >= 1` for **every** `x in T_N`, and (iii) `sum_i w_i < n`, then `T_N`
contains no `n` points at pairwise distance `>= s`. (Each `S_i` holds at most one such point, so
summing (ii) over the `n` points gives `n <= sum_i w_i`, contradicting (iii).) Rescaling by `s`:
`a_n >= N/s` for every `s > max_i diam S_i`, hence `a_n >= N/sqrt(Qmax)`. **The bound is
scale-free** — it is the ratio (side)/(max diameter) in whatever units the chart uses. Both
checkers report exactly this and both are right.

Consequence worth recording: `UNIT` (the `unit` field) is **not load-bearing for the bound**. It
enters only check (B), which is a sanity check that pieces are smaller than the separation.
fracverify demands `Qmax <= (UNIT-1)^2`; v6check demands the mathematically tight
`Qmax < UNIT^2`. fracverify's is strictly stronger, i.e. conservative — it can only false-reject.
This is the whole explanation of disagreement row A15 below.

### Why check (D) is sound (the part the brief asked me to break)

Two facts, both of which I reconstructed rather than took from the code comments.

**(1) A covering failure always has positive area.** `W(x) = sum_i w_i * 1_{S_i}(x)` is a
non-negative combination of indicators of **closed** sets, hence upper semi-continuous, hence
`{W < K}` is *open*. A non-empty open subset of `T_N` has positive area (`T_N` is the closure of
its interior). So a covering failure can never be confined to a segment or a point. This is what
makes the sliver worry vacuous — and note it depends on the pieces being closed, which they are.

**(2) `clip()` only ever discards zero-area sets, and every discarded point survives inside a
region that *is* kept.** `clip` returns `[]` when the result has `< 3` distinct vertices or zero
area. Let `R` have positive area and `H` be a closed halfplane. If `R n H` has zero area then
`R n H` is contained in the boundary line of `H` (a convex set of positive area would otherwise
have interior points strictly inside `H`, by `R = closure(int R)`), and that line lies in the
*complementary* closed halfplane too — so those points are inside the `outside` part, which is
retained. Symmetrically for the outside parts, and the same argument covers the
`if not cur: break` exit.

Together: the carried region list always covers `T_N` up to a zero-area set at every step, the
dropped regions genuinely have `acc >= K`, and an empty final list therefore certifies
`W >= K` on all of `T_N` minus a zero-area set — which by (1) is all of `T_N`. **Check (D) is
exhaustive.** The descending-weight sort is a pure speed heuristic with no effect on the verdict
(I confirmed this by construction of the invariant, and empirically: v6check, which has no such
order, agrees on all three certificates).

### Corruption table

`expect` is what a correct checker should do. `fracverify` = the manager's; `v6check` = mine.
Rows A1–A21 are mine; the manager's `selftest.py` covered only stretched-diameter,
outside-`T_N`, deleted-piece, halved-weight and inflated-budget.

| # | corruption | expect | fracverify | v6check | note |
|---|---|---|---|---|---|
| — | BASELINE n4 / n6 / n10 | accept | accept | accept | |
| A1 | reflex vertex inserted (piece made non-convex) | reject | reject | reject (refuses non-convex spec) | fracverify rejects for an *incidental* reason (coverage), it does not detect non-convexity |
| A2 | vertices reordered into a self-intersecting loop | reject | reject | reject (refuses) | same |
| A3 | convex piece listed **clockwise** | accept | accept | accept | benign, both handle |
| A4 | extra collinear vertex on an edge | accept | accept | accept | benign, both handle |
| A5 | one piece translated by 1/1000 | reject | reject | reject | |
| A6 | one vertex pulled inward by 1/1000 | reject | reject | reject | |
| A7 | box upper s-bound set to 0 | reject | reject | reject | fracverify rejects via (B) after silently *dropping* the constraint — see C1 |
| A8 | box lower s-bound set to −5 | accept | **reject** | accept | **C1**: sign flip in the box decoder |
| A9 | coordinates written as decimal strings | reject | **accept** | reject | **C2**: `RULES.md` §2 bans decimal strings |
| A10 | coordinates written as bare JSON floats | reject | **accept** | reject | **C2** |
| A11 | one negative weight, compensated in the total | reject | reject | reject | |
| A12 | `N_units` 108 → 109 (uncovered strip) | reject | reject | reject | |
| A13 | `K` doubled, weights unchanged | reject | reject | reject | |
| A14 | `unit` 1/64 → 1/1000 (diameter cap made vacuous) | accept | accept | accept | correct: `UNIT` does not enter the bound |
| A15 | `unit` 1/64 → 1/63 | — | reject | accept | not a bug: fracverify's cap is conservative, mine is tight |
| A16 | weight on a piece with no spec | reject | **crash (KeyError)** | reject | **C3**: crash, not a clean reject |
| A17 | two n10 weights swapped (65536 ↔ 65537) | accept | accept | accept | my test was worthless — the two weights differ by 1/65536 |
| A18 | `budget_points` 4 → 3 (total weight no longer under budget) | reject | reject | reject | |
| A19 | 30000/65536 of weight moved between two pieces | reject | reject | reject | the real version of A17 |
| A20 | one n10 weight reduced by **1/65536** | reject | reject | reject | the coverings are pointwise tight; both catch the minimal perturbation |
| A21 | one n4 weight reduced by 1/65536 | reject | reject | reject | |

**fracverify failed to reject nothing that threatens a bound.** A9/A10 are a `RULES.md` §2
compliance gap, A16 is robustness, A8/A7 are a decoder divergence (C1). None of them changes the
verdict on the three control certificates.

---

## Item 2 — "F2's piece family is inadequate by ~2.7 pieces"

```
checked:      - Scale-freeness of the certificate bound.  Confirmed: the bound is
                N/sqrt(Qmax), a ratio of two lengths in the same chart, invariant under dilation.
                The manager is right about this and it is the load-bearing half of the argument.
              - The arithmetic 281/63 < 1+2*sqrt3, exactly: 281/63 - 1 = 218/63 < 2*sqrt3
                <=> 109/63 < sqrt3 <=> 109^2 = 11881 < 3*63^2 = 11907.  TRUE.  And 282/63 >
                1+2*sqrt3 since 110^2 = 12100 > 11907.  So N = 281 is exactly the last N below
                the standing record, as the lane's KILL-CRITERION already says.
              - The LP's objective and constraint signs, read off `certify()`:
                `linprog(c=1, A_ub=-M, b_ub=-1, bounds=(0,None))` is min sum(w) s.t. Mw >= 1,
                w >= 0.  Correctly signed.  **The manager's alternative "budget/covering
                constraints are mis-signed" is ruled out.**
              - q_max: `WMAX = 63`, `QMAX_ALLOWED = 63^2 = 3969`; every piece is filtered at
                generation *and* re-asserted at certification.  Matches what the bound formula
                assumes.  **That alternative is ruled out too.**
              - What the LP's rows actually are.  THIS is where the manager's argument breaks —
                see correction C4.
not-checked:  - I did not re-run the LP (scipy, and it is the author's code; also outside my
                one-core/45-minute budget).  The values 17.6724 at N=281 and 17.7525 at N=282 are
                taken from `certs/results.jsonl` on trust.
              - I did not verify from the literature that A_15 = 1+2*sqrt3 is the covering
                threshold, i.e. that a 15-piece cover of T_a by diameter-<1 sets exists for
                a < 1+2*sqrt3.  I checked only that IF it does, the dilation to grid units is
                sound (a cover at ratio r gives a cover of T_N by pieces of diameter N/r, and
                281/63 < 1+2*sqrt3 means diameter < 63 units).  The literature step is
                `not-checked` and it is load-bearing for the manager's comparison.
verdict:      confirmed-with-correction  (the conclusion survives; the stated reasoning does not)
```

### Correction C4 — the LP is not the continuum relaxation restricted to a family

The manager's chain is: continuum LP at ratio 4.4603 is `<= 15`; F2's LP returns 17.6724;
therefore the piece family costs ~2.7 pieces. That skips two further restrictions, both of which
inflate the LP value and neither of which is the piece family:

1. **Cell-containment, not point coverage.** In `membership_matrix`, a piece contributes to a row
   only if it contains the **entire** cell (`Box.contains_mask` compares the cell's u/v/s
   *windows*; `Poly.contains_mask` tests all three cell vertices). A point covered by two
   different pieces on two halves of one cell counts for neither. The LP is therefore the
   continuum LP over the **erosions** of the pieces, not over the pieces. To have an eroded
   family still cover, the underlying continuum pieces must have diameter `<= 63 - diam(cell)`,
   so the reachable N is `62 * (1+2*sqrt3) = 276.77`, i.e. **N <= 276, not 281**. F2's own README
   flags this ("the price of cell granularity … erosion of up to 1 unit") and estimates it at
   1–2 units of N; the estimate is from the controls, where the optimal covers are *lattice
   aligned* (a_6 = 2 and a_10 = 3 cost zero units; a_4 = sqrt3 cost one). The 1+2*sqrt3 cover is
   not lattice-aligned in a 1/64 grid, so the control measurement does not transfer.
2. **Coarse LP rows.** `sweep16` calls `certify(..., r_bulk=3, fine_band=8, corner_rad=75)`, so in
   the bulk the rows are *size-3* lattice triangles, and a piece counts on such a row only if it
   contains all of it. That is erosion by 3 units, not 1, over most of the area. (This is sound —
   it only strengthens constraints, and the final exact check is redone on unit cells — but it
   makes 17.6724 an over-estimate on a third count.)

So the honest statement is **"the family *and/or* the 1/64 grid granularity is inadequate"**, and
17.6724 − 15 = 2.67 is an **upper bound** on the family's deficiency, not a measurement of it.

### Why I nevertheless think the conclusion holds

Not from the N=281→282 slope. The manager (and I, initially) would read the slope 17.7525 −
17.6724 = 0.080 per unit of N as licensing "you would need N ≈ 248 to reach 15". **That
extrapolation is invalid** and the controls prove it: the LP value falls off a cliff at the
threshold — n=4 goes 4.000 (N=109) → 3.000 (N=108); n=6 goes 6.000 (N=127) → **4.000** (N=126), a
drop of two in one unit; n=10 goes 10.000 (N=190) → 9.000 (N=189). Anyone reasoning from the
local slope at N=281 is reasoning about a function that is known to be locally flat and globally
step-like. I flag this because it is the exact shape of the "plateau explanation that was a
coincidence" already in `FINDINGS.md`.

What does support the conclusion is the family's *resolution*: `gen_family` places bulk boxes on
a `step_bulk = 4` lattice and edge/sector pieces on a `step_edge = 6` lattice, with sector shapes
drawn from a fixed list. The family is a coarse sample of translates, not a shape-complete family.
That makes "a richer family would do better" a live hypothesis, not the dismissible one the
KILL-CRITERION's "no re-scoping" clause treats it as. **The lane's negative result stands — the
sweep did not beat 1+2*sqrt3 — but it should be written up as "this implementation at this
resolution", not as "the fractional relaxation".**

---

## Item 3 — Theorem N's class structure (`attacks/n16-structure/` §2 and §3.1)

```
checked:      Re-derived independently, on paper, without using the file's own algebra:
              - Lemma 1 (reach): q in S n e, x in S => dist(x,e) <= |xq| <= diam S < 1.  OK.
              - Lemma 2 (no three-side piece): Viviani gives sum of the three distances from p_1
                to the sides = a*sqrt3/2; those distances are 0, <= |p_1 p_2| < 1, <= |p_1 p_3| <
                1, so a*sqrt3/2 < 2 and a < 4/sqrt3 = 2.3094.  OK.
              - Lemma 3 (corner reach): 60 degrees at the apex, |p q|^2 = alpha^2 + beta^2 -
                2*alpha*beta*cos60 = alpha^2 + beta^2 - alpha*beta >= (3/4)alpha^2 (minimum at
                beta = alpha/2), and |p q| < 1, so alpha < 2/sqrt3 = 1.1547.  OK, and the "for
                every point of the trace" extension is right because the pair was arbitrary.
              - Lemma 4 (deep triangle): each side moving in by 1 shortens the side by
                2/tan(30) = 2*sqrt3, so delta = a - 2*sqrt3; and x in S n D with q in S n e gives
                1 <= dist(x,e) <= |xq| < 1, contradiction.  OK.
              - c >= 3: each apex is covered; its piece meets the two sides through it; the three
                apexes are pairwise a > 1 apart so the pieces are distinct.  OK.
              - b >= 3(floor(a - 4/sqrt3) + 1): M_e is the closed middle segment of length
                L = a - 4/sqrt3, disjoint from the *open* end intervals of length 2/sqrt3 that
                Lemma 3 confines two-side traces to (Lemma 3 is strict, so the open/closed
                bookkeeping is right); no-side and other-side pieces miss e; three-side pieces do
                not exist.  k traces cover M_e, each inside a closed interval of length < 1, so
                sum of lengths >= L and sum < k, giving k > L and hence k >= floor(L) + 1 whether
                or not L is an integer.  The "floor + 1, not ceiling" remark is correct and is
                the step most people get wrong.  At a = 1+2*sqrt3, L = 2.1547, so b >= 9.  OK.
              - d >= 3 when delta >= 1: D's apexes are pairwise delta >= 1 > diam apart, and by
                Lemma 4 their pieces meet no side.  OK.  (The delta >= sqrt3 / d >= 4 branch also
                checks: apex-to-centroid is delta/sqrt3 >= 1.)
              - Disjointness: the classes are "meets exactly 2 / exactly 1 / exactly 0 sides" and
                "meets 3" is empty for a > 4/sqrt3, so c + b + d is the total, not a lower bound
                on a subset.  This is the step the corollary lives on and it is clean.
              - Corollary (exactly 3/9/3): 3 + 9 + 3 = 15 forces equality in each.  Then the three
                two-side pieces must be the three apex pieces (each apex needs one and they are
                distinct), so each side is met by exactly 2 of them; b = 9 with >= 3 per side
                forces exactly 3 per side; 2 + 3 = 5 per side.  D is met only by no-side pieces,
                of which there are 3.  All correct.  For a >= 5.309 the hypothesis is
                unsatisfiable (b >= 12 pushes the total past 15) and the corollary is vacuously
                true, which is fine.
not-checked:  Nothing in §2 or §3.1.  I did not audit §5.1's use of it, nor §4, §6.
verdict:      confirmed
```

**What this confirmation is worth.** V4 confirmed the same statements and V4 is Claude; I am
Claude. Both of us re-derived the same short synthetic-geometry argument and got the same answer.
That is worth more than one pass and much less than two model families. Theorem N §3.1 should
remain `sketch` until a non-Claude reviewer sees it, and worker B2's published-number claim
built on it inherits that cap (`RULES.md`: a claim is capped at the weakest status it depends on).
If one thing here goes to a different family, it should be **Lemma 3 plus the b-bound**, because
that is where the floor/ceiling and open/closed conventions do real work and where a plausible
off-by-one would silently change 9 into 6 and the corollary into nothing.

---

## Item 4 — work landed by the four live workers

```
checked:      Directory sweep at the end of my window.  `attacks/n16-tomography/` and
              `attacks/n16-budget/` contain KILL-CRITERION.md only; `attacks/n16-fractional/`
              is the lane audited in items 1-2; `attacks/n16-mixed-capacity/` does not exist.
              `experiments/packing-n16-budget/` and `.../packing-n16-tomography/` hold
              in-progress code and empty-or-partial `out/` directories.  No new certificate and
              no new claim had landed.
not-checked:  Anything those workers land after my window closes.  Nothing here should be read
              as clearing it.
verdict:      could-not-follow (nothing to check yet)
```

---

## Corrections

**C1 — `fracverify.piece_polygon`, `box` branch: the `u+v` bounds are mis-decoded when they are
zero or negative.** The two `u+v` constraints are encoded as clips against the *point pairs*
`((wlo,0),(0,wlo))` and `((whi,0),(0,whi))`. `cross` of such a pair with a test point carries a
factor of `wlo` (resp. `whi`), so the inequality **flips sign when the bound is negative** and the
constraint is **silently dropped when the bound is zero** (the two points coincide and `cross` is
identically 0). Verified against the documented semantics on a rational grid:

| `bounds` | fracverify decodes | verdict |
|---|---|---|
| `[0,4,0,4,0,4]` | 3-gon | OK |
| `[0,4,0,4,-3,4]` | **empty** | loses the whole piece |
| `[0,4,0,4,2,0]` | 5-gon | **gains 253 spurious grid points** (constraint dropped) |
| `[0,4,0,4,3,6]` | 6-gon | OK |
| `[-2,2,-2,2,-1,1]` | 3-gon | loses points **and** gains 78 spurious ones |

*Impact on the three control certificates: none.* Their box pieces are
`[0,63,0,63,0,63]`, `[0,63,63,126,63,126]`, `[63,126,0,63,63,126]`, `[0,63,126,189,126,189]`,
`[0,63,63,126,126,189]`, `[0,63,63,126,63,126]` — all `u+v` bounds `>= 0`, and the single
`wlo = 0` case is harmless because `ulo = vlo = 0` already implies `u+v >= 0`. So the item-1
verdicts stand. But `gen_family` *does* generate boxes with `L3 = L1+L2+k` and `L1, L2` down to
`-63`, so a future certificate can hit this. Fix: clip against the explicit halfplanes
`(1,1,wlo)` and `(-1,-1,-whi)`, the way the author's own `Box.verts()` already does. This is also
a `RULES.md` §3.4 checker disagreement (row A8) and should be resolved, not averaged.

**C2 — `fracverify` accepts decimal strings and bare JSON floats in exact fields.**
`F("53.5")` and `F(0.1)` both parse silently. Problem `RULES.md` §2 bans both precisely because
they are truncated optimiser output masquerading as exact values; `F(0.1)` silently becomes
`3602879701896397/36028797018963968`, a *different* piece from the one intended. Rows A9/A10.
Fix: reject any coordinate string containing `.` or `e`, and any JSON float.

**C3 — a weight naming a piece with no spec crashes with `KeyError` instead of rejecting.**
Row A16. Cosmetic (a crash is a rejection), but a checker should say what is wrong.

**C4 — the item-2 attribution.** See above: the LP carries two restrictions beyond the piece
family (cell-containment membership, and `r_bulk = 3` coarse bulk rows), so "the family is
inadequate by ~2.7 pieces" over-attributes. The corrected claim: at N = 281 the method is already
past its own granularity reach (`62*(1+2*sqrt3) = 276.8`), and the excess over 15 is shared
between family resolution and grid granularity in a proportion this audit does not determine.

**C5 — do not extrapolate the LP from its local slope.** The 0.080-per-unit slope between N = 281
and N = 282 is not informative about where the LP would reach 15: the controls show the value
dropping by 1.0 (n=4, n=10) and 2.0 (n=6) across a *single* unit of N at the threshold.

---

## Reproduce

One command, ~1 core, ~2 minutes, exact arithmetic only:

```bash
cd experiments/packing-n16-verify-6 && \
  python3 v6check.py && python3 corrupt.py && python3 probe.py
```

`v6check.py` is the independent checker (arrangement-vertex algorithm); `corrupt.py` runs the 21
corruptions through both checkers; `probe.py` runs the 171k-polygon convexity probe, the
weight-reallocation corruptions and the box-decoder comparison behind C1.
