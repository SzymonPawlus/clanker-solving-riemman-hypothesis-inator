# 2026-08-29 — inscribed equilateral triangle: literature landscape

Issue #132, lane: literature landscape. Files owned this session:
`problems/inscribed-equilateral-triangle/README.md` and this file. Nothing else touched; no git
command run (dispatcher commits centrally). Other lanes concurrently own that problem's
`RULES.md`, `attacks/`, `experiments/` — left alone.

## Headline

**The triangle peg problem is solved.** The brief's prior was right. Every Jordan curve inscribes
an equilateral triangle, and the sharper vertex-wise statement is settled with a sharp bound:
at most two points of a Jordan curve are vertices of no inscribed equilateral triangle, and two is
attained. This is the sharpest possible contrast with Toeplitz's square peg problem, which remains
open for general continuous Jordan curves.

## The thing that most constrains this write-up: I could not read anything

This is the finding I want on the record above the mathematics, because it caps how much the
README is worth.

`WebFetch` and `curl` are both blocked by the session egress proxy for every scholarly host I
tried. Confirmed blocked (403 on CONNECT for curl; `EGRESS_BLOCKED` for WebFetch):

    ams.org            arxiv.org          link.springer.com   matwbn.icm.edu.pl
    eudml.org          math.brown.edu     math.elte.hu        openproblemgarden.org
    en.wikipedia.org   zbmath.org         doi.org             semanticscholar.org
    api.semanticscholar.org               api.crossref.org    mathgenealogy.org
    bibliotekanauki.pl

Reachable: `api.github.com` (200), `raw.githubusercontent.com` (301), `github.com` (400). That is
the entire accessible internet from here. `curl -sS "$HTTPS_PROXY/__agentproxy/status"` shows
`enabled: true`, `selective: false`, no recent relay failures — this is policy, not a
misconfiguration, so per `/root/.ccr/README.md` I did not retry or route around it.

So **`WebSearch` was the only channel**. That returns real result listings (titles + URLs) plus a
synthesised summary of the snippets. I never saw a publisher page, an abstract page, or a PDF.
Every attribution in the README is therefore "reported consistently by several independent
secondary documents, seen only through search snippets" — which I coded **P2** in the README's
provenance column, defined explicitly there, and topped with a provenance warning. That is a
weaker level than the `n = 20` precedent in `problems/circle-packing-equilateral-triangle/README.md`
("abstract read, body not read"): I did not read even the abstract in situ. The README says so.

I considered downgrading every row below `cited`. I did not, because §3 `cited` means "established
in the literature, with a specific reference", and these results plainly are — the references exist,
the statements are reported identically by four unrelated documents (Schwartz's paper, the ELTE
thesis, the Gupta–Rubinstein-Salzedo paper, Springer's own record for Nielsen). What I did instead
is add a **Verification debt** section naming the five specific things a reviewer with network
access must open, and what to check in each. If that feels like too much hedging for a settled
1980 theorem: the alternative is to assert page ranges and theorem hypotheses I did not see, which
is exactly the failure §0 warns about.

## Searches run

1. `Meyerson "Equilateral triangles and continuous curves" Fundamenta Mathematicae 1980`
2. `Nielsen "Triangles inscribed in simple closed curves" Geometriae Dedicata 1992`
3. `Matschke "survey on the square peg problem" Notices AMS 2014 equilateral triangle Meyerson every Jordan curve`
4. `"Meyerson" 1980 "all but at most two points" Jordan curve equilateral triangle inscribed vertex`
5. `"Nielsen" 1992 ... dense set of vertices Geometriae Dedicata 43 291`
6. `every Jordan curve inscribed triangle similar to given triangle history Emch Meyerson Nielsen who proved first`
7. `Kronheimer "The tripos problem" JLMS 1981 inscribed triangle Jordan curve`
8. `arXiv 2102.03953 "Inscribed triangles of Jordan curves in" R^n abstract`
9. `"inscribed equilateral triangle" Jordan curve "sharp" obtuse isosceles ... Meyerson example`
10. `Matschke ... Notices 61 2014 ... statement of theorem`
11. `Schwartz "On Spaces of Inscribed Triangles" abstract ... enhanced version`
12. `Matschke ... volume 61 number 4 pages 346`
13. `square peg problem Toeplitz status 2026 still open solved ... recent progress`
14. `Meyerson ... "continuum" OR "non-Jordan" ... open question triangles`
15. `"Triangles and Quadrilaterals Inscribed in Jordan Curves" thesis Meyerson Nielsen theorem statement`
16. `Schwartz inscribed triangles "G(J)" uncountable set of shapes ... right isosceles`

Failed fetches (all `EGRESS_BLOCKED`): eudml.org/doc/211210; math.brown.edu tripeg.pdf;
ams.org Bulletin 2022 survey PDF; link.springer.com BF00151519; arxiv.org/pdf/1908.08174;
math.elte.hu thesis PDF; openproblemgarden.org inscribed_square_problem;
en.wikipedia.org Inscribed_square_problem.

## The brief's four bullets, checked

**Bullet 1 — "square peg is open in general". CORRECT.** Search 13 confirms: proven for convex,
piecewise analytic, $C^1$, bounded-total-curvature and other regularity classes; open for general
continuous Jordan curves, still, in 2026. Recent activity exists (a Greene–Lobb Lipschitz-constant
improvement reported 2024, a January 2026 preprint aimed at the $C^0$ case) but nothing reported as
a solution. I did **not** verify the 2026 preprint at all — it surfaced only as a Medium article
title. It is deliberately **not** in the README; a blog post is not a source for a status claim.

**Bullet 2 — "Meyerson (1980), Fund. Math. 110, 1–9, all but at most two points". CORRECT on every
component I could check.** Author is Mark D. Meyerson; title *Equilateral triangles and continuous
curves*; Fundamenta Mathematicae **110** (1980), no. 1, 1–9. The theorem as restated by Schwartz:
"all but at most 2 points of any Jordan loop are vertices of equilateral triangles inscribed in the
loop." Nothing in the brief's bullet 2 turned out to be wrong. Bibliographic detail and statement
agreed across four independent secondary documents.

**Bullet 3 — "Nielsen (1992), Geom. Dedicata 43, 291–297, every simple closed curve inscribes a
triangle of every similarity class". Bibliographically CORRECT; the credit is IMPRECISE.** Volume,
pages, year, journal and author (Mark J. Nielsen) all check out, `doi:10.1007/BF00151519`. But the
*existence* of an inscribed triangle of arbitrary prescribed shape was already known: two secondary
sources (the ELTE thesis and Gupta–Rubinstein-Salzedo) credit it to **Meyerson (1980)** and to
**Kronheimer & Kronheimer, "The tripos problem", J. London Math. Soc. (2) 24 (1981), 182–192**.
Nielsen's contribution is the *strengthening*: infinitely many similar triangles, and the vertex set
is **dense** in $J$. So citing Nielsen for bare existence is not false — his abstract states it —
but it misses a decade of priority. **Kronheimer & Kronheimer (1981) is a reference the brief did
not have, and it is the most useful new one I found.** I added it as its own row.

Also worth flagging so nobody conflates them: Nielsen's density statement does **not** imply
Meyerson's "all but at most two". Dense is much weaker than co-finite. The README says this
explicitly, because it is precisely the kind of slippage that would let someone "derive" Meyerson
from Nielsen and think the equilateral case was a corollary.

**Bullet 4 — "Matschke's survey very likely states the triangle case's status explicitly".
UNVERIFIED, and I would not bet on it.** I confirmed the survey exists (Notices Amer. Math. Soc.
61 (2014), no. 4) and that a search summary places Meyerson (1980) in its reference list. I could
**not** confirm the survey says anything about triangles in its body. It is a survey of the *square*
peg problem, and the one substantive theorem quoted back at me from it was Vaughan's rectangle
result, not a triangle result. The README lists it as an entry point with the coverage flagged
unconfirmed, and the Verification debt section makes checking it item 3. Also a small discrepancy I
could not resolve: page range reported as both **346–352** and **346–351**. Both are in the README.

## Other things found that the brief did not mention

- **Sharpness of the bound 2.** Reported as: the boundary of a suitable obtuse isosceles triangle
  has two points that are vertices of no inscribed equilateral triangle. I could not determine
  whether this example is Meyerson's own or a later restatement; the README says so rather than
  guessing. It makes the vertex-wise question not merely solved but *sharply* solved, which is why
  I gave it its own row.
- **Schwartz, *On spaces of inscribed triangles*, arXiv:1908.08174 (2019).** Enhanced Meyerson with
  topological content, plus: for each Jordan loop $J$ there is an *uncountable* set $G(J)$ of
  triangle shapes obeying the same all-but-two conclusion. This is the best pointer for anyone
  wanting a live question in this area.
- **Gupta & Rubinstein-Salzedo, arXiv:2102.03953 (2021).** Nielsen in $\mathbb{R}^n$, for a
  *restricted* set of triangles, plus a condition for a given point to be a vertex of an inscribed
  equilateral triangle. The restriction is where the remaining open ground is.
- One snippet asserted the all-but-finitely-many conclusion "is not known for any other shape of
  triangle (e.g. right isosceles)". Single source, unverified, and it sits awkwardly against
  Schwartz's uncountable $G(J)$ — possibly the snippet means "not known for *every* other shape".
  I did **not** put this in the README as a fact; the corresponding open item says "we do not know
  the status of this".

## Judgement calls in the README

- Statuses: everything substantive is `cited` with a provenance code. Exactly two things are
  labelled `sketch`, both mine, both explicitly marked non-load-bearing: (i) the elementary remark
  that three distinct pairwise-equidistant points cannot be collinear, so no separate
  nondegeneracy hypothesis is needed; (ii) the hand-wave about why three-point configurations are
  tractable and four-point ones are not. (ii) is the kind of sentence that hardens into folklore
  if left unlabelled, which is why it is labelled.
- I did **not** create `problems/inscribed-equilateral-triangle/attacks/` or `results/` — another
  lane owns those.
- The square peg campaign is referenced by issue range **#112–#131** only. There is no
  `problems/square-peg*` directory on this branch (`problems/` currently holds
  `circle-packing-equilateral-triangle`, `riemann-hypothesis`, `woodalls-conjecture`), so I did not
  invent a path to link to.
- The README's opening line says "solved" without hedging, because it is, and burying that behind
  qualifications would be its own kind of dishonesty. The hedging is about *which paper proved
  exactly what*, and lives in the provenance column where it belongs.

## What I would do next

Re-run this lane from an environment with real network access and close out the five Verification
debt items — Meyerson's body first, since it settles both the exact hypotheses and open item 3
(what "continuous curves" in the title covers). That is maybe an hour of reading and would move
this file from P2 to P0 across the board. Until then, treat the README as a well-sourced map drawn
without ever opening the atlas.
