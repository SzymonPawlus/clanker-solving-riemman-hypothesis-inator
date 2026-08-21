# Erdős–Oler by exhaustion: where the wall is, measured

**Outcome: the *specific* attack — pushing fixed-rational-side exhaustions toward $2(k-1)$ — is
`refuted` as a complete route, and the measured wall is the deliverable.** A finite family of
refutations at fixed rational sides cannot, on its own, prove Erdős–Oler at any $k$ (§1.1, by
monotonicity). That is **not** a statement that exhaustion is useless here: it excludes neither a
finite argument uniform in $d$ — one of which proves the $k \le 3$ case outright — nor exhaustion
combined with a gap/rigidity theorem, and §1.2 says what each would need. Everything computational
here is `numerical`; the derivations in §1, §3 and §5 are `sketch`; the only `cited` input is
Oler's inequality.

> **Two claims in the first version of this file were refuted by an independent verifier on
> 2026-08-21 and are corrected in place, originals preserved:** the topological justification in
> §1 (see §1.3) and the partition corollary in §3 (see §3.3). Both were over-broad in the same
> direction — declaring routes dead that are not — and the second had already been propagated.
> If you read the earlier version, read §1.2 and §3.2.

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

## 1. What exhaustion at fixed rational sides cannot do — and what it still might

> **CORRECTED 2026-08-21.** This section originally ran under the heading *"The structural
> obstruction — no exhaustion can finish this"* and justified itself with a topological argument
> about nested configuration spaces. **That argument is wrong, and the conclusion it was used to
> support was over-scoped.** Both errors were found by an independent verifier. The narrow
> conclusion survives — but on a completely different and far more elementary argument, given in
> §1.1 — and the broad one does not. The original text and the refutation are preserved in §1.3
> rather than deleted (repo `RULES.md` §0). Anyone who read the earlier version and concluded
> "exhaustion is dead here" should read §1.2.

### 1.1 What is actually true, and why — `sketch`

> **Claim.** No finite family of refutations at **fixed rational sides**, used alone, implies
> Erdős–Oler at any $k$.

*Proof.* Feasibility is monotone in the side: a configuration of $n$ points at separation $\ge 2$
in $T(d)$ sits inside $T(d')$ for every $d' \ge d$. So among refutations the largest side is the
strongest statement, and a finite family of exhaustions at rationals $d_1,\dots,d_N$, all below
$D = 2(k-1)$, yields exactly one thing: $d(n) > \max_i d_i$. But $\max_i d_i$ is a maximum of
*finitely many* rationals each $< D$, hence is itself $< D$. The family therefore gives
$d(n) > c$ for some $c < D$, and never $d(n) \ge D$. $\square$

That is the whole argument: **monotonicity plus finiteness.** No topology, no compactness, and no
claim about limits of configuration spaces. It is also exactly as strong as it looks — it says
something about *one particular shape of output*, not about computation in general.

### 1.2 What this does **not** exclude — two live routes

This is the part the earlier version got wrong, and it matters because two theory routes were
abandoned on the broad reading and have since been reopened.

**(a) A finite argument that is uniform in $d$.** Nothing above touches an argument that refutes
$T(k)-1$ points at *every* $d < 2(k-1)$ in one stroke. Such arguments exist and one of them is in
this very file: for $k \le 3$, at every $d < 4$ the four level-1 cells have side $d/2 < 2$, so each
holds at most one point and $5 > 4$ points cannot be placed. The bound $n \le 4$ holds at all
$d < 4$ simultaneously, so it proves $d(5) \ge 4$ — the **full** $k=3$ case of the conjecture, by a
finite cell computation. The real question at $k = 7$ is therefore not "can an exhaustion at a
rational close it" (no, by §1.1) but "is there a finite case analysis uniform in $d$", and
**nothing measured in this attack bears on that question.**

**(b) Exhaustion plus a closing gap or rigidity argument.** If one had a theorem of the form
$d(T(k)-1) \notin (2(k-1)-\delta,\; 2(k-1))$ for some explicit $\delta > 0$ — a spectral-gap or
rigidity statement about near-optimal configurations — then a *single* exhaustion at the rational
$d = 2(k-1) - \delta/2$ would finish the case. Here the measurements in §4 and §5 **do** bear
directly, and they are the useful thing this attack produced: they say how large $\delta$ would
have to be for the computational half to be affordable. At $k = 5$ a $\delta$ as small as $0.01$
is already reachable ($d > 7.99$ closed in 98 s); at $k = 6$ and $k = 7$ nothing closed even at
$\delta \approx 0.3$, i.e. at Oler's own level. So route (b) at $k=7$ currently needs a gap
theorem with $\delta > 0.27$, which is larger than the entire residual gap of §2 — meaning the
gap theorem would have to do all the work by itself.

### 1.3 The original argument, and why it is wrong — `refuted`

Preserved verbatim, because the error is instructive and because it was propagated before it was
caught:

> *An exhaustion refutes $n$ points at one explicit rational $d$ [...] no finite family of the
> first implies the second, because the configuration space at $d = 2(k-1)$ exactly is
> **non-empty** [...] So the sets $S(\varepsilon) = \{$configurations of $T(k)-1$ points at
> separation $\ge 2$ in $T(2(k-1)-\varepsilon)\}$ shrink as $\varepsilon$ grows and their "limit"
> $\bigcap_{\varepsilon>0}$ is the non-empty $S(0)$.*

**The error.** $S(\varepsilon)$ is *decreasing* in $\varepsilon$, so $\bigcap_{\varepsilon>0}
S(\varepsilon)$ is not any kind of $\varepsilon \to 0$ limit — for a decreasing family the
intersection is governed by *large* $\varepsilon$, and it is empty. Worse, the identification
$\bigcap_{\varepsilon>0} S(\varepsilon) = S(0)$ is false in exactly the case the section was
about: at $k=3$ we have $d(5) = 4$, so $S(\varepsilon) = \emptyset$ for every $\varepsilon > 0$
while $S(0) \ne \emptyset$ (the lattice packing minus its apex). So
$\bigcap_{\varepsilon>0} S(\varepsilon) = \emptyset \ne S(0)$. Under Erdős–Oler this holds at
every $k$: the intersection is empty, and the sentence asserted it was non-empty.

The "attained-maximum / exhaustion refutes open conditions" paragraph that followed it is dropped
too. It was a restatement of the same confusion: it treated "the maximum is attained at exactly 2"
as if being a closed condition were itself an obstruction to finite refutation, which §1.2(a)
disproves outright.

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

## 3. Partitions: which refinement is dead, and which is very much alive

> **CORRECTED 2026-08-21.** This section originally ran under the heading *"A dead end worth
> writing down: subdividing into regions always loses"* and concluded that any
> partition-and-count refinement of Oler is strictly worse than Oler. **The lemma is correct and
> is confirmed; that corollary is false.** The counterexample is in this repo's only complete
> Erdős–Oler case and was already sitting in §1.2(a) of this same file, which is the tension the
> original text noticed and then resolved the wrong way. Found by an independent verifier after
> the broad reading had been propagated and had killed two theory routes; those are reopened.
> Original wording preserved in §3.3.

### 3.1 The lemma — confirmed

> **Lemma.** Let a convex region $P$ be partitioned into convex pieces $P_1,\dots,P_m$, and write
> $\Omega(R) = \frac{2}{\sqrt3}A(R) + \frac12 M(R) + 1$ for **Oler's bound** on a region $R$
> (points at separation $\ge 1$). Let $I$ be the total length of the internal cuts. Then
> $$\sum_{i=1}^m \Omega(P_i) \;=\; \Omega(P) \;+\; I \;+\; (m-1).$$

*Proof.* Areas are additive: $\sum A(P_i) = A(P)$. Each internal cut lies on the boundary of
exactly two pieces, so $\sum M(P_i) = M(P) + 2I$. The constant $1$ is paid $m$ times instead of
once. $\square$

### 3.2 What it does and does not say

**Dead move: Oler-per-piece, then sum.** By the lemma this loses exactly $I + (m-1)$ — one unit
per extra piece plus the internal boundary — and since the deficit to be recovered at
$n = T(k)-1$ is exactly 1 (§2), any partition into two or more pieces overspends the whole budget
before it starts. Cutting $T(a)$ into $k$ horizontal strips by the similar-triangle cuts loses
$(k-1)(a/2+1)$; at $k=7$, $a=6$, that is 24 against a budget of 1. This part stands.

**Live move: true-capacity-per-piece, then sum.** $\Omega(P_i)$ is *not* the capacity of $P_i$.
The true capacity $\mathrm{cap}(P_i)$ — the actual maximum number of separation-1 points that fit
in $P_i$ — satisfies $\mathrm{cap}(P_i) \le \lfloor \Omega(P_i) \rfloor$, and on small pieces
Oler's bound is **badly** slack, so the inequality is strict and large. Replacing $\Omega(P_i)$ by
$\mathrm{cap}(P_i)$ can therefore recover far more than the $I + (m-1)$ the lemma charges, and
$\sum_i \mathrm{cap}(P_i) < \Omega(P)$ is perfectly possible.

**Witness** (exact; reproduce with the two commands below). Separation-1 side $a = 1.999$, i.e.
$d = 3.998$, and $n = 5$ — the $k=3$ Erdős–Oler case:

| bound | value | refutes $n=5$? |
|---|---|---|
| Oler on the whole triangle, $\Omega(T(a)) = (a+1)(a+2)/2$ | 5.9965 | **no** |
| Oler per level-1 piece, summed, $4\,\Omega(T(a/2))$ | 11.9955 | no — worse, exactly as the lemma predicts |
| **true capacity** per level-1 piece, summed | side $0.9995 < 1 \Rightarrow$ diameter $< 1 \Rightarrow$ 1 point each $\Rightarrow$ **4** | **yes** |

```sh
python3 -m eoex feasible --n 5 --d 3.998          # Oler:   5.9965, does not exclude 5
python3 -m eoex prove    --n 5 --d 1999/500 --max-level 4   # PROVED, in 1 node
```

The true-capacity partition beats Oler by nearly two whole points and is *decisive* where Oler is
not. This is not a curiosity: it is how the only complete Erdős–Oler case in this repo is proved
(§1.2(a)), and it is the mechanism behind the diameter cap in the experiment's `caps.py`.

**So the correct statement is:** *Oler-per-piece-then-sum is dead; true-capacity-per-piece-then-sum
is live, and is the only method here that has ever closed a case of the conjecture outright.* The
open question it leaves is quantitative — whether a partition of $T(a)$, $a$ slightly under $k-1$,
into pieces whose true capacities sum below $T(k)-1$ exists for $k \ge 4$ — and §4/§5 measure how
hard the cell-shaped instances of that question are, not whether the family is viable.

A third option, distinct from both, is a bound applied to the configuration's **own hull**, which
pays the $+1$ once and has no internal cuts: that is what the Oler-hull rule in the experiment
does and what the hull-corner-deficit route is about.

### 3.3 The original corollary — `refuted`

Preserved:

> *The natural pigeonhole strengthening — cut the triangle into convex pieces, cap each piece by
> Oler, add up — is **strictly worse than Oler on the whole triangle, always**, so it can never
> close the gap of §2. [...] The same accounting is why the cell-capacity rule inside a branch and
> bound is weak in the tight regime: capacity rules are pigeonhole rules on a partition.*

Two errors. First, "cap each piece by Oler" was silently generalised to "any partition-and-count
refinement" in the surrounding prose and in every downstream summary, including this file's own
§6 and my journal entry; the witness in §3.2 refutes the generalisation. Second, the last sentence
is false about this experiment's own code: the capacity rule in `caps.py` is
$\min$(diameter cap, Oler cap, cited $d(k)$ cap), and the **diameter cap is precisely the live
move** — it is what makes the $k \le 3$ case close in one node. I wrote a correct lemma, drew a
corollary that did not follow, and then contradicted it two sections earlier without noticing.

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

1. **For the specific method attacked: unbounded.** §1.1. No amount of compute converts a finite
   family of fixed-rational-side refutations into the conjecture, so for *that* method "distance"
   measured in CPU-hours is the wrong axis. This says nothing about the two routes in §1.2.
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
   exactly $(2k+1)-\sqrt{4k^2+4k-7} \approx 0.269$ in $d$ at $k=7$; §3.2 says the recovery cannot
   come from *Oler-per-piece-then-sum* but **can** in principle come from
   *true-capacity-per-piece-then-sum*, which is how the $k \le 3$ case is proved; and
   `packing-oler-slack` locates the whole deficit in the hull → triangle relaxation. That triple is
   a precise specification of the theorem the theory routes have to prove.

   *(The middle clause originally read "the recovery cannot come from any partition-and-count
   refinement". That was the over-broad corollary refuted in §3.3, and it is the sentence that
   propagated. Corrected 2026-08-21.)*

## 7. Kill-criterion

Stated before the runs: *if the exhaustion cannot certify $\rho > \rho_{\text{Oler}}$ at
$k = 5$ within a 7-minute single-core budget, the method adds nothing anywhere and $k = 6,7$ get
one confirming probe each rather than a campaign.*

**It did not fire at $k=5$** — $\rho = 0.99875$ was certified in 98 s, comfortably above
$\rho_{\text{Oler}} = 0.95377$. The attack is nevertheless recorded as `refuted` **as a complete
route to $k=7$ via fixed-rational-side exhaustion alone**, on §1.1, which is a fact about the shape
of that output and not a budget observation. §1.2 and §6.3 are what survive.

## 8. What a reviewer should attack

1. **The branching is exhaustive** — that the four children of a cell are closed and cover it.
   A wrong child set gives false `proved` verdicts everywhere while passing most tests. It is
   derived in the experiment's `eoex/lattice.py` docstring and checked only by sampling.
2. **§1.1** — the monotonicity argument, which replaces a wrong topological one (§1.3). It is
   three lines and I believe it, but it is the load-bearing negative claim in the file. Attack in
   particular whether "used alone" is doing hidden work: §1.2 exists precisely because it is.

2b. **§1.2 and §3.2** — the two *positive* statements added after the corrections. Both assert
   that a route is live rather than dead, which is the easier direction to get right, but neither
   has been checked by anyone but me and the verifier who forced them.
3. **§3 and §5** — both are mine, both are elementary, neither has been cross-examined.
4. **The separation-1 / separation-2 normalisation** everywhere. Oler is stated at separation 1;
   this problem's certificates use separation 2.
