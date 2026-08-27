# Square Peg #113: noncollapse lemmas and a chord-arc stress test

Status: `sketch` overall.  The polygonal stress test and its `C=13` estimate
were independently checked by the helper in issue #113, comment 5438047359.
The strengthened chord-arc area lemma and its Greene--Lobb corollary were also
independently checked.  A later primary-source audit kills any new-class
interpretation: Asano--Ike prove the rectangular peg problem for every
rectifiable Jordan curve, hence in particular for every chord-arc curve.

This note distinguishes two statements which must not be conflated:

1. a chosen sequence of inscribed squares on approximating curves need not
   remain nondegenerate; and
2. a curve has no inscribed square.

Only the first statement is addressed by the counterexample below.  Nothing
here is a counterexample to the Square Peg Problem.

## Graceful-sector configuration space and the collision boundary

Fix an oriented embedding `gamma : S^1 -> R^2`.  Write the compact cyclic-gap
space as

```text
K = {(t,a1,a2,a3,a4) : ai >= 0 and a1+a2+a3+a4 = 1},
```

where the four parameters are `t`, `t+a1`, `t+a1+a2`, and
`t+a1+a2+a3`, modulo one.  Its interior is the cyclically ordered
configuration space.  This is the **graceful/cyclic sector**: it requires the
four vertices to occur in square order along the curve.  The classical Square
Peg Problem does not require curve order, so this sector is sufficient for a
classical square but does not exhaust all classical square configurations.
For `pi = gamma(ti)`, one exact four-scalar square test is

```text
p1+p3-p2-p4 = 0,                         (two scalars)
(p2-p1) dot (p3-p2) = 0,
|p2-p1|^2 - |p3-p2|^2 = 0.
```

The first equation gives a parallelogram; the last two make its adjacent
edges perpendicular and equal.  A nonzero solution is therefore an ordered
graceful ordered square, and hence also a square in the classical sense.

Suppose compatibly oriented parametrizations `gamma_n` converge uniformly to
an embedding `gamma`, and `gamma_n` has ordered squares with side at least
`sigma > 0`.  Compactness of `K` gives a convergent subsequence of their gap
coordinates, and uniform convergence makes the square equations pass to the
limit.  The limit cannot lie on a face `ai=0`: that face identifies an
adjacent pair, so one square side is zero; equality of the four sides then
collapses every image vertex.  Continuity and injectivity of the limiting
embedding identify this with the deepest total-collision corner.  The side
bound excludes it.  Hence the limiting zero lies in the interior and is a
positive cyclic square.

This statement uses uniform convergence of specified, orientation-compatible
parametrizations.  Hausdorff convergence of images supplies neither those
parametrizations nor cyclic-order control.  It also assumes that the limit is
an embedding; injectivity is not closed under uniform convergence.

## A strict local-curvature lower bound (known-class infrastructure)

Let `gamma` be a rectifiable Jordan curve of length `L`.  Use the standard
shorter-subarc definition of `C`-chord-arc:

```text
length(shorter arc from x to y) <= C |x-y|.
```

Assume every subarc of length at most `rho` has total curvature strictly less
than `pi`.  Then every cyclically inscribed square has side

```text
s >= rho/(3C).
```

Indeed, at most one of the four consecutive curve arcs between the square
vertices has length greater than `L/2`.  Each of the other three is the
shorter endpoint arc and has length at most `Cs`.  Their union is a contiguous
arc through all four vertices and has length at most `3Cs`.  Total curvature
of a curve arc dominates the total turning of every polygonal chain inscribed
in it.  The open three-edge chain through four cyclic square vertices has two
right-angle turns, hence total turning `pi`.  Therefore `3Cs < rho` would
contradict the strict local hypothesis.

For the scale-normalized hypothesis `rho = lambda L`, use `L >= 2 diam(gamma)`
to obtain

```text
s / diam(gamma) >= 2 lambda/(3C).
```

This is not a new curve class.  It lies inside the finite-total-curvature
without-cusps mechanism of Cantarella--Denne--McCleary: their Lemma 6 is the
turning obstruction, Definition 7 and Lemmas 8--9 give positive pi-distance,
Proposition 10 transfers it to approximants, and Theorem 11 proves the
inscription theorem.

## Exact chord-arc family with collapsing selected squares

For `0 < e <= 1/4`, let `Gamma_e` be the orthogonal polygon with cyclic
vertices

```text
(-1,0), (0,0), (0,e), (e,e), (e,0), (1,0), (1,-1), (-1,-1).
```

It is the boundary of the simply connected orthogonal region

```text
([-1,1] x [-1,0]) union ([0,e] x [0,e]),
```

so it is a Jordan curve.  Its four consecutive vertices

```text
A=(0,0), B=(0,e), C=(e,e), D=(e,0)
```

are an exact square of side `e`.

### Uniform chord-arc constant

The perimeter is `6+2e <= 13/2`.  For boundary points `x,y` with
`|x-y| >= 1/4`, the shorter boundary arc has length at most half the perimeter,
so

```text
d_Gamma(x,y) <= 13/4 <= 13 |x-y|.
```

Suppose instead that `|x-y| < 1/4`.  Nonadjacent macroscopic edges of the
`2`-by-`1` rectangle are then unavailable.  The remaining finite cases have a
boundary route of length at most `3|x-y|`:

- on the same edge the ratio is one;
- on adjacent perpendicular edges, the route is the sum of two perpendicular
  legs and is at most `sqrt(2)|x-y|`;
- for the two vertical bump legs, the route through the bump top is at most
  `3e`, while their horizontal separation is `e`;
- between the left and right baseline pieces, the route through the bump is
  the horizontal chord plus `2e`, and that chord is at least `e`;
- between the bump top and a baseline piece, the route has two perpendicular
  coordinate contributions and ratio at most `sqrt(2)`;
- from one bump leg to the baseline beyond the opposite leg, the route is at
  most `3e+a`, while the horizontal separation is `e+a`, giving ratio at most
  three.

Reflections cover the symmetric cases.  Thus every `Gamma_e` is
`13`-chord-arc.  The constant is deliberately crude but independent of `e`.

### Explicit oriented Frechet convergence

Let `Gamma_0` be the boundary of `[-1,1] x [-1,0]`, with matching orientation.
Match every point outside the bump identically.  Parametrize the bump arc
`A-B-C-D` by its arclength `u in [0,3e]` and match it monotonically to

```text
(u/3, 0) in [A,D].
```

This extends to an orientation-preserving homeomorphism of the parameter
circles.  On each of the three bump edges, the matched points are at distance
at most

```text
(sqrt(10)/3) e.
```

Consequently

```text
d_F(Gamma_e,Gamma_0) <= (sqrt(10)/3)e -> 0.
```

The exact squares `A,B,C,D` nevertheless have sides `e -> 0`.  Therefore a
uniform chord-arc constant, even together with oriented Frechet convergence,
does not force an arbitrarily selected sequence of genuine inscribed squares
to stay away from the collision stratum.  This does not exclude other,
macroscopic squares on the same curves.

## Area-versus-diameter route

Here chord-arc and bounded turning give distinct estimates.  Let `D` be the
diameter and choose diameter endpoints `A=(0,0)` and `B=(D,0)` after a rigid
motion.  Removing `A,B` splits the curve into two open arcs from `A` to `B`.
For almost every `x in (0,D)`, the one-dimensional area formula makes the
relevant vertical slice finite.  Count only boundary intersections at which
membership in the Jordan domain changes; isolated tangencies count twice, or
equivalently zero modulo two.  Each `A`--`B` arc has odd mod-two intersection
with the separating vertical line.  The transition intersections pair as
endpoints of the open vertical slices of the Jordan domain.  At least one such
pair has one endpoint on each `A`--`B` arc: otherwise every pair would use two
endpoints of the same arc, making both odd intersection counts even.  Call a
cross-arc pair `p,q`.

The two boundary routes from `p` to `q`, respectively through `A` and through
`B`, have lengths at least `2x` and `2(D-x)`.  Under the shorter-subarc
`C`-chord-arc hypothesis,

```text
|p-q| >= 2 min(x,D-x)/C.
```

The vertical interior slice containing `p,q` has at least this length.
Fubini's theorem first gives the scale-invariant estimate

```text
Area(Omega) >= integral_0^D 2 min(x,D-x)/C dx = D^2/(2C).       (1)
```

There is a sharper estimate.  Write the cross-arc slice endpoints as
`p=(x,y1)`, `q=(x,y2)` and `delta=|y2-y1|`.  Suppose first that `x<=D/2`.
The boundary route through `A` has length at least

```text
|p-A|+|q-A|.
```

The route through `B` has at least the analogous sum with horizontal
coordinate `D-x`; since `D-x>=x`, it has the same lower bound.  Therefore the
shorter boundary route is at least `|p-A|+|q-A|`.  For fixed vertical gap
`delta`, convexity (or reflection about the horizontal axis) gives

```text
|p-A|+|q-A| >= 2 sqrt(x^2+delta^2/4).
```

Chord-arc now implies

```text
C delta >= 2 sqrt(x^2+delta^2/4),
delta >= 2x/sqrt(C^2-1).
```

The argument through `B` is symmetric for `x>=D/2`.  Integrating the
cross-arc interior component yields

```text
Area(Omega) >= D^2/(2 sqrt(C^2-1)).                             (2)
```

Greene--Lobb's Theorem A gives an interval `I subset (0,pi)` of rectangle
diagonal angles of length at least `Area/Rad^2`, where `Rad=D/2`.  If this
length is greater than `pi/2`, the interval must contain `pi/2`, producing a
square.  Equivalently, the enclosed area must exceed `pi D^2/8`.  Bound (2)
reaches that criterion in the strict range

```text
C < sqrt(1+16/pi^2) = 1.619... .                               (3)
```

This range is nonempty for closed rectifiable chord-arc curves.  Indeed, the
universal lower bound is only `C>=pi/2=1.570...`.  To prove it, parametrize by
arclength on `[0,L)` and translate so that the mean of `gamma` is zero.
Wirtinger's inequality gives

```text
integral |gamma|^2 <= (L/(2pi))^2 integral |gamma'|^2
                       = L^3/(4pi^2),
integral_0^L |gamma(s+L/2)-gamma(s)|^2 ds <= L^3/pi^2.
```

Some antipodal-arclength pair consequently has chord at most `L/pi`.  Its
shorter boundary arc has length `L/2`, so chord-arc forces `C>=pi/2`.

The slice-parity and metric estimates in (2)--(3) were independently checked.
They give a quantitative Greene--Lobb route in the narrow nonvacuous interval
`[pi/2, sqrt(1+16/pi^2))`, but **not a new square-existence class**.  The
decisive later reference is Asano--Ike, *The rectifiable rectangular peg
problem*, arXiv:2412.21057v3 (2026), Corollaries 1.2 and 5.9: every rectifiable
Jordan curve inscribes a rectangle of every prescribed diagonal angle
`theta in (0,pi)`.  A chord-arc curve is rectifiable by definition, so that
result already supplies a square without the restriction (3).  What remains
potentially useful here is only the elementary quantitative area bound (2)
and the resulting explicit lower bound on the Greene--Lobb angle interval.

For the standard `C`-bounded-turning condition

```text
min(diameter(arc_1),diameter(arc_2)) <= C |p-q|,
```

both cross-arc routes contain `A` or `B`, so their diameters are at least
`x` and `D-x`.  This gives only

```text
|p-q| >= min(x,D-x)/C,
Area(Omega) >= D^2/(4C).
```

Greene--Lobb would then require `C < 2/pi`, whereas every bounded-turning
constant satisfies `C >= 1` because an arc diameter is at least its endpoint
chord.  This bounded-turning range is empty.  Thus the sharpened chord-arc
argument does not transfer to bounded turning: it essentially uses lower
bounds on the *lengths* of both boundary routes, not merely their diameters.

## Why a parametrization modulus still does not select a macroscopic square

The following literature comparison remains `sketch` pending the required
Claude or human review.  Asano--Ike's actual ambient class is broader than the
two corollaries above.
Their Theorem 1.1 assumes smooth embeddings `c_n -> c` in parametrized `C^0`
and locally uniform convergence of primitives of `(c_n o e)^*lambda`; they
call this a continuous Legendrian lift.  Proposition 5.8 verifies it for
rectifiable curves, while Proposition 5.11 verifies it for locally monotone
curves.  Consequently a proposed nonrectifiable bounded-turning theorem must
first be checked against this primitive-convergence condition, not only
against Corollaries 5.9 and 5.12.

Uniform bounded turning, even supplemented by an ordinary bi-Hoelder or
quasisymmetric parametrization modulus, does not by itself keep an
*arbitrarily selected* square macroscopic.  Four cyclic square parameters may
lie in a parameter interval tending to a point, while the complementary arc
carries the entire macroscopic curve.  This is precisely the combinatorial
pattern in the polygonal bump above.  The bump can be inserted at scale
`epsilon` into a fixed bounded-turning or quasicircle model and assigned a
parameter interval at the corresponding modulus scale; its four marked
vertices still form an exact `epsilon`-square.  Similarities preserve the
local metric ratios, so this localization is not ruled out by a uniform
scale-independent distortion function.

Thus the next viable lemma cannot say that every square delivered on each
approximant is uniformly nondegenerate under bounded turning plus a standard
parameter modulus.  It must instead retain the parity/cobordism class of the
square family and prove that this class cannot be supported entirely near the
total-collision face, or impose a genuinely local geometric obstruction (such
as the finite-total-curvature `pi`-turning radius above).  At Hoelder exponent
above `1/2`, there is an additional caveat: uniform `alpha`-Hoelder bounds and
uniform convergence imply convergence in every lower `beta`-Hoelder norm;
choosing `1/2 < beta < alpha`, continuity of the Young integral should then
give convergence of the Liouville primitives.  This Young-integral bridge is
itself only a `sketch` here and must be checked against the exact smoothing
and periodic-primitive normalization in Asano--Ike.  The genuinely uncovered
regime to audit is therefore at or below the critical exponent and outside
their continuous-Legendrian-lift class.
