# Attack: multi-start NLP search (max-min-distance formulation)

**Claim type: construction (upper bounds on $s(n)$) only.** No statement in this file is an
optimality claim, and nothing here is a certificate. Status of every number below: `numerical`.

- Issue: [#9](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/9)
- Code: [`experiments/circle-packing-search/`](../../../../experiments/circle-packing-search/)
- Author: `claude` (Claude Opus 5), 2026-08-17

## The idea

Search, not proof. Produce candidate packings cheaply and at high precision, so that the
certification machinery (issue #2's exact checker, issues #3/#4) has something to certify.

In the point formulation of [`../../README.md`](../../README.md), place $n$ points in a **unit**
equilateral triangle maximising the minimum pairwise distance $m$. Then

$$s(n) \;=\; \frac{2}{m} + 2\sqrt{3},$$

so maximising $m$ minimises $s$. Locally this is a smooth nonconvex NLP in $2n+1$ variables with
$\binom n2 + 3n$ inequality constraints, solved by SLSQP with analytic Jacobians. Globally it is
attacked by multi-start plus basin hopping. Full method description and the reproduction command
are in the experiment README; this file records what happened.

## Kill-criterion

> If the optimiser cannot recover the published $s(n)$ for $n = 3, 6, 10, 12$ to at least 8
> significant digits within the compute budget, the approach is abandoned as implemented.

**Not met.** See below.

## Status: validation gate PASSED

Mandatory before anything else (repo `RULES.md` §6: *validate on a tiny instance first*). The
optimiser was run against every $n \le 15$ with a published exact closed form, taken from
Friedman's Packing Center — not from any computation of ours. Search budget 6 s per $n$, seed
`20260817 + n`, total wall clock 78 s.

| $n$ | published $s(n)$ | best found $s$ | agreement |
|---:|---|---|---:|
| 3 | $2+2\sqrt3$ | 5.464101615138 | 16.0 digits |
| 4 | $4\sqrt3$ | 6.928203230276 | 15.7 digits |
| 5 | $4+2\sqrt3$ | 7.464101615138 | 16.0 digits |
| 6 | $4+2\sqrt3$ | 7.464101615138 | 16.0 digits |
| 7 | $2+4\sqrt3$ | 8.928203230276 | 15.8 digits |
| 8 | $2+2\sqrt3+\tfrac{2\sqrt{33}}{3}$ | 9.293810046163 | 15.5 digits |
| 9 | $6+2\sqrt3$ | 9.464101615138 | 15.3 digits |
| 10 | $6+2\sqrt3$ | 9.464101615138 | 15.3 digits |
| 11 | $4+2\sqrt3+\tfrac{4\sqrt6}{3}$ | 10.730087938849 | 15.4 digits |
| 12 | $4+4\sqrt3$ | 10.928203230276 | 15.2 digits |
| 13 | $4+\tfrac{2\sqrt6}{3}+\tfrac{10\sqrt3}{3}$ | 11.406495853752 | 15.0 digits |
| 14 | $8+2\sqrt3$ | 11.464101615138 | 15.1 digits |
| 15 | $8+2\sqrt3$ | 11.464101615138 | 15.1 digits |

"Agreement" is $-\log_{10}$ of the relative difference between the best found $m$ and the exact
$m$, i.e. significant decimal digits. 15–16 digits is double-precision round-off: the search
reproduces the closed forms to the limit of the arithmetic it is using.

Read this narrowly. It says the pipeline finds the right *configurations* and resolves them to
machine precision. It says nothing about optimality — for $n = 13, 14$ the published values are
themselves best-known, so agreement there means "reproduced the literature's construction", not
"confirmed a proof".

## Results for $16 \le n \le 34$

<!--SWEEP-->

## What this does and does not establish

Establishes (status `numerical`, evidence only):

- A working, seeded, version-pinned generator for candidate packings at $n \le 34$, which
  recovers every published small-$n$ value to machine precision.
- Explicit coordinates for each $n$, checkpointed in `experiments/circle-packing-search/out/`.

Does **not** establish:

- Any upper bound on $s(n)$. The coordinates are doubles; the reported minimum pairwise distance
  is a float measurement, not a proof of feasibility. Until an exact-arithmetic or interval check
  confirms a configuration, it bounds nothing (problem `RULES.md` §0).
- Any lower bound or optimality, for any $n$, however many restarts converge to the same shape.
  Repeated convergence is evidence about where to look and nothing more (problem `RULES.md` §1).

## Method notes worth keeping

- **Measure, don't trust.** The solver's own $m$ is discarded; $m$ is re-measured on the output
  points after an exact barycentric projection into the triangle. SLSQP will happily return a
  point a few $10^{-12}$ outside the feasible set with a correspondingly inflated $m$, and that
  is exactly the mechanism that manufactures a fake record.
- **The float feasibility numbers are round-off, and that is the point.** Every checkpoint
  records a `containment_slack`, and across the whole run it sits at $\pm 10^{-16}$ — sometimes
  *negative*, i.e. nominally outside the triangle by half an ulp. That is the barycentric
  round-trip's rounding, not a real violation, but there is no way to tell those two apart from
  inside double precision. It is a concrete demonstration of why problem `RULES.md` §0 refuses
  float output as a result: at this precision "feasible" and "infeasible by $10^{-16}$" are the
  same bit pattern.
- **Polish separately from search.** A single SLSQP solve lands around $10^{-9}$; warm-restarting
  it from its own output three or four times reaches $10^{-15}$. Without the polish stage the
  validation table above would read "8 digits", which is enough to pass the gate but not enough
  to distinguish a genuine tie from a near-miss at larger $n$.
- **Rattlers as a search move.** Re-rolling the points that are not tight (nearest neighbour
  strictly beyond $m$) is the single most productive basin-hopping move, because those points are
  free variables that carry no gradient signal. They are re-rolled during search only — the
  reported configurations keep their rattlers, per problem `RULES.md` §5.
- **No symmetry constraint.** Triangular-lattice starts are mixed in as a prior and always
  jittered; nothing in the formulation restricts the search to symmetric configurations.

## Failure modes to watch for if this is extended

1. **Wall-clock budgeting makes runs machine-dependent.** The search is seeded and deterministic
   given a fixed iteration count, but the driver caps on seconds. A slower machine does fewer
   restarts and can return a worse configuration. For an upper bound that is the safe direction,
   but it means "reproducible" here has a caveat, stated in the experiment README.
2. **SLSQP's constraint count grows as $n^2$.** At $n \approx 60$ this becomes the bottleneck and
   an active-set restriction (or a proper LS billiard front end) is needed.
3. **Basin coverage degrades with $n$.** The number of restarts completed inside a fixed budget
   falls off sharply — see the restart counts in the sweep table. A miss at large $n$ is far more
   likely to be an under-powered search than a genuinely worse packing.
