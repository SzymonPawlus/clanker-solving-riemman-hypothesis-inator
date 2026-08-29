# Rules — inscribed equilateral triangle (the triangle peg problem)

Problem-specific. The repo-wide protocol in [`../../RULES.md`](../../RULES.md) still applies in
full; this file adds what is particular to a *plane topology* problem, where the objects are
infinite and wild, and where the whole difficulty is how little you may assume about them.

---

## 0. What makes this problem different

Neither of the other directories' instincts transfer. There is no certificate to check as in
circle packing, and no finite search space to exhaust as in Woodall. A Jordan curve is an
arbitrary homeomorphic image of a circle: it may have infinite length, positive area, and a
tangent at no point at all. **Everything you can draw is a special case.**

So the dominant failure mode here is **smuggled regularity**. Almost every fluent argument for
"every Jordan curve" quietly assumes one of: rectifiability, a tangent direction, finitely many
crossings of some auxiliary curve, local monotonicity, or that a limit of nondegenerate inscribed
triangles is nondegenerate. The square peg problem has been open for a century *precisely* because
of the last one. An argument that does not say where it uses regularity has not been checked; it
has been read.

What counts as progress, in the order it is worth having: a **precise citation** with the curve
class it covers; a **Lean formalisation of an elementary fragment** (§6.3); an **exact polygon
computation** (§5); a **documented refutation** of a candidate argument killed by a §3 filter.
A general proof for all Jordan curves is not on that list. Read §6.1 first: this may already be a
theorem, in which case the work here is citation and formalisation, not attack.

---

## 1. The regularity budget — mandatory, one line, at the top

Every `attacks/<slug>/README.md` and every file in `results/` carries a line

```
regularity budget: continuous | Jordan | locally connected | rectifiable | C¹ | convex | polygonal
```

naming **every** hypothesis on $J$ the argument consumes, plus one sentence on what breaks first if
you drop the strongest one.

1. **Name the class in the claim itself.** "Every *smooth* Jordan curve inscribes an equilateral
   triangle" is a different and strictly easier theorem than the same sentence without "smooth".
   Titling the weaker result as the stronger one is the error this file exists to stop.
2. **No budget line, or an unjustified one ⇒ the claim is `sketch`**, however good it looks, and a
   reviewer must not promote it.
3. **These words are load-bearing.** For a general Jordan curve "the tangent at $p$", "arc length
   from $p$", and "the finitely many points where…" are *undefined*. Any of those phrases is a
   regularity assumption whether or not you declared it.
4. **Approximation does not refund the budget** (§4).

## 2. Nondegeneracy is part of the claim

Three coincident points satisfy $|AB| = |BC| = |CA|$. A statement or construction that does not
exclude them proves nothing.

- Every claim states the triangle is **nondegenerate**: side length $\ge \delta$ for a $\delta > 0$
  you can point at.
- Every compactness or limiting argument carries a **noncollapse bound uniform along the sequence**
  — a $\delta$ independent of $n$, established before the limit, not observed after it.
- "The limit triangle is clearly nondegenerate" is the commonest way to accidentally claim the
  square peg problem. Treat that sentence as an unproved lemma every time.

The clean illustration is the rotation construction (§3.2): rotating $J$ about $O \in J$ fixes $O$,
so $O$ always lies in $J \cap \rho(J)$ and is exactly the degenerate solution. The entire content
of that construction is producing a *second* intersection point.

## 3. Three cheap filters — run all three, and say in the PR that you did

Each takes minutes and kills most wrong approaches before write-up. Report all three outcomes, with
reasons, in the PR body.

### 3.1 The wedge test

If all of $J$ lies in a closed convex cone with apex $O$ whose boundary rays meet at angle
$\theta < 60°$, then **no inscribed equilateral triangle has a vertex at $O$**: any $P, Q \in J$
give $\angle POQ \le \theta < 60°$, while an equilateral triangle needs exactly $60°$ at a vertex.

- **Witness:** the boundary of a $30°$-$30°$-$120°$ triangle. It is convex, so at each $30°$ apex
  the whole curve lies in a $30°$ wedge; both apexes are exceptional.
- **The filter:** "every point of every Jordan curve is a vertex of an inscribed equilateral
  triangle" is therefore **false**, and any argument implying it — including one that proves its
  conclusion for an *arbitrary* chosen $O \in J$ — is wrong. Run candidates against this witness
  *before* writing them up.
- **Do not over-read it.** The hypothesis is that the *whole curve* lies in the wedge. A reflex
  polygon may have an interior angle under $60°$ at a vertex that is still a triangle vertex,
  because the curve leaves the wedge. Convexity, or an explicit containment check, is required.
- It is also a **self-contained elementary proof of the sharpness row** in `README.md`'s
  known-results table (two exceptional points, attained). Nothing here rests on that row's
  provisional citation, which is why §7 puts formalising it early.

### 3.2 The square contrast

If your argument works verbatim with "square" for "equilateral triangle", it is either wrong or it
settles the square peg problem (`../../RULES.md` §7) — assume the former. **State in every attack
README why the argument does not transfer to the square.** An attack that cannot answer this is
`refuted` on the spot.

The reference example of a genuine non-transfer: rotate $J$ by $60°$ about $O \in J$ to get
$\rho(J)$; any $q \in J \cap \rho(J)$ with $q \ne O$ has $|Oq| = |O\rho^{-1}(q)|$ and
$\angle qO\rho^{-1}(q) = 60°$, so $O, q, \rho^{-1}(q)$ is equilateral. Isosceles-with-a-$60°$-apex
closes the figure from **three** points; a square has **four** vertices, the fourth determined but
under no constraint to lie on $J$. That gap is the whole difference between the two problems, and
is the standard against which "why not squares?" answers are judged.

### 3.3 The polygon control

Every general claim about which points are exceptional, how many triangles are inscribed, or how
they vary, is first checked against this problem's exact polygon enumerator under `experiments/`
(currently `experiments/inscribed-triangle-polygons/`). A claim that fails on a polygon is dead; a claim that
survives is **merely not-yet-dead** — polygons are the most regular curves there are, so agreement
is weak evidence about the general case and none at all about the wild one.

## 4. Approximation arguments carry extra obligations

"Prove it for polygons or smooth curves, then pass to the limit" is the natural attack, will be
proposed repeatedly, and is where the analogous square argument dies. Such an attack must also
state, up front:

1. **The topology on curves** — Hausdorff distance on images, uniform convergence of
   parametrisations, or something else. These are not equivalent.
2. **That the limit is still a Jordan curve.** Hausdorff limits of Jordan curves need not be
   Jordan or even locally connected; uniform limits of injective maps need not be injective.
3. **The uniform noncollapse bound** of §2. Without it the argument is the failed square argument
   wearing a different hat.
4. **The §3.2 answer in strong form**: which step of the limit passage breaks for squares and does
   not break here.

Missing any of the four ⇒ `sketch`, and not a promotable one.

## 5. Computation — exact, or it is not evidence

Inscribed equilateral triangles on a rational-coordinate polygon are algebraic: the $60°$ rotation
contributes $\sqrt{3}$ and the arithmetic closes in $\mathbb{Q}(\sqrt{3})$. Floating point is
avoidable here and must be avoided.

- **Exact rational or exact algebraic arithmetic** for any existence, count, or exceptional-point
  claim. Floats are for search and pictures only, never for a reported result.
- Zero tests decide the interesting cases (vertex hits, edges parallel to rotated edges, tangential
  contact). A float zero test is the bug you will actually ship.
- **Validate before believing.** The enumerator must reproduce an equilateral triangle inscribed in
  itself, and the §3.1 witness — both $30°$ apexes exceptional, no other boundary point.
- Reproducible from one command, seeds and versions pinned (`../../RULES.md` §4). Raw enumerations
  live in `experiments/`, are `numerical`, and are never a proof step.

## 6. How the `../../RULES.md` §3 statuses are earned here

### 6.1 `cited` — citation precision *is* the research

The equilateral case may already be a theorem while the square case is famously open; getting that
boundary right is the deliverable. A `cited` claim names **author, paper, year, theorem number, and
the exact curve class covered**, plus a sentence on what it does not cover. "It is known that every
Jordan curve inscribes a triangle" is not a citation, it is a rumour with a confident tone.

- **Do not cite from memory.** Recalling a plausible author and title is not reading a paper. If
  the source cannot be obtained, write "not obtained" with the routes you tried — an honest,
  useful result, and this repo has been burned by the alternative.
- Recalled names may appear in an attack README **as search targets, flagged unverified**, never in
  the known-results table or `results/` until someone has read the source.
- Failing to find a theorem is not evidence the problem is open. Say "not found", not "open".

### 6.2 `verified:review` — reconstruct the topology, do not agree with it

Per `../../RULES.md` §5, but here the examiner must **independently reconstruct the topological
step** — typically an intersection, connectedness, or degree argument — by deriving it themselves.
Agreeing that it sounds right is not a review. The examiner must attack by name at least:

1. **The Jordan curve theorem applied to something not shown to be a Jordan curve** — a rotated
   copy, an intersection, a limit, a projection, a level set.
2. **Continuity claimed where it fails.** "The inscribed triangle depends continuously on $O$" is
   false in general; multiplicity, non-uniqueness and collapse all break it.
3. **A limit of nondegenerate triangles assumed nondegenerate** (§2) — check $\delta$ exists and is
   uniform.
4. **"Obviously the curves must cross."** Crossing is a claim about parity or degree, not about the
   picture. Which theorem supplies it, and do its hypotheses hold?
5. **The regularity budget** (§1): each declared hypothesis genuinely used, no undeclared one.

Unable to follow one of these is an honest partial examination: record it under `not-checked` and
leave the claim `sketch`.

### 6.3 `verified:lean` — what is reachable

**Checked 2026-08-29** against the pinned toolchain (`lean/lean-toolchain`, mathlib `v4.33.0`; no
local `.lake`, so this was read from the Mathlib sources at that tag):

- `Mathlib.lean` at `v4.33.0` has **no Jordan curve theorem**, no winding number, no invariance of
  domain, no Brouwer fixed point. Every `Jordan` match is a Jordan *algebra*, Jordan–Chevalley,
  Jordan–Hölder, or Jordan measure decomposition.
- Mathlib's own index `docs/1000.yaml` lists `Q260928: Jordan curve theorem` with **no `decl` and
  no external link** — not in Mathlib, and no Lean formalisation known to that index. Brouwer
  appears there only as an external Lean 3 project.
- Singular homology exists but is early (`AlgebraicTopology.SingularHomology.{Basic, HomologyZero,
  HomotopyInvariance}`), with no excision or Mayer–Vietoris, so the usual route to the Jordan curve
  theorem is not available either.

Therefore:

- **Anything resting on the Jordan curve theorem is not a Lean target.** That is a genuine large
  Mathlib gap in the sense of `../../RULES.md` §4 — not "merely slow" — so `verified:review` is the
  correct target for such steps, and the PR must say so. Re-run the check rather than quoting this
  paragraph; Mathlib moves.
- **Elementary fragments are real Lean targets and are the best available work here.** The **wedge
  test** (§3.1) is plane geometry with no topology in it, and the API it needs is present
  (`Geometry.Euclidean.Angle.Unoriented.*`, `Geometry.Euclidean.Angle.Oriented.Rotation`). So is
  the **rotation identity** of §3.2 — a statement about three points and a rotation, with the
  topology entirely outside it. So is any finite exact polygon computation over
  $\mathbb{Q}(\sqrt{3})$.
- Prefer formalising the *base* of a chain (`../../RULES.md` §3): a Lean wedge test makes every
  later `verified:review` use of it free.

### 6.4 `numerical`

Polygon enumerations and exceptional-point searches (§5). Evidence about where an exceptional point
can live; never a proof step, never the reason a general claim was promoted.

## 7. Realistic targets

Roughly by achievability; partial results count.

1. **Discharge the verification debt** in `README.md`: its citations are provisional, assembled
   from search listings with no source text read. Confirm each to §6.1 precision — theorem number
   and curve class — or downgrade it. Everything else here depends on this being right.
2. Exact polygon enumerator, validated per §5, plus a census of exceptional points.
3. Formalise the wedge test in Lean, and with it the falsity of "every point is a vertex".
4. Formalise the §3.2 rotation identity in Lean.
5. Write up as `refuted` each candidate argument the §3 filters kill, naming the filter. These
   entries are what stop the next agent repeating the work.
6. A cross-examined proof for a restricted class (convex, or polygonal) with an honest regularity
   budget and the §3.2 non-transfer answered.

Do not attempt a general proof for arbitrary Jordan curves before item 1 is done. If item 1 says it
is a theorem, this directory's job is 2–5 and a faithful record of the known proof, not a race
against it.
