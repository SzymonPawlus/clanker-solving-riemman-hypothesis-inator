# Journal: round-3 cross-examination of four IET claims (2026-08-29)

Role: cross-examiner, same conversation as the four authoring lanes. Branch
`claude/inscribe-equilateral-triangle-oj15x1`. Output:
[`../../problems/inscribed-equilateral-triangle/attacks/round3-cross-review/README.md`](../../problems/inscribed-equilateral-triangle/attacks/round3-cross-review/README.md).

## Framing, read first

Same-model-family examination (Sonnet 5 examining Opus 5). Per `RULES.md` §5 and §8 this cannot
grant `verified:review` — that requires a different model *family*, and Codex was unavailable this
session. Everything below is due diligence, not promotion. A round-2 same-family cross-review
earlier today cleared three claims with no objection; that is not license to expect the same here
— it is weak evidence about the reviewer's independence, not about these four lanes' correctness,
and I looked for breaks accordingly rather than confirming what already sounded right.

Targets, in the priority order given: `attacks/exceptional-set-polygons/` (flagged highest-value
because it refutes another lane), `attacks/exceptional-pair-rigidity/`, `attacks/extremal-size/`,
`attacks/scalene-shapes/`.

## Method

For each claim: restate it independently; re-derive every step from definitions rather than
reading the proof and agreeing; attack the standard failure points (JCT applied to something not
shown Jordan, continuity claimed where it fails, nondegeneracy/limits, division by a possibly-zero
quantity, the step each lane's own brief nominated as weakest); for computational claims,
re-implement the decision procedure completely from scratch — my own `Fraction`-based
$\mathbb Q(\sqrt3)$ field (add/sub/mul/div by conjugate, syntactic zero test, sign test comparing
$a^2$ vs $3b^2$), my own exact segment-segment intersection (Cramer's rule plus a collinear-overlap
branch), my own rotation-by-60° map — sharing no code with either the committed enumerator or
either lane's decider, and no `sympy` geometry predicate anywhere. Source of the decider and every
test script is below; nothing here depends on rerunning anyone else's code.

## Lane 1 — `attacks/exceptional-set-polygons/` — outcome: survived everything I tried

This is the highest-value target because Theorem 3 refutes `spiral-tip-witness` §9.3's claim that
"every exceptional point of a simple polygon is wedge-type." A wrong refutation here would be worse
than a wrong positive result, so I rebuilt the witness completely independently before reading the
lane's own confirmation numbers.

**The alleged gap in the "tangent line" shortcut — checked, and it is real.** The brief said the
naive argument ("non-vertex point has a tangent line, hence a 180° cone, hence a triangle") has a
gap because Lemma 1's criterion needs two points at *equal radius* 60° apart, while a tangent line
only supplies two directions 180° apart. I re-derived Lemma 1 from scratch (the isosceles-with-
60°-apex-is-equilateral fact, three lines) and confirmed: a local segment through a non-vertex
point contributes exactly two directions to $\Theta(r)$ for small $r$, both differing by 180°, and
180° ≠ 60°, so the tangent-line argument alone proves nothing. The lane's actual proof (Theorem 1)
routes through the *interior region* filling a half-disc there (Lemma 2) and the region lemma
(Lemma 3), not through the curve's local direction set — that substitution is real and necessary,
not decorative.

**Lemma 3 (the region lemma), re-derived from the bare statement, both Steps 0 and 1 (the
dispatcher's named attack point).** I worked through this without reading the lane's proof text
first for the load-bearing steps:
- Step 0 (`ρ(Ω̄)⊆Ω̄ ⟹ J=ρ(J)`): confirmed the measure-zero argument
  (`λ(Ω̄\ρ(Ω̄))=0` since both have equal finite measure under an isometry and one contains the
  other), confirmed `Ω\ρ(Ω̄)` is open and null hence empty, confirmed the closure chain
  `Ω̄⊆ρ(Ω̄)⊆Ω̄` forcing equality, and confirmed `∂Ω̄=∂E=J` is the right identity to take boundaries
  through (using `Ω̄=R²\E`).
- Step 1 (`ρ(J)⊆Ω̄ ⟹ J=ρ(J)`): confirmed `E` (connected, unbounded, disjoint from `ρ(J)`) must lie
  in the unbounded component of `R²\ρ(J)`, which is `ρ(E)` because `ρ` is an isometry so `ρ(Ω)` is
  bounded and is therefore the *bounded* component; this gives `ρ(Ω̄)⊆Ω̄` and Step 0 finishes it.
- The five-step main proof: I specifically checked the place I expected trouble — Step 3's use of
  "Step 1 with the roles of `J` and `ρ(J)` exchanged" — by writing out Step 1 as a *general*
  lemma (any Jordan curve `K`, any homeomorphic isometry `τ`: `τ(K)⊆K̄ ⟹ K=τ(K)`) and instantiating
  it at `K=ρ(J)`, `τ=ρ^{-1}`. The hypothesis becomes exactly `J⊆ρ(Ω̄)` (since `Ω̄_K=ρ(Ω̄)` and
  `τ(K)=ρ^{-1}(ρ(J))=J`), and the conclusion `K=τ(K)` becomes `ρ(J)=J`. This is legitimate and I
  could not find a hidden asymmetry in it.
- I could not break Lemma 3. I tried the obvious failure points (unbounded-component uniqueness
  invoked twice, at `J` and `ρ(J)` — both licensed by JCT applied to a genuine Jordan curve each
  time, since `ρ` is a homeomorphism of the plane and image of an injective map stays injective)
  and found nothing.

**Theorem 3, the 17-vertex witness — rebuilt end to end with a decider sharing no code with either
of the lane's two.** I wrote a complete `Fraction`-based $\mathbb Q(\sqrt3)$ decider (source below)
and ran it on the exact polygon:

```
simple: True
vertex 0 (O): EXCEPTIONAL
vertices 1-16: all good, each with a rotation-witness independently produced by my code
```

This matches the lane's claim exactly. I additionally re-verified, in exact `Fraction` arithmetic,
every hand-computed rational identity the proof depends on:
- `⟨a_k, a_{k+1}−a_k⟩ = (3/5)|a_k|²` at every `k=0..6` (radial monotonicity of the inner chain) —
  confirmed exactly, term by term.
- `a₈ = 2a₇` (final segment is radial) — confirmed.
- `(9/10)|a₈|² − |a₇|² = 53248/5 > 0` (the cap stays outside radius `2⁶`) — confirmed.
- `c=⟨a₁,a₃⟩=28/25>0` and `s²−3c²=6864/625>0` (angle `∠a₁Oa₃ > 60°`, hence not wedge-type) —
  confirmed exactly.

Three independent deciders (theirs, theirs, mine) plus a from-scratch check of every rational
hypothesis in the hand proof all agree. I looked hardest here because this is the claim that
overturns another lane's `sketch`, and I could not find anything wrong with it.

**Where I did not go further.** Theorem 2 (angle-sum, at most two wedge-type points) and Lemma 2
(polygon local structure) are short and I checked them by hand rather than by code; found no issue.
§8's negative claims (why the count doesn't close) are arguments that a route fails, and I agree
with the specific failure reasons given (Lemma 1's criterion is per-circle, so exceptionality at
`O_i` says nothing about the angle `O_i` subtends at the other two points) — but "I could not find
a way to make the angle-sum argument work either" is not a proof that no argument exists, and I
flag that as inherently unfalsifiable by a reviewer in finite time, exactly as the lane itself says.

## Lane 2 — `attacks/exceptional-pair-rigidity/` — outcome: survived; one step not independently re-derived

**W0/W1/W2, re-derived from the theorem statements alone (not read-and-agreed).** The advertised
regularity budget is "none at all" — no convexity, no closedness beyond turning a sup into a max —
which the brief correctly flagged as exactly where a hidden hypothesis would hide. I rebuilt:
- W0: the law-of-cosines bound `|XY|²≤a²+b²−ab` on `[0,R]²`, and confirmed by direct calculus
  (convex in each variable separately, so max at a corner of the square) that the maximum is `R²`,
  attained only at `(R,0),(0,R),(R,R)`.
- W1: re-derived the collinear/non-collinear case split at Step (i) myself; the non-collinear case
  uses "larger angle opposite longer side," which I confirmed is licensed by the law of sines
  (`a/sin A = b/sin B` — larger sine, since angles here are `≤180°` and one of `∠XO₁O₂,∠XO₂O₁` is
  `≥60°` iff the other is `≤120°`, giving comparable sines only when both angles are `≤90°`; I
  checked the edge case where one of the two angles could exceed `90°` and confirmed law-of-sines
  still gives "larger angle → longer or equal opposite side" for angles in `(0°,180°)`, which is
  the correct generalization of "larger angle opposite longer side" beyond acute triangles).
- W2, the case `O₁∉{X,Y}`: I independently verified by direct optimization (not by reading the
  lane's argument) that `f(a,b)=a²+b²−ab` on `[0,d]²` attains its maximum `d²` **only** at
  `(d,0),(0,d),(d,d)` — fixing `b` and noting `f` is convex in `a` so the max over `a∈[0,d]` is at
  an endpoint, then checking each endpoint branch (`a=0`: `f=b²`, max `d²` only at `b=d`; `a=d`:
  `f=d²+b(b−d)`, and `b(b−d)≤0` on `[0,d]` with equality only at `b∈{0,d}`) — confirming the
  three-point solution set exactly as claimed.

**Pentagon C2 — exceptionality independently re-decided, not just the arithmetic.** The prompt says
the dispatcher already checked the distance arithmetic (725 vs 800); I decided the actual
good/exceptional verdicts with my from-scratch decider:

```
vertices: (-10,-4) good, (-5,-14) EXCEPTIONAL, (1,-4) good, (18,0) EXCEPTIONAL, (-2,5) good
max dist^2 pair: (-10,-4)-(18,0), 800   [the diameter]
exceptional pair: (-5,-14)-(18,0), dist^2 = 725
```

Matches exactly: the exceptional pair is not the diameter pair. I also checked the "mixed pair"
claim — that `(18,0)` is wedge-blocked and `(-5,-14)` is not — with a direct (float) angular-span
computation over the vertex directions: `(18,0)` spans ≈45.4°, `(-5,-14)` spans ≈85.2°, matching
the lane's reported figures and confirming one is under 60° and the other is not.

**The `|E|=1` witness, re-decided.** Triangle `(0,0),(5,0),(2,4)`: my decider agrees exactly — `(5,0)`
is the sole exceptional vertex, the other two are good with exact witnesses my code produced
independently (not the lane's). I also confirmed the lane's hand angle test
(`4(u·v)²` vs `|u|²|v|²`) algebraically: at `(5,0)`, `900>625` (angle `<60°`, exceptional); at
`(0,0)` and `(2,4)`, `400<500` (angle `>60°`, good).

**Not independently re-derived.** §6's parenthetical transfer step — that the triangle W2 produces
for `S=K` (compact convex body) actually has its other two vertices on `∂K` rather than merely in
`K`, needed to carry Corollary C2 from `S=K` to `J=∂K` — I read this and found it plausible (a
point of `K` at maximal distance from a fixed point must lie on `∂K`, which is immediate from
compactness and the definition of boundary for a set with nonempty interior) but did not write out
a fully independent proof of it. This is a small step and I do not think it hides an error, but per
§5's discipline I record it under `not-checked` rather than waving it through.

## Lane 3 — `attacks/extremal-size/` — outcome: Theorem C's elementary core survives; the two
self-flagged steps are plausible but not fully closed by me either

**Lemma W, Corollary U, Theorem D (degeneracy) — re-derived, no issues.** These use no regularity
at all (arbitrary bounded sets), and the L-hexagon witness kills every hull-continuous
normalization at once. I rebuilt the exact computation independently — my own exact maximizer,
computing `max{|OX|² : X ∈ P ∩ ρ_{O,60°}(P), X≠O}` via full edge-pair intersection (not sampled
points, the *entire* continuous boundary):

```
delta=1/10:  exact max side^2 at O=(0,0) = 2/25 + 1/25*sqrt3  =  (8+4sqrt3)*(1/10)^2   exactly
delta=1/20:  exact max side^2 at O=(0,0) = 1/50 + 1/100*sqrt3 =  (8+4sqrt3)*(1/20)^2   exactly
delta=1/50:  exact max side^2 at O=(0,0) = 2/625 + 1/625*sqrt3 = (8+4sqrt3)*(1/50)^2   exactly
```

This is a **stronger** check than the lane's own (which sampled 240 points per curve): my
computation finds the true exact maximum over the whole continuous boundary via segment
intersection, and it lands exactly on `(√6+√2)δ` in every case, confirming both the closed form and
that the lane's Lemma L upper bound is off by exactly the stated factor of 2. I also checked every
vertex as a candidate `O` and confirmed `(0,0)` is indeed the maximizer among vertices (0.149 vs
0.013 for the others at `δ=1/10`), consistent with the lane's claim that `(0,0)` attains it.

**Theorem C (the lower bound `m(K)≥√3·r`) — the elementary chain (Steps 1–3) re-derived and holds;
Step 0 (reduction to strictly convex) not independently re-derived in full.** I rebuilt Steps 1–3
by hand from the statement:
- Step 1: confirmed the tangent-line-at-a-contact-point argument gives the half-plane containment
  and the chord bound `R(θ)≥2r cos θ` — this is the standard incircle-chord fact, and I verified it
  directly (a chord through a point of tangency of a circle of radius `r`, at angle `θ` to the
  diameter through that point, has length `2r cos θ`, and that segment lies in `K` since
  `D(O,r)⊆K`).
- Step 2 (the criterion via `g(θ)=R(θ+60°)−R(θ)`, IVT on `[-90°,30°]`): confirmed
  `g(-90°)=R(-30°)>0` and `g(30°)=−R(30°)<0` directly from `(∗)`, giving a nonempty compact zero
  set and a well-defined `c=max_Z R(θ)>0`.
- Step 3 (the contradiction if `c<√3r`): re-derived the angle arithmetic myself —
  `β=arccos(c/2r)∈(30°,90°)` forces `θ≤−β` and (`θ≥β−60°` or `θ≤−60°−β`), and checked both
  disjunction branches are incompatible with `θ≤−β` and `θ≥−90°` respectively using `β>30°`.
  Confirmed `Z=∅`, contradiction. This step is correct as far as I can tell.
- Step 0 (Minkowski-sum reduction `K_n=K+\frac1n D` to strict convexity, then a Hausdorff-limit
  passage back): I read this and it is a standard technique (a Minkowski sum with a disk has no
  boundary segments unless the original had a segment parallel to one in the disk, which has none),
  and the noncollapse bound (`side ≥ √3·r(K_n) = √3(r+1/n) > √3 r > 0`, uniform along the sequence,
  established before the limit) is exactly the discipline problem `RULES.md` §2 demands. I did not,
  however, write out my own independent proof that the vertex limits land on `∂K` rather than
  merely in `K` — I read the argument given (a limit inside `int K` would put a ball inside `K_n`
  containing the vertex, contradicting the vertex being on `∂K_n`) and find it plausible, but this
  is the second of the lane's own two self-flagged weakest steps and I did not close it
  independently. **Not-checked**, load-bearing.
- The continuity claim (`θ↦A+R(θ)u(θ)` a continuous bijection onto `∂K\{A}`, up to the closed
  endpoints `θ=±90°`) is the *first* self-flagged weak step. I worked through the semicontinuity
  argument the lane gestures at (upper from closedness of `K`, lower from strict convexity) and it
  looks right for the *open* interval; I did not personally nail down continuity *up to and
  including* the closed endpoints `±90°`, which is exactly what makes `g` continuous on the full
  closed interval and the IVT usable at the endpoints in Step 2. This is the step I'd send back for
  another pass — see the objection below.

**The disk-not-extremal claim.** Correctly and explicitly float-based by the lane's own admission;
I did not attempt to certify it and agree it should not be certified as stated. What would certify
it: an *exact* maximizer of the inscribed equilateral side over a general convex body (not just
polygons), since the disk itself has no rational or `Q(√3)` parametrization compatible with the
existing exact machinery — this is a real tooling gap, not a quick fix.

**Lemma B (`w≤3r`)** — read, matches the classical proof sketch, not independently re-derived line
by line (ordinary convexity-geometry folklore, low risk).

## Lane 4 — `attacks/scalene-shapes/` — outcome: Proposition 1 re-derived and confirmed exactly;
Theorem C(1)'s self-flagged weak branch re-derived and found, on reconstruction, to be the *easier*
half rather than a hidden gap

**Proposition 1 (six-multiplier criterion), re-derived completely independently — this was
priority #1 per the lane's own attack list.** Working from the definition of similarity alone
(not reading §1.2's proof), I derived the twelve raw values of `μ=(X−O)/(P−O)` arising from the
six permutations of `(0,1,w)` assigned to `(v₀,v₁,v₂)=(O,P,X)` under a direct similarity:

```
(0,1,w) -> w        (0,w,1) -> 1/w
(1,0,w) -> 1-w       (1,w,0) -> 1/(1-w)
(w,0,1) -> (w-1)/w   (w,1,0) -> w/(w-1)
```

exactly matching the lane's own listing, plus the conjugate six from indirect similarities. I then
confirmed the three inverse-pairs directly (`w↔1/w`, `1−w↔1/(1−w)`, `(w−1)/w↔w/(w−1)`, and their
conjugate images), and confirmed the collapse `S∩σ_μ(S)≠{O} ⟺ S∩σ_{1/μ}(S)≠{O}` via the swap
argument (apply `σ_μ^{-1}=σ_{1/μ}` to a witness point). This exactly reconstructs the six-element
`M(w)` and I found no missing or extra role. §1.4's one-line explanation of why equilateral
collapses to one condition (`μ^{-1}=μ̄ ⟺ |μ|=1`) checks out algebraically by direct computation.

**Theorem C (convex, every shape) — re-derived the extreme-direction dichotomy and the "attachment"
argument, the lane's own self-flagged riskiest step, by hand, focusing on the untested `L=0`
branch.** I worked through clause (1)'s proof (`φ₁<γ(O) ⟹ O` good) from the bare statement:
- If `L₀:=lim_{θ→0⁺}R(θ)=0`, then `h(θ)=R(θ+φ)/R(θ)→R(φ)/0=+∞` directly (since `R(φ)>0` is a fixed
  continuous value, `φ` being interior to the cone as `θ→0`), giving `sup I=∞` with **no attachment
  argument needed at all** — this is in fact the *simpler* of the two sub-cases, not the fragile
  one.
- If `L₀>0`, the extreme-direction dichotomy forces the whole segment `(0,L₀]` onto `J` at
  direction `0`, and pairing points on that segment (radius `t→0⁺`) against the fixed point at
  direction `φ` gives ratios `R(φ)/t → ∞`, so `[R(φ)/L₀,∞)` is realized regardless of how large
  `L₀` is, and `b=R(φ)/L₀=lim_{θ→0⁺}h(θ)∈closure(I)`. I checked the general topological fact used
  implicitly here — if `A` is an interval and `b∈closure(A)`, then `A∪[b,∞)` is connected (hence an
  interval) — and it holds without qualification.
- Symmetrically at the other end, and the two attachments plus `I` together form a connected set
  with infimum `0` and supremum `∞`, which (being a subset of `ℝ`) must be exactly `(0,∞)`,
  containing the target ratio `k`.

**So I tried specifically to break the branch the lane named as least-tested (no polygon exercises
`L=0`, since a polygon's extreme directions always carry a segment) and could not — on
reconstruction it is the case that resolves *without* the attachment machinery at all, so if there
is an error in Theorem C(1) I do not think it lives where the lane's own flag points.** This is a
genuine, useful finding either way: either the self-flagged risk was misplaced (worth recording so
the next reviewer doesn't spend time there), or I am missing something subtler in the same step
that neither of us has located yet.

**Not independently re-derived from scratch:** Lemma A_σ (§2), the spiral-similarity nesting lemma.
I read it closely rather than rebuilding it cold, but it is structurally the `k<1` generalization of
exactly the Lemma 3 argument I *did* rebuild from scratch for Lane 1 (same three-way case split on
which side of `J`/`σ(J)` the punctured curve falls, same use of connectedness + JCT), and the one
genuinely new step — the asymmetric conclusion that only the *shrinking* nesting survives for `k<1`
— follows from a one-line measure inequality (`λ(Ω̄)≤k²λ(Ω̄)` is impossible for `k<1`, `λ(Ω̄)>0`
finite) that I did check directly. I count this as "reconstructed by close analogy plus a spot
check of the one new step," short of a fully independent line-by-line rebuild.

**Not checked at all:** Proposition 3's one-dimensional extremal-measure computation (§3.1, the
`f=max(1+q²f, qf)` self-similarity argument) — I read it, it looks like a standard
max-weight-independent-set-on-a-path argument and the lane's own DP cross-check matches the closed
form to six decimal digits, but I did not re-derive the self-similarity recursion myself.

## What I would flag as the single most useful thing for the next worker to check

In `extremal-size`, Theorem C's Step 0 (Hausdorff limit reduction) and Step 1's continuity claim
*at the closed endpoints* `θ=±90°` are the two places I read rather than independently proved, and
they are exactly the two the lane itself flagged. I did not find an error, but I did not close them
either, and a proof standing on two unclosed self-flagged steps is not the same as a proof I have
verified end to end.

## Source of the independent decider (for reproduction)

Written fresh in this session, sharing no code with any committed enumerator or any of the four
lanes' own deciders: `Q3` class for `p+q√3` arithmetic (`Fraction`-based, syntactic zero test, sign
by same-sign-shortcut or `a²` vs `3b²`), exact segment-segment intersection via Cramer's rule with
a collinear-overlap branch, `rot60` via the exact rotation matrix `(1/2, √3/2; -√3/2, 1/2)`, and an
`is_good`/`is_simple` decider operating on the full polygon (every edge against every rotated edge,
not a sampled point set). Used to independently re-decide: the 17-vertex spiral-channel witness
(Lane 1), the pentagon C2 and the `(0,0),(5,0),(2,4)` triangle (Lane 2), and the exact L-hexagon
maximizer (Lane 3, extended to compute the true maximum over full edges rather than sampled
points). All results matched the lanes' claims exactly, with no disagreement found anywhere.
