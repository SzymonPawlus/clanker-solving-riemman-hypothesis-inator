# Exact exhaustion for the Erdős–Oler cases $n = T(k) - 1$

**Claim kind:** *optimality / lower bound* (problem [`RULES.md`](../../problems/circle-packing-equilateral-triangle/RULES.md) §1), and only a
one-sided bound at one explicit rational side. Each `proved` run is the statement

> no $n$ points at mutual distance $\ge 2$ lie in the **closed** equilateral triangle of side
> $d$, for that one rational $d$

i.e. $d(n) > d$, equivalently $s(n) > d + 2\sqrt3$.

**Status: `numerical`.** The computation is a finite exhaustion in exact integer and exact
rational arithmetic — there is no tolerance anywhere in a pruning rule — but it has not been
independently reimplemented, and problem `RULES.md` §3 requires that the *other* agent write the
checker from the problem statement. Nothing here may be built on. **Every `timeout` and
`unresolved` row proves nothing at all.**

**Read this first: a finite exhaustion at rational sides can never prove Erdős–Oler.**
See [§0](#0-what-this-can-and-cannot-reach) — it is the single most important thing in this
directory, and it bounds what any amount of compute here could deliver.

---

## For the workers on the theory routes — three tools you can use directly

No coordination needed; these are stdlib-only and take no setup.

```sh
# 1. RIGOROUS FEASIBILITY SCREEN.  "Is n points at separation 2 in T(d) ruled out for free?"
#    Closed form only, instant, exact.  Use before assuming a computation is needed.
python3 -m eoex feasible --n 27 --d 12

# 2. RIGOROUS REFUTATION AT ONE SIDE.  "Prove no n points fit in T(d)" for a rational d.
#    Exact exhaustion; prints "PROVED: ..." or says plainly that nothing follows.
python3 -m eoex prove --n 20 --d 39/4 --max-level 10 --time-limit 300

# 3. THE BAR AND THE COST.  What Oler already gives per k, and what resolution a cell
#    method needs to exceed it.
python3 -m eoex gap    --kmax 12
python3 -m eoex levels --kmax 7 --ratios 0.9 0.95 0.99 0.999
```

Importable pieces, if you want a lemma checked rather than a search run:
`eoex.oler.oler_excludes(n, d)` (exact, rational), `eoex.oler.node_bound(cells, d)` (Oler on a
union of cells, rigorous upper bound), `eoex.caps.capacity(side, n)` (points in a triangle of a
given side), `eoex.lattice.pair_compatible(c1, c2, d)` (exact integer max-separation test).
**Everything returns `numerical` evidence; none of it is assumable** (repo `RULES.md` §3).

Two results in here are about what a proof *cannot* look like and may save you time:
the partition lemma in
[`attacks/eo-exhaustion/`](../../problems/circle-packing-equilateral-triangle/attacks/eo-exhaustion/README.md)
§3 (any partition-and-count refinement of Oler is strictly worse than Oler itself, by
$I + (m-1)$), and §0 below.

---

## 0. What this can and cannot reach

The Erdős–Oler conjecture at $k$ is $d(T(k)-1) = 2(k-1)$: no $T(k)-1$ points at separation $2$
fit in a triangle of side $d$ for **any** $d < 2(k-1)$.

Ruling out one rational $d$ proves $d(n) > d$ and nothing more. The set of configurations of
$T(k)-1$ points at separation $\ge 2$ in the closed triangle of side exactly $2(k-1)$ is
**non-empty** (delete any point from the $k$-row lattice packing), so the family of statements
"$d(n) > 2(k-1) - \varepsilon$" has no finite subfamily equivalent to the conjecture, and no
limiting run exists. Shrinking $\varepsilon$ narrows an enclosure; it never closes it. This is the
same point `experiments/circle-packing-bnb/README.md` makes, and it applies here verbatim.

So what this directory can honestly produce is a **measured cost curve**: for each $k$, the
largest rational $d$ at which the exhaustion closes, expressed as the ratio
$\rho = d / 2(k-1)$ of the conjectured value. Reaching $\rho$ close to $1$ is the whole
difficulty; the table in §4 says how close each $k$ gets and at what cost.

One exception, and it is worth stating because it is the only case where a cell argument *is*
uniform in $d$: for $k \le 3$ the refutation happens at level 1 for **every** $d < 2(k-1)$
simultaneously (§4.1), so those cases are settled outright rather than approached.

## 1. Why a separate directory from `circle-packing-bnb`

Three reasons, in order of importance.

1. **Independence.** Problem `RULES.md` §3 makes an independently written checker the unit of
   verification for computational claims here. Everything below was written from the problem
   statement; `experiments/circle-packing-bnb/` was read for its *results and cost analysis*, and
   no code was imported or adapted from it. Where the two agree — the four-way subdivision, the
   integer form $a^2+ab+b^2$, the $D_3$ corner quotient — that is because the mathematics forces
   it, and the agreement is evidence, not copying. The two implementations produce comparable
   verdicts and their node counts differ (different branching order, different rules), so
   cross-running them is a real check.
2. **A different, stronger pruning rule.** The Oler-hull rule (§2.3) is a *global* test on a
   search node; the existing directory has only pairwise and per-cell tests. At the root it
   reproduces Oler's closed-form bound exactly, so a run here is never weaker than Oler's
   inequality — which matters, because Oler's free bound $d(16) > \sqrt{129}-3 = 8.3578\ldots$ is
   *stronger* than the $d(16) > 7.999$ that the existing search spent CPU-hours on.
3. **A different target.** The existing runs are $n = 12$ and $n = 16$. Neither is an Erdős–Oler
   case. The cost of the tight regime is very sensitive to which $n$ you pick, so the wall has to
   be measured on the family the hypothesis is actually about.

## 2. The method, and why each rule is sound

Container, from problem `RULES.md` §2: $A=(0,0)$, $B=(d,0)$, $C=(d/2, d\sqrt3/2)$, **closed**,
all inequalities non-strict. `--d` is the point-formulation side $d$, never $s$.

### 2.1 Nodes and branching

Subdivide each triangle into four congruent triangles of half the side. With $h = d/2^L$,
$u=(h,0)$, $v=(h/2, h\sqrt3/2)$, a level-$L$ cell is $(\text{orientation}, i, j)$ with

* $\mathrm{up}(i,j)$: vertices $(i,j)$, $(i+1,j)$, $(i,j+1)$;
* $\mathrm{down}(i,j)$: vertices $(i+1,j)$, $(i,j+1)$, $(i+1,j+1)$,

in lattice coordinates $(i,j) \mapsto iu + jv$. The child sets are re-derived in
`eoex/lattice.py` from the vertex formulas (the derivation is written out in the module
docstring, so a reviewer can check it without running anything), and
`tests/test_eoex.py::test_children_cover_and_are_contained` checks both directions by sampling:
every sampled point of a parent lies in some child, and every child vertex lies in the parent.

A **node** is a multiset of closed cells with positive multiplicities summing to $n$. Its meaning
is: *there is a configuration of $n$ points at separation $\ge 2$ in the container, together with
an assignment of each point to one closed cell containing it, realising these multiplicities.*
The root is "all $n$ points in the container". Branching takes a cell of minimal level and
distributes its $k$ points over the four children in all $\binom{k+3}{3}$ ways. Because the
children are closed and cover the parent, every point of the parent lies in at least one child, so
every configuration consistent with the parent is consistent with at least one child node. Hence
refuting all branches refutes the parent.

Working with multisets of cells rather than ordered tuples of points already quotients out the
$n!$ point-relabelling symmetry.

### 2.2 The pair and capacity rules

**Pair.** Two *distinct* points assigned to cells $X \ne Y$ are at distance at most
$\operatorname{maxsep}(X,Y)$. Squared distance is convex, so its maximum over a product of
polytopes is attained at a vertex pair and scanning the nine pairs is exact. For a lattice
displacement $(a,b)$, $|au+bv|^2 = h^2(a^2+ab+b^2)$, so with $d = p/q$ the test
$\operatorname{maxsep} \ge 2$ is the **integer** comparison

$$p^2\,(a^2+ab+b^2) \ \ge\ 4\,q^2\,4^{L}.$$

No rounding, no tolerance, no epsilon — this is why `--d` must be rational: the theorem produced
is about that rational.

**Capacity.** A cell of side $h$ holds at most $\operatorname{cap}(h)$ points. Three sound caps,
combined by `min` (`eoex/caps.py`):

| cap | rule | depends on |
|---|---|---|
| diameter | $h < 2 \Rightarrow$ at most 1 point | nothing |
| Oler | $\lfloor h^2/8 + 3h/4 + 1 \rfloor$ | Oler (1961), `cited` |
| cited $d(k)$ | $h < d(k+1) \Rightarrow$ at most $k$ points, $k+1 \le 15$ | problem README table, `cited` |

The third is compared exactly: each $d(k)$ is carried as a rational combination of
$1, \sqrt3, \sqrt6, \sqrt{33}$ and compared against the rational $h$ by refining `isqrt`-based
rational enclosures until the sign is decided. Those four are linearly independent over
$\mathbb{Q}$ so the refinement terminates; the loop is nevertheless bounded and **fails closed**
(returns "undecided" ⇒ no bound), which loses pruning but never soundness. `--max-cited 1`
switches this family off and `--no-oler-caps` switches Oler off, leaving a run that depends on no
external claim whatsoever.

### 2.3 The Oler-hull rule — what this directory adds

Oler's inequality, `cited` (Oler 1961; transcribed in
`problems/circle-packing-equilateral-triangle/attacks/oler-lower-bound/README.md` §1.1): for a
Jordan polygon $\pi$ whose vertices belong to a finite $E$ contained in the closed region bounded
by $\pi$, with pairwise distances in $E$ at least $1$,

$$N \ \le\ \tfrac{2}{\sqrt3}A(\pi) \;+\; \tfrac12 M(\pi) \;+\; 1 .$$

Our points are at separation $\ge 2$; halving coordinates gives, with $A, M$ measured in the
separation-2 picture,

$$N \ \le\ \frac{A}{2\sqrt3} \;+\; \frac{M}{4} \;+\; 1. \tag{OLER-2}$$

**The rule.** In a node the points lie in the union $U$ of the occupied closed cells, so
$\operatorname{conv}(E) \subseteq K := \operatorname{conv}(U)$. Apply (OLER-2) to
$\pi = \operatorname{conv}(E)$ — hypotheses (i) and (ii) hold for the hull automatically — and then
relax using $A(\operatorname{conv} E) \le A(K)$ and $M(\operatorname{conv} E) \le M(K)$, both
monotone under inclusion of convex sets. If the resulting bound is $< n$, the node is refuted.

*This is a global test.* It fires exactly when the occupied cells have retreated from the
container's boundary, which no pairwise test can see. Applied at the root it gives
$N \le d^2/8 + 3d/4 + 1$, i.e. Oler's closed form, so **a run with this rule enabled is never
weaker than Oler's inequality**; `tests/test_eoex.py::test_oler_matches_the_closed_form_at_the_root`
checks that identity exactly.

*Exactness.* $\det[u\;v] = h^2\sqrt3/2 > 0$, so the map $(i,j) \mapsto iu+jv$ is orientation
preserving and the convex hull may be computed on integer lattice coordinates. A hull with
lattice shoelace area $A_{\text{lat}}$ has $A = (\sqrt3/2)h^2A_{\text{lat}}$, and the area term of
(OLER-2) becomes $h^2 A_{\text{lat}}/4$ — **exactly rational**, the $\sqrt3$ cancels. Only the
perimeter leaves $\mathbb{Q}$: each edge has length $h\sqrt{Q_e}$ with $Q_e$ an integer, and the
code uses a rational **upper** bound for $\sqrt{Q_e}$ obtained from `isqrt`. Over-estimating the
perimeter over-estimates the bound, so rounding can only make the rule fire *less* often. There
is no floating point in the decision.

*The collinear escape clause.* Oler's theorem needs $\operatorname{conv}(E)$ to be a Jordan
polygon, which fails when $E$ lies on a line. In that case the extreme points of $E$ are at
distance $\ge 2(N-1)$, which exceeds the container diameter $d$ as soon as $d < 2(N-1)$. The
`Prover` **refuses to construct** with the Oler rule enabled unless $d < 2(n-1)$ holds; it is
checked, not assumed. (Every run here has $n \ge 5$ and $d \le 2n$, so it holds with room.)

### 2.4 Symmetry

$D_3$ permutes the three level-1 corner cells $\mathrm{up}(0,0)$, $\mathrm{up}(1,0)$,
$\mathrm{up}(0,1)$ — which contain $A$, $B$, $C$ respectively — as the full $S_3$, and fixes the
middle cell $\mathrm{down}(0,0)$. So every configuration has an image whose corner multiplicities
are non-increasing, and imposing that at the root split only is sound. Worth up to a factor 6.
`--no-symmetry` disables it, and `test_symmetry_does_not_change_verdicts` checks agreement on
small cases.

### 2.5 The three outcomes

| outcome | meaning |
|---|---|
| `proved` | every branch refuted. No $n$ points at separation $\ge 2$ in $T(d)$, hence $d(n) > d$. |
| `unresolved` | a node survived with every cell at `--max-level`. **Nothing is proved.** |
| `timeout` | wall-clock or node budget exhausted. **Nothing is proved.** The DFS stack is written to the output JSON. |

## 3. The resolution theorem — why the cost explodes, quantitatively

This is a statement about the *method*, and it is what makes the distance to $k=7$ a number
rather than a feeling. Status `sketch` (my derivation; the arithmetic is elementary but it has not
been cross-examined).

> **Claim.** Let all cells of a node be at level $L$, with side $h = d/2^L < 2$ — so every
> multiplicity is 1 and there are exactly $n$ cells. If the node survives the pair rule, then
> $T(d)$ contains $n$ points at pairwise distance $\ge 2 - 2h/\sqrt3$, and therefore
> $d \ge d(n)\,(1 - h/\sqrt3)$.

*Proof.* Take the centroids $g_i$ of the $n$ cells; each lies in its cell, hence in $T(d)$. An
equilateral triangle of side $h$ has circumradius $h/\sqrt3$, so for $x \in c_i$, $y \in c_j$,
$|x-y| \le h/\sqrt3 + |g_i - g_j| + h/\sqrt3$, whence
$|g_i - g_j| \ge \operatorname{maxsep}(c_i,c_j) - 2h/\sqrt3 \ge 2 - 2h/\sqrt3$. Scaling the
configuration by $2/(2 - 2h/\sqrt3)$ puts $n$ points at separation $\ge 2$ in a triangle of side
$d/(1 - h/\sqrt3)$, so that side is at least $d(n)$. $\square$

**Contrapositive, the useful form.** If $h < \sqrt3\,(1 - d/d(n))$ then *no* uniform-level-$L$
node survives, so the exhaustion closes at level $L$ given enough nodes. Writing $\rho = d/d(n)$,
the level needed is

$$2^{L} \ >\ \frac{d}{\sqrt3\,(1-\rho)} .$$

For the Erdős–Oler family, $d(n) = 2(k-1)$ (used here only to *size* a computation, never as a
proof input), so matching Oler's own bound — $\rho = \rho_{\text{Oler}}(k)$ from §4.0 — needs

| $k$ | $\rho_{\text{Oler}}$ | level $L$ needed | cells at that level $=4^L$ |
|---:|---:|---:|---:|
| 4 | 0.92400 | 6 | 4 096 |
| 5 | 0.95377 | 7 | 16 384 |
| 6 | 0.96886 | 8 | 65 536 |
| 7 | 0.97758 | 9 | 262 144 |

and $L \to \infty$ as $\rho \to 1$. Pushing past Oler at $k = 7$ costs levels fast
(`python3 -m eoex levels --kmax 7 --ratios 0.9 0.95 0.99 0.999`):

| $k=7$, $\rho$ | 0.90 | 0.95 | 0.99 | 0.999 | $\to 1$ |
|---|---:|---:|---:|---:|---:|
| level needed | 6 | 8 | 10 | 13 | $\infty$ |
| cells $4^L$ | 4 096 | 65 536 | 1 048 576 | 6.7 × 10⁷ | — |

That divergence is not an implementation defect; it is why no run closes the conjecture.

## 4. Results

Single core each, CPython 3.11.15, x86-64 Linux, four searches concurrent on a 4-core box, so the
seconds column is an upper bound on single-run time. The search is deterministic: there is no
randomness and no seed, and $(n, d, \texttt{max-level}, \texttt{max-cited}, \text{rules},
\text{symmetry})$ fixes the node count bit for bit.

### 4.0 The baseline every row must beat

Oler's closed form (`cited`) already gives $d(n) > \sqrt{8n+1}-3$ for free, with no computation.
At $n = T(k)-1$ that is $d > \sqrt{4k^2+4k-7}-3$, leaving a residual gap to the conjectured
$2(k-1)$ of exactly

$$(2k+1) - \sqrt{4k^2+4k-7} \ \sim\ \frac{2}{2k+1}.$$

Reproduce with `python3 -m eoex gap --kmax 12`:

| $k$ | $n = T(k)-1$ | target $d$ | Oler gives $d >$ | residual gap | $\rho_{\text{Oler}}$ |
|---:|---:|---:|---:|---:|---:|
| 3 | 5 | 4 | 3.4031242 | 0.5968758 | 0.85078 |
| 4 | 9 | 6 | 5.5440037 | 0.4559963 | 0.92400 |
| 5 | 14 | 8 | 7.6301458 | 0.3698542 | 0.95377 |
| 6 | 20 | 10 | 9.6885775 | 0.3114225 | 0.96886 |
| 7 | 27 | 12 | **11.7309199** | **0.2690801** | **0.97758** |
| 8 | 35 | 14 | 13.7630546 | 0.2369454 | 0.98308 |
| 12 | 77 | 22 | 21.8394847 | 0.1605153 | 0.99270 |

**An exhaustion contributes nothing unless it exceeds $\rho_{\text{Oler}}$.** That is the bar, and
it is the reason the $n=16$ runs in `circle-packing-bnb` ($d(16) > 7.999$, $\rho$ against Oler's
own $8.3578$ well below 1) added nothing: Oler's one-line evaluation is strictly stronger.

### 4.1 $k = 3$ ($n = 5$, target $d = 4$) — settled outright

For any $d < 4$ the four level-1 cells have side $d/2 < 2$, so each holds at most one point and
$5 > 4$ points cannot be placed. The argument is uniform in $d$, so it gives
$d(5) \ge 4$ — the full Erdős–Oler statement at $k=3$, not an approach to it. The search finds
exactly this: `proved` in **1 node** at every $d$ tested up to $399/100$.

This generalises to "$4^L$ cells of side $d/2^L < 2$" only while $4^{\lfloor \log_2(k-1)\rfloor} <
T(k)-1$, i.e. only for $k \le 3$; at $k \ge 4$ the count no longer forces a contradiction.

The "rules" column records the Oler-hull setting, because it changes node counts and speed
by several times and the runs were not all made under one setting: **A** = hull rule at every
node (the first implementation), **S** = hull rule only at nodes whose deepest cell is at level
$\le 3$ (the shipped default), **N** = per-node hull rule off. The root Oler test is
unconditional in all three.

### 4.2 $k = 4$ ($n = 9$, target $d = 6$), $\rho_{\text{Oler}} = 0.92400$

| $d$ | $\rho$ | max level | rules | outcome | nodes | seconds |
|---:|---:|---:|:--|---|---:|---:|
| 5.5 | 0.9167 | 8 | A | **proved** | 1 | 0.0 |
| 5.6 | 0.9333 | 8 | A | **proved** | 11 673 | 1.0 |
| 5.7 | 0.9500 | 8 | A | **proved** | 18 730 | 1.5 |
| 5.8 | 0.9667 | 8 | A | **proved** | 398 707 | 30 |
| **5.9** | **0.9833** | 8 | A | **proved** | 598 254 | 46 |
| **5.9** | **0.9833** | 9 | S | **proved** | 684 342 | 12 |

The $d = 5.5$ row closes in one node because the root Oler test alone refutes it
($5.5^2/8 + 3\cdot 5.5/4 + 1 = 8.906 < 9$) — the search subsumes Oler, as designed.

### 4.3 $k = 5$ ($n = 14$, target $d = 8$), $\rho_{\text{Oler}} = 0.95377$

| $d$ | $\rho$ | max level | rules | outcome | nodes | seconds |
|---:|---:|---:|:--|---|---:|---:|
| 7.7 | 0.96250 | 10 | A | **proved** | 319 603 | 45 |
| 7.8 | 0.97500 | 10 | A | **proved** | 556 592 | 64 |
| 7.8 | 0.97500 | 10 | N | **proved** | 720 946 | 14 |
| 7.9 | 0.98750 | 10 | A | **proved** | 1 665 291 | 163 |
| 7.95 | 0.99375 | 11 | S | **proved** | 1 761 513 | 40 |
| **7.99** | **0.99875** | 11 | S | **proved** | 4 241 969 | 98 |

Node growth along the A rows: $3.2\times10^5 \to 5.6\times10^5 \to 1.7\times10^6$ as $1-\rho$
halves, i.e. roughly $(1-\rho)^{-1.5}$ over the measured range. Extrapolating that exponent is
*not* a prediction of anything at $\rho = 1$: §0 says there is no run at $\rho = 1$.

### 4.4 $k = 6$ ($n = 20$) and $k = 7$ ($n = 27$) — nothing proved above Oler

**This is the wall, and it is a negative result.** Oler's closed form already certifies every
$d \le 9.68857\ldots$ at $k=6$ and every $d \le 11.73091\ldots$ at $k=7$, so only $d$ above those
values can add anything. Every attempt above them failed:

| $k$ | $n$ | $d$ | $\rho$ | max level | rules | outcome | nodes | seconds |
|---:|---:|---:|---:|---:|:--|---|---:|---:|
| 6 | 20 | 9.7 | 0.97000 | 10 | A | timeout | 4 133 888 | 420 |
| 6 | 20 | 9.75 | 0.97500 | 10 | A | timeout | 4 097 024 | 420 |
| 6 | 20 | 9.75 | 0.97500 | 10 | A | timeout | 774 144 | 90 |
| **6** | **20** | **9.7** | **0.97000** | 10 | S | **timeout** | **8 368 128** | **400** |
| 7 | 27 | 11.75 | 0.97917 | 10 | A | timeout | 646 144 | 90 |
| 7 | 27 | 11.74 | 0.97833 | 10 | A | timeout | 3 336 192 | 420 |
| **7** | **27** | **11.74** | **0.97833** | 10 | S | **timeout** | **13 210 624** | **400** |

Every one of these rows **proves nothing**. The measured throughput at $n = 27$ is
$3.3\times10^4$ nodes/s on one core, and the frontier at cutoff still held 138 unresolved
branches, so the search was nowhere near exhausting the tree.

**Summary of the whole curve** — the exhaustion beats Oler at $k = 3, 4, 5$ and does not beat it
at $k = 6$ or $k = 7$:

| $k$ | $n$ | $\rho_{\text{Oler}}$ | best $\rho$ **proved** | beats Oler? |
|---:|---:|---:|---:|:--|
| 3 | 5 | 0.85078 | all $d<4$, uniformly (§4.1) | **yes — case settled** |
| 4 | 9 | 0.92400 | 0.98333 ($d > 5.9$) | **yes** |
| 5 | 14 | 0.95377 | 0.99875 ($d > 7.99$) | **yes** |
| 6 | 20 | 0.96886 | — | **no** |
| 7 | 27 | 0.97758 | — | **no** |

### 4.5 Ablation: does the Oler-hull rule pay for itself?

At $n = 14$, $d = 39/5$, `--max-level 10`, single core under identical load:

| rules | nodes | seconds | nodes/s |
|:--|---:|---:|---:|
| A — hull rule at every node | 556 592 | 64 | 8 700 |
| N — per-node hull rule off | 720 946 | 14 | 53 000 |

**The rule as first written was a net loss**: it removes ~23 % of the nodes and costs ~6× per
node. That is worth recording because the rule *looks* obviously good — it is the only global
test available and it strictly dominates the pairwise tests logically. It does not dominate them
economically.

The shipped default (**S**) restricts it to nodes whose deepest cell is at level $\le 3$, where
the hull is cheap to compute and most informative. Restricting where a pruning rule fires can
only lose pruning, never soundness, so **S** is as sound as **A**. Reproduce with
`./run.sh full`, which runs both.

## 5. Reproducing

```sh
./run.sh          # tests, the closed-form tables, the short searches (~3 min)
./run.sh full     # additionally the Erdos-Oler sweep (~30 min wall on 4 cores)
```

Python 3.11+, standard library only — no dependencies, no network, no randomness, no seeds.
Individual results:

```sh
python3 -m eoex gap --kmax 12                                    # §4.0
python3 -m eoex prove --n 9  --d 59/10 --max-level 8             # §4.2, d(9)  > 5.9
python3 -m eoex prove --n 14 --d 39/5  --max-level 10            # §4.3, d(14) > 7.8
python3 -m eoex prove --n 27 --d 47/4  --max-level 10 --time-limit 420
python3 -m eoex feasible --n 27 --d 12                           # the closed-form screen
python3 tests/test_eoex.py                                       # 13 checks
```

Anything not `proved` is a budget record, not a weak theorem.

## 6. What I am least sure of

In descending order of how much damage it would do.

1. **The branching is exhaustive.** Everything rests on the four children being closed and
   covering the parent. The child sets are derived in the module docstring and checked by
   sampling; sampling is evidence, not proof. A wrong child set is the one bug that produces false
   `proved` verdicts everywhere while passing most tests. A reviewer should re-derive both child
   sets from the vertex formulas by hand.
2. **The Oler-hull rule's monotone relaxation.** $A$ and $M$ are monotone under inclusion of
   *convex* sets — true, and used on $\operatorname{conv}(E) \subseteq \operatorname{conv}(U)$,
   both convex. If the hull of the cells were computed in the wrong coordinates the area would be
   scaled wrong; the root identity test pins the normalisation, and
   `test_known_packings_survive_every_rule_at_every_level` checks that the rule does **not** fire
   on the actual optimal lattice packings at $n = 3,6,10,15,21$ at levels 0–6, where Oler is
   exactly tight and the margin is exactly zero. That is the strongest soundness evidence here.
3. **The separation-1 / separation-2 normalisation.** Oler is stated at separation 1 and this
   problem's certificates use separation 2; the factor of 2 enters the area term as 4 and the
   perimeter term as 2. It is pinned by two independent checks: the root identity against the
   closed form, and exact tightness at every triangular number.
4. **The $D_3$ restriction at the root.** Argued in §2.4 and tested for verdict-agreement on small
   cases only.
5. **The cited $d(k)$ capacities.** Removable with `--max-cited 1`.

## 7. Files

| file | what |
|---|---|
| `eoex/lattice.py` | exact integer subdivision geometry, pair test, hull, areas |
| `eoex/oler.py` | Oler's inequality: closed form and the per-node hull bound |
| `eoex/algebraic.py` | exact comparison against the cited algebraic $d(k)$ |
| `eoex/caps.py` | the three capacity rules |
| `eoex/search.py` | the DFS exhaustion |
| `eoex/__main__.py` | CLI: `prove`, `sweep`, `gap`, `feasible` |
| `tests/test_eoex.py` | 13 checks, negative controls included |
| `out/` | run outputs; `out/probe/`, `out/sweep/` are the timed runs |

Nothing here touches `problems/**/results/`.
