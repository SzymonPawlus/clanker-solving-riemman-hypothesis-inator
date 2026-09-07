# AB. Euler-localised scoring on the Delaunay triangulation — outcome (a), family no stronger than Oler

**This is a lower-bound (optimality-side) attack. It produces no construction and claims no
packing. It establishes no new bound: its result is that a family of candidate bounds collapses
onto one the repo already has.**

```
status:  numerical  — every number below; the LP is solved in floating point and its
                      optimum is a HYPOTHESIS about the family, not a bound
         sketch     — the framework itself (the score family, the telescoping identity,
                      the (D)/(V) conditions), unreviewed prose by an agent
author:  claude (Opus 5), worker r4-delaunay, 2026-08-24
issue:   #110, round-4 rerun of round-3 proposal AB (attacks/r3-approaches/README.md)
code:    experiments/packing-r4-delaunay/
kill:    KILL-CRITERION.md — FIRED, outcome (a)
```

**Nothing here is assumable** (`RULES.md` §3). Depends on nothing unmerged; in particular it does
**not** use the `n = 16` covering bound of PRs #98/#104.

> **Write-up provenance — read this before trusting the framing.** The worker that produced these
> numbers was terminated by an infrastructure error (connection loss) *after* completing the
> measurement and *before* writing this file. The manager salvaged it from the committed code and
> the run report. **Everything in §§1–4 is transcribed from `experiments/packing-r4-delaunay/out/report.txt`
> and the code that produced it. §5 lists what the worker intended and did not deliver — that
> material is absent, not summarised.** No step has been reconstructed from memory or inferred.

---

## 0. Result

| | |
|---|---|
| Question | is a *nonlinear* Hales-style local score on the Delaunay triangulation stronger than Oler, which is the family's linear member? |
| Bar | Oler at `n = 16`: `d(16) ≥ √129 − 3 = 8.3578166916` (`sketch` application of a `cited` inequality) |
| LP optimum over the family at `n = 16` | `8.3578166916` — equal to Oler, to solver precision |
| Outcome | **(a): the family is no stronger than its linear member** |
| Kill-criterion | **fired** |

The measurement is *not* "we failed to find a better score". It is that the LP, given complete
freedom to choose one score value per face shape, **returns the linear member** — deviation `0.00e+00`.

## 1. The control, which is what makes the negative meaningful

A framework that cannot reproduce Oler proves nothing when it fails to beat Oler. So the
load-bearing check ran first: instantiate the family at its linear member
`σ(f) = (2/√3)·area(f) − 1/2`, `τ(l) = (l−1)/2`, and confirm the telescoped bound is *exactly*
Oler's.

```
   n      d from framework      √(8n+1)−3       abs diff
   3        2.000000000000    2.000000000000    4.44e-16
  15        8.000000000000    8.000000000000    8.88e-16
  16        8.357816691601    8.357816691601    1.78e-15
  21       10.000000000000   10.000000000000    1.78e-15
  28       12.000000000000   12.000000000000    1.78e-15
```

**CONTROL PASSED.** The framework recovers Oler at machine precision, including exactly at the
triangular numbers where Oler is tight.

Independently, the configuration library reproduces the face-excess / edge-excess / slack atlas of
the merged `attacks/oler-slack-analysis` on all 15 shared entries (lattices and
lattice-minus-apex at excess exactly 0; `n = 4` corners+centroid at `1.0980762`; the flat-arc
family at `0.1738065 … 0.1917186`). The code shares nothing with `experiments/packing-oler-slack`,
so this is an independent reconstruction rather than a rerun.

## 2. The measurement

31 configurations, each carrying exact self-checks asserted at construction: all pairwise
separations `≥ 1`; Euler `F = 2n − b − 2`; face areas summing exactly to the hull area; boundary
edge lengths summing to the hull perimeter. Areas exact in `Q(√3)`.

**Step 2 — reduced LP** (two variables `c_A`, `c_L`), library refined from 10 to 63 configurations:

```
 size  #cfgs      d(16)       d(17)       d(18)     c_A*      c_L*
    3     10   10.000000   10.666667   11.333333  0.000000  1.000000
    4     16    8.357817    8.704700    9.066667  1.154701  0.500000
    6     31    8.357817    8.704700    9.041595  1.154701  0.500000
   10     63    8.357817    8.704700    9.041595  1.154701  0.500000
 Oler          8.357817    8.704700    9.041595  1.154701  0.500000
```

The size-3 row is above Oler only because the library is too small to constrain the LP; adding
configurations drives it down to Oler and it stays there. `c_A* = 1.154701 = 2/√3` and
`c_L* = 0.5` are the linear member's own coefficients.

**Step 3 — the nonlinearity test.** `σ` is freed from being affine in area: every distinct
triangle shape in the library gets its own LP variable, likewise every distinct boundary edge
length (up to 29 shape variables and 23 edge variables).

```
 size  #shapes  #edges      d(16)       d(17)       d(18)   max|σ − linear|
    4        7       7    8.357817    8.704700    9.066667        0.00e+00
    6       16      14    8.357817    8.704700    9.041595        0.00e+00
    8       29      23    8.357817    8.704700    9.041595        0.00e+00
```

**Nonlinearity buys exactly nothing.** The LP drives every `σ` to the top of its own (D)
constraint, which *is* the linear member.

## 3. Why the direction of rounding matters here

Areas and perimeters enter the LP through `c_A·A + c_L·M + 1 ≥ n`, which are *necessary*
conditions on any family member. The code stores **outward (upper)** bounds for `A` and `M`, which
*weakens* those constraints and *enlarges* the LP's feasible set.

So the LP is an **optimistic relaxation** of the family: it can only over-estimate what the family
could prove. That is the direction which makes a negative answer meaningful — the true family
optimum is at most what the LP reports, and the LP reports Oler.

## 4. Reading

Oler is not merely *a* member of this family that happens to be good. Within what was measured, it
appears to be **the** optimum of the family, recovered from every starting point and unimproved by
freeing the score pointwise. That is a sharper statement than "we could not beat Oler", and it is
consistent with the round-3 pattern: the general-purpose lower-bound families this project has
tried keep collapsing onto bounds it already has.

## 5. What was NOT delivered — do not treat these as done

The worker died mid-sentence at exactly this point, and these gaps are real:

1. **The "collapse proposition" is missing.** The run report refers to "the collapse proposition in
   the attack README" — i.e. a *structural* argument for why the LP is forced to return the linear
   member rather than merely observed to. **That argument was never written down.** Without it, §4's
   "appears to be the optimum" is an observation over one library, not a theorem about the family.
   This is the single most valuable missing piece: it would convert a measurement into a statement
   about all such scores.
2. **The exact dual certificate is missing.** The worker's final act was to begin adding one, "so
   the conclusion doesn't rest on a float solver". It does not exist. **Every LP number above is
   float output**, hence `numerical`. An exact rational dual would make the negative rigorous, and
   it is a bounded, well-defined task for whoever picks this up.
3. **No `KILL-CRITERION.md` and no notebook entry** were written by the worker; the kill-criterion
   file accompanying this README was written by the manager from the run report.
4. The library is 31 configurations reaching `size 10`. It is not claimed to be exhaustive, and the
   LP's optimism (§3) is what licenses the negative despite that — but a larger library could only
   lower the LP value, never raise it.

## 6. Reproduce

```
python3 experiments/packing-r4-delaunay/run.py
```

Deterministic, no seeds, no network. Regenerates `out/report.txt` in full, including the step-0
exact self-checks, the control, both LPs and the verdict.

**Dependencies (required, not optional).** `numpy >= 1.26` and `scipy >= 1.11`, declared in
`experiments/packing-r4-delaunay/pyproject.toml`. STEP 0 is exact and stdlib-only, but STEPS 1–4
— the Oler control, both LPs and the verdict — are decided by `scipy.optimize.linprog` and have
no exact fallback, so there is nothing honest to skip. On an interpreter without them the command
now exits **2** with an install line rather than a raw `ModuleNotFoundError` traceback:

```
python3 -m venv .venv
.venv/bin/pip install 'numpy>=1.26' 'scipy>=1.11'
.venv/bin/python experiments/packing-r4-delaunay/run.py
```

Re-run and re-verified under numpy 2.5.2, scipy 1.18.1, CPython 3.14.5; the regenerated
`out/report.txt` was byte-identical to the committed one.

Every number this produces remains `numerical`: an LP optimum from a float solver is a hypothesis
about the family, not a bound.
