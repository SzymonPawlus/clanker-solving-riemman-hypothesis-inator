# Kill-criterion — r5-eo7 (proposal AE)

Stated in the assignment before any code was written, and reported against here
(`RULES.md` §6.2–6.3).

## The criterion as given

> If the certified branch-and-bound cannot close even a coarse bound (say $\le 30$) over
> the parameter space within the compute budget, record the parameter space, the regions
> covered, the best certified bound, and the observed cost scaling, and STOP.

## Did it fire?

**No — on Half 1, and by a wide margin.**

| | |
|---|---|
| coarse gate | $\le 30$ |
| EO(7) gate | $\le 26$ |
| **certified** | **$\le 25$** over the whole 3-parameter space |
| cost | **175 boxes, 0.6 s** — the run does not stall and there is no cost-scaling story to report |
| best possible from this relaxation | 24 (measured by float scan of the same bound), so the certificate carries 1 unit of interval slop |
| matching lower bound | 22, by an exact $\mathbb{Q}(\sqrt3)$ witness in $T(5999/1000)$ |

The parameter space, the regions, and the stalled-box lists are in
`experiments/packing-r5-eo7/out/`; every run checkpoints to disk while it is running.

## A second criterion fired, on Half 2

Half 2 (name a forcing hypothesis such that lattice-count + forcing $\Rightarrow$ EO(7))
had no pre-registered kill-criterion in the assignment, so I adopted the obvious one
while writing it:

> The hypothesis is only worth stating if the counting theorem that consumes it survives
> the hypothesis being satisfied *approximately* — because no packing satisfies an exact
> linear relation.

**That fired.** §7 of `README.md` measures it: the counting bound is **discontinuous at
zero perturbation**. At $\delta = 0$ its maximum is 24; at $\delta = 10^{-9}$ it is 27,
already past the 26 the conjecture needs, and at $10^{-6}$ it is 28 — the trivial value.
The cause is structural and is stated in §2.2: every unit of the gain from 28 to 22 comes
from the extremal configuration's chords being *exactly* integers.

So:

- the **conditional theorem stands** as stated (with exact collinearity);
- the **robust conditional does not exist** with this counting step, and cannot be
  obtained by tightening the certificate — improving 25 to the true 24, or even to 22,
  does not change the sign of the jump;
- **I stopped rather than re-scoping.** I did not weaken the target, did not tune the
  solver further, and did not go looking for a different $\delta$-regime in which the
  numbers happen to work.

## What a follow-up must answer first

The relaxation throws away the second basis direction entirely: it counts points on
lines parallel to $v_1$ and never uses $v_2$ except through the spacing $h$. A counting
step that uses both families is the obvious candidate for a $\delta$-robust bound, and it
has a measured target: it must beat **2 units** of loss at $\delta \to 0^+$ (28 vs the
26 required). Anything that cannot state how it beats that number should not be
dispatched.
