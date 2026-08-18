# Payan 1997 — acquisition attempt for the body, and what it would settle

**Issue:** [#29](https://github.com/SzymonPawlus/clanker-solving-riemman-hypothesis-inator/issues/29) ·
**Date:** 2026-08-18 · **Agent:** claude (Opus 5)

**Outcome: the body of Payan 1997 was NOT obtained.** Stage 1's 25-minute kill-criterion was
reached and work stopped there, so stage 2 (assessing k = 7 mechanisability) did not start — per
the issue's own kill-criterion, "there is no reconstructing a method nobody here has seen".

This file records every route tried with its result, three new facts that the sweep did establish,
and a precise instruction for a human with a browser.

**Status of everything below:** the bibliographic and access facts are `cited` (each names the API
or page it came from and quotes it). The one remark about what k = 7 would need is `sketch` and is
labelled as such. **Nothing here changes the `n = 20` row in either direction** — see §4.

---

## 1. The target, pinned

| Field | Value | Source |
|---|---|---|
| Author | Charles Payan (sole; "is_corresponding": true) | Unpaywall `z_authors` |
| Title | *Empilement de cercles égaux dans un triangle équilatéral a propos d'une conjecture d'Erdős-Oler* | CrossRef, OpenAlex, dblp, Unpaywall |
| Journal | Discrete Mathematics | all of the above |
| Volume | **165–166** (a double volume) | CrossRef `volume: "165-166"`; ScienceDirect page: "Volumes 165–166, 15 March 1997" |
| Pages | 555–565 | CrossRef `page: "555-565"` |
| Published | 1997-03-15 | ScienceDirect page (Unpaywall gives `1997-03-01`) |
| DOI | `10.1016/S0012-365X(96)00201-4` | CrossRef; resolves 302 → linkinghub → 200 |
| PII | `S0012365X96002014` | — |
| dblp key | `journals/dm/Payan97` | Semantic Scholar `externalIds` |
| OpenAlex | `W2002063645` | — |
| Semantic Scholar | `3dac645935d43b327f565c9be3f9fba052502f4b` (CorpusId 27760354) | — |

Four independent indexes agree on volume **165–166** and pages **555–565**. The repo has been
burned once by a volume number that oscillated 145 → 142 → 145 on the strength of an
auto-generated record; this one is not in that position — it is what CrossRef, OpenAlex, dblp and
the publisher's own article page all say, and they were checked separately.

### An English-titled duplicate record exists — unverified

A web search surfaced `dl.acm.org/doi/10.5555/261210.249560`, *"Packing of equal disks in an
equilateral triangle (after a conjecture of Erdős-Oler)"*, filed under *Proceedings of an
international symposium on Graphs and combinatorics*. DM **165–166** is such a proceedings volume,
so this is **plausibly** the same item under ACM's English rendering — but ACM's page returned
**HTTP 403** and it was not checked. Recorded only as a search handle for whoever tries next;
**do not cite it as the same paper without opening it.**

---

## 2. Access status — this is the actionable finding

The three access oracles **disagree**, and the disagreement is the point.

| Oracle | Verdict |
|---|---|
| Unpaywall | `"is_oa": false`, `"oa_status": "closed"`, `"oa_locations": []`, `"has_repository_copy": false` |
| OpenAlex | `"is_oa": false`, `"oa_status": "closed"`, `"any_repository_has_fulltext": false`; one location, the DOI landing page |
| **Semantic Scholar** | **`"isOpenAccess": true`**, `openAccessPdf.status: "BRONZE"`, `license: "publisher-specific-oa"` |
| **Publisher's own page** | **"Under an Elsevier user license — open archive"**, with a *View PDF* button |

Semantic Scholar and the publisher agree, and they are right; Unpaywall and OpenAlex are not wrong
so much as **answering a different question**. "Bronze OA" means *free to read on the publisher's
site under no open licence*. Unpaywall's `closed` is reporting that there is **no repository copy
and no open licence** — which is true — and it is **not** evidence that the PDF is paywalled.

> **Correction to how a previous entry reads.** `FINDINGS.md` lists "Unpaywall shows closed" among
> the signals that acquisition failed. That is a correct quotation but an easy thing to misread as
> "the paper is behind a paywall". It is not. The PDF is **free to any reader**; what blocks this
> project is bot protection, not a subscription wall. That distinction changes the human
> instruction in §5 from "someone with institutional access should try" to "**any** person with an
> ordinary browser can download it, no institution required".

The publisher page text was read from a Wayback capture (`20240415232000`) of the ScienceDirect
article page, which carries the label verbatim: `Under an Elsevier user license` / `open archive`,
alongside `View PDF` and `Download full issue`.

---

## 3. Routes tried, with results

Sweep run 2026-08-18, ~09:27–09:47 UTC. **No route reached the body.**

### Publisher, direct
| Route | Result |
|---|---|
| `https://doi.org/10.1016/S0012-365X(96)00201-4` | 302 → linkinghub → 200 (landing only) |
| `sciencedirect.com/science/article/pii/S0012365X96002014` (curl, browser UA) | **HTTP 403**, 1.2 MB HTML bot-challenge page |
| `.../S0012365X96002014/pdf` | **HTTP 403**, same challenge page |
| `.../S0012365X96002014/pdfft?isDTMRedir=true&download=true` | **HTTP 403**, same |
| Same landing URL via WebFetch (different network path) | **HTTP 403** |

The 403 is Elsevier's bot-detection layer, **not** an entitlement check — consistent with §2. It
was not circumvented, and circumventing it is out of scope.

### Publisher, text-mining API
CrossRef advertises two TDM links (`api.elsevier.com/content/article/PII:S0012365X96002014` in
`text/xml` and `text/plain`). Both require an Elsevier API key. **Not attempted** — that is a
credentialed route and the task forbids it.

### Wayback Machine — the near miss
`web.archive.org` has captured all three SD URLs (April 2024). But:

- the **article page** capture (38 KB) is real and gave the abstract and the footnote in §4;
- the two **PDF** captures (12 KB stored, 53 KB served) are `text/html` and resolve to
  `https://www.sciencedirect.com/craft/challenge/pdf/trace/1px?...` — i.e. **the Wayback crawler
  was bot-blocked too and archived the challenge page, not the PDF.**

So the archive route is dead for the reason the live route is dead, and no amount of retrying
different capture timestamps will fix it.

### Repositories and aggregators — all negative
| Route | Result |
|---|---|
| **HAL** (French national repo — Payan's own institution's) full-text query | 0 hits for the paper. Author query `authFullName_s:"Charles Payan"` returns 5 records, **none is this paper** (a 1997 tree-products paper, a 1977 thesis, a 1966 thesis, a 2007 pentomino paper, plus an unrelated Payan) |
| CORE v3 API | empty response |
| BASE | `"Access denied for IP address ... and user agent curl"` — never reached the index |
| OpenAIRE | no full-text web-resource returned |
| Zenodo | no relevant hits |
| CiteSeerX API | empty response |
| archive.org fulltext (`"Erdős-Oler"`) | 0 hits |
| OpenAlex `locations` | exactly one, the DOI landing page — no repository copy |
| scholar.archive.org | blocked (recorded by a previous attempt; not re-run) |

**HAL returning nothing is the most informative negative here.** Payan worked at LSD2-IMAG,
Grenoble; HAL is where a French preprint or `rapport de recherche` version would live, and it does
not have one. Combined with OpenAlex and Unpaywall both reporting no repository copy anywhere,
the conclusion is that **no free mirror of this paper exists** — the publisher's own open archive
is the only copy, and it is exactly the one behind the bot wall.

### Citing literature, as an indirect route
OpenAlex reports only **4** citing works. Two are open (Brass et al., *Packing, covering and tiling
in two-dimensional spaces*, 2013; *Circle packing in arbitrary domains*, 2023). The 2013 survey's
OA PDF is itself on ScienceDirect and returned the same **403**. arXiv:2212.12287 (*Circle packing
in regular polygons*) was downloaded and read: it cites Payan **only in its bibliography**, with no
statement about what he proved. This route was abandoned — and it is worth noting that chasing what
*other* people say Payan proved is precisely the secondary-source path that has already misled this
repo three times.

---

## 4. What the sweep did establish — one new primary datum

The Wayback capture of the publisher's article page reproduces the article's own **printed
footnote 1**, which is part of the article, not part of the abstract:

> **«La recherche des preuves a été grandement facilitée par l'utilisation de Cabri-géomètre, un
> logiciel de géométrie développé dans notre laboratoire (LSD2-IMAG) [1].»**
>
> *"The search for the proofs was greatly facilitated by the use of Cabri-géomètre, a geometry
> software developed in our laboratory (LSD2-IMAG) [1]."*

Two things follow, and one thing does not.

**It follows that Payan's proof search was computer-assisted**, by *Cabri-géomètre* — an
interactive dynamic-geometry system, not a theorem prover. That is a genuine, if modest, signal
about the shape of the method: configurations explored and constrained interactively, then written
up as a case analysis by hand. It is the first thing this project knows about the method from
inside the paper.

**It does not follow that k = 6 is proved in full.** The footnote says «les preuves», plural. It is
tempting to read that as "the k = 5 proof *and* the k = 6 proof", and therefore as confirmation
that k = 6 is carried out in the body. **That reading is not available.** French routinely
pluralises this way for the several arguments composing a single proof, and one word's grammatical
number cannot discharge the question the whole issue exists to answer. Recording the temptation
here so the next reader does not have it fresh.

**Therefore the `n = 20` row is unchanged.** It remains `cited`, qualified "abstract only — body
not read", exactly as `main` has it. This attempt neither strengthens nor weakens it. The abstract
was re-read verbatim off the publisher page during this sweep and **matches what `main` records
word for word** in both languages — so the existing quotation in
`problems/circle-packing-equilateral-triangle/README.md` is independently confirmed accurate.

**No edit to `README.md` or `FINDINGS.md` is implied by this attempt**, with one exception offered
to their holder rather than taken here: the §2 clarification that Unpaywall's "closed" means *no
repository copy*, not *paywalled*, and that the download therefore needs **no institutional
access**. That sharpens the existing "Actionable for a human" note in `FINDINGS.md`.

---

## 5. Instruction for a human — precise, ~2 minutes

The paper is **free to read**. No library, no institution, no login.

1. Open **`https://www.sciencedirect.com/science/article/pii/S0012365X96002014`** in an ordinary
   browser (the DOI `10.1016/S0012-365X(96)00201-4` lands in the same place).
2. Confirm you are on the right item: the header should read *Discrete Mathematics, Volumes
   165–166, 15 March 1997, Pages 555–565*, and under the title you should see
   **"Under an Elsevier user license"** and the words **"open archive"**. That label is why no
   sign-in is needed.
3. Click **View PDF** (or *Download full issue*). Save it as
   `1-s2.0-S0012365X96002014-main.pdf` — that is the filename ScienceDirect assigns.
4. If a challenge/captcha page appears, complete it in the browser; it is bot protection, and it is
   what blocked every automated attempt above. It does not appear for a normal human session.

**What to look for once you have it** (the paper is 11 pages, in French):

- **The k = 6 section.** This is the whole question. Determine which of three things the paper
  does: (a) carries out the k = 6 (n = 20) case in full; (b) gives the extension in outline and
  leaves cases to the reader; (c) only remarks that the method would extend. The abstract's
  «Cette preuve s'étend de manière un peu plus laborieuse pour k = 6» is a present indicative and
  is compatible with all three. **Quote the French verbatim**, wherever in the body k = 6 is
  actually discussed, including a sentence either side.
- **How the k = 5 case analysis is organised** — how many cases, and what the case split is on.
  This is what stages 3–5 of issue #29 need, and what decides whether k = 7 is mechanisable.
- **Whether the paper says anything about k = 7 or general k**, beyond the abstract's "devrait
  permettre une approche de la conjecture générale".
- **Reference [1]** — the Cabri-géomètre citation from footnote 1.
- **How Oler's inequality is used**, if it is — this feeds issue #17.

Dropping the PDF (or a transcription of the k = 5/k = 6 sections) anywhere in the repo unblocks
stages 2–5 of #29 immediately.

---

## 6. One forward-looking remark — `sketch`

**Status: `sketch`.** Not assumable, including by its author. It rests on a paper nobody here has
read, which is as weak as a claim can be while still being worth writing down.

The Cabri-géomètre footnote (§4) is mild evidence *against* k = 7 being a cheap mechanisation
target. A proof found by interactive dynamic-geometry exploration is one whose case split was
chosen by a human looking at pictures. Such splits tend to be well-adapted to the specific k and
not to carry a uniform induction — which is the shape the abstract itself hints at with «un peu
plus laborieuse» for the step from k = 5 to k = 6, one k at a time. If the effort per case grows
that way at each k, the issue's stage-4 extrapolation is the decisive measurement, and it cannot be
made without the body.

**This is a guess about a paper that has not been read, and it must not be used to close, downgrade,
or de-prioritise issue #29.** The correct next action remains §5: get the PDF.
