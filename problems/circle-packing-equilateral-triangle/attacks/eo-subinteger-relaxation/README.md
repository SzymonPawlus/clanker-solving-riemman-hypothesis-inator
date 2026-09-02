# Attack: refining the corner-occupancy relaxation to sub-integer thresholds

**Claim type (problem [`../../RULES.md`](../../RULES.md) §1 asks for this first): optimality /
lower bound, and only for $n = 5$ and $n = 9$, both of which are already `cited` as proven in
[`../../README.md`](../../README.md). No construction is claimed, no bound is claimed for any
open $n$, and Erdős–Oler at $k \ge 5$ is untouched.** What is new here is a *method* measurement:
the predecessor attack's own named weakness — that its cells were indexed by **integer** floors of
the corner coordinates — is **real, not a red herring**, and refining past it turns a break-even
relaxation into a decisive one at $k = 4$ and then fails at $k = 5$.

- Refines: [`../eo-corner-squeeze/`](../eo-corner-squeeze/) §5 (integer-threshold corner
  occupancy, feasible at $k = 4,5,6,7$), whose §7 names exactly this gap:
  *"the thresholds are integers, and a finer partition … could in principle be infeasible where
  mine is feasible."*
- Code: [`experiments/packing-eo-subinteger/`](../../../../experiments/packing-eo-subinteger/) —
  Python standard library only, exact rational arithmetic in every decision.
- Kill-criterion, written before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md).
- Author: `claude` (Claude Opus 5), worker W4, 2026-08-21.

| What | Status |
|---|---|
| §3 Lemma D (disk/circumradius capacity bound) and the star-cover bound | `sketch` — mine, three lines each, exactly checked |
| §5 **Erdős–Oler at $k = 3$ and $k = 4$ by a four-piece cover**, uniform in $a$ | `sketch` — mine; the *statements* are `cited` (Melissen 1993), the proofs are not |
| §4 LP values of the refined relaxation at $k = 3,4,5,6$ | `numerical` — exact certificates where the verdict is "decided" |
| §6 Why the method stops between $k = 4$ and $k = 5$ (efficiency ceiling) | `sketch` — mine |
| §2 re-verification of Lemma P of `../eo-corner-squeeze/` §3 | `sketch` — his, re-derived here; same-family agreement grants nothing |
| Oler's inequality; the $d(n)$ table | `cited` — [`../../README.md`](../../README.md) |

---

## 0. Kill-criterion outcome, stated up front

> **K1 (primary).** *"Run the refined relaxation at $k = 4, 5, 6$, where Erdős–Oler is
> `cited`-true. If the refined LP optimum is still $\ge T(k)-1$ at any of those $k$, the refined
> family is still too weak; report that and stop."*
>
> **Split verdict, and the split is the finding.**
>
> * At **$k = 4$** the refinement **decides** the case: LP $= 8 < 9$, where the predecessor's
>   integer-threshold system was feasible at 9. Re-run here with integer thresholds it is again
>   exactly 9, so this is a like-for-like comparison and **the coarseness gap its author named is
>   real**. The certificate is a four-piece cover valid for *every* $a < 3$, not just the
>   convenient one, and it contains no $d(n)$ value at all.
> * At **$k = 5$ and $k = 6$** the refinement is back to break-even: LP $= T(k)-1 = \lfloor
>   \mathrm{Oler}(a)\rfloor$, closing zero of the missing point. **K1 is met at $k = 5$.**
>
> **$k = 7$ is therefore not a decision procedure here.** A method that cannot see the
> contradiction at $k = 5$, where one certainly exists, cannot supply one at $k = 7$. One
> evaluation was run only to record the number: at $a = 5.99$ on the $a/6$ grid the LP returns
> **27**, i.e. exactly $\lfloor\mathrm{Oler}(a)\rfloor = T(7)-1$ — break-even, closing zero of the
> missing point, exactly as §6 predicts in advance. **That number decides nothing** and is not
> reported as if it did.

**Nothing here is circular.** The single binding capacity at $k = 4$ comes from a disk-packing
pigeonhole (§3, Lemma D) and a diameter test. No entry of the $d(n)$ table enters any capacity in
the primary run — the guard demanded by `FINDINGS.md` 2026-08-21 ("A `cited` input contained the
conclusion"), whose failure mode is exactly what this lane was warned about.

**A bug my own control caught, recorded per `RULES.md` §0.** The first capacity function returned
1 for *degenerate* regions — but a corner box can degenerate to a **segment**, and a segment of
length $\ell$ holds $1+\lfloor\ell\rfloor$ separated points, not one. Control K3 found it by
counting the $T(7)$ lattice against every box: 198 violations at $k = 7$, all on segments. The
capacities that a wrong value would have made *too small* are exactly the ones that would have
manufactured a false infeasibility. Post-fix, K3 passes with zero violations everywhere.

---

## 1. Setup, and the normalisation assertion

**Oler normalisation throughout: minimum separation 1, containing equilateral triangle $T$ of side
$a$.** The repo's certificates use separation 2 and side $d = 2a$; `controls.py` halves every
coordinate on load and re-checks separation before anything else runs. (Three separate workers
have slipped on this in one day; this is the assertion, not an inherited assumption.)

Corner coordinates: with $A = (0,0)$, $B = (a,0)$, $C = (a/2, a\sqrt3/2)$,

$$u_A = x + \tfrac{y}{\sqrt3},\qquad u_B = (a-x)+\tfrac{y}{\sqrt3},\qquad u_C = a - \tfrac{2y}{\sqrt3},
\qquad u_A+u_B+u_C = 2a,$$

so $\Delta_V(t) = \{u_V \le t\}$ is the closed corner triangle of side $t$ at $V$. Erdős–Oler at
level $k$: $n = T(k)-1$ points at separation $\ge 1$ force $a \ge k-1$. Oler's inequality alone
gives $\lfloor \mathrm{Oler}(a)\rfloor = T(k)-1$ throughout $a \in (a_0(k), k-1)$ with
$a_0(k) = \tfrac{-3+\sqrt{8T(k)-7}}{2}$ — **the gain any argument must produce is exactly one
point.**

**Two identities make every computation exact rational arithmetic with no $\sqrt3$ anywhere**
(both derived and checked in `geom.py`):

1. In the chart $(u_A, u_C)$ the squared distance is
   $d^2 = \Delta u_A^2 + \Delta u_A \Delta u_C + \Delta u_C^2$.
2. The map $(u_A,u_C)\mapsto(x,y)$ has Jacobian $\sqrt3/2$, so Oler's area term
   $\tfrac{2}{\sqrt3}A$ is **exactly the shoelace area in the $(u_A,u_C)$ chart**; and every edge
   of a corner-coordinate box has one $u_V$ constant, for which $d^2$ collapses to a single squared
   coordinate difference, so **every such edge length is rational**. Hence
   $\mathrm{Oler}(R) = \mathrm{shoelace}_u(R) + \tfrac12\mathrm{perim}_u(R) + 1$ exactly.
   Check: for $T$ itself this returns $a^2/2 + 3a/2 + 1$.

---

## 2. What is refined, and against what baseline

The predecessor indexed cells by $(\lfloor u_A\rfloor, \lfloor u_B\rfloor, \lfloor u_C\rfloor)$ —
thresholds at the **integers** $1,\dots,k-2$. Here thresholds are at multiples of $a/M$ for
$M > k-1$, so every threshold is a genuine sub-integer cut, and capacities are **recomputed from
scratch for the finer cells**, never inherited from a coarser one.

The object solved is the *fractional cover* LP, which is the strongest bound a region-capacity
family can give:

$$\text{primal}\quad \max \sum_c z_c \ \text{ s.t. } z \ge 0,\ \sum_{c\subseteq R} z_c \le
\mathrm{cap}(R)\ \forall R \qquad\Longleftrightarrow\qquad
\text{dual}\quad \min \sum_R \mathrm{cap}(R)\,y_R \ \text{ s.t. } \textstyle\sum_{R \ni c} y_R \ge 1 .$$

Its value is the best upper bound on the number of separation-1 points in $T_a$ obtainable from
these regions. **Any dual-feasible $y$ is by itself a rigorous proof** (weak duality), so a proof
needs an exactly-verified fractional cover and never needs the LP to be optimal — the search runs
in floats and every conclusion is re-derived in exact rationals.

Two soundness points that cost me a wrong run each:

* **The per-cell constraints may never be dropped.** An early filter discarded every box whose
  capacity was not below its cell count, which removed the singleton constraints and left the LP
  variables unbounded. The correct vacuity test is $\mathrm{cap}(R) \ge \sum_{c\subseteq R}\mathrm{cap}(c)$.
* Covering LPs with an all-ones right-hand side are massively degenerate; the right-hand side is
  perturbed *upward* by $10^{-9}i$, which can only make a cover harder, so a cover found is still
  exactly feasible for the true constraints.

**Lemma P re-verified** (`../eo-corner-squeeze/` §3, `sketch`, therefore not assumable —
`RULES.md` §3). I re-derived it independently: the region $\{u_V \ge k-2\}$ is a trapezoid of
vertical extent $w = (a-k+2)\tfrac{\sqrt3}{2} < \tfrac{\sqrt3}{2}$, two points in it project
horizontally at least $\sqrt{1-w^2}$ apart into an interval of length $\le a$, so
$m \le 1 + a/\sqrt{1-w^2}$, and $a^2 + 3(k-1)^2(a-k+2)^2 < 4(k-1)^2$ for $a < k-1$ with **equality
exactly at $a = k-1$**. Verified in exact rational arithmetic on a 1000-point grid of $a$ for
$k = 3..12$, plus the endpoint identity (`controls.py`, K3(c)). It is correct, and its
break-even-ness at $a = k-1$ — the author's own reading — is confirmed exactly.

---

## 3. The capacity toolkit — where all the strength lives

For a region $R$, $\mathrm{cap}(R)$ is the maximum number of pairwise-separated points in $R$.
Every bound below is geometric; **no $d(n)$ from the literature table is used anywhere**
(kill-criterion K2). `cap(R) <= floor(Oler(R))` is usually strict and increasingly so as $R$
shrinks, and that strictness is the entire budget.

| bound | statement | cost |
|---|---|---|
| **diameter** | $\mathrm{diam}(R) < 1 \Rightarrow \mathrm{cap} = 1$ | exact, instant |
| **Lemma D (disk)** | $R$ inside a closed disk of radius $\rho$ with $\rho < \tfrac{1}{2\sin(\pi/m)}$, $2 \le m \le 6$ $\Rightarrow \mathrm{cap} \le m-1$; in particular **circumradius $< 1 \Rightarrow \mathrm{cap} \le 5$** | exact minimum enclosing circle over $\le 6$ vertices |
| **star cover** | the $m$ pieces $\mathrm{conv}(g, m_{i-1}, p_i, m_i)$ ($g$ = vertex centroid, $m_i$ = edge midpoints) cover $R$; if each has diameter $< 1$ then $\mathrm{cap}\le m$ | exact |
| **subdivision / independent set** | cover $R$ by grid cells of diameter $<1$; occupied cells form an independent set of the "max mutual distance $< 1$" graph, so $\mathrm{cap} \le$ MIS (computed exactly, clique-cover bound) | exact, seconds |
| **Oler** | $\mathrm{cap} \le \lfloor \tfrac{2}{\sqrt3}A + \tfrac{P}{2}+1\rfloor$ | exact (§1) |
| **segment** | a degenerate box of length $\ell$: $\mathrm{cap} = 1+\lfloor \ell\rfloor$ | exact |

**Lemma D, proof (mine, elementary).** Let $2 \le m \le 6$ points be pairwise $\ge 1$ apart inside
a closed disk of radius $\rho$ about $O$. Sort them by polar angle about $O$; some angular gap
satisfies $\Delta \le 2\pi/m$. For that pair, with $c = \cos(2\pi/m)$ and radii $r_i, r_j \le \rho$,
$$|P_iP_j|^2 = r_i^2 - 2c\,r_ir_j + r_j^2 \;\le\; \rho^2\max(1, 2-2c) \;=\; \rho^2(2-2c),$$
so $1 \le 2\rho\sin(\pi/m)$. Contrapositive gives the table. It is **tight**: the regular $m$-gon
on the boundary circle attains it. The case $m = 6$ reads: *a set of circumradius $< 1$ holds at
most 5 separated points* — and that single line is what decides $k = 4$. $\square$

**Validation against known capacities** (`geom.py`, equilateral triangle of side $t$, truth from
the `cited` $d(n)$ table — used **only to check the tool, never inside it**):

| $t$ | 0.5 | 0.99 | 1.25 | 1.5 | 1.7 | 1.73 | 1.8 | 1.99 | 2 | 2.5 | 2.9 | 3 | 3.5 | 3.99 | 4 |
|---|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| computed | 1 | 1 | 3 | 3 | 3 | 3 | 4 | 4 | 6 | 7 | 9 | 10 | 12 | 14 | 15 |
| true | 1 | 1 | 3 | 3 | 3 | 3 | 4 | 4 | 6 | 6 | 8 | 10 | 10 | 13 | 15 |

Exact at every integer $t$ and everywhere below $t = 2$; slack $1$–$2$ in the middle of the larger
ranges, which is where the discretisation cost bites. The two entries that matter for §5 are
$t < 1 \Rightarrow 1$ and the regular hexagon of side $<1 \Rightarrow 5$, both exact.

**K3 controls pass** (`controls.py`): the repo's exact certificates and the triangular lattices
$T(k)$ for $k \le 7$ are loaded, halved, re-checked for separation, and counted against **every**
corner box on the $a/M$ grids for $M \le 4$ — 4472 boxes per configuration, **zero capacity
violations** after the segment fix. A capacity that were too small would show up here as a real
configuration exceeding it.

---

## 4. Results

$n = T(k)-1$, $a = (k-1)-10^{-2}$ unless stated, thresholds at multiples of $a/M$.
"decides" means the LP optimum is $\le n-1$, i.e. the family proves Erdős–Oler at that level.

| $k$ | $n$ | $\lfloor\mathrm{Oler}(a)\rfloor$ | integer thresholds (predecessor) | $M=3$ | $M=4$ | $M=5$ | $M=6$ | $M=8$ | $M=9$ | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 3 | 5 | 5 | **4** | 4 | 4 | – | 4 | – | – | **decides** |
| 4 | 9 | 9 | 9 | **8** | 9 | – | **8** | 9 | – | **decides** |
| 5 | 14 | 14 | 14 | – | 14 | 14 | 14 | – | 14 | break-even |
| 6 | 20 | 20 | 20 | – | – | 20 | 20 | – | – | break-even |
| 7 | 27 | 27 | – | – | – | – | 27 | – | – | break-even (decides nothing — §0) |

The "integer thresholds" column is the predecessor's family $\{0,1,\dots,k-2,a\}$ **re-run through
this same code**, not quoted from its write-up, so the comparison is like-for-like: it returns
$4, 9, 14, 20$ at $k = 3,4,5,6$ (7/16/28/43 cells and 11/66/203/482 binding boxes) and is
unchanged by taking $a = (k-1)-10^{-3}$ instead. (Note it does
decide $k=3$ — there the whole triangle alone subdivides into four pieces of side $a/2 < 1$, and no
sub-integer threshold is needed. $k = 4$ is where the two families separate.)

(Cell/box counts, build times and the exact certificates are in
[`out/`](../../../../experiments/packing-eo-subinteger/out/); $k=5$, $M=9$ is 81 cells and 1918
binding boxes after dominance pruning, and still returns exactly $\lfloor\mathrm{Oler}\rfloor$.)

Read the $k = 4$ row across: **integer thresholds 9, sub-integer thresholds 8.** That is the entire
question this attack was set, answered in one row. Note also that $M$ must be *right*, not merely
large: $M = 8$ gives 9 because the $a/8$ grid does not contain the $a/3$ cut that $M = 3$ and
$M = 6$ do.

---

## 5. The certificate at $k = 4$, and why it is uniform in $a$

The LP's dual solution at $k = 4$ is a four-piece cover with weight 1 on each piece, and it is
short enough to state without any computation at all. It proves Erdős–Oler at $k = 4$ — equivalently
$d(9) = 6$, $s(9) = 6+2\sqrt3$ — for **every** $a < 3$ at once, which is what the conjecture
asks (kill-criterion K4); a verdict at one convenient $a$ would decide nothing.

> **Proposition (mine, `sketch`).** Nine points at mutual distance $\ge 1$ do not fit in a closed
> equilateral triangle of side $a < 3$.
>
> **Proof.** Put $t = a/3 < 1$ and cover $T_a$ by the three corner triangles $\Delta_V(t)$ and
> $H = \{p : u_A, u_B, u_C \ge t\}$: a point outside all three corner triangles has $u_V > t$ for
> every $V$, so it lies in $H$. Each $\Delta_V(t)$ is an equilateral triangle of side $t < 1$,
> hence of diameter $<1$, hence contains at most **1** point. Cutting corners of side $t$ off a
> triangle of side $3t$ leaves sides $t$ (the cuts) and $3t-2t = t$ (the remnants), so $H$ is a
> **regular hexagon of side $t$**, whose circumradius is $t < 1$; by Lemma D it contains at most
> **5** points. Total $\le 3\cdot 1 + 5 = 8 < 9$. $\blacksquare$

Every quantity in it is a strict inequality in $a$, so it does not degrade as $a \to 3^-$ — and at
$a = 3$ it correctly says nothing (the corner triangles then have side 1 and hold 3 points each,
$H$ has circumradius 1 and holds 6, total 15), which is as it must be, since 10 points do fit at
$a = 3$.

**Where the sub-integer threshold is load-bearing.** The cut is at $t = a/3 < 1$. At the nearest
*integer* threshold, $t = 1$, both capacities jump — $\mathrm{cap}(\Delta_V(1)) = 3$ and the
circumradius of $H$ becomes exactly 1, so Lemma D gives 6 — and the same cover yields
$3\cdot3+6 = 15$, useless. The predecessor's family could not express $t = a/3$, and that, and
only that, is why it was stuck at 9.

The same LP at $k = 3$ certifies 4 points by the plain subdivision of $T_a$ ($a<2$) into four
triangles of side $a/2 < 1$ — the cheapest possible instance of the same mechanism, and the
control (K3(b)) that the pipeline can prove anything at all.

---

## 6. Why it stops between $k = 4$ and $k = 5$ — an efficiency ceiling

This is the structural reading of the $k=5$ break-even, and it predicts the failure before it is
computed. For an exact partition of $T_a$ into corner boxes $R_i$ with capacities $c_i$, write
$e_i = \mathrm{area}(R_i)/c_i$. Since $\sum_i \mathrm{area}(R_i) = \mathrm{area}(T_a)$, a partition
certifies $n-1$ points only if its **average efficiency** reaches

$$e_{\text{required}}(k) \;=\; \frac{\mathrm{area}(T_{k-1})}{T(k)-2} \;=\;
\frac{\sqrt3\,(k-1)^2/4}{T(k)-2}
\;=\; 0.433,\ 0.487,\ 0.533,\ 0.570,\ 0.600 \quad (k = 3,4,5,6,7).$$

Against that, the efficiencies actually available from the toolkit of §3 are bounded:

| piece | cap | area | $e$ |
|---|---:|---:|---:|
| triangle of side $<1$ | 1 | $\le 0.433$ | $\le 0.433$ |
| corner-box of diameter $<1$, best case (regular hexagon of diameter 1) | 1 | $0.6495$ | $0.6495$ |
| regular hexagon of side $<1$ (Lemma D) | 5 | $\le 2.598$ | $\le 0.5196$ |
| hexagon of side just $\ge 1$ | 7 | $2.598$ | $0.371$ |

and the honeycomb that would realise $e = 0.6495$ everywhere does not tile: three families of
parallel lines with generic offsets produce **two small triangles per hexagon**, and the periodic
pattern (1 hexagon of cap 5 plus 2 triangles of cap 1, area $3.464s^2$, capacity 7) has
$e = 0.495$. So the achievable average sits at roughly $0.49$–$0.52$:

* $k = 3$ needs $0.433$ — met by plain triangles;
* $k = 4$ needs $0.487$ — met, at $0.487$ exactly, by the §5 cover (three triangles at $0.433$
  plus one hexagon at $0.520$);
* $k = 5$ needs $0.533$ — **above the ceiling**, and the LP duly returns break-even;
* $k = 7$ would need $0.600$.

Turning that into a prediction and checking it: the best partition bound is about
$\lceil \mathrm{area}(T_{k-1})/0.495\rceil$, and the LP can never exceed
$\lfloor\mathrm{Oler}(a)\rfloor$ because $T_a$ is itself a box, so the LP should be the smaller
of the two. It is, at every level computed:

| $k$ | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|
| partition estimate $\lceil\mathrm{area}/0.495\rceil$ | 4 | 8 | 14 | 22 | 32 |
| $\lfloor\mathrm{Oler}(a)\rfloor = T(k)-1$ | 5 | 9 | 14 | 20 | 27 |
| predicted LP $=\min$ | 4 | 8 | 14 | 20 | 27 |
| **LP actually computed** | **4** | **8** | **14** | **20** | **27** |

So the mechanism is not merely consistent with the numbers, it reproduces them. **From $k = 6$
onward the best partition is worse than doing nothing at all** — plain Oler on the undivided
triangle beats every cover this family can build — and the margin grows quadratically.

The requirement climbs because Oler's inequality is asymptotically area-limited while the
capacity-strictness that beats it lives at scales below 1 and does not scale up. This is the same
"the gap widens quadratically in $k$" that [`../eo-corner-squeeze/`](../eo-corner-squeeze/) §4
found from the opposite direction, now with an explicit mechanism and an explicit crossing point:
**between $k = 4$ and $k = 5$.**

---

## 7. How much of the one point is closed, on the $\varepsilon$-scale

Measured on the side length, which is the scale on which the deficit is comparable across $k$.
Oler alone forces $a \ge a_0(k) = \tfrac{-3+\sqrt{8T(k)-7}}{2}$; the truth is $a \ge k-1$; the
refinement forces $a \ge a^{*}(k)$, found by bisection (`astar.py`).

| $k$ | $a_0(k)$ (Oler) | truth $k-1$ | gap | $a^{*}(k)$ (this attack) | fraction of the gap closed |
|---:|---:|---:|---:|---:|---:|
| 3 | 1.70156 | 2 | 0.29844 | $2$ | **1.000** |
| 4 | 2.77200 | 3 | 0.22800 | $3$ | **1.000** |
| 5 | 3.81507 | 4 | 0.18493 | $3.815\ldots = a_0(5)$ | **0.000** |
| 6 | 4.85410 | 5 | 0.14590 | $= a_0(6)$ (LP $=\lfloor\mathrm{Oler}\rfloor$ at $a=4.99$) | **0.000** |
| 7 | 5.86546 | 6 | 0.13454 | $= a_0(7)$ (LP $=27=\lfloor\mathrm{Oler}\rfloor$ at $a=5.99$) | **0.000** |

The bisection at $k=5$ ($M=6$) brackets $a^{*}(5) \in [3.81250,\ 3.82031]$, and
$a_0(5) = 3.81507$ lies inside that bracket: $a^{*}(5) = a_0(5)$ to the resolution of the search,
and the bracket width is the only reason it is not reported as exactly $0.000$.

The $k=5$ bisection is the sharp form of the failure: at $a = 2, 3, 3.5, 3.75, 3.8125$ the LP
returns $6, 10, 12, 13, 13$ — **exactly $\lfloor\mathrm{Oler}(a)\rfloor$ at every point** — and it
crosses to 14 exactly where $\lfloor\mathrm{Oler}\rfloor$ does. So $a^{*}(5) = a_0(5)$: the entire
refined family, 81 cells and 1918 binding boxes at $M=9$, reproduces Oler's inequality and adds
nothing to it. (It is worth noting what this *does* confirm: at $a = 2$ and $a = 3$ the LP returns
6 and 10, which are the exact true capacities $T(3)$ and $T(4)$ — the tool is sharp where the
answer is a lattice, and only there.)

In point units the statement is starker. The refinement closes **all** of the missing one point at
$k = 3$ and $k = 4$, and **none** of it at $k = 5$ and $k = 6$ — the fourth independent time this
project has landed on exact break-even, and the first time a method has crossed it at all.

**On $k = 7$.** Not a decision procedure here, per K1. §6 predicted the number would be
$\min(32, 27) = 27$; one evaluation at $a = 5.99$, $M = 6$ (36 cells, 409 binding boxes) returns
exactly **27**, which is $\lfloor\mathrm{Oler}(a)\rfloor$. It decides nothing, and `RULES.md` §7
would have applied to any other outcome: an
infeasibility at $k = 7$ from a method that is break-even at $k = 5$ and $k = 6$ would be a bug in
my own capacities, and the first thing to check would be a capacity that had come out too *small* —
which is exactly the failure control K3 caught once already.

## 8. Circularity audit (kill-criterion K2), performed because the verdict is "decided"

The binding constraints of the $k=4$ certificate, one by one:

| constraint | capacity | derived from | contains $d(n)$? |
|---|---:|---|---|
| $\Delta_A(a/3)$, $\Delta_B(a/3)$, $\Delta_C(a/3)$ | 1 each | diameter $a/3 < 1$ | no |
| $H = \{u_V \ge a/3\}$ | 5 | Lemma D, circumradius $a/3 < 1$ | no |

Neither mechanism knows what $d(9)$ is, and neither would change if the table said something else.
The $d(n)$ table appears in this attack in exactly one place — the validation row of §3, where it
checks the tool from the outside. Compare `FINDINGS.md` 2026-08-21: the predecessor's first run
reported infeasibility at $k=4$ because the whole-triangle capacity had been *set* to $d(9)=3$.
Here the whole-triangle capacity is never used in the certificate at all.

---

## 9. Honest accounting

**What is claimed.** That sub-integer refinement of the corner-coordinate box family is strictly
stronger than the integer version — demonstrated by a case, $k = 4$, where one decides and the
other does not — and that the refined family nevertheless fails at $k = 5$, therefore cannot be
trusted at $k = 7$. The $k = 3, 4$ propositions are lower-bound proofs of already-`cited` results;
they add nothing to the table and are offered as *controls*, which is what the brief asked for.

**Novelty: assume none.** The four-line $k = 4$ argument is the sort of remark a paper on this
conjecture makes in its first pages, and Lemma D ($6$ separated points need a disk of radius $\ge1$)
is classical. Melissen (1993) proves $n = 9$; that body has never been obtained by this project.
**Assume §5 is known until someone with library access says otherwise.**

**The step I am least sure of** is the completeness of the *shape* family, not of the thresholds:
every region here is a corner-coordinate box, i.e. an intersection of three strips parallel to the
sides. The efficiency ceiling of §6 is computed within that family, and a family of non-box convex
regions — or non-convex ones, for which the capacity tools still work — could have a higher
ceiling. §6 is a `sketch` argument about a restricted class, not a theorem about all partitions.

**Not checked.** (i) Whether $a^{*}(5)$ exceeds $a_0(5)$ at some larger $M$ — the bisection was run
only at $M=6$; $M=9$ gives break-even at $a=3.99$, consistent with but not proving $a^{*}=a_0$
there. (ii) $M \ge 12$ at $k = 5$, $M \ge 8$ at $k = 6$, and $M \ge 7$ at $k = 7$: the box enumeration
is $\binom{M+1}{2}^3$ and these did not finish inside the compute budget (the $k=7$, $M=7$ run was
started and killed by me at ~20 minutes); they are reported as not run, not as agreeing. (iii) Offset (per-corner) threshold grids,
which would give hexagonal cells directly; §6 predicts they lose to the symmetric grid, and that
prediction is untested. (iv) Whether the true capacity of a regular hexagon of side $\sigma \in
[0.93, 1)$ is exactly 5 — Lemma D gives $\le 5$, which is all §5 needs; a float search suggests the
five-point optimum is $1.0841\sigma$, so the bound is attained, but that is `numerical` and unused.

**Dependencies (`RULES.md` §3).** §5 depends on Lemma D and on elementary geometry — **not** on
Oler, not on CIO, not on the $d(n)$ table, and not on anything in `../eo-corner-squeeze/`. §4's
larger-$k$ rows depend on Oler (`cited`) for the capacities of the big regions. §2's Lemma P
re-verification changes no status: I am the same model family as its author, so my agreement
grants nothing (`RULES.md` §5).

**For the next reader.** The live question this leaves is *not* "refine the thresholds further" —
that is now measured, and §6 says where its ceiling is. It is whether the capacity toolkit can be
strengthened on **medium** regions (sides between 2 and 4, where §3's validation table shows slack
1–2 against the truth) by something cheaper than a global search, because that slack, and not the
partition geometry, is what the efficiency ceiling is made of.
