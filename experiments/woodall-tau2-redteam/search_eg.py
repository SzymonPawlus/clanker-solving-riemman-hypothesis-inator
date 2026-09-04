"""Search for a counterexample to the 0/1-weighted Edmonds-Giles statement at
tau_w = 2, reconstructed from the definitions (I could not reach Schrijver 1980:
ir.cwi.nl is blocked by this sandbox's egress proxy).

Target: a digraph D and S subset of A ("weight-one" arcs) with
   (i)  every dicut C has |C cap S| >= 2      [tau_w = 2]
   (ii) S cannot be split into two disjoint dijoins.

Observation used to make the search cheap: two disjoint dijoins inside S exist
iff the hypergraph H_S = { C cap S : C a dicut } is 2-colourable (no colour
class misses a hyperedge <=> no hyperedge monochromatic).  The smallest
obstructions with all hyperedges of size >= 2 are odd cycles of size-2
hyperedges; the smallest of those is a triangle on |S| = 3.

Search space (stated exactly): all labelled ACYCLIC simple digraphs on n
vertices whose arcs go from a lower to a higher index, i.e. every subset of the
n(n-1)/2 forward pairs -- 2^(n(n-1)/2) digraphs, covering every DAG on n
labelled vertices up to relabelling.  DAGs suffice because contracting strong
components preserves the dicut family (arcs inside a strong component lie in no
dicut), and such arcs are useless in any dijoin.
"""
import sys
from itertools import combinations
from dicut import dicuts, two_disjoint_dijoins, tau_w

def run(n, max_report=5, only_triples=True):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    P = len(pairs)
    found = []
    for mask in range(1 << P):
        arcs = [pairs[k] for k in range(P) if mask >> k & 1]
        if len(arcs) < 3:
            continue
        cs = dicuts(n, arcs)
        if len(cs) < 3:
            continue
        m = len(arcs)
        idxs = range(m)
        cands = combinations(idxs, 3) if only_triples else (
            c for r in range(3, m + 1) for c in combinations(idxs, r))
        for S in cands:
            Sset = frozenset(S)
            traces = set()
            ok = True
            for c in cs:
                t = c & Sset
                if len(t) < 2:
                    ok = False
                    break
                traces.add(t)
            if not ok:
                continue
            if two_disjoint_dijoins(n, arcs, Sset) is None:
                found.append((arcs, sorted(Sset), sorted(sorted(t) for t in traces)))
                if len(found) >= max_report:
                    return found
    return found

if __name__ == "__main__":
    n = int(sys.argv[1]); only_triples = (len(sys.argv) < 3 or sys.argv[2] != "all")
    res = run(n, only_triples=only_triples)
    print(f"n={n} only_triples={only_triples}: {len(res)} counterexample(s)")
    for arcs, S, traces in res:
        print("  arcs   =", arcs)
        print("  S      =", S, "->", [arcs[i] for i in S])
        print("  traces =", traces)
