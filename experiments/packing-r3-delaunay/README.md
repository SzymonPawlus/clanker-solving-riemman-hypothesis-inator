# Approach AB — Euler-localised Delaunay scoring: INCOMPLETE, NO RESULTS

**Status: `sketch` scaffolding only. This directory contains NO result, and nothing in it
has been validated. Do not cite it, do not build on it, do not treat its code as working.**

## What this is

Round-3 proposal AB (`../../problems/circle-packing-equilateral-triangle/attacks/r3-approaches/README.md`)
asked whether a Hales-style *localised* score on the Delaunay triangulation, telescoped by
Euler's formula, can beat Oler's inequality — Oler being the linear member of that family, and
exactly tight at triangular `n` but slack by about half a circle at `n = 16..18`.

The worker assigned to it was **terminated by an account session limit before producing any
result**. It had written `geom.py` and `lp.py` and had not yet reached its own validation gate.

## What was NOT done — the important part

The gate that mattered was never run: **the framework must first reproduce Oler's
`d(n) >= sqrt(8n+1) - 3` when the score is the linear/area one.** Until that control passes,
this code is not known to compute the right thing at all, and any number it emits is
meaningless. Nobody checked the telescoping identity, the boundary and corner terms, or the
LP setup.

The code is preserved rather than deleted so a future worker does not restart from nothing.
Treat it as a sketch of an intended structure, not as a partial result.

## If you pick this up

1. Re-derive the telescoping identity yourself, including boundary edges and container corners.
2. Recover Oler as the linear member. **If you cannot, the framework is wrong — fix that before
   anything else.**
3. Only then run the LP gate at `n = 16, 17, 18` against Oler's `8.3578`.
4. Kill-criterion: if the LP optimum at `n = 16` does not strictly exceed `sqrt(129) - 3`, the
   family is no stronger than its linear member. Report the trend over two or three
   discretisation refinements and stop.

No reproduce command is offered, because there is nothing here that reproduces a result.
