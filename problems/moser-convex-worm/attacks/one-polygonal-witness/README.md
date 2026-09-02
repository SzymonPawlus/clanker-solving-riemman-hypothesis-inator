# One additional polygonal witness

**Status:** first candidate `refuted`; search continues with a new family.

## Idea

Add one explicit unit-length polygonal arc to the segment, half-side
equilateral triangle, and one-third-side three-edge square witness family of
Khandhawit--Sriswasdi. Search for a family whose globally minimal simultaneous
convex-hull area is strictly larger than the independently reconstructed
baseline.

## Gate and kill criteria

Work begins with exploratory numerics, but certification waits for Issue #136.
Abandon a proposed witness family if any of these holds:

- it is congruent to, or weaker than, a known source witness;
- a placement with hull area at most the certified baseline is found;
- its apparent gain disappears under independent global search;
- the branch structure cannot be covered by a rigorous interval certificate
  at the agreed resource bound.

Failed explicit witnesses and their best placements should be recorded here so
they are not retried unchanged.

## Checkpoint 0: coarse rational-zigzag screen

The first explicit candidate has vertices

`(0,0), (1/4,0), (2/5,1/5), (1/5,7/20), (-1/20,7/20)`.

Its four edge vectors have lengths exactly `1/4`, so it is a unit worm. The
deterministic exploratory script `explore_zigzag.py` ran three seeds with and
without this witness. The best three-witness control was approximately
`0.234676`, worse than the source's numerical placement near `0.227590`.
Four-witness runs returned approximately `0.253873`, `0.254502`, and
`0.262990`.

These numbers are **not evidence for a lower bound**: the control failure shows
that the coarse differential-evolution implementation has not found the known
basin. The checkpoint only validates the exact witness length and exposes an
optimizer deficiency. Next action is to reproduce the source control placement
before screening or killing the zigzag.

The paper's printed rounded parameters convert to this script's gauge with
control hull area approximately `0.227624`; its figure coordinates (which use
scale 10 and segment endpoints `(-5,0),(5,0)`) independently give approximately
`0.227591`. The script now seeds this basin explicitly. These agreements test
the objective and coordinate conventions, not global optimality.

After adding local descent, seed 1 produced a joint placement of all four
witnesses with numerical hull area `0.2276655451`. The separate
`certify_zigzag_kill.py` rounds translations and rational half-angle rotation
parameters, works exactly in `Q(sqrt(3))`, proves all witness vertices lie in a
five-vertex convex polygon, and certifies its area is approximately
`0.22766564457 < 0.232239`. Its smallest exact containment determinant has
margin about `6.77e-7`.

Therefore this zigzag cannot improve the current published lower bound. This
is an explicit upper placement for the finite witness family, not a statement
about the universal-cover optimum. The next candidate must be structurally
different.

The certificate uses floating-point values only to generate rational
half-angle and translation candidates. All accepted predicates are then exact
in `Q(sqrt(3))`; it raises explicit exceptions on failure, so `python -O`
cannot remove checks. It also verifies worm edge lengths, exact rotation norm,
hull indices and turns, containment, area sign, and the rational threshold,
and prints exact rational certificate fields plus a final `PASS`. The audited
run used Python 3.14.6; the exploratory script used NumPy 2.5.1.

## Checkpoint 1: exact rational constant-turn candidate

A broader deterministic screen tested equal-edge constant-turn arcs,
alternating zigzags, and fixed-grid turn sequences with three through eight
edges. The initial rankings were not trustworthy: for example, the exact
three-edge 60-degree-turn arc initially appeared at area `0.249978`, but
blockwise descent found a simultaneous placement at approximately
`0.2275928024`. This is a useful optimizer regression case, not a lower bound.

The strongest surviving simple candidate replaces the 75-degree screen point
by nearby rational unit directions. Its traversal-order vertices are

`(0,0), (1/3,0), (32/75,8/25), (91/625,312/625)`.

The successive edge directions before scaling by `1/3` are
`(1,0)`, `(7/25,24/25)`, and `(-527/625,336/625)`. Their squared norms are all
exactly one, so the three edges have length exactly `1/3` and the arc has
total length exactly one. No closing edge is included.

`explore_constant_turn.py` challenges a pinned numerical basin with
deterministic coordinate, placement-block, and coupled moves. A longer
development run reached area approximately `0.2341114908`; the shorter
replay's three seeds remain near that basin. This clears `0.232239` only as a
**numerical candidate**. It is not a proof that this is the simultaneous
placement minimum, and it is not an area lower bound.

Reproduce with Python 3.14.6 and NumPy 2.5.1:

```text
python problems/moser-convex-worm/attacks/one-polygonal-witness/explore_constant_turn.py
```

### Candidate compact domain and certification route

Pin the unit segment at `(0,0),(1,0)`. The triangle, square, and new worm then
have placement variables `(x_i,y_i,theta_i)`, giving nine remaining degrees
of freedom with `theta_i in [0,2*pi]`. There is a direct compactness reduction
for a threshold test. Every containing hull has width at least `sqrt(3)/4` in
every direction because it contains the side-`1/2` equilateral triangle. If
its diameter is `D`, the diameter segment and the two perpendicular support
points give area at least `D*sqrt(3)/8`. Thus any hypothetical hull of area
less than `T` has `D < 8*T/sqrt(3)`. Since `(0,0)` belongs to the hull, each
placed first vertex may be restricted to the square `[-D,D]^2`. At the record
threshold `T=0.232239`, this gives `D < 1.072666` numerically. This derivation
is presently a **sketch**, not an assumable reduction. A certificate may use
the rational bound `D < 1073/1000`: exactly,
`(8*232239/1000000)^2 < 3*(1073/1000)^2`.

More explicitly, choose diameter endpoints `a,b` and coordinates in which
they lie at perpendicular height zero. Perpendicular support points have
heights `h_plus>=0` and `h_minus<=0`. The two triangles with common base
`ab` have disjoint interiors, lie in the convex hull, and have total area
`D*(h_plus-h_minus)/2`. Their height difference is that directional width,
which is at least the minimum width `sqrt(3)/4` of the contained equilateral
triangle. This also covers the case where the diameter is a supporting chord,
when one height is zero. Pinning the ordered segment endpoints uses only a
global translation and rotation, not a reflection.

A checker need not interval-evaluate trigonometric functions. Split each
rotation into two rational half-angle charts. For `epsilon in {+1,-1}` and
`t in [-1,1]`, use

`c = epsilon*(1-t^2)/(1+t^2), s = epsilon*2*t/(1+t^2)`.

The two charts cover the full rotation circle (with overlap at their
boundaries), so the three rotations give eight discrete chart combinations
and nine rational interval variables. The only algebraic constant left is
the triangle's exact `sqrt(3)/4` altitude. A sound implementation must give
`t^2` its range-aware interval `[0,max(t_lo^2,t_hi^2)]` when the box straddles
zero; ordinary dependency-blind interval multiplication would spuriously let
`1+t^2` contain zero.

For chart coverage, if a rotation has `c>=0`, take `epsilon=+1` and
`t=s/(1+c)`; if `c<=0`, apply the same construction to `(-c,-s)` and take
`epsilon=-1`. In either case `|t|<=1`, and direct substitution recovers
`(c,s)`. Thus no orientation or reflection degree of freedom is omitted.

At each leaf the checker may select an anchor `p0`, an ordered list
`p1,...,pk`, and a rational direction `u`. It must certify both
`dot(u,pj-p0)>0` for every `j` and
`det(pj-p0,p(j+1)-p0)>0` for every consecutive pair. All rays then lie in one
open half-plane and occur in strict angular order, so the fan triangles have
disjoint interiors and lie in the full convex hull. The sum of their
outward-rounded determinant lower endpoints, divided by two, is therefore a
sound hull-area lower bound. Requiring only same-sign local polygon turns is
not enough: a star polygon can pass that test while self-intersecting. All
endpoint comparisons should convert the binary64 endpoint to its exact
rational value before comparison with rational `T`. Midpoint hull cycles
provide candidate fans, but their order must be interval-certified; merely
evaluating the midpoint hull is unsound.

There is a serious feasibility warning. Near the best pose, the full numerical
hull has eight vertices and nearly collinear active turns (the smallest turn
determinant is about `1.9e-11`). Dropping fragile vertices gives the robust
four-vertex subpolygon with indices `[segment0, segment1, square1, worm2]`,
area about `0.2339397335`, and smallest turn determinant about `0.0235427`.
A prototype natural-interval evaluation of this fixed fan on a box of
half-width `0.001` in all nine half-angle/translation variables gave only
`0.2310025`, already below the target; half-width `0.002` gave `0.2280657`.
Thus naive uniform subdivision would require roughly thousandths
near this basin and is hopeless in nine dimensions. Adaptive multiple-cycle
cuts, centered/Taylor forms, or a further analytic placement reduction are
needed before a complete branch tree is computationally credible. These
figures are an engineering estimate, not a certificate. A complete branch
tree and an independent checker are still absent.

An active-support experiment enumerated the midpoint hull's cyclic vertex
subpolygons and projected zero onto the convex hull of their numerical area
gradients. At the earlier `0.2341368734` pose, 24 subpolygons individually
cleared the target, but their minimum-norm convex gradient combination still
had norm about `0.0613`. Following that common descent direction and repeating
local simplex descent produced the lower `0.2341114908` placement recorded in
the replay seed. Thus the active-support calculation was useful as an
optimizer adversary, but it did not yield translation cancellation or a
stationary weighted inequality. No analytic dimension reduction resulted.

## Checkpoint 2: nearby exact turn family

The weak support at the first rational candidate is almost collinear with the
pinned segment. A scan of nearby Pythagorean turn directions found a stronger
numerical candidate with half-angle parameter `10/13`. Its turn cosine and
sine are exactly `69/269,260/269`, and its traversal vertices are

`(0,0), (1/3,0), (338/807,260/807),
(9361/72361,105820/217083)`.

The three exact squared edge lengths are again `1/9`. A 240-member,
2500-generation differential-evolution challenge found a second basin; local
simplex descent there reached approximately `0.2350390775`. This is a stronger
**numerical candidate**, not a certified lower bound or a global minimum.
`explore_nearby_turn.py` preserves that basin and independently challenges it
with three deterministic blockwise seeds:

```text
python problems/moser-convex-worm/attacks/one-polygonal-witness/explore_nearby_turn.py
```

The active hull cycle at this pose is
`[segment0,square2,segment1,square0,worm2]`, with numerical consecutive turn
determinants `0.0011845, 0.1744761, 0.1474239, 0.0268770, 0.1953662`.
Removing the triangle leaves the area unchanged. Reinitializing its translation
uniformly in `[-1.073,1.073]^2` and its angle uniformly on the full circle,
then optimizing only those three variables, placed it inside this fixed hull
in 19 of 20 deterministic trials; the remaining run missed by about `1.64e-6`.
This is a basin stress test, not a containment proof.

For this five-cycle, write the square placement origin as `S`, its rotation
cosine/sine as `c_s,s_s`, and the placed second non-origin worm vertex as `W`.
The shoelace formula simplifies symbolically to

`A5 = (-(c_s+s_s)/3 + det(S,W))/2`.

This identity is suitable for direct interval evaluation once the fan order is
certified. A natural half-angle interval probe on a nine-variable box of
half-width `0.001` gave lower endpoint `0.2317735`, versus `0.2310025` for the
prior candidate's robust fan; linear interpolation puts the target crossing
near half-width `0.00086` rather than `0.00058`. Conditioning therefore
improves by roughly 48 percent, but naive uniform nine-dimensional subdivision
remains infeasible. These are numerical engineering estimates, not certificate
leaves.

### Exact local fan box

**Status:** `sketch` (producer-checked exact arithmetic; independent geometric
checker/review pending).

`certify_nearby_local_box.py` uses exact `Fraction` interval endpoints and the
two-chart rational rotation formula; no floating-point operation participates
in an accepted predicate. The triangle is first relocated, without changing
the five-cycle, to the numerically more interior pose
`(0.7482384613885471,0.43318521035405194,4.190525142978863)`. In the
`epsilon=-1` chart its half-angle center is the rational decimal
`0.5785074745087493`.

On the common radius `1/100000` box in all nine translation/half-angle
variables, the checker exactly certifies:

- all rays from `segment0` lie in the strict `x>0` half-plane;
- the three consecutive fan determinants have strictly positive lower bounds;
- the fan area has exact rational lower endpoint approximately
  `0.2350064194 > 0.232239`;
- all three relocated triangle vertices are strictly inside the five-cycle.

The local fan proof enlarges to radius `1/1700`, where its rational area lower
endpoint is approximately `0.2331180896`. Radius `1/1650` fails first at the
fan angular-order guard, not at the target comparison. This is only a local
box certificate and has no global force.

The fixed-cycle containment diagnostic cannot certify every omitted vertex on
any positive-radius box: `square1` and `worm0,worm1,worm3` are numerically
collinear with different cycle edges at the center, so their exact interval
margins straddle zero even at radius `1/1000000000`. This is a documented
failure of a fixed combinatorial-hull certificate, not a failure of the fan
area bound, which uses only its listed vertices. Reproduce the requested box
and the enlarged box with:

```text
python problems/moser-convex-worm/attacks/one-polygonal-witness/certify_nearby_local_box.py --summary
python problems/moser-convex-worm/attacks/one-polygonal-witness/certify_nearby_local_box.py --radius 1/1700 --summary
```

## Checkpoint 3: complementary support portfolio

**Status:** analytic reduction `sketch`; searches `numerical`; two local boxes
producer-certified `sketch`. No global coverage claim.

The tempting unconditional elimination of the triangle is false as a proof
strategy. Eight six-variable searches over only the pinned segment, square,
and new worm repeatedly found area about `0.22160134`. A representative square
pose is `(0.589274839,-0.0355518989,0.0863435664)` and worm pose is
`(0.999998650,0.0000002809,1.88963719)`. Depending on tiny collinearities, its
reported hull cycles range from `[segment0,square0,square1,segment1,square2,
square3]` to cycles additionally containing `worm0` or `worm2`. Thus a
segment-square-worm fan cannot cover the whole domain. Restoring and optimizing
the triangle while holding that pose fixed raised the best numerical area to
about `0.24279616`.

There is nevertheless a useful complementary decomposition. For a fixed
square placement `s`, let

- `m_T(s)` be the minimum segment-square-triangle hull area over triangle
  placements;
- `m_W(s)` be the minimum segment-square-worm hull area over new-worm
  placements.

Every four-witness hull contains both triple hulls, hence its area is at least
`max(m_T(s),m_W(s))`. Consequently the global lower-bound task would follow
from a certified three-dimensional outer bound

`min_s max(m_T(s),m_W(s)) > T`.

With quantifiers exposed, let `S,T,W` denote the complete compact placement
domains for the square, triangle, and new worm after pinning the segment, and
let `F(s,t,w)` be the full hull area. Define `G_T(s,t)` and `G_W(s,w)` as the
two triple-hull areas and use infima (which are minima on these compact
domains):

`m_T(s)=inf_{t in T} G_T(s,t)`,
`m_W(s)=inf_{w in W} G_W(s,w)`.

For every `(s,t,w)`, monotonicity under adding points gives

`F(s,t,w) >= G_T(s,t) >= m_T(s)` and
`F(s,t,w) >= G_W(s,w) >= m_W(s)`.

Therefore

`inf_{s,t,w} F(s,t,w) >= inf_s max(m_T(s),m_W(s))`.

For a square box `B`, a valid projected brancher must compute
`L_T(B) <= inf_{s in B,t in T} G_T(s,t)` and independently
`L_W(B) <= inf_{s in B,w in W} G_W(s,w)`. The outer box is pruned only if
`max(L_T(B),L_W(B)) > T`. Sampling or certifying one inner optimizer
neighborhood does not define either lower envelope.

This separates the triangle and worm translations/orientations into two
independent inner problems sharing only the square. It is presently a
`sketch`, and neither inner minimum is globally certified. Numerical fixed-
square challenges illustrate the complementarity:

| square basin | `m_T(s)` numerical | `m_W(s)` numerical | maximum |
|---|---:|---:|---:|
| record-candidate square | 0.234172 | 0.235057 | 0.235057 |
| alternate full basin | 0.240406 | 0.224765 | 0.240406 |
| low three-object basin | 0.242797 | 0.221611 | 0.242797 |

The exact local checker now contains two complementary fan scenarios. The
default `nearby` five-cycle ignores triangle variables and passes through
radius `1/1700`. The `alternate` robust quadrilateral
`[segment0,segment1,square2,triangle2]` ignores all worm variables and passes
through radius `1/1500`, with lower endpoint about `0.232707397`. Its symbolic
fan area is

`A4 = (square2_y + det(square2,triangle2))/2`.

At the record-candidate square, an even cheaper `square_only` fan
`[segment0,square2,segment1,square0,square1]` eliminates both other inner
objects. It certifies a common square-variable radius `1/1750` with lower
endpoint about `0.232574465`; this is currently the most direct outer-box
prune in the portfolio.

Reproduce the second portfolio cell with:

```text
python problems/moser-convex-worm/attacks/one-polygonal-witness/certify_nearby_local_box.py --scenario alternate --radius 1/1500 --summary
python problems/moser-convex-worm/attacks/one-polygonal-witness/certify_nearby_local_box.py --scenario square_only --radius 1/1750 --summary
```

These two rational boxes form only a finite cover of two optimizer
neighborhoods. They are widely separated and leave essentially the entire
compact placement domain uncovered. A plausible global brancher should first
try a segment-square-worm fan on six variables; only its unpruned square/worm
cells should be crossed with triangle variables. Symmetrically, robust
segment-square-triangle fans prune independently of the worm. Only cells where
both projected fan portfolios fail require full nine-variable subdivision.
No branch tree implementing that hierarchical cover exists yet.

### Projected inner-tree feasibility

An exploratory projected brancher fixed the alternate square box and covered
the complete compact triangle translation/rotation domain separately in the
two rational half-angle charts. Its first version used only a leftmost-`x`
anchor and left 1,985 tiny boxes unresolved after 20,000 nodes even though
their midpoint hulls were large; the failure was an anchor artifact near
vertical support ties. Allowing eight rational support directions
`(+-1,0),(0,+-1),(+-1,+-1)` removed that defect.

At a common square-variable radius `1/1500`, the improved exploratory run
exhausted the `epsilon=+1` triangle chart in 6,107 nodes and the `epsilon=-1`
chart in 8,187 nodes, with no unresolved leaves. Fan pruning handled 2,914 and
3,967 nodes; diameter pruning handled 140 and 127. This suggests that a
projected three-dimensional inner certificate is computationally realistic.

Those prototype counts are only **numerical feasibility evidence**. It uses
binary64 initialization of decimal centers and does not serialize its branch
tree. Until every rational/algebraic input is outward-enclosed from its exact
value, target comparisons are exact-rational, and the complete tree is emitted
for independent replay, it is not a lower envelope and cannot prune an outer
box in a proof.

### Exact projected triangle tree

`certify_triangle_inner_tree.py` now implements that exact replay for the
triangle side of the alternate square box.  The square translation and
half-angle variables use the displayed finite decimals as exact rationals,
each with radius `1/1000`.  Triangle translations range over
`[1-D,D] x [-D,D]`, where `D=1073/1000`, and each of the two half-angle charts
has `t in [-1,1]`.  Thus the two roots cover every orientation and every
translation that could occur in a hull of diameter less than `D`.

Every internal node is a rational midpoint split.  Every leaf stores either
(i) a triangle vertex and pinned-segment endpoint whose squared-distance
interval lies strictly above `D^2`, or (ii) an anchor, angularly ordered ray
subsequence, and integer open-half-plane direction.  In case (ii), exact
rational interval arithmetic proves every half-plane dot product and
successive determinant positive and proves the sum of the disjoint fan
triangle areas strictly above `232239/1000000`.  The midpoint hull used while
producing the tree is only a search heuristic and is not replayed or trusted.

The serialized leaf paths are prefix-free and record the split coordinate at
every level.  Replay constructs a trie and requires every internal trie node
to have both children with the same split coordinate, so the leaf boxes form
a complete binary cover rather than a collection of successful samples.
`triangle-inner-tree.json` contains 3,703 leaves in the `epsilon=+1` chart
(170 diameter, 3,533 fan) and 4,759 in the `epsilon=-1` chart (134 diameter,
4,625 fan).  The smaller `1/1500` tree was therefore not retained.

```text
python problems/moser-convex-worm/attacks/one-polygonal-witness/certify_triangle_inner_tree.py \
  --replay problems/moser-convex-worm/attacks/one-polygonal-witness/triangle-inner-tree.json \
  --self-test
```

The self-test requires rejection of six adversarial mutations: a missing leaf,
a duplicate leaf, a prefix-overlap leaf, an inconsistent split axis, an inward
change to the recorded diameter bound, and a changed target.  The certificate
header binds both `D` and the target, so replay cannot silently apply the tree
under different proof parameters.

For common-refinement bookkeeping, the cheap single quadrilateral fan has a
separate exact boundary bracket: it passes at common radius `1/1300` with area
lower endpoint about `0.2324144214`, while at `1/1200` its exact interval area
lower bound no longer exceeds the target.  This is only a failure of that one
fan predicate.  The complete projected tree above still closes the larger
`1/1000` square box, so adjacent-cell construction should start at the latter
boundary rather than treating `1/1200` as failure of the triangle envelope.

This is still a producer-side **sketch**, not `verified:review`.  Conditional
on the compact-diameter reduction above, it supplies a complete projected
triangle lower envelope for only this one alternate square box.  It does not
cover the outer square domain, does not certify the worm-side envelope, and
does not use the unrestricted support-allocation statement under audit in
Issue #165.
