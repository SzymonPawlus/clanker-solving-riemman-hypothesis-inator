# 2026-09-02 — tau = 2 complete write-up (issue #152)

Worker: claude (Fable 5.1), builder side of pair C; adversary is #153. Branch
`claude/152-tau2-complete`. No PR opened (dispatcher instruction); branch pushed.

## What I did

- Wrote `problems/woodalls-conjecture/attacks/tau2-complete/README.md`: definitions in my own
  words with the empty-dicut convention fixed; the four §4 fixtures with explicit dicut lists;
  the condensation reduction with a full proof of the dicut correspondence; Lemma A
  (bridgeless + connected), Theorem R (Robbins, re-proved ear-by-ear for multigraphs so no
  external theorem is load-bearing), Lemma B, the agreement colouring, and a table of where
  each hypothesis is used. Status `sketch`, and it says so loudly.
- Discharged the three filters in the write-up. The Schrijver step is the colouring-to-packing
  step (§5.4): the orientation is weight-blind, so the Lemma B witnesses can be weight-0 arcs.
  Lemma A holds verbatim under weights (FINDINGS.md already recorded that the old "weight-2
  bridge" story was wrong). Side result stated explicitly: the proof *is* a proof of
  Edmonds–Giles for strictly positive weights at tau_w >= 2, which is consistent with the
  literature (Schrijver needs weight 0).
- `experiments/woodall-tau2-checks/`: independent bitmask checker, the exact ear procedure of
  Theorem R, full pipeline on all simple digraphs <= 4 vertices, all 3-vertex multidigraphs
  with multiplicity <= 2, 3000 seeded random multidigraphs with cycles/loops/parallel arcs,
  condensation correspondence on 500 random digraphs, and the mechanical failure of step 5.4
  under one weight-0 arc. All pass.

## What I could not do

Every host with Schrijver's 1980 paper or a figure of it is egress-blocked (ir.cwi.nl,
dl.acm.org, ime.usp.br, arxiv.org, wikipedia, EGRES, OPG, researchgate, andrew.cmu.edu,
uwaterloo). Only search snippets: {0,1} weights, tau_w = 2, labels 1,1',1'', six minimal
dicuts of weight 2, chordless 6-cycle, Younger's "ring of length 4k+2 with 2k+1 solid paths".
I refused to write a digraph from memory and call it Schrijver's. Instead I hunted for *a*
{0,1} counterexample with my own checker: random DAGs n=7–8 (410k tau_w=2 instances), n=9–11
(1.06M), the symmetric 6-ring + three solid 3-arc paths family (1536, exhaustive), the wider
ring family (independent orientations, lengths 2–4, six matchings; count in the experiment
README), and a shore-lattice construction with out-star gadgets (32 768 configs). Nothing.
Recorded as gap G2; the checker is ready for a transcription.

Lesson: the counterexample is structurally rarer than "random small DAG + random weights"
can find; the repo census (none on <= 6 vertices) plus these runs suggest a targeted
reconstruction from the paper is the only sensible route. Someone with network access should
transcribe the instance into `tau2lib` format — that is a 10-minute task with the paper open.

## Least sure of

(W1) the blue-witness bookkeeping in §5.4; (W2) Theorem R case 2 with parallel edges;
(W3) Prop 4.1(i); (W4) conventions; (W5) the "no repair" claims in §6.2 beyond the one
mechanical demonstration. All named in README §7.

## Status

`sketch`. Not assumable by anyone, me included. Ceiling this session is exactly this.
