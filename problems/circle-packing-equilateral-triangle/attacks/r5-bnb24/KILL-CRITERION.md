# Kill-criterion — r5-bnb24 (round-4 proposal AI)

**Stated before the runs, from the assignment.**

> If the active-region propagation does not beat PR #56's `d(12) > 6.95` benchmark within
> the compute budget, record the node counts, the propagation statistics, and the
> comparison, and STOP. Do not proceed to `n = 24` with machinery that has not beaten the
> incumbent on the incumbent's own calibration case.

Two-sided calibration gate, also stated in advance:

1. **Lower side.** The method must refute some `d` meaningfully below `d(12) = 4 + 2√3 =
   7.4641...`, and in particular must refute `d = 6.95` or higher to clear the incumbent
   (`experiments/circle-packing-bnb`, PR #56).
2. **Upper side.** The method must **never** refute any `d ≥ d(12)`. A single such
   refutation means the method is unsound and everything it produced is worthless.

Outcome is recorded in `README.md` §2 and §5.

---

## Outcome: the kill-criterion did NOT fire

1. **Lower side — cleared.** `d(12) > 71/10 = 7.1` was certified by exhaustion at level 5
   (1024 cells, 4 386 939 nodes, 54 s), i.e. **95.12 %** of `d(12) = 4 + 2√3`. The bar was
   PR #56's `6.95` (93.1 %); `attacks/r3-gridmis/` had `7.0` (93.8 %).
2. **Upper side — cleared.** Eleven controls at `d >= d(n)`, including `d(3) = 2`,
   `d(6) = 4` and `d(10) = 6` on the nose, and `n = 24` at `11.47` and `12`:
   **0 refutations** (`experiments/packing-r5-bnb24/out/validate.log`). The separate
   over-pruning control — the optimal triangular-lattice packings for
   `n = 3, 6, 10, 15, 21` mapped to cells at every level 2..6 — passes 23/23.

Because the gate cleared, the `n = 24` push was permitted and was run. It reached
`d(24) > 10.3`, which is **below Oler's `10.8924`** and therefore contributes nothing to
the board; `README.md` §5 quantifies why, in closed form and without appeal to solver
engineering. That negative is the main deliverable at `n = 24`.
