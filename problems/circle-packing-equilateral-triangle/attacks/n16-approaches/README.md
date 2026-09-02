# Round-3 attack proposals for $n=16$: new mechanisms, triaged by execution

**Claim type: NEITHER of the two in problem [`../../RULES.md`](../../RULES.md) §1.** No bound on
$s(16)$ or $a_{16}$ is asserted here, in either direction. The exact computations below bound
*auxiliary* quantities only (relaxation values $M$, $M_6$, $\delta(16)$, transference ceilings,
a Handelman LP value). Nothing enters `results/`.

- Author: `claude`, worker **I1** (Fable 5, divergent/generative role per repo
  [`RULES.md`](../../../../RULES.md) §8), 2026-08-22, issue
  [#97](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/97),
  branch `claude/circle-packing-subagents-9yg5gt`
- Code: [`experiments/packing-n16-approaches/`](../../../../experiments/packing-n16-approaches/)
  — Python stdlib + numpy/scipy; **every reported kill/keep decision that carries weight is an
  exact `Fraction` computation**; floats appear only inside searches and in the one LP-value
  measurement, and are labelled as such
- Journal: [`notebook/claude/2026-08-22-n16-approaches.md`](../../../../notebook/claude/2026-08-22-n16-approaches.md)

| assertion | status |
|---|---|
| exact witnesses: $M(16)\le 17/4$, $M_6(16)\le 449/100$, $\delta(16)\le\sqrt{13}$, transference ceilings | `numerical` — exact rational verification of one explicit object each |
| the three inclusion lemmas behind the transference ceilings (§P4–P6) | `sketch` — mine, elementary; the classical constants are standard but re-derived, not sourced |
| Handelman degree-4 value $h_4\approx 1.2109$ for $n=4$ | `numerical`, **float LP** — weakest evidence class here, sufficient only for the kill it makes |
| "$M_6(16)\approx 4.48 >$ record" | **search impression, not assumable** — a failed search proves nothing ([`../approaches-round-2/`](../approaches-round-2/) §L discipline) |

Nothing above is assumable, including by me (repo `RULES.md` §3). Kill-criteria were written into
each script's docstring **before** the search/bisection ran; the honest order is recorded here.

**Circularity guard.** No value of $a_{16}/d(16)/s(16)$ enters any computation. The numerical
16-point packing (`experiments/circle-packing-search/out/n16.json`) is used in exactly one role:
as a *seed* for searches whose output only produces **upper bounds on auxiliary relaxation
values** — i.e. inputs to kill decisions about methods, never to a bound on $a_{16}$. Any future
*lower* bound on $M_6(16)$ (the surviving proposal) must not touch that file; §P1 says so again.

## §6.1 dedup statement

Checked against [`../candidate-approaches/`](../candidate-approaches/) (A–H),
[`../approaches-round-2/`](../approaches-round-2/) (I–O), all `n16-*` and `eo-*` lanes, and the
worker assignments of issue #97 (F2 fractional covering, M2 mixed-capacity pigeonhole, U2 packing
side). Nothing below re-proposes: the 15-piece covering family or its plateau
(`n16-covering*`, `n16-structure`), piece counting, area budgets (Lemma S), occupancy exhaustion
(`n16-occupancy`), corner cuts (`eo-hull-deficit` §5), boundary counting, dyadic B&B (PR #56),
strip counting (round-2 N — but see P1, which is the multi-direction disjunctive version N's own
write-up explicitly left open), fractional covering (F2), mixed capacities (M2). Where a proposal
touches a parked sketch (C, E, K, O of earlier rounds), the overlap and the new content are stated
inside the proposal.

---

## The proposals, ranked

Summary table (details below; scores are promise/cost on 1–5, after the kill-runs):

| # | mechanism | outcome of cheapest kill | promise | cost |
|---|---|---|---|---|
| P1 | $k$-direction tomography (polygonal-norm) relaxation | $k=3$ **killed exactly**; $k=6$ **survived** — transition sits numerically *above* the record | 4 | 3 |
| P2 | Lasserre level-2 SOS with symmetry reduction (ex-C) | not runnable here (no SDP solver); level-1 computed exactly: hopeless | 2–3 | 4 |
| P7 | boundary-aware Voronoi/Delaunay à la the disk-container optimality proofs | not run — literature-gated | 3 | 4 |
| P9 | CEGAR/SAT-style lazy refinement certificate search | flat encoding **killed by granularity arithmetic**; lazy variant parked | 2 | 4 |
| P10 | contact-graph rigidity census | deferred to parked E/#11; one new ingredient noted | 2 | 4 |
| P3 | Handelman/Krivine LP Positivstellensatz | **killed**: 30.1% slack at $n=4$ | 1 | — |
| P4 | transference from the square (Wengerodt-type) | **killed exactly**: ceiling $3(\sqrt6-\sqrt2)<$ Oler | 0 | — |
| P5 | transference from the disk (Fodor-type) | **killed exactly**: ceiling $2\sqrt3<$ Oler | 0 | — |
| P6 | diameter-only / distance-matrix (CNSD rank-4) relaxation | **killed exactly**: $\delta(16)\le\sqrt{13}<$ Oler | 0 | — |
| P8 | retire round-2 O (Oler stability at $T_5+1$) vs the moved record | obsolescence arithmetic, no run needed | — | 0 |

---

### P1. Tomography / polygonal-norm relaxation — piecewise-linear lower bounds in $\mathbb{Q}(\sqrt3)$

**(i) Mechanism.** Project pair differences onto $k$ lines at $180°/k$ spacing. For $k=3$ (the
three side normals), in oblique coordinates $u,v$ the squared projections of $\Delta=(du,dv)$ are
$\tfrac34 du^2,\ \tfrac34 dv^2,\ \tfrac34(du{+}dv)^2$, so $|\Delta|\ge1$ forces
$\max(|du|,|dv|,|du{+}dv|)\ge1$ — the worst case is a side-parallel unit vector, $30°$ from the
nearest projection line, losing $\cos30°$. For $k=6$ (normals + side directions) the loss is only
$\cos15°$: $|\Delta|\ge1$ forces $\mathrm{dod}(\Delta):=\max_f w_f|L_f(\Delta)|\ge\cos15°$, six
rational linear forms $L_f$, weights $w_f\in\{\tfrac{\sqrt3}2,\tfrac12\}$. Define
$M_k(n)$ = least $a$ admitting $n$ points in $T_a$ with pairwise polygonal-norm separation at the
$\cos(90°/k)$ threshold. Then $a_{16}\ge M_k(16)$, and — the point — every pair constraint is a
**disjunction of $2k$ half-planes**: the whole problem is piecewise linear, so a lower bound on
$M_k(16)$ is certifiable by a finite tree of exact rational Farkas certificates, no square roots
except the threshold ($\cos^2 15°=\tfrac{2+\sqrt3}4\in\mathbb{Q}(\sqrt3)$, the field the repo
already computes in).

**(ii) Would prove.** $a_{16}\ \ge\ M_6(16)$. The numerical transition of the $k=6$ search sits at
$\approx4.483$; **if** that is real and certifiable, it beats the standing record $1+2\sqrt3=
4.4641$ by $\approx0.019$ — by a mechanism that is not a covering, not a pigeonhole, and not
interval arithmetic.

**(iii) Cheapest kill (run — see outcomes).** Search for explicit configurations; any
exactly-verified configuration at $a$ below the record kills that $k$ forever
(it proves $M_k(16)\le a<1+2\sqrt3$, and the relaxation can never certify more than $M_k$).

**(iv) Why not already dead.** Strip counting (round-2 N, dropped) is the **one-direction**
version, and its write-up explicitly left "non-parallel slicing" open. Nothing else in the repo
projects; nothing else is piecewise linear. Multi-direction disjunctive projection appears in no
prior lane.

**(v) Scores.** Promise 4, cost 3 (certification is a disjunct branch-and-cut of unknown depth —
the honest risk).

**Kill-run outcomes (exact where stated):**

| $k$ | exact witness (verified in `Fraction`/$\mathbb{Q}(\sqrt3)$) | search floor | verdict |
|---|---|---|---|
| 3 | $M(16)\le \mathbf{17/4}=4.25$ | — | **DEAD vs record** ($17/4<1+2\sqrt3$, exact); note $17/4>$ Oler — the 3-direction LP already out-proves Oler, a curiosity the record supersedes |
| 6 | $M_6(16)\le \mathbf{449/100}=4.49$ | 150-restart iterated-LP search finds nothing at $a\le4.48$ (best margin $0.99899\times$ threshold at $4.48$; margins $0.9901,0.9945,0.9956,0.9968$ at $4.44,4.46,4.465,4.47$) | **SURVIVES**: the interval $(4.48,4.49]$ numerically brackets $M_6(16)$, *above* the record |
| controls | $M_3(3)$ search $=1=a_3$; $M_3(4)\le3/2<\sqrt3=a_4$ (the corner cheat, found by hand and by search); $M_3(15)$ search $=4=a_{15}$; the $k=6$ norm rejects the $n=4$ cheat (its dod-margin is $0.897<1$) | | engine behaves |

Read the $k=6$ line with §L discipline: the failed search below $4.48$ is `numerical` evidence for
*where to aim a certification attempt*, never a bound. Equally, the exact side is unconditional:
$M_6(16)\le 449/100$, so this route's ceiling is **at most** $4.49$ — bounded profit, cleanly
quantified, and still above the record.

**Exact first step for the next worker.** Build the disjunct branch-and-cut: at fixed rational
$a$ (start $a=4.47$), branch on the six sign-resolved forms of one violated pair per node, prune
nodes whose LP is infeasible, and emit an exact rational Farkas certificate per pruned leaf.
Validate by computing $M_6(4)$ and $M_6(5)$ exactly (pair counts 6 and 10 — enumerable), then
measure node growth on $n=10,12,15$. **Kill-criterion for that worker-day:** if measured growth
extrapolates past $10^9$ nodes at $n=16$, or if $M_6(15)<4$ turns out to hold with a witness (which
would cap how much of the $a_{15}=4$ structure the relaxation sees and bound its strength — check
this early: it costs one search run), record and stop. The certification code must not read
`circle-packing-search/out/` (guard above). Also worth one hour: the $k=12$ search, to measure the
value-vs-$k$ curve ($\cos7.5°=0.9914$; expected value $\approx4.56$, expected certification cost
worse — the curve tells us whether $k=6$ is the sweet spot).

---

### P2. Lasserre level-2 SOS with $S_{16}\times D_3$ symmetry reduction (rehabilitate parked C)

**(i)** The moment/SOS hierarchy on "16 points, pairwise $\ge1$, in $T_a$" at fixed $a$: a
degree-2 Positivstellensatz infeasibility certificate, exactly checkable after rational rounding.
Proposed as C (2026-08-17), size-counted, never run. **(ii)** $a_{16}\ge a$ for whatever $a$ the
level-2 relaxation refutes; no useful prior on the value. **(iii)** Cheapest kill: level-2 on
$n=4,5$ (tiny), measure slack against $a_4=\sqrt3$, $a_5=2$; $>1\%$ slack kills it for 16.
**Blocked here: this environment has scipy only — no SDP solver (checked: cvxpy, mosek, pysat all
absent), and scipy has none.** What I could run exactly: the **level-1** (second-moment) value —
$\sum_{i<j}|p_ip_j|^2=16\sum_i|p_i-\bar p|^2\ge\binom{16}{2}$ against the circumradius gives
$a\ge\sqrt{45/64}\approx0.84$ — hopeless, so *everything* rests on the genuinely semidefinite
part; and P3's result below shows the LP fragment of the hierarchy is also hopeless. That sharpens
C's risk assessment: there is no cheap approximation to the answer; only a real SDP run decides.
**(iv)** C is a parked sketch, not a dead one; the two new measurements (level-1 exact, LP fragment
measured) are new. **(v)** Promise 2–3, cost 4–5, **conditional on solver availability** — a
worker with network/pip access should install an SDP solver first and run the $n=4,5$ gate; that
gate is one session.

---

### P3. Handelman/Krivine LP Positivstellensatz — **KILLED**

**(i)** Same as P2 but products-of-constraints with nonnegative scalars instead of SOS
multipliers: certificate search is a pure LP, runnable in this environment, exactly
rationalizable. **(ii)** Same conclusion shape as P2. **(iii) Kill (fixed in advance, run):**
bisect the largest $a$ certified at product-degree $\le4$ for $n=4$; gate $h_4<1.6$.
**Outcome: $h_4\in[1.2109,1.2110]$ (float LP), slack $30.1\%$ against $a_4=\sqrt3$.** The gate
fired by a factor-of-four margin; at $n=16$ the needed precision is $3.5\%$. Dead. **(iv)** No
prior lane ran any Positivstellensatz LP. **(v)** Promise 1 post-mortem; the reusable content is
the poly-arithmetic scaffolding and the measured fact that the hierarchy's LP fragment carries
essentially nothing — the SOS blocks are load-bearing (feeds P2's risk assessment).

### P4–P6. Transference — **all three KILLED exactly**, with unconditional ceilings

Mechanism family: if $T_a\subseteq C$ (scaled), a lower bound for container $C$ transfers.
Each has an algebraic **ceiling**: the bound it could prove *even with a perfect lower-bound
oracle* for $C$, namely (best $C$-bound) $\times$ (inclusion factor). Computed exactly
([`transference.py`](../../../../experiments/packing-n16-approaches/transference.py)), against
Oler $=(-3+\sqrt{129})/2=4.17891$ (`cited`):

| route | inclusion factor | oracle bound | ceiling | vs Oler |
|---|---|---|---|---|
| P4 square | min enclosing square of $T_a$ has side $\frac{\sqrt6+\sqrt2}4a$ | $L(16)\le3$ (4×4 grid witness, exact) | $\le 3(\sqrt6-\sqrt2)=3.1058$ | **below** |
| P5 disk | $T_a\subset$ disk of radius $a/\sqrt3$ | $R(16)\le R(19)\le2$ (19 lattice points in radius 2, exact) | $\le 2\sqrt3=3.4641$ | **below** |
| P6 diameter-only (incl. any distance-matrix / CNSD-rank-4 relaxation, which sees the container only through $\mathrm{diam}\,T_a=a$) | — | $\delta(16)\le\sqrt{13}$ (best 16-of-19 lattice subset, exact) | $\le\sqrt{13}=3.6056$ | **below** |

All three ceilings are *witness-certified and permanent*: no future theorem about squares, disks,
or distance matrices can push them past Oler, because the witness configurations exist. The
triangle's corners are precisely where a 16-point packing earns its side length, and every
containment relaxation throws the corners away. Promise 0; documented so §6.1 stops anyone
re-deriving them. (These kills also cap P2-style relaxations *that drop the container*: any bound
factoring through pairwise distances alone is under $\sqrt{13}$.)

### P7. Boundary-aware Voronoi/Delaunay — the disk-container optimality technique, never tried on the triangle

**(i)** The modern *proven* optimality results for points in a **disk** (the Fodor-line of proofs,
$n$ around 11–19) do not use pigeonhole coverings: they partition the container along the
Delaunay/Voronoi structure of the *unknown* configuration and bound per-cell area/angle payloads
against boundary distance, deriving a contradiction below the critical radius. Oler's inequality
is the crude ancestor (uniform per-cell payload); the disk proofs show the refined per-cell
version can close *individual hard cases*. Proposal: transfer the technique, not a formula, to
$T_a$ at $n=16$. **(ii)** Potentially the full conjectured value $a_{16}=4.6247\ldots$ — this
technique family has actually closed cases of this difficulty, which nothing else on this list has.
**(iii) Cheapest kill:** one session of literature (WebSearch works in-session; full texts are
blocked — [`../n16-literature/`](../n16-literature/) §0 has the measured egress boundary) to
determine the exact per-cell inequalities used in one disk proof; then one session testing the
per-cell payload numerically against the $n=16$ slack budget ([`../oler-slack-analysis/`](../oler-slack-analysis/)
already localises where Oler's slack lives — reuse it). If the transferred per-cell floors sum
below area$(T_a)$ at $a=4.55$, the naive transfer is dead; record the table. **(iv)** The repo's
Oler-refinement attacks (`eo-hull-deficit`, `eo-boundary-counting`, `oler-slack-analysis` §4
face-excess refutation) attacked *Oler's own decomposition*; none imported the disk-container
cell inequalities. The refuted face-excess hypothesis does not refute position-dependent cell
floors. **(v)** Promise 3, cost 4 (the cost is mostly that texts are unreachable; the method must
be reconstructed from citable statements — flag to the manager that this is the single strongest
argument for getting one PDF into the repo by human hands).

### P8. Retire round-2 proposal O (Oler stability at $T_5+1$) — obsolescence arithmetic

O (2026-08-18) aimed to prove $a_{16}\ge4+\varepsilon_0$ by a stability version of Oler at
$n=15=T_5$: it was written when the rigorous floor was $a_{16}\ge4$. The floor is now
$1+2\sqrt3=4.4641$ (`sketch`), and the packing side says $a_{16}\le4.6248$ (`numerical`). For O to
matter *now* it must deliver $\varepsilon_0>0.4641$ — but $0.4641$ is $74\%$ of the whole
remaining interval $[4,4.6248]$, i.e. the "perturbative" regime O reasons in would have to extend
essentially to the answer, where 15-point configurations are nowhere near the $T_5$ lattice (they
have $11.6\%$ dilation slack to rearrange in). A stability constant of that size *is* the solved
problem. **Recommendation: mark O superseded-by-the-record on the board; do not spend its two
budgeted sessions.** No run needed; this is one line of arithmetic against the current table.

### P9. CEGAR / lazy-refinement propositional certificates — flat encoding killed by arithmetic

**(i)** Round-2 K (SAT with proof logging) at a *fixed* grid granularity, or any flat
"cells-as-Booleans" encoding. **(iii) Kill by granularity arithmetic (no run needed):** to refute
$a=4.4641$ the abstraction must separate it from the feasible scale $4.4641/4.6248=0.9653$; cells
of diameter $\delta$ blur each pair constraint by up to $2\delta$, so $\delta<0.0174$ is forced,
giving $\sim6.6\times10^4$ cells and $\sim8\times10^8$ pairwise-exclusion clauses — dead flat, at
any solver strength, before search hardness is even discussed. **(ii/v)** A *lazy* (CEGAR)
variant — coarse cells, refine only where a satisfying pattern survives, learn exclusions across
patterns — is exactly what `n16-occupancy`'s measured wall ($20349$ patterns $\times$ 30–60 s)
calls for, and clause learning is the one mechanism that engine lacks. But: no SAT solver in this
environment, and the per-pattern cost arithmetic above still governs the refined leaves. Promise
2, cost 4; parked with the arithmetic recorded so nobody builds the flat version. **(iv)** K was
never run; the flat-encoding kill is new; the occupancy wall measurement it leans on is from
`n16-occupancy` (cited as `numerical`).

### P10. Contact-graph rigidity census — defer to parked E, one new ingredient

E (candidate-approaches) already scopes contact-graph enumeration with exact algebraic solving,
including the honest exhaustiveness obstacle (rattlers). The one new ingredient this round adds:
the deep-triangle capacity from [`../n16-structure/`](../n16-structure/) (interior points $\ge1$
from all sides live in $T_{a-2\sqrt3}$, capacity $\le3$ for $a<3\sqrt3$) is a *structural
constraint on the census* — every candidate graph must place $\ge13$ of 16 vertices in the
boundary collar, which crushes the planar-graph enumeration space. Still capped by E's
exhaustiveness lemma, which nobody can yet state soundly. Promise 2, cost 4; fold into E/#11 if
that lane reopens, do not open separately.

---

## Shortlist — what I would stake the next worker-day on

1. **P1, $k=6$ certification** (first step and kill-criterion written out in P1 above). It is the
   only live mechanism whose numerical value sits *above* the standing record, its profit and its
   ceiling are both already exactly bracketed ($(4.48,\,449/100]$ numerically, $\le449/100$
   unconditionally), and its certificates live in pure rational LP — the most
   review-friendly artifact class this repo has.
2. **P7 literature-first**: one WebSearch session to reconstruct the disk-container per-cell
   inequalities, one session to budget them against the $n=16$ slack atlas. Highest ceiling on
   the list; dies cheaply if the transferred floors don't sum.
3. **P2 gate, conditional**: the moment an SDP solver is available (or a worker gets pip), run
   level-2 on $n=4,5$ and read the slack. One session, decisive either way, and P3's measured LP
   failure means no cheaper proxy exists.

## What died today (documented refutations, per repo `RULES.md` §0)

- **P1 at $k=3$**: $M(16)\le17/4$, exact — can never reach the record.
- **P3 Handelman LP**: $30.1\%$ slack at $n=4$ against a $1.6$ gate — dead at any open $n$.
- **P4/P5/P6 transference (square/disk/diameter)**: ceilings $3(\sqrt6-\sqrt2)$, $2\sqrt3$,
  $\sqrt{13}$, all exact, all below Oler — dead *permanently*, witness-certified.
- **P9 flat propositional encodings**: $\ge10^8$ clauses forced by granularity arithmetic.
- **P8 / round-2 O**: obsoleted by the record's move from $4$ to $4.4641$.

Every kill above is reproducible in one command each from
[`experiments/packing-n16-approaches/`](../../../../experiments/packing-n16-approaches/)
(`transference.py`, `hexnorm.py`, `handelman.py`, `dodeca.py`; transcripts in `out/`).
