"""Streaming statistics over the surviving level-L profiles of P(n,t,strict).

Reports:
  * how many profiles survive,
  * the union of cells that appear in any survivor (the 'supportable region'),
    as a count and as a fraction of the container's area,
  * whether every survivor puts a point in each of the three corner cells at
    level L (the corner-forcing predicted by the strict Oler-hull rule).
Usage: python3 analyse.py n t strict L out.json [time_limit]
"""
import json, sys, time
from fractions import Fraction
from eo4.search import Prover
from eo4 import geom

n = int(sys.argv[1]); t = Fraction(sys.argv[2]); strict = sys.argv[3] == "1"
L = int(sys.argv[4]); out = sys.argv[5]
tl = float(sys.argv[6]) if len(sys.argv) > 6 else 600.0

pr = Prover(n, t, strict, L, max_cited=8)
LM = pr.LM
S = 1 << LM
CORNERS = [(0, geom.UP, 0, 0), (0, geom.UP, 0, 0), (0, geom.UP, 0, 0)]
# level-L corner cells: up(L,0,0) at A, up(L,2^L-1,0) at B, up(L,0,2^L-1) at C
corner_cells = {(L, geom.UP, 0, 0), (L, geom.UP, S - 1, 0), (L, geom.UP, 0, S - 1)}

t0 = time.time()
root = ((geom.root_cell(), n),)
used = set()
nsurv = 0
all_have_3_corners = True
min_corners = 99
nodes = 0
outcome = "proved"
if not pr.node_refuted(root):
    stack = [root]
    outcome = "proved"
    while stack:
        node = stack.pop(); nodes += 1
        if time.time() - t0 > tl:
            outcome = "timeout"; break
        if min(c[0][0] for c in node) >= L:
            nsurv += 1; outcome = "survivors"
            cs = set()
            for c, m in node:
                used.add(c); cs.add(c)
            k = len(cs & corner_cells)
            min_corners = min(min_corners, k)
            if k < 3:
                all_have_3_corners = False
            continue
        for child in pr.branch(node):
            if not pr.node_refuted(child):
                stack.append(child)
res = {"n": n, "t": str(t), "strict": strict, "level": L, "outcome": outcome,
       "nodes": nodes, "survivors": nsurv, "seconds": round(time.time() - t0, 2),
       "cells_total": 4 ** L, "cells_supportable": len(used),
       "supportable_area_fraction": round(len(used) / 4 ** L, 5),
       "every_survivor_occupies_all_3_corner_cells": all_have_3_corners,
       "min_corner_cells_occupied": (None if nsurv == 0 else min_corners),
       "supportable_cells": sorted(used)}
with open(out, "w") as f:
    json.dump(res, f, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "supportable_cells"}))
