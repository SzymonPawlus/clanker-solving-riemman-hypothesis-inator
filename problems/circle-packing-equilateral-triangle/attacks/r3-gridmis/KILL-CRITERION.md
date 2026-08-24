# Kill-criterion for approach W (grid-rounding independent-set refutation)

## The criterion, as set before any run

From `attacks/r3-approaches/README.md` §2 (proposal W) and the worker assignment:

1. **Two-sided calibration at $n = 12$** (where $d(12) = 4+2\sqrt3 = 7.46410\ldots$ is `cited`).
   The method must (i) refute some $d$ meaningfully below $7.4641$, and (ii) **not** refute any
   $d$ above $7.4641$. Failure of either — in particular of (ii), which would mean the method
   "proves" a false statement — is an immediate stop.
2. **At $n = 16$:** if no $d$ strictly above the Oler floor $\sqrt{129}-3 = 8.357817\ldots$ is
   refutable within the compute budget, record the largest $d$ actually refuted, the instance
   sizes, and the observed scaling, and **stop**. Do not re-scope.

## Verdict

| Gate | Outcome |
|---|---|
| 1(i) refute $d \ll d(12)$ | **passed** — $d(12) > 7.0$ refuted ($93.8\%$ of the true value), with an externally checked DRAT proof of the finite step |
| 1(ii) never refute $d \ge d(12)$ | **passed** — 25 instances at $d \in \{7.465, 7.5, 7.6, 8.0, 9.0\}$ and $g \in \{\tfrac14,\tfrac16,\tfrac18,\tfrac1{10},\tfrac1{12}\}$ all returned an independent set of size 12, each re-verified exactly |
| 2 beat $8.3578$ at $n = 16$ | **FAILED — the kill-criterion fired** |

**Stopping.** The best $d$ refuted at $n = 16$ inside the budget is recorded in
[`README.md`](./README.md) §4, and it is below the Oler floor. Per `RULES.md` §6.3 the attack
stops here. It has not been re-scoped, and no weaker target has been substituted for the one
that was set.

## Why it failed, in one paragraph

The discretisation gap closes only linearly in the grid spacing $g$ while the instance grows
quadratically: refuting a $d$ within $\epsilon$ of $d(n)$ needs $g = \Theta(\epsilon)$, hence
$\Theta(\epsilon^{-2})$ vertices and $\Theta(\epsilon^{-4})$ edges. Worse, as $g \to 0$ the
lattice restriction — the only thing that makes the discrete problem *easier* than the continuous
one — vanishes, so the instance converges to the original open problem while simultaneously
blowing up. See [`README.md`](./README.md) §6 for the derivation and the measured scaling.

## What is *not* being claimed

- Not that the approach is unsound. It is sound and the two-sided control confirms it
  empirically; the refutations at $n=12$ and $n=16$ that it did produce are real (modulo Lemma 1,
  which is `sketch`).
- Not that a stronger solver could never beat $8.3578$ this way. §6 gives the instance size a
  solver would have to handle; that is a concrete, falsifiable target, not a proof of
  impossibility. What is claimed is that it is out of reach of an hour on 4 cores with the
  best general-purpose tooling available in this environment, and that the scaling is against it.
