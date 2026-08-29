# CROSS-REVIEW of `README.md` (convex-vertex-criterion)

```
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: elementary convexity facts F1-F6 (proved inline in README.md, re-derived below),
            the intermediate value theorem on R (textbook), the supporting hyperplane theorem
            (textbook, used in F2), "w in int K, y in K => [w,y) subset int K" (textbook, used
            in F4 and in the E1 continuity lemma), "int K nonempty => boundary of K is
            uncountable" (textbook, used in Corollary E). No claim from this repo's results/ or
            any other attack directory is used. AUDIT.md is same-family (Opus auditing Opus) and
            is treated here as a set of assertions to re-derive, not as evidence.
verdict: see per-claim table in section 0 below
```

**A note on what this document can and cannot certify.** I am Claude Sonnet 5; the author of
`README.md` and of `AUDIT.md` is Claude Opus 5. `RULES.md` §5/§8 reserve `verified:review` for an
agent of a genuinely different **model family** (its own example is Claude vs. Codex), and Sonnet
and Opus are both Claude-family models sharing training lineage, RLHF pipeline, and — plausibly —
correlated blind spots in exactly the way §8 is worried about. The dispatcher told me explicitly
that, with Codex unavailable, a human has directed this session be treated as the standard applied
here; I record that instruction rather than resolve the policy question myself. What follows is a
maximally adversarial, independently-reconstructed technical verdict on each claim. Whether it is
sufficient to move `README.md`'s status line is a call for the dispatching human, not for me — and
I do not touch `README.md` regardless, since it is not in my lane (`RULES.md` §2).

I did not read `AUDIT.md`'s proofs and then reproduce them; where I state agreement with something
`AUDIT.md` also found (E1, E2 below), I re-derived it via a **different explicit computation** than
either `README.md` or `AUDIT.md` used, specifically so that a shared blind spot in their common
parametrization could not silently repeat itself in mine. Where I found nothing new to disagree
with, I still ran fresh, from-scratch computations (below) rather than resting on "I read the
argument and it reads soundly."

---

## 0. Verdict table

| Claim | Verdict | Confidence basis |
|---|---|---|
| Theorem A (obstruction, incl. strong form) | **Holds.** Reconstructed independently; no gap. | hand re-derivation |
| Theorem B(i), α > π/3 (existence) | **Holds.** Reconstructed independently; no gap. | hand re-derivation + fresh exact code, ~950 polygon vertices |
| Theorem B(ii), α = π/3 iff | **Holds.** Reconstructed independently; no gap. | hand re-derivation (the uniqueness-of-θ argument is airtight) |
| Counterexample `K*` | **Holds**, and is global not local. | re-derived via a *different* explicit parametrization than either README or AUDIT |
| Theorem C(a), at most 2 with α<π/3 | **Holds.** | hand re-derivation + fresh exact code, 3000 random polygons |
| Theorem C(b), at most 3 with α≤π/3, =3 forces K=triangle | **Holds.** | hand re-derivation, including the 4-point exclusion algebra |
| Proposition D (sharpness witness) | **Holds**, arithmetic exact; **AUDIT's E2 correction independently reconfirmed** (README's "Case C" attribution is wrong; Case A fires) | fresh exact computation, not copied from either file |
| Corollary E | **Holds**, as a logical consequence of A/B/C. One framing point (below), not an error. | hand re-derivation |
| E1 (AUDIT's correction: `r` is continuous, not just usc, on all of `[0,α]`) | **Holds**, and Theorem B's proof genuinely needs only usc, so nothing downstream changes. | independent lemma + fresh computation on `K*` confirming the mechanism is `Σ(0)=∅`, not a jump |
| E3 (AUDIT's arithmetic-slip correction, §5.5) | **Not independently re-checked** — cosmetic, `numerical`-tier, not load-bearing for A-D or Corollary E. | not-checked |
| E4 (AUDIT's dependency-declaration correction) | **Agree it's a real gap in the "proved inline" claim**, but agree with AUDIT that none of the three facts named is remotely Jordan-curve-theorem-weight. | independent spot-check of each named fact |
| §6 β-generalisation remark | **Not checked.** Both README and AUDIT already flag it unchecked; it is explicitly not one of Theorems A-D. | not-checked |
| Literature provenance (Meyerson 1980) | **Not checked** — outside this review's scope and this attack's lane. | not-checked |

**Bottom line: I found no counterexample and no load-bearing gap in Theorems A, B, C, Proposition
D, or Corollary E.** I also did not find a *new* instance of the closure-vs-achieved-directions bug
that produced the original refutation of (C2) — I specifically hunted for one, below, since that is
the failure mode named in my brief, and Theorem A/C's uses of the tangent cone are all in the
*safe* direction (as an upper bound on an angle, where a closure can only make the bound harder to
achieve, never easier), while Theorem B's existence proof carefully derives membership in the
*achieved* set `A` from positivity of `r`, never from the closed cone `T(O)` directly. That
discipline is the reason the second bug I was sent to look for does not appear to be there.

---

## 1. Restating the claims in my own words

**Theorem A.** Let `K` be a compact convex planar body with nonempty interior and `O` a boundary
point. Look at the cone spanned by all rays from `O` through points of `K`, and take its closure —
call its angular width `α(O)`. If `α(O) < 60°`, no equilateral triangle with a vertex at `O` can
have its other two vertices on `∂K`, because *any* two points of `K` other than `O` subtend an
angle at `O` of at most `α(O) < 60°`, and an equilateral triangle's vertex angle is exactly `60°`.

**Theorem B.** If instead `α(O) > 60°`, such a triangle always exists. If `α(O)` is *exactly*
`60°`, existence depends on something the cone itself cannot see: whether `K` actually reaches all
the way out along *both* boundary rays of the cone (not just approaches them in the limit), or only
one, or neither. If both, `O` is good; if not, `O` is not good even though the cone has exactly the
right width.

**The counterexample.** There is a compact convex body — the region pinched between a downward
parabola and a `60°` ray from the origin, closed off by a vertical wall — whose tangent cone at the
origin has the correct `60°` width, but whose achieved boundary directions are `(0°, 60°]`, missing
the `0°` ray itself. So the origin is not a good vertex, showing that "cone-width `≥ 60°`" is not by
itself sufficient, only "cone-width `> 60°`" or "cone-width `= 60°` with both rays actually filled."

**Theorem C.** Take any three distinct boundary points, each with cone-width `< 60°`. I claim this
is impossible: those three points can't be collinear (a middle point would see a straight `180°`
angle, contradicting its own `<60°` bound), so they form a genuine triangle, and the angle of that
triangle at each of the three points is itself bounded by that point's cone-width — so all three
interior angles are `<60°`, summing to `<180°`, contradicting the fact that a Euclidean triangle's
angles always sum to exactly `180°`. Hence at most two such points exist. A slightly stronger
version, allowing cone-width `= 60°` (not just `<`), gives at most **three**, and if there really
are three, the same argument forces the three points to themselves be an equilateral triangle,
which then turns out to force `K` to actually **be** that triangle, with every one of the three
being good.

**Corollary.** Combining the above: on the boundary of any compact convex planar body with an
interior, all but at most two points admit an inscribed equilateral triangle with a vertex there,
and two exceptional points really can happen (a `30°-30°-120°` triangle has exactly two — its two
`30°` corners).

I can restate every one of these without reference to the source text, which per §5's own first
instruction is the necessary condition for treating them as verifiable at all.

---

## 2. Reconstructing F1-F6, including the E1 correction

I re-derived each fact from the bare definitions before checking my derivation against the file.

**F1** (`K ⊆ O + T(O)`): trivial from the definition of `Γ(O)` as the cone generated by `K-O`
(every `x-O` is `1·(x-O) ∈ Γ(O) ⊆ T(O)`). Nothing to attack; this is definitionally forced. Agree.

**F2** (`α ∈ (0,π]`): a supporting line exists at `O` by the supporting hyperplane theorem (every
boundary point of a convex set with nonempty interior has one — textbook, not re-derived here), so
`K - O`, hence `Γ(O)`, hence its closure `T(O)`, lies in a closed half-plane through `0`; a closed
convex cone confined to a half-plane is an angular sector of opening `≤ π`. Nonempty interior of
`K` gives a small disc of directions around some interior ray, so `α > 0`. Agree.

**F3** (`A` is an interval, `inf A = 0`, `sup A = α`): the file's one-line justification
("nonzero arguments of a convex cone in a half-plane form an interval") has a genuine degenerate
case I checked by hand: if `Γ(O)` contains two exactly antipodal directions `θ₀, θ₀+π` (this
happens precisely when `O` sits in the interior of a straight edge, so `K` extends in *both*
directions along that edge — e.g. an edge-interior point of a polygon, where `α = π`), the naive
"positive combinations" argument for convexity of the argument set needs a moment's care, because
positive combinations of two antipodal *rays* alone only reconstruct the line, not the interior
angle. I checked directly that the conclusion still holds in this case: such a `Γ(O)` in fact
contains the *entire* half-plane bounded by that line (since `K` has 2-D extent on that side, by
nonempty interior), so `A = [0, π]` — still an interval, `α = π`, consistent with everything else
in the file (Proposition D explicitly uses `α = π` at edge-interior points). So the one-line
justification is presentationally incomplete but the *statement* was never false. I did not need
AUDIT.md's cleaner connectedness argument to reach this conclusion; I reconstructed the degenerate
case directly. Agree, non-load-bearing gap in exposition only.

**F4** (radial interior lemma): re-derived independently. The key point I checked explicitly is
that `ψ₁, ψ₂ ∈ A` with `ψ₁ < θ < ψ₂` and `ψ₂ - ψ₁ < π` can *always* be chosen when `θ ∈ (0,α)`,
because `(0,α) ⊆ A` (F3) is itself an open interval containing `θ`, so `ψ₁, ψ₂` can be taken
arbitrarily close to `θ` from within `(0,α)`, making `ψ₂-ψ₁` arbitrarily small — no need to worry
about points of `A` near the far end of `[0,α]`. No circularity (F3 doesn't depend on F4). Agree.

**F5** (extreme rays are boundary): re-derived. If `t·e^{i0} ∈ int K` for `t>0`, an open ball
around it lies in `K`, hence contains points of `K` with argument `<0`, contradicting `K ⊆
T(O) = \{\arg \in [0,\alpha]\}` (F1). Combined with `[0, r(0)e^{i0}] ⊆ K` by convexity (since
`O, r(0)e^{i0} \in K`), this pins `\Sigma(0) = (0, r(0)]` exactly. Agree.

**F6 and E1 — I derived the continuity correction myself before checking it against `AUDIT.md`.**
The file's F6 states only upper semicontinuity at the endpoints, and its note claims `r` "genuinely
can be discontinuous" at `0` or `α`, citing `K*` as the mechanism. Working this out for myself:

> **Claim.** `r` is continuous on the *closed* interval `[0,\alpha]`.
> *Proof sketch, my own construction.* usc always gives `limsup_{ψ→0+} r(ψ) ≤ r(0)`. If `r(0)=0`
> this already forces `r(ψ)→0` since `r≥0`. If `r(0)>0`, take any `ψ₂ ∈ (0,α)` (so `r(ψ₂)>0` by
> F3) and look at the straight-edged triangle spanned by `O`, `r(0)e^{i0}`, `r(ψ₂)e^{iψ₂}` — it is
> contained in `K` by convexity, and *its own* radial function is an elementary continuous function
> of angle (it's just where a ray crosses a straight line), equal to `r(0)` at angle `0`. Since `K`'s
> radial function dominates the sub-triangle's, `liminf_{ψ→0+} r(ψ) ≥ r(0)`. Combined with usc,
> `r(ψ)→r(0)`. Symmetric argument at `α`. ∎

This is essentially the same idea `AUDIT.md` uses (a nondegenerate inscribed sub-triangle to sandwich
the liminf); I want to be honest that I did not invent a *structurally* different proof of this
particular lemma — there are only so many ways to get a lower bound on a convex body's radial
function, and "exhibit a triangle inside it" is the natural one. What I did independently is
**re-verify the conclusion against `K*` using a parametrization neither README nor AUDIT wrote
down**: parametrizing `K* = \{0≤x≤1,\ x^2≤y≤\sqrt3 x\}` directly by its `x`-coordinate rather than
by `\arctan`, the boundary point at angle `θ ∈ (0,π/3]` sits at `x = \min(\tan θ, 1)`, giving

$$ r(θ) = \min(\tan θ, 1)\cdot\sec θ \quad\text{for } θ\in(0,\pi/3], \qquad r(0)=0. $$

As `θ→0^+`, `\tan θ → 0` so `r(θ)→0 = r(0)`: **continuous**, not a jump — confirming, via a route
I built myself rather than reading, that the correction is right and the mechanism really is
`Σ(0)=\{t>0 : t·e^{i0}\in K^*\}=\emptyset` (equivalently `0\notin A`), not a discontinuity of `r`.
I also checked that Theorem B(i)'s Case C proof (§4 below) genuinely never asks for more than usc,
so E1 changes the diagnosis but not any conclusion — I confirm this by re-tracing Case C's own
estimates in section 4, not by taking AUDIT's word for it.

**Conclusion on F1-F6/E1: agree on all six facts and on the E1 correction.** The one place I would
push back gently on `AUDIT.md`'s presentation: it calls the original F6 note "wrong" in a way that
could read as a substantive proof error; having reconstructed it myself, I'd call it a **true
statement of a strictly weaker fact than is actually available**, attached to a *false* diagnosis of
where `K*` breaks (jump vs. missing direction) — the distinction matters for a reader deciding what
to formalize, exactly as AUDIT itself argues, but it is not a hole in any proof.

---

## 3. Proposition R and Theorem A

**Proposition R** (`O` good iff some `θ ∈ [0,α]` with `θ-π/3 ∈ [0,α]` has `Σ(θ)∩Σ(θ-π/3)≠∅`): I
re-derived both directions. `(⇐)` is a direct computation: `|PQ|² = 2t² - 2t²\cos(60°) = t²` for
`P=te^{iθ}, Q=te^{i(θ-π/3)}`, so all three sides equal `t>0`; both points lie on `J` by definition
of `Σ`. `(⇒)`: an equilateral triangle forces `|OP|=|OQ|=t>0` and vertex angle `π/3`; both `P,Q ∈
K\setminus\{O\}` (since `K` is closed, `J\subseteq K`) have arguments in `A\subseteq[0,\alpha]
\subseteq [0,\pi]` (F1/F2), and for two arguments confined to `[0,\pi]` the *unsigned* angle
between the vectors is exactly the difference of arguments — this is the one place a sign error
could hide (an unsigned angle could in principle be `2\pi` minus the naive difference), and I
checked it explicitly: since both arguments lie in a range of total width `\le\pi`, the naive
difference is itself already in `[0,\pi]`, so it *is* the unsigned angle, with no `2\pi` wraparound
possible. Agree, the iff is exact.

**Theorem A, strong form** (`P,Q\in K\setminus\{O\} \Rightarrow \angle POQ \le \alpha(O)`): both
`P-O,Q-O \in T(O)`, a sector of opening `\alpha(O)\le\pi`; same argument-range trick as above pins
the unsigned angle at `|\theta_P-\theta_Q|\le\alpha(O)`. Applying this to a nondegenerate equilateral
triangle gives `\pi/3 \le \alpha(O)`, i.e. the contrapositive of Theorem A. I specifically checked
**which direction of the tangent-cone closure this uses**, since that is the named failure mode:
`T(O)` is used here purely as a *superset* bound on where `P-O,Q-O` can point, which is exactly the
safe direction — a closure can only be *larger* than the achieved-direction cone, so a containment
bound derived from it can only be *weaker*, never wrong. This is the mirror image of the (C2) bug,
which tried to use the closure to certify that a direction is *achieved*. I traced every later use
of `T(O)`/`\alpha(O)` in Theorem A and Theorem C and found all of them used in this same safe,
upper-bound direction. Agree, and this is the strongest single fact in the file.

---

## 4. Theorem B, both parts

**Part (ii), `\alpha=\pi/3`.** With `\alpha=\pi/3`, Proposition R's constraint
`\theta,\theta-\pi/3\in[0,\pi/3]` forces `\theta=\pi/3` **uniquely** — there is no freedom here,
which is exactly why this case is rigid enough to decide by hand. `O` good `\iff \Sigma(0)\cap
\Sigma(\pi/3)\ne\emptyset`. If both `0,\pi/3\in A`: F5 gives `\Sigma(0)=(0,r(0)]`,
`\Sigma(\pi/3)=(0,r(\pi/3)]`, and any `t\le\min(r(0),r(\pi/3))` works. If either direction is
*not* achieved, its `\Sigma` is empty (there is no `t>0` with `t\cdot e^{i\theta}\in K` at all, since
`r(\theta)=0` there), so the intersection is empty. Since `(0,\pi/3)\subseteq A\subseteq[0,\pi/3]`
(F3), "`A=[0,\pi/3]`" is exactly "`0\in A` and `\pi/3\in A`" — exactly "both extreme rays meet `K`
in a positive-length segment." I re-derived this without reading the proof first and landed in the
same place; the argument has no room for a subtler failure because the admissible `\theta` is
unique. Agree — this is airtight.

**Part (i), `\alpha>\pi/3`.** Reconstructed the three-case split independently.

- *Case A* (`r(0)\ge r(\pi/3)`): since `\pi/3\in(0,\alpha)`, `r(\pi/3)>0` (F3), so `r(0)>0` too,
  putting `0\in A`. `t=r(\pi/3)\in\Sigma(\pi/3)` (F4), and `t\le r(0)` puts `t\in\Sigma(0)=(0,r(0)]`
  (F5). I checked specifically that `t=r(\pi/3)>0` is *guaranteed regardless of the case split* —
  it only depends on `\pi/3\in(0,\alpha)`, which holds whenever `\alpha>\pi/3`, full stop — so the
  degenerate `P=Q=O` failure mode cannot occur here even in principle.
- *Case B*: symmetric at `\alpha-\pi/3`. Same guarantee.
- *Case C* (neither A nor B): `F(\theta)=r(\theta)-r(\theta-\pi/3)` on the *open real interval*
  `(\pi/3,\alpha)`. I checked explicitly that both `\theta` and `\theta-\pi/3` stay inside `(0,\alpha)`
  throughout this open interval, so `F` is continuous there by F6 (needing only usc, per §2 above —
  E1's stronger continuity is not required, and I verified this by re-deriving the two endpoint
  estimates myself: `liminf_{\theta\to\pi/3^+}F \ge r(\pi/3) - \limsup_{\psi\to0^+}r(\psi) \ge
  r(\pi/3)-r(0) > 0` by Case C's own hypothesis, and symmetrically `\limsup_{\theta\to\alpha^-}F \le
  r(\alpha)-r(\alpha-\pi/3) < 0`). IVT on `(\pi/3,\alpha)`, a genuine connected subset of `\mathbb
  R` with no reference anywhere to `\partial K`'s own topology, gives a root `\theta_0` strictly
  inside `(\pi/3,\alpha)`, hence `\theta_0,\theta_0-\pi/3 \in (0,\alpha)`, giving `r(\theta_0)>0` by
  F3. **This is the item my brief asked me to check hardest**: is the IVT domain genuinely
  connected? Yes — it is a literal open interval of real numbers, not a curve, not `J\setminus\{O\}`,
  not requiring `\partial K\cong S^1`. The file's own §4.3 explains why it deliberately avoided the
  curve-connectedness route the original brief proposed, and I independently confirm that
  avoidance is real, not a relabeling: nothing in Case A, B, or C ever asks whether two boundary
  points can be joined by an arc of `J`.

I also specifically hunted for a case where the exhaustiveness `A\vee B\vee C` could fail (i.e. a
gap between the cases), or where Cases A/B could "fire" with `t=0`: neither happens, since `C`
is defined as `\neg A\wedge\neg B` by construction, and I showed above that both A and B always
produce `t>0` whenever they fire (via `\pi/3\in(0,\alpha)` resp. `\alpha-\pi/3\in(0,\alpha)`).

**Fresh computational check, structurally different from both README's `r(\theta)` method and
AUDIT's Q(√3) rotation checker (I wrote it before reading AUDIT's implementation details).** I
implemented, from scratch, exact rational arithmetic for random convex polygons (`fractions.
Fraction`, my own convex-hull routine) to test the polygon corollary "`O` good `\iff \alpha(O)\ge
60°`" via a genuinely different geometric method than the radial-function reduction: rotate the
whole boundary `J` by `+60°` about `O` and look for `J\cap\rho(J)` away from `O`, using exact
`\mathbb Q(\sqrt3)`-arithmetic segment intersection.

**I found a bug in my own code, exactly of the kind flagged in my brief, and it is worth recording
in full because of what it demonstrates.** My first version of the segment-intersection test
handled only *transversal* (proper) crossings via strict sign tests, and silently returned "no
intersection" for touching or collinear-overlap cases. Run against 950 boundary vertices of random
integer-coordinate convex polygons, it agreed with the theorem 950/950 times — but when I built the
one case that specifically probes the `\alpha=60°` boundary that random rational polygons cannot
reach (the equilateral triangle itself, whose every vertex has `\alpha=60°` exactly and is trivially
good, since it is inscribed in itself), my checker returned **"not good" at all three vertices**,
flatly contradicting the theorem. Diagnosing it: rotating an equilateral triangle by `60°` about one
of its own vertices maps one of its edges *exactly onto* another (`\rho(B)=C` for the standard
triangle), so `J` and `\rho(J)` share a whole edge and a shared vertex, not a transversal crossing —
precisely the touching/collinear case my sign-only test discarded. This was **my bug**, not a fact
about the theorem: after adding explicit endpoint-touching and collinear-overlap detection (segment
containment via cross-product-zero plus a dot-product betweenness test, all still exact in
`\mathbb Q(\sqrt3)`), the equilateral triangle correctly reports "good" at all three vertices, and
re-running the full 950-vertex random sweep still shows zero disagreements with the polygon
corollary of Theorem B. I record this at length because it is exactly the caution in my brief about
geometric-predicate bugs hiding in the "obviously never happens" collinear case — and it happened on
my *first* attempt, on the *one* hand-built case that actually probes the theorem's most delicate
boundary. I would not have caught it had I only run random polygons.

**What this computational work is and is not evidence for.** It is `numerical`, not committed to
`experiments/` (not my lane, `RULES.md` §2), and per the problem's `RULES.md` §3.3 only covers
convex *polygons*, where `A` is always closed — so it tests Theorem B(i) and the "closed-`A`" half
of B(ii), never the genuinely delicate `A\ne[0,\pi/3]` failure mode, which by construction cannot
occur on a polygon (straight edges always fill both extreme rays). That half is tested only by the
hand-arithmetic reconstruction of `K*` in section 5, not by any polygon sweep — mine or AUDIT's.

---

## 5. The counterexample `K*`, reconstructed via a route neither file used

`K^* = \{(x,y): 0\le x\le 1,\ x^2\le y\le \sqrt3\,x\}`, `O=(0,0)`. Convexity, compactness and
nonempty interior are immediate (intersection of two half-planes and the epigraph of `x\mapsto x^2`,
bounded, and `(1/2,1/2)` satisfies all constraints strictly). Rather than following either file's
`A = \bigcup_x [\arctan x, \pi/3]` derivation, I parametrized the boundary directly by `x`: along
the ray at angle `\theta\in(0,\pi/3]`, points of `K^*` on that ray have `y=x\tan\theta` and must
satisfy `x^2\le x\tan\theta` (i.e. `x\le\tan\theta`, from the lower parabola) and `x\le 1`, so the
farthest such point is at `x=\min(\tan\theta,1)`, giving

$$ r(\theta) = \min(\tan\theta,1)\cdot\sec\theta, \qquad \theta \in (0,\pi/3],\qquad r(0)=0. $$

A point on the ray at angle `0` other than `O` needs `y=0` and `x>0`, but `y\ge x^2>0` forbids it —
so `\Sigma(0)=\emptyset` directly, no limiting argument needed, and `r(\theta)\to0=r(0)` as
`\theta\to0^+` (continuous, confirming E1). By Proposition R, `O` good would need `\theta=\pi/3`
with `\Sigma(\pi/3)\cap\Sigma(0)\ne\emptyset`; `\Sigma(0)=\emptyset` kills it immediately, and this
argument uses no point of `J` near `O` specifically — any `P,Q\in J\setminus\{O\}` at all satisfy
`\arg P,\arg Q\in(0,\pi/3]`, so no pair can differ by exactly `\pi/3` starting from a value that
must exceed `0`. The refutation is global, matching both files' claim on this point. **Agree, via
an independently-computed route.**

I also independently checked `\alpha(O)=\pi/3` exactly: the achieved directions are `(0,\pi/3]`, an
interval whose closure is `[0,\pi/3]` — width `\pi/3` — confirming the tangent cone really is the
`60°` sector even though the origin ray itself is never reached.

---

## 6. Theorem C, both parts, and the four-point exclusion

**(a).** Three distinct points `O_1,O_2,O_3` with `\alpha(O_i)<\pi/3` cannot be collinear: if `O_2`
were between the other two, `O_1,O_3\in K\setminus\{O_2\}` would give `\angle O_1O_2O_3=\pi`,
contradicting the strong form of Theorem A (`\pi\le\alpha(O_2)<\pi/3`, absurd). So they form a
genuine triangle, and the interior angle at `O_i` **is** `\angle O_jO_iO_k`, which the strong form
bounds by `\alpha(O_i)`. Three angles each `<\pi/3` sum to `<\pi`, contradicting the Euclidean
angle-sum theorem. This uses **only** F1 (via the strong form) and Euclidean angle sums — no
rectifiability, no turning number, nothing about a general convex *curve* beyond three of its
points being in convex position. Agree, and I consider this the most robust claim in the file:
it is two applications of a single already-verified lemma (the strong form of Theorem A) plus one
Euclidean fact.

**(b).** Same argument with `\le\pi/3` forces any three such points to be exactly equilateral (all
three angles `\le\pi/3` summing to `\pi` forces all three `=\pi/3`). For the four-point exclusion I
worked the reflection algebra myself: `O_1O_2O_3` and `O_1O_2O_4` equilateral on the shared base
`O_1O_2`, `O_3\ne O_4`, forces `O_4` to be `O_3`'s reflection across line `O_1O_2` (the only other
point completing an equilateral triangle on that base), giving `|O_3O_4|=\sqrt3\,|O_1O_2|` (two
equilateral apexes, heights `\pm(\sqrt3/2)|O_1O_2|` from the base, so their separation is the sum of
heights = `\sqrt3\,|O_1O_2|`). But `\{O_1,O_3,O_4\}` must *also* be equilateral by the same
"exactly-`\pi/3`" argument (since all four points individually satisfy `\alpha\le\pi/3`), forcing
`|O_3O_4|=|O_1O_3|=|O_1O_2|`. Combining: `\sqrt3\,|O_1O_2| = |O_1O_2|`, impossible for
`|O_1O_2|>0`. For exactly three points, I re-derived that the vertex cone `T(O_i)` — a sector of
opening exactly `\pi/3` containing two rays exactly `\pi/3` apart — has **no room to be anything
other than** the sector those two rays bound (a sector cannot properly contain two rays separated
by its own full aperture), so `K\subseteq\bigcap_i(O_i+T(O_i))`. I checked directly that the
intersection of the three vertex-wedges of a triangle equals the triangle: each wedge at `O_i` is
the intersection of the two supporting half-planes whose boundary lines pass through `O_i`, and
intersecting all three wedges intersects each of the triangle's three half-planes twice, i.e. is the
triangle itself. With `T\subseteq K` by convexity, `K=T`. Agree on both halves, no gap.

**Fresh computational check on Theorem C**, independent code (not shared with either the polygon
check in §4 or with any prior file's numerics): 3000 random convex integer-coordinate polygons
(3-10 vertices), interior angles compared to `60°` via the exact sign test `4(u\cdot v)^2
\gtrless |u|^2|v|^2` on integer/rational vectors — no floating point, no trigonometric functions.
Across all 3000 trials, the maximum number of vertices with `\alpha<60°` was **2**, and the maximum
with `\alpha\le60°` was also **2** (random rational polygons never hit `\alpha=60°` exactly, matching
both files' observation that this needs `\mathbb Q(\sqrt3)`-constructed examples), consistent with
the sharp bound and with no violation found.

---

## 7. Proposition D — exact re-derivation, and an independent confirmation of AUDIT's E2

Working entirely from the vertices `O=(0,0), B=(1,0), C=(-1/2,\sqrt3/2)` and *not* from either
file's stated formulas, I derived the far edge `BC` as the line `x+\sqrt3y=1` (from the two-point
slope through `B,C`), giving `r(\theta)=1/(\cos\theta+\sqrt3\sin\theta)` for `\theta` in the cone's
range. Evaluating exactly:

$$ r(0)=1,\quad r(\pi/3)=\tfrac12,\quad r(2\pi/3)=1,\quad r(\pi/3)=\tfrac12\ (\text{again, at }
\alpha-\pi/3). $$

**Case A's hypothesis `r(0)\ge r(\pi/3)` reads `1\ge1/2`: true.** So the *proof's own case split*
takes Case A here, not Case C, and Case A's construction gives witness `t=r(\pi/3)=1/2`,
`P=(1/4,\sqrt3/4)` (angle `\pi/3`), `Q=(1/2,0)` (angle `0`). I verified this by direct distance
computation: `|OQ|=1/2`, `|OP|=\sqrt{1/16+3/16}=1/2`, `|PQ|=\sqrt{1/16+3/16}=1/2` — genuinely
equilateral, side `1/2`, both `P` and `Q` on `\partial K` (`Q` is the midpoint of edge `OB`; `P`
satisfies `x+\sqrt3y=1/4+3/4=1`, on edge `BC`). **This independently reconfirms `AUDIT.md`'s E2**:
the README's own stated witness (`O,(0,1/\sqrt3),(1/2,1/(2\sqrt3))`, side `\sqrt3/3`) is a real,
separate, and also-correct equilateral triangle — I verified all three of its side lengths equal
`\sqrt3/3` and that both non-`O` points lie exactly on line `x+\sqrt3y=1` within the segment — but
it corresponds to a root of `F` at `\theta_0=\pi/2` (I checked `r(\pi/2)=r(\pi/6)=1/\sqrt3` exactly),
which is **not** what Case A's or Case C's construction produces at this `O`, since Case A already
fires and never looks at `\theta=\pi/2`. So there exist *two* distinct inscribed equilateral
triangles with a vertex at this `120°` corner, and the one the proof of Theorem B actually
constructs is the side-`1/2` one, not the side-`\sqrt3/3` one the README's prose describes as the
output of its own Case C. This is a real, independently-confirmed write-up error (matching
`AUDIT.md`'s finding, reached here by a different arithmetic route), and it does not touch the
correctness of Theorem B or of Proposition D's headline claim (a good witness exists; the sharp
bound of 2 is attained by the `30-30-120` triangle) — only the sentence attributing the specific
witness to a specific proof branch.

I did not independently re-check `AUDIT.md`'s E3 (a decimal/closed-form mismatch in the file's
`numerical` §5.5) — it is cosmetic, in a `numerical`-tier section, and load-bears nothing in
Theorems A-D or Corollary E, so I spent my effort elsewhere per this review's priorities.

---

## 8. Corollary E

Direct consequence of A/B/C as re-derived above: not-good `\Rightarrow \alpha\le\pi/3` (contrapositive
of B(i), no need for Theorem A at all here), at most three points have `\alpha\le\pi/3` (C(b)), and
if there are exactly three then `K` is the triangle they form and all three are in fact good (so the
non-good count is *zero*, not three, in that case) — otherwise at most two points have `\alpha\le
\pi/3`, an upper bound on the non-good count. I checked this "at most 3, but 3 collapses to 0" step
carefully since it is easy to botch: the bound in Corollary E is on how many points *can* fail to be
good, and Theorem C(b)'s three-point case is exactly the one scenario where the naive bound of 3
over-counts, because all three turn out to be good — the corollary's stated bound of 2 survives this
correctly since it never claims the ≤3 points from C(b) are automatically non-good, only that
non-good points are a subset of them. Agree, no error.

**One framing point, not an error.** Corollary E's own statement is about `J=\partial K` for `K`
compact convex — a purely metric/convexity statement needing no curve topology. Identifying this
with "every convex **Jordan curve**" (as both the file's provenance banner and my own dispatch brief
phrase it) additionally needs the fact that `\partial K` for such a `K` is homeomorphic to a circle.
That fact is true and elementary (the radial map from any interior point is a bijection
`[0,2\pi)\to\partial K`, and it's continuous), but it is not proved or even stated as a lemma inside
`README.md`. This doesn't affect any proof step — it's a labeling question about how the result gets
advertised, already noted by `AUDIT.md`'s own framing caveat, and I confirm the underlying fact is
genuinely true rather than merely likely.

---

## `not-checked`

1. **The literature (Meyerson 1980).** Not looked at; not this lane's job (`RULES.md` §6.1 makes it
   verification-critical citation work).
2. **The `\beta`-generalization remark in README §6.** Both the README and `AUDIT.md` mark it
   unchecked already; it is not one of Theorems A-D or Corollary E and I did not add anything here.
3. **The three named textbook facts (E4): the supporting hyperplane theorem, `[w,y)\subseteq
   \mathrm{int}\,K`, and uncountability of `\partial K`.** I sanity-checked each conceptually
   (the last one via the radial-bijection argument in §8) but did not write out a full first-
   principles proof of any of the three. All are standard undergraduate convexity/point-set facts;
   I found nothing suspicious about any of them, but I record that I took their *truth* on trust
   in the sense that I did not reprove them from the definition of convexity alone.
4. **Case C of Theorem B exercised on a genuinely curved (non-polygon) body, by my own code.** I
   verified Case C's proof completely by hand (§4 above) and I am confident in it, but the only
   curved-body numerical exercise of Case C in the directory is `AUDIT.md`'s `K_C` (an `80°`
   wedge), which I read but did not reimplement. My own fresh computation targeted the polygon
   corollary of B(i)/(ii) and the `K^*` boundary case by hand, not a fresh Case-C curved example.
   This is a minor gap since the hand-proof of Case C has no dependency I could not independently
   verify, but I flag it because the brief specifically asked about limits-of-approximants and
   Case C is the one place a curved, non-polygonal example would be the most informative stress
   test, and I did not add a genuinely new one of my own.
5. **`README.md` §5's own claimed numerics (items 3-4, the bisection checker and the Python-closure
   bug story).** I did not reproduce these; I built independent checkers instead and they agree
   with the theorems, but I cannot confirm or deny the author's account of their own debugging
   history.
6. **Whether `\alpha=\pi/3` with `A=[0,\pi/3]` (the "good" branch of B(ii)) is realizable on a
   non-polygon.** Not needed for any claim; not attempted.

Everything else claimed as "checked" above was independently reconstructed from the definitions, not
read and found agreeable — including one place (§4) where doing so caught a real bug in my own
code before it could produce a false verdict.
