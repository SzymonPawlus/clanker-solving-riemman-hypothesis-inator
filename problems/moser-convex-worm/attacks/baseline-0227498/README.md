# Reconstruction of the `0.227498` baseline

**Status:** sketch. The published theorem is `cited`, but this independent
reconstruction is not yet an assumable result. It replaces the defective
\(\mathcal K_2\) reduction and strip cases by a global rectangle-width lemma;
that replacement and the exact trigonometric audit still need cross-review.

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

For completeness, if \(E,F,U,V\) are four points, then

\[
 \operatorname{area}(\operatorname{conv}\{E,F,U,V\})
 \geq\frac12|EF|h_{EF}(UV). \tag{H4}
\]

Indeed, use signed distances to the line \(EF\). If \(U,V\) are on opposite
sides, the two triangles on base \(EF\) have disjoint interiors and their
heights add to \(h_{EF}(UV)\). If they are on the same side, the larger height
is at least the difference of the two heights, which is
\(h_{EF}(UV)\). This exhausts the cases and proves (H4).

Apply (H4) to the square diagonal \(AC\), and then to the triangle sides
\(PQ\) and \(PR\). This gives the translation-independent bounds

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
this reduction does not depend on the later problematic decimal cutoffs. The
exact verifier checks the three endpoint inequalities used here; monotonicity
of sine on the displayed subintervals completes the domain reduction.

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
\(R\) is left of \(x=1\). The next section replaces this entire case split by
a global argument, so \(\mathcal K_2\) is not actually needed for (1).

## Global repair of Proposition 2

Here is an elementary rectangle-width lemma. It is also the substance of a
more general proposition in Khandhawit--Pagonakis--Sriswasdi, *Lower Bound for
Convex Hull Area and Universal Cover Problems*, arXiv:1101.5638v1 (2011), but
the proof below is independent and shorter for the rectangular case.

**Rectangle-width lemma.** Let a compact convex body \(K\) of finite area
contain a rectangle \(R\) whose side lengths parallel to orthogonal unit
vectors \(e_1,e_2\) are respectively \(a,b\). If \(w_1,w_2\) are the widths
of \(K\) in the directions \(e_1,e_2\), then

\[
  2\operatorname{area}(K)\geq b w_1+a w_2. \tag{RW}
\]

Translate so that the origin belongs to \(R\), hence to \(K\). Convexity gives

\[
 K+tR\subseteq K+tK=(1+t)K\qquad(t\geq0).
\]

Adding a segment of length \(s\) in direction \(e_1\) to a compact convex
body adds exactly \(s\) times its width in direction \(e_2\) to its area. This
follows directly by integrating horizontal slice lengths: every nonempty slice
is an interval and its length increases by \(s\). Adding the two orthogonal
sides of \(tR\) successively gives

\[
 \operatorname{area}(K+tR)
 =\operatorname{area}(K)+t(a w_2+b w_1)+t^2ab.
\]

On the other hand,

\[
 \operatorname{area}(K+tR)
 \leq(1+t)^2\operatorname{area}(K).
\]

Subtract \(\operatorname{area}(K)\), divide by \(t>0\), and let \(t\) tend to
zero. This proves (RW).

Now take \(K=\mathcal C(X)\), and take \(R\) to be the square, with
\(a=b=1/3\). From the source vertex convention, the directed square sides
\(AB\) and \(BC\) have angles \(\alpha+135^\circ\) and
\(\alpha+225^\circ\), respectively. Hence the width normal to \(BC\) supplied
by the horizontal unit segment is

\[
 h_{BC}(EF)=|\sin(\alpha+45^\circ)|
 =\cos(\alpha-45^\circ).
\]

The chord from the triangle vertex at angle \(\beta\) to the vertex at
\(\beta+240^\circ\) has length \(1/2\) and directed angle
\(\beta+210^\circ\). Therefore the orthogonal width supplied by \(PR\) is

\[
 h_{AB}(PR)=\frac12|\sin(\beta-\alpha+75^\circ)|
 =\frac12\cos(\alpha-\beta+15^\circ).
\]

The absolute-value identities reduce to the positive cosines only after using
\((\alpha,\beta)\in D\).

Substitution in (RW) gives

\[
 \operatorname{area}(K)\geq\frac16\left(
 \cos(\alpha-45^\circ)+
 \frac12\cos(\alpha-\beta+15^\circ)\right)=f(\alpha,\beta).
\]

This proves (1) for **every** translation of the three objects. It removes the
source's \(\mathcal K_2\) reduction, all four strip cases, and especially the
unsupported inference \(x_R\leq1\) from the load-bearing path.

Together with the height bounds, the global inequality (1) reduces the theorem
directly to the two-variable inequality

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

## Audit of the now-non-load-bearing positional reduction

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

Item 1 is a genuine gap in the source proof as printed. The prose definition
of "distance between any point ... and \(\mathcal L\)" is ambiguous. Its proof
instead assumes a point \(p\) more than one unit from an endpoint, replaces
\(EF\) by the radial unit segment from that endpoint toward \(p\), and notes
only that the new hull is contained in the old hull. This does not by itself
show that the replacement lies in all of \(\mathcal K_2\), nor that the
containment is strict. Proposition 2 later uses item 1 to infer that a vertex
\(R\) lies left of \(x=1\). For a concrete failure of the printed inference,
place a triangle vertex at \(p=(2,0)\). Then \(F=(1,0)\) already lies on
\([E,p]\), so the old segment is redundant in
\(\operatorname{conv}(E\cup\mathcal S\cup\mathcal T)\), and the proposed
radial unit segment from \(E\) toward \(p\) is exactly the original \(EF\).
The claimed new configuration is identical, not strictly smaller. This does
not refute the existence of some minimum satisfying the lens condition, but it
does refute the argument offered for it.

The global rectangle-width proof above makes this defect non-load-bearing for
Theorem 1.

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
| RW | Rectangle-width lemma | convexity and slice integration | sketch; independent proof above |
| F | Global inequality (1) | N, RW | sketch; no positional reduction |
| T | Corrected rational trigonometric contradiction | F, H | sketch with exact replay artifact |
| LB | Every placement has area at least `0.227498` | W, N, H, D, RW, F, T | cited as a published theorem; reconstruction remains sketch pending review |

The original \(K\) node has been removed from the load-bearing DAG. The new
rectangle-width proof and exact trigonometric repair still require independent
review before the reconstruction can be promoted.

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
