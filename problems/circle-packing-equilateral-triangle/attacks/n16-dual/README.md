# Attack: design the 15-piece covering against the packing it must exclude

**Claim type: OPTIMALITY / LOWER BOUND** (problem [`../../RULES.md`](../../RULES.md) §1). This
file asserts $s(16) \ge c$ for an explicit $c$. It makes **no** claim that any packing is optimal,
and nothing here enters `results/`.

- Worker `claude` C3, 2026-08-22, branch `claude/circle-equklatetal-problem-sa7tx7`.
- Kill-criteria fixed before computing: [`KILL-CRITERION.md`](./KILL-CRITERION.md).
- Code: [`experiments/packing-n16-dual/`](../../../../experiments/packing-n16-dual/), Python
  standard library only, no network, no seeds in the exact stage.

## Result

> **$a_{16} \ \ge\ \dfrac{2232048569}{500000000} \ =\ 4.4640971380$ exactly**, hence
> $$s(16)\ \ge\ 2\cdot\tfrac{2232048569}{500000000} + 2\sqrt3 \ =\ 12.3922958911\ldots$$

| bound on $s(16)$ | $a_{16}$ | value | status |
|---|---|---|---|
| Oler (1961) | — | $\ge 11.821918$ | `cited` |
| Lemma L (this repo) | — | $\ge 12.124356$ | `sketch` |
| [`../n16-covering/`](../n16-covering/) | $4.4634392688$ | $\ge 12.3909801527$ | `sketch` |
| **this attack** | $\mathbf{4.4640971380}$ | $\ge \mathbf{12.3922958911}$ | `sketch` |
| best known packing (Melissen–Schuur 1995) | $4.6247636$ | $\le 12.713629$ | `numerical` |

The gain over the standing certificate is $+0.00065787$ in $a$ ($+0.0013$ in $s$) — small, and the
reason it is small is the main finding below. Certificates are reported as $a^\star = a/\mathrm{diam}_{\max}$,
so no dilation slack is discarded.

**Status: `sketch`.** Two checkers, both Claude Opus 5 — [`RULES.md`](../../../../RULES.md) §5
needs an examiner from a different model family, and problem `RULES.md` §3 needs a checker written
independently by Codex. Until then this grants nothing.

## The mechanism

If $T_a$ is covered by 15 sets each of diameter **strictly** $<1$, then 16 points at pairwise
distance $\ge1$ cannot lie in $T_a$, so $a_{16}\ge a$. Strictness is load-bearing: separation here
is non-strict, so a closed piece of diameter exactly $1$ may hold two points exactly $1$ apart.
The certificate's maximum squared diameter is exactly
$$\frac{2499999999672084722407099206109567}{2500000000000000000000000000000000} = 0.999999999868834 \;<\; 1 .$$

Everything is in the triangular basis $e_1=(1,0)$, $e_2=(1/2,\sqrt3/2)$, where
$|ue_1+ve_2|^2 = u^2+uv+v^2$ is **rational** and $T_a=\{u\ge0,v\ge0,u+v\le a\}$: no square root
appears anywhere in the verification.

## What the enemy's structure actually said — and it was not what the brief expected

`enemy.py` rescales the best-known 16-point configuration (`experiments/circle-packing-search/out/n16.json`,
float, design heuristic only) so its minimum pairwise distance is $1$, giving $a = 4.6247636$.

**1. The rattler.** $P_4 = (1.182003,\ 1.148403)$ has exactly **one** contact ($P_4P_{11}$) and no
wall contact. Every other point has total degree $3$ or $4$; the contact graph has 21 contacts and
10 wall contacts, so the other 15 points are isostatic ($30$ constraints, $30$ dof) and $P_4$
carries the one remaining degree of freedom. Reported, not "fixed" (problem `RULES.md` §5).

**2. The Voronoi plan in the brief cannot work, and the reason is quantitative.** The brief
proposed coarsening the packing's Voronoi diagram to 15 pieces. But at $a=4.6247636$ the Voronoi
cells are far too big *before* any merge:

| cell | $P_{15}$ | $P_2$ | $P_4$ | $P_1$ | … | smallest ($P_0$, $P_7$) |
|---|---|---|---|---|---|---|
| diameter | 1.4846 | 1.3603 | 1.3279 | 1.2690 | | 0.5774 |
| area | 1.0615 | 0.9858 | 1.0176 | 0.9182 | | 0.1443 |

Thirteen of the sixteen cells already have diameter $>1$, so **no** coarsening of this diagram is a
covering. Worse, four cells ($P_{15}, P_4, P_2, P_1$) have area above $\pi/4 = 0.7854$, and by the
isodiametric inequality a set of diameter $<1$ has area $<\pi/4$ — so those four cells provably
cannot be covered by one piece each *whatever its shape*. The packing's Voronoi diagram is not the
dual of the covering; the two problems want lattices of different spacing (packing $1$, covering
$\sqrt3/2$), which is a $4/3$ mismatch in pieces-per-point in the bulk.

**3. Where the covering does win: the corners.** `overlay.py` drops the enemy configuration,
rescaled into $T_{a^\star}$ (minimum distance $a^\star/4.6247636 = 0.96526 < 1$), onto the certified
partition and asks which pieces swallow two or more of its points:

| piece | holds | what those points are |
|---|---|---|
| corner $B$ quad | $P_7, P_8, P_{13}$ | the corner **and both** of its edge neighbours |
| corner $C$ quad | $P_0, P_{10}, P_{12}$ | the corner and both edge neighbours |
| corner $A$ quad | $P_6, P_{14}$ | the corner and its interior neighbour |
| edge pentagon on $CA$ | $P_1, P_5$ | an edge point and its interior neighbour |

The binding obstruction is **the three corners**, not any single interior pair, and it is the same
mechanism as the $n=4$ case where the method is exactly tight: there the three kite pieces each
hold one corner *and* the centroid, and $|{\rm corner}-{\rm centroid}| = a/\sqrt3$ is the diameter.

## The structure of the optimum, and why 15 pieces is the number it is

The optimiser converges — from random sites, from $p$-centre seeds, from triangular-lattice seeds,
and from the enemy configuration — to one $C_3$-symmetric combinatorial type:

> **3 corner quadrilaterals + 9 edge pentagons + 3 interior hexagons**, 31 vertices,
> every one of the 15 diameters within $5\times10^{-5}$ of the maximum.

That type is **forced**, by an argument that needs no computation. A piece meets a side of $T_a$ in
a set of diameter $<1$, whose convex hull is a sub-segment of length $<1$; those sub-segments cover
the side, so **more than $a$ pieces meet each side**, i.e. $\ge5$ for $4<a<5$. Writing $B_2$ for the
pieces meeting two sides and $B_1$ for those meeting one, $2B_2+B_1\ge 3\lceil a\rceil = 15$, so the
number of interior pieces satisfies
$$I \;=\; 15-B_1-B_2 \;\le\; B_2 .$$
With $B_2=3$ (the three corner pieces, as observed) that is $I\le3$: **at most three of the fifteen
pieces can avoid the boundary.** `verify.py` confirms the certificate realises exactly this — the
boundary chain is gapless with exactly 5 segments on each side.

Measured piece areas at $a^\star$ (hexagonal tiling optimum for diameter $1$ is $3\sqrt3/8 = 0.649519$):

| kind | count | area each | efficiency |
|---|---|---|---|
| corner quad | 3 | $0.49996$ | $95.5\%$ of its own $\pi/6 = 0.5236$ ceiling |
| edge pentagon | 9 | $0.5277\ldots0.6409$, mean $0.5761$ | $88.7\%$ |
| interior hexagon | 3 | $0.6420,\ 0.6478,\ 0.6537$ | $99.0\%$ |
| total | 15 | $8.62850 = \operatorname{area}(T_{a^\star})$ | $88.6\%$ |

**The interior hexagons are already essentially perfect.** All the slack is in the nine edge
pieces and, to a lesser extent, the three corners — and both of those are boundary-constrained.

## How much room is left, stated honestly

Two facts are rigorous for pieces of **any** shape:

- the piece containing a corner lies in the $60^\circ$ wedge within distance $<1$ of the apex, so
  its area is $<\pi/6 = 0.523599$;
- every piece has area $<\pi/4 = 0.785398$ (isodiametric).

Using only those, $\tfrac{\sqrt3}{4}a^2 < 3\cdot\tfrac\pi6 + 12\cdot\tfrac\pi4 = 10.9956$, i.e.
$a<5.038$ — **no proved wall below $4.6247636$**, exactly as the manager's correction says.

If one additionally assumes the (here *unproved*, and stated as an assumption) hexagonal bound
$3\sqrt3/8$ for a non-corner piece, the accounting reads
$$\tfrac{\sqrt3}{4}a^2 \le 3\cdot\tfrac{\pi}{6} + 12\cdot\tfrac{3\sqrt3}{8} = 9.36499
\quad\Longrightarrow\quad a \le 4.65194 ,$$
which still does **not** exclude the ceiling — it says the margin is $0.6\%$ in $a$. Concretely:
reaching $a = 4.6247636$ with 15 pieces requires the twelve non-corner pieces to average
$$\frac{9.261465 - 3\cdot 0.523599}{12} = 0.640895$$
in area, i.e. **$98.7\%$ of the hexagonal optimum for all twelve**, nine of which are pinned to a
straight side. The best convex partition found reaches $88.6\%$ overall. That is the size of the
job, and it is where a non-convex or curved-piece attack should aim: the **edge pentagons**, not
the interior.

## Controls — the method reproduces the known answers, and never overshoots

Run before the real attempt (`KILL-CRITERION.md` K0). The whole pipeline, including the exact
certifier, was applied unchanged.

| $m$ pieces | certified / float $a^\star$ | truth $a_{m+1}$ | verdict |
|---|---|---|---|
| 3 | **$\tfrac{866025399}{500000000} = 1.7320507980$** (exact) | $a_4=\sqrt3 = 1.7320508076$ | **passes**, 8 decimals, and **below** $\sqrt3$ — never above |
| 4 | $1.9998838$ (float) | $a_5 = 2$ | passes |
| 9 | $2.9999947$ (float) | $a_{10} = 3$ | passes |
| 8 | **$\tfrac{2977775921}{1000000000} = 2.9777759210$** (exact) | $a_9 = 3$ | **$0.74\%$ short** |

The $m=3$ row is the sharpest control available: the method certifies $\sqrt3$ from below to eight
decimals and never crosses it, which is what a correct pigeonhole must do.

The $m=8$ row is the informative one. $m=8$ is the exact analogue of $m=15$: one piece below a
perfect square ($8 = 3^2-1$, $15 = 4^2-1$). Two structurally different optimisers — a smoothed-max
descent and a target-shrinking minimax refiner, from hundreds of starts each — both plateau at
$a^\star = 2.97779$ against the known $a_9 = 3$; the plateau is frozen as an exact certificate (`cert_m8.json`, re-verified by `verify.py 8`). So in the one case where the answer is known,
**the 15-piece-style covering argument is provably not tight**, and falls short by $0.74\%$. That
is direct evidence that $A_{15} < a_{16}$ strictly. It does *not* tell us the size of the deficit
at $m=15$: $0.74\%$ of $4.6247636$ would be $4.590$, and the certificate is at $4.464$, so the
control does **not** license a claim that $4.464$ is the end of the road.

## Kill-criteria — outcome

- **K0a ($m=3$)**: did not fire; the pipeline reproduces $\sqrt3$ exactly and from below.
- **K0b ($m=8$)**: **fired** — $2.97779 < 2.99$. Recorded above.
- **K1 (structural gap)**: fired with K0b. Per its own terms the finding is recorded and the
  attack stops rather than being re-scoped. This is why this write-up spends more space on the
  measured structure than on chasing the last $10^{-4}$.
- **K2 (no improvement)**: did not fire; $4.4640971380 > 4.4634392688$.
- **K3 (diminishing returns)**: fired at the end of the $m=15$ polish stage.
- **K4 (§7 tripwire)**: **did not fire**, and it is the one that matters. $4.4640971380$ sits
  $3.5\%$ below $4.6247636$, consistent with a 16-point packing existing there.
- **K5 (circularity)**: honoured. The float configuration seeded designs and armed the tripwire;
  every number in the bound is an exact rational produced by the certifier, and $d(16)$ is used
  nowhere as an input.

## $m=16$ — attempted, inconclusive, reported as such

A 16-piece run was made to ask whether even *sixteen* pieces reach $4.6247636$ (which would bound
how lossy the method is). It stalled at $a^\star = 4.46388$ — numerically identical to the 15-piece
answer, with one piece of area $0.324$ and diameters spread over $0.9858\ldots1.0000$. That is a
search failure, not a measurement: the refiner cannot change topology, and no seed put the 16th
piece where it was needed. **No conclusion is drawn from it.**

## Verification

Two checkers, both mine, so this is *not* independent in the sense problem `RULES.md` §3 requires.

1. `dual.certify` — containment, strict convexity, directed-edge pairing, all 105 face pairs
   meeting in exactly zero area (exact convex clipping), areas summing exactly to
   $\operatorname{area}(T_a)$, and max squared diameter $<1$ strictly.
2. `verify.py` — written separately, re-parses the JSON and re-derives everything, and adds two
   checks the first does not make: the unmatched boundary edges are walked in order and shown to
   traverse each side corner-to-corner with no gap and no overlap (5 segments per side), and a
   deterministic exact grid of 1011 rational points (plus every vertex and edge midpoint) is
   checked to be covered. Both agree, including on the exact maximum squared diameter.

The covering itself is *proved*, not sampled: faces convex and inside $T_a$, pairwise
interior-disjoint, areas summing exactly to $|T_a|$ — so the union is closed with relatively open
null complement in $T_a$, hence equal to $T_a$. The boundary-chain check is an independent
combinatorial witness of the same thing.

## Reproduce

```bash
python3 experiments/packing-n16-dual/enemy.py       # enemy structure, rattler, Voronoi diameters
python3 experiments/packing-n16-dual/verify.py 15   # exact re-verification of the certificate
python3 experiments/packing-n16-dual/overlay.py 15  # which packing points share a piece
python3 experiments/packing-n16-dual/run2.py 15 600 # re-run the search (floats, seeded, ~10 min)
```

`verify.py` is exact-rational, standard library, no seeds, no network, ~2 s.

## Novelty

**UNVERIFIED — assume known.** Scholarly hosts are blocked at the egress proxy. A covering /
pigeonhole lower bound for circle packing in a triangle is a natural idea and the "divide a
triangle into $m$ parts of least maximum diameter" problem is classical; the $m=3$ answer
$1/\sqrt3$ certainly is. Nothing here should be described as new until someone with library access
says otherwise.
