# r5-exhaust4 — mechanising the EO(4) case analysis by exhaustion, and where it provably stops

**Claim kind: optimality / lower bound** (problem [`RULES.md`](../../RULES.md) §1). Every
positive statement below is either `cited`, or a `sketch` derivation of mine, or a `numerical`
run. **Nothing here is assumable** (repo `RULES.md` §3).

**This is a reconstruction of a `cited` result, not new mathematics.** EO(4) is
$d(9) = 6$, i.e. $s(9) = 6 + 2\sqrt3$, proved by **Melissen (1993)**, Amer. Math. Monthly **100**,
916–925 (problem `README.md` table). The point of the exercise (round-4 proposal **AF**) is to
find out whether the repo's exhaustion machinery can *mechanically* reproduce a case whose answer
is already known. **It cannot, and the reason is a theorem rather than a budget observation.**

Code: [`experiments/packing-r5-exhaust4/`](../../../../experiments/packing-r5-exhaust4/).

---

## 0. Summary — what was established

| # | statement | status | how far |
|---|---|---|---|
| 1 | EO(4) $\iff$ *no 9 points in the closed unit triangle at pairwise distance $> 1/3$* | `sketch` (mine, elementary) | exact, and **uniform in $a$** |
| 2 | Machine re-derived from scratch; reproduces $d(5)\ge4$ (EO(3)) **uniformly in $a$**, and Oler's $\Delta(3),\Delta(4),\Delta(5)$ at the root | `numerical` | validation ladder passed |
| 3 | $d(9) > 5.9$, i.e. $a > 2.95$ — **independent reproduction** of `attacks/eo-exhaustion/` §4 | `numerical` | 569 301 nodes, 108 s |
| 4 | $d(9) > 5.98$ ($a > 2.99$) — beyond the repo's previous best of 5.9 | `numerical` | 1 275 604 nodes, 387 s |
| 5 | **No dyadic cell exhaustion with these rules can ever prove EO(4)** — an explicit node survives at *every* level | `sketch` + exact witness | §4, proved for all $L$ |
| 6 | **The dyadic pigeonhole closes EO($k$) if and only if $k \le 3$** | `sketch` (mine) | §4.4, two lines |
| 7 | The endgame on $(2.95, 3)$ is **not** reachable by this family; it reduces to a *partition-capacity* question that is not dyadic | `sketch` | §6 |

**Kill-criterion verdict (see [`KILL-CRITERION.md`](KILL-CRITERION.md)): fired, in the
informative direction.** AF pre-declared a ceiling at $k = 6$. The measured and then *proved*
ceiling is $k = 3$. The "measured-cheap exhaustion to $a > 2.95$" half of AF is cheap and was
delivered; the "near-lattice endgame on $(2.95,3)$" half is not merely expensive — it is
unreachable by any amount of refinement, for a reason that is exhibited explicitly.

---

## 1. The move that makes the whole thing uniform in $a$ — `sketch`

`attacks/eo-exhaustion/` §1.1 proves (monotonicity + finiteness; I re-derived it independently and
agree) that **no finite family of refutations at fixed rational sides can imply EO($k$)**, and its
§1.2(a) says the way out is *an argument uniform in $a$*. The repo's machinery never took that
step: it is parameterised by a rational side. One rescaling removes the parameter entirely.

> **Proposition 1.** Let $n \ge 2$ and $A > 0$. The following are equivalent.
> 1. For every $a < A$, no $n$ points at pairwise distance $\ge 1$ lie in the closed equilateral
>    triangle $T(a)$.
> 2. No $n$ points at pairwise distance $\;>\;1/A$ lie in the closed **unit** triangle $T(1)$.

*Proof.* (2 ⇒ 1) If $x_1,\dots,x_n \in T(a)$ have pairwise distances $\ge 1$ with $a < A$, then
$x_i/a \in T(1)$ have pairwise distances $\ge 1/a > 1/A$, contradicting 2.
(1 ⇒ 2) If $y_1,\dots,y_n \in T(1)$ have pairwise distances $> 1/A$, put
$\sigma = \min_{i<j}|y_i-y_j| > 1/A$. Then $y_i/\sigma \in T(1/\sigma)$ have pairwise distances
$\ge 1$, and $a := 1/\sigma < A$, contradicting 1. $\square$

With $n = 9$, $A = 3$ (and $d = 2a$, problem `RULES.md` §3):

> **EO(4) $\iff$ no nine points of the closed unit equilateral triangle have all
> $\binom92$ pairwise distances $> 1/3$.**

This is a **single statement with no parameter**. A machine that refutes it settles the whole
interval $a \in (0,3)$ in one run, which is exactly the shape §1.2(a) of `eo-exhaustion` asks for.
It also makes explicit what the difficulty *is*: the $\Delta(4)$ triangular lattice puts ten points
in $T(1)$ at pairwise distances $\ge 1/3$ **with the value $1/3$ attained**, so the corresponding
*closed* problem is feasible and only the strict inequality can fail. Every argument must therefore
use strictness somewhere. §4 shows where strictness can and cannot be used.

Two further consequences used below, both from the same rescaling (`sketch`):

* **Capacity.** $m$ points at distance $> t$ inside a triangle of side $h$ force
  $a(m) \le h/(t+\varepsilon) < h/t$ for some $\varepsilon>0$; so $a(m) \ge h/t$ **refutes** $m$,
  where $a(m) = d(m)/2$ is the cited least side. (In the closed problem one only gets the weaker
  $a(m) > h/t$.) Strictness buys the boundary case — and that is the *only* place it is bought.
* **Oler.** Oler's inequality at separation $\ge t$ reads
  $N \le \frac{2}{\sqrt3}\frac{A}{t^2} + \frac{M}{2t} + 1$ for the convex hull. It is strictly
  decreasing in $t$, so in the strict problem `bound ≤ n` already refutes, not just `bound < n`.

## 2. The machine — written from the problem statement

`experiments/packing-r5-exhaust4/eo4/`, stdlib only, **no floats in any decision**.

* **Container** $A=(0,0)$, $B=(1,0)$, $C=(1/2,\sqrt3/2)$, closed (problem `RULES.md` §2, scaled).
* **Cells.** The usual four-way subdivision, in lattice coordinates
  $(i,j)\mapsto iu+jv$, $u=(h,0)$, $v=(h/2,h\sqrt3/2)$, $h=2^{-L}$. The child sets are *derived* in
  `geom.children`'s docstring by doubling the parent's vertices and taking the three corner
  triangles plus the medial triangle; a sampling test (3 000 points per parent, 5 parents) confirms
  both directions — every child vertex lies in the parent, every sampled parent point lies in some
  child. Children are closed and cover the parent, so **refuting all children refutes the parent**:
  the branching is exhaustive.
* **Nodes.** A multiset of closed cells with multiplicities summing to $n$, meaning "there is a
  configuration together with an assignment of each point to a closed cell containing it". The root
  is "all $n$ points in the container", and every configuration is consistent with the root, so the
  case split at the root is exhaustive by construction.
* **Pair rule.** Squared distance is convex on a product of polytopes, so
  $\operatorname{maxsep}(X,Y)$ is attained at a vertex pair; scanning the nine pairs is exact. With
  $|au+bv|^2 = h^2(a^2+ab+b^2)$ and $t=p/q$ the test is the **integer** comparison
  $q^2\cdot\max(a^2+ab+b^2) \le p^2 4^{L}$ (strict mode) or $<$ (closed mode).
* **Capacity rule.** §1's rule with the cited $a(m)$. **Circularity guard: only $m \le 8$ is
  used.** $a(9)=3$ *is* the conclusion and $a(10)=3$ is Oler's $\Delta(4)$; neither appears in the
  table (`eo4/caps.py`). $a(5)=2$ is EO(3), cited and logically independent of EO(4), and is used.
  Rational values are compared exactly; irrational ones through certified rational enclosures that
  **fail closed**.
* **Oler-hull rule.** Oler (1961), `cited`, applied to $\operatorname{conv}(E)$ and then relaxed to
  the convex hull $K$ of the occupied cells ($A$ and $M$ are monotone under inclusion of convex
  sets). In lattice coordinates the $\sqrt3$ cancels and the area term is exactly rational; only
  the perimeter leaves $\mathbb Q$ and is **over**-estimated, so rounding can only make the rule
  fire *less* often. Perfect squares are recognised exactly — an overshoot of $10^{-7}$ is enough
  to stop this rule firing at precisely the configurations that decide these cases (this was a real
  bug, caught by the $n=10$ validation below). Degeneracy guard: collinear points at separation
  $\ge t$ span $\ge (n-1)t$, exceeding the container diameter $1$, so $(n-1)t>1$ is *checked*
  before the rule is enabled.
* **Symmetry.** $D_3$ permutes the three level-1 corner cells as $S_3$ and fixes the middle cell,
  so the corner multiplicities may be assumed non-increasing at the root split only.

**Independence.** Written from the problem statement. `experiments/packing-eo-exhaustion/` was read
for its *results and the wall it measured*, not for code; the shared ingredients (four-way
subdivision, the form $a^2+ab+b^2$, the $D_3$ quotient) are forced by the geometry. The node counts
differ from the repo's on the one instance both ran (§3, row 3: 569 301 here versus 684 342 there
for the same theorem), which is what an independent implementation should look like.

## 3. Validation ladder — run before anything else

All `numerical`; each row is one command in `experiments/packing-r5-exhaust4/README.md`.

| instance | mode | expected | got | nodes |
|---|---|---|---|---|
| $n=3$, $t=1$ | strict | proved ($a(3)\ge1$) | **proved** | 0 (root) |
| $n=6$, $t=1/2$ | strict | proved — Oler $\Delta(3)$ | **proved** | 0 (root) |
| $n=10$, $t=1/3$ | strict | proved — Oler $\Delta(4)$ | **proved** | 0 (root) |
| $n=15$, $t=1/4$ | strict | proved — Oler $\Delta(5)$ | **proved** | 0 (root) |
| **$n=5$, $t=1/2$** | **strict** | proved — **EO(3), uniform in $a$** | **proved** | **1** |
| $n=9$, $t=3/10$ | closed | must **not** prove ($a=10/3>3$) | unresolved | 873 |
| $n=9$, $t=20/59$ | closed | proved — $a>2.95$ | **proved** | 569 301 |

The Oler rows and the EO(3) row were re-run with `--max-cited 4`, which removes $a(5),\dots,a(8)$
from the capacity table, so that *no row proves a statement it was allowed to assume*. In
particular **EO(3) is reconstructed non-circularly and uniformly in $a$, in one branch node**: at
level 1 the four cells have side $1/2 = t$, so each holds at most one point by the strict capacity
rule, and $5 > 4$.

The negative control matters: at $t = 3/10$ the statement is *false* (nine points do fit in
$T(10/3)$), and the machine correctly proves nothing.

## 4. The theorem: this exhaustion can never close EO(4)

### 4.1 The witness

The $\Delta(4)$ lattice $P(p,q) = \big(\tfrac{p+q/2}{3},\ \tfrac{q\sqrt3}{6}\big)$,
$p,q\ge0$, $p+q\le3$, gives **ten** points of $T(1)$ at pairwise distances $\ge 1/3$, the value
$1/3$ being attained. Delete any one point; nine remain, still at pairwise distances $\ge 1/3$.
For each level $L\ge2$ let $\nu_L$ be the node consisting of the nine closed level-$L$ cells
containing them.

> **Theorem 2** (`sketch`, mine). For every $L \ge 2$ and each of the three $D_3$-classes of
> deleted point (corner, edge, centre), the node $\nu_L$ is refuted by **none** of the pair rule,
> the capacity rule, or the Oler-hull rule, in either strict or closed mode.

*Proof.* (i) *Distinct cells, multiplicity 1.* Distinct lattice points are $\ge1/3$ apart while a
level-$L$ cell has diameter $2^{-L}\le 1/4 < 1/3$, so the nine points lie in nine distinct cells
and every multiplicity is $1$. The capacity rule only ever refutes multiplicities $\ge2$.

(ii) *Pair rule.* For $x\in X$, $y\in Y$ lattice points,
$\operatorname{maxsep}(X,Y)\ge|x-y|\ge1/3$; the rule fires only on
$\operatorname{maxsep}(X,Y)\le1/3$, i.e. only on equality, which forces $x$ to maximise
$|\cdot-y|$ over $X$. That function is strictly convex, so over a non-degenerate triangle its
maximum is attained only at vertices. In level-$L$ lattice coordinates $P(p,q)$ is
$(2^Lp/3,\,2^Lq/3)$, and $3\nmid2^L$, so **no lattice point is ever a cell vertex**. Hence
$\operatorname{maxsep}(X,Y)>1/3$ strictly and the rule never fires.

(iii) *Oler-hull rule.* Let $E$ be the nine points and $K$ the convex hull of the nine cells. For
the corner-deleted class, $\operatorname{conv}(E)$ is the trapezoid with vertices (in the
separation-1 scale $T(3)$) $(0,0),(3,0),(2,\sqrt3),(1,\sqrt3)$: area $2\sqrt3$, perimeter $8$, so
Oler gives exactly $\tfrac{2}{\sqrt3}\cdot2\sqrt3+\tfrac82+1 = 9$ — **an exact equality case of
Oler at $n=\Delta(k)-1$**. Since $K \supsetneq \operatorname{conv}(E)$ has strictly larger area, the
node's bound is $>9$ strictly, and the strict-mode test `bound ≤ 9` never fires. (For the edge- and
centre-deleted classes $\operatorname{conv}(E) = T(3)$ and the limit is $10$.) $\square$

Consequently the depth-first search always retains the branch containing $\nu_L$ and **never
terminates with `proved`, at any level, for any node budget.**

### 4.2 The witness, verified exactly

`experiments/packing-r5-exhaust4/nontermination.py` constructs $\nu_L$ in exact arithmetic and
asks the actual `Prover` whether any rule fires. For $L = 2,\dots,12$ and all three classes:
**no rule fires, at any level** (`out/nontermination.json`). The Oler-hull bound is worth
tabulating, because it shows the failure is asymptotic and not a resolution artefact:

| $L$ | 4 | 6 | 8 | 10 | 12 | 14 | 16 | limit |
|---|---|---|---|---|---|---|---|---|
| corner-deleted | 9.9531 | 9.2354 | 9.0587 | 9.0147 | 9.0037 | 9.0009 | 9.0002 | $\to 9^{+}$ |
| edge/centre-deleted | 10.8613 | 10.2120 | 10.0528 | 10.0132 | 10.0033 | 10.0008 | 10.0002 | $\to 10^{+}$ |

The corner row converges to **exactly** the threshold and never reaches it: the deficit is
$\Theta(2^{-L})$ and always positive. This is the same phenomenon `experiments/packing-oler-slack/`
reports as "Oler exactly tight at $n=\Delta(k)-1$", seen from inside a search. (I did not re-derive
that lane's measurement; I re-derived the equality case myself, above, from Oler's statement.)

### 4.3 What is actually being observed

The relaxation a cell node encodes is *non-strict*: "there exist points in these closed cells at
pairwise distance $\ge 1/3$". That relaxation is **feasible** — the deleted lattice realises it —
so no sound rule reading only the cell geometry between distinct cells can refute it. Strictness
survives the relaxation in exactly one place: **inside a single cell**, where the diameter is
attained and $h\le t$ kills multiplicity $\ge 2$. Between cells it is always destroyed, because the
maximum separation of two distinct cells strictly exceeds the distance of the two points inside
them.

That is the whole story of the "+1", stated as a mechanism: *the missing unit of count lives at
equality, and a partition-based method sees equality only within a piece.*

### 4.4 So the ceiling is $k = 3$, not $k = 6$ — `sketch`

The only way this family produces a contradiction is pigeonhole *within pieces*: the level-$L$
dyadic subdivision has $4^L$ cells, each of capacity $1$ once $2^{-L}\le t = 1/(k-1)$, and a
contradiction needs $4^L < n = \Delta(k)-1$. From $2^L \ge k-1$,

$$(k-1)^2 \;\le\; 4^L \;<\; \frac{k^2+k-2}{2} \iff k^2-5k+4<0 \iff 1<k<4 .$$

> **Proposition 3.** The dyadic-cell pigeonhole closes EO($k$) **iff $k \in \{2,3\}$**.

At $k = 3$ it closes in one node (§3). At $k = 4$ the coarsest useful bound is already off by
exactly one: with the cited table capped at $m\le8$, the whole triangle has computed capacity $9$,
the four level-1 cells have capacity $3$ each (total 12), and every level $L\ge2$ has $4^L\ge16$
cells of capacity 1. **Refinement makes the count monotonically worse**, and the coarsest value
misses by exactly the $+1$.

## 5. The measured half of AF, delivered

`numerical`, exact arithmetic throughout; one core each, at most two concurrent (4-core box shared
with other lanes, so seconds are upper bounds). Mode `closed` at $t=1/a$ proves $d(9) > 2a$.

| $a$ | $t = 1/a$ | outcome | nodes | s |
|---:|---|---|---:|---:|
| 2.95 | $20/59$ | **proved**, $d(9) > 5.90$ | 569 301 | 108 |
| 2.97 | $100/297$ | **proved**, $d(9) > 5.94$ | 680 793 | 112 |
| 2.99 | $100/299$ | **proved**, $d(9) > 5.98$ | 1 275 604 | 387 |
| 2.995 | $200/599$ | see `out/closed-a2.995.json` | — | — |
| 2.999 | $1000/2999$ | **timeout — nothing proved**, 26 branches still live | > 2 412 544 | 600 (cap) |
| $\to 3$ | $\to 1/3$ | **impossible at every $L$**, not merely expensive (§4) | $\infty$ | $\infty$ |

**How far down in $a$ I certified: $a > 2.99$, i.e. $d(9) > 5.98$ and $s(9) > 5.98 + 2\sqrt3 =
9.4441\ldots$** against the `cited` $s(9) = 6+2\sqrt3 = 9.4641\ldots$ — so 99.67 % of the
conjectured value, versus Oler's free 92.40 % and the repo's previous 98.33 %. Each row is one
theorem at one rational side and, by §1/`eo-exhaustion` §1.1, **the whole column together still
does not imply EO(4)**. The cost curve is the honest content: roughly flat from 2.95 to 2.97, a
factor $\sim3.5$ in seconds from 2.97 to 2.99, and past the budget at 2.999.

Row 1 is an independent reproduction of `attacks/eo-exhaustion/` §4's $k=4$ row (which reports
684 342 nodes / 12 s for the same theorem, with a different implementation and branching order).
**I did not take that number on trust; I re-derived it with my own code, and I state it as an
independent confirmation rather than as an inherited input.**

The strict/uniform runs at $t = 1/3$, $n = 9$ do not close, exactly as Theorem 2 requires. What
they *do* is localise:

| level $L$ | surviving profiles | supportable cells | as a fraction of $T(1)$ | s |
|---:|---:|---:|---:|---:|
| 3 | 3 332 | 48 / 64 | 0.750 | 6 |
| 4 | 35 491 | 99 / 256 | 0.387 | 55 |
| 5 | 5 253 | 82 / 1 024 | 0.080 | 127 |
| 6 | 35 637 | 101 / 4 096 | 0.025 | 184 |

The **profile count is not monotone** (it is a count of descriptions, and a finer grid needs more
of them to describe the same region); the **supportable area is**, and it is the meaningful column.
At $L=5$ every supportable cell lies within $0.110$ of one of the ten $\Delta(4)$ lattice points
(mean $0.047$; cell circumradius $0.018$), and all ten lattice points carry supportable cells. So
**AF's "finite occupancy profiles" really do appear** — the survivors collapse onto a shrinking
neighbourhood of the lattice — but the *closure* step never arrives, because by Theorem 2 the
neighbourhood never becomes empty. That is the endgame on $(2.95,3)$, and it does not close.

## 6. What the endgame would need — and where the question actually goes

Everything in this family is a **partition-and-true-capacity** argument, the move
`attacks/eo-exhaustion/` §3.2 correctly identifies as the live one. Written in the scale-invariant
form, it needs a partition $T(1) = P_1\cup\dots\cup P_m$ with

$$\sum_{i=1}^m \operatorname{cap}_>(P_i) \;\le\; 8, \qquad
\operatorname{cap}_>(P) = \max\{\,|F| : F\subset P,\ |x-y|>\tfrac13\ \forall x\ne y\in F\,\}.$$

Three exact remarks (`sketch`, mine):

1. $\operatorname{cap}_>(P) = 1 \iff \operatorname{diam}(P)\le 1/3$. So a partition made only of
   capacity-1 pieces is exactly **an 8-piece cover of $T(1)$ by sets of diameter $\le 1/3$**. That
   is the covering question, and it is *not* what this lane runs — a sibling lane attacks it
   independently, and I have deliberately not read its files.
2. For a triangle of side $h$ the capacity is exactly $\operatorname{cap}_>= \max\{m: a(m) < h/t\}$
   (rescale by the actual minimum separation and let it tend to $t$). Hence **no triangle has
   capacity exactly 2**, because $a(2)=a(3)=1$ leaves no room for $h/t$: a triangle holds three
   points at separation $>t$ as soon as it holds two. (Likewise no triangle has capacity
   exactly 5, since $a(5)=a(6)=2$.) So a mixed partition must use **non-triangular** pieces to
   realise capacity 2 — e.g. four capacity-2 pieces, or six capacity-1 plus one capacity-2. This
   is a strictly larger search space than the covering question and, as far as I can tell, is not
   recorded anywhere in the repo.
3. The strict Oler-hull rule already yields a **forced corner structure** (`sketch`, mine). Work
   in the separation-1 scale $T(3)$ and let $\rho_i$ be the side of the largest corner sub-triangle
   at vertex $V_i$ containing no point of $E$. Cutting one corner of side $\rho$ removes area
   $\tfrac{\sqrt3}{4}\rho^2$ and, because the corner angle is $60^\circ$, replaces $2\rho$ of
   boundary by a chord of length $\rho$, so it removes perimeter $\rho$.

   *One corner first.* $\operatorname{conv}(E)$ lies in the (convex) trapezoid $T(3)$ minus the
   corner triangle at $V_1$, so Oler gives $9 \le 10 - \tfrac12(\rho_1^2+\rho_1)$, hence
   $\rho_1^2+\rho_1 < 2$ and $\rho_1 < 1$; likewise for $\rho_2,\rho_3$. In particular
   $\rho_i+\rho_j < 2 \le 3$, so **the three corner triangles are pairwise disjoint** and the
   area/perimeter bookkeeping is additive. *Then all three:* $T(3)$ minus all three corner triangles
   is a convex hexagon containing $\operatorname{conv}(E)$, and Oler gives
   $9 \le 10 - \tfrac12\sum_i(\rho_i^2+\rho_i)$, i.e.
   $$\sum_{i=1}^3 \big(\rho_i^2+\rho_i\big) < 2 .$$
   So **each corner of $T(3)$ carries a point of $E$ within distance 1 of it**, and if the three
   are balanced, within $(\sqrt{33}-3)/6 \approx 0.457$. This is a genuine interaction constraint
   and it is already inside the machine (it is what the Oler-hull rule computes); it is not enough,
   and Theorem 2 explains why it never will be — it is an inequality on the *closed* configuration,
   which is feasible.

**The honest boundary.** A closing argument must use strictness somewhere other than inside a
single piece of a partition. The two candidates the repo has are (a) a rigidity/uniqueness theorem
— every 9-point configuration in $T(1)$ at separation $\ge 1/3$ is a sub-configuration of the
$\Delta(4)$ lattice, hence has a pair at distance exactly $1/3$ — which is a *uniqueness* statement
of the kind Melissen's paper actually proves (zbMATH's review of it says "optimality *and
uniqueness*"), and (b) a 1-D chain lemma applied to a forced row. Neither is a finite cell
computation, and this lane produces no evidence that either is mechanisable.

## 7. What I verified myself, and what I took from elsewhere (PROTOCOL-R5 §6)

**Verified myself, from the problem statement, with my own code:**
the subdivision and its exhaustiveness; the pair/capacity/Oler-hull rules and their soundness;
Proposition 1; Theorem 2 (both the proof and the exact witness at $L\le12$); Proposition 3; the
corner-deficit inequality in §6.3; the $a>2.95$ refutation; the whole validation ladder including
the negative control.

**Taken from the repo and *not* re-derived:** the frontier and closure verdicts in
`PROTOCOL-R5.md` §4; `packing-oler-slack`'s "Oler exactly tight at $\Delta(k)-1$" (I re-derived the
$k=4$ equality case independently and it agrees, but I did not check their measurement);
`attacks/eo-exhaustion/` §4's node counts (quoted for comparison only — the theorem in that row I
re-proved myself).

**Taken as `cited`:** Oler's inequality; the table $a(m)=d(m)/2$ for $m\le8$ from the problem
`README.md`; and — only as the thing being reconstructed, never as an input — Melissen's
$s(9)=6+2\sqrt3$.

**Not used at all, deliberately:** $a(9)=3$ and $a(10)=3$ (see the circularity guard in §2), any
`r3-*`/`r4-*` sibling result, and anything from the sibling covering lane.
