"""EXACT construction: partition T_6 into 28 convex cells of diameter <= 1.

Cells = Voronoi cells (inside T_6) of the triangular array
    p_{ij} = (u0 + (sqrt3/2) i,  v0 + (sqrt3/2) j),   i,j >= 0,  i+j <= 6,
i.e. the Delta(7) triangular lattice of spacing sqrt3/2, centred in T_6.
All arithmetic in Q(sqrt3).  NO FLOATS DECIDE ANYTHING.
"""
from fractions import Fraction as F
from exact import Q3, q3, verify, voronoi_cells, diam2, HALF_SQ3
import sys

def build(a=6, m=6, u0=None, v0=None):
    a = q3(a)
    g = HALF_SQ3                     # lattice spacing sqrt3/2
    if u0 is None:
        # centre the side-(m*g) array inside T_a:  margin (a - m*g)/3 on each coord
        u0 = (a - g*m) * F(1, 3)
        v0 = u0
    sites = []
    for i in range(m+1):
        for j in range(m+1-i):
            sites.append((u0 + g*i, v0 + g*j))
    return sites, a

if __name__ == "__main__":
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    sites, a = build(m=m)
    print("sites: %d   offset u0=%s" % (len(sites), sites[0][0]))
    cells = voronoi_cells(sites, a)
    ok, worst = verify(cells, a)
    print("theoretical hexagon bound: every cell should sit inside a diameter-1 hexagon")
    if ok:
        import json
        json.dump({"a": "6", "n": len(cells),
                   "note": "vertices as [ [a_u,b_u], [a_v,b_v] ] meaning a+b*sqrt3 in the (e1,e2) basis",
                   "cells": [[[[str(u.a), str(u.b)], [str(v.a), str(v.b)]] for (u, v) in P]
                             for P in cells]},
                  open("cert28.json", "w"), indent=0)
        print("wrote cert28.json")
