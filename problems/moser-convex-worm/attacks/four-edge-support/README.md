# Exact rational four-edge support witness

**Status:** `sketch`; significant verification-critical candidate frozen for
independent review.  The exact checker proves the support-envelope statement
below.  Its interpretation as a universal-cover area bound depends on the
finite-polygon mixed-area bridge, whose independent review remains pending.

## Result

Take the four open-chain edge directions with rational half-angle parameters

```text
-4/5, -1/72, 1/72, 4/5
```

and respective positive rational lengths

```text
163/480, 77/480, 77/480, 163/480.
```

For a half-angle parameter `t`, the unit direction is

\[
 ((1-t^2)/(1+t^2),\;2t/(1+t^2)).
\]

Thus all four directions are rational unit vectors and the four traversed
lengths sum exactly to one.  The unlisted closing edge has length

\[
 R={11984563\over25510200};
\]

it is part of the convex hull boundary but **not** part of the worm.  Exact
cross products put the four traversed edges and closing edge in strict
counterclockwise order, so all five traversal vertices are hull vertices.

Conditional on the standard finite-polygon mixed-area bridge, the resulting
support envelope has the rigorous global floor

\[
 \boxed{47/200=0.235}>0.2346746732.
\]

This exceeds the equal-turn three-edge family optimum quoted in Issue #178.
No stronger decimal is claimed; exploratory floating-point evaluation places
the actual envelope floor near `0.2350683`.

## Balanced allocations

Number the four traversed hull edges `0,1,2,3` and the closing edge `4`.
The checker independently enumerates every maximal balanced allocation using
three edge directions.  Exactly four occur:

```text
(0,2,4), (0,3,4), (1,2,4), (1,3,4).
```

For each allocation `x`, exact arithmetic verifies

\[
 0\le x_i\le \ell_i,\qquad \sum_i x_i n_i=0.
\]

Allocate `x` to the half-side equilateral-triangle witness and the residual
balanced load to the unit-segment witness.  Including the all-segment
allocation gives five legal pointwise lower bounds.  Translation drops out
separately from each balanced support sum.

For the triangle part, the checker minimizes over the complete direct-motion
orientation period.  On every cell between a loaded normal crossing a
triangle edge normal, the support sum is a positive sinusoid and hence
concave.  Its minimum is therefore at a cell boundary.  All such boundaries
are enumerated exactly in `Q(sqrt(3))`; the four exact minima are printed by
the replay.

## Complete angular proof

Pin the unoriented unit segment and let `phi` be the new hull orientation.
The paired rational directions and paired allocations make the support
formula algebraically invariant under `phi -> pi-phi`; this does not introduce
a reflected worm placement.  It therefore suffices to take
`0 <= phi <= pi/2` and set `u=tan(phi/2)`, so `0 <= u <= 1`.

Every residual segment projection becomes

\[
 {\left|s(1-u^2)-2cu\right|\over1+u^2}
\]

with rational `c,s`.  Outward rational interval arithmetic recursively
subdivides `[0,1]`.  Each accepted leaf proves at least one of the five bounds
is at least `47/200`.  The deterministic run produces 70 closed leaves with
exactly matching endpoints; hence there are no angular gaps.

## Replay

Python 3.11 or later is sufficient; no third-party package is used and
assertions must remain enabled.

```text
python3 problems/moser-convex-worm/attacks/four-edge-support/verify_four_edge.py
python3 -m unittest discover \
  -s problems/moser-convex-worm/attacks/four-edge-support -p 'test_*.py'
```

The `search_*.py` and `refine_*.py` files are exploratory floating-point
candidate locators only.  They do not participate in the accepted predicate.
