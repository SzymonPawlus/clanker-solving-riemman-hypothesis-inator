# Second verification pass — the first pass's unexamined list, and the round-2 claims

**Claim type: neither construction nor optimality.** (Problem [`../../RULES.md`](../../RULES.md) §1
asks for that sentence first.) No bound on $s(n)$ is asserted here. This file is an adversarial
re-derivation of the claims the [first pass](../eo-verification/) explicitly did **not** examine,
plus the round-2 lanes as they land.

- Examiner: `claude` (Claude Opus 5), 2026-08-21, branch `claude/circle-equklatetal-problem-sa7tx7`
- Code: [`experiments/packing-eo-verify-2/`](../../../../experiments/packing-eo-verify-2/) —
  Python standard library only, exact arithmetic ($\mathbb{Q}$ and $\mathbb{Q}(\sqrt3)$ with an
  exact sign test) for every decision. Written from the *statements*; no author's code was read,
  imported or rerun.

> ## This grants no status. Read this before using anything below.
>
> Repo [`RULES.md`](../../../../RULES.md) §5: `verified:review` requires an examiner from a
> **different model family**. I am Claude Opus 5; so were the authors of every claim examined here.
> **Every claim below stays `sketch` and stays non-assumable, including the ones I confirm.**
> What this buys is error-finding, not certification.

---

## 0. Disagreements, each with its witness

### D1 — the resolution theorem proves a cost *upper* bound; it is being used as a lower bound

**Where:** [`../eo-exhaustion/`](../eo-exhaustion/) §5, and §6.2 which quotes it. This is the
file's cost model and nobody had checked it.

The **theorem** is correct (§2 below). It says:

> node survives the pairwise test at uniform level $L$ $\;\Longrightarrow\;$
> $d \ge d(n)\,(1 - h/\sqrt3)$, i.e. $h \ge \sqrt3\,(1-\rho)$.

§5 then writes: *"Contrapositive: a cell exhaustion can only close at ratio $\rho$ once
$h < \sqrt3(1-\rho)$."* **That is the converse, not the contrapositive.** The contrapositive is

> $h < \sqrt3\,(1-\rho)$ $\;\Longrightarrow\;$ **no** node survives $\;\Longrightarrow\;$ the
> search **closes**,

which is a *sufficient* condition — a termination guarantee and an **upper** bound on the level
needed. §5 reads it as a necessary condition and concludes "there is no budget at which this
terminates". The theorem establishes very nearly the opposite: for any fixed $d < d(n)$, uniform
subdivision at level $2^L > d/(\sqrt3(1-\rho))$ **is guaranteed to close**, so the pairwise cell
method is *complete* at every fixed rational side.

> **Witness, and it is sitting two sections earlier in the same file.** $k = 3$, $n = 5$,
> $d = 3998/1000$; $d(5) = 4$ (repo `cited`, $s(5) = 4 + 2\sqrt3$), so $\rho = 0.9995$.
> §5's formula demands level $L \ge 13$, i.e. $4^{13} = 6.7\times10^{7}$ cells.
> The cell method closes at **level 1**, with **4 cells**: side $h = 1.999 < 2$, so each closed
> cell holds at most one point, and $5 > 4$.
>
> That closure is [`../eo-exhaustion/`](../eo-exhaustion/) §1.2(a) and §3.2 — the file's own
> showcase, its only complete Erdős–Oler case, and the thing it says "closed in 1 node".
> Reproduced independently (`check_resolution.py`), together with $n = 6$ at the same $d$
> ($L$ demanded $= 13$, closes at $L = 1$) and $n = 5$ at $d = 3.9998$ ($L$ demanded $= 16$,
> i.e. $4.3\times10^{9}$ cells; closes at $L = 1$).

**What survives.** §5's arithmetic is right *given its formula* — I reproduce the levels table
(6, 8, 9, 10, 13) exactly. What is **not** established is §5's title ("why the cost diverges"),
its closing sentence ("there is no budget at which this terminates"), and §6.2's *"§5 says it
needs level $\ge 9$ … merely to match a bound Oler gives in one line."* None of those follows.
The intuition behind them may well be true — my own uniform-level search does not close $k=4$ at
$d = 5.9$ up to level 5, consistent with the theorem's $L = 8$ — but §5 proves the other half.

**Why it matters.** §5 is the quantitative backing for §6.1's "for the specific method attacked:
unbounded" and for treating exhaustion as a dead route. §1.1's monotonicity argument (confirmed by
the first pass) already gives the real obstruction — *finitely many rational sides never reach
$D$* — and it does not need §5. §5 should be relabelled as what it is: a **completeness /
termination theorem for the cell method at fixed $d$**, which is a positive result.

### D2 — T1's proof does not establish unboundedness with the family it invokes

**Where:** [`../eo-boundary-counting/`](../eo-boundary-counting/) §5, the file's strongest negative
result, quoted in [`../oler-slack-analysis/`](../oler-slack-analysis/) §4 as closing "a whole
family of routes".

T1's proof is: *"Apply the §4 family. It has $b = 3$ for every $k$, its hull is a triangle of side
$\to k-1$"*, giving $\Phi(3) \ge \frac{3k-3}{2} \to \infty$.

I rebuilt the §4 family myself in $\mathbb{Q}(\sqrt3)$ from the prose description and reproduce
the file's exact numbers ($2.963, 4.415, 5.846, 7.257, 8.649, 10.020, 11.371$ for $k = 3..9$),
confirming $b = 3$, separation $\ge 1$ and containment exactly at every $k$. Then:

> **Witness.** The §4 family is fixed at $\lambda = 101/100$, $\varepsilon = 1/1000$. Its hull is
> equilateral of side $\lambda(k-1) - \sqrt3\,\varepsilon$, which is **not** $\to k-1$: the $1\%$
> multiplicative error is squared. Exactly (closed form validated against the geometry for
> $k = 3..10$):
> $$n - \tfrac{2}{\sqrt3}A - 1 \;=\; \tfrac{k^2+k}{2} - \tfrac{\bigl(\lambda(k-1)-\sqrt3\varepsilon\bigr)^2}{2} - 1,$$
> whose $k^2$ coefficient is $\frac{1-\lambda^2}{2} = -0.01005 < 0$.
>
> | $k$ | 10 | 40 | 70 | **76** | 100 | 150 | 200 |
> |---|---:|---:|---:|---:|---:|---:|---:|
> | lower bound on $\Phi(3)$ | 12.70 | 43.28 | 55.77 | **56.10** | 50.17 | 0.64 | $-99.14$ |
>
> **The family as parameterised gives $\Phi(3) \ge 56.0999\ldots$ and nothing more.** That is a
> finite number, so it does not exclude a $\Phi$.

The two corroborations §5 offers do not close the gap either: flat arcs give $\Phi(b) \ge b-1$,
finite at each $b$; and the lattice remark compares $\Phi$ with Oler's own term. **Unboundedness at
fixed $b$ is what T1 needs, and only the §4 family was offered for it.**

**T1 is nevertheless TRUE.** The repair is to let the parameters depend on $k$. Take
$\delta_k = 1/k^3$, $\lambda_k = 1+\delta_k$, $\varepsilon_k = \delta_k/2$; then the push moves
each point by at most $\varepsilon_k$, so separation $\ge \lambda_k - 2\varepsilon_k = 1$ exactly,
still $\ge 1$; $b = 3$ still; and the bound $\to \frac{3k-3}{2}$. Verified exactly (geometry, to
$k = 25$; validated closed form to $k = 10^4$):

| $k$ | 7 | 12 | 25 | 100 | 1000 | 10000 |
|---|---:|---:|---:|---:|---:|---:|
| lower bound on $\Phi(3)$ | 8.910 | 16.435 | 35.964 | 148.49 | 1498.50 | 14998.50 |
| $\frac{3k-3}{2}$ | 9 | 16.5 | 36 | 148.5 | 1498.5 | 14998.5 |

**So: the theorem stands, the proof as written does not.** Anyone quoting T1 should quote the
$k$-dependent family, not the fixed one — and [`../oler-slack-analysis/`](../oler-slack-analysis/)
§4's sentence *"scale the lattice $T(k)$ by $1+\delta$ and push every boundary point inward by
$\varepsilon$, and … $n - \frac{2}{\sqrt3}A - 1$ grows like $\frac{3k-3}{2}$"* inherits the same
gap and needs $\delta, \varepsilon \to 0$ with $k$ stated.

*(Note what is **not** wrong: §4's own table, which is about $b$ collapsing and about hypothesis H,
is exactly right at every $k$ it prints, and W1 stands. The error is only in extrapolating that
fixed-parameter family to $k \to \infty$.)*

### D3 — Oler gives $\ge$, not $>$ (minor, but it is a strictness claim)

[`../eo-exhaustion/`](../eo-exhaustion/) §2 writes *"Oler's inequality gives
$d(n) > \sqrt{8n+1}-3$"*. Oler gives $n \le \Omega(a)$ with equality attainable, so what follows is
$d(n) \ge \sqrt{8n+1}-3$. Immaterial to every number in the file, and
[`../eo-boundary-counting/`](../eo-boundary-counting/) §2 states the same fact correctly (the open
window is $[a^\*, 6)$, **closed** at $a^\*$) — recorded only because §2's is the phrasing that gets
copied.

### Q1 — a circularity vector in `eo-exhaustion` §4 that I could not examine

[`../eo-exhaustion/`](../eo-exhaustion/) §3.3 describes its own capacity rule as
*"$\min$(diameter cap, Oler cap, **cited $d(k)$ cap**)"*. A capacity derived from a `cited` $d(n)$
is exactly the trap `FINDINGS.md` logs as *"A `cited` input contained the conclusion"*: the repo's
`cited` $d(14) = 8$ and $d(20) = 10$ **are** Erdős–Oler at $k = 5$ and $k = 6$. §4's $k = 5$ row
claims to have *proved* $d(14) > 7.99$; if any binding capacity in that run traces to the `cited`
$d(14)$, the run proves nothing about $n = 14$.

I have **not examined this** — problem `RULES.md` §3 forbids me reading or rerunning the author's
code, and I did not. It is a question for the author, not a finding. It does not affect $k = 7$
(the cells there are small and the relevant `cited` values are for small $n$), and it does not
affect any conclusion in this pass.

---

## 1. T1 and the boundary count (`../eo-boundary-counting/`)

| Claim | Verdict |
|---|---|
| **P1** $\lvert E\cap\partial T\rvert \le 3\lfloor a\rfloor$, $a\ge1$ | **CONFIRMED**, proof and all |
| **P1 sharp** for every $a \ge 1$ | **CONFIRMED** — attained in my own search |
| **W1** $b$ collapses to 3 at the perturbed lattice; H fails there | **CONFIRMED** exactly |
| **T1** as a theorem | **CONFIRMED**, with a repaired family (D2) |
| **T1** as proved in §5 | **DISAGREED** (D2) |
| §2 window table, $a^\*$, $t_7$ | **CONFIRMED** exactly |

**P1's proof, re-derived.** Write $k=\lfloor a\rfloor$, $m_i$ for points on side $i$, $s$ for
occupied corners, $\gamma_i = \alpha_i+\beta_i$ the two extreme legs of side $i$. Two steps do the
work and both are correct: $m_i \le 1 + \lfloor a-\gamma_i\rfloor$, and at an unoccupied corner the
two adjacent legs satisfy $x^2-xy+y^2 \ge 1$, whence $\max(x,y)\ge1$ (if $y\le x$ then
$x^2-xy+y^2 = x^2-y(x-y) \le x^2$). Charging each unoccupied corner to a side carrying a leg
$\ge 1$ gives $\gamma_i \ge n_i$ and so $m_i \le 1+k-n_i$, and $B = \sum m_i - s \le 3+3k-(3-s)-s
= 3k$.

**The place it nearly breaks, checked.** The tempting counterexample is to make one side's two legs
both tiny (so it carries $k+1$ points) and pay only $1$ on each of the other two, giving $3k+1$.
It does not exist: if side 2's legs are both $\approx 0$ then corners $A_2$ and $A_3$ must each be
paid by their *other* leg, which lands on sides 1 and 3 respectively, and corner $A_1$ must then be
paid by a *second* leg on side 1 or side 3. So some side is charged twice and $\gamma \ge 2$ there.
The charging bookkeeping is exactly what closes this, and it is correct. The empty-side cases
($z' = 2$: $B\le 2k+1$; $z'=1$: $B\le k+1$) are correct too, using the fact that a corner adjacent
to an empty side cannot be occupied.

**Break attempt** (`break_p1.py`): enumerate Pareto-minimal leg pairs at each corner on a rational
grid, build the explicit point set, verify **every** pairwise squared distance exactly. Max
attained, over 11 values of $a$:

| $a$ | 1 | 3/2 | 2 | 5/2 | 3 | 17/5 | 4 | 9/2 | 5 | **59/10** | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $3\lfloor a\rfloor$ | 3 | 3 | 6 | 6 | 9 | 9 | 12 | 12 | 15 | **15** | 18 |
| $\lfloor 3a\rfloor$ | 3 | 4 | 6 | 7 | 9 | 10 | 12 | 13 | 15 | **17** | 18 |
| best found | 3 | 3 | 6 | 6 | 9 | 9 | 12 | 12 | 15 | **15** | 18 |

No violation; sharp everywhere. §8(iii)'s correction of the manager — that the honest
$\partial T$ bound is $3\lfloor a\rfloor$, not $\lfloor 3a\rfloor$ — is **right**, and the
$a = 5.9$ row (15, not 17) is the reason.

---

## 2. The resolution theorem (`../eo-exhaustion/` §5)

**Verdict: the theorem is CONFIRMED; its stated contrapositive is REFUTED (D1).**

**Restated.** Let the cells of a node all be at level $L$, side $h = d/2^L < 2$, so each closed
cell (diameter $h$) holds at most one point of a separation-2 set and the node is a choice of $n$
distinct cells. If every pair of chosen cells admits points at distance $\ge 2$, then $T(d)$
contains $n$ points at pairwise distance $\ge 2 - 2h/\sqrt3$, so $d \ge d(n)(1-h/\sqrt3)$.

**Derived independently.** A cell is equilateral of side $h$, so its centroid is its circumcentre
and every point of it is within $R = h/\sqrt3$ of the centroid. Hence for $x\in c_i$, $y\in c_j$,
$|x-y| \le |g_i-g_j| + 2R$, so $|g_i-g_j| \ge \mathrm{maxsep}(c_i,c_j) - 2h/\sqrt3 \ge 2-2h/\sqrt3$.
The centroids lie in $T(d)$ by convexity. Scaling by $1/(1-h/\sqrt3)$ (positive iff $h<\sqrt3$;
for $\sqrt3 \le h < 2$ the conclusion is vacuously true) puts $n$ points at separation $\ge 2$ in a
triangle of side $d/(1-h/\sqrt3)$, which must be $\ge d(n)$. $\square$

Checked exactly on **8568** cell pairs at levels 1–3 for $d \in \{4, 3.998, 5.9, 12\}$: the
circumradius bound $(\mathrm{maxsep}-|g_i-g_j|)^2 \le 4h^2/3$ holds on every one, zero violations.
All arithmetic in the lattice basis, where squared distances are rational.

**The direction.** Survival $\Rightarrow h \ge \sqrt3(1-\rho)$. Contrapositive:
$h < \sqrt3(1-\rho) \Rightarrow$ closure. The file asserts closure $\Rightarrow h < \sqrt3(1-\rho)$.
Refuted in D1. I also looked for a valid necessity argument in the vicinity and did not find one:
scaling an optimal $d(n)$-configuration down into $T(d)$ gives points at separation $2\rho$, and
the best per-pair bound that yields is $\mathrm{maxsep} \ge 2\rho - h/\sqrt3$, which never reaches
the required $2$ for $\rho<1$. **The necessity half is simply not proved anywhere.**

---

## 3. `../oler-slack-analysis/` — and no disagreement with Codex

Codex (`Flow-25`) cross-examined this on **PR #90** at head `fa9933d`, with its own SymPy checker,
and approved. Per the brief I checked *its* claims rather than duplicating the pass.

| Codex's claim | My verdict |
|---|---|
| $F = 2n-b-2$ from Euler + edge incidence, with $b$ counting **all** hull-boundary points | **agree** — re-derived; Euler closes for every $(n,b)$, and the face count matches an explicitly built triangulation of $\Lambda(k)$ for $k = 2..8$ |
| boundary-edge excess $\ge 0$ (consecutive boundary points are separated points) | **agree** |
| the decomposition follows exactly | **agree** — re-derived |
| $(0,0),(1,0),(2,\tfrac12)$ has squared distances $1, \tfrac54, \tfrac{17}4$ and area $\tfrac14$ | **agree**, exact |
| FP's supremum below $a=k-1$ is $T(k)-\tfrac32$, hence $n \le T(k)-2$ | **agree**, exact for $k \le 29$ |
| the "15 non-degenerate configurations" count is a typo; the true count is 14 | **agree**; already fixed in `8c94de3` |

**No disagreement with Codex on any point.** The one thing to flag: Codex reviewed head `fa9933d`;
the §4 paragraph now in the file that repeats T1 ("grows like $\frac{3k-3}{2}$") carries D2's gap,
and was not part of what Codex examined.

---

## 4. `../eo-oler-equality/` — Lemma T, T2, S2

Not on the first pass's list, but the round-2 `eo-epsilon` lane depends on all three, so I checked
them in advance.

| Claim | Verdict |
|---|---|
| **Lemma T** $\frac2{\sqrt3}A+\frac p2 \ge 2$, equality iff $(1,1,1)$ or $(2,1,1)$ | **CONFIRMED**, proof and all |
| **Step 3** (the author's flagged step) | **CONFIRMED** — see below |
| **T2** the $\tau$-identity | **CONFIRMED** |
| **S2** deficit $\ge 1$ *is* Erdős–Oler | **CONFIRMED** |

**Step 3, the flagged step, in my own words.** With $\alpha = y+z-x$ etc. and $S = \alpha+\beta+\gamma
= p$, the constraint $x \ge 1$ is $\alpha \le S-2$ (since $\beta+\gamma = 2x$), and
$\alpha = S-\beta-\gamma \ge 4-S$. For $S \in (3,4)$ the vertices of $\Delta_S$ are the points with
two active constraints: two upper bounds gives $(S-2,S-2,4-S)$, feasible iff $S \ge 3$; two lower
bounds gives $(4-S,4-S,3S-8)$, feasible iff $S \le 3$; one upper and one lower gives
$(S-2, 4-S, S-2)$, a permutation of the first. So exactly three vertices, as claimed. And
$\alpha\beta\gamma$ restricted to any line in the plane $\sum = S$ is a downward parabola (times a
fixed non-negative factor), hence concave, so its minimum is at an endpoint; iterating reaches a
vertex. Minimum $= (S-2)^2(4-S)$. **Correct.** Confirmed numerically too: a $200\times200$ exact
grid over $\Delta_S$ reproduces $(S-2)^2(4-S)$ for $S = 3.0, 3.1, \dots, 3.9$.

Step 4's identity $S(S-2)^2+3S-12 = (S-3)(S^2-S+4)$ verified exactly; $S^2-S+4$ has discriminant
$-15$.

**Exact scans** (`check_lemma_t.py`): 7 761 grid triangles (sides in $[1,4]$, step $1/12$),
142 035 random rational triangles (sides in $[1,7]$), the full degenerate family $x = y+z$, a
$13^3$ box of radius $6/1000$ around each equality case, and large-$S$/thin-sliver probes.
**Zero violations; the equality set is exactly $\{(1,1,1),(1,1,2)\}$.** Every decision is a
rational comparison — with rational sides $16A^2 = S\alpha\beta\gamma$ is rational, so
$\frac2{\sqrt3}A \ge 2-\frac p2$ becomes $\frac{16}{3}A^2 \ge (4-S)^2$ when the right side is
non-negative, and $\frac p2 \ge 2$ otherwise.

**T2** re-derived: $|\mathcal E| = \frac{3F+b}{2} = 3n-b-3$, $|\mathcal E_{\rm int}| = 3n-2b-3$,
$\sum_f p_f = M(P)+2L_{\rm int}$, and subtracting gives
$L_{\rm int} - |\mathcal E_{\rm int}| = \sum_{e\ \rm int}(\ell_e-1)$. Correct.

**S2** re-derived: $\frac{a^2+3a+2}{2}$ is strictly increasing and equals $T(k)$ exactly at
$a = k-1$ (checked for $k \le 39$), so "deficit $\ge 1$ at $n = T(k)-1$" $\iff$ "$a \ge k-1$"
$\iff$ Erdős–Oler at $k$. **This is the single most important thing for the `eo-epsilon` lane to
respect**: $\varepsilon = 1$ is not a target on the way to the conjecture, it *is* the conjecture,
and anything short of it is partial by exactly the amount stated.

---

## 5. `../eo-literature/` — the null result is real

The file's central operational claim is that this session has **no scholarly egress at all**, so a
literature task cannot succeed however it is attempted. **Confirmed independently**: `curl` to
`api.crossref.org`, `www.cambridge.org`, `zbmath.org` and `en.wikipedia.org` all fail at the proxy
(exit 000). The file's advice — probe reachability before spending a task on literature — is
correct and worth adopting.

The file promotes nothing to `cited`, quotes no source it did not read, and explicitly flags the
Locatelli–Raber trap (that paper is about the **square**, not the triangle) and the
Academia.edu/ResearchGate item. All of that is the right posture. **No disagreement.** Its
Folkman–Graham bibliographic detail (Canad. Math. Bull. **12** (1969) 745–752) matches my own
recollection, which is worth exactly nothing as evidence and is recorded only so that a future
session with egress knows what to confirm.

---

## 6. What I confirmed exactly, in arithmetic

All in `check_part1_arith.py`, all exact (irrationals via certified rational brackets):

- `eo-exhaustion` §2: $8(T(k)-1)+1 = 4k^2+4k-7$; the residual-gap identity
  $(2k+1)^2-(4k^2+4k-7)=8$; Oler's RHS at $a=k-1$ is exactly $T(k)$ for $k \le 39$; and every
  digit of the §2 table (target $d$, Oler's $d$, residual, $\rho_{\rm Oler}$) for
  $k = 3,4,5,6,7,8,12$.
- `eo-exhaustion` §4: the $\rho$ column ($0.98333$, $0.99875$).
- `eo-exhaustion` §5: the levels table ($6, 8, 9, 10, 13$ and $4^L$), *given* §5's formula.
- `eo-boundary-counting` §2: the window table at $k = 3,4,6,7$, both columns, including the
  non-integrality column that reproduces the manager's retracted numbers; the brackets
  $5.865459 < a^\* < 5.865460$ and $0.457427 < t_7 < 0.457428$ with $t_7^2+t_7 = \frac23$.

---

## 7. Not examined — no opinion is offered on any of these

- **Oler's inequality itself.** `cited` throughout; I did not re-derive it.
- **Every author's code.** Problem `RULES.md` §3 required me to reimplement from the statement, and
  I did. I read nothing from `packing-eo-exhaustion`, `packing-eo-boundary`, `packing-eo-equality`,
  `packing-oler-slack` or any round-2 experiment.
- **`eo-exhaustion` §4's `numerical` rows** — the node counts, the seconds, and the `proved` /
  `timeout` verdicts. These are properties of the author's implementation: a wall-clock measurement
  cannot be re-derived, and rerunning their prover is exactly what `RULES.md` §3 forbids. What I
  *can* say is (a) the derived quantities ($\rho$, the comparison against $\rho_{\rm Oler}$) are
  exactly right, (b) the `proved` rows are consistent with the `cited` table (they are strictly
  weaker than the known values, as they must be), and (c) Q1 above names a circularity vector in
  that pipeline that someone should check.
- **`eo-exhaustion` §8.1**, that the four children of a cell are closed and cover it. The author
  flags it as checked only by sampling; I did not examine their branching either. My own cell
  machinery builds the level-$L$ subdivision directly rather than by recursive splitting.
- **Novelty** of anything here.

---

# Part 2 — the round-2 lanes

Each lane wrote its kill-criteria before computing, which made this half of the job much easier:
in every case I could check the reported outcome against a criterion fixed in advance.

## 8. `../eo-epsilon/` — explicit $\varepsilon = 0$, and it says so in its first line

**No overclaim.** K3 fired as its author predicted, the headline is *"Explicit $\varepsilon$
proved: $0$"*, and the non-explicit result is labelled non-explicit throughout. That is the
posture `RULES.md` §7 asks for. Four substantive claims, all checked from the statements
(`check_epsilon.py`; the lane's `verify.py` was not read, imported or rerun):

### 8.1 "Groemer 1960 $\equiv$ Oler 1961" — **CONFIRMED**, and it is the most consequential thing in the round

Groemer's Satz is $n\sqrt{12} \le F - \varkappa U + \lambda$ with $\varkappa = \frac{2-\sqrt3}{2}$,
$\lambda = \sqrt{12}-\pi(\sqrt3-1)$, for $n$ unit circles in a convex region of area $F$,
perimeter $U$. Apply it to $K = H \oplus B_1$, the hull of the circles, where Steiner gives
$F = A(H)+M(H)+\pi$ and $U = M(H)+2\pi$. I re-did the substitution in my own symbolic ring
$\mathbb{Q}[\sqrt3,\pi]/(\sqrt3^2-3)$ with $A(H), M(H)$ as formal symbols:

$$F - \varkappa U + \lambda \;=\; A(H) + \tfrac{\sqrt3}{2}M(H) + \sqrt{12}$$

**exactly** — the $\pi$ terms cancel identically, because $1-2\varkappa = \sqrt3-1$ is precisely
what $\lambda$'s $-\pi(\sqrt3-1)$ is built to kill. Dividing by $\sqrt{12} = 2\sqrt3$ and
rescaling to separation 1 gives $n \le \frac2{\sqrt3}A + \frac M2 + 1$: **Oler's inequality,
verbatim.** Also checked tight on every $T(k)$ lattice, $k = 2..7$.

Three consequences the repo should absorb, in increasing order of importance:

1. **`eo-literature` §3's open question is answered, and its guess was right.** The problem
   `README.md`'s `sketch` table showing Groemer "slack at every triangular $n$" applies Groemer to
   the **containing triangle**; applied to the **hull of the circles** it is Oler and is exactly
   tight there. Two different applications of one inequality, exactly as §3 conjectured.
2. **The Groemer co-credit question is not as settled as `README.md` says.** That section rejects
   the co-credit because "the paper contains no result about triangles" — still true — but its
   supporting slack table does not support it, and "Zassenhaus–Groemer–Oler" now has an
   explanation. *I did not read Groemer.* This is a literature matter, verification-critical, for
   someone with egress; what I confirm is only the algebra above, from the transcription already
   on `README.md`.
3. **The equality case of Oler may already be `cited`.** Groemer's Satz as transcribed comes
   *with* its equality clause. If that transcription is right, then
   [`../eo-oler-equality/`](../eo-oler-equality/)'s targets (A) and (C) — the equality
   characterisation it could only prove in the no-interior-points case (T4) — are literature, not
   open. That reframes a whole attack. **Conditional on a transcription this repo has from one
   page of one scan**, which is exactly the sort of dependency that should be re-read before
   anything is built on it.

### 8.2 Theorem E — **CONFIRMED**, and it does give $d(27) > a^\*$ strictly

> $\mathrm{def}(a,n) = 0 \Rightarrow a \in \mathbb{Z}_{\ge0}$, $E = \Lambda \cap T(a)$, $n$
> triangular. Hence $d(n) > a^\*_n$ strictly for every non-triangular $n$.

Re-derived. $\mathrm{def} = G + \mathrm{slack}$ with $G = \Phi(T)-\Phi(P) \ge 0$ by monotonicity of
area and perimeter under inclusion; $\mathrm{def}=0$ kills both. $G = 0$ forces $A(P) = A(T)$,
and a closed convex $P \subsetneq T$ leaves a relatively open non-empty subset of $T$, which has
positive area — so $P = T(a)$, in particular non-degenerate, which disposes of Groemer's
degenerate alternative. $\mathrm{slack}=0$ is then Groemer's equality clause (§8.1), so $T(a)$ is
tiled by unit equilateral triangles with all vertices in $E$; each side of $T$ is a union of tile
edges, so $a \in \mathbb{Z}$; and no extra point can exist, since every point of a unit
equilateral tile is within its circumradius $1/\sqrt3 < 1$ of a vertex. Attainment of $d(n)$ is
compactness. **Correct.**

> **Consistency test, and it is a strong one.** Theorem E predicts $a_n = a^\*_n$ **iff** $n$ is
> triangular. Against all 16 of the repo's `cited` values ($n \le 15$, $n = 20, 21$): equality at
> exactly $n = 3, 6, 10, 15, 21$ and strict inequality at every other row, with **zero**
> exceptions. That is 16 independent chances to fail and it takes none of them.

Its number-theoretic lemma ($4k^2+4k-7$ is never a perfect square for $k \ge 2$; from
$(2a+3)^2 = (2k+1)^2-8 \Rightarrow (k-a-1)(k+a+2) = 2$) is correct, and I found no $k < 300\,000$
against it.

**Two caveats, neither the author's fault.** (i) Theorem E rests entirely on Groemer's equality
clause, i.e. on one transcribed page — see §8.1(3). (ii) "$a$ is a **positive** integer" should be
"non-negative": $n = 1$ gives $a = 0$, the degenerate $k=1$ case. Trivial.

**What it is worth.** The repo previously had $d(27) \ge a^\*$; it now has $d(27) > a^\*$ with no
modulus. That is a real strict improvement and it is also, on the $\varepsilon$-scale, exactly
nothing — $\varepsilon$ stays $0$. The lane says both. Agreed on both.

### 8.3 Theorem Q (quantitative Lemma T) — **CONFIRMED**

$\tau \ge \frac{SQ-3(4-S)^2}{12}$ on $3\le S\le4$. The proof rationalises $\tau = N/D$ with
$N = \frac{SQ}{12}-\frac{(4-S)^2}{4}$, $D = \frac{2}{\sqrt3}A + \frac{4-S}{2}$, then needs
$D \le 1$: $\frac2{\sqrt3}A \le \frac{S^2}{18}$ (equilateral maximises area at fixed perimeter),
and $\frac{S^2}{18}+\frac{4-S}{2}$ is decreasing on $[3,4]$ (derivative $\frac S9-\frac12<0$) with
value exactly $1$ at $S=3$. Every step re-derived and checked exactly. Scanned on **93 366**
exactly-decided triangles of my own choosing — full grid, 60 000 random rationals, both
equality-case neighbourhoods, exactly-degenerate families, thin slivers with long side up to 12,
integer sides to 29. **Zero violations.** The bound vanishes at exactly $(1,1,1)$ and $(2,1,1)$
and nowhere between, as claimed.

### 8.4 Proposition V — **CONFIRMED**, with one phrasing caveat

T2 is an *identity*, so any $0 \le \Psi \le \tau$ gives
$\sum_f\Psi - \sum_{\rm int}(\ell-1) \le \mathrm{slack}$, with equality at $\Psi=\tau$. A lower
bound on the slack obtained this way is therefore never stronger than the identity itself. **The
logic is right and the no-go is real.** (V3) is correct too: for a face with all three edges
interior, $\sigma(f) = \frac2{\sqrt3}A_f - \frac12$, negative whenever $A_f < \frac{\sqrt3}4$ —
i.e. the already-refuted face-excess hypothesis. Checked exactly.

**Caveat on (V1)'s phrasing.** *"No quantitative Lemma T is a strengthening of anything"* reads
more broadly than what is proved. $\Psi$ **combined with an independent upper bound on**
$\sum_{\rm int}(\ell_e-1)$ is not excluded — that is step (3) of the same programme, and (V2)
says so. Read (V1) as *"the inequality (\*) produces is never stronger than the target"*, which is
what the argument gives.

## 9. `../eo-subinteger-relaxation/` — no open case claimed, and its $k=4$ proof is sound

**No infeasibility at $k=7$, so the brief's `extraordinary-claim` path is not triggered.** The
lane's scope line is right: it claims optimality only for $n = 5$ and $n = 9$, both already
`cited`. K1 fired with a split verdict — the refinement *decides* $k=4$ and fails at $k=5$.

The thing worth checking hard is its new proof, because a short proof of a `cited` case is exactly
where a circular capacity would hide (the brief's *"a `cited` input contained the conclusion"*).
I checked it (`check_eo4_proof.py`).

> **§5 Proposition.** Nine points at mutual distance $\ge 1$ do not fit in $T_a$ for $a < 3$.
> Cover $T_a$ by the three corner triangles $\Delta_V(t)$, $t = a/3 < 1$, and the central region
> $H$. Each corner triangle has diameter $t<1$, so holds $\le1$; $H$ is a regular hexagon of side
> $t$, circumradius $t < 1$, so holds $\le 5$ by Lemma D. Total $\le 8 < 9$.

**Verdict: CONFIRMED, and non-circular.** Every step re-derived:

- **The cover is complete** — a point outside every $\Delta_V(t)$ has $u_V > t$ for all $V$, which
  is the definition of $H$; the cuts are disjoint since $2t \le a$.
- **$H$ is a regular hexagon of side $t$** — cutting corners of side $t$ off a triangle of side
  $3t$ leaves remnants $3t-2t = t$ and introduces cut edges of length $t$; checked exactly at five
  values of $a$. Its circumradius is exactly $t$.
- **Lemma D re-derived independently.** Sort $m$ points by polar angle about $O$; some gap is
  $\le 2\pi/m$, so $|P_iP_j|^2 \le r_i^2+r_j^2-2c\,r_ir_j$ with $c=\cos(2\pi/m)$, and the
  maximum of $x^2+y^2-2cxy$ on $[0,\rho]^2$ is $\rho^2\max(1,2-2c)$ — I verified that maximum for
  $m = 2..6$. At $m=6$, $c=\tfrac12$ and $2-2c=1$, so the bound is $\rho^2$: **six separated points
  force circumradius $\ge 1$**, hence $\rho<1 \Rightarrow \mathrm{cap}\le5$. A point at $O$ is
  covered too ($|P_iP_j|^2 = r_j^2 \le \rho^2 < 1$). This is the same $x^2-xy+y^2 \le \max^2$
  trick as P1's corner bound, and it is exactly tight (the regular hexagon).
- **Circularity: none.** The only capacities used are *diameter $<1\Rightarrow1$* and
  *circumradius $<1\Rightarrow5$*. Both geometric; neither reads $d(n)$, $s(n)$ or $a_n$. The
  lane's validation table uses `cited` values only to check its computed capacities are never *too
  small* — the safe direction, and outside the proof.
- **It degrades correctly.** At $a=3$ the same cover gives $3\cdot3+6 = 15$ — vacuous, as it must
  be, since 10 points do fit at $a=3$. The proof is uniform in $a<3$, which is what its K4 demanded.

Its earlier transcript rows are consistent with the finished file: LP $=4<5$ at $k=3$, and the
integer-threshold family stuck at 9 at $k=4$ where the sub-integer one reaches 8.

## 10. The two covering lanes — best is 28, floor is 25, and every certificate verifies

§10.1 and §10.2 were written while both lanes were still searching and are kept as the record of
what their mid-flight output looked like. **§10.3 is the finished verdict**, after both write-ups
landed and I verified every certificate they produced.

**The construct lane's verification plan is sound** and I want to record that, because it is the
right plan: exact squared diameters in the lattice basis, pairwise disjoint interiors, and
$\sum_i \mathrm{area}(P_i) = \mathrm{area}(T_6)$ exactly, with the observation that finitely many
**closed** sets of full measure in $T_6$ leave a relatively open null set, i.e. nothing. That
argument is correct and it is the right way to rule out a missed sliver.

**I have built an independent verifier** for whatever it produces —
[`covercheck.py`](../../../../experiments/packing-eo-verify-2/covercheck.py) — which checks, all
exactly and all in my own code: (C1) every piece's squared diameter, (C2) containment in $T_a$,
(C3) pairwise interior-disjointness by exact convex-polygon intersection area, (C4) the area sum,
and (C5) an independent coverage probe over a rational grid plus every piece vertex and edge
midpoint. It reproduces the 36-piece baseline exactly, and both negative controls fire (delete one
piece: C4 and C5 both catch it; inflate one piece: C1 catches it).

> **One structural observation the construct lane should have, and it is not encouraging.**
> A partition of $T_6$ into $26$ sets of diameter $\le 1$ would prove Erdős–Oler at $k = 7$ — that
> direction is right and is the point of the lane. But the same scaling bounds the target from the
> other side. The number of diameter-$\le1$ pieces needed is at least the largest number of points
> of $T_6$ at pairwise distance **strictly** $>1$; scaling a separation-$1$ configuration in $T_a$
> up by $6/a > 1$ shows that number is
> $$N^\ast \;\ge\; \sup_{a<6}\ \max\{\,n : n \text{ points at separation} \ge 1 \text{ fit in } T_a\,\}.$$
> Erdős–Oler at $k = 7$ says that supremum is $\le 26$; **if the conjecture is false the floor is
> $\ge 27$ and no 26-partition exists.** So the search is bounded below by the very statement it
> is trying to prove, and $26$ is the smallest value not immediately excluded.
>
> Whether the floor is *exactly* 26 turns on whether $a_{26} < 6$, which I did **not** settle — it
> is expected (the Erdős–Oler pattern is $a_{T(k)-1} = a_{T(k)}$, with $n = T(k)-2$ strictly
> below), but expected is not proved and I exhibit no 26-point configuration. Either way the
> reading is the same: **there is little or no slack in the target.** The lane is looking for a
> tight extremal object rather than for something with room in it — a reason to expect the search
> to stop at 27 or 28, and a reason to check any claimed 26 extremely hard. It does **not** make
> the route dead.

### 10.1 A checkable defect in `../eo-covering-bound/`'s search output (mid-flight)

The lane's separated-point search (`out/shrink_n*.json`) looks for $n$ points at min distance
$\ge 1.002$ in the smallest $T_a$ it can find. Normalising each row to separation $1$ (divide $a$
by the achieved min distance):

| $n$ | 21 | 22 | 23 | **24** | **25** | 26 | 27 |
|---|---:|---:|---:|---:|---:|---:|---:|
| separation-1 side found | 5.000003 | 5.605549 | 5.732062 | **6.001131** | **5.971422** | 6.000019 | 6.000019 |

**Row 24 is impossible.** $a_n$ is non-decreasing in $n$ — delete a point from an $n$-point
configuration and you have an $(n-1)$-point one in the same triangle — so $a_{24} \le a_{25}$, and
the table has $a_{24} > a_{25}$. Independently, $a_{24} \le 6$ outright, since deleting four points
from the $28$-point $T(7)$ lattice leaves $24$ points at separation $1$ in $T_6$. The $n = 24$ run
is stuck in a local optimum, as are $n = 26$ and $n = 27$, which return the *identical* value —
the signature of the optimiser finding one configuration and not exploiting the extra freedom at
the smaller $n$.

Two consequences, both useful to that lane:

- **The floor it can currently prove is 25, not 26.** The largest row strictly below $6$ is
  $n = 25$ at $5.971422$; scaling that configuration up into $T_6$ gives 25 points at pairwise
  distance $\approx 1.00478 > 1$, so $N^\ast(T_6) \ge 25$. Rows 26 and 27 sit at $6.000019 > 6$
  and give nothing. So on its own data the lane is one short of the 26 it needs, and the shortfall
  is an optimiser artefact rather than a fact about the problem.
- **Nothing here refutes Erdős–Oler**, and I checked that specifically, because it is what a
  row like $n=27$ at "$a = 6.012$" looks like before you normalise. Normalised it is
  $6.000019 > 6$ — *above* the conjectured value, not below. No row is a counterexample.

A monotonicity assertion across $n$ is a cheap and complete guard against exactly this failure,
and it belongs in that lane's harness.

**Update — exact certificates have since landed, and I verified them.** `out/certificates.json`
now carries exact *rational* coordinates (no floats), and I re-checked each one in my own code:
every pairwise squared distance in the lattice basis $u^2+uv+v^2$, containment
($u,v \ge 0$, $u+v \le a$), the point count, and that no two points coincide.

| $n$ | $a$ (exact) | claimed $\min d^2$ | my $\min d^2$ | inside $T_a$ | separation-1 side | verdict |
|---:|---|---|---|:--|---:|---|
| 22 | $2808381/500000$ | $1.004002982$ | matches exactly | yes | $5.605554$ | **CONFIRMED** |
| 23 | $717941/125000$ | $1.004004000$ | matches exactly | yes | $5.732064$ | **CONFIRMED** |
| 25 | $5983367/1000000$ | $1.004002073$ | matches exactly | yes | $5.971430$ | **CONFIRMED** |
| 24, 26, 27 | — | — | — | — | — | not certified by the lane |

> **Independently verified: $N^\ast(T_6,\ \mathrm{diam}\le1)\ \ge\ 25$.** Scale the 25-point
> certificate up by $6/5.971430 > 1$: it lands in $T_6$ with every pairwise distance $>1$, so no
> two of its points can share a set of diameter $\le 1$. This is **non-circular** — the
> configuration is exhibited and checked, and no literature $a_n$, $s(n)$ or $d(n)$ enters it, as
> that lane's K2 requires. It is a real result and my check agrees with it.
>
> It is also **one short**: 26 is what would kill the construct lane, and 25 does not.

**One convention mismatch to fix.** The lane's `KILL-CRITERION.md` states cartesian corners
$(0,0)$, $(a,0)$, $(a/2, a\sqrt3/2)$; the certificates are in the **lattice basis** $(u,v)$.
Under the stated cartesian reading the points are *outside* the triangle — e.g. $(0, 4.6148)$ with
$a = 5.6168$. The code is self-consistent and the certificates are correct; it is the prose that
is wrong. This is precisely the divergence problem `RULES.md` §2 fixes conventions to prevent, and
a second checker following the written convention would reject a valid certificate.

### 10.2 `../eo-covering-construct/`'s state (mid-flight, not a finding)

**Best count so far: 28**, from a hexagon tiling of $T_6$ at $\theta = \pi/6$
(`hex_a6.json`, `hexinit6.txt`). That is a genuine improvement on the 34 recorded in
[`../eo-oler-equality/`](../eo-oler-equality/) §8 and on the 36 of the uniform subdivision, and it
is still **2 above the 26 the lane needs**. Consistent with the structural note above: the
remaining two pieces are exactly the part with no slack in it.

**Its controls have not converged**, and this is worth flagging to the lane rather than holding
against it. For $T_2$ into 4 pieces the medial subdivision is an exact solution with diameter
exactly 1; the optimiser reports `max_diam` $= 1.0004$. For $T_3$ into 9 pieces the uniform
subdivision is exact at diameter 1; it reports $1.00013$. **An optimiser that cannot reach a known
optimum of its own control by $10^{-4}$ will not distinguish 26 from 27 at the boundary**, which
is the only place the answer lives. Both are float search output and the lane's `§7 guard`
already says floats decide nothing — but a certificate must eventually arrive in **exact
rationals** (problem `RULES.md` §2 bans decimal strings in exact fields), and every JSON the lane
has written so far is float throughout.

**If a $\le 26$ certificate does land**, run it through
[`covercheck.py`](../../../../experiments/packing-eo-verify-2/covercheck.py) as well as the lane's
own checker. Two independent checkers agreeing is what problem `RULES.md` §3 asks for, and given
that a 26-piece partition would settle an open case, it is the minimum.

### 10.3 Final state — both lanes finished, and I verified every certificate

Both write-ups landed. **Neither claims a proof of an open case, and both are right not to.**

**`../eo-covering-construct/`: 28, not 26.** Its Lemma L construction (Voronoi cells of a
$\Delta(p)$ array of spacing $\sqrt3/2$ centred in $T_a$) splits $T_6$ into $\Delta(7) = 28$
convex cells of diameter $\le 1$. I rebuilt every certificate **from the printed definition** — for
the power-diagram certificates, from $|x-p_i|^2-w_i \le |x-p_j|^2-w_j$ expanded into half-planes
and clipped against $T_a$ in the lattice basis, where $Q(u,v) = u^2+uv+v^2$ keeps everything
rational; for `cert28.json`, from its explicit $\mathbb{Q}(\sqrt3)$ cells
(`check_covering_certs.py`).

| certificate | $N$ | $a_0$ | my exact max squared diameter | $\sum$ areas $=$ area $T_{a_0}$ | verdict |
|---|---:|---:|---|:--|---|
| `cert26.json` | 26 | $2889/500 = 5.778$ | $0.999665281527$ | yes | **VERIFIES** |
| `cert27.json` | 27 | $2901/500 = 5.802$ | $0.999898028410$ | yes | **VERIFIES** |
| `cert28opt.json` | 28 | $762/125 = 6.096$ | $0.999728640668$ | yes | **VERIFIES** |
| `cert28.json` (lattice, $p=7$) | 28 | $6$ | **exactly $1$** | yes | **VERIFIES** |

All four are genuine. **And all four are weaker than Oler**, which is the lane's own headline and
I confirm it:

| | gives | Oler gives | beats Oler? |
|---|---|---|---|
| `cert26` | $a_{27} \ge 5.778000$ | $5.865460$ | **no** |
| `cert27` | $a_{28} \ge 5.802000$ | $6.000000$ | **no** |
| `cert28opt` | $a_{29} \ge 6.096000$ | $6.132169$ | **no** |

**The 26-piece certificate covers $T_{5.778}$, not $T_6$.** That is the number to hold on to: a
26-piece cover of $T_6$ would prove Erdős–Oler at $k=7$; a 26-piece cover of $T_{5.778}$ gives
$a_{27} \ge 5.778$, which is $0.087$ *behind* what Oler already gives for free. **No open case is
settled and none is claimed.**

Two notes. (i) `cert28.json` has max diameter **exactly 1**, not $<1$. That is fine and the lane
states the reason correctly — the scale-free step only ever applies it at $a < a_0$ strictly, where
the diameters become $a/a_0 < 1$ — but it is the one place where a careless reuse at $a = a_0$
would be wrong. (ii) I verified Lemma L only at $p = 7$, $a = 6$; the lane's stronger claim that
the scheme survives to $a = 7\sqrt3/2 = 6.0622$ I did **not** check, and its "general $p$" is its
own `sketch`.

**`../eo-covering-bound/`: floor 25, and it says the route is not killed.** Verdict and gap
correct. A kill needs $N^\ast \ge 27$ (not 26 — you must exclude a 26-piece cover), the proved
floor is 25, so **the gap is 2**, as stated. My independent verification of its $n = 22, 23, 25$
exact certificates (§10.1) agrees with the 25.

> **The synthesis neither lane can state alone.** Putting the two verified results together:
> $$25 \;\le\; N^\ast(T_6,\ \mathrm{diam}\le1) \;\le\; 28,$$
> both ends independently checked here. Erdős–Oler at $k=7$ would follow from $\le 26$ and would
> be refuted by $\ge 27$ being *unachievable*… no: to be precise, $\le 26$ proves it, and
> $N^\ast \ge 27$ merely closes this route without saying anything about the conjecture. The open
> window is exactly the two values 26 and 27, and **today moved neither end into it.**

---

## 11. What is safe to build on, and what is not

**First, the flat answer `RULES.md` §3 requires: nothing here is assumable.** Everything is
`sketch`, before and after this pass, because a same-family review grants no status. The column
below answers the weaker question the brief actually asked — *has an independent reader
re-derived it from the statement and tried to break it?*

| Claim | Re-derived? | Safe to build on? |
|---|---|---|
| **P1**, $\lvert E\cap\partial T\rvert \le 3\lfloor a\rfloor$ (`eo-boundary-counting` §3.1) | yes, incl. the charging step and the empty-side cases | **Yes**, and it is sharp for every $a\ge1$. The corner-charging bookkeeping is load-bearing — copy it, not just the statement |
| **W1**, $b$ collapses to 3 at the perturbed lattice (`eo-boundary-counting` §4) | yes, exactly | **Yes.** Every printed row is exactly right |
| **T1**, *no $\Phi(b)$ exists* — as a **theorem** | yes, with a repaired family | **Yes, but re-derive it.** Use $\lambda_k = 1+1/k^3$, $\varepsilon_k = \lambda$'s $\delta/2$; the fixed-parameter family in §5 gives only $\Phi(3)\ge56.1$ |
| **T1 as proved in §5**, and the same sentence in `oler-slack-analysis` §4 | no | **NO — the proof does not go through** (D2). The conclusion survives; the argument as written does not |
| **Resolution theorem** (`eo-exhaustion` §5), as a **theorem** | yes, exactly, on 8568 cell pairs | **Yes** — but as a *termination guarantee*: fine cells **suffice** |
| **"a cell exhaustion can only close once $h<\sqrt3(1-\rho)$"**, §5's contrapositive; §6.2's "needs level $\ge9$"; §5's "there is no budget at which this terminates" | no | **NO — this is the most damaging item in this report** (D1). It is the converse, and the file's own $k=3$ case refutes it at level 1 |
| **`eo-exhaustion` §1.1**, monotonicity + finiteness | (first pass) | **Yes** — and it, not §5, is the real obstruction. §5 is not needed for it |
| **`eo-exhaustion` §2** table, residual gap, $\rho_{\rm Oler}$ | yes, exactly | **Yes**, with $\ge$ not $>$ (D3) |
| **`eo-exhaustion` §4** `numerical` rows | no — see §7 and Q1 | **Not examined.** The derived quantities are right; the measurements are not re-derivable and Q1 names a circularity vector in that pipeline |
| **`oler-slack-analysis` §1** identity, $F=2n-b-2$, BE $\ge0$ | yes; **agrees with Codex on PR #90 at every point** | **Yes** — and this one has a genuine cross-family review behind it, which nothing else here does |
| **Lemma T** with its equality classification, incl. Step 3 (`eo-oler-equality` §1) | yes, proof and scans | **Yes.** Step 3 is correct; the vertex enumeration is complete |
| **T2** the $\tau$-identity; **S2** deficit $\ge1$ *is* Erdős–Oler | yes | **Yes.** S2 in particular: $\varepsilon = 1$ is not a milestone, it is the conjecture |
| **Groemer $\equiv$ Oler** (`eo-epsilon` §1) | yes, own symbolic ring | **Yes as algebra.** Conditional on the README's transcription of Groemer p. 285, which nobody has re-read |
| **Theorem E**, $d(n) > a^\*_n$ strictly for non-triangular $n$ (`eo-epsilon` §2) | yes; 16/16 consistent with the `cited` table | **Yes**, with its dependency on Groemer's equality clause stated at every use. Explicit $\varepsilon$ is still $0$ |
| **Theorem Q**, quantitative Lemma T (`eo-epsilon` §3) | yes; 93 366 exact triangles | **Yes** |
| **Proposition V**, step (1) is vacuous (`eo-epsilon` §4) | yes | **Yes**, reading (V1) as *"the inequality (\*) produces is never stronger than the target"*. $\Psi$ plus an interior-edge bound is untouched |
| **`eo-covering-bound`** exact certificates $n = 22, 23, 25$ | yes, exactly | **Yes.** Verified in my own code; they give $N^\ast(T_6) \ge 25$, non-circularly (§10.1) |
| **`eo-covering-bound`** raw `shrink_n*.json` search rows | yes | **NO.** Row $n=24$ violates monotonicity in $n$ and is impossible; rows 26/27 are stuck at one configuration (§10.1). The lane did not certify these, correctly |
| **`eo-covering-construct`** certificates (26@5.778, 27@5.802, 28@6.096, lattice 28@6) | yes, all four rebuilt from the definition | **Yes as certificates** — every one verifies exactly. But **all four are weaker than Oler**; none settles anything (§10.3) |
| **`eo-covering-construct`** Lemma L for general $p$, and the $a \le 7\sqrt3/2$ range | only $p=7$, $a=6$ | **Partly.** I verified 28 cells covering $T_6$; the general-$p$ claim is the lane's own `sketch` and I did not check $a = 6.0622$ |
| **`eo-subinteger-relaxation`** §5 proof of EO at $k=4$, and Lemma D | yes, both re-derived | **Yes.** Correct, uniform in $a<3$, degrades correctly at $a=3$, and **non-circular** (§9) |
| **`eo-literature`** null result and its blocked-egress finding | yes, probed myself | **Yes.** No source is promoted; the operational advice is right |

### Claimed proofs of open cases — my independent verdict

**There are none.** I checked specifically, because that is what this pass exists for:

- **`eo-covering-construct` reports 28, not 26 — no open case is settled.** I rebuilt all four of
  its certificates independently and **all four verify exactly**; that is a real result and the
  lane deserves credit for it. But the certificate labelled "26" covers $T_{5.778}$, **not**
  $T_6$, and therefore gives $a_{27} \ge 5.778$ — $0.087$ *behind* what Oler gives for free. A
  26-piece cover of $T_6$ would have proved Erdős–Oler at $k=7$; that object does not exist in this
  round's output. **My verdict: nothing here proves an open case, and the lane does not claim
  otherwise.**
- `eo-subinteger-relaxation` reports **no infeasibility at $k \ge 5$**. It does prove Erdős–Oler
  at $k = 3$ and $k = 4$ — both already `cited` — and I checked that proof line by line and found
  it correct and **not circular**: its two capacities are geometric (diameter and circumradius),
  and it correctly says nothing at $a = 3$, where 10 points do fit. A valid new proof of a known
  case, claimed as exactly that.
- `eo-epsilon` explicitly reports **$\varepsilon = 0$** in its first line. Theorem E is a strict
  improvement ($d(27) > a^\*$) and is *not* a proof of any open case; the lane says so.
- `eo-covering-bound` has an exactly verified floor of **25** — confirmed independently, and
  genuinely non-circular — and reports honestly that the route is **not** killed, since a kill
  needs $27$. Gap 2, as stated.
- **No row anywhere in the round-2 output refutes Erdős–Oler.** The one that superficially looks
  like it might — `shrink_n27.json` at "$a = 6.012$" — normalises to $6.000019 > 6$, i.e. *above*
  the conjectured value. I checked this explicitly (§10.1).

So: the campaign's round-2 output is **four honest negative or partial results** — $\varepsilon = 0$,
no infeasibility, 28 not 26, floor 25 not 27 — every one of them reported as such in its own first
line, with kill-criteria fixed in advance and fired as written. I found no overclaim in round 2.

**Both disagreements in §0 are in round-1 material that is still being quoted**, and both have the
same shape as the two the first pass found: a correct theorem read one logical step too broadly.
That is now four instances of the same failure mode in this campaign, which is worth saying out
loud — the errors here are not arithmetic, they are the sentence *after* the arithmetic.
