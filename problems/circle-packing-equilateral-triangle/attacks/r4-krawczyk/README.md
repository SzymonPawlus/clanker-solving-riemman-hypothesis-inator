# Approach: interval Krawczyk certificates for 16 <= n <= 34

**This is a CONSTRUCTION (upper bound). It is not an optimality claim, for any n.** What is
established is a list of bounds `s(n) <= 2*sqrt(3) + d` with `d` an explicit exact rational,
each witnessed by an exactly-verified packing. Nothing here bears on the lower bound, and every
`n` in the range remains exactly as open as it was.

```
status:  numerical      — every claim in this file, without exception
author:  claude (Opus 5), worker r4-krawczyk, 2026-08-24
code:    experiments/packing-r4-krawczyk/   (reproduce: python3 run_all.py, ~40 s)
scope:   problem RULES.md §6 target 3 — "verify Graham-Lubachevsky's 22 <= n <= 34 packings
         with exact certificates"
```

Under [`../../../../RULES.md`](../../../../RULES.md) §3 this is `numerical` and stays
`numerical` until an agent of a **different model family** writes its own checker from
[`../../README.md`](../../README.md). Until then **nothing here may be built on**, and the
certificates deliberately sit in `experiments/packing-r4-krawczyk/certificates/` rather than in
[`../../results/`](../../results/).

---

## 1. The gap this aimed at

Two exact-certificate routes existed and neither covers the range:

- `experiments/circle-packing-ls/certificate.py` snaps to rationals with denominator 1e15 and
  then **inflates** `s` by ~1e-11 until feasibility returns. Honest, but structurally never
  tight, so under problem `RULES.md` §2 it can never support a record claim.
- [`../r3-qsqrt3/`](../r3-qsqrt3/README.md) produced exact *tight* certificates at
  `n = 17, 24, 31` by recognising their closed forms in `Q(sqrt 3)`. That works only where a
  closed form exists. `n = 16` has only a PSLQ degree-10 minimal-polynomial candidate with no
  elimination link, and most of `22..34` has nothing at all.

The idea tested: **certify that a solution of the contact system exists, instead of solving for
it.** An interval Krawczyk operator proves existence and uniqueness of a zero inside an
explicit rational box without any closed form.

## 2. What was established

Krawczyk contracted at **all 20** `n` attempted — 7 calibration, 13 open — and every `n` got an
exact, exactly-verified, **tight** certificate.

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

Columns: `K` tight constraints (contacts + wall incidences), `rank` of their Jacobian, `vars`
= 2n+1, `frozen` = variables the tight system leaves undetermined, `dropped` = tight equations
outside the square subsystem. "vs GL record" is against the exact rational **band** implied by
Graham–Lubachevsky's printed 15 significant figures, not against a single rounded float.

Of the 15 `n` with a published Graham–Lubachevsky entry, **13 reproduce it (inside the
printed-precision band), 2 (`n = 33, 34`) are above it, and none is below.** The other 5 are
calibration cases, compared against exact closed forms instead, and all match. Problem
`RULES.md` §4's escalation was therefore never triggered — and matching is the outcome §4
names as good.

`s(n) = 2*sqrt(3) + d(n)`; the certificates report `s`, per problem `RULES.md` §2.

### Two statements, deliberately kept apart

**(A) The bound is unconditional and does not rest on the Krawczyk theorem.** Each certificate
carries explicit `Q(sqrt 3)` coordinates and is verified by exact rational arithmetic: all
C(n,2) distances `>= 2`, all points in the closed triangle in the fixed placement, and the
declared `d` equal to the exact minimal enclosing side for that point set — so **tight** per
problem `RULES.md` §2. A reader who distrusts every line of interval code can still check it.

**(B) The Krawczyk enclosure is what the interval machinery adds.** For each `n`, a square
subsystem of the tight equations (undetermined variables frozen at exact rationals) is proved
to have exactly one solution in an explicit rational box, and the `d` of that solution is
enclosed to width ~1e-49. This pins the conjectured exact value to 49 digits. It is a statement
about an equation system, **not** a packing certificate.

## 3. The load-bearing negative finding: the box cannot carry the bound

The assignment flagged step 5 as the easiest thing to get subtly wrong, and it is wrong in a
specific, measurable way here.

Turning the enclosure into a packing certificate needs three things. Two hold: the enclosed
solution satisfies the selected equations exactly (the theorem), and every **non**-tight
constraint is strictly satisfied across the whole box (verified in exact interval arithmetic at
all 20 `n`). The third fails:

> **At every one of the 20 configurations the tight constraint set is over-determined:
> `K > rank`, with `K - rank` between 1 and 24.**

The square subsystem therefore has to drop `K - rank` tight equations. A dropped tight equation
is an inequality that is *active* at the solution, so over any box containing that solution its
interval evaluation straddles zero and it can never be certified. The `dropped` column above is
never 0. **So the box-derived bound is never unconditional at these packings**, and the actual
bound has to come from an explicit configuration — which is exactly what the assignment
demanded be stated precisely.

The complementary deficiency also shows up: at `n = 16, 22, 23, 29, 30, 32` the tight system
leaves 1–4 variables undetermined (rattler degrees of freedom), i.e. `rank < 2n+1`. These are
frozen at exact rationals by rank-revealing pivoting, which is what makes a square system exist
at all.

Both failure modes anticipated in [`../r3-stationarity/`](../r3-stationarity/README.md) §6 —
over-determination killing a square system, positive-dimensional strata from rattlers — are
present *in the same configurations*. The finding worth recording is that **neither of them
blocks the upper-bound pipeline**: they only block using the enclosure as the certificate. The
r3-stationarity worry was about the lower-bound enumeration, and this measurement neither
confirms nor relieves it there.

## 4. How the bound is actually obtained

`witness.py`, in four exact steps. Working in sheared coordinates `y = sqrt(3) u` makes every
constraint rational (`u >= 0`, `x - u >= 0`, `d - x - u >= 0`,
`(dx)^2 + 3 (du)^2 >= 4`, `d_min = max_i (x_i + u_i)`), so no irrational constant ever enters
the arithmetic:

1. snap the 80-digit Newton solution to denominator 1e40;
2. restore exact wall incidences and clamp so `u >= 0` and `x >= u` hold exactly;
3. repair separation by a **homothety about `A = (0,0)`** with a rational `lambda` satisfying
   `lambda^2 >= 4 / min_sep^2`. A homothety about `A` maps `T_d` onto `T_{lambda d}`, so
   containment survives and every separation is multiplied by `lambda >= 1`;
4. declare `d = max_i (x_i + u_i)`, which is exactly the minimal enclosing side, and re-verify
   everything from scratch in exact rational arithmetic.

Step 3 is what makes the result unconditional: whatever the snapping did, the homothety repairs
it, and the repair is measured — `lambda - 1 ~ 1e-41`, and exactly 1 at the lattice cases where
the snap is already exact. The witness `d` exceeds the Krawczyk enclosure's upper endpoint by
~1e-40, so the bound is within 1e-40 of the best this contact structure can give.

Compare with the existing generator: `certificate.py` inflates by ~1e-11 and is never tight;
this is 29 orders of magnitude closer *and* tight, at every `n` in the range, with no closed
form required.

## 5. Controls

- **Calibration first.** The seven solved cases `n = 3, 6, 10, 15, 21` (triangular) and
  `n = 8, 12` were run before any open `n`. For all seven the certified `d` is `>= ` the known
  exact value **and** the Krawczyk enclosure contains it, both decided by exact rational
  comparison against `a + b*sqrt(c)`, never by float distance. Sources for the exact values:
  `experiments/circle-packing-search/reference.py` (Friedman, Packing Center).
- **Independent checker.** All 20 algebraic certificates were fed to
  `experiments/packing-r3-recheck/recheck.py`, written by a different worker directly from the
  problem statement with no knowledge of this code. It **accepts all 20 and reports
  `tight = True` for all 20**, alongside its own positive, negative and cited-value controls
  (`experiments/packing-r4-krawczyk/out/recheck-crosscheck.txt`). This is a strong control on
  the *conventions*, which is where this class of work usually fails. It is **not** a
  `verified:review`: same model family (problem `RULES.md` §3 requires the other one).
- **Record comparison uses error bars.** Graham–Lubachevsky print `d(n)` to 15 significant
  figures, so the implied `D = 2/d(n)` is an interval of width ~4e-14. Comparing against a
  single rounded float would have manufactured a spurious "record" at `n = 25`, where the
  certified value sits 8e-15 below the midpoint and comfortably inside the band, and at
  `n = 29` it sits 3.4e-14 below it. Problem
  `RULES.md` §4 requires an improvement to exceed the error bars; the comparison implements
  that literally (`exactvals.gl_D_band`).

## 6. What this does *not* show

- **Not optimality**, for any `n`. These are upper bounds. The exact contacts and the tightness
  are local statements about one configuration.
- **Not that Graham–Lubachevsky's values *are* `s(n)`.** The agreement is that our certified
  construction reproduces their number; both could be non-optimal.
- **Not that the enclosed contact solution is the global optimum**, or even a local one.
  Krawczyk certifies a solution of an equation system; nothing here tests second-order
  conditions.
- **Not a dependency for anything.** `numerical` (`RULES.md` §3).
- `n = 33, 34` are **not** reproductions of the record: they are valid bounds that are worse
  than the published one (by 2.2e-6 and 2.0e-4), because the best float candidate available for
  those `n` is a poorer local optimum. A seeded multistart front end pulled `n = 29` from
  1.5e-3 above the band to inside it, and improved 33 and 34 without closing the gap.

## 7. Kill-criterion

Did not fire. See [`KILL-CRITERION.md`](KILL-CRITERION.md).

## 8. Least certain step

Not the exact arithmetic and not the Krawczyk test — the exposure is the **identification of
the tight structure** at step 2 of the pipeline. It is chosen by a float tolerance (1e-7, with
a retry sweep), and a wrong choice would send Newton to a different solution. Three things
bound the damage and none of them removes it: the final feasibility check is exact and would
reject an infeasible outcome; the homothety repair factor `lambda - 1 ~ 1e-41` shows the
snapped configuration was already almost exactly feasible, which a badly-chosen structure would
not produce; and 17 of 20 land inside the published band. What remains unchecked is whether a
*better* tight structure exists near the same float configuration — that would only improve the
bound, never invalidate it, but it is the reason `n = 33, 34` should not be read as evidence
about those packings.
