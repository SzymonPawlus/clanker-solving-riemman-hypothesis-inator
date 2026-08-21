# Attack: how many sets of diameter $<1$ does $T_a$ need? (the covering route, attacked from below)

**Claim type: lower bound — but not on $s(n)$.** Problem [`../../RULES.md`](../../RULES.md) §1 asks
which of the two kinds of statement this is. It is neither: nothing here bounds $s(n)$ or $d(n)$
in either direction. What is bounded below is an auxiliary quantity, the **covering number**
$N^*(a)$ of the triangle by sets of diameter $<1$, which is the resource the covering route to
Erdős–Oler consumes. A lower bound on $N^*$ is an *obstruction* to that route, not a packing result.

**Verdict: the route is NOT killed.** Best proved floor $N^*(a)\ge 25$; a kill needs $27$;
**the exact remaining gap is 2**. Details, and why the second of those two is much harder than
the first, in §5.

- Author: `claude` (Claude Opus 5 — convergent role, repo [`RULES.md`](../../../../RULES.md) §8:
  this is checking and exact calculation), 2026-08-21, worker **W2 (Refuter)**
- Branch: `claude/circle-equklatetal-problem-sa7tx7`
- Kill-criteria, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code: [`experiments/packing-eo-covering-bound/`](../../../../experiments/packing-eo-covering-bound/)
  — stdlib only, one command, **every decision exact**; floats only *propose* configurations
- Journal: [`notebook/claude/2026-08-21-eo-covering-bound.md`](../../../../notebook/claude/2026-08-21-eo-covering-bound.md)

## Status table

| What | Status |
|---|---|
| **T1** corner-refined isodiametric floor: $N^*(a)\ge 3+\bigl(\tfrac{\sqrt3}4a^2-\tfrac\pi2\bigr)\tfrac4\pi$, giving $N^*(a)\ge 21$ for $a\in[5.9,6]$ | `sketch` — my proof (§2); depends on the isodiametric inequality (`cited`) |
| **T2** the duality $N^*(a)\ge m$ for any $m$ points of $T_a$ at pairwise distance $\ge1$ | `sketch` — one line (§3); already stated in [`../eo-small-cases/`](../eo-small-cases/) §3.3 and **credited there, not reclaimed** |
| **C22–C25** explicit $1$-separated sets of $22,23,24,25$ points in $T_a$ with $a<6$ | `numerical` — exact rational certificates, verified twice by independent routes |
| **F** $N^*(a)\ge 25$ for every $a\in[\tfrac{5983367}{10^6},\,6)$ | `sketch` (T2, applied to C25) |
| **T3** the $\chi$-vs-$\omega$ bound $N^*(a)\ge m+\chi(G_Z)$ — the only method here that could reach 27 | `sketch` — my proof (§4) |
| **N1** no $\chi>\alpha$ gap found over 200 searched configurations | `numerical` — a failed search, not a theorem (§4) |
| **N2** $n=26$ and $n=27$: no configuration below $a=6$ found | `numerical` — see §3.3 and the §6 control |
| isodiametric (Bieberbach) inequality: $\operatorname{diam}K\le d\Rightarrow \operatorname{area}K\le\pi d^2/4$ | `cited` — standard |

**Nothing here is assumable, including by me.** Nothing enters `results/`.

## Kill-criterion outcomes, up front (repo `RULES.md` §6.3)

> **K1 (primary).** *"If the best floor I can prove is $\le 26$, stop and report the floor and the
> gap; do not re-scope."* — **MET.** Floor 25. I stopped; I did not drift into constructing
> coverings (W1's lane) or into attacking Erdős–Oler directly.
>
> **K2 (separated points).** *"If the separated-point method reaches 26 it is exhausted, not
> promising."* — **not reached** (I got 25, §3.3). The criterion still bites in the other
> direction: even a perfect run of this method tops out at 26 and cannot kill the route.
>
> **K3 ($\chi$-vs-$\omega$).** *"If every $G_Z$ I build is $\alpha$-colourable, declare the method
> unproductive and stop."* — **MET, §4.** 25 single-deletion and 175 double-deletion patterns off
> the $n=25$ certificate; **no gap in any of them**, and in fact the freed regions were so small
> that $\chi(G_Z)\le1$ throughout.
>
> **K4 (LP/area).** *"If the area–perimeter relaxation tops out below 27, record the number and
> stop optimising it."* — **MET, §2.3.** The relaxation's own ceiling is around 22–23 and its
> *proved* value here is 21. I did not go back for one more weight function.

## Normalisation — asserted in code, not assumed in prose

Separation **1**. $T_a$ is the closed equilateral triangle of side $a$. A **piece** is a set of
diameter $<1$ (strict); $N^*(a)$ is the least number of pieces whose union contains $T_a$.
$N^*$ is non-decreasing in $a$.

The repo's `results/` certificates use separation $2$ and side $d=2a$. **Nothing in this attack
reads them**, and no conversion happens anywhere, so the normalisation slip that caught several
workers today (including the manager) has no place to occur. The code works in **triangular
coordinates**: a point is $(u,v)$ meaning the Cartesian point $\bigl(u+\tfrac v2,\ \tfrac{v\sqrt3}2\bigr)$,
so that
$$T_a=\{u\ge0,\ v\ge0,\ u+v\le a\},\qquad |P-Q|^2=\Delta u^2+\Delta u\,\Delta v+\Delta v^2 .$$
Both the three containments and all $\binom n2$ distances are then comparisons of **rationals**;
$\sqrt3$ never appears, and no field extension is needed.

## What the route needs, and what this file says about it

W1 is trying to cover $T_a$, $a<6$, with $N\le26$ pieces. That would prove Erdős–Oler at $k=7$:
27 points at pairwise distance $\ge1$ cannot be distributed among 26 pieces, since two points at
distance $\ge1$ cannot share a set of diameter $<1$. So the route lives or dies on

$$N^*(a)\ \le\ 26\quad\text{for every }a<6 .$$

**Proved here:** $N^*(a)\ \ge\ 25$ for every $a\in[5.9833670,\,6)$.

The route therefore survives, in a window of width at most **one piece**: on that interval a
covering proof must use 25 or 26 pieces, and no more. Before this file the repo's floor was 20
(area alone) against a best construction of 34.

---

## 1. Circularity guard — read this before using any number below

The bound $N^*(a)\ge\max\{n:a_n\le a\}$ is the sharpest tool available here, and it is **worth
nothing** if the $a_n$ fed into it is the statement being derived. That is exactly the failure
recorded in `FINDINGS.md` under *"A `cited` input contained the conclusion"*, where a `cited`
$d(9)=3$ — which **is** Erdős–Oler at $k=4$ — was handed to a relaxation which correctly derived
it back out.

**Rule adopted before computing, and kept:** every separated set used below is one this attack
**exhibits explicitly** and verifies with exact rational arithmetic. No literature value of $a_n$,
$s(n)$ or $d(n)$ is an input to any bound in this file. A construction is self-certifying; that is
the whole reason to insist on one.

This cuts the other way too, and it is worth being precise about which side of the line things fall:

- a published *optimal value* $a_{26}$, used as a bound, would be circular-adjacent and is refused;
- a published *construction* — Graham–Lubachevsky's coordinates for $n=26$, re-verified here from
  scratch — would be perfectly legitimate, and would lift the floor from 25 to 26 immediately.
  I could not obtain one: network egress is blocked in this session, as
  [`../eo-literature/`](../eo-literature/) already recorded. **This is the cheapest available
  improvement to this file and it needs no cleverness, only a table.**

Erdős–Oler itself is used **nowhere as a step**. It appears only as an expectation, in K2/K3 and in
§5, to explain why a method has a ceiling.

## 2. T1 — the corner-refined isodiametric floor (no construction needed)

The floor the repo had was $N^*>\operatorname{area}(T_a)/(\pi/4)$, i.e. $\ge20$ as $a\to6^-$.
One elementary observation buys a piece.

> **Lemma 2.1.** If a piece $S$ contains a corner $V$ of $T_a$ then $\operatorname{area}(S\cap T_a)\le\pi/6$.

*Proof.* $\operatorname{diam}S<1$ and $V\in S$, so $S\subseteq B(V,1)$. For $a\ge2$ the set
$B(V,1)\cap T_a$ is exactly the $60°$ circular sector of radius 1 at $V$, of area $\pi/6$. $\square$

> **Lemma 2.2.** The three corners lie in three **distinct** pieces (they are pairwise at distance
> $a\ge1$).

> **Theorem T1.** For $a\ge2$, every covering of $T_a$ by pieces satisfies
> $$\operatorname{area}(T_a)\ \le\ 3\cdot\frac\pi6+(N-3)\cdot\frac\pi4,\qquad\text{i.e.}\qquad
> N\ \ge\ 3+\Bigl(\frac{\sqrt3}4a^2-\frac\pi2\Bigr)\frac4\pi .$$

*Proof.* Sum $\operatorname{area}(S_i\cap T_a)$ over the covering: three of the terms are $\le\pi/6$
by Lemmas 2.1–2.2, and every term is $<\pi/4$ by the isodiametric inequality (`cited`). $\square$

Evaluated with **certified rational enclosures** of $\pi$ (checked against Machin's formula inside
`bound_area.py`) and of $\sqrt3$, rounded in the direction that weakens the conclusion:

| $a$ | area-only floor | **T1 floor** |
|---|---:|---:|
| $6$ | $19.8478\Rightarrow 20$ | $20.8478\Rightarrow\mathbf{21}$ |
| $5.999999$ | $19.8478\Rightarrow 20$ | $20.8478\Rightarrow\mathbf{21}$ |
| $5.9833670$ | $19.7379\Rightarrow 20$ | $20.7379\Rightarrow\mathbf{21}$ |
| $5.9$ | $19.1918\Rightarrow 20$ | $20.1918\Rightarrow\mathbf{21}$ |

**$N^*(a)\ge21$ for every $a\in[5.9,6]$**, with no construction and no search behind it — this is
the strongest *construction-free* statement in the file, and the only one that is uniform in $a$
without reference to a particular configuration.

### 2.3 Why I did not push the area route further (K4)

The natural next step is an area–**perimeter** relaxation: weight $\mu=\text{area}+\lambda\cdot
(\text{length on }\partial T_a)$ and divide $\mu(T_a)$ by the largest $\mu$-value of a single
piece. I set this up, estimated it, and stopped, because the method has a ceiling well below 27
and the estimate is not close:

- **The fractional relaxation of "cover by diameter-$<1$ sets" has value exactly
  $\operatorname{area}/(\pi/4)$ in the interior.** The measure $\text{Lebesgue}/(\pi/4)$ is
  feasible, and a disc of diameter 1 placed anywhere in the interior saturates it. So *no
  non-negative excess supported near $\partial T_a$ can simply be added on top*: a disc tangent to
  an edge already attains the bound with equality, forcing any added boundary density to vanish.
  All the available gain is redistribution, not addition.
- Estimating the best redistribution (the piece-value trade-off between area and the boundary
  length a piece can cover) puts the ceiling of the whole area–perimeter family at roughly
  **22–23**, and that estimate already uses the *optimistic* piece bound — the true maximal
  area of a diameter-1 set covering a chord of length $\ell$ on a boundary line, which I did not
  prove. With a bound I can actually prove, the family delivers less.

The distance from 34 (best construction) to 20 (area) is an **integrality gap**, not a boundary
effect, and no area-type relaxation closes an integrality gap. K4 says record and stop; recorded,
stopped. **This paragraph is an estimate, explicitly not a theorem** — it is here so that a later
"just one more weight function" is visibly a violation of a criterion written in advance.

## 3. T2 and the certificates — the floor of 25

> **T2.** If $P\subseteq T_a$ has $|P|=m$ and all pairwise distances $\ge1$, then $N^*(a)\ge m$.

*Proof.* Two points at distance $\ge1$ cannot lie in one set of diameter $<1$, so the $m$ points
occupy $m$ distinct pieces. $\square$

(This is [`../eo-small-cases/`](../eo-small-cases/) §3.3, found there first and **credited, not
reclaimed**; it is restated because everything below is an application of it.)

### 3.1 The certificates

Found by float search (`shrink.py`, `hop.py` — shrink-the-triangle with basin hopping, seeds
pinned), then **snapped to rationals with denominator $10^6$ and certified exactly**. The float
runs used a separation margin of $1.0002$–$1.002$, so the rounding — at most $5\cdot10^{-7}$ per
coordinate — is absorbed with three orders of magnitude to spare, and *no float takes part in any
decision*.

| $n$ | certified $a$ | $a$ (decimal) | min squared distance | $a<6$ |
|---:|---|---:|---:|:--:|
| 22 | $\tfrac{2808381}{500000}$ | $5.6167620$ | $1.004002982$ | yes |
| 23 | $\tfrac{717941}{125000}$ | $5.7435280$ | $1.004004000$ | yes |
| 24 | $\tfrac{14333}{2500}$ | $5.7332000$ | $1.000399211$ | yes |
| **25** | $\tfrac{5983367}{1000000}$ | $\mathbf{5.9833670}$ | $1.004002073$ | **yes** |
| 26 | — | best hypothesis $6.001118$ | — | **no** |
| 27 | — | best hypothesis $6.001203$ | — | **no** |

Full coordinates: `experiments/packing-eo-covering-bound/out/certificates.json`.

**Checked twice, by deliberately different routes** (problem `RULES.md` §3 asks for reimplementation,
not a rerun): `verify.py` tests the triangular-coordinate inequalities directly, while `recheck.py`
converts to **Cartesian** coordinates and re-tests there — squaring the three half-plane conditions
so that $\sqrt3$ need not be approximated, plus a 60-digit decimal cross-read of the heights with a
certified $\sqrt3$ enclosure. Both routes agree on all four certificates.

*(A first draft of `recheck.py` reported all four as FAILING on the left edge. That was the
re-check being wrong, not the certificates: it compared $y$ against $\sqrt3x$ using an interval for
$\sqrt3$ on **both** sides of an identity in which $\sqrt3$ cancels, so every point with $u=0$ — i.e.
every point actually on that edge — failed by the width of the enclosure. Recorded because it is
the exact shape of error this file exists to catch, and because it went the safe way: a spurious
rejection, not a spurious acceptance.)*

### 3.2 The floor

> **F.** $N^*(a)\ \ge\ 25$ for every $a\in[\tfrac{5983367}{10^6},\ 6)$.

*Proof.* C25 exhibits 25 points of $T_{5983367/10^6}$ at pairwise distance $\ge1$; T2 gives
$N^*(5983367/10^6)\ge25$; $T_a\supseteq T_{a'}$ for $a\ge a'$, so $N^*$ is non-decreasing. $\square$

That is the interval that matters: a covering proof of Erdős–Oler at $k=7$ must handle **every**
$a<6$, this window included.

### 3.3 Where $n=26$ stopped, honestly

$n=26$ is the value that would make the requirement exactly tight, and I did not get it. What was
tried, and what the failure looks like:

- random multistart + inflation; shrink-the-triangle with adaptive step; basin hopping with three
  shake amplitudes; seeding from the certified $n=25$ and best $n=24$ configurations plus extra
  points; and a **targeted screen** of deletions from the side-6 lattice, on the observation that
  the 28-point lattice is rigid at $a=6$ because each edge carries 7 points spanning length 6, and
  that deleting a **corner** breaks two of those three edges at once.
- Every lattice-derived start relaxed to $a=6.0012=6\times1.0002$ — i.e. to a configuration whose
  true side is exactly 6, refusing to compress at all. That is consistent with the two smaller
  proven cases: the optimal $\Delta(k)-2$ configuration is **not** the lattice minus two points
  (which is rigid) but a genuine rearrangement — at $k=4$, $a_8=1+\tfrac{\sqrt{33}}3$, and at
  $k=5$, $a_{13}\approx3.9712$, neither of them a truncated lattice.
- The gap being searched for is small. Extrapolating the two known deficits
  $3-a_8\approx0.0849$ and $4-a_{13}\approx0.0288$ (a ratio near 3) suggests $6-a_{26}$ of order
  $3\cdot10^{-3}$. A local search must therefore find a global rearrangement worth a few parts in
  a thousand; mine did not. **This is a failure of my search, and should not be read as evidence
  that $a_{26}=6$** — that extrapolation is arithmetic on two data points and is offered as
  context, not as a claim.

## 4. T3 — the $\chi$-vs-$\omega$ tool, and why it is the only way to 27

T2 cannot reach 27, and this is structural rather than a matter of effort: $m\le26$ separated
points is exactly what Erdős–Oler at $k=7$ asserts, so a 27th would refute the conjecture, not
prove it. **Any kill must therefore come from a bound that exceeds the largest separated set** —
an integrality gap between the clique number and the chromatic number of the "distance $\ge1$"
graph. There is one such tool:

> **T3.** Let $P\subseteq T_a$ be $1$-separated, $|P|=m$, and let
> $Z=\{z\in T_a:\ |z-p|\ge1\ \ \forall p\in P\}$ be the region free of $P$. Then for **any** finite
> $Z'\subseteq Z$,
> $$N^*(a)\ \ge\ m+\chi(G_{Z'}),$$
> where $G_{Z'}$ joins two points of $Z'$ when their distance is $\ge1$.

*Proof.* In any covering, the $m$ points of $P$ occupy $m$ distinct pieces (T2). No $z\in Z$ lies
in any of those pieces, since $z$ is at distance $\ge1$ from their $P$-point. So the remaining
$N-m$ pieces cover $Z'$, and each of them meets $Z'$ in a set of pairwise distances $<1$ — an
independent set of $G_{Z'}$. Hence $N-m\ge\chi(G_{Z'})$. Passing to a finite $Z'$ only lowers
$\chi$, so the inequality is safe. $\square$

**Why this can beat T2 and nothing else can.** $m+\alpha(G_Z)$ is just "a larger separated set", so
T3 improves on T2 exactly when $\chi(G_Z)>\alpha(G_Z)$. Such gaps genuinely exist in this setting:
five points in pentagram position on a circle of radius $r\in[0.5257,\,0.8507)$ have
"distance $\ge1$" graph $C_5$, with $\alpha=2$ but $\chi=3$. So the target is concrete: a
$1$-separated $P$ with $|P|=24$ whose free region contains an **odd cycle** — that alone gives
$N^*\ge24+3=27$ and kills the route, while implying nothing about Erdős–Oler.

**What the search found: nothing (N1).** Over the $n=25$ certificate, on a $1/16$ triangular grid
of $Z$, exactly: 1 full configuration, 25 single-deletion patterns, 175 double-deletion patterns
(all pairs at squared distance $\le9$, the ones that leave a single connected hole rather than two
distant ones). **No $\chi>\alpha$ gap anywhere.** The freed regions were not merely bipartite —
they were *edgeless*: deleting one or two points from a saturated configuration leaves a hole of
diameter $<1$, which one piece covers, so $\chi(G_Z)\le1$ and T3 returns the floor 25 it started
from. K3 is met and I stopped.

The diagnosis is worth stating, because it tells the next worker where **not** to look. A gap needs
$Z$ to be *large and awkward at the same time*, and those pull against each other: deleting points
from a tight configuration makes $Z$ small (no gap possible), while starting from a loose $P$ makes
$Z$ large but then $\alpha(G_Z)$ grows with it, so the gap has to be found against a bigger
$\alpha$. The productive regime is a $P$ that is **locally maximal but globally poor** — every
point jammed, yet the whole configuration far from optimal, leaving one large connected cavity.
None of my configurations had that shape, and I did not find a way to search for it directly.

## 5. Verdict, and the exact remaining gap

| | pieces |
|---|---:|
| best construction (W1's side, from [`../eo-oler-equality/`](../eo-oler-equality/) §8) | 34 |
| **requirement to prove Erdős–Oler at $k=7$** | **$\le26$** |
| **floor proved here** | **25** |
| previous floor in the repo (area/isodiametric) | 20 |

**The route is not killed. The gap is 2.** It does not divide into two equal halves:

1. **25 → 26** is the *easy* one, and it is not even a research step: any $1$-separated 26-point
   configuration in some $T_a$ with $a<6$ closes it, and one is almost certainly tabulated in
   Graham–Lubachevsky. It needs a table, not an idea (§1). Its consequence is sharp: it would show
   the covering must be **exactly optimal**, $N=26$ with every piece containing exactly one point
   of a maximum separated set — zero slack, which is the same "the optimum is the minimum
   conceivable" wall that [`../eo-small-cases/`](../eo-small-cases/) §3.3 hit at $k=4$.
2. **26 → 27** is the *whole* problem. It cannot come from separated points at all (K2), so it
   must come from T3 or something like it: a proof that the triangle's covering number strictly
   exceeds its packing number. I searched 201 configurations for the smallest instance of that
   phenomenon and found none.

**For W1 concretely:** your target is not merely "26 pieces". On $a\in[5.9833670,6)$ you must reach
25 or 26 pieces against constructions currently at 34, and if step 1 above is closed you must hit
26 exactly with every piece carrying exactly one point of a maximum separated set. Nothing here
proves you cannot. But the room is one piece wide at most, and the two known-proven cases suggest
that room is zero.

## 6. The §7 control — what would have been an extraordinary claim, and was not

A floor of 27 proves an open case; 27 separated points below $a=6$ would *refute* the conjecture.
Both were live outcomes of this attack and both were treated as bugs-first by construction:

- The $n=27$ search was run as a **control**. Its best float hypothesis is $a=6.001203$, i.e. at or
  above 6, and the exact verifier rejected it for exactly that reason. **No Erdős–Oler violation
  was found, and none was reported.**
- Mid-run, one float configuration for $n=27$ appeared at $a/\text{margin}=5.99998$, which read
  naively is 27 separated points below 6. It is float noise on the side-6 lattice at $2\cdot10^{-5}$,
  and the exact rational verifier — which never sees the rescaling — rejects it. This is why the
  certificate pipeline never divides by the search margin: the certified $a$ is the one the float
  search actually achieved, so the margin is spent on rounding slack rather than on shaving $a$.

## 7. What to review hardest

- **§4's T3**, specifically that no $z\in Z$ can lie in a piece containing a point of $P$, and that
  restricting to a finite $Z'$ lowers rather than raises the bound. It is the only statement here
  that could reach 27, so an error in it would be the expensive kind.
- **§2's Lemma 2.1** — that $B(V,1)\cap T_a$ *is* the $60°$ sector (it needs $a\ge2$, and it is the
  step where a piece could sneak extra area past me), and Lemma 2.2's "distinct pieces".
- **The certificates**, ideally by a third checker written from the problem statement rather than
  from `exactlib.py`. The triangular-coordinate identity $|P-Q|^2=\Delta u^2+\Delta u\Delta v+\Delta v^2$
  is where a systematic error would hide, and it would hide in *both* of my checkers at once —
  §3.1's cartesian re-check shares that identity even though it shares no code.
- **§2.3's claim that the fractional relaxation is capped at $\operatorname{area}/(\pi/4)$.**
  It is an estimate, it is load-bearing for the decision to stop, and it is the thing here I am
  least sure of.

## 8. Reproducing

```
sh experiments/packing-eo-covering-bound/run.sh
```

Standard library only. Exact rational arithmetic in every decision; $\pi$ and $\sqrt3$ enter only
as certified enclosures rounded against the conclusion. The float searches that *propose*
configurations pin their seeds and their output is checked in under `out/`; nothing they say
decides anything.
