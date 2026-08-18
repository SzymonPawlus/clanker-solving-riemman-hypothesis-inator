# Candidate attack approaches for the open cases

```
status: sketch          — every claim in this file, without exception
author:  claude (Fable 5, divergent/generative role per RULES.md §8), 2026-08-17
revised: claude (Opus 5, convergent role), 2026-08-18 — corrections from Codex's
         CHANGES_REQUESTED reviews of PR #26; see the per-section "corrected" notes in A, B, C,
         D and F. Nothing was promoted; two things (A's scope, D's k = 6 premise) were demoted.
revised: claude (Opus 5), 2026-08-18, second pass — C's size count recomputed by script rather
         than by hand (t is a program variable, so 33 variables, not 32); the n = 20 wording
         rebased onto merged main, where it is `cited` and qualified, not unresolved.
issue:   #24
```

**Read this first.** This file is a *triage of proposals*, not a record of results. Nothing here
is established; nothing here may be cited or built on as if it were (repo `RULES.md` §3 — a
`sketch` is not assumable, including by its author). Where a statement comes from the literature
it says so with a reference; everything else is speculation by a language model and is labelled
as such. No bound, packing, or value of $s(n)$ is claimed anywhere in this file.

The open cases, per the corrected [`../../README.md`](../../README.md): $n = 16, 17, 18, 19$,
$n = 22\text{–}34$, and everything past 34 (all triangular $n$ are proven, and so is $n = 20$ —
`cited`, **qualified**: it rests on Payan's published abstract asserting that his $k = 5$ proof
extends to $k = 6$, and on no inspection of the paper's body. Issue #14 / PR #36 settled that
provenance and is closed; see D for how this file uses the qualified row).
Every result the repo can currently produce is an **upper bound** (an explicit packing). The
real gap is **lower bounds** — that is what optimality needs and what nothing on the board
currently attacks. Approaches A–D below aim at that gap; E–H aim at better upper bounds, where
the repo already has machinery.

**Board note (2026-08-18, updated).** The follow-up issues filed off the back of this triage
(#27, #28, #29) were filed unassigned, since filing an issue is not the same as claiming it and
`claude` was at the `RULES.md` §1 cap at the time. Current state: **#27** is claimed by `codex`
and implemented in PR #53; **#28** is claimed and in progress under the corrected enclosure-only
scope; **#29** is unassigned and **no longer blocked** — its blocker #14 is closed (PR #36
merged).

## What the board already covers (do not re-propose)

Checked against open issues as of 2026-08-17, so that nothing below duplicates queued work:

| Issue | Scope |
|---|---|
| #2 (+ PR 16) | exact-arithmetic certificate checker |
| #3, #4, #18 | certifying known packings ($n \le 15$, G–L 22–34, fixtures) |
| #9 | multi-start NLP + inflation search (upper bounds) |
| #11 | lifting float output to exact certificates via the contact graph |
| #12 | Lubachevsky–Stillinger billiard front-end |
| #13 | extending past $n = 34$; numerically testing the G–L conjectured families |
| ~~#14~~ | attribution literature gaps — **closed**, PR #36 merged; its outcome is used in D and F |
| #15 (+ PR 19) | Lean feasibility for small $n$ |
| #17 | understanding and writing up Oler's inequality |
| #24 (this file, PR 26) | this triage |
| #27 (+ PR 53), #28, #29 | the follow-ups filed from B, A, D — see the scope corrections in each section |

---

## A. Rigorous interval branch-and-bound: certified near-optimal lower bounds for n = 16

**Scope, corrected 2026-08-18 (Codex review of PR #26).** An earlier draft of this section
presented A as a route to *the exact optimum* for $n = 16$. That was wrong and is withdrawn. A is
scoped here as a **certified near-optimal lower bound** yielding an enclosure of $d(16)$; the
exact-closure mechanism it would additionally need is named below but not proposed.

**The idea.** In the point formulation, fix a side length $d$ and ask whether 16 points at mutual
distance $\ge 2$ fit in the triangle of side $d$. That question is decidable by interval
branch-and-bound: subdivide the configuration box $(x_1, y_1, \dots, x_{16}, y_{16})$, discard any
sub-box on which interval evaluation proves some pairwise distance $< 2$ or some point outside the
triangle, and if every box is discarded then no such packing exists, i.e. $d(16) > d$. Symmetry of
the triangle ($D_3$) and of point relabelling ($S_{16}$) must be quotiented out (fix a canonical
ordering, pin one point's region) or the tree size is hopeless.

**What this delivers, and what it does not.** Closing the exhaustion at one fixed side
$d^* - \varepsilon$ proves exactly $d(16) > d^* - \varepsilon$. Together with the Melissen–Schuur
construction, which gives $d(16) \le d^*$, the output is an **enclosure**
$d^* - \varepsilon < d(16) \le d^*$ of width $\varepsilon$: a rigorous, near-optimal lower bound,
**not** the equality $d(16) = d^*$. Shrinking $\varepsilon$ narrows the enclosure and never closes
it — each run is a separate finite exhaustion at a separate side length, and no finite family of
such runs excludes $d(16)$ from lying strictly between $d^* - \varepsilon$ and $d^*$ for every
$\varepsilon$ actually run. **A write-up reporting such a run as "$n = 16$ solved" is
overclaiming.** Filed issue #28 now carries this scope in its own title *and* body — the
deliverable stated there is the enclosure $d^* - \varepsilon < d(16) \le d^*$, with the two
exact-closure ingredients below named as explicitly out of scope and an $\varepsilon$-cost and
informativeness gate attached — so a worker following that issue cannot pick up the equality
reading from it.

**What exact closure would additionally require (named here, not proposed).** Two further
certified ingredients, neither of which follows from the exhaustion: (i) an interval proof that
*isolates all global optimizers* — outside a finite union of small boxes nothing attains the
optimum, with existence and local uniqueness inside each box established by a validated
fixed-point argument (Krawczyk / interval Newton) rather than by numerical convergence; and (ii) a
separately certified structural or algebraic argument identifying the objective value of the
configurations in those boxes **exactly** — e.g. solving the contact system in exact algebraic
arithmetic, which is approach E's machinery. Ingredient (ii) is where an algebraic $d^*$ would
actually be pinned. Naming them is the point: nobody should mistake the enclosure for the
equality.

**Precedent — this is a transfer, not an invention.** Exactly this programme was carried out on
the hard unit-*square* cases: Markót & Csendes treated 28, 29 and 30 circles in the square
by a fully interval-arithmetic branch-and-bound
([SIAM J. Optim. 2005](https://epubs.siam.org/doi/10.1137/S1052623403425617),
[Numer. Algorithms 2005](https://link.springer.com/article/10.1023/B:NUMA.0000049472.75023.0a);
reported CPU times ~21–53 h on 2005 hardware), and Markót extended it to 31–33
([2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8550790/)). Read what those papers actually
report, because it is the same distinction drawn above: the Markót–Csendes abstract says the
cases $n = 28\text{–}30$ were solved *"within very tight tolerance values"*, and Markót 2021 reports
high-precision **enclosures** of the optimal values. The precedent therefore supports the enclosure
scope and supplies **no** exact-closure mechanism. A web search (2026-08-17) found
**no published attempt at the equilateral-triangle container for $n = 16\text{–}19$** — the
triangle proofs to date (Melissen 1993/1994, Payan 1997, Joós 2020) are hand case analyses. That
absence is an opportunity, but note honestly: it may also mean people tried and it was too
expensive; the triangle literature is smaller than the square's.

**Why n = 16.** Smallest open case; 32 coordinates before symmetry reduction, comparable to the
square's $n = 28\text{–}33$ successes (56–66 coordinates) — so *a priori* not obviously too big;
and a sharp conjectured answer to match (Melissen & Schuur 1995) rather than an open-ended
search. $n = 17, 18, 19$ are the follow-ons if the machinery works.

**Kill-criterion.** Gate on a validation instance, per problem `RULES.md` §5/§6: the code must
first reproduce a *known* bound — suggested $n = 12$ (proven, non-trivial, non-triangular) —
by closing the exhaustion at $d^*(12) - \varepsilon$ for an $\varepsilon$ small enough that the
resulting enclosure is non-trivial. If the validated $n = 12$ run cannot close within a budgeted
box count (say $10^8$ boxes or ~10 h), or if extrapolating its cost to $n = 16$ (tree growth
measured empirically on $n = 10, 11, 12$) exceeds ~$10^3$ CPU-hours, abandon or downscope.
Second kill, specific to the corrected scope: cost must be reported *as a function of*
$\varepsilon$, and if no $\varepsilon$ affordable within budget yields an enclosure narrow enough
to separate the conjectured optimum from the nearest competing configuration, the run is not
informative and the attack stops. Third kill: if Markót-style tools turn out
to depend essentially on the square's axis-aligned structure (their polygon representation
machinery) in a way that does not transfer, say so and stop.

**Cost.** The largest item on this list: serious engineering over many sessions, plus real CPU
(long runs need per-run human OK under the 1-hour rule; the design must checkpoint). Incremental
and parallelisable by subtree, which suits the issue/worker model.

**Reuse.** Point formulation and conventions from `RULES.md` §2; the exact checker (#2) verifies
the *witness* side; the B&B trace itself is a new kind of artifact (a proof by exhaustion) whose
verification story needs designing — plausibly the other agent re-runs an independently
implemented verifier over the emitted box tree, mirroring the §3 two-checkers pattern.

**Literature status.** Method: established in the square (cited above), where it produced
high-precision enclosures rather than closed-form optima. Application to the triangle: not found
— *believed novel, unverified*. Exact-optimum closure by this method alone: not claimed and not
available (see the scope note at the head of this section).

---

## B. Automated partition (pigeonhole) certificates — the Lean-compatible lower bound

**The idea.** The oldest lower-bound trick in this subject: if the triangle of side $d$ (point
formulation) can be partitioned into $n - 1$ pieces each of diameter $< 2$, then $n$ points at
mutual distance $\ge 2$ cannot fit (two land in one piece). So a *lower-bound certificate* for $s(n)$ has **two** parts, and only the second
is a diameter computation:

1. **A cover/partition certificate — the part an earlier draft omitted.** The $n-1$ cells must be
   *proved* to cover the whole triangle. Rational vertex-distance checks say nothing about
   coverage: a family of tiny polygons passes every diameter check and covers almost nothing, and
   the pigeonhole step then simply fails. What discharges this is a combinatorial *incidence*
   certificate — present the cells as the faces of an explicit **triangulation** of the container
   (vertex list, edge list, face list) together with the checks that make it one: every interior
   edge shared by exactly two faces, every boundary edge belonging to exactly one face and lying
   on a side of the container, faces consistently oriented with positive rational area, and the
   face areas summing *exactly* to the container's area. These are again rational (in)equalities
   plus finite combinatorial bookkeeping, so they stay Lean-checkable — but they must be stated
   and checked, never inferred from a picture.
2. **A diameter bound per cell.** For a *convex* cell this reduces to the pairwise vertex
   distances (a convex polygon attains its diameter at vertices) — the finite conjunction of
   rational inequalities. Convexity of each cell is therefore itself part of what (1) must
   certify: for a non-convex cell the maximum vertex distance is not the diameter and the bound
   is unsound.

**Coordinates.** Work in **oblique triangle coordinates**: container
$\{(u,v) : u \ge 0,\ v \ge 0,\ u + v \le d\}$ in the basis $\{(1,0),\ (1/2,\ \sqrt{3}/2)\}$. In
Cartesian coordinates the apex $(d/2,\ d\sqrt{3}/2)$ is irrational for rational $d$, so a
"rational polygon cover" of the Cartesian triangle either fails to cover a neighbourhood of the
apex or quietly rounds it — exactly the kind of silent gap part (1) exists to catch. In oblique
coordinates all three corners are rational and the cover can be exact; the price is that squared
Euclidean distance becomes $\Delta u^2 + \Delta u\,\Delta v + \Delta v^2$, still a rational
quadratic form, so the diameter checks remain rational.

Both parts have the shape of object the in-flight Lean feasibility work (#15) can verify, which
would make this the **only route on this list to a `verified:lean` lower bound**, the strongest
artifact this repo can produce.

Melissen's proofs use partition arguments of this flavour (his 1993 Monthly paper; `cited` at
the level of "this is his method family" — the exact structure of each proof was not re-read for
this triage). The proposal is to *automate the search for the partition*: parametrise a
candidate partition by its interior vertices, maximise the slack $\min(2 - \mathrm{diam})$ by
local optimisation over vertex positions and over combinatorial partition topologies, and emit
any partition with positive slack as an exact certificate after rational rounding.

**The honest catch (speculation, load-bearing).** Plain pigeonhole is generally *not* tight: at
the critical side length a diameter-$<2$ partition into $n-1$ pieces need not exist, and for the
hard $n$ Melissen needed case analysis beyond pure pigeonhole. So the expected outcome for the
open $n$ is a lower bound *short of* the conjectured optimum — still a first rigorous,
machine-checked lower bound for, say, $n = 16$, which the repo currently has none of, at any
strength. Whether pigeonhole can be tight for any open $n$ is unknown to me.

**Which n.** Sweep $n \le 15$ first (each solved case tells us how far pigeonhole alone
reaches — cheap, decisive calibration data). Then $n = 16\text{–}19$ at the conjectured values
and just below.

**Kill-criterion.** If the automated search cannot rediscover partition certificates matching
the known lower bounds for the *easy* solved cases (the ones Melissen handled by
partition-style arguments — identify these while executing, coordinating with #17), the
automation is not working; fix or abandon within ~2 sessions. If it works on solved cases but
for every open $n$ the best certified bound is farther from the conjectured optimum than the
weakest already-published lower bound found in the literature for that $n$ (to be looked up as
part of the attack), the approach adds nothing — write up the calibration table as the result
and close.

**Cost.** Low-to-moderate. Search is cheap (few dozen variables per candidate topology); the
deliverable is exact certificates plus a Lean statement per certificate.

**Reuse.** Highest reuse on this list: rational-arithmetic style from #2, Lean pipeline from
#15, Oler/lower-bound context from #17.

**Literature status.** Partition arguments: classical, used by Melissen (cited). Automating the
partition search for this container: not found in a (shallow) search — *believed novel,
unverified*. A deeper check for "diameter partition" / "plank-type" automated bounds should be
step zero of the attack.

---

## C. SDP / Lasserre moment hierarchy lower bounds

**The idea.** Fix the triangle side $d$ and consider the polynomial optimisation problem
"maximise $t$ subject to $\|p_i - p_j\|^2 \ge t$ for all pairs, $p_i$ in the triangle
(three linear constraints each)". **The formulation used throughout this section is that one**:
$t$ is a *decision variable of the polynomial program*, on exactly the same footing as the point
coordinates, so at $n$ points the program has $2n + 1$ variables and every dimension quoted below
is computed at that count. (The alternative — fix $t$ externally and ask only whether the system is
feasible, deriving the bound from infeasibility at that $t$ — has $2n$ variables and different
dimensions; `moment_sizes.py --fixed-t` prints those. Do not mix the two.) A Lasserre/moment
relaxation of this maximisation yields
rigorous *upper* bounds on the best achievable minimal distance — equivalently lower bounds on
$s(n)$ — once the SDP's dual solution is post-processed into an exact certificate (rational
rounding of the sum-of-squares decomposition, standard but fiddly). Symmetry reduction
(invariance under $S_n \times D_3$, Gatermann–Parrilo style) is mandatory for the sizes here.

**Why it might bite, and why it might not.** SDP hierarchies are the state of the art for
packing bounds in the infinite setting (Cohn–Elkies; de Laat–Vallentin,
[arXiv:1311.3789](https://arxiv.org/pdf/1311.3789), a hierarchy for packing problems in
discrete geometry that converges in finitely many steps). I found **no application to the
finite triangle-container problem** — *possibly novel, unverified*. The threat is size, and this
section has now had **two** hand-counts of it wrong (first the wrong units, then a count that
forgot $t$ is a variable). The numbers below are therefore no longer hand-computed: they are the
output of [`moment_sizes.py`](./moment_sizes.py) in this directory, which anyone can re-run.

For $n = 16$ the program has $2 \times 16 + 1 = 33$ variables — 32 coordinates and $t$. The *dense
order-2 moment matrix* therefore has $\binom{35}{2} = 595$ rows (order 3 has
$\binom{36}{3} = 7140$) — both comfortably inside what open solvers handle, so a
matrix-*dimension* cutoff cannot rule out level 2, even before symmetry reduction. The real
bottleneck is the rest of the problem data: the level-2 SDP carries one scalar variable per moment
of degree $\le 4$, i.e. $\binom{37}{4} = 66{,}045$ of them, plus one localizing matrix for each of
the $\binom{16}{2} = 120$ pairwise-distance constraints and each of the $3 \times 16 = 48$
containment constraints (order 1 at level 2, hence $34 \times 34$ apiece), after which the
exact-certificate step must round a dual solution of that size into rational sum-of-squares data.
Those counts, not the moment-matrix dimension, are what a size gate has to measure. Separately, low
levels of the hierarchy are usually slack for maximin-distance
problems. Unlike A, there is no precedent that
low-level relaxations are tight for any container problem of this kind — this is the most
speculative lower-bound route here.

**Which n.** Calibrate on $n = 5, 7, 8$ (known $t$, tiny). Only if slack there is small, try
$n = 16$.

**Kill-criterion.** Two gates. (i) *A reproducible size count before any code*, gating on the
quantities that actually bind. The *unreduced* half of that count is already done and reproducible:
[`moment_sizes.py`](./moment_sizes.py) prints it (`python3 moment_sizes.py`, no dependencies), and
the figures quoted above — $595$, $7140$, $66{,}045$, $34 \times 34$ localizing blocks,
$120 + 48$ of them — are exactly its output at $n = 16$, level 2. What remains for the attack is
the reduced half: the block structure and dimensions of the moment and localizing matrices after
reduction by $S_{16} \times D_3$, and the resulting SDP data size for symmetry-reduced level 2 at
$n = 16$; compare that against what an open solver (SDPA-GMP, SCS, or Mosek where available) is
documented to handle and against what the rational-rounding step can process. Stop if it does not
fit, and record the counts either way. The unreduced figures are the *starting point*, not the gate
itself. This estimate is a one-day task and should be done first. (ii) On the calibrated
small cases: if the level-2 (or affordable level-3) bound's relative slack against the known
optimum exceeds ~1%, the hierarchy will not distinguish conjectured optima from nearby values at
open $n$; abandon and record the slack table.

**Cost.** High expertise cost, moderate compute. Weakest reuse of existing repo machinery.

**Literature status.** Hierarchy: established elsewhere (cited above). This application: not
found; treat the novelty claim as unverified.

---

## D. Erdős–Oler for k = 7 (n = 27) — mechanise Payan's method

**Dependency, stated first (corrected 2026-08-18, Codex reviews of PR #26).** An earlier draft of
this section asserted the $k = 6$ / $n = 20$ result flatly as `cited` on a secondary source, with
no record of what had actually been read. The first correction over-corrected and called it
*unresolved*. Neither is the settled position. **Issue #14 is closed and PR #36 is merged**, and
`main` now records the row in the form this section adopts:

> $s(20) = 10 + 2\sqrt{3}$ is optimal — **`cited`, qualified**. Payan's published abstract states
> that his $k = 5$ ($n = 14$) proof extends, "un peu plus laborieusement", to $k = 6$ ($n = 20$):
> the author positively asserting, in his own paper's abstract, that the method applies at
> $k = 6$. This project has read that abstract from the publisher's page and has **not** obtained
> the paper's body, so it has not seen how the extension is carried out and cannot distinguish a
> case written out in full from one left to the reader. That is a reason to record the provenance,
> not a reason to call the result unproved.

Three consequences for this attack:

- $k = 6$ / $n = 20$ **is** usable — it is `cited` — but every use of it must carry the
  abstract-only qualification, here and in F. It is not the anchor to lean an argument on where a
  fully-warranted alternative ($n = 14$) is available.
- "$k = 7$ is the next open case" therefore stands, on that same qualified footing.
- The attribution audit that step (1) below used to duplicate is **done** (#14 / PR #36). What
  remains for step (1) is the part #14 did *not* do: obtaining and reading the **body** of
  Payan 1997. Issue #29's scope starts from the completed audit and is no longer blocked.

**The idea.** The Erdős–Oler conjecture $s(\Delta(k) - 1) = s(\Delta(k))$ is proven for
$k \le 4$ (Melissen 1993) and for $k = 5$, $n = 14$ (Payan 1997 — his abstract states this one
outright, so it is `cited`); $k = 6$ is `cited` with the abstract-only qualification above. The
case $n = 27 = \Delta(7) - 1$, with predicted $s(27) = 12 + 2\sqrt{3}$, sits *inside* the open
22–34 band and has both a sharp predicted answer and a proof template two sizes down. The attack:
(1) obtain and digest the **body** of Payan (Discrete Math. 165–166, in French — the #14
attribution audit read the abstract only, so the body is the remaining literature step);
(2) reconstruct the $k = 5$ proof — the one case whose proof the abstract states unambiguously —
with a computer-checked case analysis; (3) measure how the case count scales $k = 5 \to 6$, which
would also show how the $k = 6$ case is actually discharged, the one thing the abstract does not
reveal; (4) attempt $k = 7$ only if the scaling permits.

**Why this n.** A proof would be the first optimality result in the 22–34 band and would
progress a named conjecture; even step (2) alone would upgrade the repo's understanding of the
only modern lower-bound technique beyond Oler's inequality.

**Kill-criterion.** (0) If the body of Payan 1997 cannot be obtained at all, steps (2)–(4) do not
start — there is no reconstructing a method nobody here has seen; report that and stop. (a) If
step (1) shows Payan's argument is ad hoc per-$k$ with no mechanisable
skeleton, stop after writing up what the method actually is (that write-up is a deliverable —
it feeds #17). (b) If the measured case growth $k=5 \to 6$ extrapolates to an infeasible count
at $k = 7$ (estimate before launching anything), stop. (c) If a citation search on Payan 1997
turns up an existing $k \ge 7$ attempt or proof, defer to the literature.

**Cost.** Literature-heavy start (cheap), then medium. Sequenced so every stage yields a
standalone write-up.

**Reuse.** #17 (Oler) is the natural companion; the exact checker verifies any constructions
used in the case analysis.

**Literature status.** Conjecture: cited. $k \le 4$ and $k = 5$ ($n = 14$) proofs: cited.
$k = 6$ ($n = 20$): **`cited`, qualified** — positively asserted by Payan's own abstract, body not
inspected (#14, closed); cite it only with that qualification attached. $k = 7$: no attempt found
in a shallow search — needs the citation sweep in step (1). The preprint an earlier draft referred
to without a link is:
*Optimal Circle Packings for Triangular Numbers: A Detailed Mathematical Proof For Paul Erdos and
Norman Oler conjecture*, posted 2024-12-09,
[ResearchGate publication 387465203](https://www.researchgate.net/publication/387465203_Optimal_Circle_Packings_for_Triangular_Numbers_A_Detailed_Mathematical_Proof_For_Paul_Erdos_and_Norman_Oler_conjecture)
(also mirrored on Academia.edu). Identified by web search on 2026-08-18; **not peer-reviewed, and
nobody here has opened it** — so its own status in this repo is nothing at all. Step (1) must
assess it, since if it were right this attack would be moot; per repo norms an unreviewed preprint
settles nothing either way.

---

## E. Contact-graph enumeration with exact algebraic solving

**The idea.** An optimal packing at its critical side length is (generically) held by a rigid
contact structure: a subgraph of touching pairs and wall contacts whose contact system pins the
configuration. Enumerate the combinatorially plausible contact graphs for a given $n$ (planar;
degree bounds; enough contacts for rigidity of the jammed core, in Connelly's jamming sense —
that framework is established literature), solve each contact system in exact algebraic
arithmetic (Gröbner bases / resultants over the equations "distance = 2" and "point on wall"),
discard infeasible solutions, and take the best survivor. Two distinct uses, in descending
ambition: (i) if the enumeration class can be *proven* exhaustive, this is an optimality proof —
that is how Tedeschi's programme aims to re-derive $n = 13$ discretely (cited in the problem
README); (ii) without exhaustiveness it is still an exact-candidate generator that feeds the
contact-graph lifting issue #11 with *systematically enumerated* rather than search-discovered
graphs.

**The hard part (honest).** Exhaustiveness. Optimal packings contain rattlers (problem
`RULES.md` §5), so the contact graph does not span all $n$ circles — the enumeration must cover jammed cores with
$m < n$ circles plus certified placements of the rest, and the lemma "every optimal packing has
a jammed core with $\ge$ [bound] contacts" needs an actual proof before use (a `sketch` until
then). I do not know such a bound for this container — speculation.

**Which n.** $n = 16$ for the proof ambition (smallest open); any of 22–34 for the generator use.

**Kill-criterion.** Estimate the size of the rigidity-constrained graph class for $n = 16$
before solving anything (pure combinatorial enumeration, cheap). If it exceeds ~$10^7$, or if
after two sessions no sound exhaustiveness lemma can even be *stated*, demote to use (ii) and
fold into #11 — that demotion is the expected outcome and is still useful.

**Cost.** Medium-high; the algebraic solving per graph is standard but slow.

**Reuse.** Direct overlap with #11 (by design), exact checker #2 for every emitted candidate.

**Literature status.** Rigidity/jamming framework: established (Connelly et al.). Exhaustive
contact-graph optimality proof for the triangle at open $n$: none found; Tedeschi is the nearest
programme (cited).

---

## F. An Oler inequality with a vacancy correction (theory attack, cheap to kill)

**The idea — pure speculation.** Oler's inequality is *attained* at triangular $n$: the
triangular-lattice packing meets the bound there, so the bound cannot be improved at those $n$.
What must **not** be said — and what an earlier draft of this section did say — is that Oler is
tight "exactly" at triangular $n$. That phrasing asserts *strict slackness at every
non-triangular $n$*, which has never been established for the $n$ whose optimum is unknown:
comparing Oler's lower bound against a **construction** upper bound at an open $n$ shows only that
the two known bounds differ, and cannot rule out $s(n) = s_{\text{Oler}}(n)$, because $s(n)$ itself
is unknown there. (PR #21 is withdrawing exactly this overclaim.) So "tight only at triangular $n$"
survives here as **conjectural motivation** only, unless an equality-characterisation theorem —
one saying which configurations attain Oler's bound — is found and cited; looking for one belongs
to #17.

With that qualification: the proven near-triangular cases ($n = 5, 9, 14$, and $n = 20$ on the
qualified abstract-only footing described in D) and all seven Graham–Lubachevsky conjectured
families are lattice packings
with structured vacancies (G–L 1995, cited). Conjecture *shape* (not a claim): an inequality
of the form "$n$ points at distance $\ge 2$ in a triangle of side $d$ imply the Oler bound
minus a correction term $f(j)$ that vanishes as the vacancy structure degenerates" — informally,
removing $j$ points from the lattice can only buy a bounded, quantifiable amount of side length.
Even a crude such inequality would be the first *general-purpose* lower-bound tool beyond Oler
and would bite exactly on the near-triangular open cases $n = 25, 26, 27$ and the G–L families.

**Concrete first step (one day, numeric only).** Compute the slack of Oler's inequality — and
of the Folkman–Graham refinement (*A packing inequality for compact convex subsets of the
plane*, Canad. Math. Bull. 1969; existence cited, statement not yet pulled — do this via #17) —
at the proven values $n = 5, 9, 14$ and $n = 20$. Label the $n = 20$ row with its abstract-only
provenance (see D) and keep $n = 14$ as the primary anchor, since that is the case whose proof the
abstract states outright. The pattern of slacks either suggests a correction-term shape or shows
there is no usable pattern.

**Kill-criterion.** If no candidate correction term reproduces the proven case $n = 14$
(i.e., every attempted $f$ either fails soundness on triangular $n$ or gives a bound weaker
than plain Oler at $n = 14$), abandon after the calibration computation and write up the slack
table as a refutation-grade note. $n = 20$ may corroborate but should not displace $n = 14$ as the
anchor, for the provenance reason in D. Hard cap: two sessions before either a precise conjectured
inequality exists (then it goes to the convergent model for attempted proof) or the attack
closes.

**Cost.** Nearly free to test; unbounded to complete — which is why the cap above is the real
control.

**Reuse.** #17's write-up is a prerequisite; slack computations use the exact-arithmetic habits
of #2.

**Literature status.** Oler, Folkman–Graham: cited. A vacancy-corrected Oler inequality: none
found — *speculation*; a real literature pass (Groemer's Math. Z. 1960 line of work included)
is step zero.

---

## G. Symmetry-orbit and vacancy-template seeding (generator, upper bounds)

**The idea.** Use structure to *generate seeds*, never to constrain claims (problem `RULES.md`
§5 forbids symmetric-restricted optimality claims; several known optima are asymmetric — the
final optimisation always releases all constraints). Two template families: (i) triangular
lattice $\Delta(k)$ minus $j$ vacancies, enumerated as orbits under the triangle's $D_3$ action
(small orbit counts, exhaustively enumerable for relevant $j$); (ii) $C_3$/$D_3$-symmetric cores
with a free remainder. Feed every template as a warm start to the #9/#12 optimisers, then relax
without symmetry. Purpose: cheaper record discovery for $35 \le n \le 56$ (virgin territory
past the G–L table, target of #13) and re-derivation pressure on the 1995-era 22–34 records.

**Which n.** 35–56 primarily; 22–34 secondarily.

**Kill-criterion.** A/B test against unbiased multistart at equal compute on $n$ where records
exist (G–L table / Packomania): if template seeding fails to reach records that unbiased
restarts reach, or reaches them no faster over a batch of ~$10^3$ runs, the templates add
nothing — drop and record the comparison.

**Cost.** Low, *conditional on #9/#12 existing* — this is a seeding module, not an engine.
Coordinate with those issue holders; scope here is strictly the template enumerator.

**Literature status.** G–L 1995 explicitly exploited lattice-with-vacancy structure and grouped
their records into families (cited) — the *idea* is theirs. Systematic exhaustive enumeration of
vacancy orbits as seeds is not reported in their paper as far as a skim shows; verify against
the open-access text before claiming any novelty. Novelty here is modest and the value is
practical, not conceptual.

---

## H. Rattler-aware escape moves (local search operator, upper bounds)

**The idea.** Rattlers mark wasted space. After a converged run: identify the jammed core (the
force/contact network), then (i) delete a rattler and re-insert it at the deepest point of the
free space (furthest-point Voronoi computation), re-optimise; (ii) "vacancy migration" — swap a
rattler with an adjacent jammed circle to walk the hole toward a wall or corner, re-optimise.
Motivation: in the 22–34 band the dominant failure of restarts is convergence to near-records
differing from the record by exactly this kind of defect placement (my reading of G–L's
descriptions; their paper discusses rattlers — cited — but does not report using them as an
explicit move operator, as far as a skim shows).

**Which n.** Anywhere #9/#12 run; most valuable where records are old (22–34) or absent (>34).

**Kill-criterion.** A/B against plain random perturbation restarts on $n$ with reproducible
records: if over ~$10^3$ trials the rattler moves never reach a strictly better basin than
plain restarts at equal compute, drop the operator and log the comparison.

**Cost.** Low; a plugin to #9/#12.

**Literature status.** Rattlers: discussed by G–L (cited). This move class in this problem: not
found in the two 1995 papers; similar restart heuristics surely exist in the broader packing
literature (unverified) — novelty claim weak. Value is practical.

---

## Triage — ranked recommendation (author's judgement, sketch)

1. **B — partition certificates.** Cheapest credible path to the repo's first rigorous lower
   bound for an open $n$, and the only approach whose output is plausibly `verified:lean` —
   provided the cover/partition certificate of B(1) is delivered, not just the diameter checks.
   Its calibration step is fast and decisive in either direction. → **filed as issue #27**, since
   claimed by `codex` and implemented in PR #53, whose verifier checks exactly the load-bearing
   cover requirement (containment, pairwise zero-area intersection, exact total-area coverage,
   exactly $n-1$ cells, exact squared diameter $< 4$) rather than diameters alone.
2. **A — interval branch-and-bound for $n = 16$, scoped as an enclosure.** The only approach with
   a literature record of closing container cases of this difficulty (the square programme), and
   what it closes there is a high-precision *enclosure*, not a closed-form optimum — so the
   deliverable here is a certified near-optimal lower bound, not "$n = 16$ solved". Heavy, but
   incremental, checkpointable, and parallelisable. → **filed as issue #28**, whose title *and*
   body now state the enclosure-only deliverable, the exact-closure ingredients it does not
   deliver, and an $\varepsilon$-cost and informativeness gate.
3. **D — Erdős–Oler $k = 7$.** Sharpest target in the open band, and **no longer blocked**:
   #14 is closed, the $k = 6$ premise is `cited` with an abstract-only qualification, and the
   remaining literature step is the one #14 did not do — reading the body of Payan 1997.
   → **filed as issue #29, unassigned and unblocked.**
4. **F** — nearly free to test, likely to die, and a documented refutation is a first-class
   outcome here. Do the slack computation opportunistically after #17 lands.
5. **E** — pursue as generator (ii) inside #11's orbit; promote only if an exhaustiveness lemma
   materialises.
6. **G, H** — cheap add-ons once #9/#12 exist; hand to whoever holds those issues rather than
   opening parallel work.
7. **C** — do the one-day size estimate before anything else; expected outcome is that it dies
   on SDP size, in which case record the estimate and close.

## Considered and rejected as already done (or already queued)

- **Billiard/LS search for 22–34.** This *is* Graham & Lubachevsky 1995; porting the method is
  already issue #12. Nothing new to propose.
- **Hand-crafted candidate constructions for 16–18.** Melissen & Schuur 1995 already did the
  constructions; only optimality is open. Proposing "find good packings for 16–18" in 2026 is
  rediscovery.
- **Symmetric-restricted search presented as optimality.** Banned by problem `RULES.md` §5 and
  wrong on the merits (known asymmetric optima). Symmetry appears above only as a seed
  generator (G).
- **Re-proving $n \le 15$ as a goal in itself.** Already on the board as certification (#3);
  solved cases appear above only as validation instances for A, B, C, E.
- **Numerically testing the G–L conjectured families.** Already scoped inside issue #13; not
  duplicated here. The *lower-bound* side of those families is covered by D and F instead.

## Sources consulted for this triage

- Graham & Lubachevsky 1995, Melissen & Schuur 1995, Melissen 1993/1994, Payan 1997, Joós 2020,
  Tedeschi 2021 — as catalogued with links in [`../../README.md`](../../README.md) (the two 1995
  papers were used as the primary "already done in 1995" filter, per the task).
- [Markót & Csendes, SIAM J. Optim. 2005](https://epubs.siam.org/doi/10.1137/S1052623403425617);
  [Numer. Algorithms 2005](https://link.springer.com/article/10.1023/B:NUMA.0000049472.75023.0a);
  [Markót 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8550790/) — square-container
  optimality proofs by interval methods (approach A's precedent).
- [de Laat & Vallentin, arXiv:1311.3789](https://arxiv.org/pdf/1311.3789) — SDP hierarchy for
  packing problems in discrete geometry (approach C's precedent).
- Folkman & Graham 1969, Canad. Math. Bull.; Groemer 1960, Math. Z. — existence cited, contents
  not read (flagged inside approaches D/F).
- [*Optimal Circle Packings for Triangular Numbers: A Detailed Mathematical Proof For Paul Erdos
  and Norman Oler conjecture*, ResearchGate 387465203](https://www.researchgate.net/publication/387465203_Optimal_Circle_Packings_for_Triangular_Numbers_A_Detailed_Mathematical_Proof_For_Paul_Erdos_and_Norman_Oler_conjecture),
  posted 2024-12-09 — the preprint referred to in D. Located by web search 2026-08-18 so that the
  reference is checkable; **not peer-reviewed and not read here**, so it carries no status.
- Web search 2026-08-18 to locate the ResearchGate preprint above (previously cited only as
  "a preprint exists", which is not a checkable citation).
- Web searches 2026-08-17 confirming $n = 16\text{–}19$ remain open and finding no
  triangle-container interval-B&B or SDP attempt. Absence of evidence from a search is weak —
  each filed attack repeats its own literature step as stage zero.
