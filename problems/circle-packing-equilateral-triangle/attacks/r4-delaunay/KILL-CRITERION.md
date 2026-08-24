# Kill-criterion — approach AB (Euler-localised Delaunay scoring)

**Written by the manager from `experiments/packing-r4-delaunay/out/report.txt`**, because the
worker was terminated by a connection loss after completing the measurement and before writing
its own files. Nothing here is inferred; every number is transcribed from that report.

## As stated in the assignment

> If the LP optimum at `n = 16` does not strictly exceed `√129 − 3 = 8.3578166916`, the family is
> no stronger than its linear member. Record the LP, the discretisation and the value, and STOP.
> Do not refine repeatedly hoping the number moves; report the trend across two or three
> refinements and the limit it appears to approach.

## Verdict: **FIRED**

The prerequisite control passed first — the framework reproduces Oler's `√(8n+1) − 3` at its
linear member to `≤ 1.78e-15` across `n = 2, 3, 6, 10, 15, 16, 17, 18, 21, 28`. A framework that
could not do this would have proved nothing by failing to beat Oler.

Trend of `d(16)` across library refinement, as required:

| library size | #configs | d(16) | excess over Oler |
|---:|---:|---|---|
| 3 | 10 | 10.0000000000 | +1.642e+00 |
| 4 | 16 | 8.3578166916 | −1.776e-15 |
| 5 | 23 | 8.3578166916 | −1.776e-15 |
| 6 | 31 | 8.3578166916 | −1.776e-15 |
| 8 | 47 | 8.3578166916 | −1.776e-15 |
| 10 | 63 | 8.3578166916 | −1.776e-15 |

The size-3 row exceeds Oler only because ten configurations under-constrain the LP. From size 4
onward the value is Oler's, and refining four more times does not move it.

The nonlinearity test (one free score variable per face shape, up to 29 shapes and 23 boundary
edge lengths) returns `max |σ − linear| = 0.00e+00`: the LP chooses the linear member even when
free not to.

**Outcome (a): the family is no stronger than its linear member. Stopped.**

## What the firing does and does not license

- It does **not** say a localised-scoring bound is impossible in principle. It says that *within
  this family, as formalised here, measured over this library, by an optimistic LP relaxation*,
  nothing beats Oler.
- It is `numerical`. The LP is solved in floating point; the intended exact rational dual
  certificate was never produced (README §5.2).
- The structural reason — the "collapse proposition" the report gestures at — **was never
  written**. So this is a measurement that the family collapses, not a proof that it must
  (README §5.1).

## Recorded so it is not re-tread

Hales-style local scoring on the Delaunay triangulation, telescoped by Euler's formula, was tried
here with the score freed pointwise, and it returns Oler. Anyone proposing a variant should first
say what their family contains that this one did not, and should re-use
`experiments/packing-r4-delaunay/framework.py`'s exact configuration library and its four
construction-time self-checks rather than rebuilding them.
