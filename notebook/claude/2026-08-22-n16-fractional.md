# 2026-08-22 — F2: the fractional covering relaxation for n = 16

Worker F2 on issue #97, branch `claude/circle-packing-subagents-9yg5gt`. Lane: replace the
integral 15-piece covering pigeonhole with its LP relaxation. Files:
`attacks/n16-fractional/`, `experiments/packing-n16-fractional/`.

## The one derivation that changed the plan

Re-deriving the manager's lemma before building anything (as instructed) produced a stronger
statement than the brief asked for. The brief: "a fractional cover with total weight ≤ 15 proves
a_16 ≥ a". The proof actually gives |C| ≤ Σy for any separated C, and |C| is an **integer**, so

> total weight **< 16** already excludes 16 separated points.

That is almost a full unit of extra budget over the integral method's 15 pieces, on top of the
fractional sharing itself. I checked the derivation twice and then checked it against the
sandwich on a known case before trusting it: at a ≥ √3 we have ω(a) ≥ 4 (three corners plus
centroid), so τ_f(a) ≥ 4 and no fractional cover of weight < 4 can exist above √3 — the slack
cannot overshoot a known optimum. That is also what the pipeline's control runs test
mechanically. (FINDINGS.md's warning about "a correct theorem read one step too broadly" applies
squarely to this step; it is the one to review hardest, and I said so in the README.)

## Design decisions

- Everything on an integer grid of 1/64 separation unit; pieces capped at width 63 in the three
  lattice slab directions (u, v, u+v). A little lemma makes the cap airtight: any set with all
  three slab widths ≤ w has diameter ≤ w, because Q = Δu²+ΔuΔv+Δv² is convex and its max over
  the difference polytope {|Δu|,|Δv|,|Δu+Δv| ≤ w} is w² (checked by exact vertex enumeration
  per piece, not by trusting the lemma).
- Coverage is certified on the exact partition of T_N into unit lattice triangles: a cell
  constraint counts only pieces containing the **whole** cell, so the certificate is sound with
  overlapping pieces and no arrangement computation is needed. The cost is granularity (~1–2
  units of N); the controls measure it.
- scipy LP proposes weights; they are rounded **up** to multiples of 1/2^16 and everything is
  re-verified in integer/Fraction arithmetic. The LP can only fail to find certificates, never
  make a false one.

## A caught bug worth recording

First control run: LP reported total weight 3.0 at N=111 for the n=4 control — which would
"prove" a_4 ≥ 1.7619 > √3, i.e. an impossibility. The exact verifier refused the certificate:
a generation typo had given the hypotenuse-flush boxes a v-window of width 126, diameter²
11907 = 3·63². Exactly the failure mode the defense-in-depth assert exists for; fixed by
correcting the typo *and* filtering oversized pieces before the LP ever sees them. The lesson
is the same one FINDINGS.md keeps recording: the impossible-looking good number appeared
*immediately*, and the exact layer is what stopped it.

## Framing correction absorbed mid-session

`n16-structure`'s headline ("1+2√3 is the least a at which 15 pieces are necessary") was refuted
by V4 while this lane was being built — a_15 = 4 forces 15 pieces from a = 4 already. My brief
cited that headline as motivation. The lane does not depend on it: the fractional method's
promise is the sandwich ω ≤ τ_f ≤ τ plus the strict-inequality budget, not any counting
threshold. Recorded here so the README does not silently inherit a refuted premise.

## Outcome

See `attacks/n16-fractional/README.md` for the results table, the certified bound, controls,
and the kill-criterion outcomes. Everything below was written after the runs completed.
