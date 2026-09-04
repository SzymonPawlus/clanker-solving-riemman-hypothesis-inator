# Cross-examination: round 3 (exceptional-set-polygons, exceptional-pair-rigidity, extremal-size, scalene-shapes)

```
regularity budget: not applicable. This file introduces no new mathematical claim of its own; it
examines regularity budgets already declared by the four lanes below, checking (per problem
RULES.md §6.2 item 5) that each declared hypothesis is genuinely used and no undeclared one is
smuggled in. Where I ran independent computation it is exact (Q or Q(sqrt3), Fraction-based,
no sympy geometry predicate), per RULES.md §5.
```

**Examiner: Claude Sonnet 5, 2026-08-29, same conversation as the four authoring workers (all
Claude Opus 5).**

**This is not cross-family review, and grants no status.** Per [`../../../../RULES.md`](../../../../RULES.md)
§5 and §8, `verified:review` requires an examiner from a *different model family* than the author.
Sonnet 5 and Opus 5 are the same family — the closest decorrelation available today, with Codex
unavailable — but explicitly **not** what §5 asks for. Every claim below stays at the status its
own lane assigned it (`sketch` or `numerical`), pending genuine cross-family (Codex) or human
review. An earlier same-family cross-review today (round 2) cleared three other claims with no
objection; that is weak evidence about this reviewer's independence, not about these four lanes,
and it is not treated here as license to expect the same outcome.

Full method, reasoning, and every re-derivation is in the journal:
[`../../../../notebook/claude/2026-08-29-iet-round3-review.md`](../../../../notebook/claude/2026-08-29-iet-round3-review.md).
In summary: each claim was restated independently before reading the proof for agreement; every
step was re-derived from definitions; the standard failure points (JCT applied to something not
shown Jordan, continuity claimed where it fails, nondegeneracy/limits, division by a possibly-zero
quantity, the step each lane itself nominated as weakest) were attacked by name; and every
computational claim was re-decided with a decider written from scratch in this session — its own
`Fraction`-based $\mathbb{Q}(\sqrt3)$ field, its own exact segment intersection, its own rotation —
sharing no code with the committed enumerator or with any of the four lanes' own deciders, and
using no `sympy` geometry predicate.

---

## Lane 1 — `../exceptional-set-polygons/README.md`

### Verdict — Lemma 1 (criterion) and Lemma 2 (polygon local structure)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — same model family as the author; does not
             satisfy RULES.md §5's cross-family requirement
depends-on: nothing beyond elementary plane geometry (Lemma 1) and the polygonal Jordan curve
            theorem (Lemma 2), both re-derived here rather than assumed
checked: both re-derived from the bare statements. Lemma 1's (only) subtlety — the "mod 360°"
         residue, not an unsigned angle — was checked against exactly the case that needs it
         (Theorem 3's direction sets wrap most of the way around the circle). Lemma 2's two-sector
         dichotomy, and that "exactly one sector is in Ω" genuinely needs both directions of the
         argument (not both in Ω, not both in E), both present via O ∈ ∂Ω ∩ ∂E.
not-checked: nothing load-bearing.
```

### Verdict — Lemma 3 (region lemma) and Lemma 4 (sector criterion)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — same family, not cross-family
depends-on: the Jordan curve theorem (for a general Jordan curve here, not merely the polygonal
            case — correctly declared "Jordan" not "polygonal" in the file's own budget line),
            isometry-invariance of planar Lebesgue measure
checked: reconstructed Steps 0 and 1 from the bare statement (the dispatcher's named attack
         point), including the specific subtlety in Step 3's "Step 1 with the roles of J and
         ρ(J) exchanged" — I wrote Step 1 as a general lemma over any Jordan curve K and any
         homeomorphic isometry τ, instantiated it at K=ρ(J), τ=ρ^{-1}, and confirmed the
         hypothesis and conclusion translate exactly as the file uses them. Checked the
         five-step main proof's use of connectedness (circle-minus-a-point) and the two
         invocations of JCT (once at J, once at ρ(J), both licensed since ρ is a homeomorphism
         of the plane carrying one Jordan curve to another). Attempted to break it via the
         standard failure points (JCT applied to something not shown Jordan; an unjustified
         "obviously the curves must cross") and found nothing.
not-checked: nothing load-bearing; this is the step I attacked hardest and it survived.
```

### Verdict — Theorem 1 (the reduction, `E(P) ⊆` vertices with angle `< 60°`)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: Lemma 2, Lemma 3, Lemma 4 (all re-derived above, all sketch, correctly not treated
            as assumable — the file re-derives rather than imports)
checked: the "where the brief's shortcut fails" paragraph specifically — confirmed the gap is
         real (a tangent line gives two directions 180° apart, and 180 != 60, so the criterion
         needs the interior-filling-a-half-disc route instead) — and confirmed the repair
         (Lemma 2 + Lemma 4) actually closes it rather than merely restating the problem.
         Independently re-decided on the polygon control (below).
not-checked: nothing load-bearing.
```

### Verdict — Theorem 2 (at most two wedge-type points)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing (pure angle-sum argument on point sets, correctly budgeted "none")
checked: re-derived by hand — the collinearity exclusion (a collinear third point subtends 180°,
         contradicting a cone opening < 60°) and the angle-sum contradiction (three angles each
         < 60° cannot sum to 180°).
not-checked: —
```

### Verdict — Theorem 3 (the 17-vertex non-wedge exceptional witness)

**This is the claim I attacked hardest, because it refutes a `sketch` in `spiral-tip-witness`.**

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — same family, does NOT confer verified:review
depends-on: Lemma 1 only (re-derived above); the proof is explicitly topology-free
checked: rebuilt the entire witness independently. Wrote a from-scratch Q(sqrt3) decider
         (Fraction-based; own segment intersection; own rotation) sharing no code with either
         of the lane's two deciders or the committed enumerator, and ran it on the exact
         polygon: confirmed simple; confirmed vertex O is the ONLY exceptional vertex out of 17;
         confirmed all 16 others good, with witnesses my code produced independently (not
         cross-checked against the lane's witnesses, freshly found). Separately, in exact
         Fraction arithmetic, independently re-verified every hand-computed rational identity
         the proof depends on: <a_k, a_{k+1}-a_k> = (3/5)|a_k|^2 for k=0..6 (radial
         monotonicity); a_8 = 2*a_7 (final segment radial); (9/10)|a_8|^2 - |a_7|^2 = 53248/5
         > 0 (cap stays outside radius 2^6); c = <a_1,a_3> = 28/25 > 0 and s^2-3c^2 = 6864/625
         > 0 (angle(a_1,a_3) > 60 degrees, hence not wedge-type). All confirmed exactly, with no
         float anywhere in the decision. Three independent deciders (the lane's two, mine) now
         agree, and the hand proof's own rational hypotheses check out independently of all
         three.
not-checked: nothing load-bearing. I looked hardest here and found nothing wrong.
```

### Verdict — §7.4 corollary (refutation of `spiral-tip-witness` §9.3's "every exceptional point
is wedge-type")

```
status: refuted (unchanged — the refutation is exactly Theorem 3, confirmed above)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: Theorem 3
checked: the target sentence in spiral-tip-witness §9.3 and the specific step named as wrong
         (that the rotating-wedge mechanism "needs I_r to rotate through unboundedly many turns")
         — confirmed the counter-argument is correct: Lemma 2 of that lane only needs the arc
         I_r to have length < 60 degrees at each radius, never that it rotate at all, and a
         finite polygonal rotation (as in Theorem 3) supplies exactly that.
not-checked: I did not re-examine spiral-tip-witness's own claims beyond the one sentence this
             corollary targets; that lane is out of this round's scope.
```

### Verdict — §8 (`|E(P)| ≤ 2` not proved) and Proposition 5 (no-sweep)

```
status: sketch (unchanged); the "not proved" claim is an honest negative report, not a theorem
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: Lemma 1 (Proposition 5); the discussion in §8 depends on Theorem 1-3 and half-density
checked: Proposition 5 re-derived (one line from Lemma 1 plus IVT on a continuous angular
         separation). §8.2's claim that the angle-sum route needs the bound
         "angle(O_j,O_i,O_k) < 60deg with no slack" and that exceptionality only constrains each
         circle separately (different radii for O_j and O_k unless isosceles) — confirmed this
         is a correct description of why the route is unavailable, not merely restated.
not-checked: §8.3's claim that "no measure argument of this shape can do better" is a claim
             about the nonexistence of an argument, which cannot be verified by reconstruction —
             only by someone finding one. Flagged, as the lane itself flags it, as the kind of
             "I could not do it" that risks quietly becoming "it cannot be done."
```

---

## Lane 2 — `../exceptional-pair-rigidity/README.md`

### Verdict — Lemma R (radial criterion)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing (re-derived, same three-line fact as Lane 1's Lemma 1)
checked: identical re-derivation to Lane 1's Lemma 1; agreement across lanes noted as
         decorrelation evidence only, per the lane's own framing.
not-checked: —
```

### Verdict — Theorem W0 (blocked point realises diam), W1 (two blocked points are the diameter), W2 (uniqueness)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing beyond the law of cosines, law of sines, and triangle angle sum — the
            budget line's claim of "no regularity at all" is correct as far as I can determine
checked: rebuilt W0's corner-maximum argument for f(a,b)=a^2+b^2-ab on [0,R]^2 directly (convex
         in each variable, so max at a corner) and confirmed the maximum R^2. Rebuilt W1 Step
         (i)'s case split (collinear vs. not) independently, including confirming "larger angle
         opposite longer side" generalizes correctly to non-acute angles via the law of sines.
         Rebuilt W2's case O_1 not in {X,Y} by direct optimization: independently confirmed the
         solution set of a^2+b^2-ab=d^2 on [0,d]^2 is EXACTLY {(d,0),(0,d),(d,d)} (fixing b,
         f convex in a forces the max to an endpoint a in {0,d}; each endpoint branch then
         attains d^2 only at the stated points) — this was flagged by the lane itself as the
         single most attackable step, and it holds.
not-checked: —
```

### Verdict — Proposition T (thinness)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: W1, the inscribed-angle theorem
checked: read and spot-checked against the tight 30-30-120 case (d=sqrt3, apex at exactly 1/2,
         matching the bound exactly); did not rebuild the general chord-locus argument from
         scratch.
not-checked: the general claim that the farthest point of the locus-arc from the chord is its
             isosceles apex, at distance (d/2)cot(theta/2) — standard circle geometry, plausible,
             not independently rebuilt.
```

### Verdict — the convex criterion re-derivation (§5, F1-F5, existence half)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing beyond convexity, IVT, compactness — matches the file's own budget
checked: read closely; the trichotomy on sign(h) at theta_0 in (60,alpha) is a clean IVT
         argument and I did not find a flaw in the semicontinuity claims (F4) as stated for the
         *interior* of the cone.
not-checked: did not independently rebuild F1-F5 from scratch line by line (time budget); this
             overlaps closely with the boundary-branch analysis I DID do in full for the
             analogous step in Lane 4 (scalene-shapes' Theorem C(1), see below), which is
             structurally the same dichotomy and survived there.
```

### Verdict — Corollary C1/C2/C3 (convex exceptional points are diameter endpoints)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: W0-W2, the convex criterion (§5)
checked: the chain of implications C1=W0, C2=W1+W2.
not-checked: the parenthetical transfer step in §6 — that the triangle W2 produces when S=K
             (compact convex body) has its OTHER TWO vertices actually on ∂K, not merely in K,
             which is needed to carry the corollary from S=K to J=∂K. I read the given argument
             (a point of K at maximal distance from a fixed point lies on ∂K) and find it
             plausible but did not write an independent proof. This is a genuine gap in my own
             examination, not a claimed error — flagged per RULES.md §5's instruction that an
             honest not-checked beats a wave-through.
```

### Verdict — pentagon C2 (exceptional pair ≠ diameter pair)

```
status: numerical (unchanged; exact arithmetic, not a proof step)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: Lemma R
checked: independently re-decided with my own decider (not merely the distance arithmetic,
         which the dispatcher had already checked, but the actual good/exceptional verdict at
         every vertex): confirmed (-5,-14) and (18,0) are exactly the two exceptional vertices,
         confirmed the diameter pair is (-10,-4)-(18,0) at d^2=800 versus the exceptional pair's
         d^2=725, and confirmed simplicity of the pentagon. Also independently checked the
         "mixed pair" wedge-classification claim by direct angular-span computation: (18,0)
         spans ~45.4 degrees (wedge-blocked), (-5,-14) spans ~85.2 degrees (not) — matching the
         lane's reported figures.
not-checked: —
```

### Verdict — `|E(J)|=1` witness (triangle (0,0),(5,0),(2,4))

```
status: sketch + numerical (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: the convex criterion (§5) for the hand proof; nothing for the decider check
checked: independently re-decided with my own decider — confirmed (5,0) is the sole exceptional
         vertex, the other two good with fresh witnesses. Independently verified the hand angle
         test algebraically: at (5,0), 4(u.v)^2=900 > 625=|u|^2|v|^2 (angle < 60, exceptional);
         at (0,0) and (2,4), 400 < 500 (angle > 60, good).
not-checked: —
```

### Verdict — §7.3/§7.4/§7.5 census (W1 fails on non-convex polygons; non-wedge exceptional
points are ~25% of the non-convex census; W1's prediction survives where its hypothesis holds)

```
status: numerical (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: the same decision procedure as above
checked: spot-checked one of the three explicit integer counterexamples (the pentagon, above,
         since it is the smallest and the lane itself recommends it as the cheapest to re-decide).
not-checked: did not re-run the two larger explicit counterexamples (C1, C3) or the bulk census
             (4400+ polygons); those scripts are explicitly not committed (the lane says so,
             correctly, since experiments/ is another worker's lane) and are therefore not
             independently reproducible by anyone without rewriting them, which is exactly what
             this review's time budget did not stretch to beyond the one spot check.
```

---

## Lane 3 — `../extremal-size/README.md`

### Verdict — Lemma W, Corollary U, and the L-hexagon degeneracy (Lemma L, Theorem D)

```
status: sketch (Lemma W, Corollary U, Lemma L, Theorem D); numerical (the exact side^2 values)
         — unchanged
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing (arbitrary bounded sets)
checked: re-derived Lemma W's minimal-width computation and Corollary U's monotonicity argument.
         Independently recomputed the L-hexagon's exact maximum side with a decider that checks
         the FULL continuous boundary via exact segment intersection (not the lane's 240 sampled
         points): confirmed max side^2 at O=(0,0) equals exactly (8+4*sqrt3)*delta^2 for
         delta in {1/10, 1/20, 1/50}, i.e. side = (sqrt6+sqrt2)*delta exactly, matching the
         lane's reported value and confirming Lemma L's upper bound is off by exactly the
         claimed factor of 2. Also confirmed (0,0) is the maximizing vertex by checking every
         other vertex of the hexagon.
not-checked: whether an edge-interior point (not a vertex) could exceed the vertex-0 maximum —
             my exact computation checks candidate O at every vertex but I did not run it at a
             continuum of edge-interior O's; the lane's own 39-samples-per-edge check is denser
             than what I re-ran, though still a sample, not a proof of the vertex-0 maximum's
             global optimality.
```

### Verdict — Theorem C (`m(K) ≥ √3·r` for convex bodies, disk sharp)

```
status: sketch (unchanged) — this is the lane's flagged "most novel-looking" result
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing beyond convexity, compactness, IVT
checked: Steps 1-3 rebuilt independently from the bare statement. Step 1: confirmed the
         tangent-at-contact-point half-plane argument and the chord bound R(theta) >= 2r*cos
         theta directly from elementary circle geometry. Step 2: confirmed g(-90)=R(-30)>0 and
         g(30)=-R(30)<0 from (*), giving a nonempty compact zero set. Step 3: independently
         redid the angle arithmetic (beta=arccos(c/2r) in (30,90), forcing theta<=-beta and
         (theta>=beta-60 or theta<=-60-beta)) and confirmed both disjunction branches are
         incompatible with the other constraint, giving the contradiction.
not-checked: Step 0 (Minkowski-sum reduction K_n=K+(1/n)D to strictly convex, then the
             Hausdorff-limit passage back to K) — I read it and find it plausible (this is a
             standard convexity technique and the noncollapse bound is established correctly
             before the limit, per RULES.md §2's discipline) but did not independently prove the
             claim that vertex limits land on ∂K rather than merely in K. This is one of the
             lane's own two self-flagged weakest steps and I did NOT close it. The continuity
             claim at the CLOSED endpoints theta=+-90 (the lane's other self-flagged weak step,
             needed for g to be continuous on the closed interval and the IVT to apply at the
             endpoints) — I worked through the semicontinuity argument for the open interval and
             found it sound, but did not personally nail down the closed-endpoint case. Both of
             these remain open per this review; see "strongest objection" below.
```

### Verdict — Lemma B (`w ≤ 3r`, classical)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing
checked: read; matches the standard proof sketch for this classical fact.
not-checked: not independently re-derived line by line (low risk, standard convexity folklore,
             and the lane correctly reproves rather than cites it per this problem's burn history
             with unread citations).
```

### Verdict — "the disk is not extremal" (§7)

```
status: sketch (first-order) + numerical (second-order sign) — unchanged, and the lane's own
        honest self-assessment ("float", "not claiming 0.857205 is the answer") is correct and
        should not be upgraded
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: the first-order perturbation formula (sketch); the numerical sign check (float)
checked: the first-order argument itself (max F >= mean = min G always, so no perturbation helps
         at first order, with equality band n = ±1 mod 6) is a clean, checkable Fourier-style
         argument and I found no issue with the derivation as written.
not-checked: did not re-run the float search or verify the two independent numerical estimators
             the lane reports agree to 1e-9; per the brief, this claim must NOT be certified as
             is, and I concur — an exact result here needs an exact maximizer over general convex
             bodies, which does not exist in this repo's tooling, and the lane correctly does not
             claim otherwise.
```

---

## Lane 4 — `../scalene-shapes/README.md`

### Verdict — Proposition 1 (six-multiplier spiral-similarity criterion)

**This was the lane's own priority-1 attack target.**

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — does NOT confer verified:review
depends-on: nothing (set-theoretic)
checked: rebuilt the (=>) direction completely independently from the definition of similarity,
         deriving the twelve raw mu-values from the six permutations of (0,1,w) under a direct
         similarity myself BEFORE reading the lane's own table, and got: w, 1/w, 1-w, 1/(1-w),
         (w-1)/w, w/(w-1) — an EXACT match to the lane's listing. Independently confirmed the
         three inverse-pairs and their conjugate images, and confirmed the collapse
         S ∩ sigma_mu(S) != {O} <=> S ∩ sigma_{1/mu}(S) != {O} via the swap argument (apply
         sigma_mu^{-1} to a witness). Found no missing or extra role in M(w). Independently
         verified §1.4's claim mu^{-1}=conj(mu) iff |mu|=1 by direct algebra.
not-checked: nothing load-bearing; this was the step I attacked hardest per the lane's own
             priority order and it survived completely.
```

### Verdict — Lemma A_sigma (nesting for spiral similarities), Proposition 3 (sharp half-density constant 1/(1+k^2))

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: for Lemma A_sigma, the Jordan curve theorem (correctly budgeted); for Proposition 3,
            nothing (pure measure theory)
checked: Lemma A_sigma was reconstructed by close analogy to Lane 1's Lemma 3, which I DID
         rebuild fully from scratch (same three-way case split on connectedness + JCT), plus a
         direct spot-check of the one genuinely new step for k<1 — the asymmetric conclusion
         that only the shrinking nesting survives, which follows from the one-line inequality
         "lambda(Omega-bar) <= k^2*lambda(Omega-bar) is impossible for k<1 with
         0 < lambda(Omega-bar) < infinity" — confirmed directly. Proposition 3's attained
         construction (alternating log-shells) was checked by direct computation of the
         geometric series sum, matching pi/(1+k^2) exactly.
not-checked: Proposition 3's upper-bound proof (the log-polar shear, Fubini reduction, and the
             one-dimensional max-weight-independent-set self-similarity argument
             f=max(1+q^2 f, q f)) was read but not independently re-derived step by step; the
             lane's own DP cross-check matches the closed form to six digits, which is
             corroborating but not a substitute for a from-scratch proof check.
```

### Verdict — Theorem 5 (spiral tip, every corner role) and Corollary 6

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: the spiral witness's own definition (data, re-derived as a normal form, not a claim)
checked: read the case split on radii (r<1 & kr<1; r=1; kr=1; r>1 or kr>1) and confirmed by hand
         that the three isolated values from the first case land inside the interval from the
         second, so the union is exactly |Lambda_c(mu)| <= beta as claimed.
not-checked: did not independently re-run the brute-force cross-check against 480 random
             parameter sets; relied on hand-verification of the case-split logic instead.
```

### Verdict — Theorem C (`|E_T(∂K)| ≤ 2` for every shape on every convex curve)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29 — does NOT confer verified:review
depends-on: Proposition 1 (re-derived above, confirmed)
checked: THIS IS WHERE I FOCUSED, per the brief's specific instruction ("the lane names C(1)'s
         boundary branch as its own best guess at where an error would be ... go there first").
         Reconstructed clause (1)'s proof (phi_1 < gamma(O) => O good) from the bare statement,
         specifically targeting the L=0 sub-case at an extreme direction, which the lane flags as
         untested by any polygon fixture (a polygon's extreme directions always carry a segment,
         so L is never 0 there). Result: when L_0 = lim_{theta->0+} R(theta) = 0, the ratio
         function h(theta)=R(theta+phi)/R(theta) -> R(phi)/0 = +infinity DIRECTLY, with NO
         attachment argument needed — this is the SIMPLER of the two sub-cases, not the fragile
         one. The genuinely delicate step is instead the L>0 attachment (pairing points on a
         boundary segment against a fixed point to realize an unbounded ray of ratios,
         b = R(phi)/L_0 in closure(I)), which I checked using the general topological fact "A an
         interval, b in closure(A) => A union [b,infinity) is connected" — this holds without
         qualification and I found no gap.
not-checked: I did not find an error in Theorem C(1), including at the specific branch the lane
             named as riskiest — on reconstruction that branch turned out to be the easy one. I
             record this as a genuine finding (the self-flagged risk may be misplaced) rather than
             a clearance, since it is possible the real fragility is somewhere neither of us has
             located. I also did not build the specific fixture the lane suggests (a convex body
             with a circular-arc corner, to actually exercise L=0 computationally) — this remains
             a re-derivation on paper, not a fresh independent numerical test, since it would
             require exact arithmetic beyond Q(sqrt3).
```

### Verdict — Proposition 7 (wedge mechanism caps at two, every shape)

```
status: sketch (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: nothing beyond the corner-excess sum of a convex curve (<=360 degrees)
checked: re-derived directly — each wedge-blocked point is an extreme point of conv(J) with
         corner excess > 120 degrees (since gamma(O_i) < phi_1 <= 60), and at most two such
         points can exist since the excesses sum to at most 360.
not-checked: —
```

### Verdict — the §7.7 hand-checkable scalene example (`|E_T|=2` for a scalene shape)

```
status: sketch + numerical (unchanged; the arithmetic is exact and elementary)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: Theorem C
checked: independently redid the hand arithmetic — P-O=(-2,-1)=-2-i; mu*(P-O)=(-3+2i)(-2-i)=8-i;
         X=O+(8,-1)=(58,0); squared sides 5:65:100 = 1:13:20, matching the target shape exactly.
not-checked: —
```

### Verdict — census (§7.5, no |E_T|≥3 found across 66,075 pairs) and the non-wedge exceptional
points (§7.4)

```
status: numerical (unchanged)
examined-by: Claude Sonnet 5 (claude), 2026-08-29
depends-on: the decision procedure of §7.1
checked: not independently re-run; the scripts are not committed (same reproducibility caveat
         as Lane 2's census) and this round's time did not stretch to rewriting the census.
not-checked: the bulk numerics. The lane's own honest caveats (finitely many sampled points per
             curve; polygons are the most regular curves there are) are the correct caveats and
             I have nothing to add to them.
```

---

## Strongest objections found, and what I could not follow

**Objection 1 (Lane 3, `extremal-size`, Theorem C).** The proof's continuity claim for
`θ↦A+R(θ)u(θ)` is stated to hold "continuously up to the closed endpoints `θ=±90°`," and this is
exactly what makes `g(θ)=R(θ+60°)−R(θ)` continuous on the *closed* interval `[-90°,30°]` and the
IVT applicable at the boundary values `g(-90°)`, `g(30°)`. I worked through the semicontinuity
argument for the interior of the cone and found it sound, but did not close the closed-endpoint
case myself. Paired with Step 0's Hausdorff-limit-lands-on-`∂K` claim (also not independently
closed by me), this is a proof standing on two self-flagged, unclosed steps — the lane says so
plainly and I could not do better in the time available. I tried to construct a strictly convex
body where the endpoint behavior might misfire (something with a corner formed by circular arcs,
as the lane itself suggests building) and did not get far enough to either break it or clear it.
This survives my attempt to break it only in the weak sense that I found no counterexample; it does
not survive in the strong sense of having been independently proved.

**Objection 2 (Lane 4, `scalene-shapes`, Theorem C(1)).** Not really an objection so much as a
redirection: the lane names the untested `L=0` branch as its best guess at where an error would be.
On reconstruction, that branch resolves *without* the attachment machinery (`h→∞` directly), so if
Theorem C(1) is wrong, I do not think it is wrong there. I have no candidate for where else it might
be wrong, which is itself a limitation of this review rather than a clean bill of health — the next
worker should not spend time on the `L=0` branch specifically, but should not treat that as the
whole surface either.

**What I could not follow at all.** Nothing rose to that level this round — every claim I attempted
to restate, I could restate, and every proof I attempted to reconstruct, I got far enough into to
form a specific opinion about (agreement, a located gap, or a named unclosed step). The two items
above are the honest boundary of what I checked, not places where the argument was opaque to me.

## What survived hardest scrutiny

Lane 1's Theorem 3 (the 17-vertex witness) and Lemma 3 (the region lemma) were the targets I
attacked most aggressively, because Theorem 3 overturns another lane's claim and Lemma 3 is the
one piece of real topology doing work across two of the four lanes (its `k<1` generalization is
Lane 4's Lemma A_σ). Both survived a genuinely independent, from-scratch reconstruction — a third
decider for the former, a from-definitions proof reconstruction including the specific
role-exchange step for the latter — and I could not find an error in either.

Lane 4's Proposition 1 (the six-multiplier criterion) is the other claim I am most confident in: I
derived its `M(w)` independently before reading the lane's table and landed on an exact match,
including the inversion-collapse mechanism.
