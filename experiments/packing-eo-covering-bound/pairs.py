"""Which points must be removed from the 28-point lattice before T_a can be compressed below 6?

The side-6 lattice has 7 points on each edge spanning length 6, so it is rigid at a = 6.
Deleting a corner breaks TWO edges at once.  This script screens every deletion pattern.

NUMERICAL / float only.  Winners are re-certified exactly by verify.py.
"""
import math, random, json, os, sys, itertools
from shrink import lattice28, relax, min_dist, sample, clamp, SQ3

def compress(pts, a0, rng, margin=1.0002, floor=5.4, sweeps=350, kicks=6, fine=2e-8):
    pts = [tuple(p) for p in pts]
    n = len(pts)
    if not relax(pts, a0, margin, 3000, rng):
        return None, a0
    a = a0; step = 0.004
    while step > fine and a > floor:
        na = max(a * (1.0 - step), floor)
        r = na / a
        trial = [(x * r, y * r) for (x, y) in pts]
        ok = relax(trial, na, margin, sweeps, rng)
        if not ok:
            for k in range(kicks):
                bad, bv = -1, -1.0
                for i in range(n):
                    v = 0.0
                    for j in range(n):
                        if j == i: continue
                        d = math.hypot(trial[i][0] - trial[j][0], trial[i][1] - trial[j][1])
                        if d < margin: v += margin - d
                    if v > bv: bv, bad = v, i
                trial[bad] = sample(na, rng)
                if relax(trial, na, margin, sweeps, rng):
                    ok = True; break
        if ok:
            pts = trial; a = na
        else:
            step *= 0.5
    return pts, a

if __name__ == '__main__':
    ndel = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 4242
    here = os.path.dirname(os.path.abspath(__file__))
    rng = random.Random(seed)
    base = lattice28(6.05)
    n = 28 - ndel
    results = []
    best = (1e9, None, None)
    for combo in itertools.combinations(range(28), ndel):
        pts = [base[i] for i in range(28) if i not in combo]
        p, a = compress(pts, 6.05, rng)
        if p is None: continue
        results.append((a, combo))
        if a < best[0]:
            best = (a, combo, p)
            print(f"  delete {combo}: a = {a:.8f}  (min dist {min_dist(p):.9f})", flush=True)
            with open(os.path.join(here, 'out', f'shrink_n{n}p.json'), 'w') as f:
                json.dump({"n": n, "a": a, "pts": p, "min_dist": min_dist(p),
                           "deleted": list(combo), "margin": 1.0002}, f)
    results.sort()
    print("best 10:", [(round(a, 6), c) for a, c in results[:10]])
    print(f"n={n}: best a = {best[0]:.8f}")
