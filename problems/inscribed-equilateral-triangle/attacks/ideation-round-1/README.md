# Ideation round 1 — candidate attacks, each with a kill-criterion, triaged

```
regularity budget: not applicable to the file as a whole — this file proves nothing and
nothing in it is assumable. Each idea carries its own provisional budget inline. Every
mathematical statement below is `sketch` at best, and most are explicitly speculation.
```

- Lane: **ideation** (divergent lane per [`../../../../RULES.md`](../../../../RULES.md) §8 —
  wrong ideas are cheap here and get filtered downstream).
- Author: `claude` (Fable 5, per the §8 model-selection table), 2026-08-29, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Journal, including the ideas discarded *before* write-up and the derivation scratch for I1
  and I2: [`../../../../notebook/claude/2026-08-29-iet-ideation.md`](../../../../notebook/claude/2026-08-29-iet-ideation.md).
- Inputs read in full: [`../rotation-continuity/README.md`](../rotation-continuity/README.md),
  [`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md),
  [`../../README.md`](../../README.md), [`../../RULES.md`](../../RULES.md).
- **This file starts no work.** It proposes; a future claimed issue per idea does the work.
  Ideas needing the polygon enumerator are flagged for the `experiments/` lane and touch none
  of its files here.

**Format.** Every idea carries the four fields [`../../../../RULES.md`](../../../../RULES.md)
§6.2 and this round's brief require:

1. **Idea** — concrete enough to start tomorrow.
2. **Kill** — the observation that would make us abandon it (§6.2; met ⇒ stop, mark `refuted`).
3. **Meyerson?** — honest guess whether it is already in the unread literature, and whether
   that matters. (No scholarly host is reachable; every such guess is provenance-free.)
4. **Square test** ([`../../RULES.md`](../../RULES.md) §3.2) — run verbatim with 90° for 60°:
   if it would prove the square peg problem, it is wrong.

Notation is the repo's: $J$ a Jordan curve, $\Omega$ its interior, $E(J)$ the exceptional set,
$\rho_{O,\theta}$ rotation by $\theta$ about $O$, and Observation R the established-in-lane
(but still `sketch`) iff: $O$ is a vertex of an inscribed equilateral triangle $\iff$
$J \cap \rho_{O,60°}(J) \supsetneq \{O\}$.

---

## The ideas

### I1. The half-density obstruction: exceptional points see at most half of every circle

**Idea.** Suppose $O \in E(J)$. By Observation R, $J \cap \rho_{O,60°}(J) = \{O\}$, and by the
rotation lane's Lemma A dichotomy (`sketch`, must be re-derived in any write-up) this forces
$\Omega \cap \rho(\Omega) = \emptyset$. Now intersect with the circle $C(O,r)$: writing
$A_r = \{\theta : O + re^{i\theta} \in \Omega\}$ (open), disjointness says
$A_r \cap (A_r + 60°) = \emptyset$, hence $|A_r| \le 180°$ **for every $r > 0$** (else
inclusion–exclusion on the circle gives $|A_r \cap (A_r+60°)| \ge 2|A_r| - 360° > 0$).
Integrating in polar coordinates:

> **Speculative Lemma (half-density).** If $O \in E(J)$ then
> $\lambda(\Omega \cap B(O,R)) \le \tfrac12 \lambda(B(O,R))$ for **every** $R > 0$.
> Contrapositive criterion: if the interior fills **more than half of any single ball centred
> at $O$**, then $O$ is a vertex of an inscribed equilateral triangle.

Provisional budget: Jordan (Lemma A uses the Jordan curve theorem) — but note the *core*
inequality "$U$ open, $U \cap \rho_{O,60°}(U) = \emptyset$ $\Rightarrow$ density of $U$ at most
$1/2$ in every ball at $O$" is pure measure theory with **no topology at all**, and looks like
a genuine Lean target (Mathlib has Lebesgue measure and polar-coordinate integration), unlike
anything JCT-dependent.

**Why it is not the sector criterion in disguise.** Lemma B (sector criterion) needs a single
$60°$ sector inside $\overline\Omega$. The density criterion fires on a "pinwheel" point where
no such sector exists: four petals of angular width $50°$ apexed near $O$ (one touching $O$,
the other three truncated at tiny inner radii and joined into one Jordan domain away from
$O$) give $|A_r| \approx 200° > 180°$ on a range of radii, hence a ball of density $> 1/2$,
while no $60°$ sector at $O$ fits inside $\overline\Omega$ — the gaps between petals are
exterior. Sketch of the witness in the journal; making it exact is part of the work.

**Also delivers structure.** At every exceptional point the interior occupies at most half of
*every* ball at *every* scale. That is a quantitative constraint the wedge obstruction does
not give (the wedge is a direction statement; this is a measure statement), and it feeds I5.

**Kill.** (a) A gap in the disjointness-to-$180°$ step or the Lemma A re-derivation that
cannot be repaired; (b) an exact example of an exceptional point with some ball of interior
density $> 1/2$ — that would be an outright refutation of the lemma (and would mean Lemma A
is wrong, which the polygon enumerator could then hunt for); (c) the pinwheel witness failing
on exact computation, which would demote the idea to "true but never stronger than Lemma B",
i.e. not worth a lane.

**Meyerson?** The rotation-disjointness trick is elementary and the paper reportedly proceeds
by rotations, so a version may well be in there or be folklore. Matters little: even if known,
it is a short, self-contained, checkable lemma with a Lean-plausible core, which is exactly
the kind of base-of-chain object [`../../../../RULES.md`](../../../../RULES.md) §3 says to
prefer. Confidence the *density formulation* is novel: low-to-moderate (~30%).

**Square test.** With $90°$: "$\Omega$ disjoint from its $90°$ rotate about $O$ $\Rightarrow$
density $\le 1/2$" still holds (same computation with $|A_r \cap (A_r + 90°)|$), and the
contrapositive produces $P, Q \in J$ with $|OP| = |OQ|$, $\angle POQ = 90°$ — an inscribed
isosceles **right triangle**, not a square. The fourth corner is unconstrained, exactly the
convex lane's §6 counting gap. Does not transfer. Pass.

### I2. Spiral-tip exceptional points: a second mechanism, with full direction set

**Idea.** Every exceptional point this repo can exhibit is wedge-obstructed: the whole curve
sits in a cone of opening $< 60°$ at $O$. Propose a **structurally different mechanism**: a
logarithmic-spiral tip. Take the log spiral $r(\theta) = e^{c\theta}$, $c \neq 0$, an arm of
it spiralling into $O$ (finite length — the curve is even rectifiable), closed up far from $O$
into a Jordan curve $J$. Rotating the doubly-infinite spiral by $60°$ about $O$ gives the
"parallel" spiral $r(\theta) = e^{-c\pi/3}e^{c\theta}$, which is **disjoint** from the
original (radius ratio $e^{-c\pi/3 + 2\pi c k} = 1$ never, for $c \neq 0$), so near $O$ the
arm and its rotate interleave without touching. If the closing arc can be arranged so that
$J \cap \rho_{O,60°}(J) = \{O\}$ **globally**, then by Observation R:

> **Speculative claim.** There is a Jordan curve with an exceptional point $O$ at which the
> achieved direction set is **all of $S^1$** (the spiral winds through every direction at
> arbitrarily small radii). The wedge obstruction is therefore *not* the only exceptional
> mechanism, and — since the log-spiral arm has finite length — non-wedge exceptional points
> occur even on **rectifiable** curves.

Provisional budget of the intended result: Jordan (the witness is explicit; Observation R's
$\Rightarrow$ direction is set-theoretic). The hard part is purely the global disjointness of
the closing arc from everything, which is finitely checkable if the closing arc is polygonal
and the spiral is truncated-plus-limit.

Consistency checks already run: the point count respects Meyerson's bound (one tip per
spiral; nobody is claiming three of these yet — that is I3); nesting is impossible by the
measure half of Lemma A, so the configuration must be the external one, which is what the
parallel-spiral picture shows; and the tip is not a differentiability point of the arclength
parametrisation (the direction winds forever), so this does not contradict — and does not
touch — the rectifiable lane's a.e. question. Ownership note: this idea must be executed in
its own lane, not in `attacks/rectifiable-case/`.

**Kill.** (a) Proof that every closing-up of a spiral arm creates a second intersection with
its rotate — i.e. a demonstration that the global obstruction is unavoidable; a serious
honest attempt (say, two worktree-days) failing for a *reason* counts; (b) discovery that the
parallel-spiral disjointness fails for the truncated arm (endpoints effects) in a way that
cannot be repaired by re-truncating; (c) a literature snippet showing this is Meyerson's or
Schwartz's own second example, which would rescope the lane to reconstruction.

**Meyerson?** The reported sharpness example is the obtuse isosceles triangle, i.e. wedge
type. A spiral mechanism is natural enough that experts plausibly know it; Schwartz's
"topological information" paper is the likeliest home. Guess: ~40% known somewhere. Still
worth doing: "the wedge is not the only mechanism" changes what the exceptional-set
structure question (I5) even means, and a fully explicit witness is checkable in-repo.

**Square test.** The construction blocks the $60°$ rotation at one point; with $90°$ it
blocks the $90°$ rotation ($e^{c\pi/2} = 1$ iff $c = 0$) and would make $O$ fail to be the
apex of an inscribed isosceles *right triangle*. No statement about squares is produced in
either direction. Pass (vacuously — it is a counterexample construction, not an existence
proof).

### I3. Scalene shapes via spiral similarity: attack the "all but two" bound where it is not known

**Idea.** For a non-equilateral triangle shape $T$ and a chosen corner with angle $\beta$ and
adjacent-side ratio $\lambda$, the rotation trick does not degenerate — it becomes a **spiral
similarity** $\sigma_{O,\beta,\lambda}$ (rotate $\beta$, scale $\lambda$), and Observation R
generalises verbatim: $O$ is a vertex of an inscribed $T$-similar triangle in that corner
role iff $J \cap \sigma_O(J) \supsetneq \{O\}$ (up to the finitely many corner roles and
orientations; $\sigma^{-1}$ handles the $\lambda \leftrightarrow 1/\lambda$ swap). Two
consequences worth chasing:

- **The measure argument dies for $\lambda \ne 1$.** Lemma A's no-nesting half is an
  equal-area argument under an isometry. A spiral similarity with $\lambda < 1$ *can* nest:
  $\sigma(\overline\Omega) \subseteq \overline\Omega$ touching only at $O$ is exactly what
  happens at a log-spiral tip of matching pitch. So the equilateral case is special in a
  precise, statable way: *the isometry kills nesting; for every other side ratio, nesting is
  a live exceptional mechanism.* This locates "the boundary between where the rotation trick
  works and where it doesn't", which the round's brief asked for.
- **Target: three or more exceptional points for a scalene $T$.** At a log-spiral tip of
  pitch $c$, the realisable corner roles are exactly those on the pitch curve
  $\lambda = e^{c\beta}$ (spiral maps into itself iff $(\beta,\lambda)$ sits on it; parallel
  and disjoint otherwise). For a scalene $T$, all corner roles have $\lambda \ne 1$, so a
  single pitch $c$ avoiding the finitely many role points blocks them all locally. Three
  spiral tips of suitable pitches on one curve, globally arranged, would give
  $|E_T(J)| \ge 3$ — which would settle (negatively) the "does the all-but-two conclusion
  hold for every shape?" question that [`../../README.md`](../../README.md) records as
  status-unknown (open item 2). Even the failure of the construction, if it fails for a
  reason, teaches where Schwartz's uncountable $G(J)$ comes from.

Provisional budget: Jordan; the witness would be explicit. Depends on I2's construction
technology; do not start before I2 resolves.

**Kill.** (a) I2 dying kills this automatically; (b) a proof that any two spiral tips on one
Jordan curve force a realising intersection for at least one corner role (a "two tips
interfere" lemma) — that would be a *positive* structural result and should be written up as
such; (c) confirmation that Schwartz's $G(J)$-complement is known to be always at most
two-point-exceptional, i.e. the question was not open after all.

**Meyerson?** Meyerson/Kronheimer/Nielsen prove *existence* for all shapes; the vertex-wise
"all but two" for non-equilateral shapes is exactly what one unverified snippet called not
known for any other shape. This is the round's only idea aimed at something the README
explicitly flags as possibly open. Confidence the target is genuinely open: moderate
(~50%), resting entirely on secondary snippets. Confidence the spiral mechanism is the right
tool: speculative.

**Square test.** The whole idea is about triangle shapes; the $90°$-for-$60°$ substitution
does not parse (a square is not a triangle corner role). The adjacent worry is instead: does
the spiral-similarity iff secretly prove strong square statements? No — one spiral
similarity constrains a *pair* $(P, \sigma(P))$, three points total with $O$; a square needs
a fourth constrained point. Pass.

### I4. A sharp turning criterion for convex arcs — where the theorem first fails for non-closed curves

**Idea.** The existence theorem is false for arcs: a **circular arc of angular extent
$< 60°$** inscribes no equilateral triangle (all chord directions from any of its points span
$< 60°$ — a wedge-test argument at every point simultaneously), and a segment is the
degenerate extreme. Conjecture the exact boundary, for the class where our machinery is
strong:

> **Speculative criterion.** A convex arc $\gamma$ (connected subset of the boundary of a
> convex body) inscribes an equilateral triangle iff its direction spread (angle between
> extreme chord directions / total turning) is $\ge 60°$, with an equality case needing a
> Theorem-B(ii)-style attainment condition — a polygonal corner of exterior angle exactly
> $60°$ succeeds, a circular arc of extent exactly $60°$ is expected to fail.

Hand computation already done for the two-segment arc (journal): legs meeting at interior
angle $\theta$ inscribe a triangle iff $\theta \le 120°$, i.e. turning $\ge 60°$, with the
apex-locus cone $(90°, 120°]$ from the bend doing the work — an intermediate-value argument
in one scalar, the same shape as the convex lane's Theorem B. The general convex-arc case
looks reachable with the radial-function toolkit already built in
[`../convex-vertex-criterion/README.md`](../convex-vertex-criterion/README.md) (which this
idea may *not* assume — `sketch` — but may re-derive).

Provisional budget: convex + arc; no JCT (an arc separates nothing — that is the point; the
sector/dichotomy machinery must be replaced by direct radial arguments, which is the actual
work).

**Kill.** An exact two-segment or three-segment polygonal arc with turning $> 60°$ and no
inscribed equilateral triangle (finitely checkable in $\mathbb{Q}(\sqrt3)$-adjacent fields)
kills the criterion as stated; if the equality-case bookkeeping grows past a page, retreat to
the strict-inequality statement and stop.

**Meyerson?** Very likely subsumed: the reported proof outline goes through "end-straight
triods", which suggests the paper handles arc-like pieces with controlled ends. Being second
is fine here — the value is a *self-contained, sharp, checkable* statement for the frontier
class "not a Jordan curve", which the README lists as unknown-to-us (open item 3), and it is
completable without any literature access.

**Square test.** With $90°$: "convex arc with turning $\ge 90°$ inscribes an isosceles right
triangle" — plausible, easy, and again not a square (fourth corner). Pass.

### I5. Exceptional-pair rigidity: what does $E(J) = \{O_1, O_2\}$ force?

**Idea.** In the only witness we have (the $30$–$30$–$120$ triangle), the two exceptional
points realise the **diameter** of the curve. Question-first: run the (other lane's) exact
polygon enumerator over polygons with two exceptional vertices and tabulate invariants of
the pair — $|O_1O_2|/\mathrm{diam}(J)$, mutual wedge orientations, whether each $O_i$ lies
in the other's blocked cone. Conjecture-second: candidates include "$|O_1O_2| = \mathrm{diam}$"
(strong, probably too strong once non-convex examples exist) and "$|O_1O_2| \ge
\tfrac12\mathrm{diam}$" (weaker). I1's half-density bound at *both* points simultaneously is
the obvious proof tool if a pattern survives: two points at which $\Omega$ fills at most half
of every ball, on one bounded domain, should not be free to sit anywhere.

Provisional budget: polygonal for the census; Jordan for any eventual theorem.

**Kill.** A polygon census with $\ge 2$ exceptional vertices showing $|O_1O_2|/\mathrm{diam}$
scattered across $(0,1]$ with no floor — then no rigidity exists and the write-up is the
(valuable) negative census. If I2's spiral tips work, test the conjecture against a
two-spiral-tip curve immediately; it is the likeliest counterexample.

**Meyerson?** The bound $\le 2$ is his; snippets say nothing about *where* the two points
can be. Guess: not in the paper (~70% novel as a question, no confidence about the answer).

**Square test.** Not an existence argument; with $90°$ it asks about pairs of points failing
to be right-isosceles apexes, a different and unstudied set. No transfer either way. Pass.

### I6. Extremal problem: the largest guaranteed triangle, correctly normalised

**Idea.** Normalising by diameter is dead on arrival — a $1 \times \varepsilon$ rectangle
has diameter $\approx 1$ but every inscribed equilateral triangle has side
$O(\varepsilon)$ (three points within $\varepsilon$ of a line that are pairwise equidistant
are pairwise within $\approx 2\varepsilon/\sqrt3$). The right convex normalisation is
**width** $w(J)$ (minimal width of the convex hull): conjecture there is a sharp constant
$c$ with $\max\{\text{inscribed side}\} \ge c \cdot w(J)$ for every **convex** $J$, find $c$
and the extremal body (candidates to test first: the equilateral triangle itself, where the
max inscribed side is $(2/\sqrt3)w$; the $30$–$30$–$120$ witness; Reuleaux-adjacent bodies).
For general Jordan curves, decide whether any positive-constant normalisation survives at
all — a thin spiral strip has width comparable to diameter and is the candidate killer.

Provisional budget: convex for the constant; the general-curve half is a search for a
counterexample, budget-free.

**Kill.** For the convex half: a convex polygon family with $\max$-side$/w \to 0$ (exact
enumerator check) — would be surprising and publishable-in-repo either way. For the general
half: the spiral strip either kills every normalisation (write that up, done) or resists,
which after one exact computation session means park it.

**Meyerson?** Quantitative refinements are exactly what the README's open item 4 says we
could not source. Inscribed-triangle extremal problems over convex bodies are classical
territory (largest-area triangle etc.), so the convex constant may exist in the convexity
literature rather than the peg literature. Guess: ~50% known, unlocatable from here. A sharp
constant with an exact extremal body would still be verifiable in-repo by the polygon lane.

**Square test.** With $90°$: "guaranteed inscribed square of side $\ge c \cdot w$" would
presuppose the square peg theorem for the class considered — for convex curves squares *do*
exist (cited in the README's contrast row), so the convex version is legitimate there and
the general version is automatically out of bounds. The argument shape (optimise over an
existence set) never proves existence, so no transfer. Pass.

### I7. The modulus of goodness $m(O)$ and how triangles die at $E(J)$

**Idea.** For $O \in J$ let $m(O) = \sup\{\text{side of inscribed equilateral triangles at }
O\}$ ($0$ if none). Two-line compactness sketch: limits of inscribed triangles with side
$\ge \delta > 0$ are inscribed triangles, so the sup is attained when positive and $m$ is
**upper semicontinuous**; consequently if $O_n \to O$ with $m(O_n) \ge \delta$ then
$m(O) \ge \delta$ — so $m$ is *forced to vanish continuously* on approach to an exceptional
point: $m(O_n) \to 0$ whenever $O_n \to O \in E(J)$. (Note usc here is safe precisely
because the side is bounded *below* along the sequence — the noncollapse is assumed, not
concluded; [`../../RULES.md`](../../RULES.md) §2 compliant.) The concrete deliverable: the
**rate**. On the $30$–$30$–$120$ witness, compute $m(O_t)$ exactly for $O_t$ at distance $t$
from a $30°$ apex and extract the exponent $\gamma$ in $m \asymp t^\gamma$ (expected
$\gamma = 1$ by scaling heuristics, but the wedge geometry may say otherwise). Then
conjecture and polygon-test a general modulus $m(O) \ge c \cdot d(O, E(J))^\gamma$ for
convex curves.

Provisional budget: Jordan for the usc remark; polygonal/convex + exact arithmetic for the
rate.

**Kill.** If the exact computation on the witness shows $m$ is *not* monotone-comparable to
$t$ near the apex in any clean way (oscillating rate), record the numbers and stop —
"there is no modulus" is the finding. If the usc sketch breaks (it should not; it takes no
limit of degenerate triangles), the idea dies and that break must be understood, because
I1's contrapositive quietly relies on the same compactness pattern.

**Meyerson?** Almost certainly not in a 1980 nine-page paper; this is a quantitative
refinement in the README's open item 4 territory. Guess: ~70% novel, low stakes.

**Square test.** $m$ with squares would be identically $0$ on curves with no inscribed
square at $O$ — nearly all points even on nice curves, per the convex lane's twelve-points
observation. The usc argument is shape-agnostic and proves nothing about existence. Pass.

### I8. The orientation set $\Phi(J)$ — with an immediate refutation to bank

**Idea.** Let $\Phi(J) \subseteq \mathbb{R}/120°$ be the set of orientations of inscribed
equilateral triangles. First deliverable is a **refutation**: "every Jordan curve inscribes
an equilateral triangle of every orientation" is *false*, witness the thin
$1 \times \varepsilon$ rectangle — by the I6 computation all inscribed triangles are
$O(\varepsilon)$-small with two vertices on one long side, so their orientations cluster in
an $O(\varepsilon)$-neighbourhood of the two axis-aligned classes; a $45°$-tilted triangle
is impossible for small $\varepsilon$. (Convexity does not save orientation-surjectivity.)
Then the real questions: is $\Phi(J)$ always closed (not obvious — orientations can
accumulate along triangles whose side $\to 0$, and such limits carry no triangle)? Is it
connected for convex $J$? What are the realisable $\Phi$? All exactly computable per polygon.

Provisional budget: polygonal for computations; Jordan for structure questions.

**Kill.** If Schwartz's paper (once readable) turns out to be precisely a computation of the
homotopy/homology of the space of inscribed triangles including its orientation map — the
likeliest single overlap in this whole file — the lane rescopes to reconstruction.
Numerically: if random polygons always give $\Phi = $ everything or always an interval, the
structure question is boring; record and stop.

**Meyerson?** Nielsen's density theorem is about vertex *positions*, not orientations;
Schwartz's "spaces of inscribed triangles" almost certainly touches orientation. Guess: the
refutation is folklore-level (but cheap to bank exactly); the structure of $\Phi$ ~40%
addressed by Schwartz.

**Square test.** Orientation-surjectivity for squares fails maximally (a triangle has
exactly 3 inscribed squares — finitely many orientations), and our refutation witness is the
same in spirit. Nothing transfers toward existence. Pass.

### I9. The side-length spectrum $S(J)$ as an inverse problem

**Idea.** $S(J) = \{s > 0 : J \text{ inscribes an equilateral triangle of side } s\}$ is
nonempty (the theorem) and, away from $0$, closed and bounded by the diameter — compact in
$(0, \mathrm{diam}]$ once one shows small sides cannot accumulate at a positive
non-realised value (same compactness pattern as I7). The circle shows $S$ can be a single
point. Inverse question: **which compact subsets of $(0,1]$ arise as $S(J)$** (after
scaling)? Guess: finite unions of points and intervals all arise (multi-scale bump
constructions: a big triangle across the curve, small triangles on a decorated corner,
nothing in between); whether *every* compact set arises is the interesting edge.

Provisional budget: Jordan; constructions polygonal-plus-limits, so all four obligations of
[`../../RULES.md`](../../RULES.md) §4 apply to any limit construction — this is the idea
most exposed to that section.

**Kill.** An unexpected closure/connectivity obstruction (that would be a theorem — keep
it); or the first two-component construction already failing its exact check; or the §4
obligations making every limit construction longer than the payoff, in which case park after
the finite-union-of-intervals case.

**Meyerson?** Almost certainly not; this is invented here. ~80% novel as a question;
no confidence it is *interesting* to anyone downstream — rank accordingly.

**Square test.** $S$ for squares can be empty as far as anyone knows (open problem); the
inverse problem does not parse without existence. No transfer. Pass.

### I10. The solution variety $\Sigma(J) \subseteq J \times J$ for polygons — exact topology census

**Idea.** Inscribed equilateral triangles with vertex order are the points of
$\Sigma(J) = \{(O, q) : q \in J \cap \rho_{O,60°}(J)\}$, a piecewise-algebraic curve over
$\mathbb{Q}(\sqrt3)$ for a rational polygon, containing the degenerate diagonal
$\{(O, O)\}$. Compute its exact combinatorial topology per polygon: number of components,
which components meet the diagonal, the image of projection to the first factor (= the good
set). Data-driven conjectures: is the diagonal always in the closure of the nondegenerate
part except at exceptional points? Do components ever project onto proper sub-arcs
("trapped families")? This is the pair-$(O, \theta)$ continuity idea from the brief made
finite and exact — and it is the natural machine behind I5's census and I8's $\Phi(J)$.

Provisional budget: polygonal, exact arithmetic ([`../../RULES.md`](../../RULES.md) §5).

**Kill.** If the variety's combinatorics explode (component counts growing so fast per
vertex that no pattern is visible by $n \approx 10$), record the tables and stop. This idea
cannot be *wrong*, only barren — which is why it must not rank above the falsifiable ones.

**Meyerson?** Schwartz's title *is* "on spaces of inscribed triangles"; assume the
qualitative topology is his. The exact per-polygon census is in-repo tooling work and new
regardless. Belongs to the `experiments/` lane's skill set; propose as an issue there, not
as a second enumerator here.

**Square test.** The square analogue of $\Sigma$ has codimension 2 in $J \times J$ (two
constraints, fourth vertex) — generically empty components; the census machinery transfers
but proves nothing. Pass.

### I11. The frontier for non-Jordan continua: what is the minimal hypothesis?

**Idea.** Order the failures: segments fail (collinear); circular arcs of extent $< 60°$
fail (I4); every continuum *containing* a Jordan curve succeeds (inherit). So the open
frontier is exactly the **tree-like continua** (dendrites), with triods the base case — and
the reported (P3, unverified) outline of Meyerson's proof is *built* on triods, so this is
likely his home turf. In-repo version worth having anyway: a self-contained statement and
proof for the simplest dendrites (triods made of three segments; then three convex arcs)
of a criterion in the style of I4 — which turning/spread data of the three legs decide
inscription?

Provisional budget: explicit continua only; nothing general.

**Kill.** Confirmation that Meyerson's triod lemma states exactly this (rescope to
reconstruction); or the three-segment case already requiring case analysis past a few pages
— then the criterion is not clean and the idea was wrong about there being one.

**Meyerson?** Highest overlap probability in the file (~80%): his title says "continuous
curves" and his method reportedly says triods. Rank low for novelty, moderate for
usefulness as reconstruction fodder once the paper is readable.

**Square test.** A triod cannot contain a Jordan curve, and squares on trees are as
unconstrained-by-parity as ever; nothing transfers. Pass.

### I12. Integral-geometric averaging — dead on arrival, recorded so nobody walks in

**Idea (pre-refuted).** "Average the count $\#(J \cap \rho_O(J))$ over $O \in J$ against
arclength; positivity forces some good $O$." Dies three times: (1) arclength presupposes
rectifiability — smuggled budget; (2) the count needs finiteness/transversality — undefined
for wild curves and unavailable even a.e. without exactly the local structure §6.4 of the
rotation lane could not certify; (3) the degenerate intersection at $O$ contributes to every
fibre, so positivity of the average is vacuously true and separates nothing. **Kill:**
already met at proposal time. Recorded per [`../../RULES.md`](../../RULES.md) §7-target list
item 5 (documented dead candidates) so the next ideation round does not regenerate it.

**Meyerson?** Certainly not his route. **Square test:** with $90°$ the same average is
positive for the same vacuous reason and proves nothing about squares — the test is passed
only because the argument proves nothing at all, which is the point.

### I13. Mod-2 crossing in the pair picture — collapsed, but its corpse feeds I1

**Idea (collapsed on inspection).** Hope: "two closed curves cross evenly; $O$ is one
intersection; parity forces a second." Inspection: if $J \cap \rho_O(J) = \{O\}$ then
$\rho(J) \setminus \{O\}$ is connected and disjoint from $J$, hence lies **entirely in
$\Omega$ or entirely in $E$** — so there is no crossing at $O$ in any separation sense, and
parity has nothing to say; this is exactly the rotation lane's Lemma A dichotomy re-found
from the parity side, and the local end-interleaving criterion it suggests (ends of $J$ at
$O$ interleaving with their $60°$ rotates) turns out to certify only what the sector
criterion already certifies, while the wild-curve case hits the identical third-strand wall
as §6.4. **Kill: met** — no new theorem lives here. Salvage: the dichotomy statement "$O$
exceptional $\Rightarrow \rho_O(J)\setminus\{O\}$ is trapped in one complementary
component" is the cleanest formulation in the repo of what exceptionality *means*, and it is
the exact input I1 quantifies with measure. Recorded as collapsed-with-salvage.

**Meyerson?** The dichotomy is surely implicit in any rotation proof. **Square test:** the
parity that fails here for triangles fails worse for squares; nothing transfers.

---

## Triage

| Idea | Verdict | One line |
|---|---|---|
| I1 half-density | **now** | Elementary, new-to-repo, strictly stronger than the sector criterion on an explicit pinwheel, Lean-plausible core, near-zero risk. |
| I2 spiral tip | **now** | Concrete construction with a checkable payoff ("wedge is not the only mechanism"), moderate risk, enriches every structure question downstream. |
| I4 convex-arc criterion | **now** | Completable with in-repo machinery, sharp iff target, colonises the "not a Jordan curve" frontier cheaply. |
| I3 scalene $\ge 3$ | later | Highest ceiling in the file (README-flagged unknown) but gated on I2's construction technology; do not start first. |
| I5 exceptional-pair rigidity | later | Census-first; needs the `experiments/` enumerator lane and ideally I2's second witness type. |
| I7 modulus $m(O)$ | later | Small, safe, exact-computation shaped; a good filler task, not a lane. |
| I6 extremal constant | later | Real question, but the general-curve half likely dies on the spiral strip; convex half worth one session. |
| I8 orientation set | later | Bank the thin-rectangle refutation cheaply whenever convenient; structure half waits for Schwartz to be readable. |
| I10 $\Sigma(J)$ census | later | Tooling for the experiments lane; propose as an issue there, produces data not theorems. |
| I9 spectrum $S(J)$ | later (low) | Fun inverse problem, most exposed to §4 limit obligations, no downstream customer yet. |
| I11 dendrite frontier | later (low) | ~80% Meyerson's own turf; becomes reconstruction fodder once the paper is readable. |
| I12 averaging | **DOA** | Pre-refuted at proposal time; recorded to prevent regeneration. |
| I13 mod-2 crossing | **DOA (collapsed)** | No new theorem; its dichotomy salvage is already I1's input. |

## Ranked shortlist of 3

1. **I1 — the half-density obstruction.** Best value-to-risk in the file: a one-page lemma,
   a genuinely new sufficient criterion (the pinwheel point is good by density and invisible
   to the sector criterion), a quantitative constraint on exceptional points at every scale,
   and a topology-free core inequality that is the most Lean-shaped object anyone has
   proposed here since the wedge test. If only one issue gets opened from this round, open
   this one.
2. **I2 — the spiral-tip exceptional point.** The most *informative* construction available:
   it would prove the wedge obstruction is not the whole story of $E(J)$, on a rectifiable
   witness, with everything explicitly checkable. Riskier than I1 (global closing-arc
   disjointness is unproved), and its failure-with-reason would itself be a §6.3-grade
   refutation write-up. Also the gateway to I3, the only idea aimed at a possibly-open
   published question.
3. **I4 — the convex-arc turning criterion.** Guaranteed-completable with the radial-function
   toolkit, produces a sharp iff with an honest equality-case subtlety matching the convex
   lane's Theorem B(ii) pattern, and plants a flag on the non-Jordan frontier where the
   README says our knowledge is weakest. Likely known to Meyerson; being second with a
   self-contained checkable proof is exactly what this repo is for.

## What I believe is genuinely novel here, with honest confidence

- **I1's density formulation** (exceptional $\Rightarrow$ interior density $\le 1/2$ in
  every ball, and the pinwheel separation from the sector criterion): ~30% novel. The
  ingredients are too elementary to be safely presumed new, but no snippet we have seen
  states anything measure-theoretic about exceptional points.
- **I2's spiral mechanism** as an explicit non-wedge exceptional point: ~40% novel;
  Schwartz is the likeliest prior home.
- **I3's target** ($|E_T| \ge 3$ for scalene $T$): the *question* appears genuinely open
  per the README's snippet evidence (~50%); the *approach* is pure speculation.
- Everything else I assume is known, folklore, or minor. All of these estimates rest on
  zero primary sources, per the provenance warning in [`../../README.md`](../../README.md).
