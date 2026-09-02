"""Search the 'ring of length 6 + three solid 3-arc paths' family for a {0,1}-weighted
Edmonds-Giles counterexample with tau_w = 2 (Schrijver / Younger k=1 shape, per literature
snippets).  Status: numerical.  Exhaustive over the stated family; uses tau2lib only."""
import json, itertools, sys, time
from tau2lib import dicuts, two_packing_within, tau

def instance(ring_or, ends, path_or, ring_w=0):
    # ring r0..r5 = vertices 0..5 ; path i has internal vertices 6+2i, 7+2i
    arcs, w = [], []
    for k in range(6):
        u, v = k, (k + 1) % 6
        arcs.append((u, v) if ring_or[k] else (v, u)); w.append(ring_w)
    for i in range(3):
        x, y = ends[i]
        p, q = 6 + 2 * i, 7 + 2 * i
        chain = [(x, p), (p, q), (q, y)]
        for j, (u, v) in enumerate(chain):
            arcs.append((u, v) if path_or[i][j] else (v, u)); w.append(1)
    return 12, arcs, w

def check(n, arcs, w):
    tw = tau(n, arcs, w)
    if tw != 2:
        return None
    return two_packing_within(n, arcs, w) is None

hits = []
t0 = time.time()
end_patterns = {"opposite": [(0, 3), (2, 5), (4, 1)], "adjacent": [(0, 1), (2, 3), (4, 5)],
                "skip": [(0, 2), (2, 4), (4, 0)]}
count = 0
for name, ends in end_patterns.items():
    for ring_or in itertools.product((0, 1), repeat=6):
        for por in itertools.product((0, 1), repeat=3):      # same orientation pattern on all 3 paths
            n, arcs, w = instance(ring_or, ends, [por] * 3)
            count += 1
            r = check(n, arcs, w)
            if r:
                hits.append({"pattern": name, "ring_or": ring_or, "path_or": por, "arcs": arcs, "w": w})
                print("HIT", name, ring_or, por, flush=True)
print(f"symmetric family: {count} instances, {len(hits)} hits, {time.time()-t0:.0f}s")
json.dump(hits, open("ring_hits.json", "w"), indent=1)
