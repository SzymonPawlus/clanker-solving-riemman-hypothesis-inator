# Rational-arc compact-domain audit

**Status:** exact witness and compact-domain certificate; no area lower bound.

**Issue:** #140. Producer/search issue: #137.

This attack was derived independently after PR #139 was frozen. It does not
read or adapt the producer's optimizer or checker logic.

## Exact witness

In traversal order, let

```text
P0 = (0,0)
P1 = (1/3,0)
P2 = (32/75,8/25)
P3 = (91/625,312/625).
```

The three edge vectors are

```text
P1-P0 = (1/3,0),
P2-P1 = (7/75,8/25) = (1/3)(7/25,24/25),
P3-P2 = (1/3)(-527/625,336/625).
```

Their squared norms are `1/9`, because
`7^2+24^2=25^2` and `527^2+336^2=625^2`. Each edge
therefore has positive length `1/3`, and the traversal length is exactly one.
There is no closing edge. The witness is an ordinary polygonal arc, hence a
continuous rectifiable unit worm.

## Compact counterexample domain

Pin the forced unit segment at `E=(0,0), F=(1,0)`. Let `K` be the convex hull
of a simultaneous placement of the segment, side-`1/2` equilateral triangle,
side-`1/3` square, and the rational arc.

For any direction, the equilateral triangle has width at least its altitude
`sqrt(3)/4`. If `A,B` realize the diameter `d` of `K`, choose two triangle
vertices whose projection on the line perpendicular to `AB` realizes the
triangle's width in that direction. The four-point height inequality gives

```text
area(K) >= d * sqrt(3) / 8.
```

Thus a counterexample to `area(K) >= T` must satisfy
`d < 8T/sqrt(3)`. Since `E` belongs to `K`, every selected anchor vertex of
the other three witnesses has Euclidean distance at most `d` from `E`, and
hence both coordinates lie in `[-D,D]` for any rational
`D > 8T/sqrt(3)`. Squaring is safe for positive values, so the checker proves
the outward condition exactly as `3*D^2 > 64*T^2`.

The square's own quarter-turn symmetry restricts its angle to `[0,90]`, and
the equilateral triangle's third-turn symmetry restricts its angle to
`[0,120]`. A global half-turn about the fixed segment's midpoint preserves the
unlabelled segment and shifts the asymmetric arc angle by 180 degrees, so it
restricts that angle to `[0,180]`. This does not break the translation box:
after the half-turn the coordinate origin is the other segment endpoint, and
every anchor is still within diameter `d` of that endpoint. Endpoints are
duplicated representations but leave no gap. No reflection quotient is taken.
This matches the repository's orientation-preserving convention and is
essential for the asymmetric new arc. Reversing its traversal does not reflect
its image and supplies no further angular reduction.

The resulting closed box has nine variables:

```text
triangle: tx, ty, theta
square:   tx, ty, theta
arc:      tx, ty, theta.
```

The strict counterexample domain is contained in this closed box, including
when a hypothetical configuration approaches the target from below.

## Machine-readable boundary certificate

Replay:

```sh
python3 problems/moser-convex-worm/attacks/rational-arc-domain-audit/check_domain.py \
  problems/moser-convex-worm/attacks/rational-arc-domain-audit/domain.json
python3 -m unittest discover \
  -s problems/moser-convex-worm/attacks/rational-arc-domain-audit \
  -p 'test_*.py' -v
```

The checker recomputes all rational edge lengths, the exact outward diameter
inequality, and the complete variable ledger. It rejects a global claim,
reflection quotient, inward diameter bound, missing pose coordinate, an
unproved angular quotient, altered pinned segment, unknown field, duplicate
JSON key, or noncanonical rational.

## Hull-combinatorics-independent leaf predicate

`check_fan_leaf.py` demonstrates a contained-fan predicate. A leaf chooses
placed witness vertices and a finite family of nonoverlapping oriented
triangles. The checker recomputes every selected point box from witness-local
coordinates and the pose box, interval-evaluates each determinant, requires a
strictly positive lower endpoint, and sums half those lower endpoints. The
triangles lie in the convex hull of their selected vertices, hence in the full
joint hull, regardless of which points are actual hull vertices or how the
true hull combinatorics change across the box.

The fixture is nontrivial in both translation coordinates: with the arc angle
fixed at zero, `tx in [-1/10,1/10]` and `ty in [0,1/100]`, the triangle from
the pinned segment and arc endpoint `P3` has certified area at least
`(312/625)/2 = 156/625 = 0.2496`, clearing `0.232239`. Controls reject a
vertical interval crossing the base line, a positive orientation with
insufficient area, any midpoint-hull hint, and a global-coverage label.

This fixture exercises a two-dimensional slice, not the trigonometric
nine-dimensional implementation still required. A generic leaf must derive
rotated point boxes with outward sine/cosine enclosures and either prove fan
interiors disjoint or use a single contained polygon with a certified cyclic
order; summing overlapping triangles would be unsound.

## Subdivision feasibility

Uniform subdivision is infeasible. Even 16 bins per variable produces
`16^9 = 68,719,476,736` leaves. Translation resolution `0.01` on the current
width-`2D` boxes gives about 215 bins in each of six translation variables;
one-degree angular bins after the exact symmetry reductions give 120, 90, and
180 bins. Their product exceeds `10^20` leaves. The fan predicate must
therefore be combined with adaptive splitting, width/support leaves, symmetry
canonicalization, and reuse of certificates over large boxes.

The exact rotational gauges above reduce angular volume by a factor 24 from
three naive `[0,360]` intervals. No safe continuous translation gauge remains
after pinning the segment: translating or rotating an individual remaining
witness changes the optimization, while global Euclidean freedom is already
spent. The diameter lemma bounds anchors but does not identify a canonical
contact. Any further translation reduction needs a proved containment or
minimal-contact lemma, not a numerical observation that an optimum touches a
particular hull edge.

Acceptance certifies only the witness and compact search domain. It says
nothing about the numerical minimum near `0.23645` and supplies no branch tree
or sound area-pruning leaves. A global result still requires exhaustive
coverage of this nine-dimensional box with independently verified outward
rigid transforms, containment polygons/support bounds, and target-clearing
area lower endpoints.
