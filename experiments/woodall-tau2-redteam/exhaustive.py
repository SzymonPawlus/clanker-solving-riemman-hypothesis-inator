"""Exhaustive attack on the tau=2 theorem AND on the tau2-robbins construction.

Search space (stated exactly), pass 1: every digraph on n=4 labelled vertices in
which each of the 12 ordered pairs (u,v), u != v, carries multiplicity 0, 1 or 2
-- 3^12 = 531441 digraphs, all of them, no isomorphism reduction.  Loops are
excluded (they lie in no cut).  Multiplicity 2 is included because parallel arcs
are exactly what makes tau = 2 achievable on tiny vertex sets.

For every digraph with tau = 2 we check, independently:
  (T)  two arc-disjoint dijoins partitioning A exist               [the theorem]
  (L1) the underlying multigraph has no bridge                     [Lemma 1]
  (L1c) every weakly connected component is bridgeless
  (R)  the DFS Robbins orientation is strongly connected on each
       nontrivial component                                        [Robbins]
  (C)  the agreement/disagreement colouring from that orientation
       gives two dijoins                                    [the construction]
Any failure is a counterexample to the sketch and is printed.
"""
import sys, itertools
from dicut import dicuts, is_dijoin
from twocol import two_dijoins_exact
from robbins import robbins_colouring, components, has_bridge, strongly_connected_on


def check_digraph(n, arcs, stats, fails):
    cs = dicuts(n, arcs)
    if not cs:
        return
    t = min(len(c) for c in cs)
    if t != 2:
        return
    stats['tau2'] += 1
    res = two_dijoins_exact(n, arcs, cs)
    if res is None:
        fails.append(('THEOREM-FAILS', arcs)); return
    br = has_bridge(n, arcs)
    if br is not None:
        fails.append(('LEMMA1-FAILS(bridge)', arcs, br))
    Jp, Jm, O = robbins_colouring(n, arcs)
    for comp in components(n, arcs):
        if len(comp) > 1 and not strongly_connected_on(n, O, comp):
            fails.append(('ROBBINS-ORIENTATION-NOT-STRONG', arcs, sorted(comp)))
            break
    else:
        if not (is_dijoin(n, arcs, Jp, cs) and is_dijoin(n, arcs, Jm, cs)):
            fails.append(('CONSTRUCTION-FAILS', arcs, sorted(Jp), sorted(Jm)))
    ncomp = len(components(n, arcs))
    if ncomp > 1:
        stats['disconnected_tau2'] += 1


def main():
    n = 4
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v]
    stats = {'tau2': 0, 'total': 0, 'disconnected_tau2': 0}
    fails = []
    for mult in itertools.product((0, 1, 2), repeat=len(pairs)):
        arcs = []
        for p, k in zip(pairs, mult):
            arcs.extend([p] * k)
        stats['total'] += 1
        if len(arcs) < 2:
            continue
        check_digraph(n, arcs, stats, fails)
    print(f"n=4, multiplicity<=2, all {stats['total']} digraphs")
    print(f"  with tau=2: {stats['tau2']}  (of which weakly disconnected: {stats['disconnected_tau2']})")
    print(f"  FAILURES: {len(fails)}")
    for f in fails[:20]:
        print("   ", f)

if __name__ == "__main__":
    main()
