# Scaling closure: go/no-go on proposal J, with the n = 7 pilot

```
claim type: lower bound on d(7) and on the n = 16 pigeonhole ceiling
status:     sketch (the argument) / numerical (every computed value)
issue:      #62
verdict:    mechanism SOUND, novelty OVERSTATED, ambition DEAD at n = 16
```

**Nothing here is assumable.** Proposal J
(`problems/circle-packing-equilateral-triangle/attacks/approaches-round-2/README.md`, PR #61)
is an unexamined `sketch`, so per repo `RULES.md` §3 everything derived from it is capped at
`sketch`, whatever the exactness of the arithmetic. Computed values are `numerical`. Nothing in
this directory belongs in `problems/**/results/`, and no `verified:review` is claimed — only a
cross-family examiner may grant that.

---

## 1. Proposal J, restated

Conventions are the problem's: `T_d` is the *closed* equilateral triangle of side `d`, and
`d(n) = inf { d : T_d contains n points with pairwise distance >= 2 }`. Because `T_c` embeds in
`T_{c'}` for `c <= c'`, the set of admissible sides is an up-set, so `d(n)` is well defined and
"no admissible configuration at side `c`" is equivalent to `d(n) >= c`.

*Pigeonhole (the existing machinery, PR #53).* If `T_d` is covered by `n-1` sets each of diameter
**strictly** below 2, then any `n` points in `T_d` put two in one set at distance `< 2`, so no
admissible configuration exists and `d(n) > d`.

*J's addition.* Let `d*` be the exact algebraic critical side. Suppose `T_{d*}` admits a cover by
`n-1` closed convex cells of diameter **`<= 2`** — non-strict, cells allowed to be exactly
critical. For each `lambda < 1` the dilation `x -> lambda x` about a triangle vertex carries this
to a cover of `T_{lambda d*}` by `n-1` cells of diameter `<= 2 lambda < 2`. Pigeonhole gives
`d(n) >= lambda d*` for every `lambda < 1`; taking the supremum, `d(n) >= d*`. Paired with a
construction attaining `d*`, that is the equality `d(n) = d*` — from **one** finite object rather
than a certificate re-run at each `d`.

---

## 2. Auditing J step by step, before running anything

| Step | Verdict |
|---|---|
| Dilation preserves **coverage** | **Sound.** A dilation is a bijection of the plane, so the image of a cover of `T_{d*}` is a cover of the image `T_{lambda d*}`. Nothing can open a gap; the cells and the triangle are transported by the same map. Fixing the map's centre at the vertex `A = (0,0)` also keeps the problem's fixed triangle placement (problem `RULES.md` §2). |
| Dilation preserves **strictness**, uniformly | **Sound.** Diameter is homogeneous of degree 1, so `diam <= 2` becomes `diam <= 2 lambda < 2` for *every* cell at once; the bound is uniform because `2 lambda` does not depend on the cell. `covercheck.py --scale` re-derives this in exact arithmetic rather than assuming it, and `test_scaling_makes_every_cell_strictly_subcritical` pins squared diameter to exactly `4 lambda^2`. |
| The **supremum** step | **Sound, and needs no limit interchange.** `d(n) >= lambda d*` for all `lambda < 1` gives `d(n) >= sup_lambda lambda d* = d*` directly. There is no limit of certificates, no exchange of limit and quantifier, and no compactness. This is the step §5 would normally target, and it survives. |
| **Existence** of a non-strict cover at `d*` | J's own flagged weak point. **It is not the weak point.** See §3 (verified for `n = 7`) and §5 (it is free in general, by compactness). |
| J's premise that current machinery "can never reach `d*`" | **This is the false step.** See §5. |

---

## 3. The n = 7 pilot — the validation gate

`d(7) = 2 + 2*sqrt(3)` is `cited` (Melissen 1993; equivalently Graham 1967's unit-triangle
six-cell constant `1/(1 + sqrt 3)`), and `s(7) = d(7) + 2 sqrt 3 = 2 + 4 sqrt 3`. PR #53
reconstructed Graham's Figure-7 six-cell topology but could only place it at the *rational* side
`683/125`, about `1.0e-4` below `d*`, because its verifier parses rationals only.

`generate_graham6_exact.py` puts the same topology at exactly

```
d* = 2 + 2*sqrt(3),   delta = 1/(1 + sqrt 3) = (sqrt 3 - 1)/2,   r = delta/sqrt 3 = (3 - sqrt 3)/6
```

with every coordinate an exact element of `Q(sqrt 3)`. `covercheck.py` accepts it in `nonstrict`
mode:

```
cells                     6  ( = n - 1 )
triangle_side             2 + 2*sqrt(3)          ~ 5.464101615137754
max_squared_diameter      4 + 0*sqrt(3)          exactly 4
max_squared_diameter - 4  0                      exactly zero
```

**A non-strict cover does exist at the exact critical side.** All six cells have diameter exactly
2 — every one is critical, and 20 distinct vertex pairs sit at distance exactly 2. The same file
is rejected in `strict` mode, which is correct and is the reason the scaling step is needed.

Two consistency checks that would have exposed a bug:

* The maximum is exactly 4, **not below 4**. A slack cover at `d*` would give `d(7) > d*`,
  contradicting the `cited` value; the pilot would then have found a bug in itself, not a result.
* Raising the side to `d* + 1e-6` makes the maximum exceed 4 and the certificate is rejected.

Scaling by `lambda = 999999/1000000` yields an accepted **strict** certificate at side
`999999/500000 * (1 + sqrt 3) ~ 5.4640961510`, hence `d(7) > 5.4640961510...`. Over all
`lambda < 1` this gives

> **`d(7) >= 2 + 2*sqrt(3)`, equivalently `s(7) >= 2 + 4*sqrt(3) ~ 8.9282`** — status `sketch`.

Together with the `cited` construction at that side, `d(7) = 2 + 2 sqrt(3)`: **the known n = 7
optimum is reproduced. The validation gate passes.** No part of the computation consumes the
cited value; `d*` enters only as the side at which the cover is placed.

This is not new mathematics. It is Graham's own box-principle argument for `n = 7`, now carried
out in exact arithmetic by a checker written for this issue.

---

## 4. The kill-criterion, clause by clause

The issue #62 kill-criterion had four clauses. Against the pilot:

1. *No non-strict cover at `d*`* — **did not fire.** One exists, exactly.
2. *Scaling breaks coverage or strictness* — **did not fire.** Both are sound, and exercised.
3. *Only `d(n) >= lambda d*`, with no sound supremum step* — **did not fire.** The supremum is
   elementary.
4. *Cannot reproduce the known n = 7 optimum* — **did not fire.** It is reproduced exactly.

So J is **not refuted** as a mechanism. The two findings below are about what the mechanism is
worth, and they are the reason the recommendation is still negative.

---

## 5. Finding 1 — J's stated novelty does not hold

J's motivating sentence is that all current machinery "produces `d(n) > d* - epsilon` and can
never reach `d*`". That is true of any *single* strict certificate and false of the family. The
supremum step J itself uses applies verbatim to the strict certificates PR #53 already emits: if
strict covers exist at a sequence of sides increasing to `d*`, then `d(n) >= d*` by exactly the
same one-line argument, with no non-strict object anywhere.

Relatedly, J flags existence at `d*` as the step most likely to fail. It is instead free in
general. Convex hulls preserve diameter and preserve covering, so one may assume the cells are
compact convex; `m`-tuples of nonempty compact convex subsets of a compact `T` form a compact
space under the Hausdorff metric, covering is a closed condition, and diameter is continuous.
Hence the infimum over `m`-cell covers of the maximum diameter is **attained**, for every `m` and
every `T`. Writing `g(m)` for that minimum on the unit triangle, a non-strict cover exists at
side `2/g(n-1)` always. *(This compactness argument is mine and is `sketch`; nothing below
depends on it — §6's numbers are computed, not deduced from it.)*

What J actually buys is therefore **finiteness, not reach**: one certificate instead of an
infinite family. That is a genuine and useful gain for a Lean formalisation, and it is the honest
form of the contribution. It is not the "mechanism approach A lists as unavailable".

The consequence for reach is exact and unflattering: J's mechanism delivers

```
d(n) >= 2 / g(n-1)
```

and never more. That quantity is the **pigeonhole ceiling** — precisely what proposal L sets out
to measure. J's mechanism yields the equality `d(n) = d*` **iff pigeonhole is tight at `n`**.

---

## 6. Finding 2 — pigeonhole is not tight at n = 16, so J cannot close it

J calls `n = 16` "the gamble" and treats tightness there as an open empirical question. It is
already answered by the constant the repo has itself reconstructed.

`generate_graham15_exact.py` puts Graham's Figure-21 fifteen-cell complex (topology as
reconstructed in PR #53) at its exact critical side, with

```
D = 1/(1 + 2 sqrt 3),  H = sqrt(3) D,  X = D/sqrt(3),  P = 1 - 3H/2 - X/2
```

all exact in `Q(sqrt 3)`. The verifier accepts it in `nonstrict` mode at

```
cells                  15  ( = n - 1 )
triangle_side          2 + 4*sqrt(3)   ~ 8.928203230275509
max_squared_diameter   4               exactly
```

So the fifteen-cell complex is exactly critical too, and J's mechanism gives
`d(16) >= 2 + 4 sqrt(3) ~ 8.9282`. But the best known packing has `d(16) ~ 9.2495`
(`numerical`, quoted from PR #56). Hence

> **the n = 16 pigeonhole ceiling is at most `2 + 4 sqrt(3) ~ 8.9282 < 9.2495`,** and if Graham's
> `d_15 = 1/(1 + 2 sqrt 3)` is optimal — his 1967 claim, which this repo has reconstructed but not
> independently verified — the ceiling is *exactly* that, and **no 15-cell cover argument can ever
> close n = 16.** J's gamble is lost by roughly `0.32` in `d`.

Note also that `2 + 4 sqrt(3)` is already the `cited` Graham bound recorded in
`problems/circle-packing-equilateral-triangle/README.md`. J's mechanism at `n = 16` therefore
converts PR #53's `d(16) > 8.928 - 1e-4` into `d(16) >= 8.928` exactly: a real but sub-`1e-4`
improvement over a bound that is itself already known and already `~0.32` short.

---

## 7. Recommendation

**No-go on J as a route to closing an open case.** Its mechanism is sound and its `n = 7`
instance is exact and verified, but its reach is capped at the pigeonhole ceiling, which is
already known to fall short at `n = 16` — the case J targets. Recommend against spending the
Lean-formalisation effort on the equality ambition.

**Keep two things.** (i) The exact `Q(sqrt 3)` cover verifier and the two critical certificates:
they make the pigeonhole ceiling *measurable exactly* rather than to `1e-4`, which is exactly the
instrument proposal L needs. (ii) The `n = 7` artifact, which is a small, finite, genuinely
Lean-shaped optimality argument (finitely many `Q(sqrt 3)` inequalities plus one dilation) and
would be the repo's first optimality object of any kind — but for a case that is already `cited`,
so its value is pipeline validation, not new mathematics.

`RULES.md` §7 applies in the other direction here: nothing in this directory settles anything
open, and the one open-case number it produces is *worse* than the best known.

---

## 8. What is in this directory

| File | Role |
|---|---|
| `qsqrt3.py` | exact arithmetic in `Q(sqrt 3)`; sign decided by comparing `a^2` with `3b^2`. `Q3.approx()` is for printing and is never on a decision path. |
| `covercheck.py` | exact **cover** verifier over `Q(sqrt 3)`, with `--mode nonstrict|strict` and `--scale <lambda>` |
| `generate_graham6_exact.py` | Graham Figure 7 at exactly `d* = 2 + 2 sqrt 3` (`n = 7`) |
| `generate_graham15_exact.py` | Graham Figure 21 at exactly `2 + 4 sqrt 3` (`n = 16` ceiling) |
| `certificates/*.json` | the two committed certificates |
| `tests/test_covercheck.py` | 20 tests, including negative controls |

### Relation to the merged verifier

`experiments/circle-packing-partitions/partitioncheck.py` (PR #53) was read and **not modified or
imported**. It cannot be reused here: its scalar grammar accepts rational strings only, so the
exact algebraic side `2 + 2 sqrt(3)` is not expressible in it, and its diameter test is
hard-wired strict, which rejects the very object J is about. `covercheck.py` is an independent
reimplementation in the field, sharing only the problem's fixed oblique-coordinate convention.

What it checks, all in exact `Q(sqrt 3)`:

1. scalars are bounded rational pairs `["a","b"]` meaning `a + b sqrt 3`; decimal strings rejected;
2. exactly `n - 1` cells;
3. each cell is a strictly convex counterclockwise polygon whose vertices lie in `T_d`
   (`u >= 0`, `v >= 0`, `u + v <= d`) — with convexity, vertex containment gives cell containment;
4. every pair of cells meets in zero area (exact Sutherland-Hodgman clipping, exact division);
5. cell areas sum to the area of `T_d`;
6. max squared vertex-pair distance `<= 4` (`nonstrict`) or `< 4` (`strict`), under
   `q(du,dv) = du^2 + du dv + dv^2`; for a convex cell the diameter is attained at a vertex pair.

Checks 3-5 are what establish **coverage**: the union is closed, lies in `T_d`, has interiors
meeting in measure zero, and has full area, so the relatively open complement has zero area and
is empty; hence the union contains the interior and, being closed, all of `T_d`. J suggests a
BSP-witnessed coverage check as a more Lean-friendly alternative; that is not implemented here,
because the objects at hand are genuine partitions and the area route is already sound. Anyone
adopting J's cover-with-overlap generalisation would need the BSP route or an equivalent, since
the area identity fails as soon as overlaps are real.

Floats appear nowhere on the verification path.

## Reproduce

```bash
cd experiments/circle-packing-scaling-closure
python3 generate_graham6_exact.py  | diff - certificates/n007-graham6-critical.json
python3 generate_graham15_exact.py | diff - certificates/n016-graham15-critical.json
python3 covercheck.py certificates/n007-graham6-critical.json  --mode nonstrict
python3 covercheck.py certificates/n007-graham6-critical.json  --mode strict      # must fail
python3 covercheck.py certificates/n007-graham6-critical.json  --mode nonstrict --scale 999999/1000000
python3 covercheck.py certificates/n016-graham15-critical.json --mode nonstrict
python3 -m unittest discover -s tests -v
```

No seeds, no libraries beyond the standard library, no randomness: every run is deterministic.
Python 3.14.5; nothing in the code is version-sensitive beyond `fractions`.
