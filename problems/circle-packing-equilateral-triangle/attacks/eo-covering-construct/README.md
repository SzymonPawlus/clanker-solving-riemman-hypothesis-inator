# Attack: build a small-diameter covering of $T_a$, $a<6$ — how far the pieces get

**Claim type: construction (upper bounds on a covering number).** Every positive statement here
is a finite, self-certifying object — a list of convex cells — checked in exact arithmetic. The
*negative* statements (why 26 was not reached) are measurements and accounting, not theorems.

- Author: `claude` (W1, Constructor), 2026-08-21, branch `claude/circle-equklatetal-problem-sa7tx7`
- Code: [`experiments/packing-eo-covering/`](../../../../experiments/packing-eo-covering/) —
  one command, Python standard library only.
- Kill-criteria fixed before computing: [`KILL-CRITERION.md`](./KILL-CRITERION.md)

| What | Status |
|---|---|
| §2 lattice lemma, $T_a \to \Delta(p)$ cells of diameter $\le1$ for $a\le p\sqrt3/2$, checked $p\le10$ | `numerical` — **exact** arithmetic, but one implementation (mine). Problem [`RULES.md`](../../RULES.md) §3 needs a second, independent checker before this is assumable |
| §2 the same statement for all $p$ | `sketch` — proof sketched, not machine-checked |
| §3 the 26- and 27-cell certificates (`cert26.json`, `cert27.json`) | `numerical` — exact, same caveat |
| §3 the search numbers $D(N)$ | `numerical` — floats, local search, no optimality claim |
| §4–§5 the waste accounting and the deficit table | `sketch` — arithmetic on top of measurements |
| §6 the resulting lower bounds $a_n$ for $n=\Delta(p)+1$ | `numerical`, and **novelty UNVERIFIED** — see §6 |
| Oler's inequality (used only for comparison) | `cited`, via [`../oler-lower-bound/`](../oler-lower-bound/) |

**Headline.** The best covering of $T_6$ in this repo was **34** pieces. It is now **28**, exactly
verified, and 28 is *not* an accident of one scheme: it is $\Delta(7)$, and the same construction
gives $\Delta(p)$ for every $p$. Erdős–Oler at $k=7$ needs **26**. So the covering route is short
by **2 pieces, not by 8** — but every attempt to remove those 2 lands 3–4 % short, and §4 says
where the 4 % sits.

---

## 0. Normalisation — asserted in code, not in prose

Separation **1**. $T_a$ = the closed equilateral triangle of side $a$ with corners $(0,0)$,
$(a,0)$, $(a/2,\,a\sqrt3/2)$, exactly as [`../../RULES.md`](../../RULES.md) §2 fixes it. A *piece*
is a set of diameter $<1$; write $N^*(a)$ for the least number of pieces covering $T_a$. Several
workers, including the manager, mixed this up with the separation-2 / side-$d{=}2a$ certificate
convention today; **nothing in this attack reads or writes `results/`**, so no conversion happens
anywhere, and `run.py` asserts the basis identities before doing anything else.

Everything is computed in the **triangular-lattice basis** $e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$, in
which
$$|u\,e_1+v\,e_2|^2 \;=\; u^2+uv+v^2 ,\qquad T_a=\{u\ge0,\ v\ge0,\ u+v\le a\},$$
a **rational** quadratic form: no square root ever enters a distance. Coordinates live in
$\mathbb{Q}(\sqrt3)$ (the good schemes use spacing $\sqrt3/2$), with an exact sign test.

**Scale-free restatement, used throughout.** A partition of $T_{a_0}$ into $N$ sets of diameter
$\le1$ scales to a partition of $T_a$, $a<a_0$, into $N$ sets of diameter $a/a_0<1$. So
$$T_{a_0}=\bigsqcup_{i=1}^{N}(\text{diam}\le1)\ \Longrightarrow\ N^*(a)\le N \ \text{ for all } a<a_0
\ \Longrightarrow\ a_{N+1}\ \ge\ a_0 .$$
Erdős–Oler at $k=7$ ($n=27$, $a<6$) follows from **26 pieces at $a_0=6$**.

## 1. What was already known here, and what it cost

`eo-oler-equality` §8 measured 34 (hexagon tiling) and 36 (uniform $m^2$ sub-triangles) against a
requirement of 26, with an isodiametric floor of 20. `eo-small-cases` §4.1 read the $m^2$ scheme's
overshoot, $(k-1)^2-(\Delta(k)-2)=\tfrac{(k-2)(k-3)}2$, as the size of the gap: **10 at $k=7$.**

That number is an artefact of the scheme. The $m^2$ subdivision is the *right* scheme only while
$a\le3$; past that it is beaten by the hexagonal one, and the real gap is 2 (§5).

## 2. The lattice lemma — the construction that gives 28

> **Lemma L.** Let $p\ge2$ and $a\le p\sqrt3/2$. Then $T_a$ is the union of
> $\Delta(p)=\tfrac{p(p+1)}2$ convex sets with pairwise disjoint interiors, each of diameter
> $\le 1$.

**The construction.** Put $g=\sqrt3/2$ and place the $\Delta(p)$ sites
$$P_{ij}\;=\;\bigl(u_0+g\,i,\;u_0+g\,j\bigr)_{(u,v)},\qquad i,j\ge0,\ i+j\le p-1,
\qquad u_0=\tfrac{a-g(p-1)}3,$$
i.e. the triangular lattice of spacing $\sqrt3/2$, arranged in a $\Delta(p)$ triangle and
**centred** in $T_a$. The cells are the Voronoi cells of these $\Delta(p)$ sites, clipped to
$T_a$. They are convex, have pairwise disjoint interiors and cover $T_a$ by construction; the
content of the lemma is that **every** cell has diameter $\le1$.

**Why $p\sqrt3/2$ is exactly the right threshold — the corner is what binds.** An interior cell is
the Voronoi cell of the full lattice: a regular hexagon of circumradius $g/\sqrt3=1/2$, i.e.
diameter exactly 1, for any $a$. The cells that grow with $a$ are the boundary ones, and the
extreme case is a corner: the corner of $T_a$ must lie inside the corner site's hexagon. With the
centred array the corner-to-site distance is $\sqrt3\,u_0$, the corner direction is a hexagon
*vertex* direction, so the reach available is the circumradius $1/2$:
$$\sqrt3\,u_0\le\tfrac12 \iff u_0\le\tfrac1{2\sqrt3} \iff a\le (p-1)\tfrac{\sqrt3}2+\tfrac{\sqrt3}2
=p\tfrac{\sqrt3}2 .$$
At $a=p\sqrt3/2$ the corner sits **exactly** on a hexagon vertex; that is why the verified maximum
squared diameter is exactly 1 and not less, for every $p$.

**Status.** Machine-checked in exact $\mathbb{Q}(\sqrt3)$ arithmetic for $p=2,\dots,10$: each cell
convex and inside $T_a$, every squared diameter $\le1$ (attained $=1$), pairwise interiors
separated, and the cell areas summing **exactly** to the area of $T_a$. That last check plus
disjointness is what rules out a missed sliver: finitely many closed sets whose union has full
measure leave a relatively open null set, i.e. nothing. The general $p$ is a `sketch` — the
argument above is complete in outline but the "no other cell is worse than the corner cell" step
is verified case-by-case, not proved.

| $p$ | 2 | 3 | 4 | 5 | 6 | **7** | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cells $\Delta(p)$ | 3 | 6 | 10 | 15 | 21 | **28** | 36 | 45 | 55 |
| valid for $a\le p\sqrt3/2$ | 1.732 | 2.598 | 3.464 | 4.330 | 5.196 | **6.062** | 6.928 | 7.794 | 8.660 |

The $p=7$ row is the one that matters: **$T_6$ splits into 28 convex cells of diameter $\le1$**,
and the scheme survives up to $a=7\sqrt3/2=6.0622$ (it fails at $a=6.07$; `run.py` checks both).

## 3. The search: 28 is where it stops

Beyond the lattice I searched the much larger family of **power diagrams** (weighted Voronoi):
$N$ sites and $N$ weights, cells $\{x:\ |x-p_i|^2-w_i\le|x-p_j|^2-w_j\}$ clipped to $T_6$ — still
convex, still automatically a partition, so any local optimum is directly certifiable. Objective:
minimise the largest cell diameter $D(N)$, by annealed coordinate descent on a $p$-norm of the
cell diameters, from honeycomb, greedy-removal and random starts (floats; ~35 min CPU).

Calibration first, on cases with known answers: $a=2$, $N=4$ → $1.0004$ (truth 1, the medial
subdivision); $a=3$, $N=9$ → $1.00013$ (truth 1). So the optimiser recovers known optima to
$\sim0.05\%$, and its numbers below are pessimistic by about that much.

| $N$ | best $D(N)$ at $a=6$ | largest $a$ that $N$ pieces cover | **exactly certified** $a$ |
|---:|---:|---:|---|
| 28 | 0.98412 | 6.0968 | $762/125=6.096$ (`cert28opt.json`); lattice: $7\sqrt3/2$ |
| 27 | 1.03061 | 5.8218 | $2901/500=5.802$ (`cert27.json`) |
| **26** | **1.03825** | **5.7793** | $2889/500=5.778$ (`cert26.json`) |
| 25 | 1.06869 | 5.6141 | — |
| 24 | 1.07952 | 5.5580 | — |

Read the last column as lower bounds on $a_n$, and compare with Oler:

| | 26 pieces | 27 pieces | 28 pieces |
|---|---|---|---|
| gives | $a_{27}\ge5.778$ | $a_{28}\ge5.802$ | $a_{29}\ge6.096$ |
| Oler gives | $a_{27}\ge5.8655$ | $a_{28}\ge6$ | $a_{29}\ge6.1322$ |
| EO($7$) needs | $a_{27}\ge6$ | — | — |

**Every row is weaker than Oler.** That is the honest summary of the route as I can execute it:
at the one $n$ that matters it is $0.088$ behind Oler in side length and $0.222$ behind the
target. The jump between $N=28$ ($D=0.984$) and $N=27$ ($D=1.031$) is a cliff, and $N=26$ then
costs almost nothing more ($1.038$) — the 27-cell optima are 26-cell optima with one nearly
redundant cell (the best 27-cell solution has a cell of area $0.259$ against a mean of $0.577$).
The barrier is at 28, not at 26.

## 4. Where the waste is — measured, not guessed

Cell areas of the optimised 28-cell partition, rescaled to diameter exactly 1, against the
per-piece ceilings:

| cells | count | measured area | ceiling | what the ceiling is |
|---|---:|---|---|---|
| interior | 10 | 0.637 – 0.647 | $3\sqrt3/8=0.6495$ | regular hexagon of diameter 1 — the densest *tiling* piece |
| edge | 15 | 0.536 – 0.563 | $0.6095$ | best pentagon with a flat side on $\partial T$ (below) |
| corner | 3 | 0.463 – 0.469 | $\pi/6=0.5236$ | **proved**: the piece containing a $60°$ corner lies in the unit sector there |

The interior is **at** the hexagonal ceiling — there is nothing to win there. The budget arithmetic:

- $28\times0.6495-15.5885 = 2.598$ — the 28-cell scheme wastes exactly **4 cells' worth** of area.
- $26\times0.6495-15.5885 = 1.299$ — a 26-cell scheme may waste at most **2 cells' worth**.

So the whole question is whether boundary waste can be halved. The *individual* ceilings say yes:
an edge piece with a flat side of length $s$ on $\partial T$, vertical sides and a peak, has
$$\text{area}=\tfrac{s}{2}\bigl(\sqrt{1-s^2}+\sqrt{1-s^2/4}\bigr),\qquad\max = 0.6095 \text{ at } s\approx0.83,$$
against the $0.5413$ that a diameter-1 hexagon cut at its lower vertices delivers. Fifteen edge
cells at $0.6095$ and three corners at $\pi/6$ leave $15.5885-9.14-1.57=4.88$ for the interior, i.e.
$7.5$ hexagons: $3+15+8=26$ **on paper**.

**Why the paper number is not reachable — the deep-notch boundary taxes every row above it.**
Raising an edge cell's peak from $0.75$ to $0.909$ (its individual optimum, at $s=0.835$) forces
the row above to sit only $t=0.486$ higher, since the peak height is $t/2+s^2/8t$. That pins the
whole stack into an alternating-gap regime: for the staggered-row family with period $s$ and row
gaps $t,t'$,
$$A-B=\tfrac{t}{2}+\tfrac{s^2}{8t}+\tfrac{t'}{2}+\tfrac{s^2}{8t'}\le1,\qquad
\text{area}=\tfrac{s}{2}\bigl[(A-B)+(U-L)\bigr],$$
and the recursion settles immediately into gaps alternating $0.486,\,0.977$ with **every** cell at
area $0.6109$ — better than the $0.5413$ of a cut hexagon, but $0.039$ *below* the regular hexagon
at every row, for ever. Cumulatively, per column of cells:

| rows | 1 | 2 | 3 | 4 | 7 |
|---|---:|---:|---:|---:|---:|
| plain hexagon lattice, cut at $\partial T$ | 0.541 | 1.191 | 1.840 | 2.490 | 4.438 |
| deep-notch stack | **0.609** | **1.220** | 1.831 | 2.442 | 4.274 |

The deep-notch boundary wins for two rows and then loses, and $T_6$ is about seven rows deep. So
the gain has to be **localised** to the first row or two and relaxed back to the regular lattice
inland — and the relaxation is not free either, because the period has to migrate from $0.835$ to
$0.866$ through rows that are neither. The measured $0.55$ for edge cells is exactly that
compromise: it recovers about half of the four cells of waste, which is why the optimum sits at 28
and not at 26.

## 5. The deficit is 2 — and $k=7$ is the last case where it is even that small

Combining Lemma L with the $m^2$ subdivision, the best construction known here at $a=k-1$ is
$\min\{\Delta(\lceil 2(k-1)/\sqrt3\rceil),\,(k-1)^2\}$, against a requirement of $\Delta(k)-2$:

| $k$ | 3 | 4 | 5 | 6 | **7** | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|
| needed $\Delta(k)-2$ | 4 | 8 | 13 | 19 | **26** | 34 | 43 |
| $m^2$ subdivision | **4** | **9** | 16 | 25 | 36 | 49 | 64 |
| lattice, $\Delta(\lceil1.1547(k-1)\rceil)$ | 6 | 10 | **15** | **21** | **28** | **45** | **55** |
| best deficit | **0** | 1 | 2 | 2 | **2** | 11 | 12 |

Three things follow, and they replace §4.1 of `eo-small-cases` for $k\ge5$:

1. **The gap at $k=7$ is 2, not 10.** The $(k-2)(k-3)/2$ overshoot is a property of the uniform
   sub-triangle scheme, which stops being the right scheme at $a>3$.
2. **$k=8$ is much worse than $k=7$, by a hair.** $1.1547\times7=8.083$ just clears 8, so the
   lattice jumps from $\Delta(8)=36$ to $\Delta(9)=45$ and the deficit goes 2 → 11. $k=7$ is the
   last case where the covering route is anywhere near.
3. **There is a ceiling that kills the route outright for $k\ge10$.** If the densest partition of
   the plane into diameter-1 sets is the hexagon tiling ($3\sqrt3/8$ per piece — *this is the
   natural conjecture, not something I can cite or prove*), then any covering of $T_a$ needs
   $\ge \tfrac{2}{3}a^2$ pieces, and
   $$\tfrac23(k-1)^2\le\Delta(k)-2 \iff k^2-11k+16\le0 \iff k\le 9.32 .$$
   At $k=7$ that ceiling is 24, so the **entire** budget for boundary and corner waste, over a
   perimeter of 18 and three corners, is 2 pieces.

**Small rigorous by-product, for W2's lane not mine.** The three corner pieces are distinct (the
corners are $6$ apart) and each lies in a unit $60°$ sector, so has area $\le\pi/6$; the rest is
bounded isodiametrically by $\pi/4$. Hence
$N^*(6^-)\ \ge\ 3+\lceil(9\sqrt3-\pi/2)/(\pi/4)\rceil = 3+18 = 21$, improving the recorded floor
of 20. I record it and do not develop it — lower bounds are W2's lane.

## 6. By-product: covering bounds that beat Oler for $n=\Delta(p)+1$, $p\le6$

Lemma L gives $a_{\Delta(p)+1}\ge p\sqrt3/2$ directly. Oler gives
$a_n\ge(\sqrt{8n+1}-3)/2$, which at $n=\Delta(p)+1$ is $\approx p-1+\tfrac1{2p+1}$, so the lattice
bound wins exactly while $p\le6$:

| $n$ | 4 | 7 | 11 | 16 | 22 | 29 |
|---|---:|---:|---:|---:|---:|---:|
| lattice bound $p\sqrt3/2$ | **1.7321** | **2.5981** | **3.4641** | **4.3301** | **5.1962** | 6.0622 |
| Oler | 1.3723 | 2.2749 | 3.2170 | 4.1789 | 5.1521 | **6.1322** |
| true value | $\sqrt3$ (tight) | $1{+}\sqrt3=2.7321$ | $2{+}\tfrac{2\sqrt6}3=3.6330$ | $\le4.6304$ | $\le5.6484$ | — |

At $n=4$ the bound is **tight**: three cells of diameter $\le1$ cover $T_{\sqrt3}$, so
$a_4\ge\sqrt3$, and the lattice configuration attains it — a three-line reproof of $s(4)=4\sqrt3$
in the same style as the $k=3$ medial argument. For $n=16$ and $n=22$ these are the best lower
bounds in this repo (the true values are open), but **novelty is UNVERIFIED**: covering arguments
of exactly this shape are standard in the discrete-geometry literature and scholarly hosts are
blocked at this session's egress, so assume they are known. The $n=16$ and $n=22$ rows are also
cross-checked against explicit packings found here ($a_{16}\le4.6304$, $a_{22}\le5.6484$, with the
same optimiser reproducing the *known exact* $a_7$ and $a_{11}$ to $5\times10^{-5}$) — no
contradiction, which is the check I would want to see before believing a bound of my own making.

## 7. Kill-criterion, honestly

Neither K1 nor K2 fired.

- **K1** was "stop at $\ge30$ with a structural reason". I reached 28, so K1 does not apply.
- **K2** was "stop if the interior is at the hexagonal ceiling and the residual gap exceeds the
  removable boundary waste". The interior *is* at the ceiling (§4). The residual gap is 2 cells
  and the boundary waste is 4 cells, of which the individual ceilings say $\sim2.5$ is removable —
  so K2 does not *strictly* fire either. What kills the attempt is §4's second paragraph: the
  removable part is not removable **jointly**, because the second row pays back what the first row
  gains.
- I stopped on the **compute budget** (`RULES.md` §6.6), with the best scheme at 28 and every
  attempt at 26 landing 3.8 % short in diameter.

**What would move it**, in the order I would try next: (i) optimise the planar subdivision's
*vertices* directly under convexity constraints, which strictly contains the power-diagram family
used here; (ii) allow non-convex pieces, where the per-piece diameter ceiling is unchanged but the
interlocking is freer; (iii) settle whether $3\sqrt3/8$ really is the ceiling for plane partitions
into diameter-1 sets — if it is, §5's inequality closes $k\ge10$ permanently and turns this from a
search into a finite question.

## 8. Reproducing

```
python3 experiments/packing-eo-covering/run.py
```

Standard library only; exact $\mathbb{Q}(\sqrt3)$ and $\mathbb{Q}$ arithmetic with an exact sign
test; no seeds, no tolerances, no float in any decision. 22 checks, all passing; exits non-zero on
any failure. The float search that *found* the certificates is `worker.py` / `greedy.py` and is
not part of any claim.

## 9. What to review hardest

- **The exact verifier `exact.py`.** Everything rests on it. The three checks that matter are the
  squared-diameter comparison in $\mathbb{Q}(\sqrt3)$ (`Q3.sign`, the opposite-signs branch), the
  Sutherland–Hodgman clip on exact coordinates, and the claim that *convex + pairwise-separated +
  areas summing exactly to $\operatorname{area}(T_a)$* implies a covering with no missed sliver.
  Problem [`RULES.md`](../../RULES.md) §3 asks for a **second, independently written checker** —
  this attack has one implementation, so nothing here is assumable yet.
- **§2's threshold $a\le p\sqrt3/2$ and the claim that the corner cell is the extremal one.** It is
  verified per $p$, not proved. If some non-corner cell were worse for large $p$, the table's later
  rows would be wrong (the $k=7$ row would not be, since $p=7$ is checked directly).
- **§6's novelty disclaimer.** If any of those bounds is actually new, that is a claim to make
  carefully and with a literature search this session could not do.
- **§5.3's ceiling.** I have asserted, without citation or proof, that $3\sqrt3/8$ is the maximum
  density of a plane partition into diameter-1 sets. Everything in §5 that depends on it is
  conditional, and the $k\ge10$ conclusion is *only* as good as that assertion.
