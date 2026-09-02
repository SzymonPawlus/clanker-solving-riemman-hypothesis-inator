# 2026-08-22 — worker I1: round-3 ideation for n=16, with kill-runs

Issue #97, branch `claude/circle-packing-subagents-9yg5gt`. Role: divergent (repo RULES.md §8).
Deliverable: [`attacks/n16-approaches/`](../../problems/circle-packing-equilateral-triangle/attacks/n16-approaches/),
code in [`experiments/packing-n16-approaches/`](../../experiments/packing-n16-approaches/).

## What I did, in order

1. **Dedup pass** over candidate-approaches (A–H), approaches-round-2 (I–O), all `n16-*` and
   `eo-*` lanes. Notable for anyone repeating this: round-2's §J and §L had already written down
   the dilation/limit trick and the $m(n)$ target that the 08-22 covering lanes rediscovered —
   the board's memory is better than the board thinks. I made sure nothing below re-proposes
   F2/M2/U2 (owned today) or anything with a documented kill.
2. **Checked the environment before designing experiments**: scipy/numpy only; no SDP, SAT, or
   CAS. This decided the triage — it kills the *runnability* of the parked SDP proposal (C) here
   and made the LP-only Positivstellensatz (Handelman) the right cheap probe of that family.
3. Wrote ten proposals, then ran the four cheapest kill-experiments (all four fit in well under
   the 45-min budget, single core).

## Kill-run results

- **Transference (square / disk / diameter-only)** — all three dead, exactly and permanently.
  Each has a witness-certified ceiling below Oler: $3(\sqrt6-\sqrt2)=3.106$, $2\sqrt3=3.464$,
  $\sqrt{13}=3.606$. The diameter kill also buries any distance-matrix (CNSD rank-4) relaxation.
  Moral, worth remembering: **every containment relaxation throws away the triangle's corners,
  and the corners are where a 16-point packing pays for its side length.**
- **Handelman/Krivine LP Positivstellensatz** — dead. Degree-4 value at $n=4$: $h_4\approx1.211$
  vs $a_4=\sqrt3=1.732$, i.e. 30% slack against a pre-registered 7.6% gate. Also computed the
  exact level-1 moment bound ($a\ge\sqrt{45/64}\approx0.84$): the LP fragment of the moment
  hierarchy carries nothing; SOS blocks would be load-bearing. No SDP solver here, so that stays
  parked with a sharpened risk note.
- **3-direction tomography (hexagonal norm)** — dead vs the record, exactly: $M(16)\le17/4$.
  Curious footnote: $17/4=4.25$ *beats Oler* — a two-page piecewise-linear argument would
  out-prove Oler 1961 if anyone certified it; the covering record supersedes it, so nobody should.
- **6-direction tomography (dodecagonal norm)** — **survived, and is the headline.** Exact:
  $M_6(16)\le449/100=4.49$. Search (iterated LP over active disjuncts, 150 restarts): feasible
  configurations found and exactly verified at $a=4.49$, none found at $a\le4.48$, with the
  margin curve crossing threshold at $a\approx4.483$. The standing record is $4.4641$. So the
  relaxation's value *numerically* sits $\approx0.019$ above the record, its profit is capped at
  $4.49$ (exact), and its certificates would be finite trees of rational Farkas data in
  $\mathbb{Q}(\sqrt3)$. Failed search $\ne$ bound (§L discipline), stated everywhere.

## Discipline notes

- Kill-criteria were written into each script docstring before the runs; the attacks README says
  so and preserves the order.
- The numerical 16-point packing was used only as a *seed* for upper bounds on auxiliary
  relaxation values (kill decisions). The README's circularity-guard paragraph forbids the future
  $M_6$ certification worker from touching it.
- Nothing today asserts any bound on $a_{16}$; claim type "neither" on line 1 of the README.

## Handoff

Shortlist (details and exact first steps in the README): (1) certify a lower bound on $M_6(16)$
by disjunct branch-and-cut with exact Farkas leaves — validate on $M_6(4), M_6(5)$, measure node
growth at $n=10,12,15$, kill past $10^9$ extrapolated nodes, and check early whether $M_6(15)<4$;
(2) literature-first reconstruction of the disk-container Voronoi/Delaunay optimality technique
(WebSearch works; texts blocked — this is the best argument yet for a human importing one PDF);
(3) the Lasserre level-2 gate on $n=4,5$ the moment any worker has an SDP solver.

The proposal a cautious reader will underrate: the $k=6$ tomography. Its three siblings died
today ($k=3$, and the two containment transferences), which pattern-matches to "relaxations lose
too much here" — but this one's loss factor is $\cos15°$, its measured transition is on the far
side of the record, and it is the only live route whose certificate is pure rational linear
algebra end to end.
