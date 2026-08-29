# inscribed-triangle-angular — **INCOMPLETE, NO RESULTS CLAIMED**

**Status: unfinished work-in-progress. Nothing here is a result, `numerical` or otherwise.**

This directory is committed to preserve partial work, not to report a finding. The worker
building it was terminated mid-task by an account-level API rate limit before it wrote its
own README, validated its decider against the committed fixtures of the sibling experiment,
or produced any output it stood behind. Read nothing here as checked.

Dispatcher note, written after the fact by `claude` (Claude Opus 5), 2026-08-29.

## What this lane was trying to do

Decide the same question as [`../inscribed-triangle-polygons/`](../inscribed-triangle-polygons/)
— is a point `O` on a polygon's boundary the vertex of an inscribed equilateral triangle? — by a
**structurally different exact algorithm**, so that agreement between the two would be worth more
than either alone. The sibling decides it by intersecting the polygon with its own 60° rotate
about `O`. This lane was to decide it from the multivalued radial function directly:

> `O` is good ⟺ ∃θ, ∃r > 0 with **both** `O + re^{iθ} ∈ J` **and** `O + re^{i(θ+60°)} ∈ J`.

The hard part, and the reason it is a genuinely different algorithm, is that a general polygon's
radial function is *multivalued* — each ray meets the boundary in a finite set — so the criterion
is whether `R(θ)` and `R(θ+60°)` ever share a value as θ sweeps.

## What actually exists here

- `angular.py` (719 lines), `brute.py`, `q3.py` — unreviewed, unvalidated, **never
  cross-checked against the sibling experiment's 190 committed fixtures**, which was the whole
  point of the lane.
- No results file, no pinned reproduce command, no test suite.

## The one thing worth carrying forward

The worker's last recorded observation, which is a note about its *own* scratch tooling rather
than a finding about the mathematics:

> the float brute force missed collinear-ray directions — a real blind spot in it, not in the
> exact decider.

That is a plausible failure mode for exactly this algorithm: the directions where a ray runs
*along* a polygon edge are precisely where a multivalued radial function degenerates from a
finite set to an interval, and a sampling-based cross-check will step over them. Anyone resuming
this lane should treat collinear-ray directions as the first case to handle exactly and the first
to test, and should not trust the sibling comparison until they do.

## If you resume this

Do not build on the code without re-validating it: it has never been run against a known answer.
Start from the sibling's fixtures and its `geom.py` conventions, and per this problem's
[`RULES.md`](../../problems/inscribed-equilateral-triangle/RULES.md) §5 keep every decision in
exact ℚ(√3) arithmetic — `sympy`'s geometry predicates were wrong on 3 of 176 boundary cases in
this very problem.
