# Reconstruction of the `0.227498` baseline

**Status:** sketch. The published theorem is `cited`, but this independent
reconstruction is not yet an assumable result. In particular, the reduction to
the paper's class \(\mathcal K_2\) and the strip case analysis need an
independent geometric proof.

## Source and scope

The primary source is T. Khandhawit and S. Sriswasdi, *An Improved Lower Bound
for Moser's Worm Problem*, arXiv:math/0701391v2 (5 June 2009), Theorem 1:

> For every simultaneous placement of a unit segment, an equilateral triangle
> of side \(1/2\), and a square of side \(1/3\), the convex hull has area at
> least `0.227498`.

The exact v2 source archive contains one TeX file, bundled AMS style files, and
four EPS plots. It contains no search program, input data, dependency lockfile,
or machine-checkable certificate.

This note separates the analytic proof in Section 2 from the heuristic search
in Section 3. The grid search is not a dependency of Theorem 1.

## Why the three objects are valid witnesses

The unit segment is itself a worm of length one. Traverse two consecutive
sides of an equilateral triangle of side \(1/2\); this is an open polygonal arc
of length \(1/2+1/2=1\). Traverse three consecutive sides of a square of side
\(1/3\); this is an open polygonal arc of length
\(1/3+1/3+1/3=1\). A convex cover containing either open arc contains its
convex hull, hence the whole triangle or square. Neither unlisted closing edge
is part of the worm.

Both polygonal witnesses have reflection symmetries, so the repository's
orientation-preserving motion convention loses no placement used below.

## Coordinates and gauge

Fix the segment endpoints

\[
 E=(0,0),\qquad F=(1,0).
\]

Let the square have center \((x_1,y_1)\), circumradius \(\sqrt2/6\), and
vertices at angles
\(\alpha,\alpha+\pi/2,\alpha+\pi,\alpha+3\pi/2\). Let the triangle have
centroid \((x_2,y_2)\), circumradius \(\sqrt3/6\), and vertices at angles
\(\beta,\beta+2\pi/3,\beta+4\pi/3\). Thus a normalized placement has six
parameters

\[
 (x_1,y_1,\alpha,x_2,y_2,\beta).
\]

Square and triangle rotational symmetries initially give
\(0\leq\alpha\leq90^\circ\) and \(0\leq\beta\leq120^\circ\). Reflection of
the entire configuration across the perpendicular bisector of \(E F\), and a
half-turn about its midpoint, give the source's working angular gauge

\[
 45^\circ\leq\alpha\leq90^\circ,
 \qquad60^\circ\leq\beta\leq120^\circ.
\]

Write \(\mu(X)\) for the area of the convex hull of all three placed objects.

## Load-bearing analytic inequalities

The source proves the following translation-independent height bounds:

\[
 g(\alpha)=\frac{\sqrt2}{6}\sin\alpha\leq\mu(X),
\]

\[
 h(\beta)=\max\left\{
   \frac14\sin(\beta-30^\circ),
   \frac14\sin(\beta+30^\circ)
 \right\}\leq\mu(X).
\]

They come respectively from the square diagonal together with \(EF\), and
from two quadrilaterals formed by \(EF\) and triangle vertices.

These bounds show directly that any placement outside

\[
 D=[45^\circ,78^\circ]\times[83^\circ,97^\circ]
\]

has area greater than `0.23`. The integer-degree endpoints are conservative;
this reduction does not depend on the later problematic decimal cutoffs.

For a purported minimum in the source's reduced positional class
\(\mathcal K_2\), Proposition 2 claims

\[
 f(\alpha,\beta)=\frac16\left(
   \frac12\cos(\alpha-\beta+15^\circ)
   +\cos(\alpha-45^\circ)
 \right)\leq\mu(X). \tag{1}
\]

Its proof divides the position of \(E,F\) relative to the two strips determined
by opposite square sides. It charges disjoint exterior triangles to square
sides, using the transverse heights of \(EF\) and the triangle side \(PR\).
The difficult subcase uses the positional assertion that a triangle vertex
\(R\) is left of \(x=1\).

Assuming (1) and valid coverage by \(\mathcal K_2\), the theorem reduces to the
two-variable inequality

\[
 \max\{f(\alpha,\beta),g(\alpha),h(\beta)\}\geq
 c,\qquad c=\frac{113749}{500000}.
\]

## Directed repair of the final decimal step

The paper's printed implications

\[
 \alpha<74.838^\circ,
 \qquad84.496^\circ<\beta<95.504^\circ
\]

are rounded in the wrong directions. Numerically, the underlying thresholds
are about \(74.83845968^\circ\), \(84.49575399^\circ\), and
\(95.50424601^\circ\). Thus, for example, \(g(\alpha)<c\) does **not** imply
\(\alpha<74.838^\circ\).

Use instead the outward rational cutoffs

\[
 A=74.8385^\circ,\quad B_-=84.4957^\circ,\quad B_+=95.5043^\circ. \tag{2}
\]

Exact outward interval evaluation proves

\[
 g(A)>c,\qquad h(B_-)>c,\qquad h(B_+)>c. \tag{3}
\]

The required monotonicities on \(D\) then show that \(g(\alpha)<c\) and
\(h(\beta)<c\) imply

\[
 \alpha<A,\qquad B_-<\beta<B_+.
\]

Because \(B_-+B_+=180^\circ\) and \(A<75^\circ\), the endpoint \(B_+\)
has the largest absolute value of \(\alpha-\beta+15^\circ\). Hence

\[
 \cos(\alpha-\beta+15^\circ)
 \geq\cos(\alpha-(B_+-15^\circ)).
\]

Set

\[
 q(\alpha)=\frac16\left(
 \frac12\cos(\alpha-80.5043^\circ)+
 \cos(\alpha-45^\circ)\right).
\]

Both cosine arguments have magnitude below \(36^\circ\) on \([45^\circ,A]\),
so \(q''<0\) there. A concave function on an interval is bounded below by the
smaller endpoint value. Exact outward intervals give

\[
 q(45^\circ)>c,\qquad q(A)>c. \tag{4}
\]

Equations (3)--(4) repair the final contradiction. Replay with

```text
python3 problems/moser-convex-worm/attacks/baseline-0227498/verify_trig.py
```

The verifier uses only Python's standard-library exact `Fraction` arithmetic.
It derives an interval for \(\pi\) from Machin's formula, encloses trigonometric
values between consecutive alternating Taylor sums, checks a rational
enclosure of \(\sqrt2\) by squaring, and accepts only exact rational
comparisons. Binary floating point is used solely to print compact diagnostics.

## The positional reduction requiring further proof

The paper defines \(\mathcal K_2\) by:

1. each point of the square and triangle is within the stated unit-distance
   restriction relative to the segment;
2. both polygons lie in \(-0.46\leq y\leq0.46\);
3. both polygons intersect the segment.

Item 2 is safe for any putative configuration of area below `0.23`: a point
with \(|y|>0.46\), together with \(E,F\), already spans a triangle of area
greater than `0.23`.

For item 3, translating a polygon toward the segment until first contact can
produce a hull contained in the old hull. This establishes existence of a
no-larger contact placement, not the paper's stronger wording that every
non-contact placement "is not minimal." A complete proof must explicitly show
the containment during translation and apply the operation to a chosen global
minimum (or directly to a hypothetical area-\(<c\) configuration).

Item 1 is the main unresolved gap in this reconstruction. The prose definition
of "distance between any point ... and \(\mathcal L\)" is ambiguous. Its proof
instead assumes a point \(p\) more than one unit from an endpoint, replaces
\(EF\) by the radial unit segment from that endpoint toward \(p\), and notes
only that the new hull is contained in the old hull. This does not by itself
show that the replacement lies in all of \(\mathcal K_2\), nor that the
containment is strict. Proposition 2 later uses item 1 to infer that a vertex
\(R\) lies left of \(x=1\). This dependency must be repaired before the
analytic reconstruction is `verified:review`.

The source's compactness argument also needs cleanup. It invokes inscribed
circles and bounded center disks, but prints a dimensionally suspicious term
`1/6^4` and is imprecise about whether disk subscripts denote radii or squared
radii. Coercivity of convex-hull area as either polygon center escapes to
infinity should provide a clean replacement.

## Dependency DAG

| Node | Claim | Depends on | Current status |
|---|---|---|---|
| W | The three open polygonal arcs have length one and force the three convex objects | definitions | sketch |
| N | Six-variable rigid normalization and angular symmetry coverage | W | sketch |
| C | The area objective attains a global minimum | N, coercivity | sketch; source proof needs repair |
| H | Height bounds \(g,h\) | N | cited; independently readable |
| D | Low-area angles lie in \(D\) | H | sketch |
| K | A relevant minimum may be chosen in \(\mathcal K_2\) | C | sketch; unresolved item 1 |
| F | Strip/case inequality (1) | D, K | cited; independent geometry incomplete |
| T | Corrected rational trigonometric contradiction | F, H | sketch with exact replay artifact |
| LB | Every placement has area at least `0.227498` | W--T | cited as a published theorem; reconstruction remains sketch |

The weakest dependencies \(K\) and \(F\) cap the reconstruction. The exact
trigonometric repair does not promote the combined result by itself.

## Source errors and transcription issues

- The fourth square vertex prints
  \(\sin(\alpha+\pi/2)\); it must be \(\sin(\alpha+3\pi/2)\).
- Reflection across \(x=1/2\) prints the new center as
  \((1/2-x_1,y_1)\); it must be \((1-x_1,y_1)\).
- A half-turn is said to "fix a square." It preserves its orientation class
  modulo square symmetry but generally moves its center.
- The compactness formula contains the suspicious `1/6^4` term noted above.
- The strict phrase "is not minimal" is not justified by non-strict hull
  containment in the \(\mathcal K_2\) reductions.
- The final decimal angular cutoffs are inward-rounded, as repaired above.
- The search conjecture says \(\mathcal L,\mathcal T,\mathcal T\), evidently
  intending \(\mathcal L,\mathcal T,\mathcal S\).

## The separate, non-load-bearing grid proposition

For spatial grid width \(d_1\) and angular width \(d_2\), the paper bounds a
vertex perturbation by

\[
 \delta=\frac{d_1}{\sqrt2}+\frac{\sin(d_2/4)}{\sqrt3}
\]

and cites

\[
 |\mu(X')-\mu(X)|\leq\delta\,\operatorname{peri}(\mathcal C(X))+\pi\delta^2.
\]

After reporting the approximate perimeter cap `3.46364`, it claims the linear
error `2.44916 d1 + 0.49993 d2` **"by ignoring second order terms."** Dropping
the nonnegative \(\pi\delta^2\) term cannot prove an upper error bound. The
source also gives no directed-rounding provenance for `3.46364` or the derived
coefficients. Therefore Proposition 3, as printed, is refuted as a rigorous
error estimate. It is irrelevant to Theorem 1, which precedes it.

The final reported heuristic placement has area `0.22758966937711944` and
parameters

```text
(x1, y1, alpha, x2, y2, beta)
=(0.6605, 0.1878, 1.3077, 0.741, 0.1274, 1.6373)
```

with angles in radians. It comes from a fine two-angle search constrained by
an unproved conjecture that the triangle's rightmost vertex is \(F\) and the
topmost square and triangle vertices coincide. It is numerical evidence only.
