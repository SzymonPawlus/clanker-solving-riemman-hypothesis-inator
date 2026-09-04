"""Seed the n=26 search from the certified n=25 configuration (plus one extra point) and from the
best n=24 configuration (plus two).  NUMERICAL / float only."""
import random, json, os, sys, math
from shrink import min_dist, sample
from hop import compress

here = os.path.dirname(os.path.abspath(__file__))
seed = int(sys.argv[1]); n = int(sys.argv[2]); src = sys.argv[3]
rng = random.Random(seed)
data = json.load(open(os.path.join(here, 'out', src)))
base = [tuple(p) for p in data['pts']]
a_src = data['a']
best = (1e9, None)
for r in range(400):
    a0 = 6.25
    sc = a0 / a_src
    pts = [(x * sc, y * sc) for x, y in base]
    while len(pts) < n:
        pts.append(sample(a0, rng))
    pts = [(x + rng.gauss(0, 0.10), y + rng.gauss(0, 0.10)) for x, y in pts]
    p, a = compress(pts, a0, rng, 1.0002, 5.6, sweeps=2000, kicks=5, fine=1e-7)
    if p is not None and a < best[0]:
        best = (a, p)
        flag = "   <-- BELOW 6" if a < 6.0 else ""
        print(f"round {r}: a = {a:.8f}  mind = {min_dist(p):.9f}{flag}", flush=True)
        with open(os.path.join(here, 'out', f'shrink_n{n}s.json'), 'w') as f:
            json.dump({"n": n, "a": a, "pts": p, "min_dist": min_dist(p), "margin": 1.0002}, f)
