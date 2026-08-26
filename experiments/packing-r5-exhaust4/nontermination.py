"""Why the cell exhaustion can never close EO(4): the explicit surviving node.

T(1) contains the 10-point triangular lattice
    P(p,q) = ((p + q/2)/3, q*sqrt3/6),   p,q >= 0, p+q <= 3,
whose pairwise distances are all >= 1/3, with the 1/3's attained.  Delete any one
point and 9 points at pairwise distance >= 1/3 remain.  For every level L, put
each of those 9 points in a closed level-L cell containing it.  If the resulting
node is refuted by none of the rules, the branch containing it is never pruned,
so the search cannot terminate at that level -- at ANY level.

This script tests exactly that, in exact arithmetic, for each of the three
D3-classes of deleted point (corner / edge / centre) and for L = 2..LMAX.
"""
import json, sys
from fractions import Fraction
from eo4.search import Prover
from eo4 import geom

LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
OUT = sys.argv[2] if len(sys.argv) > 2 else "out/nontermination.json"

LATTICE = [(p, q) for q in range(4) for p in range(4 - q)]
assert len(LATTICE) == 10
CLASSES = {"corner": (0, 0), "edge": (1, 0), "centre": (1, 1)}


def cell_of(p, q, L):
    """A closed level-L cell containing the lattice point P(p,q).

    In level-L lattice coordinates P(p,q) is (2^L p/3, 2^L q/3).  The cell
    up(L,i,j) is {x>=i, y>=j, (x-i)+(y-j)<=1}; down(L,i,j) is the complementary
    half of the unit rhombus.  3 never divides 2^L so neither coordinate is an
    integer; only the anti-diagonal can be hit exactly, and then either cell
    contains the point (its closed edge), so `<=` is safe.
    """
    S = 1 << L
    x = Fraction(S * p, 3)
    y = Fraction(S * q, 3)
    i, j = int(x), int(y)              # floor: x, y >= 0
    if (x - i) + (y - j) <= 1:
        return (L, geom.UP, i, j)
    return (L, geom.DOWN, i, j)


def exact_min_sq_distance(pts):
    """Exact min squared distance among lattice points P(p,q), in units of 1."""
    best = None
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            (p1, q1), (p2, q2) = pts[a], pts[b]
            dp, dq = p1 - p2, q1 - q2
            v = Fraction(dp * dp + dp * dq + dq * dq, 9)
            best = v if best is None else min(best, v)
    return best


rows = []
for name, dropped in CLASSES.items():
    pts = [pq for pq in LATTICE if pq != dropped]
    assert len(pts) == 9
    mind2 = exact_min_sq_distance(pts)
    for L in range(2, LMAX + 1):
        cells = {}
        for pq in pts:
            c = cell_of(pq[0], pq[1], L)
            cells[c] = cells.get(c, 0) + 1
        node = tuple(sorted(cells.items()))
        pr = Prover(9, Fraction(1, 3), True, L, max_cited=8)
        refuted = pr.node_refuted(node)
        # which rule, if any
        why = []
        for c, m in node:
            if pr.cell_refutes(c, m):
                why.append("cap")
        ks = list(node)
        for a in range(len(ks)):
            for b in range(a + 1, len(ks)):
                if pr.pair_refutes(ks[a][0], ks[b][0]):
                    why.append("pair")
        if pr.use_oler and pr.oler_refutes(node):
            why.append("oler")
        rows.append({"dropped": name, "level": L, "distinct_cells": len(node),
                     "min_sq_distance_exact": str(mind2),
                     "refuted": refuted, "rules_firing": sorted(set(why))})

res = {"min_sq_distance_target": "1/9", "rows": rows,
       "survives_at_every_tested_level": {
           name: all(not r["refuted"] for r in rows if r["dropped"] == name)
           for name in CLASSES}}
with open(OUT, "w") as f:
    json.dump(res, f, indent=1)
for r in rows:
    print(r["dropped"], "L=%d" % r["level"], "cells=%d" % r["distinct_cells"],
          "refuted=%s" % r["refuted"], r["rules_firing"])
print(json.dumps(res["survives_at_every_tested_level"]))
