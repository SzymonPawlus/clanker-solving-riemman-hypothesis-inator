# Findings

Running log of things worth a human's attention. Newest first. Agents append here when they find
something genuinely interesting — a result, a refutation, a near-miss, or an error in our own work.

**This is a highlights log, not a claims register.** Nothing here is citable. Every entry points at
the PR or file where the claim lives with its real status (`RULES.md` §3).

---

## 2026-08-21

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
