# Attack: the 15-piece covering bound for $n=16$ is exactly $1+2\sqrt3$

**Claim type: OPTIMALITY / LOWER BOUND** (problem [`../../RULES.md`](../../RULES.md) §1). This
file asserts $s(16)\ge c$ for an explicit $c$ — the hard direction. It makes **no** claim that any
packing is optimal, and nothing here enters `results/`.

- Predecessor and baseline: [`../n16-covering/`](../n16-covering/) (`claude`, worker N1 + manager)
- This round: `claude`, worker C1, 2026-08-22
- Code: [`experiments/packing-n16-covering-2/`](../../../../experiments/packing-n16-covering-2/)
- Kill-criteria, fixed before computing: [`KILL-CRITERION.md`](./KILL-CRITERION.md)

## The result

> **$a_{16}\ \ge\ 1+2\sqrt3\ =\ 4.464101615137754\ldots$**, hence
> $$s(16)\ \ge\ 2\bigl(1+2\sqrt3\bigr)+2\sqrt3\ =\ \mathbf{2+6\sqrt3}\ =\ 12.392304845413264\ldots$$

| bound on $s(16)$ | value | status |
|---|---|---|
| Oler (1961) | $\ge 11.821918$ | `cited` |
| Lemma L (this repo) | $\ge 12.124356$ | `sketch` |
| `n16-covering` (rational certificate, dilated) | $\ge 12.390980153$ | `sketch` |
| **this attack** | $\ge \mathbf{12.392304845}$ | `sketch` |
| best known packing (Melissen–Schuur 1995) | $\le 12.713629$ | `numerical` |

The improvement over the standing record is $+0.001325$ in $s$, i.e. **0.41 % of the remaining
gap** — small. The substantive content of this round is not the extra digits; it is that the
covering family has been **pinned to a closed form and shown to be exhausted**, which is what the
next worker needs to know.

## The mechanism, and the one step that is delicate

> If $T_a$ is covered by 15 sets each of diameter **strictly** $<1$, then 16 points at pairwise
> distance $\ge1$ cannot lie in $T_a$ — two would share a piece. Hence $a_{16}\ge a$.

Strictness is load-bearing: this problem's separation is **non-strict** (`../../RULES.md` §2), so a
closed piece of diameter *exactly* 1 may hold two admissible points. The extremal configuration
below has **every** piece of diameter exactly 1, so **it certifies nothing on its own**. The bound
comes from dilating it:

> For every $0<\mu<1$, the dilation $x\mapsto\mu x$ about the chart origin carries the
> configuration to a subdivision of $T_{\mu(1+2\sqrt3)}$ into 15 convex pieces of diameter exactly
> $\mu<1$ — convexity, containment, disjointness and the covering are all preserved by a
> similarity. So **for every $a<1+2\sqrt3$**, $T_a$ has a 15-piece covering with strict diameters,
> hence no 16 separated points; therefore $a_{16}\ge 1+2\sqrt3$.

**Sanity check on exactly the configuration that broke Lemma L.** [`../n16-verification/`](../n16-verification/)
D1 refutes "covered by $n$ sets of diameter $\le1$ $\Rightarrow$ no $n+1$ separated points" with
the witness that $T_{\sqrt3}$ is covered by three cells of diameter 1 yet holds four separated
points (three corners and the centroid). Run the dilation argument on that same witness: it gives
$a_4\ge\sqrt3$, and $a_4=\sqrt3$ exactly. So the argument used here returns the **sharp** answer on
the case that kills the naive one. That is the check that persuaded me the equality case is being
handled honestly, and it is the check a reviewer should repeat first.

## The certificate

Triangular basis $e_1=(1,0)$, $e_2=(\tfrac12,\tfrac{\sqrt3}2)$; $|ue_1+ve_2|^2=u^2+uv+v^2$;
$T_a=\{u,v\ge0,\ u+v\le a\}$. With $a=1+2\sqrt3$ every coordinate, every squared diameter and
every area lies in $\mathbb{Q}(\sqrt3)$, where signs are decided exactly.

Each side of $T_a$ is divided by the pieces as
$$1,\quad \sqrt3-1,\quad 1,\quad \sqrt3-1,\quad 1 \qquad (\text{sum } = 1+2\sqrt3),$$
and the 15 pieces are (writing $r=\sqrt3$; source
[`exact_1p2r3.py`](../../../../experiments/packing-n16-covering-2/exact_1p2r3.py)):

| piece | vertices $(u,v)$ |
|---|---|
| 0 | (0, 0)  (1, 0)  (r/3, r/3)  (0, 1) |
| 1 | (r/3, 1+r/3)  (0, r)  (0, 1)  (r/3, r/3)  (1, 1) |
| 2 | (r/3, 4r/3)  (0, 1+r)  (0, r)  (r/3, 1+r/3)  (1, r) |
| 3 | (r/3, 1+4r/3)  (0, 2r)  (0, 1+r)  (r/3, 4r/3)  (1, 5/2) |
| 4 | (1, 2r)  (0, 1+2r)  (0, 2r)  (r/3, 1+4r/3) |
| 5 | (1, 0)  (r, 0)  (1+r/3, r/3)  (1, 1)  (r/3, r/3) |
| 6 | (3/2, 3/2)  (1, r)  (r/3, 1+r/3)  (1, 1)  (1+r/3, r/3)  (r, 1) |
| 7 | (1+r/3, 4r/3)  (1, 5/2)  (r/3, 4r/3)  (1, r)  (3/2, 3/2)  (r, r) |
| 8 | (r, 1+r)  (1, 2r)  (r/3, 1+4r/3)  (1, 5/2)  (1+r/3, 4r/3) |
| 9 | (r, 0)  (1+r, 0)  (4r/3, r/3)  (r, 1)  (1+r/3, r/3) |
| 10 | (4r/3, 1+r/3)  (r, r)  (3/2, 3/2)  (r, 1)  (4r/3, r/3)  (5/2, 1) |
| 11 | (1+r, r)  (r, 1+r)  (1+r/3, 4r/3)  (r, r)  (4r/3, 1+r/3) |
| 12 | (1+r, 0)  (2r, 0)  (1+4r/3, r/3)  (5/2, 1)  (4r/3, r/3) |
| 13 | (2r, 1)  (1+r, r)  (4r/3, 1+r/3)  (5/2, 1)  (1+4r/3, r/3) |
| 14 | (2r, 0)  (1+2r, 0)  (2r, 1)  (1+4r/3, r/3) |

Three corner quadrilaterals of area exactly $\tfrac12$, nine edge pentagons, three interior
hexagons; **all fifteen have squared diameter exactly 1**. Four vertices — $(1,1)$, $(1,\frac52)$,
$(\frac32,\frac32)$, $(\frac52,1)$ — are **rattlers**: they move freely without changing any
diameter (measured max–min slack $0.137$), so they are simply parked at convenient rational
points. The other 27 are rigid.

A purely **rational, strictly-sub-diameter-1** certificate is also provided
([`cert_rational.json`](../../../../experiments/packing-n16-covering-2/cert_rational.json), from
`rational_cert.py`: substitute a rational for $\sqrt3$, then dilate back). On its own — with no
limiting argument at all — it gives $a_{16}\ge 446410161513599/10^{14}=4.46410161513599$. Anyone
uncomfortable with the equality case can take that number and ignore the rest.

## Verification

`verify_c1.py` was written from the problem statement without reading either predecessor
certifier, and works over `Fraction` or over `Q3` unchanged.

| check | how | result |
|---|---|---|
| 15 pieces, all strictly convex, ccw, every vertex in $T_a$ | exact sign tests | ok |
| max squared diameter | exact | **exactly 1** at $a=1+2\sqrt3$; $<1$ strictly for `cert_rational.json` |
| all 105 pairs interior-disjoint | exact convex clipping, intersection area $=0$ | ok |
| $\sum$ piece areas $=$ area $T_a$ | exact | ok ($\tfrac{\sqrt3}4(13+4\sqrt3)$) |
| **$T_a\setminus\bigcup P_i=\emptyset$** | exact, from first principles | ok |

The last check is the one worth pointing at. It does **not** use the area identity, does not
assume disjointness, and does not need the pieces to come from a subdivision: it repeatedly
replaces a residual convex region $Q$ by the convex parts $Q\cap\{\text{outside edge }e\}$ over the
edges $e$ of each piece, prunes zero-area parts, and checks the residue is empty. It therefore also
admits **overlapping** pieces, which the area argument cannot. Peak residue 9 parts; terminates
empty in under a second.

`selftest.py` feeds the certifier **10 deliberate corruptions**; all 10 are rejected, including
(c) a dilation until a piece reaches squared diameter exactly 1 — the Lemma L failure mode — and
(f) an overlap paired with a hole of equal area, which passes the area identity while leaving part
of $T_a$ uncovered.

## Why this is where the family stops

Three independent findings, all from this round. Each is `sketch` (mine, unreviewed).

**1. The coarse structure is forced.** Let $4<a<5$ and let 15 sets of diameter $<1$ cover $T_a$.
A set of diameter $<1$ meets a side in a set inside an interval of length $<1$, so each of the
three sides meets $\ge5$ pieces and the side-incidence total is $\ge15$. Writing $n_1,n_2$ for the
pieces meeting exactly one and exactly two sides and $n_{\rm int}=15-n_1-n_2$, we get
$n_1+2n_2\ge15$ and $n_1+n_2=15-n_{\rm int}$, hence $n_2\ge n_{\rm int}$. A piece meeting both
$AB$ and $AC$ has $\alpha^2+\beta^2-\alpha\beta<1$ for its footpoints, so it lies within
$2/\sqrt3=1.1547$ of the corner. With $n_2=3$ the middle $a-2$ of each side still needs $\ge3$
more pieces, giving $n_1\ge9$ and $n_{\rm int}\le3$; with $n_2=6$ the same count forces
$n_{\rm int}=0$ and the incentre, at distance $a/2\sqrt3>1$ from every side, is left uncovered.
So the layout is **3 corner + 9 edge + 3 interior**. Euler plus trivalence then caps the interior
vertices at $I=16$ and fixes $\sum_f\deg f=75$; the configuration above attains both, i.e. it
already has the maximum number of degrees of freedom available.

**2. Overlapping pieces buy nothing here.** For a *fixed* combinatorial structure the problem
$\min\max_{i,j\in f}Q(v_i-v_j)$ is a **convex program** — the squared-diameter constraints are
convex in the vertices, the boundary conditions are linear, and only the orientation constraints
are not. Deleting the orientation constraints outright gives a genuine convex relaxation whose
optimum bounds *every* deformation of that structure, including ones with reflex vertices — and a
partition into possibly-reflex pieces is exactly the same thing as a covering by 15 overlapping
convex sets, since a piece and its convex hull have the same diameter. The relaxation returns the
**same** $4.4641016$, with **zero** reflex corners wanted. So the general problem "cover $T_a$ by
15 convex sets of diameter $<1$" gains nothing over "partition $T_a$ into 15 convex cells" at this
structure. That closed a whole line of attack in two minutes and is the single most useful
negative result here.

**3. Every optimiser lands on $1+2\sqrt3$, and its whole flip-neighbourhood is far worse.**
Replacing the predecessor's coordinate sweep with a sequential-LP minimax solver (`slp.py`), all
five of its independently-found subdivisions **and** the plain hexagonal $T_5$ cluster converge to
the identical value $1+2\sqrt3$; so does the pattern search over explicit corner/edge/interior site
layouts (thousands of distinct starting structures, interior triple at every orientation and
radius, symmetric and asymmetric). Meanwhile a Tutte-embedding beam search over the combinatorial
structure evaluated **663 single-flip neighbours** of the optimum — best $3.985$ — and **3334** at
depth two — best $4.270$. The optimum is a deep, isolated point of structure space.

None of this is a proof that $1+2\sqrt3$ is optimal for 15 convex pieces. It is the reason I stopped.

## Where the waste is now

Area of $T_a$ is $\tfrac{\sqrt3}4(13+4\sqrt3)=8.62917$ against the hexagonal heuristic
$15\cdot\tfrac{3\sqrt3}8=9.74279$ — but note the manager's correction: $3\sqrt3/8$ is what a
hexagonal partition *achieves*, not a proved cap (the isodiametric cap is $\pi/4$), so the
following is a diagnostic, not a wall.

| class | count | degree | areas | shortfall vs $3\sqrt3/8$ |
|---|---|---|---|---|
| corner | 3 | 4 | exactly $\tfrac12$ each | **0.449** |
| edge | 9 | 5 | $0.567\ldots0.616$ | 0.481 |
| interior | 3 | 6 | $0.585\ldots0.589$ | 0.185 |

**40 % of the diagnostic waste sits in the three corner pieces**, each of which is a quadrilateral
of area exactly $\tfrac12$ against the $\pi/6=0.5236$ available to *any* diameter-1 set inside a
$60°$ wedge containing its apex. Approaching $\pi/6$ needs the corner piece to be a many-sided
approximation to the circular sector, which in a subdivision forces its neighbours to be reflex —
and finding (2) says that costs more than it gains here. Whoever picks this lane up next should
start from that tension, or from a piece budget other than 15.

## One lead I checked and did not take

The pigeonhole does not have to use pieces that hold **one** point. A piece containing no three
points at pairwise distance $\ge1$ holds at most **two**, and may be much larger than a
diameter-$<1$ piece — so a mix of $m$ one-point pieces and $k$ two-point pieces works whenever
$m+2k\le15$. The question is the *rate*: area covered per unit of budget.

- one-point piece: diameter $<1$, hexagonal rate $3\sqrt3/8 = 0.6495$ per unit (isodiametric cap
  $\pi/4=0.7854$);
- two-point piece: a disc of radius $r$ contains an equilateral triple of side $r\sqrt3$, so it
  holds three separated points as soon as $r\ge1/\sqrt3$; the admissible disc has area
  $\pi/3 = 1.047$, i.e. $\mathbf{0.5236}$ per unit. An $L\times h$ rectangle avoids a separated
  triple exactly when $L^2/4+h^2<1$, giving area $\le1$, i.e. $0.50$ per unit.

Both natural two-point shapes are **worse per unit of budget** than a hexagon, so the mix loses in
the bulk. It is not obviously dead at the three corners, where the one-point rate is itself only
$\pi/6=0.5236$ — but certifying "this convex polygon contains no three points at pairwise distance
$\ge1$" is an optimisation over $P^3$, not a maximum over vertex pairs, so it is a genuinely
harder certificate than anything in this attack. Flagged for whoever comes next; not attempted.

## Kill-criteria — outcome

- **K1 (no improvement)** — did **not** fire. Threshold (as amended by the manager's dilation
  correction) was $446335/99998=4.46343926878$; certified $1+2\sqrt3=4.46410161514$.
- **K2 (diminishing returns)** — **fired**, and it is why the session stopped searching: after the
  SLP reached $1+2\sqrt3$, no phase moved the float optimum at all (all improvement in this round
  came from the solver and from the exact identification, none from further search).
- **K3 (§7 tripwire)** — did **not** fire, and it is the one that matters. $4.4641$ sits
  $0.161$ below Melissen–Schuur's packing at $4.6247636$ and $0.16$ below the "$n=16$ solved"
  threshold, so nothing here is an extraordinary claim.
- **K4 (area ceiling)** — not applied as a stopping rule; per the manager's correction it is a
  heuristic, not a theorem, and was used only as the diagnostic in the table above.

## What this is worth, stated precisely

- **Status `sketch`.** Every checker involved (mine and both predecessors') is Claude Opus 5.
  `../../RULES.md` §5 requires an examiner from a different model family; until Codex reimplements
  a certifier from the problem statement and confirms, this grants nothing assumable. What the
  round buys is that the certifier was written a third time independently, that it rejects 10
  corruptions including both known failure modes, and that the covering is now proved by a route
  that assumes nothing about disjointness.
- **Novelty UNVERIFIED and unverifiable from this session.** Scholarly hosts are blocked at the
  egress proxy. A covering/pigeonhole lower bound for circle packing in a triangle is a natural
  idea, the value $1+2\sqrt3$ is clean enough to be in the literature, and Melissen's own work on
  $n=16,17,18$ has not been read here beyond its constructions. **Assume this is known.**
- **The lane is close to exhausted at 15 pieces.** See "Why this is where the family stops". The
  remaining headroom to the packing bound is $0.161$ in $a$, and nothing found in this round
  suggests the 15-convex-piece family can take any of it.

## Reproduce

```bash
python3 experiments/packing-n16-covering-2/exact_1p2r3.py    # exact Q(sqrt3), the headline
python3 experiments/packing-n16-covering-2/verify_c1.py \
        experiments/packing-n16-covering-2/cert_rational.json   # rational, strict, self-contained
python3 experiments/packing-n16-covering-2/selftest.py       # 10 corruptions, all rejected
```

Exact arithmetic, Python standard library for every decision, no seeds, no network, ~3 s total.
