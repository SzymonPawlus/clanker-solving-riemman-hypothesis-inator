# 2026-08-26 — r6-interaction (execution worker, round 6)

Assignment: find a lower-bound scheme whose conclusion is **not affine in (area, perimeter)** and
which charges for interactions between regions. Output expected to be a measurement, not a proof.

Work lives in `problems/circle-packing-equilateral-triangle/attacks/r6-interaction/` and
`experiments/packing-r6-interaction/`. Branch `r6-interaction`.

## What I did, in order

1. Wrote four candidate conclusion shapes down as formulas before computing anything (C1 affine =
   Oler; C2 the (A, M)-realisability bound; C3 Oler-minus-defect / discharging; C4 pair
   correlation). Every arithmetic statement below came out of a script; none was done by hand.
2. Ran step 2 (match Oler where Oler is exactly tight): `shapes.py`. Only **C2** matched at every
   triangular `n`, and it matches by an identity, not numerically.
3. Ran step 3 for C2: `rho_probe.py`, multistart SLSQP minimisation of `max(√r, M/3)` over free
   `n`-point unit-separated configurations. `n = 9` (300 starts) and `n = 16` (60 starts) both
   return exactly the lattice value and never improve.
4. While reading the F3 requirement I noticed the thing that turned out to matter more than the
   candidate table: the target `Δ(k) − 1` is where `N(a)` jumps by **2**, not 1. Wrote that up as
   the **Jump Lemma** and verified the jump structure over the whole proven range from the `cited`
   `s(n)` table (`jumps.py`). Every jump of size 2 is at `a = k − 1`; all others are size 1.

## The two things worth remembering

- **The `+1` at `Δ(k) − 1` is one half of a jump of two, and continuity is what cannot supply it.**
  This generalises `r4-dual` from "affine in (A, M)" to "any continuous conclusion of any shape" —
  but only on that family. At every other `n` the jump has size 1 and continuity is fine. So
  `n = 16` and `EO(k)` need *different* kinds of method, and the repo should stop treating them as
  one target.
- **The non-affine part of the (A, M) class is worth 14.3 % of the `n = 16` gap and nothing at all
  at `Δ(k) − 1`.** That is a ceiling, measured, for a whole class rather than a single method.

## Mistakes and near-misses

- My first instinct was that a continuous bound cannot beat Oler *anywhere*. That is wrong, and the
  jump-size dichotomy is what corrected it: at jump-size-1 targets a continuous bound can be sharp.
  I nearly wrote the strong version into the README before checking `n = 8, 11, 12, 13`.
- I did **not** observe an infeasibility bug, but I guarded against the one problem `RULES.md` §0
  names: every configuration the optimiser returns is rescaled so its minimum separation is exactly
  `1` before its value is recorded, so no reported number can come from a configuration that is
  infeasible by `10⁻⁸`. Worth saying plainly rather than implying a harder path was walked.

## Left open

A rigorous lower bound on `ρ(n)` (container-free, two hull functionals) and a quantitative
stability version of Oler. Both are written up as README §5. Neither would help at `Δ(k) − 1`;
per the Jump Lemma only a classification/rigidity statement can.
