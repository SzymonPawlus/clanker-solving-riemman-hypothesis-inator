# Kill criterion — r6-interaction

**Pre-declared** (from the assignment, before any computation):

> If none of the candidate shapes survives step 2 — i.e. every one either fails to match Oler at
> the triangular numbers, or matches it and provably gains nothing elsewhere — record the
> candidates, the reason each died, and stop.

**Verdict: FIRED, in the informative direction — one candidate survived.**

| candidate | step-2 test (match Oler at every triangular `n`?) | outcome |
|---|---|---|
| C1 affine in (A, M) | matches, by definition — it *is* Oler | not a candidate, the baseline |
| C2 (A, M)-realisability, `a ≥ min_E max(√r, M/3)` | **matches exactly** (identity + numerics, `k = 2..8`) | **SURVIVED** — taken to step 3 |
| C3 Oler-minus-defect / discharging | matches (defect `= 0` there) but **provably gains nothing** at `Δ(k)−1`: validity forces `D = 0` at every Oler-tight configuration, and the `Δ(k)−1` optimum is Oler-tight | died at step 2, second clause |
| C4 pair correlation / Delsarte | this shape **is** `ϑ′`; its gain is measured elsewhere as exactly `0.000000` at criticality | died at step 2, second clause (on a quoted measurement, not mine) |

**What step 3 then measured for C2:** `ρ(16) ≤ 3√2`, giving a ceiling of `d(16) ≥ 8.4853` against
Oler's `8.3578` — a real but bounded gain, 14.3 % of the way to the best known construction. And
`ρ(9) ≤ 2√2 = 2.8284` against the `EO(4)` target `3`: **C2 cannot close the `+1`.**

**Second, unplanned outcome.** The lane also produced a negative stronger than the one it was sent
to test: the **Jump Lemma** (README §3) shows that on the `Δ(k) − 1` family *no* conclusion that is
left-continuous in the container scale can work, of any shape whatsoever. That answers the question
`r4-dual` left open — the collapse is not special to affine conclusions — but relocates the cause:
on that family the obstruction is **continuity**, not affineness. Elsewhere (jump size 1) continuity
is no obstruction at all.
