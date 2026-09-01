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

## Deterministic adaptive subtree probe

`probe_adaptive.py` exercises the contained-fan predicate on the full compact
`ty in [-D,D]`, `theta in [0,180]` projection for the rational arc. It derives
pi by exact alternating Machin bounds and evaluates sine/cosine with rational
Taylor intervals. Every split is an exact midpoint split; a second traversal
reconstructs the root from the children and rechecks every prune. Unresolved
depth-limit leaves remain explicit and force `global_claim: false`.

The deterministic policy compares direct `ty` width with the derivative bound
`(|P3.x|+|P3.y|)*delta_theta` and splits the larger certified source of
vertical-coordinate uncertainty. At depth 10 it reports 1,491 nodes, 492
theta splits, 253 `ty` splits, 31 fan-pruned leaves, and 715 unresolved leaves:
an acceptance rate of `31/746 = 4.16%`.

The dominant split count is angular, but the deeper bottleneck is predicate
strength: this fan can prune only placements putting `P3` more than `2*T`
above the fixed segment. Refining the other 95.8% cannot make that geometric
condition true. A full search needs a portfolio of fans or support-width
predicates involving triangle and square vertices, then selects the predicate
with the largest certified margin. Finer uniform splitting alone is not a
viable route.

`probe_portfolio.py` lifts the same experiment to four dimensions by adding
the square angle `alpha in [45,90]` and triangle angle
`beta in [60,120]`. Its independent portfolio consists of the segment-square
height bound `g`, the two segment-triangle height bounds combined as `h`, the
global square rectangle-width bound `f`, and the segment-arc fan. At every
leaf it computes all lower margins and selects the first predicate in a fixed
incremental-coverage order only when that predicate's interval lower endpoint
clears the target. No midpoint hull or combinatorial guess is an input.

At depth 10, exact replay covers 711 nodes and 356 leaves. Incremental pruning
is `square_g: 28`, `triangle_h: 28`, `rectangle_width_f: 36`, and
`arc_fan: 12`, for 104 pruned and 252 unresolved leaves: `104/356 = 29.2%`.
Splits are `alpha: 101`, `beta: 170`, `theta: 28`, and `ty: 56`.
The baseline width predicates produce most of the gain, but more than 70% of
this reduced tree remains unresolved. The next bottleneck is no longer raw
trigonometric interval width: it is the absence of predicates coupling the
arc to off-axis triangle/square vertices and the six translation variables
omitted by this probe.

`probe_mixed.py` adds the square centre's vertical translation over `[-D,D]`
while fixing its horizontal translation to zero, and adds a genuinely mixed
contained-triangle predicate using the origin, one rotated square vertex, and
rotated arc endpoint `P3`. A nontrivial box

```text
alpha in [88,90], arc theta in [130,140],
arc ty and square ty in [D-1/100,D]
```

clears the target by an exact interval determinant; the full root is rejected
as sign-uncertain. At feasible depth 7 the five-dimensional tree has 239 nodes
and volume-weighted coverage `3/16` by `f`, `7/16` by `h`, and `3/8`
unresolved. The mixed predicate adds no coarse-root prune at that depth even
though its targeted fixture passes. Introducing one translation dimension
therefore increases interval uncertainty and runtime without improving coarse
coverage; mixed fans need candidate-informed boxes or a much better selection
portfolio before more translation axes are introduced.

## Second exact rational candidate checkpoint

The later Issue #137 candidate

```text
(0,0), (1/3,0), (338/807,260/807),
(9361/72361,105820/217083)
```

also passes an independent exact length calculation. Its normalized edge
directions are

```text
(1,0), (69/269,260/269), (-62839/72361,35880/72361),
```

and `69^2+260^2=269^2` while
`62839^2+35880^2=72361^2`; all three edges therefore have length `1/3`.
The reported stable active cycle
`segment0,square2,segment1,square0,worm2` suggests a five-vertex polygon leaf,
not the current origin-square-`P3` triangle. Without the candidate placement
coordinates and an interval neighborhood, its active-box prune margin cannot
be independently compared. The sound next predicate is a checker-recomputed
five-cycle with strict interval orientation and shoelace guards; the cycle
label alone is not evidence and is never accepted as a midpoint hull order.

Acceptance certifies only the witness and compact search domain. It says
nothing about the numerical minimum near `0.23645` and supplies no branch tree
or sound area-pruning leaves. A global result still requires exhaustive
coverage of this nine-dimensional box with independently verified outward
rigid transforms, containment polygons/support bounds, and target-clearing
area lower endpoints.
