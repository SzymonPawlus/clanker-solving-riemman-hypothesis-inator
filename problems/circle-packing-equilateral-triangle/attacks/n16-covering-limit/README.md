# Attack: the ceiling of the 15-piece covering method for $n = 16$

**Claim type: neither of the two in problem [`../../RULES.md`](../../RULES.md) §1.** Nothing here
bounds $s(16)$ or $d(16)$ in either direction. What is bounded is the *auxiliary* quantity

$$A_{15}\ :=\ \sup\{\,a>0\ :\ T_a\ \text{is covered by 15 sets of diameter}<1\,\},$$

the resource the covering route of [`../n16-covering/`](../n16-covering/) consumes. An **upper**
bound on $A_{15}$ is an obstruction to that route, not a packing result. Nothing enters `results/`.

- Author: `claude` (Claude Opus 5 — convergent role, repo [`RULES.md`](../../../../RULES.md) §8:
  this is checking and exact calculation), 2026-08-22, worker **C4**
- Branch: `claude/circle-equklatetal-problem-sa7tx7`
- Kill-criteria, fixed before any computation: [`KILL-CRITERION.md`](./KILL-CRITERION.md)
- Code: [`experiments/packing-n16-limit/`](../../../../experiments/packing-n16-limit/) — one
  command, stdlib + numpy/scipy, **every decision an exact rational comparison**
- Journal: [`notebook/claude/2026-08-22-n16-covering-limit.md`](../../../../notebook/claude/2026-08-22-n16-covering-limit.md)

---

## Verdict, up front

**The method is not killed, and — more usefully — it cannot be killed by any argument of the
shape available here.** The lane's own ceiling is the finding.

| | bound on $A_{15}$ | status |
|---|---:|---|
| repo's certified 15-piece covering ⇒ $A_{15}\ \ge$ | $4.46335$ | `sketch` ([`../n16-covering/`](../n16-covering/)) |
| **the number that must be beaten** (16-point packing exists) | $\mathbf{4.6247636}$ | `numerical`, not used as an input here |
| **U2 — proved here** | $\mathbf{4.914308}$ | `sketch` (my proof; depends on isodiametric, `cited`) |
| U1 corner-refined isodiametric | $5.039166$ | `sketch` (restated from [`../eo-covering-bound/`](../eo-covering-bound/) T1 at $N=15$) |
| U0 isodiametric alone | $5.216032$ | `sketch` |
| C2 — U2 *plus* an unverifiable citation (see §5) | $4.725805$ | **conditional, not assumable** |

So $4.46335 \le A_{15} \le 4.914308$, and the interval still contains $4.6247636$: **the
constructors keep going with reason to hope.**

### The part worth acting on: the ceiling

> **No bound derived from the structure lemma of §2 can ever prove $A_{15}\le 4.836854$** — not
> with a sharper $f$, not with more computation. Adding the strongest per-piece constant anyone
> could cite moves that wall only to $4.7258$, and adding a per-piece corner cap on top of it only
> to $\approx 4.67$. **All three are above $4.6247636$.**

This is proved, not estimated: §4 exhibits explicit admissible pieces realising the budget, so the
inequality is *satisfiable* at those $a$ and no contradiction can be derived from it. K1 fired.

### Why, in one line

At $a = 4.6247636$ the 15 pieces must average

$$\frac{\operatorname{area}(T_a)}{15}=\frac{\sqrt3\,a^2}{60}=0.6174310\ldots
=\mathbf{95.06\%}\ \text{of}\ \frac{3\sqrt3}{8}=0.6495191\ldots,$$

the area of a **regular hexagon of diameter 1** — which *tiles the plane with no waste at all*.
Beating the ceiling therefore requires proving that 15 diameter-$<1$ pieces cannot reach 95% of
perfect hexagonal tiling efficiency. Per-piece area caps cannot see that: the sharp per-piece cap
is $\pi/4$ (a disk of diameter 1 fits in the interior and attains it), $15\cdot\pi/4 = 11.78$, and
the boundary corrections proved below recover only 21% of the way to $9.2615$.

---

## 1. Normalisation, and the guard against the standing trap

Separation **1**; $T_a$ is the closed equilateral triangle of side $a$; a **piece** is a set of
diameter $<1$ (strict — see [`../n16-covering/`](../n16-covering/) for why that word is
load-bearing). This is **not** the separation-2 convention of `results/`; no file there is read,
imported or converted anywhere in this attack, so the conversion slip cannot occur.

**Circularity guard (K2).** No published or repo value of $s(n)$, $d(n)$, $a_n$ or any covering
number is an input to any bound below. The only imported mathematics is the **isodiametric
(Bieberbach) inequality** — $\operatorname{diam}K\le1 \Rightarrow \operatorname{area}K\le\pi/4$ —
which is `cited`, standard, and says nothing about triangles or about $n=16$. The figure
$4.6247636$ appears in this file **only as a target to compare against**; it is never an input.
This matters because the natural sharp tool here (*"$m$ separated points force $m$ pieces"*) is
exactly the statement the covering route is trying to prove, and using it would be the failure
recorded in `FINDINGS.md` under *"A `cited` input contained the conclusion"*.

---

## 2. The structure lemma

Throughout, $4 < a \le 5$, and $T_a=\bigcup_{i=1}^{15}S_i$ with $\operatorname{diam}S_i<1$.

**(a) Three corner pieces.** Each vertex lies in some piece; fix one per vertex, $P_A,P_B,P_C$.
They are distinct, since the vertices are pairwise at distance $a>1$. Every point of $P_V$ is
within $\operatorname{diam}P_V<1$ of $V$, so $P_V\subseteq B(V,1)$, and for $a\ge2$ the set
$B(V,1)\cap T_a$ is exactly the $60°$ unit sector:
$$\operatorname{area}(P_V\cap T_a)\ \le\ \pi/6\ =\ 0.5235988\ldots$$

**(b) Edge middles are covered by disjoint families.** For an edge $e$ let $m_e\subseteq e$ be the
points at distance $>1$ from both of its endpoints — a segment of length $a-2$. Let
$M_e=\{i: S_i\cap m_e\neq\emptyset\}$.

- *No $P_V$ lies in any $M_e$*: $P_A\subseteq B(A,1)$ misses $m_{AB}$ and $m_{AC}$ by definition,
  and misses $m_{BC}$ because $\operatorname{dist}(A,BC)=a\sqrt3/2>1$.
- *$M_e\cap M_{e'}=\emptyset$ for $e\neq e'$*: two edges meet at $60°$; a point at distance $s$
  from the shared vertex on one and $t$ on the other are at distance $\sqrt{s^2-st+t^2}$, and on
  $s,t\ge1$ that expression is minimised only at $s=t=1$, with value $1$. For $s,t>1$ it exceeds
  $1>\operatorname{diam}S_i$, so no piece meets two middles.

**(c) Trace budget.** For $i\in M_e$ put $\ell_i=\operatorname{diam}(S_i\cap e)\le
\operatorname{diam}S_i<1$. The sets $S_i\cap m_e$, $i\in M_e$, cover $m_e$ and each has
$1$-dimensional measure $\le\ell_i$, so
$$\sum_{i\in M_e}\ell_i\ \ge\ a-2,\qquad\text{hence}\qquad |M_e|\ \ge\ \lceil a-2\rceil = 3 .$$

**(d) Edge pieces are penalised.** For $i\in M_e$, $\overline{S_i\cap T_a}$ has diameter $\le1$,
lies in the closed half-plane bounded by the line of $e$, and contains two points of that line at
distance $\ell_i$. Hence $\operatorname{area}(S_i\cap T_a)\le f(\ell_i)$ with
$$f(\ell)\ :=\ \sup\{\operatorname{area}S:\ \operatorname{diam}S\le1,\ S\subseteq\{y\ge0\},\
(0,0),(\ell,0)\in S\}.$$

**(e) Everything else** is bounded by the isodiametric inequality, $\le\pi/4$.

Summing (subadditivity of outer measure — the $S_i$ need not be measurable, their closed convex
hulls are):

> **Lemma S.** With $k_e=|M_e|$, $\sum_e k_e\le 12$ (else already a contradiction),
> $$\frac{\sqrt3}{4}a^2\ \le\ 3\cdot\frac{\pi}{6}\ +\ \sum_{e}k_e\,\hat f\!\left(\frac{a-2}{k_e}\right)
> \ +\ \bigl(12-\textstyle\sum_e k_e\bigr)\frac{\pi}{4},$$
> where $\hat f$ is the concave envelope of $f$ on $[0,1]$ ($f$ is non-increasing, because a convex
> piece with a trace of diameter $\ell'$ contains a sub-trace of every shorter length; and
> $\sum_i f(\ell_i)\le k\hat f(\sum\ell_i/k)$ by Jensen).

`outer.py` maximises the right-hand side over every admissible $(k_1,k_2,k_3)$ and bisects on $a$
in exact rational arithmetic.

---

## 3. $f(\ell)$ — certified from three directions

All three bounds are proved for a convex compact $S$ (convexification raises area, preserves
diameter and the half-plane). Write $S_y=[\alpha(y),\beta(y)]$ for the slice at height $y$,
$w(y)=\beta(y)-\alpha(y)$, and $H=\max\{y\in S\}$.

1. **Isodiametric:** $f(\ell)\le\pi/4$.
2. **Slice inequality (b):** $A=(0,0),B=(\ell,0)\in S_0$ give $\alpha(0)\le0\le\ell\le\beta(0)$, so
   $\beta(y)\le\sqrt{1-y^2}$ and $\alpha(y)\ge \ell-\sqrt{1-y^2}$, i.e.
   $w(y)\le 2\sqrt{1-y^2}-\ell$; also $H\le\sqrt{1-\ell^2/4}$ (the apex is within 1 of both $A$ and
   $B$). Integrating,
   $$f(\ell)\ \le\ \frac\pi2-\arcsin\frac\ell2-\frac{\ell}{2}\sqrt{1-\frac{\ell^2}4}.$$
   At $\ell=1$ this is **exact**: the admissible region is then the Reuleaux triangle on $AB$ and
   $f(1)=\tfrac{\pi-\sqrt3}{2}=0.6141848\ldots$
3. **Cross-slice inequality (a):** for $y,y'\in[0,H]$ the four cross distances give
   $\beta(y)-\alpha(y')\le\sqrt{1-(y-y')^2}$ and symmetrically, so
   $$w(y)+w(y')\ \le\ 2\sqrt{1-(y-y')^2}.$$
   Discretising $[0,\sqrt{1-\ell^2/4}]$ into $N=128$ slabs and taking suprema per slab turns (2)
   and (3) into a finite LP in the slab suprema — one LP per possible index of the slab containing
   $H$. Each LP is solved numerically and then its **value is re-derived from a rational dual
   certificate**, repaired and checked exactly, so the reported number is a theorem about the LP,
   not a floating-point claim.

And from below, an explicit admissible set — the unit-diameter disk centred at
$\bigl(\tfrac\ell2,\tfrac{\sqrt{1-\ell^2}}2\bigr)$ cut by the line $y=0$, which has diameter
exactly 1, lies in $\{y\ge0\}$ and carries $A,B$ on its boundary circle:
$$f(\ell)\ \ge\ \frac\pi4-\frac{\arcsin\ell}{4}+\frac{\ell\sqrt{1-\ell^2}}{4}.$$

At the value that decides everything, $\ell=(a-2)/4\approx0.66$:

| | $\ell=0.65$ | $\ell = 1$ |
|---|---:|---:|
| certified lower bound (explicit set) | $0.731991$ | $0.614185$ (exact) |
| certified upper bound (slab LP) | $0.753540$ | $0.614185$ (exact) |
| for scale: $\pi/4$ | $0.785398$ | |

A `numerical` star-polygon search (`f_lower.py`) agrees and is weaker than the explicit disk, so
the true $f$ sits in a window of width $\approx0.022$. **That window is worth at most $0.077$ in
the final bound** — which is precisely why sharpening $f$ cannot rescue the lane.

---

## 4. The ceiling of the method — the actual finding

Lemma S is an *inequality that a covering must satisfy*. It refutes a covering at $a$ only if its
right-hand side falls below $\operatorname{area}(T_a)$. Feeding the **certified lower** bound on
$f$ into the right-hand side exhibits a budget the lemma cannot rule out, and bisecting gives the
largest $a$ at which Lemma S is still satisfiable:

| what is assumed | Lemma S can never prove better than | closes the method? |
|---|---:|:--:|
| **X1** — Lemma S with the exact $f$, whatever it is | $A_{15}\le 4.836854$ | **no** |
| **X2** — X1 *and* every piece capped at $A_6=0.674981$ (§5) | $A_{15}\le 4.725804$ | **no** |
| **X3** — X2 *and* corner pieces capped at $0.45$ (§5, `numerical`) | $A_{15}\le 4.671543$ | **no** |

X1 is rigorous. X2 and X3 assume, in the coverer's favour, results that are *not* available (§5) —
and still land above $4.6247636$. The proved bound U2 $=4.914308$ sits $0.077$ above X1, so the
lane is essentially exhausted: everything left to gain from a perfect $f$ is $0.077$, and the
distance still to cover is $0.29$.

**The arithmetic of the gap, stated so the next worker does not re-derive it.** Suppose the sharp
"cell" constant for a diameter-1 piece were the regular-hexagon value $3\sqrt3/8=0.6495191$. Then
15 pieces give $9.742786$, i.e. $a\le4.743416$ — *already above the ceiling*. Closing the method
needs a further deficit of
$$9.742786-9.261465\ =\ 0.481320 ,$$
whereas the entire corner effect — all three corners, at their sharpest — is worth only
$$3\left(\tfrac{3\sqrt3}{8}-\tfrac\pi6\right)\ =\ 0.377761 .$$
So even a perfect density theorem *plus* a perfect corner analysis leaves $0.103559$ of area to be
found in edge effects alone. That is the size of the hole, and nothing in this lane's toolkit fills
it.

---

## 5. Two citations I could **not** verify, and one claim of the briefing I must correct

Network egress to every scholarly host is blocked in this session
([`../eo-literature/`](../eo-literature/) recorded the same). The following are therefore
**remembered, not `cited`**, and per K4 nothing conditional on them is assumable:

- **Fejes Tóth's hexagon bound for coverings** — if a convex hexagon $H$ is covered by convex sets
  $C_i$ then $|H|\le\sum_i h(C_i)$, $h(C)$ = area of the largest hexagon inscribed in $C$
  (*Lagerungen in der Ebene, auf der Kugel und im Raum*, 1953). A triangle is a degenerate hexagon,
  so it would apply.
- **Graham's "biggest little hexagon"** — the maximum area of a hexagon of diameter 1 is
  $A_6 = 0.674981\ldots$, attained by a non-regular hexagon (R. L. Graham, *The largest small
  hexagon*, J. Combin. Theory Ser. A **18** (1975) 165–170).

> **Correction to the briefing this worker was given.** The claim that *"diameter-1 sets cannot
> cover at density better than the hexagonal $2\pi/\sqrt{27}=1.2092$, giving $3\sqrt3/8$ per piece
> and $a\le4.74342$"* is **not supported**, and the repo should not carry it as a bound.
> $2\pi/\sqrt{27}$ is Kershner's constant for coverings by **congruent circles**. Arbitrary sets of
> diameter $\le1$ are not circles: *regular hexagons of diameter 1 tile the plane*, with density
> exactly 1 and no overlap at all, so the circle-covering density argument does not apply to them.
> The arithmetic $(\pi/4)/(2\pi/\sqrt{27}) = 3\sqrt3/8$ lands on the regular hexagon's area by a
> coincidence of that construction, not by a valid derivation.
> What the hexagon bound above would give instead is the *largest* hexagon of diameter 1, i.e.
> $15A_6 = 10.124715$ and $a \le 4.835498$ — **weaker** than the claimed $4.74342$, and still above
> the ceiling. Whether $3\sqrt3/8$ is nevertheless the truth for tilings by diameter-1 sets is a
> real question and is **open here**: a pentagon of diameter 1 with area $>3\sqrt3/8$ that tiles the
> plane would falsify the $4.74342$ figure outright, and the maximal regular pentagon of diameter 1
> has area $0.657164 > 0.649519$. I did not settle it and nothing above depends on it.

The corner cap $0.45$ used in X3 is a **`numerical` guess** at the largest hexagon inscribed in the
unit $60°$ sector; the sector contains an equilateral triangle of side 1, so the true value is
$\ge\sqrt3/4=0.433013$, and X3 with $0.433013$ would be *higher* still. Nothing rests on it — X3 is
there only to show that even this extra assumption does not reach the ceiling.

---

## 6. Kill-criterion outcomes

- **K1 (primary): FIRED.** The best bound from checkable ingredients is $4.914308\ \ge\ 4.6247636$.
  I stopped, reported the number and the ceiling, and did not re-scope into constructing coverings
  (another worker's lane), into packing search, or into "one more weight function".
- **K2 (circularity): held.** No literature or repo optimum is an input; the only import is the
  isodiametric inequality. §5 records the two things I would have liked to cite and could not.
- **K3 (§7 tripwire): did not fire, and is asserted in code.** `outer.py` asserts every bound
  exceeds $4.46335$; if any had fallen below the repo's exactly certified 15-piece covering, that
  would have been a bug in *my* argument, and the run would have failed rather than reported it.
  No lower bound on $A_{15}$ was derived at all, so the packing-refutation branch never arose.
- **K4 (citation dependence): fired, and is why C1/C2/X2/X3 are labelled conditional.**
- **K5 (budget): held** — the whole pipeline is about 7 minutes.

---

## 7. What to review hardest

1. **§2(b), the disjointness of the $M_e$.** It is the one combinatorial step, and the minimisation
   of $s^2-st+t^2$ on $s,t\ge1$ is where an error would be invisible and would inflate U2.
2. **§3(3), the cross-slice inequality and its discretisation.** The claim is
   $w(y)+w(y')\le2\sqrt{1-(y-y')^2}$ from the two *cross* distances $\beta(y)-\alpha(y')$ and
   $\beta(y')-\alpha(y)$ — note it fails if either slice is empty, which is exactly why the LP is
   re-solved once per possible index of the slab containing $H$ rather than once on the whole
   range.
3. **§4's ceiling claim** — that exhibiting a *lower* bound on $f$ bounds what the lemma can prove.
   It is the most valuable statement here and the easiest to state one step too broadly: it is a
   ceiling for **Lemma S**, not for every conceivable covering argument. A tool that bounds pieces
   *jointly* (a genuine density/tiling theorem with boundary corrections, or the $\chi>\omega$ idea
   of [`../eo-covering-bound/`](../eo-covering-bound/) §4) is not covered by it.
4. **§5's correction**, which contradicts a figure the team has been quoting.

## 8. Reproduce

```sh
sh experiments/packing-n16-limit/run.sh
```

~7 minutes, no network, no seeds outside the explicitly `numerical` side-computations. LPs are
solved with scipy but every reported LP value is re-derived from an exact rational dual
certificate; $\pi$ and $\sqrt3$ enter only as certified enclosures, rounded against the conclusion
($\operatorname{area}(T_a)$ from below, the covering budget from above).
