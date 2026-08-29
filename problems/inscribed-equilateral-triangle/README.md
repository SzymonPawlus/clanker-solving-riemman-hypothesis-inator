# The inscribed equilateral triangle problem (the "triangle peg problem")

**Status: SOLVED in the literature — on citations this project has not been able to read.**
Every Jordan curve inscribes an equilateral triangle, and the sharper vertex-wise question is
settled too: at most two points of a Jordan curve fail to be a vertex of some inscribed
equilateral triangle, and the bound of two is attained.

> **Read the [provenance warning](#provenance-warning--read-before-relying-on-anything-below)
> before the results table.** No paper body and no abstract was read in situ for any row of it.
> The `cited` labels are marked `cited`\* throughout and are **not assumable** in the sense of
> [`../../RULES.md`](../../RULES.md) §3 until the verification debt below is discharged. A reader
> who stops at this banner has the unhedged claim, which is exactly what the warning is for.

> **This is not the square peg problem.** Toeplitz's square peg problem — does every Jordan curve
> inscribe a *square*? — is **open**. The triangle case is not. Confusing the two is the single
> most likely way for work in this directory to go wrong; see
> [Relation to the square peg campaign](#relation-to-the-square-peg-campaign-issues-112131).

Shared conventions: [`../README.md`](../README.md). Repo-wide protocol:
[`../../RULES.md`](../../RULES.md). **Problem-specific rules: [`RULES.md`](./RULES.md) — read
before working on this problem.**

What *this project* has itself produced is a separate matter from the literature recorded below,
and is kept in its own table under
[What this project has established](#what-this-project-has-established--a-separate-table-and-none-of-it-assumable).
All of it is `sketch` or `numerical`, none of it is assumable, and none of it has been examined
outside the Claude family.

---

## Provenance warning — read before relying on anything below

Every attribution in this file was assembled under a hard network restriction. **No primary text
and no secondary full text was retrieved.** The session's egress proxy blocked every scholarly
host tried (`ams.org`, `arxiv.org`, `link.springer.com`, `matwbn.icm.edu.pl`, `eudml.org`,
`math.brown.edu`, `math.elte.hu`, `openproblemgarden.org`, `en.wikipedia.org`, `zbmath.org`,
`doi.org`, `semanticscholar.org`, `crossref.org`) for both `WebFetch` and `curl`; only GitHub was
reachable. What is recorded below therefore rests on **web-search result listings and the snippets
surfaced with them** — real titles, real URLs, consistent across several independent secondary
documents, but not text this project has read.

Concretely: **no abstract was read in situ and no paper body was read at all.** This is a weaker
evidence level than the "abstract read, body not read" qualification used for the `n = 20` row in
[`../circle-packing-equilateral-triangle/README.md`](../circle-packing-equilateral-triangle/README.md),
and it is deliberately flagged as such rather than smoothed over.

The `cited` labels below are therefore **provisional**. See
[Verification debt](#verification-debt--what-a-reviewer-must-actually-do) for exactly what a
reviewer with network access must confirm before any of these are built on. Nothing in this file
is `verified:lean` or `verified:review`.

---

## Statement

A **Jordan curve** is a subset $J \subset \mathbb{R}^2$ that is the image of a continuous
injective map $S^1 \to \mathbb{R}^2$; equivalently, a homeomorphic copy of the circle in the
plane. No smoothness, rectifiability, or finite-total-curvature assumption is made — those
hypotheses are what the *square* peg literature spends its effort on, and they are not needed
here.

> **Existence question.** For every Jordan curve $J \subset \mathbb{R}^2$, do there exist three
> points $a, b, c \in J$ with
> $$|ab| = |bc| = |ca| > 0\,?$$

### Degeneracy conventions

- The three points are required to be **pairwise distinct**, and the common side length is
  required to be **positive**. Without this the question is vacuous: $a = b = c$ satisfies the
  equalities trivially.
- Requiring three distinct points at equal pairwise distances already forces
  **nondegeneracy** — three distinct collinear points cannot be pairwise equidistant, since the
  distance between the two outer ones is the sum of the other two distances and hence strictly
  larger than either. So "nondegenerate equilateral triangle" and "three distinct points at equal
  pairwise distances" define the same object, and no separate non-collinearity hypothesis is
  needed. *(status `sketch` — an elementary remark of this project's own, not load-bearing for
  anything below; it is a convention-fixing observation, not a step in any proof.)*
- Contrast with the square peg literature, where degenerate "squares" (all four points equal) are
  a genuine nuisance and must be excluded by hand in limiting arguments. The equilateral case is
  cleaner in this one respect.

### The vertex-wise refinement — the sharper question, and the one the other lanes work on

> **Vertex-wise question.** For which $O \in J$ does there exist an equilateral triangle inscribed
> in $J$ having $O$ as one of its vertices?

Call $O \in J$ **exceptional** (for $J$) when no equilateral triangle inscribed in $J$ has $O$ as
a vertex. Write $E(J) \subseteq J$ for the set of exceptional points.

The existence question is exactly the assertion $E(J) \neq J$. The vertex-wise question asks how
much smaller than $J$ the set $E(J)$ is, and the literature answers this completely: $|E(J)| \le
2$ for every Jordan curve $J$, and there are curves with $|E(J)| = 2$.

Terminology note: much of the literature says "**Jordan loop**" (Schwartz) or "**simple closed
curve**" (Nielsen) for what is called a Jordan curve here. These are the same object. Some sources
say a point "**inscribes**" a triangle, meaning it is a vertex of one; that usage is avoided in
this file in favour of "is a vertex of".

---

## Status

**Solved.**

| Question | Status | Settled by |
|---|---|---|
| Does every Jordan curve inscribe an equilateral triangle? | **Yes — solved** | Meyerson (1980); also follows from Kronheimer & Kronheimer (1981) and from Nielsen (1992) |
| How large can the exceptional set $E(J)$ be? | **Solved, sharply: $\lvert E(J)\rvert \le 2$, and $2$ is attained** | Meyerson (1980); sharpness by an explicit example |
| Same questions for an arbitrary similarity class of triangle, not just equilateral? | **Solved** | Meyerson (1980) / Kronheimer & Kronheimer (1981) for existence; Nielsen (1992) for density of vertices |
| Does every Jordan curve inscribe a **square**? | **OPEN** | — (Toeplitz, 1911) |

There is no open existence question here. An issue in this directory proposing to "prove that
every Jordan curve inscribes an equilateral triangle" is proposing to reprove a 1980 theorem, and
should be closed or rescoped (a Lean formalisation of the known result is a legitimate rescoping;
a fresh proof attempt presented as new is not).

---

## Known results

Each row carries a status per [`../../RULES.md`](../../RULES.md) §3 and a **provenance** code
saying what this project actually saw. The provenance codes are:

- **P0** — primary text read. *(No row has this. Nothing was fetchable.)*
- **P1** — abstract read in situ from the publisher or preprint server. *(No row has this.)*
- **P2** — statement reported consistently by two or more independent secondary documents, seen
  only through web-search result snippets. This is the strongest provenance available in this
  session.
- **P3** — reported by a single secondary snippet.

| # | Result | Attribution | Status | Prov. |
|---|---|---|---|---|
| 1 | Every Jordan curve $J \subset \mathbb{R}^2$ contains the vertices of an equilateral triangle. | Meyerson (1980) | `cited`\* | P2 |
| 2 | **Meyerson's theorem (vertex-wise form).** For every Jordan curve $J$, all but at most two points of $J$ are vertices of an equilateral triangle inscribed in $J$ — i.e. $\lvert E(J)\rvert \le 2$. | Meyerson (1980) | `cited`\* | P2 |
| 3 | **Sharpness of the bound 2.** There is a Jordan curve with exactly two exceptional points; the reported example is the boundary of a suitable (obtuse) isosceles triangle, two of whose vertices are vertices of no inscribed equilateral triangle. | Reported as the standard sharpness example, restated in Schwartz (2019/2021); this project did not determine whether it originates with Meyerson | `cited`\* | P2 |
| 4 | Every simple closed curve $J \subset \mathbb{R}^2$ contains the vertices of a triangle similar to any prescribed triangle $T$ — the existence statement for an arbitrary similarity class. | Meyerson (1980) and, independently, Kronheimer & Kronheimer (1981) | `cited`\* | P2 |
| 5 | **Nielsen's theorem.** For any triangle $T$ and any simple closed curve $J \subset \mathbb{R}^2$ there are **infinitely many** triangles similar to $T$ with all vertices on $J$; in fact the set of such vertices is **dense** in $J$. | Nielsen (1992) | `cited`\* | P2 |
| 6 | **Schwartz's enhancement.** A version of Meyerson's theorem carrying topological information, plus: for each Jordan loop $J$ there is an **uncountable** set $G(J)$ of triangle shapes for which the "all but at most two points" conclusion also holds; $G(J)$ meets every angle $\theta \in (0, \pi/2)$. | Schwartz, *On spaces of inscribed triangles* (arXiv 2019) | `cited`\* | P2 for the abstract-level statement; the $G(J)$-meets-every-angle detail is P3 |
| 7 | **Higher dimensions, partial.** Nielsen's theorem generalises to Jordan curves embedded in $\mathbb{R}^n$ for a *restricted* set of triangles, together with a condition under which a given point of $J$ is a vertex of an inscribed equilateral triangle. | Gupta & Rubinstein-Salzedo, *Inscribed triangles of Jordan curves in $\mathbb{R}^n$* (arXiv:2102.03953, 2021) | `cited`\* | P2 |
| 8 | **Square peg contrast.** Toeplitz's square peg problem — every Jordan curve inscribes a square — is **open** for general (merely continuous) Jordan curves. It is known for convex curves, piecewise analytic curves, $C^1$ curves, curves of bounded total curvature, and other regularity classes. | Toeplitz (1911); survey: Matschke (2014). Regularity-class attributions per that survey's summary | `cited`\* | P2 |
| 9 | **Rectangle contrast.** Every continuous embedding $S^1 \to \mathbb{R}^2$ inscribes a rectangle (Vaughan's argument), and the *rectangular* peg problem for smooth curves saw major progress from Greene & Lobb. This is a different problem from both of the above. | Vaughan, via Matschke (2014); Greene & Lobb (2020–) | `cited`\* | P3 — included for orientation only; do not build on it without checking |

> **\* `cited` is marked provisional throughout this table, and provisional `cited` is _not_
> assumable.** `RULES.md` §3 defines `cited` as "established in the literature, with a specific
> reference", and makes it assumable precisely so that a later worker need not re-check it. Every
> row above rests on search-result snippets alone — no abstract read in situ, no paper body read
> at all — so taking the status column at face value would be doing the exact thing the provenance
> warning forbids. Until a reader with journal access discharges the
> [verification debt](#verification-debt--what-a-reviewer-must-actually-do), treat these rows as
> leads, not as premises, and do not build on them.
>
> The repo taxonomy has no tier for "a real reference exists but nobody here has read it", which
> is why this is handled with an asterisk and a paragraph rather than a status. That gap is worth
> a human's attention: it is not specific to this problem, and the same situation will arise
> wherever an agent works without literature access.

### How rows 1, 2, 4 and 5 fit together

The logical shape matters, because it is easy to over-attribute.

- Row 2 **implies** row 1 (a curve has more than two points).
- Row 5 **implies** row 4, and row 4 with $T$ equilateral **implies** row 1. So there are three
  independent routes to "every Jordan curve inscribes an equilateral triangle".
- Row 5 does **not** imply row 2. Density of the vertex set is strictly weaker than "all but at
  most two points": a dense set can miss a dense set. For the equilateral class specifically,
  Meyerson's bound is the stronger statement.
- Priority: the secondary sources consulted credit the *existence* of inscribed triangles of
  arbitrary shape to Meyerson (1980) and Kronheimer & Kronheimer (1981), and credit Nielsen (1992)
  with the *strengthening* to infinitude and density. A summary that says only "Nielsen proved
  every simple closed curve inscribes every triangle shape" understates what was already known in
  1981. Nielsen's own abstract, as reported, does state the existence together with the density,
  so citing Nielsen for existence is not wrong — merely not the earliest reference.

---

## What this project has established — a separate table, and none of it assumable

Everything in this section was produced **inside this repository**, by `claude` workers, on
2026-08-29. It is recorded here because [`../README.md`](../README.md) makes a problem's README the
place its state lives. It is kept **apart from the known-results table above**, and it must stay
apart: the two tables carry opposite kinds of risk, and merging them would destroy the only
distinction that makes either useful.

> **Status banner — it applies to every row below, without exception.** Every in-repo result here is
> **`sketch`** (an argument a `claude` worker wrote and nobody else has certified) or **`numerical`**
> (exact computation over finitely many fixtures). **Nothing below is `cited`, `verified:lean`, or
> `verified:review`. Nothing below is assumable** in the sense of
> [`../../RULES.md`](../../RULES.md) §3 — not by another lane, not by a later worker, and not by its
> own author. That is why the same three or four lemmas recur across the lanes below, re-derived
> from scratch each time rather than imported: a `sketch` may not rest on a `sketch`.
>
> **No agent outside the Claude family has examined any of it, and Codex has reviewed none of it.**
> Exactly one lane carries any independent examination at all — `convex-vertex-criterion`, with one
> same-family audit (Opus, which found and forced three corrections) and one same-family
> cross-review (Sonnet). By [`../../RULES.md`](../../RULES.md) §5 and §8 both are decorrelation
> passes only and confer **no** verification credit; every other lane below has had none. Read this
> table as a record of what was tried and what currently appears to work, never as a premise.

The contrast with the [known-results table](#known-results) is worth stating in one line. Those rows
are *probably true and unread*; these rows are *read in full and unverified by anyone outside a
single model family*. Neither is assumable, for opposite reasons, and no row of either table may be
cited as settling anything.

**Dependency hygiene, which is the one genuinely reassuring thing here.** No in-repo result below
uses a `cited`\* row as an input. Every lane checked its conclusion *against* Meyerson afterwards as
an external consistency test and said so explicitly. So the provisional citations and the in-repo
arguments are independent of each other, and a failure of the verification debt would not propagate
into this table.

### Results

| # | Result | Status | Regularity budget | Lane |
|---|---|---|---|---|
| A1 | **Observation R (the rotation criterion, as an iff).** $O$ is a vertex of an inscribed equilateral triangle $\iff J \cap \rho_{O,60°}(J) \supsetneq \{O\}$. The $\Rightarrow$ direction is what makes a single orientation sufficient, so a failed rotation test *proves* exceptionality rather than merely failing to find a triangle. | `sketch` | **none** — holds for any $S \subseteq \mathbb{R}^2$ with $O \in S$ | [`attacks/rotation-continuity/`](./attacks/rotation-continuity/README.md) §2; re-derived independently in three other lanes and both experiments |
| A2 | **Lemma A / Lemma 3 (no nesting), and Criterion M.** $J \cap \rho(J) = \{O\} \Rightarrow \overline\Omega \cap \rho(\overline\Omega) = \{O\}$. With A1 this gives an iff: $O$ is a vertex $\iff \overline\Omega \cap \rho(\overline\Omega) \supsetneq \{O\}$ — a *region*-overlap test in place of a curve-intersection test. | `sketch` | **Jordan** (Jordan curve theorem twice, plus Lebesgue measure) | [`rotation-continuity`](./attacks/rotation-continuity/README.md) §4; re-derived from scratch in [`rectifiable-case`](./attacks/rectifiable-case/README.md) §6.1 and [`half-density-obstruction`](./attacks/half-density-obstruction/README.md) §4–§5 |
| A3 | **The convex tangent-cone criterion.** For $K$ compact convex with $\operatorname{int}K \ne \emptyset$, $J = \partial K$, and $\alpha(O)$ the opening of the tangent cone at $O$: $\alpha(O) > 60° \Rightarrow O$ good (Thm B(i)); $\alpha(O) < 60° \Rightarrow O$ exceptional (Thm A); and at $\alpha(O) = 60°$ exactly, $O$ is good **iff** both extreme rays of the tangent cone meet $K$ in a segment of positive length (Thm B(ii)) — the boundary case is genuinely two-sided, not a formality. Counting (Thm C): at most two points have $\alpha < 60°$; at most three have $\alpha \le 60°$, and exactly three forces $K$ to *be* an equilateral triangle, all of whose vertices are then good. Hence (Cor E) all but at most two points of a convex $J$ are vertices, attained by the $30$–$30$–$120$ triangle (Prop D, exact witness). | `sketch` | **convex** ($K$ compact, $\operatorname{int}K \ne \emptyset$, $O \in \partial K$); Thm B additionally uses compactness and the IVT. Explicitly **not** used: smoothness, rectifiability, the Jordan curve theorem, any degree or winding argument | [`attacks/convex-vertex-criterion/`](./attacks/convex-vertex-criterion/README.md), with [`AUDIT.md`](./attacks/convex-vertex-criterion/AUDIT.md) and [`CROSS-REVIEW.md`](./attacks/convex-vertex-criterion/CROSS-REVIEW.md) — both same-family, see the banner |
| A4 | **The sector (wedge) criterion, and $60°$ as the exact threshold.** A closed sector at $O$ of aperture $\ge 60°$ and some positive radius lying inside $\overline\Omega$ $\Rightarrow$ $O$ is a vertex; aperture $< 60°$ is genuinely insufficient. Corollary: a simple polygon's exceptional set is contained in its vertices of interior angle $< 60°$ — a containment that can be attained and can be strict. A local crosscut hypothesis (Thm C) discharges the sector hypothesis for $C^1$ and polygonal curves; the lane could **not** discharge it for merely rectifiable ones and says so. | `sketch` | **Jordan + the sector hypothesis** (a one-sided cone condition at one point — the hypothesis *is* the regularity); Thm C: Jordan + Hypothesis (C) at one point | [`rotation-continuity`](./attacks/rotation-continuity/README.md) §5–§6 |
| A5 | **Theorem T (the rectifiable case).** If $\gamma$ is the arclength parametrisation of a rectifiable Jordan curve and $\gamma$ is differentiable at $t_0$ with $\lvert\gamma'(t_0)\rvert = 1$, then $\gamma(t_0)$ is a vertex of an inscribed equilateral triangle. Corollaries: $E(J)$ is $\mathcal{H}^1$-**null** for every rectifiable $J$ (T1); every point of a regular $C^1$ Jordan curve is a vertex (T2, which reproves A4's $C^1$ corollary without its unverifiable crosscut clause); and no rectifiable curve has an exceptional point at which $\gamma$ is differentiable with unit speed (T3). | `sketch` | **rectifiable Jordan + differentiability of $\gamma$ at the one point $t_0$.** Drop rectifiability and the hypothesis cannot be stated; drop differentiability and the conclusion is false (the $30°$ apexes of a $30$–$30$–$120$ triangle) | [`attacks/rectifiable-case/`](./attacks/rectifiable-case/README.md) §6 |
| A6 | **The spiral-tip witness — the wedge obstruction is not the whole story.** An explicit **rectifiable** Jordan curve $J_{c,\beta}$ (two logarithmic-spiral arms plus a closing arc, total length $2\sqrt{1+c^2}/c + \beta$) whose tip $O$ is exceptional even though the directions of $J$ seen from $O$ fill **all of $S^1$ at every scale** — so no wedge argument, local or global, can see it. Generalisation: the obstruction is a **rotating** wedge — arcs of angular width $< 60°$ that are allowed to depend on the radius (Lemma 2). §12.3 is explicit that rotating-wedge is a *mechanism, not a classification* of $E(J)$. | `sketch` | **Jordan + rectifiable, both as *conclusions* rather than hypotheses** — the file is one explicit curve and proves its own Jordanness and rectifiability | [`attacks/spiral-tip-witness/`](./attacks/spiral-tip-witness/README.md) |
| A7 | **The half-density obstruction, with the lane's own demotion attached.** If $O$ is exceptional then for every $r>0$ the angular section of $\overline\Omega$ on the circle of radius $r$ has measure $< 180°$, hence $\lambda(\overline\Omega \cap \bar B(O,R)) < \tfrac12\lambda(B(O,R))$ for **every** $R > 0$; the constant $\tfrac12$ is sharp and cannot be improved to $1/6$. The lane then demoted its own headline: the density statement is a *packaging* of Criterion M (A2) rather than an independent obstruction, it is **incomparable** to the sector criterion A4 rather than stronger, and it is **vacuous on every convex curve** (a supporting line already gives density $\le \tfrac12$). | `sketch` (core measure lemma), `numerical` (the exact pinwheel witness) | **none** for the measure core — an arbitrary measurable set and an arbitrary isometry fixing $O$; **Jordan** for the full chain | [`attacks/half-density-obstruction/`](./attacks/half-density-obstruction/README.md) |
| A8 | **An exact $\mathbb{Q}(\sqrt3)$ decider for polygons**, with no floating point in any decision, plus a validated battery: $190$ fixtures and a seeded hunt over $88\,346$ convex vertices, with **zero** violations of "a convex polygon's vertex is good $\iff$ its interior angle is $\ge 60°$", the exactly-$60°$ case resolved on the *good* side, and non-convex vertices good at interior angles down to $0.29°$ — so the governing quantity is the angular spread of $J$ seen from $O$, not the interior angle. | `numerical` | **polygonal** (simple polygons over $\mathbb{Q}(\sqrt3)$) | [`../../experiments/inscribed-triangle-polygons/`](../../experiments/inscribed-triangle-polygons/README.md) |
| A9 | **A second, structurally different exact decider** (angular sweep rather than segment intersection), agreeing with A8 on all $190$ fixtures and $2\,270$ boundary points, and used for an exceptional-set census: over $51\,587$ exactly-decided boundary points on $1\,640$ polygons the maximum exceptional count found was **2**, never $3$ — an independent check *on* the unread bound of row 2, and nothing more. | `numerical` | **polygonal** | [`../../experiments/inscribed-triangle-angular/`](../../experiments/inscribed-triangle-angular/README.md) |
| A10 | **Ideation round 1** — thirteen candidate directions, each with a kill-criterion, a "is this already Meyerson?" guess and a square-transfer test, triaged into a ranked shortlist. Proves nothing; it is the map the lanes above were dispatched from. | speculation (nothing assumable, per its own budget line) | not applicable | [`attacks/ideation-round-1/`](./attacks/ideation-round-1/README.md) |

### Refuted or corrected in-repo — kept, because these are what stop the work being redone

| Statement | Verdict | Where |
|---|---|---|
| "Every point of every Jordan curve is a vertex of an inscribed equilateral triangle." | **`refuted`**, exact witness: both $30°$ apexes of the $30$–$30$–$120$ triangle, with $J \cap \rho_{O,\pm60°}(J) = \{O\}$ computed exactly in $\mathbb{Q}(\sqrt3)$ | [`rotation-continuity`](./attacks/rotation-continuity/README.md) §3 |
| "For a convex body, $\alpha(O) \ge 60° \Rightarrow O$ is good." | **`refuted` as stated** — false at $\alpha(O) = 60°$ exactly, with an explicit convex witness $K^*$; replaced by the two-sided A3 Thm B(ii) | [`convex-vertex-criterion`](./attacks/convex-vertex-criterion/README.md) §4.1 |
| The sector criterion's "…and the triangle produced has side $\varepsilon/2$". | **`refuted`** by an exact unit-square witness, and **deleted in place** with a correction note — Corollary A′ is a non-constructive contrapositive, so the point it returns need not be the one constructed | refuted in [`rectifiable-case`](./attacks/rectifiable-case/README.md) §7, corrected in [`rotation-continuity`](./attacks/rotation-continuity/README.md) §5, §6 and its correction note |
| "The half-density criterion is strictly stronger than the sector criterion." | **wrong** — they are incomparable; recorded by the lane that inherited the claim | [`half-density-obstruction`](./attacks/half-density-obstruction/README.md) §5.4 |
| Three arithmetic/attribution errors in the convex lane, including a `[ATTACK HERE]` marker pointing at the file's *safest* step. | found by the same-family audit and fixed in place | [`convex-vertex-criterion/AUDIT.md`](./attacks/convex-vertex-criterion/AUDIT.md) |

### The one synthesis no single lane could state

`rectifiable-case` and `spiral-tip-witness` ran concurrently, in disjoint files, without contact.
Put together, and **only** together:

> On a rectifiable Jordan curve, every exceptional point is a point where the arclength
> parametrisation fails to be differentiable with unit speed — and such exceptional points
> genuinely exist.

Theorem T (A5) supplies the "only"; the spiral witness (A6) supplies the "they exist". They do not
collide, and the reason is checkable in four lines: at the spiral tip the chord/arc ratio is the
**constant** $c/\sqrt{1+c^2} < 1$, so the unit-speed parametrisation has no derivative there at all
— the tangent fails by infinite winding, not by oscillation — and the tip falls outside Theorem T's
hypothesis. The witness is therefore not a counterexample to Corollary T1 either: a single point is
$\mathcal{H}^1$-null.

**This synthesis is `sketch`, and weaker than either half.** It is capped at the weakest status of
what it rests on ([`../../RULES.md`](../../RULES.md) §3), both halves are unreviewed outside the
Claude family, and the "with unit speed" qualifier is load-bearing — Theorem T's hypothesis is
differentiability *with $\lvert\gamma'\rvert = 1$*, and dropping those three words states something
the lanes did not prove.

**Snapshot date.** This section reflects the lanes present on 2026-08-29. Further lanes were in
flight when it was written and land in their own PRs; a reader should treat
[`attacks/`](./attacks/) and [`../../experiments/`](../../experiments/) as authoritative over this
summary wherever they disagree, and any disagreement is a defect in this file.

---

## What remains open

Nothing in the planar equilateral question. The items below are the genuinely adjacent open or
unknown-to-us directions. Each is labelled with how confident this project is that it is *open*,
which is a separate matter from whether the statement is true.

1. **Jordan curves in $\mathbb{R}^n$, general similarity classes.** Gupta &
   Rubinstein-Salzedo (2021) extend Nielsen's theorem to $\mathbb{R}^n$ only for a *restricted*
   set of triangles, and give only a *condition* under which a point of $J$ is a vertex of an
   inscribed equilateral triangle. The framing "restricted set" / "a condition under which" comes
   from the reported abstract, so the unrestricted $\mathbb{R}^n$ statement is at least not
   claimed there. *We regard this as open on the strength of that framing; we have not seen the
   paper state it as an open problem.*
2. **The vertex-wise property for other triangle shapes.** Schwartz produces an uncountable set
   $G(J)$ of shapes obeying the "all but at most two points" conclusion. Whether $G(J)$ is *all*
   shapes for every $J$ — or, equivalently, whether the exceptional set is finite for every
   prescribed shape — is a question this project could not settle from the available snippets.
   One snippet asserted the all-but-finitely-many conclusion "is not known for any other shape of
   triangle (e.g. right isosceles)", but that was a single unverified secondary summary and is not
   recorded as fact. **We do not know the status of this.**
3. **Non-Jordan continuous curves.** Meyerson's 1980 title is "Equilateral triangles and
   *continuous* curves", which suggests the paper treats curves more general than Jordan curves,
   but the body was not read and it is unknown to this project what is proved there for
   non-injective curves or for planar continua generally. **We do not know the status of this**,
   and in particular we do not know whether it is open or already answered inside the very paper
   we are citing. This is the cheapest verification win available here.
4. **Quantitative and extremal refinements.** Whether there are bounds on the *size* of the
   inscribed equilateral triangle relative to the diameter of $J$, on how many essentially
   distinct inscribed equilateral triangles a curve must carry, or on the structure of the space
   of inscribed equilateral triangles for a fixed $J$, is not something this project has sourced.
   Schwartz's "topological information" enhancement (row 6) is the obvious place to look first.
   **We do not know the status of these.**
5. **Formalisation.** No Lean formalisation of Meyerson's theorem is known to this project. This
   is not a research open problem — it is an in-repo opportunity, and the most defensible kind of
   work this directory can host, because a `verified:lean` proof of a *known* theorem carries no
   §7 extraordinary-claim risk. See `RULES.md`.

Nothing above should be read as an invitation to attack the planar equilateral existence question.
It is closed.

---

## Relation to the square peg campaign (issues #112–#131)

Issues **#112–#131** are the codex-owned square peg campaign. **This is a separate problem area and
the two must not be merged**, for three reasons:

1. **Different status.** Square peg is open; triangle peg is not. A directory whose central
   question is settled runs on completely different rules from one whose central question is open:
   here, "I have a proof" is a red flag about duplication, not a §7 extraordinary claim; there, it
   is a §7 extraordinary claim.
2. **Different file ownership.** Merging the trees would put two agents' work in one directory and
   break [`../../RULES.md`](../../RULES.md) §2.
3. **Different mathematics, despite the family resemblance.** The odd-cardinality / parity and
   continuity arguments that make three-point configurations tractable do not transfer to
   four-point configurations, which is broadly why the triangle case fell in 1980 and the square
   case has not fallen in a century. *(status `sketch` — this is this project's own
   characterisation of why the problems differ; it is offered as orientation, it is not sourced,
   and it must not be used as a step in any argument.)*

**Practical rule for anyone working here.** A result in this directory is **not** evidence for or
against the square peg conjecture, and must never be cited in the square peg campaign as though it
were. Conversely, if some technique developed here appears to settle the square case, the
overwhelmingly likely explanation is an error — see [`../../RULES.md`](../../RULES.md) §7, and note
that a method which genuinely proved both would have to explain why a century of experts missed it.

The legitimate connection is bibliographic: Matschke's square peg survey is a good entry point to
*both* literatures, and several authors (Schwartz, Greene & Lobb, Nielsen) appear on both sides.
Share references freely; share claims not at all.

---

## Verification debt — what a reviewer must actually do

Because of the provenance warning at the top, this file's `cited` labels are provisional. A
reviewer with network access should, in decreasing order of value:

1. **Read Meyerson (1980) itself** — the Fundamenta Mathematicae archive at
   `matwbn.icm.edu.pl` reportedly carries full text, and EUDML indexes the paper at
   `https://eudml.org/doc/211210`. Confirm: (a) the exact theorem statement, (b) that the
   hypothesis is "Jordan curve" and not something weaker or stronger, (c) whether the bound of two
   exceptional points and its sharpness example are both in that paper, and (d) what the title's
   "continuous curves" covers — this bears directly on open item 3 above.
2. **Read the abstract page for Nielsen (1992)**, `doi:10.1007/BF00151519`, and confirm the exact
   statement (infinitude + density) and the page range 291–297.
3. **Read Matschke's survey PDF**, `https://www.ams.org/notices/201404/rnoti-p346.pdf`, and record
   what it actually says about the triangle case. This project could **not** confirm that the
   survey states the triangle status explicitly — only that Meyerson (1980) appears in its
   reference list, and even that came from a search summary. Also settle the page range: sources
   seen gave both 346–352 and 346–351.
4. **Read Schwartz, arXiv:1908.08174**, and confirm row 6, in particular the precise form of the
   $G(J)$ statement.
5. **Read Gupta & Rubinstein-Salzedo, arXiv:2102.03953**, and confirm the exact scope of the
   $\mathbb{R}^n$ restriction — open item 1 depends entirely on this.

Any row that survives step 1–5 should have its provenance code upgraded to P0/P1. Any row that
does not survive should be corrected in place with a note saying what was wrong, in the style of
the "Resolution of the source conflict" section of
[`../circle-packing-equilateral-triangle/README.md`](../circle-packing-equilateral-triangle/README.md).

---

## Sources

Bibliographic records as this project believes them; none of these pages was retrievable from this
session, so the URLs are provided for a reviewer rather than as evidence already consulted.

- **Meyerson, Mark D.**, *Equilateral triangles and continuous curves*, Fundamenta Mathematicae
  **110** (1980), no. 1, 1–9. EUDML record: <https://eudml.org/doc/211210>. Full text reportedly
  in the Fundamenta open archive at <https://matwbn.icm.edu.pl/>. **The central reference.**
- **Kronheimer, E. H. & Kronheimer, P. B.**, *The tripos problem*, J. London Math. Soc. (2)
  **24** (1981), 182–192, `doi:10.1112/jlms/s2-24.1.182`. Independent source for the
  arbitrary-similarity-class existence statement.
- **Nielsen, Mark J.**, *Triangles inscribed in simple closed curves*, Geometriae Dedicata **43**
  (1992), 291–297, `doi:10.1007/BF00151519`. Infinitude and density of vertices.
- **Schwartz, Richard Evan**, *On spaces of inscribed triangles*, arXiv:1908.08174 (2019).
  Enhanced Meyerson theorem with topological content; the uncountable shape set $G(J)$.
- **Gupta, Aryaman & Rubinstein-Salzedo, Simon**, *Inscribed triangles of Jordan curves in
  $\mathbb{R}^n$*, arXiv:2102.03953 (2021). Higher-dimensional partial generalisation.
- **Matschke, Benjamin**, *A survey on the square peg problem*, Notices Amer. Math. Soc. **61**
  (2014), no. 4, 346–352 (one source gave 346–351). PDF:
  <https://www.ams.org/notices/201404/rnoti-p346.pdf>. Entry point to the *square* problem; its
  coverage of the triangle case is **unconfirmed**.
- **Apró, J.**, *Triangles and quadrilaterals inscribed in Jordan curves*, BSc thesis, Eötvös
  Loránd University, 2023. A secondary survey that restates both Meyerson and Nielsen; useful as a
  cross-check, not as an authority.

Working journal for the search that produced this file, including what could not be reached:
`notebook/claude/2026-08-29-iet-literature.md`.

---

## Layout

- [`RULES.md`](./RULES.md) — how work on this problem must be done. **Read it first.**
- `attacks/` — one directory per approach.
- `results/` — statements that reached `cited`, `verified:lean`, or `verified:review`. Still
  **empty**, and correctly so: nothing this project has produced qualifies.
- This problem's numerics live outside the directory, in
  [`../../experiments/inscribed-triangle-polygons/`](../../experiments/inscribed-triangle-polygons/README.md)
  and [`../../experiments/inscribed-triangle-angular/`](../../experiments/inscribed-triangle-angular/README.md);
  both are `numerical` and neither is a proof step.
