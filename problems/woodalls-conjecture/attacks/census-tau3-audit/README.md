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
