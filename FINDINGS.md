# Findings

Running log of things worth a human's attention. Newest first. Agents append here when they find
something genuinely interesting — a result, a refutation, a near-miss, or an error in our own work.

**This is a highlights log, not a claims register.** Nothing here is citable. Every entry points at
the PR or file where the claim lives with its real status (`RULES.md` §3).

---

## 2026-08-22

### A plateau "explained" by a coincidence — the explanation was withdrawn the same day
`issue #97` · `problems/circle-packing-equilateral-triangle/attacks/n16-structure/` · no claim changed status

**This entry replaces one that asserted the explanation was correct.** The original is withdrawn
and the reasoning is kept, because the withdrawal is the finding.

Four independent searches had converged on the same covering side length $a = 1+2\sqrt3$ for
$n = 16$, and the campaign had logged the plateau four times without asking why that number. The
manager produced a counting theorem — classify the pieces of a diameter-$<1$ covering by how many
sides of the triangle each meets, note the classes are disjoint so their lower bounds add, and
observe that the *deep triangle* (points at distance $\ge 1$ from all three sides) has side
$\delta = a - 2\sqrt3$, which reaches $1$ exactly at $a = 1+2\sqrt3$. The forced count jumps from
13 to 15 precisely there. Headline: **$1+2\sqrt3$ is the least side length at which fifteen pieces
are necessary**, so the optimisers are not stuck, they are sitting on an extremal point.

**It is false, and the refutation is one line.** The 15-point unit triangular lattice sits in
$T_4$ — that is just $a_{15} = 4$, which is `cited` and was sitting in the same table the argument
drew its other inputs from. A piece of diameter $<1$ holds at most one of those 15 points, so
fifteen pieces are necessary for **every $a \ge 4$**, which is $0.46$ below the claimed threshold.
The counting theorem forces only $10$ at $a = 4$, where the truth is $\ge 15$: it is five pieces
slack, and its arriving at 15 exactly at $1+2\sqrt3$ is a coincidence.

**The mechanism, and it is not "check your arithmetic" — the arithmetic was all correct.** Two
different quantities were conflated. The plateau is about
$A_{15} = \sup\{a : T_a \text{ is coverable by } 15\}$; the theorem bounds
$\min\{a : N(a) \ge 15\}$. Both are "15 and $a$", they move in the same direction, and the
numerical agreement at $1+2\sqrt3$ made the conflation invisible. **A coincidence that lands on the
number you were trying to explain is the most persuasive possible evidence and the least
diagnostic** — the prior that an unexplained empirical constant has a one-line explanation is low,
and matching it exactly should have raised the question "what else forces 15?", which the `cited`
table answers immediately.

**What survives** is the half nobody had asked for: the theorem's *class structure* — any 15-piece
covering has exactly 3 two-side, 9 one-side and 3 no-side pieces — which is a rigorous replacement
for a "forced $3+9+3$" claim two separate audits had just shown was unproved. The plateau itself is
**still unexplained.**

**Third coordinator error in two days**, after the broadcast wrong table and the near-miss below.
All three had the same shape: a conclusion more interesting than the boring alternative, believed
because it was interesting. The reviewer who caught this one was given an explicit brief that
manager output carries no privilege; that appears to have been the operative difference.

---

### The dramatic version of that result was wrong, and being dramatic is what should have flagged it
`issue #97` · same lane · no claim changed status

Deriving the above, the manager reached for Borsuk's planar constant — every plane set of diameter
$d$ splits into three of diameter $\le \tfrac{\sqrt3}{2}d$ — to bound when three pieces can no
longer cover the deep triangle. That puts the 16-piece threshold at $8\sqrt3/3 = 4.6188$, which is
**below** the best-known 16-point packing at $4.6247637$ — i.e. an apparent proof that the covering
method can never settle $n = 16$, however much compute is thrown at it. A sharp, quotable,
campaign-redirecting negative result.

It is false. $\sqrt3/2$ is extremal for the disk and the Reuleaux triangle; the equilateral triangle
splits far better, into three parts of diameter $\delta/\sqrt3$, by joining the centroid to the
three side midpoints. The correct threshold is $\delta \ge \sqrt3$, i.e. $a \ge 3\sqrt3 = 5.196$ —
far above the target, and the striking conclusion evaporates entirely.

**This is the fifth instance of the pattern this file tracks, and the second from the coordinator.**
The shape is the same every time: a remembered constant, applied without re-deriving it, that
happens to produce a *more interesting* conclusion than the boring alternative. The new detail
worth recording is the tell. The wrong constant did not announce itself by looking wrong — it
announced itself by making the result **land just below the target**, at $4.6188$ against
$4.6248$. A margin that narrow, in your favour, on a question centuries of effort have not settled,
is not a lucky break; it is a prompt to re-derive the input that produced it. The rewritten rule:
**the more a result would change what the project does next, the earlier its inputs get checked —
not the later.**

The final write-up needs no Borsuk-type input at all; it uses only the apex-to-centroid distance,
which is elementary.

---

### `WebSearch` works in this session; four lanes had written the literature off
`issue #97` · `problems/circle-packing-equilateral-triangle/attacks/n16-literature/` · no claim changed status

Four workers recorded "novelty unverifiable from this session — scholarly hosts are blocked" and
stopped. Measured: `WebFetch` is blocked universally (4/4 probes, including hosts nobody had tried),
but the `WebSearch` tool returns results normally. The session has **bibliographic egress without
textual egress** — enough to settle volumes, pages and what a paper announces; not enough to read a
proof or a table.

That distinction matters here because it produced a live candidate for the campaign's novelty
question: Gáspár & Tarnai, *Upper bound of density for packing of equal circles in special domains
in the plane*, Periodica Polytechnica Ser. Civ. Eng. **44**:1 (2000) 13–32, which refines Groemer's
and Oler's inequalities for the equilateral triangle and, per its abstract, prints numerical bounds
**up to 30 circles**. An upper bound on density at fixed $n$ *is* a lower bound on $s(n)$, so one
line of one table decides whether this campaign's $s(16) \ge 2+6\sqrt3$ is a record or a
rediscovery of something weaker. The body is behind the same block.

**The transferable point is not about this session's proxy.** A capability that four workers
reported as absent was half-present, and none of them had tested the half. "Blocked" was inherited
from an earlier lane's note and propagated as fact.

---

## 2026-08-21

### Every error found today was a correct theorem read one step too broadly
`PR #95` · `issue #91` · no claim changed status

Two verification passes over a day's work found six disagreements. A third party — the same
verifier, summarising at the end — noticed what they have in common, and it is worth more than any
of them individually:

> All four errors found across both passes are the same failure: a correct theorem read one step
> too broadly. None is arithmetic — every table reproduces exactly. The errors are in the sentence
> *after* the arithmetic.

The instances, all from 2026-08-21:

| The theorem, correct | The sentence after it, false |
|---|---|
| $\sum \mathrm{Oler}(P_i) = \mathrm{Oler}(P) + I + (m-1)$ | "every partition-and-count refinement of Oler is dead" |
| A resolution theorem bounding cell size | "there is no budget at which a cell exhaustion terminates" (it is the *converse*: a termination guarantee) |
| A family with $b = 3$ and growing deficit | "therefore no function $\Phi$ exists" (the published family's deficit peaks at $k=76$ and falls) |
| The atlas: stage 1 is zero at $n=T(k)-1$ | "so the relaxation is what fails, not the packing bound" (false for interior-deleted configurations) |
| The Barrier Theorem at integer side | "convex-cut relaxations are dead at $a<6$" |
| Oler's paper has no equality clause | "the equality characterisation is missing" (Groemer's has it) |

**Why this is the shape.** Exact arithmetic is checkable and was checked — every disputed table
reproduced to the digit. What is not checkable by rerunning is the *scope* of a conclusion, and
scope is where a language model generalises for free: the true statement is about
`Oler-per-piece`, the remembered statement is about `partitions`; the true statement is about
`Oler's paper`, the remembered one is about `the literature`. Nothing in a test suite fails when
a quantifier widens.

**Three of the six were the coordinator's**, and two of those were broadcast to running workers as
instructions before anyone caught them — so the failure compounds with authority. The coordinator's
own summary of its errors matches the pattern exactly: in each case it had a ready explanation for
a discrepancy and stopped checking.

**What it argues for.** Exactness discipline (`RULES.md` §4, this problem's §2) protects the
numbers and does nothing for the sentences. The cheap countermeasure is the one that actually
caught these: when a file states a general claim *and* notes an exception to it, the exception is
the finding. Three of today's six were sitting, labelled "one exception" or equivalent, two
sections above the claim they refute, in the author's own file.

---

### The equality characterisation the repo calls "missing" has been quoted in its own README all along
`issue #96` · `PR #95` · affects `attacks/oler-lower-bound/` §5.2 and the problem README

`attacks/oler-lower-bound/` §5.2 records, from a full reading of Oler's Acta Math. paper, that it
**does not** contain an equality characterisation for Oler's inequality, and names that as the
missing tool — the thing a lower-bound attack on Erdős–Oler would need. Issue #44 exists to find
it. A worker today spent a session proving special cases of it from scratch.

It is on page 225 of this repository's own problem README, quoted verbatim from the GDZ scan of
**Groemer (1960)**, and has been since before today:

> with equality iff the region is the convex hull of the circles *and* the hull $H$ of the centres
> decomposes into equilateral triangles of side 2 whose vertices are all centres (or degenerates to
> a segment or a point).

**The link that makes it apply.** Groemer's Satz is $n\sqrt{12} \le F - \varkappa U + \lambda$ for
unit-radius circles in a convex region. Apply it to $K = H \oplus B_1$, the outer-parallel body of
the hull of the centres, and substitute Steiner's $F = A + M + \pi$, $U = M + 2\pi$. Every $\pi$
cancels — $\lambda$'s $-\pi(\sqrt3-1)$ against $(1-2\varkappa)\pi$ — leaving
$n \le \tfrac{\sqrt3}{6}A + \tfrac{M}{4} + 1$, which is **Oler's inequality verbatim** once
rescaled from separation 2 to separation 1. Verified symbolically here. Groemer's equality clause
therefore transfers directly, and equality in Groemer requires the region to *be* the hull of the
circles, which the substitution makes automatic.

**Why it was invisible.** The README's Groemer section applies his Satz to the **containing
triangle** ($F = \sqrt3 s^2/4$, $U = 3s$) and tabulates it as slack at every triangular $n$ — the
comparison that supports the correct conclusion that Groemer's paper credits no particular $n$. But
that is Groemer evaluated on the *wrong region*. On the right one he is not slack; he is exactly
Oler. The section is `sketch` and says it is offered only as a consistency check, so nothing
false was asserted — the number simply answered a different question than the one later readers
brought to it, and no one re-read it while looking for an equality clause.

A literature worker flagged this possibility this morning, as a **question** rather than a
correction, on the strength of a paper title alone (*"A new proof for the Zassenhaus–Groemer–Oler
inequality"*, unread) suggesting the three results are standardly named together. That instinct
was right and the caution was right.

**The general point.** Two attacks and an open issue were organised around the absence of something
the repository already held, quoted from a primary source, one file away. The failure was not of
reading but of **indexing**: the fact was filed under an attribution question ("does Groemer
deserve co-credit?" — answered no, correctly) and never re-surfaced under the question it actually
answers. A repository whose value is that a reader can tell verified from unverified needs its
`cited` material findable by *what it says*, not only by the question that first prompted it.

**Not yet checked, and load-bearing:** pp. 286–293 of Groemer — the proof of the Satz — remain
unread, so whether the equality clause carries a hypothesis dropped in the one-sentence
transcription is unknown. GDZ is blocked at this session's egress proxy. That check is what would
turn this from a strong `sketch` into something citable.

---

### A `cited` input contained the conclusion, and the run reported a proof of an open case
`PR #90` · `issue #91` · no claim changed status

A worker built an exact integer relaxation of the corner-occupancy constraints and ran it at
$k = 4$, where Erdős–Oler is *proven*, as a control. The run came back **infeasible** — which,
read at face value, is a counting proof of Erdős–Oler at $k = 4$.

It was circular. The worker extracted the violated constraint instead of believing the verdict:
the single binding constraint was the whole-triangle box, whose capacity had been supplied by the
`cited` value $d(9) = 3$ — and $d(9) = 3$ **is** Erdős–Oler at $k = 4$. The model had been handed
its own conclusion as an input and had correctly derived it back out.

**The general point, which `RULES.md` §3 does not currently make.** Status is treated as a property
of a claim: `cited` claims are assumable, so you may use them. But assumability is not
context-free. A `cited` fact is safe as an *input* only when it is not the *output* you are
deriving. A table of known optimal values is exactly the kind of input that silently contains the
conjecture for the cases where the conjecture is known — which is to say, precisely the cases you
would use as controls.

**What makes this worth logging rather than fixing quietly:** the control was working as designed.
Running the method where the answer is known is what caught it. Had the same circular input been
present only at $k = 7$ — where the whole-triangle capacity is *not* known and so would have come
from somewhere else — the run would have reported infeasible on an open case, and the result would
have read as a solved open problem produced by a clean exact computation with all inputs `cited`.
Nothing in the status discipline would have flagged it. The guard is now a named variable in the
code rather than a habit.

The same worker separately caught itself asserting that a pair region $\{u_A \ge 4\} \cap
\{u_B \ge 4\}$ was a triangle when it is a rhombus holding 8 points rather than 4.

---

### The manager "corrected" a worker with worse arithmetic, and shipped it to two provers
`PR #90` · `issue #91` · no claim changed status

A worker reported that the side-length gap between Oler's bound and the truth at $n = T(k)-1$
collapses like $2/(2k+1)$ — $0.298$ at $k = 3$, $0.135$ at $k = 7$. The manager (claude, Opus 5)
re-derived it, got $0.628 \to 0.272$, concluded the worker had made a separation-1/separation-2
slip, **published the wrong table in a commit message, and relayed it to two live provers as a
correction.** Prover A caught it independently an hour later.

The worker was right. The manager's root-solve had the discriminant wrong and solved
$\mathrm{Oler}(a) = T(k) - \mathbf{2}$ instead of $T(k) - \mathbf{1}$. The correct root is
$a_0 = \tfrac{-3 + \sqrt{8T(k) - 7}}{2}$, giving exactly the worker's figures; $2/(2k+1)$ is a
good approximation to them.

**This is the fourth instance of the pattern this file exists to track, and the first where the
error came from the coordinator rather than a worker.** The previous three — the Melissen–Schuur
volume, the $n = 20$ withdrawal, the Approach C recount — all had the same shape: a correction
that felt *more* certain than what it replaced, because withdrawing a claim reads as rigour from
the inside. The new element here is the delivery mechanism. A worker's error stays in a worker's
file until review; **a manager's error is broadcast to every worker as an instruction**, arrives
with the authority of coordination, and lands in files the manager never sees. One prover was
mid-run with the bad table when the correction went out.

**The mechanism, and it is not "check your arithmetic".** The manager had *just* written a section
warning that separation-1 vs separation-2 is the standing trap on this problem. Holding a
ready-made explanation for a discrepancy is what made the discrepancy stop being a question: the
two numbers differed by roughly a factor of two, a factor of two had a known cause, and the
check ended there. The available explanation was wrong and the arithmetic was never re-examined.

**What it argues for:** a coordinator's numbers are not a review; they are one more input needing
the same check as any other. When a discrepancy has an obvious explanation, that is exactly when
the boring possibility — the coordinator simply computed it wrong — is worth eliminating first.

---

## 2026-08-18

### The Melissen–Schuur volume went 145 → 142 → 145, and `main` was right the whole time
`PR #21` · `issue #17` · no claim changed status

The citation is *Discrete Mathematics* **145**(1–3) (1995) 333–342. It was correct on `main`, was
"corrected" to **142** on the PR #21 branch, and has now been put back. Both moves were made in good
faith; the second was a cross-family review item that its author, Codex, then publicly withdrew
(comment `5325654348` on PR #21) after checking the published article.

**The mechanism is what is worth keeping.** The 142 came from the University of Twente Pure record —
an institutional repository's auto-generated metadata page. Its DOI, issue number and page range are
all *correct*; only the volume field is corrupt. That is precisely what made it persuasive: a record
that agrees with everything you can check it against, differing only in the one field you were not
checking. The same institution hosts the publisher-typeset PDF, whose front-matter banner and all
ten running heads read 145 — the source contradicted itself, one click apart.

Established independently twice, once by each model family: the publisher PDF
([ris.utwente.nl](https://ris.utwente.nl/ws/files/6509759/Melissen95packing.pdf)), CrossRef for
DOI `10.1016/0012-365X(95)90139-C`, and OpenAlex all give volume **145**(1–3), 333–342.

**The rule it argues for:** a publisher's typeset front matter and CrossRef outrank a repository's
generated metadata. Repository records are derived data, and a bibliographic field taken from one is
evidence *about* the publication, not the publication.

**The uncomfortable part: this is the third time today that a correction was itself the error.** The
n = 20 withdrawal overshot (entry below); the Approach C moment recount on `PR #26` was got wrong
twice; now the volume. None of the three was careless — each was argued from a source it named. The
common factor is confident propagation of a **secondhand record**: a survey's silence, a recount
someone else had already done, a repository's generated field. Each felt *more* certain than what it
replaced, because withdrawing a claim reads as rigour from the inside — which is the same tell the
n = 20 entry flagged, now frequent enough to be a habit rather than an incident.

---

## 2026-08-17

### n = 20 is unverified, not unproven — and our first correction overshot
`PR #36` · closes `issue #14`

Our README asserted **n = 20 is proven optimal (Payan 1997)** flatly, on a survey, with no record of
what had actually been read. Payan's abstract, obtained verbatim from the publisher in both
languages Elsevier prints:

> "In this paper, we give a proof for k = 5 (arrangement for 14 disks). **This proof can be
> extended for the case k = 6** (arrangement for 20 disks) and should allow an approach of the
> general conjecture."

French: *"Cette preuve s'étend de manière un peu plus laborieuse pour k = 6."* That is a present
indicative — the author asserting, in his own paper's abstract, that his proof **applies** to
k = 6. The body was not obtained, so we cannot tell an extension written out in full from one left
to the reader; but that is a gap in *our* reading, not evidence the result is absent. The honest
position is **unverified — neither proven by us nor disproven**, and the row now carries its
provenance ("abstract only — body not read") instead of a bare citation. **n = 14 is unaffected and
is now better sourced**, resting on Payan's own abstract rather than a survey.

**The finding worth keeping is what the first revision of this PR did.** It concluded n = 20 was
never proven, moved the row to best-known and downgraded Erdős–Oler from k ≤ 6 to k ≤ 5 — on the
strength of three sources' **silence**: Tedeschi & Mackey's abstract omitting n = 20, Wikipedia
summarising only n ≤ 15, zbMATH's uninformative review. None of those denies anything. T&M's
introduction states n = 20 as proven and cites Payan for it; its abstract simply does not mention
the separate result, and omission is not denial. Reading those silences as refutation is the same
error as reading a survey's summary as a primary source — inverted. Cross-family review caught it
and the PR was reworked to the qualified attribution above.

So this does not file cleanly as one more secondary-source miss (after the Friedman misreading and
the reversal/contraction error). It is the **first time our own correction overshot**, which is the
more instructive case: withdrawing a claim feels like rigour from the inside, and that feeling is
not evidence either.

Two gaps closed the same way, by going to primaries:

- **Melissen split resolved.** zbMATH Zbl 0814.52006 confirms the 1993 Monthly paper covers
  $n = 2,\dots,10,12$ plus triangular $n$, with $n = 11$ merely *announced* there and settled in
  Acta 1994 — vindicating the earlier inference, including that Friedman has 11/12 backwards.
- **Groemer co-credit rejected on the primary.** Math. Z. **73** (1960) 285–294 was read directly
  (free GDZ scan). It contains exactly one theorem, a general convex-region inequality, with **no
  triangle application and no per-$n$ result**. Oler-only credit now stands as a checked
  conclusion rather than a flagged guess.

**Actionable for a human:** Payan's article page is marked *"Open archive"*. Automated fetches are
bot-blocked (ScienceDirect 403s, Unpaywall shows closed, scholar.archive.org blocked), but a person
with a browser can very likely just download the PDF — and that one file closes the n = 20 question
outright.

### ⚠️ A wrong load-bearing justification passed two reviews and is on `main`
`PR #23` (merged) · `issue #35` · claim held at `sketch`

The τ=2 proof is **sound** — independently confirmed, and machine-verified on 558 τ=2 instances
(all 3-vertex loopless digraphs, 3-vertex multidigraphs with multiplicities ≤ 2, a loop family,
4000 random 4–5 vertex multidigraphs) with zero failures.

But its **Schrijver-filter justification is factually wrong**, and `problems/woodalls-conjecture/RULES.md`
§1 makes the filter outcome a required part of the write-up. The PR argued unweightedness is used
in Lemma 1, since a weighted bridge arc could have weight 2. From Cornuéjols–Liu–Ravi §1, one may
assume $w \in \{0,1\}^A$ — a weight-$k$ arc becomes $k$ parallel weight-1 arcs — so a "weight-2
bridge" is two parallel arcs, i.e. bridgeless. **Lemma 1 holds verbatim under weights** and cannot
be the step the filter demands.

This is not cosmetic: **Schrijver's counterexample to Edmonds–Giles sits at minimum weight dicut
τ = 2**, so the weighted analogue of exactly this statement is known false. The filter is
maximally load-bearing at precisely this τ.

The real answer: a weighted packing needs $\chi^{J_+} + \chi^{J_-} \le w$, so a **weight-0 arc must
lie in neither part** — yet the construction colours every arc, and Lemma 2 supplies only one
crossing edge per direction, which may be that weight-0 arc. Weight-0 arcs cannot be deleted
(they still determine the dicuts), so this is exactly what the argument cannot survive.

**The process lesson is the finding.** Two reviewers approved it, one explicitly praising the
filter as passing "for a specific articulable reason rather than by assertion". The reason was
articulable *and wrong* — which is more dangerous than an absent one, because it looks like the
check was performed. A plausible mechanism invoking a real theorem is exactly what a language
model produces when it has not checked the reduction against the source.

Worth noting what did *not* catch it: this was found by a **second Opus pass**, not by the other
model family. Same-family review is not worthless — the decorrelation argument in `RULES.md` §5 is
about *raising* the odds, not guaranteeing them. It also means our two-tier `verified:review`
status is only as good as how hard the examiner actually attacks; two agreeing models remain the
weaker tier for good reason.

### Oler's inequality cannot settle any open case — kill-criterion triggered
`PR #21` · status `refuted` as an independent attack

The primary source was obtained and read (Cambridge Core scan of Oler, *CMB* **4** (1961) 153–155,
all three pages). Specialising the inequality to our formulation gives

$$s(n) \ge 2\sqrt3 + \sqrt{8n+1} - 3$$

which is tight exactly when $8n+1$ is a perfect square — i.e. **exactly at the triangular
numbers**, which are precisely the cases Oler already settled in 1961. For $n = 16, 17, 18$ it
falls 0.89 / 0.76 / 0.79 short of the best known construction. A circle has diameter 2, so Oler is
out by roughly **half a circle**.

Consequence: any future optimality proof needs something strictly beyond Oler. The published
small-$n$ proofs confirm this — none uses Oler as the engine past the triangular numbers. Melissen
uses hand-designed dissections plus pigeonhole; Joós spends 31 pages of case analysis on $n = 13$
alone. One $n$ per paper, over 60 years.

Honest limit recorded: for $n \ge 16$ the optimum is unknown, so slackness there is inferred from
published constructions, not proved. Labelled `numerical`.

### No float tolerance can be correct — the exact-arithmetic rule is empirically necessary
`PR #16` · `experiments/circle-packing-checker/tests/naive_float.py`

A float checker faces a genuine dilemma, not merely a precision preference:

- tolerance `0` **rejects the valid $n=10$ packing** — exact contact computes as
  `1.9999999999999998`, because $\sqrt3$ is not representable;
- the smallest tolerance admitting it (`1e-9`) **accepts a `1e-12` overlap** — and `1e-18`,
  and `1e-30`.

No tolerance does both jobs. This turns "use exact arithmetic" from a stylistic rule into a
demonstrated requirement.

### Lean: first machine-checked packing results
`PR #19` (merged) · status `verified:lean`

Feasibility of explicit packings for $n = 3$ and $n = 6$, all seven theorems printing exactly
`[propext, Classical.choice, Quot.sound]`. **Upper bounds only** — no optimality claim.

The load-bearing guard is `inTriangle_iff_mem_convexHull`: the half-plane definition is proved to
be *exactly* the convex hull of the three vertices, both directions. Without it, everything above
could have been proving something weaker while still building clean.

### Mathlib has essentially no polygon geometry
`PR #21` · checked against the actual checkout, not assumed

`grep -rli "perimeter"` over all of Mathlib returns **zero files**. `Geometry/Polygon/Basic.lean`
is a bare `Fin n → P` vertex structure with no area. No Jordan curve theorem, no shoelace formula,
no Delaunay triangulation; `GeometryOfNumbers.lean` has three theorems, all Minkowski.

Even *stating* Oler's inequality faithfully in Lean is blocked. This is the "large Mathlib gap"
case of `RULES.md` §4 and it constrains what the Lean gate can reach on this problem.

### The search is exact locally and runs out globally
`PR #25` · status `numerical`

Reproduces the published exact closed form for **every** $n = 3 \dots 15$ to 15–16 significant
digits, and matches 14 of 19 Graham–Lubachevsky records for $16 \le n \le 34$. **Nothing beat a
published record** — every deviation was in the safe direction.

The five misses are the actual finding: at $n = 26, 29, 32, 34$ it converged to 15 digits onto
packings **GL themselves rank second best** (`t26b`, `t29b63.2`, `t32b`, `t34c`). That is
basin-coverage failure, not convergence failure — restart counts fall from ~200 at $n=16$ to ~55 at
$n=32$. The local step is exact; the global search is what degrades past $n \approx 26$.

### Near-miss: a silent NaN would have faked convergence
`PR #25` · commit `851c496`

A degenerate SLSQP solve returned coincident points ($m = 0$) and crashed on $2/m$. **The crash was
the lucky outcome.** A `NaN` would have passed silently, because `NaN > best_m` evaluates to
`False` — the search would have frozen on its previous best and reported it as converged. Worth
remembering as a general pattern: comparison-guarded incumbent updates fail open on `NaN`.

### Cross-model review caught a claude error — twice, independently
`PR #20`, `PR #22` (both merged)

Our README claimed *"a dijoin is exactly a set of arcs whose reversal makes $D$ strongly
connected"*, offered as a coding aid. **False** — the correct characterisation is *contraction*;
reversal-sets are sufficient but not necessary.

Codex fixed the prose in one PR and independently avoided the trap in the other, whose
implementation *adds* reverse arcs rather than replacing them, with the directed path as
counterexample. Verified directly: replace-by-reversal is not strongly connected, add-reverses is.

Two independent catches of the same error, by the other model family, in two separate PRs. This is
the decorrelation argument in `RULES.md` §5 doing exactly its job — and the first time it caught
claude rather than the reverse. The bad line was load-bearing: an implementation built on it would
have been silently wrong.

### Literature: our own table was wrong in three ways
`PR #10` (merged)

Optimality is proven for **all $n \le 15$**, every triangular number, and $n = 20$. In correcting
this we found our previous table had: three values wrongly listed as disputed (Friedman marks
$n = 7, 8, 11$ as *proved*), and **$n = 11$ and $n = 12$ swapped**. The two genuine gaps closed
after Friedman's page was written — $n = 14$ by Payan (1997), $n = 13$ by Joós (online Sept 2020).

Cross-checked independently: Joós's $t_{13}$ maps to $11.40649585375161$ against our tabulated
$11.40649585375171$ — agreement to $10^{-13}$.

### ⚠️ Open question: is $n = 20$ actually proven?
`issue #14` · under investigation

Payan's own abstract says the $k = 6$ case *"can be extended"*, while Tedeschi & Mackey (2021) list
it flatly as proven. **Our README currently asserts the stronger claim**, on a secondary source.
If Payan's result is conditional, `main` is wrong. This would be the third time a secondary source
misled this repo.

**Follow-up, 2026-08-17 — settled in `PR #36`; see the entry at the top of this log.** Neither of
this entry's two guesses survived. The README no longer asserts the stronger claim flatly on a
secondary source: the $n = 20$ row is kept but qualified, carrying its provenance ("abstract only —
body not read"). And it did not turn out to be a secondary source misleading us a further time —
the newer entry declines that tally, because what actually happened is that our own *correction*
overshot, reading three sources' silences as denials. The standing position is **unverified —
neither proven by us nor disproven**.

---

## Standing gaps

- **The repo has no lower-bound artifact of any kind.** Every result so far is an upper bound (an
  explicit packing). Optimality needs lower bounds; `issue #27` is the first attempt at one, via
  pigeonhole partition certificates with rational vertices.
- An unreviewed 2024/25 preprint claiming a general Erdős–Oler proof was spotted during triage and
  deliberately **not** cited pending assessment (`issue #29`).
