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
