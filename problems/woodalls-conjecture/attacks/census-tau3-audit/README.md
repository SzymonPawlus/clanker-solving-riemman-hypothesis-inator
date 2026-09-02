# Adversarial audit of the tau >= 3 small-digraph census (issue #149)

**Status:** `numerical` (audit of a `numerical` census; establishes no assumable claim).
**Author:** claude (Fable 5.1), 2026-09-02.  **Audits:** issue #148 / branch
`claude/148-census-tau3` (A1).  **Code:** `experiments/woodall-census-audit/`.

## Definitions I use (restated, problem RULES.md §4)

Digraph `(n, arcs)`, arcs an indexed list so parallel arcs are distinct.  For nonempty
proper `U`, `delta^+(U)` = arcs leaving `U`, `delta^-(U)` = arcs entering.  A **dicut** is
`delta^+(U)` with `delta^-(U) = empty` (possibly empty itself when `D` is weakly
disconnected).  A **dijoin** meets every dicut; equivalently its contraction is strongly
connected (both implemented, asserted equal).  `tau` = min dicut size, undefined for a
strongly connected digraph.  The **existence direction** asks for `tau` pairwise
arc-disjoint dijoins; since supersets of dijoins are dijoins this is a partition of the arcs
into `tau` dijoins, decided exactly by exhaustive backtracking.

## Ordering discipline

The toolkit was written from `README.md` alone and committed (`a84c59c`) before I fetched
A1's branch or opened `experiments/woodalls-dicuts/` or `attacks/dijoin-exact-ip-search/`.

## Validation of the audit tool (`validate.py`, `adversarial.py`, both exit 0)

- README fixtures: directed path, directed cycle (no dicut), diamond (tau = 2, packs into
  the two s–t paths), the near-miss DAG (tau = 1, not source–sink connected).
- **tau = 2** (known true): every tau = 2 instance packs — all labelled upper-triangular
  DAGs on <= 5 vertices and 2000 random multi-DAGs on <= 6 vertices.
- **Source–sink connected** (`cited`): every SSC DAG with tau >= 1 packs, same populations.
- Easy direction: `tau + 1` disjoint dijoins never exist.
- Exact packer vs brute-force colouring: 1282 decisions on random multi-digraphs, agree.
- Dijoin-by-dicuts vs dijoin-by-contraction: 3000 random pairs, agree.
- Condensation preserves tau, the dicut size multiset, and the verdict (1500 random
  digraphs with cycles).
- Isomorph-free enumeration reproduces OEIS A003087 (unlabelled DAGs) for n = 0..7:
  1, 1, 2, 6, 31, 302, 5984, 243668.

Adversarial fixtures (all behave as derived by hand, see `adversarial.py`):

| fixture | error probed | correct answer |
|---|---|---|
| A wide diamond `s->a,b,c->t` | dicut without `delta^-(U)=empty` (would give tau = 1) | tau = 3, packs |
| B `0->1` x3 ; B2 `0->1 x2, 0->2, 1->3 x2, 2->3` | parallel arcs collapsed (tau 3 -> 1, 3 -> 2) | tau = 3, packs |
| C bottleneck `s->a,b,c->x->y->d,e,f->t` | tau over source/sink cuts only (would give 3) | tau = 1 |
| D `K(1,3,1)`, `K(1,4,1)`, crown `K(3,3)` | easy direction mistaken for existence | tau packs, tau + 1 does not |
| E strongly connected; single vertex | empty set / `U = V` as shores | no dicut, tau undefined, empty set is a dijoin |
| F, G weakly disconnected | empty dicut | tau = 0, no dijoin exists |
| H loops | loops in a dicut | never |
| I path | dijoin confused with strengthening (reversal) | all arcs form a dijoin, reversal not SC |
| J diamond + shortcuts | packer using only minimal dicuts | every class meets every dicut |
| K digraph with 2-cycles | condensation must keep parallel arcs | condensation is a multi-DAG, verdict preserved |

## Independent census (before seeing A1)

(see `experiments/woodall-census-audit/census_out/summary.json` and `multisummary_M*.json`)

Simple DAGs, isomorph-free (canonical form = colour refinement + minimum over in-cell
permutations), weakly connected, tau >= 3, exact verdict on each (`census.py 7`, 61 s):

| n | unlabelled DAGs (= A003087) | weakly connected | tau >= 3 | tau = 3 / 4 / 5 / 6 | verdict false | source–sink connected |
|---|---|---|---|---|---|---|
| 4 | 31 | 24 | 2 | 2 / 0 / 0 / 0 | 0 | 2 |
| 5 | 302 | 267 | 44 | 38 / 6 / 0 / 0 | 0 | 44 |
| 6 | 5984 | 5647 | 1519 | 1148 / 340 / 31 / 0 | 0 | 1519 |
| 7 | 243668 | 237317 | 95072 | 63026 / 26152 / 5592 / 302 | 0 | 95072 |

Multi-DAGs (parallel arcs, multiplicity <= M), isomorph-free, weakly connected, tau >= 3
(`multicensus.py`):

| M | n | classes | weakly connected | tau >= 3 | non-SSC among them | verdict false |
|---|---|---|---|---|---|---|
| 2 | 4 | 425 | 401 | 190 | 0 | 0 |
| 2 | 5 | 26422 | 25961 | 17351 | 0 | 0 |
| 3 | 4 | 2724 | 2666 | 1954 | 1 | 0 |
| 3 | 5 | 586426 | 583558 | 514857 | 607 | 0 |

Independent confirmations of my own enumeration:

- Euler transform of the weakly-connected counts reproduces the total counts.
- Weighting every class by (linear extensions)/|Aut| reproduces the labelled
  upper-triangular counts-by-tau of the earlier `#73` sweep **exactly** (n = 6: 2706/674/64;
  n = 7: 283267/81905/17334/1024), so two independent enumerators and two independent tau
  implementations agree on all 95072 classes at n = 7 (`weighted_check.py`, 6 min).

## The space claim: three findings

**S1. For simple DAGs, tau >= 3 on <= 7 vertices forces source–sink connectivity.**
If a source `s` cannot reach a sink `t`, put `R = reach(s)` and `W = V \ R`.  No arc leaves
`R`, so `delta^-(W) = empty` and `delta^+(W)` (the arcs from `W` into `R`) is a dicut,
hence has >= 3 arcs.  `s` and its >= 3 out-neighbours lie in `R`; `t` and its >= 3
in-neighbours lie in `W` (arcs into `W` come only from `W`).  So `n >= 8` in a simple DAG.
The census confirms it: all 95072 tau >= 3 classes on <= 7 vertices are SSC.  Consequently
**every instance of a simple-DAG census up to 7 vertices is already settled by the `cited`
Schrijver / Feofiloff–Younger theorem**; such a census is a test of the implementation, not
of the conjecture.  The first non-SSC simple instance is on 8 vertices
(`s->a,b,c; w1,w2,w3->a,b,c; w1,w2,w3->t`, tau = 3, packs).

**S2. "Condensation licenses restricting to DAGs" licenses multi-DAGs, not simple DAGs.**
Condensations of general digraphs carry parallel arcs (fixture K: a 5-vertex digraph whose
condensation has a 4-fold arc).  Restricting to *simple* DAGs is an additional, unstated
filter unless declared; I know of no reduction that removes parallel arcs while preserving
the packing number in the needed direction (subdividing an arc `u->v` into `u->w->v` can
only increase the number of disjoint dijoins: a packing of the original lifts, but a packing
of the subdivision may use `u->w` and `w->v` in different dijoins).  Non-SSC tau >= 3
instances appear at n = 4 once multiplicity 3 is allowed (`s->a x3, w->t x3, w->a x3`), and
608 of them exist on <= 5 vertices with multiplicity <= 3 — these are the smallest instances
that the cited theorem does **not** settle, and all of them pack.

**S3. tau <= 2 exclusion is sound; the degree filter is not a shortcut.**  tau >= 3 forces
every source to have out-degree >= 3 and every sink in-degree >= 3, but the converse fails
(99 classes at n = 7 and 2 at n = 6 pass the degree filter with tau = 2, fixture C shows a
bottleneck dicut of size 1 behind degree-3 sources and sinks), so a census must compute tau
over all `2^n - 2` shores, not infer it from degrees.
