# Attack: how large a triangle is guaranteed — the extremal / quantitative question

```
regularity budget:
  Sec 2 (Lemma W), Sec 4 (Lemma L, Theorem D):  none -- arbitrary bounded subset of the
      plane; no hypothesis on J is consumed, so these hold for every Jordan curve.
  Sec 6 (Theorem C, Lemma B), Sec 7:            convex.
  Sec 4 and Sec 9.3 computations:               polygonal, with exact Q(sqrt3) arithmetic.
What breaks first if you drop convexity in Sec 6: the incircle of the interior region stops
controlling the boundary at all.  This is not a technicality -- Sec 4's witness is a
rectifiable, piecewise-linear, NON-convex Jordan curve on which m/w is arbitrarily small,
so Sec 6's conclusion is false for general Jordan curves and "convex" is load-bearing.
Sec 5's Conjecture I is the guess about what survives; it is a conjecture, not a claim.
```

- Lane: **quantitative / extremal** — idea **I6** of
  [`../ideation-round-1/README.md`](../ideation-round-1/README.md).
- Author: `claude` (Claude Opus 5), 2026-08-29, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), **written before any computation
  in this lane**. Outcomes: §10.
- Journal: [`../../../../notebook/claude/2026-08-29-iet-extremal.md`](../../../../notebook/claude/2026-08-29-iet-extremal.md).
- Problem rules consumed: [`../../RULES.md`](../../RULES.md) §1 (budget, above), §2
  (nondegeneracy — every triangle below has an explicit positive side), §3.1/§3.2/§3.3 (all
  three filters run and reported, §9), §5 (exact arithmetic — §8 says exactly which numbers are
  exact and which are float), §6 (statuses).

## Headline

**The question as the brief posed it is empty, and not only for the diameter.** For every
normalisation that is a function of the *convex hull* — diameter, width, hull perimeter, hull
area, in- or circumradius of the hull — and also for curve length and enclosed area, the
infimum of $m(J)/N(J)$ over Jordan curves is $0$. One witness, an L-shaped hexagon, kills all
of them simultaneously. The surviving formulations are (a) the **convex** question, which is
non-empty and is where the rest of this file lives, and (b) the **inradius of the interior
region**, which resisted every attempt to make it degenerate and is left as a conjecture.

## Result table

| § | Statement | Status |
|---|---|---|
| §2 | **Lemma W.** An equilateral triangle of side $s$ has minimal width exactly $\tfrac{\sqrt3}{2}s$. | `sketch` — mine, elementary |
| §2 | **Corollary U.** For any $S\subseteq\mathbb{R}^2$, every equilateral triangle with vertices in $S$ has side $\le \tfrac{2}{\sqrt3}\,w(\operatorname{conv}S)$. Hence $m(J)\le\tfrac{2}{\sqrt3}w(J)\le\tfrac{2}{\sqrt3}\operatorname{diam}(J)$. | `sketch` — mine |
| §3 | The constant $2/\sqrt3$ in Corollary U is **attained** (thin rectangle; equilateral triangle). | `sketch` + `numerical` |
| §4 | **Lemma L.** Every equilateral triangle with all vertices within $\delta$ of two perpendicular unit segments has side $\le 2(\sqrt6+\sqrt2)\,\delta$. | `sketch` — mine |
| §4 | **Theorem D (degeneracy).** $\inf_J m(J)/N(J)=0$ for every hull-continuous normalisation $N$ positive on a triangle, and for curve length and enclosed area. | `sketch` — mine; this is the **answer to the dispatched question**, in the negative |
| §4 | On the L-hexagon $J_\delta$, $\max_O$ (over sampled $O$) side $=(\sqrt6+\sqrt2)\delta$ **exactly**, for four values of $\delta$. | `numerical` — exact in $\mathbb{Q}(\sqrt3)$ |
| §6 | **Theorem C (lower bound, convex).** For every planar convex body $K$ with inradius $r$, $m(K)\ge\sqrt3\,r$. **Sharp**: equality for the disk. | `sketch` — mine; the one I would most like reviewed |
| §6 | **Lemma B.** $w\le 3r$ for planar convex bodies (Blaschke; reproved here, not cited). | `sketch` — mine |
| §6 | **Corollary.** $m(K)\ge w(K)/\sqrt3$ for convex $K$, i.e. $\mu_{\mathrm{conv}}\ge 1/\sqrt3\approx0.5774$. | `sketch` — mine |
| §7 | The disk gives $m/w=\sqrt3/2$ exactly, so $\mu_{\mathrm{conv}}\le\sqrt3/2\approx0.8660$. | `sketch` — mine, exact |
| §7 | **The disk is not extremal.** First-order perturbation is stationary exactly on harmonics $n\equiv\pm1\ (\mathrm{mod}\ 6)$; second order is negative there. | `sketch` (the first-order half) + `numerical` (the sign of the second order) |
| §7 | Constant-width body $h=1+\tfrac1{24}\cos5\theta$: $w=2$ exactly, $m\approx1.714410$, ratio $\approx0.857205$. | `numerical` — **float**, two independent estimators agreeing to $10^{-9}$ |
| §8 | Theorem T of [`../rectifiable-case/`](../rectifiable-case/) yields **no** lower bound on $m$. | `sketch` — mine, a reading of that file, not a use of it |
| §8 | "The largest equilateral triangle *contained* in a convex body is inscribed" as a route to the lower bound | **`refuted`** for fixed orientation (unit square), and abandoned in general |

**Nothing here is assumable** ([`../../../../RULES.md`](../../../../RULES.md) §3), including by
me. Every argument below is self-contained: it uses nothing from any other attack directory and
nothing from the provisional `cited`\* rows of [`../README.md`](../README.md).

---

## 1. The question, and why the normalisation had to be settled first

For a Jordan curve $J$ put

$$m(J)=\sup\{\,s>0 : \text{some equilateral triangle of side } s \text{ has all three
vertices on } J\,\}$$

(the supremum of a set of *positive* numbers only — the degenerate "triangle" $O,O,O$ is
excluded by fiat, [`../../RULES.md`](../../RULES.md) §2; every triangle exhibited below has an
explicit positive side, and every upper bound below is an upper bound on the side of a genuine
nondegenerate triangle, so nondegeneracy is never smuggled in or out).

For a normalising functional $N$, homogeneous of degree 1 under scaling, put
$\mu_N=\inf_J m(J)/N(J)$. The brief named $N=\operatorname{diam}$ and required the degeneracy
check first. That instruction was the right one: §4 shows the degeneracy is much wider than
I6 anticipated.

Throughout, $w(X)$ is the **minimal width** of $X$ — the smallest distance between two parallel
supporting lines of $\operatorname{conv}X$ — and $r(\Omega)$ the inradius of the interior
region.

## 2. The one lemma the whole upper-bound side rests on

> **Lemma W.** Let $T$ be an equilateral triangle of side $s$. Then
> $\min_{u\in S^1}\bigl(\max_{p\in T}\langle p,u\rangle-\min_{p\in T}\langle p,u\rangle\bigr)
> =\tfrac{\sqrt3}{2}s$, the altitude.

*Proof.* Put the centre at the origin, so the vertices are $R\,u(\varphi+120°k)$, $k=0,1,2$,
with $R=s/\sqrt3$. For a unit vector $u(\psi)$ the extent is
$R\bigl(\max_k\cos(\varphi-\psi+120°k)-\min_k\cos(\varphi-\psi+120°k)\bigr)$. Write
$\alpha=\varphi-\psi$ and let $E(\alpha)=\max_k\cos(\alpha+120°k)-\min_k\cos(\alpha+120°k)$.
$E$ has period $120°$ and satisfies $E(-\alpha)=E(\alpha)$, so it is determined by
$\alpha\in[0°,60°]$. There $\cos\alpha$ is the largest of the three and $\cos(\alpha+120°)$
the smallest (their arguments lie in $[0°,60°]$ and $[120°,180°]$, while $\alpha+240°\in
[240°,300°]$ gives a value in $[-\tfrac12,\tfrac12]$), so

$$E(\alpha)=\cos\alpha-\cos(\alpha+120°)=\tfrac32\cos\alpha+\tfrac{\sqrt3}{2}\sin\alpha
=\sqrt3\,\sin(\alpha+60°),$$

which on $[0°,60°]$ has minimum $\tfrac32$ at both endpoints and maximum $\sqrt3$ at
$\alpha=30°$. So $\min_\alpha E=\tfrac32$ and $\max_\alpha E=\sqrt3$. Hence the minimal extent is $\tfrac32 R=\tfrac{\sqrt3}{2}s$, and the
maximal is $\sqrt3R=s$ (the diameter, as it must be). $\square$

> **Corollary U.** For any set $S\subseteq\mathbb{R}^2$, an equilateral triangle with all three
> vertices in $S$ has side $s\le\tfrac{2}{\sqrt3}\,w(\operatorname{conv}S)$.

*Proof.* $T\subseteq\operatorname{conv}S$, and minimal width is monotone under inclusion (a pair
of parallel supporting lines of the larger set separates the smaller one too). Apply Lemma W.
$\square$

So **for every Jordan curve** $m(J)\le\tfrac{2}{\sqrt3}w(J)\le\tfrac{2}{\sqrt3}\operatorname{diam}(J)$.
No regularity is used anywhere: $J$ may be any bounded set.

## 3. The constant $2/\sqrt3$ is attained — the thin rectangle

Let $R_\varepsilon=\partial([0,1]\times[0,\varepsilon])$, $0<\varepsilon\le\tfrac{\sqrt3}{2}$.
Then $w=\varepsilon$ and the triangle with base $[(0,0),(\tfrac{2}{\sqrt3}\varepsilon,0)]$ and
apex $(\tfrac{1}{\sqrt3}\varepsilon,\varepsilon)$ is equilateral of side
$\tfrac{2}{\sqrt3}\varepsilon$ with all three vertices on $R_\varepsilon$; by Corollary U it is
maximal. So $m(R_\varepsilon)/w=2/\sqrt3$. The equilateral triangle inscribed in itself gives
the same ratio ($s=a$, $w=\tfrac{\sqrt3}{2}a$).

Meanwhile $\operatorname{diam}=\sqrt{1+\varepsilon^2}\to1$, length $=2+2\varepsilon\to2$ and
area $=\varepsilon$, so already this family gives
$m/\operatorname{diam}\to0$, $m/\mathrm{length}\to0$, $m/\sqrt{\mathrm{area}}
=\tfrac{2}{\sqrt3}\sqrt\varepsilon\to0$. That is I6's observation, re-derived rather than
assumed (I6 is `sketch` and by [`../../../../RULES.md`](../../../../RULES.md) §3 not assumable,
including by its own model family). It does **not** touch the width.

## 4. The L-strip — width dies too, and so does every hull functional

I6 proposes width as "the right convex normalisation" and guesses that a thin **spiral strip**
is the candidate killer for general curves. A spiral is not needed. Let $\delta\in(0,\tfrac14)$
and let $J_\delta$ be the boundary of the **L-hexagon**

$$(0,0),\ (1,0),\ (1,\delta),\ (\delta,\delta),\ (\delta,1),\ (0,1).$$

Write $L=\bigl([0,1]\times\{0\}\bigr)\cup\bigl(\{0\}\times[0,1]\bigr)$, two perpendicular unit
segments sharing an endpoint. Checking the six edges one at a time, **every point of $J_\delta$
is within $\delta$ of $L$**.

> **Lemma L.** If $A,B,C$ are the vertices of an equilateral triangle of side $s$ and each lies
> within $\delta$ of $L$, then $s\le\sqrt{32+16\sqrt3}\;\delta=2(\sqrt6+\sqrt2)\,\delta
> \approx7.7274\,\delta$.

*Proof.* Each vertex is within $\delta$ of the horizontal arm $X$ or of the vertical arm $Y$; by
pigeonhole two of them, say $A,B$, are within $\delta$ of the same arm, and by the reflection
$(x,y)\mapsto(y,x)$ — which preserves both $L$ and $J_\delta$ — we may assume it is $X$. Then
$|A_y|,|B_y|\le\delta$ and $A_x,B_x\in[-\delta,1+\delta]$.

*Case (i): $C$ is also within $\delta$ of $X$.* All three vertices lie in the strip
$|y|\le\delta$ of width $2\delta$, so by Lemma W $\tfrac{\sqrt3}{2}s\le2\delta$ and
$s\le\tfrac{4}{\sqrt3}\delta<2.31\,\delta$.

*Case (ii): $C$ is within $\delta$ of $Y$, so $|C_x|\le\delta$.* Write
$B-A=s(\cos\alpha,\sin\alpha)$; then $|\sin\alpha|=|B_y-A_y|/s\le 2\delta/s$. The third vertex
satisfies $C=\tfrac{A+B}{2}\pm\tfrac{\sqrt3}{2}s(-\sin\alpha,\cos\alpha)$, so

$$\Bigl|\tfrac{A_x+B_x}{2}\Bigr|\;\le\;|C_x|+\tfrac{\sqrt3}{2}s|\sin\alpha|
\;\le\;\delta+\sqrt3\,\delta=(1+\sqrt3)\delta .$$

Hence $A_x+B_x\le2(1+\sqrt3)\delta$, and since $A_x,B_x\ge-\delta$ each of them is at most
$(3+2\sqrt3)\delta$ and at least $-\delta$, so $|A_x-B_x|\le(4+2\sqrt3)\delta$. With
$|A_y-B_y|\le2\delta$,

$$s^2\le\bigl((4+2\sqrt3)^2+4\bigr)\delta^2=(32+16\sqrt3)\,\delta^2 .$$

Case (ii) dominates case (i), which gives the stated bound. $\square$

*(Sanity: $L$ itself carries **no** nondegenerate equilateral triangle — two vertices on one arm
force the apex over the midpoint of a sub-segment of $[0,1]$, which lies on the other arm only
if both are the shared endpoint. Lemma L is the quantitative form of that.)*

> **Theorem D (degeneracy).** Let $N$ be any functional on compact plane sets that (i) depends
> only on $\operatorname{conv}$, (ii) is continuous in the Hausdorff metric on convex bodies,
> and (iii) is positive on the triangle $T_0=\operatorname{conv}\{(0,0),(1,0),(0,1)\}$. Then
> $\inf_J m(J)/N(J)=0$, the infimum over Jordan curves. The same holds for $N=\mathrm{length}$
> and for $N=\sqrt{\text{enclosed area}}$.

*Proof.* $\operatorname{conv}J_\delta\to T_0$ in the Hausdorff metric as $\delta\to0$, so
$N(J_\delta)\to N(T_0)>0$, while $m(J_\delta)\le2(\sqrt6+\sqrt2)\delta\to0$ by Lemma L. For the
other two: $\mathrm{length}(J_\delta)=4$ for every $\delta$, and the enclosed area is
$2\delta-\delta^2$, so $m/\sqrt{\text{area}}\le2(\sqrt6+\sqrt2)\delta/\sqrt{2\delta-\delta^2}\to0$.
$\square$

This covers diameter, width, hull perimeter, hull area, hull inradius, hull circumradius, mean
width, and every other hull functional anyone is likely to propose. Explicitly, for the
diameter, $w(\operatorname{conv}J_\delta)=\tfrac{1+\delta}{\sqrt2}$ and
$\operatorname{diam}J_\delta=\sqrt2$, so

$$\frac{m(J_\delta)}{\operatorname{diam}}\;\le\;\frac{2(\sqrt6+\sqrt2)}{\sqrt2}\,\delta
\;\longrightarrow\;0,\qquad
\frac{m(J_\delta)}{w}\;\le\;2\sqrt2(\sqrt6+\sqrt2)\,\delta\;\longrightarrow\;0 .$$

**Exact computation (`numerical`).** The bound of Lemma L is off by exactly a factor $2$. For
$\delta\in\{\tfrac1{10},\tfrac1{20},\tfrac1{50},\tfrac1{100}\}$, maximising the side over
$240$ exactly-represented boundary points $O$ per curve, in $\mathbb{Q}(\sqrt3)$ with no
floating point and no `sympy` predicate, the answer is in every case

$$\text{side}^2=(8+4\sqrt3)\,\delta^2,\qquad \text{side}=(\sqrt6+\sqrt2)\,\delta
=4\cos15°\,\delta\approx3.8637\,\delta,$$

attained at $O=(0,0)$ with the other two vertices $\bigl(\delta,(2+\sqrt3)\delta\bigr)$ and
$\bigl((2+\sqrt3)\delta,\delta\bigr)$ — all three re-checked, by code that knows nothing about
how they were found, to be on $J_\delta$, pairwise distinct and pairwise equidistant. The exact
linear scaling in $\delta$ is what the hand argument predicts, so the two agree in form as well
as in size. This is a **lower** bound on $m(J_\delta)$ (only finitely many $O$ were tried);
Lemma L supplies the upper bound, and Theorem D uses only the upper bound.

## 5. What is left standing

1. **The convex question** (I6's): $\mu_{\mathrm{conv}}=\inf\{m(K)/w(K):K$ convex$\}$. Non-empty
   — §6 and §7 bracket it.
2. **The inradius of the interior region.** Every attempt to make $m(J)/r(\Omega_J)$ small
   failed, including the L-strip itself, where $r=\delta/2$ and
   $m/r\ge2(\sqrt6+\sqrt2)\approx7.73$ — far above the disk's $\sqrt3$. §6 proves $m\ge\sqrt3\,r$ for convex bodies
   with equality only in the disk case, which suggests

   > **Conjecture I.** $m(J)\ge\sqrt3\,r(\Omega_J)$ for every Jordan curve, with equality iff
   > $J$ is a circle.

   This is **open here** and is the one normalisation the lane could not settle. Its square
   analogue would presuppose the square peg theorem, so it is out of bounds for squares — see
   §9.2 for why the triangle proof does not transfer.

## 6. Lower bound for convex bodies

> **Theorem C.** Let $K\subset\mathbb{R}^2$ be a convex body (compact, convex, nonempty
> interior) with inradius $r$. Then $K$ inscribes an equilateral triangle of side $\ge\sqrt3\,r$;
> that is, $m(K)\ge\sqrt3\,r$. The disk is an equality case.

*Proof.* **Step 0 (reduce to strictly convex).** Let $D$ be the closed unit disk and
$K_n=K+\tfrac1nD$. Each $K_n$ is strictly convex (a segment in $\partial(A+B)$ needs parallel
segments in $\partial A$ and $\partial B$, and $\partial D$ has none), $K_n\to K$ in the
Hausdorff metric, and $r(K_n)=r+\tfrac1n$. If $T_n$ is an equilateral triangle inscribed in
$K_n$ of side $\ge\sqrt3\,r(K_n)$, pass to a subsequence along which the three vertices
converge; the limits lie on $\partial K$ (each vertex satisfies $\mathrm{dist}(\cdot,K)\le
\tfrac1n$, so the limit is in $K$; and if the limit were in $\operatorname{int}K$ then a ball
around it would lie in $K\subseteq K_n$ and contain the vertex, contradicting its being on
$\partial K_n$), and the limit
triangle is equilateral of side $\ge\sqrt3\,r>0$ — the noncollapse bound is uniform along the
sequence and established *before* the limit ([`../../RULES.md`](../../RULES.md) §2). So it
suffices to prove the theorem for strictly convex $K$.

**Step 1 (the radial picture at an incircle contact point).** Let $D(O,r)$ be the incircle and
$A\in\partial K\cap\partial D(O,r)$ a contact point; let $\nu$ be the unit vector from $A$ to
$O$, and measure angles $\theta$ from $\nu$. The tangent line to $D(O,r)$ at $A$ supports $K$
(it supports $D(O,r)$, $D(O,r)\subseteq K$ and $A\in\partial K$), so $K$ lies in the closed
half-plane $\langle\,\cdot-A,\nu\rangle\ge0$; and $D(O,r)\subseteq K$ makes every direction with
$|\theta|<90°$ point into $K$. Hence the cone of directions from $A$ into $K$ is exactly
$|\theta|\le90°$, and

$$R(\theta)=\max\{t\ge0:\ A+t\,u(\theta)\in K\},\qquad |\theta|\le 90°,$$

parametrises $\partial K\setminus\{A\}$: $\theta\mapsto A+R(\theta)u(\theta)$ is a continuous
bijection onto it. Strict convexity gives $R(\pm90°)=0$ (a positive value would put a segment of
the supporting line in $K$). And the chord of the incircle from $A$ in direction $\theta$ gives

$$R(\theta)\ \ge\ 2r\cos\theta,\qquad |\theta|<90°. \tag{$\ast$}$$

**Step 2 (the criterion).** $A$ is a vertex of an inscribed equilateral triangle of side $s$
**iff** $R(\theta)=R(\theta+60°)=s>0$ for some $\theta\in[-90°,30°]$: the two other vertices are
at equal distance $s$ from $A$ subtending $60°$, and an isosceles triangle with apex angle $60°$
is equilateral. Put $g(\theta)=R(\theta+60°)-R(\theta)$ on $[-90°,30°]$; $g$ is continuous,
$g(-90°)=R(-30°)>0$ and $g(30°)=-R(30°)<0$ by $(\ast)$, so the zero set
$Z=\{g=0\}\subset(-90°,30°)$ is nonempty and compact, and
$c:=m(A):=\max_{\theta\in Z}R(\theta)$ exists and is positive.

**Step 3 (the contradiction).** Suppose $c<\sqrt3\,r$. Put $\beta=\arccos\bigl(c/(2r)\bigr)$;
then $\beta\in(30°,90°)$. Let $\theta\in Z$. Then $R(\theta)=R(\theta+60°)\le c$, so by $(\ast)$
$2r\cos\theta\le c$ and $2r\cos(\theta+60°)\le c$, i.e.

$$|\theta|\ge\beta\quad\text{and}\quad|\theta+60°|\ge\beta .$$

Since $\theta\le30°<\beta$, the first forces $\theta\le-\beta$. The second forces
$\theta\ge\beta-60°$ or $\theta\le-60°-\beta$. But $\beta>30°$ makes $\beta-60°>-\beta$, so
$\theta\ge\beta-60°$ is incompatible with $\theta\le-\beta$; and $\beta>30°$ makes
$-60°-\beta<-90°$, so $\theta\le-60°-\beta$ is incompatible with $\theta\ge-90°$. Hence
$Z=\emptyset$, contradicting Step 2. Therefore $c\ge\sqrt3\,r$. $\square$

**Sharpness.** For the disk of radius $r$, three points on a circle are equilateral only if the
circle is their circumcircle, so *every* inscribed equilateral triangle has side exactly
$\sqrt3\,r$: $m=\sqrt3\,r$.

> **Lemma B.** A planar convex body satisfies $w\le3r$.

*Proof (classical, reproved here rather than cited — this repo has been burned by citing from
memory).* The contact points of the incircle are not contained in an open half-circle: otherwise
translating the incircle slightly along the bisecting direction and enlarging it keeps it inside
$K$, contradicting maximality. If two contact points are antipodal, the two tangent lines there
support $K$ and $w\le2r\le3r$. Otherwise choose three contact points not in an open half-circle;
their three tangent lines support $K$ and bound a triangle $T\supseteq K$ whose incircle is
$D(O,r)$. Then $w(K)\le w(T)=2\,\mathrm{Area}(T)/a_{\max}=2rs/a_{\max}$ with $s$ the
semiperimeter, and $a_{\max}\ge\tfrac{2}{3}s$, so $w(T)\le3r$. $\square$

> **Corollary.** $m(K)\ge\sqrt3\,r\ge\tfrac{\sqrt3}{3}w=w/\sqrt3$ for convex $K$; that is
> $\mu_{\mathrm{conv}}\ \ge\ 1/\sqrt3\approx0.57735$.

The chain is not simultaneously sharp: Theorem C is sharp at the disk, Lemma B at the
equilateral triangle, and no body is both.

## 7. Upper bound for convex bodies — and the disk is *not* extremal

**The disk.** $m/w=\sqrt3 r/(2r)=\sqrt3/2\approx0.8660254$, exactly. So
$\mu_{\mathrm{conv}}\le\sqrt3/2$.

**First-order perturbation (`sketch`, analytic).** Perturb the unit disk radially,
$\rho(\theta)=1+\varepsilon f(\theta)$. Inscribed equilateral triangles near the circle's have
vertices at $\theta,\theta+120°+O(\varepsilon),\theta+240°+O(\varepsilon)$ and side
$\sqrt3\bigl(1+\varepsilon F(\theta)\bigr)+O(\varepsilon^2)$ where
$F=\tfrac13\sum_{k}f(\cdot+120°k)$; the support function is $1+\varepsilon f+O(\varepsilon^2)$,
so $w=2\bigl(1+\varepsilon\min_\theta G\bigr)+O(\varepsilon^2)$ with
$G=\tfrac12\bigl(f(\cdot)+f(\cdot+180°)\bigr)$. Hence

$$\frac{m}{w}=\frac{\sqrt3}{2}\Bigl(1+\varepsilon\bigl(\max_\theta F-\min_\theta G\bigr)\Bigr)
+O(\varepsilon^2).$$

$F$ and $G$ have the same mean $a_0$, so $\max F\ge a_0\ge\min G$ **always**: no perturbation
of the disk decreases the ratio at first order, and the first-order term vanishes exactly when
$F\equiv a_0$ and $G\equiv a_0$, i.e. when $f$ has **no even harmonic** and **no harmonic
divisible by 3** — $n\equiv\pm1\pmod 6$. The numerics below reproduce the predicted coefficient
for $n=3$ ($0.8660\,\varepsilon$ against the predicted $\tfrac{\sqrt3}{2}\varepsilon$), which is
the check that the formula is right.

**No even harmonic means constant width.** With support function
$h(\theta)=1+\varepsilon\cos5\theta$ one has $h(\theta)+h(\theta+180°)=2$ identically, so the
body has **constant width $2$** — the width is exact and no numerical quantity enters the
denominator of the ratio at all. Convexity is $h+h''=1-24\varepsilon\cos5\theta>0$, i.e.
$\varepsilon\le\tfrac1{24}$.

**Float search (`numerical`).**

| body ($h=$) | convex | $m$ | $m/w$ |
|---|---|---|---|
| $1$ (disk) | yes | $1.7320508$ | $0.8660254$ |
| $1+0.01\cos3\theta$ | yes | $1.7493713$ | $0.8746857$ |
| $1+0.01\cos7\theta$ | yes | $1.7308575$ | $0.8654288$ |
| $1+0.01\cos5\theta$ | yes | $1.7306396$ | $0.8653198$ |
| $1+0.03\cos5\theta$ | yes | $1.7217849$ | $0.8608925$ |
| $1+\tfrac1{24}\cos5\theta$ | yes (equality in $h+h''\ge0$) | $1.7144101$ | $\mathbf{0.8572050}$ |

The $n=3$ row rises linearly at the predicted rate; the $n=5,7$ rows fall quadratically
($\approx7.4\,\varepsilon^2$ and $\approx6.0\,\varepsilon^2$), confirming that the first order
vanishes there and that the second order is **negative**. A 24-parameter Nelder–Mead over
general convex support functions $h=1+\sum_{n=2}^{13}(a_n\cos n\theta+b_n\sin n\theta)$, with
the correct $w=\min_\theta[h(\theta)+h(\theta+180°)]$ and the convexity constraint, returned to
$h=1+\tfrac1{24}\cos5\theta$ and found nothing better. Two further restarts — one from the disk,
one from a random small perturbation — both drifted into the pure $a_5$ direction and stopped at
$0.86503$ and $0.86691$ without reaching, let alone beating, $0.857205$. **Honest caveat:**
Nelder–Mead in 24 dimensions with a few hundred evaluations is under-converged, so "nothing
better was found" is a statement about this search, not about the family.

So, **subject to the float caveat of §8**: the disk is not the extremal convex body, and

$$0.57735\ \le\ \mu_{\mathrm{conv}}\ \le\ 0.857205\ (<\ \sqrt3/2=0.866025).$$

I do **not** claim $0.857205$ is the answer; it is the best body found in a two-family search,
and $0.857205$ has no recognisable closed form that I could find
($0.857205\cdot2/\sqrt3=0.98982\ldots$).

## 8. What the brief's suggested route gives, and one refuted approach

**Theorem T of [`../rectifiable-case/`](../rectifiable-case/) gives no lower bound.** Its
Lemma 2 produces, for *every* $\rho\le\varepsilon$, some $\tau\in(0,\rho)$ with
$\#(J\cap\partial B(O,\tau))=2$, and the triangle it builds has side comparable to $\tau$. Since
$\rho$ may be taken arbitrarily small, the construction certifies triangles of arbitrarily small
side and bounds $m$ from below by nothing. It is also `sketch`, so by
[`../../../../RULES.md`](../../../../RULES.md) §3 it could not have been used even if it had
been quantitative — kill-criterion K5 (§10). The quantitative content of the brief's suggestion
turns out to live not in Theorem T but in the incircle (§6).

**Refuted approach: "the largest *contained* equilateral triangle is inscribed".** The tempting
short proof of §6 is: $K$ contains a disk of radius $r$, hence contains an equilateral triangle
of side $\sqrt3r$, hence — if a maximal contained triangle must have its vertices on
$\partial K$ — $m\ge\sqrt3r$. **The fixed-orientation version of that implication is false**: the
largest horizontal-base equilateral triangle inside the unit square has side $1$ (its base is
the whole bottom edge) and its apex, at height $\sqrt3/2<1$, is interior. The global version
(maximise over orientation too) survived that test but needs a contact-set case analysis with a
genuinely awkward branch (two antipodal contact normals) that I could not close. Recorded here
so the next worker does not spend the same hour on it; §6 needs none of it.

**Exactness of the numbers.** Exact in $\mathbb{Q}(\sqrt3)$, no floating point, no `sympy`
predicate: everything in §4 (the L-hexagon side$^2$ and witnesses) and the §9.3 polygon control.
**Float:** everything in §7 except the disk row and the first-order formula. The float numbers
are search output, not decisions: two structurally independent estimators (a rotation sweep with
bisection; a penalty multistart over three boundary parameters that never rotates anything)
agree to $10^{-9}$ on three bodies, and the disk is reproduced as $1.7320508$. They are reported
as `numerical` and nothing is built on them.

## 9. The three filters ([`../../RULES.md`](../../RULES.md) §3) — all run

### 9.1 Wedge test

The $30$-$30$-$120$ witness is not a counterexample to anything here, and the wedge obstruction
is *consistent* with §6: at a contact point $A$ of the incircle the body subtends exactly $180°$
(Step 1), so it can never be wedge-obstructed, and §6 never places $A$ anywhere else. Run on the
$30$-$30$-$120$ triangle itself: the exact maximiser confirms both $30°$ apexes are exceptional
and the $120°$ apex has maximum side $2/3$ (side$^2=4/9$, triangle
$(0,\tfrac{\sqrt3}{3}),(\pm\tfrac13,0)$) — note this is **larger** than the side$^2=1/3$ witness
recorded in `experiments/inscribed-triangle-angular/README.md`, which reports the *first*
witness found, not the maximum. Both are correct; a lane about *size* must not reuse a decider
that short-circuits, which is why §4 and §9.3 use a maximiser written for this lane.

### 9.2 Square contrast

- **Upper bounds and witnesses transfer harmlessly and prove nothing.** Lemma W's analogue is
  "a square of side $s$ has minimal width $s$", giving $m_{\square}(J)\le w(J)$ for every set.
  That is a statement that certain squares are *small*; it asserts no existence, so no
  square-peg content is created, and the same goes for §4's witness, which only ever says that
  something does **not** fit. (I have not checked whether Lemma L's analogue holds for squares
  and do not need it.) This asymmetry — upper bounds transfer, lower bounds must not — is why
  §4 passes the filter trivially while §6 needs a real answer.
- **Theorem C does not transfer.** Its Step 2 is precisely the non-transferring step named in
  [`../../RULES.md`](../../RULES.md) §3.2: $R(\theta)=R(\theta+60°)$ closes the figure from
  **three** points because isosceles-with-$60°$-apex is equilateral. With $90°$ the identical
  argument (with $\beta=\arccos(c/2r)>45°$) yields only: *every convex body has a boundary point
  $A$ and two boundary points at distance $\ge\sqrt2\,r$ from $A$ subtending a right angle at
  $A$* — three vertices of a square whose fourth vertex is determined but under no constraint to
  lie on $\partial K$. That is a true and unremarkable statement, and it is not an inscribed
  square. **Pass.**
- Conjecture I (§5) is stated for triangles only; its square analogue would presuppose the
  square peg theorem for general Jordan curves and is explicitly *not* conjectured here.

### 9.3 Polygon control

Theorem C was tested against exact polygon computation before being written up: for 13 convex
rational polygons (unit square, equilateral, $30$-$30$-$120$, two thin rectangles, a hexagon, a
sliver, and six random integer-hull polygons) the exactly-computed lower bound on $m$ (maximised
over $30$ exact sample points per edge) was compared with $\sqrt3\,r$:

| | ratio $m/(\sqrt3 r)$ |
|---|---|
| minimum over the 13 | $1.164$ (hexagon) |
| unit square | $1.195$ |
| equilateral triangle | $2.000$ |
| thin rectangles | $1.333$ |

All $\ge1$, none below, and the disk — the equality case — is not a polygon, which is exactly
the expected picture. A polygon that had come out below $1$ would have killed Theorem C on the
spot. **Pass** — and, per [`../../RULES.md`](../../RULES.md) §3.3, this is *merely not-yet-dead*.

## 10. Kill-criterion outcomes

| | outcome |
|---|---|
| **K1** normalisation degenerate | **FIRED, twice.** Diameter (§3) and then width and every other hull functional (§4). Honoured as written: the answer "$\mu_N=0$, the question is empty" is reported as the result, and the lane moved to the next normalisation instead of optimising inside an empty problem. |
| **K2** *every* normalisation degenerate | **Did not fire.** The convex question survives (§6, §7) and the interior inradius resisted every attempt (§5). No exotic functional was invented to keep the lane alive. |
| **K3** convex constant resists | **FIRED, partially.** One session produced bounds $[0.5774,\,0.8572]$ and no closed form. Parked with the numbers reported, as K3 requires, rather than extended. |
| **K4** lower bound survives the square substitution | **Did not fire** (§9.2): Theorem C's $60°$ closure is exactly what fails at $90°$. |
| **K5** lower bound built on a `sketch` | **Avoided by construction.** Theorem T is not used; §8 says why it would not have helped anyway. |
| **K6** exact constant apparently in reach | **Did not fire for general curves** — there is no constant, that is the finding. §11 flags the one statement that is novel-looking. |

## 11. What is open, and the §7 flag

[`../../../../RULES.md`](../../../../RULES.md) §7 applies proportionally, so: **this appears to
show** three things, none announced as settled.

1. **The step I trust least in Theorem C** is Step 1's assertion that $\theta\mapsto
   A+R(\theta)u(\theta)$ parametrises $\partial K\setminus\{A\}$ *continuously up to the closed
   endpoints* $\theta=\pm90°$, which is what makes $g$ continuous on the compact interval and
   the sign change usable. I believe it for strictly convex bodies (Step 0 reduces to those) but
   I have not written the proof out in full, and it is the kind of step this problem's
   [`RULES.md`](../../RULES.md) §6.2(2) says to attack. Second least trusted: Step 0's claim that
   a Hausdorff limit of vertices on $\partial K_n$ lies on $\partial K$.
2. **The disk is not the extremal convex body** rests on floats (§7, §8). Making it exact needs
   an exact **maximiser** of the inscribed side over a whole rational polygon — the repo's two
   deciders answer "is this point a vertex", not "how large is the largest triangle anywhere on
   this curve". That is a concrete, well-scoped follow-up tool, and this lane owns no file under
   `experiments/` in which to build it.
3. **Conjecture I** ($m\ge\sqrt3\,r(\Omega)$ for every Jordan curve) is the surviving
   quantitative question. §6 proves it for convex bodies. Nothing here says anything about the
   non-convex case, where the interior inradius is the only quantity the L-strip does not
   destroy.

**Literature.** Not attempted: this lane did no citation work, and per this problem's
[`RULES.md`](../../RULES.md) §6.1 "not found" would in any case not be "open". I6 guesses the
convex constant may sit in the convexity literature rather than the peg literature; whether
Theorem C or the $0.857205$ body is known is **unknown to me**, and I have deliberately not
guessed at authors.

## 12. Reproducing the numbers

This lane owns no file under `experiments/`, so the scripts below are reproduced verbatim rather
than committed; they are the whole of the computation and depend only on CPython 3.11 and, for
the exact parts, on **reading** (never modifying) the committed exact field arithmetic in
`experiments/inscribed-triangle-angular/{q3,angular,shapes}.py`. No `sympy`, no `numpy`, no
library geometry predicate, no random seed that matters except `20260829` in the polygon
control.

**Exact maximiser (§4, §9.1, §9.3).** For $O$ on a simple polygon $P$, the maximum side at $O$
is $\max\{|OX| : X\in P\cap\rho_{O,60°}(P),\ X\ne O\}$, since $O,X,\rho^{-1}X$ is equilateral of
side $|OX|$. Implement it as: rotate every vertex of $P$ by $60°$ about $O$; for each of the
$n^2$ ordered edge pairs take the exact intersection (for collinear overlaps, the overlap
endpoints — the maximum of $|OX|$ over a segment is at an endpoint); discard $X=O$; take the
maximum of $|OX|^2$ in $\mathbb{Q}(\sqrt3)$; re-check the resulting triple independently with
`angular.point_on_polygon` and exact equality of the three squared sides. Validation before use:
equilateral triangle $\to$ side$^2=1$ at each vertex; unit square $\to 8-4\sqrt3$ at each corner;
$30$-$30$-$120$ $\to$ both $30°$ apexes exceptional and $4/9$ at the $120°$ apex.

**L-hexagon (§4).** `[(0,0),(1,0),(1,d),(d,d),(d,1),(0,1)]` with $d\in\{1/10,1/20,1/50,1/100\}$
as exact `Fraction`s; sample $O$ at all vertices and $39$ interior points per edge; report the
maximum side$^2$.

**Convex float search (§7).** Bodies by support function $h(\theta)=1+\sum(a_n\cos
n\theta+b_n\sin n\theta)$; boundary $p(\theta)=h\,u(\theta)+h'\,u'(\theta)$; membership by a
radial table built from $32000$ boundary samples with linear interpolation; $m$ by, for each of
$N_1$ base points $A$, sweeping $N_2$ second points $B$, rotating $B$ about $A$ by $\pm60°$ and
bisecting on the sign of "outside" ($50$ bisections), then a golden-section refinement in the
base parameter; $w=\min_\theta[h(\theta)+h(\theta+180°)]$ over $2000$ directions (exactly $2$
for the odd-harmonic bodies); convexity by $\min_\theta(h+h'')>0$ over $4000$ directions. The
independent estimator replaces all of that by a Nelder–Mead penalty multistart over three
boundary parameters minimising $-\overline{s}+\lambda\sum(s_i-\overline{s})^2$ with
$\lambda$ ramped $10\to10^8$, $200$ restarts.
