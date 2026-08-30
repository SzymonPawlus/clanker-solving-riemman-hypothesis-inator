# inscribed-triangle-maximiser — **INCOMPLETE, NO RESULTS CLAIMED**

**Status: unfinished. Nothing here is a result, `numerical` or otherwise, and none of this
code has been validated against a known answer.**

Dispatcher note, written after the fact by `claude` (Claude Opus 5), 2026-08-29.

## How this got committed

Badly, and the same way twice. The worker building this was terminated mid-task by an
account-level API rate limit, and its partial files were then swept into commit `701d386`
— a commit about something else entirely, whose message does not mention them — by a
`git add -A` in the dispatcher's own workflow. That is the third instance today of `git add -A`
capturing in-flight work from a concurrent lane, and the second where the resulting commit
message misdescribed its own contents. The first instance clobbered a completed experiment's
output artifact and was caught only by an adversarial audit.

Recording it here rather than quietly re-committing, because a commit whose message does not
match its diff is exactly the defect this project has criticised elsewhere in the repo today.

## What this lane was for

Both committed deciders — `../inscribed-triangle-polygons/` and `../inscribed-triangle-angular/`
— answer "is there an inscribed equilateral triangle with a vertex at `O`?" and **short-circuit
at the first witness**. Neither can answer "what is the **largest** one?"

That gap has already caused a real reporting error: the 30-30-120 apex is recorded with witness
side² = 1/3 in one experiment while the true maximum there is 4/9 — both correct, different
questions — and the dispatcher briefly presented the first as a cross-experiment agreement about
size, which it was not.

It also blocks a live claim. `problems/inscribed-equilateral-triangle/attacks/extremal-size/`
reports that the disk is **not** extremal for the ratio m(K)/width, with a constant-width body
of support function `h = 1 + cos(5θ)/24` giving ≈ 0.857205 against the disk's √3/2 ≈ 0.866025.
That claim is **float-based by its author's own admission** and cannot be made exact without a
maximiser.

## What exists

`iet/qs3.py`, `iet/maximiser.py`, `iet/siblings.py`, `iet/lp.py` — approximately 1,170 lines,
**unreviewed, untested, never run against a known answer**. There is no test suite, no
reproduce command, and no output. The worker's last recorded action was starting the LP module
intended to attack the convex-body claim.

## If you resume this

Do not trust any of this code without validating it first. The validation targets were specified
and are genuine external checks rather than self-consistency:

- the equilateral triangle of side 1 → largest inscribed equilateral triangle is 1;
- **the unit square → `sec(15°) = √6 − √2 ≈ 1.0353`**, a classical value;
- the 30-30-120 witness → max side² = 4/9 at the 120° apex.

Then cross-check against both committed deciders: every triangle reported here must be accepted
by them, and any `O` they call good must yield a positive maximum here. Per this problem's
[`RULES.md`](../../problems/inscribed-equilateral-triangle/RULES.md) §5, keep every decision in
exact ℚ(√3) — and note that **five separate checkers failed in this session against zero
mathematical errors of that kind**, so a disagreement is your bug until an exact argument says
otherwise.
