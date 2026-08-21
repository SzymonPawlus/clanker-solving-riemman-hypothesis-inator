# 2026-08-21 — Erdős–Oler literature pass (k = 7). Null result.

Role: Literature Helper on the 5-agent team. Branch `claude/circle-equklatetal-problem-sa7tx7`.
Write-up: `problems/circle-packing-equilateral-triangle/attacks/eo-literature/README.md`.

## Outcome

**Zero sources obtained.** Not a paywall problem — this session has essentially no scholarly
egress. `curl` gets `403 CONNECT` from the agent proxy for every host; `WebFetch` returns
`EGRESS_BLOCKED` for every scholarly host. Reachable: `github.com`, `raw.githubusercontent.com`.
That is all I found.

Blocked hosts include ones the problem README records as having *worked* before —
`www.cambridge.org` (where Oler was read in full), `api.crossref.org`, `api.openalex.org`,
`api.zbmath.org`, `gdz.sub.uni-goettingen.de`, `ris.utwente.nl`, `www.combinatorics.org`,
`www.ajuronline.org`, `arxiv.org`, `en.wikipedia.org`. So the blocklist is a property of this
session, not of the sources. Full list in the attack README §1.

`WebSearch` works. It returns a result list plus a **model-written summary of snippets**, which is
not source text. Given this repo's history (a survey's summary read as a warrant, PR #36; a
repository's generated volume field read as the publication, PR #21) I refused to let any of it
become a claim. Everything I recorded is labelled search-index level and nothing was promoted to
`cited`.

## The temptation, named

The strong pull, once fetching failed, was to write down what I *know* about Payan's method or
Folkman & Graham's inequality from training data and dress it as a finding. The manager's brief
called that out in advance and it was correct to. I have not read those papers. Two useful things
I could have written would have been unfalsifiable from inside the repo. "Not obtained" is the
honest output and it is what I filed.

## What I did produce that is worth something

1. **The egress map** — so nobody spends another task discovering the same wall. Operational
   change proposed: probe `api.crossref.org` with one `WebFetch` before accepting a literature
   task; it decides in a second whether the task is possible.
2. **Two new Payan routes** the README does not list, both blocked here but both live for a human
   with a browser: ACM DL indexes the paper under its English title
   (`dl.acm.org/doi/10.5555/261210.249560`), and DM **165–166** is the *Graphs and Combinatorics,
   Marseille 1995* proceedings — a proceedings volume scans differently from an ordinary issue,
   and dblp's volume page would give the full TOC.
3. **Three Folkman–Graham routes** the README does not list: Ron Graham's own publication archives
   (`rongraham.org`, `fanchung.ucsd.edu/ron/publist.pdf`, `math.colgate.edu/~integers/`). Author
   copies, blocked here, plausibly free.
4. **Two traps defused.** A search summary asserted "optimal solutions for n ≤ 35 by Locatelli and
   Raber (2002)" *while discussing the equilateral triangle* — the article title in the same
   result identifies it as the **square**. Taken at face value it would have told the provers k=7
   is already solved. And the academia.edu/ResearchGate "detailed proof of Erdős–Oler" item was
   the top hit on five separate queries; flagged, not used (`issue #29`).

## One open question I deliberately did not turn into a correction

A paper title surfaced in search: *"A NEW PROOF FOR ZASSENHAUS–GROEMER–OLER INEQUALITY"* (DMAA,
`10.1142/S1793830912500140`). The title alone suggests "Zassenhaus–Groemer–Oler" is standard usage
— i.e. the literature treats Groemer 1960 as containing a form of Oler's inequality. That agrees
with the problem README's conclusion ("attribution of the underlying tool"), so no correction is
implied there. But it makes me suspect the `sketch` table in that section — which computes
Groemer's inequality as *slack* at every triangular n while Oler's is tight — is comparing the two
on different regions (Groemer applied to the containing triangle T; Oler's route to the hull of the
centres, relaxed to T only afterwards). That is exactly the stage-1/stage-2 split measured in
`attacks/oler-slack-analysis/` §3, where stage 2 is the lossy one.

I did not read Groemer, Oler, or the DMAA paper this session, so I cannot settle it. The table is
labelled `sketch` and the README says outright it is a consistency check and not the foundation of
the rejection, so nothing load-bearing rests on it. Filed as a question for a session with egress,
not as a correction — this repo's last three corrections were themselves the error, and I have
strictly less evidence than any of those three had.

## For the provers

Nothing changes today. No route opened, no route closed. Payan's method remains unknown here, so
"does it visibly extend to k = 7" is still unanswerable; whether Folkman & Graham already contains
the slack identity or Conjecture FP is still open. Both need egress or a human with a library card.
