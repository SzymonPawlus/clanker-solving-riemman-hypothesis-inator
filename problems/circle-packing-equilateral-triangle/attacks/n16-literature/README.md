# Literature pass for the $n = 16$ covering bound — what search can and cannot settle

**Claim type: NEITHER.** No bound on $s(16)$, upper or lower, is asserted here. Problem
[`../../RULES.md`](../../RULES.md) §1 asks for that sentence first. Two bibliographic items are
proposed for promotion to `cited` (§3b below) and one repo figure is confirmed *unchanged*; nothing
else in this file is assumable.

- Author: `claude`, worker **L2** (Claude Opus 5 — convergent role, repo `RULES.md` §8: literature)
- Date: 2026-08-22 · Issue #97 · Branch `claude/circle-packing-subagents-9yg5gt`
- Subject: novelty of [`../n16-covering-2/`](../n16-covering-2/)'s $a_{16}\ge 1+2\sqrt3$, i.e.
  $s(16)\ge 2+6\sqrt3 = 12.392304845\ldots$

---

## 0. The egress boundary, measured — correcting a half-truth this campaign has repeated

Four workers have written "novelty unverifiable from this session — scholarly hosts are blocked".
Measured today, that is **half right**:

| channel | result today | evidence |
|---|---|---|
| `WebFetch` | **blocked, universally** | 4 probes, 4 × `{"error_type":"EGRESS_BLOCKED"}`: `ris.utwente.nl`, `mathworld.wolfram.com`, `research.utwente.nl`, `www.inf.u-szeged.hu`. The last three were **not** on [`../eo-literature/`](../eo-literature/) §1's blocklist, so the block is not a curated list — it is everything. |
| `WebSearch` | **works** | 17 queries, all returned result lists |

So this session has **bibliographic egress but no textual egress**. That is enough to settle
volume/page/year questions and to establish that a paper exists and roughly what its abstract
announces. It is **not** enough to read a proof, a table of numbers, or a definition. Every finding
below sits on the bibliographic side of that line, and each is labelled accordingly.

### Provenance vocabulary used here

The repo's ladder (`../../README.md`) is *primary read in full* > *primary abstract only* >
*review of the primary* > *secondary survey*. Everything obtained today is **below** all four of
those. Two new rungs, and I use them literally:

- **`search-result item`** — the title/URL/venue as returned in a `WebSearch` result list. This is
  a machine-emitted record, comparable in reliability to a repository's metadata field, which
  `FINDINGS.md` 2026-08-18 establishes is *derived data*, not the publication.
- **`search-backend summary`** — the prose the search tool writes from snippets. It is a **language
  model paraphrasing text neither of us has seen**. It is the weakest evidence in this repo's
  history and is used below only to name leads and to state what a paper is *about*.

**Nothing in this file is a substitute for a PDF, and none of it should be quoted as if a paper
said it.** Where I give a verbatim-looking sentence, it is verbatim *from the search backend*, not
from the source.

---

## 1. Q1 — Is there a published *lower* bound for $n = 16$ better than Oler's?

**Answer: not determined, and one specific unread paper is the reason.** No published lower bound
for $s(16)$ above Oler's $11.821918$ surfaced in eleven queries aimed at it. But a *documented
negative search is not a negative result*, and there is one live candidate I could not read.

### 1a. What is confirmed about the shape of the field

Every query about $n = 16$ optimality returned the same picture, from independent hits
(Wikipedia, the Szeged global-optimisation survey, Melissen–Schuur's own listing, Tedeschi &
Mackey): **optimality is proved for $n \le 15$, for triangular $n$, and for $n = 20$; $n = 16$ is
construction-only.** One search-backend summary of the Tedeschi & Mackey PDF renders their
statement as

> "Configurations that maximize the minimum distance between $n$ points in an equilateral triangle
> have been proven for $n \le 12$, $n = 14$, $20$, and $n = k(k+1)/2$ for any $k \in \mathbb{N}$."

*(provenance: `search-backend summary` of `ajuronline.org` PDF; **corroborates** `../../README.md`'s
account that T&M's body asserts $n = 20$ — it is not a new warrant for it.)*

**Oler's inequality itself was independently re-derived from search today** and it checks out
against the repo's number. A summary of the Graham–Lubachevsky arXiv copy gives Oler as
$p(K) \le \tfrac{2}{\sqrt3}A(K) + \tfrac12 P(K) + 1$, inverting for the equilateral triangle to
$$L(n) \ \ge\ \tfrac12\left(-3+\sqrt{8n+1}\right).$$
At $n = 16$: $(-3+\sqrt{129})/2 = 4.17890834\ldots$, and $2 \cdot 4.17890834 + 2\sqrt3 =
11.8219185$ — **exactly the repo's Oler row**. *(provenance: `search-backend summary`; the
arithmetic is mine and is a consistency check, not a citation.)* This does not promote anything —
the repo already has Oler `cited` from a full read — but it is a cheap independent confirmation
that the campaign's baseline is the right number.

### 1b. The one candidate that could overturn this — **unread, and it must be read**

> **Gáspár, Zs. and Tarnai, T., *Upper bound of density for packing of equal circles in special
> domains in the plane*, Periodica Polytechnica Civil Engineering (Budapest).**
> `pp.bme.hu/ci/article/view/648`, PDF at `pp.bme.hu/ci/article/download/648/403/4701`.

This is the closest thing found to published competition for the campaign's bound, and it is
directly on target. From the search-backend summary of its abstract:

- it gives upper bounds on the **packing density** for equal circles in *a square, **an equilateral
  triangle**, and a circle* — an upper bound on density for fixed $n$ **is** a lower bound on
  $s(n)$;
- it uses **Groemer's and Oler's inequalities** as its starting point and refines the boundary
  interstice area, so its bounds are *by construction* at least as strong as Oler's;
- "the obtained upper bounds are **sharper than those known before**";
- "**numerical values are listed up to 30 circles**" — so **there is a printed number for $n = 16$
  in that paper**;
- and the summary describes the bounds as **heuristic**.

*(Provenance: `search-backend summary` of the abstract, plus two `search-result item`s for the
journal page and the PDF. The body was not obtained — `pp.bme.hu` is blocked, and
[`../eo-literature/`](../eo-literature/) §2.2 already recorded it blocked.)*

**Why this is the whole of Q1.** If that table's $n = 16$ entry is a rigorous bound above
$12.392305$, this campaign's result is a rediscovery of something weaker than the state of the art.
If it is below $12.392305$, or if "heuristic" means what it usually means and the bounds are not
proofs, the campaign's bound stands as the best *rigorous* one this project knows of. **One page of
one PDF decides it, and I could not fetch that page.** I am not going to guess which way it falls
from the word "heuristic" in a paraphrase of an abstract.

### 1c. What was checked and found empty

- **Melissen's 1997 Utrecht thesis** *Packing and covering with circles* — confirmed to exist
  (`search-backend summary`, Utrecht University, 1997) and confirmed **not obtainable**; consistent
  with `../../README.md`'s 2026-08 attempt and `../eo-literature/` §2.4. If it contains lower bounds
  for $n \ge 16$ absent from the papers, that is invisible from here.
- **Joós** — nothing for $n = 16$. His published triangle result is $n = 13$ only.
- **Nurmela & Östergård** — their triangle work that surfaced is **coverings**, not packing lower
  bounds (see §2c); their packing work is the *square*.
- **Payan** — nothing beyond `../../README.md`. Body still not obtained.
- **Markót's interval-arithmetic optimality proofs** ($n = 28,\dots,33$) are for the **unit
  square**. No analogous computer-assisted optimality proof for the *triangle* surfaced.
- **The Locatelli–Raber trap fired again.** A search-backend summary today, again inside a
  discussion of the equilateral triangle, said *"in 2002 optimal solutions were provided for
  $n \le 35$ by Locatelli and Raber"*. `../eo-literature/` §2.3 already identified this as a
  **square** result being mis-attached to the triangle. **It reproduced verbatim.** Treat it as a
  known contaminant of this topic's search results, not as evidence.

---

## 2. Q2 — Is the covering/pigeonhole method, applied to this problem, published?

**Answer: the method, yes — emphatically. The specific 15-piece subdivision and the constant
$1+2\sqrt3$, not found.**

### 2a. R1's claim about Melissen (1993), verified independently

R1 reported that Melissen proved $n = 4\ldots12$ "using only partitions and direct applications of
Dirichlet's pigeon-hole principle", attributed to Tedeschi & Mackey. I re-ran that search without
looking at R1's wording and got the same sentence back:

> "In a 1993 paper, Melissen proved the optimal placements of 4 through 12 points in an equilateral
> triangle using only partitions and direct applications of Dirichlet's pigeon-hole principle."

*(provenance: `search-backend summary`, sourced to the Tedeschi & Mackey AJUR PDF, which
`../../README.md` records as **read in full** by this project — so this specific sentence is
recoverable from a source the repo already holds, and a worker with that PDF can upgrade it to
*secondary survey, read* in one minute. I did not read it today.)*

**Consequence for the campaign, and it is not small.** The method of
[`../n16-covering-2/`](../n16-covering-2/) — subdivide $T_a$ into $n-1$ pieces of diameter $<1$,
pigeonhole — is **exactly Melissen's published method**, applied to a larger $n$. So:

> Whatever the status of the *number* $1+2\sqrt3$, the *technique* is thirty-three years old and
> belongs to Melissen. The campaign's write-ups should say so.

There is also a structural remark worth recording. Melissen's pigeonhole proofs for $n \le 12$ are
*tight* — they reach the true optimum. The 15-piece bound reaches only $4.4641$ against the
best-known $4.6248$, so **the same method demonstrably does not close $n = 16$**, which is
consistent with $n = 16$ having stayed open for 30 years while the method was public. That is
indirect evidence *for* the campaign's own conclusion in "Why this is where the family stops", and
it is the most useful thing this literature pass can tell the provers.

### 2b. The specific subdivision, and the constant

**Nothing found.** No source, at any level, mentioning a 15-piece diameter-limited subdivision of
an equilateral triangle, or the value $1+2\sqrt3 = 4.4641016$, or $1/(1+2\sqrt3) = 0.2240092$, in
this context. Queries in §4.

Two adjacent named problems were checked and are **not** it:

- **Borsuk number / diameter partition.** Settled and useless here: for any bounded planar set the
  Borsuk number is $\le 3$ (Borsuk 1932 for $n = 2$; conjecture false for $d \ge 298$,
  Hinrichs–Richter). *(provenance: `search-backend summary` + Wikipedia `search-result item`.)* The
  Borsuk question is *qualitative* — "into how few parts of **strictly smaller** diameter" — and the
  answer is 3 for any planar set of any size. It says nothing about "diameter $< 1$ for a triangle
  of side $a$", which is the quantitative question the campaign needs. **The Borsuk literature does
  not settle $A_{15}$ and cannot.**
- **Diameter-minimising partitions of polygons.** Damian & O'Rourke, *Partitioning Regular Polygons
  into Circular Pieces I/II* (arXiv `cs/0304023`, `cs/0412095`), and Abrahamsen, *Partitioning a
  Polygon Into Small Pieces* (arXiv `2211.01359`) exist and are about partitioning regular polygons
  into small pieces — but Damian–O'Rourke minimise **aspect ratio**, not diameter.
  *(`search-result item` + `search-backend summary`; none read.)* One summary line —
  "it seems out of reach to efficiently compute optimal diameter partitions of an equilateral
  triangle" — is tantalising and I could not attach it to a source sentence, so **do not quote it**.

### 2c. The lead I would chase next, and it is a good one

There **is** a substantial published literature on the covering side, and it produces numbers
directly comparable to $A_{15}$:

> If an equilateral triangle of side $a$ can be covered by 15 circles of radius $r < 1/2$, then it
> is covered by 15 sets of diameter $< 1$, so $a_{16} \ge a$. Equivalently, if $s_{\rm cov}(15)$ is
> the largest equilateral triangle coverable by 15 **unit** circles, then $a_{16} \ge
> s_{\rm cov}(15)/2$.

That quantity is tabulated in published and semi-published sources:

| source | what it would give | obtained? |
|---|---|---|
| **K. J. Nurmela, *Conjecturally optimal coverings of an equilateral triangle with up to 36 equal circles*, Experimental Mathematics **9**(2) (2000) 241–250** (Project Euclid `em/1045952348`; EUDML 226818) | the $n = 15$ covering radius directly | **no** — Project Euclid not fetchable |
| **J. B. M. Melissen, *Loosest circle coverings of an equilateral triangle*, Mathematics Magazine **70** (1997)**, April 1997 issue; page range reported as **118–124** in one place and **119–125** in another — *unresolved, see §3c* | same family | **no** |
| **Melissen & Schuur, *New circle coverings of an equilateral triangle*** (PDF at `ris.utwente.nl/ws/files/280923669/Melissen1997new.pdf`) | same family | **no** — host blocked |
| **Erich Friedman, *Circles Covering Triangles*** (`erich-friedman.github.io/packing/circovtri/`) — described in a `search-result item` as showing "$n$ unit circles covering the largest known equilateral triangle (of side $s$)" | $s_{\rm cov}(15)$ as a decimal, immediately | **no** — value not in any snippet |

*(All four: `search-result item` only, none read.)*

**This is a concrete, cheap, high-value next step** and nobody in the campaign has taken it. It
does not need a paywalled PDF — Friedman's page is a public HTML table. A crude hexagonal estimate
suggests circle coverings will land *below* $4.4641$ (circles waste area where the 15-piece
subdivision does not), which would make it a clean corroboration rather than competition; **but
that is my arithmetic on an unread number and it is `sketch`, so do not report it as a finding.**

---

## 3. Q3 — The two open provenance items

### 3a. Melissen & Schuur's volume: **145 is right, and the repo already has it right**

The briefing asked me to settle 145 vs 142 and report a correction. **There is no correction to
make.** Reproduced today:

| query | volume returned | associated host |
|---|---|---|
| neutral query naming the paper | **145**(1–3), 333–342, 1995 | ScienceDirect / `ris.utwente.nl` PDF |
| a second neutral query | **145**, 1995, 333–342 | cited inside `pp.bme.hu` |
| query with `"142"` forced into it | **142**(1–3), 333–342, DOI `10.1016/0012-365X(95)90139-C` | `research.utwente.nl` (Pure record) ranked first |

That third row is **exactly the failure mode `FINDINGS.md` 2026-08-18 documents**: the University
of Twente Pure record's DOI, issue and pages are correct and only its *volume* field is corrupt, and
the same institution hosts the publisher PDF whose front matter reads 145. I reproduced the corrupt
record without knowing which host it would come from, and it came from the predicted host.

> **For the manager: this is a no-op, and the interesting part is that it is a no-op.** The 142
> sighting that prompted this question is the third recorded encounter with the same corrupt field.
> `../../README.md`'s "**145**(1–3) (1995) 333–342" is correct and must **not** be changed.
> `FINDINGS.md` 2026-08-18's rule — publisher front matter and CrossRef outrank repository metadata
> — held on a live test today.

### 3b. Two citations promoted from "remembered" — with a caveat that matters

[`../n16-covering-limit/`](../n16-covering-limit/) §5 lists two results it had to treat as
*remembered, not `cited`*. Both bibliographic records are now corroborated at
`search-result item` + `search-backend summary` level:

**(i) Graham's largest small hexagon — reference confirmed, value confirmed.**

> R. L. Graham, *The largest small hexagon*, **Journal of Combinatorial Theory, Series A 18 (1975)
> 165–170**. ScienceDirect PII `0097316575900047`.

The search backend renders the paper's own framing as: the problem of "the largest area a plane
hexagon of unit diameter can have", raised ~20 years earlier by **H. Lenz**; the optimal hexagon is
**unique** and has area exceeding the regular unit-diameter hexagon "by about 4%". Consistency
check, mine: $0.674981/(3\sqrt3/8) = 0.674981/0.649519 = 1.0392$ — **+3.9%, matching "about 4%"**.
So the value $A_6 = 0.674981\ldots$ that `n16-covering-limit` was carrying from memory is
corroborated by an independent statement about the same quantity.

**(ii) Fejes Tóth's *Lagerungen* — book confirmed; the *statement* is confirmed only in a narrower
form, and the narrowing is load-bearing.**

> L. Fejes Tóth, *Lagerungen in der Ebene, auf der Kugel und im Raum*, **Grundlehren der
> mathematischen Wissenschaften 65, Springer, Berlin, 1953, x + 197 pp.** Reviewed by H. S. M.
> Coxeter, Bull. Amer. Math. Soc., March 1954 (`ams.org/journals/bull/1954-60-02/...`; Project
> Euclid `euclid.bams/1183518610`). Springer reprint `10.1007/978-3-662-01206-2`.

**Caveat — read this before promoting anything.** `n16-covering-limit` §5 states the hexagon bound
for coverings as: *if a convex hexagon $H$ is covered by convex sets $C_i$ then
$|H| \le \sum_i h(C_i)$* — i.e. for **arbitrary, distinct** convex sets. What surfaced today, in
two independent summaries of *other* papers restating Fejes Tóth, is narrower:

> "if **non-crossing congruent copies of a convex disc $K$** cover a convex hexagon $H$, then the
> density of the discs relative to $H$ is at least $\operatorname{area}K / f_K(6)$, where $f_K(6)$
> is the maximum area of a hexagon contained in $K$"

and, in the density formulation, $\theta_T(K) \ge A(K)/A(h_{\max})$ — again for **one** convex disc
$K$ and its congruent copies. *(Both: `search-backend summary`.)*

> **This is a real gap, not pedantry.** The 15 pieces in this campaign's coverings are **not
> congruent copies of one set** — they are 3 quadrilaterals, 9 pentagons and 3 hexagons of five
> different areas. The congruent-copies form of the hexagon bound **does not apply to them.** The
> general form may well be true and in the book; I have no evidence either way, because I have not
> seen the book. **Do not promote the general form to `cited` on the strength of this file.** What
> §3b(ii) supplies is the book's bibliographic record, nothing more.

**(iii) The isodiametric (Bieberbach) inequality — a reference at last.**

Used throughout this campaign as `cited` with no reference at all. The standard one:

> L. Bieberbach, *Über eine Extremaleigenschaft des Kreises*, **Jahresbericht der Deutschen
> Mathematiker-Vereinigung 24 (1915) 247–250**. EUDML `doc/145444`.

*(provenance: `search-backend summary` giving all five fields, plus an EUDML `search-result item`
for the exact title.)* The statement — a convex body of diameter $\le d$ has area $\le \pi d^2/4$,
with equality only for the disc — is textbook and appears in every convex-geometry source; the
*gap* the campaign had was a reference, not a doubt. Note the fields above are **not** confirmed
against CrossRef or publisher front matter (both blocked), so by `FINDINGS.md`'s own ladder this is
below the standard that settled the Melissen–Schuur volume. It is offered as *the* reference to
cite, to be spot-checked by the first worker with egress.

### 3c. One new, small discrepancy found today

The Melissen *Mathematics Magazine* covering paper's page range came back **two different ways in
one summary**: "**70** (1997), pages **119–125**", with the same summary noting "some sources cite
the page range as **118–124**". Unresolved. It does not affect anything in the repo (that paper is
not cited anywhere here), but if §2c's covering lead is taken up, settle it before citing.

---

## 4. Q4 — The honest verdict on novelty

> **Cannot be determined from search results alone.** Specifically: **not shown to be known, and
> not shown to be new.** The campaign should keep [`../n16-covering-2/`](../n16-covering-2/)'s own
> instruction — *"Assume this is known"* — but may now soften it from "unverifiable" to "one
> specific unread paper decides it".

Decomposing the question, because the three parts have different answers:

| sub-question | verdict | basis |
|---|---|---|
| Is the **method** (partition + pigeonhole for this problem) published? | **Yes — Melissen (1993), $n = 4\ldots12$.** Not novel. | §2a, corroborated independently today |
| Is a **lower bound for $s(16)$ above Oler's** published? | **Undetermined.** None found in 11 targeted queries; one live candidate (Gáspár–Tarnai) unread and known to print a number for every $n \le 30$. | §1b |
| Is the **value $1+2\sqrt3$** or the 15-piece subdivision published? | **Not found.** Documented negative across 6 queries; weak evidence, and a search engine's silence is not a denial. | §2b, §5 |

**What would settle it, in decreasing order of cost-effectiveness:**

1. **The Gáspár–Tarnai PDF** (`pp.bme.hu/ci/article/download/648/403/4701`, open access, one
   click in a browser). Read its numerical table at $n = 16$ for the equilateral triangle, and read
   whether the bounds are asserted as proved or as heuristic. **This single file is 80% of Q1.**
2. **Friedman's `circovtri` page** — a public HTML table; gives $s_{\rm cov}(15)$ and hence an
   immediately comparable published-derived bound (§2c). Costs seconds with any browser.
3. **Melissen's 1997 Utrecht thesis.** The one place a lower bound for $n \ge 16$ would plausibly
   sit unpublished-elsewhere. Repeatedly unobtainable; needs a library.
4. **Nurmela, Exp. Math. 9 (2000) 241–250** — the $n = 15$ covering radius, same comparison as (2)
   but from a refereed source.
5. **Melissen (1993) Monthly, pp. 916–925** — to see the actual dissections and check whether any of
   them is the campaign's configuration at smaller $n$, and whether he states a general $A_m$.

**One thing the campaign should stop saying.** "Novelty unverifiable from this session — scholarly
hosts are blocked" is now inaccurate in its second clause. Bibliographic verification works;
textual verification does not. The correct sentence is *"the bound could not be compared against
Gáspár–Tarnai's tabulated bounds, which are the only published competitor identified"*.

---

## 5. Queries tried that returned nothing useful

Recorded so nobody repeats them. All via `WebSearch`, 2026-08-22.

**On a better lower bound for $n = 16$ (Q1) — all returned only "proved for $n\le15$" restatements:**
1. `lower bound packing 16 circles equilateral triangle optimality proof`
2. `"equilateral triangle" circle packing improved lower bound Oler inequality n=16 17 18 not triangular`
3. `Joós packing 16 circles equilateral triangle proof optimal`
4. `"equilateral triangle" packing 16 circles best known "12.713" OR "4.6247" optimality open` — *neither numeral appeared in any result*
5. `improvement of Oler's inequality lower bounds equal circles equilateral triangle rigorous bounds table n=16`
6. `Markót interval arithmetic verified optimality circle packing equilateral triangle computer-assisted proof` — *all hits are the unit square*
7. `Nurmela Östergård packing circles equilateral triangle` — *returns their covering work and their square work; no triangle packing bounds*
8. `Erdős Oler conjecture k=7 n=27 equilateral triangle circle packing progress since 1997` — *nothing past the repo's state; reproduced the Locatelli–Raber contaminant*
9. `Melissen "Packing and covering with circles" thesis Utrecht 1997 lower bounds triangle` — *thesis confirmed to exist, no content*
10. `Amore "circle packing in regular polygons" 2022 triangle bounds optimal packings n=16` — *constructions only, by the paper's own description*
11. `Tarnai Gáspár upper bound packing density equilateral triangle 16 circles numerical values table 30 circles` — *confirms the table exists; does not show it*

**On the covering constant and the subdivision (Q2):**
12. `partition equilateral triangle into n parts of smaller diameter Borsuk number triangle minimum diameter partition`
13. `divide equilateral triangle into n pieces minimizing maximum diameter partition smallest diameter`
14. `"sets of diameter" cover equilateral triangle pigeonhole lower bound maximum minimum distance points triangle` — *returns Lebesgue universal cover and opaque-set literature; unrelated*
15. `"largest equilateral triangle" divided into n parts of diameter 1 pieces smaller diameter known values` — *the search backend could not parse the question and answered about circle packing instead; this phrasing is a dead end*
16. `Melissen dissection pigeonhole method lower bound "equilateral triangle" points minimum distance eleven pieces subdivision proof technique` — *confirms the method, not the pieces*
17. `covering an equilateral triangle with 15 equal circles smallest radius Friedman circles covering triangles table` and
    `"Circles Covering Triangles" Erich Friedman 15 unit circles largest equilateral triangle side length s=` — *both find the page, neither surfaces the number*

**Negative result, stated as such:** no source at any level was found that states a lower bound for
$s(16)$ other than Oler's, or that states the value $1+2\sqrt3$ in this context. Per
`FINDINGS.md` 2026-08-17, **that is not a denial** — it is the absence of a hit, from a channel that
cannot see inside PDFs, on a question whose one live candidate is a PDF.

---

## 6. Reference table — everything touched today

| reference | what it says | provenance | how obtained |
|---|---|---|---|
| Gáspár & Tarnai, *Upper bound of density for packing of equal circles in special domains in the plane*, Periodica Polytechnica Civil Eng. | Refines Groemer/Oler with sharper boundary-interstice areas; upper density bounds for **square, equilateral triangle, circle**; numerical values **listed up to 30 circles**; described as *heuristic* | **`search-backend summary` of abstract** — body NOT obtained | `WebSearch` ×3; `pp.bme.hu` blocked to `WebFetch` |
| Oler, Canad. Math. Bull. **4** (1961) 153–155 | $p(K)\le\frac{2}{\sqrt3}A+\frac12P+1$; for the triangle $L(n)\ge\frac12(-3+\sqrt{8n+1})$ | `search-backend summary`; **repo already holds a full read** | `WebSearch`; arithmetic check mine |
| Melissen, Amer. Math. Monthly **100** (1993) 916–925 | Optimal placements $n = 4\ldots12$ "using only partitions and direct applications of Dirichlet's pigeon-hole principle"; conjectures $n = 13,14,17,19$ | `search-backend summary`, sourced to the T&M PDF | `WebSearch` ×2 |
| Melissen & Schuur, Discrete Math. **145**(1–3) (1995) 333–342 | Constructions for $n = 16,17,18$ by simulated annealing + quasi-Newton "supplemented with some human intelligence" | `search-result item` + `search-backend summary`; repo holds a read | `WebSearch` ×3, incl. the adversarial "142" query |
| Tedeschi & Mackey, AJUR **18**(2) (2021) 3–12 | "proven for $n\le12$, $n=14$, $20$, and $n=k(k+1)/2$"; Melissen's method; Payan 1997 $n=14$; Joós 2020 $n=13$ | `search-backend summary`; **repo holds a full read** | `WebSearch` ×3 |
| Graham, *The largest small hexagon*, JCTA **18** (1975) 165–170 | Max area of a unit-diameter hexagon; unique optimum; ~4% above the regular one; problem due to H. Lenz | `search-result item` + `search-backend summary` | `WebSearch` |
| Fejes Tóth, *Lagerungen in der Ebene, auf der Kugel und im Raum*, Grundlehren 65, Springer 1953, x+197 pp | Book confirmed. Hexagon bound found only in the **congruent-copies-of-one-disc** form (§3b(ii)) | `search-result item` (book) + `search-backend summary` (statement, from *other* papers) | `WebSearch` ×2 |
| Bieberbach, *Über eine Extremaleigenschaft des Kreises*, Jahresber. DMV **24** (1915) 247–250 | The isodiametric inequality | `search-backend summary` + EUDML `search-result item` | `WebSearch` |
| Nurmela, Exp. Math. **9**(2) (2000) 241–250 | Conjecturally optimal coverings of an equilateral triangle, up to 36 equal circles; 19 new or improved | `search-result item` + `search-backend summary` | `WebSearch` |
| Melissen, *Loosest circle coverings of an equilateral triangle*, Math. Mag. **70** (1997), April issue, pages **118–124 or 119–125 (unresolved)** | Covering counterpart | `search-result item` | `WebSearch` |
| Melissen & Schuur, *New circle coverings of an equilateral triangle* | Covering counterpart | `search-result item` only | `WebSearch`; `ris.utwente.nl` blocked |
| Friedman, *Circles Covering Triangles*, `erich-friedman.github.io/packing/circovtri/` | "$n$ unit circles covering the largest known equilateral triangle (of side $s$)" | `search-result item` | `WebSearch` ×2; value not surfaced |
| Borsuk literature (Wikipedia; Hinrichs–Richter arXiv `0712.4009`) | Planar Borsuk number $\le3$; false for $d\ge298$ | `search-result item` + `search-backend summary` | `WebSearch` |
| Damian & O'Rourke, arXiv `cs/0304023`, `cs/0412095`; Abrahamsen arXiv `2211.01359` | Partitioning regular polygons into small pieces — **aspect ratio**, not diameter | `search-result item` | `WebSearch` |
| Graham & Lubachevsky, arXiv `math/0406252` / Electron. J. Combin. **2** #A1 | $22\le n\le34$; source of the Oler restatement above; repo holds a read | `search-result item` | `WebSearch` |
| Locatelli & Raber (2002) | **The square, not the triangle.** Recorded only as a contaminant that reproduced today | `search-backend summary` | `WebSearch` |
| Markót, SIAM J. Optim. / Computing | Interval-arithmetic optimality, **unit square**, $n=28,\dots,33$ | `search-backend summary` | `WebSearch` |
| Academia.edu 129891186 / ResearchGate 387465203 | **Deliberately not used** (issue #29). Still dominates ranking; hit again today | — | — |

---

## 7. Corrections to repo files — for the manager to route

I own only this directory (and my notebook). Each item below names the file, the text, and the
proposed replacement. **None is applied.**

### C1 — `problems/circle-packing-equilateral-triangle/README.md` — **NO CHANGE. Do not "fix" the volume.**
- Current: "Melissen & Schuur, Discrete Math. **145**(1–3) (1995) 333–342"
- Proposed: **unchanged.** 145 is correct; the 142 sighting is the `research.utwente.nl` Pure
  record's corrupt volume field, reproduced under controlled conditions today (§3a). This is the
  third encounter. Consider adding, in `../../README.md`'s provenance table row for that paper, the
  half-sentence *"(the Twente Pure record's volume field reads 142 and is wrong — see
  `FINDINGS.md` 2026-08-18)"* so the fourth encounter costs nobody an hour.

### C2 — `attacks/n16-covering-limit/README.md` §5 — two bullets can be upgraded, one only partly
- Current: "**Graham's 'biggest little hexagon'** — … (R. L. Graham, *The largest small hexagon*,
  J. Combin. Theory Ser. A **18** (1975) 165–170)" under the heading "Two citations I could **not**
  verify".
- Proposed: move to a verified footing with the provenance label *"bibliographic record confirmed at
  search-result level 2026-08-22 (`attacks/n16-literature/` §3b(i)); body not read"*. The value
  $A_6 = 0.674981$ is corroborated by the independent "~4% above the regular hexagon" statement.
- Current: the Fejes Tóth bullet, stated for **arbitrary convex sets $C_i$**.
- Proposed: keep it as **not `cited`**, and add the caveat from §3b(ii): the form recoverable today
  is for **non-crossing congruent copies of a single convex disc**, which does **not** cover this
  campaign's 15 non-congruent pieces. The book's bibliographic record (Grundlehren 65, Springer,
  1953, x+197 pp) can be added; the *statement* cannot.

### C3 — every file using the isodiametric inequality — supply the missing reference
- Current: used as `cited` with no reference (`n16-covering-limit` §"the only imported mathematics",
  `eo-covering-bound`, and others).
- Proposed: attach **L. Bieberbach, *Über eine Extremaleigenschaft des Kreises*, Jahresber. Deutsch.
  Math.-Verein. **24** (1915) 247–250**, flagged *"fields from a search-backend summary, not yet
  checked against CrossRef"*.

### C4 — `attacks/n16-covering-2/README.md` "What this is worth, stated precisely"
- Current: "**Novelty UNVERIFIED and unverifiable from this session.** Scholarly hosts are blocked
  at the egress proxy."
- Proposed: "**Novelty UNDETERMINED.** `WebSearch` works even where `WebFetch` and `curl` do not;
  a bibliographic pass (`attacks/n16-literature/`) found (a) the *method* is Melissen's, published
  1993 for $n=4\ldots12$, so the technique is not new; (b) no published lower bound for $s(16)$
  above Oler's, in 11 targeted queries; (c) one live candidate that could contain one —
  Gáspár & Tarnai, Periodica Polytechnica Civil Eng., which tabulates density upper bounds for the
  equilateral triangle for every $n \le 30$ and could not be read here. **Assume this is known
  until that table is checked.**"

### C5 — `attacks/eo-literature/README.md` §1 — the operational advice is now wrong
- Current: "**Consequence for the team.** Any literature task in a session with this egress profile
  will return nothing, however it is attempted."
- Proposed: "…will return **no source text**. Bibliographic work — volumes, pages, years, whether a
  paper exists and what its abstract announces — **does** succeed via `WebSearch`, as
  `attacks/n16-literature/` demonstrates. Probe `WebFetch` once to learn which of the two kinds of
  literature task is possible."

### C6 — `../../README.md` "Remaining gaps" — one entry to add
- Proposed addition: "**Gáspár & Tarnai (Periodica Polytechnica Civil Eng.) not obtained.** It
  tabulates density-based upper bounds for the equilateral triangle for every $n \le 30$, refining
  Groemer and Oler. It is the only identified published source that might contain a lower bound on
  $s(16)$ stronger than Oler's, and its abstract calls its bounds *heuristic*. Open access at
  `pp.bme.hu`; blocked to automated fetch, trivial for a human with a browser."

---

## 8. What this changes for the provers, today

- **The technique is not novel.** Stop describing the pigeonhole/covering route as an original
  idea; describe it as Melissen's method pushed to $n = 16$. Nothing about the campaign's
  arithmetic is affected.
- **The bound's novelty is one PDF away from being settled**, in either direction.
- **A cheap comparison number exists and nobody has fetched it** (§2c): the best known 15-circle
  covering of an equilateral triangle. It bounds $a_{16}$ from below by a completely independent,
  published route.
- **Nothing here is assumable.** Two bibliographic records (§3b) are offered for promotion and are
  the only candidates; the Fejes Tóth *statement* is explicitly **not** among them.
