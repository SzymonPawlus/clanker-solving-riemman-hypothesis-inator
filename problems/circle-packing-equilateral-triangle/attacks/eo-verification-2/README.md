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
