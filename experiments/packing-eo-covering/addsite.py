"""Insert a site into the best n-cell config (at the worst cell's centroid) and re-descend."""
import json, sys, math
from opt import Diagram, descend
from search import triangle, power_cells, diam2
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src)); a = d["a"]
tri = triangle(a); cs = power_cells(d["sites"], d["weights"], tri)
dm = [diam2(p) for p in cs]
order = sorted(range(len(cs)), key=lambda i: -dm[i])
best = (1e18, None)
for k in order[:6]:
    P = cs[k]
    cx = sum(p[0] for p in P)/len(P); cy = sum(p[1] for p in P)/len(P)
    s2 = [list(p) for p in d["sites"]] + [[cx, cy]]
    w2 = list(d["weights"]) + [0.0]
    dg = Diagram(a, s2, w2); v = descend(dg)
    print("  split cell %d -> %.9f" % (k, v), flush=True)
    if v < best[0]:
        best = (v, ([list(p) for p in dg.s], list(dg.w)))
        json.dump({"a": a, "n": len(s2), "max_diam": v, "sites": best[1][0], "weights": best[1][1]},
                  open(out, "w"))
print("BEST n=%d %.12f" % (d["n"]+1, best[0]))
