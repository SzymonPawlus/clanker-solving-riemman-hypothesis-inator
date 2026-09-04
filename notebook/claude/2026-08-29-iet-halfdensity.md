# 2026-08-29 — the half-density obstruction (idea I1), working journal

Worker: `claude` (Claude Opus 5), branch `claude/inscribe-equilateral-triangle-oj15x1`.
Lane files owned: `problems/inscribed-equilateral-triangle/attacks/half-density-obstruction/{README.md,KILL-CRITERION.md}`
and this file. Nothing else touched; ran no git command (the dispatcher commits).

Result summary is in the attack README §0. This file is the working record: order of events, the
things I got wrong on the way, and the things I decided not to do.

---

## 1. Reading, before anything

`RULES.md` §0/§3/§7; then the problem `README.md` and `RULES.md`; then, in the attacks tree,
`ideation-round-1/README.md` §I1, `rotation-continuity/README.md` (all of it — it is the lane my
chain sits on top of), `convex-vertex-criterion/README.md` (§0–§2, enough to know what Theorem
A/B claim and that they are convex-only). Also skimmed `experiments/inscribed-triangle-polygons/`
README + `geom.py` + `k3.py` to learn the decider's API, since my brief lets me read and run it
but not modify it.

Two facts from that reading shaped everything after:

- the problem `RULES.md` §6.3 says Mathlib has no JCT, so anything downstream of Lemma A is not a
  Lean target and `verified:review` is the right ceiling for it;
- the rotation lane's §7.1 already records that the measure argument kills only *nesting*, and
  that the externally-tangent configuration is real. So I knew before starting that I was not
  going to get a general theorem out of this, only a criterion.

## 2. The core lemma — I started down the wrong road, then noticed

My first half hour went into the brief's polar-coordinate route: sections `A_r`, disjointness on
the circle, inclusion–exclusion `|A ∩ (A+60°)| ≥ 2|A| − 360°`, Tonelli. It all works. I wrote out
the measurability discussion (`A_r` open for every `r`, no a.e. needed) and the `C₆`
independent-set analysis of the sharp constant, and then, while writing the integration step, saw
that the integration is pointless:

> `ρ` maps `B(O,R)` onto itself. So `W = V ∩ B(O,R)` and `ρ(W)` are two disjoint subsets of
> `B(O,R)` of equal measure. Therefore `2λ(W) ≤ λ(B(O,R))`. Done.

Two lines, no coordinates, no angle, and it holds for **any** isometry fixing `O` in **any**
dimension. That is now §3.1 of the README, and the polar route survives only as §3.2 because the
per-circle statement it produces is genuinely stronger than the ball statement (§5.3) — that is
the one thing the detour buys.

I record the detour because the brief said "getting the inclusion–exclusion right is most of the
mathematical content, and I do not know the answer". The truthful answer is that the
inclusion–exclusion is correct, is not needed, and the "content" is a bookkeeping identity.

**The sharp constant.** The brief hoped for `1/6` from six-fold rotation. It is `½`, attained, and
the six-fold hope is structurally dead: the extremal set
`A* = (0,60) ∪ (120,180) ∪ (240,300)` satisfies `A* + 120° = A*` exactly, so the six translates
are nowhere near pairwise disjoint. Cleanest framing: rotation by `60°` cuts the circle into
`6`-element orbits, the hypothesis says `A` meets each orbit in an independent set of `C₆`, and
`α(C₆) = 3`. Deeper reason, and the one that caps the method: **the proof never uses the angle**,
so it cannot see the order of the rotation, so no measure argument of this shape can beat `½` for
any angle. Wrote that into §3.3.

**The one place with content.** Chasing whether `½` is attainable *by an exceptional point* — not
just by an abstract set — gave the only real theorem in §3. `Ω̄` is closed, and a closed
`B ⊆ S¹` with `B ∩ (B+α) = ∅` and `|B| = 180°` forces `B ⊔ (B+α)` to be a closed set of full
measure, hence all of `S¹`, exhibiting the circle as a disjoint union of two nonempty closed sets.
The circle is connected. So `|B| < 180°` **strictly**, and the same argument in the disc (using
connectedness of the *punctured* disc, since `O` itself is in both `Ω̄` and `ρΩ̄`) gives strict
density. Consequence: the criterion can be stated with `≥ ½`, not `> ½`, and with `Ω̄` rather than
`Ω` — which is not vacuous, because Osgood curves have positive area.

This is the one respect in which I improved on I1 rather than deflating it.

## 3. Lemma A

Derived it before re-reading the rotation lane's proof closely, exactly as §3 and §6.2 demand.
Landed in the same place. The one difference: at the end of Case A they take complements to get
`E = E'` and then boundaries; I took interiors, using `int(Ω̄) = Ω` (which needs `J = ∂E`, i.e.
the second JCT fact). Same content, and I would not claim my version is better — but deriving it
rather than reading it is what makes the agreement worth anything.

Things I checked deliberately, because §6.2 names them:

- `J' = ρ(J)` really is a Jordan curve with interior `ρ(Ω)` — `ρ` is a homeomorphism of the
  plane, so this is safe. If anything in Lemma A were going to be smuggled, it would be here.
- No crossing/parity/degree step anywhere. Good: that is what lets it survive wild curves.
- No limit anywhere in the whole lane, so §2's noncollapse obligation is free — the triangle in
  §6 has an explicitly named positive side.
- The measure step is used exactly once and only to upgrade an inclusion to an identity.

If Lemma A is wrong, my bet is `int(Ω̄) = Ω` in Step 2, since that is the JCT-flavoured input.
I could not break it.

## 4. The criterion hierarchy, and I1's ranking being wrong

Writing the criteria out side by side made the ordering obvious and made I1's triage line
("strictly stronger than the sector criterion") false:

```
O is a vertex  ⟺  Ω̄ ∩ ρΩ̄ ⊋ {O}  ⟺  ∃r: B_r ∩ (B_r+60°) ≠ ∅      (an iff)
     ⟸ ∃r: |B_r| ≥ 180°            (per-circle)
          ⟸ ∃R: density ≥ ½        (ball; I1's form)
     ⟸ a closed 60° sector in Ω̄    (rotation lane Lemma B)
```

The sector criterion fires at the `120°` vertex of the `30-30-120` witness, where the density is
`0.1378`; the density criterion fires on the pinwheel, where no sector exists. **Incomparable.**
Also, I1's ball form strictly loses information against the per-circle form — the domain
`{0.9<r<1, 0<θ<190°} ∪ {0<r<0.9, 0<θ<10°}` has `|B_r| = 190°` yet density at most `0.123`.

Per the kill-criterion file this is explicitly *not* a kill (§3 of that file), but it does mean
the lane's headline should be "new coverage in the non-convex world", not "stronger criterion".

Then the deflating observation: **a convex curve can never trigger it**, because a supporting line
at `O` puts the whole body in a half-plane, so density `≤ ½` always and `|B_r| ≤ 180°` always.
Since the convex case is exactly where this repo already has an iff (the convex lane's Theorem B),
the density criterion adds nothing precisely where we are strongest. Checked exactly on 200 seeded
convex fixtures, 805 vertices, 0 failures.

## 5. The pinwheel — one genuine scare, then it worked

**The scare.** I1's picture is "four petals of angular width ~50° near `O`". My first reaction was
that this is impossible: four petals *apexed at `O`* would put eight boundary arcs at `O`, and a
Jordan curve `J` has `J\{O} ≅ ℝ`, whose two ends are all the arcs that can reach `O` — so at most
two, so at most one petal. I was about to write the idea up as refuted on those grounds when I
re-read I1 and saw it already says "one touching `O`, the other three truncated at tiny inner
radii". So the picture is sound and my objection only rules out a version nobody proposed. Kept
the remark in README §6.1 because the drawing genuinely invites the impossible version.

**A design I dropped.** Before the polygon I worked out a cleaner continuous witness: the
logarithmic-spiral band `{0<r<1, θ − c·log(1/r) mod 360° ∈ (0°,200°)}`, closed up outside. Its two
spiral edges are rectifiable arcs ending at `O`, it is simply connected, its density at `O` is
`200/360 = 5/9` at *every* scale, and no sector of **any** positive aperture lies in `Ω̄` (the
band rotates past every direction infinitely often as `r → 0`). It is a strictly better separation
than the polygon. I dropped it as the headline witness because §5 of the problem `RULES.md` wants
exact arithmetic and a polygon the committed decider can adjudicate, and I did not want a witness
whose Jordan-ness rests on my own prose. Recording it here because it is the right object if
someone ever wants the *sharpest* statement of the separation, and because it overlaps the
spiral-tip lane (`attacks/spiral-tip-witness/`, another worker) — they should own any spiral
construction, not me.

**The polygon.** Built the 4-arm pinwheel with rational unit-circle directions. First attempt was
**not simple**: I had arm 0 closing through an inner arc at radius `δ` *and* running to `O`, which
made the first and last edges cross. `is_simple` from the committed `geom.py` caught it
immediately, which is the whole reason to use someone else's checked code for the predicates.
Second attempt: 21 vertices, all coordinates with denominator ≤ 50 (Pythagorean directions
`(3/5,4/5)` etc.), everything exact:

```
simple, 21 vertices; interior angle at O: cmp60 = -1 (53.13°)
R² = max|v−O|² = 1  exactly (P ⊆ closed unit ball)
area = 1723/1000 exactly;  (π/2)·R² < 1.5708  ⟹  density > ½ certified (≈ 0.5484)
ε² = 4/125 to the nearest non-incident edge ⟹ no 60° sector at O at any radius
committed decider: good = True, verified_ok = True, side² = 252/169 − (54/169)√3
independent certificate: x = (39/200,−84/125) ∈ Ω and ρ⁻¹x ∈ Ω, equal radii, exact
```

The area coming out as `1723/1000` on the nose was luck from the small denominators; the first
(finer, 137-vertex) version had an area with a ~400-digit denominator, which was correct but
unpublishable. Coarsening to eight Pythagorean directions cost nothing — the margin over `π/2` is
still ~10%.

Note the arm width is `53.13°`, not `50°`: that is `arccos(3/5)`, the price of exact rational
directions. Still `< 60°`, which is all the argument needs, and the `< 60°` test is exact
(`s² < 3c²` with `c > 0`), not a float comparison.

## 6. Refutation attempts

Wrote `KILL-CRITERION.md` before running anything, with three pre-registered predictions. All
three held:

- **A**: the pinwheel exists and the decider agrees `O` is good. Held.
- **B**: no exceptional vertex with `x ∈ Ω` and `ρ⁻¹x ∈ Ω`. 349 seeded star-shaped simple
  polygons, 2683 vertices decided, 358 exceptional, 698 236 interior samples, **zero** float
  candidates and therefore zero exact violations. Held.
- **C**: convex curves never fire it. Held, 0/805.

Honest weight of B: star-shaped polygons cannot wrap around an external point, so the hunt never
entered the regime where Lemma A could plausibly fail. It is a consistency check, not an attack.
The real attack was §4 above — trying to break the *proof* — and it failed to break it.

Runtime for the whole reproduction script: ~90 s. Well inside the §6 item-6 compute budget. No background jobs
started, nothing left running.

## 7. Lean

Could not attempt it: no `elan` in this container, GitHub releases and the `leanprover` hosts are
blocked by the egress proxy, and there is no vendored Mathlib under `lean/` to read (only
`lean-toolchain`, `lakefile.toml`, `Verified/`). So README §3.5 is a *target specification* with
every Mathlib identifier flagged unverified, and it says so.

The target I would hand a Lean worker is the **isometry** form, not the `60°` form:

```
V measurable, σ an isometry with σ O = O, λ(V ∩ σ''V) = 0  ⟹  λ(V ∩ ball O R) ≤ λ(ball O R)/2
```

because (a) it is JCT-free so §6.3's gap does not bite, (b) its proof needs only
"isometry fixing `O` maps `ball O R` onto itself", "isometries preserve volume", and additivity,
and (c) it is *more general* than the informal statement, which is the ideal shape for a first
target. `H′` (the strict version) is a worse first target — punctured-ball connectedness plus a
full-measure-closed-set step.

## 8. What I did not do, and what I would do next

Not done:

- No literature check. Every scholarly host is blocked, as the problem README's provenance warning
  records; I made no attempt and claim no citation. Whether the density formulation is in Meyerson
  or is folklore is unknown to me and I did not guess a number for it beyond repeating I1's ~30%.
- Did not cross-check my exact interior test against the polygon lane's own `sympy` cross-checker.
  I deliberately used **no** sympy geometry predicate anywhere, per the brief's warning about
  `Segment2D.intersection` failing on 3/176 boundary cases; everything is `Fraction`-based
  `ℚ(√3)` from the committed `k3.py`.
- Did not attempt a uniform (scale-independent) improvement of the strict inequality. `H′` gives
  `<` at each `R` with no uniform gap, and I do not know whether
  `sup_R density = ½` is approachable by an actual exceptional point. That is the obvious next
  question in this lane and I have no opinion on the answer.

Next, in order of value:

1. Hand README §3.5's isometry statement to a Lean worker. It is the most formalisable object
   this directory has produced after the wedge test.
2. Ask whether `sup_R λ(Ω̄ ∩ B(O,R))/λ(B(O,R))` over exceptional `O` is `½` or something smaller.
   `H′` only rules out attainment at a single `R`.
3. Cross-family review of Lemma A. Both the rotation lane and I have now derived it independently
   — but we are the same model family, so per §5 and §8 that is decorrelation only and carries no
   verification credit. A Codex derivation is what would move it.

## 9. Suspicion register

- The moment that felt most like a result — "exceptional points have density below ½ at every
  scale" — is one line of measure theory. That gap between how it feels and what it costs is
  exactly what `RULES.md` §0 warns about, and it is why README §0 leads with the deflation rather
  than burying it.
- I wanted the pinwheel to work, and I built it myself, and the decider that adjudicated it is not
  mine but *is* this repo's and was written by the same agent. Weakest link in §6: if
  `decide_good` were wrong, my independent `Ω ∩ ρΩ` certificate would still stand (it uses only
  my own ray-casting), but the *triangle* would not. I checked the two agree; I did not
  re-implement `decide_good`.
- I have not proved that no `60°` sector lies in `Ω̄` for the pinwheel *from the definition of
  Lemma B*; I proved `Ω̄ ∩ B(O,ε)` is exactly the `53.13°` wedge for `ε² < 4/125` and argued that
  larger radii are worse. That argument is short and I believe it, but it is the step in §6 a
  reviewer should redo rather than read.
