# Independent finite-polygon mixed-area bridge red-team

Issue #174.  This directory was derived without consulting the Issue #170 Lean
implementation or adapting code from PR #168.

## Frozen derivation

Let `P` be a convex polygon contained in a convex polygon `K`.  Traverse `P`
counterclockwise.  For each directed edge `e` let `d_e` be its displacement,
`l_e=|d_e|`, and let `n_e=rot_cw(d_e)/l_e` be its outward unit normal.  The exact
polygonal Minkowski expansion is

```
area(K + t P)
  = area(K) + t sum_e l_e h_K(n_e) + t^2 area(P).       (1)
```

One way to prove (1) is to refine the edge directions of `K` and `P` to their
common normal fan.  In the boundary of `K+tP`, parallel edge vectors add.  The
shoelace formula is quadratic in these vectors; its constant and quadratic
parts are `area(K)` and `area(P)`, while collecting the cross terms against
the support line of each edge of `P` gives the displayed sum.  Equivalently,
add the translated edge strips one direction at a time; edge `e` contributes
`t l_e h_K(n_e)` to first order and the overlaps comprise the quadratic term.

Containment gives, for every `t >= 0`,

```
K + tP  subset  K + tK = (1+t)K.
```

Compare areas, substitute (1), subtract `area(K)`, divide by positive `t`, and
let `t` tend to zero.  This proves

```
(1/2) sum_e l_e h_K(n_e) <= area(K).                    (2)
```

The factor `1/2` is necessary: `P=K` makes the unhalved sum equal to
`2 area(K)`.

Translation causes no hidden origin assumption.  Translating `K` by `a` adds
`a . rot_cw(d_e)` to the edge term, and the total addition vanishes because
`sum_e d_e=0`.  Translating `P` leaves all edge vectors unchanged.

For a nondegenerate segment `[a,b]`, use its two oriented boundary edges
`d=b-a` and `-d`.  The sum in (1) is

```
h_K(rot_cw(d)) + h_K(-rot_cw(d)),
```

namely segment length times the perpendicular width of `K`.  This is also the
linear coefficient obtained by extruding `K` by the segment, so the same
containment argument proves (2).  A point follows by a zero limit and has sum
zero.

## Exact checker

`mixed_area.py` uses `fractions.Fraction`.  It avoids unit normals and square
roots using

```
l_e h_K(n_e) = h_K(rot_cw(d_e)).
```

It deliberately rejects clockwise, duplicate, and collinear boundary data
rather than silently changing certificate semantics.  Tests cover equality,
the missing `1/2`, segments, two independent translations, noncontainment,
wrong normals, a missing edge, and 1,000 seeded exact rational instances.

Run:

```
python -m unittest discover -s experiments/moser-mixed-area-redteam -v
```
