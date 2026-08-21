"""Drive the power-diagram optimiser from a honeycomb start, deleting sites."""
import math, json, random, sys, itertools
from opt import Diagram, descend, lattice_init
from search import triangle, diams

SQ3 = math.sqrt(3.0)

def load(a):
    d = json.load(open("hex_a%g.json" % a))
    return d["centres"], d["clipped_area"]

def cellareas(dg):
    from honeycomb import area
    return [area(dg.cell(i)) for i in range(dg.n)]

def try_subset(a, cs, drop, seed, verbose=True):
    sites = [c for i, c in enumerate(cs) if i not in drop]
    w = [0.0]*len(sites)
    dg = Diagram(a, sites, w)
    v0 = dg.truemax()
    v = descend(dg)
    return v0, v, ([list(p) for p in dg.s], list(dg.w))

if __name__ == "__main__":
    a = float(sys.argv[1]); ndrop = int(sys.argv[2]); ntry = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    cs, ar = load(a)
    order = sorted(range(len(cs)), key=lambda i: ar[i])
    rng = random.Random(seed)
    best = (1e18, None)
    cands = []
    if ndrop == 0:
        cands = [()]
    else:
        # smallest-area sites first, plus random subsets
        for combo in itertools.combinations(order[:8], ndrop):
            cands.append(combo)
        rng.shuffle(cands)
        cands = cands[:ntry]
    for drop in cands:
        v0, v, cfg = try_subset(a, cs, set(drop), seed)
        print("drop=%s  start %.6f -> %.9f" % (str(drop), v0, v), flush=True)
        if v < best[0]:
            best = (v, cfg, drop)
            json.dump({"a": a, "n": len(cs)-ndrop, "max_diam": v,
                       "sites": cfg[0], "weights": cfg[1]},
                      open("drv_a%g_n%d.json" % (a, len(cs)-ndrop), "w"))
    print("BEST n=%d : %.12f (drop %s)" % (len(cs)-ndrop, best[0], str(best[2])))
