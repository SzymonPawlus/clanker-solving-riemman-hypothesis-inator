# Attack: the 60° rotation route, and exactly how far it goes

**regularity budget: varies by statement — see the per-statement line in each section.** The
strongest statement proved here consumes **Jordan + an explicit local cone/crosscut hypothesis at
one point** (§6), which I can verify for **$C^1$** and **polygonal** curves and, importantly,
**cannot** verify for merely rectifiable ones (§6.4 — a gap I found by re-deriving my own first
draft, and the single most instructive thing in this file). Nothing here proves anything about a
general continuous Jordan curve; §7 and §8 say precisely where that fails.

- Route: for $O \in J$, rotate $J$ by $60°$ about $O$ and look for a second intersection point.
- Author: `claude` (Claude Opus 5), 2026-08-29, issue #132.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md) (see its provenance note — it was
  **not** written before the §3 computation).
- Journal: [`../../../../notebook/claude/2026-08-29-iet-rotation.md`](../../../../notebook/claude/2026-08-29-iet-rotation.md).
- Problem rules consumed: [`../../RULES.md`](../../RULES.md) §1 (budget lines), §2 (noncollapse,
  §8 below), §3.1/§3.2/§3.3 (three filters, all three run — §3, §9, §10 below), §5 (exact
  arithmetic — everything computational here is exact in $\mathbb{Q}(\sqrt3)$).

| § | Statement | Status |
|---|---|---|
| §2 | **Observation R.** $O$ is a vertex of an inscribed equilateral triangle $\iff J \cap \rho_{O,60°}(J) \supsetneq \{O\}$ | `sketch` — mine; three lines, and the $\Leftarrow$ half is [`../../RULES.md`](../../RULES.md) §3.2's reference statement. Not assumable. |
| §3 | **The naive strategy "pick any $O \in J$" is false**, with an exact witness | `refuted` — settled; exact witness, exact computation |
| §3 | Exact intersection sets for the $30$–$30$–$120$ triangle | `numerical` (exact algebraic, not floating point) |
| §4 | **Lemma A (no nesting).** $J \cap \rho(J) = \{O\} \Rightarrow \overline{\Omega} \cap \rho(\overline{\Omega}) = \{O\}$ | `sketch` — mine; Jordan curve theorem + Lebesgue measure |
| §5 | **Lemma B (sector criterion).** A closed sector of aperture $\ge 60°$ at $O$ inside $\overline{\Omega}$ $\Rightarrow$ $O$ is a vertex | `sketch` — mine; depends on §2 and §4 |
| §6 | **Theorem C (local crosscut criterion).** Hypothesis (C) at $O$ $\Rightarrow$ $O$ is a vertex | `sketch` — mine; depends on §4, §5 |
| §6.3 | Corollaries: every point of a regular $C^1$ Jordan curve, and every point of a simple polygon with interior angle $\ge 60°$ | `sketch` — mine. **Subsumed by Meyerson (1980)**, see §10 |
| §6.4 | The same for merely **rectifiable** curves | **not established** — I could not verify hypothesis (C) at an a.e.-differentiability point; my first draft claimed it, wrongly. See §6.4 |
| §7 | Area/measure framing as a *standalone* route to the general case | `refuted` — it kills nesting only, and the counterexample of §3 is the other case |
| §7 | Winding-number / degree framing | **not achieved** — I could not get anything past what §4 already gives |
| §8 | Varying $O$ for a general Jordan curve | no theorem; §8 states the precise obstruction and its noncollapse form |
| §9 | Square non-transfer ([`../../RULES.md`](../../RULES.md) §3.2) | `sketch` — checked, and the argument does **not** transfer |
| §10 | The rotation route is (reportedly) the classical proof | `sketch`-level literature note at provenance **P3**; **not** a citation, see the caveat |

**Dependency hygiene.** Every argument in §2–§8 is self-contained and rests only on the Jordan
curve theorem and Lebesgue measure. Nothing here uses the `cited` rows of
[`../README.md`](../README.md); Meyerson's theorem appears only in §10 as an external cross-check
*on* my conclusions, never as an input to them. That matters because those rows are provisional
(provenance P2, no source text read), and because a `sketch` may not rest on a `sketch`.

---

## 1. Why this lane exists

The problem's central question is settled ([`../README.md`](../README.md)), so this directory's job
is a faithful record of *which* arguments work and which do not. This lane records the elementary
rotation route: what it proves, the exact point at which it stops, and the counterexample that
stops it. The counterexample is the main deliverable — a documented refutation is a first-class
result here ([`../../../README.md`](../../../README.md)).

Concurrent lanes own the convex case (`attacks/convex-vertex-criterion/`), the literature, and the
polygon enumerator. This file makes no claim about any of them.

---

## 2. Observation R — the reduction, and its converse

> **Observation R.** Let $J$ be a Jordan curve, $O \in J$, and $\rho = \rho_{O,60°}$ the rotation
> of the plane by $+60°$ about $O$. Then
> $$O \text{ is a vertex of an equilateral triangle inscribed in } J \iff J \cap \rho(J) \supsetneq \{O\}.$$

**regularity budget: none** — $J$ is used only as a set of points; injectivity, connectedness and
even closedness are unused. The statement holds for an arbitrary $S \subseteq \mathbb{R}^2$ with
$O \in S$.

*Proof.* ($\Leftarrow$) Let $q \in J \cap \rho(J)$, $q \neq O$, and put $p = \rho^{-1}(q) \in J$.
A rotation about $O$ is an isometry fixing $O$, so $|Op| = |\rho(O)\rho(p)| = |Oq|$, and the angle
$\angle pOq$ is the rotation angle $60°$. An isosceles triangle with apex angle $60°$ has base
angles $(180° - 60°)/2 = 60°$, hence is equilateral. Nondegeneracy: $|Oq| > 0$ because $q \ne O$,
and $p \ne q$ because $\angle pOq = 60° \ne 0$. So $O, p, q$ are three distinct points of $J$ at
equal pairwise distances.

($\Rightarrow$) Let $O, A, B \in J$ be an equilateral triangle. Then $B = \rho_{O,+60°}(A)$ or
$B = \rho_{O,-60°}(A)$. In the first case $B \in J \cap \rho(J)$ and $B \ne O$. In the second,
$A = \rho_{O,+60°}(B)$, so $A \in J \cap \rho(J)$ and $A \ne O$. $\square$

**Two remarks that matter downstream.**

1. **The $\pm$ is redundant.** [`../../RULES.md`](../../RULES.md) §3.2 states the $\Leftarrow$
   direction. The $\Rightarrow$ direction shows a single orientation already captures every
   inscribed equilateral triangle through $O$, so testing $\rho_{+60°}$ alone is *complete*: if
   $J \cap \rho_{+60°}(J) = \{O\}$ then $O$ is exceptional, full stop. This is what upgrades §3
   from "the rotation trick fails here" to "$O$ is genuinely exceptional".
2. **$O$ is always in the intersection**, since $\rho(O) = O$. It is the degenerate solution, as
   [`../../RULES.md`](../../RULES.md) §2 warns. The entire content of the route is producing a
   *second* point — and, note, no limit is taken anywhere, so noncollapse is free here (§8).

**Self-check performed.** Verified symbolically that for $p$ at polar $(r,\theta)$ and
$q = \rho_{O,60°}(p)$, all three of $|Op|, |Oq|, |pq|$ simplify to $r$ (script in §11, part (a)).
The observation held up; nothing in this lane collapses.

---

## 3. `refuted`: "rotate at *any* point of $J$" — exact witness

> **Refuted statement.** *For every Jordan curve $J$ and every $O \in J$,
> $J \cap \rho_{O,60°}(J) \supsetneq \{O\}$* — equivalently, every point of every Jordan curve is
> a vertex of an inscribed equilateral triangle.

**regularity budget of the refutation: polygonal + convex** (a triangle boundary). Dropping
convexity is what would break it — see "Do not over-read this" below.

### The witness, with exact coordinates

$$T = \text{boundary of the triangle } O=(0,0),\quad A=(1,0),\quad C=\left(\tfrac12,\tfrac{\sqrt3}{6}\right).$$

Exact data, all computed in $\mathbb{Q}(\sqrt3)$ rather than asserted:

$$|OA| = 1,\qquad |OC| = |AC| = \tfrac{\sqrt3}{3},\qquad \angle O = \angle A = 30°,\quad \angle C = 120°.$$

So $T$ is the $30°$–$30°$–$120°$ isosceles triangle, and $O$ and $A$ are its two $30°$ apexes.

$$\rho_{O,+60°}(T) \text{ has vertices } (0,0),\ \left(\tfrac12,\tfrac{\sqrt3}{2}\right),\ \left(0,\tfrac{\sqrt3}{3}\right),$$
$$\rho_{O,-60°}(T) \text{ has vertices } (0,0),\ \left(\tfrac12,-\tfrac{\sqrt3}{2}\right),\ \left(\tfrac12,-\tfrac{\sqrt3}{6}\right).$$

Exact segment-by-segment intersection over $\mathbb{Q}(\sqrt3)$ (9 segment pairs each; §11 part (b))
returns

$$T \cap \rho_{O,+60°}(T) = \{(0,0)\}, \qquad T \cap \rho_{O,-60°}(T) = \{(0,0)\},$$

and by symmetry the same at $A$ (verified: $T \cap \rho_{A,\pm60°}(T) = \{(1,0)\}$). By
Observation R ($\Rightarrow$), **$O$ and $A$ are exceptional points of $T$**: no equilateral
triangle inscribed in $T$ has either as a vertex.

### The two-line reason, independent of the computation

$T$ is **convex**, so $T \subseteq K$ where $K$ is the closed cone at $O$ spanned by the directions
$0°$ and $30°$ (the two edge directions). Then $\rho_{O,60°}(T) \subseteq \rho_{O,60°}(K)$, the
cone spanned by $60°$ and $90°$. Two closed convex cones at $O$ with disjoint direction arcs
$[0°,30°]$ and $[60°,90°]$ meet only at their apex. Hence $T \cap \rho(T) = \{O\}$. The same for
$-60°$ (arc $[-60°,-30°]$).

This is exactly the **wedge test** of [`../../RULES.md`](../../RULES.md) §3.1, arrived at
independently here. The computation adds the exact intersection sets and confirms that the wedge
test and the rotation route agree on the same witness rather than merely being compatible.

### The curve is not a counterexample to the theorem

$T$ *does* inscribe equilateral triangles — the failure is of the strategy at a bad choice of $O$,
not of the conclusion. At the $120°$ vertex $C$ the route works, and exactly (§11 part (b) again):

$$T \cap \rho_{C,+60°}(T) = \left\{\left(\tfrac12,0\right),\ \left(\tfrac12,\tfrac{\sqrt3}{6}\right),\ \left(\tfrac23,0\right),\ \left(\tfrac34,\tfrac{\sqrt3}{12}\right)\right\},$$

yielding for instance the inscribed equilateral triangle
$$\left(\tfrac12,\tfrac{\sqrt3}{6}\right),\ \left(\tfrac13,0\right),\ \left(\tfrac23,0\right)\quad\text{of side } \tfrac13,$$
whose vertices lie on $T$ ($C$, and two points of the edge $OA$) and whose three side lengths are
each exactly $1/3$. Two further triangles of side $\sqrt3/6$ appear in the same output.

### Do not over-read this

The refutation kills "every $O$ works". It does **not** say "interior angle $< 60°$ $\Rightarrow$
exceptional". Convexity is doing real work: it is what promotes the *local* statement (the two
wedges separate near $O$) to the *global* one (the two curves are disjoint away from $O$). For a
reflex polygon a vertex of interior angle $< 60°$ may still be a triangle vertex, because the curve
leaves the wedge and can meet the rotated copy far away. This is the same warning as
[`../../RULES.md`](../../RULES.md) §3.1 and I restate it because the temptation to drop convexity
here is strong and the resulting statement is false.

---

## 4. Lemma A — the intersection dichotomy, and what measure actually buys

Notation for the rest of this file: $\Omega$ is the bounded complementary component of $J$ and $E$
the unbounded one, so $\partial\Omega = \partial E = J$ and $\overline{\Omega} = \mathbb{R}^2
\setminus E$. Primes denote the $\rho$-image: $J' = \rho(J)$, $\Omega' = \rho(\Omega)$,
$E' = \rho(E)$. $\lambda$ is planar Lebesgue measure.

> **Lemma A.** If $J \cap \rho(J) = \{O\}$ then $\Omega \cap \Omega' = \emptyset$; in fact
> $\overline{\Omega} \cap \overline{\Omega'} = \{O\}$.

**regularity budget: Jordan only.** No rectifiability, no tangent, no local structure. What breaks
first if you drop "Jordan": the argument uses the Jordan curve theorem twice (two complementary
components, and $\partial E = J$), so it does not survive weakening $J$ to a general continuum.

*Proof.* $J' \setminus \{O\}$ is connected ($S^1$ minus a point) and disjoint from $J$, so it lies
in $\Omega$ or in $E$.

**Case A: $J' \setminus \{O\} \subseteq \Omega$.** Then $J' \subseteq \overline\Omega$, so
$E \cap J' = \emptyset$; $E$ is connected and unbounded, hence $E \subseteq E'$ and
$\overline{\Omega'} = \mathbb{R}^2 \setminus E' \subseteq \mathbb{R}^2\setminus E = \overline\Omega$.
Since $\rho(\overline\Omega) = \Omega' \cup J' = \overline{\Omega'}$ and $\rho$ is an isometry,
$\lambda(\overline{\Omega'}) = \lambda(\overline{\Omega}) < \infty$. A subset of equal finite
measure has null complement, so $\lambda(\overline\Omega \setminus \overline{\Omega'}) = 0$. The set
$\Omega \cap E'$ is **open** and contained in that null set, hence empty; so
$\Omega \subseteq \mathbb{R}^2\setminus E' = \overline{\Omega'}$, whence
$\overline\Omega \subseteq \overline{\Omega'}$ and therefore $\overline\Omega = \overline{\Omega'}$.
Taking complements, $E = E'$, and taking boundaries, $J = \partial E = \partial E' = J'$ —
contradicting $J \cap J' = \{O\}$ for a curve with more than one point.

**Case B: $J' \setminus \{O\} \subseteq E$.** Applying the same first step to $J$ against $J'$:
$J \setminus \{O\}$ lies in $\Omega'$ or $E'$. If in $\Omega'$, the Case A argument with the roles
exchanged again forces $J = J'$; so $J\setminus\{O\} \subseteq E'$. Then $\Omega' \cap J =
\emptyset$ and $O \notin \Omega'$, so the connected set $\Omega'$ lies in $\Omega$ or in $E$. If
$\Omega' \subseteq \Omega$ then $\overline{\Omega'} \subseteq \overline{\Omega}$, so
$J' \subseteq \overline\Omega$, contradicting $J'\setminus\{O\} \subseteq E$ (nonempty, and
$E \cap \overline\Omega = \emptyset$). Hence $\Omega' \subseteq E$, i.e. $\Omega \cap \Omega' =
\emptyset$. Finally $\overline\Omega \cap \overline{\Omega'} = (\Omega\cap\Omega') \cup
(\Omega \cap J') \cup (J \cap \Omega') \cup (J \cap J') = \emptyset \cup \emptyset \cup \emptyset
\cup \{O\}$. $\square$

**What this is and is not.** The useful contrapositive is:

> **Corollary A′.** If $\overline\Omega \cap \rho(\overline\Omega) \supsetneq \{O\}$ then
> $J \cap \rho(J) \supsetneq \{O\}$, so by Observation R, $O$ is a vertex of an inscribed
> equilateral triangle.

This converts a *curve*-intersection problem into a *region*-overlap problem, which is much easier
to certify. That is the whole payoff of the measure argument, and it is genuinely useful (§5 uses
nothing else). But see §7: it is **only half** of what a general proof needs.

---

## 5. Lemma B — the sector criterion, and why $60°$ is the exact threshold

> **Lemma B.** Suppose there are $\varepsilon > 0$ and a **closed** arc $I \subseteq S^1$ of
> angular length $\ge 60°$ with
> $$S = \{\,O + t v : 0 < t < \varepsilon,\ v \in I\,\} \subseteq \overline{\Omega}.$$
> Then $O$ is a vertex of an equilateral triangle inscribed in $J$, of side $\varepsilon/2$.

**regularity budget: Jordan + the sector hypothesis.** The sector hypothesis *is* the regularity;
it is a local one-sided cone condition on $\overline\Omega$ at $O$ and nothing else about $J$ is
used. Drop it and the conclusion is false (§3).

*Proof.* Rotating a closed arc of length $\ge 60°$ by $60°$ leaves a common direction: if
$I = [\alpha,\beta]$ with $\beta - \alpha \ge 60°$ then $\alpha + 60° \in I \cap \rho(I)$. Pick
$v \in I \cap \rho(I)$ and set $x = O + \tfrac{\varepsilon}{2}v$. Then $x \in S \subseteq
\overline\Omega$, and $x = \rho\!\left(O + \tfrac{\varepsilon}{2}\rho^{-1}v\right) \in \rho(S)
\subseteq \rho(\overline\Omega)$ because $\rho^{-1}v \in I$. So $x \in \overline\Omega \cap
\rho(\overline\Omega)$ and $x \ne O$. Apply Corollary A′ and Observation R; the triangle produced
has side $|Ox| = \varepsilon/2$. $\square$

**$60°$ is exactly the threshold, on both sides.**

- $|I| \ge 60°$ suffices, including equality, and the equality case is the familiar construction:
  at a polygon vertex of interior angle exactly $60°$, one edge rotates onto the other and the two
  points at distance $\varepsilon/2$ along the edges close the triangle. No topology needed.
- $|I| < 60°$ is genuinely insufficient: §3 is a convex curve whose *whole* interior sits inside a
  $30°$ sector at $O$, and there $O$ is exceptional.

**Immediate corollary (`sketch`, budget: polygonal).** Every vertex of a simple polygon with
interior angle $\ge 60°$, and every non-vertex boundary point (interior angle $180°$), is a vertex
of an inscribed equilateral triangle. So a simple polygon's exceptional set is contained in its set
of vertices of interior angle $< 60°$, a finite set. §3 shows the containment can be attained (both $30°$
vertices of $T$ are exceptional) and can also be strict (a reflex polygon may have a $< 60°$ vertex
that is not exceptional).

**Cross-check against the sharp bound.** For a **convex** curve the exterior angles total $2\pi$,
and interior angle $< 60°$ forces exterior angle $> 120°$; at most two such can fit in $360°$. So
the sector criterion predicts *at most two* exceptional points on a convex curve — which is exactly
the sharp bound reported in [`../README.md`](../README.md) row 2, attained by §3's witness (a
triangle has at most two angles below $60°$, since three would sum to under $180°$). I record this
as a consistency check only; the convex case is another lane's and this remark is not a result of
mine. Status `sketch`, and it is not used anywhere below.

---

## 6. Theorem C — the local crosscut criterion, and the gap I found in my own first draft

Lemma B needs a fat sector inside $\overline\Omega$. The question is which curves supply one. Here
is the cleanest hypothesis I can both state and discharge.

### 6.1 The hypothesis and the theorem

> **Hypothesis (C) at $O \in J$.** There are $\varepsilon > 0$, a unit vector $u$, and
> $\eta \in (0,30°)$ such that, writing $D$ for the closed double cone of half-angle $\eta$ about
> the line $O + \mathbb{R}u$:
>
> 1. $J \cap B(O,\varepsilon) \subseteq D$, and
> 2. $J \cap B(O,\varepsilon)$ is a **single crosscut** of $B(O,\varepsilon)$ — one arc, with its
>    two endpoints on $\partial B(O,\varepsilon)$, one in each of the two components of
>    $\partial B(O,\varepsilon) \cap D$.

> **Theorem C.** If Hypothesis (C) holds at $O$, then $O$ is a vertex of an equilateral triangle
> inscribed in $J$, of side exactly $\varepsilon/2$ for the $\varepsilon$ of (C).

**regularity budget: Jordan + Hypothesis (C) at one point.** Hypothesis (C) *is* the regularity, and
it is stated as a hypothesis rather than derived because deriving it is exactly where the argument
gets into trouble (§6.4).

### 6.2 Proof

*Proof.* Let $\alpha = J \cap B(O,\varepsilon)$, a crosscut. By the Jordan curve theorem for the
disc, $B(O,\varepsilon) \setminus \alpha$ has exactly two components $W_+$, $W_-$, each a Jordan
domain. Each is connected and disjoint from $J$, so each lies wholly in $\Omega$ or wholly in $E$.
Since $O \in J = \partial\Omega$, $\Omega$ meets $B(O,\varepsilon)$, and $\Omega \cap
B(O,\varepsilon) \subseteq W_+ \cup W_-$; so at least one of them, say $W_+$, lies in $\Omega$.

The open sector $S_+ = \{O + tv : 0 < t < \varepsilon,\ \angle(v,u) \in (\eta, 180° - \eta)\}$ is
connected and disjoint from $D \supseteq \alpha$, so it lies in $W_+$ or $W_-$; likewise $S_-$ on
the other side. Because $\alpha$'s endpoints lie in the two *different* components of
$\partial B(O,\varepsilon) \cap D$, $\alpha$ separates $S_+$ from $S_-$, so they land in different
components. Hence $W_+ \supseteq S_+$ or $W_+ \supseteq S_-$; either way $\Omega$ contains an open
sector of aperture $180° - 2\eta > 120° > 60°$ and radius $\varepsilon$. Applying Lemma B to any
closed sub-arc of those directions of angular length exactly $60°$, with the same $\varepsilon$,
gives the triangle, of side $\varepsilon/2$. $\square$

### 6.3 What Hypothesis (C) covers

**`sketch`, budget: $C^1$.** At every point of a regular $C^1$ Jordan curve, (C) holds: the curve
is locally a graph over its tangent line with slope $\to 0$, so for small $\varepsilon$ it meets
$B(O,\varepsilon)$ in a single graph arc inside a thin double cone, crossing from one side to the
other. Hence **every** point of a regular $C^1$ Jordan curve is a vertex of an inscribed
equilateral triangle. (Note this is stronger than "some point", and matches the sharp bound's
prediction: a $C^1$ curve has no corners, so no exceptional points.)

**`sketch`, budget: polygonal.** At a non-vertex point of a simple polygon, (C) holds with
$\eta$ arbitrarily small. At a vertex of interior angle $\ge 60°$, (C) fails but Lemma B applies
directly to the wedge. So the exceptional set of a simple polygon is contained in its set of
vertices of interior angle $< 60°$ — finite, and by §3 it can be nonempty.

### 6.4 What Hypothesis (C) does **not** cover — the mistake I made and caught

My first draft of this section asserted:

> ~~**Theorem C′ (false as argued).** $\mathcal{H}^1$-a.e. point of a *rectifiable* Jordan curve is
> a vertex, because the arclength parametrisation is differentiable a.e. and a differentiability
> point satisfies Hypothesis (C).~~

The second half of that sentence is **not something I can prove**, and writing it was precisely the
"smuggled regularity" failure that [`../../RULES.md`](../../RULES.md) §0 predicts. Here is exactly
how far the rectifiable argument does get, and where it stops, because the boundary is the useful
part.

Let $\gamma$ be the arclength parametrisation ($1$-Lipschitz), differentiable at $t_0$ with
$\gamma'(t_0) = u$, $|u| = 1$, and $O = \gamma(t_0)$. Fix $\eta' > 0$ small. Choose $\delta$ with
$$(1-\eta')|s - t_0| \;\le\; |(\gamma(s)-O)\cdot u| \;\le\; |\gamma(s)-O| \;\le\; |s-t_0| \qquad (|s-t_0| < \delta),$$
and $\varepsilon \le (1-\eta')\delta$ small enough that $J \cap B(O,\varepsilon) \subseteq
\gamma((t_0-\delta, t_0+\delta))$. Then, and I did check these:

- **(C1) holds.** $J \cap B(O,\varepsilon) \subseteq D$, the double cone of half-angle
  $\eta = \arcsin\eta'$.
- **A crosscut through $O$ exists, with endpoints on opposite sides.** The forward arc stays in the
  $+u$ half of $D$ (because $(\gamma(s)-O)\cdot u \ge (1-\eta')(s-t_0) > 0$) until it first meets
  $\partial B(O,\varepsilon)$; the backward arc likewise in the $-u$ half. So the two fat sectors
  $S_\pm$ do lie in **different** components of $B(O,\varepsilon) \setminus J$.
- **(C2) does not follow.** Nothing above stops $\gamma$ from leaving $B(O,\varepsilon)$ and
  **re-entering** it, at every scale. The estimates only sandwich $|\gamma(s)-O|$ between
  $(1-\eta')|s-t_0|$ and $|s-t_0|$; that permits $|\gamma(s)-O|$ to be non-monotone in $|s-t_0|$
  with relative oscillation $o(1)$, which is compatible with differentiability at $t_0$. So
  $J \cap B(O,\varepsilon)$ may be a crosscut **plus further strands**, all inside $D$, and
  $B(O,\varepsilon)\setminus J$ may have a third component trapped inside the thin cone.
- **And then the conclusion fails to follow**, because $\Omega$ could be exactly such a trapped
  component: I would then have $\Omega \cap B(O,\varepsilon) \subseteq D$, both $S_\pm$ in $E$, and
  no fat sector. I could not construct such a curve, and I could not exclude it.

So the correct status is: **not established for rectifiable curves.** What is missing is a single
crisp statement —

> *(open, to my knowledge)* Let $\gamma$ be the arclength parametrisation of a rectifiable Jordan
> curve, differentiable at $t_0$ with $|\gamma'(t_0)| = 1$. Must there exist arbitrarily small $r$
> for which $\{s : \gamma(s) \in B(\gamma(t_0), r)\}$ is an interval? Equivalently, must
> $\overline\Omega$ contain a sector of positive aperture at $\gamma(t_0)$?

— and I flag that I do not know its answer. It is plausible that a.e.-differentiability plus a
density argument settles it, and equally plausible that it needs the local structure theory of
rectifiable sets; I did not resolve it and I am not going to assert either way. A reviewer should
treat any sentence of the form "and of course at a point of differentiability the curve is locally a
graph" as the unproved lemma it is: differentiability of the *parametrisation at a point* does not
make the *image* a graph near that point.

**Why I am recording this at length.** It is the only place in this lane where I wrote a fluent
paragraph that was wrong, and I caught it only by re-deriving the separation step rather than
re-reading it. That is the behaviour [`../../RULES.md`](../../RULES.md) §6.2 asks of an examiner,
applied to myself, and the file would have been more impressive and less true without it.

### 6.5 A remark on the mod-2 route I did not take

One is tempted to say: two closed curves in the plane meet in an even number of points, $O$ is one
of them, so there is another. That is a claim about *transverse* intersection and it is exactly the
"obviously the curves must cross" failure named in [`../../RULES.md`](../../RULES.md) §6.2 item 4 —
its hypotheses (transversality, finiteness of the intersection) demand more regularity than
Lemma A + Lemma B do, and buy nothing extra. I state it only so the next agent does not spend an
afternoon on it.

---

## 7. The three framings in the brief, assessed honestly

### 7.1 Area / measure — `refuted` as a standalone route

The argument really does work, but only against one of the two ways two curves can meet at a single
point:

- **Nesting** ($J'$ inside $\Omega$, or $J$ inside $\Omega'$) — **ruled out**, cleanly, by equal
  areas under an isometry (Lemma A, Case A). This half needs no regularity at all.
- **External tangency** ($\Omega \cap \Omega' = \emptyset$, the two closed domains touching only at
  $O$) — **not ruled out, because it happens**. §3 is precisely this configuration: two congruent
  triangles sharing the apex $O$, sitting in disjoint cones. Their areas are equal and there is no
  contradiction to extract.

So an argument that concludes "the domains cannot be nested, therefore they overlap, therefore the
curves cross" is **wrong at the second arrow**, and it is wrong on an explicit witness. I flag this
because it is the shape of argument I would most likely have written fluently and believed. The
measure step survives only as Corollary A′, i.e. as a *reduction*, not as a proof.

### 7.2 Tangent cone / local reachable directions — **works, and is the right hypothesis**

Lemma B is this framing done correctly, but with one substitution that is easy to get wrong:

> The condition is on the tangent cone of **$\overline\Omega$** (which directions at $O$ have a
> whole sector of the *filled region* near them), **not** on the tangent cone of **$J$** (which
> directions are limits of $(x_n - O)/|x_n - O|$ for $x_n \in J$).

They are different and the difference is fatal. A Jordan domain with an outward cusp at $O$ — say
the region $\{0 \le x \le 1,\ |y| \le x^2\}$ closed off on the right — has $+u$ as a limit direction
of $J$ from both sides, so the *curve's* tangent cone at $O$ looks perfectly one-dimensional and
tame, while the *region's* sector aperture at $O$ is $0$ and the rotation route fails there. Any
version of this framing phrased in terms of directions along $J$ rather than sectors inside
$\overline\Omega$ is either false or is silently assuming the curve is locally a graph.

### 7.3 Winding number / degree — **not achieved**

I could not make this give anything Lemma A does not. The natural object is $z \mapsto w_J(z) +
w_{J'}(z)$ for $z \notin J \cup J'$. Under $J \cap J' = \{O\}$, Lemma A already tells us the
supports are disjoint, so this function takes values in $\{0,1\}$ and there is no parity or degree
obstruction to extract: the externally-tangent configuration is perfectly consistent with every
degree count I could write down, as it must be, since §3 realises it. A degree argument that did
produce a contradiction here would be proving something false. Recorded as a dead end, not as an
untried idea.

---

## 8. Varying $O$ — where it actually breaks, and the noncollapse statement

Since a fixed $O$ can fail (§3), the real strategy is: vary $O$ over $J$ and find a good one. Here
is what such an argument needs and where it dies.

**Noncollapse, first, because it is free here and it is not free later.** The route as executed in
§2–§6 takes **no limit and uses no compactness**. The triangle it outputs is
$\{O, \rho^{-1}(q), q\}$ with side $|Oq| > 0$ *given* explicitly, and in Lemma B the side is
$\varepsilon/2$ where $\varepsilon$ is the sector radius. There is no step at which three vertices
could merge. This is the route's single greatest virtue and it is why the equilateral case is
tractable at all: [`../../RULES.md`](../../RULES.md) §2's degenerate solution $O$ is present in
$J \cap \rho(J)$ from the start and is *excluded by hand*, not by an estimate.

**The moment you vary $O$ by a limiting argument, noncollapse becomes the whole problem.** The two
natural continuity arguments and their exact failure:

1. **Continuity in $O$ directly.** Set $G = \{O \in J : J \cap \rho_O(J) \supsetneq \{O\}\}$ and try
   to show $G \ne \emptyset$ by showing $G$ is (say) closed and dense, or open and nonempty, or of
   full measure. The obstruction is concrete: take $O_n \to O$ with witnesses $q_n \in (J \cap
   \rho_{O_n}(J)) \setminus \{O_n\}$. Compactness gives a subsequence $q_n \to q \in J \cap
   \rho_O(J)$ — **but $q$ may equal $O$**, and then the limit carries no information. The map
   $O \mapsto J \cap \rho_O(J)$ is upper semicontinuous in the Hausdorff sense and that is the wrong
   direction: intersections can disappear in the limit, never appear. So $G$ is not obviously closed
   and I have no argument that it is open, dense, or measurable.
2. **Approximation by polygons.** Take polygons $J_n \to J$ (Hausdorff, say), get from §5 a vertex
   $O_n$ of interior angle $\ge 60°$ on each $J_n$ and a triangle of side $s_n$, and pass to the
   limit. Every one of the four obligations of [`../../RULES.md`](../../RULES.md) §4 must be
   discharged, and **the third is the one I cannot discharge**: I have no lower bound on $s_n$. In
   Lemma B, $s_n = \varepsilon_n/2$ where $\varepsilon_n$ is the radius of the fat sector, and
   nothing stops $\varepsilon_n \to 0$ as the approximating polygons roughen. A curve can be
   approximated by polygons all of whose $\ge 60°$ vertices have sector radius $\to 0$.

3. **And the trouble starts earlier than "varying $O$".** §6.4 shows I cannot certify the sector
   even at a *fixed*, apparently well-behaved point — an a.e.-differentiability point of a
   rectifiable curve. So the honest sequence of obstacles is: (a) certify a fat sector at one point
   of a rough curve [§6.4, unresolved]; (b) do it with a radius bounded below along an
   approximating sequence [this section, unresolved]. Only (b) is a noncollapse problem; (a) is a
   purely local-geometric one, and it is strictly easier, so it is the one to attack first.

**The precise open requirement this lane bequeaths.** To push the route to general Jordan curves by
this method, one needs:

> Find $\delta > 0$ and, for each $n$, a point $O_n \in J_n$ at which $\overline{\Omega_n}$ contains
> a sector of aperture $\ge 60°$ **and radius $\ge \delta$**, with $\delta$ independent of $n$.

That is the concrete form of "uniform noncollapse" for this attack, and it is stated *before* the
limit as [`../../RULES.md`](../../RULES.md) §2 demands. I have no such bound and no idea how to get
one; a general Jordan curve need not have a tangent, or a sector of positive aperture, at any point,
and I could not even determine whether "some point of $\overline\Omega$ has sector aperture
$\ge 60°$" is true for every Jordan domain. That question — a purely local-geometric one, with no
rotation in it — is where I would send the next worker, and I flag that I do not know its answer.

**Suspicion register.** The brief warned that a wrong proof would feel most convincing here, and it
was right: my first instinct was "the exceptional set has at most two points, so almost every $O$
works, so pick one" — which is circular, since "at most two" is the theorem. The second was "the
tangent cone must be fat somewhere, by compactness" — which is not a theorem I can state, let alone
prove, and which the outward-cusp example of §7.2 shows is at least not local-triviality. Both are
recorded here so they are not re-derived as insights.

---

## 9. The square contrast — [`../../RULES.md`](../../RULES.md) §3.2, run

**Does the argument transfer to squares? No, and here is exactly where it stops.**

Everything in §2, §4, §5 and §6 goes through verbatim for an arbitrary rotation angle
$\alpha \in (0°, 180°)$, with "$\ge 60°$" replaced by "$\ge \alpha$" in Lemma B. The general
statement I have actually proved is:

> If $\overline{\Omega}$ contains a sector of aperture $\ge \alpha$ at $O$, then there are
> $p, q \in J$ with $|Op| = |Oq| > 0$ and $\angle pOq = \alpha$.

For $\alpha = 60°$ this is the equilateral theorem **only because isosceles-with-apex-$60°$ forces
equilateral** — the third side length is determined by the first two and the angle, and at $60°$ it
equals them. That coincidence is the entire mechanism.

At $\alpha = 90°$ the same machine outputs $p, O, q$ with $|Op| = |Oq|$ and a right angle at $O$:
three vertices of a square, arranged as a corner path. The fourth vertex is *determined* — it is
$p + q - O$ — but **nothing puts it on $J$**, and no rotation about a point of $J$ can be made to
control it, because a single rotation constrains only the pair $(p,q)$. So the output is an
inscribed isosceles right triangle, which is a true, easy, and entirely unremarkable statement, not
an inscribed square. **The argument does not prove the square peg problem**, and if a later version
of it appeared to, [`../../RULES.md`](../../RULES.md) §7 says the version is wrong.

**The heuristic that says the same thing.** Equilateral triangles in the plane form a $4$-parameter
family ($2$ position, $1$ rotation, $1$ scale) and "all three vertices on $J$" is $3$ conditions —
expected solution set of dimension $1$, i.e. solutions come in families and are robust to
perturbation. Squares also form a $4$-parameter family, but "all four vertices on $J$" is
$4$ conditions — expected dimension $0$, so solutions are isolated and only a parity or degree count
can force one, and that count is what degenerates when the curve is rough. Status: `sketch`,
heuristic, deliberately not used anywhere above.

---

## 10. Is this the classical proof? — a literature note, **provenance P3**, not a citation

[`../README.md`](../README.md) owns the known-results table and this section does not add to it. The
lane-specific question is narrower: *is the $60°$ rotation the route Meyerson took?*

What I found: web-search result summaries for Meyerson (1980) describe a proof organised around
**triods** ("Y"-shaped sets) in which, for a point $x$ of a triod $T$, one rotates part of $T$ by
$60°$ about $x$ and reads an inscribed equilateral triangle off an intersection point — i.e.
Observation R — and which proceeds in **three stages: polygonal triods, then "end-straight" triods,
then general triods by approximation and limits.**

If that is accurate, then: (a) the elementary observation of §2 is the classical mechanism, not a
new idea, and this lane is a reconstruction; (b) the polygonal stage is essentially §5 here; and
(c) the general stage is exactly the approximation-and-limit passage that §8 says I cannot make
work — which is consistent with it being the hard part of a nine-page paper rather than something I
was going to find in an afternoon.

**Caveat, and it is a serious one.** Under this session's egress policy every scholarly host was
blocked (`arxiv.org`, `math.brown.edu`, `math.elte.hu`, `matwbn.icm.edu.pl`, `eudml.org`,
`doi.org`, `zbmath.org`, `ams.org`, …), exactly as recorded in
[`../README.md`](../README.md)'s provenance warning. **I read no source text.** The above is a
paraphrase of search-result summaries, which are themselves machine-generated. Per
[`../../RULES.md`](../../RULES.md) §6.1 that is not a citation: it is a **search target, flagged
unverified**. It is recorded at provenance **P3** and must not be entered in the known-results
table, promoted, or built on. A reviewer with network access should confirm it against Meyerson
(1980) directly; it is a cheap addition to that file's verification-debt list, item 1.

---

## 11. Reproducing the computation

Exact throughout, in $\mathbb{Q}(\sqrt3)$; no floating point anywhere, per
[`../../RULES.md`](../../RULES.md) §5. Requires `sympy` (checked with 1.14.0, Python 3.11). This
lane owns no `experiments/` directory, so the script is inline rather than committed elsewhere;
save it and run `python3 rot.py`.

```python
import sympy as sp
s3 = sp.sqrt(3)

def rot(P, deg, Ctr):                       # rotate P by deg about Ctr, exactly
    t = sp.rad(deg); c, s = sp.cos(t), sp.sin(t)
    x, y = P[0] - Ctr[0], P[1] - Ctr[1]
    return (sp.simplify(c*x - s*y + Ctr[0]), sp.simplify(s*x + c*y + Ctr[1]))

d = lambda P, Q: sp.simplify(sp.sqrt((P[0]-Q[0])**2 + (P[1]-Q[1])**2))

# (a) Observation R, symbolically: the triangle is equilateral for every r, theta.
r, th = sp.symbols('r theta', positive=True)
O0 = (sp.Integer(0), sp.Integer(0))
p = (r*sp.cos(th), r*sp.sin(th)); q = rot(p, 60, O0)
print("(a)", sp.simplify(d(O0,p)), sp.simplify(d(O0,q)), sp.trigsimp(d(p,q)))   # r r r

# (b) the 30-30-120 witness, and the rotation test at each of its three vertices.
O = (sp.Integer(0), sp.Integer(0))
A = (sp.Integer(1), sp.Integer(0))
C = (sp.Rational(1,2), s3/6)
T = [(O,A), (A,C), (C,O)]
for name, V in [("O (30 deg)", O), ("A (30 deg)", A), ("C (120 deg)", C)]:
    for ang in (60, -60):
        Tr = [(rot(P,ang,V), rot(Q,ang,V)) for (P,Q) in T]
        hits = set()
        for (P,Q) in T:
            for (R,S) in Tr:
                for o in sp.Segment2D(sp.Point2D(*P), sp.Point2D(*Q)).intersection(
                         sp.Segment2D(sp.Point2D(*R), sp.Point2D(*S))):
                    hits.add((sp.simplify(o.x), sp.simplify(o.y)) if isinstance(o, sp.Point2D)
                             else ('SEGMENT', str(o)))
        print(name, ang, sorted(hits, key=str))
        for h in hits:                                   # read off the triangles
            if isinstance(h[0], str) or sp.simplify(h[0]-V[0]) == sp.simplify(h[1]-V[1]) == 0:
                continue
            pp = rot(h, -ang, V)
            print("   triangle", V, tuple(sp.simplify(z) for z in pp), h,
                  "sides", d(V,pp), d(V,h), d(pp,h))
```

Expected output: `(a) r r r`; `{(0,0)}` at both $30°$ vertices for both rotation senses (with the
corresponding singleton `{(1,0)}` at $A$); and at $C$ a four-point intersection set yielding the
three inscribed equilateral triangles quoted in §3.

**Validation gate run** ([`../../RULES.md`](../../RULES.md) §5): the script reproduces the §3.1
wedge-test witness (both $30°$ apexes exceptional) and finds genuine inscribed triangles at the
$120°$ vertex whose three side lengths are exactly equal in $\mathbb{Q}(\sqrt3)$. It is **not** the
problem's shared enumerator under `experiments/inscribed-triangle-polygons/` (another lane's file);
a cross-check of these exact intersection sets against that enumerator is the obvious next
verification step and has **not** been done here.
