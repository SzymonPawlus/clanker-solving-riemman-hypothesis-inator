# Attack: trying to **refute** Erdős–Oler — the measured shape of the search space at $k = 7,8,9,10$

**Claim type: neither.** No bound on $s(n)$, upper or lower, is claimed anywhere in this file
(problem [`../../RULES.md`](../../RULES.md) §1 asks for that sentence first). What is here is a
*failed refutation*, made quantitative: a measured census of the top of the optimisation landscape
at $n = \Delta(k)-1$ for $k = 7,8,9,10$, an exact-arithmetic gate that every candidate was pushed
through, one **exact rational certificate for a positive control**, and a margin curve saying how
much room a counterexample has left to hide in — and how fast that room is closing as $k$ grows.
Nothing enters `results/`; nothing here is assumable, including by me (repo
[`RULES.md`](../../../../RULES.md) §3).

- **Outcome: no counterexample.** **30 830** local optima in the census plus **4 672** targeted
  insertions, at $k = 7,8,9,10$; not one exceeded $1/(k-1)$, and the abort-and-exactify trigger
  never fired. Rationalised, the best configuration at every $k$ is *exactly* the $T(k)$ lattice
  minus a point — margin exactly zero in $\mathbb{Q}$, not merely small (§5d). This is evidence
  that *this search* did not find a counterexample, and nothing more; §8 says where it did not look.
- **The most useful thing here is §7**, the counterexample window: any violation of EO($k$) is
  confined to $a \in [1/m(\Delta(k)-2),\, k-1)$, an interval whose width collapses geometrically
  in $k$. At $k=7$ it is $2.6\times10^{-3}$ wide out of 6. **Large $k$ is not a better place to
  look for a refutation; it is a worse one.**
- Author: `claude` (Claude Opus 5), 2026-08-21, branch `claude/circle-equklatetal-problem-sa7tx7`
- Code: [`experiments/packing-eo-hunt/`](../../../../experiments/packing-eo-hunt/) — one command
  per stage, `numpy`/`scipy` for search, Python-stdlib **exact** arithmetic for every decision
- Transcript: [`out/report.txt`](../../../../experiments/packing-eo-hunt/out/report.txt)
- Kill-criterion, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Journal: [`notebook/claude/2026-08-21-eo-hunt.md`](../../../../notebook/claude/2026-08-21-eo-hunt.md)

| What | Status |
|---|---|
| §2 the exact refutation test in $\mathbb{Q}$ | elementary; the identity is checked below and reproduces the lattice exactly |
| §3 validation on the proven cases $k \le 6$ | `numerical` — reproduction, claims nothing new |
| §4 the $n = 26$ positive control and its exact certificate | **exact** construction (of a *published* record), status `numerical` pending the §3-of-problem-`RULES` independent checker |
| §4b the negative control (gate rejects a $10^{-12}$ near-miss) | **exact** |
| §5 the census at $k = 7,8,9,10$ | `numerical` |
| §6 the insertion attack | `numerical` |
| §6b no rotated lattice beats $T(k)$ minus a point | `numerical` — a scan over $(\theta,\text{offset})$, not a proof |
| §7 the counterexample window and margin curve | `numerical`, and **conditional** on published records being optimal |
| Erdős–Oler at $k \ge 7$ | **untouched.** Still open. |

---

**Kill-criterion outcome.** [`KILL-CRITERION.md`](./KILL-CRITERION.md) was written before any
code ran. **K1 (budget) is met**: the planned solve budget was spent with no local optimum
exceeding $1/(k-1) + 10^{-12}$ at any target $k$, so the attack stops here and the deliverable is
the measured landscape. **K2 (structural) is *not* met** and I am not claiming it: §5b shows the
values below $1/(k-1)$ trail off continuously rather than leaving a clean gap, so I cannot say
there is no basin a further order of magnitude of solves would reach. Saying K2 was met would be
the more impressive report and it would be false.

The attack is therefore `refuted` **as a route** — this method, at this budget, does not decide
Erdős–Oler either way — and *not* a refutation of the conjecture, which is untouched.

---

## 1. Normalisation — fixed once, because this is where the errors live

Separation 1: $n$ points at pairwise distance $\ge 1$ in the closed equilateral triangle $T_a$ of
side $a$; $\Delta(k) = k(k+1)/2$. The optimiser works in the **unit** triangle
$T = \mathrm{conv}\{(0,0),(1,0),(\tfrac12,\tfrac{\sqrt3}{2})\}$ and maximises the minimum pairwise
distance $m$; then $a = 1/m$. So

> **EO($k$) is false $\iff$ $m(\Delta(k)-1) > \dfrac{1}{k-1}$.**

Targets $k = 7,8,9,10$ are $n = 27, 35, 44, 54$ against $1/6, 1/7, 1/8, 1/9$. This repo's
certificates use separation 2 and side $d = 2a$; the factor of 2 is the single likeliest place to
fool oneself and **every number in this file is in the separation-1 $(a,m)$ normalisation**.
Graham–Lubachevsky's tabulated $d(n)$ equals $m(n)$ in this normalisation.

## 2. The exact gate, and why it needs no $\sqrt3$

Problem `RULES.md` §0 is blunt: every optimiser returns a slightly infeasible configuration and
reports a record, and that result is always wrong. So the gate was built *first*, before any
search, and it is exact rational arithmetic with no tolerance anywhere.

Write each point by its barycentric coordinates $(\ell_0,\ell_1,\ell_2)$ with respect to the
triangle. Containment is then **literally** $\ell_i \ge 0$ — no irrational enters. For two points
with barycentric difference $u = \ell^P - \ell^Q$, so that $u_0+u_1+u_2 = 0$, the barycentric
distance formula for side lengths $a_0=a_1=a_2=a$ gives
$|P-Q|^2 = -a^2(u_0u_1+u_1u_2+u_2u_0)$, and expanding $(\sum u_i)^2 = 0$ turns that into

$$|P-Q|^2 \;=\; \frac{a^2}{2}\left(u_0^2+u_1^2+u_2^2\right).$$

Everything is rational when the $\ell_i$ and $a^2$ are. Setting
$q_{\min} = \min_{i<j}\tfrac12(u_0^2+u_1^2+u_2^2)$, the least side admitting the configuration at
separation 1 is $a = q_{\min}^{-1/2}$, and

> **the refutation test is the single exact rational comparison $q_{\min} > 1/(k-1)^2$.**

A second, independent checker works in Cartesian coordinates over $\mathbb{Q}(\sqrt3)$ — exact sign
of $p + q\sqrt3$ by squaring, containment as the three half-planes, squared distances compared
against the separation — written from the geometry rather than from the identity above, per
problem `RULES.md` §3. The two agree everywhere they were both run (§4).

**Self-test.** Fed the $T(7)$ lattice minus its apex, the gate returns $q_{\min} = 1/36$ exactly,
$a = 6$ exactly, margin exactly $0$: the known packing, recovered as an exact rational fact, and
*not* mistaken for a counterexample.

---

## 3. Validation before anything else — the proven cases, and a near-miss worth recording

`run.py validate` runs the full pipeline on the cases the literature has **settled**: $k = 2..6$,
i.e. $n = 2,5,9,14,20$ (Melissen 1993 for $k \le 4$; Payan 1997 for $k = 5$ and, on his abstract,
$k=6$ — see [`../../README.md`](../../README.md) for the qualification on that attribution).

| $k$ | $n$ | best $m$ found | target $1/(k-1)$ | exact $a_{\min}$ | digits |
|---|---|---|---|---|---|
| 2 | 2 | 1.000000000000000 | 1.000000000000000 | 1.000000000000 | 16.0 |
| 3 | 5 | 0.500000000000000 | 0.500000000000000 | 2.000000000000 | 16.3 |
| 4 | 9 | 0.333333333333333 | 0.333333333333333 | 3.000000000000 | 16.3 |
| 5 | 14 | 0.250000000000000 | 0.250000000000000 | 4.000000000000 | 15.9 |
| 6 | 20 | 0.200000000000000 | 0.200000000000000 | 5.000000000000 | 15.7 |

The exact gate returned $a_{\min} = k-1$ **exactly** in every case and never a sub-$(k-1)$ value.
An optimiser that "beats" a proven case is broken, not brilliant, and the attack would have
stopped here.

**The near-miss, recorded because it is exactly the §4 failure ordering.** Spot-checking
uniform-start success rates, I compared against reference $d(n)$ values typed **from memory** and
read "best $0.2518$ against reference $0.1694$" at $n = 13$ — apparently a 50% improvement on the
world record. The optimiser was right and my memory was wrong:
$d(13) = 0.251813236653061$, exactly what it found, per
[`experiments/circle-packing-search/reference.py`](../../../../experiments/circle-packing-search/reference.py)
(Graham–Lubachevsky 1995 / Friedman). *Misread normalisation* is second on problem `RULES.md` §4's
list of likelier explanations than a discovery, and it took about ninety seconds to occur here.
**Never hand-type a reference value.** Re-checked against the file, the pipeline reproduces
$d(13), d(17), d(19), d(27), d(28)$ to 12 or more significant digits.

---

## 4. The positive control: $n = 26$, and the only test of the gate's "yes" branch

A gate that has only ever answered "no" is not evidence of anything. It needed a case where the
correct answer is **yes**, and $n = 26$ is exactly that case — and it is also the *shape* a
counterexample to EO(7) would have: an irregular, non-lattice packing sitting strictly below side
$6$. The published record is $d(26) = 0.166738399395271 > 1/6$
(Graham–Lubachevsky 1995), i.e. $a = 5.99742\ldots < 6$.

`control_n26.py`, 2658 solves:

- **search**: best $m = 0.166738399395271$, agreeing with the published record to **14.7
  significant digits** — an independent rediscovery, from random and structured seeds, of a
  packing of 26 points below side 6;
- **exact gate, barycentric**: rationalised at denominator $10^6$,
  $q_{\min} = \frac{14625558147611836881}{526067161137417544324}$, exactly $> 1/36$, all
  $\ell_i \ge 0$, giving $a_{\min} = 5.997418733\ldots < 6$;
- **exact gate, $\mathbb{Q}(\sqrt3)$ cross-check**: at the exact rational side
  $\frac{299871}{50000} = 5.99742$, all 26 points exactly contained and all $\binom{26}{2}$
  separations exactly $\ge 1$. **Both checkers agree.**

So the pipeline demonstrably *can* find and certify a sub-$(k-1)$ packing when one exists. That is
the strongest thing that can be said for a negative result at $n = 27$, and it is the reason the
$k=7$ null is worth reporting at all.

The certificate (26 exact rational barycentric triples, exact side $299871/50000$) is in
[`out/control-n26.json`](../../../../experiments/packing-eo-hunt/out/control-n26.json). It is a
certificate for a **known** record, offered as a validated artifact; it is deliberately **not**
promoted into `results/`, which is verification-critical and needs the independent checker of
problem `RULES.md` §3 written by the other model family.

A **third** exact checker (`verify3.py`) was then written from a different observation again: in
the triangle $(0,0), (L,0), (L/2, L\sqrt3/2)$ with $L$ rational, every rational convex combination
of the vertices has the form $(x, t\sqrt3)$ with $x, t$ **rational**, so dividing $\sqrt3$ out by
hand turns all three containment tests into rational comparisons ($t \ge 0$, $x - t \ge 0$,
$L - x - t \ge 0$) and every squared distance into $(\Delta x)^2 + 3(\Delta t)^2$. It shares no
representation with either of the other two. All three agree on the $n = 26$ certificate: minimum
squared distance $\tfrac{1315168458468353297523988136721}{1315167902843543860810000000000} > 1$,
closest pair $(1, 20)$, all 26 points contained.

## 4b. The negative control — the gate must reject a near-miss

The complement of §4, and the test problem `RULES.md` §0 is really about. Take the $T(7)$ lattice
minus its apex — 27 points, side exactly 6, separation exactly 1 — and shrink the triangle by a
factor $1-\varepsilon$. Every such configuration "fits 27 points below side 6" and every one is
infeasible; at $\varepsilon = 10^{-12}$ it is infeasible by $2\times10^{-12}$ in squared distance,
which is invisible to a float check at tolerance $10^{-9}$ and to any solver reporting its own $m$.

| shrink $\varepsilon$ | side | exact min squared distance | separation $\ge 1$? | gate reports refutation? |
|---|---|---|---|---|
| 1e-3 | 5.994000000000000 | 0.998001000000000027 | False | **False** |
| 1e-5 | 5.999940000000000 | 0.999980000099999988 | False | **False** |
| 1e-7 | 5.999999400000000 | 0.999999800000009986 | False | **False** |
| 1e-9 | 5.999999994000000 | 0.999999997999999946 | False | **False** |
| 1e-12 | 5.999999999994000 | 0.999999999998000044 | False | **False** |

No false positive at any scale, and the barycentric gate independently returns
$a_{\min} = 6$ exactly ($q_{\min} = 1/36$) for those 27 points. The gate is exact, not
tolerance-based — which is the only reason a null result from it is worth reporting.
---

## 5. The census at $k = 7, 8, 9, 10$

`run.py hunt`, five seed families cycled round-robin for the first 40% of the budget; after that
each iteration hops from an eight-strong elite pool with probability 0.65 and takes a fresh seed
otherwise, so structured restarts continue for the whole run. The hop has four move types (teleport a random subset, re-roll the
rattlers, Gaussian shake, and *delete-one-and-reinsert-at-the-emptiest-site* — the last aimed
squarely at the degree of freedom Erdős–Oler is about). Every solve reports the minimum pairwise
distance **measured after projecting the points into the triangle**, never the solver's own value
for $m$; trusting the latter is how a fake record is born.

The five seed families:

| family | what it samples |
|---|---|
| `uniform` | uniform random points |
| `lattice_defect` | the $T(k)$ lattice minus $T(k)-n$ points, jittered over 2 decades of amplitude |
| `rotated_lattice` | a hexagonal lattice at random spacing/rotation/offset, cropped to the triangle — the structured competitor a random multi-start is worst at finding, and the shape several known optima (e.g. $n = 13, 26$) actually take |
| `rows` | random row structures with row counts *not* equal to the lattice's $k, k-1, \dots, 1$ |
| `corner_dense` | the three corner clusters of the lattice pinned at scale 2–4, interior scattered — seeded at the necessary conditions of [`../eo-hull-deficit/`](../eo-hull-deficit/) §9 |

### 5a. What the sweep found

| $k$ | $n$ | solves | best $m$ found | $1/(k-1)$ | best $-$ threshold | landed on $1/(k-1)$ | distinct basins |
|---|---|---|---|---|---|---|---|
| 7 | 27 | 12344 | 0.166666666666666 | 0.166666666666667 | -1.94e-16 | 12001 | 196 |
| 7 | 27 | 12382 | 0.166666666666667 | 0.166666666666667 | -1.39e-16 | 12019 | 193 |
| 8 | 35 | 4734 | 0.142857142857143 | 0.142857142857143 | -1.67e-16 | 4519 | 156 |
| 9 | 44 | 902 | 0.125000000000000 | 0.125000000000000 | -2.08e-16 | 825 | 73 |
| 10 | 54 | 468 | 0.111111111111111 | 0.111111111111111 | -1.94e-16 | 413 | 49 |

**30830 local solves in total across the four targets, and not one exceeded $1/(k-1)$.** The largest value seen at any $k$ sits at the threshold to machine precision (the negative entries in the fourth column are the last bit of a double), so the abort-and-exactify trigger at $1/(k-1) + 10^{-9}$ never fired.

### 5b. How far below the lattice value the next basin lies

The naive statistic — best local optimum strictly below $1/(k-1)$ — is junk: it is dominated by incompletely converged copies of the lattice sitting $10^{-8}$ below it. Instead, for a ladder of exclusion radii $\varepsilon$, the best local optimum found below $1/(k-1) - \varepsilon$:

| $k$ | $\varepsilon = 10^{-9}$ | $10^{-6}$ | $10^{-4}$ | $10^{-3}$ |
|---|---|---|---|---|
| 7 | 0.166666665 | 0.166665586 | 0.166371035 | 0.165614855 |
| 8 | 0.142857141 | 0.142855825 | 0.142301027 | 0.140964689 |
| 9 | 0.124999994 | 0.124998969 | 0.123541185 | 0.123541185 |
| 10 | 0.111111025 | 0.109680570 | 0.109680570 | 0.109680570 |

Census keys are values rounded to 9 decimals and only the top 40 per run are kept, so 'none in top-40' means the retained tail did not reach that far down.

### 5c. Seed families

| $k$ | family | solves | reached $1/(k-1)$ | best $m$ |
|---|---|---|---|---|
| 7 | `corner_dense` | 2747 | 2707 (98.5%) | 0.166666666666666 |
| 7 | `hop` | 10874 | 10600 (97.5%) | 0.166666666666666 |
| 7 | `lattice_defect` | 2779 | 2778 (100.0%) | 0.166666666666666 |
| 7 | `rotated_lattice` | 2813 | 2732 (97.1%) | 0.166666666666667 |
| 7 | `rows` | 2750 | 2549 (92.7%) | 0.166666666666666 |
| 7 | `uniform` | 2763 | 2654 (96.1%) | 0.166666666666666 |
| 8 | `corner_dense` | 528 | 514 (97.3%) | 0.142857142857143 |
| 8 | `hop` | 2055 | 1975 (96.1%) | 0.142857142857143 |
| 8 | `lattice_defect` | 543 | 542 (99.8%) | 0.142857142857143 |
| 8 | `rotated_lattice` | 526 | 494 (93.9%) | 0.142857142857143 |
| 8 | `rows` | 545 | 496 (91.0%) | 0.142857142857143 |
| 8 | `uniform` | 537 | 498 (92.7%) | 0.142857142857143 |
| 9 | `corner_dense` | 110 | 100 (90.9%) | 0.125000000000000 |
| 9 | `hop` | 338 | 320 (94.7%) | 0.125000000000000 |
| 9 | `lattice_defect` | 119 | 117 (98.3%) | 0.125000000000000 |
| 9 | `rotated_lattice` | 116 | 100 (86.2%) | 0.125000000000000 |
| 9 | `rows` | 112 | 98 (87.5%) | 0.125000000000000 |
| 9 | `uniform` | 107 | 90 (84.1%) | 0.125000000000000 |
| 10 | `corner_dense` | 64 | 58 (90.6%) | 0.111111111111111 |
| 10 | `hop` | 181 | 157 (86.7%) | 0.111111111111111 |
| 10 | `lattice_defect` | 60 | 59 (98.3%) | 0.111111111111111 |
| 10 | `rotated_lattice` | 58 | 50 (86.2%) | 0.111111111111111 |
| 10 | `rows` | 50 | 46 (92.0%) | 0.111111111111111 |
| 10 | `uniform` | 55 | 43 (78.2%) | 0.111111111111111 |

### 5d. The best configuration at every $k$, put through the exact gate

Not just "$m$ agreed with $1/(k-1)$ to 15 digits": rationalised (denominator bound $10^8$) the best configuration found at each $k$ has $q_{\min}$ **exactly** equal to $1/(k-1)^2$, i.e. it *is* the $T(k)$ lattice minus a point, certified in exact rational arithmetic. The margin is exactly zero — not small, zero.

| $k$ | exact $a_{\min}$ | $q_{\min} - 1/(k-1)^2$ | gate reports refutation? |
|---|---|---|---|
| 7 | 6.000000000000000 | 0 | no |
| 8 | 7.000000000000000 | 0 | no |
| 9 | 8.000000000000000 | 0 | no |
| 10 | 9.000000000000000 | 0 | no |


---

## 6. The targeted attack: insert one point into a packing that already beats $k-1$

Waiting for a random multi-start to stumble into a counterexample is a poor use of the budget when
the *shape* of one is known. EO($k$) says $\Delta(k)-1$ points force side $k-1$; one point fewer
does not — the best known $\Delta(k)-2$ packings sit strictly below side $k-1$ (this is exactly
$d(26) > 1/6$). So:

> **a counterexample to EO($k$) is precisely a $\Delta(k)-2$ packing below side $k-1$ with room
> for one more point.**

`insert.py` attacks that directly, in three stages: (1) search for an elite pool of twelve
$\Delta(k)-2$ configurations; (2) for each, rank every site on a triangular grid plus random
sites by clearance from the existing points, insert the extra point at each of the top 220 holes
in turn, and re-optimise all $\Delta(k)-1$ points; (3) *delete-and-reinsert* on the resulting
incumbent — pull one point out, re-optimise the remaining $\Delta(k)-2$, and try every deep hole
again. Stage 3 is the same degree of freedom approached from the other side, and it is the move
that a plain basin-hop is least likely to make.

### 6a. The insertion attack

| $k$ | $\Delta(k){-}2$ | best $m(\Delta(k){-}2)$ | its side $a$ | insertions tried | best $m(\Delta(k){-}1)$ | excess over $1/(k-1)$ | exact $a_{\min}$ |
|---|---|---|---|---|---|---|---|
| 7 | 26 | 0.166738399395270 | 5.997418732738 | 2494 | 0.166666666666666 | -1.94e-16 | 6.000000000000 |
| 8 | 34 | 0.142860447191429 | 6.999838091365 | 1172 | 0.142857142857143 | -2.50e-16 | 7.000000000000 |
| 9 | 43 | 0.125000668124556 | 7.999957240257 | 654 | 0.125000000000000 | -2.36e-16 | 8.000000000000 |
| 10 | 53 | 0.111111111111111 | 9.000000000000 | 352 | 0.111111111111111 | -3.33e-16 | 9.000000000000 |

**4672 insertions in total; the exact gate refuted every resulting configuration** (`exact_refutes` = [False, False, False, False]). In every case adding the extra point drove the separation back to exactly $1/(k-1)$ or below.

| $k$ | reference $d(\Delta(k){-}2)$ | ours | agreement |
|---|---|---|---|
| 7 | 0.166738399395271 | 0.166738399395270 | 14.5 digits |
| 8 | 0.142869646754496 | 0.142860447191429 | 4.2 digits |
| 9 | *no published value* (GL stops at $n=36$) | 0.125000668124556 | — |
| 10 | *no published value* (GL stops at $n=36$) | 0.111111111111111 | — |


Stage 1 doubles as an independent check of the published table — and as an honest measure of how
much of the budget the shortened insertion stage had. At $k = 7$ it rediscovers
$d(26) = 0.166738399395271$ from scratch, and finds **twelve** distinct 26-point configurations
all sitting strictly below side 6. At $k = 8$ it does **not** reach the record: 130 s of stage-1
search returned $m(34) = 0.1428604\ldots$ against the published $0.1428696\ldots$, so the $k = 8$
insertion attack started from a slightly *worse* base packing than the best known, and its null is
correspondingly weaker. At $k = 9, 10$ there is no published value to compare against —
Graham–Lubachevsky's table stops at $n = 36$ — so those rows are this project's own best find, and
given the $k = 8$ shortfall they should be read as under-searched lower bounds, not as estimates
of $m(\Delta(k)-2)$.

**What actually happens.** In every case, inserting the extra point drives the separation back down
to exactly $1/(k-1)$ or below: the configuration relaxes into the lattice-with-a-hole rather than
finding somewhere new to put the point. That is not a proof of anything — it is what a local method
does — but it is the specific behaviour a next attack has to break.

### 6b. The most obvious structural candidate, killed: no **rotated** lattice does better

This came out of a sanity check on the seed families and is worth more than the seeds were.
A hexagonal lattice at spacing $\approx 1/(k-1)$, placed at a *random* rotation and offset,
does not even **hold** $\Delta(k)-1$ points inside the triangle: the aligned $T(k)$ lattice gets
$T(k)$ points only because every one of its boundary points lies exactly on an edge, and
rotating destroys that bonus. So ask the question directly —

> over all rotations $\theta$ and offsets, what is the largest spacing $s$ of a hexagonal
> lattice with at least $\Delta(k)-1$ points inside the unit triangle?

`lattice_scan.py` bisects on $s$ (the count is non-increasing in $s$) over a deterministic
$61 \times 81$ grid of $(\theta, \text{offset})$ plus random draws:

| $k$ | $n$ | $1/(k-1)$ | best rotated spacing | excess | attained at |
|---|---|---|---|---|---|
| 7 | 27 | 0.166666666666667 | 0.166666666666858 | +1.91e-13 | $\theta = 0^\circ$ |
| 8 | 35 | 0.142857142857143 | 0.142857142857305 | +1.62e-13 | $\theta = 0^\circ$ |
| 9 | 44 | 0.125000000000000 | 0.125000000000286 | +2.86e-13 | $\theta = 0^\circ$ |
| 10 | 54 | 0.111111111111111 | 0.111111111111237 | +1.25e-13 | $\theta = 0^\circ$ |

The maximum is $1/(k-1)$ at **every** $k$ and is attained at $\theta = 0^\circ$ — the aligned
lattice — with the excess column at the $10^{-13}$ level of the bisection itself, not a real
margin. **No rotated hexagonal-lattice fragment beats $T(k)$ minus a point.**

That is a heavily restricted statement and it is `numerical`: it samples $(\theta, \text{offset})$
rather than proving anything about the pairs it missed, and — more importantly — a counterexample
need not be a lattice fragment at all. But "a differently oriented lattice" is the first thing
one reaches for, several known optima genuinely are rotated fragments ($n = 13, 26$), and it is
now off the table for these four $k$.

---

## 7. The counterexample window, and the margin curve in $k$

This is the part that is quantitative rather than merely negative, and it is the part a next
worker should use.

**The elementary step.** Deleting a point from a configuration cannot decrease its minimum
separation, so $m(n) \le m(n-1)$ for every $n$. Hence any counterexample to EO($k$) satisfies

$$\frac{1}{k-1} \;<\; m(\Delta(k)-1) \;\le\; m(\Delta(k)-2),$$

so **its triangle side is confined to $a \in \bigl[\,1/m(\Delta(k)-2),\; k-1\,\bigr)$.** Write
$\delta(k) = m(\Delta(k)-2) - \tfrac{1}{k-1}$: an upper bound on how badly EO($k$) can fail.

**The conditionality, stated plainly.** $m(\Delta(k)-2)$ is not known exactly for any $k \ge 3$;
the table below substitutes the published *best-known* $d(\Delta(k)-2)$, so the window is
**conditional on that record being optimal** and is `numerical`. Nothing here is assumable.

The table stops at $k = 8$ because Graham–Lubachevsky's stops at $n = 36$. This project's own
values at $n = 43$ and $n = 53$ (§6a) are *lower* bounds on $m(\Delta(k)-2)$ from a two-to-four
minute search, and at $n = 53$ that search did not beat the lattice value at all — so they would
understate the window rather than measure it, and they are deliberately not tabulated as if they
did.

| $k$ | $n{-}2$ | $d(\Delta(k)-2)$ | $1/(k-1)$ | $\delta(k)$ | $\delta(k{-}1)/\delta(k)$ | window for $a$ | width | width$/(k-1)$ |
|---|---|---|---|---|---|---|---|---|
| 3 | 4 | 0.577350269189626 | 0.5 | 7.735e-2 | — | [1.732050808, 2) | 2.68e-1 | 1.34e-1 |
| 4 | 8 | 0.343070330817254 | 0.333333333 | 9.737e-3 | 7.94 | [2.914854216, 3) | 8.51e-2 | 2.84e-2 |
| 5 | 13 | 0.251813236653061 | 0.25 | 1.813e-3 | 5.37 | [3.971197119, 4) | 2.88e-2 | 7.20e-3 |
| 6 | 19 | 0.200321458983439 | 0.2 | 3.215e-4 | 5.64 | [4.991976422, 5) | 8.02e-3 | 1.60e-3 |
| **7** | **26** | **0.166738399395271** | **0.166666667** | **7.173e-5** | **4.48** | **[5.997418733, 6)** | **2.58e-3** | **4.30e-4** |
| 8 | 34 | 0.142869646754496 | 0.142857143 | 1.250e-5 | 5.74 | [6.999387363, 7) | 6.13e-4 | 8.75e-5 |

Sources for the $d$ column: Graham–Lubachevsky (EJC 2 (1995) #A1, 15 s.f.) and Friedman's exact
closed forms, both via
[`experiments/circle-packing-search/reference.py`](../../../../experiments/circle-packing-search/reference.py).
Nothing in that column is computed here.

**What the curve says.** $\delta(k)$ collapses by a factor of roughly **5 per increment of $k$**,
and the window width relative to the side collapses by roughly **4 per increment**. At $k = 7$ a
counterexample has $0.043\%$ of the side length to hide in; at $k = 8$, $0.0088\%$.

This **inverts the strategic guess** that motivated running $k = 8,9,10$ at all — that a
counterexample at large $k$ is "as good and the search space is differently shaped". It is
differently shaped, but it is *smaller*: conditional on the records, the room available for a
refutation shrinks geometrically in $k$. If Erdős–Oler is false anywhere, the most room is at the
**smallest** open case, $k = 7$, and even there the target is a $2.6\times10^{-3}$ interval of side
length. A future refutation attempt should not expect large $k$ to be easier.

The same curve is a warning about numerics. At $k = 8$ the entire window is $6\times10^{-4}$ wide
in $a$, i.e. $1.25\times10^{-5}$ in $m$ — comfortably inside the range where a sloppy optimiser
"beats" the conjecture. That is precisely why §2's gate is exact rational arithmetic and why every
number in §5 is measured on points that have been projected into the triangle first.

---

---

## 8. What this attack did **not** cover — read this before repeating it

A null result is only useful with its coverage attached. This search is a **stochastic local**
method: it establishes nothing about regions it did not visit, and the following regions it
provably did not visit or visited badly.

1. **Nothing here is exhaustive.** There is no branch-and-bound, no interval covering of
   configuration space, no rigorous global optimisation. The negative result is
   "$N$ SLSQP descents from these seed distributions found nothing", full stop. A rigorous
   exhaustion is what [`../eo-exhaustion/`](../eo-exhaustion/) measured the cost of, and it
   concluded a rational-side-length exhaustion cannot prove EO at *any* $k$ for a structural
   reason — so this gap is not one more compute budget away from being closed.

2. **The lattice attractor dominates the sampling, so the hit rate is not coverage.** At
   $n = \Delta(k)-1$ roughly 95% of *all* local solves — from uniform random seeds included — land
   on exactly $1/(k-1)$. That looks like thorough coverage and is the opposite: most of the budget
   is spent rediscovering the same basin. The $n = 26$ control makes the danger concrete — **0 of
   60 uniform starts** reached $d(26)$, an optimum only $7\times10^{-5}$ above $1/6$. A structure
   of that kind at $n = 27$ would be correspondingly hard for this method to reach, and the fact
   that it was not reached is weak evidence.

3. **Deep off-lattice structures.** Basin hopping perturbs at most $n/3$ points at a time and SLSQP
   then descends; a counterexample requiring the *simultaneous* precise placement of many points in
   a configuration far from every lattice fragment is exactly what this cannot construct.

4. **Feasibility formulations were not tried.** Everything here is max–min optimisation. Fixing
   $a = 5.999$ and searching for *any* feasible 27-point placement — constraint propagation, SAT/SMT
   over a cell decomposition, interval Newton — is a differently shaped search with different
   failure modes and was not run.

5. **Lubachevsky–Stillinger was not ported.** Problem `RULES.md` §5 names LS billiard simulation as
   the standard generator; `experiments/circle-packing-ls/` exists and was not used here. The NLP
   was used as both generator and polisher, which is the same choice
   `experiments/circle-packing-search` made and inherits the same blind spots.

6. **$k = 9$ and $k = 10$ are thin.** Solve counts there are in the hundreds, not thousands, because
   a single solve costs 0.5 s and 1.4 s respectively. Those two rows are orientation, not a search.

7. **$k \ge 11$ was not touched at all**, and neither was any non-triangular pattern.

8. **Symmetry classes were not enumerated.** No symmetric ansatz ($C_3$, $D_3$, mirror) was solved
   in its own reduced coordinates, which is the cheapest way to reach highly symmetric
   configurations that random seeding hits with vanishing probability. Problem `RULES.md` §5 warns
   against *restricting* to symmetric configurations — but sampling them deliberately *in addition*
   is not that mistake, and it was not done.

9. **The corner-density necessary conditions were used only as a seeding heuristic**, never as a
   filter and never as an assumption. [`../eo-hull-deficit/`](../eo-hull-deficit/) §9 derives (status
   `sketch` there, and therefore not assumable) that a $k = 7$ counterexample must have at least
   $T(j)$ points in the open corner triangle of side $j$ at every corner, $j \le 5$. The right way
   to use that is to *enumerate* configurations satisfying it; here it only shaped one of five seed
   families.

## 9. Honest accounting

**The single thing I am least sure of** is §7's conditionality. The window
$[1/m(\Delta(k)-2), k-1)$ is rigorous, but every numeric window in the table replaces the unknown
$m(\Delta(k)-2)$ with a *best-known* record. If any of those records is not optimal, the
corresponding window is wider than stated. The $k = 8$ row is the one to distrust first: this
project's own short search fell $9\times10^{-6}$ short of the published $d(34)$ (§6a), which is
most of $\delta(8)$ itself, so the table's precision there is inherited, not confirmed. The
qualitative conclusion (geometric collapse in $k$) would survive a modest error in any single row;
a systematic one it would not.

**Next in doubt**: §6b's rotated-lattice scan samples $(\theta, \text{offset})$ on a grid plus
random draws and bisects a float spacing to $\sim10^{-13}$. It is not exact and it is not
exhaustive over orientations; read it as "no rotated lattice was found that beats the aligned one",
which is weaker than "none exists". It is also silent about non-lattice structures, which is what a
counterexample most likely is.

**After that**: the claim that ~95% of solves land on the lattice value is measured on *this* seed
mixture, and the mixture was chosen by me. A different mixture would give a different number, so
the figure characterises the method, not the problem.

**Novelty: none is claimed, and I would assume there is none.** Every ingredient is standard:
multi-start NLP, basin hopping, exact rational verification. The margin curve in §7 is arithmetic
on published tables plus a one-line monotonicity remark; anyone who has looked at Graham–Lubachevsky's
table next to the conjecture has probably noticed it.

**What is not claimed.** No bound on $s(n)$ for any $n$. No optimality. No statement that
Erdős–Oler is true at any $k \ge 7$ — failing to find a counterexample is not a proof, and the
coverage list in §8 says exactly how far from one this is.
