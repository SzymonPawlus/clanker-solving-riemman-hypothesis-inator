# Ideation round 2 — candidate attacks against ground that shifted, each with a kill-criterion, triaged

```
regularity budget: not applicable to the file as a whole — this file proves nothing and
nothing in it is assumable. Each idea carries its own provisional budget inline. Every
mathematical statement below is speculation or `sketch` at best, and is labelled so.
```

- Lane: **ideation, round 2** (divergent lane per [`../../../../RULES.md`](../../../../RULES.md)
  §8 — wrong ideas are cheap here and get filtered downstream).
- Author: `claude` (Fable 5, per the §8 model-selection table), 2026-08-30, branch
  `claude/inscribe-equilateral-triangle-oj15x1`. Issue linkage is the dispatcher's to record.
- Journal, including the ideas discarded *before* write-up and the derivation scratch:
  [`../../../../notebook/claude/2026-08-30-iet-ideation2.md`](../../../../notebook/claude/2026-08-30-iet-ideation2.md).
- Predecessor: [`../ideation-round-1/README.md`](../ideation-round-1/README.md). **Nothing from
  its thirteen ideas is re-proposed here**, including the six it left unexecuted
  (I4, I7, I8, I9, I10, I11); where a round-2 idea is adjacent to one of those, the
  adjacency and the difference are stated inline.
- Inputs read in full: [`../rectifiable-case/`](../rectifiable-case/README.md),
  [`../spiral-tip-witness/`](../spiral-tip-witness/README.md),
  [`../exceptional-set-polygons/`](../exceptional-set-polygons/README.md),
  [`../exceptional-pair-rigidity/`](../exceptional-pair-rigidity/README.md),
  [`../half-density-obstruction/`](../half-density-obstruction/README.md),
  [`../extremal-size/`](../extremal-size/README.md), [`../scalene-shapes/`](../scalene-shapes/README.md),
  [`../polygon-count-closure/`](../polygon-count-closure/README.md),
  [`../round3-cross-review/`](../round3-cross-review/README.md), [`../../README.md`](../../README.md),
  [`../../RULES.md`](../../RULES.md), repo [`RULES.md`](../../../../RULES.md).
- **This file starts no work.** It proposes; a future claimed issue per idea does the work.

**Ceded territory — eight lanes are running now and none of the following is proposed here:**
classifying non-wedge exceptional points (what the family $\{\Theta(r)\}_r$ can look like);
proving that no such classification exists; proving $\lvert E(P)\rvert \le 2$ for polygons
(the [`exceptional-set-polygons`](../exceptional-set-polygons/README.md) §8.6 target); hunting
three (or more) exceptional points on one Jordan curve; closing the convex extremal bracket
$[1/\sqrt3, \sqrt3/2]$; breaking it; the exact maximiser tool. Where an idea below brushes one
of these, the boundary is stated and the deep half is explicitly left to the running lane.

**Format.** Every idea carries the five fields this round's brief requires:

1. **Idea** — concrete enough to start tomorrow.
2. **Kill** — the observation that would make us abandon it
   ([`../../../../RULES.md`](../../../../RULES.md) §6.2; met ⇒ stop, mark `refuted`).
3. **Known?** — honest guess whether it is already in the unread literature, and whether that
   matters. (No scholarly host was reachable in any session so far; every guess is
   provenance-free.)
4. **Square test** ([`../../RULES.md`](../../RULES.md) §3.2) — run verbatim with $90°$ for
   $60°$: if it would prove the square peg problem, it is wrong.
5. **If it fails** — what the failure would teach, stated in advance. Round 1's top-ranked idea
   failed to teach ("incomparable and vacuous exactly where it mattered"); its second-ranked
   idea over-delivered. This field exists so that round 2 is ranked by that lesson.

Notation is the repo's: $J$ a Jordan curve with interior $\Omega$, $E(J)$ the exceptional set,
$\rho_{O,\theta}$ rotation by $\theta$ about $O$, $\sigma_\mu(z) = O + \mu(z - O)$ the spiral
similarity with multiplier $\mu \in \mathbb{C}^\times$, $\Theta_S(r)$ the direction set of $S$
at radius $r$ about $O$, and Observation R / Lemma R the six-times-re-derived (still `sketch`)
criterion: $O$ good $\iff J \cap \rho_{O,60°}(J) \supsetneq \{O\}$ $\iff$ some circle about $O$
carries two points of $J$ exactly $60°$ apart.

---

## The ideas

### II1. The apex spectrum $A(O)$ and the multiplier spectrum $M(O)$: "1 is never isolated"

**Idea.** Stop asking only about $60°$. For $O \in J$ define

$$A(O) \;=\; \{\alpha \in (0°,180°) : O \text{ is the apex of an inscribed isosceles triangle
of apex angle } \alpha\}, $$
$$M(O) \;=\; \{\mu \in \mathbb{C}^\times \setminus \{1\} : J \cap \sigma_\mu(J) \supsetneq \{O\}\},$$

so that $O \in E(J) \iff 60° \notin A(O)$, and $M(O)$ restricted to the unit circle is $A(O)$
(both orientations). This one object organises what three finished lanes computed separately:
the spiral tip has $A(O) = (0°, \beta]$ **exactly** (`spiral-tip-witness` Corollary 5) and
$M(O) = \{\mu : |\arg\mu + (\ln|\mu|)/c| \le \beta\}$, a log-spiral band
(`scalene-shapes` Theorem 5); a wedge point of opening $w$ has $A(O) \subseteq (0°, w]$; a
unit-speed differentiability point of a rectifiable curve has $A(O) \supseteq (0°, 120°]$
(`rectifiable-case` §9.2, the general-$\alpha$ run of Theorem T).

The first deliverable is a theorem, not a survey. *Speculative claim, with the proof route
stated so it can be attacked:*

> **Small-apex theorem (speculative).** For every Jordan curve $J$ there is $\alpha_0(J) > 0$
> such that **every** $O \in J$ is the apex of an inscribed isosceles triangle of apex angle
> $\alpha$, for **every** $\alpha \in (0°, \alpha_0)$. In particular no point of any Jordan
> curve is "totally exceptional": every point is a vertex of inscribed triangles of some
> shapes.

*Route:* $\lambda(\Omega \cap \rho_{O,\alpha}\Omega) \to \lambda(\Omega) > 0$ as $\alpha \to 0$,
uniformly in $O \in J$ (the displacement of $\rho_{O,\alpha}$ on $\overline\Omega$ is at most
$\alpha_{\mathrm{rad}} \cdot \operatorname{diam}\overline\Omega$, and
$\lambda(\Omega \,\Delta\, \tau\Omega) \to 0$ uniformly over isometries $\tau$ with sup-displacement
$\to 0$ — standard $L^1$-continuity of the indicator). A nonempty open overlap
$\Omega \cap \rho\Omega$ plus the region lemma's contrapositive (Lemma A / Lemma 3, `sketch` in
three lanes, to be re-derived in-lane) gives $J \cap \rho_\alpha(J) \supsetneq \{O\}$, i.e.
$\alpha \in A(O)$. Derivation scratch in the journal. Note the contrast that makes this worth
stating: at $60°$ the same overlap statement is **false at up to two points**; the theorem
locates exactly what is special about $60°$ — not the mechanism (which works at every angle) but
the fact that $60°$ need not be below $\alpha_0$.

Then the structure questions, which are the lane's actual subject: is $A(O)$ always an interval?
(The spiral says it can be one; no witness says it must be.) Is it $F_\sigma$ but not closed
(collapse of witnesses — the $\delta$-noncollapsed part $A_\delta(O)$ *is* closed)? What is the
invariant $\alpha_0(O) = \sup\{\alpha : (0,\alpha) \subseteq A(O)\}$ on the known witnesses —
spiral: $\beta$; $30°$ apex: is it $30°$ exactly? Is $1$ interior to $M(O) \cup \{1\}$ in
$\mathbb{C}^\times$ (true at the spiral tip, where the band is a 2-dimensional neighbourhood of
$1$), or can the shrinking-nesting alternative of `scalene-shapes` Lemma A$_\sigma$ block
multipliers arbitrarily close to $1$ off the unit circle? All of this is exactly computable on
polygons for angles with rational cosine, and the $60°$ deciders generalise.

Provisional budget: **Jordan** for the theorem (region lemma); **none** for the definitions and
for everything downstream of an explicit witness.

Adjacency note: this is *not* round 1's I7 (modulus of goodness = triangle **size** at one
angle) and not I8 (orientations of equilateral triangles). It is the angle/multiplier axis,
which no round-1 idea and no finished lane owns; `scalene-shapes` §11.3 explicitly leaves the
per-point spectrum unstudied.

**Kill.** (a) The measure-continuity or region-lemma step of the small-apex theorem has an
unfixable gap — this would be *important* (it would mean the Lemma A dichotomy is less stable
than five lanes believe) and must be written up as the finding. (b) A polygon census shows
$A(O)$ is always simply $(0°, \theta_{\max}(O)]$ with $\theta_{\max}$ the obvious geometric
quantity — then the invariant is boring, the theorem survives as a two-line remark, and the
lane stops there. (c) Uniformity of $\alpha_0$ fails — again a finding (a curve where the
realisable apex angle degenerates along the curve), not a loss.

**Known?** Nielsen (1992, `cited`\*, unread) gives every *shape* somewhere on the curve —
a different quantifier order from every *point* for some shapes. The Kronheimers' "tripos
problem" (1981, unread) is the likeliest home for a per-point statement. Guess: the small-apex
theorem is folklore-or-known at ~65%; the spectrum $A(O)$/$M(O)$ as an object of study, with
$\alpha_0$ as an invariant, ~20% known. Even if known, an in-repo self-contained proof is
assumable-track material and directly reusable by the running classification lanes.

**Square test.** With $90°$: the theorem's output at angle $90°$ (when $90° < \alpha_0$, which
need not hold) is an inscribed isosceles **right** triangle; the fourth corner of the would-be
square is determined and unconstrained — the same non-transfer as `rectifiable-case` §9.2. The
spectrum contains $90°$ sometimes and that closes nothing. Pass.

**If it fails.** Failure mode (a) teaches that the repo's most-reused lemma has a stability
gap; (b) teaches that the angle axis carries no structure beyond the wedge data, which would
itself simplify the classification lanes' problem. Both failures leave residue.

### II2. The density-point criterion: wild curves are easy, and it is Lean-shaped

**Idea.** Every positive criterion in the repo (sector, convex cone, Theorem T) consumes
regularity. Here is one that consumes *anti*-regularity, with a two-line proof and **no
topology at all**. *Speculative lemma, proof route inline:*

> **Density-point lemma (speculative).** Let $S \subseteq \mathbb{R}^2$ be measurable,
> $O \in S$, and suppose **some** ball $B = B(O,r)$ has $\lambda(S \cap B) > \tfrac12 \lambda(B)$
> — in particular this holds whenever $O$ is a Lebesgue density point of $S$. Then $O$ is a
> vertex of a nondegenerate equilateral triangle with all vertices in $S$.

*Route:* $\rho = \rho_{O,60°}$ preserves $B$ and $\lambda$, so $\lambda(S \cap B) +
\lambda(\rho(S) \cap B) - \lambda(B) > 0$ forces $\lambda(S \cap \rho(S) \cap B) > 0$; a set of
positive measure contains a point $\ne O$; Lemma R closes. **Corollary:** for a Jordan curve
$J$ with $\lambda_2(J) > 0$ (Osgood-type curves — *recalled attribution, Osgood 1903, flagged
unverified per [`../../RULES.md`](../../RULES.md) §6.1, a search target not a citation*), the
Lebesgue density theorem makes $\lambda_2$-almost every point of $J$ a density point, hence a
vertex. So: rectifiable curves have $E(J)$ $\mathcal{H}^1$-null (Theorem T, `sketch`);
positive-area curves have $E(J)$ $\lambda_2$-null within $J$. The two ends of the regularity
spectrum are now both covered by null-statements, by completely different mechanisms, and the
middle (dimension strictly between 1 and 2) is exposed as the open band — see II9.

Why this ranks despite its size: it is the **most Lean-shaped positive statement anyone has
proposed here**. It quantifies over a measurable set — no Jordan curve theorem, no curve at
all — and its ingredients (rotation-invariance of $\lambda$, inclusion–exclusion, the Lebesgue
density theorem, Lemma R's law-of-cosines computation) are all plausibly in Mathlib
(*recollection, to be verified against the pinned toolchain per
[`../../RULES.md`](../../RULES.md) §6.3 — the density theorem via Besicovitch covering is
believed present; the angle API is confirmed present by that section*). A `verified:lean`
statement of the form "density points of any planar set are equilateral-triangle vertices"
would be the first machine-checked positive vertex statement in this problem.

Provisional budget: **none** (measurable set); the corollary adds "Jordan with positive area"
only to name a curve class it applies to.

**Kill.** (a) An error in the two-line route (checked twice in the journal; the risk is small
but the file must be attackable). (b) No in-repo-constructible witness: building an Osgood
curve to this repo's exactness standard is itself a JCT-flavoured project, so if the corollary
cannot be instantiated the write-up is honest about being conditional on the curve class being
nonempty (literature-dependent). That demotes but does not kill: the lemma itself needs no
witness. (c) Lean infrastructure still unreachable (see II6) — then the Lean half parks and
the mathematical half is a one-page `sketch`, which is a thin lane; if (b) and (c) both fire,
fold into II6 rather than running alone.

**Known?** As mathematics, if Meyerson's $\lvert E(J)\rvert \le 2$ is right then this is
vacuous for curves (all but two points are good anyway); as a statement about arbitrary
measurable sets it is surely folklore-level, unwritten because trivial. ~90% "known or would
bore an expert". That is fine: its value is *in-repo and formal* — a topology-free, assumable-
track base per [`../../../../RULES.md`](../../../../RULES.md) §3's "prefer to formalise the
base of a chain".

**Square test.** With $90°$: density points are apexes of inscribed isosceles right triangles.
Fourth vertex unconstrained; no square. (And with all four rotations $90°, 180°, 270°$
simultaneously: density $> 3/4$ in a ball gives a point whose full 4-orbit lies in $S$ — which
*would* give a square! Checked: that is a statement about sets of density $> 3/4$, satisfied by
no curve of measure zero and by no Jordan curve known to be relevant to the square peg problem,
whose difficulty lives at measure zero. Recorded in the journal so nobody mistakes it for
progress; it proves the square peg statement only for sets so fat the problem is trivial.)
Pass, with the near-miss documented.

**If it fails.** It essentially cannot fail mathematically; it can only fail to matter. The
informative failure is (c)/(b): it would establish that even the most Lean-shaped statement
available cannot currently be formalised in this environment, which is a fact the dispatcher
should know before commissioning any Lean work.

### II3. Connectivity is the load-bearing hypothesis: unbounded $E$ for disconnected sets, and the figure-eight gap

**Idea.** In-repo, nothing yet says *which hypothesis* makes $\lvert E \rvert \le 2$ possible.
Sharpen that with three graded targets.

*(i) Bankable immediately (speculative, derivation in the journal).* For the disjoint union of
$n$ copies of the $30$–$30$–$120$ triangle boundary, scaled to diameter $1$ and placed at
mutual distances $\ge 9$ along a line (e.g. centres at $x = 10^k$), **all $2n$ sharp apexes are
exceptional**: from any apex, its own triangle occupies radii $(0,1]$ with angular spread
$30°$, and every other triangle occupies a radius interval disjoint from $(0,1]$ and from the
others, with angular spread $< 2°$; no circle ever carries two points $60°$ apart. So
$\lvert E \rvert$ is **unbounded over disjoint unions of Jordan curves**, and with a convergent
sequence of components, infinite. Two consequences worth having on record: any proof of any
finite bound **must consume connectedness** (not just "closed curve locally"); and the
rotating-wedge mechanism is trivially realisable with *discontinuous* radial arcs $I_r$ once
connectivity is dropped — so what connectivity buys is precisely the no-sweep continuity that
`exceptional-set-polygons` Proposition 5 extracts. This is a finitely-checkable exact
computation (the committed deciders work on any union of segments; simplicity is never used by
the criterion).

*(ii) The figure-eight gap.* For a figure-eight $J_1 \vee J_2$ (two Jordan curves sharing one
point) the union is connected, $(\dagger)$-style radial nonemptiness returns, and the trivial
bounds are $\lvert E(J_1 \vee J_2)\rvert \le \lvert E(J_1)\rvert + \lvert E(J_2)\rvert$
(a point of $J_1$ exceptional in the union is exceptional in $J_1$) — i.e. $\le 4$ modulo the
unread Meyerson bound, and $\le$ whatever the in-repo polygon lanes eventually prove. **What is
the true maximum: 2, 3, or 4?** Note the cheap route to 4 is *pre-refuted*: `exceptional-set-polygons`
Theorem 2 is a statement about arbitrary point sets, so at most two points of the union can be
wedge-type — three-plus exceptional points on a figure-eight would need the channel mechanism,
under the no-sweep constraint, in a connected set. An exact search over two-triangle and
two-channel bouquets is a few sessions with the existing decider technology. (See D2 below for
the naive four-wedge-tip bowtie, killed at proposal time by Theorem 2 — an instructive death.)

*(iii) The hierarchy.* Segments and sub-$60°$ arcs: $E$ = everything (connected, so
connectedness alone gives nothing). Figure-eights: unknown, in $[2,4]$. Jordan: reportedly 2.
The question "where between *continuum without endpoints* and *Jordan* does the finite bound
switch on" is a precise frontier question that none of the running lanes owns, and every
data point constrains what a proof of the polygon bound can look like.

Provisional budget: **none** for (i) (point sets, exact arithmetic); **none** for (ii)'s
searches; any eventual figure-eight theorem would need whatever replaces the region lemma when
the complement has three components — which is itself an interesting sub-question (the JCT
machinery does not die, it *triples*).

Adjacency note: not I11 (dendrites/triods — Meyerson's home turf, unexecuted and still
banned); the objects here are unions of closed curves, where the existence theorem is not in
doubt and only the *count* is at stake.

**Kill.** (a) The exact check of (i) fails — i.e. some far pair does land $60°$ apart on a
common circle; the construction has free parameters (spacings, scales) and one repair round is
allowed, after which fail = `refuted` and the write-up says why the radial-separation intuition
is wrong. (b) For (ii): two sessions of exact search plus one of hand-construction produce
neither a 3-example nor an interference lemma — park with the census recorded. (c) A running
lane's output (the $\lvert E(P)\rvert \le 2$ lane or the three-point hunt) subsumes the
figure-eight question — cede immediately; (i) survives regardless.

**Known?** Meyerson's title is "Equilateral triangles and **continuous curves**", and a
figure-eight *is* a continuous closed curve, so (ii) may be answered inside the very paper this
project cannot read — the README's open item 3 already flags that title as the cheapest
verification win. Guess: (ii) ~50% answered there; (i) ~5% written down anywhere (too easy),
yet it is exactly the kind of hypothesis-isolating remark this repo exists to record.

**Square test.** With $90°$: disconnected unions give unboundedly many $90°$-blocked points by
the same radial separation — a statement about isosceles right apexes, producing no square.
The figure-eight count question does not parse for squares (no existence theorem to refine).
Pass.

**If it fails.** (a) failing would reveal a real error in the repo's shared mental model of
the per-circle criterion — worth more than the construction. (b) failing still leaves (i)
banked and the bounds of (iii) recorded, which is the map the count lanes need.

### II4. $\mathbb{R}^3$: the metric half of Theorem T survives, the topological half dies — which one was doing the work?

**Idea.** For a Jordan curve $J \subset \mathbb{R}^3$ (no planarity), Lemma R survives
verbatim on spheres: $O$ is a vertex iff some sphere about $O$ carries two points of $J$ at
spherical angle exactly $60°$. The wedge test survives (cone of angular radius $< 30°$), and so
does the wedge count — three wedge-type points still span a Euclidean *plane* triangle with
angle sum $180°$, so **at most two wedge-type points in any dimension** (one-line extension of
`exceptional-set-polygons` Theorem 2; journal). What does *not* survive is everything built on
the Jordan curve theorem: no interior, no region lemma, no half-density chain, no Theorem T
endgame. Meanwhile Theorem T's *metric* half — localisation (Lemma 1), the $\tfrac83\rho$
length bound, the thin-annulus two-point count (Lemma 2) — is dimension-free. So in
$\mathbb{R}^3$, at a unit-speed differentiability point, most small spheres meet $J$ in
**exactly two nearly-antipodal points** … and then nothing forces a $60°$ pair, because the
planar proof's next move was the interior arc. Two concrete deliverables:

- *(a) A cheap witness to bank (speculative, construction in the journal).* A conical
  log-spiral: arm $\{r(t)(\sin\varphi\cos\theta(t), \sin\varphi\sin\theta(t), \cos\varphi)\}$
  winding into $O$ on a cone of half-angle $\varphi = 30°$, closed by a return path routed in a
  thin tube along the cone's **axis** — in $\mathbb{R}^3$ the return does not have to spiral
  (no separation), which was the entire difficulty of the planar witness. Every sphere about
  $O$ meets: the arm once (direction at angle $30°$ from the axis), the return tube in
  directions within $\varepsilon$ of the axis. All same-radius pairs subtend $\approx 30°$ or
  $< 2\varepsilon$ — never $60°$. If the closing bookkeeping holds, this is a **rectifiable
  Jordan curve in $\mathbb{R}^3$ with an exceptional point**, by a construction dramatically
  simpler than the planar one — evidence that exceptionality is *easier* in space, as the
  criterion's codimension count suggests.
- *(b) The real question.* Does unit-speed differentiability still force vertexhood in
  $\mathbb{R}^3$ — is there a **$C^1$ (or smooth) space curve with an exceptional point**? If
  yes, Theorem T is revealed as genuinely topological (the plane was doing the work); if no,
  the proof of the $\mathbb{R}^3$ statement would have to invent a JCT-free mechanism, which
  would be the most transplantable object this problem has produced. Start numerically on
  knot parametrisations; the failure of the two-branch angle to sweep through $60°$ as $r$
  grows is the thing to hunt for.

Provisional budget: (a) explicit-witness, rectifiable-as-conclusion; (b) rectifiable +
differentiability at one point, in $\mathbb{R}^n$.

**Kill.** (a)'s closing bookkeeping fails after one repair round — write up why the tube
interferes; (b): two focused worktree-days with neither a proof mechanism nor a candidate
curve that survives numerics — park with the partial census. Rescope both to reconstruction if
Gupta & Rubinstein-Salzedo (arXiv:2102.03953, `cited`\*, unread — their abstract reportedly
gives "a condition under which a given point of $J \subset \mathbb{R}^n$ is a vertex") becomes
readable and answers them.

**Known?** Highest overlap risk in this file: GRS is *about* exactly this. Guess ~60% that (b)
or its answer is in or near that paper; (a) ~40%. The README's open item 1 rests entirely on
that paper's unread scope, so even a reconstruction-grade in-repo answer has value: it would
tell the literature lane exactly what to look for.

**Square test.** With $90°$ in $\mathbb{R}^3$: blocked/realised isosceles right apexes on
space curves; the square peg problem is planar and four-point, and nothing here closes a
fourth vertex. (Squares *inscribed in space curves* is a different known question this file
takes no position on.) Pass.

**If it fails.** Even total failure of (b) after honest effort produces the precise statement
"the planar proof's topological half has no known substitute in $\mathbb{R}^3$", which is the
right shape of hand-off to a literature session.

### II5. The topology of goodness: robust versus grazing witnesses, and whether $E(J)$ is closed

**Idea.** Split good points by *how* they are good: $O$ is **robustly good** if
$\Omega \cap \rho_{O,60°}(\Omega) \ne \emptyset$ (open regions overlap), and **grazing** if it
is good but all contact is boundary-only ($\overline\Omega \cap \rho\overline\Omega \supsetneq
\{O\}$ while the open overlap is empty). The master iff of `half-density-obstruction` §5.1
(`sketch`, re-derive in-lane) says good = robust ∪ grazing. *Speculative but short:* robust
goodness is an **open** condition in $O$ — if $x \in \Omega \cap \rho_{O}(\Omega)$ with
$\rho_O^{-1}(x) \in \Omega$, then for $O'$ near $O$ (anywhere in the plane, not just on $J$)
the same two open membership conditions persist. Hence exceptional points can accumulate
**only at grazing points**, i.e. $E(J) \cup \mathrm{Graze}(J)$ is closed. The lane then:

- exhibits grazing points exactly — first candidate already in hand: each corner of the
  equilateral triangle itself is grazing (the rotated triangle occupies the adjacent $60°$
  cone; interiors disjoint; $J \cap \rho J$ is a whole shared edge — exact, journal), and the
  exactly-$60°$ convex vertices that `experiments/inscribed-triangle-polygons/` resolved good
  are the natural family to test;
- makes "grazing" decidable in the polygon deciders (all witnesses on $J \cap \rho J$ with
  empty open overlap — a finite exact check) and censuses how common it is;
- and asks the honest open question: **is $E(J)$ closed for every Jordan curve?**
  Equivalently, can exceptional points accumulate at a grazing point? Under the unread
  Meyerson bound this is vacuous (finite sets are closed); unconditionally and in-repo it is
  open, and a "no" would need infinitely many exceptional points — which is the running
  three-point-hunt lane's territory escalated, so this lane states the reduction and **stops
  there**, leaving the hunt where it belongs.

Provisional budget: **Jordan** (the master iff); the openness argument itself is two lines of
point-set topology on top of it; the censuses are polygonal and exact.

**Kill.** (a) The openness argument breaks — must be understood, because half the repo
implicitly treats open overlap as stable. (b) Polygons turn out to have no grazing points
except trivial symmetric coincidences (census empty) — record and retreat to the general-curve
statement only; the lane shrinks to a half-page. (c) The running classification lanes' output
covers the robust/grazing split — cede.

**Known?** The robust/grazing distinction is the kind of thing Schwartz's "topological
information" enhancement (arXiv:1908.08174, `cited`\*, unread) plausibly contains in some
form (~35%). The convex lane's Theorem B(ii) boundary case is exactly a grazing statement for
convex curves, so in-repo this is the general-curve extension of an existing two-sided
subtlety, which is why I believe it is well-posed.

**Square test.** With $90°$: robust/grazing splits the isosceles-right-apex property; open-ness
of robust apexhood says nothing about a fourth vertex. Pass.

**If it fails.** (a)'s failure would be a repo-wide alarm about stability arguments; (b)'s
failure would say goodness on polygons is always robust, itself a usable lemma (it would make
the polygon good-set open, hence $E(P)$ closed, for free).

### II6. The Lean-able layer, bundled: formalise the topology-free corpus while the JCT gap stands

**Idea.** The problem now has a substantial corpus of statements whose budgets are literally
**none** — they quantify over bare point sets or measurable sets: Lemma R (six derivations);
the wedge test; the wedge count (`exceptional-set-polygons` Theorem 2); the rotating-wedge
lemma and the spiral-tip Theorem 1 *in its set form* (the version `spiral-tip-witness` §12.4
itself nominates: no Jordan word, monotonicity of $\exp$ plus arithmetic); the no-sweep
Proposition 5; W0/W1/W2 (`exceptional-pair-rigidity`); the scalene multiplier criterion
(Proposition 1) and Lemma 2; the $C_6$ half-density core (`half-density-obstruction` §3.5's own
nominated target); the partition inequality (rectifiable §5, Sub-lemma 2a); Lemma 0; and from
this round, II2's density-point lemma and the three-fold-symmetry one-liner (journal: a curve
invariant under rotation by $120°$ about $c$ has every point $O \ne c$ good, witness
$\{O, \rho_{c,120°}O, \rho_{c,240°}O\}$ — topology-free, two lines). One campaign, smallest
first, one issue per statement, so that every later `verified:review` use of these is free
([`../../../../RULES.md`](../../../../RULES.md) §3: formalise the base of the chain). The
deliverable that matters most: a machine-checked "**the $30$–$30$–$120$ triangle boundary has
at least two exceptional points, and no planar set has three wedge-type points**" — sharpness
of the reported Meyerson bound, verified at `verified:lean` strength with zero dependence on
the unread paper *or* on the Jordan curve theorem.

Provisional budget: none (that is the selection criterion).

**Kill.** (a) **The known infrastructure blocker**: two lanes independently record that `elan`
cannot be installed through the egress proxy. One honest session against the pinned toolchain;
if the container still cannot build, park the whole campaign with the blocker documented and
tell the dispatcher — that information gates every Lean plan in this problem. (b) A per-item
API audit shows a statement needs Mathlib surface that is absent (e.g. circle-arc measure for
the $C_6$ argument) — drop that item, keep the rest; the campaign is severable by design.

**Known?** As mathematics, all of it is elementary and most is presumably folklore; as
formalisation it is ~95% novel (Mathlib's own index records no Jordan curve theorem and
nothing near this problem). Novelty is not the point; §3-grade assumability is.

**Square test.** Everything here is either an obstruction (wrong polarity for existence) or an
isosceles producer. One genuinely informative non-transfer to record in the formalisation
itself: the wedge count's angle-sum proof needs three angles each $< \varphi$ to sum below
$180°$, which forces $\varphi \le 60°$ — at $\varphi = 90°$ there is no contradiction and
three $90°$-blocked points genuinely exist (the corners of an equilateral triangle, each of
opening $60° < 90°$). The bound "two" is special to $60° = 180°/3$; the $90°$ analogue of the
count is simply false. Formalising that contrast is the cleanest available answer to "why does
this not transfer". Pass.

**If it fails.** Failure mode (a) is pure information and costs one session; (b) prunes
itemwise. There is no outcome in which the campaign misleads.

### II7. An invariant separating the three mechanisms: the wedge scale $\varepsilon_w(O)$

**Idea.** The brief asks for an invariant separating the known exceptional mechanisms. The
cheapest candidate that is well-defined with no classification theory: for $O \in E(J)$,

$$\varepsilon_w(O) \;=\; \sup\{\varepsilon \in (0,\infty] : \text{the directions from } O
\text{ of } J \cap B(O,\varepsilon)\setminus\{O\} \text{ lie in a closed arc of length}< 60°\}.$$

Then: global wedge points have $\varepsilon_w = \infty$; the 17-vertex polygonal channel tip
has $\varepsilon_w \in (0,\infty)$ (locally a sub-$60°$ vertex, globally spread $258°$); the
spiral tip has $\varepsilon_w = 0$ (full direction set at every scale). Three mechanisms,
three regimes of one scalar. Deliverables: compute $\varepsilon_w$ exactly on the rigidity
census's $327$ non-wedge-blocked exceptional points (is $\varepsilon_w > 0$ always on
polygons? — should follow from `exceptional-set-polygons` Theorem 1, every exceptional point
being a sub-$60°$ vertex, so yes, and the *distribution* of $\varepsilon_w$ against the
channel data is the new content); and pose, without attacking, the boundary question
"$\varepsilon_w = 0$ ⟹ what?" — **which belongs to the running classification lanes and is
explicitly not proposed here.** This idea is only the instrument: a scalar every lane can
report, so that witnesses become comparable across lanes.

Provisional budget: none (definition over point sets); polygonal for the census.

**Kill.** (a) The classification lanes' output makes the invariant redundant — cede on sight.
(b) The census shows $\varepsilon_w$ carries no information beyond the interior angle on
polygons — record and stop; the definition survives as vocabulary at zero cost.

**Known?** As a definition, ~70% novel (it is the localised wedge test, which anyone could
write; nobody in-repo or in any seen snippet has). Low stakes either way.

**Square test.** $\varepsilon_w$ at $90°$ classifies right-isosceles blockings; no square is
produced or excluded. Pass.

**If it fails.** Its failure is cheap and diagnostic: it would say mechanism-separation needs
more than one scale, which itself constrains what a classification can look like.

### II8. How close can two exceptional points be?

**Idea.** `exceptional-pair-rigidity` proved (sketch) that *wedge-type* pairs realise the
diameter exactly, refuted the extension to general pairs with exact witnesses down to
$\lvert O_1O_2\rvert/\operatorname{diam} = 0.7241$, and stopped. The inverse extremal
question is open in-repo and unclaimed: is
$\inf \{\lvert O_1O_2\rvert/\operatorname{diam}(J) : \lvert E(J)\rvert = 2\}$ **zero or
positive**? A positive infimum would be a new universal constant of the problem ("exceptional
points repel"); zero would want a family of curves with two nearby exceptional points, for
which the natural candidates are now available: two polygonal channels (17-gon style) sharing
most of their length, or a spiral tip adjacent to a sharp corner (the $c=1$ spiral witness
already shows a mixed pair numerically, at unknown separation). Joint half-density at two
nearby points — two density-$\le\tfrac12$-at-every-scale points with overlapping balls — is
the one tool with a chance at a lower bound, and its failure mode is already understood
(`half-density` §3.3: no packing inequality between different rotates), so the attempt is
cheap to run and cheap to abandon.

Provisional budget: polygonal for constructions; Jordan for any bound.

**Kill.** (a) A construction session drives the ratio below $0.1$ — then the answer is
almost certainly $0$; finish the family, write it up, done. (b) Neither the constructions nor
the joint-density bound move in two sessions — park with the census. Coordinate with the
running three-point-hunt lane before starting: their constructions and these overlap in
technique, and if they produce nearby pairs en route, this question inherits the answer free.

**Known?** No seen snippet says anything about *where* the two points sit (round 1's I5 asked
the rigidity question; this is its extremal remainder, which the executing lane explicitly did
not claim). ~70% novel as a question.

**Square test.** Pairs of $90°$-blocked points at small separation: a well-posed different
question, no square produced. Pass.

**If it fails.** Both outcomes of (a) are results; (b) leaves a census that the pair-rigidity
file lacks.

### II9. The middle of the dimension spectrum: $E$ of a self-similar (Koch-type) curve

**Idea.** Theorem T covers dimension 1 ($\mathcal{H}^1$-null $E$); II2 covers dimension 2
($\lambda_2$-null). Nothing covers $1 < \dim < 2$. The Koch snowflake is the tractable
entry: exact self-similarity means the direction sets $\Theta(r)$ at a corner satisfy an exact
renormalisation ($\Theta(r/3)$ at the same corner is $\Theta(r)$ rotated by the substitution
data), so "no $60°$ pair at any radius" becomes a finite fixed-point condition — plausibly
decidable exactly, in the same spirit as the spiral's Lemma 3 but with a discrete
renormalisation replacing monotonicity. Conjecture to test first (speculation): the snowflake
has $E = \emptyset$ — its uniform wiggliness should defeat both the wedge and the channel at
every point. A proof for the distinguished orbit points (corners of all generations) plus
numerics for generic points is a complete, self-contained lane.

Provisional budget: one explicit curve; the renormalisation argument, if it closes, is exact.

**Kill.** (a) One session fails to make $\Theta(r)$ computable through the self-similarity —
park; the curve is famous but the sections may be genuinely intractable. (b) A corner turns
out exceptional — not a kill but a headline (a fractal exceptional point with
$\varepsilon_w = 0$ and no winding — it would break the mechanism trichotomy of II7 and feed
the classification lanes a witness they cannot currently imagine).

**Known?** Specific-curve inscribed-figure analyses exist in the *square* literature
(recalled, unverified); for triangles-on-the-snowflake, no snippet seen. ~50% someone has done
it. Moderate stakes: mostly a testbed for whether renormalisation and the per-circle criterion
compose.

**Square test.** Squares inscribed in the snowflake is a known-flavoured separate problem this
lane must not touch; the $90°$ version of our machinery yields right-isosceles apex
statements only. Pass.

**If it fails.** (a)'s failure delimits the method: the per-circle criterion is only as usable
as the sections are computable, and the snowflake is the easiest hard case — a negative here
redirects all wild-curve hopes through measure (II2) rather than sections.

### II10. Uniform Theorem T: a modulus for $C^1$ curves, the bridge `extremal-size` asked for

**Idea.** `extremal-size` §8 proved that Theorem T yields **no** lower bound on the maximal
inscribed side $m(J)$, and its Theorem C covers convex bodies only. The gap between them: for
a **regular $C^1$** Jordan curve, Theorem T's hypothesis holds at *every* point with uniform
constants (uniform continuity of $\gamma'$ + a compactness "modulus of embeddedness" from
injectivity), so its proof should deliver $\inf_{O \in J} \sup\{\text{side at } O\} \ge
c(J) > 0$ with $c(J)$ explicit in the tangent modulus and the embeddedness modulus — a
per-point uniform quantitative statement, where the convex lane's is global and convex.
Deliverable: the statement with explicit constants, plus exact/numeric checks on smoothed
polygons. This is *not* round 1's I7 (rate of vanishing of $m$ near $E$ — banned) and not the
running extremal lanes (convex bracket); it is the quantitative content already sitting inside
the rectifiable lane's proof, never extracted.

Provisional budget: regular $C^1$ Jordan.

**Kill.** (a) The uniformisation genuinely needs more than $C^1$ (if the embeddedness modulus
interacts badly with the annulus argument, the honest outcome is "uniform on $C^{1,\alpha}$,
open at $C^1$" — still a result); (b) the running extremal lanes claim this corridor when
their briefs surface — check the board before claiming, cede if occupied.

**Known?** Quantitative refinements are the README's open item 4 ("not something this project
has sourced"). ~60% something equivalent exists in the smooth-curve literature. Low
originality, decent utility: it is the statement a future "how big is the guaranteed triangle
on a nice curve" reader will actually want.

**Square test.** At $90°$: uniform inscribed right-isosceles apexes on $C^1$ curves — for
squares one would need the fourth vertex, which nothing supplies; also the square peg problem
is *solved* for $C^1$ curves per the README's contrast row (`cited`\*, unread), so no
paradox either way. Pass.

**If it fails.** Failure mode (a) would locate exactly which regularity the uniformity
consumes — the kind of boundary this problem's `RULES.md` §1 exists to chart.

---

## Dead on arrival — recorded so round 3 does not regenerate them

### D1. The six-fold cover / quotient-group reformulation

**Idea (pre-refuted).** "Map the plane by angle-sixfolding about $O$ (or quotient directions by
$60°$); inscribed-triangle pairs become self-intersections of the image; import covering-space
machinery." Dies twice: (1) collapsing by the subgroup generated by $60°$ identifies
differences of $120°$ and $180°$ as well, so the image's self-intersections certify strictly
more than triangles — the criterion does not factor through any quotient; (2) what survives
factoring is exactly Observation R (one rotation, compared pointwise), already in six lanes.
**Kill: met at proposal time.** The salvageable germ — the $C_6$ fibre structure of the
per-circle criterion — is already `half-density-obstruction` §3.3's independent-set argument.
**Known?** The observation that it collapses is the content; nothing to attribute. **Square
test:** at $90°$ the quotient is $C_4$ and collapses the same way; nothing transfers.

### D2. Four wedge-blocked tips on a bowtie / far-pair of thin triangles

**Idea (pre-refuted, and the refutation is itself the useful part).** "Join or place two
$30$–$30$–$120$ triangles axis-to-axis so all four $30°$ apexes stay wedge-blocked in the
union; get $\lvert E\rvert = 4$ on a connected or two-component set *by wedges alone*."
Killed at proposal time by `exceptional-set-polygons` **Theorem 2, which is a statement about
arbitrary point sets**: three wedge-type points of *any* set form a triangle with all angles
$< 60°$, impossible. The journal shows the failure concretely: whichever way the second
triangle is placed, at least one tip's view of it leaves the $30°$ cone (in the worked
placement, spread at the back tip jumps to $\approx 90°$). This is what forced II3(i) through
the *radius-separation* route (disjoint radii, not narrow cones) — the construction that
survives is the one Theorem 2 does not see. **Kill: met.** **Square test:** the $90°$
angle-sum does not even forbid three $90°$-wedges (equilateral triangle corners), so the
transfer question inverts — recorded under II6's non-transfer note.

---

## Triage

| Idea | Verdict | One line |
|---|---|---|
| II1 apex/multiplier spectrum | **now** | A provable everywhere-theorem plus the organising invariant $\alpha_0(O)$; unifies three finished lanes' outputs; failure would itself be a repo-level alarm. |
| II3 connectivity & the count | **now** | Banks an exact unbounded-$E$ construction immediately; the figure-eight gap $[2,4]$ is sharp, cheap, and feeds the count lanes either way. |
| II2 density-point criterion | **now** | Two lines, topology-free, the most Lean-shaped positive statement in the problem; risk ≈ 0, upside = the first `verified:lean`-track vertex criterion. |
| II5 robust vs grazing goodness | **now** (4th) | Five-line openness theorem in hand, exact grazing witnesses already identified, honest stop-line at the running lanes' territory. |
| II4 $\mathbb{R}^3$ | later | Highest ceiling; do the cheap witness (a) first, gate (b) on a GRS literature check the moment any scholarly host answers. |
| II6 Lean layer | later (infra-gated) | The corpus is assembled and severable; one session decides whether `elan` can exist here at all — run that session before promising anything. |
| II8 pair separation | later | Real extremal remainder of the rigidity lane; coordinate with the three-point hunt first. |
| II10 uniform $C^1$ modulus | later | Extract the quantitative content of Theorem T; check the extremal lanes' briefs before claiming. |
| II7 wedge scale $\varepsilon_w$ | later (low) | Vocabulary plus one census; cede to the classification lanes on contact. |
| II9 Koch snowflake | later (low) | Beautiful if the renormalisation closes; park fast if it does not. |
| D1 six-fold cover | **DOA** | Collapses to Observation R; recorded to prevent regeneration. |
| D2 four wedge tips | **DOA** | Killed by the point-set wedge count at proposal time; its corpse routed II3 to the construction that works. |

## Ranked shortlist of 3

1. **II1 — the apex spectrum and the small-apex theorem.** The only idea in the file with a
   guaranteed nontrivial theorem *and* a new organising object. The theorem ("no point of any
   Jordan curve is totally exceptional; small apex angles are realised uniformly") is two known
   lemmas plus uniform measure-continuity, and every already-built witness slots into the
   spectrum with an exactly computed value. If the structure half is boring, the theorem
   stands; if the proof half breaks, the break is at the region lemma every lane leans on —
   either failure teaches. Ranked first *because* its worst case is informative, per the
   round-1 lesson.
2. **II3 — connectivity is the load-bearing hypothesis.** An exact, immediately bankable
   construction (unbounded $E$ without connectedness) that no finiteness proof can ignore,
   plus the sharpest cheap open gap in the file (figure-eight: 2, 3 or 4?). It is the round's
   best ratio of certainty to consequence, and its by-product — Theorem 2 is point-set, so
   only non-wedge mechanisms can beat 2 anywhere — is already banked in D2.
3. **II2 — the density-point criterion.** Small, safe, and strategically placed: the first
   positive criterion living at the wild end of the regularity spectrum, and the best
   candidate this problem has for a first `verified:lean` statement. Its explicit downside
   (mathematically subsumed by the unread Meyerson bound) is priced in: the value is formal
   and in-repo, not novelty.

*(II5 is the reserve: promote it if a slot opens before the later tier unblocks.)*

## What I believe is genuinely novel here, with honest confidence

All estimates rest on zero primary sources, per the provenance warning in
[`../../README.md`](../../README.md); "novel" means "not seen in any snippet and not in this
repo", nothing stronger.

- **II1's spectrum objects and the invariant $\alpha_0(O)$**: ~20% that the framing is in the
  literature; the small-apex theorem itself ~35% novel (folklore risk is high; the *uniform*
  version slightly less so).
- **II3(i) unbounded $E$ under disconnection**: ~95% that nobody bothered to write it, ~100%
  that it is easy; its value is hypothesis-isolation, not depth. The figure-eight maximum:
  genuinely unknown to this repo, ~50% inside Meyerson's unread "continuous curves".
- **II4(a) the conical-spiral witness in $\mathbb{R}^3$**: ~40% novel; (b) the smooth-space-curve
  question: ~40% that GRS answers it, and finding that out is itself the deliverable.
- **II5's robust/grazing dichotomy**: ~65% novel as a stated dichotomy; the openness lemma is
  elementary and surely known in spirit.
- Everything else I assume is known, folklore, or minor, and is proposed for its in-repo
  structural value rather than for priority.
