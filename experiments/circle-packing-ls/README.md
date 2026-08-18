# circle-packing-ls — Lubachevsky–Stillinger billiard, as a front end

**Status: `numerical`.** Everything in this directory is a floating-point *construction
hypothesis*, or a rational certificate derived from one. Nothing here is an optimality
claim, nothing here is assumable, and nothing here belongs in `results/`. See
[`../../problems/circle-packing-equilateral-triangle/RULES.md`](../../problems/circle-packing-equilateral-triangle/RULES.md)
§0–§1.

Issue: [#12](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/12).
Follow-up from [#9](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/9)
(`../circle-packing-search`, the multi-start NLP this is measured against).

**A configuration found here is a candidate. It becomes an upper bound on $s(n)$ only
once it is verified as a valid packing** — by an exact checker, written by the other
agent, per that `RULES.md` §3. This directory does not do that and cannot.

---

## What this is

Lubachevsky–Stillinger is event-driven molecular dynamics: particles fly ballistically,
collide elastically, and a shared exclusion diameter inflates with time, compacting the
configuration toward a jammed packing. The problem's `RULES.md` §5 names it as the
standard generator here, and it is the method Graham & Lubachevsky used (EJC 2 (1995)
#A1, §1).

It is used here as a **generator only**. LS terminates at its own collision tolerance,
not at machine precision, so its output is fed to the SLSQP polish that already exists
in `../circle-packing-search` for the final digits. LS finds the basin; SLSQP descends it.

### Formulation

Point formulation, on the *unit* equilateral triangle $T$ with vertices $(0,0)$,
$(1,0)$, $(\tfrac12,\tfrac{\sqrt3}{2})$: place $n$ points in $T$ maximising the minimum
pairwise distance $m$. Rescaling by $2/m$ gives $n$ points at pairwise distance $\ge 2$
in a triangle of side $D = 2/m$, hence

$$s(n) \;\le\; \frac{2}{m} + 2\sqrt{3}.$$

The particles are **points**, so the walls are the actual edges of $T$ with no radius
inset — a point may sit exactly on an edge, and in every known optimum several do.
Insetting the walls by $D/2$, which is what LS-for-disks-in-a-container does, silently
solves a different problem. That is the first place this can go wrong.

### The algorithm, in the order it is worth reviewing

1. **Wall reflection.** Each edge is stored as an outward *unit* normal $n_k$ and offset
   $c_k$ with interior $n_k\cdot x \le c_k$, so the slack $c_k - n_k\cdot x$ is a true
   Euclidean distance. Crossing time is $(c_k - n_k\cdot x)/(n_k\cdot v)$ when
   $n_k\cdot v > 0$; reflection is $v \mapsto v - 2(n_k\cdot v)n_k$.
   The three edges meet at 60°, so a particle can be on two of them at once. After each
   reflection the particle is re-reflected off any edge it is *on* and still moving into,
   and projected back onto the edge line if it drifted outside.
2. **Pair collision prediction.** With $\Delta x$, $\Delta v$ the relative position and
   velocity, exclusion diameter $D$ and growth rate $\gamma$, contact solves
   $|\Delta x + \Delta v\tau| = D + \gamma\tau$, i.e.
   $A\tau^2 + 2B\tau + C = 0$ with $A = |\Delta v|^2 - \gamma^2$,
   $B = \Delta x\cdot\Delta v - D\gamma$, $C = |\Delta x|^2 - D^2$. Smallest positive
   root, via a cancellation-avoiding solver ($B^2 \gg AC$ is the normal case).
3. **Contact handling.** $C \le 0$ (in contact) is special-cased on the sign of $B$,
   which is the sign of $\frac{d}{dt}(|\Delta x|^2 - D^2)$: still closing ⇒ collide now;
   already separating ⇒ *no event*. **This is the bug that will bite anyone reimplementing
   this**, so it is called out in the code too. Leaving the quadratic to handle it gives a
   root that is negative in exact arithmetic but which round-off flips to $\sim 10^{-17}$
   when $C = -10^{-17}$; the pair then re-collides every event, simulated time stops
   advancing, and the run reports a confident "jammed" at a *third* of the density it
   should reach. It looks like a physics result. During development this directory
   produced $m = 0.112$ for $n = 10$ against the true $1/3$, with no error and no warning.
4. **Collision resolution.** With $u$ the unit separation and $g = \Delta v\cdot u$, the
   gap $|\Delta x| - D$ closes at $g - \gamma$; elastic reflection off the growing
   exclusion surface gives $g' = 2\gamma - g$, so $v_i \mathrel{+}= (\gamma - g)u$ and
   $v_j \mathrel{-}= (\gamma - g)u$. Momentum is conserved; energy is *injected*, which is
   correct — the growing surface does work.
5. **Thermostat.** Velocities are rescaled to unit RMS speed every 200 events, so the
   only parameter that matters, the dimensionless compression rate $\gamma/v_{\text{rms}}$,
   stays put. Without it the injected energy makes the effective rate drift to zero and
   the run looks like it is still annealing when it has frozen.
6. **Termination.** Not a fixed event count: as the packing jams the collision rate
   diverges, so simulated time — and therefore $D$ — stops advancing while events keep
   being processed. A stage stops when $D$ gains less than $10^{-9}$ relative over 500
   events.

**No event queue.** Textbook LS keeps a priority queue with invalidation bookkeeping,
because it targets $n$ in the thousands. Here $n \le 40$, so `ls.py` rescans all
$\binom n2$ pairs and $3n$ wall candidates after every event: ~700 vectorised NumPy
operations, and it removes the largest single source of LS bugs (a stale event surviving
a collision). It is still exactly event-driven — no time stepping, no discretisation
error in the trajectories. This is a deliberate correctness-over-throughput trade.

### This is a float program, and that is fine

The dynamics is double precision throughout and makes no attempt at rigour. That is the
right design *because* its output is `numerical` and gets certified downstream by a
separate exact checker written by the other agent. What this directory owes the pipeline
is not rigour but a format the checker can consume, which is what `certificate.py` does.

---

## Parameters

| Parameter | Default | Meaning |
|---|---|---|
| `DEFAULT_SCHEDULE` | `(5e-2, 5e-3)` | compression rates $\gamma$, run in order, each to jamming |
| `DEFAULT_STALL_WINDOW` | `500` | events between stall checks; a stage costs at least two windows |
| `stall_rel` | `1e-9` | relative gain in $D$ below which a stage is called jammed |
| `thermostat_every` | `200` | events between velocity rescalings |
| `max_events_per_stage` | `60000` | hard cap, a safety net rather than a termination rule |
| `--budget` | `8.0` s | wall clock per $n$ per arm; matches `../circle-packing-search`'s default |
| `--seed` | `20260818` | $n$'s stream is seeded `seed + n` |

The schedule was chosen by measurement, not by physics. Longer schedules give a slightly
better packing *per run* but fewer runs per second, and at fixed wall clock the extra
basin coverage wins:

| $n$ | 4 stages (3e-2…3e-5) | 3 stages (5e-2…5e-4) | 2 stages (5e-2, 5e-3) |
|---:|---|---|---|
| 22 | 99.161 % (3 runs) | 100.000 % (7) | **100.000 % (7)** |
| 26 | 100.000 % (5) | 100.000 % (4) | **100.000 % (4)** |
| 29 | 99.947 % (3) | 99.312 % (1) | **99.947 % (5)** |
| 34 | 99.998 % (2) | 99.995 % (2) | **99.991 % (4)** |

(% of the published $m$, best over an 8 s budget, seed 9000 + $n$.)

---

## Validation on known $n$ — the gate

`RULES.md` §6 requires reproducing a known answer before any long run, so `validate` is a
gate: it refuses to declare success unless every $n$ in it matches the published value to
at least 8 significant digits **and none exceeds it**. Exceeding a published optimum is
the signature of an infeasible configuration, not of a discovery, so it is a hard failure.

$n = 3, 6, 10$ are the triangular numbers the repo already holds exact certificates for
(`../circle-packing-checker/certificates/`); $n = 5, 8, 12$ add cases with irrational
optima, and $15, 21$ add larger lattices.

```
    n                m (LS)         m (published)   digits  source
    3     1.000000000000000     1.000000000000000     16.0  Friedman (exact closed form)
    5     0.500000000000000     0.500000000000000     15.7  Friedman (exact closed form)
    6     0.500000000000000     0.500000000000000     15.5  Friedman (exact closed form)
    8     0.343070330817253     0.343070330817254     15.3  Friedman (exact closed form)
   10     0.333333333333333     0.333333333333333     15.2  Friedman (exact closed form)
   12     0.267949192431122     0.267949192431123     15.1  Friedman (exact closed form)
   15     0.250000000000000     0.250000000000000     14.8  Friedman (exact closed form)
   21     0.200000000000000     0.200000000000000     14.7  Graham-Lubachevsky 1995 (15 s.f.)
```

GATE PASSED — 14.7 to 16 significant digits, nothing exceeded.

Worth recording: on these the **raw** LS output, before any polish, already reaches the
exact optimum to 9 digits. The polish is buying the last six, not the packing.

Beyond the gate, `test_ls.py` tests the walls *in isolation* before growth is coupled to
them, which is the order the issue asks for. The sharpest of those is
`test_wall_only_billiard_is_time_reversible`: run a wall-only billiard forward for a fixed
simulated time, flip the velocity, run the same time back, and require it to return to
where it started. A wrong normal, a wrong offset or a mishandled corner all break that
immediately, and unlike a containment test it pins the geometry of each bounce rather
than only its sign.

---

## Results — candidates, all unverified

`out/nNN.json` is the float candidate (this directory's own format, field names matching
`../circle-packing-search/out/`). `candidates/nNNN-ls.json` is the same configuration in
the certificate schema pinned in the problem's `RULES.md` §2.

| n | s(n) candidate (LS) | s(n) published | digits | published source |
|---:|---|---|---:|---|
| 3 | 5.464101615138 | 5.464101615138 | 16.0 | Friedman |
| 5 | 7.464101615138 | 7.464101615138 | 15.7 | Friedman |
| 6 | 7.464101615138 | 7.464101615138 | 15.5 | Friedman |
| 8 | 9.293810046163 | 9.293810046163 | 15.3 | Friedman |
| 10 | 9.464101615138 | 9.464101615138 | 15.2 | Friedman |
| 12 | 10.928203230276 | 10.928203230276 | 15.1 | Friedman |
| 15 | 11.464101615138 | 11.464101615138 | 14.8 | Friedman |
| 16 | 12.713628774151 | 12.713628774151 | 14.8 | Graham–Lubachevsky 1995 |
| 17 | 12.928203230276 | 12.928203230276 | 15.0 | Graham–Lubachevsky 1995 |
| 18 | 13.293790434223 | 13.293790434223 | 14.5 | Graham–Lubachevsky 1995 |
| 19 | 13.454066980113 | 13.448054458479 | 3.2 | Graham–Lubachevsky 1995 |
| 20 | 13.464101615138 | 13.464101615138 | 14.8 | Graham–Lubachevsky 1995 |
| 21 | 13.464101615138 | 13.464101615138 | 14.7 | Graham–Lubachevsky 1995 |
| 22 | 14.612565741279 | 14.612565741279 | 14.7 | Graham–Lubachevsky 1995 |
| 23 | 14.928203230276 | 14.882669779630 | 2.4 | Graham–Lubachevsky 1995 |
| 24 | 14.928203230276 | 14.928203230275 | 14.3 | Graham–Lubachevsky 1995 |
| 25 | 15.293810046163 | 15.293810046163 | 14.3 | Graham–Lubachevsky 1995 |
| 26 | 15.458939080614 | 15.458939080614 | 14.5 | Graham–Lubachevsky 1995 |
| 27 | 15.464101615138 | 15.464101615138 | 14.3 | Graham–Lubachevsky 1995 |
| 28 | 15.464101615138 | 15.464101615138 | 14.3 | Graham–Lubachevsky 1995 |
| 29 | 16.612565741279 | 16.605602842691 | 3.3 | Graham–Lubachevsky 1995 |
| 30 | 16.928203230276 | 16.730087938849 | 1.8 | Graham–Lubachevsky 1995 |
| 31 | 16.928203230276 | 16.928203230275 | 14.2 | Graham–Lubachevsky 1995 |
| 32 | 17.247493078197 | 17.247493078197 | 14.2 | Graham–Lubachevsky 1995 |
| 33 | 17.419862218177 | 17.406493622838 | 3.0 | Graham–Lubachevsky 1995 |
| 34 | 17.463615158459 | 17.462876340442 | 4.3 | Graham–Lubachevsky 1995 |

**Nothing beat a published record anywhere, and every deviation is in the safe direction**
(a *larger* $s$, i.e. a worse packing). 20 of 26 match the published value to 14–16
significant digits; the six that do not — $n = 19, 23, 29, 30, 33, 34$ — are basin
misses at an 8 s budget, not infeasibilities. `../circle-packing-search/out/` has better
values for several of those, and its $n = 30$ (0.150762 vs 0.148543 here) is the largest
gap; the two directories are complementary, not redundant.

Published values are as recorded in `../circle-packing-search/reference.py`: Friedman's
Packing Center closed forms for $n \le 15$, Graham–Lubachevsky 1995's $d(n)$ for
$16 \le n \le 36$. Nothing here re-derives them, and per the problem's §4 no record claim
is made — this reproduces, it does not improve.

---

## The equal-compute comparison — issue #12's kill-criterion

Issue #12 sets the kill-criterion: *if, at equal wall clock on $n = 22\ldots34$, LS-seeded
search does not match or beat the plain multi-start baseline on at least half the $n$
tested, the port is not paying for its complexity.*

Both arms get 8 s per $n$, use the **same** `local_solve` (imported from
`../circle-packing-search/search.py`, not copied) and the **same** final polish, applied
outside the timed budget to both. The arms differ only in where start points come from.
The baseline arm is `search.search(...)` unmodified — the #9 pipeline, multi-start plus
basin hopping — re-run here rather than read off its stored `out/`, because those files
were produced on a different machine and "equal compute" then means nothing.

```
    n        m (LS-seeded)      m (multi-start)      winner                  ref   LS runs  base runs
   22    0.179396908611866    0.179132453213559          LS    0.179396908611866         6         44
   23    0.174457630187009    0.175153309170525  multi-start    0.175153309170525         3         56
   24    0.174457630187009    0.174457630187009         tie    0.174457630187010         6         51
   25    0.169065874417890    0.167283376307446          LS    0.169065874417891         5         47
   26    0.166738399395270    0.166705910916225          LS    0.166738399395271         3         62
   27    0.166666666666666    0.166666666666666         tie    0.166666666666667         3         51
   28    0.166666666666666    0.166666666666666         tie    0.166666666666667         3         35
   29    0.152109020552727    0.151902272411046          LS    0.152189614060732         5         25
   30    0.148543145110505    0.150761500215427  multi-start    0.150761500215428         2         23
   31    0.148543145110505    0.147258912852996          LS    0.148543145110506         4         15
   32    0.145102169183848    0.145102169183848         tie    0.145102169183849         4         19
   33    0.143309996272392    0.142908385607191          LS    0.143447408371201         4         33
   34    0.142862106873283    0.142857142857143          LS    0.142869646754496         4         30
```

**LS matched or beat multi-start on 11 of 13** (7 wins, 4 ties, 2 losses). The
kill-criterion is **not met**; on this evidence the port is worth keeping.

Read the two right-hand columns before reading anything else into that: LS gets 2–6 starts
in 8 s where multi-start gets 15–62, so it wins with an order of magnitude fewer basins
tried. That is the claim the issue actually wanted tested — LS is a better *basin finder*
per start — and it is the reason to expect it to scale where the NLP does not.

### What this comparison does not show

- **One seed.** 13 values of $n$, one seed each. Several margins are small, and the two
  losses ($n = 23, 30$) are cases where LS found a worse basin than the published one and
  then had too few starts left to escape it. This is evidence, not a measurement.
- **It is wall-clock bounded**, so it is machine-dependent in exactly the way
  `../circle-packing-search/README.md` flags for itself. Run on slower hardware both arms
  do less; the ratio is the part that should survive, and that has not been tested on a
  second machine.
- **It says nothing about $n > 34$**, which is the regime the port was actually motivated
  by. The trend in the run counts is suggestive and no more.

---

## Certificates for the exact checker

`candidates/nNNN-ls.json` are in the schema pinned in the problem's `RULES.md` §2, so the
exact checker can consume them directly. Since that spec bans bare floats — for the reason
its §0 gives — `certificate.py` snaps each configuration to exact rationals (denominator
$10^{15}$) and **inflates the reported side length until the rational configuration is
exactly feasible**, by about $10^{-11}$.

That trade is deliberate: the certificate is a genuine, exactly feasible upper bound that
is *weaker* than the float optimum it came from. It will therefore always be reported as
"not tight", and it can never be a record claim (`RULES.md` §4 requires tightness for
that). An honest loose certificate is worth more than a tight one nobody can check.

Containment avoids $\sqrt3$ entirely: with $x, y$ rational and $y \ge 0$,
$\sqrt3\,x \ge y \iff x \ge 0 \wedge 3x^2 \ge y^2$, and likewise at the third edge. Those
are exact integer comparisons. The squaring step is valid only because the sign of the
left factor is checked first.

`certificate.exact_feasible` re-derives feasibility from scratch in exact arithmetic and
has no tolerance parameter. **It confers no status.** Under the problem's `RULES.md` §3 a
certificate earns `verified:review` only from the *other* agent's independently written
checker; this is our own code checking our own output, and it exists to stop this
directory ever emitting something infeasible, not to bless what it emits.

### Compatibility check against the checker in PR #16

All 26 certificates were run through `experiments/circle-packing-checker` as it stands on
branch `claude/2-exact-checker` (PR #16, **not merged**), from a read-only copy outside
the repo. All 26 returned `ACCEPT (exact)`, each with the expected
`WARNING: side_length is not tight`.

**That is a format-compatibility result and nothing more.** PR #16 is also `claude`'s
work, so this is one agent's code checking the same agent's output — precisely the
same-family self-check that the problem's §3 exists to rule out. It does not verify
anything, and these certificates remain `numerical`.

---

## Reproducing

One command per mode, from this directory:

```bash
uv run pytest -q                                # 33 tests, ~45 s
uv run run.py validate                          # the gate: known n, ~65 s
uv run run.py sweep    --min 16 --max 34        # candidates, ~8 s per n
uv run run.py compare  --min 22 --max 34        # the kill-criterion, ~16 s per n
uv run run.py table                             # re-render out/
```

Pinned in `pyproject.toml` / `uv.lock`: Python 3.13, numpy 2.3.4, scipy 1.16.3 — the same
versions as `../circle-packing-search`, deliberately, so the comparison is not confounded
by a different SLSQP. Default seed `20260818`; $n$'s stream is `seed + n`. Recorded run
environment is in every `out/*.json` under `meta`, including the git commit.

**Runtime estimate, as launched:** validate ≈ 8 s × 8 = 65 s; sweep 16–34 ≈ 8 s × 19 =
150 s plus polish; compare 22–34 ≈ 2 × 8 s × 13 = 210 s plus polish. Total for everything
in this README, including the schedule-tuning table and the test suite, was **under 30
minutes of wall clock**, against the one-hour budget in `RULES.md` §6. Nothing was run
unattended for longer than four minutes at a stretch, and no background jobs were left
running.

**Reproducibility caveat, stated plainly** (same one as `../circle-packing-search`): the
search is seeded and otherwise deterministic, but it is *wall-clock bounded*. On a slower
or busier machine a run completes fewer LS starts and may return a worse configuration.
These results are reproducible in the sense of "at least this good, from this seed, given
at least this much time" — the direction that matters for an upper bound. The files in
`out/` and `candidates/` are the actual artefacts.

Checkpointing: `out/nNN.json` is written on every improvement and is **monotone** — a
later mode that draws a worse basin will not erase a better candidate. A killed run leaves
its best configuration on disk.

---

## Files

| File | What it is |
|---|---|
| `ls.py` | the billiard: geometry, event prediction, collision resolution, annealing |
| `certificate.py` | float candidate → exactly feasible rational certificate, and the exact check |
| `polish.py` | thin adapter onto `../circle-packing-search/search.py` (imported, never written) |
| `run.py` | CLI: `validate`, `sweep`, `compare`, `table`; checkpointing and metadata |
| `test_ls.py` | 33 tests; walls in isolation first, then collisions, then coupled runs |
| `out/` | float candidates, one per $n$, plus `compare.json` |
| `candidates/` | the same configurations as `RULES.md` §2 certificates |

## Limits

- **Not a proof of anything.** Not even of the upper bounds: those need the other agent's
  checker (`RULES.md` §3), and optimality needs an argument no optimiser can supply.
- **$n \le 40$ by construction.** The no-queue rescan is $O(n^2)$ per event. Past roughly
  $n = 50$ this needs the priority queue and cell lists that were deliberately skipped, and
  that is exactly the regime the port was motivated by — so the scaling argument for LS
  remains *untested* here.
- **Basin coverage is still the binding constraint**, just less so than for the NLP. Six of
  26 $n$ land in a worse basin at 8 s.
- **The comparison is one seed per $n$ on one machine.** See the caveats above; treat it
  as evidence that LS is competitive, not as a measurement of by how much.
- **No symmetry is imposed** at any stage (`RULES.md` §5), and rattlers are left alone.
