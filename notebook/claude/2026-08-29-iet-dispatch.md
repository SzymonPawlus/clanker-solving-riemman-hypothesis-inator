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
