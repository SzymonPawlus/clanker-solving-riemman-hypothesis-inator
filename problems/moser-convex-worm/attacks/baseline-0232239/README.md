# Source audit of the `0.232239` benchmark

**Status:** sketch. The published decimal is `cited`; this independent audit
does not yet make its proof assumable. The primary proof is analytic, with a
two-angle four-case estimate, but it gives no directed provenance for the
broadworm breadth or its tight decimal cutoffs.

## Pinned source

T. Khandhawit, D. Pagonakis, and S. Sriswasdi, *Lower Bound for Convex Hull
Area and Universal Cover Problems*, arXiv:1101.5638v1, submitted 28 January
2011; later published in *International Journal of Computational Geometry and
Applications* **23** (2013), 197--212, DOI
`10.1142/S0218195913500076`.

The arXiv v1 archive has SHA-256
`03518f85d1d19fc6b0888c60b05831dc130afbf10218913723c6764d2cd71ccb`.
Its sole TeX source, `main_v3.tex`, has SHA-256
`1ca573fc5ad6e2f1f633fbea288f00492d7006c42b7703d29cbb68204820bc8a`.
The result used here is Proposition 3.5 (`result`, source lines 338--371),
combined with the four witness inequalities immediately before it. The
abstract and conclusion of Section 3 state the universal-cover bound
`0.232239`; there is no separately numbered universal-cover theorem.

## Exact witness family

The proof requires every convex universal cover to contain congruent copies
of four unit arcs:

1. A unit segment \(\mathcal L\).
2. A two-edge V-shaped arc \(\mathcal T\), consisting of two sides of an
   equilateral triangle of side \(1/2\). Its length is exactly
   \(1/2+1/2=1\), and its convex hull is the triangle.
3. A three-edge U-shaped arc \(\mathcal R\) whose convex hull is a
   \(1/2\)-by-\(1/4\) rectangle. The unit traversal must use short--long--short
   sides, of lengths \(1/4+1/2+1/4=1\). The paper says
   \(AB=CD=1/2\), \(BC=AD=1/4\), so the vertex order \(A,B,C,D\) is the
   rectangle's boundary order, **not** the worm traversal order: traversing
   \(AB,BC,CD\) would have length \(5/4\).
4. Schaer's unit broadworm \(\mathcal B\), a nonpolygonal rectifiable unit arc
   of constant minimum width \(b_0\), cited to Schaer (1968) and
   Schaer--Wetzel (1972). The paper records only \(b_0\) "approximately
   0.4389"; other literature commonly prints approximately `0.438925` or
   `0.43893`. A source-level directed lower bound for the precision needed
   below remains to be reconstructed.

The Khandhawit--Pagonakis--Sriswasdi paper gives no vertices, arc order, or
exact formula for \(\mathcal B\); those data cannot be validated from that
paper alone. The standard Zalgaller--Schaer description starts with a
unit-width symmetric path made from four line segments and two circular arcs.
Later surveys report the exact parameters

\[
 \phi=\arcsin\!\left({1\over6}+{4\over3}
   \sin\!\left({1\over3}\arcsin {17\over64}\right)\right),
 \qquad
 \psi=\arctan\!\left({1\over2}\sec\phi\right),
\]

and unit-width length

\[
 \ell_0=2\left({\pi\over2}-\phi-2\psi+	an\phi+	an\psi\right)
 \approx2.27829164144.
\]

Scaling this finite concatenation by \(1/\ell_0\) makes its length exactly one
and its minimum width \(b_0=1/\ell_0\approx0.43892536926\). A finite union of
line segments and circular arcs is rectifiable, so this gives the required
unit rectifiable witness conditional on the cited geometric construction and
constant-width proof. The exact formula numerically supports
\(b_0>0.438925\), but pinning it to Schaer's inaccessible 1968 report or the
1972 Schaer--Wetzel paper, with a directed analytic evaluation, remains a
literature-verification task rather than something supplied by the 2011 paper.

Convexity forces each witness's convex hull once the arc is placed. The V and
U witnesses are reflection-symmetric as unlabelled arcs, while the broadworm's
reflection convention still needs to be checked directly against its primary
construction before using orientation-reversing gauge symmetries.

## Parameters and proof architecture

Pin \(\mathcal L\) horizontally. Let

\[
 \theta_0=\arctan(1/2),\qquad
 \theta_0\leq\alpha\leq\theta_0+\pi/2,
 \qquad \pi/3\leq\beta\leq2\pi/3.
\]

Here \(\alpha\) is the angle of the rectangle diagonal and \(\beta\) locates a
triangle vertex. Section 3.1 obtains this angular rectangle using a half-turn
and reflection. The centers remain arbitrary, but all ensuing lower bounds are
translation-independent. Because reflection is orientation-reversing, its use
for the broadworm-free \((\mathcal L,\mathcal R,\mathcal T)\) terms is harmless;
the broadworm term depends only on its width and does not reflect a placed
broadworm.

Section 2 first proves an analytic rectangle-and-four-points inequality. It is
then specialized to define

\[
\begin{aligned}
 p(\alpha)&={\sqrt5\over8}\sin\alpha,\\
 q(\beta)&={1\over4}\max\{\sin(\beta-\pi/6),\sin(\beta+\pi/6)\},\\
 f(\alpha,\beta)&={1\over8}\{\cos(\alpha-\theta_0)
   +\sin(\beta-\alpha+\theta_0+\pi/6)\},\\
 g(\alpha)&={1\over4}\{\tfrac12\cos(\alpha-\theta_0)+b_0\}.
\end{aligned}
\]

Every placement has area at least
\(F=\max\{p,q,f,g\}\). Proposition 3.5 divides the compact angular rectangle
into outer \(\alpha\)-tails handled by \(p,g\), outer \(\beta\)-tails handled by
\(q\), and a central rectangle handled by \(f\). This is a finite analytic case
split, not a spatial grid, optimizer, interval subdivision, or contact
conjecture. The claim that \(f\)'s central minimum occurs at a corner can be
repaired transparently: both sine arguments lie in \((0,\pi)\), so \(f\) is
concave on the rectangle and its minimum is attained at an extreme point.

There is a separate hypothesis gap in the paper's use of its Section 2
proposition. Proposition 2.3 assumes both selected transverse heights exceed
the corresponding rectangle side lengths. Section 3 applies it without
checking those assumptions, and they are false on parts of the full angular
domain (for example \(h_{BC}(EF)=\cos(\alpha-\theta_0)=0\) at
\(\alpha=\theta_0+\pi/2\)). The resulting simplified inequality is nevertheless
globally valid: for any convex \(K\) containing an \(a\)-by-\(b\) rectangle,
the rectangle-width inequality

\[
 2\operatorname{area}(K)\geq b\,w_1+a\,w_2
\]

follows from \(K+tR\subseteq(1+t)K\) and the first-order Minkowski area
formula. Substituting widths supplied by the segment and triangle/broadworm
gives exactly the paper's formulas for \(f\) and \(g\), without the missing
height assumptions. This is an independent analytic repair and remains
`sketch` pending cross-review.

## Directed-decimal audit

The printed case boundaries overlap, so they cover the angular domain:

\[
\begin{aligned}
 a_-&=0.663720972, &a_+&=0.980693573,\\
 d_-&=0.1443850668,&&
 \end{aligned}
\]

with slightly interior tail cutoffs `0.663720973`, `0.980693572`, and
`0.1443850667`. Direct high-precision evaluation reproduces the four printed
central-corner values; the tight corner is approximately
`0.23223921015175`, safely above the target at the displayed precision.

Two tail assertions, however, are rounded in the unsafe direction.

- At \(\alpha=0.663720973\), the inequality \(g(\alpha)>0.232239\) requires
  \[
    b_0>4(0.232239)-\tfrac12\cos(\alpha-\theta_0)
       \approx0.4389299999864.
  \]
  With \(b_0\approx0.4389253\), the left side is only about
  `0.23223782505`. The paper's claimed `0.232239000003` corresponds to using
  `0.43893`, an upward-rounded breadth, as if it were a lower bound.
- At \(\beta=\pi/2-0.1443850667\), the relevant \(q\)-value is approximately
  `0.23223899998396`, not the claimed value greater than
  `0.232239000012`. The exact transition offset is approximately
  `0.1443850668733`, so the printed tail cutoff is inward-rounded.

These observations refute the two displayed tail inequalities as written, but
they do **not** refute Proposition 3.5. Both defective slivers overlap the
central \(f\)-rectangle, whose weakest printed corner has roughly
\(2.1\times10^{-7}\) margin. Numerically, moving the lower \(\alpha\) edge to
about `0.6636737` and the \(\beta\) half-width to about `0.1443850669` still
leaves the tight \(f\)-corner near `0.23223921015`. A rigorous repair therefore
looks plausible, conditional on a cited outward lower bound for \(b_0\), but it
has not yet been certified here.

One explicit repaired cover uses the rational cutoffs

\[
 \alpha_-=0.66367,\qquad \alpha_+=0.980694,
 \qquad d=0.1443851,
\]

and the conditional literature input \(b_0\geq0.438925\). Exact-rational
Machin/Taylor intervals then give lower margins over `0.232239` of about
`1.61e-8` for \(g(\alpha_-)\), `6.67e-8` for \(p(\alpha_+)\), and `3.07e-9`
for \(q(\pi/2\pm d)\). The smallest of the four central \(f\)-corner margins
is about `1.91e-7`. Replay these terminal inequalities with

```text
python3 problems/moser-convex-worm/attacks/baseline-0232239/verify_repaired_cases.py
```

This proves the union-of-inequalities coverage **conditional** on the stated
broadworm lower bound and the analytic geometric predicates. It does not
establish \(b_0\geq0.438925\), nor does it independently check Section 2.
For the tails, \(g\) decreases up to \(\alpha_-\), while \(q\) moves away from
its central minimum and \(p\)'s concavity makes its minimum on the upper tail
occur at an endpoint (the other endpoint gives \(p=1/4\)). On the core, both
sine arguments lie in \((0,\pi)\), so joint concavity reduces the minimum to
the four checked corners. Closed tail/core endpoints overlap, leaving no gaps.

## Dependency and current verdict

| Node | Claim | Status in this audit |
|---|---|---|
| W | all four listed objects are valid unit arcs | sketch; broadworm source pending |
| R4 | the U-worm forces the stated \(1/2\)-by-\(1/4\) rectangle | sketch; traversal clarified |
| B | \(b_0\) has a sufficiently precise directed lower bound | cited only approximately; blocking exact replay |
| P2 | Section 2 rectangle/four-point inequality | cited, but Section 3 omits its hypotheses |
| RW | global rectangle-width replacement | sketch; repairs the omitted P2 hypotheses |
| A | formulas \(p,q,f,g\) lower-bound every placement | sketch, depends on RW and B |
| C | finite angular case cover and concavity | sketch; printed tail predicates partly refuted |
| LB | universal convex-cover area is at least `0.232239` | cited; reconstruction not yet verified |

The benchmark is based on a global analytic proof architecture, not a
computational search and not a contact-conjectural reduction. Its present
reconstruction bottlenecks are the exact primary-source value of \(b_0\),
directed repair of the two tail cutoffs, and independent review of the Section
2 rectangle inequality. Until those are supplied, `0.232239` remains a cited
publication claim rather than an independently verified campaign baseline.
