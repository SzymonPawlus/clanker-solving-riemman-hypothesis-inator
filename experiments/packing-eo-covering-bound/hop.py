"""Basin-hopping search for a 1-separated 26-point set in T_a with a < 6.

NUMERICAL / float only; winners must survive verify.py (exact rationals) before they count.
"""
import math, random, json, os, sys
from shrink import lattice28, relax, min_dist, sample, SQ3

def compress(pts, a0, rng, margin, floor, sweeps=2500, kicks=6, fine=1e-7):
    pts = [tuple(p) for p in pts]
    n = len(pts)
    if not relax(pts, a0, margin, 3000, rng):
        return None, a0
    a = a0; step = 0.003; good = 0
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
            pts = trial; a = na; good += 1
            if good >= 3:
                step = min(step * 1.6, 0.004); good = 0
        else:
            step *= 0.5; good = 0
    return pts, a

if __name__ == '__main__':
    n = int(sys.argv[1]); margin = float(sys.argv[2]); seed = int(sys.argv[3])
    rounds = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    here = os.path.dirname(os.path.abspath(__file__))
    rng = random.Random(seed)
    besta, bestp = 1e9, None
    for r in range(rounds):
        if bestp is None or r % 4 == 0:
            start = [sample(6.30, rng) for _ in range(n)]
            a0 = 6.30
        else:
            # shake the incumbent
            amp = rng.choice([0.05, 0.12, 0.25])
            a0 = besta * 1.02
            sc = a0 / besta
            start = [(x * sc + rng.gauss(0, amp), y * sc + rng.gauss(0, amp)) for x, y in bestp]
        p, a = compress(start, a0, rng, margin, 5.6)
        if p is not None and a < besta:
            besta, bestp = a, p
            print(f"  n={n} round {r}: a = {a:.8f}  mind = {min_dist(p):.9f}", flush=True)
            with open(os.path.join(here, 'out', f'shrink_n{n}h.json'), 'w') as f:
                json.dump({"n": n, "a": besta, "pts": bestp, "min_dist": min_dist(bestp),
                           "margin": margin}, f)
    print(f"n={n}: best a = {besta:.8f}", flush=True)
