# Polygon count closure: the metric argument has a replacement, and it is still not enough

```
regularity budget: NONE (J used as a bare point set, plus continuity of two named
      radial branches) for Lemma 1 and Theorem A - the lane's new tool;
      polygonal for Lemma 2, Theorem 1, Corollaries A1 and A2, Proposition S and all numerics;
      Jordan for Lemma 3 and Lemma 4 (Jordan curve theorem twice, plus Lebesgue measure).
      Every statement carries its own budget line in situ.
      What breaks first if "polygonal" is dropped from Corollary A2: the radial function
      f = |.-O| on a general Jordan curve need not have finitely many critical values, need
      not have isolated local maxima, and the components of {f > r} need not shrink to points,
      so "leaf component" is undefined and the trapping argument has nothing to trap.
      What breaks first if "Jordan" is dropped from Lemma 3: its proof uses the Jordan curve
      theorem three times (two complementary components; the boundary of each is J; the
      unbounded component is unique), and a planar continuum supplies none of that.
      Theorem A consumes NO regularity at all: it is a statement about an arbitrary subset of
      the plane and two continuous curves in it, which is exactly why it survives where the
      wedge and the diameter arguments do not.
```

- Lane: **prove `|E(P)| <= 2` for every simple polygon, or localise the failure exactly.**
- Author: `claude` (Claude Opus 5), 2026-08-30, branch `claude/inscribe-equilateral-triangle-oj15x1`.
  Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md). **It was written by an earlier
  worker in this lane, before any computation, and that worker was killed mid-task.** I did not
  edit it and did not need to deviate from it; §12 scores every one of its criteria K1-K8 and its
  predictions P1-P4 against what actually happened, and says plainly which of them were *its*
  pre-registration rather than mine.
- Journal: [`../../../../notebook/claude/2026-08-30-iet-count-prove.md`](../../../../notebook/claude/2026-08-30-iet-count-prove.md).
- Read before starting, **edited by this lane: none of them** —
  [`../exceptional-set-polygons/`](../exceptional-set-polygons/README.md),
  [`../exceptional-pair-rigidity/`](../exceptional-pair-rigidity/README.md),
  [`../half-density-obstruction/`](../half-density-obstruction/README.md), plus
  [`../../README.md`](../../README.md), [`../../RULES.md`](../../RULES.md), repo `RULES.md`
  §0, §3, §7. The committed deciders under `../../../../experiments/` were **read and run,
  never modified**.
- A concurrent lane, [`../three-exceptional-hunt/`](../three-exceptional-hunt/), is attempting
  the **opposite** of this one: to construct a simple polygon with three exceptional vertices.
  **I did not read its files and did not coordinate with it.** If it produces a witness and this
  file's §9.4 numerics stand, exactly one of the two lanes is wrong, and that is the point.

---

## 0. Verdict, up front

| § | Statement | Status |
|---|---|---|
| §2 | **Lemma 1 (criterion).** For `S ⊆ R²`, `O ∈ S`: `O` is a vertex of a nondegenerate equilateral triangle in `S` **iff** some `p,q ∈ S` have `\|Op\| = \|Oq\| = \|pq\| > 0` | `sketch` — mine, re-derived; budget **none** |
| §3 | **Lemma 2 (local structure).** At every boundary point of a simple polygon the interior contains an open sector of aperture the interior angle | `sketch` — mine, re-derived |
| §4 | **Lemma 3 (region lemma)** `J ∩ ρ(J) = {O} ⟹ Ω̄ ∩ ρ(Ω̄) = {O}`, and **Lemma 4 (sector criterion)** | `sketch` — mine, re-derived from scratch |
| §5 | **Theorem 1 (reduction).** `E(P) ⊆ { vertices of interior angle < 60° }` | `sketch` — mine, re-derived |
| §6 | **Theorem 2 (wedge count).** At most two wedge-type points on any set | `sketch` — mine, re-derived; budget **none** |
| §7 | **Theorem A (branch trapping) — the lane's new tool.** Two continuous radial branches about an exceptional point that *merge* at one end of their common interval satisfy `\|p(r) − q(r)\| < r` for the **whole** interval. One line, no lifts, no angles, no topology | `sketch` — mine; budget **none** |
| §7.3 | **Corollary A1 (channel).** Below the first local-minimum radius the two points of `J` at radius `r` satisfy `\|pq\| < r` | `sketch` — mine |
| §7.4 | **Corollary A2 (leaf trapping).** Every *leaf* component of `{f > r}` and every *single-minimum* component of `{f < r}` has its two endpoints at distance `< r` | `sketch` — mine |
| §7.6 | **Proposition S (a topology-free fragment).** If `f = \|·−O\|` is unimodal on `J∖{O}` and the interior angle at `O` is `≥ 60°`, then `O` is good — **no Jordan curve theorem, no measure, no region lemma** | `sketch` — mine |
| §8 | **The small-triangle family at a sharp vertex,** explicitly: at a vertex whose two edges meet at unsigned angle `γ ≤ 60°` there are arbitrarily small inscribed equilateral triangles with two vertices on one edge and one on the other, with `d² = (4 − s²)/3`, `s = 2cos γ`. Exact `Q(√3)` witness inside the `30`-`30`-`120` triangle | `sketch` + `numerical` (exact) |
| §9.1 | **The joint constraint is essentially empty.** The *only* mutual condition three exceptional points impose on one another through the criterion is that they do not form an equilateral triangle | `sketch` — mine; this is the sharpest statement of where the count dies |
| §9.4 | **The new tools provably cannot close the count.** An explicit **5-vertex integer pentagon** has **three** vertices satisfying *every* necessary condition proved here, and `\|E\| = 1` | `numerical` (exact, two independent deciders) |
| §9 | **`\|E(P)\| ≤ 2` for simple polygons** | **not closed.** §9 says exactly where and why |
| §10.3 | Census: `850` simple polygons decided exactly; max `\|E\|` observed **2**, never `3` | `numerical` |

**One-sentence summary.** The metric argument that settles the convex case (a blocked point is a
diameter endpoint) does have a replacement — **Theorem A**, which traps *pairs of radial branches*
rather than pairs of points and needs no regularity whatsoever — and that replacement is strictly
stronger than the necessary condition the wedge picture yields (`γ(O) < 60°`, which is only its
`r → 0` shadow), explains the spiral tip, the tuning fork and the mixed pair in one mechanism, and
reproves the local part of the convex criterion with no topology at all; but it is
**still a condition on one point at a time**, and an exact five-vertex integer pentagon shows three
vertices of one polygon can satisfy every consequence of it simultaneously. **I did not close
`|E(P)| ≤ 2` and I can now say precisely why no argument of this shape will.**

**Nothing here is assumable** (repo [`RULES.md`](../../../../RULES.md) §3), including by me.
Nothing is `verified:review`; no agent outside the Claude family has examined any of it.

**Dependency hygiene.** Everything below rests on: elementary Euclidean plane geometry (law of
cosines, angle sum, "larger angle opposite longer side"), the intermediate value theorem, the
Jordan curve theorem *for polygons* where declared, and isometry-invariance of Lebesgue measure.
Every lemma this lane needs from another lane has been **re-derived here from the definitions**
before use, because `RULES.md` §3 forbids resting on a `sketch` — including my own. The statements
in this file do rest on *each other*, as any proof rests on its own lemmas; that internal chain is
what makes the whole file exactly one `sketch`, capped at its weakest link, and it is the reason
nothing here may be imported by a later lane without being re-derived there. Where I land
in the same place as another lane I say so as a *cross-check*, which confers nothing.
**Meyerson's bound is not an input anywhere.** It appears once, in §10.3, as an after-the-fact
consistency check on output; [`../../README.md`](../../README.md) marks it `cited`\* (provisional,
provenance P2, no source text read anywhere in this project), which is a second reason it may not
be one.

---

## 1. Setting and notation

`P ⊂ R²` is a **simple polygon**: the compact region bounded by a simple closed polygonal curve
`J = ∂P` with finitely many straight edges. `Ω` is the bounded component of `R² ∖ J`, `E` the
unbounded one, `Ω̄ = Ω ∪ J = R² ∖ E`. For `O ∈ J`, `ρ = ρ_{O,60°}` is rotation by `+60°` about `O`.

`O ∈ J` is **good** if some nondegenerate equilateral triangle has all three vertices on `J` and
one of them equal to `O`; **exceptional** otherwise. `E(J)` is the exceptional set.

Fix a parametrisation `γ : [0,1] → R²` of `J` with `γ(0) = γ(1) = O`, injective on `[0,1)`, and put

```
f(t) = |γ(t) − O|,        R = max f,        Θ(r) = { θ : O + r e^{iθ} ∈ J }.
```

`O` is **wedge-type** when all of `J` lies in a closed convex cone of opening `< 60°` with apex `O`.
`γ(O)` denotes the interior angle at `O`.

**Nondegeneracy** ([`../../RULES.md`](../../RULES.md) §2). "Equilateral triangle" always means
three *pairwise distinct* points at equal pairwise distances, equivalently side length `> 0`. Every
existence statement below exhibits a strictly positive side. **There is no limiting argument
anywhere in §7**, which is the section carrying the new content: Theorem A produces its triangle
from an intermediate value theorem applied to a scalar function of a scalar radius, and the side
length it returns is the radius `r > 0` itself. So the classical trap — a limit of nondegenerate
triangles assumed nondegenerate — has nowhere to hide here, and I want that on the record rather
than assumed.

---

## 2. Lemma 1 — the criterion, in metric form

> **Lemma 1.** Let `S ⊆ R²` and `O ∈ S`. Then `O` is a vertex of a nondegenerate equilateral
> triangle with all three vertices in `S` **iff** there are `p, q ∈ S` with
> ```
> |Op| = |Oq| = |pq| > 0.
> ```
> Equivalently: iff for some `r > 0` two elements of `Θ(r)` differ by exactly `60° (mod 360°)`.

**regularity budget: none.** `S` is a bare point set — not closed, not connected, not a curve.
Nothing topological can leak into any use of it.

*Proof.* (⇐) `O, p, q` are three points at equal pairwise distances `r > 0`; distinctness is forced
by `r > 0` and `|pq| = r > 0`. That is a nondegenerate equilateral triangle of side `r`.
(⇒) If `O, p, q` are equilateral of side `s > 0` then `|Op| = |Oq| = |pq| = s > 0` by definition.
For the angular restatement: `|Op| = |Oq| = r` and the law of cosines give
`|pq|² = 2r²(1 − cos ∠pOq)`, so `|pq| = r ⟺ cos ∠pOq = 1/2 ⟺ ∠pOq = 60°`. ∎

**Why I state it metrically rather than angularly, and it matters twice.** First, the metric form
`|pq|² = r²` is a **rational** identity on a rational polygon — no `√3`, no angle, no continuous
lift of an argument — which is what makes §7's instrument decide by exact rational sign tests
(§10.1). Second, the angular form invites comparing *lifted* angles across radii, and every lift is
a place to make an error that no fixture will catch. §7 uses no lift at all.

**Cross-check, not a dependency.** This is the same three lines as `rotation-continuity` §2,
`convex-vertex-criterion` §1, `spiral-tip-witness` §2, `half-density` §2, `rectifiable-case` §2,
`exceptional-set-polygons` §2 and `exceptional-pair-rigidity` §2. Eight independent derivations of
one fact now exist in this directory; that is decorrelation evidence and nothing more — all are
`sketch`, and a `sketch` may not rest on a `sketch`.

---

## 3. Lemma 2 — what a polygon looks like at a boundary point

> **Lemma 2.** Let `O ∈ J`. For all small `ε > 0`, `J ∩ B(O,ε)` is a diameter of `B(O,ε)` (`O` not
> a vertex) or a pair of radii (`O` a vertex), and `B(O,ε) ∖ J` has exactly two components, open
> circular sectors of apertures `γ` and `360° − γ`. Exactly one lies in `Ω`; its aperture is the
> interior angle `γ(O)`, and `γ(O) = 180°` at a non-vertex point.

**regularity budget: polygonal + the Jordan curve theorem for polygons.**

*Proof.* `J` is a finite union of closed segments; take `ε` below the distance from `O` to every
edge and vertex not containing `O`. Then `J ∩ B(O,ε)` is exactly the part of the one or two edges
through `O` inside the ball, and `B(O,ε) ∖ J` is two open sectors `S₁, S₂` of apertures summing to
`360°`. Each `Sᵢ` is connected and misses `J`, so lies wholly in `Ω` or wholly in `E`. Since
`O ∈ J = ∂Ω = ∂E`, the ball meets both, and `B(O,ε) ∩ (Ω ∪ E) = S₁ ∪ S₂`; so one sector is in `Ω`
and the other in `E`. ∎

This is the only place "polygon" is used in §§4-6, and it is worth naming what it supplies that a
general Jordan curve does not: **a sector of positive aperture inside `Ω̄` at every boundary point**.

---

## 4. Lemma 3 (region lemma) and Lemma 4 (sector criterion), re-derived

> **Lemma 3.** `J` a Jordan curve, `O ∈ J`, `ρ` a rotation about `O` by an angle that is not a
> multiple of `360°`. If `J ∩ ρ(J) = {O}` then `Ω̄ ∩ ρ(Ω̄) = {O}`.

**regularity budget: Jordan.** Jordan curve theorem (two components, `∂Ω = ∂E = J`, the unbounded
component is unique) plus isometry-invariance of Lebesgue measure. No rectifiability, no tangent.

*Proof.* `ρ` is a homeomorphism of the plane, so `ρ(J), ρ(Ω), ρ(E)` are the curve, bounded and
unbounded components of the rotated configuration and `ρ(Ω̄) = R² ∖ ρ(E)`.

**Step 0.** *If `ρ(Ω̄) ⊆ Ω̄` then `J = ρ(J)`.* `λ(ρΩ̄) = λ(Ω̄) < ∞`, so `λ(Ω̄ ∖ ρΩ̄) = 0`; the set
`Ω ∖ ρ(Ω̄)` is open and contained in that null set, hence empty, so `Ω ⊆ ρ(Ω̄)` and, `ρ(Ω̄)` being
closed, `Ω̄ ⊆ ρ(Ω̄)`, i.e. `Ω̄ = ρ(Ω̄)`. Boundaries: `J = ∂Ω̄ = ∂ρ(Ω̄) = ρ(J)`.

**Step 1.** *If `ρ(J) ⊆ Ω̄` then `J = ρ(J)`.* `E` is connected, unbounded, disjoint from `ρ(J)`, so
lies in the unbounded component `ρ(E)` of `R² ∖ ρ(J)`; hence `ρ(Ω̄) = R² ∖ ρ(E) ⊆ R² ∖ E = Ω̄`, and
Step 0 applies.

Now assume `J ∩ ρ(J) = {O}`. `J` has more than one point, so `J ≠ ρ(J)` and Steps 0-1 are
contradiction generators.

**Step 2.** `ρ(J) ∖ {O}` is connected (a circle minus a point) and misses `J`, so lies in `Ω` or in
`E`. In `Ω` it would give `ρ(J) ⊆ Ω̄` and Step 1 a contradiction. **So `ρ(J) ∩ Ω = ∅`.**

**Step 3.** Symmetrically `J ∖ {O}` lies in `ρ(Ω)` or `ρ(E)`; the first contradicts Step 1 with the
roles exchanged. **So `J ∩ ρ(Ω) = ∅`** (and `O ∈ ρ(J)`, so `O ∉ ρ(Ω)`).

**Step 4.** `ρ(Ω)` is connected and, by Step 3, misses `J`, so lies in `Ω` or `E`; in `Ω` it gives
`ρ(Ω̄) ⊆ Ω̄` and Step 0 a contradiction. **So `Ω ∩ ρ(Ω) = ∅`.**

**Step 5.** `Ω̄ ∩ ρΩ̄ = (Ω∩ρΩ) ∪ (Ω∩ρJ) ∪ (J∩ρΩ) ∪ (J∩ρJ) = ∅ ∪ ∅ ∪ ∅ ∪ {O}`. ∎

> **Lemma 4 (sector criterion).** If for some `ε > 0` and some `a` the **closed** sector
> `S = { O + t e^{iθ} : 0 ≤ t ≤ ε, θ ∈ [a, a+60°] }` lies in `Ω̄`, then `O` is good.

*Proof.* `x = O + (ε/2)e^{i(a+60°)} ∈ S ⊆ Ω̄` and `ρ^{-1}(x) = O + (ε/2)e^{ia} ∈ S ⊆ Ω̄`, so
`x ∈ ρ(Ω̄)` and `x ≠ O`. Thus `Ω̄ ∩ ρ(Ω̄) ⊋ {O}`, so by Lemma 3 (contrapositive)
`J ∩ ρ(J) ⊋ {O}`; take `q` there with `q ≠ O`, put `p = ρ^{-1}(q) ∈ J`, and apply Lemma 1 with
`r = |Oq| > 0` (note `|Op| = |Oq| = r` and `∠pOq = 60°`, so `|pq| = r`). ∎

**A quantitative warning I am not falling for.** Lemma 4 gives *some* triangle with **no control on
its side**: `q` comes from a non-constructive contrapositive and is not `x`. `rotation-continuity`
§5 once claimed side `ε/2` here and `rectifiable-case` §7 refuted it with the unit square. I state
Lemma 4 with no side clause, and nothing below wants one.

---

## 5. Theorem 1 — the reduction

> **Theorem 1.** For a simple polygon `P` with `J = ∂P`, every `O ∈ J` with interior angle
> `γ(O) ≥ 60°` is good. Hence `E(P) ⊆ { vertices of P of interior angle < 60° }`, a finite set; in
> particular **no non-vertex boundary point of a simple polygon is exceptional.**

**regularity budget: polygonal + Jordan** (through Lemmas 2 and 3).

*Proof.* By Lemma 2 there is an open sector `U ⊆ Ω` at `O` of aperture `γ(O)` and radius `ε`; its
closure contains the closed sector of the same aperture and radius `ε/2`, which therefore lies in
`Ω̄`. If `γ(O) ≥ 60°` that closed sector contains one of aperture exactly `60°`, and Lemma 4
applies. A non-vertex point has `γ = 180°`, a reflex vertex `γ > 180°`. A polygon has finitely many
vertices. ∎

Cross-check: this is `exceptional-set-polygons` Theorem 1, reached independently. Numerically it
survived every test I ran (§10.2), and a `60°` vertex is good by a direct construction with no
topology in it — the two points at a common distance `t` along the two edges are on `J`, at equal
radius, `60°` apart.

---

## 6. Theorem 2 — at most two wedge-type points

> **Theorem 2.** Any set with at least two points has at most **two** wedge-type points. Since
> wedge-type ⟹ exceptional, at most two exceptional points are wedge-type.

**regularity budget: none.**

*Proof.* Suppose `O₁,O₂,O₃` are distinct and wedge-type with cone openings `wᵢ < 60°`. Two points
of `J ∖ {Oᵢ}` subtend at `Oᵢ` an angle at most `wᵢ`, both lying in the cone. They are not
collinear: in a collinear arrangement the middle point subtends `180° > 60°`. So they form a
nondegenerate triangle whose angle at `Oᵢ` is `≤ wᵢ < 60°`; the three angles sum to `180°` while
each is `< 60°`. Contradiction. ∎

**Sharpness.** The `30`-`30`-`120` triangle has exactly two wedge-type points, its `30°` apexes,
and they are its only exceptional points — verified exactly in §10.1.

**This is the whole of the convex count that transfers for free, and §7 is about the rest.** The
argument consumes exactly one thing: at `Oᵢ`, *the other two exceptional points* subtend `< 60°`.
A wedge-type point gives that free because all of `J` is in the cone. §9.1 shows nothing else does.

---

## 7. Theorem A — branch trapping, the replacement for the metric argument

This is the lane's new tool. It is one line, it needs no regularity at all, and it is what the
brief asked for: a mechanism that constrains an exceptional point *across* radii instead of
circle-by-circle.

### 7.1 The statement

> **Theorem A (branch trapping).** Let `S ⊆ R²`, let `O ∈ S` be **exceptional** for `S` (no
> nondegenerate equilateral triangle in `S` has a vertex at `O`), let `I ⊆ (0,∞)` be an interval,
> and let `p, q : I → S` be continuous with
> ```
> |p(r) − O| = |q(r) − O| = r   and   p(r) ≠ q(r)      for every r ∈ I.
> ```
> Suppose that at one endpoint `c` of `I` (with `c` finite, `c > 0`, `c ∉ I` allowed) the two
> branches **merge**: `|p(r) − q(r)| → 0` as `r → c`. Then
> ```
> |p(r) − q(r)| < r        for every r ∈ I.
> ```
> Equivalently, `∠ p(r) O q(r) < 60°` throughout.

**regularity budget: none.** `S` is a bare point set. The only hypotheses are the continuity of the
two named branches and the merge at one end — no Jordan curve theorem, no measure, no convexity,
no rectifiability, no tangent, and *no continuous lift of any argument anywhere*.

*Proof.* Put `h(r) = |p(r) − q(r)|² − r²`, continuous on `I`. By Lemma 1, `h(r) = 0` for some
`r ∈ I` would give `p(r), q(r) ∈ S` with `|Op| = |Oq| = |pq| = r > 0` — an inscribed equilateral
triangle with a vertex at `O`, contradicting exceptionality. So `h` never vanishes on the interval
`I`, hence has constant sign. As `r → c`, `|p − q|² → 0` and `r² → c² > 0`, so `h → −c² < 0`.
Therefore `h < 0` on all of `I`. ∎

**Where the nondegeneracy is paid, since [`../../RULES.md`](../../RULES.md) §2 asks.** In `r > 0`
and `p(r) ≠ q(r)`: those two hypotheses are exactly what makes the triangle produced by `h(r) = 0`
nondegenerate, and both are hypotheses of the theorem rather than conclusions of a limit. The merge
hypothesis is used only to fix the *sign* at one end; the theorem never takes a limit of triangles.

**Variant A′ (the other sign at the origin).** If instead `0` is an endpoint of `I` and
`|p(r) − q(r)| / r → κ` as `r → 0⁺` with `κ ≠ 1`, the same one line gives `|p − q| < r` throughout
when `κ < 1`, and `|p − q| > r` throughout when `κ > 1`. This is the form Corollary A1 uses.

### 7.2 Why this is the replacement the brief asked for, and what it replaces

The convex count works because a blocked point *sees the whole curve in a `60°` cone*, so the other
two exceptional points are constrained directly (Theorem 2). The brief is right that this provably
does not extend: the criterion (Lemma 1) compares points **on one circle at a time**, and two other
exceptional points sit on two *different* circles about the first.

Theorem A is the only escape I found from "one circle at a time", and it escapes by a different
door: it does not compare different circles, it **propagates one comparison along a continuous
family of circles**. That is why it needs no regularity — the propagation is the intermediate value
theorem on a scalar function of `r`, and the "merge" endpoint supplies the sign for free.

What it subsumes:

- **`exceptional-set-polygons` Proposition 5 ("no sweep")** is Theorem A with the sign left open:
  that statement says two continuous branches may not sweep across `±60°`; Theorem A adds *which
  side they are trapped on* whenever the branches merge at one end, which is the part that has
  content. Every branch pair produced by a polygon merges at one end (§7.4), so the addition is not
  a special case — it is the generic one.
- **The necessary condition the wedge picture yields**, namely `γ(O) < 60°` (Theorem 1): that is
  the `r → 0` shadow of Corollary A1, which says the same thing at *every* radius below the first
  pinch. (The wedge test itself is a *sufficient* condition for exceptionality and is a different
  kind of statement; Theorem A neither implies nor is implied by it, and I am not claiming it is.)
- **The local half of the convex tangent-cone criterion**, with no topology: Proposition S (§7.6).

What it does **not** subsume: the half-density obstruction, which is a statement about area rather
than about branches, and which §9.3 confirms is structurally incapable of reaching three points.

### 7.3 Corollary A1 — the channel lemma

Let `O` be a vertex of a simple polygon `P`, and let

```
r₁(O) = min { f(t) : t is a local minimum of f = |γ(·) − O| on J ∖ {O} },
```

with `r₁(O) = R` if `f` has no interior local minimum. For `0 < r < r₁(O)` the set `{f < r}` has a
single component (every component contains a local minimum, and the only one below `r₁` is `O`),
hence so does `{f > r}`, hence `J` meets the circle of radius `r` about `O` in **exactly two**
points `p(r), q(r)`, both depending continuously on `r`.

> **Corollary A1 (channel).** Let `O` be exceptional. If `γ(O) < 60°` then
> `|p(r) − q(r)| < r`, i.e. `∠p(r) O q(r) < 60°`, for **every** `r ∈ (0, r₁(O))`; and if
> `γ(O) > 60°` then `|p(r) − q(r)| > r` throughout. By Theorem 1 only the first case occurs.

**regularity budget: polygonal.** The final sentence — and only that sentence — consumes Theorem 1,
hence Lemmas 2-4, hence the Jordan curve theorem for polygons; the two-case statement above it does
not, and holds for any `O` with two well-defined edge directions.

*Proof.* Theorem A, variant A′, on `I = (0, r₁(O))`. For small `r` the two points are on the two
edges at `O`, at distance `r` along each, so `|p − q|² = 2r²(1 − cos γ(O))` and
`|p−q|/r → 2 sin(γ(O)/2) = κ`. Then `κ < 1 ⟺ sin(γ(O)/2) < 1/2 ⟺ γ(O) < 60°`, and `κ > 1 ⟺
γ(O) > 60°`; variant A′ gives the corresponding sign for the whole interval. ∎

**Read it as a picture.** Near an exceptional point the curve is a **channel**: at *every* radius up
to the first pinch, the two walls are less than `60°` apart. That is exactly the mechanism of the
spiral tip of [`../spiral-tip-witness/`](../spiral-tip-witness/README.md) and of the 17-gon of
[`../exceptional-set-polygons/`](../exceptional-set-polygons/README.md) §7, now derived rather than
observed, and it is strictly stronger than `γ(O) < 60°`, which is only its `r → 0` shadow.

### 7.4 Corollary A2 — leaf trapping, the global form

For non-critical `r`, write `f^{-1}(r) = {t₁ < … < t_{2k}}` in the boundary order started at `O`.
The components of `{f > r}` are `(t₁,t₂), (t₃,t₄), …`; those of `{f < r}` are `(t₂,t₃), …` together
with the one through `O`. Call a component of `{f>r}` a **leaf** when it contains exactly one
critical point of `f` (necessarily a local maximum), and call a component of `{f<r}` **that does
not contain `O`** a **single-minimum** component when it contains exactly one critical point (a
local minimum, necessarily at a level `> 0`).

> **Corollary A2 (leaf trapping).** Let `O` be exceptional for a simple polygon. Then at every
> non-critical radius `r`, **every** leaf component of `{f > r}` and **every** single-minimum
> component of `{f < r}` has its two endpoints `p, q` at distance `|pq| < r`.

**The component of `{f < r}` through `O` is excluded, and the exclusion is load-bearing.** Its two
endpoints merge at `O` itself, where `c = 0` and Theorem A's hypothesis `c > 0` fails — indeed
`|p−q|/r → 2sin(γ(O)/2) ≠ 0` there, so nothing merges in the required sense. That pair is exactly
what Corollary A1 handles instead, by variant A′. Stating A2 without the exclusion would be false
in general and is the one place I nearly overreached.

**regularity budget: polygonal.** Used for: `f` restricted to an edge is a strictly convex quadratic
(so an edge carries no interior local maximum and at most one interior local minimum, its
perpendicular foot); hence `f` has finitely many critical values, all local extrema are isolated,
and a leaf component genuinely shrinks to a point as `r` rises to its maximum.

*Proof.* Take a leaf component `C`, with maximum value `c` attained at the unique critical point
inside. Let `I = (m, c)` be the maximal interval of radii on which the component tracking `C`
remains a leaf: as `r` decreases from `c` the component grows, and it stops being a leaf exactly
when it absorbs a second critical point, i.e. at the level `m` of the local minimum where it merges
with a neighbouring component (`m = 0` if that never happens). On `I` the two endpoints are
continuous functions `p(r), q(r)` of `r` with `p(r) ≠ q(r)`, and as `r → c⁻` both converge to the
maximum point, so `|p − q| → 0`. Theorem A applies with the endpoint `c > 0`. The single-minimum
case is identical with `r` increasing and decreasing exchanged: the two endpoints merge as `r`
decreases to the local minimum's level, which is `> 0` because that component avoids `O` and `O` is
the only point of `J` at distance `0`. ∎

**Both halves are needed and neither implies the other.** §10.2 measures this: on the tuning fork
the leaf condition is violated at both tips (which is *why* they are good) while the channel
condition holds; on the 8-gon `C3` of `exceptional-pair-rigidity` §7.3 the channel condition is
violated at vertex 5 while the leaf condition holds. The two corollaries of one theorem are
**incomparable as tests**.

### 7.5 What Theorem A explains that the wedge does not

Run against the three witnesses [`KILL-CRITERION.md`](./KILL-CRITERION.md) K5 demands, all decided
exactly and by two independent deciders (§10.1):

| witness | exceptional points | wedge-type? | channel A1 | leaf A2 |
|---|---|---|---|---|
| `30`-`30`-`120` triangle | both `30°` apexes | **yes** | holds | holds |
| 17-gon spiral channel (`exceptional-set-polygons` §7) | the tip `O = (0,0)` | **no** (directions span `258°`) | holds | holds |
| pentagon `C2` (`exceptional-pair-rigidity` §7.3) | `(−5,−14)` non-wedge, `(18,0)` wedge | **mixed** | holds at both | holds at both |
| 8-gon `C3` | `(−1,−19)`, `(−20,0)` | — | holds at both | holds at both |
| tuning fork (`exceptional-set-polygons` §9) | none — both tips **good** | — | holds at both | **fails at both** |

The last row is the point. The tuning fork is the standard example of "several sharp tips cannot
all be exceptional", and the channel lemma does **not** see it — the tips' channels stop at the
notch. Corollary A2 does see it, at a radius reaching past the notch to the far prong. So the two
halves of Theorem A together cover every mechanism this directory has recorded, wedge and non-wedge
alike, which is more than any single previous criterion here does.

### 7.6 Proposition S — a topology-free fragment, and the best Lean target this lane found

> **Proposition S.** Let `P` be a simple polygon and `O ∈ ∂P` a point such that `f = |γ(·) − O|` is
> **unimodal** on `J ∖ {O}` (one local maximum, no interior local minimum). If the two edges at `O`
> meet at unsigned angle `≥ 60°`, then `O` is good.

**regularity budget: polygonal — and *no topology at all*.** No Jordan curve theorem, no Lemma 3,
no Lemma 4, no measure. This is the whole reason to state it separately.

*Proof.* Unimodality makes `J` meet each circle of radius `r ∈ (0,R)` in exactly two points
`p(r), q(r)`, continuous in `r`, with `|p − q| → 0` as `r → R⁻`. Put `h(r) = |p−q|² − r²`. As
`r → 0⁺`, `h(r)/r² → 2(1 − cos γ) − 1 = 1 − 2cos γ ≥ 0` since `γ ≥ 60°`; if `γ = 60°` exactly then
`h ≡ 0` for small `r` and `O` is good outright, so assume `γ > 60°` and `h > 0` near `0`. As
`r → R⁻`, `h → −R² < 0`. By the intermediate value theorem `h` vanishes somewhere, and Lemma 1
converts that zero into a nondegenerate inscribed equilateral triangle of side `r > 0` at `O`. ∎

This is the local half of the convex criterion (`convex-vertex-criterion` Theorem B(i),
`exceptional-pair-rigidity` §5.3) proved without the Jordan curve theorem and without convexity —
unimodality of the radial function is what those lanes were really using, and it is available at
every boundary point of a convex body but at some points of non-convex ones too.

**Why it is the right Lean target.** [`../../RULES.md`](../../RULES.md) §6.3 records that Mathlib
`v4.33.0` has no Jordan curve theorem, no winding number, no invariance of domain — so everything
in §§4-6 is out of reach, and §6.3 is explicit that this is a large Mathlib gap rather than a slow
formalisation. Theorem A and Proposition S contain **no topology**: Theorem A is the intermediate
value theorem on a continuous real function plus the law of cosines, and Proposition S adds only a
two-point-per-circle hypothesis. Both should be reachable with `Geometry.Euclidean.Angle.*` and
`intermediate_value_Ioo`. I did **not** attempt the formalisation — I did not verify that Mathlib
snapshot myself, so the paragraph above is a **restatement of another file's finding and an
unverified search target**, not a result of this lane, and a Lean worker must re-run the check
rather than quote it (Mathlib moves).

---

## 8. Small triangles at a sharp vertex — where the inscribed triangles actually go

A fact I needed while checking whether a topological argument could deliver the constant `2`, and
which is worth recording on its own because it is exact, cheap and slightly surprising.

> **Proposition T.** Let `v` be a vertex of a simple polygon whose two edges leave `v` in unit
> directions `u, w` at unsigned angle `γ ∈ (0°, 60°]`. Put `s = 2cos γ ∈ [1, 2)`. Then for every
> small `z > 0` the three points
> ```
> p = v + x·u,   q = v + y·u,   c = v + z·w,     with   d = z·√((4 − s²)/3),
> x = z(s − d/z)/2 = (zs − d)/2,   y = x + d,
> ```
> lie on the two edges and form a **nondegenerate equilateral triangle of side `d > 0`** inscribed
> in the polygon — with **two vertices on one edge and one on the other, and none at `v`**.
> Conversely these (and their mirror images with `u, w` exchanged) are the only inscribed
> equilateral triangles all of whose vertices lie on the two edges at `v`, and `x ≥ 0` requires
> exactly `γ ≤ 60°`.

*Proof.* Normalise `z = 1`. With `x < y` on the first ray and `1` on the second,
`|pc|² = x² + 1 − sx`, `|qc|² = y² + 1 − sy` (law of cosines, `2cos γ = s`), and `|pq| = y − x =: d`.
`|pc| = |qc|` gives `x² − sx = y² − sy`, i.e. `(x−y)(x+y−s) = 0`, so `x + y = s`. Substituting
`x = (s−d)/2` into `d² = x² + 1 − sx` gives `d² = (s−d)²/4 + 1 − s(s−d)/2 = d²/4 − s²/4 + 1`, so
`d² = (4 − s²)/3`. Then `x ≥ 0 ⟺ s ≥ d ⟺ 3s² ≥ 4 − s² ⟺ s ≥ 1 ⟺ cos γ ≥ 1/2 ⟺ γ ≤ 60°`. The
side is `d > 0` since `s < 2`, so the triangle is nondegenerate; scaling by `z` scales the whole
configuration. ∎

**Exact witness, `Q(√3)`, inside the `30`-`30`-`120` triangle.** At the `30°` apex `(√3, 0)` of
`J = {(−√3,0), (√3,0), (0,1)}` we have `s = √3`, `d = 1/√3`, `x = 1/√3`, `y = 2/√3`, `z = 1`, giving

```
p = (2/√3, 0),   q = (1/√3, 0),   c = (√3/2, 1/2),     side² = 1/3.
```

All three points lie on `∂J` and the three squared side lengths are `1/3` exactly — checked by an
independent re-verifier that rebuilds the triangle from its coordinates and knows nothing about how
it was found (§10.1). **So the `30`-`30`-`120` triangle inscribes equilateral triangles arbitrarily
close to its exceptional apex; what fails at the apex is only that the apex is not a *vertex* of
one.** That distinction is easy to lose and is exactly what "exceptional" means.

**What this kills, and it is a route I would otherwise have spent the rest of the budget on.**
The natural topological attack is: the space `X = {(a,b) ∈ J² : a + ω(b−a) ∈ J}` of inscribed
equilateral triangles is compact (it is `G^{-1}(J)` for a continuous `G`, `J` closed) and contains
the diagonal `Δ`; if `X ∖ Δ` had compact closure disjoint from `Δ`, the vertex map `X∖Δ → J` would
be a proper map from a compact 1-complex and its image would be closed, forcing the *open* set
`E(P)` to be empty — contradicting the `30`-`30`-`120` witness. Proposition T says precisely why
that is false: `closure(X ∖ Δ)` meets `Δ` exactly at the vertices with `γ ≤ 60°`, i.e. exactly at
the candidate exceptional points, and it meets it in `6` branches there. **The topology degenerates
precisely where the question lives.** A degree count on `X` therefore yields "all but finitely many
points are good" — which is Theorem 1 again, by a longer route — and yields nothing about the
constant. *This paragraph is the least certain thing in the file*: the compactness of `X` and the
branch count are mine and elementary, but the degree language is a heuristic reading of them, I did
not carry out a transversality argument, and I am recording it as a **reason not to spend a budget
on that route**, not as a theorem. If a later worker wants the topological route, this is the
obstruction to defeat, and it is exact.

---

## 9. Where `|E(P)| ≤ 2` dies — precisely

### 9.1 The joint constraint is essentially empty

This is the sharpest statement I can make, and it is the answer to "find the replacement, or show
there is none".

> **Proposition J.** Let `O₁, O₂, O₃ ∈ J` be distinct exceptional points. The complete content of
> Lemma 1, applied at each `Oᵢ` to pairs of points drawn from `{O₁,O₂,O₃}`, is the single statement
> ```
> the triangle O₁O₂O₃ is not equilateral.
> ```
> No constraint on its angles, its side ratios, or its shape follows.

**regularity budget: none.**

*Proof.* At `Oᵢ` the criterion forbids `p, q ∈ J` with `|Oᵢp| = |Oᵢq| = |pq| > 0`. Feeding
`{p,q} = {Oⱼ,O_k}` gives: **not** (`d_ij = d_ik = d_jk`). That is one statement, and it is the same
statement for each of `i = 1,2,3`: the triple is not equilateral. Nothing else is available,
because the criterion at `Oᵢ` only ever compares two points **at equal distance from `Oᵢ`**: if
`d_ij ≠ d_ik` — the generic case — then `Oⱼ` and `O_k` lie on *different* circles about `Oᵢ` and
the criterion says nothing whatever about the angle `∠OⱼOᵢO_k`; and if `d_ij = d_ik`, the criterion
says only `∠OⱼOᵢO_k ≠ 60°`, which combined with the isosceles hypothesis is again exactly
"not equilateral". ∎

**Contrast this with Theorem 2, which is the whole point.** The convex/wedge count consumes
`∠OⱼOᵢO_k < 60°` at all three points and then uses the angle sum. Proposition J says exceptionality
alone supplies *no* upper bound on `∠OⱼOᵢO_k` at any point. So the angle-sum engine has no fuel,
and this is not a failure of ingenuity: the criterion's per-circle character is the reason, and
that character is not an artefact of how it is stated (it is an iff, §2).

**Consequence for the whole family of arguments.** Every necessary condition for exceptionality in
this repository — wedge-type ([`../../RULES.md`](../../RULES.md) §3.1), interior angle `< 60°`
(Theorem 1), half-density (`half-density-obstruction`), no-sweep (`exceptional-set-polygons` §9),
and Theorem A with its two corollaries — is a condition on the **pair `(J, O)`**. A bound on
`|E(J)|` needs a condition on a **triple `(J, Oᵢ, Oⱼ)`** that is not implied by the two separate
pair conditions. Proposition J says the criterion supplies exactly one such condition, and it is
the weakest imaginable one. That is where the count dies, and it dies in the same place for every
argument of this shape.

### 9.2 What survives, and what would have to be new

The one genuine joint resource left is **that `J` is a single simple closed curve through all three
points**: each `Oᵢ`'s condition constrains the *whole* of `J`, including the parts near `Oⱼ` and
`O_k`. That is a real constraint and it is not captured by any pair condition. But it is
topological-plus-metric and I could not turn it into an inequality; §8 explains why the purely
topological part of it cannot produce a constant at all.

So the precise open statement this lane bequeaths, sharpened from
`exceptional-set-polygons` §8.6 by Theorem A:

> *(open, to my knowledge; the polygonal case of what is presumably in Meyerson (1980), which this
> project has not read.)*
> Let `P` be a simple polygon and `O₁,O₂,O₃` three exceptional vertices. Derive a contradiction
> from: `γ(Oᵢ) < 60°`; Corollaries A1 and A2 at each `Oᵢ`; and `J` being one simple closed curve
> through all three. §9.4 shows the first three hypotheses alone are **not** contradictory, so any
> proof must consume the fourth.

### 9.3 The measure route, re-derived, cannot reach three

`half-density`'s Lemma H, re-derived in two lines: if `V` is measurable and `λ(V ∩ σV) = 0` for an
isometry `σ` fixing `O`, then `2λ(V ∩ B(O,R)) = λ(W) + λ(σW) = λ(W ∪ σW) ≤ λ(B(O,R))`. Applied to
`V = Ω̄` and `σ = ρ_{Oᵢ,60°}` via Lemma 3, this gives `λ(Ω̄ ∩ B(Oᵢ,R)) < ½λ(B(Oᵢ,R))` for each `i`.
Three exceptional points give three such inequalities **about three different balls**, with no
packing relation between them: `ρᵢ(Ω̄) ∩ ρⱼ(Ω̄)` is `ρᵢ` of `Ω̄` intersected with a *translate* of
`Ω̄` by `(ω^{-1} − 1)(Oⱼ − Oᵢ)`, and exceptionality constrains `Ω̄` against *rotates*, never against
translates. And `½` is sharp and unimprovable for any angle, because rotation by `60°` cuts the
circle of directions into `6`-cycles and `α(C₆) = 3`; the proof of Lemma H never uses the angle at
all, so no measure argument of that shape can see the order of the rotation. I re-derived all of
this and agree with `half-density` §3.3 and `exceptional-set-polygons` §8.3: **there is no third
point in it.**

### 9.4 The new tools provably cannot close the count — an exact five-vertex refutation

`KILL-CRITERION.md` K3/K4 demand that I stop and report rather than re-scope if the conditions turn
out jointly satisfiable. They do, at the smallest possible size.

> **Refutation.** The integer pentagon
> ```
> (18, 15),  (−5, 5),  (−19, 7),  (−2, −5),  (1, −21)
> ```
> is simple, and its vertices `0`, `2`, `4` — `(18,15)`, `(−19,7)`, `(1,−21)` — **all three**
> satisfy every necessary condition proved in this file: interior angle `< 60°` (Theorem 1),
> Corollary A1 (channel), and Corollary A2 (leaf trapping). Yet `|E| = 1`: only `(18,15)` is
> exceptional. Both deciders agree on all five vertices (§10.1).

So the conditions of §5 and §7 are **jointly satisfiable at three vertices of one simple polygon**,
and therefore cannot, alone, yield `|E(P)| ≤ 2`. Over a seeded population of `250` random simple
polygons the number of vertices simultaneously passing all of them reached **5**, with the
distribution

```
0: 27    1: 64    2: 71    3: 45    4: 31    5: 12       (250 polygons)
```

while `|E(P)|` over the same polygons never exceeded `2`. **The tools are roughly a factor of two
and a half too weak, and the gap is not marginal.** This is the honest verdict of the lane and I am
reporting it as the result rather than padding it: per repo `RULES.md` §0 a clearly documented
refutation is a success.

### 9.5 Routes considered and rejected, with reasons, so they are not rediscovered as insights

- *"Three exceptional points, apply Theorem 2"* — needs wedge-type at all three; refuted by
  `exceptional-set-polygons` §7's 17-gon, which I reproduced exactly (§10.1).
- *"An exceptional point is a hull vertex, use the hull's angle sum"* — false; the 17-gon's tip is
  interior to `conv(J)`. That containment is `exceptional-set-polygons` §7.5's claim, not mine; I
  corroborated it only with a **float** computation of the angular gaps between the directions from
  the tip (largest gap `101.9° < 180°`, so no closed half-plane through the tip contains `J`), and I
  am flagging it as float rather than pretending otherwise. The exceptionality of that tip, which is
  what I actually use, was re-decided **exactly** by both deciders (§10.1).
- *"Exceptional ⟹ diameter endpoint"* (the convex `W0`/`W1` route) — false without convexity;
  I re-decided `C3` exactly and its exceptional point `(−20,0)` has maximal distance² `977` against
  diameter² `1377`.
- *"Use the group generated by the three rotations"* — `ρᵢρⱼ^{-1}` is a **translation** of length
  `|OᵢOⱼ|`; the hypotheses constrain `Ω̄` against rotates, not translates (§9.3).
- *"Interior angles sum to `(n−2)·180°`"* — bounds nothing once reflex vertices exist. The turning
  form is sharper and still not enough: `Σ (180° − γ(v)) = 360°`, so three vertices with
  `γ < 60°` force `> 360°` from those three alone and hence *some* reflex vertex — which merely
  reproves that a three-exceptional polygon must be non-convex, already known.
- *"Compactify the space of inscribed triangles and count"* — §8: the compactification degenerates
  exactly at the sharp vertices, and a degree count returns Theorem 1, not a constant.

---

## 10. Numerics — `numerical`, evidence only, never a proof step

### 10.1 Instruments, and the validation gate (K1) run first

Two exact deciders, sharing no code:

1. **The committed** `experiments/inscribed-triangle-polygons/geom.py` — **read and run, never
   modified** (another lane's files, repo `RULES.md` §2). Works in `Q(√3)` by segment intersection.
2. **Mine, written from scratch for this lane** — my own `Q(√3)` class with its own sign algorithm,
   my own parametric segment solve by Cramer with an explicit parallel/collinear branch, my own
   simplicity test, and an independent witness re-verifier that rebuilds a triangle from its
   coordinates and checks membership and the three squared side lengths.

**No `sympy` predicate decides anything** — the committed experiment's own README records that
`sympy.geometry` gave false positives on this problem's tightest fixtures. **No float decides
anything**: the deciders are exact in `Q(√3)`; the §7 instrument is exact in `Q` except that square
roots are handled by **certified rational brackets refined until a sign is proved**, never by
floating point, and a sign that cannot be certified is reported as undecided rather than guessed
(it never occurred).

**Gate, run before anything else.** Controls: equilateral triangle — all three vertices good;
`30`-`30`-`120` — both `30°` apexes exceptional and the `120°` vertex good; unit square — all four
good; the triangle `(0,0),(5,0),(2,4)` — exactly one exceptional vertex, `(5,0)`. All four match
the values recorded in `exceptional-set-polygons` §10 and `exceptional-pair-rigidity` §8.1, and
every "good" verdict carries a witness that passes the independent re-verifier.
**Cross-check: 400 seeded random simple polygons, 3 078 vertices, zero disagreements** between my
decider and the committed one. Independent reproduction of the four published witnesses:

```
spiral17  mine=[0]     committed=[0]     agree
C2        mine=[1, 3]  committed=[1, 3]  agree
C3        mine=[1, 7]  committed=[1, 7]  agree
FORK      mine=[]      committed=[]      agree
```

**The hazard the killed worker flagged, and how it is discharged.** Its last note — *"the `1e9` is
a grid artifact — my `r`-sampling can skip narrow radial windows; let me partition by critical radii
instead"* — is correct and load-bearing, and the §7 instrument is built the way it prescribes. The
critical radii are computed **exactly and completely**: the squared distances `|Ov|²` to every
vertex, plus the squared distance to every edge whose perpendicular foot is strictly interior. The
branch structure is constant on each open interval between consecutive critical values, so the
instrument evaluates **one rational midpoint per interval** and that is a *partition*, not a sample:
no radial window, however narrow, can be stepped over, because every window's endpoints are
critical values and every interval between them is visited. A uniform sweep would have manufactured
false exceptional points here exactly as that worker predicted.

### 10.2 How much of `good` the new conditions actually explain

Seeded population, `200` random simple polygons (`4`-`13` vertices, half "spiky"), restricted to
the `440` **sharp** vertices (interior angle `< 60°`), which by Theorem 1 is where `E(P)` must live:

| | count |
|---|---|
| sharp vertices | 440 |
| of which exceptional | 177 |
| exceptional violating Corollary A1 | **0** |
| exceptional violating Corollary A2 | **0** |
| sharp **good** vertices | 263 |
| good, caught by A1 (channel fails) | 68 |
| good, caught by A2 (leaf fails) | 32 |
| good, caught by at least one | 92 |
| **good, satisfying both conditions anyway** | **171** (65 %) |

**What was and was not tested.** The instrument tests Corollary A1 in full and the `{f > r}`
**leaf** clause of Corollary A2 in full. It does **not** test A2's `{f < r}` single-minimum clause;
that clause is proved but unexercised, and I am flagging it rather than letting the table imply
otherwise. Every "violating" count in the table therefore means "violating A1" or "violating A2's
leaf clause".

Two things to read off. **First, the zeros are the falsifiable half**: Corollaries A1 and A2 are
consequences of exceptionality, so a single violation at an exceptional vertex would mean my proof
of Theorem A is wrong. `177` exceptional vertices, `0` violations, on top of the five hand-checked
witnesses. **Second, the `171` is the honest half**: the conditions explain only about `35 %` of
good sharp vertices, and A1 and A2 overlap on only `8` — they are largely complementary and jointly
still far from sufficient. That number is the quantitative form of §9.4.

### 10.3 Census, and the consistency check on the unread bound

Over the two seeded populations (`400 + 250` polygons, plus the `200` of §10.2 — `850` simple
polygons, all decided exactly), the `|E(P)|` histograms were

```
400 random:   0:145  1:143  2:112              max 2
250 mixed:    0: 83  1: 97  2: 70              max 2
200 mixed:    0: 76  1: 71  2: 53              max 2
```

**Three never occurred.** [`../../README.md`](../../README.md) row 2 records `|E(J)| ≤ 2` as
`cited`\* — provisional, no source text read — and it is used here **only** as this after-the-fact
check on output. The check passes. It cannot promote the citation, and nothing in §§2-9 used it.

**What would make this weak.** The generators are mine and draw small integer coordinates in a
bounded box. A polygon carrying three exceptional vertices, if one exists, would very plausibly be
a *deliberate* construction — the 17-gon is proof that the interesting polygons here are built, not
sampled — and a concurrent lane is trying to build exactly that. So this census is weak evidence
and I am not treating it as more. What it does establish, and this is not weak, is §9.4: the
*conditions* are satisfiable at three vertices at once.

---

## 11. The three cheap filters ([`../../RULES.md`](../../RULES.md) §3), all run

### 11.1 Wedge test (§3.1) — run, in both directions

**As a tool:** Theorem 2 is the sharp count of how many points pass it — at most two — and that is
the part of the convex argument that transfers for free. **As a target:** the 17-gon of
`exceptional-set-polygons` §7, which I re-decided exactly with both deciders, has an exceptional
vertex that *fails* the test (its curve spans `258°` from that vertex), so the test is sufficient
and **not necessary**, exactly as §3.1's own "do not over-read it" warns. Consistency check: the
§3.1 witness itself, the `30`-`30`-`120` triangle, has both `30°` apexes wedge-type and exceptional
and no other exceptional point — reproduced exactly, twice.

### 11.2 Square test (§3.2) — run; the argument does not transfer, and the reason is structural

Replace `60°` by `90°` throughout, and note first, as the brief requires, that **the square peg
problem *is* known for polygons**, so a transfer would not be an automatic error — but it would be
an alarm, and here is what actually happens.

- **Lemma 1 has no square analogue, and everything in this file is phrased in it.** Its content is
  that an isosceles triangle with a `60°` apex *is* equilateral, so the third point is free. Two
  points at equal radius subtending `90°` at `O` give three corners of a square; the fourth,
  `p + q − O`, is *determined* and under no constraint to lie on `J`. There is no iff at `90°`, so
  the object every statement here quantifies over does not exist.
- **Theorem A does survive verbatim** — its proof never uses the angle, only that `|pq| = r`
  characterises the configuration — and yields: *two continuous radial branches about a point
  admitting no inscribed isosceles right triangle, merging at one end, satisfy `|p−q| < r√2`
  throughout.* True, and about **isosceles right triangles**, not squares. Likewise Proposition S
  becomes a statement about inscribed isosceles right triangles.
- **Theorem 2 transfers in weakened form** ("at most three", four points in convex position with
  interior angles summing to `360°`), and is equally powerless, for the same reason.

The decisive evidence that nothing here proves too much is that the analogue of **Theorem 1** is
flatly false at `90°`: Theorem 1 says all but finitely many boundary points of a polygon are
triangle vertices, whereas a triangle admits only finitely many inscribed squares, so only finitely
many of its uncountably many boundary points are corners of one — the opposite of "all but finitely
many". `convex-vertex-criterion` §5 records the numerical form (399 sampled points on a side of the
equilateral triangle, **zero** admitting an inscribed square with a corner there). I did not verify
the exact count of inscribed squares in a triangle and do not rely on it; the qualitative gap is
what the filter needs. **Pass.**

### 11.3 Polygon control (§3.3) — run, and it is this lane's home ground

Every claim here is a claim about polygons, so the control applies directly and was run in full:
the gate and cross-check of §10.1 (`3 078` vertices, zero disagreements, four published witnesses
reproduced), Theorem 1 tested implicitly at every one of those vertices, Corollaries A1 and A2
tested at `177` exceptional vertices with zero violations, and the `≤ 2` conjecture surviving `850`
polygons. Per §3.3 the surviving claims are therefore **merely not yet dead** — polygons are the
most regular curves there are, and Theorem 1 is *known* to have no general analogue
(`spiral-tip-witness` exhibits a Jordan curve whose exceptional point has no sector at all). The
place the control did decisive work in the *other* direction is §9.4, where it killed this lane's
own route with a five-vertex integer pentagon.

---

## 12. Kill-criterion outcomes

[`KILL-CRITERION.md`](./KILL-CRITERION.md) was written **by an earlier worker in this lane**, before
any computation, and that worker was terminated before producing an attack. It is a genuine
pre-registration artifact and I have **not edited it**. Its predictions P1-P4 are *its* predictions,
not mine; I score them below only because a pre-registration nobody scores is worthless, and I flag
clearly that P2/P3 concern a search design (a straight-armed "Y" tree) that I did **not** run — I
attacked the count analytically via Theorem A instead, which is a different route within the same
lane question, and I say so rather than pretending its predictions were about my work.

| | outcome |
|---|---|
| **K1** validation gate | **Passed and run first.** Four controls reproduced exactly; `3 078` vertices cross-checked against the committed decider with zero disagreements; no search result was computed before the gate passed. |
| **K2** extraordinary-claim trip-wire | **Did not fire.** No polygon with three exceptional vertices appeared, in `850` exactly decided polygons. Nothing in this file claims one. |
| **K3** arc/ancestor lemma jointly satisfiable ⟹ stop | **Fired, in the form appropriate to my route (§9.4).** The conditions I proved are jointly satisfiable at three vertices of a five-vertex pentagon. I stopped trying to close the count with them and reported that, which is what K3 instructs. |
| **K4** search infeasible, mechanism unknown | **Not applicable, and better than it feared.** The route did not merely fail to find a mechanism — §9.1 and §9.4 identify *why* no mechanism of this shape exists. That is a mechanism for the failure, not a shrug. |
| **K5** proof self-audit against three witnesses | **Run, and it is §7.5.** The `30`-`30`-`120` triangle, the 17-gon spiral witness and the pentagon `C2` all survive every statement in §§5-7, decided exactly by two deciders. Nothing here kills any of them. |
| **K6** square test | **Run, §11.2**, including the honest note that square peg is known for polygons so a transfer would be an alarm rather than an automatic error. There is no transfer: Lemma 1 has no `90°` analogue. |
| **K7** compute budget | Respected. Everything in §10 runs in a few minutes of wall clock; no background job was started and none was left running. |
| **K8** no self-granted status | Respected. Everything here is `sketch` or `numerical`, nothing goes in `results/`, and Meyerson appears once, in §10.3, as a consistency check on output. |

| its prediction | outcome |
|---|---|
| **P1** decider reproduces all four controls first or second attempt | **Correct** for my from-scratch decider: all controls and all four published witnesses on the first run. |
| **P2** thin-tree reduction sound | **Not tested.** I did not build the thin-tree search; Theorem A supersedes the need for it, since §7.5 explains the tuning-fork family analytically. |
| **P3** the three arc conditions are not jointly satisfiable | **Wrong in spirit, and decisively.** Its own confidence line called this "the prediction I most expect to be wrong". The analogous conditions I proved *are* jointly satisfiable, at three vertices of a five-vertex integer pentagon (§9.4). |
| **P4** this lane will not close `\|E(P)\| ≤ 2` | **Correct.** |

---

## 13. Reproducing everything

Python 3.11, standard library only. No `sympy`. The first block imports the **committed**
`experiments/inscribed-triangle-polygons/` modules, which this lane **reads and runs but never
modifies** (another lane's files, repo `RULES.md` §2). My own scripts were written in a scratch
directory and are **not committed**, because `experiments/` is not mine to write to — so this
section does **not** meet repo `RULES.md` §4's "reproducible from a single command" bar and must
not be read as though it did. What *is* fully reproducible from this file alone is every explicit
witness: the five-vertex pentagon of §9.4, the `Q(√3)` small triangle of §8, and the four published
polygons of §10.1. Seeds: `20260830` (§10.2 census and the 400-polygon cross-check), `424242`
(§9.4 population), `777` (§9.4 minimal search).

### 13.1 The §9.4 refutation, decided by the committed decider

```python
import sys
sys.path.insert(0, "experiments/inscribed-triangle-polygons")   # committed; read-only
from geom import P, decide_good, is_simple

V = [(18, 15), (-5, 5), (-19, 7), (-2, -5), (1, -21)]
poly = [P(x, y) for (x, y) in V]
print(is_simple(poly))                                     # (True, 'simple')
print([decide_good(poly, O)["good"] for O in poly])        # [False, True, True, True, True]
```

Vertices `0`, `2`, `4` are the three with interior angle `< 60°` that pass Corollaries A1 and A2;
only vertex `0` is exceptional.

### 13.2 The §8 small triangle, exact in `Q(√3)`

```python
import sys
sys.path.insert(0, "experiments/inscribed-triangle-polygons")
from fractions import Fraction as F
from geom import P, decide_good, verify_triangle
from k3 import K

T = [P(K(0, -1), 0), P(K(0, 1), 0), P(0, 1)]      # (-sqrt3,0), (sqrt3,0), (0,1)
p = P(K(0, F(2, 3)), 0)                           # (2/sqrt3, 0)
q = P(K(0, F(1, 3)), 0)                           # (1/sqrt3, 0)
c = P(K(0, F(1, 2)), K(F(1, 2), 0))               # (sqrt3/2, 1/2)
print(decide_good(T, T[1])["good"])         # False -- the 30-degree apex is exceptional
ok, det = verify_triangle(T, p, q, c)
print(ok, det["side_squared"])              # True ['1/3', '0'] -- side^2 = 1/3 exactly
```

Both blocks above were executed as printed; the comments are the actual output.

### 13.3 The §7 instrument, in outline

The full scripts are `mydec.py` (independent `Q(√3)` decider), `channel.py` (Corollary A1) and
`gaptree.py` (Corollary A2). Their whole content is:

1. **Critical radii, exactly.** `{ |Ov|² : v a vertex }` together with, for each edge `[A,B]` whose
   perpendicular foot from `O` is strictly interior (`0 < (O−A)·(B−A) < |B−A|²`), the exact squared
   distance from `O` to the line. Local minima of `f` are the interior feet plus the vertices `v`
   with `(v−O)·(A−v) > 0` and `(v−O)·(B−v) > 0`; local maxima are the vertices with both dot
   products negative.
2. **One rational midpoint per interval** between consecutive critical values — a partition, never
   a sweep.
3. **Boundary points at that radius**, per edge, from the quadratic
   `|A + s(B−A) − O|² = ρ`, with `√D` held as a **certified rational bracket** (bisection on
   `Fraction`s) and propagated through interval arithmetic.
4. **The test.** For a branch pair `p, q`, the certified sign of `|p−q|² − ρ`. Refine the bracket
   until the sign is proved; report "undecided" otherwise (it never occurred). By Lemma 1 the value
   is nonzero at an exceptional point, so refinement terminates there.
5. **Which pairs to test.** Boundary points sorted by curve parameter from `O`; consecutive pairs
   `(t₁,t₂), (t₃,t₄), …` bound the components of `{f > ρ}`; a component is a **leaf** when exactly
   one critical point lies strictly inside it and it is a maximum.

**No angle is ever computed and no argument is ever lifted**, which is the implementation payoff of
stating Lemma 1 metrically (§2).
