# Literature pass for Erdős–Oler $k = 7$ — a null result, and the reason

**Claim type: neither.** No bound on $s(n)$, upper or lower, is claimed here, and no source is
promoted to `cited`. Problem [`../../RULES.md`](../RULES.md) §1 asks for that sentence first; here
it is literally true, because **nothing was obtained**.

- Author: `claude` (Claude Opus 5 — convergent role, repo `RULES.md` §8: literature), 2026-08-21
- Branch: `claude/circle-equklatetal-problem-sa7tx7`
- Targets: Payan (1997) body; published work on Erdős–Oler for $k \ge 7$; Folkman & Graham
  (Canad. Math. Bull.); Melissen's 1997 Utrecht thesis; Joós (2021)

| Target | Obtained | Status of anything below |
|---|---|---|
| Payan (1997) body | **nothing** | unchanged from `main` |
| Erdős–Oler for $k \ge 7$ | **nothing beyond what `../../README.md` already records** | unchanged |
| Folkman & Graham | **nothing** (bibliographic detail only, at search-index level) | not `cited` |
| Melissen thesis 1997 | **nothing** | unchanged |
| Joós (2021) | **nothing** | unchanged |

**Read in this session: zero primary sources, zero secondary sources, zero abstracts.** Everything
in §2 below is at the level of *a search engine's result list*, which is weaker than every tier of
evidence this repo has previously relied on — weaker than a zbMATH review, weaker than a
repository's generated metadata (the thing `FINDINGS.md` 2026-08-18 warns about). It is recorded so
the next worker does not repeat the attempts, not so it can be built on.

---

## 1. Why: this session has no scholarly egress at all

This is the finding. It is not "some publishers are blocked"; it is **near-total**.

Two independent channels were tested and both fail the same way:

- **Bash / `curl`** — the local agent proxy returns `connect_rejected`,
  `"gateway answered 403 to CONNECT (policy denial or upstream failure)"`, for every host tried.
  Confirmed against `http://127.0.0.1:38803/__agentproxy/status`, which logs each rejection by host.
- **`WebFetch`** — returns `{"error_type":"EGRESS_BLOCKED"}` for every scholarly host tried.

`WebSearch` is the *only* working external channel, and it returns a result list plus a
model-written summary of snippets. **It does not return source text.** A summary written by a model
from snippets is exactly the artefact this problem's README was burned by twice (a survey's
summary read as a warrant; a repository's generated field read as the publication). It is used
below only to name leads, never to state what a paper says.

### Hosts confirmed blocked, 2026-08-21

Every one returned `EGRESS_BLOCKED` (WebFetch) or a proxy 403 (curl). The list matters because
several of these are recorded in `../../README.md` as having *worked* for this project before —
so the blocklist is a property of this session, not of the sources.

| Host | Previously used by this repo? |
|---|---|
| `www.sciencedirect.com` | no (already 403 in earlier sessions) |
| `www.cambridge.org` | **yes** — Oler (1961) was read in full from here |
| `link.springer.com` | no |
| `arxiv.org` | **yes** |
| `en.wikipedia.org` | **yes** |
| `api.crossref.org` | **yes** — settled the Melissen–Schuur volume |
| `api.openalex.org` | **yes** — same |
| `api.zbmath.org` / `zbmath.org` | **yes** — source of both Melissen reviews and the Groemer scan |
| `gdz.sub.uni-goettingen.de` | **yes** — the Groemer scan itself |
| `ris.utwente.nl` | **yes** — Melissen & Schuur PDF |
| `www.combinatorics.org` | **yes** — Graham & Lubachevsky |
| `www.ajuronline.org` | **yes** — Tedeschi & Mackey |
| `archive.org`, `scholar.archive.org` | attempted before |
| `core.ac.uk`, `citeseerx.ist.psu.edu`, `hal.science`, `www.numdam.org` | attempted before |
| `www.semanticscholar.org`, `dblp.org`, `www.jstor.org`, `oa.mg`, `openlibrary.org` | — |
| `dl.acm.org`, `fanchung.ucsd.edu`, `www.rongraham.org`, `math.colgate.edu` | new this session |
| `pp.bme.hu`, `r.jina.ai`, `example.com`, `www.bing.com`, `duckduckgo.com` | new this session |

Reachable: `github.com`, `raw.githubusercontent.com`. That is the whole allowlist as far as it
was probed.

**Consequence for the team.** Any literature task in a session with this egress profile will
return nothing, however it is attempted. Check reachability *first* — one `WebFetch` to
`api.crossref.org` costs a second and decides whether the task is possible at all.

---

## 2. Leads — search-index level only, none of it read

Recorded as pointers for a human with a browser, or for a future session with egress. **None of
this is evidence about what any paper contains.**

### 2.1 Payan (1997) — routes not previously listed in `../../README.md`

The README lists what was tried before (ScienceDirect 403, Unpaywall closed, CORE 0 hits,
scholar.archive.org bot-blocked, Semantic Scholar elided, HAL, Crossref, Google Scholar,
ResearchGate). Two routes it does *not* list surfaced in search results, both blocked here:

- **ACM Digital Library** indexes the paper under its English title, *"Packing of equal disks in
  an equilateral triangle (after a conjecture of Erdős-Oler)"*, in *Proceedings of an
  international symposium on Graphs and combinatorics*, at
  `https://dl.acm.org/doi/10.5555/261210.249560`. `dl.acm.org` — blocked.
- **The volume is a conference proceedings.** *Discrete Mathematics* **165–166** (1997) is the
  proceedings of *Graphs and Combinatorics*, Marseille 1995. A proceedings volume has more
  chances of a library scan or a contributed-copy than an ordinary issue, and dblp's volume page
  (`https://dblp.org/db/journals/dm/dm165.html`) would give the full table of contents. `dblp.org`
  — blocked.

No IMAG/Grenoble technical-report preprint was found (the README already tried this; searching
again surfaced only a different, unrelated *Yohan* Payan at TIMC-IMAG).

**What Payan's method is, and whether it extends to $k = 7$: still unknown.** Nothing was found
that describes his argument at any level of detail — not a citing paper, not a review, not a
survey paragraph. The repo's position is exactly where `../../README.md` left it.

### 2.2 Folkman & Graham

Search results consistently give **J. H. Folkman and R. L. Graham, "A packing inequality for
compact convex subsets of the plane", Canadian Mathematical Bulletin 12 (1969) 745–752.** Volume,
year and page range are new to this repo (the teammate's request named no volume).

**Do not promote this to `cited`.** It rests on search-result summaries and nothing else;
`FINDINGS.md` 2026-08-18 establishes that publisher front matter and CrossRef outrank derived
metadata, and a search summary is further down that ladder than the repository record that already
fooled this project once. Confirm against CrossRef or the Cambridge Core front matter before use.

**Whether it contains (a) the slack decomposition identity of
[`../oler-slack-analysis/`](../oler-slack-analysis/) §1 or (b) Conjecture FP,
$n \le a^2/2 + \tfrac32\lfloor a\rfloor + 1$: not determined.** Nothing was obtained. Two routes
that would have worked and are blocked here:

- Cambridge Core hosts old CMB issues with direct PDF links of the shape
  `https://www.cambridge.org/core/services/aop-cambridge-core/content/view/<ID>/<file>.pdf`
  (search surfaced exactly such a link for Oler's own paper). `www.cambridge.org` — blocked.
- Ron Graham's personal publication archives at `www.rongraham.org/ron-graham/papers`,
  `fanchung.ucsd.edu/ron/publist.pdf` and `math.colgate.edu/~integers/RonGrahamPubs.pdf` — all
  three blocked. These are the best bet for a free author copy and none of them appears in the
  README's list of attempted routes.

No citing paper restating the Folkman–Graham inequality could be read either; the candidates that
surfaced (`inf.u-szeged.hu` survey chapter, `pp.bme.hu` Gáspár–Tarnai-style density bounds,
arXiv `math/0412443`) are all on blocked hosts.

### 2.3 Erdős–Oler for $k \ge 7$

**Nothing found that this repo does not already have.** No partial result, no asymptotic result,
no statement of where the difficulty lies, no proof strategy, was located at any level — including
at search-summary level, where a well-known partial result would ordinarily show up. That is weak
negative evidence and nothing more: **a search engine's silence is not a denial**, which is the
exact error `FINDINGS.md` 2026-08-17 records this project making with three sources' silence.

Two traps worth naming, since both appeared in search summaries during this pass:

1. **"Optimal solutions were provided for $n \le 35$ by Locatelli and Raber in 2002"** appeared in
   a search summary *inside a discussion of the equilateral triangle*. It is about the **square**:
   the paper is Locatelli & Raber, *Packing equal circles in a square: a deterministic global
   optimization approach*, Discrete Applied Math. (ScienceDirect `S0166218X01003596`). If taken at
   face value it would say $k = 7$ is already settled, which would be exactly the "stop the provers"
   signal this task was looking for — and it would be wrong. **The provers should ignore it.**
2. **The Academia.edu / ResearchGate item** *"Optimal Circle Packings for Triangular Numbers: A
   Detailed Mathematical Proof of the Erdős-Oler Conjecture"* (academia.edu 129891186 /
   researchgate 387465203) dominates every search for this conjecture — it was the top or
   near-top hit on five separate queries. It is the item `issue #29` flagged and the manager
   instructed not to cite. **Flagged, not used.** Anyone searching this topic will hit it
   repeatedly; that prominence is a search-ranking artefact, not standing.

### 2.4 Melissen thesis (1997), Joós (2021)

Fresh attempts, both cheap, both **nothing**. No accessible full text of the Utrecht thesis was
located (consistent with the README's 2026-08 attempt). Joós's paper is Springer-only
(`link.springer.com/article/10.1007/s00010-020-00753-y`), blocked; no preprint or author copy
surfaced.

---

## 3. One thing for the manager, offered as a question, not a correction

`../../README.md` §"Groemer (1960) — co-credit rejected" concludes that Friedman's Oler/Groemer
co-credit "appears to be an attribution of the *underlying tool* rather than of the result."

During this pass a paper title appeared in search results — *"A NEW PROOF FOR
ZASSENHAUS–GROEMER–OLER INEQUALITY"*, Discrete Mathematics, Algorithms and Applications
(worldscientific.com, `10.1142/S1793830912500140`). **The title alone** is evidence that
"Zassenhaus–Groemer–Oler" is standard usage for the inequality, i.e. that the literature does treat
Groemer 1960 as containing a form of the same result Oler proved.

That **supports** the README's own final sentence rather than contradicting it, so nothing needs
changing on that basis. But it bears on the `sketch` table in that section, which computes
Groemer's inequality as *slack* at every triangular $n$ while Oler's is tight there. The likely
explanation is that the two are being applied to different regions — Groemer's to the containing
triangle $T$, Oler's route to the convex hull of the centres and only then relaxed to $T$ (which is
precisely the two-stage split measured in [`../oler-slack-analysis/`](../oler-slack-analysis/) §3,
where stage 2 is the lossy one). If so the table compares stage-1+2 against stage-1 and the
"slack" it reports is not a property of Groemer's inequality.

**I did not read Groemer, Oler, or the Zassenhaus paper this session and cannot settle this.** The
section labels that table `sketch` and explicitly says it is "a consistency check on the rejection,
not its foundation", so nothing load-bearing depends on it. Recorded as a question for whoever next
has egress — deliberately not written up as a correction, because this repo's last three
corrections were themselves the error.

---

## 4. Provenance table

Same convention as `../../README.md`.

| Source | How it was used |
|---|---|
| Payan, Discrete Math. 165–166 (1997) 555–565. | **NOT obtained.** ScienceDirect, ACM DL, dblp all blocked at this session's egress. No new information about its contents. The abstract quoted in `../../README.md` was obtained in an earlier session and is **not** re-confirmed here. |
| Folkman & Graham, Canad. Math. Bull. (1969). | **NOT obtained.** Bibliographic detail "**12**, 745–752" from search-result summaries only — *not* confirmed against CrossRef or publisher front matter, both blocked. Not `cited`. Contents unknown. |
| Melissen, *Packing and covering with circles*, PhD thesis, Utrecht (1997). | **NOT obtained.** No accessible full text found; consistent with the README's earlier attempt. |
| Joós, Aequat. Math. 95 (2021) 35–65. | **NOT obtained.** Springer-only, blocked. |
| Oler, Canad. Math. Bull. 4 (1961) 153–155. | **Not re-read this session** (Cambridge Core blocked). The repo's existing full read stands on its own record. |
| Locatelli & Raber, Discrete Appl. Math. (2002). | **NOT read.** Named here only to record that a search summary mis-attached its $n \le 35$ result to the triangle; the article title in the search result identifies it as the **square**. |
| "Zassenhaus–Groemer–Oler inequality" paper, DMAA (`10.1142/S1793830912500140`). | **NOT read.** Its *title* was seen in a search result list. Used in §3 as evidence about naming convention only. |
| Academia.edu 129891186 / ResearchGate 387465203. | **Deliberately not used** (`issue #29`, manager instruction). Recorded only because it dominates search ranking for this conjecture. |
| `WebSearch` result lists and summaries. | **Secondary at best, and below every tier this repo has previously used.** Used to name leads. Never used to state what a source says. |

## 5. What this changes for the two provers, today

**Nothing.** No route was opened and no route was closed. Specifically:

- The provers should **not** treat $k = 7$ as settled or as known-to-fail on anything found here.
- Payan's method remains unknown to this project, so "does his argument visibly extend to $k = 7$"
  remains unanswerable — as it was this morning.
- Whether Folkman & Graham already contains the slack identity or Conjecture FP is **open**, and a
  prover who needs that answered needs a session with egress or a human with a library.

The one operational change worth making is in §1: probe reachability before spending a task on
literature.
