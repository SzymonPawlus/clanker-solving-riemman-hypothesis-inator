# 2026-08-30 — inscribed equilateral triangle, ideation round 2 (journal)

Worker: ideation lane, `claude` (Fable 5), branch `claude/inscribe-equilateral-triangle-oj15x1`.
Output file: `problems/inscribed-equilateral-triangle/attacks/ideation-round-2/README.md`.
Everything here is scratch: speculation and derivation notes, nothing assumable, nothing with a
status above `sketch` even where a derivation looks complete.

## What I read, in order

RULES.md (§6, §8 in particular), problems/inscribed-equilateral-triangle/README.md and RULES.md,
ideation-round-1 in full, then the seven changed attack READMEs in full or at depth
(rectifiable-case and spiral-tip-witness line by line; exceptional-set-polygons §§0,6,7.4–9,13,14;
exceptional-pair-rigidity header + result table + outline; half-density header + outline;
extremal-size header + §5, §11; scalene-shapes header + §11, §12; polygon-count-closure whole;
round3-cross-review verdict blocks), plus the dispatcher journal's round-2 synthesis section.

## Constraints I wrote down before generating

- Eight lanes running: Θ-family classification of non-wedge points; anti-classification;
  |E(P)| ≤ 2 for polygons; the ≥3-point hunt; closing the convex extremal bracket; breaking it;
  exact maximiser tooling. **None of these may be proposed.** Where an idea's natural
  continuation lands in one of those, the idea must state its stop-line.
- Round 1's thirteen ideas may not be re-proposed, including the unexecuted ones
  (I4 convex arcs, I7 modulus, I8 orientations, I9 spectrum S(J), I10 Σ(J) census, I11 dendrites).
- The round-1 lesson, applied as a ranking rule: prefer ideas whose failure teaches. I1
  ("strictly stronger") failed silently; I2 (concrete construction) over-delivered. So concrete
  objects and guaranteed-partial-deliverable ideas outrank grand criteria.

## Derivation scratch

### Small-apex theorem (README II1)

Claim: for every Jordan curve J there is α₀ > 0 with (0°, α₀) ⊆ A(O) for every O ∈ J.

Route: fix O ∈ J. λ(Ω ∩ ρ_{O,α}Ω) = λ(Ω) − λ(Ω \ ρ_{O,α}Ω) ≥ λ(Ω) − λ(Ω Δ ρ_{O,α}Ω).
The isometry ρ_{O,α} moves each x ∈ Ω̄ by |ρx − x| = 2 sin(α/2)·|x − O| ≤ α_rad · diam(Ω̄).
For indicators of bounded measurable sets, λ(Ω Δ τΩ) → 0 as the sup-displacement of the
isometry τ → 0 (approximate 1_Ω in L¹ by f continuous with compact support; uniform continuity
of f gives ∫|f∘τ⁻¹ − f| → 0 uniformly over such τ; triangle-inequality the three error terms).
The bound depends only on the displacement, hence is uniform over O ∈ J. Choose α₀ with
λ(Ω Δ ρ_{O,α}Ω) < λ(Ω) for all α < α₀ and all O ∈ J. Then Ω ∩ ρ_{O,α}Ω ≠ ∅, and the region
lemma's contrapositive (Lemma A / Lemma 3 — sketch in three lanes, would be re-derived in any
executing lane) gives J ∩ ρ_{O,α}J ⊋ {O}: a witness x ≠ O with |Ox| = |O ρ⁻¹x| and angle α,
i.e. an inscribed isosceles triangle with apex angle exactly α, nondegenerate since α ∈ (0°,180°)
and |Ox| > 0.

Consistency checks run against the finished lanes before I believed it:
- Spiral tip: Corollary 5 of spiral-tip-witness says apex angle θ realisable iff θ ≤ β. So
  A(O) = (0, β], α₀(J_{c,β}) ≤ β > 0. Consistent, and the invariant α₀ is exactly β there.
- 30–30–120 apex: wedge of opening 30° caps A(O) ⊆ (0°, 30°]; the theorem only claims small
  angles are realised. Consistent.
- Rectifiable curves at unit-speed differentiability points: rectifiable-case §9.2 gives
  A(O) ⊇ (0°, 120°]. Consistent (stronger, under stronger hypotheses).
- The theorem does NOT contradict exceptionality at 60°: it only says α₀ > 0, not α₀ > 60°.

The multiplier extension (|μ| ≠ 1 near 1): the same measure-continuity argument gives
λ(Ω ∩ σ_μΩ) > 0 for μ near 1, but Lemma A_σ (scalene-shapes §2) has the shrinking-nesting
alternative for |μ| < 1: σΩ̄ ⊆ Ω̄ touching only at O would have Ω ∩ σΩ = σΩ ≠ ∅ *without* a
curve intersection. So the off-circle extension is genuinely open, and "can nesting block
multipliers arbitrarily close to 1" is a good sub-question for the lane. At the spiral tip the
band |arg μ + ln|μ|/c| ≤ β is a full 2-D neighbourhood of 1, so no blocking near 1 there.

### Density-point lemma (README II2)

S measurable, O ∈ S, some ball B = B(O,r) with λ(S∩B) > ½λ(B). ρ = ρ_{O,60°} preserves B and λ,
so λ(ρ(S)∩B) = λ(S∩B), and λ(S∩ρ(S)∩B) ≥ 2λ(S∩B) − λ(B) > 0. Positive measure ⟹ contains a
point x ≠ O; Lemma R turns (x, ρ⁻¹x, O) into a nondegenerate equilateral triangle in S.
Checked the inclusion–exclusion twice; checked that ρ(S∩B) = ρ(S)∩B needs only that ρ fixes O
and preserves B(O,r), which it does.

Density theorem step: J closed ⟹ measurable; if λ₂(J) > 0 then a.e. x ∈ J has density 1 in J
(Lebesgue density theorem), so some ball at x has λ(J∩B) > ½λ(B). Hence λ₂-a.e. point of a
positive-area Jordan curve is a vertex. NOTE: "Osgood 1903" for positive-area Jordan curves is
a *memory* attribution — flagged unverified in the README per problem RULES §6.1; it is a
search target for the literature lane, not a citation.

The square near-miss, recorded so nobody trips on it later: with rotations by 90°, 180°, 270°
simultaneously, density > 3/4 at O gives a point whose whole 4-orbit lies in S — an honest
square. But no measure-zero curve has density > 3/4 anywhere, and the square peg problem's
difficulty is entirely at measure zero, so this is not progress on anything; it is the
quantitative reason the density mechanism stops at "isosceles" for curves (a pair costs
density ½, which positive-area curves can pay; a 4-orbit costs ¾ — payable too, actually, by
fat Osgood curves… so the 90° version DOES give: density-¾ points of a positive-area set have
inscribed squares-with-center-O? No — the 4-orbit {x, ρx, ρ²x, ρ³x} is a square centred at O,
NOT a square with vertex O, and O itself need not be a vertex of anything. Re-checked: the
four orbit points are the square's vertices and all four lie in S; O is the centre. So a
positive-area set has squares (as vertex sets) centred at each of its density-¾ points. True,
trivial for fat sets, irrelevant to square peg (curves have measure zero). Recorded and
closed.)

### Disconnected unions: |E| = 2n exactly (README II3(i))

n copies of the 30–30–120 boundary, diameter 1, centres at (10^k, 0), axes along x.
From any 30° apex: own triangle at radii (0,1] with direction spread 30° (exceptionality of
the isolated triangle is the repo's exact witness, rotation-continuity §3); triangle T_j at
distance d ≈ |10^k − 10^j| ≥ 9 occupies radii [d−1, d+1]; these intervals are pairwise
disjoint and disjoint from (0,1] (checked: distances 10^j − 10^k differ by ≥ 8·10^{max−1} ≫ 2).
Same-circle pairs are therefore always within one component; within T_j the angular spread
seen from the apex is ≤ 2 arcsin(1/(2(d−1))) < 2° < 60° (float sanity run in scratchpad:
own radii (0,1], far radii [10,11], far spread 1.57°). No circle carries a 60° pair. So all
2n apexes are exceptional. With components shrinking and accumulating, E infinite.
This must be verified exactly (Q(√3)) by the executing lane — the deciders intersect segment
lists and never use simplicity, so the extension is mechanical.

### The bowtie discard (README D2) — killed during generation

First version of the connectivity idea: join two 30–30–120 triangles at their 120° apexes
("bowtie"), hope all four 30° tips stay wedge-blocked. Killed before write-up by
exceptional-set-polygons Theorem 2, which is point-set: three wedge-type points form a triangle
with angles < 60° each — impossible. Worked the geometry anyway to see the failure concretely:
triangle A=(0,0), B=(1,0), C=(1/2, tan30°/2), second triangle reflected through C; from A the
reflected tip 2C−B = (0, tan30°) sits at direction 90°, far outside A's [0°,30°] cone. The
survivor construction is radius-separation (above), which Theorem 2 does not see because the
blocked points are not wedge-type (their direction sets are unions of two narrow arcs ~180°
or ~150° apart). Also noted: radius-separation is a *discontinuous-I_r* rotating wedge, not a
new mechanism — connectivity is exactly what forbids the discontinuity (no-sweep, Prop 5).

### R³ conical spiral (README II4(a))

Arm on the cone of half-angle φ = 30°: every sphere about O meets the arm once (radial
monotonicity as in the planar spiral), direction at constant angle 30° from the axis. Return
path inside a thin tube around the axis: directions within ε of the axis, so same-radius pairs
are (arm, tube): angle 30° ± ε ≠ 60° for ε < 30°; (tube, tube): < 2ε; (arm, arm): one point
per radius. In R³ nothing forces the return to spiral — the planar witness's whole difficulty
(spiral-tip-witness §4.1, the closing arc forced through the spiral channel) evaporates because
a curve does not separate R³. What still needs care in an executing lane: the junctions where
tube meets arm (radii near the outer closure), and Jordan-ness (injectivity) of the explicit
parametrisation. Also derived for the README: the wedge count survives in R^n (three wedge
points still span a planar triangle, angle sum 180°), and Theorem T's Lemmas 1–2 are
dimension-free while its endgame (interior arc) is planar-only — that split is the whole point
of II4(b).

### Robust vs grazing (README II5)

Robust: x ∈ Ω ∩ ρ_O(Ω) with ρ_O⁻¹x ∈ Ω. Both memberships are open in (x, O) jointly (Ω open,
ρ_O(x) continuous in both), so robust goodness is open in O — exceptional points accumulate
only at grazing points. Exact grazing example: corner O of the equilateral triangle T. T lies
in the closed 60° cone at O; ρ_{+60}T lies in the adjacent closed cone; open cones disjoint ⟹
Ω ∩ ρΩ = ∅; but ρ maps the edge at direction 0° onto the edge at direction 60°, so J ∩ ρJ
contains that whole edge: good, with a continuum of witnesses, all grazing. So grazing-good
points exist and are exactly computable on polygons.
Stop-line noted in the README: "is E(J) closed unconditionally" reduces to whether exceptional
points can accumulate at a grazing point, which needs infinitely many exceptional points —
the running hunt lane's territory escalated; the ideation entry must not propose it.

## Ideas considered and discarded before write-up, with reasons

1. **Θ(r)-realizability for the family {Θ(r)}_r at an exceptional point** — the primer names
   the inverse problem, but the family-level version IS the running classification /
   anti-classification pair. Discarded for lane collision; the single-radius version ("which
   closed subsets of S¹ arise as J ∩ ∂B(O,r) for one r") looked like trivia (almost any closed
   set, by decorating a curve) and was dropped as boring rather than colliding.
2. **Conjecture I (m ≥ √3·r(Ω) for general J)** — the surviving extremal normalisation, but
   "closing and breaking the extremal bound" lanes are running and this is their natural
   corridor. Ceded. II10 (uniform C¹ modulus) is the disjoint corridor I kept, with an explicit
   board-check gate.
3. **Witness-count parity on polygons** (is #(J ∩ ρJ \ {O}) generically even; a degree-theory
   germ) — this is Schwartz-shaped "topological information" and the likeliest overlap with
   both the unread paper and the classification lanes. Discarded.
4. **Translation-composition identity for exceptional pairs** (ρ₁ρ₂⁻¹ = translation) —
   already tried and recorded fruitless by exceptional-pair-rigidity §8.5. Re-examined in the
   A(O)-spectrum language for five minutes; still nothing couples the two spectra. Not
   re-proposed.
5. **Random / SLE-type curves, E(J) = ∅ a.s.** — no probabilistic machinery in-repo, no exact
   arithmetic possible, and the deterministic content (wild curves are good) is captured
   better by II2 and II9. Dropped.
6. **Symmetric curves** — the 3-fold-symmetry one-liner (O, ρ_{c,120°}O, ρ_{c,240°}O is an
   inscribed equilateral triangle for any curve invariant under 120° rotation about c, so
   E ⊆ {c} ∩ J) is real but too small to be a lane; folded into II6's Lean-fodder list.
   Checked the degenerate case: if c ∈ J (a symmetric curve through its own centre) the
   triangle at O = c degenerates and c's status is genuinely undetermined by symmetry — cute,
   noted, not pursued. Central symmetry (n = 2) gives nothing: the acute rhombus has two
   sub-60° opposite corners, |E| = 2, no improvement.
7. **Uniform wiggliness ⟹ good** (a "spread ≥ 60° at every scale ⟹ vertex" hope) — false at
   proposal time: the spiral tip has full spread at every scale and is exceptional. The
   criterion compares points on one circle; spread across scales certifies nothing. This
   discard is what re-routed the wild-curve hope through measure (II2) and through
   renormalisation on a specific curve (II9).
8. **A quantitative "turn budget" for channels** (minimum total rotation of I_r needed for a
   non-wedge exceptional point) — the trivial bound (≥ 360° − w to have full direction span)
   is immediate and anything sharper is classification-lane territory. Kept only as the
   ε_w-invariant census (II7), which is instrumentation rather than theory.

## Ranking rationale (against the round-1 lesson)

II1 over II3: both have guaranteed deliverables, but II1's worst case (the small-apex proof
breaking) would be a repo-level event touching Lemma A, whereas II3's worst case is a merely
empty search. II2 third despite near-zero risk because its ceiling is lowest; it is ranked at
all because the repo currently has zero Lean-track positive statements and it is the cheapest
one that could exist. II5 is the reserve — its openness lemma is as safe as II2's and its
census is cheap, but its deep half is fenced off by a running lane, capping the payoff.

## Honest uncertainty

- The small-apex theorem's uniform-α₀ step leans on uniform L¹-continuity of the indicator
  under isometries with small displacement. I believe the standard argument covers it; it is
  the step an executing lane should nail down first, and the step I would attack as a
  cross-examiner.
- The 2n-tips construction was checked by hand and by one float sanity run only; the README
  labels it bankable-after-exact-check, not banked.
- Every "known?" percentage in the README is a guess from zero primary sources. The two I am
  least sure of: Meyerson's coverage of figure-eights (his title is the only evidence either
  way), and GRS's coverage of the R³ smooth question (their abstract's "a condition under
  which" could be exactly II4(b) or could be orthogonal).
