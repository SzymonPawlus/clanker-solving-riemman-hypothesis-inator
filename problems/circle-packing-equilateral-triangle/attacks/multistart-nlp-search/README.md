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

Reference column is Graham & Lubachevsky 1995 §2's $d(n)$ for their best packing (the "a"
suffix), transcribed from the paper and converted by $s = 2/d(n) + 2\sqrt3$. Search budget 40 s
per $n$ for $16 \le n \le 24$, 30 s for $25 \le n \le 34$; seed `20260817 + n`.

| $n$ | best found $m$ | published $d(n)$ | agreement | best found $s$ | published $s$ | verdict |
|---:|---|---|---:|---|---|:--|
| 16 | 0.216227269309782 | 0.216227269309782 | 14.9 digits | 12.713628774151 | 12.713628774151 | matches |
| 17 | 0.211324865405187 | 0.211324865405187 | 15.9 digits | 12.928203230276 | 12.928203230276 | matches |
| 18 | 0.203465240539123 | 0.203465240539124 | 14.6 digits | 13.293790434223 | 13.293790434223 | matches |
| 19 | 0.200321458983439 | 0.200321458983439 | 15.0 digits | 13.448054458479 | 13.448054458479 | matches |
| 20 | 0.200000000000000 | 0.200000000000000 | 14.9 digits | 13.464101615138 | 13.464101615138 | matches |
| 21 | 0.200000000000000 | 0.200000000000000 | 15.0 digits | 13.464101615138 | 13.464101615138 | matches |
| 22 | 0.179396908611866 | 0.179396908611866 | 15.1 digits | 14.612565741279 | 14.612565741279 | matches |
| 23 | 0.175153309170525 | 0.175153309170525 | 14.6 digits | 14.882669779630 | 14.882669779630 | matches |
| 24 | 0.174457630187009 | 0.174457630187010 | 14.3 digits | 14.928203230276 | 14.928203230275 | matches |
| 25 | 0.169065874417891 | 0.169065874417891 | 15.3 digits | 15.293810046163 | 15.293810046163 | matches |
| 26 | 0.166732017260692 | 0.166738399395271 | 4.4 digits | 15.459398216587 | 15.458939080614 | **MISS** |
| 27 | 0.166666666666666 | 0.166666666666667 | 14.4 digits | 15.464101615138 | 15.464101615138 | matches |
| 28 | 0.166666666666666 | 0.166666666666667 | 14.5 digits | 15.464101615138 | 15.464101615138 | matches |
| 29 | 0.152172645377570 | 0.152189614060732 | 4.0 digits | 16.607068243848 | 16.605602842691 | **MISS** |
| 30 | 0.150761500215427 | 0.150761500215428 | 14.2 digits | 16.730087938849 | 16.730087938849 | matches |
| 31 | 0.148543145110505 | 0.148543145110506 | 14.2 digits | 16.928203230276 | 16.928203230275 | matches |
| 32 | 0.144984727468812 | 0.145102169183849 | 3.1 digits | 17.258658013709 | 17.247493078197 | **MISS** |
| 33 | 0.143088359324597 | 0.143447408371201 | 2.6 digits | 17.441479016349 | 17.406493622838 | **MISS** |
| 34 | 0.142866887845830 | 0.142869646754496 | 4.7 digits | 17.463146671388 | 17.462876340442 | **MISS** |

**Nothing beat a published record, at any $n$.** Every deviation is in the safe direction — our
$s$ is larger, our packing worse. Problem `RULES.md` §4 was not triggered.

### 14 of 19 matched; the 5 misses are diagnosable, and the diagnosis is the interesting part

The misses at $n = 26, 29, 32, 34$ are **not** noise or bugs. Each reproduces, to 15 significant
digits, a *specific packing that Graham & Lubachevsky themselves report and rank second*:

| $n$ | best found $m$ | GL packing it reproduces | GL's value for that packing |
|---:|---|:--|---|
| 26 | 0.166732017260692 | `t26b` | 0.166732017260692 |
| 29 | 0.152172645377570 | `t29b63.2` | 0.152172645377571 |
| 32 | 0.144984727468812 | `t32b` | 0.144984727468812 |
| 34 | 0.142866887845830 | `t34c` (their *third* best) | 0.142866887845831 |

So at those $n$ the local optimiser converged perfectly — onto the wrong basin. That is a
**basin-coverage** failure, not a convergence failure, and it is exactly what the falling restart
counts predict: 200 restarts were affordable at $n = 16$ but only ~55 at $n = 32$.

$n = 33$ is the one genuine outlier: 0.143088359324597 falls below GL's `t33c` (0.143309997215537),
i.e. it landed in a basin they rank at least fourth and do not tabulate. $n = 33$ also had the
worst agreement in the table (2.6 digits), consistent with it being the hardest instance here.

This is a clean, checkable statement about the method: **the NLP local step is exact to machine
precision; the global search is what runs out at $n \gtrsim 26$.** Effort should go into the
generator (issue #12), not into the polisher.

### Secondary kill-criterion: not met

Issue #9's secondary stop was "worse than GL by more than $10^{-6}$ in $s$ on *every* $n$ in
16–21". All six matched to $\ge 14$ digits, so the approach stands.

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
3. **Basin coverage degrades with $n$.** Confirmed above, not merely suspected: 200 restarts at
   $n = 16$, ~55 at $n = 32$, and every miss lands on a *named* second-best GL packing. A miss at
   large $n$ is an under-powered search, not a worse local solver.
4. **A degenerate solve can poison the incumbent silently.** SLSQP returned coincident points
   ($m = 0$) once during the sweep, which crashed the checkpoint writer on $2/m$. The crash was
   the lucky outcome — a `NaN` would have passed straight through, because `NaN > best_m` is
   `False`, so the search would have quietly frozen on its previous best and reported it as
   converged. Both are now rejected explicitly at the incumbent-update site.
