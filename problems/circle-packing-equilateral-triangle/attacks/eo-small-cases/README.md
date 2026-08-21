# Attack: reconstructing the proven Erdős–Oler cases, and where the method dies

**Claim type: lower bound (optimality direction), for one case only.** One case is proved
($k = 3$); one is not ($k = 4$); one was not attempted ($k = 5$). Problem
[`../../RULES.md`](../RULES.md) §1 asks which of the two kinds of statement this is: it is the
**hard** kind, $s(n) \ge c$, which is why only the smallest case falls.

**This is a reconstruction, not a discovery.** $k \le 6$ is published (Melissen 1993, Payan 1997);
the point is to give this project a proof it can actually check, since every Erdős–Oler case the
repo cites rests on a paper nobody here has read — and, per
[`../eo-literature/`](../eo-literature/), nobody here *can* read this session. Nothing below is
offered as novel.

- Author: `claude` (Claude Opus 5 — convergent role, repo `RULES.md` §8: this is checking and
  exact calculation), 2026-08-21
- Branch: `claude/circle-equklatetal-problem-sa7tx7`
- Code: [`experiments/packing-eo-small-cases/`](../../../../experiments/packing-eo-small-cases/) —
  one command, Python standard library only, exact $\mathbb{Q}(\sqrt3)$ / $\mathbb{Q}(\sqrt{33})$
  arithmetic throughout. **No float decides anything.**

| What | Status |
|---|---|
| §1 the subdivision lemma | `sketch` — my proof; elementary, but not cross-examined and **not assumable, including by me** |
| §2 EO for $k = 3$ ($n = 5$, $a < 2$) | `sketch` (the *result* is `cited` from the literature; this proof of it is not) |
| §2 the $n = 5$ and $n = 6$ witnesses at $a = 2$ | `numerical` — exact, explicit configurations |
| §3 EO for $k = 4$ ($n = 9$, $a < 3$) | **NOT PROVED** — stalled, obstruction identified |
| §3 the row-capacity witnesses at $a = 2.7$ | `numerical` — exact; they **refute** the decomposition route |
| §4 the scaling analysis | `sketch` — arithmetic on top of Oler (`cited`) |
| Oler's inequality | `cited` — Oler 1961, via [`../oler-lower-bound/`](../oler-lower-bound/) |

**Kill-criterion, stated before starting** (repo `RULES.md` §6.2), and its outcome:

> (a) *If $k = 3$ does not fall to an elementary argument quickly, report and stop.* — **not met**,
> it fell immediately (§1–2).
>
> (b) *For $k = 4$: if after exhausting the dissection, strip and nested-small-case routes the
> shortfall turns out to be structural — the same deficit recurring for a reason I can state —
> rather than a matter of more effort, stop and report the obstruction.* — **MET, §3.** Four
> independent decompositions all give capacity exactly 9 where 8 is needed, and §3.4 says why that
> is not a coincidence. I stopped rather than re-scoping.

**Normalisation.** Separation 1 throughout: $n$ points at pairwise distance $\ge 1$ in the closed
equilateral triangle $T_a$ of side $a$. Write $a_n$ for the least such $a$, and
$\Delta(k) = k(k+1)/2$. Erdős–Oler for $k$ is the statement $a_{\Delta(k)-1} = k-1$; since
$a_{\Delta(k)} = k-1$ is Oler's theorem, the content is the lower bound

> **EO($k$).** $n = \Delta(k) - 1$ points at separation $\ge 1$ do not fit in $T_a$ for any
> $a < k-1$.

$k = 7$ is $n = 27$, $a < 6$. (The repo's certificates use separation 2 and side $2a$.)

---

## 1. The subdivision lemma — `sketch`

> **Lemma.** Let $m \ge 1$ be an integer. If $a < m$, then any set of points in $T_a$ with pairwise
> distances $\ge 1$ has at most $m^2$ elements.

**Proof.** Subdivide $T_a$ by the lines parallel to its three sides through the points dividing
each side into $m$ equal parts. This gives $m^2$ closed equilateral cells of side $a/m$ — $\binom{m+1}{2}$
upward and $\binom{m}{2}$ downward, and $\binom{m+1}{2} + \binom{m}{2} = m^2$ — whose union is
$T_a$. Each cell is an equilateral triangle of side $a/m < 1$, hence has diameter $a/m < 1$, so it
contains at most one of the points: two distinct points in one cell would be at distance
$\le a/m < 1$. Every point lies in at least one cell, so $n \le m^2$. $\blacksquare$

Two remarks, both used below.

- The lemma is **strict in $a$ and closed in the cells**; that is the whole content. At $a = m$ it
  says nothing, and it must not, since $\Delta(m+1) > m^2$ points fit at $a = m$ for $m \le 3$.
- Contrapositive form: $n > m^2 \Rightarrow a \ge m$.

**Bonus, checked in §1 of the transcript.** The same lemma re-proves Oler's triangular-number case
without Oler, exactly when $\Delta(k) > (k-1)^2$, i.e. **for $k \le 4$**. So this repo now has a
self-contained proof of $a_{\Delta(k)} = k-1$ for $k \le 4$ (lower bound from the lemma, upper
bound from the lattice configuration), independent of the Oler paper.

## 2. EO($3$): $n = 5$, $a < 2$ — proved

> **Proposition.** Five points at pairwise distance $\ge 1$ do not fit in $T_a$ for $a < 2$; hence
> $a_5 = 2 = a_6$, which is EO($3$).

**Proof.** Apply the Lemma with $m = 2$: if $a < 2$ then $n \le 4 < 5$. So $a_5 \ge 2$. Conversely
the five points
$$(0,0),\ (1,0),\ (2,0),\ \left(\tfrac12, \tfrac{\sqrt3}{2}\right),\ \left(\tfrac32,\tfrac{\sqrt3}{2}\right)$$
lie in $T_2$ with all pairwise distances $\ge 1$ (minimum exactly 1), so $a_5 \le 2$. Adding the
apex $(1,\sqrt3)$ keeps every distance $\ge 1$, so $a_6 \le 2$; and $a_6 \ge a_5 = 2$. Hence
$a_5 = a_6 = 2$. $\blacksquare$

Both configurations are verified exactly in §2 of the transcript (all $\binom{n}{2}$ squared
distances, and all three half-plane containments, over $\mathbb{Q}(\sqrt3)$).

**Worth noting: Oler cannot do this.** Oler gives $a \ge (\sqrt{8n+1}-3)/2$, which at $n = 5$ is
$1.7016$ — short of 2 by 0.30. The four-cell pigeonhole beats it. That is the *only* $n$ in this
family where it does.

## 3. EO($4$): $n = 9$, $a < 3$ — NOT PROVED, and the obstruction

The Lemma with $m = 3$ gives $n \le 9$ for $a < 3$. **That is exactly one point too many.** Oler
gives $a \ge 2.7720$ for $n = 9$, also short of 3. Everything below is the attempt to find the
missing point, and the reason it did not work.

Throughout, $a < 3$ and $h = a/3 < 1$; the reference value for the exact witnesses is
$a = \tfrac{27}{10}$, $h = \tfrac{9}{10}$.

### 3.1 What the pigeonhole does buy: a rigid structure

With $m = 3$ there are 9 cells and 9 points, each cell holding at most one. Since the cells cover
$T_a$, every point lies in at least one, so counting incidences both ways gives exactly 9: **each
cell contains exactly one point, and no point lies on an edge shared by two cells.** (Points may
lie on $\partial T_a$, whose edges belong to one cell each.) In particular the three rows of the
subdivision contain exactly 5, 3 and 1 points from the bottom up.

This is genuinely strong structure — it confines each point to a specific triangle of side $h$ —
and it is still not enough.

### 3.2 The row decomposition is at capacity — `numerical`, and it **refutes** the route

The obvious next move is to bound each row separately and hope one of them cannot be full. It
cannot: **both non-trivial rows are exactly at capacity for $a < 3$.** Exact witnesses at
$a = \tfrac{27}{10}$, all coordinates in $\mathbb{Q}(\sqrt3)$, verified in §3 of the transcript:

**Bottom row** (the trapezoid $0 \le y \le \tfrac{\sqrt3}{2}h$), five points:
$$(0,0),\quad \left(\tfrac{27}{20},0\right),\quad \left(\tfrac{27}{10},0\right),\quad
\left(\tfrac{7}{10}, \tfrac{9\sqrt3}{20}\right),\quad \left(2, \tfrac{9\sqrt3}{20}\right).$$
Minimum squared distance $\tfrac{412}{400} = 1.03 > 1$.

**Middle row** (the trapezoid $\tfrac{\sqrt3}{2}h \le y \le \sqrt3 h$), three points:
$$\left(\tfrac{9}{20}, \tfrac{9\sqrt3}{20}\right),\quad \left(\tfrac{45}{20},\tfrac{9\sqrt3}{20}\right),
\quad \left(\tfrac{27}{20}, \tfrac{9\sqrt3}{10}\right).$$
Minimum squared distance $\tfrac{567}{400} = 1.4175 > 1$.

So row capacities are $5 + 3 + 1 = 9$, attained termwise, at $a = 2.7 < 3$. **Any argument that
partitions $T_a$ and sums per-part capacities is therefore capped at 9 for this partition, and
cannot reach 8.** Three other decompositions do exactly the same:

| decomposition of $T_a$, $a<3$ | capacities | total |
|---|---|---|
| three rows | $5 + 3 + 1$ | **9** |
| bottom row + top sub-triangle of side $2h < 2$ | $5 + 4$ (the 4 by §2, since $2h < 2 = a_5$) | **9** |
| bottom two rows + top cell | $8 + 1$ | **9** |
| uniform 9-cell subdivision | $1 \times 9$ | **9** |

Every one lands on 9. **The missing point is an interaction term**, and a partition-plus-capacity
argument discards exactly that by construction. The transcript makes this concrete: the bottom-row
and middle-row witnesses above are each individually valid and are **jointly infeasible** — four
cross pairs fall below separation 1, the closest at squared distance $\tfrac{1}{16}$.

### 3.3 The general-dissection route needs an *optimal covering*

Weakening "partition" to "cover by sets of capacity 1" is the natural generalisation: if $T_a$ is
covered by $N$ sets of diameter $< 1$, then $n \le N$. To prove EO($k$) this way one needs
$N \le \Delta(k) - 2$ pieces. How much room is there? None:

> If $T_a$ is covered by $N$ sets of diameter $<1$, then $N \ge n^*(a)$, where $n^*(a)$ is the
> maximum number of points of $T_a$ at pairwise distance **strictly** $> 1$ — because no two of
> them can share a piece. And $n^*(a) = \max\{n : a_n < a\}$, by scaling.

Verified exactly (§5 of the transcript) from the repo's `cited` $a_n$ values:
$n^*(a) = \Delta(k)-2$ for $a$ just below $k-1$, at $k = 3$ (via $a_4 = \sqrt3 < 2$) and $k = 4$
(via $a_8 = 1 + \tfrac{\sqrt{33}}{3} = 2.9149 < 3$).

**So the number of pieces the method needs is exactly the minimum conceivable.** The dissection
must be an *optimal* covering of $T_a$ by diameter-$<1$ sets, with no slack at all. At $k = 3$ that
optimum is 4 and the trivial subdivision achieves it — which is why §2 is three lines. At $k = 4$
the optimum would have to be 8, and I could not construct it.

### 3.4 The best covering I found also gives 9 — `numerical`

Rescaled to side 3, the natural construction is: the three **corner sectors** $\{|P-V|\le1\}$ —
a $60°$ sector of radius 1 has diameter exactly 1, and is the *largest* diameter-1 set containing
the corner — plus three **Reuleaux triangles**, one on each edge's middle unit segment together
with the centroid. Those six sets are maximal among diameter-1 sets meeting the boundary, and they
cover the whole boundary.

They leave three uncovered points, verified exactly (§6 of the transcript):
$$\left(\tfrac32,\tfrac32\right),\quad
\left(\tfrac94 - \tfrac{3\sqrt3}{4},\ \tfrac{3\sqrt3}{4}-\tfrac34\right),\quad
\left(\tfrac34 + \tfrac{3\sqrt3}{4},\ \tfrac{3\sqrt3}{4}-\tfrac34\right),$$
pairwise at squared distance $9 - \tfrac{9\sqrt3}{2} = 1.2058 > 1$. Three mutually-far gaps need
three more pieces: **6 + 3 = 9 again.**

**Honest limit.** This is a proof only in the regime where each edge is met by exactly three
pieces, which is what forces every boundary piece inside one of the six maximal sets. Outside that
regime I have no bound. **So I have not proved that 8 pieces are impossible** — only that four
partitions and the best cover I could construct all land on 9. Whether
$T_3$ admits a cover by 8 sets of diameter $\le 1$ is, to me, open; if it does, EO($4$) follows
immediately by scaling.

### 3.5 Routes tried and their exact yields

| route | best lower bound on $a$ for $n=9$ | verdict |
|---|---|---|
| uniform subdivision, $m=3$ | $a \ge 2$ (from $9 > 2^2$) | too weak |
| Oler on the containing triangle | $a \ge \tfrac{\sqrt{73}-3}{2} = 2.7720$ | too weak by $0.228$ |
| three-row / two-piece decompositions | none — capacity 9 | **refuted**, §3.2 |
| nested small case: each corner sub-triangle of side $2h$ holds 4 points, so $2h \ge a_4 = \sqrt3$ | $a \ge \tfrac{3\sqrt3}{2} = 2.598$ | weaker than Oler |
| 8-piece diameter-$<1$ cover | would prove it outright | **not constructed**, §3.4 |

Best proved: $a \ge 2.7720$, from Oler. **EO($4$) is not proved here.** $k = 5$ was not attempted;
the manager's plan made it conditional on $k = 4$ landing.

## 4. The part that is actionable for Provers A and B — `sketch`

### 4.1 The subdivision method's deficit grows quadratically, and it is 10 at $k = 7$

EO($k$) needs $n \le \Delta(k)-2$ at $a < k-1$; the Lemma with $m = k-1$ delivers $n \le (k-1)^2$.
Exactly (§1 of the transcript, all $k$):
$$(k-1)^2 - \bigl(\Delta(k)-2\bigr) \;=\; \frac{(k-2)(k-3)}{2}.$$
This is $\le 0$ **iff $k \le 3$**. So the pigeonhole is not "weak for large $k$" — it is exactly
sufficient for $k \le 3$ and fails for every $k \ge 4$, by

| $k$ | 3 | 4 | 5 | 6 | **7** | 8 |
|---|---:|---:|---:|---:|---:|---:|
| pieces needed $\Delta(k)-2$ | 4 | 8 | 13 | 19 | **26** | 34 |
| uniform subdivision gives $(k-1)^2$ | 4 | 9 | 16 | 25 | **36** | 49 |
| deficit | 0 | 1 | 3 | 6 | **10** | 15 |

**At $k = 7$ the uniform dissection overshoots by 10 pieces.** Anyone reaching for a pigeonhole
argument on 27 points should know it starts ten short, not one.

### 4.2 The unit that must be found is scale-free — this is the load-bearing observation

Oler gives $n \le \tfrac{a^2}{2} + \tfrac{3a}{2} + 1$. Substituting $a = k-1$ gives **exactly**
$\Delta(k)$ — verified as an exact rational identity for every $k$ in §4 of the transcript. Hence
as $a \to (k-1)^-$ Oler permits $\Delta(k)-1$ points, and EO needs $\Delta(k)-2$:

> **For every $k$, Oler must be improved by exactly one point. Not by a factor, not by an amount
> that depends on $k$ — by 1.**

Meanwhile the corresponding gap *in $a$* collapses:
$$ (k-1) - \frac{\sqrt{(2k+1)^2-8}-3}{2} \;=\; \frac{(2k+1)-\sqrt{(2k+1)^2-8}}{2} \;\sim\; \frac{2}{2k+1}.$$

| $k$ | 3 | 4 | 5 | 6 | **7** | 8 |
|---|---:|---:|---:|---:|---:|---:|
| Oler's $a$-bound for $n=\Delta(k)-1$ | 1.7016 | 2.7720 | 3.8151 | 4.8443 | **5.8655** | 6.8815 |
| target $k-1$ | 2 | 3 | 4 | 5 | **6** | 7 |
| gap in $a$ | 0.2984 | 0.2280 | 0.1849 | 0.1557 | **0.1345** | 0.1185 |
| gap in points | 1 | 1 | 1 | 1 | **1** | 1 |

**Two consequences for the two live routes.**

1. **A mechanism whose yield scales with $k$ is the wrong shape.** Anything proportional to the
   boundary ($\propto k$), to the area ($\propto k^2$), or to the number of corners times something
   $k$-dependent, will either be far too weak at $k = 7$ or would prove more than is true at
   $k = 3$. The correct mechanism produces $+1$ and stops. The one structure in this problem with
   that signature is the **three corners**, contributing a bounded amount — which is consistent
   with [`../oler-slack-analysis/`](../oler-slack-analysis/) §3 finding stage-2 loss exactly 1 at
   every $n = \Delta(k)-1$ it measured, $k = 3,4,5,6$.
2. **Being close in $a$ is not being close.** At $k = 7$ Oler is within $0.135$ of the target and
   this looks like a small push. It is not: it is the same one point as at $k = 3$, where the gap
   in $a$ is more than twice as large. Progress should be measured in points, never in side length.

### 4.3 A negative result worth having

Prover B's boundary-counting route should note §3.2 concretely: at $a = 2.7$ the bottom row of the
3-subdivision *does* hold 5 points and the middle row *does* hold 3, so any count that treats rows
(or any partition) independently is provably capped at $\Delta(k)-1$ and can never reach
$\Delta(k)-2$. The exact witnesses are in the transcript and are cheap to re-check. Whatever
supplies the missing unit has to be a statement about **two regions at once**.

## 5. Reproducing

```
python3 experiments/packing-eo-small-cases/check.py
```

Standard library only; exact $\mathbb{Q}(\sqrt3)$ and $\mathbb{Q}(\sqrt{33})$ arithmetic with an
exact sign test; no seeds, no tolerances, no floats in any decision. Exits non-zero if any check
fails. 44 checks, all passing at the time of writing.

## 6. What to review hardest

- **§1's cell count** $\binom{m+1}{2} + \binom{m}{2} = m^2$ and the claim that the cells cover
  $T_a$ — everything rests on it, and it is the step where an off-by-one would be invisible.
- **§1's strictness**: the lemma needs $a < m$, not $a \le m$. If that slipped, §2 would prove
  something false.
- **§3.3's duality**, $N \ge n^*(a)$ and $n^*(a) = \max\{n : a_n < a\}$ — the scaling argument in
  both directions, and the fact that it uses only $a_n$ for $n \le 8$, so it is **not** circular
  with EO($4$).
- **§4.2's identity** that Oler's bound at $a = k-1$ is exactly $\Delta(k)$. It is the basis of the
  "exactly one point" claim, which is the main thing I am asking the other provers to act on.
