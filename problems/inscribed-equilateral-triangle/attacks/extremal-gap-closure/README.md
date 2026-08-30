# Attack: closing the two gaps in `extremal-size` Theorem C ($m(K)\ge\sqrt3\,r$)

```
regularity budget: convex.  Every statement below is about a planar convex body
  (compact, convex, nonempty interior).  Nothing here is claimed for general Jordan curves,
  and the counterexample in the SISTER lane (extremal-size Sec 4) shows the conclusion is
  FALSE for general Jordan curves, so "convex" is load-bearing, not decorative.
  Sec 5's counterexample body and Sec 7's polygon checks: exact Q(sqrt3)/Q arithmetic.
What breaks first if you drop convexity: the incircle stops controlling the boundary
  (extremal-size Sec 4's L-hexagon has m/r arbitrarily small relative to any hull functional),
  the radial function R(theta) stops being single-valued, and the tangent cone at a contact
  point stops being a half-plane -- i.e. everything.
What breaks if you keep convexity but drop STRICT convexity: Sec 5 below, exactly.
```

- Lane: **prove side of a deliberate clash.** A concurrent lane
  (`../extremal-refutation-hunt/`) is trying to *refute* the same bound. Its files were
  **not read** and no coordination took place; that is the point of the exercise.
- Author: `claude` (Claude Opus 5), 2026-08-30, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), **written before any computation
  in this lane** ([`../../../../RULES.md`](../../../../RULES.md) §6.2). Outcomes: §8.
- Journal: [`../../../../notebook/claude/2026-08-30-iet-extremal-gap.md`](../../../../notebook/claude/2026-08-30-iet-extremal-gap.md).
- Files this lane owns: this one, `KILL-CRITERION.md`, and that journal. **No file in
  `../extremal-size/` was edited**; corrections it needs are requested in §9.
- Target: the two steps that [`../extremal-size/README.md`](../extremal-size/README.md) §6
  self-flagged and that [`../round3-cross-review/README.md`](../round3-cross-review/README.md)
  ("Objection 1") could neither close nor break.

## Headline

**Both gaps are now settled, and one of them was a real error.**

1. **Gap 2 (endpoint continuity) closes**, and the sub-interval route the brief suggested does
   work — but it is *not* a free lunch: it removes the need to define $R$ at $\pm90°$ and the
   need for the bijection claim, while still requiring the one substantive fact
   ($R(\theta)\to0$ as $\theta\to\pm90°$, which is strict convexity at the contact point). Both
   routes are written out in §3; the honest accounting is that the reformulation relocates the
   difficulty rather than deleting it, so I give the underlying lemma a proof either way.
2. **Gap 1 (Step 0) contains a false assertion.** `extremal-size` §6 asserts that
   $K_n=K+\tfrac1nD$ is *strictly convex*. It is not: **$K+\varepsilon D$ is strictly convex if
   and only if $K$ is.** Minkowski summation with a disk *smooths* the boundary; it does not
   round off flat pieces. Exact witness: $[0,1]^2+D$ contains the segment
   $[(0,-1),(1,-1)]$ in its boundary (§4, CHECK 6).
3. **That error is load-bearing, not cosmetic.** §5 exhibits an explicit convex body — a disk
   with one point pulled out to a spike, $K_{100}=\operatorname{conv}\bigl(D((0,1),1)\cup\{(100,0)\}\bigr)$
   — with a genuine incircle contact point $A=(0,0)$ at which the Step-2 zero set
   $Z=\{\theta: R(\theta)=R(\theta+60°)\}$ is **empty**. So the machinery of Steps 1–3 really
   does need the reduction; it is not a convenience. As a side effect the "**iff**" in Step 2 is
   *false* for non-strictly-convex bodies (that same $A$ *is* a vertex of an inscribed
   equilateral triangle of side $\approx2.283$, found off the radial criterion entirely).
4. **The reduction has a clean correct replacement**, given in §4: a gauge (Minkowski-functional)
   smoothing $K_\varepsilon=\{(1-\varepsilon)\gamma_K^2+\varepsilon|x|^2/b^2\le1\}$ which *is*
   strictly convex, satisfies $K\subseteq K_\varepsilon\subseteq(1-\varepsilon)^{-1/2}K$, and
   therefore keeps every other line of Step 0 (including the "limit lands on $\partial K$" step,
   which is correct as written and is re-derived here) working verbatim.
5. §6 assembles the **repaired proof end to end**, self-contained, plus a simplification of
   Step 3 that deletes the auxiliary angle $\beta$.
6. §2 records the ten minutes spent on replacing the approach: the containment route fails for a
   specific reason, but the attempt produced **Lemma R**, which gives a short *limit-free,
   IVT-free* proof of $m(K)\ge\sqrt3\,r$ for every convex body with 3-fold rotational symmetry
   (disk, equilateral triangle, Reuleaux triangle, regular $3k$-gons) — an independent
   confirmation of the theorem on a nontrivial family.

**Status of everything here: `sketch` or `numerical`.** Nothing in this file is assumable
([`../../../../RULES.md`](../../../../RULES.md) §3), including by me, and I grant no
`verified:review`. The theorem is *not* proved here to a promotable standard; what changed is
that its two named holes now have a located error, a repair, and a witness showing why the
repair is necessary.

## Result table

| § | Statement | Status |
|---|---|---|
| §2 | **Lemma R.** If $D(O,r)\subseteq K$ and $P_1,P_2,P_3\in\partial K$ lie on rays from $O$ at mutual $120°$, then every side $\ge\sqrt3\,r$. | `sketch` — mine, elementary |
| §2 | **Corollary R'.** Every convex body with 3-fold rotational symmetry satisfies $m(K)\ge\sqrt3\,r$. No limits, no IVT, no strict convexity. | `sketch` — mine |
| §2 | The containment route ("$D(O,r)\subseteq K$, so the disk's triangle works") is **`refuted`**, for a stated reason. | `refuted` |
| §3 | **Lemma C (interior continuity).** $R$ is continuous on the open cone $(-90°,90°)$. | `sketch` — mine, re-derived |
| §3 | **Lemma E (endpoint decay).** For strictly convex $K$, $R(\theta)\to0$ as $\theta\to\pm90°$. Closes Gap 2. | `sketch` — mine |
| §3 | The sub-interval IVT runs on $[-90°+\varepsilon,\,30°-\varepsilon]$ and needs no value of $R$ at $\pm90°$ — but still needs Lemma E. | `sketch` — mine |
| §4 | **$K+\varepsilon D$ is strictly convex iff $K$ is.** `extremal-size` §6 Step 0's assertion and its parenthetical justification are both **wrong**. | `sketch` + `numerical` (exact witness) |
| §4 | **Lemma S (repair).** The gauge smoothing $K_\varepsilon$ is strictly convex with $K\subseteq K_\varepsilon\subseteq(1-\varepsilon)^{-1/2}K$. | `sketch` — mine |
| §4 | **Lemma L0 (limit).** If $K\subseteq K_n$, $K_n\to K$, $v_n\in\partial K_n$, $v_n\to v$, then $v\in\partial K$. Step 0's limit step is **correct as written**. | `sketch` — mine, re-derived |
| §5 | **$Z=\emptyset$ for $K_{100}$ at the contact point $(0,0)$.** Step 0 is load-bearing. | `sketch` (exact case analysis) + `numerical` (grid corroboration) |
| §5 | Step 2's "**iff**" is false for non-strictly-convex bodies. | `sketch` — mine |
| §6 | **Theorem C (repaired).** Every planar convex body with inradius $r$ inscribes an equilateral triangle of side $\ge\sqrt3\,r$; sharp at the disk. | `sketch` — mine; the repair, not a promotion |
| §7 | Wedge test, square test, polygon control — all run, all reported. | `sketch` + `numerical` |

---

## 1. What is being proved, and what I re-derived rather than assumed

> **Theorem C.** Let $K\subset\mathbb{R}^2$ be a convex body (compact, convex, nonempty interior)
> with inradius $r>0$. Then some equilateral triangle of side $s\ge\sqrt3\,r$ has all three
> vertices on $\partial K$. The disk is an equality case.

[`../../../../RULES.md`](../../../../RULES.md) §3 forbids building on a `sketch`, including this
repo's own, so **everything the argument uses is re-derived below from definitions**: the
existence of an incircle contact point, the fact that the supporting line there is the incircle's
tangent, the chord bound $R(\theta)\ge2r\cos\theta$, continuity of $R$, the criterion for an
inscribed equilateral triangle with a vertex at $A$, and the angle arithmetic. Nothing is taken
from `../extremal-size/`, `../rectifiable-case/`, the provisional `cited`\* rows of
[`../README.md`](../README.md), or the unvalidated
`experiments/inscribed-triangle-maximiser/`. I read `../extremal-size/README.md` to know *what*
to check; I did not import any of its claims as premises.

Standing notation, fixed once. $D(c,\rho)$ is the closed disk. $r$ is the inradius; **a** largest
inscribed disk is $D(O,r)$ (the inball need **not** be unique — a stadium has a whole segment of
inball centres — and nothing below uses uniqueness). $u(\theta)=(\sin\theta,\cos\theta)$ in a
frame whose $+y$ axis is $\nu$, the unit vector from the contact point $A$ towards $O$. And

$$R(\theta)=\max\{t\ge0:\ A+t\,u(\theta)\in K\}.$$

Since $K$ is compact this maximum exists, and $A+R(\theta)u(\theta)\in\partial K$ always.

**Two facts I re-derive immediately, because everything rests on them.**

> **Fact 1 (a contact point exists, and its supporting line is the incircle's tangent).**
> $r=\operatorname{dist}(O,\partial K)$, so a nearest boundary point $A$ exists with $|OA|=r$;
> then $A\in\partial K\cap\partial D(O,r)$. Any supporting line $H$ of $K$ at $A$ has
> $D(O,r)\subseteq K\subseteq H^-$ and passes through $A\in\partial D(O,r)$, so it is a line
> through a point of the circle with the disk on one side: it is *the* tangent line, i.e.
> $H\perp OA$. Hence $K\subseteq\{x:\langle x-A,\nu\rangle\ge0\}$, and the cone of directions
> from $A$ meeting $K$ is contained in $\{|\theta|\le90°\}$; since $D(O,r)\subseteq K$, every
> $|\theta|<90°$ meets $K$ in a segment of positive length.

> **Fact 2 (chord bound).** For $|\theta|\le90°$, $R(\theta)\ge2r\cos\theta$. *Proof.* $A$ lies on
> the circle $\partial D(O,r)$ and $\nu$ points along the diameter through $A$; the chord from $A$
> making angle $\theta$ with that diameter has length $2r\cos\theta$ (Thales: the far endpoint
> subtends a right angle at the antipode). That chord lies in $D(O,r)\subseteq K$. $\square$
> Note this is trivially true at $|\theta|=90°$ too, where it says $R\ge0$; the estimate
> *degenerating* there is precisely Gap 2.

> **Fact 3 (sufficient criterion).** If $R(\theta)=R(\theta+60°)=s>0$ for some $\theta$ with
> $\theta,\theta+60°\in[-90°,90°]$, then $A$, $A+s\,u(\theta)$, $A+s\,u(\theta+60°)$ are three
> points of $\partial K$ forming an equilateral triangle of side $s$ (two sides of length $s$
> with a $60°$ angle between them force the third). **This is an implication, not an
> equivalence** — see §5, where the converse fails.

---

## 2. Ten minutes on replacing the approach (as the brief required)

**Why the containment route fails — precisely.** Every convex body of inradius $r$ contains a
disk $D(O,r)$, and that disk inscribes an equilateral triangle of side exactly $\sqrt3\,r$
(three points on a circle are equilateral only if that circle is their circumcircle, so *every*
equilateral triangle inscribed in $D(O,r)$ has side exactly $\sqrt3\,r$ — which also gives the
sharpness claim). The triangle so obtained is **contained** in $K$. But "inscribed" is a
*boundary* condition, not a containment condition: its vertices lie on $\partial D(O,r)$, which
for any $K\ne D(O,r)$ meets $\partial K$ in a proper subset of the circle, so generically all
three vertices are in $\operatorname{int}K$. Pushing them out to $\partial K$ — by dilating about
the centre, say — moves the three vertices onto $\partial K$ at three *different* dilation
factors, and the triangle stops being equilateral the instant the first vertex lands. There is no
monotonicity to appeal to either: $m(\cdot)$ is not monotone under inclusion in a usable
direction, and the only inclusion-monotone quantity in sight (minimal width, via
`extremal-size` §2's Corollary U) bounds $m$ from *above*, which is the wrong side. **Route
`refuted`; per KILL-CRITERION K4 I stopped looking after one further attempt.**

**The one further attempt, which paid for itself.** Fix the incircle $D(O,r)\subseteq K$ and
shoot three rays from $O$ at mutual $120°$.

> **Lemma R.** Let $D(O,r)\subseteq K$ and let $P_1,P_2,P_3\in\partial K$ lie on three rays from
> $O$ at mutual angles $120°$. Then $|P_iP_j|\ge\sqrt3\,r$ for every $i\ne j$.
>
> *Proof.* $\rho_i:=|OP_i|\ge r$, because $D(O,r)\subseteq K$ and $P_i\in\partial K$ forces
> $P_i\notin\operatorname{int}D(O,r)$. The angle $P_iOP_j$ is $120°$, so
> $|P_iP_j|^2=\rho_i^2+\rho_j^2-2\rho_i\rho_j\cos120°=\rho_i^2+\rho_j^2+\rho_i\rho_j\ge3r^2$.
> $\square$

So *any* $120°$-symmetric radial triple is automatically large enough; the entire remaining
difficulty is making one of them **equilateral**, which needs
$\rho(\varphi)=\rho(\varphi+120°)=\rho(\varphi+240°)$ — two equations in one unknown $\varphi$,
and generically unsolvable. (Indeed with the $120°$ structure, $|P_1P_2|=|P_2P_3|$ already forces
$\rho_1=\rho_3$, and then equilaterality forces $\rho_2=\rho_1$ as well: the three-way equality is
the *only* way, so the deficient equation count is real and not an artefact of the parametrisation.)
That is why the working proof puts the vertex at a boundary point and varies one angle instead.

It does, however, buy a genuine special case for free:

> **Corollary R'.** If $K$ is invariant under rotation by $120°$ about a point $z$, then
> $m(K)\ge\sqrt3\,r$, with no approximation, no IVT, and no strict convexity.
>
> *Proof.* The set of inball centres is convex, compact, and invariant under that rotation, so
> its centroid is a fixed point of the rotation; the rotation has exactly one fixed point, $z$,
> so $z$ is an inball centre. Take $O=z$. Then $\rho(\varphi)=\rho(\varphi+120°)=\rho(\varphi+240°)$
> for every $\varphi$, so the triple of boundary points is equilateral, and Lemma R gives side
> $\sqrt3\,\rho(\varphi)\ge\sqrt3\,r$. $\square$

This covers the disk (equality), the equilateral triangle, the Reuleaux triangle and every
regular $3k$-gon, by an argument sharing no step with §6. It is not a proof of Theorem C, but it
is an independent confirmation on a family where a wrong theorem would plausibly have shown a
crack, and it is the kind of check §0 of the repo rules asks for.

---

## 3. Gap 2 — the closed endpoints $\pm90°$ (tried first, as instructed)

The brief's question: *does the IVT argument actually need continuity at the closed endpoint, or
can it run on a slightly smaller closed sub-interval where continuity is unproblematic?*

**Answer: it can run on a sub-interval, and that is the cleaner write-up — but the sub-interval
still needs the fact that $R$ is small near the tangent directions, which is exactly the content
of endpoint continuity. The reformulation removes two *incidental* claims and zero *substantive*
ones.** Per KILL-CRITERION K3 I say so plainly rather than presenting the move as a deletion of a
hypothesis.

Here is the accounting. `extremal-size` §6 Step 1 asserts three things at once:
(i) $\theta\mapsto A+R(\theta)u(\theta)$ is a continuous **bijection** onto $\partial K\setminus\{A\}$;
(ii) $R(\pm90°)=0$; (iii) $g$ is continuous on the **closed** interval $[-90°,30°]$.
The sub-interval route needs **none of (i)–(iii)** as stated. It needs only Lemma C and Lemma E:

> **Lemma C (interior continuity).** $R$ is continuous on $(-90°,90°)$.
>
> *Proof.* *Upper semicontinuity* holds on all of $[-90°,90°]$: if $\theta_n\to\theta_0$ and
> $R(\theta_n)\to L$ (possible after a subsequence, $R$ being bounded by $\operatorname{diam}K$),
> then $A+L\,u(\theta_0)=\lim(A+R(\theta_n)u(\theta_n))\in K$ since $K$ is closed, so
> $L\le R(\theta_0)$.
> *Lower semicontinuity* on the open cone: I claim the **open** segment $(A,\,A+R(\theta_0)u(\theta_0))$
> lies in $\operatorname{int}K$ whenever $|\theta_0|<90°$. Write $c=2r\cos\theta_0>0$ for the
> incircle chord length of Fact 2. The relative interior of a chord of a disk lies in the open
> disk, so $A+su(\theta_0)\in\operatorname{int}D(O,r)\subseteq\operatorname{int}K$ for
> $0<s<c$. For a general $t\in(0,R(\theta_0))$, put $p_0=A+R(\theta_0)u(\theta_0)\in K$ and note
> $W:=\{(1-\lambda)x+\lambda p_0:\ x\in\operatorname{int}D(O,r),\ \lambda\in[0,1)\}$ is a union of
> open sets, hence open, and $W\subseteq K$ by convexity, hence $W\subseteq\operatorname{int}K$.
> Setting $x=A+s\,u(\theta_0)$ with $s=(t-\lambda R(\theta_0))/(1-\lambda)$, the map
> $\lambda\mapsto s$ is continuous on $[0,t/R(\theta_0)]$ with $s(0)=t$ and $s(t/R(\theta_0))=0$,
> so by the IVT some $\lambda$ gives $s\in(0,c)$, i.e. $x\in\operatorname{int}D(O,r)$ and
> $A+t\,u(\theta_0)\in W\subseteq\operatorname{int}K$. Now given $\varepsilon>0$, the point
> $A+(R(\theta_0)-\varepsilon)u(\theta_0)$ is interior, so a whole ball around it lies in $K$, so
> $R(\theta)\ge R(\theta_0)-\varepsilon$ for all $\theta$ near $\theta_0$. $\square$

> **Lemma E (endpoint decay).** If $K$ is strictly convex ($\partial K$ contains no segment) and
> $A$ is as in Fact 1, then $R(\theta)\to0$ as $\theta\to\pm90°$.
>
> *Proof.* Let $H$ be the supporting line at $A$ (Fact 1). $K\cap H$ is convex and contained in
> $\partial K$, so strict convexity makes it a single point: $K\cap H=\{A\}$. Let
> $\theta_n\to90°$ with $R(\theta_n)\to L$. Then $A+L\,u(90°)=\lim(A+R(\theta_n)u(\theta_n))\in K$,
> and $A+L\,u(90°)\in H$ because $u(90°)$ spans $H$'s direction; so $A+Lu(90°)\in K\cap H=\{A\}$,
> giving $L=0$. Every subsequential limit is $0$ and $R$ is bounded, so $R(\theta)\to0$. Same at
> $-90°$. $\square$

**The sub-interval IVT.** Let $K$ be strictly convex, $A$ a contact point,
$g(\theta)=R(\theta+60°)-R(\theta)$. By Lemma E pick $\varepsilon\in(0,30°)$ with
$R(\theta)<\sqrt3\,r$ whenever $90°-\varepsilon\le|\theta|<90°$. Put $a=-90°+\varepsilon$,
$b=30°-\varepsilon$ (so $a<b$, and $[a,b]\subset(-90°,30°)$). Then, using Fact 2 and
$\cos(30°-\varepsilon)>\cos30°$:

$$R(-30°+\varepsilon)\ \ge\ 2r\cos(30°-\varepsilon)\ >\ \sqrt3\,r\ >\ R(-90°+\varepsilon)
\quad\Longrightarrow\quad g(a)>0,$$
$$R(30°-\varepsilon)\ \ge\ 2r\cos(30°-\varepsilon)\ >\ \sqrt3\,r\ >\ R(90°-\varepsilon)
\quad\Longrightarrow\quad g(b)<0.$$

$g$ is continuous on $[a,b]$ by **Lemma C alone** — every argument of $R$ involved lies in
$[-90°+\varepsilon,\,90°-\varepsilon]\subset(-90°,90°)$ — so the IVT gives
$\theta^\*\in(a,b)$ with $R(\theta^\*)=R(\theta^\*+60°)$.

**What this bought and what it did not.** Bought: no value of $R$ at $\pm90°$ is ever needed, so
claim (ii) is not used; the bijection claim (i) is not used anywhere in the lower bound and can be
deleted; continuity on a *closed* interval whose endpoints are the bad directions, claim (iii),
is not used. Not bought: Lemma E is still required, and Lemma E *is* the endpoint statement in
disguise (given $R(\pm90°)=0$, "$R\to0$" and "continuous at $\pm90°$" are the same sentence).
So **Gap 2 closes**, by Lemma E, whichever presentation is chosen — and Lemma E's proof is three
lines once one notices $K\cap H=\{A\}$ is what strict convexity actually says at a supporting
line. The round-3 examiner's Objection 1 is answered.

**And this is where Gap 1 becomes unavoidable:** Lemma E consumed strict convexity. §5 shows that
consumption is not negotiable.

---

## 4. Gap 1 — Step 0 contains a false assertion, and here is the repair

### 4.1 The error

`extremal-size` §6 Step 0 reads: *"Each $K_n$ is strictly convex (a segment in $\partial(A+B)$
needs parallel segments in $\partial A$ and $\partial B$, and $\partial D$ has none)"*, with
$K_n=K+\tfrac1nD$.

Both the parenthetical and the conclusion are wrong. The correct statement about faces of a
Minkowski sum is
$$F(A+B,u)=F(A,u)+F(B,u),$$
where $F(X,u)=\{x\in X:\langle x,u\rangle=h_X(u)\}$ is the face in direction $u$: a segment in
$\partial(A+B)$ needs a segment in **at least one** of $F(A,u)$, $F(B,u)$, not in both. And since
$F(D,u)$ is always a single point, $F(K+\varepsilon D,u)$ is a **translate of $F(K,u)$**. Hence

> **$K+\varepsilon D$ is strictly convex if and only if $K$ is.**

Minkowski summation with a disk makes the boundary $C^1$ (it removes *corners*); it does not
remove *flats*. Explicit exact witness, verified in §10 CHECK 6 with rational arithmetic: for
$K=[0,1]^2$ and $\varepsilon=1$, every point $(t,-1)$ with $t\in[0,1]$ is at distance exactly $1$
from $K$ and every point $(t,-1-\delta)$ at distance $>1$, so the whole unit segment
$[(0,-1),(1,-1)]$ lies in $\partial(K+D)$.

Smoothness would not have helped even if it had been claimed: what Lemma E needs is
$K\cap H=\{A\}$ at a contact point, and the rounded square has a perfectly smooth boundary with a
flat bottom whose midpoint is an incircle contact point.

### 4.2 The repair

> **Lemma S (strictly convex outer approximation).** Let $K$ be a convex body with
> $0\in\operatorname{int}K$ and $D(0,a)\subseteq K\subseteq D(0,b)$. Let $\gamma=\gamma_K$ be the
> gauge, $\gamma(x)=\inf\{t>0:x\in tK\}$, so $K=\{\gamma\le1\}$. For $\varepsilon\in(0,1)$ put
> $$q_\varepsilon(x)=(1-\varepsilon)\,\gamma(x)^2+\varepsilon\,|x|^2/b^2,\qquad
> K_\varepsilon=\{q_\varepsilon\le1\}.$$
> Then $K_\varepsilon$ is a **strictly convex** body and
> $$K\ \subseteq\ K_\varepsilon\ \subseteq\ (1-\varepsilon)^{-1/2}K .$$
>
> *Proof.* $\gamma$ is convex, nonnegative and positively homogeneous, so $\gamma^2$ is convex
> ($t\mapsto t^2$ is convex increasing on $[0,\infty)$); $|x|^2$ is strictly convex; a positive
> combination of a convex and a strictly convex function is strictly convex. $q_\varepsilon$ is
> continuous, homogeneous of degree $2$, and $q_\varepsilon(x)\ge\varepsilon|x|^2/b^2$, so
> $K_\varepsilon$ is compact, convex, with $0$ in its interior. If $x\ne y$ lie in $K_\varepsilon$
> then $q_\varepsilon(\tfrac{x+y}2)<\tfrac12(q_\varepsilon(x)+q_\varepsilon(y))\le1$, so the
> midpoint is interior; hence $\partial K_\varepsilon$ contains no segment, i.e.
> $K_\varepsilon$ is strictly convex. For the inclusions: $x\in\gamma(x)K\subseteq\gamma(x)D(0,b)$
> gives $|x|/b\le\gamma(x)$, hence $q_\varepsilon\le(1-\varepsilon)\gamma^2+\varepsilon\gamma^2=\gamma^2$
> and $K=\{\gamma\le1\}\subseteq K_\varepsilon$; and $q_\varepsilon\ge(1-\varepsilon)\gamma^2$
> gives $K_\varepsilon\subseteq\{\gamma\le(1-\varepsilon)^{-1/2}\}=(1-\varepsilon)^{-1/2}K$.
> $\square$

Consequences, all immediate from the two inclusions with $\lambda_n=(1-1/n)^{-1/2}\downarrow1$
and $K_n:=K_{1/n}$: $d_H(K_n,K)\le(\lambda_n-1)b\to0$; $r(K_n)\ge r(K)=r$ (since $K\subseteq K_n$);
and $K\subseteq K_n$ for every $n$, which is what the limit step needs.

*(An alternative repair, if one prefers a geometric construction: the ball hull
$K^{(\rho)}=\bigcap\{D(x,\rho):K\subseteq D(x,\rho)\}$ is strictly convex — every boundary point
lies on one of the spheres, by a compactness argument on the admissible centres, and a segment in
$\partial K^{(\rho)}$ would be a segment inside a circle — and $K^{(\rho)}\downarrow K$ as
$\rho\to\infty$. I use the gauge version above because its two inclusions are one line each and
give the Hausdorff and inradius statements without further work.)*

### 4.3 The limit step is correct as written — re-derived

> **Lemma L0.** Suppose $K\subseteq K_n$ for all $n$, $d_H(K_n,K)\to0$, $v_n\in\partial K_n$, and
> $v_n\to v$. Then $v\in\partial K$.
>
> *Proof.* $\operatorname{dist}(v_n,K)\le d_H(K_n,K)\to0$ and $K$ is closed, so $v\in K$. If
> $v\in\operatorname{int}K$, pick $\delta>0$ with $D(v,\delta)\subseteq K\subseteq K_n$ for every
> $n$. For $n$ large, $|v_n-v|<\delta/2$, so $D(v_n,\delta/2)\subseteq D(v,\delta)\subseteq K_n$,
> making $v_n$ an interior point of $K_n$ — contradicting $v_n\in\partial K_n$. $\square$

So the round-3 examiner's specific worry ("did not independently prove the claim that vertex
limits land on $\partial K$ rather than merely in $K$") is now closed: the claim is true, its
proof needs $K\subseteq K_n$, and the gauge smoothing supplies that.

### 4.4 The brief's question about $m(\cdot)$ under Hausdorff convergence

*Is $m$ continuous, or only semicontinuous, and is the direction I need the direction I get?*

What Lemma L0 delivers is the **outer-approximation half**: if $K\subseteq K_n\to K$ then any
limit of triangles inscribed in $K_n$ is inscribed in $K$, hence
$\limsup_n m(K_n)\le m(K)$. **That is exactly the direction needed**, because the lower bound is
proved *for the approximants* ($m(K_n)\ge\sqrt3\,r(K_n)\ge\sqrt3\,r$) and transported *down* to
$K$. The opposite direction ($m(K)\le\liminf m(K_n)$, i.e. lower semicontinuity) is neither
established nor needed here, and I make no claim about it.

The classic failure mode — a limit of nondegenerate inscribed triangles degenerating — **is
genuinely avoided**, and `extremal-size` handled that part correctly: the noncollapse bound
$\sqrt3\,r>0$ is uniform in $n$ and is established *before* the limit is taken, exactly as
[`../../RULES.md`](../../RULES.md) §2 demands. Side lengths converge, so the limit triangle is
equilateral of side $\ge\sqrt3\,r>0$. The bug in Step 0 was never the noncollapse discipline; it
was the one-line assertion about which bodies $K+\varepsilon D$ are.

---

## 5. Step 0 is load-bearing: an exact convex body where the criterion returns nothing

Could one skip the reduction and run Steps 1–3 on a general convex body? No. Here is an explicit,
exactly-specified convex body and an explicit incircle contact point at which the zero set of $g$
is **empty**.

Fix $M>0$ and let
$$K_M=\operatorname{conv}\bigl(D((0,1),1)\ \cup\ \{(M,0)\}\bigr),\qquad A=(0,0),\ \nu=(0,1).$$

*Setup, all exact.* $K_M\subseteq\{0\le y\le2\}$ (both generators are), so every inscribed disk
has radius $\le1$; and $D((0,1),1)\subseteq K_M$; so $r(K_M)=1$ and $D((0,1),1)$ is a largest
inscribed disk with $A=(0,0)$ one of its contact points. The two tangent lines from $(M,0)$ to the
circle touch it at $(0,0)$ and at
$$T=\Bigl(\tfrac{2M}{M^2+1},\ \tfrac{2M^2}{M^2+1}\Bigr),$$
both with $x\ge0$; hence $K_M\cap\{x<0\}=D((0,1),1)\cap\{x<0\}$. The boundary is: the segment
$[(0,0),(M,0)]$, the segment $[(M,0),T]$, and the circular arc from $T$ counterclockwise back to
$(0,0)$. Writing $\psi_T$ for the angle of $T$ from $\nu$, one gets $\tan\psi_T=1/M$, and the
outer tangent line is $\hat n\cdot x=p$ with $\hat n=(2M,M^2-1)/(M^2+1)$, $p=2M^2/(M^2+1)$, so
that $\hat n\cdot u(\psi)=\cos(\psi-2\psi_T)$ (using $\tan2\psi_T=2M/(M^2-1)$). Therefore

$$R(\theta)=\begin{cases}2\cos\theta, & -90°\le\theta\le\psi_T\quad(\text{exit on the arc}),\\[2pt]
\dfrac{2M^2}{(M^2+1)\cos(\theta-2\psi_T)}, & \psi_T\le\theta\le90°\quad(\text{exit on }[T,(M,0)]).\end{cases}$$

The two branches agree at $\theta=\psi_T$ (both give $2M/\sqrt{M^2+1}$), and at $\theta=90°$ the
second gives $R(90°)=M$, the spike tip. **CHECK 4** of §10 re-derives this branch formula against
an independent exact convex-hull membership oracle (the quadratic-in-$\lambda$ test for
$x\in\operatorname{conv}(D\cup\{P\})$) at 80 rational directions, confirming in each case that the
predicted exit point is in $K_M$ and that $(1+10^{-6})$ times it is not.

**(a) The endpoint sign hypothesis of Step 2 fails outright.** For every $M>4/\sqrt3$:

$$g(-90°)=R(-30°)-R(-90°)=\sqrt3-0>0,\qquad
g(30°)=R(90°)-R(30°)=M-R(30°)\ \ge\ M-\tfrac4{\sqrt3}>0,$$

using $R(-30°)=2\cos30°=\sqrt3$ exactly (the ray at $-30°$ has $x<0$, where $K_M$ *is* the disk),
$R(-90°)=0$, $R(90°)=M$, and $R(30°)\le4/\sqrt3$ (because $K_M\subseteq\{y\le2\}$ forces
$t\cos30°\le2$). **Both endpoint values are strictly positive**, so `extremal-size` §6 Step 2's
"$g(-90°)>0$ and $g(30°)<0$" is simply false here. Verified exactly at $M=3$ and $M=100$ in §10
CHECK 2.

**(b) At $M=100$ the zero set is empty.** With $r=1$, $\psi_T=\arctan(1/100)<0.01\ \mathrm{rad}<0.6°$
(using $\arctan x<x$), so $2\psi_T<1.2°$. Split $[-90°,30°]$ into four pieces:

- $\theta\in[-90°,\ \psi_T-60°]$: both $\theta$ and $\theta+60°$ are on the arc branch, so
  $g=2\bigl(\cos(\theta+60°)-\cos\theta\bigr)=-2\sin(\theta+30°)>0$, since
  $\theta+30°\in[-60°,\psi_T-30°]$ is strictly negative.
- $\theta\in[\psi_T-60°,\ -30°]$: $R(\theta)=2\cos\theta\le2\cos30°=\sqrt3$, while
  $\theta+60°\in[\psi_T,30°]$ gives $R(\theta+60°)\ge\frac{2M^2}{M^2+1}=\frac{20000}{10001}>\sqrt3$
  (as $20000^2=4\cdot10^8>3\cdot10001^2=300\,060\,003$). So $g>0$.
- $\theta\in[-30°,\ \psi_T]$: $R(\theta)=2\cos\theta$ and
  $R(\theta+60°)=\frac{2M^2}{(M^2+1)\cos(\theta+60°-2\psi_T)}$, so $g>0$ is equivalent to
  $\frac{M^2}{M^2+1}>\cos\theta\cos(\theta+60°-2\psi_T)$. The right side is maximised over
  $\theta$ at $\theta=-(30°-\psi_T)$, which lies in the interval, with value
  $\cos^2(30°-\psi_T)$. Now $30°-\psi_T>29.4°>0.51\ \mathrm{rad}$ and
  $\cos x\le1-\tfrac{x^2}2+\tfrac{x^4}{24}$ give $\cos^2(30°-\psi_T)<0.873^2<0.77$, while
  $\frac{M^2}{M^2+1}=\frac{10000}{10001}>0.9999$. So $g>0$.
- $\theta\in[\psi_T,\ 30°]$: both on the tangent branch, where
  $R(\psi)=\frac{2M^2}{(M^2+1)\cos(\psi-2\psi_T)}$ is strictly increasing in $|\psi-2\psi_T|$ on
  $|\psi-2\psi_T|<90°$. Here $|\theta-2\psi_T|\le30°$ while
  $|\theta+60°-2\psi_T|\ge60°-\psi_T>59.4°$ and $\le90°-2\psi_T<90°$. So $g>0$.

Hence $g>0$ on all of $[-90°,30°]$ and $Z=\emptyset$: **the Step-1/2/3 machinery, applied at this
genuine incircle contact point of this genuine convex body, produces no triangle at all.** §10
CHECK 1 corroborates on 4038 exactly-represented directions in $\mathbb{Q}(\sqrt3)$ (the case
analysis above is the decision; the sweep is the safety net).

**(c) Step 2's "iff" is false.** $A=(0,0)$ nevertheless *is* a vertex of an inscribed equilateral
triangle of $K_{100}$: take $B=(R(30°),0)$ on the bottom segment and $C=R(30°)\,u(30°)$ on
$[T,(M,0)]$, with $R(30°)=\frac{-8000000+399960000\sqrt3}{299900003}\approx2.2833$ (exact value
from §10 CHECK 2). The triangle $ABC$ is equilateral of side $\approx2.2833\ge\sqrt3$. The
criterion misses it because $B$ is **not** the far intersection of its ray with $K$ — the whole
segment $[(0,0),(M,0)]$ lies in $\partial K$, so a ray can meet $\partial K$ in a continuum, and
"$R(\theta)=R(\theta+60°)$" is sufficient (Fact 3) but not necessary. **Theorem C itself is
unharmed here**; what fails is the criterion.

**(d) The phenomenon is real but not generic.** At $M=3$ the endpoint signs are still both
positive, yet $g$ *does* change sign in the interior (§10 CHECK 3 finds it at
$\tan\theta\in[-9/20,0]$, two crossings rather than none), so a zero exists anyway. The unit
square (§7) has both endpoint signs behaving as Step 2 wants, despite not being strictly convex.
So non-strict-convexity does not always break the argument — which is exactly why a witness was
needed rather than an appeal to intuition, and why the reduction cannot be waved away as
"standard".

---

## 6. The repaired proof, end to end

> **Theorem C.** Every planar convex body $K$ with inradius $r$ inscribes an equilateral triangle
> of side $\ge\sqrt3\,r$. Equality holds for the disk.
> *(Status `sketch`. Mine. Not assumable, including by me.)*

**Step 0 (reduce to strictly convex).** Translate so $0\in\operatorname{int}K$ and take
$D(0,a)\subseteq K\subseteq D(0,b)$. Let $K_n=K_{1/n}$ be the gauge smoothing of Lemma S: each is
strictly convex, $K\subseteq K_n\subseteq(1-1/n)^{-1/2}K$, $d_H(K_n,K)\to0$, $r(K_n)\ge r$.
Suppose the theorem holds for strictly convex bodies. Then each $K_n$ has an inscribed equilateral
triangle $T_n$ of side $s_n\ge\sqrt3\,r(K_n)\ge\sqrt3\,r$ — **a noncollapse bound uniform in $n$
and established before any limit is taken**. The vertices lie in $(1-1/n)^{-1/2}K$, a bounded set,
so a subsequence has all three vertices converging; by Lemma L0 each limit lies on $\partial K$;
side lengths converge, so the limit triangle is equilateral with side $\ge\sqrt3\,r>0$, in
particular nondegenerate. Hence it suffices to treat strictly convex $K$.

**Step 1 (the radial picture).** Let $D(O,r)$ be a largest inscribed disk, $A$ a contact point,
$\nu,\,u(\theta),\,R(\theta)$ as in §1. Fact 1 gives $K\subseteq\{\langle\cdot-A,\nu\rangle\ge0\}$
and a $180°$ direction cone; Fact 2 gives $R(\theta)\ge2r\cos\theta$; Lemma C gives continuity of
$R$ on $(-90°,90°)$; Lemma E gives $R(\theta)\to0$ as $\theta\to\pm90°$. *(No bijection claim and
no value of $R$ at $\pm90°$ is used.)*

**Step 2 (IVT on a compact sub-interval).** Choose $\varepsilon\in(0,30°)$ with $R(\theta)<\sqrt3\,r$
for $90°-\varepsilon\le|\theta|<90°$ (Lemma E). On $[a,b]=[-90°+\varepsilon,\,30°-\varepsilon]$ the
function $g(\theta)=R(\theta+60°)-R(\theta)$ is continuous (Lemma C, since every argument lies in
$[-90°+\varepsilon,90°-\varepsilon]$), and $g(a)>0>g(b)$ by the two displayed inequalities of §3.
So $g(\theta^\*)=0$ for some $\theta^\*\in(-90°,30°)$; write $s=R(\theta^\*)=R(\theta^\*+60°)$.

**Step 3 (the size, simplified — no auxiliary $\beta$).** Suppose $s<\sqrt3\,r$. Both
$\theta^\*$ and $\theta^\*+60°$ lie in $(-90°,90°)$, so Fact 2 applies to each:
$2r\cos\theta^\*\le s<\sqrt3\,r$ and $2r\cos(\theta^\*+60°)\le s<\sqrt3\,r$, i.e.
$\cos\theta^\*<\tfrac{\sqrt3}2$ and $\cos(\theta^\*+60°)<\tfrac{\sqrt3}2$, i.e.
$|\theta^\*|>30°$ and $|\theta^\*+60°|>30°$. From $\theta^\*<30°$ and $|\theta^\*|>30°$ we get
$\theta^\*<-30°$; but then $\theta^\*+60°<30°$, so $|\theta^\*+60°|>30°$ forces
$\theta^\*+60°<-30°$, i.e. $\theta^\*<-90°$, contradicting $\theta^\*>-90°$. Hence
$s\ge\sqrt3\,r$.

**Conclusion.** By Fact 3, $A$, $A+s\,u(\theta^\*)$, $A+s\,u(\theta^\*+60°)$ are three points of
$\partial K$ forming an equilateral triangle of side $s\ge\sqrt3\,r>0$. Combined with Step 0 this
holds for every convex body. **Sharpness:** for $K=D(O,r)$, three points on the circle are
equilateral only if the circle is their circumcircle, so every inscribed equilateral triangle has
side exactly $\sqrt3\,r$. $\square$

**Where each hypothesis is spent** ([`../../RULES.md`](../../RULES.md) §1.3): convexity in Fact 1
(supporting line), Fact 2 (the incircle is inside), Lemma C (the segment-to-interior argument) and
Lemma L0; compactness in the existence of $R$, of the contact point and of the limit; strict
convexity **only** in Lemma E, and only after Step 0 has arranged it. There is no undeclared
regularity: no tangent, no arc length, no "finitely many" anything, no rectifiability.

**What is still not proved to a promotable standard.** Everything above is one model's derivation.
It has not been examined by a different model family, so it stays `sketch`
([`../../../../RULES.md`](../../../../RULES.md) §3, §5), and its Lean prospects are poor for a
different reason than usual: the obstruction is not the Jordan curve theorem (this argument never
uses it) but the amount of convex-geometry API — gauges, faces of Minkowski sums, Hausdorff
convergence of convex bodies — that the repair leans on. A reviewer who wants to attack it should
start at Lemma S (is $K_\varepsilon$ really strictly convex, and are the inclusions the right way
round?) and at Lemma C (the $W$-open argument), which are the two places I would put an error if I
had made one.

---

## 7. The three filters ([`../../RULES.md`](../../RULES.md) §3) — all run

**§3.1 wedge test.** The wedge test says: if all of $K$ lies in a closed cone of half-angle
$<30°$ at $O\in\partial K$, then no inscribed equilateral triangle has a vertex at $O$. The
argument above is structurally immune, and this is worth stating rather than assuming: the vertex
$A$ is always an **incircle contact point**, where Fact 1 gives a direction cone of exactly $180°$
— the largest possible. So the test can never fire at the point the proof uses. Conversely the
test is a genuine constraint on any *strengthening* of Theorem C to "every boundary point is a
vertex of a large triangle": the $30°$-$30°$-$120°$ triangle has two boundary points where no
inscribed equilateral triangle has a vertex at all, so **no vertex-wise version of Theorem C can
be true**, and nothing here claims one. (Consistency check: at either $30°$ apex of that body the
incircle contact points are elsewhere, on the three edges, so the theorem and the test coexist.)

**§3.2 square contrast.** Replace $60°$ by $90°$ and the argument dies at Fact 3, which is where
its whole content sits. Two rays from $A$ at $60°$ with equal lengths $s$ close up into an
equilateral triangle *automatically*: the third side is forced to be $s$ by the isosceles-with-
$60°$-apex identity, so **three** points and **one** scalar equation $R(\theta)=R(\theta+60°)$
suffice, and one equation is exactly what a one-parameter IVT can deliver. Two rays from $A$ at
$90°$ with equal lengths give a right isosceles triangle; the square's **fourth** vertex
$A+s\,u(\theta)+s\,u(\theta+90°)$ is then completely determined and is under **no** constraint to
lie on $\partial K$ — a second equation with no second parameter. The IVT count fails, and no
amount of repairing Step 0 or Lemma E changes it. Additionally, Step 3's arithmetic is specific to
$60°$: it needs $\theta$ and $\theta+60°$ to be unable to be simultaneously $\ge30°$ away from
$0°$ inside a $120°$-long window, which is a statement about the numbers $30$, $60$, $90$ and is
false for the corresponding $90°$ configuration. **This lane does not transfer to squares, and
does not bear on the square peg problem.**

**§3.3 polygon control.** The construction and the bound were checked exactly in
$\mathbb{Q}(\sqrt3)$ on two polygons (§10 CHECK 5), both chosen because they are *not* strictly
convex and so probe the very failure mode of §5:

- **Unit square** $[0,1]^2$: $r=\tfrac12$, contact point $A=(\tfrac12,0)$. At $\theta=-30°$,
  $R(-30°)=R(30°)=1$ exactly, giving the equilateral triangle
  $(\tfrac12,0),(0,\tfrac{\sqrt3}2),(1,\tfrac{\sqrt3}2)$ of side $1\ge\sqrt3\,r=\tfrac{\sqrt3}2$.
  Note the endpoint signs here are $g(-90°)=\tfrac12>0>g(30°)=-\tfrac12$: Step 2's hypothesis
  holds despite the square not being strictly convex.
- **Equilateral triangle** with vertices $(\pm\sqrt3,0),(0,3)$: $r=1$, $A=(0,0)$. Here
  $g(-90°)=g(30°)=0$: the endpoints themselves are zeros, and the one at $\theta=-90°$ yields the
  triangle $(0,0),(-\sqrt3,0),(-\tfrac{\sqrt3}2,\tfrac32)$ of side exactly $\sqrt3=\sqrt3\,r$ —
  the construction is **tight** here, even though $m(K)=2\sqrt3$ for this body (it inscribes
  itself). A second reason the closed-endpoint question was not idle.

A claim that survives polygons is *merely not-yet-dead* (§3.3), and I make no more of it than
that. The two polygons above were selected adversarially, not for convenience: both are bodies on
which the strictly-convex reduction is doing work.

---

## 8. Kill-criterion outcomes

| Condition | Outcome |
|---|---|
| **K1** convex counterexample to Theorem C | **Not met.** No counterexample found; §2's Corollary R' and §7's polygon checks are positive evidence, not proof. I ran the search honestly — §5's body was built *trying* to break the theorem and broke only the criterion. |
| **K2** Step 0 unrepairable + machinery fails | **Half met, and reported as such.** The machinery genuinely fails on a convex body (§5) — so the second clause fired — but Step 0 *is* repairable (Lemma S), so the lane did not stop. Recorded as a located error plus a fix, per K2's own wording. |
| **K3** sub-interval route only relocates the difficulty | **Met, and reported.** §3 states plainly that the sub-interval removes claims (i)–(iii) but not Lemma E, rather than presenting it as a deleted hypothesis. |
| **K4** ten-minute cap on replacing the approach | **Respected.** Containment route `refuted` for a stated reason; one further attempt (Lemma R) made, which failed to give the general theorem for a counted reason (two equations, one unknown) and was stopped. It did yield Corollary R'. |
| **K5** compute budget | **Far under.** All computation is exact evaluation of closed forms; total runtime under a second. No background jobs started, none left running. |
| **K6** scope | **Respected.** Three files written, none outside them. Corrections to `../extremal-size/` are requested in §9, not applied. |

---

## 9. Correction requests for [`../extremal-size/`](../extremal-size/) — **not applied here**

For whoever holds that file (I do not, and did not touch it):

1. **§6 Step 0, first sentence — factual error.** "Each $K_n$ is strictly convex (a segment in
   $\partial(A+B)$ needs parallel segments in $\partial A$ and $\partial B$...)" is false in both
   halves. $F(A+B,u)=F(A,u)+F(B,u)$, so a segment is needed in only **one** summand, and
   $K+\varepsilon D$ is strictly convex iff $K$ is. Suggested replacement: Lemma S of §4.2 above
   (or the ball hull). The rest of Step 0 — including the "limit lies on $\partial K$" argument —
   is **correct** and survives verbatim, because the replacement also satisfies $K\subseteq K_n$.
2. **§6 Step 2 — "iff" is false.** "$A$ is a vertex of an inscribed equilateral triangle of side
   $s$ **iff** $R(\theta)=R(\theta+60°)=s>0$" holds only for strictly convex $K$; §5(c) gives a
   convex body where the left side is true and the right side has no solution at all. Only the
   "if" direction is used, so the proof is unaffected — but a reader could reasonably use the
   stated equivalence elsewhere, and it would be wrong.
3. **§6 Step 1 — two claims that are not needed and are not proved as stated.** The "continuous
   bijection onto $\partial K\setminus\{A\}$" and the closed-endpoint continuity can both be
   dropped in favour of Lemma C + Lemma E + the sub-interval IVT (§3), which is shorter and has
   no unproved step.
4. **§6 Step 3 — simplification available.** The auxiliary $\beta=\arccos(c/2r)$ and the maximum
   over $Z$ are unnecessary: *every* zero of $g$ in $[-90°,30°]$ has $R\ge\sqrt3\,r$ directly
   (§6 Step 3 above), which also removes the need for $Z$ to be compact.
5. **§5 Conjecture I, a remark not a correction.** The equality discussion says the disk is the
   equality case for Theorem C. That is right for $m(K)=\sqrt3\,r$, but the *construction* is also
   exactly tight at the equilateral triangle (§7), where $m(K)=2\sqrt3\,r$; anyone tempted to read
   an equality-case rigidity statement out of the proof should not.

---

## 10. Reproducing the exact checks

This lane owns three files and may not create anything under `experiments/`, so the checker is
reproduced in full below rather than committed as a script. Save it as `verify.py` and run
`python3 verify.py` (Python 3, standard library only — `fractions`; **no numpy, no sympy, no
floating point anywhere, and no library geometry predicate**, per
[`../../RULES.md`](../../RULES.md) §5 and this session's standing warning that a failing checker
is far likelier than a mathematical error of this kind). It prints one line per check and asserts
on failure. Version pinning is vacuous — only `fractions.Fraction` is used, and
$\mathbb{Q}(\sqrt3)$ with its exact sign test is implemented from scratch in the file.

Output on 2026-08-30 (Python 3, exit 0):

```
CHECK 1  K_100, A=(0,0):  sampled directions with g<=0 : []
CHECK 1  sign g(+30 deg) = 1    sign g(-30 deg) = 1
CHECK 2  M=3: R(-30)=(0+1*sqrt3) (=sqrt3? True), R(+30)=(-18/13+24/13*sqrt3), R(+90)=(3+0*sqrt3)
         g(-90) = R(-30) - 0  > 0 : True;  g(+30) = R(+90)-R(+30) > 0 : True
CHECK 2  M=100: R(-30)=(0+1*sqrt3) (=sqrt3? True), R(+30)=(-8000000/299900003+399960000/299900003*sqrt3), R(+90)=(100+0*sqrt3)
         g(-90) = R(-30) - 0  > 0 : True;  g(+30) = R(+90)-R(+30) > 0 : True
CHECK 3  M=3: sampled slopes tan(theta) with g<0 : 10 of them, from -9/20 to 0
CHECK 4  branch formula agrees with the hull-membership oracle at 80 rational directions (exit in K, (1+1e-6)*exit not in K)
CHECK 5a unit square: (True, True, (1+0*sqrt3), (3/4+0*sqrt3), 1)
CHECK 5b equilateral triangle: (True, (3+0*sqrt3), True)
CHECK 6  segment [(0,-1),(1,-1)] lies in the boundary of [0,1]^2 + D : True

ALL EXACT CHECKS PASSED
```

**What each check decides, and what it does not.** CHECK 1 is a *sweep*, and a sweep of a
continuum by finitely many samples proves nothing on its own — the decision that $Z=\emptyset$ for
$K_{100}$ is the four-case analysis in §5(b), and CHECK 1 exists to catch an algebra slip in that
analysis. CHECK 2, 5 and 6 are exact evaluations of closed-form quantities and do decide their
statements. CHECK 3 exhibits sign changes and so is a positive existence statement, decided. CHECK
4 is the one genuinely independent cross-check: the branch formula for $R$ is compared against a
convex-hull membership oracle sharing no code with it. All of this is `numerical` in the sense of
[`../../../../RULES.md`](../../../../RULES.md) §3 and is never a proof step.

```python
#!/usr/bin/env python3
"""
extremal-gap-closure : exact checks.  Python 3 stdlib only (fractions).
No float anywhere.  No sympy.  No geometry predicate from any library.

Field Q(sqrt3) implemented from scratch as pairs (p,q) meaning p + q*sqrt3.
Sign decision is exact: sign(p+q*sqrt3) from sign(p), sign(q), and p^2 vs 3q^2.
"""
from fractions import Fraction as F

# ---------------------------------------------------------------- Q(sqrt3)
class S:
    __slots__ = ("p", "q")
    def __init__(self, p=0, q=0):
        self.p = F(p); self.q = F(q)
    def __add__(a, b): b = S.c(b); return S(a.p + b.p, a.q + b.q)
    def __radd__(a, b): return S.c(b) + a
    def __sub__(a, b): b = S.c(b); return S(a.p - b.p, a.q - b.q)
    def __rsub__(a, b): return S.c(b) - a
    def __neg__(a): return S(-a.p, -a.q)
    def __mul__(a, b):
        b = S.c(b)
        return S(a.p * b.p + 3 * a.q * b.q, a.p * b.q + a.q * b.p)
    def __rmul__(a, b): return S.c(b) * a
    def inv(a):
        d = a.p * a.p - 3 * a.q * a.q
        assert d != 0, "zero divisor"
        return S(a.p / d, -a.q / d)
    def __truediv__(a, b): return a * S.c(b).inv()
    def __rtruediv__(a, b): return S.c(b) * a.inv()
    @staticmethod
    def c(x): return x if isinstance(x, S) else S(x, 0)
    def sign(a):
        # exact sign of p + q*sqrt3
        if a.p == 0 and a.q == 0: return 0
        if a.p >= 0 and a.q >= 0: return 1
        if a.p <= 0 and a.q <= 0: return -1
        # opposite signs: compare p^2 with 3q^2
        d = a.p * a.p - 3 * a.q * a.q
        if a.p > 0:   # q < 0 : positive iff p^2 > 3q^2
            return 1 if d > 0 else (-1 if d < 0 else 0)
        else:         # p < 0, q > 0 : positive iff 3q^2 > p^2
            return -1 if d > 0 else (1 if d < 0 else 0)
    def __lt__(a, b): return (a - S.c(b)).sign() < 0
    def __gt__(a, b): return (a - S.c(b)).sign() > 0
    def __eq__(a, b): d = a - S.c(b); return d.p == 0 and d.q == 0
    def __repr__(a): return f"({a.p}+{a.q}*sqrt3)"

RT3 = S(0, 1)
HALF = S(F(1, 2), 0)
assert (RT3 * RT3) == S(3, 0)
assert RT3.sign() == 1 and (S(2, 0) - RT3).sign() == 1 and (S(1, 0) - RT3).sign() == -1
assert (S(20000, 0) / S(10001, 0) - RT3).sign() == 1        # 20000/10001 > sqrt3

def rot60(v):
    """u(theta) = (sin t, cos t)  ->  u(theta+60) = (a/2 + b*sqrt3/2, b/2 - a*sqrt3/2)."""
    a, b = v
    return (a * HALF + b * RT3 * HALF, b * HALF - a * RT3 * HALF)

# --------------------------------------------- the body K_M = conv(D((0,1),1) u {(M,0)})
# A = (0,0) is an incircle contact point; r = 1 since K_M is contained in 0 <= y <= 2.
# boundary: arc of the circle from T counterclockwise to A ; segment [T,P] ; segment [P,A].
# T = (2M/(M^2+1), 2M^2/(M^2+1)), P = (M,0), tangent line n.x = p with
# n = (2M, M^2-1)/(M^2+1), p = 2M^2/(M^2+1).
# For a direction v = (a,b) with b > 0 (i.e. |theta| < 90):
#     exit on the arc            iff  M*a <= b        (theta <= psi_T, tan psi_T = 1/M)
#     s_max = 2b/(a^2+b^2)                      [arc branch]
#     s_max = 2M^2/(2M*a + (M^2-1)*b)           [tangent-segment branch]
# and R = s_max * |v|.  Comparing R for two directions of EQUAL length reduces to comparing s_max.

def smax(v, M):
    a, b = v
    assert b.sign() >= 0, "direction must have b>=0 (|theta| <= 90)"
    if b.sign() == 0:
        # theta = +-90 : along the supporting line y = 0.  a>0 exits at (M,0); a<0 exits at A.
        return S(M, 0) / a if a.sign() > 0 else S(0, 0)
    if (S(M, 0) * a - b).sign() <= 0:
        return S(2, 0) * b / (a * a + b * b)
    return S(2 * M * M, 0) / (S(2 * M, 0) * a + S(M * M - 1, 0) * b)

def g_sign(v, M):
    """sign of g(theta) = R(theta+60) - R(theta) for the direction v = u(theta)."""
    v2 = rot60(v)
    return (smax(v2, M) - smax(v, M)).sign()

# ------------- independent membership oracle for K_M, rational directions, no formula reuse
def in_KM(x, y, M):
    """exact test: is (x,y) in conv(D((0,1),1) u {(M,0)}) ?   x,y,M rational.
    point = (1-l)*d + l*P with |d-C|<=1  <=>  exists l in [0,1] with
    |(x,y) - l*P - (1-l)*C|^2 <= (1-l)^2 .  Quadratic in l; check its minimum on [0,1]."""
    x = F(x); y = F(y); M = F(M)
    # (x - l*M)^2 + (y - (1-l))^2 - (1-l)^2 = M^2 l^2 + (-2xM + 2y) l + (x^2 + y^2 - 2y)
    A2 = M * M
    A1 = -2 * x * M + 2 * y
    A0 = x * x + y * y - 2 * y
    def val(l): return A2 * l * l + A1 * l + A0
    cands = [F(0), F(1)]
    if A2 != 0:
        lstar = -A1 / (2 * A2)
        if 0 < lstar < 1: cands.append(lstar)
    return min(val(l) for l in cands) <= 0

# --------------------------------------------------------------------- CHECK 1
# K_100 at A=(0,0): g(theta) > 0 for every theta in [-90,30]  =>  the zero set Z is EMPTY,
# so extremal-size Step 2's criterion produces no triangle at this incircle contact point.
def check1():
    M = 100
    bad = []
    slopes = []
    n = 4000
    for i in range(-n, n + 1):
        slopes.append(F(i, 40))                      # tan theta in [-100, 100] step 1/40
    slopes += [F(-10**k) for k in range(2, 9)]       # theta -> -90 deg
    slopes += [F(-10**k) + F(1, 7) for k in range(2, 9)]
    for t in slopes:
        v = (S(t, 0), S(1, 0))
        if (S(t, 0) - RT3 / S(3, 0)).sign() > 0:     # keep theta <= 30 deg
            continue
        if g_sign(v, M) <= 0:
            bad.append(t)
    v30 = (HALF, RT3 * HALF)                         # theta = +30 deg exactly
    vm30 = (-HALF, RT3 * HALF)                       # theta = -30 deg exactly
    return bad, g_sign(v30, M), g_sign(vm30, M)

bad, s30, sm30 = check1()
print("CHECK 1  K_100, A=(0,0):  sampled directions with g<=0 :", bad)
print("CHECK 1  sign g(+30 deg) =", s30, "   sign g(-30 deg) =", sm30)
assert bad == [] and s30 > 0 and sm30 > 0

# --------------------------------------------------------------------- CHECK 2
# the two endpoint values of extremal-size Step 2, exactly, for K_M:
#   g(-90) = R(-30) - R(-90) = sqrt3 - 0 > 0      (STRICTLY POSITIVE)
#   g(+30) = R(+90) - R(+30) = M - R(30) > 0      (STRICTLY POSITIVE for M > 4/sqrt3)
# so BOTH endpoint values are positive and the sign hypothesis of the IVT fails outright.
def check2(M):
    vm30 = (-HALF, RT3 * HALF); v30 = (HALF, RT3 * HALF)   # unit vectors, so R = s_max
    return smax(vm30, M), smax(v30, M), S(M, 0)

for M in (3, 100):
    R_m30, R_p30, R_p90 = check2(M)
    print(f"CHECK 2  M={M}: R(-30)={R_m30} (=sqrt3? {R_m30 == RT3}), "
          f"R(+30)={R_p30}, R(+90)={R_p90}")
    print(f"         g(-90) = R(-30) - 0  > 0 : {R_m30.sign() > 0};  "
          f"g(+30) = R(+90)-R(+30) > 0 : {(R_p90 - R_p30).sign() > 0}")
    assert R_m30 == RT3
    assert R_m30.sign() > 0 and (R_p90 - R_p30).sign() > 0

# --------------------------------------------------------------------- CHECK 3
# M = 3 : the endpoint signs still both fail, but g DOES change sign inside.
def check3():
    M = 3
    neg = []
    for t in [F(i, 20) for i in range(-200, 12)]:
        v = (S(t, 0), S(1, 0))
        if (S(t, 0) - RT3 / S(3, 0)).sign() > 0: continue
        if g_sign(v, M) < 0: neg.append(t)
    return neg

neg3 = check3()
print("CHECK 3  M=3: sampled slopes tan(theta) with g<0 :",
      f"{len(neg3)} of them, from {min(neg3)} to {max(neg3)}" if neg3 else "NONE")
assert neg3

# --------------------------------------------------------------------- CHECK 4
# independent verification of the branch formula against the convex-hull membership oracle.
def check4():
    M = 3
    eps = F(1, 10**6)
    tested = 0
    for t in [F(i, 13) for i in range(-60, 20)]:
        v = (S(t, 0), S(1, 0))
        s = smax(v, M)
        assert s.q == 0, "rational direction should give rational s"
        s = s.p
        x, y = s * t, s
        assert in_KM(x, y, M), f"exit point not in K at slope {t}"
        assert not in_KM(x * (1 + eps), y * (1 + eps), M), f"beyond-exit point in K at slope {t}"
        assert in_KM(x * (1 - eps), y * (1 - eps), M)
        tested += 1
    return tested

print("CHECK 4  branch formula agrees with the hull-membership oracle at",
      check4(), "rational directions (exit in K, (1+1e-6)*exit not in K)")

# --------------------------------------------------------------------- CHECK 5
# the repaired construction on two polygons (problem RULES.md 3.3), exact in Q(sqrt3).
def d2(P, Q): return (P[0] - Q[0]) * (P[0] - Q[0]) + (P[1] - Q[1]) * (P[1] - Q[1])

def check5_square():
    # [0,1]^2, r = 1/2, A = (1/2, 0); theta = -+30 deg both give R = 1.
    A = (S(F(1, 2), 0), S(0, 0))
    B = (A[0] + (-HALF), A[1] + RT3 * HALF)
    C = (A[0] + HALF,    A[1] + RT3 * HALF)
    ok_equi = d2(A, B) == d2(A, C) == d2(B, C)
    onb = (B[0] == S(0, 0)) and (C[0] == S(1, 0)) and (B[1] - S(1, 0)).sign() < 0
    side2 = d2(A, B)
    bound2 = S(F(3, 4), 0)                     # (sqrt3 * 1/2)^2
    return ok_equi, onb, side2, bound2, (side2 - bound2).sign()

print("CHECK 5a unit square:", check5_square())
assert check5_square()[0] and check5_square()[1] and check5_square()[4] > 0

def check5_tri():
    # equilateral triangle (-sqrt3,0),(sqrt3,0),(0,3): r = 1, A = (0,0), theta = -90 deg.
    A = (S(0, 0), S(0, 0))
    B = (-RT3, S(0, 0))
    C = (-RT3 * HALF, S(F(3, 2), 0))
    equi = d2(A, B) == d2(A, C) == d2(B, C)
    side2 = d2(A, B)
    return equi, side2, side2 == S(3, 0)       # side^2 = 3 = (sqrt3 * r)^2 exactly
print("CHECK 5b equilateral triangle:", check5_tri())
assert check5_tri()[0] and check5_tri()[2]

# --------------------------------------------------------------------- CHECK 6
# extremal-size Step 0's assertion "K + (1/n)D is strictly convex" is FALSE.
def check6():
    def dist2_to_square(x, y):
        cx = min(max(x, F(0)), F(1)); cy = min(max(y, F(0)), F(1))
        return (x - cx) ** 2 + (y - cy) ** 2
    pts = [F(i, 10) for i in range(0, 11)]
    on = all(dist2_to_square(t, F(-1)) == 1 for t in pts)
    out = all(dist2_to_square(t, F(-1) - F(1, 100)) > 1 for t in pts)
    return on and out

print("CHECK 6  segment [(0,-1),(1,-1)] lies in the boundary of [0,1]^2 + D :", check6())
assert check6()
print("\nALL EXACT CHECKS PASSED")
```

---

## 11. What remains open

1. **Cross-family review.** Everything here is Claude Opus 5 output checked by Claude Opus 5's own
   arithmetic. The repair in §4.2 and the three lemmas in §3 are exactly the sort of thing that
   reads well and can still be wrong; §6 names Lemma S and Lemma C as the places to attack first.
   Codex or a human is required before any of this moves off `sketch`.
2. **A limit-free proof.** §5 shows the strictly-convex reduction cannot simply be dropped from
   *this* argument, but that is a statement about the argument, not about the theorem. A proof
   that handles flat boundary pieces directly — presumably by parametrising $\partial K$ by a
   monotone angle function and tracking the plateaux, where the radial "function" becomes
   set-valued — would be worth more than the patch, and I did not find one. Note the obstruction
   precisely: with plateaux, "$\Gamma$ starts below and ends above its $60°$-shift" is the *same*
   sign condition that §5 breaks, so a genuinely different mechanism is needed, not a better
   parametrisation.
3. **The equality case.** Theorem C is sharp at the disk. Whether the disk is the *only* convex
   body with $m(K)=\sqrt3\,r$ is untouched here; §7 shows the *construction* is tight at the
   equilateral triangle too, so any rigidity proof will have to work harder than reading the
   equality condition off Step 3.
4. **`extremal-size` §5 Conjecture I** ($m(J)\ge\sqrt3\,r(\Omega_J)$ for every Jordan curve) is
   untouched. Nothing here bears on it: every step above spends convexity, most of them twice.
5. **Lean.** Not attempted, and not promising in the short term — not because of the Jordan curve
   theorem (never used) but because of the convex-geometry API the repair needs. The most
   formalisable fragment is Lemma R + Corollary R' of §2, which is finite-dimensional metric
   geometry with a law of cosines and no analysis at all.
