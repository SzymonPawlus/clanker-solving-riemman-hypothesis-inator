"""Reproduce everything: validation on the cited small cases, then k = 7.

  python3 run_all.py          (about 3 minutes)
"""
import json, sys, time
from certify import bnb

# a = k-1 is the Erdos-Oler threshold side; the target is Delta(k) - 2, i.e. one less
# than the number of points a counterexample to EO(k) would need.
CASES = [(2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
res = []
for a, k in CASES:
    target = k * (k + 1) // 2 - 2
    best = None
    for t in range(target, 0, -1):
        t0 = time.time()
        w, st, stats = bnb(a, t, max_boxes=60000, progress=0)
        stats["seconds"] = round(time.time() - t0, 1)
        if st:
            break
        best = stats
        if t <= a * (a + 1) // 2 + 1:
            break
    row = {"a": a, "k": k, "n_counterexample": k * (k + 1) // 2 - 1,
           "EO_target_leq": target,
           "best_certified": (best or {}).get("worst_certified_R2"),
           "R1_lemmaA": a * (a + 1) // 2 + 1,
           "closes_EO_lattice_case": best is not None and best["worst_certified_R2"] <= target,
           "boxes": (best or {}).get("boxes_processed"), "seconds": (best or {}).get("seconds")}
    print(json.dumps(row), flush=True)
    res.append(row)
json.dump(res, open("out/run_all.json", "w"), indent=1)
