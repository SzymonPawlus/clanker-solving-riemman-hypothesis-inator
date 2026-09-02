# The exceptional set of a simple polygon: the reduction closes, "wedge-type" is false, the count does not close

```
regularity budget: polygonal (simple polygon, finitely many straight edges) for
      Theorems 1, 3 and 4; Jordan only for Lemma 3, Lemma 4 and Theorem 2; and
      *none at all* (J used as a bare point set) for Lemma 1 and Propositions 5-6.
      Every statement carries its own budget line in situ.
      What breaks first if "polygonal" is dropped from Theorem 1: Lemma 2 - a
      general Jordan curve need not contain any sector of positive aperture in
      its interior at any point, so there is nothing to feed Lemma 4.
      What breaks first if "Jordan" is dropped from Lemma 3: the proof uses the
      Jordan curve theorem three times (two complementary components; d(Omega) =
      d(E) = J; the unbounded component is unique), and a planar continuum has
      none of that.
```

- Lane: **prove `|E(P)| <= 2` for every simple polygon, or find what actually happens.**
- Author: `claude` (Claude Opus 5), 2026-08-29, branch `claude/inscribe-equilateral-triangle-oj15x1`.
  Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), **written before any computation in
  this lane** (`../../RULES.md` §6.2 / repo `RULES.md` §6.2) — read its provenance paragraph, which
  says exactly what had and had not happened at the moment it was written. Outcomes: §11.
- Journal: [`../../../../notebook/claude/2026-08-29-iet-exceptional.md`](../../../../notebook/claude/2026-08-29-iet-exceptional.md).
- Read before starting, edited by this lane: none of them —
  [`../convex-vertex-criterion/`](../convex-vertex-criterion/), [`../rotation-continuity/`](../rotation-continuity/),
  [`../spiral-tip-witness/`](../spiral-tip-witness/), [`../half-density-obstruction/`](../half-density-obstruction/),
  [`../rectifiable-case/`](../rectifiable-case/), plus [`../../README.md`](../../README.md),
  [`../../RULES.md`](../../RULES.md) and repo `RULES.md` §0, §3, §7.

---

## 0. Verdict, up front

| § | Statement | Status |
|---|---|---|
| §2 | **Lemma 1 (criterion).** For any `S ⊆ R²` and `O ∈ S`: `O` is a vertex of a nondegenerate equilateral triangle with all vertices in `S` **iff** some circle about `O` carries two points of `S` exactly `60°` apart | `sketch` — mine, re-derived from the definitions in three lines |
| §3 | **Lemma 2 (local structure of a polygon).** At every `O ∈ ∂P` the interior contains an open sector of aperture equal to the interior angle | `sketch` — mine; polygonal Jordan curve theorem |
| §4 | **Lemma 3 (region lemma).** `J ∩ ρ(J) = {O}` ⟹ `Ω̄ ∩ ρ(Ω̄) = {O}` | `sketch` — mine, **re-derived from scratch**; the same statement is `rotation-continuity`'s Lemma A and `half-density`'s §4 |
| §4 | **Lemma 4 (sector criterion).** a closed `60°` sector at `O` inside `Ω̄` ⟹ `O` good | `sketch` — mine; two lines from Lemma 3 |
| §5 | **Theorem 1 (the reduction).** For every simple polygon `P`, `E(P) ⊆ { vertices of interior angle < 60° }` — in particular `E(P)` is finite and contains no non-vertex boundary point | `sketch` — mine |
| §6 | **Theorem 2 (wedge count).** Every Jordan curve has **at most two** wedge-type points, hence at most two wedge-type exceptional points | `sketch` — mine; pure angle-sum, no topology |
| §7 | **Theorem 3 (the witness).** An explicit rational simple polygon (17 vertices) with an exceptional vertex `O` that is **not** wedge-type: the directions from `O` to points of `J` span `258°` | `sketch` — mine, with an elementary proof that uses **no** topology; independently confirmed by two exact deciders |
| §7.4 | **Corollary.** "Every exceptional point of a simple polygon is wedge-type" is **false**. `spiral-tip-witness` §9.3 states it as motivation; that motivation is wrong, and the rotating-wedge mechanism is **not** invisible to polygons | `refuted` |
| §8 | **`|E(P)| ≤ 2` for simple polygons** | **not closed.** §8 says exactly where it dies |
| §9 | **Proposition 5 (no sweep).** The angular separation of two continuous radial branches of `J` about an exceptional point can never cross `±60°` | `sketch` — mine; one line from Lemma 1 plus the intermediate value theorem |
| §10 | Numerics: 6 026 simple polygons scanned exactly for exceptional counts (plus a 746-polygon control battery); **max 2 exceptional vertices**, never 3 | `numerical` |

**One-sentence summary.** The reduction `E(P) ⊆ vertices` is true and provable, and can be sharpened
to interior angle `< 60°`; the natural next step — "and every such exceptional vertex is wedge-type,
so the convex angle-sum count applies" — is **false**, refuted here by an explicit 17-vertex
rational polygon; consequently `|E(P)| ≤ 2` is *not* proved by this route, and I did not prove it by
any other, though a 6 026-polygon exact search found no polygon with three.

**Nothing here is assumable** (repo `RULES.md` §3), including by me, including Theorem 1.

**Dependency hygiene.** Everything below rests on: the Jordan curve theorem (for polygons only,
where it is elementary — but it *is* a dependency and is declared), isometry-invariance of planar
Lebesgue measure, the intermediate value theorem, and arguments written out in full here. I have
**re-derived** rather than imported: the rotation criterion (`rotation-continuity` §2 Observation R,
`convex-vertex-criterion` §1 Proposition R, `spiral-tip-witness` §2 Lemma 1, `half-density` §2,
`rectifiable-case` §2 — five statements of the same fact, and I derived a sixth before rereading
them), the region lemma (`rotation-continuity` §4 Lemma A = `half-density` §4 = `rectifiable-case`
§6 Lemma 3), and the sector criterion (`rotation-continuity` §5 Lemma B). Where I land in the same
place I say so as a *cross-check*, which confers nothing: all of those are `sketch`, and a `sketch`
may not rest on a `sketch`. I use **nothing** from `rectifiable-case`'s Theorem T, from
`convex-vertex-criterion`'s Theorems A–E, or from `spiral-tip-witness`'s Theorems 1–3. Meyerson's
bound is **not** an input anywhere; it appears only in §8.4 as an external consistency check *on*
the output, and [`../../README.md`](../../README.md) marks it `cited`\* (provisional, provenance
P2, no source text read), which is a second reason it must not be one.

---

## 1. Setting and notation

`P ⊂ R²` is a **simple polygon**: the closed bounded region bounded by a simple closed polygonal
curve `J = ∂P` with finitely many vertices and straight edges. `Ω` is the bounded component of
`R² \ J` and `E` the unbounded one; by the Jordan curve theorem (elementary in the polygonal case)
these are the only two, and `∂Ω = ∂E = J`. Write `Ω̄ = Ω ∪ J = R² \ E`, a compact set. Identify
`R² = C`.

For `O ∈ J`, `ρ = ρ_{O,60°}` is rotation by `+60°` about `O`. `O` is **good** if some nondegenerate
equilateral triangle has all three vertices on `J` and one of them equal to `O`, and **exceptional**
otherwise; `E(J)` is the set of exceptional points. For `r > 0` put

```
Θ(r) = { θ ∈ R/360° : O + r e^{iθ} ∈ J }        (the direction set of J at radius r about O)
D(O) = { arg(x − O) : x ∈ J \ {O} }             (all directions from O)
```

`O` is **wedge-type** when there is a closed convex cone with apex `O` and opening `< 60°`
containing all of `J` — equivalently, when `D(O)` lies in a closed arc of length `< 60°`. This is
[`../../RULES.md`](../../RULES.md) §3.1's hypothesis; that section proves wedge-type ⟹ exceptional.

**Interior angle.** For `O ∈ J` let `γ(O) ∈ (0°, 360°)` be the aperture of the sector of
`B(O,ε) \ J` that lies in `Ω`, for `ε` small (Lemma 2 shows this is well defined and equals the
usual interior angle: `180°` at a non-vertex point, the vertex angle at a vertex).

---

## 2. Lemma 1 — the criterion, re-derived

> **Lemma 1.** Let `S ⊆ R²` and `O ∈ S`. Then `O` is a vertex of a nondegenerate equilateral
> triangle with all three vertices in `S` **iff** there are `r > 0` and `θ` with
> `O + r e^{iθ} ∈ S` and `O + r e^{i(θ + 60°)} ∈ S`.

**regularity budget: none.** `S` is used only as a set of points — not closed, not connected, not
a curve. That is why nothing topological can leak into any use of it below.

*Proof.* Normalise `O = 0`.

(⇐) Put `Pt = r e^{iθ}`, `Qt = r e^{i(θ+60°)}`. Then `|O Pt| = |O Qt| = r` and, by the law of
cosines, `|Pt Qt|² = r² + r² − 2r² cos 60° = r²`. So all three pairwise distances equal `r > 0`;
the three points are distinct (`r > 0` separates each from `O`, and `e^{i60°} ≠ 1` separates
`Pt` from `Qt`). Nondegenerate, side exactly `r`.

(⇒) Let `O, Pt, Qt ∈ S` be equilateral of side `s > 0`. Then `|OPt| = |OQt| = s`, so
`Pt = s e^{iθ_P}`, `Qt = s e^{iθ_Q}`, and `cos ∠Pt O Qt = (s²+s²−s²)/(2s²) = 1/2`, so the residue
`θ_Q − θ_P ≡ ±60° (mod 360°)`. Take `r = s` and `θ = θ_P` or `θ = θ_Q` accordingly. ∎

**Restated.** `O` is exceptional **iff** for every `r > 0`, no two elements of `Θ(r)` differ by
exactly `60°` mod `360°`. Note this compares points **on one circle at a time**; it never compares
different radii. That single feature is what §7 exploits.

**Cross-check, not a dependency.** This is the polar form of `rotation-continuity` §2 Observation R,
`convex-vertex-criterion` §1 Proposition R, `spiral-tip-witness` §2 Lemma 1, `half-density` §2 and
`rectifiable-case` §2. Six independent derivations of one three-line fact now exist in this
directory; that is decorrelation evidence and nothing more (all are `sketch`). It is also
**kill-criterion K1**, which was run against the committed exact decider before anything else in
this lane: equilateral triangle — all three vertices good; `30`–`30`–`120` triangle — both `30°`
apexes exceptional, the `120°` vertex good; unit square — all four corners good. All three match.
One caution I want on the record: the `mod 360°` in Lemma 1 cannot be replaced by an unsigned
difference in `[0°,180°]`; the convex lane can drop it only because convexity puts every direction
in a half-plane, and §7's direction sets wrap most of the way round the circle.

---

## 3. Lemma 2 — what a polygon looks like at a boundary point

> **Lemma 2.** Let `O ∈ J = ∂P`. For all sufficiently small `ε > 0`, `J ∩ B(O,ε)` is either a
> diameter of `B(O,ε)` (if `O` is not a vertex) or a pair of radii (if `O` is a vertex), and
> `B(O,ε) \ J` has exactly two components, open circular sectors of apertures `γ` and `360° − γ`.
> Exactly one of them is contained in `Ω`; its aperture is `γ(O)`, and `γ(O) = 180°` when `O` is
> not a vertex.

**regularity budget: polygonal + Jordan curve theorem for polygons.**

*Proof.* `J` is a finite union of closed segments. Choose `ε` smaller than the distance from `O` to
every edge and every vertex of `P` not containing `O`. Then `J ∩ B(O,ε)` consists exactly of the
parts of the (one or two) edges through `O` inside `B(O,ε)`: a diameter if `O` is interior to an
edge, two radii if `O` is a vertex. In both cases `B(O,ε) \ J` is a disjoint union of two open
sectors `S₁, S₂` with apertures summing to `360°`.

Each `Sᵢ` is connected and disjoint from `J`, hence lies wholly in `Ω` or wholly in `E`. Since
`O ∈ J = ∂Ω = ∂E`, the ball `B(O,ε)` meets both `Ω` and `E`; and `B(O,ε) ∩ (Ω ∪ E) = S₁ ∪ S₂`. So
one sector lies in `Ω` and the other in `E`. ∎

This is the entire use made of "polygon" anywhere in this file, and it is worth naming what it
supplies that a general Jordan curve does not: **a sector of positive aperture inside `Ω̄` at every
single boundary point**. `rotation-continuity` §8 records that it could not establish this for a
general Jordan domain even at one point, and `spiral-tip-witness` §4.3 exhibits a Jordan domain
where it fails at a point outright. It is not a technicality; it is the whole reason the polygonal
case is tractable.

---

## 4. Lemma 3 (the region lemma) and Lemma 4 (the sector criterion), re-derived

Lemma 1 is a statement about the *curve*; what Lemma 2 hands me is a statement about the *region*.
Lemma 3 is the bridge. It is `rotation-continuity`'s Lemma A and `half-density`'s §4; I re-derived
it before rereading either, and I record my derivation in full because `RULES.md` §3 forbids me
from leaning on theirs.

> **Lemma 3.** Let `J` be a Jordan curve, `O ∈ J`, `ρ` any rotation about `O` by an angle not a
> multiple of `360°`. If `J ∩ ρ(J) = {O}` then `Ω̄ ∩ ρ(Ω̄) = {O}`.

**regularity budget: Jordan.** Uses the Jordan curve theorem (two components; `∂Ω = ∂E = J`; the
unbounded component is unique) and isometry-invariance of Lebesgue measure. Nothing else — no
rectifiability, no tangent, no local structure.

*Proof.* Throughout, `ρ` is a homeomorphism of the plane with `ρ(J), ρ(Ω), ρ(E)` the curve, bounded
component and unbounded component of the rotated configuration, and `ρ(Ω̄) = R² \ ρ(E)`.

**Step 0 (the squeeze).** *If `ρ(Ω̄) ⊆ Ω̄` then `J = ρ(J)`.* Indeed `λ(ρ(Ω̄)) = λ(Ω̄) < ∞` (isometry;
`Ω̄` compact), so `λ(Ω̄ \ ρ(Ω̄)) = 0`. The set `Ω \ ρ(Ω̄)` is open (`Ω` open, `ρ(Ω̄)` closed) and
contained in that null set, hence empty. So `Ω ⊆ ρ(Ω̄)`, and taking closures (`ρ(Ω̄)` is closed)
`Ω̄ ⊆ ρ(Ω̄)`, so `Ω̄ = ρ(Ω̄)`. Taking boundaries and using `∂Ω̄ = ∂(R²\E) = ∂E = J`, we get
`J = ∂Ω̄ = ∂ρ(Ω̄) = ρ(∂Ω̄) = ρ(J)`.

**Step 1 (the containment test).** *If `ρ(J) ⊆ Ω̄` then `J = ρ(J)`.* `E` is connected, unbounded and
disjoint from `ρ(J)`, so it lies in one component of `R² \ ρ(J)`; being unbounded it lies in the
unbounded one, `ρ(E)`. Hence `ρ(Ω̄) = R² \ ρ(E) ⊆ R² \ E = Ω̄`, and Step 0 applies.

Now assume `J ∩ ρ(J) = {O}`. Since `J` has more than one point, `J ≠ ρ(J)`, so Steps 0 and 1 are
available as *contradiction generators*.

**Step 2.** `ρ(J) \ {O}` is connected (a circle minus a point, homeomorphically) and disjoint from
`J`, so it lies in `Ω` or in `E`. If it lies in `Ω`, then `ρ(J) ⊆ Ω ∪ {O} ⊆ Ω̄` and Step 1 gives
`J = ρ(J)` — contradiction. **So `ρ(J) \ {O} ⊆ E`**, i.e. `ρ(J) ∩ Ω = ∅`.

**Step 3.** Symmetrically, `J \ {O}` is connected and disjoint from `ρ(J)`, so it lies in `ρ(Ω)` or
in `ρ(E)`. If in `ρ(Ω)`, then `J ⊆ ρ(Ω̄)` and Step 1 with the roles of `J` and `ρ(J)` exchanged
gives `ρ(J) = J` — contradiction. **So `J \ {O} ⊆ ρ(E)`**, whence `J ∩ ρ(Ω) = ∅` (also
`O ∈ ρ(J)`, so `O ∉ ρ(Ω)`).

**Step 4.** `ρ(Ω)` is connected and, by Step 3, disjoint from `J`; so it lies in `Ω` or in `E`. If
`ρ(Ω) ⊆ Ω` then `ρ(Ω̄) = ρ(cl Ω) = cl(ρΩ) ⊆ cl Ω = Ω̄` and Step 0 gives `J = ρ(J)` — contradiction.
**So `ρ(Ω) ⊆ E`**, i.e. `Ω ∩ ρ(Ω) = ∅`.

**Step 5.** `Ω̄ ∩ ρ(Ω̄) = (Ω ∩ ρΩ) ∪ (Ω ∩ ρJ) ∪ (J ∩ ρΩ) ∪ (J ∩ ρJ) = ∅ ∪ ∅ ∪ ∅ ∪ {O} = {O}`, using
Step 4, Step 2, Step 3 and the hypothesis in that order. ∎

> **Lemma 4 (sector criterion).** If for some `ε > 0` and some `a` the **closed** sector
> `S = { O + t e^{iθ} : 0 ≤ t ≤ ε, θ ∈ [a, a + 60°] }` is contained in `Ω̄`, then `O` is good.

*Proof.* Let `x = O + (ε/2) e^{i(a+60°)}`. Then `x ∈ S ⊆ Ω̄`; and `ρ^{-1}(x) = O + (ε/2)e^{ia} ∈ S
⊆ Ω̄`, so `x ∈ ρ(Ω̄)`. Since `ε/2 > 0`, `x ≠ O`, so `Ω̄ ∩ ρ(Ω̄) ⊋ {O}`. By Lemma 3 (contrapositive)
`J ∩ ρ(J) ⊋ {O}`; pick `q` in that intersection with `q ≠ O`, put `p = ρ^{-1}(q) ∈ J`, and apply
Lemma 1 with `r = |Oq| > 0`. ∎

**A quantitative warning I am not falling for.** Lemma 4 produces *some* triangle, with **no control
on its side length** — `q` is produced by a non-constructive contrapositive and is in general not
`x`. `rotation-continuity` §5 originally claimed side `ε/2` here; `rectifiable-case` §7 refuted that
with the unit square at `(1/2, 0)`, and the correction is now applied in that file. I state Lemma 4
with no side-length clause for exactly that reason, and nothing below wants one.

---

## 5. Theorem 1 — the reduction

> **Theorem 1.** Let `P` be a simple polygon, `J = ∂P`. Every `O ∈ J` with interior angle
> `γ(O) ≥ 60°` is good. Consequently
> ```
> E(P) ⊆ { vertices of P of interior angle < 60° },
> ```
> a finite set; in particular **no non-vertex boundary point of a simple polygon is exceptional**.

**regularity budget: polygonal + Jordan (through Lemmas 2 and 3).** Drop "polygonal" and Lemma 2
fails; drop "Jordan" and Lemma 3 fails.

*Proof.* By Lemma 2 there is `ε > 0` with an open sector `U ⊆ Ω` of aperture `γ(O)`, apex `O`,
radius `ε`. Its closure contains the closed sector of aperture `γ(O)` and radius `ε/2`, which
therefore lies in `Ω̄`. If `γ(O) ≥ 60°`, that closed sector contains a closed sector of aperture
exactly `60°`, and Lemma 4 applies. A non-vertex boundary point has `γ = 180° ≥ 60°`; a reflex
vertex has `γ > 180° ≥ 60°`. So an exceptional point must be a vertex of interior angle `< 60°`, and
a polygon has finitely many vertices. ∎

**Where the briefing's suggested shortcut fails, and why I did not take it.** The brief suggested
that a non-vertex point has a tangent *line*, hence a local cone of opening `180°`, hence a
triangle. That is a genuine gap: the criterion (Lemma 1) needs two points of `J` at **equal radius**
`60°` apart, and a tangent line gives only the two directions `±u`, which are `180°` apart, not
`60°`. The local segment through `O` contributes exactly two directions to `Θ(r)` for small `r`, and
`180° ≠ 60°`. What actually closes the gap is that the polygon's *interior* fills a half-disc there
— a statement about `Ω`, not about `J` — and that half-disc only becomes points of `J` through the
region lemma. `rotation-continuity` §7.2 makes the same point in the other direction: the condition
must be on the tangent cone of `Ω̄`, never on the set of limit directions along `J`, and a Jordan
domain with an outward cusp shows the two differ fatally.

**The `60°` boundary is on the good side, and that is not an accident of the proof.** Lemma 4's
sector is closed and its aperture is allowed to equal `60°` exactly. At a polygon vertex of interior
angle exactly `60°` there is also a direct construction needing no topology at all: the two incident
edges make an angle of exactly `60°`, so the two points at a common distance `t ≤ min(edge lengths)`
along them are on `J`, at equal radius, `60°` apart. The committed exact battery has two fixtures
with an interior angle of exactly `60°` (`cvx-60deg-scalene`, `cvx-60deg-kite`) and both are good;
its `10^-14`-degree bracketing of the boundary agrees. `Q`-coordinate polygons can never realise the
boundary case (`tan 60° = √3 ∉ Q`), which is why those two fixtures live in `Q(√3)`.

---

## 6. Theorem 2 — at most two wedge-type points, and why that is not enough

> **Theorem 2.** For any Jordan curve `J` (indeed any set with at least two points) there are at
> most **two** wedge-type points. Since wedge-type ⟹ exceptional, at most two exceptional points
> are wedge-type.

**regularity budget: none** — `J` is a point set. No topology, no convexity, no measure.

*Proof.* Suppose `O₁, O₂, O₃ ∈ J` are distinct and each wedge-type, with cone openings
`w₁, w₂, w₃ < 60°`. Any two points of `J \ {Oᵢ}` subtend at `Oᵢ` an angle at most `wᵢ`: both lie in
the closed convex cone at `Oᵢ` of opening `wᵢ`.

They are not collinear: in any collinear arrangement one of the three lies between the other two,
and the angle it subtends is `180° > 60°`.

So they form a nondegenerate triangle, whose angle at `Oᵢ` is `∠Oⱼ Oᵢ O_k ≤ wᵢ < 60°`. The three
angles sum to `180°`, but each is `< 60°`, so the sum is `< 180°`. Contradiction. ∎

**This is the convex lane's Theorem C(a) with the hypothesis it actually needs.** The brief warned
that the convex counting argument "does not transfer", because it consumes `K ⊆ O + T(O)`. Correct —
but the transfer *does* survive if one replaces "the tangent cone at `O` has opening `< 60°`" by
"`J` lies in a cone of opening `< 60°` at `O`", which for a convex body are the same statement
(`convex-vertex-criterion` F1) and for a general polygon are not. So Theorem 2 is exactly the part
of the convex count that is free, and §7 shows it is not the whole story.

**Sharpness.** The `30`–`30`–`120` triangle of [`../../RULES.md`](../../RULES.md) §3.1 has two
wedge-type points, its two `30°` apexes (the whole triangle lies in the `30°` cone at each), and
they are its only exceptional points. So the bound `2` in Theorem 2 is attained.

---

## 7. Theorem 3 — an exceptional polygon vertex that is not wedge-type

This is the lane's main finding and it kills the obvious route to `|E(P)| ≤ 2`.

### 7.1 The construction

Let `ω` be rotation about `O = 0` by the angle `w` with

```
cos w = 4/5,   sin w = 3/5,          so   w = arcsin(3/5) = 36.8698...°,
```

a **rational** rotation: `ω(x,y) = ((4x − 3y)/5, (3x + 4y)/5)`. Two facts, both exact:
`0 < w` since `sin w > 0` and `cos w > 0`; and `w < 60°` since `tan w = 3/4` and
`(3/4)² = 9/16 < 3 = (tan 60°)²`.

Define the **inner chain** `A` by

```
a₁ = (1, 0),        a_{k+1} = 2·ω(a_k)  for k = 1,…,6,        a₈ = 2·a₇,
A  = [O, a₁] ∪ [a₁, a₂] ∪ … ∪ [a₇, a₈],
```

the **outer chain** `B = ω(A)`, with `b_k = ω(a_k)`, and

```
J = A ∪ B ∪ [a₈, b₈].
```

As a polygon this is the 17-gon with vertex list `O, a₁, …, a₈, b₈, b₇, …, b₁`. Exact coordinates
(denominators are powers of `5`):

| k | `a_k` | `b_k = ω(a_k)` |
|---|---|---|
| 1 | `(1, 0)` | `(4/5, 3/5)` |
| 2 | `(8/5, 6/5)` | `(14/25, 48/25)` |
| 3 | `(28/25, 96/25)` | `(−176/125, 468/125)` |
| 4 | `(−352/125, 936/125)` | `(−4216/625, 2688/625)` |
| 5 | `(−8432/625, 5376/625)` | `(−49856/3125, −3792/3125)` |
| 6 | `(−99712/3125, −7584/3125)` | `(−376096/15625, −329472/15625)` |
| 7 | `(−752192/15625, −658944/15625)` | `(−1031936/78125, −4892352/78125)` |
| 8 | `(−1504384/15625, −1317888/15625)` | `(−2063872/78125, −9784704/78125)` |

`|a_k| = 2^{k−1}` for `k ≤ 7` and `|a₈| = 2⁷`; `arg a_k = (k−1)w` for `k ≤ 7` and `arg a₈ = 6w`.

Picture: a **polygonal spiral channel** of constant angular width `w`, pinching to a point at `O`,
winding `6w = 221.2°` outward, and closed off by the chord `[a₈, b₈]`.

### 7.2 Theorem 3, with proof

> **Theorem 3.** `J` above is a simple polygon; `O = (0,0)` is an **exceptional** point of `J`; and
> `J` is contained in **no** cone of opening `< 60°` with apex `O`, so `O` is not wedge-type.

**regularity budget: polygonal, and nothing else.** The proof uses no topology whatsoever — no
Jordan curve theorem, no Lemma 3, no Lemma 4, no measure. Lemma 1 is a statement about point sets,
and everything below is elementary plane geometry over `Q`.

*Proof.*

**(i) `A` is radially monotone**: `|z|` is strictly increasing along `A`, from `0` at `O` to `2⁷` at
`a₈`. On `[O,a₁]` and on `[a₇,a₈]` this is clear (both are radial). On `[a_k, a_{k+1}]` for
`1 ≤ k ≤ 6`, parametrise `p(t) = a_k + t(a_{k+1} − a_k)`, `t ∈ [0,1]`; then
`½ d|p|²/dt = ⟨a_k, a_{k+1} − a_k⟩ + t|a_{k+1} − a_k|²`, and

```
⟨a_k, a_{k+1}⟩ = ⟨a_k, 2ω a_k⟩ = 2 cos(w) |a_k|² = (8/5)|a_k|²   ⟹   ⟨a_k, a_{k+1} − a_k⟩ = (3/5)|a_k|² > 0,
```

so the derivative is `> 0` throughout `[0,1]`. Hence `A` meets each circle `|z| = r`,
`0 < r ≤ 2⁷`, in exactly one point `A(r)`, depending continuously on `r`. Let `α(r)` be a
continuous lift of `arg A(r)`, with `α(r) = 0` on `(0,1]`; extend by `α(r) = 6w` for `r ≥ 2⁷`.
`α` is continuous on `(0,∞)` and `α ≡ 6w` on `[2⁶, ∞)`, since `[a₇,a₈]` is radial.

**(ii) `B` meets each such circle exactly once, at argument `α(r) + w`**, because `B = ω(A)` and
`ω` is a rotation about `O`, which changes no modulus.

**(iii) the cap lies in the channel.** `a₈` and `b₈` both have modulus `2⁷` and arguments `6w` and
`7w`. Every point of the segment `[a₈,b₈]` therefore has argument in `[6w, 7w]` (it is a convex
combination of two vectors spanning a cone of opening `w < 180°`), and modulus at least
`2⁷ cos(w/2)`, where `cos²(w/2) = (1+cos w)/2 = 9/10`. So its modulus² is at least
`(9/10)·2^14 > 2^12 = (2⁶)²`, i.e. its modulus exceeds `2⁶`, where `α ≡ 6w`. Hence every cap point
of modulus `r` has argument in `[6w, 7w] = [α(r), α(r) + w]`.

**(iv) conclusion.** By (i)–(iii), for every `r > 0`

```
Θ(r) = { θ : r e^{iθ} ∈ J }  ⊆  [ α(r), α(r) + w ]   (mod 360°),
```

an arc of length `w < 60°` — empty for `r > 2⁷`, and for `0 < r ≤ 2⁷` consisting of the two points
`α(r), α(r)+w` plus (for `r > 2⁷cos(w/2)`) at most two cap points inside that arc. Two elements of a
closed arc of length `w < 60° < 180°` differ, as residues mod `360°`, by at most `w` in absolute
value, hence never by exactly `±60°`. By Lemma 1, **`O` is exceptional**.

**(v) simplicity.** `A ∩ B = {O}`: at modulus `r ∈ (0, 2⁷]` the unique point of `A` has argument
`α(r)` and the unique point of `B` has argument `α(r) + w`, and these coincide mod `360°` only if
`w ≡ 0`, false. The cap meets `A` only at `a₈`: cap points of modulus `r > 2⁶` would have to have
argument `α(r) = 6w`, and the argument is strictly monotone along the chord `[a₈,b₈]` (which does
not pass through `O`), attaining `6w` only at `a₈`. Symmetrically the cap meets `B` only at `b₈`.
Together with the fact that consecutive edges meet exactly at their shared vertex, `J` is simple.
(Independently confirmed by the committed exact `is_simple`.)

**(vi) not wedge-type.** `a₁ = (1,0)` and `a₃ = (28/25, 96/25)` both lie on `J`. With
`c = ⟨a₁,a₃⟩ = 28/25 > 0` and `s = a₁ × a₃ = 96/25`, the unsigned angle `∠a₁ O a₃` exceeds `60°`
because `s² − 3c² = (9216 − 2352)/625 = 6864/625 > 0` (i.e. `tan ∠ = |s|/c = 24/7 > √3`). Any closed
convex cone with apex `O` containing `J` contains both directions, hence has opening at least
`∠a₁ O a₃ > 60°`. ∎

The direction set is in fact far bigger than that pair needs: `D(O)` contains `arg a_k = (k−1)w` for
`k = 1..7` and `arg b_k = kw`, i.e. it spans `[0°, 7w] = [0°, 258.09°]`.

### 7.3 Independent exact confirmation

Two exact deciders, sharing no code, were run on this polygon (§10, §12):

- the **committed** decider `experiments/inscribed-triangle-polygons/geom.py` (read and run, not
  modified), which works in `Q(√3)` with a segment-intersection routine, and
- a **second decider written from scratch for this lane**, with its own `Q(√3)` arithmetic and a
  different method: Cramer's rule on the linear system `ρ_σ(A + t(B−A)) = C + u(D−C)` per ordered
  edge pair, with the parallel/collinear cases handled separately.

Both report: the polygon is simple, and **exactly one of its 17 vertices is exceptional — vertex 0,
i.e. `O`.** Every other vertex is good and every reported witness passes an independent
`verify_triangle` re-check (three points on `J`, pairwise distinct, pairwise equidistant, exactly).
The interior angles found are `36.8699°` at `O` (`= w`, as constructed) and `≥ 71.57°` everywhere
else, consistent with Theorem 1.

The exact rational hypotheses of the proof — `⟨a_k, a_{k+1} − a_k⟩ = (3/5)|a_k|² > 0` at each `k`,
`a₈ = 2a₇`, `(9/10)|a₈|² > |a₇|²`, and `s² − 3c² > 0` for the pair `(a₁,a₃)` — were also checked
term by term in exact `Q`. **No floating-point comparison decides anything**; floats appear only in
the printed angle column.

### 7.4 What this refutes

> **`refuted`:** *"Every exceptional point of a simple polygon is wedge-type."*

That sentence appears — flagged `sketch`, and honestly labelled "stated as motivation rather than
used" — in [`../spiral-tip-witness/README.md`](../spiral-tip-witness/README.md) §9.3, where it is
the reason that lane declares the polygon control inapplicable to itself. Its supporting reasoning
is that the rotating-wedge mechanism "needs `I_r` to rotate through unboundedly many turns as
`r → 0`, which requires infinitely many direction changes in every neighbourhood". **That is the
step that is wrong.** Lemma 2 of that lane requires only that the arc `I_r` have length `< 60°` at
each radius; it does not require the arc to rotate at all, let alone infinitely often. A *finite*
rotation is plenty, and a polygon supplies it: the channel above rotates `I_r` through `221°` in
finitely many straight edges and then simply stops, terminating at `O` in an ordinary polygonal
wedge of angle `w`.

The log-spiral of that lane needs infinite winding for a different reason, which is worth separating
out: its two arms are *curves*, of zero width, so the region between them can only close up into a
Jordan curve by spiralling (that lane's §4.1, and it is right about that). Here the region *is* the
channel and the two arms are its two walls, so nothing has to accumulate. **Consequently the
rotating-wedge mechanism is not invisible to polygons, the polygon control does apply to it, and it
has now been run.** I cannot edit that file; this is a correction request for whoever owns it.

It also settles, in the negative, the polygonal case of the classification question that lane opens
in §12.3.

### 7.5 Two further things the witness kills

- **Exceptional points need not be extreme points of the convex hull.** `O = (0,0)` is in the
  *interior* of `conv(J)` here: the directions from `O` to points of `J` span `258° > 180°`, so no
  closed half-plane with `O` on its boundary contains `J`, i.e. no line supports `conv(J)` at `O`. Any
  proposed proof of `|E(P)| ≤ 2` that begins "an exceptional point is a hull vertex" is dead on this
  witness.
- **"Small interior angle" is neither necessary nor sufficient, in both directions at once.** The
  committed battery already had the sufficiency half: `ncv-cstrip` has good vertices down to
  `0.286°`. This witness supplies a sharp exceptional vertex whose polygon is nevertheless spread
  over `258°` of directions — so the governing quantity really is, as that experiment's README says,
  the angular spread at each radius, and not the interior angle.

---

## 8. `|E(P)| ≤ 2`: **not closed**, and exactly where it dies

I did not prove it. Honest statement of the position, and of every route I tried.

**8.1 What is proved.** `E(P)` is finite and contained in the vertices of interior angle `< 60°`
(Theorem 1); at most two of its elements are wedge-type (Theorem 2). If it were true that every
exceptional vertex of a polygon is wedge-type, `|E(P)| ≤ 2` would follow immediately from Theorem 2.
**Theorem 3 says it is not true**, so this route is closed off, and it is closed off by an explicit
polygon rather than by a failure of nerve.

**8.2 The angle-sum route dies at exactly one point.** Theorem 2 needs, at `Oᵢ`, that *the other two
exceptional points* subtend at most `wᵢ < 60°` there. For a wedge-type point that is free, because
all of `J` is inside the cone. For a non-wedge exceptional point it is false in general: the witness
of §7 has points of `J` subtending `258°` at `O`. And nothing weaker suffices — the angle-sum
argument consumes exactly the bound `∠OⱼOᵢO_k < 60°`, with no slack.

Could one instead bound `∠Oⱼ Oᵢ O_k` using only exceptionality? Lemma 1 gives, at an exceptional
`Oᵢ`, a constraint on each circle **separately**: `Oⱼ` and `O_k` lie at radii `|OᵢOⱼ|` and
`|OᵢO_k|`, which are different circles unless the triangle is isosceles at `Oᵢ`. So the criterion
says *nothing at all* about the angle they subtend, and the whole engine of the convex count is
unavailable. This is the sharpest way I can state where the count dies. (It also shows why the
equilateral case with three *exceptional* points is not immediately absurd: three points pairwise
equidistant would be on a common circle from each other's viewpoint, and then the criterion *would*
bite — but nothing forces the three to be equidistant.)

**8.3 The measure route provably cannot reach 3.** `half-density`'s Lemma H′ gives, at an
exceptional `O`, `λ(Ω̄ ∩ B̄(O,R)) < ½λ(B(O,R))` for every `R`; I re-derived the one-line version
(`Ω̄ ∩ ρ(Ω̄)` null ⟹ two disjoint congruent sets in the ball ⟹ each at most half) and it is correct.
It cannot be pushed to three exceptional points, and the obstruction is structural, not technical:
for three exceptional points `O₁,O₂,O₃` one gets `λ(Ω̄ ∩ ρᵢ(Ω̄)) = 0` for each `i`, but
`ρᵢ(Ω̄) ∩ ρⱼ(Ω̄)` for `i ≠ j` is completely unconstrained, so there is no packing inequality to
violate. The same obstruction in its cleanest form: rotation by `60°` partitions the circle of
directions into `6`-cycles, a maximum independent set in `C₆` has size `3`, so the density bound is
exactly `½` and no measure argument of this shape can do better — for any rotation angle, since the
proof never uses the angle. `half-density` §3.3 says this too, and I agree with it after
re-deriving it.

**8.4 What I did instead, and what it is worth.** An exact search (§10) over **6 026** simple
polygons — 3 218 seeded star-shaped random polygons with rational affine squashing, and 2 808 thin
multi-armed "star" polygons built specifically to carry several simultaneous sharp tips — found
**no polygon with three exceptional vertices**; the maximum was
`2`, attained constantly. This is `numerical` evidence and is not a proof step
([`../../RULES.md`](../../RULES.md) §3.3: a claim that survives the polygon control is *merely not
yet dead*). It is consistent with the provisional Meyerson bound, which per
[`../../README.md`](../../README.md)'s provenance warning I may not use as a premise and did not.

**8.5 Routes I considered and rejected, with reasons, so they are not re-derived as insights.**

- *"Three exceptional points, apply Theorem 2"* — circular unless they are wedge-type; §7 kills it.
- *"An exceptional point is a hull vertex; use the hull's angle sum"* — false, §7.5.
- *"Use the group generated by the three rotations"* — `ρ₁ ∘ ρ₂^{-1}` is a **translation** by
  `(e^{iπ/3} − 1)(O₂ − O₁)`, a vector of length exactly `|O₁O₂|`. That is a pretty identity and I
  could get nothing from it: the hypotheses constrain `Ω̄` against `ρᵢ(Ω̄)`, not against translates.
- *"Interior angles of a polygon sum to `(n−2)·180°`"* — allows arbitrarily many sub-`60°` vertices
  once reflex vertices are present, so it bounds nothing.
- *"Exterior angles sum to `360°`, so at most two exceed `120°`"* — true for **convex** polygons only
  (that is the convex lane's Theorem C(a) again, and the committed battery's C-argument for convex
  polygons), and reflex vertices contribute negatively in general.

**8.6 The precise open statement this lane bequeaths.**

> *(open, to my knowledge; the polygonal case of a question that is presumably answered in
> Meyerson (1980), which this project has not been able to read.)*
> Let `P` be a simple polygon and let `O₁, O₂, O₃` be three exceptional vertices. Derive a
> contradiction using only: `Ω̄` compact and connected with `Oᵢ ∈ ∂Ω̄`; `Ω̄ ∩ ρ_{Oᵢ,60°}(Ω̄) = {Oᵢ}`
> for each `i`; and `γ(Oᵢ) < 60°`.

Anyone attacking it should note that the three hypotheses are *individually* satisfiable in
abundance (§7 and §10), so the contradiction must be genuinely joint.

---

## 9. Proposition 5 — the "no sweep" constraint, and why multi-tip constructions fail

The witness works because the two walls of the channel keep a **constant** angular separation `w` at
every radius. That is not decorative; it is forced.

> **Proposition 5 (no sweep).** Let `O` be exceptional for `S`, let `I ⊆ (0,∞)` be an interval, and
> let `α, β : I → R` be continuous with `O + r e^{iα(r)} ∈ S` and `O + r e^{iβ(r)} ∈ S` for all
> `r ∈ I`. Then `δ = β − α` takes no value in `{±60° + 360°Z}`, and hence — `I` being an interval
> and `δ` continuous — `δ(I)` lies entirely inside a single one of the intervals
> `(−60°, 60°), (60°, 300°), (300°, 420°), …` between consecutive forbidden values.

**regularity budget: none** beyond the stated continuity of the two branches.

*Proof.* If `δ(r) ≡ ±60° (mod 360°)` for some `r ∈ I`, Lemma 1 makes `O` good. `δ` is continuous on
an interval, so `δ(I)` is an interval avoiding the closed discrete set `{±60° + 360°Z}`, hence lies
in one component of its complement. ∎

**What it explains.** Two continuous radial branches of `J` about an exceptional point may not
*sweep past* `60°` of separation: they are trapped between consecutive forbidden values for as long
as both are defined. The §7 channel keeps `δ ≡ w ∈ (0°,60°)` for every radius, which is the
extreme case of "trapped". Conversely any configuration in which two branches start nearly aligned
and end nearly perpendicular is good, automatically.

**A worked case: the tuning fork.** Take the simple polygon
`(0,0), (1,−400), (2,−400), (3,0), (4,−402), (−1,−402)` — two thin parallel prongs of length `400`,
tips at `(0,0)` and `(3,0)` with interior angle `0.2858°` each. Both deciders report **both tips
good**, with verified witnesses. The mechanism is Proposition 5 read backwards: at the tip `O =
(0,0)`, one branch is the tip's own inner edge `[(0,0),(1,−400)]`, which is radial from `O`, so
`α ≡ −89.86°` is constant; the other is the near wall `[(2,−400),(3,0)]` of the second prong, whose
direction from `O` runs from about `0°` (near `(3,0)`) to about `−89.7°` (near `(2,−400)`) as the
radius grows. Their separation `δ` therefore sweeps across most of `(0°, 90°)` and cannot avoid
`60°`. That is exactly why "several thin parallel prongs" — the most obvious way to try to
manufacture three simultaneous exceptional tips — cannot work, and it matches the committed
battery's `ncv-cstrip` family, whose taper tips are good down to `0.286°`.

Proposition 5 is a necessary condition, not a classification, and I want to be clear that it does
**not** yield `|E(P)| ≤ 2`: it constrains pairs of branches around **one** point and says nothing
about two different exceptional points.

---

## 10. Numerics — `numerical`, evidence only, never a proof step

Everything is exact (`Q` or `Q(√3)`); floats appear only in printed angle columns. Scripts are in
§12, runnable as given. Total wall clock about 6 minutes, far inside the one-hour budget
(`RULES.md` §6.6). No `sympy` predicate decides anything (kill-criterion K7): the committed
experiment's own README documents that `sympy.geometry` gave three **false positives** on this very
problem's tightest fixtures.

1. **Validation gate first (K1).** Before anything else: the three controls, decided by the
   committed decider. Equilateral triangle — all three vertices good; `30`–`30`–`120` — both `30°`
   apexes exceptional, `120°` vertex good; unit square — all four good. Matches Lemma 1's
   predictions and the committed battery.

2. **The §7 witness.** Simple; exactly one exceptional vertex out of 17, namely `O`; interior angle
   `36.8699°` there and `≥ 71.57°` elsewhere; all 16 good vertices have witnesses that pass
   `verify_triangle`. Reproduced identically by my independently written decider.

3. **Polygon control on Theorem 1** — the reduction is the claim most worth attacking numerically,
   because it is the one I would most like to be true. Over **746** seeded random simple polygons:
   **4 043** vertices of interior angle `≥ 60°`, all **good**, `0` violations; **16 749** sampled
   non-vertex boundary points (three rational parameters per edge), all **good**, `0` violations.

4. **Hunt for three exceptional points (K5).** Seeded, deterministic.
   - *Star-shaped random polygons*, `5`–`12` vertices, half of them squashed by a rational
     affine map to manufacture near-degenerate angles: **3 218** simple polygons.
     Distribution of `|E(P)|`: `0` — 571, `1` — 849, `2` — 1 798, `≥3` — **0**.
   - *Thin multi-armed polygons* (`k = 3,4,5` far tips interleaved with `k` notch points near the
     origin — built specifically so that several sharp tips coexist): **2 808** simple polygons.
     Distribution: `0` — 31, `1` — 370, `2` — 2 407, `≥3` — **0**.
   - Maximum over all 6 026 polygons: **2**. (The 746 polygons of item 3 were used for the
     reduction control and were not scanned for exceptional counts, so they are not included here.)

   Search over vertices only is legitimate here *because of Theorem 1* — but note the circularity
   risk and that item 3 exists to break it: the non-vertex points were tested directly, not assumed.

**What would make this wrong.** The generators are mine, they draw small integer coordinates in a
bounded box, and the "thin multi-armed" family is my own idea of what a three-tip polygon would look
like. A polygon carrying three exceptional vertices — if one exists — would very plausibly be a
*deliberate* construction like §7's rather than anything a random generator emits, and §7 itself is
proof that the interesting polygons here are constructed, not sampled. The search is therefore weak
evidence and I am not treating it as more.

---

## 11. The three cheap filters ([`../../RULES.md`](../../RULES.md) §3), all run

### 11.1 Wedge test (§3.1) — run, and it is half of this lane's subject

The test says: `J` inside a cone of opening `< 60°` at `O` ⟹ `O` exceptional. I use it twice, in
opposite directions. **As a tool:** Theorem 2 is the sharp count of how many points can pass it —
at most two, by the angle-sum argument, which is the §3.1 witness's own mechanism made quantitative.
**As a target:** Theorem 3 exhibits a polygon vertex that *fails* the test (its curve spans `258°`)
and is exceptional anyway, so the test is sufficient and **not necessary**, even for polygons. That
is precisely §3.1's own warning ("do not over-read it") discharged with a witness rather than
restated. Consistency check: the §3.1 witness itself, the `30`–`30`–`120` triangle, has both `30°`
apexes wedge-type and exceptional, and both deciders reproduce that exactly.

### 11.2 Square test (§3.2) — run; the argument does not transfer, and I can say where

Replace `60°` by `90°` throughout. What happens to each ingredient:

- **Lemma 1 does not survive.** Its content is that an isosceles triangle with apex `60°` *is*
  equilateral, so the third vertex is free. For a square, two points at equal radius subtending
  `90°` at `O` give three corners `S, O, Pt` of a square; the fourth, `Pt + S − O`, is *determined*
  and under no constraint to lie on `J`. There is no square analogue of the iff, so the criterion —
  the object every statement in this file is phrased in — simply does not exist at `90°`.
- **Lemmas 3 and 4 do survive verbatim** (Lemma 3 is proved above for *any* rotation angle), and
  Theorem 1's proof then yields: *every boundary point of a simple polygon with interior angle
  `≥ 90°` carries `p, q ∈ J` with `|Op| = |Oq| > 0` and `∠pOq = 90°`.* True, easy, and **not** the
  square peg problem — it is an inscribed isosceles right triangle.
- **Theorem 2 transfers in weakened form** (four points with cone opening `< 90°` would be in convex
  position with interior angles summing to `360°`, each `< 90°`), giving "at most three", and it is
  equally powerless for the same reason.

The decisive evidence that nothing here proves too much: the analogue of Theorem 1's conclusion is
**flatly false** for squares. Theorem 1 says all but finitely many boundary points of a polygon are
triangle vertices; for squares the corresponding set is *tiny*. A triangle admits only finitely many
inscribed squares (each has, by pigeonhole, two corners on one side of the triangle, and the
resulting configurations are rigid), so only finitely many of its uncountably many boundary points
are corners of one. `convex-vertex-criterion` §5 item 5 records the numerical version: for the
equilateral triangle, of 399 sampled points along one side, **zero** admitted an inscribed square
with a corner there. I have not verified the exact count of inscribed squares in a triangle and do
not rely on it; the qualitative gap — finitely many points versus all but finitely many — is what
the filter needs. **Pass.**

### 11.3 Polygon control (§3.3) — run, and it is this lane's home ground

Every claim here is a claim *about polygons*, so unlike `spiral-tip-witness` §9.3 the control is
directly applicable and was run in full: §10 items 1–4, using the committed exact decider plus a
second decider written from scratch. Theorem 1 survived 4 043 + 16 749 direct tests; Theorem 3's
witness was confirmed by both deciders; the `≤ 2` conjecture survived 6 026 polygons. Per §3.3 that
makes the surviving claims **merely not yet dead** — polygons are the most regular curves there are,
so this says nothing whatever about the general Jordan case, and Theorem 1 in particular is *known*
to be a statement whose general analogue fails (the §3.1 witness is a polygon with exceptional
points, and `spiral-tip-witness` exhibits a non-polygonal curve whose exceptional point has no
sector at all). The one place the control did real work in the other direction: it is what confirmed
that the §7 construction is not merely plausible but decided, twice, exactly.

---

## 12. Reproducing everything

Exact throughout; standard library only, except that the first block imports the **committed**
`experiments/inscribed-triangle-polygons/` modules, which this lane **reads and runs but never
modifies** (they are another lane's files, `RULES.md` §2). Python 3.11.15; the committed decider
has no external dependency; `sympy` is not used anywhere in this lane.

### 12.1 The witness, decided by the committed decider

```python
import sys
from fractions import Fraction as F
sys.path.insert(0, "experiments/inscribed-triangle-polygons")   # committed; read-only
from geom import P, decide_good, is_simple, vertex_angle_class

def rot_w(p):                       # rotation by w, cos w = 4/5, sin w = 3/5
    x, y = p
    return (F(4,5)*x - F(3,5)*y, F(3,5)*x + F(4,5)*y)

N = 7
A = [(F(1), F(0))]
for _ in range(N-1):
    q = rot_w(A[-1]); A.append((2*q[0], 2*q[1]))
A.append((2*A[-1][0], 2*A[-1][1]))          # final radial segment
B = [rot_w(a) for a in A]
verts = [(F(0), F(0))] + A + list(reversed(B))
poly = [P(x, y) for x, y in verts]

print("simple:", is_simple(poly))
for i, v in enumerate(poly):
    a = vertex_angle_class(poly, i); r = decide_good(poly, v)
    print(i, "%9.5f" % a["degrees_display"], r["good"], r["verified_ok"])
```

Expected: `simple: (True, 'simple')`; vertex `0` at `36.86990°` with `good = False`; all sixteen
others `good = True` with `verified_ok = True`.

### 12.2 The exact rational checks behind the hand proof

```python
def n2(p): return p[0]*p[0] + p[1]*p[1]
for k in range(0, len(A)-1):                       # radial monotonicity of A
    a, b = A[k], A[k+1]
    assert n2(b) > n2(a)
    assert a[0]*(b[0]-a[0]) + a[1]*(b[1]-a[1]) >= 0          # = (3/5)|a|^2 for the spiral steps
assert A[-1] == (2*A[-2][0], 2*A[-2][1])                     # last segment radial
assert F(9,10)*n2(A[-1]) >= n2(A[-2])                        # cap stays outside radius |a_7|
c = A[0][0]*A[2][0] + A[0][1]*A[2][1]; s = A[0][0]*A[2][1] - A[0][1]*A[2][0]
assert c > 0 and s*s - 3*c*c > 0                             # angle(a1, a3) > 60 degrees
```

All of these assertions pass. They are the hypotheses of Theorem 3 (i), (iii) and (vi), verified in
exact `Q` rather than trusted.

### 12.3 The second, independent decider

Written from scratch for this lane: its own `Q(√3)` as pairs of `Fraction`s with a syntactic zero
test (`a + b√3 = 0 ⟺ a = b = 0`) and a sign test comparing `a²` with `3b²`; and a different
decision method — for each ordered pair of edges it solves
`ρ_σ(A + t(B−A)) = C + u(D−C)` by Cramer's rule and tests `t, u ∈ [0,1]`, with the
parallel-and-collinear case handled by intersecting parameter intervals. It shares no code with
`geom.py`. It reproduces the three controls, the §7 witness (one exceptional vertex, vertex `0`) and
the §9 tuning fork (both tips good). Full source is in the journal,
[`../../../../notebook/claude/2026-08-29-iet-exceptional.md`](../../../../notebook/claude/2026-08-29-iet-exceptional.md).

**Two deciders agreeing is decorrelation, not verification.** The brief notes that four separate
checkers failed in this session against zero mathematical errors of that kind, so the adjudication
rule I used is: where code and hand argument could disagree, the hand argument in §7.2 is exact,
rational, and does not depend on either decider. They agree with it. If they had not, §7.2 is what
I would have trusted, after re-deriving it once more.

### 12.4 The hunts

Seeded (`20260829` and `31415`), deterministic, checkpointed to JSON; each ran under two minutes.
Generators: (a) `n` random integer points in `[−60,60]²` sorted by angle about the origin — always a
star-shaped, hence simple, polygon — optionally squashed by `(x,y) ↦ (x, y/k)` for `k ∈ {3,8,20,60}`;
(b) `k` random tips in `[−200,200]²` interleaved by angle with `k` random notch points in `[−6,6]²`.
Both filtered by the committed exact `is_simple`. Source in the journal.

---

## 13. What is **not** proved here, and where to attack

- **`|E(P)| ≤ 2` is not proved**, for polygons or anything else. §8 is the honest account. The
  single most useful next result would be an answer to §8.6.
- **Nothing about non-polygonal Jordan curves.** Theorem 1 consumes Lemma 2, which is exactly the
  statement that fails in general (`rotation-continuity` §8 could not certify a sector at a single
  point of a general Jordan domain; `spiral-tip-witness` §4.3 exhibits a Jordan domain with **no**
  sector of positive aperture at its exceptional point). Theorem 2 and Proposition 5 do hold for
  arbitrary sets, and are the only statements here that do.
- **No claim of novelty.** [`../../README.md`](../../README.md) reports, at provisional provenance
  P2 with no source text read, that Meyerson (1980) settles `|E(J)| ≤ 2` for every Jordan curve, and
  that the proof proceeds through a polygonal stage. If that is right, Theorem 1 is a fragment of
  that stage and Theorem 3 is presumably folklore to anyone who has read the paper. It is recorded
  here because this project cannot read the paper and because a polygon that a reader can check by
  hand is worth having either way.
- **No status above `sketch`.** `verified:review` requires a different model family
  (`RULES.md` §5); I cannot grant it to myself and have not. Nothing here belongs in `results/`.
- **No Lean.** Theorem 2 and Lemma 1 are plausible targets (angle sums and the law of cosines,
  with the relevant Mathlib API present per [`../../RULES.md`](../../RULES.md) §6.3); Theorem 3
  would need an exact `Q`-arithmetic development plus the argument-monotonicity step of (v);
  Lemmas 3 and 4 rest on the Jordan curve theorem and are therefore **not** Lean targets, which
  §6.3 of that file explains is a genuine Mathlib gap and not mere slowness.

## 14. For a cross-examiner: where to attack, in order

1. **Lemma 3, Step 0 and Step 1.** Everything topological funnels through them. Specifically:
   is `∂Ω̄ = J` (I use `∂(R²\E) = ∂E = J`)? Is `Ω \ ρ(Ω̄)` really open? Does "unbounded connected set
   disjoint from `ρ(J)`" really force containment in `ρ(E)`? **[ATTACK HERE]**
2. **Theorem 3 (iv), the quantifier order.** The arc `[α(r), α(r)+w]` depends on `r`. The claim is
   `∀r`, not `∃` an arc working for all `r`. If that were confused, the theorem would be the trivial
   wedge test and the witness would prove nothing. **[ATTACK HERE]**
3. **Theorem 3 (i).** The derivative computation `⟨a_k, a_{k+1} − a_k⟩ = (3/5)|a_k|²` is the single
   line that makes the chain radially monotone, and radial monotonicity is what makes `Θ(r)` a
   two-point set. Redo it.
4. **Theorem 3 (iii).** `cos²(w/2) = 9/10` and the inequality `(9/10)·2^14 > 2^12`. If the cap
   dipped below radius `2⁶` the argument in (iv) would break, since `α` is only constant above `2⁶`.
5. **Lemma 2.** "Exactly one of the two sectors lies in `Ω`" — check that both the "not both in `Ω`"
   and "not both in `E`" halves are actually argued (they are, via `O ∈ ∂Ω ∩ ∂E`).
6. **Theorem 2.** The collinearity exclusion. Short, and geometric by hand.
7. **§8's negative claims** are claims too. In particular 8.3's assertion that no measure argument
   can reach three: I believe it, and it is the kind of "I could not do it" that can quietly become
   "it cannot be done".
