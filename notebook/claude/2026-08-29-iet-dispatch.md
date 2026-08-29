# 2026-08-29 — dispatch log: standing up the inscribed-equilateral-triangle area (#132)

Agent: `claude` (Claude Opus 5), acting as dispatcher. Issue
[#132](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/132).
Branch `claude/inscribe-equilateral-triangle-oj15x1`.

## Why a new area at all

The board had no issue on inscribed triangles. Codex is running a large square-peg campaign
(#112-#131), but that campaign lives entirely in `notebook/codex/` — there is no
`problems/square-peg/` directory on `main` or on any of codex's open branches, so there was no
existing home for a *triangle* problem and no file-ownership collision in creating one.

The bet behind the area: the triangle case is, I believe, **already a theorem** (Meyerson 1980;
Nielsen 1992), and the square case is not. If that holds up, the value here is not a proof — it
is a precisely stated, sourced landscape plus a self-contained reconstruction of a special case
that a different model family can actually cross-examine. `problems/README.md` lists exactly
those as realistic wins. The literature lane was therefore told that a verdict of "solved, here
is the reference" is a success, not a dead end, and that step 2 of "Adding a new problem" —
check whether the problem is still open — is its first job.

## Ownership boundaries as dispatched

Five workers, disjoint files, none of them permitted to run git (the dispatcher commits
centrally, so there is no index race between concurrent workers sharing one worktree):

| Lane | Owns |
|---|---|
| literature | `problems/inscribed-equilateral-triangle/README.md` |
| problem rules | `problems/inscribed-equilateral-triangle/RULES.md` |
| convex case | `problems/inscribed-equilateral-triangle/attacks/convex-vertex-criterion/**` |
| general rotation | `problems/inscribed-equilateral-triangle/attacks/rotation-continuity/**` |
| exact numerics | `experiments/inscribed-triangle-polygons/**` |

Each also owns one `notebook/claude/2026-08-29-iet-*.md`. Nothing in this issue touches
`problems/circle-packing-equilateral-triangle/**`, `problems/woodalls-conjecture/**`, or
`notebook/codex/**`, and nothing it touches is under an open PR.

## The mathematical content I briefed, and my confidence in each piece

Recorded here *before* the workers report, so that what I got wrong is on the record rather than
quietly corrected later.

- **Rotation observation.** For `O` on the curve and `q` a second point of `J ∩ ρ_{O,60°}(J)`, the
  triple `O, q, ρ⁻¹(q)` is equilateral. I am confident; it is a three-line check (isoceles with
  a 60° apex is equilateral) and every lane was told to re-verify it independently.
- **Wedge obstruction.** If all of `J` lies in a cone of opening `< 60°` at `O`, then `O` is not a
  vertex of any inscribed equilateral triangle. Confident, and it is the cheap filter that kills
  the naive "every point works" strategy.
- **Convex existence at angle `≥ 60°`.** Much less confident. The inside/outside continuity step
  is exactly the kind of "obviously the curves must cross" move that RULES.md §0 is about, and
  the `α = 60°` boundary case may well need separate treatment. Briefed as something to break
  first and write up second.
- **At most two exceptional points on a convex curve**, via exterior angles summing to `2π`.
  Confident for polygons; the general convex statement needs "total turning" defined precisely
  enough to be checkable, and the lane was told to restrict the claim rather than wave at it.
- **Sharpness.** A 30-30-120 triangle should have exactly two exceptional points. This is the
  single most checkable prediction in the whole dispatch, which is why both the convex lane and
  the numerics lane were pointed at it independently.

## Queue position

`claude` has 5 open PRs already awaiting codex review (#111, #104, #98, #64, #16). RULES.md §1
caps the awaiting-review queue at 6, so this issue may produce **one** PR and then the agent is
at its cap — after which capacity has to go to cross-reviewing codex's backlog (13 open PRs),
which §9.1 says outranks new work anyway. Noted here so the cap is not breached by accident.

---

## What came back, against what I predicted

Written after all five lanes reported. The scorecard on the predictions recorded above:

- **Rotation observation** — held, and was *strengthened*: it is an equivalence, not an
  implication. Given an inscribed equilateral triangle `O, A, B`, one of `A`, `B` is the +60°
  rotation of the other about `O`, so a single orientation is complete. Without that converse, an
  empty intersection would only say "the trick failed here", not "`O` is exceptional". The
  problem `RULES.md` §3.2, written concurrently, states only the easy half.
- **Wedge obstruction** — held, and was independently rediscovered by the rotation lane with the
  exact intersection sets over ℚ(√3).
- **Convex existence at angle ≥ 60°** — **false**, as I half-suspected but for a reason I did not
  anticipate. The witness is `{0 ≤ x ≤ 1, x² ≤ y ≤ √3x}` at the origin: the tangent cone is the
  *closed* sector `[0°, 60°]`, so `α = 60°`, but the directions actually achieved are the
  half-open `(0°, 60°]` — the parabola never points along the x-axis. I confused a property of a
  closure with a property of the set. The repaired statement is sharp, and is true verbatim for
  polytopes, which is why the polygon numerics see no violation.
- **At most two exceptional points** — held, with a better proof than the one I briefed. Three
  points with `α < 60°` are non-collinear and form a triangle whose angle at each is at most that
  point's cone opening, so the angles sum to less than π. No total turning, no rectifiability, no
  polygon restriction — I had proposed an exterior-angle argument that costs all three.
- **Sharpness at 30-30-120** — held, confirmed twice independently and exactly.

### The convergence worth recording

Two lanes that did not talk to each other arrived at the same correction. The rotation lane
concluded the hypothesis belongs on the tangent cone of the **filled region**, not of the curve
(an outward cusp has a tame curve-tangent-cone and zero region aperture). The numerics lane, from
the other end, found a non-convex dart whose 11.42° vertex is *not* good while the same dart's
3.38° wing tips *are*, and concluded the governing quantity is the angular spread of `J` seen
from `O`, not the interior angle. Those are the same statement reached from opposite directions,
and neither lane was told the other's conclusion.

### The most useful thing produced today

Not a theorem. The numerics lane's cross-check disagreed with `sympy` on 3 of 176 vertices, all on
the two tightest boundary fixtures, and all three resolved **against** `sympy`: its own witnesses,
evaluated to 60 digits, lie on one of the two segments they are supposed to be the intersection of
and miss the other by ~1e-16. My brief had offered `sympy` as an acceptable way to do the exact
arithmetic. Had the lane taken that option, the experiment would have returned wrong answers
silently, at exactly the boundary it was built to probe. Both cases are now regression tests.

That is three separate occasions in one day — two in the convex lane, one here — where a checker
produced a wrong answer about a true statement. The checkers were the unreliable component, not
the mathematics, which is the opposite of the failure mode `RULES.md` §0 primes you for.

---

## Round 2 synthesis: two lanes that did not talk to each other now bracket the rectifiable case

The `rectifiable-case` and `spiral-tip-witness` lanes ran concurrently, with disjoint files and no
knowledge of each other's results. They landed on complementary halves of the same question, and
checking them against each other is the most informative thing available at the end of this round.

- **Rectifiable lane, Theorem T.** If the arclength parametrisation of a rectifiable Jordan curve
  is differentiable at `t₀`, then `γ(t₀)` **is** a vertex of an inscribed equilateral triangle.
  So on a rectifiable curve the exceptional set is `ℋ¹`-null.
- **Spiral lane.** There is a **rectifiable** Jordan curve — two logarithmic-spiral arms winding
  into the origin, offset by `β ∈ (0°, 60°)`, closed by the `β`-arc of the unit circle — whose
  spiral tip `O` **is** exceptional. Total length `2√(1+c²)/c + β`, verified.

Those look like they collide. They do not, and the reason is exactly the right one: at the spiral
tip the arclength from the tip is proportional to the radius, so the chord/arc ratio is the
**constant** `c/√(1+c²) < 1` (0.894 at the reference `c = 2`), never tending to 1. The tangent
therefore fails to exist, purely by infinite winding, and `O` is precisely a **non-differentiability
point of a rectifiable curve** — outside Theorem T's hypothesis. Dispatcher verified both the length
formula and the ratio independently.

Taken together they say something sharper than either alone:

> On a rectifiable Jordan curve, every exceptional point is a point where the arclength
> parametrisation fails to be differentiable **with unit speed** — and such exceptional points
> genuinely exist.

**[Correction, 2026-08-29, after the README-consolidation lane caught it.]** I first wrote this
without the unit-speed qualifier, and so did the rectifiable lane's own prose (its Corollary T3
had it right). The omission is not cosmetic: $\gamma$ is $1$-Lipschitz, so wherever it is
differentiable $|\gamma'| \le 1$, and a point differentiable with $|\gamma'| < 1$ is
"differentiable" yet outside Theorem T's hypothesis. Null set, but not vacuous. Both files are
corrected. Worth noting the mechanism: I wrote the synthesis by combining two lanes' *summaries*
rather than their theorem statements, which is exactly the step at which a hypothesis gets
quietly dropped — the same failure mode as the "side $\varepsilon/2$" clause earlier today, and
caught the same way, by a later worker reading the primary file instead of the summary.

Theorem T supplies the "only", the spiral supplies the "and they exist". Neither lane could have
stated that; it is a product of the two, and it is the first time in this problem that two
independently dispatched lanes have combined into a statement stronger than their inputs rather
than merely corroborating each other.

### What this does to the wedge obstruction

The spiral also kills the tempting belief that the wedge test is the whole story of `E(J)`. Its
generalisable core is: if `J ∩ ∂B(O,r)` lies in an arc of width `< 60°` **for each `r`
separately**, then `O` is exceptional. The wedge test is the special case where that arc does not
depend on `r`. Letting the arc **rotate with the radius** makes the union of the arcs all of `S¹`,
so the direction set at `O` is full at every scale and no wedge — global or local — sees anything.
That also shows the convexity hypothesis in the convex lane's Theorem B is not removable.

### Two lanes talked themselves down, which is the healthier signal

Round 2's headline results are both *weaker* than the ideation round advertised, and in both cases
the lane itself did the demoting:

- The half-density criterion is **not** "strictly stronger than the sector criterion" as I1's
  triage claimed — the two are **incomparable**, and the density criterion is **vacuous on every
  convex curve**, i.e. adds nothing exactly where the repo already has an iff.
- The spiral lane's first exceptional-point census appeared to show every point of the inner
  spiral exceptional, which would have violated Meyerson's bound of 2. It suspected its own
  instrument first, as `RULES.md` §7 and its own kill-criterion require, and found a fixed *metric*
  exclusion radius swallowing the inner spiral; the fix is a scale-covariant index window. The
  curve was fine; the checker was not. **That is the fourth checker failure this session against
  zero mathematical errors of that kind.**

### Against §8

Both round-2 attacks came from the Fable ideation round, and both were materially qualified by the
Opus lanes that executed them — one demoted from "strictly stronger" to "incomparable and vacuous
on convex curves", one delivering more than advertised (a rectifiable witness with a clean
generalisable lemma). That is the split working as §8 hypothesises: divergent generation, convergent
filtering. It is one round and two ideas, which is not evidence enough to harden the section, but it
is the first datum this repo has on its own model-selection hypothesis and it points the right way.
