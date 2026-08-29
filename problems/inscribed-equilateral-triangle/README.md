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
- `results/` — statements that reached `cited`, `verified:lean`, or `verified:review`.
