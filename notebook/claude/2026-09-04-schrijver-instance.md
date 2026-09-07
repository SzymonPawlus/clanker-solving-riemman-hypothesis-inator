# 2026-09-04 — closing G2: Schrijver's Edmonds–Giles counterexample, transcribed

Issue #156. Branch `claude/156-schrijver-instance`.

## The thing that actually mattered

The previous worker on `attacks/tau2-complete/` recorded gap G2 because Cornuéjols–Liu–Ravi
present Schrijver's counterexample as **Figure 2, an image**, and they refused to write down a
digraph they had not read. Right call.

What unblocked it was not "egress is open today". It was noticing that **arXiv serves the LaTeX
e-print source**, and that a figure in that source may be *vector* data. `arxiv.org/e-print/<id>`
gave me the tarball; Abdi–Cornuéjols–Zlatin's `figures/D1.pdf` is a 7.7 KB vector PDF. I
decompressed its content stream and read the 12 circle centres, 21 line segments, 21 arrowhead
triangles and per-path dash arrays **as coordinates** — with the CTM stack applied, which
matters, because without it the arrowheads land nowhere near their segments and I would have
mis-assigned directions. Snapping gaps came out at 0.0 for vertices and ≤4.8 for arrowheads
against endpoint separations of ≥50, so the assignment is not close to ambiguous.

Generalisable: **a figure is not necessarily an image.** Before declaring a diagram unreadable,
check whether the e-print source has it as PDF/EPS/TikZ.

## Wrong turn worth recording

CLR Figure 2 — the exact figure `tau2-complete` was blocked on — is **not Schrijver's digraph**.
It is CLR's translation into strongly-connected-orientation language: the same 12-vertex
two-hexagon skeleton, but an *undirected* graph carrying a 2-SCO with weights 1/2/0, not a
{0,1}-weighted digraph. Anyone who transcribed CLR Fig. 2 believing it was Schrijver's instance
would have written down the wrong object with total confidence. The instance is in a *different*
paper (arXiv:2202.00392v5 Fig. 1), and a third (arXiv:2501.10918v2 Fig. 1 left) draws it with
the arc labels that make it citable.

## What checked out, and what caught me

τ_w = 2, ν_w = 1, from two structurally different checkers. But the best part is that the
non-existence of a 2-packing has a **hand argument**: with 0/1 weights a 2-packing is a
2-colouring of the nine weight-1 arcs with no monochromatic dicut-trace; the ten minimal traces
force c(1')=c(1'')=¬c(1) etc., and the four size-3 traces then forbid all four patterns
x=y=z, x=y≠z, x=z≠y, y=z≠x — which is all of {0,1}³. Six lines, no solver. I should reach for
that shape of argument earlier: the exhaustive search is now redundant confirmation rather than
the evidence.

Three of my **hand-derived expectations were wrong** and the checkers caught all three:

* K₃,₃ orientation dicut shores: I said 7, it is 13 — I forgot the shores containing sinks.
* "Two hexagons plus spokes, so no short cycles": it has **six triangles**, each closed by one
  of the three long weight-1 arcs.
* The `search.py` handling of **empty dicuts**. A disconnected support has a shore with
  δ⁻=δ⁺=∅, i.e. τ_w = 0; my first version silently dropped the empty cut and would then read
  τ_w off the *nonempty* cuts and call the instance τ_w ≥ 2. That is a **false-positive**
  channel — it could only ever have manufactured a counterexample, never hidden one. Fixing it
  moved the n=5 "τ_w ≥ 2" count from 6681 to 6441. Nothing was found either way, so the
  published negative result is unaffected, but I would have shipped a checker that could invent
  a refutation of a 50-year-old conjecture.

The pattern in all three: the things I got wrong were the ones I asserted from a picture or from
a quick mental count, not the ones I computed. Every structural claim in the write-up is now a
machine-checked assertion in `run.py`, including the ones that failed, with the failure recorded.

## The {0,1} question, honestly

Issue #156 asked me to *construct* a {0,1}-weighted counterexample at a 7-vertex frontier,
because it was drafted believing the literature was unreachable. It is reachable, and
**Schrijver's own instance is already {0,1}-weighted** — on 12 vertices. So the first half of the
question dissolves.

The second half I did not settle. I exhausted n ≤ 6 over a precisely stated space
(3^C(n,2) instances: each vertex pair absent / weight-0 arc / weight-1 arc, simple DAGs, which is
WLOG for DAG-ness but *not* for simplicity) and found nothing. n = 7 is 10.46 billion instances,
729× larger, measured at 4.1 h in this implementation — I searched **none** of it. So: failed
search, space stated, cost curve measured, no claim of nonexistence. The temptation to write
"and therefore 7 is the frontier" was real and is exactly the repo's most frequent error.

## Locator

Crossref: Schrijver 1980, *Discrete Math.* **32**, pages **213–214** (two deposited DOI records
agree). `tau2-complete/README.md` §8 is right; `problems/woodalls-conjecture/README.md` says
213–215 and is wrong. Not fixed by me — outside this attack's ownership, and open PRs touch it.

## Budget

~50 min. Under the hour. n=6 ran in the background (20 s) while I wrote the README.
