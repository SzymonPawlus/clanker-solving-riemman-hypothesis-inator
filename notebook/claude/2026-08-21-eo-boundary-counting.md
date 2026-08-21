# 2026-08-21 — Erdős–Oler k = 7: the boundary count, done properly

Worker: `claude` (Opus 5, convergent role — this is checking and exact calculation, not ideation,
`RULES.md` §8). Branch `claude/circle-equklatetal-problem-sa7tx7`.
Files I own: `problems/circle-packing-equilateral-triangle/attacks/eo-boundary-counting/**`,
`experiments/packing-eo-boundary/**`, this journal. Nothing else.

## Brief

`attacks/oler-slack-analysis/` refuted step (i) of the floored-perimeter route (hypothesis H,
face-excess nonnegativity) and flagged step (ii), `b ≤ 3⌊a⌋`, as *unjustified* — because `b`
counts points on ∂conv(E), which need not lie on ∂T. My job: find the version of the boundary
count that is actually **true** and actually **usable**.

## Kill-criteria, written before the deciding computations

1. **KC-1 (primary).** If I find an exact, unit-separated configuration inside an equilateral
   triangle of side `a` with more than `3⌊a⌋` points on ∂T, Lemma P1 is refuted and I stop
   claiming it.
2. **KC-2.** If I find an exact configuration realising a *near-extremal* `n` at a *near-extremal*
   `a` with `b` (hull-boundary count) far below `3⌊a⌋` — i.e. `b` is not perturbation-stable at the
   very configurations Erdős–Oler is about — then the count-based route is dead **regardless of how
   good the bound on b is**, and I record that as the outcome rather than looking for a
   further-restricted hypothesis H′ to save.
3. **KC-3.** If validity of *any* count-based boundary term `Φ(b)` forces the resulting inequality
   to be weaker than Oler's own on near-lattice configurations, the whole family is dead. Stop; do
   not re-scope to `Φ(n, b)` and call it a boundary count.

Explicitly forbidden to myself (`RULES.md` §6.3): re-scoping after any of these fires.

## Order of work (recorded so the write-up is not retro-fitted)

- Float-only *search* probe (no decisions) of `a_conv(b)` = least side of an equilateral triangle
  holding `b` points in convex position at separation 1, run **before** these criteria were
  written down. It reported `a_conv(b) ≈ ⌈b/3⌉` for `b = 3…10`, i.e. evidence *for* `b ≤ 3⌊a⌋`
  rather than against — the opposite of what the brief anticipated. That is what redirected the
  attack from "refute step (ii)" to "prove step (ii) and show it does not help".
- Everything after that is exact.

## Outcome

See `attacks/eo-boundary-counting/README.md`. Short version: step (ii) is **true** (proved in the
∂T reading, sharp; proved up to ⌊3a⌋ in the hull reading, conjectured sharp there). KC-2 and KC-3
both fired. The route dies at the composition of its two steps, not at step (ii).
