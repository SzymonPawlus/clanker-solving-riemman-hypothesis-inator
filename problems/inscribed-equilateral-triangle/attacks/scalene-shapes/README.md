# Scalene shapes: the spiral-similarity criterion, and where "all but two" stops being an isometry statement

```
regularity budget: Jordan for §2 (Lemma A_sigma: two complementary components, J = boundary of
each, Omega bounded, Lebesgue measure).  NONE for §1, §3, §4 (set-theoretic / measure-theoretic;
S is used only as a set of points).  convex (K compact, int K nonempty) for §5, plus the IVT and
continuity of the radial function on the tangent cone; NO Jordan curve theorem, no degree, no
winding, no smoothness, no rectifiability there.  polygonal + rational (or Q(sqrt3)) coordinates
for §7's computations, which decide finitely many points of finitely many curves and are
`numerical` throughout.
What breaks first if the strongest hypothesis is dropped: dropping convexity in §5 kills the
theorem outright and §7.4 exhibits the failure -- on a NON-convex polygon a point can be
T-exceptional while lying in no cone of opening < phi_min(T), so the tangent-cone criterion is
false there.  Dropping "Jordan" in §2 removes the two-component dichotomy the whole of Lemma
A_sigma is built on.
```

- Lane: **idea I3** of [`../ideation-round-1/README.md`](../ideation-round-1/README.md) — the one
  target the round rated plausibly open.
- Author: `claude` (Claude Opus 5), 2026-08-29, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), **written before any computation in
  this lane** (see its provenance paragraph for the honest qualification). Outcomes in §10.
- Journal, with the complete source of every program run here:
  [`../../../../notebook/claude/2026-08-29-iet-scalene.md`](../../../../notebook/claude/2026-08-29-iet-scalene.md).
- Problem rules consumed: [`../../RULES.md`](../../RULES.md) §1 (budget line, above), §2
  (nondegeneracy — §1.3), §3.1/§3.2/§3.3 (three filters, all three run, §8), §5 (exact arithmetic
  — §7.1 is the ledger), §6 (statuses).

## Result table

| § | Statement | Status |
|---|---|---|
| §1 | **Proposition 1 (spiral-similarity criterion).** For $S \subseteq \mathbb{C}$, $O \in S$ and a nondegenerate triangle shape $T$: $O$ is a vertex of a triangle with all vertices in $S$ and similar to $T$ **iff** $S \cap \sigma_\mu(S) \ne \{O\}$ for one of six explicit multipliers $\mu \in M(T)$, where $\sigma_\mu(z) = O + \mu(z-O)$. | `sketch` — mine, derived here |
| §1.4 | **Remark (why $k=1$ is special).** $M(T)$ has 6 elements for scalene $T$, 3 for isosceles, **1** for equilateral; the collapse is exactly the identity $\mu^{-1} = \bar\mu$, i.e. $\lvert\mu\rvert = 1$. | `sketch` — mine |
| §1.5 | **Lemma 2 (the ratio you cannot escape).** The smallest-angle corner of *every* triangle has adjacent-side ratio in $[1,2)$. | `sketch` — mine |
| §2 | **Lemma A$_\sigma$ (what survives of no-nesting).** If $J \cap \sigma_\mu(J) = \{O\}$ with $\lvert\mu\rvert < 1$ then either $\Omega \cap \sigma_\mu(\Omega) = \emptyset$ **or** $\sigma_\mu(\overline\Omega) \subseteq \overline\Omega$. The *expanding* nesting is killed by area; the *shrinking* one is not, and is realised. | `sketch` — mine |
| §3 | **Proposition 3 (half-density, sharp).** For $\sigma$ a spiral similarity fixing $O$ with $k = \lvert\mu\rvert < 1$: $\sup\{\lambda(V \cap B(O,R))/\lambda(B(O,R)) : \lambda(V \cap \sigma V) = 0\} = \dfrac{1}{1+k^2}$, attained. The bound $\tfrac12$ is recovered exactly at $k = 1$ and degrades to $1$ as $k \to 0$. | `sketch` — mine |
| §3.3 | **Corollary.** The half-density *obstruction* is nevertheless dead for $k \ne 1$: its hypothesis is supplied by Lemma A, and Lemma A is exactly what §2 breaks. | `sketch` — mine |
| §4 | **Proposition 4 (rotating wedge, two radii).** The wedge/rotating-wedge obstruction generalises to a comparison between the circles of radius $r$ and $kr$, not one circle. | `sketch` — mine |
| §4.3 | **Theorem 5 (spiral tip, all shapes at once).** For the witness $J_{c,\beta}$, $O$ is a vertex of an inscribed triangle in the corner role $\mu$ **iff** $\lvert\Lambda_c(\mu)\rvert \le \beta \pmod{360°}$, where $\Lambda_c(\mu) = \arg\mu + (\ln\lvert\mu\rvert)/c$. Hence $O$ is $T$-exceptional iff $\lvert\Lambda_c(\mu)\rvert > \beta$ for all six $\mu \in M(T)$. | `sketch` — mine, derived independently; **agrees with** [`../spiral-tip-witness/README.md`](../spiral-tip-witness/README.md) §10, the line that lane flagged as its least-checked |
| §4.4 | **Corollary 6.** For **every** triangle shape $T$ there are $c,\beta$ making the spiral tip $T$-exceptional; and for fixed $(c,\beta)$ the set of such shapes is open and uncountable. So the tip is a genuine *family* obstruction, not an equilateral coincidence. | `sketch` — mine |
| §5 | **Theorem C (convex, every shape).** For every compact convex $K$ with interior and every triangle shape $T$, $\lvert E_T(\partial K)\rvert \le 2$, and $E_T(\partial K) = \{O : \gamma(O) < \varphi_{\min}(T)\}$ up to an explicit boundary case. **The "all but two" conclusion therefore holds for every shape on every convex curve.** | `sketch` — mine |
| §6 | **Proposition 7.** The *wedge mechanism alone* yields at most two exceptional points, for every shape $T$ and every Jordan curve. Any $\lvert E_T\rvert \ge 3$ needs a non-wedge point. | `sketch` — mine |
| §7 | Exact decider for general $T$; validation against the committed equilateral decider; a census of $66\,075$ (polygon, shape) pairs; $1774$ exactly-confirmed exceptional points; **no $\lvert E_T\rvert \ge 3$ found**; non-wedge exceptional points exhibited on polygons for both scalene and equilateral shapes. | `numerical` |
| §9 | The apparent contradiction between Schwartz's $G(J)$ and the "not known for any other shape" snippet is a **quantifier-order** difference and needs no contradiction. This is an observation about the two *statements*, not about either paper. | `sketch` — mine, and explicitly not a literature finding |

**Nothing here is assumable** ([`../../../../RULES.md`](../../../../RULES.md) §3), including by me.
In particular §5 is *not* a proof that $\lvert E_T(J)\rvert \le 2$ in general, and §7 found no
counterexample but certifies nothing about the uncountably many points it did not test (§7.5).

**Dependency hygiene.** Every statement below is re-derived here from elementary plane geometry,
measure theory, and — in §2 only — the Jordan curve theorem. Nothing is imported from
[`../rotation-continuity/`](../rotation-continuity/README.md),
[`../convex-vertex-criterion/`](../convex-vertex-criterion/README.md),
[`../half-density-obstruction/`](../half-density-obstruction/README.md) or
[`../spiral-tip-witness/`](../spiral-tip-witness/README.md); all four are `sketch` and therefore
unassumable. Where my conclusions coincide with theirs I say so as a **cross-check** (§1.2, §3.4,
§4.3, §5.5), never as a dependency. Meyerson's bound is `cited`\* and provisional
([`../../README.md`](../../README.md) provenance warning) and is used nowhere as an input.

---

## 0. What this lane was asked, and what it found

For a triangle shape $T$ and a Jordan curve $J$, call $O \in J$ **$T$-exceptional** if no triangle
inscribed in $J$ and similar to $T$ has a vertex at $O$, and write $E_T(J)$. The equilateral case
is $\lvert E(J)\rvert \le 2$ (Meyerson, `cited`\*, provisional). The lane's target was
$\lvert E_T(J)\rvert \ge 3$ for a scalene $T$.

**I did not find one.** What the lane produced instead:

1. The criterion for general $T$ is a **spiral similarity**, and the exact place the equilateral
   argument's symmetry is lost is the single identity $\mu^{-1} = \bar\mu$, which holds iff
   $\lvert\mu\rvert = 1$ (§1.4).
2. The **no-nesting lemma** — not the half-density lemma — is the load-bearing casualty. Its
   measure step survives in one direction only: for $\lvert\mu\rvert<1$ the *expanding* nesting is
   still impossible, the *shrinking* one is not, and the spiral tip realises it (§2).
3. The half-density lemma itself **does** have a sharp analogue, with constant $1/(1+k^2)$ (§3) —
   but it is useless here, because the hypothesis it needs is exactly what (2) destroys. Both
   halves of that sentence are results; the second is the one that matters.
4. The spiral tip is $T$-exceptional for an **open uncountable family of shapes**, described in
   closed form by a single "spiral angle" $\Lambda_c(\mu)$ (§4). This confirms, by an independent
   derivation and an independent numerical check, the corollary the spiral lane flagged as its
   least-checked line.
5. On **convex** curves the "all but two" conclusion holds for **every** shape, with the exceptional
   set identified exactly (§5). So whatever is hard about the scalene question, it is not hard for
   convex curves.
6. The wedge mechanism alone can never give three exceptional points, for any shape (§6). So a
   counterexample must contain a non-wedge exceptional point — and §7.4 shows those exist on
   polygons, for scalene *and* for equilateral shapes.

---

## 1. The criterion for a general shape

### 1.1 Setup

Identify $\mathbb{R}^2 = \mathbb{C}$. A **triangle shape** is the similarity class of a
nondegenerate triangle; parametrise it by $w \in \mathbb{C} \setminus \mathbb{R}$, the shape being
that of $T_w = (0, 1, w)$. Two triangles are **similar** when some similarity of the plane
(orientation-preserving or not) carries one to the other; this is the standard convention and it is
what makes $w$ and $\bar w$ the same shape.

For $\mu \in \mathbb{C}^\times$ write
$$\sigma_\mu(z) \;=\; O + \mu\,(z - O),$$
the **spiral similarity** about $O$: rotation by $\arg\mu$ composed with scaling by $\lvert\mu\rvert$.
It is an isometry iff $\lvert\mu\rvert = 1$.

> **Proposition 1.** Let $S \subseteq \mathbb{C}$, $O \in S$, and let $T_w$ be a triangle shape.
> Then $O$ is a vertex of a nondegenerate triangle with all three vertices in $S$ and similar to
> $T_w$ **iff** there is $\mu \in M(w)$ with
> $$S \cap \sigma_\mu(S) \;\ne\; \{O\},$$
> where
> $$M(w) \;=\; \bigl\{\,w,\;\; 1-w,\;\; \tfrac{w-1}{w}\,\bigr\} \;\cup\;
> \bigl\{\,\bar w,\;\; 1-\bar w,\;\; \tfrac{\bar w-1}{\bar w}\,\bigr\}.$$

**regularity budget: none.** $S$ is used only as a set of points — not closed, not connected, not
injectively parametrised. Every use of Proposition 1 below is therefore a set-membership statement
and no topology can leak in unnoticed.

### 1.2 Proof

*(⇐)* Suppose $X \in S \cap \sigma_\mu(S)$ with $X \ne O$, for some $\mu \in M(w)$. Put
$P = \sigma_\mu^{-1}(X)$. Then $P \in S$ (that is what $X \in \sigma_\mu(S)$ says), and
$X - O = \mu\,(P - O)$. Since $\mu \ne 0$ and $X \ne O$ we get $P \ne O$; and $P \ne X$ because
$\mu \ne 1$ — indeed $\mu = 1$ would force $w = 1$, $w = 0$ or $w - 1 = w$, all excluded by
$w \notin \mathbb{R}$. So $O, P, X$ are three distinct points of $S$.

Their shape: the map $z \mapsto O + (P-O)z$ is a direct similarity sending $0 \mapsto O$,
$1 \mapsto P$, $\mu \mapsto X$. Hence the triangle $(O,P,X)$ is directly similar to $(0,1,\mu)$.
It remains to check that each $\mu \in M(w)$ makes $(0,1,\mu)$ similar to $(0,1,w)$:

| $\mu$ | similarity carrying $(0,1,\mu)$ to a labelling of $(0,1,w)$ |
|---|---|
| $w$ | identity |
| $1-w$ | $z \mapsto 1 - z$ maps $(0,1,1-w) \mapsto (1,0,w)$ |
| $(w-1)/w$ | $z \mapsto w(1-z)$ maps $(0,1,\tfrac{w-1}{w}) \mapsto (w,0,1)$ |
| $\bar w, 1-\bar w, (\bar w-1)/\bar w$ | the same three, post-composed with conjugation |

so in every case $(O,P,X)$ is similar (directly or not) to $T_w$, and it is nondegenerate because
$w \notin \mathbb{R}$ makes $(0,1,\mu)$ non-collinear.

*(⇒)* Suppose $O, P, X \in S$ are the vertices of a triangle similar to $T_w$. Some similarity $f$
carries $(0,1,w)$ to $(O,P,X)$ in *some* order of the three vertices; $f(z) = a z + b$ or
$f(z) = a\bar z + b$ with $a \ne 0$. Consider $\mu := (X-O)/(P-O)$, which is well defined because
$P \ne O$. Applying $f^{-1}$, the triple $(O,P,X)$ corresponds to a permutation
$(v_0, v_1, v_2)$ of $(0,1,w)$, and $\mu = (v_2 - v_0)/(v_1 - v_0)$ in the direct case,
$\overline{(v_2-v_0)/(v_1-v_0)}$ in the indirect one. The six permutations give
$$\frac{v_2-v_0}{v_1-v_0} \in \Bigl\{\,w,\ \frac1w,\ 1-w,\ \frac{1}{1-w},\ \frac{w-1}{w},\
\frac{w}{w-1}\Bigr\},$$
i.e. the three listed generators together with their **inverses**, and the indirect case gives the
complex conjugates of the same six. Now $X = \sigma_\mu(P)$ with $P \in S$, so
$X \in S \cap \sigma_\mu(S)$, and $X \ne O$ since the triangle is nondegenerate. Finally
$$S \cap \sigma_{\mu}(S) \ne \{O\} \iff S \cap \sigma_{\mu^{-1}}(S) \ne \{O\},$$
because $\sigma_{\mu^{-1}} = \sigma_\mu^{-1}$ and applying $\sigma_\mu^{-1}$ to a point
$X \ne O$ of the first intersection gives a point $\ne O$ of the second. So each inverse pair
contributes one condition, and the six listed representatives of $M(w)$ exhaust them. $\square$

**Reading it.** $\mu$ encodes a *corner role*: $\arg\mu$ is the angle of $T$ at the vertex placed
at $O$, and $\lvert\mu\rvert$ is the ratio of the two sides adjacent to it, in one of the two
possible orders. Twelve maps (3 corners × 2 neighbour-orders × 2 orientations) collapse to six
conditions under $\mu \leftrightarrow \mu^{-1}$.

**Cross-check, not a dependency.** At $w = e^{i60°}$ one computes $1-w = e^{-i60°}$ and
$(w-1)/w = e^{i60°}$, so $M(e^{i60°}) = \{e^{i60°}, e^{-i60°}\}$: the two $60°$ rotations, which is
the reduction the committed enumerator `experiments/inscribed-triangle-polygons/` uses and the
"Observation R" of [`../rotation-continuity/`](../rotation-continuity/README.md) §2. I derived
Proposition 1 before re-reading either. §7.2 turns this agreement into a machine check on 1566
points. Both of those files are `sketch`; the agreement is decorrelation evidence and confers
nothing.

### 1.3 Nondegeneracy ([`../../RULES.md`](../../RULES.md) §2)

Every triangle produced by Proposition 1 has three named distinct vertices with a positive side
$\lvert OP\rvert > 0$ fixed before any limit is taken; no sequence of triangles occurs anywhere in
this file, so there is nothing to collapse and no uniform $\delta$ to establish. The degenerate
solution $X = O$ is the one always present in $S \cap \sigma_\mu(S)$ (because $\sigma_\mu$ fixes
$O$) and is excluded by hand, in the statement, every time.

### 1.4 Where the symmetry is lost — the one-line answer

For each corner, the two conditions in $M(w)$ coming from that corner are $\mu$ and $\bar\mu$.
$$\mu^{-1} = \bar\mu \iff \lvert\mu\rvert = 1 .$$
Since $\mu$ and $\mu^{-1}$ give the *same* condition (proof above), the two orientations at a
corner give the same condition precisely when that corner's adjacent-side ratio is $1$. Hence

| shape $T$ | $\lvert M(w)\rvert$ as *conditions* |
|---|---|
| equilateral | **1** |
| isosceles, not equilateral | 3 (one per corner: the apex has ratio $1$, the two base corners are swapped by the reflection) |
| scalene | **6** |

That is the arithmetic content of "the rotation trick degenerates". It is not merely that $\sigma$
stops being an isometry: it is that a scalene shape imposes **six independent** conditions where
the equilateral shape imposes one, and $O$ is exceptional only if **all** of them fail.

### 1.5 Lemma 2 — the ratio you cannot escape

> **Lemma 2.** Let $T$ have sides $t_1 \ge t_2 \ge t_3 > 0$. Then the corner between the sides
> $t_1$ and $t_2$ — which is the corner **opposite the shortest side**, hence the corner of
> **smallest angle** — has adjacent-side ratio $t_1/t_2 \in [1,2)$.

*Proof.* $t_1/t_2 \ge 1$ by the ordering, and the triangle inequality gives
$t_1 < t_2 + t_3 \le 2t_2$. $\square$

This is a hard constraint on any attempt to block all six roles by making ratios extreme: **the
corner with the smallest angle — the hardest to block by an angular argument — is always the corner
whose ratio is closest to $1$**, i.e. the one where the equilateral-style symmetry is least broken.
Every construction in this lane ran into it, and §7.3 shows the census did too: the shapes that
produce exceptional points at all are mildly, not wildly, scalene.

---

## 2. Lemma A$_\sigma$ — nesting, and which direction of it survives

Let $J$ be a Jordan curve, $O \in J$, $\Omega$ its interior and $E$ its exterior, and
$\sigma = \sigma_\mu$ with $\mu \ne 1$. Write $J' = \sigma(J)$, $\Omega' = \sigma(\Omega)$,
$E' = \sigma(E)$; since $\sigma$ is a homeomorphism of the plane, $J'$ is a Jordan curve with
interior $\Omega'$ and exterior $E'$.

> **Lemma A$_\sigma$.** Suppose $J \cap \sigma(J) = \{O\}$ and $k := \lvert\mu\rvert < 1$. Then
> exactly one of
> 1. $\Omega \cap \sigma(\Omega) = \emptyset$ (the *external* configuration), or
> 2. $\sigma(\overline\Omega) \subseteq \overline\Omega$ (the *shrinking nesting*),
>
> holds. The **expanding** nesting $\overline\Omega \subseteq \sigma(\overline\Omega)$ is
> impossible.

**regularity budget: Jordan.** Used: $\mathbb{R}^2 \setminus J = \Omega \sqcup E$ with both open,
$\Omega$ bounded, $J = \partial\Omega = \partial E$, $\operatorname{int}\overline\Omega = \Omega$,
and $\lambda(\sigma A) = k^2\lambda(A)$.

*Proof.* $J' \setminus \{O\}$ is connected (a circle minus a point) and disjoint from $J$, so it
lies entirely in $\Omega$ or entirely in $E$.

*Case $J'\setminus\{O\} \subseteq \Omega$.* Then $J' \subseteq \overline\Omega$, so $J'$ misses
$E$; $E$ is connected, disjoint from $J'$ and unbounded, hence $E \subseteq E'$, hence
$\overline{\Omega'} = \mathbb{R}^2 \setminus E' \subseteq \mathbb{R}^2\setminus E = \overline\Omega$.
That is alternative (2). Note where the equilateral proof used measure and this one cannot: with
$k=1$ one continues $\lambda(\overline{\Omega'}) = \lambda(\overline\Omega) < \infty$, upgrades the
inclusion to equality, and derives $J = J'$, a contradiction. Here
$\lambda(\overline{\Omega'}) = k^2\lambda(\overline\Omega) < \lambda(\overline\Omega)$ and there is
no contradiction at all. **This is the precise death of the equilateral argument.**

*Case $J\setminus\{O\} \subseteq \Omega'$ (the expanding nesting).* Symmetrically
$\overline\Omega \subseteq \overline{\Omega'}$, so
$\lambda(\overline\Omega) \le \lambda(\overline{\Omega'}) = k^2\lambda(\overline\Omega)$. Since
$\Omega$ is open and nonempty, $\lambda(\overline\Omega) \ge \lambda(\Omega) > 0$, and it is finite
because $\Omega$ is bounded; so $1 \le k^2$, contradicting $k < 1$. **Impossible.**

*Case $J'\setminus\{O\} \subseteq E$.* The hypothesis $J \cap J' = \{O\}$ is symmetric, so the
previous paragraph also rules out $J \setminus \{O\} \subseteq \Omega'$, leaving
$J\setminus\{O\} \subseteq E'$. Now $\Omega$ is connected and disjoint from $J'$, hence
$\Omega \subseteq \Omega'$ or $\Omega \subseteq E'$. The first gives
$\overline\Omega \subseteq \overline{\Omega'}$, hence $J \subseteq \overline{\Omega'}$,
contradicting $J\setminus\{O\} \subseteq E'$ and $E' \cap \overline{\Omega'} = \emptyset$ (and
$J \setminus \{O\} \ne \emptyset$). So $\Omega \subseteq E'$, i.e. alternative (1). $\square$

**Alternative (2) is not vacuous.** At a logarithmic-spiral tip of matching pitch,
$\sigma$ maps the spiral channel strictly inside itself; §4.3 makes this explicit and gives the
exact condition. Iterating, $\sigma^n(\overline\Omega)$ is a decreasing sequence of compacta of
diameter $k^n \operatorname{diam}\overline\Omega \to 0$ all containing $O$, so
$\bigcap_n \sigma^n(\overline\Omega) = \{O\}$: the shrinking nesting is a genuine, and geometrically
forced, picture.

**So the ideation entry's claim is confirmed and sharpened.** I3 wrote "the isometry kills nesting;
for every other side ratio, nesting is a live exceptional mechanism". That is right, and the sharp
form adds the *direction*: for $k<1$ only the shrinking nesting is live, and the expanding one is
still killed — by the same area argument, run the other way.

---

## 3. The half-density lemma: a sharp analogue, and why it does not help

The equilateral obstruction ([`../half-density-obstruction/`](../half-density-obstruction/README.md))
rests on: *if $\rho$ is an isometry fixing $O$ and $\lambda(V \cap \rho V) = 0$, then
$\lambda(V \cap B(O,R)) \le \tfrac12 \lambda(B(O,R))$*, whose two-line proof uses
$\rho(B(O,R)) = B(O,R)$. A spiral similarity does not map the ball to itself, so the proof fails.
Does the statement?

### 3.1 The ball form fails, and by how much — exactly

> **Proposition 3.** Fix $O$, $R>0$ and $\mu$ with $k = \lvert\mu\rvert < 1$. Then
> $$\sup\Bigl\{\ \frac{\lambda(V \cap B(O,R))}{\lambda(B(O,R))} \ :\ V \subseteq \mathbb{R}^2
> \text{ measurable},\ \lambda\bigl(V \cap \sigma_\mu(V)\bigr) = 0 \Bigr\} \;=\;
> \frac{1}{1+k^{2}},$$
> and the supremum is **attained**.

**regularity budget: none** — pure measure theory; $V$ is an arbitrary measurable set.

*Attained.* Take $O = 0$, $R = 1$ and the union of alternate geometric shells
$$V^{*} \;=\; \bigcup_{n \ \mathrm{even}} \{\, z : k^{\,n+1} < \lvert z\rvert \le k^{\,n}\,\}.$$
$\sigma_\mu(V^*)$ is the union of the *odd* shells, disjoint from $V^*$, and
$$\lambda(V^*) \;=\; \pi \sum_{n \ \mathrm{even}} \bigl(k^{2n} - k^{2n+2}\bigr)
\;=\; \pi\,\frac{1-k^2}{1-k^4} \;=\; \frac{\pi}{1+k^2} \;=\; \frac{\lambda(B(0,1))}{1+k^2}.$$
For $k$ small this is close to the *whole* ball: the obstruction becomes vacuous as $k \to 0$, which
is already the qualitative answer.

*Upper bound.* Put $O = 0$, $R = 1$, $a = -\ln k > 0$, $\varphi = \arg\mu$, and use log-polar
coordinates $z = e^{u + i\theta}$, in which $\sigma_\mu$ is the **translation**
$(u,\theta) \mapsto (u - a,\ \theta + \varphi)$ of the cylinder
$\mathbb{R} \times (\mathbb{R}/2\pi)$, and planar Lebesgue measure is
$\mathrm{d}\lambda = e^{2u}\,\mathrm{d}u\,\mathrm{d}\theta$.

*Step 1: remove the rotation.* The shear
$\Phi(u,\theta) = \bigl(u,\ \theta + \tfrac{\varphi}{a}u\bigr)$ is a bijection of the cylinder, it
preserves $u$, and it preserves $\mathrm{d}u\,\mathrm{d}\theta$, hence it preserves
$e^{2u}\mathrm{d}u\,\mathrm{d}\theta$ and it preserves the ball $\{u \le 0\}$. It conjugates the
translation by $(-a,\varphi)$ to the translation by $(-a,0)$:
$$\Phi(u-a,\theta+\varphi) = \bigl(u-a,\ \theta+\varphi+\tfrac{\varphi}{a}(u-a)\bigr)
= \bigl(u-a,\ \theta + \tfrac{\varphi}{a}u\bigr) = \Phi(u,\theta) - (a,0).$$
So we may assume $\varphi = 0$: **the angle of the spiral similarity is irrelevant to this
inequality**, exactly as the angle was irrelevant in the isometry case.

*Step 2: it decouples over directions.* With $\varphi = 0$ the constraint is, for each fixed
$\theta$, that the slice $S_\theta = \{u \le 0 : (u,\theta) \in V\}$ satisfies
$\lambda_1(S_\theta \cap (S_\theta + a)) = 0$ (Fubini; the planar null set has null slices for
a.e. $\theta$, and $\lambda$ and $\mathrm{d}u\,\mathrm{d}\theta$ are mutually absolutely
continuous away from $0$ and $\infty$). A null intersection may be replaced by an empty one:
putting $N = S \cap (S+a)$ and $S' = S \setminus (N \cup (N-a))$ gives
$S' \cap (S'+a) = \emptyset$ with $\lambda_1(S\setminus S') = 0$. It therefore suffices to bound
$\int_{S} e^{2u}\mathrm{d}u$ for one slice with $S \cap (S+a) = \emptyset$.

*Step 3: the one-dimensional problem.* Write $u = x - na$ with $x \in (-a,0]$, $n \ge 0$. Then
$$\int_S e^{2u}\,\mathrm{d}u = \int_{-a}^{0} \Bigl(\sum_{n \ge 0} \mathbf 1_S(x-na)\,q^{\,n}\Bigr)
e^{2x}\,\mathrm{d}x, \qquad q := e^{-2a} = k^2 .$$
For fixed $x$, the index set $N_x = \{n : x-na \in S\}$ contains no two consecutive integers
(if $n, n+1 \in N_x$ then $y = x-(n+1)a \in S$ and $y + a \in S$, contradicting
$S \cap (S+a) = \emptyset$). Among subsets of $\mathbb{Z}_{\ge 0}$ with no two consecutive elements,
$\sum_{n \in N} q^n$ is maximised by $N = \{0,2,4,\dots\}$: writing $f$ for the supremum, the
self-similarity $f = \max(1 + q^2 f,\ q f)$ and $q<1$ give $f = 1/(1-q^2)$, the value at
$\{0,2,4,\dots\}$. The unconstrained total is $\sum_{n\ge0} q^n = 1/(1-q)$, so
$$\frac{\int_S e^{2u}du}{\int_{-\infty}^{0} e^{2u}du} \;\le\; \frac{1/(1-q^2)}{1/(1-q)}
\;=\; \frac{1}{1+q} \;=\; \frac{1}{1+k^{2}} . \qquad\square$$

At $k = 1$ the formula returns exactly $\tfrac12$, the isometry constant, so Proposition 3 is a
one-parameter deformation of the equilateral lemma rather than a different statement. §7.6 records
a numerical check of the one-dimensional optimum against an exact dynamic program.

### 3.2 The annulus form, where the constant stays $\tfrac12$

The reason $1/(1+k^2)$ is worse than $\tfrac12$ is that the *ball* is not a natural domain for a
scaling. The natural invariant measure for $\sigma_\mu$ is
$\mathrm{d}\nu = \mathrm{d}\lambda/\lvert z-O\rvert^2 = \mathrm{d}u\,\mathrm{d}\theta$, which
$\sigma_\mu$ preserves exactly, and the natural domains are log-annuli
$A_N = \{e^{-Na} \le \lvert z - O\rvert \le 1\}$, with $\nu(A_N) = 2\pi N a$. The two-line argument
then runs verbatim up to a boundary term: $W = V \cap A_N$ has
$\sigma(W) \subseteq A_{N+1}$, so
$$2\nu(W) = \nu(W) + \nu(\sigma W) = \nu\bigl(W \cup \sigma W\bigr) \le \nu(A_{N+1})
= 2\pi(N{+}1)a,$$
giving $\nu(V \cap A_N)/\nu(A_N) \le \tfrac12\bigl(1 + \tfrac1N\bigr)$. So:

> **the half-density lemma survives for spiral similarities with the same constant $\tfrac12$,
> asymptotically, on log-annuli, with respect to the scale-invariant measure** — and the $O(1/N)$
> error is unavoidable, since a single shell realises density $1$ at $N = 1$.

This answers the brief's sub-question in the affirmative and in the sharp form: *a different
constant on balls ($1/(1+k^2)$, sharp), the same constant on annuli (asymptotically, for the
invariant measure)*.

### 3.3 …and it does not matter

In the equilateral lane the chain is
$$O \text{ exceptional} \;\Rightarrow\; J \cap \rho(J) = \{O\} \;\overset{\text{Lemma A}}{\Rightarrow}\;
\Omega \cap \rho(\Omega) = \emptyset \;\overset{\text{Lemma H}}{\Rightarrow}\;
\lambda(\Omega \cap B) \le \tfrac12\lambda(B).$$
The second arrow is Lemma A, and §2 shows that for $k \ne 1$ it has a second alternative: the
shrinking nesting, in which $\sigma(\Omega) \subseteq \Omega$ and hence
$\lambda(\Omega \cap \sigma(\Omega)) = \lambda(\sigma\Omega) = k^2\lambda(\Omega) > 0$ — the
hypothesis of Proposition 3 fails as badly as it possibly can. And the nesting alternative is
precisely the case that occurs at the interesting witness (§4.3).

> **Corollary.** For $\lvert\mu\rvert \ne 1$ the half-density *obstruction* yields nothing about
> exceptional points, even though the half-density *lemma* has a sharp analogue. The casualty is
> Lemma A, not Lemma H.

This is worth stating plainly because the brief guessed the other way round, and because the
distinction is exactly the kind of thing that gets lost when a lemma and the argument that uses it
are conflated.

### 3.4 Cross-check, not a dependency

[`../half-density-obstruction/`](../half-density-obstruction/README.md) proves the isometry case
with constant $\tfrac12$ and shows $\tfrac12$ is sharp there, with the maximal independent sets of
$C_6$ as the reason. My Proposition 3 reproduces $\tfrac12$ at $k=1$ by a different route (a path
graph on $\mathbb{Z}_{\ge0}$ with geometric weights, not a $6$-cycle), which is a mild independent
confirmation of that constant. Their file is `sketch`; nothing here rests on it.

---

## 4. The wedge obstruction at two radii, and the spiral tip

### 4.1 Direction sets

For $O \in S$ and $r > 0$ put
$$\Theta_S(r) \;=\; \{\theta \in \mathbb{R}/360° \;:\; O + re^{i\theta} \in S\}.$$
Proposition 1 in polar form: writing $\mu = k e^{i\varphi}$,
$$O \text{ is good in role } \mu \iff \exists\, r>0:\ \bigl(\Theta_S(r) + \varphi\bigr)
\cap \Theta_S(kr) \ne \emptyset. \tag{$\ast$}$$
*(Immediate: $X = \sigma_\mu(P)$ with $\lvert P - O\rvert = r$ has $\lvert X-O\rvert = kr$ and
$\arg(X-O) = \arg(P-O)+\varphi$.)*

For $k = 1$ this compares a circle with **itself**; for $k \ne 1$ it compares the circles of radius
$r$ and $kr$. That is the whole structural difference, and it cuts both ways: the comparison is
harder to satisfy (two different circles must cooperate) but also harder to block (a condition at
one scale says nothing about another).

> **Proposition 4 (rotating wedge, two radii).** Suppose there are $\psi : (0,\infty) \to
> \mathbb{R}/360°$ and $\delta \ge 0$ with $\Theta_J(r) \subseteq [\psi(r),\psi(r)+\delta]$ for
> every $r$. If for every $r>0$
> $$\bigl[\psi(r)+\varphi,\ \psi(r)+\varphi+\delta\bigr] \cap
> \bigl[\psi(kr),\ \psi(kr)+\delta\bigr] = \emptyset \pmod{360°},$$
> equivalently $\operatorname{dist}\bigl(\psi(kr) - \psi(r) - \varphi,\ 0\bigr) > \delta$ in
> $\mathbb{R}/360°$, then $O$ is exceptional in role $\mu = ke^{i\varphi}$.

*Proof.* Immediate from $(\ast)$: the two arcs containing the two sides of the intersection are
disjoint. $\square$

**One Jordan-curve fact constrains all of this.** If $J$ is a Jordan curve (indeed any connected
compact set) containing $O$, then $r \mapsto \lvert z - O\rvert$ maps the connected set $J$ onto
$[0,D]$, $D = \max_{z\in J}\lvert z-O\rvert$. Hence
$$\Theta_J(r) \ne \emptyset \quad\text{for every } 0 < r \le D. \tag{$\dagger$}$$
So the tempting "lacunary radii" mechanism — arrange $J$ to have no points at all at the radii
$kr$ for the relevant $r$ — is **impossible**, and $(\dagger)$ is the reason a general
$\lvert E_T\rvert \ge 3$ construction is not free.

### 4.2 The witness

Take the spiral witness of [`../spiral-tip-witness/`](../spiral-tip-witness/README.md):
for $c>0$ and $0<\beta<60°$,
$$J_{c,\beta} = \{0\} \cup S \cup e^{i\beta}S \cup B, \qquad
S = \{e^{-ct}e^{it} : t \ge 0\},\qquad B = \{e^{is} : 0 \le s \le \beta\},$$
whose direction sets are, with $\tau(r) = -(\ln r)/c$,
$$\Theta(r) = \{\tau(r),\ \tau(r)+\beta\} \ (0<r<1), \qquad \Theta(1) = [0,\beta], \qquad
\Theta(r) = \emptyset \ (r>1).$$
**I take this normal form as the definition of the object I analyse**, and derive everything below
from it directly; I do not import that lane's Theorem 1, Corollary 5 or §10 (all `sketch`). The
normal form itself is one line of calculus — $t \mapsto e^{-ct}$ is a strictly decreasing bijection
$[0,\infty) \to (0,1]$ — and I re-derived it before using it.

### 4.3 Theorem 5 — every corner role at once

> **Theorem 5.** Let $\mu = k e^{i\varphi} \ne 0$ and define the **spiral angle**
> $$\Lambda_c(\mu) \;=\; \varphi + \frac{\ln k}{c} \;=\; \arg\mu + \frac{\ln\lvert\mu\rvert}{c}
> \ \in\ \mathbb{R}/360° .$$
> Then $O = 0$ is a vertex of a triangle inscribed in $J_{c,\beta}$ in the corner role $\mu$
> **iff** $\operatorname{dist}\bigl(\Lambda_c(\mu), 0\bigr) \le \beta$ in $\mathbb{R}/360°$.

*Proof.* Write $L = -(\ln k)/c$, so $\tau(kr) = \tau(r) + L$ and $\Lambda_c(\mu) = \varphi - L$. By
$(\ast)$ we must decide whether some $r$ has $(\Theta(r)+\varphi) \cap \Theta(kr) \ne \emptyset$;
both sets must be nonempty, so $r \le 1$ and $kr \le 1$.

*Radii with $r<1$ and $kr<1$.* Then $\Theta(r)+\varphi = \{\tau+\varphi, \tau+\beta+\varphi\}$ and
$\Theta(kr) = \{\tau+L, \tau+L+\beta\}$ with $\tau = \tau(r)$. The four differences are
$\varphi - L$, $\varphi - L - \beta$, $\varphi - L + \beta$, $\varphi - L$. So these radii
contribute exactly when $\Lambda_c(\mu) \in \{-\beta, 0, \beta\}$ — three isolated values,
**independent of $r$**: the two arms rotate together, so no radius in this range is any different
from any other. *(This is the exact sense in which a matched-pitch spiral is invariant under
$\sigma_\mu$: $\sigma_\mu(S) = e^{i(\varphi - L)} \cdot \{e^{-cs}e^{is} : s \ge L\}$, a rotate of a
truncation of $S$ by the angle $\Lambda_c(\mu)$. $\sigma_\mu$ acts on the family of pitch-$c$
spirals through $O$ as the rotation by $\Lambda_c(\mu)$, and fixes $S$ setwise iff
$\Lambda_c(\mu) = 0$.)*

*The radius carrying the closing arc.* If $k<1$, take $r = 1$: $\Theta(1)+\varphi = [\varphi,
\varphi+\beta]$ and $\Theta(k) = \{L, L+\beta\}$, and these meet iff $L - \varphi \in [0,\beta]$ or
$L-\varphi \in [-\beta,0]$, i.e. iff $\lvert\Lambda_c(\mu)\rvert \le \beta$. If $k>1$, take
$r = 1/k$: $\Theta(1/k) + \varphi = \{-L+\varphi, -L+\beta+\varphi\}$ meets $\Theta(1) = [0,\beta]$
iff $\varphi - L \in [0,\beta]$ or $\in[-\beta,0]$, the same condition. If $k = 1$ the two coincide.

*Nothing else.* $r > 1$ or $kr > 1$ gives an empty $\Theta$.

The three isolated values of the first case are contained in the interval of the second, so the
union of all cases is exactly $\lvert\Lambda_c(\mu)\rvert \le \beta$. $\square$

> **Consequence.** $O$ is $T$-exceptional for $J_{c,\beta}$ **iff**
> $\operatorname{dist}(\Lambda_c(\mu),0) > \beta$ for all six $\mu \in M(w)$.

**Consistency at $\mu \leftrightarrow \mu^{-1}$**: $\Lambda_c(\mu^{-1}) = -\Lambda_c(\mu)$, and the
criterion is even in $\Lambda_c$ — as it must be, since $\mu$ and $\mu^{-1}$ give the same
condition (§1.2). This is a real check and it passes; note that $\Lambda_c(\bar\mu)$ is *not*
$-\Lambda_c(\mu)$ unless $\lvert\mu\rvert=1$, which is again §1.4.

**Recovering the equilateral case.** $M(e^{i60°}) = \{e^{\pm i60°}\}$, all of modulus $1$, so
$\lvert\Lambda_c\rvert = 60° > \beta$ always: the tip is exceptional for the equilateral shape and
every $(c,\beta)$ with $\beta<60°$, which is the spiral lane's Theorem 1.

**Cross-check with the spiral lane's §10 — the point of contact this lane was told to test.**
That file states, as its least-checked line and explicitly as a hand-off to I3: *the corner role
$(\alpha,\lambda)$ is realised iff $\lvert\alpha + (\ln\lambda)/c\rvert \le \beta \pmod{360°}$*.
That is Theorem 5 with $(\alpha,\lambda) = (\varphi,k)$. **I derived mine from the normal form
before re-reading their §10, and the two agree**, including the direction of the sign on
$\ln\lambda$. §7.6 adds an independent brute-force check over $r$ on 480 random
$(c,\beta,\varphi,k)$ with zero mismatches. Kill-criterion **K3** is therefore not met. Their
statement remains `sketch` and so does mine; two `sketch` derivations agreeing is decorrelation
evidence, not verification ([`../../../../RULES.md`](../../../../RULES.md) §3).

### 4.4 Corollary 6 — a family of shapes, not a coincidence

> **Corollary 6.**
> (a) For fixed $(c,\beta)$, the set of shapes $w$ for which $O$ is $T_w$-exceptional in
> $J_{c,\beta}$ is **open** in $\mathbb{C}\setminus\mathbb{R}$ (the six conditions are strict
> inequalities in continuous functions of $w$), and it is nonempty — it contains $e^{i60°}$ and a
> neighbourhood of it.
> (b) For every shape $w$ there are $c > 0$ and $\beta \in (0°,60°)$ making $O$ $T_w$-exceptional:
> for each of the six $\mu \in M(w)$, $\Lambda_c(\mu) \equiv 0$ holds for at most countably many
> $c>0$ (namely $c = \ln\lvert\mu\rvert/(360°n - \arg\mu)$ over $n \in \mathbb{Z}$, those that are
> positive), so pick $c$ outside that countable set and then $\beta < \min_\mu
> \operatorname{dist}(\Lambda_c(\mu),0)$.

So the answer to the brief's question — *for which $(\varphi,k)$ is the spiral tip $T$-exceptional,
and is it a whole family?* — is: for all $(\varphi,k)$ off the **pitch curve**
$\Lambda_c = 0$, i.e. $k = e^{-c\varphi}$, thickened by the band $\lvert\Lambda_c\rvert \le \beta$
that the closing arc contributes. It is a family, it is open, it is uncountable, and it is
described in closed form. That is the structural result I3 predicted, and it is now derived rather
than conjectured.

**What it does not give.** One tip is one exceptional point. Corollary 6 says nothing about three,
and §8.3 says what actually blocks the three-tip construction.

---

## 5. Convex curves: "all but two" holds for every shape

This is the lane's one positive general theorem, and it is the reason the counterexample hunt was
confined to non-convex curves.

Let $K \subseteq \mathbb{R}^2$ be compact convex with $\operatorname{int}K \ne \emptyset$,
$J = \partial K$, and $O \in J$. Let $\Gamma(O) \subseteq \mathbb{R}/360°$ be the **tangent cone
directions** at $O$, i.e. the closure of $\{\arg(z-O) : z \in K, z\ne O\}$; it is a closed arc of
some length $\gamma(O) \in (0°,180°]$ (convexity). For $\theta$ in the *interior* of $\Gamma(O)$ let
$R(\theta) = \max\{t \ge 0 : O + te^{i\theta} \in K\} > 0$; $R$ is continuous there — for
$\theta$ interior to the cone, $O + \varepsilon e^{i\theta} \in \operatorname{int}K$ for small
$\varepsilon$, so every $O + te^{i\theta}$ with $t < R(\theta)$ is a convex combination of an
interior point and a point of $K$ and is therefore interior, which gives lower semicontinuity;
upper semicontinuity is closedness of $K$ — and for such
$\theta$ the ray meets $J$ in the single point $O + R(\theta)e^{i\theta}$ (convexity: the ray meets
$K$ in the segment $[O, O+R(\theta)e^{i\theta}]$, whose interior points are interior to $K$).

At an **extreme** direction $\theta_0$ of $\Gamma(O)$ exactly one of two things happens:
$L := \lim_{\theta \to \theta_0} R(\theta) = 0$, and then the ray meets $J$ only at $O$; or
$L > 0$, and then the whole segment $(O, O+Le^{i\theta_0}]$ lies in $J$ — for if one of its points
were interior to $K$, a neighbourhood of it would be in $K$ and $\Gamma(O)$ would contain
directions beyond $\theta_0$. **So the radii available in an extreme direction are either $\emptyset$
or the whole interval $(0,L]$**, never a single positive value; this dichotomy is what the proof
turns on and it is the same phenomenon as the boundary clause of the equilateral convex lane.

> **Theorem C.** Let $T$ have angles $\varphi_1 \le \varphi_2 \le \varphi_3$. Then
> 1. if $\varphi_1 < \gamma(O)$, $O$ is $T$-good;
> 2. if $\varphi_j > \gamma(O)$ for every $j$, $O$ is $T$-exceptional;
> 3. if $\varphi_1 = \gamma(O)$, $O$ is $T$-good iff both extreme directions of $\Gamma(O)$ carry a
>    segment of $J$ ($L>0$ at both ends).
>
> Consequently $E_T(J) \subseteq \{O : \gamma(O) \le \varphi_1\}$ and
> $$\boxed{\ \lvert E_T(\partial K)\rvert \le 2\ }$$
> for every compact convex $K$ with interior and every triangle shape $T$.

**regularity budget: convex.** Used: the tangent cone is an arc; the radial function is positive
and continuous on its interior; the extreme-direction dichotomy above; the IVT; and, for the
counting, that the exterior angles of a convex curve sum to $360°$. **Not used:** the Jordan curve
theorem, smoothness, rectifiability, any degree or winding argument, any limit of triangles.

*Proof of (2).* If $O,P,Q \in K$ then $\angle POQ \le \gamma(O)$, because $K$ lies in the tangent
cone. A triangle similar to $T$ with $O$ at its $j$-th corner needs $\angle POQ = \varphi_j$.

*Proof of (1).* Fix the corner of angle $\varphi := \varphi_1 < \gamma$ and let $k$ be the ratio of
its two adjacent sides, in either order; by Proposition 1 it suffices to realise $k$ **or** $1/k$ as
$\lvert OQ\rvert / \lvert OP\rvert$ with $\arg(Q-O)-\arg(P-O) = \varphi$. Normalise
$\Gamma(O) = [0,\gamma]$ and consider
$$h(\theta) = \frac{R(\theta+\varphi)}{R(\theta)}, \qquad \theta \in (0,\gamma-\varphi),$$
continuous and positive. Let $\mathcal R \subseteq (0,\infty)$ be the set of ratios realised at
angle $\varphi$; it contains $h\bigl((0,\gamma-\varphi)\bigr)$, which is an interval $I$.

- *Upper end.* If $L_0 := \lim_{\theta\downarrow 0}R(\theta) = 0$ then $h(\theta) \to +\infty$, so
  $\sup I = \infty$. If $L_0 > 0$, the extreme direction $0$ carries the segment $(0,L_0]$ of $J$,
  so pairing any $P$ on it with $Q$ at direction $\varphi$ realises every ratio in
  $[R(\varphi)/L_0,\infty)$; and $R(\varphi)/L_0 = \lim_{\theta\downarrow0}h(\theta)$ is an endpoint
  of $\overline I$. Either way $\mathcal R$ contains a set of the form $I \cup [\,b,\infty)$ with
  $b \in \overline I$, i.e. an interval unbounded above.
- *Lower end.* Symmetrically at $\theta \to (\gamma-\varphi)^-$, using the extreme direction
  $\gamma$: $\mathcal R$ contains an interval with infimum $0$, meeting $\overline I$.

Since $\varphi < \gamma$, the interval $(0,\gamma-\varphi)$ is nonempty and $I$ is a nonempty
interval; both additions attach at points of $\overline I$, so $\mathcal R$ contains an interval
with infimum $0$ and supremum $\infty$, i.e. $\mathcal R = (0,\infty) \ni k$. So $O$ is good.

*Proof of (3).* If $\varphi_1 = \gamma$ then the only admissible pair of directions is
$(0,\gamma)$, the two extremes. If both carry segments, the realisable ratios are
$\{t'/t : t \in (0,L_\gamma],\ t'\in(0,L_0]\} = (0,\infty)$ and $O$ is good. If one of them carries
no point of $J$ but $O$, there is no admissible pair at all and $O$ is exceptional.

*Proof of the count.* $E_T(J) \subseteq \{O : \gamma(O) \le \varphi_1\}$ by (1). The corner
excesses $180° - \gamma(O)$ of a convex curve sum to **at most** $360°$ (the total turning of a
convex curve is $360°$ and the corners carry a part of it; equality holds exactly when $\partial K$
is a polygon). So at most two points can have
$180° - \gamma(O) > 120°$, i.e. $\gamma(O) < 60°$. Now $\varphi_1 \le 60°$ always (the smallest angle
of a triangle). If $\varphi_1 < 60°$, then $\gamma(O) \le \varphi_1 < 60°$ at every point of
$E_T(J)$ and at most two such points exist. If $\varphi_1 = 60°$ — i.e. $T$ is equilateral — three
points with $\gamma \le 60°$ would need three exterior angles $\ge 120°$ summing to $\le 360°$,
hence exactly $120°$ each, no other corner, and no turning left over for the corner-free part: the
boundary is then a triangle with three $60°$ corners, i.e. $K$ is equilateral, and each corner carries segments in both extreme directions,
so by (3) all three are **good**. Either way $\lvert E_T(J)\rvert \le 2$. $\square$

### 5.1 What Theorem C settles and what it does not

- It settles the scalene question **for convex curves, affirmatively**: the "all but at most two"
  conclusion holds there for every shape, so a counterexample must be non-convex. Given how easily
  the convex case falls, I would expect this to be known; per
  [`../../RULES.md`](../../RULES.md) §6.1 I record "not found", not "new".
- The bound is attained for every shape: take a convex $K$ with two corners of angle
  $<\varphi_1(T)$, e.g. a sufficiently thin isosceles triangle. §7.7 gives an exact scalene example
  with a hand-checkable witness.
- It says nothing about non-convex curves, and §7.4 shows the criterion is genuinely false there.

### 5.2 Cross-check, not a dependency

[`../convex-vertex-criterion/`](../convex-vertex-criterion/README.md) proves the $\varphi = 60°$
case of this (Theorems A, B(i), B(ii), C, Cor E), including the same two-sided boundary clause. My
proof was written from Proposition 1 and the extreme-direction dichotomy without consulting it, and
the two agree on the equilateral specialisation, including the boundary case — which is the
delicate part. That lane is `sketch`; nothing here rests on it, and §7.2's machine check covers the
same ground independently.

---

## 6. The wedge mechanism alone can never give three

> **Proposition 7.** Let $J$ be any Jordan curve and $T$ any triangle shape, with smallest angle
> $\varphi_1$. Call $O \in J$ **wedge-blocked** if $J$ lies in a closed convex cone with apex $O$
> of opening $< \varphi_1$. Then at most two points of $J$ are wedge-blocked.

*Proof.* A cone is convex, so if $J$ lies in the cone $C_i$ at $O_i$ then so does
$\operatorname{conv}(J) =: K$, a compact convex set. Each $O_i \in J \subseteq K$ and, being the
apex of a cone containing $K$, is an extreme point of $K$ at which the tangent cone has opening
$\gamma(O_i) < \varphi_1 \le 60°$. The corner excesses of $\partial K$ sum to at most $360°$, and
each such point contributes more than $120°$, so there are at most two. $\square$

So **any** curve with $\lvert E_T(J)\rvert \ge 3$ must contain a non-wedge exceptional point. This
is why the search in §7 targeted non-convex curves, and it is the general form of
[`../../RULES.md`](../../RULES.md) §3.1's warning not to over-read the wedge test.

---

## 7. Computation

### 7.1 The exact ledger ([`../../RULES.md`](../../RULES.md) §5)

Everything that decides a `good`/`exceptional` verdict is exact. The complete source is in the
journal, [`../../../../notebook/claude/2026-08-29-iet-scalene.md`](../../../../notebook/claude/2026-08-29-iet-scalene.md),
which is reproducible from one command; nothing is imported from the committed enumerator, which
was **read and run but not modified**.

| step | arithmetic |
|---|---|
| shape $w$, multipliers $M(w)$ | exact in $\mathbb{Q}(\sqrt3)(i)$; for **Gaussian-rational** $w$ the whole computation stays in $\mathbb{Q}$ |
| $\sigma_\mu(J)$ for a polygon $J$ | exact: $\sigma_\mu$ has coefficients in the coordinate field, so $\sigma_\mu(J)$ is again a polygon over it |
| segment intersection, membership, $\lvert E_T\rvert$ verdicts | exact; zero test is syntactic ($1,\sqrt3$ are $\mathbb{Q}$-independent), sign test compares $a^2$ with $3b^2$ |
| witness verification | exact and **correspondence-free**: recompute $P = \sigma_\mu^{-1}(X)$, check $X,P \in J$ from scratch, check pairwise distinctness, and check SSS similarity by sorting the three squared side lengths and comparing ratios — $\mu$ is not trusted |
| angle comparisons (wedge classification, $\varphi_{\min}$) | exact: $\cos\theta_1 \gtrless \cos\theta_2$ decided by comparing $A^2D$ with $C^2B$ with sign bookkeeping, never by an arctangent |
| **search heuristics only** | float (`screen.py`) and a float raster of the blocked-multiplier region; **every candidate they emit is re-decided exactly**, and every reported verdict below is the exact one |

**No sympy geometry predicate is used anywhere**, per the brief and
[`../../RULES.md`](../../RULES.md) §5; the committed enumerator's own cross-check found sympy wrong
on 3 of 176 boundary cases in this problem.

**A bug I introduced and caught, recorded because §0 of the repo rules is about exactly this.** My
first witness verifier hard-coded the corner correspondence $O \leftrightarrow 0$,
$P \leftrightarrow 1$, $X \leftrightarrow w$, which is right only for the role $\mu = w$; on the
role $\mu = 1-w$ it rejected perfectly good witnesses and aborted the run. The *decider* was
correct; the *checker* was wrong — the failure mode the brief warned about, four times over in this
session. The fix was to make the check correspondence-free (sorted side-length triples), which is
also strictly more independent of how the witness was found.

### 7.2 Validation — K1

My general-$T$ decider, specialised to $\mu = e^{i60°}$, versus the committed equilateral decider
`experiments/inscribed-triangle-polygons/`, on that decider's **entire** battery:

| | value |
|---|---|
| fixtures | **190** (its full battery, including the three controls, the exactly-$60°$ family and the non-convex C-strips) |
| points compared | **1566** (every vertex and every edge midpoint) |
| disagreements | **0** |

Independently, the float pre-screen was checked against my exact decider on **2736** points
(7 polygons × 36 scalene shapes × all candidate points) with **0** disagreements in either
direction, and in the main scans **1774** screened-exceptional points were re-decided exactly and
**all 1774** were confirmed exceptional (no false positives).

The controls come out right: the unit square's corners are good, the $30$–$30$–$120$ triangle's two
$30°$ apexes are exceptional and its $120°$ vertex is good, the equilateral triangle's vertices are
all good.

### 7.3 Theorem C against the machine — K2

66 convex polygons (hand fixtures plus seeded random rational hulls) × 11 shapes (10 scalene
Gaussian-rational, 1 equilateral), all vertices and all edge midpoints:

| | value |
|---|---|
| points decided exactly | **6380** |
| predicted good $\iff$ $\gamma(O) \ge \varphi_{\min}(T)$ (polygon case of Theorem C) | **0 mismatches** |
| $\lvert\{$exceptional vertices$\}\rvert$ per (polygon, shape) | $0$: 617 · $1$: 64 · $2$: 45 · $\ge3$: **0** |

### 7.4 A non-wedge exceptional point on a polygon

The census (below) recorded, for every exactly-confirmed exceptional point, whether it is
wedge-blocked in the sense of Proposition 7 — decided exactly, by searching pairs of vertex
directions spanning a cone that contains all of them and comparing its opening with
$\varphi_{\min}(T)$ by an exact cosine comparison.

Of **1774** exactly-confirmed exceptional points on non-convex polygons, **22 are not
wedge-blocked**. An example, exact and reproducible:

$$J = \partial\bigl[(9,1),(26,18),(15,16),(12,18),(-8,12),(-30,-20),(-26,-24),(-3,-19),(5,-24)\bigr],
\qquad O = (26,18),$$
$$w = \tfrac13 + i \quad\text{(sides}^2 = 1 : \tfrac{10}{9} : \tfrac{13}{9},\ \text{angles}
\approx 71.57°,\ 56.31°,\ 52.13°,\ \text{scalene)} .$$
All six roles are blocked — the exact decider returns no witness for any $\mu \in M(w)$ — and
no cone at $O$ of opening $< \varphi_{\min} \approx 52.13°$ contains $J$. So $O$ is $T$-exceptional
by a mechanism the wedge test cannot see, on a *polygon*.

**Do not over-read it.** I ran the same scan with the **equilateral** shape and found non-wedge
exceptional points there too (4 of 30 exceptional points, e.g. the vertex $(1,0)$ of the polygonal
spiral fixture). So "non-wedge exceptional points exist on polygons" is a fact about non-convex
curves, **not** a phenomenon of $k \ne 1$; it is [`../../RULES.md`](../../RULES.md) §3.1's own
warning ("a reflex polygon may have an interior angle under $60°$ that is still a triangle vertex")
showing up from the other side. What §7.4 adds is that these points are common enough to find by
search, in both regimes, and that the wedge test is therefore not a classification for either.

### 7.5 The census — no $\lvert E_T\rvert \ge 3$

| | value |
|---|---|
| polygons | **75** — the $30$–$30$–$120$ control, slivers, a square, a thin "Y", 25 spiked stars ($k=3..7$ spikes, 5 depths), 6 polygonal **rational logarithmic spirals** ($z_{n+1} = s\cdot\tfrac{3+4i}{5}z_n$, exactly rational), 3 combs, 40 seeded random star-shaped polygons (5–12 vertices) |
| shapes | **881** scalene Gaussian-rational $w = a/3 + (b/3)i$, plus the equilateral shape as a control |
| (polygon, shape) pairs | **66 075** |
| candidate points per curve | every vertex and 3 interior points per edge |
| distribution of the number of exceptional candidate points | $0$: 65 146 · $1$: 50 · $2$: **879** · $\ge3$: **0** |
| exact re-decisions of screened-exceptional points | **1774**, all confirmed |

A second, sharper pass computed for each candidate point a **raster of its blocked multiplier set**
$B(O) = \mathbb{C}^\times \setminus \{(X-O)/(P-O)\}$ in log-polar coordinates — an outer
approximation, so it cannot miss a genuine counterexample at its resolution — and searched shape
space for a $w$ whose six multipliers lie in $B(O)$ for three points at once. It flagged 5
polygons; **984** exact shape decisions on those flagged cases returned **maximum
$\lvert E_T\rvert = 2$** and **zero** hits.

**What this does and does not establish.** It is `numerical`, and doubly limited: (i) it decides
finitely many points per curve, so it could not certify $\lvert E_T(J)\rvert \le 2$ even for the
*particular* polygons tested — a third exceptional point could sit in an edge interior between
sampled points; (ii) polygons are the most regular curves there are, and the spiral tip (§4) is
already an example of a mechanism that no polygon exhibits. So this is evidence that
$\lvert E_T\rvert \ge 3$ is not *easy*, and nothing more.

### 7.6 Two auxiliary checks

- **Theorem 5** (spiral tip): a brute-force search over $r$ using only the direction-set normal form
  — independent of my algebra — on **480** random $(c,\beta,\varphi,k)$ with
  $c \in \{0.3,1,2,5\}$, $\beta \in \{10°,30°,55°\}$: **0 mismatches** with
  $\lvert\Lambda_c(\mu)\rvert \le \beta$.
- **Proposition 3** (sharp constant): the one-dimensional optimum of §3.1 computed by an exact
  max-weight-independent-set dynamic program on a fine grid, versus $1/(1+k^2)$:

| $k$ | 0.9 | 0.7 | 0.5 | 0.3 | 0.1 |
|---|---|---|---|---|---|
| DP | 0.552486 | 0.671141 | 0.800000 | 0.917431 | 0.990099 |
| $1/(1+k^2)$ | 0.552486 | 0.671141 | 0.800000 | 0.917431 | 0.990099 |

### 7.7 An exact scalene example attaining $\lvert E_T\rvert = 2$, with a hand check

$J$ = the sliver triangle $(0,0),(100,0),(50,1)$; $w = -3+2i$, so
$T$ has squared sides $1 : 13 : 20$ and angles $\approx 146.31°, 26.57°, 7.13°$ —
scalene, with $\varphi_{\min} \approx 7.13°$.

- The two apexes have interior angle $\arctan(1/50) \approx 1.146° < \varphi_{\min}$, so they are
  wedge-blocked and hence $T$-exceptional; the decider agrees.
- The apex $(50,1)$ has interior angle $\approx 177.71° > 146.31°$, so Theorem C says it is good.
  The decider returns the role $\mu = -3+2i$ with $P = (48,0)$, $X = (58,0)$.
  **Hand check:** $P - O = (-2,-1) = -2-i$; $\mu(P-O) = (-3+2i)(-2-i) = 6+3i-4i-2i^2 = 8-i$; so
  $X = O + (8,-1) = (58,0)$ ✓. $P$ and $X$ lie on the edge $[(0,0),(100,0)]$ ✓. Squared sides
  $\lvert OP\rvert^2 = 5$, $\lvert OX\rvert^2 = 65$, $\lvert PX\rvert^2 = 100$, i.e.
  $5 : 65 : 100 = 1 : 13 : 20$ ✓ — the shape of $T$, exactly. All three sides positive, so
  nondegenerate ✓.
- Edge midpoints: all good.

So $\lvert E_T(J)\rvert = 2$ for this scalene $T$ (by Theorem C, which decides *every* point of a
convex curve, not merely the sampled ones). **The bound two is attained for scalene shapes as well
as for the equilateral one** — which is the expected answer and is worth recording because it is
the first thing a reader will ask.

---

## 8. The three cheap filters ([`../../RULES.md`](../../RULES.md) §3), all run

### 8.1 Wedge test (§3.1)

Run, and generalised rather than merely passed. The generalisation is "$J$ inside a cone of opening
$< \varphi_{\min}(T)$ at $O$ $\Rightarrow$ $O$ is $T$-exceptional", which is Theorem C(2) and is
proved above. The $30$–$30$–$120$ witness is reproduced by the decider for the equilateral shape
(§7.2), and Proposition 7 says the mechanism caps at two points for every shape — so no argument in
this file can imply "every point of every Jordan curve is a $T$-vertex", and none does.

### 8.2 Square test (§3.2) — why nothing here transfers

**The honest form of the test for a general shape $T$ is a *quadrilateral* peg problem**, and this
is where the file must be explicit.

Fix a quadrilateral shape $Q = (q_0,q_1,q_2,q_3)$ and ask whether $O \in J$ is a vertex of an
inscribed similar copy. A similar copy is determined by the images of two vertices, so with $O$ at
$q_0$ and $P$ the image of $q_1$ the other two vertices are forced:
$$R = \sigma_{\mu_2}(P), \qquad S = \sigma_{\mu_3}(P), \qquad
\mu_j = \frac{q_j - q_0}{q_1 - q_0}.$$
Hence the criterion becomes
$$O \text{ good} \iff J \cap \sigma_{\mu_2}^{-1}(J) \cap \sigma_{\mu_3}^{-1}(J) \ne \{O\},$$
a **triple** intersection. Proposition 1 produces a **double** intersection. Two plane curves
generically meet in points; three generically do not meet at all. **Every result in this file
consumes exactly that difference:**

- *Proposition 1* is an iff between "$O$ is a vertex" and one intersection being non-trivial. The
  quadrilateral version is an iff with a triple intersection, and nothing here says anything about
  triple intersections.
- *Theorem C* solves **one** scalar equation $R(\theta+\varphi)/R(\theta) = k$ in **one** unknown
  $\theta$ by the intermediate value theorem, with the extreme directions supplying the two ends.
  The square version needs $R(\theta+90°)/R(\theta) = 1$ **and** the fourth vertex
  $P + Q - O$ to lie on $J$ — two conditions, one unknown. The IVT gives the first and is silent on
  the second. So Theorem C does **not** prove "every point of a convex curve with $\gamma \ge 90°$
  is a vertex of an inscribed square", and I make no such claim.
- *Theorem 5* computes $\Theta_J(r)$ for one explicit curve and compares two circles. A square at
  $O$ would constrain three points besides $O$, i.e. three circles, and the normal form gives no
  purchase on that.
- *Lemma A$_\sigma$* and *Proposition 3* are statements about one map $\sigma$ and say nothing about
  a pair of maps constrained simultaneously.

The lane is in any case a *counterexample* hunt for triangles, so the §3.2 failure mode ("your
argument proves the square peg theorem") could only arise through Theorem C, and the paragraph above
is the specific reason it does not. **Pass.**

### 8.3 Polygon control (§3.3)

Run in full: §7.2 (my decider against the committed one, 1566 points), §7.3 (Theorem C against 6380
exact decisions), §7.5 (the census). Every general claim in this file that *can* be tested on a
polygon was tested on one:

| claim | polygon test | outcome |
|---|---|---|
| Proposition 1 | equilateral specialisation vs. committed decider | 1566 points, 0 disagreements |
| Theorem C | 66 convex polygons × 11 shapes | 6380 points, 0 mismatches |
| Proposition 7 / §7.4 | wedge classification of every exceptional point found | 22 non-wedge points found — the wedge test is not a classification |
| the lane's target | 66 075 (polygon, shape) pairs | no $\lvert E_T\rvert \ge 3$ |

Lemma A$_\sigma$, Proposition 3 and Theorem 5 are **not** polygon-testable: the first two are about
measure and nesting rather than about which points are exceptional, and Theorem 5 is a statement
about a curve with infinitely many windings, which no polygon has. Their checks are §7.6's and
their own proofs. A claim that survives polygons is *merely not-yet-dead*, per §3.3.

---

## 9. The literature tension — what can and cannot be settled here

[`../../README.md`](../../README.md) records two things in tension, both `cited`\* and both
provisional, from a session in which **no scholarly host is reachable** and no paper body or
abstract was read:

- **Row 6.** Schwartz: for each Jordan loop $J$ there is an **uncountable** set $G(J)$ of shapes for
  which the "all but at most two points" conclusion holds, and $G(J)$ meets every angle in
  $(0,\pi/2)$.
- **Open item 2.** A single snippet asserting the all-but-finitely-many conclusion "is not known for
  any other shape of triangle (e.g. right isosceles)".

**These do not contradict each other, and the reason is the order of the quantifiers.**
Row 6 is
$$\forall J\ \exists G(J) \text{ uncountable}\ \forall T \in G(J):\ \lvert E_T(J)\rvert \le 2,$$
in which the shape set is allowed to **depend on the curve**. The snippet is about
$$\exists T \text{ (a fixed shape)}\ \forall J:\ \lvert E_T(J)\rvert \le 2,$$
uniformly in $J$. The second does not follow from the first: $\bigcap_J G(J)$ could be exactly the
equilateral shape even with every $G(J)$ uncountable. So a reader need not conclude that one of the
two rows is wrong, and this lane's target — *is there a fixed scalene $T$ and a curve $J$ with
$\lvert E_T(J)\rvert \ge 3$?* — is the negation of the **uniform** statement and is untouched by
row 6 as recorded.

**This is an observation about two sentences in our own README, not a finding about either paper.**
I could not read Schwartz, I do not know whether $G(J)$ is in fact curve-independent, and per
[`../../RULES.md`](../../RULES.md) §6.1 "not found" is not "open". Kill-criterion **K9** applies:
I do not assert that the scalene question is open. What I can say precisely is what §5 adds to it:
**for convex $J$, $G(J)$ is everything**, so any curve-dependence of $G(J)$ lives entirely in the
non-convex world.

**What a reader with journal access must check**, in priority order:

1. Schwartz, *On spaces of inscribed triangles*, arXiv:1908.08174 — is $G(J)$ curve-dependent, and
   does it contain shapes with all three angles distinct? If $G(J)$ is curve-**in**dependent and
   uncountable, this lane's target is dead and §5 is a special case of a known theorem.
2. The provenance of the "not known for any other shape" snippet. It is a single secondary summary;
   if it is a paraphrase of Schwartz's own introduction it is strong evidence the uniform question
   is open, and if it is a garbled restatement of row 6 it is worthless.
3. Meyerson (1980) — whether the proof is specific to the $60°$ rotation, or whether it is a degree
   argument that would run for any spiral similarity. §1.4 says what would have to be replaced: one
   condition becomes six, and $\mu^{-1} \ne \bar\mu$.
4. Whether the convex case (Theorem C) is in the literature. It falls out of an IVT and I would
   expect it to be folklore.

---

## 10. Kill-criterion outcomes

Against [`KILL-CRITERION.md`](./KILL-CRITERION.md), written before any computation here.

| # | Criterion | Outcome |
|---|---|---|
| **K1** | criterion wrong (disagrees with the committed decider at $\mu = e^{i60°}$) | **not met.** 190 fixtures, 1566 points, 0 disagreements (§7.2). |
| **K2** | convex theorem false | **not met.** 6380 exact decisions, 0 mismatches (§7.3). The theorem's boundary clause (3) was exercised by the committed battery's exactly-$60°$ family, which my decider re-decided identically. |
| **K3** | my spiral corollary disagrees with the spiral lane's §10 | **not met.** Independent derivation (§4.3) agrees, sign included; 480 random parameter sets brute-forced with 0 mismatches (§7.6). That lane's least-checked line survives a genuinely independent check. |
| **K4** | apparent $\lvert E_T\rvert \ge 3$ (reporting gate) | **did not fire — nothing to report.** The gate was never reached: no candidate survived exact decision. The five raster-flagged polygons were all false positives of the float screen, and were caught by exact re-decision, which is what the two-stage design is for. |
| **K5** | half-density analogue not as claimed | **not met.** Sharp constant $1/(1+k^2)$ proved both ways (attaining set and matching upper bound), and checked against an exact DP (§7.6). |
| **K6** | a float decides something | **not met.** §7.1 is the ledger. Floats appear only in the screen and the raster, both of which feed the exact decider; the exact decider re-decided 1774 screened points and confirmed all of them, plus 984 shapes on the raster-flagged polygons. No sympy geometry predicate anywhere. |
| **K7** | compute budget (20 minutes) | **not met.** Total wall clock across all runs is **under 10 minutes**: cross-check 22 s, convex test 93 s, census 68 s, raster 85 s, exact confirmation of the raster flags under 3 min, mechanism scan 70 s, first coarse hunt 2 s, auxiliary checks $< 30$ s. Two runs were backgrounded and both were collected; nothing was left running. |
| **K8** | three-tip construction not closed | **met — and reported as not done.** §11.2 states the obstruction; no partial construction is written up as a result. |
| **K9** | over-reading the literature gap | **not met**, and §9 is the discipline: the tension is described as a quantifier-order artefact of our own README, no claim of openness is made, and the reader's checklist is explicit. |

**Verdict.** The lane's target was not achieved and is not claimed. What it produced is the
criterion (§1), a sharp account of which equilateral tools survive $k \ne 1$ (§2–§4), a positive
theorem for convex curves and every shape (§5), a general cap on the wedge mechanism (§6), and a
negative census (§7).

---

## 11. What is open, and what I did not do

### 11.1 The question itself

Whether there is a scalene $T$ and a Jordan curve $J$ with $\lvert E_T(J)\rvert \ge 3$ is, as far as
this lane could determine, **unresolved in this repository** — which is a statement about this
repository, not about the mathematical literature (§9, K9). Nothing here is evidence that it is
open; nothing here is evidence that it is known.

### 11.2 The three-tip construction (K8 — not done)

I3 proposes three spiral tips of suitable pitches on one Jordan curve. §4 supplies the local theory
in closed form and shows that the six pitch conditions at one tip are avoidable for every shape
(Corollary 6). What is **not** done is the global arrangement, and the obstruction is specific:

- Exceptionality at a tip $O_1$ is a condition on $\Theta_{O_1}(r)$ for **every** $r$, including the
  radii at which the other two tips and the connecting arcs live. Theorem 5's proof works only
  because $J_{c,\beta}$ *is* two arms and one arc, so that every circle meets $J$ in at most two
  points plus one arc.
- $(\dagger)$ of §4.1 forbids the cheap fix: $\Theta_J(r) \ne \emptyset$ for every $r \le D$, so one
  cannot arrange the curve to be *absent* at the radii $kr$.
- A connecting arc that is radial from $O_1$ contributes one direction, constant in $r$; the arms
  contribute $\tau(r)$, which sweeps every direction. The coincidence
  $\tau(r) + \varphi \equiv \theta_{\text{seg}}$ is then a single equation in $r$, and whether it has
  a solution in the admissible window depends on how far $\tau$ turns while $kr$ stays inside the
  segment's radius range — a *finite* set of conditions, plausibly dodgeable, and I did not verify
  that they can all be dodged at three tips simultaneously.

I estimate this at one to two focused worktree-days and it is the natural successor issue. **It is
not a result and is not written up as one.**

### 11.3 Other things this lane opens

1. **Is $\lvert E_T(J)\rvert \le 2$ true for polygons and every $T$?** The census found no
   counterexample in 66 075 pairs. Deciding it for a *given* polygon is a semialgebraic
   quantifier-elimination problem (§7.5(i)) and would make the numerics into a theorem for that
   curve; deciding it for all polygons is a real question and might be reachable, since §4.1's
   $(\dagger)$ and §6 constrain the possibilities heavily.
2. **Does the shrinking-nesting alternative of Lemma A$_\sigma$ have any consequence at all?** It is
   the only surviving configuration for $k<1$, it is realised at the spiral tip, and I found no
   obstruction that sees it. A measure or index argument adapted to $\nu = \mathrm{d}\lambda/r^2$
   (§3.2) is the obvious place to look.
3. **A Lean target.** Proposition 1 is plane geometry with no topology in it — the same shape as the
   rotation identity that [`../../RULES.md`](../../RULES.md) §6.3 already names as a real Lean
   target, with $\mu \in \mathbb{C}^\times$ in place of $e^{i60°}$. Lemma 2 (§1.5) is two lines and
   needs only the triangle inequality. Proposition 3 needs a Fubini/independent-set argument and is
   harder but topology-free. Theorem C needs the IVT and convexity but no Jordan curve theorem, so
   it is not blocked by the Mathlib gap. I could not attempt any of these: `elan` is absent from
   this container and every route to install it is blocked by the egress proxy, exactly as the
   half-density lane records.

---

## 12. For a cross-examiner: where to attack

Per [`../../RULES.md`](../../RULES.md) §6.2, and in the order I think an error is most likely.

1. **§1.2, the $(\Rightarrow)$ direction of Proposition 1 — the enumeration of $M(w)$.** This is the
   single load-bearing piece of bookkeeping in the file and everything else is downstream of it.
   Reconstruct it yourself: the six permutations of $(0,1,w)$, their $\mu$-values, the closure of
   that set under inversion, and the conjugates. If $M(w)$ is missing a role, then *every*
   "exceptional" verdict in §7 is potentially a false positive, and §5's Theorem C(1) proves too
   little rather than too much. Attack in particular whether I am entitled to reduce twelve maps to
   six by $\mu \leftrightarrow \mu^{-1}$.
2. **§5, Theorem C(1) — continuity of $R$ and the "attachment" step.** First check the
   continuity of the radial function on the *interior* of the tangent cone, and the claim that a
   direction interior to the cone enters $\operatorname{int}K$ — both are used without further
   comment. Then the claim that
   $\mathcal R \supseteq I \cup [b,\infty) \cup (0,a]$ is an interval, using that $b$ and $a$ are in
   $\overline I$. Check the degenerate configurations: $\gamma - \varphi$ tiny, $I$ empty, both
   extreme directions carrying segments, neither carrying one, and $K$ with a segment through $O$
   in its *interior* direction. This is where the equilateral convex lane needed a two-sided
   boundary clause, and boundary clauses are where such proofs break.
3. **§5's counting step.** "Exterior angles of a convex curve sum to $360°$" is doing real work for
   a possibly non-polygonal, non-smooth convex body, where "the exterior angle at $O$" must be read
   as $180° - \gamma(O)$ and summed over the countably many corners. Check that the sum is
   $\le 360°$ in that generality, and check the equality case I use for $\varphi_1 = 60°$.
4. **§4.3, the case split on radii.** Verify that $r<1, kr<1$; $r=1$; $kr=1$; and $r>1$ or $kr>1$
   exhaust the possibilities, and that the three isolated values of the first case really are
   inside the interval of the second (they are, but the mod-$360°$ bookkeeping is the kind of thing
   that goes wrong).
5. **§3.1, Step 1.** The shear $\Phi$ must be well defined on the cylinder, measure preserving, and
   must preserve the ball $\{u\le 0\}$. Check that it does not shear the ball into something else —
   it does not, because it fixes $u$ — and that conjugating the translation is legitimate when
   $\varphi/a$ is irrational.
6. **§2, Lemma A$_\sigma$.** The Jordan curve theorem is applied to $J' = \sigma(J)$; that is
   legitimate because $\sigma$ is a homeomorphism of the plane, and this is the one place topology
   could be smuggled. Check also that "the expanding nesting is impossible" really uses
   $\lambda(\overline\Omega) < \infty$ and $\lambda(\Omega) > 0$ and nothing else.
7. **§7.** Reimplement the decider independently rather than rerunning mine — the problem's
   [`RULES.md`](../../RULES.md) §3.3 and the repo's §5 both require this for computational content,
   and my own §7.1 records a checker bug that a rerun would have reproduced faithfully. The cheapest
   independent check is §7.7's hand computation, which needs no code at all.

**Where I would put my own money on an error:** §5's Theorem C(1), specifically the boundary
behaviour at the extreme directions. It is the only argument in the file with a case analysis I did
not machine-check exhaustively — §7.3 tests polygons, where both extremes always carry segments, so
the $L = 0$ branch is exercised by *no* fixture in the census. A convex body with a corner formed by
two circular arcs would exercise it, and I did not build one.
