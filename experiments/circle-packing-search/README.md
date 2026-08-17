# circle-packing-search

**Status: `numerical`.** Everything this directory produces is a floating-point *construction
hypothesis*. It is not a certificate, and it is never an optimality claim. See
[`../../problems/circle-packing-equilateral-triangle/RULES.md`](../../problems/circle-packing-equilateral-triangle/RULES.md)
§1.

Issue: [#9](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/9).
Writeup: [`../../problems/circle-packing-equilateral-triangle/attacks/multistart-nlp-search/`](../../problems/circle-packing-equilateral-triangle/attacks/multistart-nlp-search/).

## Question

Given $n$, find a packing of $n$ unit circles in an equilateral triangle of side as small as
possible — i.e. produce good *upper* bounds on $s(n)$, as explicit coordinates.

This is the **search** half of the problem. The **checking** half — exact/interval feasibility
verification of a candidate — is deliberately not here; it is issue #2's
`experiments/circle-packing-checker/`. Keeping the generator and the verifier in separate
codebases written by separate agents is the point (problem `RULES.md` §3).

## Method

Point formulation. Fix the unit equilateral triangle $T$ with vertices $(0,0)$, $(1,0)$,
$(\tfrac12,\tfrac{\sqrt3}{2})$ and place $n$ points in $T$ maximising the minimum pairwise
distance $m$. Rescaling by $2/m$ gives $n$ points at pairwise distance $\ge 2$ in a triangle of
side $D = 2/m$, hence

$$s(n) \;=\; \frac{2}{m} + 2\sqrt{3}.$$

Maximising $m$ minimises $s$. The local step is the nonconvex NLP

$$\max_{p_1,\dots,p_n,\,m} m \quad\text{s.t.}\quad \lVert p_i - p_j\rVert^2 \ge m^2,\qquad p_i \in T,$$

solved by SLSQP over $2n+1$ variables with analytic constraint Jacobians ($\binom n2 + 3n$
inequality rows; 561 + 102 at $n = 34$). On top of that:

1. **Multi-start** — uniform-random starts mixed with jittered subsets of a triangular lattice.
2. **Basin hopping** on the incumbent — teleport a random subset, re-roll the *rattlers*
   (points whose nearest neighbour is strictly further than $m$), or Gaussian-shake everything.
3. **Polish** — warm-restart SLSQP from its own output a few times. This is what buys the last
   several digits; a single solve lands around $10^{-9}$, the polished value around $10^{-15}$.

No symmetry is imposed at any stage (problem `RULES.md` §5). Rattlers are re-rolled as a *search
move* only; they are never removed or pinned in the reported configuration.

### Why not Lubachevsky–Stillinger directly

The problem `RULES.md` names LS billiard simulation as the standard generator, and Graham &
Lubachevsky (EJC 2 (1995) #A1, §1) describe it: simulate $n$ perfectly elastic disks, grow them
uniformly, resolve collisions as discrete events, stop when growth stalls. It is an excellent
basin *finder*, but it terminates at its collision tolerance, not at machine precision — GL's own
15-digit values come from post-processing the contact structure, not from the simulation. Since a
polish stage is needed either way, and since at $n \le 34$ the NLP is milliseconds per solve, we
use the NLP as both generator and polisher. Porting LS properly is filed as follow-up work; the
honest expectation is that it matters at $n \gtrsim 50$, not here.

### Reported $m$ is measured, not asserted

`local_solve` throws away the solver's own value of $m$ and re-measures
$\min_{i<j}\lVert p_i - p_j \rVert$ on the (barycentrically clipped, hence exactly contained)
output points. SLSQP is allowed to sit a hair outside the feasible set; trusting its $m$ is
precisely how a fake record gets born. The measured value errs on the conservative side.

Even so: these are floats. A `feasibility_floats` block in every checkpoint records the measured
minimum pairwise distance and the containment slack, but a float check is not a check. Anything
promoted to `results/` must first pass an exact-arithmetic verifier.

## Reproducing

```
uv run run.py validate                       # the gate: n = 3..15 against exact closed forms
uv run run.py sweep --min 16 --max 34        # candidates for the open range
```

Versions are pinned in `pyproject.toml` (numpy 2.3.4, scipy 1.16.3, Python 3.13); the default
seed is `20260817`, and $n$'s stream is seeded `seed + n`.

**Reproducibility caveat, stated plainly:** the search is seeded and otherwise deterministic, but
it is *wall-clock bounded* (`--budget` seconds per $n$). On a slower or busier machine a run
completes fewer restarts and may return a worse configuration. Results are therefore reproducible
in the sense that "at least this good, from this seed, given at least this much time" — which is
the direction that matters for an upper bound. The checkpoints in `out/` are the actual artefacts.

Output: `out/n<NN>.json` per $n$, rewritten on every improvement so a killed run still leaves its
best configuration behind. Coordinates are in the unit triangle; multiply by $2/m$ for the
repo's point formulation.

## Reference data

`reference.py` holds the published values this is measured against, and nothing computed by us:

- $n \le 15$: exact closed forms from Erich Friedman's Packing Center. Used as the validation
  target because a closed form is infinitely precise where GL's decimals stop at 15 digits.
- $16 \le n \le 36$: $d(n)$ as printed in Graham–Lubachevsky 1995, converted by
  $s = 2/d(n) + 2\sqrt3$. GL define $d(n)$ as the disk *diameter* in units of the side of the
  smallest equilateral triangle containing all disk *centres* (their §2) — which is exactly this
  code's $m$. The conversion was checked against the $n$ where both sources exist
  ($n = 4, 7, 8, 11, 12, 13$) and agrees to all printed digits.
- $n \in \{20, 21, 27, 28, 35, 36\}$ are $T(k)$ and $T(k)-1$; GL report (§2) that their runs
  reproduced the known triangular-lattice packings there, for which $d = 1/(k-1)$ exactly.

`reference.py` does **not** take a position on the proven-vs-best-known discrepancy flagged in
the problem README — that is issue #1's job. These are numerical targets only.

## Result

`validate` reproduces every published $s(n)$ for $3 \le n \le 15$ to **15–16 significant
digits** — the closed-form value to within double-precision round-off. The sweep results and
their comparison against Graham–Lubachevsky are written up in the attack directory.
