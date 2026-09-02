# 2026-09-02 — Woodall census audit (issue #149, adversary side of pair A)

Worktree `/home/user/wt/149-census-audit`, branch `claude/149-census-audit`.  Model: Fable 5.1.

## Ordering discipline

Per repo RULES.md §5 and problem RULES.md §2 I wrote my own toolkit from
`problems/woodalls-conjecture/README.md` alone and committed it (`a84c59c`) **before**
fetching or reading anything from A1's branch `claude/148-census-tau3`, and before opening
`experiments/woodalls-dicuts/` or `attacks/dijoin-exact-ip-search/`.

## What I reconstructed (experiments/woodall-census-audit/woodall_audit.py)

- Dicut enumeration over all `2^n - 2` shores, insisting on `delta^-(U) = empty`; the arc
  set is a list, so parallel arcs are distinct arcs.  Empty `delta^+(U)` is reported (it
  means weak disconnection, tau = 0, no dijoin exists).
- Dijoin recognition two independent ways (meets every dicut / contraction is strongly
  connected), asserted equal on every call.
- tau, minimum-dicut witness, condensation (keeps parallel inter-component arcs).
- Exact "tau pairwise disjoint dijoins?" by backtracking colouring of arcs (partition WLOG,
  since supersets of dijoins are dijoins) over inclusion-minimal dicuts, symmetry-broken,
  pruned by "missing colours <= unassigned arcs"; cross-checked against a brute-force
  colouring enumerator on 1282 random small multi-digraphs.
- Canonical form for multidigraphs (colour refinement + minimum over in-cell permutations)
  and isomorph-free DAG enumeration by sink extension.

## Validation (validate.py, exit 0; adversarial.py, exit 0)

- README fixtures: path tau=1, cycle has no dicut, diamond tau=2 packs into the two s-t
  paths, near-miss tau=1 and not source-sink connected.
- Every tau=2 instance packs (labelled upper-triangular DAGs n<=5, 2000 random multi-DAGs).
- Every source-sink-connected DAG with tau>=1 packs (same populations).
- tau+1 disjoint dijoins never exist (easy direction is not being mistaken for the hard one).
- verdict(D) == verdict(condensation(D)) on 1500 random digraphs with cycles.
- Unlabelled DAG counts n=0..7: 1,1,2,6,31,302,5984,243668 = OEIS A003087.
- Adversarial fixtures A–K all behave as derived by hand.  One slip was mine: in fixture B2
  I first wrote tau=3 for `0->1 x2, 0->2, 1->3, 2->3 x2`; the tool said tau=2 and it is
  right (U={0,1} cuts only two arcs).  Replaced with `0->1 x2, 0->2, 1->3 x2, 2->3`, tau=3.

## Independent census, before seeing A1

Simple DAGs, isomorph-free, weakly connected, tau>=3 (census.py 7, 61 s):

| n | unlabelled DAGs | weakly connected | tau>=3 | verdict false | source-sink connected |
|---|---|---|---|---|---|
| 4 | 31 | 24 | 2 | 0 | 2 |
| 5 | 302 | 267 | 44 | 0 | 44 |
| 6 | 5984 | 5647 | 1519 | 0 | 1519 |
| 7 | 243668 | 237317 | 95072 | 0 | 95072 |

**Every simple DAG with tau>=3 on <=7 vertices is source-sink connected**, i.e. inside the
`cited` Schrijver / Feofiloff–Younger class where the packing is a theorem.  A simple-DAG
census to n<=7 therefore cannot test the conjecture beyond that theorem.  Reason: if a source
s cannot reach a sink t, then W = V \ reach(s) has delta^-(W) = empty, so delta^+(W) is a
dicut with >=3 arcs, t and its >=3 in-neighbours lie in W, s and its >=3 out-neighbours lie
in reach(s): at least 8 vertices in a simple DAG.  Witness on 8 vertices, checked by the
tool (tau=3, non-SSC, packs): `s->a,b,c; w1,w2,w3->a,b,c; w1,w2,w3->t`.

Multi-DAGs (parallel arcs, multiplicity <= M), isomorph-free, weakly connected, tau>=3:

| M | n | classes | tau>=3 | non-SSC among them | verdict false |
|---|---|---|---|---|---|
| 2 | 4 | 425 | 190 | 0 | 0 |
| 2 | 5 | 26422 | 17351 | 0 | 0 |
| 3 | 4 | 2724 | 1954 | 1 | 0 |
| 3 | 5 | (running) | | | |

The first tau>=3 instance outside the cited theorem is a **multi**-DAG on 4 vertices:
`s->a x3, w->t x3, w->a x3` (tau=3, packs).  Condensations of general digraphs are
multi-DAGs, so "condensation lets us restrict to DAGs" licenses restricting to multi-DAGs,
not to simple DAGs; no reduction removing parallel arcs is stated in the README and I know
of none that preserves the packing number in the needed direction (subdividing a parallel
arc can only increase the number of disjoint dijoins).

Multi-DAG census finished for M=3, n=5: 586426 classes, 514857 with tau>=3, 607 of them
non-SSC, all 514857 pack (110 s).

## Cross-checks against the prior #73 sweep (labelled, redundant enumeration)

- My labelled upper-triangular tau-histograms agree with `sweep-n5` and `sweep-n6` on every
  tau (their tau=0 is one less because they skip the empty graph).
- Weighted check (`weighted_check.py`): sum over my isomorphism classes of
  e(G)/|Aut(G)| (linear extensions over automorphisms) equals the number of upper-triangular
  matrices in the class, so my isomorph-free census weighted this way must reproduce their
  counts by tau.  It does, exactly: n=6 {3: 2706, 4: 674, 5: 64}; n=7 {3: 283267, 4: 81905,
  5: 17334, 6: 1024} (6 min).  This simultaneously checks isomorph-freeness (no class
  counted twice or missed) and tau agreement between two independent implementations on all
  95072 tau>=3 classes at n=7.
- Euler transform of my weakly-connected unlabelled counts reproduces my total unlabelled
  counts, and the totals equal OEIS A003087 as I remember it (oeis.org is egress-blocked;
  1, 1, 2, 6, 31, 302, 5984, 243668 taken from memory, n=8 = 20286025 unverified).
