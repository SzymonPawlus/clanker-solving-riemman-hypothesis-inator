# Verification pass over today's Erdős–Oler lemmas

**Claim type: neither construction nor optimality.** (Problem [`../../RULES.md`](../RULES.md) §1
asks for that sentence first.) No bound on $s(n)$ is asserted here, and no status is granted here.
This file is an adversarial re-derivation of six load-bearing claims produced today, written
without reading the authors' code for any of them.

- Examiner: `claude` (Claude Opus 5), 2026-08-21, branch `claude/circle-equklatetal-problem-sa7tx7`.
- Code: [`experiments/packing-eo-verify/`](../../../../experiments/packing-eo-verify/) — one
  command (`./run.sh`), Python standard library only, exact arithmetic throughout, **101 checks,
  all passing**. Transcript: [`out/report.txt`](../../../../experiments/packing-eo-verify/out/report.txt).

> ## This grants no status. Read this before using anything below.
>
> Per repo [`RULES.md`](../../../../RULES.md) §5, `verified:review` requires an examiner from a
> **different model family**. I am Claude Opus 5; so were the authors of every claim examined here.
> A same-family check is decorrelated only by the fact that I re-derived everything from the
> problem statement and tried to break it — **it is not decorrelated at the level that matters.**
>
> **Every claim below remains `sketch` and remains non-assumable, including the ones I confirm.**
> What this pass buys is error-finding, not certification. Six disagreements are recorded; the
> confirmations are worth exactly as much as one careful reader, no more.

---

## 0. Disagreements, each with its witness

Ordered by how much damage each is doing right now.

### D1 — "every partition-and-count refinement of Oler is dead" is FALSE

**Where:** the corollary being drawn from [`../eo-exhaustion/`](../eo-exhaustion/) §3. It has been
used to kill two routes.

The **lemma** in §3 is correct (see §1 below). What it says is that summing **Oler's bound**
$\Omega(P_i)$ over the pieces of a partition loses $I + (m-1)$. What is being read off it is that
summing *anything* over the pieces loses. That is false, and the repo contains its own
counterexample.

> **Witness.** [`../eo-small-cases/`](../eo-small-cases/) §2 proves EO(3) by partitioning $T_a$
> ($a < 2$) into 4 closed cells of side $a/2 < 1$ and capping **each cell at its true capacity, 1**.
> That gives $n \le 4$. Oler on the whole triangle gives $n \le \Omega(a) = a^2/2 + 3a/2 + 1$,
> which at $a = 1.999$ is $5.9965$. The partition beats Oler by nearly two whole points.
>
> Exactly, at three values of $a$ (`check_partition.py` §8):
>
> | $a$ | $\sum_i \Omega(\text{cell}_i)$ | $\Omega(T_a)$ | true 4-cell capacity |
> |---|---|---|---|
> | 1.9000 | 11.5050 | 5.6550 | **4** |
> | 1.9900 | 11.9500 | 5.9650 | **4** |
> | 1.9990 | 11.9950 | 5.9965 | **4** |
>
> The middle column is what the lemma is about and it is indeed always the largest. The right-hand
> column is what a partition argument actually uses, and it is the smallest.

[`../eo-exhaustion/`](../eo-exhaustion/) §1 states this same argument itself, as its "one
exception" for $k \le 3$ — so the file simultaneously contains the broad claim and a refutation of
it. The slide happens in §3's last paragraph: *"the same accounting is why the cell-capacity rule
inside a branch and bound is weak — capacity rules are pigeonhole rules on a partition."* A
capacity rule is **not** Oler's bound on the cell; for a cell of side $h<1$ Oler gives
$h^2/2 + 3h/2 + 1 \in (1,3)$ while the true capacity is 1.

**What is actually dead:** partitions in which each piece is capped **by Oler's inequality**.
**What is not dead:** partitions capped by true capacities, by a better bound on some piece, or by
the knowledge that some piece is empty. The last of those is precisely
[`../eo-hull-deficit/`](../eo-hull-deficit/) §4. Any route killed on the broad reading should be
re-examined.

*(This does not resurrect the $k=7$ pigeonhole: `../eo-small-cases/` §4.1 shows the uniform
subdivision overshoots by $(k-2)(k-3)/2 = 10$ pieces at $k=7$, which is a separate and correct
obstruction. The point is that the correct obstruction is a counting one, not this identity.)*

### D2 — the Barrier Theorem's equality case is much larger than stated

**Where:** [`../eo-hull-deficit/`](../eo-hull-deficit/) §6: *"Largest observed gain: 0, attained
exactly when the removed region $T\setminus K$ is an open corner triangle of integer side (and,
trivially, when $K = T$)."*

Theorem 6 itself is confirmed (§4 below). Its equality description is not. Exhaustive exact
enumeration of half-plane cuts at $m = 6$ finds **30 distinct non-trivial equality cases**, not 5:
equality holds for a half-plane cut along **any** of the three lattice directions at **any**
integer level, in both orientations. So besides the three families of corner cuts, these are all
exactly neutral:

| $K$ | $T \setminus K$ | $\mathrm{def}(K)$ | lattice points removed |
|---|---|---|---|
| $T_j$ (sub-triangle at a corner), $j = 1..5$ | a strip along the opposite side | $\Omega(6)-\Omega(j)$ | $28 - T(j{+}1)$ |
| $\{u \le j\}$, $\{v \le j\}$, $j = 1..5$ | a trapezoidal strip along a side | | |

e.g. $K = T_5$: $\mathrm{def} = 28 - 21 = 7$ and exactly 7 lattice points lie outside. None of
these removed regions is a corner triangle. Corrected reading: **the barrier is saturated by every
lattice line, not only at the corners** — which strengthens the file's own conclusion rather than
weakening it, but the stated characterisation is wrong and someone will build on it.

### D3 — §5's "Reading" paragraph is false for $j \ge 2$

**Where:** [`../eo-hull-deficit/`](../eo-hull-deficit/) §5: *"side just under 2 gains just under 3
and displaces $T(2) = 3$; side just under $j$ gains just under $T(j)$ and displaces $T(j)$"*, and
the accompanying *"[the supremum] is approached as $t \to j^-$ for a positive integer $j$."*

> **Witness.** $a_4 = \sqrt3 = 1.7320\ldots < 2$ (repo's `cited` table, $n=4$). So for
> $t \in [\sqrt3, 2)$ a corner triangle of side $t$ holds **four** unit-separated points, not
> $T(2) = 3$. Hence $\lim_{t \to 2^-}\mathrm{gain}(t) = 3 - 4 = -1$, not 0.
>
> Using the repo's `cited` $a_n$ for $n \le 15$ (`check_cio_and_small.py`, Claim 2e):
>
> | $j$ | 1 | 2 | 3 | 4 |
> |---|---:|---:|---:|---:|
> | $\lim_{t\to j^-}\mathrm{gain}(t)$ | **0** | $-1$ | $-2$ | $-3$ |

Proposition 5's headline survives intact: $\mathrm{gain}(t) < 0$ strictly for all $t$, and
$\sup_t \mathrm{gain}(t) = 0$. But the supremum is approached **only** as $t \to 1^-$, and the
"break-even at every integer scale" intuition — which is what a reader takes away — is wrong. The
corner mechanism is *even more* neutral than advertised at scales $\ge 2$.

### D4 — the exhaustion-impossibility argument's justification is false as written

**Where:** [`../eo-exhaustion/`](../eo-exhaustion/) §1: *"the sets $S(\varepsilon)$ shrink as
$\varepsilon$ grows and their 'limit' $\bigcap_{\varepsilon>0}$ is the non-empty $S(0)$."*

$S(\varepsilon)$ is **decreasing** in $\varepsilon$, so $\bigcap_{\varepsilon>0} S(\varepsilon)$ is
the *smallest* member of the family, not the largest; the object that is contained in $S(0)$ is the
**union** $\bigcup_{\varepsilon>0}S(\varepsilon)$. Worse, if Erdős–Oler at $k$ is true then every
$S(\varepsilon)$, $\varepsilon>0$, is **empty**, so the intersection is empty and equals $S(0)$ only
if $S(0)$ is empty too — which it is not.

> **Witness at $k = 3$, where everything is known.** $S(0)$ contains the 5-point configuration at
> $a = 2$ verified exactly in `check_cio_and_small.py`; and $S(\varepsilon) = \varnothing$ for every
> $\varepsilon > 0$ by the subdivision lemma (Claim 5, confirmed below). So
> $\bigcap_{\varepsilon>0}S(\varepsilon) = \varnothing \ne S(0)$.

**The conclusion still holds**, for a much more elementary reason the file does not give:
$d(n) \ge D$ is not implied by finitely many statements of the form $d(n) > d_i$ with $d_i < D$,
because the strongest of them only gives $d(n) > \max_i d_i < D$. Nothing topological is needed.

**But the conclusion is stated more broadly than it is proved.** *"A finite exhaustion at rational
side lengths cannot prove Erdős–Oler at any $k$"* rules out only *"refute at finitely many rational
$d < D$ and stop"*. It does not rule out:

1. **a finite argument uniform in $d$** — the file's own $k\le3$ exception is one, and
   [`../eo-small-cases/`](../eo-small-cases/) §1 is the general form. These are finite case
   analyses; calling them "not exhaustion" is a definitional move, not a theorem.
2. **exhaustion plus a separate closing argument.** A gap/rigidity theorem of the form
   *"$d(n) > D - \delta \Rightarrow d(n) \ge D$"* would let a **single** rational refutation at
   $D-\delta$ finish the job. Nothing in §1 excludes such a theorem; §1's own last paragraph
   ("any proof must contain a step uniform in $d$") is the correct and much weaker statement.

The file's §6.1 "Qualitatively: infinite" should be read as *for the method as implemented*, not as
a theorem about computation.

### D5 — the Barrier's extension below integer side is vacuous, so the route is not killed there

**Where:** [`../eo-hull-deficit/`](../eo-hull-deficit/) §6, the "And for $a<6$" paragraph, and the
conclusion *"that is the precise sense in which this route is dead"*.

The displayed inequality
$\mathrm{def}_a(K) - N(T_a\setminus K) \le [N(T_6\setminus K) - N(T_a\setminus K)] - [\Omega(6)-\Omega(a)]$
is correct algebra, but the bracket it leaves is not small.

> **Witness.** $a = 5.9$, $K = T_a$ (in the natural corner-aligned embedding $T_a \subseteq T_6$).
> Then $T_a\setminus K = \varnothing$ so $N(T_a\setminus K) = 0$, while $T_6\setminus K$ is the
> strip $\{5.9 < u+v \le 6\}$, which contains the 7 lattice points of the far edge, so
> $N(T_6\setminus K) \ge 7$. And $\Omega(6)-\Omega(5.9) = 0.745$. The bound therefore reads
> $\text{gain} \le 6.255$, against a required gain of $1$. It excludes nothing.

Theorem 6 is a theorem **at integer side length**. At $a < 6$ — which is where Erdős–Oler at $k=7$
lives — there is at present **no barrier theorem**, only the observation that any gain must be
integer-flavoured. A prover told "convex-cut relaxations are dead at $a<6$" has been told something
that is not established.

### D6 — §9's two "sharper" instances need $t$ strictly above the stated root

**Where:** [`../eo-hull-deficit/`](../eo-hull-deficit/) §9, instances 1 and 2.

Instance 1 takes $t^\ast$ to be *the root* of $\frac{t^2+t}{2} = \frac{2+\varepsilon}{3}$ and
concludes each $\Delta_V(t^\ast)$ contains a point. At the root exactly the inequality gives
$\sum_V m_V \ge (2+\varepsilon) - \varepsilon = 2$; with $m_V \le 1$ (Lemma 2, valid since
$t^\ast<1$) that permits one empty corner. To force all three corners occupied one needs
$\sum_V m_V \ge 3$, i.e. $t$ **strictly** greater than the root. Same slip in instance 2 ($\ge 8$
is obtained where $\ge 9$ is claimed).

Both conclusions survive the fix, and both are in any case weaker than §9's own headline, which is
correct (see §2 below). Low severity — recorded because it is the same non-attained-supremum
subtlety that the headline gets right, and a reader who copies instance 1's phrasing into a proof
will have an off-by-one.

---

## 0.1 A correction to my own examination, recorded per `RULES.md` §0

I spent a substantial part of this pass convinced that §9's **headline** — *"for every corner $V$
and every integer $1 \le j \le 5$, the open corner triangle $\Delta_V(j)^\circ$ contains at least
$T(j)$ points of $E$"* — was off by one, and that the correct threshold was $T(j)-1$. **That was my
error, and it would have been the most damaging finding in this file if I had shipped it.**

The step I got wrong: I required the CIO gain to reach $1$, when what a contradiction actually
requires is $\mathrm{gain} > \varepsilon(a)$, and $\varepsilon(a) = \Omega(a) - (\Delta(k)-1) < 1$
**strictly** for every $a < k-1$ (because $\Omega$ is strictly increasing and
$\Omega(k-1) = \Delta(k)$). The supremum $\sup_{t<j}\frac{t^2+t}{2} - m_{\text{open}} = T(j)-m$
is not attained, but the condition *"$\le \varepsilon$ for all $t<j$"* is closed, so it transfers to
the supremum: $T(j) - m \le \varepsilon < 1$ forces $m \ge T(j)$ for integer $m$. The headline is
correct as written, including the choice of the **open** triangle.

What caught it was writing the threshold down as an exact predicate and testing it against
$\varepsilon$ rather than against 1 (`check_cio_and_small.py`, Claim 2c). Two lessons, both
already in `RULES.md` §0: a supremum that is not attained is where these arguments live, and
"1" is not the budget — $\varepsilon(a)$ is.

---

## 1. Claim 1 — the partition lemma (`../eo-exhaustion/` §3)

**Verdict: CONFIRMED as an identity, under hypotheses the write-up does not state. The corollary
circulated from it is DISAGREED (D1).**

**Restated in my words.** Let $P \subset \mathbb R^2$ be a convex body, and let $P_1,\dots,P_m$ be
compact convex sets with non-empty interior, pairwise disjoint interiors, and $\bigcup_i P_i = P$.
Let $I = \mathcal H^1\bigl(\bigcup_i \partial P_i \cap \operatorname{int}P\bigr)$ — the internal
boundary, measured once. Then with $\Omega(R) = \frac2{\sqrt3}A(R) + \frac12 M(R) + 1$,
$$\sum_{i=1}^m \Omega(P_i) = \Omega(P) + I + (m-1).$$

**Derived independently.** Two facts, neither of which needs the pieces to be convex:

1. $\sum_i A(P_i) = A(P)$, since the interiors are disjoint and the internal boundary is null.
2. $\sum_i M(P_i) = M(P) + 2I$. Split each $\partial P_i$ into its part in $\partial P$ and its part
   in $\operatorname{int}P$. A.e. point of $\partial P$ lies on exactly one $\partial P_i$ (two
   pieces sharing a positive-length arc of $\partial P$ from inside would have overlapping
   interiors), giving $\sum_i \mathcal H^1(\partial P_i \cap \partial P) = M(P)$. A.e. point of the
   internal boundary lies on exactly **two** $\partial P_i$, giving $2I$.

The "exactly two" step is where I looked hardest. At a relative-interior point $p$ of a shared arc,
a convex $P_i$ with $p\in\partial P_i$ lies locally in one closed half-plane; two full-dimensional
pieces on the *same* side both contain interior points arbitrarily near every nearby point of the
arc, hence overlap. So there is at most one per side, exactly two in total. **A pleasant
by-product I did not find stated in the file:** two convex sets with disjoint interiors are
separated by a hyperplane and meet inside it, so *every internal boundary between convex pieces is
automatically a straight segment* — "cut length" is well defined without assuming polygons.

Then $\sum_i \Omega(P_i) = \frac2{\sqrt3}A(P) + \frac12 M(P) + I + m$. $\square$

**Hypotheses the write-up omits, all of which I broke on purpose:**

| Edge case asked about | Result |
|---|---|
| $m = 1$ | holds trivially ($I=0$) — checked |
| pieces meeting at a point | holds; a point has $\mathcal H^1 = 0$ — checked (3-piece fan at the centroid, 4-piece fan in a quadrilateral) |
| T-junction: one cut shared as a full edge by one piece and split between two others | holds — checked |
| **pieces with no interior** | **identity FAILS.** Add the cut segment itself as a third "piece" of a bisected $4\times4$ square: the union and the disjoint-interiors condition still hold, but $\sum\Omega$ exceeds $\Omega(P)+I+(m-1)$ by exactly 4. A degenerate piece has $A=0$ and, as a convex body, $M = 2\,\text{len}$, so it pays $\text{len}+1$ where the formula credits it only $+1$; the excess is the segment's length. Harmless direction — the sum is still an upper bound — but the identity is not an identity. |
| **cuts along the boundary** | **identity FAILS** if any part of $\partial P$ is counted in $I$; the file never says $I$ excludes it. Checked by adding the base of $T_6$ to $I$: predicted $10$, actual $4$. |
| non-simply-connected unions | cannot arise: $P$ is convex and the $P_i$ tile it |
| "$\Omega(P)$" = region or hull? | it must be the formula applied to the **region**. Oler's inequality itself (`cited`) is about a Jordan polygon with vertices in $E$; $\Omega(\text{region})$ is a *relaxation* of it, valid because area and perimeter are monotone under inclusion of convex sets. The lemma is an identity about the relaxation, not about Oler. |

**Also checked exactly:** the §3 arithmetic *"cutting $T(a)$ into $k$ horizontal strips loses
$(k-1)(a/2+1)$; at $k=7$, $a=6$, that is 24"* — reproduced exactly, loss $= 24$.

**What the lemma does not say** (this is D1): it bounds $\sum_i\Omega(P_i)$, and a partition
argument that caps pieces by anything sharper than $\Omega$ is untouched by it. Note also that even
the naive version has unused slack — a point lying on a cut is counted in two pieces, so
$n \le \sum_i\Omega(P_i) - \#\{\text{points on cuts}\}$.

---

## 2. Claim 2 — the conditional Erdős–Oler (`../eo-hull-deficit/` §4)

**Verdict: CONFIRMED.** This is the one another prover is building on, so it got the most attention.

**Restated.** $n = \Delta(k)-1$ points at pairwise distance $\ge 1$ in the closed equilateral
triangle $T_a$. If for some corner $V$ the closed corner triangle $\Delta_V(1)$ contains no point,
then $a \ge k-1$.

**Derived independently.** Let $K = T_a \cap \{h_V \ge \frac{\sqrt3}{2}\}$, i.e. $T_a$ with the unit
corner triangle at $V$ sliced off (needs $a \ge 1$; for $a<1$ the triangle has diameter $<1$ and
holds one point, so the statement is vacuous for $n \ge 2$). Then
$$A(K) = A(T_a) - \tfrac{\sqrt3}{4},\qquad M(K) = M(T_a) - 2\cdot 1 + 1 = M(T_a) - 1,$$
so $\Omega(K) = \Omega(a) - \frac2{\sqrt3}\cdot\frac{\sqrt3}{4} - \frac12 = \Omega(a) - 1$:
**a unit corner cut costs exactly $\frac12$ in area and exactly $\frac12$ in perimeter.**
$E \subseteq K$, $H = \operatorname{conv}E \subseteq K$, and area and perimeter are monotone under
inclusion of convex sets, so Oler gives $n \le \Omega(K) = \Omega(a)-1 = \frac{a^2}2+\frac{3a}2$.
If $a<k-1$ then $\frac{a^2}2+\frac{3a}2 < \frac{(k-1)(k+2)}{2} = \Delta(k)-1 = n$. $\square$

Verified exactly: $\mathrm{def}$ of a one-corner cut of side $t$ equals $\frac{t^2+t}{2}$ on 160+
values of $(a,t)$; $\Omega(k-1) = \Delta(k)$ for $k \le 60$; and
$\frac{a^2}2+\frac{3a}2\big|_{a=k-1} = \Delta(k)-1$ for $k \le 60$.

**The boundary cases the brief asked about:**

- **Corner exactly occupied.** Then $m_V \ge 1$, the hypothesis fails, and the corollary simply
  does not apply. No false conclusion is available. (This is also why the corollary is not a proof
  of Erdős–Oler: §5/§7.3's kill is exactly that $m_V$ cannot be bounded away from $N(t)$ without
  extra input.)
- **A point exactly on the far edge of $\Delta_V(1)$** ($h_V = \frac{\sqrt3}{2}$ exactly). This is
  the case that distinguishes the readings, and **it is safe in both**. Such a point lies in the
  *closed* triangle, so the closed hypothesis fails; but it lies in $K$, so the containment
  $E \subseteq K$ — which is all the proof uses — still holds.
- **Open vs closed.** $E \cap \Delta_V(1)^\circ = \varnothing \iff E \subseteq K$. So the
  **open** hypothesis is the weaker one *and is exactly what the proof needs*: the corollary is
  true under "the **open** unit corner triangle is empty", which is strictly more general than what
  is stated. Stating it with the closed triangle is sound (a stronger hypothesis), just not sharp.
  There is no reading of "empty" under which the conclusion fails.

**The generalisation in §4 and the headline of §9 are also confirmed**, and their derivation is
subtle enough that I got it wrong once (see §0.1). Statement: for a counterexample at $a<k-1$, for
every corner $V$ and every integer $1 \le j \le a$, $|E \cap \Delta_V(j)^\circ| \ge T(j)$. The
argument needs, and has, $\varepsilon(a) < 1$ strictly; the non-attained supremum transfers because
the constraint is a non-strict inequality holding for all $t<j$. Verified as an exact predicate
over $j \le 7$, $m \le T(j)+2$, $\varepsilon \in \{0,\frac12,\frac9{10},\frac{999}{1000},10^{-6}\}$.

**§7.2's claim re-derived independently:** all 28 single-point deletions of the lattice $\Lambda(7)$
are excluded for $a<6$, and the best available gain is a supremum of exactly $1$ — never 2, never
attained. At $a=6$ exactly, $\varepsilon = 1$ and the sup is not attained, so CIO correctly fails to
exclude configurations that demonstrably exist. That consistency check is the strongest single piece
of evidence that the $\varepsilon$-bookkeeping in §§4, 7, 9 is right.

**Dependencies.** Oler's inequality (`cited`, taken on trust here — I did not re-derive Oler);
monotonicity of area and perimeter under inclusion of convex bodies (elementary); the degenerate-$E'$
case analysis in §3, which I re-derived and agree with ($|E'|\le1$: $\Omega(K)\ge1$; $|E'|=2$:
$M(K) \ge 2\,\mathrm{diam}(K) \ge 2$; $m\ge3$ collinear: the spanned segment has length $\ge m-1$,
so $M(K) \ge 2(m-1)$ and $\Omega(K)\ge m$).

---

## 3. Claim 3 — the Corner-Deficit Lemma (`../eo-hull-deficit/` §2)

**Verdict: CONFIRMED under its stated hypothesis. The side condition is genuinely necessary, is
correctly stated, and is tight — but it is sufficient, not necessary.**

**Derived independently.** $K = T_a \cap \bigcap_V\{h_V \ge \frac{\sqrt3}{2}t_V\}$. Under
$t_U + t_V \le a$ for each of the three pairs, the three corner triangles are pairwise disjoint —
along the side $UV$ they occupy $[0,t_U]$ and $[a-t_V,a]$, which are disjoint iff exactly
$t_U + t_V \le a$ — so areas subtract and each side of $T$ keeps length $a - t_U - t_V \ge 0$:
$$A(K) = A(T) - \tfrac{\sqrt3}{4}\textstyle\sum t_V^2,\qquad M(K) = 3a - 2\textstyle\sum t_V + \textstyle\sum t_V = M(T) - \textstyle\sum t_V,$$
giving $\mathrm{def}(K) = \sum_V \frac{t_V^2+t_V}{2}$, and $\mathrm{def}(H) \ge \mathrm{def}(K)$ by
monotonicity. So the side condition is exactly the disjointness condition — it is not a convenience.

**Tests (all exact).**

- **Sufficiency:** the lemma holds on all **2148** random rational configurations
  (1–7 points, six values of $a$, denominators up to 12) that satisfy the side condition. Zero
  failures.
- **Necessity:** of **1852** random configurations violating it, **660 break the lemma**. Minimal
  witness: $E = \{\text{apex}\}$ in $T_a$ gives $t = (a,a,0)$ and
  $\mathrm{def}(H) = \frac{a^2}2+\frac{3a}2$ against a claimed $a^2+a$ — false for every $a>1$
  ($a=6$: $27$ vs $42$). A full-dimensional witness: $E = \{(0,6),(1,5),(0,5)\}$ in lattice
  coordinates, $t = (5,5,0)$, $\mathrm{def}(H) = 25 < 30$.
- **At the boundary** $t_U+t_V = a$ exactly (the medial-triangle configuration, $t=(a/2,a/2,a/2)$):
  the lemma holds **with equality**, at $a = 2,4,6$. The formula does not degrade there.
- **Along the whole extremal family** $t = (s,s,s)$, $s \le a/2$: **equality throughout**, exactly.
  This is worth recording — §2 reports the lemma tight only on the 12 stored certificates and on
  $T(k)-\text{apex}$; it is in fact tight on a one-parameter family, i.e. the bound is the exact
  value of $\mathrm{def}(K)$ and all the slack in the lemma is in the step $H \subseteq K$.
- **Just past the boundary** the lemma does not fail immediately: at $a=6$ with $t=(s,s,s)$ it
  survives for $s$ up to $3.5$ and first fails at $s = 4$ ($\mathrm{def}-\text{RHS} = -3$). So the
  side condition is **sufficient but not necessary**; a prover who finds it inconvenient cannot
  simply drop it, but the failure set is smaller than the condition suggests.
- **Reproduces §2's stated sanity value:** $T(k)-\text{apex}$ gives $t = (0,0,1)$ and
  $\mathrm{def}(H) = 1$ exactly, for $k = 3,4,5,6,7$.

The three-corner closed form was separately checked against exactly clipped polygons: correct on
all 130 admissible triples at $a=6$, and it **over-states** $\mathrm{def}(K)$ on 21 inadmissible
ones (e.g. $t = (2,3,5)$: true 23, claimed 24). §10's warning that Theorem 3 is *false* without the
hypothesis, not merely unproven, is accurate.

---

## 4. Claim 4 — the Barrier Theorem (`../eo-hull-deficit/` §6)

**Verdict: CONFIRMED at integer side length, for configuration-independent relaxations. The
equality case is misstated (D2); the extension to $a<6$ is vacuous (D5); the headline "no
convex-cut relaxation improves Oler at all" is broader than the theorem.**

**Derived independently.** $\Lambda$ is any unit-separated subset of $T_m$ with
$|\Lambda| = \Omega(m) = T(m+1)$ — the lattice is one. For convex $K \subseteq T_m$, the set
$\Lambda \cap K$ is unit-separated with hull inside $K$, so Oler gives
$|\Lambda\cap K| \le \Omega(K) = \Omega(m) - \mathrm{def}(K)$. Also
$|\Lambda\cap K| = \Omega(m) - |\Lambda\setminus K|$. Subtract:
$\mathrm{def}(K) \le |\Lambda\setminus K| \le N(T_m\setminus K)$. $\square$

The proof turns entirely on $|\Lambda| = \Omega(m)$ *exactly* — the tightness of Oler at integer
side — which is why it is an integer-side statement and nothing else.

**Tested exhaustively and exactly** at $m = 3,4,5,6$: 5232 half-plane cuts with rational normals,
3840 one/two/three-corner cuts, 1051 random convex hulls. **Maximum gain over all of them:
exactly 0.** I could not break it and do not expect anyone to.

**Two things the file flags as unchecked, now answered:**

1. **Non-convex $K$ breaks it.** Witness at $m=6$: $K$ = two disjoint closed unit cells,
   $(0,0),(1,0),(0,1)$ and $(4,0),(5,0),(4,1)$ in lattice coordinates. Then
   $\frac2{\sqrt3}A(K)+\frac12M(K)+1 = 1 + 3 + 1 = 5$ while $|\Lambda \cap K| = 6$, so
   $\mathrm{def}(K) = 23 > 22 = |\Lambda\setminus K|$. The mechanism is exactly Claim 1's: a
   disconnected region is charged the "$+1$" once but behaves like two pieces. So the barrier is
   specifically a *convex*-cut barrier, and non-convex cut regions are not covered — though, as
   §10 notes, non-convexity also breaks the monotonicity step that makes a cut usable.
2. **The equality family** is every lattice-line half-plane cut, not just corner triangles (D2).

**What the theorem does and does not kill.** It kills relaxations that charge the cut region its
**worst-case** capacity $N(T\setminus K)$. It does **not** kill relaxations that use the actual
count $|E \cap (T\setminus K)|$ — the file's own CIO is a convex-cut relaxation of exactly that
shape, and §7.2 shows it strictly improving on Oler for 28 explicit configurations. §10 says this;
the §6 headline and §0's kill summary do not, and it is the §6 headline that is being quoted.

---

## 5. Claim 5 — the $k=3$ proof (`../eo-small-cases/` §§1–2)

**Verdict: CONFIRMED.** The strongest thing in today's output: elementary, complete, and it does
something Oler cannot.

**Cell count.** For integer $m$, the lines parallel to the three sides through the points dividing
each side into $m$ equal parts cut $T_a$ into $\binom{m+1}{2}$ upward and $\binom{m}{2}$ downward
cells, $\frac{m(m+1)}2 + \frac{m(m-1)}2 = m^2$. Verified for $m = 1..7$ that the construction
yields exactly $m^2$ pieces and that **every one is equilateral with side exactly $a/m$** (all three
squared edge lengths equal $(a/m)^2$, exactly).

**Covering.** Verified two ways: (i) the exact area identity $\sum_i \text{shoelace}(P_i) =
\text{shoelace}(T_a)$ holds for $m = 2,3,4,5$ (this certifies both interior-disjointness and
covering up to measure zero, and it is the same computation as Claim 1's area check); (ii) an
explicit cell was located for every one of ~10 000 exact rational grid points of $T_6$, including
all cell corners and edge points, for $m=2,3,4,5$ — 0 misses.

**Closed cells and double counting.** This is the step the author flagged, and it is fine, in the
direction that matters. Each closed cell has diameter $a/m < 1$, so contains at most one point of a
unit-separated set. Every point lies in $\ge 1$ cell; choose one such cell for each point. The map
is injective — two points sharing a cell would contradict the diameter bound — so
$n \le \#\text{cells} = m^2$. A point on a shared edge belongs to two cells and is assigned to one;
the *other* cell is then also blocked, which only loses information and cannot inflate the **upper**
bound. The bound is correct; it is simply not tight when points sit on cell edges.

**Strictness.** $a < m$ is load-bearing and correctly stated: at $a = m$ cells have diameter exactly
1 and two points at separation exactly 1 may share one. At $a = 2$, $m = 2$ the 5-point
configuration exists, which is exactly the failure the strictness prevents.

**EO(3).** $m = 2$, $a<2 \Rightarrow n \le 4 < 5$, so $a_5 \ge 2$; and the five points
$(0,0),(1,0),(2,0),(\frac12,\frac{\sqrt3}2),(\frac32,\frac{\sqrt3}2)$ lie in $T_2$ with minimum
squared separation exactly 1 (verified exactly), so $a_5 \le 2$; adding the apex gives $a_6 \le 2$
and $a_6 \ge a_5$. Hence $a_5 = a_6 = 2$ = EO(3). Confirmed.

**Also confirmed:** the bonus (the lemma re-proves $a_{\Delta(k)} = k-1$ exactly for $k \le 4$,
since $\Delta(k) > (k-1)^2 \iff k \le 4$), and §4.1's identity
$(k-1)^2 - (\Delta(k)-2) = \frac{(k-2)(k-3)}2$, which is 10 at $k=7$.

---

## 6. Claim 6 — exhaustion impossibility (`../eo-exhaustion/` §1)

**Verdict: DISAGREED on the justification (D4); the narrow conclusion is CONFIRMED for a reason the
file does not give; the broad conclusion is NOT ESTABLISHED.**

Precisely:

| Statement | Verdict |
|---|---|
| No finite set of refutations at rational $d < D$ implies $d(n) \ge D$ | **confirmed** — immediate from $d(n) > \max_i d_i < D$; no topology needed |
| The justification via $\bigcap_{\varepsilon>0}S(\varepsilon) = S(0)$ | **disagreed** — the family is decreasing, so this is the wrong set operation, and under EO every $S(\varepsilon)$ is empty. Witness at $k=3$ in D4 |
| "A finite exhaustion at rational side lengths cannot prove Erdős–Oler at **any** $k$" | **not established** — the file's own $k \le 3$ exception and `../eo-small-cases/` §1 are finite arguments that do prove it, uniformly in $d$ |
| Exhaustion + a separate closing argument is also ruled out | **not established** — a gap theorem $d(n) > D-\delta \Rightarrow d(n) \ge D$ would let one rational refutation finish. Nothing here excludes one |
| "Any proof at $k=7$ must contain a step uniform in $d$" (§1, last para) | **confirmed**, and this is the statement the file should lead with |
| §2's residual-gap table, both normalisations | **confirmed exactly** (see §7) |

The `numerical` rows in §4 (the measured wall) were **not** examined — I did not read, rerun or
reimplement `packing-eo-exhaustion`, and that work needs its own independent checker under problem
`RULES.md` §3.

---

## 7. Cross-file consistency: the separation-1/2 normalisation

The brief warned that multiple workers slipped on this today. It is clean in the three files
examined, and I checked it from both ends:

- `eo-exhaustion` §2 works in $d$ (separation 2) and gives $d(n) > \sqrt{8n+1}-3$; at $n=27$,
  $\sqrt{217}-3 = 11.7309199$.
- `eo-hull-deficit` §0.1(d) works in $a$ (separation 1) and gives
  $a_0 = \frac{-3+\sqrt{8\Delta(k)-7}}{2}$; at $k=7$, $5.8654600$.
- $2 \times 5.8654600 = 11.7309199$. The two tables are exactly a factor of 2 apart, everywhere.
  Verified exactly for all the rows both files print. **The two files agree.**

`eo-hull-deficit` §0.1(d) is also right on the merits about the disputed table: the manager's
$k=3:1.3723,\dots$ solve $\Omega(a) = \Delta(k)-2$, not $\Delta(k)-1$; the worker's
$0.298 \to 0.135$ figures are the correct ones. Confirmed exactly.

---

## 8. What is safe to build on, and what is not

**First, the flat answer required by `RULES.md` §3: nothing here is assumable.** Everything below
is `sketch`, before and after this pass, because a same-family review grants no status. The column
below is *"has an independent reader tried to break it and failed"* — that is a different and much
weaker question, and it is the one the manager asked.

| Claim | Confirmed? | Safe to build on? |
|---|---|---|
| **Conditional EO / Corollary 4** (`eo-hull-deficit` §4) | yes, re-derived | **Yes — use it.** Sound under both readings of "empty"; the boundary cases do not bite. The prover working its contrapositive can proceed. Still `sketch`: cite it as an assumption, not a fact |
| **§9 headline** (open $\Delta_V(j)$ holds $\ge T(j)$ points) | yes, re-derived, after I got it wrong once | **Yes.** But copy the $\varepsilon(a)<1$ step, not just the statement — it is the whole argument |
| **§9 instances 1 and 2** (the $t^\ast$, $t^+$ values) | no | **Only with "$t$ strictly above the root"** (D6). They are weaker than the headline; prefer the headline |
| **Corner-Deficit Lemma** (`eo-hull-deficit` §2) | yes | **Yes, with the side condition $t_U+t_V\le a$ checked at every use.** Without it the lemma is false, not just unproven — 660 explicit counterexamples |
| **Barrier Theorem 6, at integer $a$** (`eo-hull-deficit` §6) | yes | **Yes for integer $a$ and worst-case charging.** Not for non-convex $K$ (explicit counterexample), not for configuration-dependent counts |
| **"Convex-cut relaxations are dead at $a<6$"** | no | **NO — do not build on this** (D5). There is no barrier theorem below integer side. If a route was killed on it, reopen it |
| **Theorem 6's equality characterisation** | no | **NO** (D2) — the equality family is every lattice line, not just corner triangles |
| **Prop 5's "break-even at every integer scale"** | no | **NO** (D3). Prop 5's headline (gain $<0$, sup $0$ at $t\to1^-$) is fine |
| **Partition identity** (`eo-exhaustion` §3 lemma) | yes | **Yes**, with the omitted hypotheses: full-dimensional pieces, $I$ excluding $\partial P$ |
| **"Every partition-and-count refinement is dead"** | no | **NO — this is the most damaging item in this report** (D1). It is refuted by the repo's own EO(3) proof. Any route killed on it should be reopened |
| **Exhaustion §1, narrow form** | yes | **Yes**: no finite family of rational-side refutations closes it |
| **Exhaustion §1, broad form** ("no exhaustion, ever") | no | **NO** (D4). Finite arguments uniform in $d$ work, and exhaustion-plus-closing-argument is untouched |
| **$k=3$ proof / subdivision lemma** (`eo-small-cases` §1–2) | yes | **Yes.** Cleanest result of the day. Keep the strict $a<m$ |
| **§4.1 / §4.2 counting identities** | yes | **Yes.** "Oler must be improved by exactly one point, for every $k$" is exact |

---

## 9. Honest accounting

**Not checked at all** — no opinion is offered on any of these, and none of them was read for the
claims above:

- **Oler's inequality itself.** Taken as `cited` throughout. I did not re-derive it and cannot.
- Every author's **code**. Problem `RULES.md` §3 required me to reimplement from the statement, and
  I did; I did not read, import or run `packing-eo-hull-deficit`, `packing-eo-small-cases` or
  `packing-eo-exhaustion`. The only file I read from another experiment is
  `packing-oler-slack/exact.py`, for the `sqrt_bounds` idea, as the brief permitted.
- The **`numerical` rows** of `eo-exhaustion` §4 (the measured wall) and §5's resolution theorem.
- [`../eo-boundary-counting/`](../eo-boundary-counting/),
  [`../oler-slack-analysis/`](../oler-slack-analysis/),
  [`../eo-literature/`](../eo-literature/) — not examined this pass.
- **Novelty.** I have no view on whether any of these lemmas is in Payan (1997) or
  Folkman–Graham. `eo-hull-deficit` §10's advice — assume they are known — looks right to me.

**Where my own check is weakest.** Claim 2's $\varepsilon$-bookkeeping is the step I would most
like a different model family to look at, precisely because I got it wrong on the first pass and
the corrected version is the one everything downstream uses. Claim 4's *interpretation* (what the
theorem does and does not kill) is a judgement about arguments rather than a theorem, and
judgements are where two same-family models agree for bad reasons.

**What would settle these properly.** Cross-family review by Codex, and — for Claims 1, 3, 4, 5,
all of which are finite exact statements — Lean. Claim 5 in particular (a covering argument over
$m^2$ triangles with an exact diameter bound) looks formalisable with no Mathlib gap worth
mentioning, and it would give the repo its first machine-checked Erdős–Oler case.

## 10. Reproducing

```
experiments/packing-eo-verify/run.sh
```

Standard library only, exact arithmetic (a formal-sum-of-square-roots field with exact equality and
an exact sign test), no seeds affecting any verdict, no tolerance anywhere. 101 checks; exits
non-zero if any fails.
