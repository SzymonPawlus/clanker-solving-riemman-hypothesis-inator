"""Soundness controls for the active-region B&B.  Run before any bound is believed.

Control 1 (the one that matters).  The optimal triangular-lattice packings
n = k(k+1)/2 at d = 2(k-1) (Oler / Erdos-Oler, `cited`) must map to independent sets
of the conflict graph, at every level.  If the conflict relation ever declared two of
those cells adjacent, the whole method would over-prune and every "unsat" would be
worthless.

Control 2.  The solver must return SAT at side lengths where a packing demonstrably
exists (d >= d(n)); a single UNSAT there is a bug or a broken lemma.
"""
import sys
from fractions import Fraction

sys.path.insert(0, ".")
from arbb import geom, search


def lattice_packing(k):
    """(n, d) and the exact points of the triangular packing: n = k(k+1)/2, d = 2(k-1)."""
    pts = [(i, j) for j in range(k) for i in range(k - j)]
    return len(pts), 2 * (k - 1), pts


def control_known_packings(levels=(2, 3, 4, 5, 6)):
    ok = True
    for k in range(2, 7):
        n, d, pts = lattice_packing(k)
        for L in levels:
            h = Fraction(d, 1 << L)
            if h >= 2:
                continue
            adj, cells, verts = geom.conflict_bitsets(L, d, 1)
            idx = []
            for (i, j) in pts:
                a = Fraction(2 * i) / h
                b = Fraction(2 * j) / h
                idx.append(geom.locate(a, b, L))
            if len(set(idx)) != n:
                print(f"FAIL n={n} d={d} L={L}: two points landed in one cell")
                ok = False
                continue
            bad = [(u, v) for ui, u in enumerate(idx) for v in idx[ui + 1:]
                   if (adj[u] >> v) & 1]
            if bad:
                print(f"FAIL n={n} d={d} L={L}: {len(bad)} optimal pairs declared conflicting")
                ok = False
            else:
                print(f"  ok  n={n:2d} d={d} L={L}: {n} distinct cells, independent")
    return ok


def control_feasible_sat(cases):
    ok = True
    for (n, p, q, L) in cases:
        inst = search.Instance(n, p, q, L)
        r = inst.solve(node_budget=3_000_000, time_budget=120)
        star = "" if r == "sat" else "   <-- PROBLEM" if r == "unsat" else "   (undecided)"
        print(f"  n={n:2d} d={p}/{q}={float(Fraction(p,q)):.4f} L={L}: {r}"
              f" nodes={inst.nodes}{star}")
        if r == "unsat":
            ok = False
    return ok


if __name__ == "__main__":
    print("Control 1 - known optimal packings survive the conflict relation")
    ok1 = control_known_packings()
    print("Control 2 - solver returns SAT where a packing exists")
    ok2 = control_feasible_sat([
        (12, 7465, 1000, 4), (12, 15, 2, 4), (12, 8, 1, 4),
        (15, 8, 1, 4), (15, 9, 1, 4),
        (24, 1147, 100, 4), (24, 12, 1, 4),
    ])
    print("ALL CONTROLS PASS" if (ok1 and ok2) else "CONTROLS FAILED")
    sys.exit(0 if (ok1 and ok2) else 1)
