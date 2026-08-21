"""Greedy site removal from a good n=28 covering: 28 -> 27 -> 26 -> ...
FLOATS ONLY (search stage)."""
import math, json, time, sys, os
from opt import Diagram, descend
HERE = os.path.dirname(os.path.abspath(__file__))

def full(dg):   return descend(dg, ps=(12., 50., 300.), step0=0.06, tol=1e-5)
def quick(dg):  return descend(dg, ps=(15., 80.), step0=0.05, tol=2e-3)

def main():
    a = 6.0
    d = json.load(open(os.path.join(HERE, "hex_a6.json")))
    sites = [list(c) for c in d["centres"]]; w = [0.0]*len(sites)
    dg = Diagram(a, sites, w); v = full(dg)
    sites, w = [list(p) for p in dg.s], list(dg.w)
    print("n=%d  %.9f" % (len(sites), v), flush=True)
    json.dump({"a": a, "n": len(sites), "max_diam": v, "sites": sites, "weights": w},
              open(os.path.join(HERE, "greedy_n%d.json" % len(sites)), "w"))
    while len(sites) > 24:
        best = (1e18, None, None)
        for i in range(len(sites)):
            s2 = [p for j, p in enumerate(sites) if j != i]
            w2 = [x for j, x in enumerate(w) if j != i]
            dg = Diagram(a, s2, w2)
            v2 = quick(dg)
            if v2 < best[0]:
                best = (v2, ([list(p) for p in dg.s], list(dg.w)), i)
            print("   remove %d -> %.6f" % (i, v2), flush=True)
        sites, w = best[1]
        dg = Diagram(a, sites, w)
        v = full(dg)
        for _ in range(2):
            v = min(v, full(dg))
        sites, w = [list(p) for p in dg.s], list(dg.w)
        print("n=%d  BEST %.9f (removed %d)" % (len(sites), v, best[2]), flush=True)
        json.dump({"a": a, "n": len(sites), "max_diam": v, "sites": sites, "weights": w},
                  open(os.path.join(HERE, "greedy_n%d.json" % len(sites)), "w"))

main()
