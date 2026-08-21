# Attack: trying to **refute** Erdős–Oler — the measured shape of the search space at $k = 7,8,9,10$

**Claim type: neither.** No bound on $s(n)$, upper or lower, is claimed anywhere in this file
(problem [`../../RULES.md`](../RULES.md) §1 asks for that sentence first). What is here is a
*failed refutation*, made quantitative: a measured census of the top of the optimisation landscape
at $n = \Delta(k)-1$ for $k = 7,8,9,10$, an exact-arithmetic gate that every candidate was pushed
through, one **exact rational certificate for a positive control**, and a margin curve saying how
much room a counterexample has left to hide in — and how fast that room is closing as $k$ grows.
Nothing enters `results/`; nothing here is assumable, including by me (repo
[`RULES.md`](../../../../RULES.md) §3).

- **Outcome: no counterexample.** No local optimum anywhere in this attack exceeded $1/(k-1)$.
  The abort-and-exactify trigger never fired. This is evidence that *this search* did not find one,
  and nothing more.
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
| §5 the census at $k = 7,8,9,10$ | `numerical` |
| §6 the insertion attack | `numerical` |
| §7 the counterexample window and margin curve | `numerical`, and **conditional** on published records being optimal |
| Erdős–Oler at $k \ge 7$ | **untouched.** Still open. |

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
**conditional on that record being optimal** and is `numerical`. Graham–Lubachevsky's table stops
at $n = 36$, so $k \ge 9$ has no published entry at all; those rows use this project's own
best-found value, which is a *lower* bound on $m(\Delta(k)-2)$ and therefore gives a window that
understates the true one. Nothing here is assumable.

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

## 5. The census at $k = 7, 8, 9, 10$

`run.py hunt`, five seed families cycled round-robin for the first 40% of the budget, then basin
hopping from an eight-strong elite pool with four move types (teleport a random subset, re-roll the
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
