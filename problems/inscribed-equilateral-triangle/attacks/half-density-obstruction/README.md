# Attack: the half-density obstruction — the core is true, cheap, and smaller than advertised

**regularity budget, stated twice because the two halves of this lane are very different:**

```
core measure lemma (§3)  regularity budget: none
        Lemma H is a statement about an arbitrary measurable set and an arbitrary isometry
        fixing a point. No curve, no topology, no continuity, no Jordan hypothesis appears in
        it. Drop measurability and the statement is not false, it is meaningless.

full chain (§4-§5)       regularity budget: Jordan
        Lemma A consumes the Jordan curve theorem twice (exactly two complementary components;
        J is the boundary of each) plus boundedness of the interior and isometry-invariance of
        Lebesgue measure. Nothing else: no rectifiability, no tangent, no local connectivity
        beyond what JCT gives, no smoothness. What breaks first if you drop "Jordan": a general
        planar continuum has neither of the two facts Lemma A uses, and every criterion in §5
        collapses with it. Weakening "Jordan" is not a small step here; it is the whole step.
```

- Lane: idea **I1** of [`../ideation-round-1/README.md`](../ideation-round-1/README.md), the
  top-ranked entry of that round.
- Author: `claude` (Claude Opus 5), 2026-08-29, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Kill-criterion: [`KILL-CRITERION.md`](./KILL-CRITERION.md), written **before** any computation
  in this lane, with three pre-registered predictions and a fixed verdict rule. Read its
  provenance note: it was not written before the *algebra*.
- Journal: [`../../../../notebook/claude/2026-08-29-iet-halfdensity.md`](../../../../notebook/claude/2026-08-29-iet-halfdensity.md).
- Read in full before starting: [`../rotation-continuity/README.md`](../rotation-continuity/README.md),
  [`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md),
  [`../ideation-round-1/README.md`](../ideation-round-1/README.md) §I1,
  [`../../README.md`](../../README.md), [`../../RULES.md`](../../RULES.md),
  [`../../../../RULES.md`](../../../../RULES.md) §0, §3, §7.

---

## 0. Verdict, up front

| # | Statement | Status |
|---|---|---|
| §2 | **Observation R** (rotation reduction), re-derived here | `sketch` — mine, three lines, self-contained |
| §3 | **Lemma H** (topology-free core): `U ∩ ρ(U) = ∅` ⟹ `U` has density `≤ ½` in every ball centred at `O` | `sketch` — mine. **True, and the proof is two lines, not the polar-coordinate computation I1 proposed** |
| §3.3 | **The constant is exactly `½` and cannot be improved to `1/6`** | `sketch` — mine, with the extremal set exhibited and the reason the six-fold argument fails |
| §3.4 | **Lemma H′** (strict form for closed sets, via connectedness of the punctured disc) | `sketch` — mine; a genuine sharpening of I1, and the only part of §3 with real content |
| §4 | **Lemma A**, re-derived from scratch | `sketch` — mine. **Survives.** I land in the same place as the rotation lane, by a route that differs only cosmetically |
| §5 | The criterion hierarchy, with the master statement an **iff** | `sketch` — mine |
| §5.4 | **The density criterion is *incomparable* to the sector criterion, not stronger** | `sketch` — mine. This **corrects** I1's triage line |
| §6 | **The pinwheel witness is real**, as an exact rational polygon | `numerical` (exact in `ℚ` and `ℚ(√3)`; no float decides anything) |
| §7 | The criterion is **vacuous on every convex curve** | `sketch` — mine, one line from a supporting half-plane |
| §8 | Refutation attempts: 358 exceptional vertices, 698 236 interior samples, **zero** violations | `numerical` |
| §9 | Square test, wedge test, polygon control — all three run | reported below |

**One-sentence summary.** The half-density lemma is **true**, its core has **no mathematical
content beyond "two disjoint sets of equal measure fit in the ball"**, the sharp constant is `½`
and not `1/6`, Lemma A **survives** independent re-derivation, the pinwheel witness **is real**
and exhibited exactly — and I1's claim that the criterion is *strictly stronger* than the sector
criterion is **wrong**: the two are incomparable, and the density criterion is furthermore
strictly weaker than the per-circle criterion it is a corollary of.

**Nothing here is assumable.** Everything is `sketch` by [`../../../../RULES.md`](../../../../RULES.md)
§3, including by me. §5's chain is self-contained: it rests only on the Jordan curve theorem, on
isometry-invariance of Lebesgue measure, and on arguments written out in §2–§4 of this file. It
does **not** import the rotation lane's Lemma A, which is that lane's `sketch`; I re-derived it,
which is what §3 requires and what §6.2 asks of an examiner.

---

## 1. The objects

`J ⊂ ℝ²` is a Jordan curve. By the Jordan curve theorem `ℝ² \ J` has exactly two connected
components — `Ω` bounded ("the interior") and `E` unbounded — and `∂Ω = ∂E = J`. Write
`Ω̄ = Ω ∪ J = ℝ² \ E`, a compact set.

Fix `O ∈ J`, and let `ρ = ρ_{O,60°}` be rotation by `+60°` about `O`. Primes denote `ρ`-images.
`λ` is planar Lebesgue measure, `B(O,R)` the open ball, `B̄(O,R)` the closed one.

`O` is **exceptional** when no equilateral triangle inscribed in `J` has `O` as a vertex.

For `r > 0` define the two angular sections at radius `r`,

```
A_r = { θ ∈ ℝ/360° : O + r e^{iθ} ∈ Ω  }     (open in the circle, since Ω is open)
B_r = { θ ∈ ℝ/360° : O + r e^{iθ} ∈ Ω̄ }     (closed in the circle, since Ω̄ is closed)
```

and note `ρ` acts on the section at each fixed radius as `θ ↦ θ + 60°`, because `ρ` fixes `O`
and preserves every circle centred at `O`. That single sentence is the only "geometry" anywhere
in §3.

**The Jordan curve theorem is a dependency and is not `cited` in this repo.** It is classical and
universally available, but per [`../../RULES.md`](../../RULES.md) §6.3 it is **not in Mathlib**,
so no statement below that uses it is a Lean target. §3 is deliberately quarantined from it.

---

## 2. Observation R, re-derived

> **Observation R.** For any `S ⊆ ℝ²` with `O ∈ S`: some equilateral triangle with all three
> vertices in `S` has `O` as a vertex `⟺ S ∩ ρ(S) ⊋ {O}`.

*Proof.* (⟸) Let `x ∈ S ∩ ρ(S)`, `x ≠ O`, and `p = ρ^{-1}(x) ∈ S`. `ρ` is an isometry fixing `O`,
so `|Op| = |Ox| =: r > 0`, and the angle at `O` between `p` and `x` is the rotation angle `60°`.
The triangle `Opx` is isosceles with apex angle `60°`, hence its base angles are `(180-60)/2 =
60°`, hence it is equilateral with side `r > 0`. Nondegeneracy: `r > 0` and the apex angle is
`60° ≠ 0`, so `O, p, x` are three distinct points. (⟹) If `O, P, Q ∈ S` is equilateral then `Q`
is the image of `P` under rotation about `O` by `+60°` or `−60°`; in the first case
`Q ∈ S ∩ ρ(S)\{O}`, in the second `P ∈ S ∩ ρ(S)\{O}`. ∎

**regularity budget: none.** `S` is used as a bare point set.

Applying it to `S = J`: **`O` is exceptional `⟺ J ∩ ρ(J) = {O}`.** The `⟸` half is the reference
non-transfer statement of [`../../RULES.md`](../../RULES.md) §3.2; I derived the `⟹` half above
and it is what makes the criterion an *iff* rather than a one-way test. I re-derived this rather
than importing the rotation lane's §2 because that file is `sketch` and §3 forbids leaning on it.
I landed in the same place, with the same three lines; there was nothing to disagree with.

---

## 3. Lemma H — the topology-free core

This is the object the lane exists to isolate. **It contains no topology at all**, which matters
because [`../../RULES.md`](../../RULES.md) §6.3 records that Mathlib has no Jordan curve theorem,
so everything in §4–§5 is out of Lean's reach while this is not.

### 3.1 Statement and proof

> **Lemma H.** Let `O ∈ ℝ²`, let `σ : ℝ² → ℝ²` be **any** isometry with `σ(O) = O`, and let
> `V ⊆ ℝ²` be Lebesgue measurable with `λ(V ∩ σ(V)) = 0`. Then for every `R > 0`,
> ```
> λ(V ∩ B(O,R))  ≤  ½ · λ(B(O,R)).
> ```

*Proof.* Put `W = V ∩ B(O,R)`. An isometry fixing `O` maps `B(O,R)` onto `B(O,R)`, so
`σ(W) = σ(V) ∩ B(O,R) ⊆ B(O,R)`. Isometries of `ℝ²` preserve Lebesgue measure, so
`λ(σ(W)) = λ(W)`. And `W ∩ σ(W) ⊆ V ∩ σ(V)` is null. Hence

```
2 λ(W) = λ(W) + λ(σ(W)) = λ(W ∪ σ(W)) ≤ λ(B(O,R)),
```

which is the claim. ∎

**That is the whole proof.** No polar coordinates, no inclusion–exclusion on a circle, no
measurability-for-a.e.-`r` question, no `60°`. The brief and I1 both route this through the
angular sections `A_r`; that route works, but it is a detour, and the detour is where the brief's
worries (measurability of `A_r`, the sharp constant, six-fold rotation) all live. **They are
artefacts of the detour, not of the statement.**

### 3.2 The per-circle version, which is the one worth having

The same two lines applied to the circle instead of the disc give strictly more information, and
that extra information is what §5 actually uses:

> **Lemma H₁.** With `σ, O` as above and `σ` acting on the circle of radius `r` about `O` as a
> rotation by `α`: if `A ⊆ ℝ/360°` is measurable with `A ∩ (A + α) = ∅`, then `|A| ≤ 180°`.

*Proof.* `A` and `A + α` are disjoint measurable subsets of a circle of total measure `360°`, and
translation on the circle preserves measure, so `2|A| = |A| + |A + α| ≤ 360°`. ∎

**Measurability, since the brief asked.** There is no "for a.e. `r`" anywhere. `Ω` is open, so
`A_r` is open — hence measurable — for **every** `r > 0`; `Ω̄` is closed, so `B_r` is closed for
every `r > 0`. Both are sections of a Borel set under the continuous map `(r,θ) ↦ O + re^{iθ}`, so
Borel measurability is automatic even for a merely Borel `V`. The disjointness
`B_r ∩ (B_r + 60°) = ∅` likewise holds for *every* `r`, not almost every `r`, because it is a
pointwise set statement, not an integral one. Tonelli is needed only if one wants to *integrate*
`|A_r|` (§5.3), and there the integrand is non-negative and measurable, so it applies unconditionally.

### 3.3 The constant is exactly `½`. There is no route to `1/6`.

The brief asks whether the six-fold family `A, A+60°, …, A+300°` gives `|A| ≤ 60°` instead of
`180°`. **It does not, and the obstruction is structural rather than technical.**

> **Sharpness.** `sup { |A| : A ⊆ ℝ/360° measurable, A ∩ (A + 60°) = ∅ } = 180°`, and the
> supremum is **attained**, by the open set
> ```
> A* = (0°,60°) ∪ (120°,180°) ∪ (240°,300°),      |A*| = 180°,
> A* + 60° = (60°,120°) ∪ (180°,240°) ∪ (300°,360°),   disjoint from A*.
> ```

The six-fold argument needs the six translates to be **pairwise** disjoint, and they are not:
`A* + 120° = A*` exactly. Disjointness of *consecutive* translates propagates to **no other
pair**. The clean way to see it: rotation by `60°` partitions `ℝ/360°` into orbits
`{θ, θ+60°, …, θ+300°}`, each a `6`-cycle, and the hypothesis says precisely that `A` meets each
orbit in an **independent set of the cycle graph `C₆`**. The maximum independent sets of `C₆`
have size `3` — the two alternating triples — so the bound is `3/6 = ½` and it is achieved, by a
set that is invariant under `+120°`. An independent set of size `4` in `C₆` does not exist, which
is exactly why `1/6` is unreachable.

**The deeper reason, and it is worth stating because it caps the whole method.** Lemma H's proof
never used the angle. It holds verbatim for `σ` a reflection, or a rotation by `1°`, or by `179°`.
A measure argument of this shape cannot see the *order* of the rotation, so it cannot produce a
constant better than `½` for any angle. Any improvement past `½` must come from somewhere other
than measure — and §3.4 is the only such improvement I found.

### 3.4 Lemma H′ — the strict form, which is where the content is

Everything above is bookkeeping. This is not, and it is a genuine sharpening of I1's statement:

> **Lemma H′.** Let `C ⊆ ℝ²` be **closed**, `σ` an isometry fixing `O`, and `C ∩ σ(C) ⊆ {O}`.
> Then for every `R > 0`,
> ```
> λ(C ∩ B̄(O,R))  <  ½ · λ(B(O,R))      —  strictly.
> ```

*Proof.* Let `W = C ∩ B̄(O,R)`; as in §3.1, `σ(W) = σ(C) ∩ B̄(O,R)`, `λ(σ W) = λ(W)`, and
`W ∩ σW ⊆ {O}` is null, so `2λ(W) ≤ λ(B̄(O,R)) = λ(B(O,R))`. Suppose equality held. Then
`W ∪ σW` is a **closed** subset of `B̄(O,R)` of full measure, so its complement in `B̄(O,R)` is
relatively open and null, hence empty:  `W ∪ σW = B̄(O,R)`. Deleting `O`,

```
B̄(O,R) \ {O}  =  (W \ {O})  ⊔  (σW \ {O}),
```

a partition into two **disjoint** sets (`W ∩ σW ⊆ {O}`), each **closed** in `B̄(O,R)\{O}` (each is
a closed set intersected with it), and each **nonempty** (each has measure `½λ(B) > 0`). But
`B̄(O,R)\{O}` is connected for `R > 0`. Contradiction. ∎

The circle version is the same argument one dimension down and is the one §5 uses:

> **Lemma H′₁.** If `B ⊆ ℝ/360°` is **closed** with `B ∩ (B + α) = ∅` for some `α ≠ 0`, then
> `|B| < 180°` strictly.
> *Proof.* If `|B| = 180°` then `B ⊔ (B+α)` is closed of full measure, hence all of `ℝ/360°`,
> exhibiting the circle as a disjoint union of two nonempty closed sets. The circle is connected. ∎

Note where the closedness enters: for **open** sets equality *is* attained (`A*` above), so `H′`
is genuinely a statement about `Ω̄`, not about `Ω`, and it is the reason §5's criterion can be
stated with `≥ ½` rather than `> ½`. The single ingredient beyond measure theory is connectedness
of a punctured disc — which is a topological fact, so `H′` is *not* topology-free the way `H` is.
It remains far below the Jordan curve theorem in strength.

### 3.5 The Lean target, and why this is the right one

I **could not** attempt a formalisation: `elan` is absent from this container and every route to
install it (GitHub releases, `leanprover` hosts) is blocked by the egress proxy, and there is no
vendored Mathlib under `lean/` to read. So what follows is a target specification, not a result,
and the Mathlib names in it are **unverified search targets** in the sense of
[`../../RULES.md`](../../RULES.md) §6.1 — treat every identifier as a guess.

The statement to formalise is **Lemma H in the isometry form of §3.1**, not the `60°` rotation
form and not the polar-coordinate form:

```lean
-- target shape; identifiers unverified, Mathlib not readable from this session
theorem half_density
    {n : ℕ} {O : EuclideanSpace ℝ (Fin n)} {R : ℝ} (hR : 0 < R)
    (σ : EuclideanSpace ℝ (Fin n) ≃ᵢ EuclideanSpace ℝ (Fin n)) (hO : σ O = O)
    {V : Set (EuclideanSpace ℝ (Fin n))} (hV : MeasurableSet V)
    (hdisj : volume (V ∩ σ '' V) = 0) :
    volume (V ∩ Metric.ball O R) ≤ volume (Metric.ball O R) / 2
```

Why this is the right target:

1. **It is JCT-free**, so it is not blocked by the Mathlib gap of §6.3 — unlike every other
   statement in this directory except the wedge test and the rotation identity.
2. **Its proof needs three facts, all of which Mathlib certainly has in some form**: an isometry
   fixing a point maps a ball about that point onto itself; isometries of a finite-dimensional
   real inner-product space preserve Haar/Lebesgue measure; and measure is additive on disjoint
   measurable sets. Nothing about `√3`, nothing about `60°`, nothing about angles at all.
3. **It generalises for free** — any dimension, any isometry, any angle — so the formal statement
   is *easier* than the informal one, which is the ideal situation for a first Lean target.
4. It is the **base of the chain** in the sense of [`../../../../RULES.md`](../../../../RULES.md)
   §3: every later `verified:review` use of §5 would inherit it.

The `60°` specialisation is then a corollary once someone supplies "rotation by `π/3` about `O` is
an isometry fixing `O`", which is `Geometry.Euclidean.Angle.Oriented.Rotation` territory and is
the same API the wedge-test target needs. **Lemma H′ is a harder and less attractive target** — it
needs connectedness of a punctured ball and a full-measure-closed-set argument — and I would not
start there.

**Honest caveat.** Because I could not run Lean, I do not know that this compiles, that
`EuclideanSpace ... ≃ᵢ ...` is the idiomatic spelling, or that the measure-preservation lemma
exists under a usable name. A Lean worker should re-do the §6.3 availability check rather than
trust this paragraph.

---

## 4. Lemma A, re-derived from scratch

The rotation lane proved this and marked it `sketch`; [`../../../../RULES.md`](../../../../RULES.md)
§3 forbids me from assuming it, so I derived it independently before reading their proof
carefully, then compared. **It survives.** My route differs from theirs only in the last step of
Case A (I take interiors where they take complements and boundaries); the substance is identical,
which is a weak but real signal.

> **Lemma A.** If `J ∩ ρ(J) = {O}` then `Ω̄ ∩ ρ(Ω̄) = {O}`; in particular `Ω ∩ ρ(Ω) = ∅`.

**regularity budget: Jordan.** Used: two complementary components; `J = ∂Ω = ∂E`; `Ω` bounded;
`λ` isometry-invariant; `int(Ω̄) = Ω`.

*Proof.* Write `J' = ρ(J)`, `Ω' = ρ(Ω)`, `E' = ρ(E)`; since `ρ` is a homeomorphism, `J'` is a
Jordan curve with interior `Ω'` and exterior `E'`.

**Step 1 (the dichotomy).** `J' \ {O}` is connected (a circle minus a point) and, by hypothesis,
disjoint from `J`. Since `ℝ² \ J = Ω ⊔ E` with both parts open, `J' \ {O}` lies entirely in `Ω` or
entirely in `E`.

**Step 2 (the nesting case is impossible).** Suppose `J' \ {O} ⊆ Ω`. Then `J' ⊆ Ω ∪ {O} ⊆ Ω̄`, so
`J'` misses `E`. `E` is connected and disjoint from `J'`, hence lies in one complementary
component of `J'`; being unbounded, `E ⊆ E'`. Taking complements,
`Ω̄' = ℝ² \ E' ⊆ ℝ² \ E = Ω̄`. Now `ρ` is an isometry and `ρ(Ω̄) = Ω̄'`, so
`λ(Ω̄') = λ(Ω̄) < ∞` (finite because `Ω` is bounded). A measurable subset of equal finite measure
has null complement: `λ(Ω̄ \ Ω̄') = 0`. But `Ω \ Ω̄'` is **open** (an open set minus a closed one)
and contained in that null set, so it is empty. Hence `Ω ⊆ Ω̄'`, so `Ω̄ ⊆ Ω̄'`, so `Ω̄ = Ω̄'`.

For a Jordan domain `int(Ω̄) = Ω`: `Ω ⊆ int(Ω̄)` is clear, and no `x ∈ J` is interior to `Ω̄`,
because `J = ∂E` means every neighbourhood of `x` meets `E = ℝ² \ Ω̄`. Applying this to both
domains, `Ω = int(Ω̄) = int(Ω̄') = Ω'`, hence `J = ∂Ω = ∂Ω' = J'`. That contradicts
`J ∩ J' = {O}`, since a Jordan curve has more than one point.

**Step 3 (so the configuration is external).** By Steps 1–2, `J' \ {O} ⊆ E`. Exchanging the roles
of `J` and `J'` in Steps 1–2 — the hypothesis `J ∩ J' = {O}` is symmetric — gives likewise
`J \ {O} ⊆ E'`. Now `Ω` is connected and disjoint from `J'` (as `J' ⊆ E ∪ {O}`, `Ω ∩ E = ∅`, and
`O ∈ J` so `O ∉ Ω`), hence `Ω ⊆ Ω'` or `Ω ⊆ E'`. If `Ω ⊆ Ω'` then `Ω̄ ⊆ Ω̄'`, so `J ⊆ Ω̄'`,
contradicting `J \ {O} ⊆ E'` and `E' ∩ Ω̄' = ∅` (`J \ {O} ≠ ∅`). Therefore `Ω ⊆ E'`, i.e.
`Ω ∩ Ω' = ∅`.

**Step 4 (the closed form).**
`Ω̄ ∩ Ω̄' = (Ω∩Ω') ∪ (Ω∩J') ∪ (J∩Ω') ∪ (J∩J')`. The first is empty by Step 3; the second because
`J' ⊆ E ∪ {O}` and `Ω` meets neither; the third because `J \ {O} ⊆ E'` and `O ∉ Ω'`; the fourth is
`{O}`. ∎

**Where I pushed hardest, per [`../../RULES.md`](../../RULES.md) §6.2.**

- *"JCT applied to something not shown to be a Jordan curve."* `J'` is the image of `J` under a
  homeomorphism of the plane, so it is a Jordan curve and `ρ(Ω) = Ω'` really is its interior
  (`ρ` maps components to components and preserves boundedness). This is the one place the
  argument could have smuggled something, and it does not.
- *"Obviously the curves must cross."* Nowhere. There is no parity, degree, or transversality step
  anywhere in Lemma A, which is exactly why it survives for wild curves. Compare the rotation
  lane's §6.5, which reaches the same conclusion from the other side.
- *The measure step.* It is used **once**, in Step 2, and only to upgrade `Ω̄' ⊆ Ω̄` to equality.
  It is not doing geometric work; it is replacing an inclusion by an identity. Note also what
  Lemma A does **not** give: it kills only the *nested* configuration. The *externally tangent*
  configuration is real — the `30°`-`30°`-`120°` witness realises it — so no amount of extra
  measure theory turns Lemma A into a proof that `O` is never exceptional. The rotation lane
  records the same finding at its §7.1 and I confirm it independently.
- *Limits and noncollapse.* There are none. No sequence is taken anywhere in this file; the
  triangle produced in §5 has an explicitly named positive side length. [`../../RULES.md`](../../RULES.md)
  §2's degenerate solution `O` is excluded by hand throughout, never by an estimate.

---

## 5. The criteria, and how they actually relate

### 5.1 The master criterion is an iff

Combining §2 and §4 (both directions):

> **Criterion M.** `O ∈ J` is a vertex of an inscribed equilateral triangle
> `⟺ Ω̄ ∩ ρ(Ω̄) ⊋ {O}`
> `⟺ ∃ r > 0 with B_r ∩ (B_r + 60°) ≠ ∅`.

*Proof.* `O` is a vertex `⟺ J ∩ ρJ ⊋ {O}` (§2). Forwards, `J ⊆ Ω̄` gives `Ω̄ ∩ ρΩ̄ ⊋ {O}`.
Backwards is the contrapositive of Lemma A. For the second equivalence: `x ∈ Ω̄ ∩ ρ(Ω̄)` with
`x ≠ O` means, with `r = |Ox| > 0` and `θ = arg(x - O)`, that `θ ∈ B_r` and `θ - 60° ∈ B_r`, i.e.
`θ ∈ B_r ∩ (B_r + 60°)`; and conversely. ∎

Everything else in this lane, **including the half-density lemma**, is a sufficient condition for
this iff. That is worth saying plainly: the density statement is not an independent obstruction,
it is a *packaging* of Criterion M into a quantity one can estimate.

### 5.2 The obstruction, in its sharpest form

> **Theorem (half-density, strict).** If `O` is exceptional then for **every** `r > 0`
> ```
> |B_r| < 180°        (angular measure of the closed section of Ω̄)
> ```
> and consequently for **every** `R > 0`
> ```
> λ(Ω̄ ∩ B̄(O,R))  <  ½ λ(B(O,R)),   a fortiori  λ(Ω ∩ B(O,R)) < ½ λ(B(O,R)).
> ```

*Proof.* Exceptional ⟹ `J ∩ ρJ = {O}` (§2) ⟹ `Ω̄ ∩ ρΩ̄ = {O}` (§4). Hence for each `r > 0`,
`B_r ∩ (B_r + 60°) = ∅`, and `B_r` is closed, so `|B_r| < 180°` by Lemma H′₁. The ball statement
is Lemma H′ applied to `C = Ω̄`, `σ = ρ`. ∎

This is I1's Speculative Lemma, **proved, with `≤` improved to `<` and `Ω` improved to `Ω̄`**. The
two improvements are not cosmetic: they are what let the contrapositive be stated with `≥`.

### 5.3 The contrapositives, in decreasing strength

```
(M)  ∃ r>0 : B_r ∩ (B_r + 60°) ≠ ∅              ⟺  O is a vertex        [iff]
(C)  ∃ r>0 : |B_r| ≥ 180°                       ⟹  O is a vertex        [per-circle]
(D)  ∃ R>0 : λ(Ω̄ ∩ B̄(O,R)) ≥ ½ λ(B(O,R))       ⟹  O is a vertex        [ball density; = I1's]
(S)  a closed 60° sector at O lies in Ω̄         ⟹  O is a vertex        [rotation lane, Lemma B]
```

`D ⟹ C`: if `|B_r| < 180°` for every `r ∈ (0,R]` then, by Tonelli in polar coordinates,
`λ(Ω̄ ∩ B̄(O,R)) = ∫₀^R |B_r| r dr < ∫₀^R π r dr = ½λ(B(O,R))` — the strict inequality survives the
integration because it is strict pointwise on a set of positive measure. `C ⟹ M` is immediate.

`C ⟹̸ D`: the domain
`Ω = {re^{iθ} : 0.9 < r < 1, 0° < θ < 190°} ∪ {re^{iθ} : 0 < r < 0.9, 0° < θ < 10°}`
is a Jordan domain with `O = 0` on its boundary; `|B_r| = 190° > 180°` for `r ∈ (0.9,1)`, so `C`
fires, while its density in `B(O,R)` is largest at `R = 1`, where it equals
`(190·0.19 + 10·0.81)/360 = 0.1228 < ½`, so `D` never fires. **The ball-density formulation of I1
therefore throws away information, and the per-circle form is the one to state.**

### 5.4 `S` and `C` are **incomparable** — I1's triage line is wrong

I1's triage says the density criterion is "strictly stronger than the sector criterion". It is
not.

- **`C` fires where `S` cannot.** §6's pinwheel: exact, polygonal, `S` provably silent at `O`.
- **`S` fires where `C` and `D` cannot.** Take the `30°`-`30°`-`120°` witness of
  [`../../RULES.md`](../../RULES.md) §3.1 at its `120°` vertex `C`. The curve is convex, so
  `|B_r| ≤ 120° < 180°` for every `r` and (§7) the density never reaches `½` — yet a closed `120°`
  sector sits in `Ω̄` at `C`, so `S` fires and produces a triangle. Verified exactly: the
  committed decider reports `C` good with an explicit triangle, and the density there is
  `0.1378 < ½` (§9).

So `S` and `C` are two incomparable sufficient conditions for the same iff `M`, and neither
subsumes the other. Recording this is the honest outcome; it is a correction to I1's ranking
rationale, not a kill (see [`KILL-CRITERION.md`](./KILL-CRITERION.md) §3).

---

## 6. The pinwheel witness — exact, polygonal, and real

I1 proposed a "pinwheel": a point where the density criterion fires and no `60°` sector fits.
**It is real.** Here it is as an explicit simple polygon with rational vertices, so every claim
about it is decided by exact rational arithmetic ([`../../RULES.md`](../../RULES.md) §5).

### 6.1 The polygon

Let `u₀,…,u₇` be these eight **exactly** unit vectors (small Pythagorean directions, chosen so
every coordinate below has denominator at most `50`):

```
u0 = ( 1,  0)      u1 = ( 3/5, 4/5)    u2 = ( 0,  1)      u3 = (-4/5, 3/5)
u4 = (-1,  0)      u5 = (-3/5,-4/5)    u6 = ( 0, -1)      u7 = ( 4/5,-3/5)
```

so the eight directions sit at `0°, 53.13°, 90°, 143.13°, 180°, 233.13°, 270°, 323.13°`. With
`δ = 1/5` and `ring = 9/10`, the polygon `P` is the closed walk through these 21 vertices, in
order:

```
 0  O    = (0,0)                 7  u6     = (0,-1)            14  δ·u4  = (-1/5, 0)
 1  u0   = (1,0)                 8  u7     = (4/5,-3/5)        15  r·u4  = (-9/10, 0)
 2  u1   = (3/5,4/5)             9  δ·u7   = (4/25,-3/25)      16  r·u3  = (-18/25, 27/50)
 3  u2   = (0,1)                10  δ·u6   = (0,-1/5)          17  δ·u3  = (-4/25, 3/25)
 4  u3   = (-4/5,3/5)           11  r·u6   = (0,-9/10)         18  δ·u2  = (0, 1/5)
 5  u4   = (-1,0)               12  r·u5   = (-27/50,-18/25)   19  r·u2  = (0, 9/10)
 6  u5   = (-3/5,-4/5)          13  δ·u5   = (-3/25,-4/25)     20  r·u1  = (27/50, 18/25)
```

(`r` abbreviates `ring = 9/10`.) Shape: an outer band of radii `[9/10, 1]` spanning the directions
`u₀ … u₇` (`323.13°` of arc, with the last `36.87°` left open — that gap is what keeps the region
simply connected), four **arms** of angular width `53.13°` reaching inward to radius `δ = 1/5`,
and the **first arm alone continued all the way to `O`**. Only one arm touches `O`, which is
forced: a Jordan curve passes through `O` once, so at most two boundary arcs can emanate from it
and `Ω̄` can have at most one "petal" pinched at `O`. I1's phrasing ("one touching `O`, the other
three truncated at tiny inner radii") already respects this; a version with four petals apexed at
`O` would be impossible, and it is worth saying so since the picture invites it.

### 6.2 What is certified, exactly

| Claim | Method | Result |
|---|---|---|
| `P` is a simple polygon (so `∂P` is a Jordan curve) | committed `geom.is_simple`, exact | **true**, 21 vertices |
| interior angle at `O` is `< 60°` | committed `geom.vertex_angle_class`: `s² < 3c²` with `c = u·w > 0`, exact | **`cmp60 = −1`** (`53.1301°` display) |
| `P ⊆ B̄(O,1)` | every vertex has `‖v‖² ≤ 1`, exact; `max ‖v‖² = 1` | **true**, so `R = 1` exactly |
| `area(P)` | shoelace, exact rational | **`1723/1000`** exactly |
| density `> ½` in `B(O,1)` | `1723/1000 > (π/2)·1²`, using only `3.1415 < π < 3.1416` so `(π/2) < 1.5708` | **fires**: `1.723 > 1.5708`; density `≈ 0.5484` |
| no closed `60°` sector at `O` in `Ω̄` | min squared distance from `O` to a non-incident edge is `ε² = 4/125` exactly (attained on the edge `(4/25,−3/25) → (0,−1/5)`), so `Ω̄ ∩ B(O,ε)` is exactly the `53.13°` wedge for every `ε < 4/125^{1/2} ≈ 0.1789`; a sector of larger radius contains points of that ball, so `S` fails at **every** radius | **`S` is silent** |
| `Ω ∩ ρ(Ω) ≠ ∅` (Criterion M, directly) | exact witness `x = (39/200, −84/125) ∈ Ω` with `ρ^{-1}(x) = (39/400 − (42/125)√3, −42/125 − (39/400)√3) ∈ Ω`, both by exact ray-casting in `ℚ(√3)`; `|Ox|² = |Oρ^{-1}x|² = 489609/1000000` | **certified** |
| `O` is a vertex — independent check | the repo's committed exact decider `experiments/inscribed-triangle-polygons/geom.decide_good`, **read and run, not modified** | **good = True, verified_ok = True** |

The triangle the committed decider returns at `O`:

```
O = (0, 0)
Q = ( -3/13 + (9/13)√3 ,  0 )                        ≈ (0.968343, 0)
X = ( -3/26 + (9/26)√3 ,  27/26 - (3/26)√3 )         ≈ (0.484171, 0.838610)
side² = 252/169 - (54/169)√3   ≈ 0.937688,  side ≈ 0.968343 > 0    (σ = +1)
```

`Q` lies on the edge `O → (1,0)` and `X` on the chord `(3/5,4/5) → (0,1)`; all three squared
pairwise distances are equal **exactly in `ℚ(√3)`**, and the decider's `verify_triangle` re-checks
on-curve, distinctness, equilaterality and nondegeneracy without reusing the search's reasoning.

### 6.3 What the witness establishes, and what it does not

It establishes that **`D` (hence `C`, hence `M`) fires at a point where `S` is silent**, on an
object that is a genuine Jordan curve with all data exact. That is I1's separation claim, made
good — kill-condition **K4 is not met**.

It does **not** establish that the density criterion is the reason `O` is good: `M` is an iff, so
`O` is good, full stop, and the density is merely one certificate for it. Nor does it say anything
about wild curves. A polygon is the most regular curve there is
([`../../RULES.md`](../../RULES.md) §3.3): surviving on it is *not-yet-dead*, not evidence.

---

## 7. Where the criterion is worthless: every convex curve

> **Proposition.** If `K` is a compact convex set with nonempty interior and `O ∈ ∂K`, then for
> every `R > 0`, `λ(K ∩ B(O,R)) ≤ ½λ(B(O,R))`, and `|{θ : O + re^{iθ} ∈ K}| ≤ 180°` for every `r`.
> Hence criteria `C` and `D` **never fire on a convex curve.**

*Proof.* A supporting line at `O` puts `K` inside a closed half-plane `H` through `O`. Then
`K ∩ B(O,R) ⊆ H ∩ B(O,R)`, which has measure exactly `½λ(B(O,R))`; and the directions from `O`
into `H` form a closed half-circle. ∎

Checked exactly on `200` seeded convex fixtures of the committed experiment (`805` vertices): at
every vertex the whole polygon lies in the closed half-plane of the outgoing edge, `0` failures.

**This is a real limitation and it should be stated at the top of any summary of the lane.** The
convex case is precisely where this repo has a sharp criterion already
([`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md), Theorem B, an
iff), and the density criterion adds *nothing* there. Its entire value lives in the non-convex
world, where the sector criterion is only sufficient — and there it is one of two incomparable
sufficient conditions.

---

## 8. Attempts to refute it

An exceptional point with interior density `> ½` in some ball would break the lemma **and**
Lemma A (kill-condition K3). Prediction B of [`KILL-CRITERION.md`](./KILL-CRITERION.md), fixed in
advance, was that none exists.

**Hunt.** `400` seeded pseudorandom star-shaped simple polygons with rational vertices (seed
`20260829`, `5`–`10` vertices each; `349` passed the exact simplicity test, `339` of them
non-convex), all `2683` vertices decided by the committed exact decider. For each of the `358`
vertices it called **not good**, uniform interior samples were drawn and tested for the direct
Lemma A violation `x ∈ Ω  ∧  ρ^{-1}(x) ∈ Ω`. Floats were used **only to search**; any hit would
have been adjudicated exactly (`RULES.md` §5).

```
exceptional vertices found                       358
interior samples drawn at them               698 236
float candidate hits                               0
exact-confirmed Lemma A violations                 0
largest area(P)/(π·R²) seen at an exceptional vertex   0.121
```

Zero violations. K3 not met. The honest weight of this: star-shaped polygons cannot wrap around an
external point, so the search never approached the interesting regime; it is a **consistency
check on Lemma A, not a serious attempt to break it**. The serious attempt is §4, where I tried to
break the proof rather than the statement, and failed to.

**Where I would attack it if I wanted to break it.** Not the measure step — that is airtight and
angle-blind. Step 1 of Lemma A, "`J' \ {O}` is connected, hence lies in one component", is where
a wild curve would have to do its damage, and it does not: connectedness of `S¹` minus a point
needs no regularity. If Lemma A is wrong, it is wrong in Step 2's `int(Ω̄) = Ω`, which uses
`J = ∂E` — that is the JCT-flavoured input and the one to hand a cross-examiner.

---

## 9. The three cheap filters ([`../../RULES.md`](../../RULES.md) §3), all run

**§3.1 wedge test — passed, and the lemma predicts it.** The `30°`-`30°`-`120°` triangle
`O=(0,0)`, `A=(1,0)`, `C=(1/2, √3/6)` was run through the committed decider, exactly:

```
O (30° apex):  good = False      density ≤ area/(π·R²) = (√3/12)/π = 0.0459  <  ½
A (30° apex):  good = False      same by symmetry
C (120°):      good = True       density = 0.1378  <  ½     ← S fires, C and D do not (§5.4)
```

Both exceptional points have density far below `½`, as the theorem of §5.2 **requires**: any
criterion that fired at those points would be refuted on the spot. Mine does not fire, and could
not — its statement is the assertion that it cannot.

**§3.2 square contrast — the argument does not transfer, and I verified I1's version of this
rather than repeating it.** I1 claims the `90°` computation is identical and yields an isosceles
right triangle. **Correct on both counts, and here is the check.** Lemma H, Lemma H′ and Lemma A
are all *angle-blind*: Lemma H is stated for an arbitrary isometry fixing `O` (§3.1), and Lemma
A's proof never mentions `60°`. So with `α = 90°`:

- the measure bound is unchanged — `A ∩ (A + 90°) = ∅` still gives `|A| ≤ 180°`, attained by
  `(0°,90°) ∪ (180°,270°)`. The constant does **not** improve to `1/4`, for the same `C₄`
  independent-set reason as in §3.3 (max independent set in a `4`-cycle is `2`);
- so density `> ½` at `O` yields `P, Q ∈ J` with `|OP| = |OQ| > 0` and `∠POQ = 90°`;
- an isosceles triangle with apex angle `90°` is **not** determined to be anything special: the
  fourth square corner `P + Q − O` is determined as a *point* but is under no constraint to lie
  on `J`, and a single rotation about a single point of `J` constrains only the pair `(P,Q)`.

At `60°`, and only at `60°`, "isosceles with apex angle `α`" forces "equilateral" — the third side
equals the other two exactly when `α = 60°`. **That coincidence is the whole mechanism**, it is
what the rotation lane's §9 says, and it is why nothing here approaches the square peg problem.
If a later version of this argument appeared to settle squares,
[`../../../../RULES.md`](../../../../RULES.md) §7 says the version is wrong.

**§3.3 polygon control — run, and it agreed.** Every computational claim in §6, §8 and this
section was decided by the repo's committed exact decider at
`experiments/inscribed-triangle-polygons/`, **read and run, never modified** (that directory
belongs to another lane). It reproduced the §3.1 witness (both `30°` apexes exceptional, the
`120°` vertex good) before anything else was believed, per
[`../../RULES.md`](../../RULES.md) §5's validation gate. My own additions — exact interior test by
ray-casting in `ℚ(√3)`, exact shoelace area, exact point-to-segment distance — are in the script
of §11 and were checked against the decider wherever the two overlap (§6.2, last two rows: the
independent `Ω ∩ ρΩ ≠ ∅` certificate and `decide_good` agree).

**On the `sympy` warning in my brief.** I used **no** `sympy` geometry predicate anywhere. The
committed decider's `ℚ(√3)` arithmetic (`k3.py`) is standard-library `Fraction` only, with a
syntactic zero test, and my own code adds nothing but `Fraction` arithmetic on top of it. The
documented `Segment2D.intersection` failures on `3` of `176` boundary cases therefore cannot
reach any decision in this lane.

---

## 10. What in the brief and in I1 turned out to be wrong

Recorded explicitly, because [`../../../../RULES.md`](../../../../RULES.md) §0 says a documented
correction is the product.

1. **"Six-fold rotation might give the sharp constant `1/6`."** No. The maximum is `½`, attained,
   and the six translates are provably not pairwise disjoint — the extremal set is `+120°`
   invariant (§3.3). The brief flagged this as the place where most of the mathematical content
   sat; the content turned out to be that the question has a clean negative answer.
2. **"Watch measurability of `A_r` for a.e. `r`."** There is no `a.e.` here: `A_r` is open and
   `B_r` closed for **every** `r`, and the disjointness is a pointwise set identity, not an
   integral statement (§3.2).
3. **The polar-coordinate route is unnecessary.** Lemma H is two lines with no coordinates at all,
   and generalises to any isometry in any dimension (§3.1). I1's inclusion–exclusion computation is
   correct but is a detour, and it is the detour that generated items 1 and 2.
4. **I1's triage line "strictly stronger than the sector criterion" is wrong.** They are
   incomparable (§5.4); the sector criterion fires at the `120°` vertex of the standard witness
   where the density criterion cannot.
5. **I1's ball-density formulation is the wrong statement to carry.** The per-circle form `C` is
   strictly stronger and equally cheap (§5.3).
6. **I1 understated the lemma.** With `Ω̄` in place of `Ω`, the inequality is **strict** and the
   criterion can be stated with `≥ ½` instead of `> ½` (§3.4, §5.2). The distinction is not
   vacuous: Jordan curves of positive Lebesgue measure exist (Osgood), so `λ(Ω ∩ B)` and
   `λ(Ω̄ ∩ B)` genuinely differ in general.
7. **The pinwheel is real** — I1's construction survives exact realisation (§6). Its "four petals"
   phrasing is only sound because just one petal touches `O`; four petals apexed at `O` is
   impossible for a Jordan curve (§6.1).
8. **The lane's honest value is lower than its ranking suggested.** The core lemma is a
   bookkeeping identity; the content is in `H′` (§3.4), in the iff of §5.1, and in the exact
   witness of §6. That is a real but modest contribution, and the "one-page lemma with a
   Lean-plausible core" framing of I1 is accurate about the Lean part and generous about the
   mathematics.

---

## 11. Reproducing everything

Exact throughout; no floating-point value decides anything. Requires **CPython 3.11** and the
repo's committed `experiments/inscribed-triangle-polygons/` on the path (`k3.py`, `geom.py`,
`fixtures.py`) — **read-only; this lane modifies nothing there and owns no `experiments/`
directory of its own**, so the script is inline. Save as `hd.py` beside this file and run
`python3 hd.py`. Wall clock on the machine of record: about **90 seconds**, dominated by the §8
hunt. No random seed enters any decision; the hunt's generator is seeded `20260829`.

```python
import sys, math, random
from fractions import Fraction as F
sys.path.insert(0, "<repo>/experiments/inscribed-triangle-polygons")
from k3 import K
from geom import (P, psub, padd, scal, cross, dot, norm2, peq, rot60, is_simple, is_convex,
                  signed_area2, vertex_angle_class, decide_good, point_on_polygon, pt_pair)

def q(a, b=1): return K(F(a, b), 0)
def pt(ax, ay, bx=1, by=1): return P(q(ax, bx), q(ay, by))
def sc(r, U): return scal(K(r, 0), U)

U = [pt(1,0), pt(3,4,5,5), pt(0,1), pt(-4,3,5,5), pt(-1,0), pt(-3,-4,5,5), pt(0,-1), pt(4,-3,5,5)]
O = pt(0,0); DELTA, RING = F(1,5), F(9,10)

def pinwheel(delta=DELTA, ring=RING, arms=((0,1),(2,3),(4,5),(6,7))):
    pts = [O] + [U[i] for i in range(8)]
    for k in range(len(arms)-1, 0, -1):
        a0, a1 = arms[k]
        pts += [sc(delta, U[a1]), sc(delta, U[a0]), sc(ring, U[a0]), sc(ring, U[arms[k-1][1]])]
    return pts

def area(poly):
    a = signed_area2(poly) / K(2)
    return a if a.sign() > 0 else K(0) - a

def in_interior(X, poly):                      # exact ray casting in Q(sqrt3)
    if point_on_polygon(X, poly): return False
    inside = False; n = len(poly)
    for i in range(n):
        A, B = poly[i], poly[(i+1) % n]
        if (A[1] > X[1]) != (B[1] > X[1]):
            if X[0] < (B[0]-A[0]) * (X[1]-A[1]) / (B[1]-A[1]) + A[0]:
                inside = not inside
    return inside

def dist2_pt_seg(X, A, B):
    AB, AX = psub(B, A), psub(X, A); d2 = norm2(AB)
    if d2.sign() == 0: return norm2(AX)
    t = dot(AX, AB) / d2
    if t.sign() <= 0: return norm2(AX)
    if (t - K(1)).sign() >= 0: return norm2(psub(X, B))
    return norm2(psub(X, padd(A, scal(t, AB))))

W = pinwheel()
print("simple:", is_simple(W)[0], " n =", len(W))
print("angle at O < 60:", vertex_angle_class(W, 0)["cmp60"] == -1)
print("R^2 =", max((norm2(psub(v, O)) for v in W), key=float), "  area =", area(W))
print("density > 1/2 certified:", (area(W) - K(F(31416,20000),0)).sign() > 0)   # (pi/2) < 1.5708
print("eps^2 to nearest non-incident edge:",
      min((dist2_pt_seg(O, W[i], W[(i+1) % len(W)]) for i in range(len(W))
           if not peq(W[i], O) and not peq(W[(i+1) % len(W)], O)), key=float))
r = decide_good(W, O); print("committed decider: good =", r["good"], " verified =", r["verified_ok"])
print("  witness:", r["witness"], r["verified"])
X = P(q(39,200), q(-84,125)); Y = rot60(X, O, -1)
print("overlap certificate in Omega:", in_interior(X, W), in_interior(Y, W),
      "| equal radii:", norm2(psub(X,O)) == norm2(psub(Y,O)))

# ---- section 9 validation gate: the RULES 3.1 witness, exact in Q(sqrt3)
T = [P(K(0,0),K(0,0)), P(K(1,0),K(0,0)), P(K(F(1,2),0), K(0,F(1,6)))]
for i, nm in ((0,"O 30deg"), (1,"A 30deg"), (2,"C 120deg")):
    print(nm, "good =", decide_good(T, T[i])["good"],
          " angle cmp60 =", vertex_angle_class(T, i)["cmp60"])

# ---- section 8 hunt (float search, exact adjudication) and section 7 convex check
def ucirc(t):
    d = 1 + t*t
    return P(K((1-t*t)/d, 0), K((2*t)/d, 0))
def fpip(x, y, fp):
    ins = False
    for i in range(len(fp)):
        ax, ay = fp[i]; bx, by = fp[(i+1) % len(fp)]
        if (ay > y) != (by > y) and x < (bx-ax)*(y-ay)/(by-ay) + ax: ins = not ins
    return ins
rng = random.Random(20260829); C60, S60 = math.cos(math.pi/3), math.sin(math.pi/3)
npoly = nex = nsamp = nhit = 0
for _ in range(400):
    ts = sorted({F(rng.randrange(-4000,4000),1000) for _ in range(rng.randrange(5,11))})
    if len(ts) < 4: continue
    poly = [scal(K(F(rng.randrange(1,40),10),0), ucirc(t)) for t in ts]
    if not is_simple(poly)[0]: continue
    npoly += 1
    fp = [(float(v[0]), float(v[1])) for v in poly]
    xs = [p[0] for p in fp]; ys = [p[1] for p in fp]
    for i, V in enumerate(poly):
        if decide_good(poly, V)["good"]: continue
        nex += 1; vx, vy = fp[i]
        for _ in range(6000):
            x = rng.uniform(min(xs),max(xs)); y = rng.uniform(min(ys),max(ys))
            if not fpip(x, y, fp): continue
            nsamp += 1; dx, dy = x-vx, y-vy
            if fpip(vx + C60*dx + S60*dy, vy - S60*dx + C60*dy, fp):
                Xe = P(q(round(x*100000),100000), q(round(y*100000),100000))
                if in_interior(Xe, poly) and in_interior(rot60(Xe, V, -1), poly): nhit += 1
                break
print(f"hunt: {npoly} polygons, {nex} exceptional vertices, {nsamp} interior samples, "
      f"{nhit} exact Lemma A violations")

from fixtures import random_convex
bad = tot = 0
for f in random_convex(seed=20260829, count=200):
    poly = f["poly"]
    if not is_simple(poly)[0] or not is_convex(poly): continue
    m = len(poly)
    for i in range(m):
        tot += 1
        e = psub(poly[(i+1) % m], poly[i])
        s = {cross(e, psub(v, poly[i])).sign() for v in poly}
        if 1 in s and -1 in s: bad += 1
print(f"convex supporting-line check: {tot} vertices, {bad} failures")
```

Expected output: `simple: True n = 21`; angle-at-`O` test `True`; `R^2 = 1`, `area = 1723/1000`;
density certified; `eps^2 = 4/125`; decider `good = True verified = True`; overlap certificate
`True True | equal radii: True`; `O 30deg good = False`, `A 30deg good = False`,
`C 120deg good = True`; `hunt: 349 polygons, 358 exceptional vertices, 698236 interior samples,
0 exact Lemma A violations`; `convex supporting-line check: 805 vertices, 0 failures`.
