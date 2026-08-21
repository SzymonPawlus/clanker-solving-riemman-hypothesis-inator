# Erdős–Oler by exhaustion: where the wall is, measured

**Outcome: the attack is `refuted` as a route to $k = 7$, and the refutation is the deliverable.**
A finite exhaustion at rational side lengths cannot prove Erdős–Oler at *any* $k$ — not for want of
compute, but for a structural reason given in §1 — and the measured cost curve says how far a
cell-based exhaustion actually gets on the family. Everything computational here is `numerical`;
the derivations in §1, §3 and §5 are `sketch`; the only `cited` input is Oler's inequality.

Code and reproduction: [`experiments/packing-eo-exhaustion/`](../../../../experiments/packing-eo-exhaustion/).

**Nothing in this file is assumable** (repo `RULES.md` §3).

---

## 0. What was targeted, and why

The hypothesis under attack is Erdős–Oler at the first open case: **27 points at pairwise distance
$\ge 1$ do not fit in a closed equilateral triangle of side $a < 6$.** In this repo's separation-2
normalisation that is $d(27) \ge 12$, with $d = 2a$; the factor of 2 is the most likely source of
error in anything written about this problem and every number below is in $d$ unless it says
otherwise.

Two theory routes are being run by other workers. The computational question is narrower and
answerable: **how much of the remaining gap can rigorous exhaustion actually eat?** That question
has a definite answer, it is cheap to get wrong by measuring the wrong $n$, and the existing
branch-and-bound in the repo measured $n = 12$ and $n = 16$ — neither an Erdős–Oler case.

## 1. The structural obstruction — no exhaustion can finish this

`refuted`, and this is the most important paragraph in the file.

An exhaustion refutes $n$ points at **one explicit rational** $d$, giving $d(n) > d$. Erdős–Oler
at $k$ asserts $d(T(k)-1) \ge 2(k-1)$, i.e. refutation at *every* $d < 2(k-1)$. Those are not the
same kind of statement, and no finite family of the first implies the second, because the
configuration space at $d = 2(k-1)$ exactly is **non-empty**: delete any point from the $k$-row
lattice packing. So the sets

$$S(\varepsilon) \;=\; \{\text{configurations of } T(k)-1 \text{ points at separation} \ge 2 \text{ in } T(2(k-1)-\varepsilon)\}$$

shrink as $\varepsilon$ grows and their "limit" $\bigcap_{\varepsilon>0}$ is the non-empty
$S(0)$. Refuting $S(\varepsilon)$ for one $\varepsilon$ — or for a thousand — never reaches
$\varepsilon = 0$. **Shrinking $\varepsilon$ narrows an enclosure; it never closes it, and there is
no limiting run.**

The scaling restatement makes the same point sharper. $d(n) < 2(k-1)$ holds iff there are
$T(k)-1$ points in $T(2(k-1))$ at separation **strictly** greater than 2. So the conjecture is
"the maximum separation of $T(k)-1$ points in the side-$2(k-1)$ triangle is exactly 2", an
attained-maximum statement. Exhaustion refutes open conditions; this one is closed.

**Consequence for the team.** Any proof of Erdős–Oler at $k=7$ must contain a step that is uniform
in $d$ — a counting or structural argument — and a computation can only ever be a finite case
analysis *inside* such an argument. Budgeting compute at the whole conjecture is budgeting at
something the method cannot reach.

*One exception, recorded because it is the only case where a cell argument is uniform:* for
$k \le 3$ the refutation is uniform in $d$. For every $d < 4$ the four level-1 cells have side
$d/2 < 2$, so each holds at most one point and $5 > 4$ points cannot be placed. That proves
$d(5) \ge 4$ outright — the full $k=3$ case (known: Melissen 1993). It generalises to
"$4^L$ cells of side $d/2^L < 2$" only while $4^{\lfloor\log_2(k-1)\rfloor} < T(k)-1$, which fails
from $k = 4$ on.

## 2. The bar: what Oler already gives for free

Oler's inequality (`cited`) gives $d(n) > \sqrt{8n+1} - 3$ with no computation at all
(`attacks/oler-lower-bound/` §2.2). At $n = T(k)-1$ this is $d > \sqrt{4k^2+4k-7} - 3$, so the
**exact residual gap** Erdős–Oler leaves for any further argument is

$$\boxed{\,(2k+1) \;-\; \sqrt{4k^2+4k-7} \;=\; \frac{8}{(2k+1)+\sqrt{4k^2+4k-7}} \;\sim\; \frac{2}{2k+1}\,}$$

in $d$, i.e. $\sim 1/(2k+1)$ in the separation-1 side $a$. (`sketch` — elementary algebra, mine.)
Numerically, from `python3 -m eoex gap --kmax 12`:

| $k$ | $n = T(k)-1$ | target $d$ | Oler gives $d >$ | residual gap | $\rho_{\text{Oler}} = $ fraction certified |
|---:|---:|---:|---:|---:|---:|
| 3 | 5 | 4 | 3.4031242 | 0.5968758 | 0.85078 |
| 4 | 9 | 6 | 5.5440037 | 0.4559963 | 0.92400 |
| 5 | 14 | 8 | 7.6301458 | 0.3698542 | 0.95377 |
| 6 | 20 | 10 | 9.6885775 | 0.3114225 | 0.96886 |
| **7** | **27** | **12** | **11.7309199** | **0.2690801** | **0.97758** |
| 8 | 35 | 14 | 13.7630546 | 0.2369454 | 0.98308 |
| 12 | 77 | 22 | 21.8394847 | 0.1605153 | 0.99270 |

**Two readings, and the second is the one that matters.**

*Encouraging:* the gap **shrinks** with $k$, absolutely and relatively. At $k = 7$ Oler is already
within 2.24 % of the conjecture, and at $k=12$ within 0.73 %. Erdős–Oler is a $\sim 1/(2k+1)$
correction to a `cited` theorem, not a wide-open question.

*Sobering:* the gap is exactly the "$-1$" in $T(k)-1$. Applying Oler to the container gives
$N \le (a+1)(a+2)/2$, which equals $T(k)$ exactly at $a = k-1$ — so Oler *proves* the triangular
case $n = T(k)$ and misses $n = T(k)-1$ by one unit of count. That single unit is the entire
conjecture, and it does not get easier as $k$ grows; it merely translates into a smaller and
smaller slice of side length, which is *worse* for any method whose cost blows up as the slice
narrows. This is consistent with `experiments/packing-oler-slack/`, which measures the hull-level
Oler bound as **exactly tight** at $n = T(k)-1$, with the whole deficit of 1 sitting in the
hull → triangle relaxation.

**An exhaustion contributes nothing at all unless it certifies a ratio above
$\rho_{\text{Oler}}$.** That is the bar, and it is worth stating because the repo has already paid
for a run that did not clear it: `experiments/circle-packing-bnb` certified $d(16) > 7.999$ at a
cost of CPU-hours, while Oler's one-line closed form gives $d(16) > \sqrt{129}-3 = 8.3578\ldots$
for free. The prover in `packing-eo-exhaustion` therefore applies Oler at its root unconditionally,
so no run of it can be weaker than Oler.

## 3. A dead end worth writing down: subdividing into regions always loses

`sketch`. The natural pigeonhole strengthening — cut the triangle into convex pieces, cap each
piece by Oler, add up — is **strictly worse than Oler on the whole triangle, always**, so it can
never close the gap of §2. It is a natural enough idea that it should be recorded as closed.

> **Lemma.** Let a convex region $P$ be partitioned into convex pieces $P_1,\dots,P_m$, and write
> $\Omega(R) = \frac{2}{\sqrt3}A(R) + \frac12 M(R) + 1$ for Oler's bound on a region $R$ (points at
> separation $\ge 1$). Let $I$ be the total length of the internal cuts. Then
> $$\sum_{i=1}^m \Omega(P_i) \;=\; \Omega(P) \;+\; I \;+\; (m-1).$$

*Proof.* Areas are additive: $\sum A(P_i) = A(P)$. Each internal cut lies on the boundary of
exactly two pieces, so $\sum M(P_i) = M(P) + 2I$. The constant $1$ is paid $m$ times instead of
once. $\square$

So a partition pigeonhole loses exactly $I + (m-1)$: one unit per extra piece, plus the internal
boundary. Since the deficit to be recovered at $n = T(k)-1$ is exactly $1$ (§2), *any* partition
into two or more pieces already gives back more than the whole budget. Concretely, cutting $T(a)$
into $k$ horizontal strips by the similar-triangle cuts loses $(k-1)(a/2+1)$ — at $k=7$, $a=6$,
that is 24, against a budget of 1.

The same accounting is why the cell-capacity rule inside a branch and bound is weak in the tight
regime: capacity rules are pigeonhole rules on a partition. What *can* help is a bound applied to
the configuration's own hull (which pays the $+1$ once and has no internal cuts) — which is what
the Oler-hull rule in the experiment does, and what the hull-corner-deficit route is about.

## 4. The measured wall

`numerical`. Exact integer/rational exhaustion, one CPU core each, CPython 3.11,
four searches concurrent on a 4-core box (so seconds are upper bounds). $\rho = d/2(k-1)$ is the
fraction of the conjectured value that the run certifies; a run only says something new when
$\rho > \rho_{\text{Oler}}$.

| $k$ | $n$ | best $d$ **proved** | $\rho$ | vs $\rho_{\text{Oler}}$ | nodes | s |
|---:|---:|---:|---:|:--|---:|---:|
| 3 | 5 | *every* $d<4$ | $\to 1$ | settled outright | 1 | 0.0 |
| 4 | 9 | $59/10 = 5.9$ | 0.98333 | **beats** 0.92400 | 684 342 | 12 |
| 5 | 14 | $799/100 = 7.99$ | 0.99875 | **beats** 0.95377 | 4 241 969 | 98 |
| 6 | 20 | **none above Oler** | — | fails at $\rho = 0.970$ | 8 368 128 (timeout) | 400 |
| 7 | 27 | **none above Oler** | — | fails at $\rho = 0.978$ | 13 210 624 (timeout) | 400 |

**The wall sits between $k = 5$ and $k = 6$.** Below it the exhaustion is strictly stronger than
Oler; at and above it, Oler's one-line closed form is strictly stronger than everything the
exhaustion produced, and the $k=6,7$ rows prove nothing whatsoever. Seven attempts spanning
$d = 9.7\text{–}9.75$ ($k=6$) and $d = 11.74\text{–}11.75$ ($k=7$), at up to 400 s each and
$1.3\times10^7$ nodes, all timed out with a non-empty frontier.

Each `proved` row is a genuine finite exhaustion: e.g. $d(14) > 7.95$, hence
$s(14) > 7.95 + 2\sqrt3 = 11.414\ldots$ against the `cited` $s(14) = 8+2\sqrt3 = 11.464\ldots$.
These are correct and weak — and, note, **consistent with** the literature values, which is the
point of running them.

Two observations about the shape of the curve, because they are easy to misread:

* **$\rho$ is not monotone in $k$.** It depends on whether $2(k-1)$ sits just above a power of two,
  because the cheap regime is "cells of side $d/2^L < 2$", i.e. $d < 2^{L+1}$. At $k=5$
  ($d < 8 = 2^3$) level 2 already forces 14 points into 16 cells of side $<2$, which is why $k=5$
  reaches a *higher* $\rho$ than $k=4$. Reading the sequence 0.983, 0.994 as improvement with $k$
  would be wrong.
* **The bar rises faster than the achievement.** $\rho_{\text{Oler}}$ climbs 0.924 → 0.954 → 0.969
  → 0.978, and the residual slice of $d$ that an exhaustion must cover shrinks like $2/(2k+1)$
  while the number of points grows like $k^2/2$. Both move the wrong way at once.

## 5. The resolution theorem — why the cost diverges

`sketch` (my derivation). This makes "the cost explodes" a number instead of an impression.

> **Claim.** Suppose every cell of a surviving search node is at level $L$, with side
> $h = d/2^L < 2$ (so all multiplicities are 1 and there are exactly $n$ cells), and the node
> survives the pairwise test. Then $T(d)$ contains $n$ points at pairwise distance
> $\ge 2 - 2h/\sqrt3$, and hence $d \ge d(n)\,(1 - h/\sqrt3)$.

*Proof.* Take the cell centroids $g_i \in T(d)$. An equilateral triangle of side $h$ has
circumradius $h/\sqrt3$, so for $x \in c_i$, $y \in c_j$ we have
$|x - y| \le h/\sqrt3 + |g_i - g_j| + h/\sqrt3$, giving
$|g_i - g_j| \ge \operatorname{maxsep}(c_i, c_j) - 2h/\sqrt3 \ge 2 - 2h/\sqrt3$. Scaling by
$2/(2 - 2h/\sqrt3)$ places $n$ points at separation $\ge 2$ in a triangle of side
$d/(1 - h/\sqrt3)$, which must therefore be at least $d(n)$. $\square$

Contrapositive: a cell exhaustion can only close at ratio $\rho = d/d(n)$ once
$h < \sqrt3\,(1-\rho)$, i.e. at level

$$2^L \;>\; \frac{d}{\sqrt3\,(1-\rho)} \;\longrightarrow\; \infty \quad \text{as } \rho \to 1 .$$

For $k = 7$ ($n = 27$, $d(n) = 12$ assumed **only to size the computation**), from
`python3 -m eoex levels --kmax 7 --ratios 0.9 0.95 0.99 0.999`:

| $\rho$ | 0.90 | 0.95 | $\rho_{\text{Oler}} = 0.9776$ | 0.99 | 0.999 | $\to 1$ |
|---|---:|---:|---:|---:|---:|---:|
| level $L$ needed | 6 | 8 | 9 | 10 | 13 | $\infty$ |
| cells $4^L$ | 4 096 | 65 536 | 262 144 | 1 048 576 | $6.7\times10^7$ | — |

At $k = 7$ the search must place 27 points into a subdivision with $\ge 2.6 \times 10^5$ cells
merely to **match** a bound Oler gives in one line, and the level — hence the branching depth and
the number of ways to distribute points among cells — grows without bound as the conjecture is
approached. There is no budget at which this terminates.

## 6. The honest distance from $k = 7$

1. **Qualitatively: infinite.** §1. No amount of compute converts a rational-side exhaustion into
   the conjecture, so "distance" measured in CPU-hours is the wrong axis.
2. **Against the achievable sub-goal** — beating Oler at $k=7$, i.e. certifying
   $d(27) > 11.7309\ldots$ — the answer is that this implementation does not, and the wall is
   located: it sits between $k=5$ (which clears Oler comfortably, $\rho = 0.99875$ in 98 s) and
   $k=6$ (which does not clear it at all in 400 s). At $k=7$, $d = 11.74$, the search burned
   $1.3\times10^7$ nodes at $3.3\times10^4$ nodes/s and stopped with 138 branches still on the
   frontier — not close. §5 says it needs level $\ge 9$, i.e. a subdivision with
   $\ge 2.6\times10^5$ cells, merely to *match* a bound Oler gives in one line. No extrapolation
   from the $k \le 5$ node counts is offered, because the branching factor at 27 points is a
   different regime from 14 and an extrapolated exponent would be a guess dressed as a
   measurement.
3. **The useful residue** is not a bound at all: it is the exact statement of *what remains*.
   Erdős–Oler at $k$ is Oler's inequality plus a recovery of exactly **one unit of count**, worth
   exactly $(2k+1)-\sqrt{4k^2+4k-7} \approx 0.269$ in $d$ at $k=7$; §3 shows the recovery cannot
   come from any partition-and-count refinement; and `packing-oler-slack` locates the whole deficit
   in the hull → triangle relaxation. That triple is a precise specification of the theorem the
   theory routes have to prove.

## 7. Kill-criterion

Stated before the runs: *if the exhaustion cannot certify $\rho > \rho_{\text{Oler}}$ at
$k = 5$ within a 7-minute single-core budget, the method adds nothing anywhere and $k = 6,7$ get
one confirming probe each rather than a campaign.*

**It did not fire at $k=5$** — $\rho = 0.99375$ was certified in 40 s, comfortably above
$\rho_{\text{Oler}} = 0.95377$. The attack is nevertheless recorded as `refuted` **as a route to
$k=7$**, on §1, which is a structural fact and not a budget observation. §6.3 is what survives.

## 8. What a reviewer should attack

1. **The branching is exhaustive** — that the four children of a cell are closed and cover it.
   A wrong child set gives false `proved` verdicts everywhere while passing most tests. It is
   derived in the experiment's `eoex/lattice.py` docstring and checked only by sampling.
2. **§1** — whether the structural obstruction is really structural, or whether some
   compactness/rational-approximation argument converts finitely many rational refutations into
   the closed statement. I claim not, on the non-emptiness of $S(0)$; this is the step to break.
3. **§3 and §5** — both are mine, both are elementary, neither has been cross-examined.
4. **The separation-1 / separation-2 normalisation** everywhere. Oler is stated at separation 1;
   this problem's certificates use separation 2.
