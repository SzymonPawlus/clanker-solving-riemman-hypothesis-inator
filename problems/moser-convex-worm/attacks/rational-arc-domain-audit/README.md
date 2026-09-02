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

`check_five_cycle.py` implements that predicate independently from the nine
decimal pose centres and half-angle charts. It reconstructs the corner-anchored
square and second rational arc, computes every transformed selected point by
exact rational interval arithmetic, and does not trust the supplied cycle
label. For every directed cycle edge it requires **every other selected cycle
vertex** to lie strictly to the left. This stronger all-edge guard proves both
simplicity and convex cyclic order before an outward shoelace lower bound is
accepted.

On the `1e-5` box it independently obtains area lower
`0.23500641941252148...`, matching the separately reported value. Radius
`1/1700` still certifies `0.23311808957579225...`; radius `1/1650` is rejected
because a convex-order determinant crosses zero. A changed cycle label and a
global scope are adversarially rejected.

Omitted witness vertices, including ones collinear with a selected cycle edge
at the centre, do not invalidate this **lower** bound. The joint hull contains
each selected vertex and therefore contains their certified convex polygon;
an omitted point can enlarge that hull but cannot remove polygon area. It
would be unsound to claim the selected cycle equals the full hull, or to use
the same collinear guard for an upper bound, but neither claim is made here.
Triangle containment is likewise unnecessary for this leaf's area inequality;
the triangle pose remains in the nine-variable box ledger only so the leaf
domain is explicit.

## Common-outer-cell envelope schema

There is a sound dimension reduction, but it is pointwise rather than a license
to combine two unrelated global minima.  Fix a square pose `s`, and write

```text
m_T(s) = inf_t area hull(segment, square(s), triangle(t)),
m_W(s) = inf_w area hull(segment, square(s), worm(w)).
```

For every joint placement `(s,t,w)`, the full hull contains both subfamily
hulls.  Therefore its area is at least
`max(m_T(s),m_W(s))`, and taking infima gives

```text
inf_(s,t,w) full_area >= inf_s max(m_T(s),m_W(s)).
```

The triangle and worm minimizers need not be correlated: the two containment
bounds hold simultaneously for every `(t,w)`.  Compactness is needed only to
replace `inf` by `min`.  The diameter argument above supplies the same closed
translation boxes for all three moving witnesses, and the exact rotational
gauges supply closed angle intervals, so the finite polygonal objectives are
continuous on compact pose boxes.

`check_composed_envelope.py` enforces the certificate consequence.  Each outer
square cell must occur identically in a complete triangle inner tree and a
complete worm inner tree.  Bounds must be uniform over that whole outer cell;
trees using different outer partitions must first be common-refined.  The
checker rejects a maximum of separately optimized global minima, a missing
inner pose cell, a nonuniform bound, an incorrect compact root, and any global
scope escalation.

The initial `composed_envelope.json` is deliberately local but sound.  It uses
one small cell around the recorded square scenario,

```text
square tx in [3029/5000,303/500],
square ty in [-13/10000,-11/10000],
square theta in [2507/100,2509/100] degrees.
```

For every triangle pose and every worm pose, the corresponding subfamily hull
contains the four selected points `segment.P0, segment.P1, square.P2,
square.P3`.  Outward rational trigonometric intervals prove these points remain
in strict convex order throughout the outer cell and give area lower endpoint
`0.2333312123...`.  The fixture conservatively records

```text
L_T = 2333/10000, L_W = 2333/10000,
max(L_T,L_W) = 2333/10000 > 232239/1000000.
```

Each one-leaf inner tree covers its entire compact pose root, so unresolved
triangle-inner and worm-inner volume is zero on this outer cell.  This is a
genuine uniform prune, although both bounds come from the shared
segment-square subfamily rather than from triangle- or worm-specific geometry.
The translation anchor is the opposite square corner after reducing the
recorded `epsilon=-1` chart angle modulo 180 degrees; retaining the old anchor
would describe a different placed square.  Its outer cell volume is
`1/1250000000`
out of root volume
`103555883601/250000000`, a covered fraction
`1/517779418005` (about `1.9313e-10%`).  The exact uncovered outer volume is
`129444854501/312500000`.  Broader progress requires less dependency-prone
interval formulas, subdivision of a larger outer neighborhood, and eventually
triangle- or worm-specific leaves; the local five-cycle worm pose still cannot
be reused as though it minimized over all worm placements.

## Exact support-allocation polytope skeleton

The mixed-area route removes translations before an angular branch tree.  If
`P` is any one of the placed witness hulls and `P` is contained in the joint
hull `K`, its actual edge lengths and outward normals satisfy

```text
area(K) >= V(K,P) = (1/2) sum_e length_e(P) h_K(n_e(P)).
```

For every template edge, distribute its support with nonnegative allocations
whose sum is one.  The translation of moving witness `j` then has coefficient
`(1/2) sum_e length_e lambda_(e,j) n_e`; requiring that vector to vanish gives
a translation-free support lower bound.  The edge lengths here are the actual
surface measure of the contained template, not arbitrary unit weights.

The unit segment is lower-dimensional, so its template bound is proved
directly rather than hidden in a continuity assertion.  Put the segment on a
horizontal line, and let `h+` and `h-` be the greatest perpendicular distances
of `K` above and below it.  The convex hull contains the two triangles formed
by the unit base and points attaining those heights; their interiors are on
opposite sides and their total area is `(h+ + h-)/2`.  This equals the
two-atom support formula with normals `(0,1)` and `(0,-1)`.

`check_support_bfs.py` constructs the capacity and two-coordinate load matrix
for all four templates.  Gaussian elimination and sign tests are exact in
`Q(sqrt(3))`; rational templates remain in the rational subfield.  It
enumerates every distinct basic feasible allocation, reconstructs all
coordinates from the recorded canonical bases, and rechecks nonnegativity,
per-edge capacity, and all six moving-witness load equations.  The counts are

```text
segment: rank 5, 4 BFS       triangle: rank 9, 4 BFS
square:  rank 10, 16 BFS     worm:     rank 10, 16 BFS.
```

The worm gauge `[0,180]` is accepted only with the explicit orientation-
preserving half-turn about the pinned segment midpoint.  It preserves the
unlabelled segment, shifts the asymmetric worm angle by 180 degrees, and
reanchors all translations inside the already-proved diameter boxes.  A
reflection flag, shortened domain, or altered action is rejected; without this
action the checker instructs the caller to restore `[0,360]`.

`probe_support_lipschitz.py` is the first angular prototype, still
`numerical`.  At the coarse sweep's worst sampled basin
`(triangle,square,worm)=(120,0,100)` degrees, exact worm-template BFS 13 with
basis `[0,1,2,3,5,6,7,8,12,13]` has floating centre value
`0.2395757346...`.  Centred support radii give per-radian Lipschitz constants
`L_triangle=0.09622504...`, `L_square=0`, and `L_worm=0.30564264...`.
Subtracting their sum times a `0.25`-degree half-width gives
`0.2378222560...`, above the target on that one periodic angular cell.  This is
not outward interval evaluation, and the rest of the common three-angle domain
is explicitly uncovered.  A real certificate must replace the centre value
and radii by exact outward bounds and attach one exact primal basis to every
leaf of a complete common-domain tree.

`check_support_cell.py` replaces that one floating centre by an exact outward
calculation.  The selected worm BFS allocates edges 0 and 2 to the segment,
edge 1 to the triangle, and the closing edge in fractions `138/407` and
`269/407`.  After inserting the actual edge lengths, the support functional is

```text
(1/6)(h_S(n0)+h_S(n2)+(138/269)h_S(n3)+h_T(n1)+h_T(n3)).
```

Machin/Taylor rational intervals evaluate the centre at triangle angle 120 and
worm angle 100 degrees.  The exact triangle circumradius is bounded above by
`289/1000`, giving per-radian constants `L_beta=289/3000` and
`L_phi=82247/269000`; the square constant is zero.  Subtracting these constants
times the exact `pi/720` outward upper bound proves the conservative rational
lower endpoint `237/1000` on a quarter-degree-radius cell.  The triangle cell
crosses its 120-degree quotient boundary, so the certificate explicitly stores
both `[0,1/4]` and `[479/4,120]`; silently dropping either piece is rejected.

`check_support_cells.py` expands the same exact primal into a 24-cell staircase
with triangle centres from 118 through 120 degrees and worm centres from 98
through 100.5 degrees where the bound remains at least `237/1000`.  The square
angle is absent from this functional, so every accepted rectangle covers its
full `[0,90]` gauge.  Exact prefix-free overlap checks and periodic splitting
give covered angular volume `540` degree-cubed out of `1,944,000`, namely
`1/3600`; uncovered fraction `3599/3600` remains explicit and forces partial
scope.  This is rigorous local angular coverage, not yet the complete adaptive
portfolio tree suggested by the numerical sweep.

The same primal actually yields a much larger slab.  Its two triangle normals
are antipodal, so the triangle contribution is one sixth of a width and is
uniformly at least `sqrt(3)/24`, independent of the triangle angle.  The square
angle was already absent.  The remaining segment term is

```text
(1/12)(|n0.x| + |n2.x| + (138/269)|n3.x|),
```

depending only on the worm angle.  `check_support_slab.py` evaluates this term
on 119 adjacent half-degree worm cells covering `[75,269/2]`, using the exact
segment Lipschitz constant `169/807` and outward `pi` and `sqrt(3)` bounds.
Every cell proves the rational lower endpoint `2323/10000`, while the triangle
and square domains are checked as the complete `[0,120]` and `[0,90]` gauges.
Thus this single exact primal certifies a full two-angle slab occupying
`119/360` of the common angular domain.  The unresolved complement has two
worm-angle components, `[0,75]` and `[269/2,180]`, with total fraction
`241/360`; complementary template primals are still required there.

Acceptance certifies only the witness and compact search domain. It says
nothing about the numerical minimum near `0.23645` and supplies no branch tree
or sound area-pruning leaves. A global result still requires exhaustive
coverage of this nine-dimensional box with independently verified outward
rigid transforms, containment polygons/support bounds, and target-clearing
area lower endpoints.
