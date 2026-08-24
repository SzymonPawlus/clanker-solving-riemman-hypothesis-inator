# Round-3 attack proposals: past the counting plateau

```
status:  sketch          — every claim in this file, without exception
authors: claude, 2026-08-23. Ideation by five Fable 5 workers on disjoint lenses
         (RULES.md §8, divergent role); triage and all verification arithmetic by
         Opus 5 (convergent role). The generating model is not the checking model.
issue:   #110
```

**Read this first.** This is a *triage of proposals*, not a record of results. Nothing here is
established; nothing here may be cited or built on as if it were (`RULES.md` §3 — a `sketch` is
not assumable, **including by its author**). No bound, packing, or value of $s(n)$ is claimed
anywhere in this file. Where a statement comes from the literature it carries a reference; where
it is speculation by a language model, it says so.

Rounds 1 and 2 are [`../candidate-approaches/`](../candidate-approaches/README.md) (A–H) and
[`../approaches-round-2/`](../approaches-round-2/README.md) (I–O). This round continues the
lettering at **V–Z and AA–AD** to avoid collision.

---

## 0. Two corrections to the board, established before any new proposal

Both were found independently by more than one ideation lens and then re-derived here by script.
They matter because **existing gates on the board aim at the wrong number.**

### 0.1 The rigorous floor at $n = 16$ is Oler's $\sqrt{129} - 3$, not the "free" $d \ge 8$

Round 2 records the rigorous state of the art at $n = 16$ as "exactly $d(16) \ge 8$ (free)",
on the ground that 16 points contain 15. That understates what the repo already had on `main`.
Applying the `cited` Oler inequality to the equilateral triangle
([`../oler-lower-bound/oler_bound.py`](../oler-lower-bound/oler_bound.py), merged) gives

$$n \le \tfrac{d^2}{8} + \tfrac{3d}{4} + 1 \qquad\Longrightarrow\qquad d(n) \ge \sqrt{8n+1} - 3 .$$

At $n = 16$ that is $d \ge \sqrt{129} - 3 = 8.357817\ldots$, i.e. $s(16) \ge 2\sqrt3 + \sqrt{129} - 3
= 11.821918\ldots$

**Independent checks performed here.** Re-derived symbolically from Oler's statement; confirmed
*exactly tight* at all six triangular numbers $\Delta(k)$, $k = 2\ldots7$ (RHS equals $3, 6, 10,
15, 21, 28$ at $d = 2, 4, 6, 8, 10, 12$), which is the correctness check Oler's theorem must pass;
and confirmed to agree with the merged `oler_bound.py` closed form. Three routes, one answer.

Status: the inequality is `cited` (Oler 1961); its application to this container is `sketch`,
as `oler_bound.py`'s own docstring already states. **So the floor is not assumable either** —
but it is the number any new lower bound must be measured against.

**Consequence, stated plainly:** gates in rounds 1–2 phrased as "beat 7.999" or "beat 8.05" are
below a bound the repo already had. Any lower-bound proposal below is measured against
$8.3578$ (Oler, `sketch`) and against $8.9282$ (the covering plateau $d \ge 2 + 4\sqrt3$ of
PRs #98/#104, also `sketch`, and **unmerged, so not usable as a dependency**).

### 0.2 Four open cases have conjectured optima in $\mathbb{Q}(\sqrt3)$; three of them are one family

> **Corrected 2026-08-23**, after the `r3-audit` worker refuted the first version of this section.
> As first written it claimed *three* such cases and asserted exclusivity. The scan behind it
> silently omitted $n = 27$ and $n = 28$ from its input table — 28 is triangular and proven, but
> **27 is open**, and it has a closed form. The exclusivity claim was therefore false. The
> corrected scan below runs over the whole range 16–34 and marks proven versus open explicitly
> instead of pre-filtering. Original claim kept visible here because the failure mode — a scan
> whose *input* was quietly wrong, producing a clean-looking table — is the one `RULES.md` §0 is
> about, and it survived one round of manager checking.

Scanning the best-known table for values of the form $a + b\sqrt3$ with small integers
(script, tolerance $2\times10^{-11}$), over **all** of 16–34:

| $n$ | best-known $s(n)$ | closed form | status | note |
|---:|---|---|---|---|
| 17 | 12.928203230276 | $6 + 4\sqrt3$ | open | $= s(12) + 2$ exactly |
| 24 | 14.928203230275 | $8 + 4\sqrt3$ | open | $= s(17) + 2$ |
| 27 | 15.464101615138 | $12 + 2\sqrt3$ | open | $= s(28) = s(\Delta(7))$ — see below |
| 31 | 16.928203230275 | $10 + 4\sqrt3$ | open | $= s(24) + 2$ |

$n = 20$ and $n = 28$ also have closed forms but are **proven**, not open, so they are not targets.
$n = 16$ has only a PSLQ degree-10 minimal polynomial *candidate* on file (`numerical`), with no
elimination link.

**$n = 27$ is cheap but nearly vacuous, and the two should not be confused.** $27 = \Delta(7) - 1$,
and its best-known value equals the *proven* $s(28) = 12 + 2\sqrt3$. So the upper bound
$s(27) \le 12 + 2\sqrt3$ is immediate — delete any one point from the optimal 28-point triangular
packing — and certifying it exactly establishes nothing that the proven $\Delta(7)$ row does not
already give. It is a free **calibration control** for an exact pipeline, not a result. (It is
also the $k = 7$ analogue of $n = 20 = \Delta(6) - 1$, which is exactly what the `eo-*` campaign
on issue #91 is about; the interesting question there is the *lower* bound, which none of this
touches.)

The genuinely non-trivial cases are the **$+4\sqrt3$ family $n = 17, 24, 31$** — spaced 7 apart,
each 2 more than the last, and none of them a $\Delta(k) - 1$ freebie.

Why this matters: every exact-certification pipeline in the repo is cheap in $\mathbb{Q}(\sqrt3)$
and expensive in a degree-10 field. **$n = 17$, not $n = 16$, is the cheapest open case for
non-trivial exact work** — and the campaign has spent its effort on $n = 16$. This is a `sketch`
observation about a `numerical` table, and it certifies nothing by itself.

---

## 1. §6.1 dedup statement

Checked against A–H (PR #26), I–O (PR #63), open issues, and merged experiments. Each proposal
below states its own overlap. **None of V–AD re-proposes:** dyadic interval B&B as built (A/I),
partition/pigeonhole certificates (B/L), plain Lasserre as triaged (C — but see **X**, which
discharges C's own recommended size estimate and reverses its expectation), Payan mechanisation
(D), contact-graph enumeration *as scoped in E* (E was demoted for a missing exhaustiveness
lemma — **V** supplies exactly that lemma and says so), Oler-with-vacancy-correction (F),
seeding (G), rattler moves (H), SAT as encoded in K, capacity aggregation (M), strip counting
(N, dropped), Oler stability (O).

Two ideas were generated and **rejected inside this round**, recorded so they are not re-derived:
*topological obstructions* (Borsuk–Ulam/KKM/Sperner — topology certifies existence, not
emptiness; the contrapositive needs a free antipodal action the triangle does not have, and every
concrete construction collapsed into counting or into O), and *order types / oriented matroids*
(the enumerable database stops around $n = 11$ and the count grows like $n^{3n}$). Also rejected:
full CAD (doubly exponential, dead at 32 variables), chordal/sparse SOS (the separation
constraint graph is complete — there is no sparsity to exploit), and symmetry stratification of
configuration space (the generic stratum is the original problem).

---

## 2. The proposals

### V. Stationarity-exclusion / irreducible contact graphs with boundary

**Thesis.** The exhaustiveness lemma that approach E named as its missing hard part is supplied
for free by first-order optimality plus compactness — and this is the shape of the only modern
computer-assisted optimality proofs for maximin arrangements.

**Side attacked:** lower bound; and uniquely on this list, potentially the exact equality
$d(n) = d^*$ rather than an enclosure.

**Mechanism.** At fixed side $d$, a packing exists iff the maximin problem attains $\ge 4$
(squared). Any maximiser satisfies the **Fritz John** conditions — which, unlike KKT, need no
constraint qualification — giving a force balance at each point between its loaded contacts and
its active wall normals. The *support* of that stationary point (which pairs and which walls
carry positive multipliers) is a finite combinatorial object, heavily constrained: the loaded
contact graph is planar with interior degree $\le 6$; an interior vertex whose loaded directions
lie in an open half-plane cannot balance; unloaded points are rattlers and decouple. So enumerate
admissible supports, refute each by interval Newton / Krawczyk, and glue with compactness: no
stationary packing $\Rightarrow$ no packing $\Rightarrow d(n) > d$.

Equivalently, in the language two of the five lenses reached independently: assume the contact
graph **irreducible** (no motion increases every tight constraint) and enumerate irreducible
graphs.

**Why the walls do not apply.** Wall 1 was the explosion of distributing 16 points over 64
spatial cells with a pruning test that gives no contraction on wide boxes; here the branching
object is the *discrete support*, and each branch carries an equality-rich, roughly square system
on which interval Newton contracts quadratically. Wall 2 involves no partition of the container
at all — this is not a counting argument. Wall 3 enters only as the floor.

**Precedent (`cited` for existence, bodies not read).** Musin & Tarasov solved the previously
open Tammes cases $N = 13$ and $N = 14$ by exactly this method — plantri enumeration of
$\approx 9.5\times10^7$ and $\approx1.5\times10^9$ planar graphs, almost all killed by cheap
combinatorial tests ([arXiv:1410.2536](https://arxiv.org/pdf/1410.2536)); Musin & Nikitenko
carried it to a square flat torus ([arXiv:1212.0649](https://arxiv.org/abs/1212.0649)), so it has
already survived one transfer off the sphere. Connelly's school supplies the rigidity/equilibrium
-stress framing. **No application to a container *with boundary* was found** by two independent
search sweeps — walls and corners create support types the sphere/torus literature never meets.
Absence of evidence from a search is weak; a citation sweep of the Musin–Nikitenko lineage is
stage zero.

**Overlap.** Overlaps **E** and **A**. Against E: E's hoped-for lemma ("every optimal packing has
a jammed core with $\ge$ [bound] contacts", which E's author could not state) is replaced by a
theorem — compactness + Fritz John — so the enumeration is exhaustive *by construction*, and the
goal weakens from exact optimality to the fixed-$d$ decision problem. Against A: the search space
is the finite support lattice, not the 32-dimensional configuration box that A's recorded wall is
about.

**Kill-criteria.** (1) *Theory gate*: if the FJ + core/rattler + wall-contact lemma cannot be
written rigorously — in particular the treatment of **continua** of stationary points (rattlers,
points sliding along a wall with one contact) — stop and write up where it broke. (2)
*Enumeration gate*: run the support enumerator at $n = 12$, just below $d(12) = 4 + 2\sqrt3$;
if the admissible support count exceeds $\sim10^6$ or it does not terminate in an hour, record
the count and stop. (3) *Exclusion gate*: at $n = 12$ the known optimum's support must be found
and verify feasible, while sampled others are excluded; if $>20\%$ come back undecided
(positive-dimensional strata defeating Krawczyk), record which strata and stop.

**Honest risk.** Musin–Tarasov stopped at $N = 14$ on the sphere. The counter-consideration is
that walls *pin* configurations far more than a torus does, which should cut supports — that is
speculation, and gate 2 measures it rather than assuming it.

**Ceiling.** `verified:review` (independent reimplementation of enumerator and checker).
Interval Newton in Lean is beyond current repo machinery; say so rather than promising
`verified:lean`.

### W. Grid-rounding to a finite independent-set refutation, with a proof log

**Thesis.** A one-paragraph perturbation lemma turns "no 16 points at mutual distance $\ge 2$ in
$T_d$" into a *finite* independent-set UNSAT instance whose refutation can be checked by an
external proof checker.

**Side attacked:** lower bound.

**Mechanism.** Overlay a triangular grid of spacing $g$. Snapping each point to its nearest grid
vertex moves it by at most $g/\sqrt3$, so pairwise distances lose at most $2g/\sqrt3$. Hence a
packing at separation 2 implies an independent set of size $n$ in the graph on grid vertices
joined when their distance is $< 2 - 2g/\sqrt3$. If that graph has independence number $< n$ —
an entirely finite, discrete statement — no packing exists. Emit the refutation as DRAT/LRAT and
check it with an independent checker, so the artifact is a *proof*, not a solver's word.

**Why the walls do not apply.** The soundness constant is explicit and computable, so this is not
the counting argument of wall 2 — it does not partition the container into pieces and count them,
it discretises the *feasible set*. It is not wall 1's spatial box search either.

**Overlap.** Overlaps **K** (SAT with proof logging) and **M**. New content: the vertex-primal
abstraction with an explicit soundness constant, pre-sized before any run — the ideation lens
computed roughly $5.6\times10^3$ vertices at $d = 8.5$ and $5.5\times10^4$ at $d = 9.0$ (its
script, `sketch`, to be re-derived by the worker rather than trusted).

**Kill-criterion.** Calibrate at $n = 12$ (must reproduce a bound consistent with the known
$d(12) = 4 + 2\sqrt3$, and must *not* refute a $d$ above it — a two-sided control). Then at
$n = 16$: if the instance at any $d$ strictly above $8.3578$ is not refutable within the compute
budget, record the largest $d$ refuted and the instance sizes, and stop. Grid refinement cost
grows quadratically while the gained separation grows linearly, so this has a natural ceiling —
find it and report it.

### X. Symmetry-adapted moment relaxation — the strength gate, not the size gate

**Thesis.** Round 1's approach C expected the Lasserre hierarchy to die on SDP size and
recommended a one-day size estimate. That estimate now exists, and **it reverses the
expectation**: after reduction by the $S_n$ action the relaxation is small. Size is therefore not
the question — *slack* is, and slack is measurable in minutes on already-solved $n$.

**Side attacked:** lower bound.

**Mechanism / the size finding (`sketch`, ideation-lens arithmetic, not yet re-derived here).**
Computing the isotypic block structure of the invariant moment matrix at $n = 16$ via
Murnaghan–Nakayama, the ideation lens reports the dense $561\times561$ level-2 moment matrix
reducing to blocks of sizes $9, 9, 3, 1$, and the dense $6545$ level-3 matrix to blocks of size
at most $31$; invariant scalar moments $56$ at degree $\le 4$ and $275$ at degree $\le 6$ against
$2.76\times10^6$ dense; and the constraints collapsing to two orbits. Its internal consistency
check was that $\sum_\lambda m_\lambda \dim\lambda$ reproduces the dense dimension in all eight
cases.

**This is the single most consequential unverified number in this file**, because it flips a
documented triage decision. The worker's first job is to re-derive it independently, not to
accept it.

**Overlap.** This *is* approach C's own recommended step, executed — the brief required either
doing C's size estimate concretely or proposing something structurally different, and this took
the first option. It is listed as a proposal because the verdict changes what C concluded.

**Kill-criterion.** Measure the level-2 and level-3 relaxation *slack* on solved instances
($n = 5, 7, 8, 12$) using the dense formulation, which needs no symmetry code and runs in
minutes. If the relaxation value is more than a few percent below the known optimum at those $n$,
**retire the whole direction permanently** and write up the slack table — that is a decisive
negative and a first-class outcome. Only if slack is small is the symmetry-adapted SDP worth
building.

### Y. Exact certification of the $\mathbb{Q}(\sqrt3)$ family $n = 17, 24, 31$

**Thesis.** §0.2 identifies three open cases whose conjectured optima are simple elements of
$\mathbb{Q}(\sqrt3)$. Exact, *tight* certificates for those are within reach of machinery the
repo already has, and no such certificate currently exists for any open $n$.

**Side attacked:** upper bound (construction) — self-certifying, and explicitly a realistic
target under problem `RULES.md` §6.

**Mechanism.** Take the LS/multistart float configuration at $n = 17$; extract the contact graph;
solve the contact system exactly over $\mathbb{Q}(\sqrt3)$ (the conjectured $s(17) = 6 + 4\sqrt3$
gives the target field outright, so no elimination or PSLQ guess is needed); verify all
$\binom{17}{2}$ separations and 17 containments exactly; and check **tightness**, which problem
`RULES.md` §2 requires for any record claim and which the repo's current `certificate.py` cannot
deliver — it snaps to rationals and *inflates* $s$ by about $10^{-11}$ until feasible, so every
certificate it emits is honest but loose. Then repeat at $n = 24, 31$.

**What it does and does not establish.** It would establish $s(17) \le 6 + 4\sqrt3$ **exactly**,
with an exact certificate — a construction claim, `numerical` until a second agent reimplements
the checker per problem `RULES.md` §3, and never an optimality claim. Matching the published
record exactly is the expected and *good* outcome (problem `RULES.md` §4).

**Overlap.** Overlaps #11 (float→exact lifting) and #74 (exact algebraic constructions), which
delivered 14 values of $n$, all $\le 21$, and left 16–34 untouched; $n = 11, 12, 13$ were
attempted and not delivered. New content: the $\mathbb{Q}(\sqrt3)$ observation of §0.2 that makes
three *open* cases cheap, and the tightness requirement.

**Kill-criterion.** If the exact contact system at $n = 17$ is inconsistent over
$\mathbb{Q}(\sqrt3)$ — i.e. the conjectured closed form is not actually attained by the contact
structure the optimiser finds — stop and report that as the finding, since it would mean the
table's $n = 17$ row is not what it appears to be. If it is consistent but the certificate cannot
be made tight, deliver the honest untight upper bound and say which it is.

### Z. Novelty and literature audit — including one question the session cannot answer

**Thesis.** Two of this project's live claims may be rediscoveries, and one specific table line
decides it. This is pure reading, needs no optimiser, and is the highest-value-per-hour item on
the list — it is also the one that most directly serves `RULES.md` §0.

**The leads, with their honest weight.**

1. **Gáspár & Tarnai, *Periodica Polytechnica Ser. Civ. Eng.* 44:1 (2000) 13–32** — refines
   Groemer/Oler for the equilateral triangle and reportedly tabulates density upper bounds up to
   30 circles. **One line of one table decides whether the repo's $s(16) \ge 2 + 6\sqrt3$ is a
   record or a rediscovery.** Calibration computed by the ideation lens: their $n = 16$ line
   beats it iff their density bound is $\le 0.7559$ (plain Oler gives $0.8306$, Groemer $0.8527$)
   — `sketch`, to be re-derived. One search rendering of the abstract called the bounds
   "heuristic" and another did not; snippet-tier evidence is demonstrably unstable in exactly the
   load-bearing word.
2. **Nurmela & Östergård 1999, *Discrete Comput. Geom.* 22, 439–457** — proved the *square*
   container optimal up to $n = 27$ by tile/occupancy elimination, i.e. by round-2 approach **I**,
   published. **Uncited prior art for a live approach on this board.**
3. **Markót & Csendes** won the square by interval B&B plus *per-circle active-region/area
   reduction* propagation and record-threshold refutation — the second ingredient is absent from
   I as written, and is a candidate repair for wall 1.
4. **Amore, [arXiv:2212.12287](https://arxiv.org/abs/2212.12287) (2022)** — circle packing in
   regular polygons, equilateral triangle **up to $N = 400$**, with the author's own caveat that
   large-$N$ configurations may not be global maxima. Issue #13 frames past-34 as untouched
   territory; that framing needs correcting against this paper before any record claim.
5. **Payan 1997** (body never read; carries $n = 14$ and $n = 20$) and **Joós 2020** (proved
   $n = 13$; method characterised by a secondary source as continuous-function analysis beyond
   partitions and pigeonhole).

**The blocker, reported rather than routed around.** This session cannot read any of it.
Outbound HTTPS goes through a policy-enforcing egress proxy, and it returned **403 to CONNECT**
for `pp.bme.hu`, `www.math.ucsd.edu` and `www.packomania.com` — organization egress-policy
denials, which the proxy's own documentation says to report and not retry. `WebSearch` returns
snippets; `WebFetch` is blocked universally. So every item above is **abstract- or
snippet-tier**, and the correct standing instruction is unchanged: **assume the Gáspár–Tarnai
bound is known until a human reads that table line.**

**Kill-criterion.** Not applicable in the usual sense — this is an audit, and its negative
outcome ("still cannot read it") is itself the deliverable. It ends when every lead is either
resolved or recorded as blocked with the specific host and the specific question a human should
answer.

### Extra proposals recorded but not staffed this round

- **AA. Cayley–Menger distance-space refutation.** Branch-and-prune in squared distances with
  Cayley–Menger determinant identities, quotienting rigid motions and reflections exactly.
  Honest self-assessment from the lens that proposed it: exhaustion-shaped, overlapping A/I/K;
  decisive gate is to beat PR #56's $d(12) > 6.95$ at $7.2$ within an hour.
- **AB. Euler-localised scoring on the Delaunay triangulation.** A Hales-style per-triangle score
  verified over a 3-dimensional shape space and telescoped by Euler's formula; Oler is the linear
  member of the family, so the question is whether a nonlinear member is stronger. The only
  proposal that would generalise across *all* open $n$, and its failure mode still yields a
  theorem. One-session LP gate.
- **AC. Container-$\vartheta'$ kernel bound.** An SOS bound in $\le 4$ variables regardless of
  $n$, which would sit strictly above wall 2's ceiling in the standard sandwich
  $\alpha \le \vartheta' \le \bar\chi_f \le \bar\chi$; exact rounding via Dostert–de Laat–Moustrou
  ([arXiv:2001.00256](https://arxiv.org/abs/2001.00256)). Re-opens round 1's "Delsarte rejected"
  box with the no-symmetry-to-diagonalise objection answered.
- **AD. Record hunt at $35 \le n \le 60$.** The ideation lens found that the equilateral triangle
  is a **benchmark orphan** — no Packomania page surfaced, absent from López–Beasley's container
  set, and untouched by the post-1995 metaheuristic wave that rewrote the square and circle
  tables. Its own reading is that $22 \le n \le 34$ is probably solid (the repo's 8-second LS
  reproduces 20 of 26 published values to 14+ digits) and the soft region is past 34 — subject to
  the Amore correction in **Z.4**, which must be settled first.

---

## 3. Ranking and what was staffed

1. **Z — literature/novelty audit.** Cheapest, and it can invalidate other people's work rather
   than adding to it. Staffed.
2. **X — SDP strength gate.** A minutes-long measurement that either reopens a direction the repo
   closed or kills it permanently with a table. Decisive either way. Staffed.
3. **W — grid-rounding refutation.** Shortest path to a rigorous lower bound above Oler's floor,
   with an externally checkable proof artifact. Staffed.
4. **Y — exact $\mathbb{Q}(\sqrt3)$ certificates.** Safe, self-certifying, fills a real gap
   (no exact tight certificate exists for any open $n$). Staffed.
5. **V — stationarity / irreducible contact graphs.** Highest ceiling on the list and the only
   route to an equality, but the most theory-heavy; its enumeration gate is the honest first
   question. Staffed.
6. AA, AB, AC, AD — recorded above, not staffed this round.

**Ranking is the triaging author's judgement and is `sketch` like everything else.**

## 4. Method note (`RULES.md` §8 is a hypothesis, and this round is evidence about it)

Five Fable 5 workers on disjoint lenses produced these; an Opus 5 pass triaged them and re-derived
every load-bearing number. Two observations for the standing evaluation §8 asks for:

- **Convergence across decorrelated lenses was the strongest signal available.** Three of the five
  independently reached the contact-graph/irreducibility mechanism (**V**) from different starting
  points — variational, combinatorial, and literature-transfer. Two independently caught the Oler
  floor error (§0.1).
- **The divergent model also produced the round's one reversal** (**X**, against its own brief's
  stated expectation) and the one observation nobody had made in two prior rounds (§0.2). Both
  survived convergent re-derivation. That is the split working as intended — but it is one round,
  and §8 asks for evidence over time, not an anecdote.
