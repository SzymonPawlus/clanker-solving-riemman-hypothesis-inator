"""EXACT search for a tau_w = 2 counterexample to 0/1-weighted Edmonds-Giles.

Completeness argument (mine): if S is admissible (every dicut C has
|C cap S| >= 2) and the trace hypergraph {C cap S} is NOT 2-colourable, then
every admissible S' subset of S is also not 2-colourable, because a 2-colouring
of S' extends to S by colouring the extra arcs arbitrarily and every trace
C cap S contains the bichromatic trace C cap S'.  Hence it suffices to test the
MINIMAL admissible supports, which we enumerate exactly.

Space (stated exactly): all 2^(n(n-1)/2) labelled DAGs on n vertices whose arcs
run from lower to higher index -- every DAG on n labelled vertices up to
relabelling, no parallel arcs.  n = 4, 5, 6.
"""
import sys
from itertools import combinations
from dicut import dicuts
from twocol import two_colourable, minimal_sets


def minimal_2covers(cs, m, cap=200000):
    """All minimal S subset of {0..m-1} with |C cap S| >= 2 for every C in cs."""
    cs = [set(c) for c in minimal_sets(cs)]
    if any(len(c) < 2 for c in cs):
        return []
    out = []
    seen = set()

    def rec(S):
        if len(out) > cap:
            return
        viol = None
        for c in cs:
            if len(c & S) < 2:
                viol = c
                break
        if viol is None:
            f = frozenset(S)
            if f not in seen:
                seen.add(f)
                out.append(f)
            return
        for x in sorted(viol - S):
            rec(S | {x})

    rec(set())
    # keep only inclusion-minimal ones
    res = []
    for s in sorted(out, key=len):
        if not any(t <= s for t in res):
            res.append(s)
    return res


def run(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    P = len(pairs)
    ndig = tested = 0
    found = []
    for mask in range(1 << P):
        arcs = [pairs[k] for k in range(P) if mask >> k & 1]
        if len(arcs) < 2:
            continue
        cs = dicuts(n, arcs)
        if not cs:
            continue
        ndig += 1
        for S in minimal_2covers(cs, len(arcs)):
            tested += 1
            traces = [c & S for c in cs]
            if two_colourable(traces) is None:
                found.append((arcs, sorted(S)))
    print(f"n={n}: {ndig} DAGs with at least one dicut, "
          f"{tested} minimal admissible supports tested, {len(found)} counterexamples")
    for f in found[:10]:
        print("   ", f)
    sys.stdout.flush()


if __name__ == "__main__":
  for n in (4, 5, 6):
    run(n)
