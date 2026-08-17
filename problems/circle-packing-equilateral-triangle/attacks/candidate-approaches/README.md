# Candidate attack approaches for the open cases

```
status: sketch          — every claim in this file, without exception
author: claude (Fable 5, divergent/generative role per RULES.md §8), 2026-08-17
issue:  #24
```

**Read this first.** This file is a *triage of proposals*, not a record of results. Nothing here
is established; nothing here may be cited or built on as if it were (repo `RULES.md` §3 — a
`sketch` is not assumable, including by its author). Where a statement comes from the literature
it says so with a reference; everything else is speculation by a language model and is labelled
as such. No bound, packing, or value of $s(n)$ is claimed anywhere in this file.

The open cases, per the corrected [`../../README.md`](../../README.md): $n = 16, 17, 18, 19$,
$n = 22\text{–}34$, and everything past 34 (with $n = 20, 21$ and all triangular $n$ proven).
Every result the repo can currently produce is an **upper bound** (an explicit packing). The
real gap is **lower bounds** — that is what optimality needs and what nothing on the board
currently attacks. Approaches A–D below aim at that gap; E–H aim at better upper bounds, where
the repo already has machinery.

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
| #14 | attribution literature gaps |
| #15 (+ PR 19) | Lean feasibility for small $n$ |
| #17 | understanding and writing up Oler's inequality |

---

## A. Rigorous interval branch-and-bound optimality for n = 16

**The idea.** In the point formulation, "the Melissen–Schuur construction for $n = 16$ is
optimal" is a global-optimisation statement over a compact box: there do not exist 16 points at
mutual distance $\ge 2$ in the triangle of side $d^* - \varepsilon$. That statement is decidable
by interval branch-and-bound: subdivide the configuration space $(x_1, y_1, \dots, x_{16},
y_{16})$, discard any box on which interval evaluation proves some pairwise distance $< 2$ or
some point outside the triangle, and terminate when every box is discarded. Symmetry of the
triangle ($D_3$) and of point relabelling ($S_{16}$) must be quotiented out (fix a canonical
ordering, pin one point's region) or the tree size is hopeless.

**Precedent — this is a transfer, not an invention.** Exactly this programme settled the hard
unit-*square* cases: Markót & Csendes proved optimality for 28, 29 and 30 circles in the square
by a fully interval-arithmetic branch-and-bound
([SIAM J. Optim. 2005](https://epubs.siam.org/doi/10.1137/S1052623403425617),
[Numer. Algorithms 2005](https://link.springer.com/article/10.1023/B:NUMA.0000049472.75023.0a);
reported CPU times ~21–53 h on 2005 hardware), and Markót extended it to 31–33
([2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8550790/)). A web search (2026-08-17) found
**no published attempt at the equilateral-triangle container for $n = 16\text{–}19$** — the
triangle proofs to date (Melissen 1993/1994, Payan 1997, Joós 2020) are hand case analyses. That
absence is an opportunity, but note honestly: it may also mean people tried and it was too
expensive; the triangle literature is smaller than the square's.

**Why n = 16.** Smallest open case; 32 coordinates before symmetry reduction, comparable to the
square's $n = 28\text{–}33$ successes (56–66 coordinates) — so *a priori* not obviously too big;
and a sharp conjectured answer to match (Melissen & Schuur 1995) rather than an open-ended
search. $n = 17, 18, 19$ are the follow-ons if the machinery works.

**Kill-criterion.** Gate on a validation instance, per problem `RULES.md` §5/§6: the code must
first *re-prove* a known optimum, suggested $n = 12$ (proven, non-trivial, non-triangular). If
the validated $n = 12$ run cannot close within a budgeted box count (say $10^8$ boxes or ~10 h),
or if extrapolating its cost to $n = 16$ (tree growth measured empirically on $n = 10, 11, 12$)
exceeds ~$10^3$ CPU-hours, abandon or downscope. Secondary kill: if Markót-style tools turn out
to depend essentially on the square's axis-aligned structure (their polygon representation
machinery) in a way that does not transfer, say so and stop.

**Cost.** The largest item on this list: serious engineering over many sessions, plus real CPU
(long runs need per-run human OK under the 1-hour rule; the design must checkpoint). Incremental
and parallelisable by subtree, which suits the issue/worker model.

**Reuse.** Point formulation and conventions from `RULES.md` §2; the exact checker (#2) verifies
the *witness* side; the B&B trace itself is a new kind of artifact (a proof by exhaustion) whose
verification story needs designing — plausibly the other agent re-runs an independently
implemented verifier over the emitted box tree, mirroring the §3 two-checkers pattern.

**Literature status.** Method: established in the square (cited above). Application to the
triangle: not found — *believed novel, unverified*.

---

## B. Automated partition (pigeonhole) certificates — the Lean-compatible lower bound

**The idea.** The oldest lower-bound trick in this subject: if the triangle of side $d$ (point
formulation) can be partitioned into $n - 1$ pieces each of diameter $< 2$, then $n$ points at
mutual distance $\ge 2$ cannot fit (two land in one piece). So a *lower-bound certificate* for
$s(n)$ is: a family of $n-1$ polygons with rational vertices covering the triangle, with each
diameter bounded by an explicit rational computation — a finite conjunction of rational
inequalities. That is precisely the shape of object the in-flight Lean feasibility work (#15)
can verify, which would make it the **only route on this list to a `verified:lean` lower
bound**, the strongest artifact this repo can produce.

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
(three linear constraints each)". A Lasserre/moment relaxation of this maximisation yields
rigorous *upper* bounds on the best achievable minimal distance — equivalently lower bounds on
$s(n)$ — once the SDP's dual solution is post-processed into an exact certificate (rational
rounding of the sum-of-squares decomposition, standard but fiddly). Symmetry reduction
(invariance under $S_n \times D_3$, Gatermann–Parrilo style) is mandatory for the sizes here.

**Why it might bite, and why it might not.** SDP hierarchies are the state of the art for
packing bounds in the infinite setting (Cohn–Elkies; de Laat–Vallentin,
[arXiv:1311.3789](https://arxiv.org/pdf/1311.3789), a hierarchy for packing problems in
discrete geometry that converges in finitely many steps). I found **no application to the
finite triangle-container problem** — *possibly novel, unverified*. The threat is size: for
$n = 16$ the level-2 moment matrix over 32 variables is already enormous, and low levels of the
hierarchy are usually slack for maximin-distance problems. Unlike A, there is no precedent that
low-level relaxations are tight for any container problem of this kind — this is the most
speculative lower-bound route here.

**Which n.** Calibrate on $n = 5, 7, 8$ (known $t$, tiny). Only if slack there is small, try
$n = 16$.

**Kill-criterion.** Two gates. (i) *Size estimate on paper before any code*: if the
symmetry-reduced level-2 SDP for $n = 16$ exceeds what open solvers handle (~$10^4$-dim moment
matrix), stop — this estimate is a one-day task and should be done first. (ii) On the calibrated
small cases: if the level-2 (or affordable level-3) bound's relative slack against the known
optimum exceeds ~1%, the hierarchy will not distinguish conjectured optima from nearby values at
open $n$; abandon and record the slack table.

**Cost.** High expertise cost, moderate compute. Weakest reuse of existing repo machinery.

**Literature status.** Hierarchy: established elsewhere (cited above). This application: not
found; treat the novelty claim as unverified.

---

## D. Erdős–Oler for k = 7 (n = 27) — mechanise Payan's method

**The idea.** The Erdős–Oler conjecture $s(\Delta(k) - 1) = s(\Delta(k))$ is proven for
$k \le 6$ (Melissen 1993 for $k \le 4$; Payan 1997 for $k = 5, 6$ — `cited`, per the problem
README). The next case, $n = 27 = \Delta(7) - 1$ with predicted $s(27) = 12 + 2\sqrt{3}$, sits
*inside* the open 22–34 band and is the only open case with a sharp predicted answer and a proof
template two sizes down. The attack: (1) obtain and digest Payan (Discrete Math. 165–166, in
French — nobody in this repo has read it; the README flags that even its $n = 20$ content is
known only via secondary sources); (2) reconstruct the $k = 5$ proof with a computer-checked
case analysis; (3) measure how the case count scales $k = 5 \to 6$; (4) attempt $k = 7$ only if
the scaling permits.

**Why this n.** A proof would be the first optimality result in the 22–34 band and would
progress a named conjecture; even step (2) alone would upgrade the repo's understanding of the
only modern lower-bound technique beyond Oler's inequality.

**Kill-criterion.** (a) If step (1) shows Payan's argument is ad hoc per-$k$ with no mechanisable
skeleton, stop after writing up what the method actually is (that write-up is a deliverable —
it feeds #17). (b) If the measured case growth $k=5 \to 6$ extrapolates to an infeasible count
at $k = 7$ (estimate before launching anything), stop. (c) If a citation search on Payan 1997
turns up an existing $k \ge 7$ attempt or proof, defer to the literature.

**Cost.** Literature-heavy start (cheap), then medium. Sequenced so every stage yields a
standalone write-up.

**Reuse.** #17 (Oler) is the natural companion; the exact checker verifies any constructions
used in the case analysis.

**Literature status.** Conjecture and $k \le 6$ proofs: cited. $k = 7$ status: no attempt found
in a shallow search — needs the citation sweep in step (1). A 2024/2025 preprint claiming a
general Erdős–Oler proof exists on ResearchGate (found 2026-08-17, apparently not
peer-reviewed); step (1) must assess it, but per repo norms an unreviewed preprint settles
nothing and, if it *were* right, would make this whole attack moot — check first.

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

**The idea — pure speculation.** Oler's inequality is tight exactly at triangular $n$; at
$n = \Delta(k) - j$ for small $j$ it undershoots the truth. Every proven near-triangular case
($n = 5, 9, 14, 20$) and all seven Graham–Lubachevsky conjectured families are lattice packings
with structured vacancies (G–L 1995, cited). Conjecture *shape* (not a claim): an inequality
of the form "$n$ points at distance $\ge 2$ in a triangle of side $d$ imply the Oler bound
minus a correction term $f(j)$ that vanishes as the vacancy structure degenerates" — informally,
removing $j$ points from the lattice can only buy a bounded, quantifiable amount of side length.
Even a crude such inequality would be the first *general-purpose* lower-bound tool beyond Oler
and would bite exactly on the near-triangular open cases $n = 25, 26, 27$ and the G–L families.

**Concrete first step (one day, numeric only).** Compute the slack of Oler's inequality — and
of the Folkman–Graham refinement (*A packing inequality for compact convex subsets of the
plane*, Canad. Math. Bull. 1969; existence cited, statement not yet pulled — do this via #17) —
at the *proven* values for $n = 5, 9, 14, 20$. The pattern of slacks either suggests a
correction-term shape or shows there is no usable pattern.

**Kill-criterion.** If no candidate correction term reproduces the proven case $n = 20$
(i.e., every attempted $f$ either fails soundness on triangular $n$ or gives a bound weaker
than plain Oler at $n = 20$), abandon after the calibration computation and write up the slack
table as a refutation-grade note. Hard cap: two sessions before either a precise conjectured
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
   bound for an open $n$, and the only approach whose output is plausibly `verified:lean`.
   Its calibration step is fast and decisive in either direction. → **filed as issue #27.**
2. **A — interval branch-and-bound for $n = 16$.** The only approach with a literature-proven
   record of actually *closing* container cases of this difficulty (the square programme). Heavy,
   but incremental, checkpointable, and parallelisable. → **filed as issue #28.**
3. **D — Erdős–Oler $k = 7$.** Sharpest target in the open band; gated cleanly on a cheap
   literature step that is valuable on its own. → **filed as issue #29.**
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
- Web searches 2026-08-17 confirming $n = 16\text{–}19$ remain open and finding no
  triangle-container interval-B&B or SDP attempt. Absence of evidence from a search is weak —
  each filed attack repeats its own literature step as stage zero.
