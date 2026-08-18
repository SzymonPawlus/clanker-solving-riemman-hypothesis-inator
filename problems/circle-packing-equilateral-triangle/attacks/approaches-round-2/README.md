# Round-2 attack proposals: after the n = 16 wall

```
status: sketch          — every claim in this file, without exception
author: claude (Fable 5, divergent/generative role per RULES.md §8), 2026-08-18
issue:  #58
```

**Read this first.** This is a *triage of proposals*, not a record of results. Nothing here is
established, nothing here is assumable — including by its author (repo `RULES.md` §3). Every
number quoted as a feasibility estimate was computed by the script in the appendix, whose full
output is pasted there; nothing is hand-counted. No bound, packing, or value of $s(n)$ is
claimed anywhere in this file. Where a statement would, if true, close an open case, it is
flagged as conditional and the condition is stated.

Two status conventions that this file's first version got wrong and now states explicitly
(§3, and problem `RULES.md` §1): the appendix computations are **`numerical` evidence at
best**, and a search that *fails to find* an object is evidence of nothing more than that
this search did not find it — never a proof that the object is absent. Where such a search
drives a decision below (N, and the negative branch of L), the decision is recorded as a
discretionary **kill decision on negative numerical evidence**, not as a `refuted` claim, and
nothing else in this file is allowed to depend on it.

Proposal letters continue the first triage's A–H
([`../candidate-approaches/README.md`](../candidate-approaches/README.md), PR #26): the
proposals here are **I–O**.

## What this round responds to

Raw material, all from 2026-08-18 (each item's real status lives in the linked artifact, not
here):

1. **PR #56 (branch `claude/28-interval-bnb`, open): the B&B hit a diagnosed wall at n = 16.**
   It certified $d(12) > 139/20$ from scratch (95.3 % of the true optimum), but at $n = 16$
   proved only $d(16) > 7.999$ — weaker than the free bound $d(16) \ge d(15) = 8$ (16 points
   contain 15). Its own diagnosis: below side 8 the level-2 dyadic cells have side $< 2$,
   forcing 16 points into 16 cells one apiece, which the pair test kills instantly; at $d = 8$
   that forcing evaporates and the search must distribute 16 points over 64 level-3 cells.
   Fourteen runs timed out at up to $2.2 \times 10^8$ nodes. The wall is *combinatorial*, not
   arithmetic.
2. **PR #53 (merged): the exact partition engine works.** Rational convex partitions in oblique
   coordinates, exact `Fraction` checks of containment, strict convexity, pairwise zero-area
   overlap, exact total-area coverage, exactly $n-1$ cells, squared diameter $< 4$.
   Calibrated on $n = 3,4,5,6,7$. Nobody has yet pushed it hard.
3. **PR #50 (merged): the LS billiard generator** matches published values to 14–16 significant
   digits for 20 of 26 $n$ in 3..34.
4. **PR #21 (open): Oler is slack away from triangular $n$** — by about half a circle at
   16–18 — so nothing closes an open case without going beyond Oler.

Open cases: $n = 16, 17, 18, 19, 22\text{–}34$, and beyond. Primary target throughout:
$n = 16$, best known $d(16) \approx 9.2495$ (`numerical`, quoted from PR #56), rigorous state
of the art exactly $d(16) \ge 8$ (free).

## §6.1 dedup statement

Checked against A–H (PR #26), open issues #2–#57, and the merged experiments. Where a proposal
touches an existing approach, the overlap and the *new* content are stated inside the proposal.
None of I–O re-proposes: interval B&B as designed in #28/PR #56 (dyadic multiset DFS — I repairs
its diagnosed failure with a different search structure), partition certificates as merged
(L and J extend the engine in stated new directions), SDP hierarchies (C), Payan mechanisation
(D/#29), contact-graph enumeration (E/#11), Oler-with-vacancy-correction (F/#44), seeding (G),
or rattler moves (H).

---

## I. Grid-forcing occupancy patterns: restore at any $d$ the forcing the B&B lost at 8

**The idea.** PR #56's subdivision is dyadic: each cell splits into 4, so cell side is
$d/2^\ell$ and the "one point per cell" forcing exists only when some level's cell count is
close to $n$ *and* its cell side is $< 2$ — an accident of $d$ that fails exactly at $d \ge 8$
for $n = 16$. But the uniform $k \times k$ subdivision of an equilateral triangle into $k^2$
congruent side-$d/k$ cells exists for **every** $k$, and its cells have diameter $d/k < 2$
whenever $k > d/2$. For $d \in [8, 10)$ take $k = 5$: 25 closed cells of side $< 2$, so any
16 valid points occupy 16 *distinct* cells (two points in one closed cell would be at distance
$\le \mathrm{diam} < 2$). The search then factors into two phases:

- **Phase 1 — enumerate occupancy patterns**: which 16 of the 25 cells are occupied.
  $\binom{25}{16} = 2{,}042{,}975$ patterns (computed, appendix); quotienting the $D_3$ action
  brings this down to roughly $\binom{25}{16}/6 = 340{,}495$ — a *floor* on the orbit count
  (Burnside adds the symmetric patterns' contribution, so the true count is slightly above it;
  the exact figure is an implementation detail).
- **Phase 2 — refute each pattern** as a 16-variable constraint-satisfaction problem: each
  point is confined to its own known cell; refine cells dyadically *inside* the pattern and
  propagate the exact pairwise maximum-separation test (same exact-integer arithmetic as
  PR #56) only between geometrically near cells, with arc-consistency instead of multiset DFS.

The point: PR #56 branches over *multisets of cells with multiplicities*, so above $d = 8$ it
pays the full distribution explosion at every node. Here the combinatorial choice is made
exactly once (phase 1), and phase 2 is a bounded CSP whose variables never interact except
through local binary constraints. Phase-1 patterns are also independent — embarrassingly
parallel and checkpointable per pattern.

**Delivers.** Certified $d(16) > 8 + \varepsilon$ for the largest affordable $\varepsilon$ —
the first rigorous bound for an open $n$ beyond the free bound, closing part of the enclosure
$8 \le d(16) \le 9.2495$. Status ceiling: `numerical` on landing, `verified:review` after the
other agent reimplements a verifier over the emitted trace (problem `RULES.md` §3 pattern).

**Why not A.** A (issue #28, PR #56) is dyadic multiset B&B; its recorded obstruction is
precisely that its forcing is tied to the dyadic accident. The new content is (i) non-dyadic
root subdivision chosen as $k = \lfloor d/2 \rfloor + 1$ so forcing holds at *every* $d$, and
(ii) the two-phase pattern/CSP structure replacing multiset DFS. The obstruction recorded in
PR #56 does not apply because it is specifically about the disappearance of per-cell forcing
at $d = 8$ under powers of 4.

**Most likely to be wrong.** The per-pattern cost. Root-level pruning between pattern cells is
weak — at $d = 9.24$, side-1.848 cells, even edge-adjacent up/down cell pairs have maximum
separation $1.848\sqrt{3} \approx 3.2 > 2$, so *no* pattern dies at the root (computed
geometry, not tested in code); everything depends on how deep phase 2 must refine, and near
the true optimum it may still blow up pattern-by-pattern.

**Kill-criterion.** Sample 1000 uniformly random patterns at $d = 8.5$, measure the median and
95th-percentile phase-2 node count; if the extrapolated total over all patterns exceeds
$10^9$ nodes, stop and record the measurement. Second kill: if phase 2 at $d = 8.1$ cannot
refute a random pattern sample within $10^4$ nodes each, the CSP propagation is not stronger
than PR #56's pruning and the redesign adds nothing — stop.

**Effort.** Multi-session; reuses PR #56's exact lattice arithmetic (coordination note: that
branch is open — reuse means *after it merges*, or reimplementation, not editing its files).
The kill-criterion measurement alone fits one session. Long runs need the §6.6 human OK.

**Dependencies.** None unresolved. The free bound $d(16) \ge d(15)$ rests on `cited`
$d(15) = 8$ (Oler).

---

## J. Scaling closure: one exact critical partition closes a case *exactly*

**The idea — a theory observation first.** All current lower-bound machinery (PR #53, PR #56,
approach A's enclosure scope) produces $d(n) > d^* - \varepsilon$ and can never reach $d^*$.
But note what scaling does to a partition certificate. Suppose the triangle $T_{d^*}$ at the
**exact algebraic** critical side $d^*$ admits a cover by $n-1$ closed convex cells each of
diameter $\le 2$ — *non-strict*, so cells are allowed to be exactly critical. For every
$\lambda < 1$, scaling by $\lambda$ carries it to a cover of $T_{\lambda d^*}$ by $n-1$ cells
of diameter $\le 2\lambda < 2$, which by pigeonhole excludes $n$ points for every
$d < d^*$. Hence $d(n) \ge d^*$ from **one** finite certificate. Pair it with an exact
feasible $n$-point configuration at $d^*$ (issue #11's contact-graph lifting delivers exactly
this object) and the conclusion is the equality $d(n) = d^*$ — the enclosure *closed*, which
approach A explicitly names as unavailable to it.

Two further simplifications fall out:

- **Coverage without measure theory.** Pigeonhole needs a *cover*, not a partition — overlap
  is harmless. So the Lean-blocking area/shoelace machinery (FINDINGS: Mathlib has essentially
  no polygon geometry) can be avoided entirely: present a witness BSP tree of halfplane cuts
  of $T_{d^*}$ (coverage of a BSP's leaves is inductively free), plus a finite check that each
  leaf's vertices lie in some declared cell. Coverage becomes syntactic. PR #53's exact-area
  accounting is one sound way to prove coverage; this is a strictly more Lean-friendly one.
- **The arithmetic is a fixed quadratic field.** For the pilot case below everything lives in
  $\mathbb{Q}(\sqrt{3})$: numbers $a + b\sqrt{3}$, $a, b \in \mathbb{Q}$, with exact sign
  tests. No interval arithmetic anywhere.

**Pilot: $n = 7$, a case that is already proven — deliberately.** $d(7) = 2 + 2\sqrt{3}$
(`cited`, Melissen 1993). PR #53 reconstructs Graham's six-cell topology with ideal parameters
$\delta = 1/(1+\sqrt{3})$, $r = \delta/\sqrt{3}$ — all in $\mathbb{Q}(\sqrt{3})$ — and its
*rational approximation* certifies to within $10^{-4}$ of the optimum. Step 1 of this attack
is the exact computation nobody has done: do the six ideal cells at exactly $d^* = 2+2\sqrt{3}$
have diameter $\le 2$, verified in $\mathbb{Q}(\sqrt{3})$? If yes, then critical partition +
exact 7-point configuration + the scaling lemma + pigeonhole is a complete, machine-checkable
**optimality proof of $n = 7$** — which would be the repo's first optimality artifact of any
kind, and a realistic `verified:lean` target (PR #19 already did $n = 3, 6$ feasibility in
Lean; this adds finitely many $\mathbb{Q}(\sqrt{3})$ inequalities and one scaling argument).

**Then the gamble: $n = 16$.** The same mechanism closes $n = 16$ **iff a 15-cell
diameter-$\le 2$ cover of $T_{d(16)}$ exists** — i.e. iff pigeonhole is *tight* at 16. That is
unknown (A–H's approach B records "pigeonhole is generally not tight" as its honest catch).
Whether it holds is exactly what proposal L measures. Note pigeonhole *is* tight at $n = 7$
if step 1 succeeds — so tightness at non-trivial, non-triangular $n$ is not fantasy; whether
it survives to 16 is an open empirical question this pair of proposals turns into a
computation.

**Delivers.** Pilot: a Lean-formalisable optimality re-proof of $n = 7$ (ceiling:
`verified:lean`; even the pre-Lean exact artifact is `verified:review`-able by independent
reimplementation). Conditional on tightness at an open $n$: exact closure of that case —
ceiling `verified:lean`, capped by the status of the construction side (issue #11 output) per
§3 propagation.

**Why not B.** B (merged as PR #53) is $\varepsilon$-below-optimum *rational strict* partition
certificates. The new content: (i) the observation that a single non-strict certificate at the
exact algebraic critical value yields $d(n) \ge d^*$ — converting the engine from enclosures
to equalities, a mechanism A's write-up explicitly lists as missing; (ii) cover-not-partition
plus BSP-witnessed coverage, removing the measure-theoretic obstacle FINDINGS records against
Lean; (iii) number-field arithmetic replacing rational approximation.

**Most likely to be wrong.** Step 1 itself: Graham's ideal six-cell configuration might have
some cell diameter *strictly greater* than 2 at exactly $d^*$, with the merged rational
certificate passing only because it sits at $d^* - 10^{-4}$. Then $n = 7$ pigeonhole is not
tight after all, the pilot dies, and the mechanism has no validated instance. (The scaling
lemma itself is elementary — diameter is homogeneous of degree 1 under dilation — and is the
step I judge *least* likely to be wrong; say so and let the reviewer attack it.)

**Kill-criterion.** If the exact $\mathbb{Q}(\sqrt{3})$ computation at $n = 7$ shows max cell
diameter $> 2$ at $d^*$, and one session of searching (L's machinery) finds no alternative
6-cell critical cover, the mechanism has no known instance: record that as a finding and
drop the equality ambition, keeping only the BSP-coverage simplification as a contribution to
the partition engine. For open $n$: dropped for that $n$ once L's search
stalls well below the conjectured $d(n)$ — noting the asymmetry, since L can *certify* only
lower estimates of $m(n)$, so an upper impression of $m(n)$ is `numerical` evidence for a
decision and never a proof that no $(n-1)$-cell cover exists (see L).

**Effort.** Step 1 is under an hour (a dozen exact quadratic-field distance evaluations).
The Lean formalisation is multi-session but bounded and parallelises with everything else.

**Dependencies.** The construction side of any equality needs exact coordinates at $d^*$
(issue #11, in progress, `active-work`); the pilot's $n = 7$ configuration is classical and
can be transcribed and checked directly. Uses `cited` $d(7)$ only as the target to compare
against, not as a proof step.

---

## K. SAT with proof logging: clause learning against the combinatorial wall

**The idea.** The $n = 16$ explosion is a *structured* combinatorial search — exactly the
shape modern CDCL SAT solvers dominate, and exactly what PR #56's DFS lacks: no learning, so
it re-refutes near-identical subproblems $10^8$ times. Encode the occupancy abstraction at a
fixed subdivision level as CNF:

- one Boolean per cell, "some point lies in this cell", over the $k=5$ grid refined $r$ times
  ($25 \cdot 4^r$ cells; cell side $< 2$ makes multiplicities impossible, so points inject
  into occupied cells);
- a cardinality constraint: at least 16 cells occupied;
- a binary clause $\lnot c_i \lor \lnot c_j$ for every cell pair whose **exact maximum
  separation is $< 2$** (the same exact-integer oblique-lattice test as PR #56 — each clause
  is a one-line rational fact);
- optionally, "at most $m$ occupied among $S$" clauses imported from any certified region
  capacity (see M) — the encoding composes.

UNSAT then implies no 16 valid points at that $d$, i.e. $d(16) > d$. The instance sizes are
small (computed, appendix): at $d = 9.24$, refinement $r = 2$ gives 400 cells and roughly
$4 \times 10^4$ binary clauses; $r = 3$ gives 1600 cells and $\sim 5 \times 10^5$ clauses —
trivial for CDCL *as instances*; the open question is search hardness, which is the bet.

**The decisive extra: the proof artifact.** CDCL solvers emit DRAT/LRAT unsatisfiability
proofs, checkable by small, independently implemented — and in Lean 4's case *formally
verified* — checkers (`bv_decide`'s LRAT infrastructure). The verification story is then:
(a) each geometric clause is a one-line exact rational check, reimplementable independently;
(b) the propositional UNSAT is replayed through a verified checker. This is the
Keller-conjecture / Schur-number-5 methodology (Heule et al.) transferred to this container —
a literature check for prior circle-packing-via-SAT work is stage zero of the attack.

**Delivers.** Certified $d(16) > d$ for $d$ beyond the wall, with a two-part certificate whose
combinatorial half is machine-checkable by a *verified* checker. Ceiling: `verified:review`
realistically; plausibly `verified:lean` for the full statement if the geometric clause facts
are also proven in Lean (they are finitely many rational inequalities, PR #19-shaped) and the
LRAT replay is done inside Lean. Granularity governs strength: the abstraction at cell side
$t$ can only prove bounds roughly up to $d(16)$ scaled down by $\approx (1 - t/2 \cdot d/d(16))$
— refine until UNSAT or budget out, and report the granularity/strength trade-off table.

**Why not A.** Same soundness skeleton (occupancy + exact pair tests) but a categorically
different search engine (clause learning = automatic dominance/isomorphism rejection between
subproblems, which the round-2 task names as the missing ingredient) and a categorically
different artifact (replayable proof vs. a trusted trace). Not proposed in A–H; A's write-up
contains no proof-logging or learning mechanism.

**Most likely to be wrong.** The abstraction may be too coarse at affordable granularity: the
only geometric fact the encoding sees is pairwise cell maximum separation, and if that
relaxation stays satisfiable until $r = 4{+}$ ($6400$ cells, clause count in the millions and,
more importantly, a possibly exponentially hard UNSAT instance), CDCL wins nothing over DFS.

**Kill-criterion.** Calibrate on $n = 12$ (known answer, PR #56's own gate): if SAT at
$r \le 3$ cannot certify $d(12) > 7.2$ — beating PR #56's $139/20 = 6.95$ — within one hour of
solver time, the approach does not outperform the incumbent; record the table and stop.
Then the $n = 16$ gate: if $d(16) > 8.05$ is not reachable at $r \le 3$ within budgeted solver
time, stop.

**Effort.** Encoder is 1–2 sessions (the geometry is PR #56's exact test, re-derived
independently); solving runs are the standard §6.6 negotiation. Cheap to try relative to its
upside.

**Dependencies.** None unresolved; free bound as in I. Off-the-shelf solver (kissat/cadical)
and checker — pin versions per problem `RULES.md` §5.

---

## L. Measure the pigeonhole ceiling $m(n)$: topology-moving partition search

**The idea.** Define $m(n) = \sup\{d :$ $T_d$ admits a cover by $n-1$ closed convex cells of
diameter $\le 2\}$. Everything the merged engine can ever certify is $d(n) > m(n) - \varepsilon$;
J's closure works at $n$ iff $m(n) \ge d(n)$. Nobody knows $m(16)$ — not even roughly. Compute
it: search over cell *topologies*, not just vertex positions. Concretely: start from principled
seeds — the Delaunay/Voronoi complexes of the 15-point optimum ($\Delta(5)$ lattice) and of the
best-known 16-point packing (PR #50 coordinates) restricted to $T_d$ — then locally move
vertices to minimise max cell diameter (the merged `search_graham6.py` already does
fixed-topology descent on 2 parameters; this generalises to all vertex coordinates), and move
*between* topologies by edge flips and cell merges/splits when descent stalls. Bisect on $d$:
each $d$ where the optimiser finds a valid cover rationalises (PR #53 pipeline) into a
certificate; the largest certified $d$ is a lower bound on $m(16)$ and a new best rigorous
lower bound for $d(16)$ if it exceeds 8.

**Delivers.** (i) Best-yet certified lower bounds for open $n$ via the *already-merged*
engine (ceiling `verified:review` via the existing two-checker route; `verified:lean`
inherits B's story); (ii) the decision quantity for J at $n = 16$–19: measured
$m(n)$ vs. conjectured $d(n)$; (iii) if the search tops out well below 8 — pigeonhole cannot
even beat the free bound — that is a decisive *negative* result redirecting partition effort
toward M. Note its status: a search that fails to find an $(n-1)$-cell cover does not prove
that none exists, so that branch is `numerical` evidence for a redirection decision, never a
refutation of pigeonhole at 16. Any of the three outcomes is worth having.

**Why not B.** B proposed automating partition search and is merged as a *fixed-topology,
two-parameter* calibration. The new content: topology as a search variable, packing-derived
seed complexes, the explicit target quantity $m(n)$ (upper *and* lower estimates of it), and
the framing as the decision procedure for J. This is the "push the merged engine" direction
the round-2 task names; it is listed here as an extension of B, not as novel framework.

**Most likely to be wrong.** Local search over topologies may be badly non-convex — max-diameter
landscapes have combinatorial ridges, and the search may report a badly pessimistic $m(16)$
estimate, wrongly killing J at 16. (Mitigation: report only "certified lower estimate of
$m$" and "failed-search upper *impression*", never "$m(16) = $".)

**Kill-criterion.** Calibration: the search must rediscover $m \approx d^*$ behaviour on the
known-tight small cases (at minimum $n = 4, 5, 6$, plus $n = 7$ if J's step 1 confirms it)
to within $10^{-3}$ in one session; otherwise the optimiser is not working — fix or stop.
At $n = 16$: two sessions of stalled search below $d = 8$ ⇒ record and hand the baton to M.

**Effort.** 2–4 sessions on top of merged code. Each certificate emitted is checked by the
existing engine, so the marginal soundness burden is zero.

**Dependencies.** None unresolved. Uses PR #50 output as *seeds only* (numerical input to a
search, never to a claim).

---

## M. Capacity-augmented counting: fractional pigeonhole with an exact Farkas certificate

**The idea.** Plain pigeonhole dies when no $(n-1)$-cell diameter cover exists (the B honest
catch; possibly the situation at 16 — L will say). The classical proofs (Melissen's case
analyses) then argue "this *region* holds at most $k$ points". Systematise that: a **capacity
certificate** for a region $R \subseteq T_d$ is a proof that at most $c$ points at pairwise
distance $\ge 2$ fit in $R$. Sources of capacities, in increasing strength: diameter $< 2$
gives $c = 1$ (the merged engine); strip geometry gives analytic $c$ for trapezoids (appendix,
proposal N — weak but free); and a *mini*-B&B or SAT run on a single small region gives sharp
$c$ cheaply, because the region is far smaller than $T_d$ — this recursion is what PR #56's
global search never exploits. Then aggregate: pick regions $R_1, \dots, R_m$ with capacities
$c_j$ and nonnegative rational weights $y_j$ such that $\sum_j y_j \mathbf{1}[x \in R_j] \ge 1$
for every $x \in T_d$ (a finite check on the arrangement's faces, or trivially for a
partition); then $n' \le \sum_j y_j c_j$ for any valid configuration of $n'$ points, and
$\sum_j y_j c_j < 16$ certifies $d(16) > d$. The aggregation is exact rational linear
algebra — a Farkas-style certificate, the most Lean-friendly object in this whole area — and
finding good $(R_j, y_j)$ is an LP over a fixed region library, i.e. *searchable*, the
LP/dual view of "cover by few small cells" the round-2 task asks about.

**Delivers.** Lower bounds strictly beyond the reach of plain pigeonhole (whenever any single
region genuinely holds fewer points than its diameter-1 cell count suggests), with a layered
certificate: per-region capacity proofs + one rational aggregation inequality. Ceiling:
`verified:review`; the aggregation layer and the $c = 1$ capacities are `verified:lean`-shaped
now, the mini-B&B capacities inherit K/I's verification story (§3 caps the whole at the
weakest layer, stated openly).

**Why not B or F.** B is the $c_j \equiv 1$, $y_j \equiv 1$, partition-only special case. F is
an *analytic* corrected Oler inequality (issue #44 adjacent); M is finite, per-$n$, and
computational — no new global inequality is conjectured. Neither A–H item combines
capacities $> 1$ with weighted covering aggregation.

**Most likely to be wrong.** Usefulness, not soundness: capacities of large regions may be
exactly as hard to certify as the original problem (the recursion may not bottom out cheaply
enough), leaving only weak analytic capacities — and every cut set N's search below tried
gives strip capacities far too weak to carry the count alone.

**Kill-criterion.** One session must produce a *single* example beating plain pigeonhole:
some $d$, some region set, with $\sum y_j c_j < n$ where no $(n-1)$-cell diameter cover is
known at that $d$ — validated first on a solved case (suggested: $n = 12$ at $d$ near
$d(12) = 4 + 2\sqrt{3} \approx 7.464$, where PR #56 stalled at 6.95). If no such example
exists after two sessions, the aggregation buys nothing over its ingredients; record and stop.

**Effort.** Medium: region library + LP + capacity mini-searches, all on existing arithmetic.
Runs after L (which tells us *whether* it is needed at 16) but is independent of it.

**Dependencies.** Sharp capacities for medium regions depend on I or K machinery; the analytic
and $c=1$ layers depend on nothing unresolved. From N, M takes only the *per-cut-set* strip
capacity bound — an elementary standalone fact — and explicitly **not** N's `numerical` kill
decision, which is not assumable (§3) and is not used as a premise anywhere.

---

## N. Strip counting — proposed, tried, and dropped in the same hour

**The idea (the designated cheap-to-kill probe).** Slice $T_d$ into horizontal strips of
height $h < 2$. Two points in one strip have $|\Delta y| \le h$, so pairwise distance $\ge 2$
forces $|\Delta x| \ge \sqrt{4 - h^2}$; sorted by $x$, a strip of maximal width $W$ holds at
most $1 + \lfloor W / \sqrt{4 - h^2} \rfloor$ points. If some choice of strip cuts gives total
capacity $\le 15$ at some $d > 8$, that is a one-page lower bound $d(16) > d$ beating the
state of the art, essentially for free.

**Result: dropped, on negative numerical evidence.** The appendix script searches strip cuts
(uniform grids plus 20 000 random cut sets per $d$) and reports the smallest total it *found*:
**19 at $d = 8.0$**, 20 at 8.2, 21 at 8.5, 24 at 9.24 — nowhere near the required 15, while
$d(16) \ge 8$ is already free.

**Read those numbers correctly.** Each is a best-*found* value, hence an **upper estimate of
the minimum capacity sum over cut sets** — not the best achievable one. A randomised search
that failed to find a cut set with total $\le 15$ does **not** establish that no strip
partition achieves it, and this file does not assert that. The possibility that some cut set
outside the searched family — a finer or unevenly spaced set of horizontal cuts, or a
non-horizontal or non-parallel slicing — reaches 15 is left explicitly open.

What I have instead is a mechanism and a margin, and together they are a **kill decision**,
not a refutation: the 1-D projection discards too much (it cannot see that three mutually-far
points in a wide strip also constrain each other in $y$), and the shortfall at $d = 8$ is four
points, far outside what a luckier cut set plausibly recovers. So: **do not pursue standalone
strip counting** — unless someone exhibits a cut set with capacity sum $\le 15$, which would
overturn this decision immediately and is a welcome contribution. Salvage: the per-cut-set
strip capacity bound remains valid (if weak) as an entry in M's region library, and the
numbers above are the honest baseline any M capacity must beat.

**Status.** `numerical`, and it stays there: the evidence is a randomised search, so nothing
in N is `refuted` and nothing in N is assumable (§3). Separately verifiable *would* be the
per-strip capacity bound $1 + \lfloor W/\sqrt{4-h^2}\rfloor$ for a **fixed** cut set — that
argument is elementary, ceiling `verified:review` or plausibly `verified:lean` — but it is a
statement about one cut set, not about the minimum over all of them, and it is what M may
reuse. The minimum over cut sets is not claimed at any status.

**Why not A–H.** Not previously proposed; tried and set aside here, with the measurement
recorded, so the question does not recur uninformed (§6.1).

**Kill-criterion.** Stated and met at proposal time: "no cut set found within the search
budget comes near 15." That is exactly what fired — a decision criterion about the search,
not a mathematical impossibility statement. Effort spent: well under one hour.

**Dependencies.** None, and nothing else in this file depends on N's kill decision; M's use of
strip capacities is per-cut-set and independent of it.

---

## O. Quantitative Oler stability at $n = \Delta(k) + 1$ — a theory probe

**The idea.** $16 = \Delta(5) + 1$. Any 16-point configuration in $T_d$ contains 15 points in
$T_d$, and for $d$ near 8, $d(15) = 8$ says the 15-subset is *extremal or near-extremal* for
Oler. A quantitative **stability** version of Oler's theorem — "if $\Delta(k)$ points at
pairwise distance $\ge 2$ fit in side $2(k-1) + \varepsilon$, then the configuration is within
$\delta(\varepsilon)$ of the triangular lattice" — would force every 15-subset to be
near-lattice, and the 16th point to sit in a near-lattice hole. The deepest hole of the exact
$\Delta(5)$ lattice has fit radius $2/\sqrt{3} \approx 1.155 < 2$ (circumradius of a spacing-2
lattice triangle; boundary corrections belong to the attack), so for small $\varepsilon$ no
16th point fits: $d(16) \ge 8 + \varepsilon_0$ for whatever $\varepsilon_0$ the stability
constants deliver. Stability theorems of this type exist for hexagonal packing in the plane
(e.g. the Fejes-Tóth-tradition literature; a real citation sweep is stage zero — none is
claimed here); whether one exists or is provable for Oler's inequality is open to my
knowledge, and issue #44 (Oler equality characterisation) is its natural companion: a
stability theorem is precisely a robust equality characterisation.

**The computed scaling check (appendix), and which way it points.** Dilate the exact
$\Delta(5)$ lattice-with-hole picture from $d = 8$ upward. Hole fit radius is homogeneous of
degree 1, so it grows as $(d/8) \cdot 2/\sqrt{3}$ and first reaches 2 — the value at which a
16th point would fit into the *scaled* hole — at $d = 8\sqrt{3} \approx 13.856$. Since
$13.856 > 9.2495$, the simple hole obstruction **persists throughout the conjectured range**:
at $d = 9.2495$ the scaled hole radius is still only $\approx 1.335$, well short of 2. The
check therefore says the obstruction does not self-destruct before the conjectured optimum —
it is neutral-to-favourable for O, not a negative prior. (The first version of this file read
this backwards, concluding that "the perturbative regime ends far below the truth"; that was a
direction error and it is retracted here.)

Equally, it licenses nothing: pure dilation is a one-parameter family, and at $d > 8$ the 15
points have slack and may *rearrange* rather than dilate. The scaling figure bounds nothing
about that.

**The real limitation** is the one this proposal's failure analysis already identifies below:
the unknown *quantitative* stability control — how large $\varepsilon$ may be before
"$\Delta(5)$ points fit in side $8 + \varepsilon$" stops forcing near-lattice structure, and
how weak $\delta(\varepsilon)$ is when it does. That constant, not the $8\sqrt{3}$ figure, is
what decides whether any usable $\varepsilon_0$ survives; it is unknown to me, plausibly very
weak, and possibly nonexistent without extra hypotheses. Against that, the rigorous state of
the art is exactly $d(16) \ge 8$, so *any* $\varepsilon_0 > 0$ — even 0.05 — would be the best
lower bound the repo has, by a theory route independent of all search machinery, and would
compose with I/K (which need a foothold above the $d = 8$ cliff, exactly where their search is
hardest).

**Delivers.** A conjectured stability lemma with an attempted proof for $k = 5$ (ceiling:
`sketch` until cross-examined; `verified:review` realistic for a careful finite-case argument;
`cited` if the literature sweep finds it already exists, which would be the best outcome).

**Why not F.** F corrects Oler *downward* for vacancies at $n$ *below* triangular
($\Delta(k) - 1$); O sharpens Oler's *equality case* into a robust statement to attack $n$
*above* triangular. Different inequality, different open cases, different mechanism. Overlap
with #44 is complementary (literature on the equality case feeds both) and #44 is
`ready`/unassigned — coordinate, do not duplicate its reading list.

**Most likely to be wrong.** The stability constant: a first-order rigidity analysis may give
$\delta(\varepsilon)$ so weak that the surviving $\varepsilon_0$ is indistinguishable from 0,
and the lemma might simply be false without convexity/jamming hypotheses (rattler freedom in
the 15-point optimum is exactly a zero-stiffness direction — the $\Delta(5)$ optimum's
uniqueness properties need checking against the literature first, not assuming).

**Kill-criterion.** One session of literature (with #44) plus one session of honest
estimation: if no route to $\varepsilon_0 \ge 0.05$ is visible after both — in particular if
the 15-point optimum at side $8 + \varepsilon$ admits configurations far from the lattice for
tiny $\varepsilon$ (checkable numerically with PR #50's generator as *evidence*) — record and
stop. Explicitly forbidden per §6.3: re-scoping to "stability is philosophically interesting"
after the numbers fail.

**Effort.** Two sessions to the kill decision; open-ended only if it survives, at which point
it goes to the convergent model for an attempted proof (§8).

**Dependencies.** Uniqueness/structure of the $\Delta(5)$ optimum: status unknown to me —
must be resolved from literature before any proof attempt (flagged, not assumed).

---

## Ranking and recommendation

1. **I — grid-forcing occupancy patterns.** Directly attacks the one diagnosed wall; cheap
   first measurement (its kill-criterion is a one-session experiment); reuses PR #56's exact
   arithmetic; every increment is a publishable bound. The round-2 brief is right that
   breaking this specific explosion is worth more than a new framework — this is the smallest
   change that could do it.
2. **J — scaling closure.** The $n = 7$ pilot is under an hour to its go/no-go computation,
   its success would hand the repo its **first optimality artifact** (and a credible first
   Lean-verified optimality proof anywhere in this problem), and the mechanism is the only
   route on the board to *closing* an enclosure rather than narrowing it. Ranked below I only
   because its open-case payoff is conditional on tightness, which is not ours to choose.
3. **K — SAT with proof logging.** Highest ceiling among the search routes (verified-checker
   artifact, clause learning where DFS drowns); slightly more machinery than I, and its
   calibration gate ($n = 12$, beat 6.95 → 7.2) is decisive within a session or two. If I's
   kill-criterion fires, K is the fallback with a fundamentally different search engine on the
   same sound skeleton.
4. **L — pigeonhole ceiling $m(n)$.** Should run early regardless: it decides J-at-16, it can
   only produce certified bounds or a decisive negative, and it is the cheapest use of the
   already-merged engine. Ranked fourth only because it is an extension of B rather than new
   ground.
5. **M — capacity aggregation.** The right successor *when* plain pigeonhole tops out; its
   one-session existence gate (beat pigeonhole once, anywhere) keeps it honest. Do after L
   reports.
6. **O — Oler stability.** Keep alive to its two-session kill decision because it is the only
   *theory* route to a foothold above $d = 8$ and it feeds #44. Its computed scaling check is
   neutral-to-favourable rather than the negative prior the first version of this file called
   it, so O is no longer ranked down *for that reason*; it stays sixth because its deciding
   unknown — the quantitative stability constant — is not measurable in a session, whereas
   I/K/L/M all have gates that resolve in one or two. Expected outcome: still killed by the
   constants, and that write-up teaches us what the equality case needs.
7. **N — strip counting.** Tried above and dropped on negative numerical evidence — a kill
   *decision*, not a refutation, and not assumable. Zero further effort planned; its residue
   lives inside M, and the door stays open to anyone who exhibits a cut set with capacity sum
   $\le 15$.

**Would not pursue:** N (dropped above on `numerical` evidence — a decision, not a proof of
impossibility); O beyond its stated two-session gate; and the two ideas
generated and rejected during this round — *reflection unfolding* (lift $T_d$ to the plane via
the reflection group and apply plane-packing density bounds: the mirror copies near walls
violate the packing constraint, and repairing that boundary effect *is* Oler's proof — it
collapses into F/#44 territory) and *Delsarte-style LP potentials on the triangle* (no
symmetry to diagonalise against; the systematic version is exactly C, already triaged).

**Recommended issues (dispatcher's call, not filed here per the round-2 brief):** one for
**I + K** as a single "break the wall" issue with two engines and a shared calibration gate,
and one for **J's $n = 7$ pilot** (go/no-go computation plus, on go, the Lean plan). L can
ride as a scoped extension inside the partition-certificates line rather than a fresh issue.

---

## Appendix: feasibility script and full output

Everything numeric quoted above comes from this script (Python 3, stdlib only; deterministic
seed for the strip search). It is a *feasibility estimator*, not a checker: floats are fine
here because nothing below is a claim.

```python
from math import comb, sqrt, floor, ceil, pi

print("== I: occupancy patterns for k=5 grid, n=16 ==")
print("C(25,16) =", comb(25, 16))
print("C(25,16)/|D3| floor =", comb(25, 16) // 6)

print("== K: SAT abstraction sizes ==")
d = 9.24
for r in [1, 2, 3]:
    ncell = 25 * 4**r
    side = d / (5 * 2**r)
    cell_area = (sqrt(3) / 4) * side * side
    neigh = pi * (2 + side) ** 2 / cell_area
    print(f"r={r}: cells={ncell}, side={side:.3f}, "
          f"est binary clauses ~ {ncell*neigh/2:,.0f}")

print("== N: strip counting, best capacity sums ==")
def caps(d, cuts):
    ys = [0.0] + list(cuts) + [d * sqrt(3) / 2]
    tot, parts = 0, []
    for y0, y1 in zip(ys, ys[1:]):
        h = y1 - y0
        if h >= 2:
            return None
        w = d - 2 * y0 / sqrt(3)          # widest x-extent of the strip
        c = 1 + floor(w / sqrt(4 - h * h) + 1e-12)
        parts.append(c); tot += c
    return tot, parts

import random
random.seed(0)
for dd in [8.0, 8.2, 8.5, 9.0, 9.24]:
    H = dd * sqrt(3) / 2
    best = None
    for m in range(int(ceil(H / 2)), 9):
        r = caps(dd, [H * i / m for i in range(1, m)])
        if r and (best is None or r[0] < best[0]):
            best = r
    for _ in range(20000):
        m = random.randint(int(ceil(H / 2)), 8)
        r = caps(dd, sorted(random.uniform(0, H) for _ in range(m - 1)))
        if r and (best is None or r[0] < best[0]):
            best = r
    print(f"d={dd}: best strip-cap sum = {best[0]} parts={best[1]}  (need <= 15)")

print("== O: pure-scaling hole depth ==")
print("lattice hole radius at d=8: 2/sqrt(3) =", 2 / sqrt(3))
print("scaling reaches radius 2 at d = 8*sqrt(3) =", 8 * sqrt(3))
```

Output (run 2026-08-18):

```
== I: occupancy patterns for k=5 grid, n=16 ==
C(25,16) = 2042975
C(25,16)/|D3| floor = 340495
== K: SAT abstraction sizes ==
r=1: cells=100, side=0.924, est binary clauses ~ 3,633
r=2: cells=400, side=0.462, est binary clauses ~ 41,207
r=3: cells=1600, side=0.231, est binary clauses ~ 541,395
== N: strip counting, best capacity sums ==
d=8.0: best strip-cap sum = 19 parts=[5, 6, 4, 3, 1]  (need <= 15)
d=8.2: best strip-cap sum = 20 parts=[6, 5, 4, 3, 2]  (need <= 15)
d=8.5: best strip-cap sum = 21 parts=[6, 5, 4, 3, 2, 1]  (need <= 15)
d=9.0: best strip-cap sum = 21 parts=[6, 5, 4, 3, 2, 1]  (need <= 15)
d=9.24: best strip-cap sum = 24 parts=[6, 5, 5, 4, 2, 2]  (need <= 15)
== O: pure-scaling hole depth ==
lattice hole radius at d=8: 2/sqrt(3) = 1.1547005383792517
scaling reaches radius 2 at d = 8*sqrt(3) = 13.856406460551018
```

(An earlier exploratory variant of this script — different RNG stream order, same seed —
found 24 rather than 21 at $d = 9.0$; the strip search is randomised and these are best-found
values, i.e. *upper* estimates of the true minimum capacity sum. Either number is far above
the 15 the attack needed, so N's kill *decision* does not depend on the run — but no run here
is evidence that no cut set reaches 15, only that this search did not find one.)
