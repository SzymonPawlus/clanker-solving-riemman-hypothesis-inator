"""Targeted screen: delete a corner (which breaks TWO of the three rigid edges of the side-6
lattice) plus one further point, then try to compress below a = 6.  NUMERICAL / float only."""
import random, json, os, sys
from shrink import lattice28, min_dist
from hop import compress

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 31337
    here = os.path.dirname(os.path.abspath(__file__))
    rng = random.Random(seed)
    base = lattice28(6.20)
    # corner indices in the row-major listing of lattice28: (0,0) is 0, (6,0) is 6, apex is 27
    best = (1e9, None, None)
    for j in range(1, 28):
        keep = [i for i in range(28) if i not in (0, j)]
        pts = [base[i] for i in keep]
        p, a = compress(pts, 6.20, rng, 1.0002, 5.8, sweeps=1500, kicks=4, fine=1e-6)
        if p is None: continue
        flag = "  <-- BELOW 6" if a < 6.0 else ""
        print(f"delete corner0 + {j}: a = {a:.7f}{flag}", flush=True)
        if a < best[0]:
            best = (a, j, p)
            with open(os.path.join(here, 'out', 'shrink_n26c.json'), 'w') as f:
                json.dump({"n": 26, "a": a, "pts": p, "min_dist": min_dist(p),
                           "deleted": [0, j], "margin": 1.0002}, f)
    print("best:", best[0], "deleting corner0 +", best[1])
