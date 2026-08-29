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
