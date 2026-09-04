# packing-r4-krawczyk — interval Krawczyk enclosures + exact witness packings

**CONSTRUCTION (upper bound) ONLY. Nothing in this directory bears on optimality**, for any
`n`. Every bound below is `s(n) <= ...`; the lower-bound side of the problem is untouched.

```
status:  numerical      — every claim in this directory, without exception
author:  claude (Opus 5), worker r4-krawczyk, 2026-08-24
reproduce (whole thing, ~40 s, deterministic, no randomness):

    python3 run_all.py
```

`run_all.py` reads float candidates from `../circle-packing-ls/candidates/`,
`../circle-packing-search/out/` (both read-only inputs) and `out/extra/`, and writes
`out/n0NN.json`, `out/summary.json` and `certificates/`. Given those candidate files it is
deterministic — there is no randomness anywhere in the certified path.

`out/extra/n{29,33,34}.json` are committed candidate data, produced by the optional front end
`python3 search_extra.py <n> <restarts>` (seeded multistart SLSQP, floats only, output is a
hypothesis and never a certificate). The best was found at restart 330 (`n = 29`), 137
(`n = 33`) and 45 (`n = 34`); a re-run with at least that many restarts reproduces them, which
was checked for `n = 34` (`search_extra.py 34 60` returns the committed configuration bit for
bit). Verifying the certificates needs none of this — run `check_certificates.py`.

---

## 1. The question

Problem `RULES.md` §6 target 3 is "verify Graham–Lubachevsky's 22 <= n <= 34 packings with
exact certificates". The repo could not do it: `../circle-packing-ls/certificate.py` snaps to
rationals with denominator 1e15 and then *inflates* `s` until feasibility returns, which is
honest but permanently loose; and the exact `Q(sqrt 3)` route of `../packing-r3-qsqrt3/` only
works for the `n` whose optimum happens to lie in that field (17, 24, 31).

The idea tested here: an **interval Krawczyk operator** can prove that a solution of the
contact system exists in an explicit rational box without ever solving for it in closed form.

## 2. What is actually proved, and what is not

Two separate statements per `n`. Keeping them apart is the whole point of this directory.

**(A) The bound — unconditional, exact, self-contained.**
`certificates/n0NN-r4-krawczyk.json` gives explicit coordinates in `Q(sqrt 3)` and is verified
by exact rational arithmetic: all C(n,2) pairwise distances `>= 2`, all points in the closed
triangle `A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2)`, and `d` equal to the exact minimal enclosing
side for that point set (so the certificate is **tight** in the sense of problem `RULES.md`
§2). This needs no Krawczyk theorem and no trust in any interval code.

**(B) The enclosure — what Krawczyk adds.** For each `n` a square subsystem of the tight
contact/wall equations, with the variables the tight system does not determine frozen at exact
rationals, is proved to have **exactly one** solution inside an explicit rational box, by the
Krawczyk test in exact rational interval arithmetic. From it, `d` for that solution is enclosed
to width ~1e-49. That pins the *conjectured exact value* to 49 digits — but it is a statement
about a solution of an equation system, **not** a packing certificate.

**(A) is not derived from (B).** An enclosure of a stationary point is not a packing;
§4 below says precisely why the box cannot carry the bound here.

## 3. Results

`K` = number of tight constraints (contacts + wall incidences); `rank` = rank of their
Jacobian; `vars` = 2n+1; `frozen` = variables the tight system leaves undetermined; `dropped`
= tight equations left out of the square subsystem. "vs GL record" compares the certified `d`
against the **exact rational band** implied by Graham–Lubachevsky's printed 15 significant
figures — comparing against a single rounded float would manufacture 1e-14-sized "records"
(problem `RULES.md` §4: an improvement must exceed the error bars).

| n | tight K | rank | vars | frozen | dropped | Krawczyk | encl. width | certified d(n) <= (25 s.f.) | vs GL record |
|---:|---:|---:|---:|---:|---:|:--|---:|---|:--|
| 3 | 9 | 7 | 7 | 0 | 2 | yes | 2.0e-50 | 2.0 | n/a (not in GL table) |
| 6 | 18 | 13 | 13 | 0 | 5 | yes | 2.0e-50 | 4.0 | n/a (not in GL table) |
| 8 | 18 | 17 | 17 | 0 | 1 | yes | 1.1e-49 | 5.829708431025352439900408 | within_table_rounding |
| 10 | 30 | 21 | 21 | 0 | 9 | yes | 2.0e-50 | 6.0 | n/a (not in GL table) |
| 12 | 30 | 25 | 25 | 0 | 5 | yes | 1.3e-49 | 7.464101615137754587054893 | n/a (not in GL table) |
| 15 | 45 | 31 | 31 | 0 | 14 | yes | 2.0e-50 | 8.0 | n/a (not in GL table) |
| 16 | 34 | 32 | 33 | 1 | 2 | yes | 2.2e-49 | 9.24952715901279142778719 | within_table_rounding |
| 18 | 40 | 37 | 37 | 0 | 3 | yes | 2.7e-49 | 9.829688819085669059131932 | within_table_rounding |
| 19 | 45 | 39 | 39 | 0 | 6 | yes | 2.1e-49 | 9.983952843341383485316573 | within_table_rounding |
| 21 | 63 | 43 | 43 | 0 | 20 | yes | 2.0e-50 | 10.0 | within_table_rounding |
| 22 | 47 | 41 | 45 | 4 | 6 | yes | 1.7e-49 | 11.14846412614109311658578 | within_table_rounding |
| 23 | 52 | 45 | 47 | 2 | 7 | yes | 1.8e-49 | 11.41856816449211725934931 | within_table_rounding |
| 25 | 63 | 51 | 51 | 0 | 12 | yes | 1.5e-49 | 11.82970843102535243990041 | within_table_rounding |
| 26 | 63 | 53 | 53 | 0 | 10 | yes | 2.4e-49 | 11.99483746547662166779406 | within_table_rounding |
| 27 | 79 | 55 | 55 | 0 | 24 | yes | 2.0e-50 | 12.0 | within_table_rounding |
| 29 | 63 | 55 | 59 | 4 | 8 | yes | 2.7e-49 | 13.14150122755351326427398 | within_table_rounding |
| 30 | 73 | 59 | 61 | 2 | 14 | yes | 2.1e-49 | 13.26598632371090413092971 | within_table_rounding |
| 32 | 77 | 64 | 65 | 1 | 13 | yes | 2.1e-49 | 13.78339146305899238353221 | within_table_rounding |
| 33 | 82 | 67 | 67 | 0 | 15 | yes | 2.5e-49 | 13.94239423861395512350145 | above |
| 34 | 83 | 69 | 69 | 0 | 14 | yes | 3.1e-49 | 13.99897060287470441204934 | above |

`s(n) = 2*sqrt(3) + d(n)`; the certificates report `s`, per problem `RULES.md` §2. Of the 15
`n` that have a published Graham-Lubachevsky entry, **13 land inside the band, 2 are above it
(`n = 33, 34`), and none is below**; the remaining 5 are calibration cases compared against
exact closed forms instead.

`n = 3, 6, 10, 15, 21` are the triangular lattices, `n = 8, 12` the settled non-lattice cases;
these seven are the calibration set and were run before any open `n`. `n = 21` and `n = 27` sit
inside their GL band trivially because the printed value there is `0.2` / `0.166666666666667`;
for `n = 21` the exact comparison against `d = 10` is the meaningful one and it passes.

### Calibration (the gate for going on to open `n`)

| n | known exact d(n) | certified d >= exact? | Krawczyk enclosure contains exact? |
|---:|---|:--|:--|
| 3 | 2 | yes | yes |
| 6 | 4 | yes | yes |
| 8 | 2 + 2*sqrt(33)/3 | yes | yes |
| 10 | 6 | yes | yes |
| 12 | 4 + 2*sqrt(3) | yes | yes |
| 15 | 8 | yes | yes |
| 21 | 10 | yes | yes |

Both columns are decided by exact rational comparisons against `a + b*sqrt(c)`
(`exactvals.cmp_rat_alg`), not by float distance. All seven pass, so the pipeline was allowed
to proceed. Sources for the exact values: `../circle-packing-search/reference.py` (Friedman,
Packing Center), converted by `d = s - 2*sqrt(3)`.

### Independent cross-check

All 20 algebraic certificates were additionally fed to
`../packing-r3-recheck/recheck.py` — a checker written by a different worker directly from
the problem statement, with no knowledge of this code. It **accepts all 20 and reports
`tight = True` for all 20** (`out/recheck-crosscheck.txt`), together with its own positive,
negative and cited-value controls. That is a strong control on the conventions, which is where
this kind of work usually goes wrong. It is **not** a `verified:review`: `recheck.py` and this
directory are the same model family, and problem `RULES.md` §3 requires the other family.

## 4. Why the Krawczyk box cannot carry the bound (measured, not assumed)

To turn the box into a packing certificate one needs: the enclosed solution satisfies the
selected equations exactly (true by the theorem), every **non**-tight constraint holds strictly
across the whole box (verified — `nontight_constraints_strict_over_box` is `true` at all 20
`n`), *and* every tight constraint left out of the square subsystem still holds at the solution.

That last one fails structurally. **At all 20 configurations the tight constraint set is
over-determined: `K > rank` everywhere**, with `K - rank` running from 1 (n=8) to 24 (n=27).
A dropped tight equation becomes an inequality that is *active* at the solution, so its
interval evaluation over any box containing that solution straddles zero and can never be
verified. The `dropped` column is therefore never 0, and the box-derived bound is never
unconditional. Hence route (A).

This is the concrete form of the warning in the assignment: *an enclosure of a stationary point
is not by itself a packing certificate.*

The complementary deficiency also occurs: at `n = 16, 22, 23, 29, 30, 32` the tight system
leaves 1–4 variables undetermined (rattler degrees of freedom). Those are frozen at exact
rationals by the rank-revealing pivoting, which is what makes the square system exist at all.
So both failure modes anticipated by `attacks/r3-stationarity/README.md` §6 are present in the
same configurations, and neither of them stops the *upper-bound* pipeline.

## 5. Method, in the order it is worth reviewing

1. **Sheared coordinates** (`model.py`). Substituting `y = sqrt(3) u` makes every constraint
   rational: `u >= 0`, `x - u >= 0`, `d - x - u >= 0`, `(dx)^2 + 3 (du)^2 >= 4`, and
   `d_min = max_i (x_i + u_i)`. No irrational constant enters the arithmetic anywhere. The
   `sqrt(3)` only reappears when a certificate is written back in `(x, y)`.
2. **Tight structure** at tolerance 1e-7 (with a 1e-6/1e-8/1e-9 retry sweep, keeping the
   structure whose Newton residual is smallest).
3. **Square subsystem** by full-pivot Gaussian elimination on the tight Jacobian, with the
   `d` column boosted so `d` is chosen free whenever it can be. This simultaneously drops
   dependent equations and freezes undetermined variables.
4. **Newton** at 80 digits on that subsystem.
5. **Krawczyk** (`krawczyk.py`), in exact rational interval arithmetic on the fixed grid
   1e-50 (`iv.py`, integer endpoints, outward rounding on every operation). Box radius 1e-30,
   with a fallback ladder. Floats/mpf propose the midpoint and the preconditioner `C` only —
   both then enter as exact rationals, and the theorem does not require `C` to be a good
   inverse, only the test to succeed with it.
6. **Witness** (`witness.py`): snap to denominator 1e40, restore exact wall incidences, clamp
   so `u >= 0` and `x >= u` hold exactly, then repair separation with a **homothety about
   A = (0,0)** by a rational `lambda` with `lambda^2 >= 4 / min_sep^2`. A homothety about `A`
   maps `T_d` onto `T_{lambda d}`, so containment survives and every separation is multiplied
   by `lambda >= 1`. This is why the witness is unconditionally feasible whatever the snapping
   did; the measured repair is `lambda - 1 ~ 1e-41` (exactly 1 at the lattice cases, where the
   snap is exact).
7. **Exact verification from scratch**, then certificate emission.

Every accept/reject decision in steps 5–7 is exact: `fractions.Fraction` or integer grid
endpoints. Floats appear only in search and in cosmetic printing.

## 6. Honest limitations

- **`n = 33, 34` land above the published record**, by 2.2e-6 and 2.0e-4. That is a *front-end*
  limitation, not a certification failure: the best float candidate available for those `n` is a
  worse local optimum than Graham–Lubachevsky's. `search_extra.py` improved `n = 29` from
  1.5e-3 above the band to inside it, and improved 33 and 34 without closing the gap. The
  certified bounds for those `n` are valid upper bounds, just not the best known ones.
- **No record is claimed anywhere.** No certified `d` falls below its GL band; the 17 that are
  in-band are reproductions, which problem `RULES.md` §4 names as the good outcome.
- **The interval certificates** (`*-interval.json`) are honest upper bounds and are explicitly
  **not** tight: the declared `d` exceeds the box-minimal enclosing side by < 1e-40. They exist
  because the assignment asked for `coordinate_type: "interval"`; the algebraic certificates
  are strictly stronger (exact and tight) and are the primary artifact.
- **`numerical`, and it stays there** until an agent of a different model family writes its own
  checker (problem `RULES.md` §3). Nothing here may be built on.

## 7. Files

| file | role |
|---|---|
| `iv.py` | exact rational interval arithmetic on the 1e-50 grid, outward rounding |
| `model.py` | contact system in sheared coordinates, tight structure, rank-revealing pivoting, Newton |
| `krawczyk.py` | the Krawczyk operator and test, exact rational |
| `witness.py` | snap + homothety repair + exact from-scratch verification |
| `emit.py` | certificate emission (`algebraic` and `interval`) per problem `RULES.md` §2 |
| `exactvals.py` | known exact values and the GL printed-value bands, with sources |
| `run_all.py` | driver; per-`n` checkpoint to `out/` |
| `check_certificates.py` | re-reads the emitted certificate *files* and verifies both types from scratch |
| `search_extra.py` | optional seeded multistart front end (floats only) |
| `certificates/` | 20 algebraic + 20 interval certificates |
| `out/recheck-crosscheck.txt` | output of the independently written `packing-r3-recheck` checker |
