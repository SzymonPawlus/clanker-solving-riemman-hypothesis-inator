"""Feasibility search: can n points sit in T_a with all pairwise distances >= 1?

NUMERICAL / float only.  A hit is a *hypothesis*; verify.py re-checks it in exact rationals.
Normalisation: separation 1; T_a corners (0,0), (a,0), (a/2, a*sqrt(3)/2).
"""
import math, random, json, sys, os

SQ3 = math.sqrt(3.0)

def clamp(x, y, a):
    if y < 0.0: y = 0.0
    g = SQ3 * x - y
    if g < 0.0:
        x += (-g) * SQ3 / 4.0; y -= (-g) / 4.0
    g = SQ3 * (a - x) - y
    if g < 0.0:
        x -= (-g) * SQ3 / 4.0; y -= (-g) / 4.0
    if y < 0.0: y = 0.0
    return x, y

def sample(a, rng):
    u, v = rng.random(), rng.random()
    if u + v > 1.0: u, v = 1.0 - u, 1.0 - v
    return (a * (u + v * 0.5), a * v * SQ3 / 2.0)

def energy(pts, target):
    """sum of squared violations"""
    e = 0.0; n = len(pts)
    for i in range(n):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            d = math.hypot(xi - pts[j][0], yi - pts[j][1])
            if d < target:
                e += (target - d) ** 2
    return e

def solve(n, a, target, rng, sweeps=3000):
    pts = [sample(a, rng) for _ in range(n)]
    for s in range(sweeps):
        alpha = 0.55
        worst = 0.0
        for i in range(n):
            fx = fy = 0.0
            xi, yi = pts[i]
            for j in range(n):
                if j == i: continue
                dx = xi - pts[j][0]; dy = yi - pts[j][1]
                d = math.hypot(dx, dy)
                if d < 1e-12:
                    ang = rng.random() * 6.2831853
                    dx, dy, d = math.cos(ang), math.sin(ang), 1e-9
                if d < target:
                    w = (target - d) / d
                    fx += dx * w; fy += dy * w
                    if target - d > worst: worst = target - d
            pts[i] = clamp(xi + alpha * fx, yi + alpha * fy, a)
        if worst < 1e-13:
            return pts, 0.0
        if s % 200 == 199:
            # kick the most-violated point to a fresh random spot
            bad, bv = -1, -1.0
            for i in range(n):
                v = 0.0
                for j in range(n):
                    if j == i: continue
                    d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
                    if d < target: v += target - d
                if v > bv: bv, bad = v, i
            if bad >= 0 and bv > 0:
                pts[bad] = sample(a, rng)
    return pts, energy(pts, target)

def min_dist(pts):
    m = float('inf'); n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            if d < m: m = d
    return m

def hunt(n, a, tries, seed, sweeps=3000, margin=1.002):
    rng = random.Random(seed)
    best = None; bestm = -1.0
    for t in range(tries):
        pts, e = solve(n, a, margin, rng, sweeps=sweeps)
        m = min_dist(pts)
        if m > bestm:
            bestm, best = m, list(pts)
        if e == 0.0 and m >= margin - 1e-12:
            return m, best, t
    return bestm, best, tries

if __name__ == '__main__':
    a = float(sys.argv[1]); ns = [int(t) for t in sys.argv[2].split(',')]
    tries = int(sys.argv[3]); seed = int(sys.argv[4]) if len(sys.argv) > 4 else 2024
    here = os.path.dirname(os.path.abspath(__file__))
    res = {}
    for n in ns:
        m, pts, t = hunt(n, a, tries, seed + 7 * n)
        ok = "FEASIBLE(margin)" if m >= 1.002 - 1e-12 else ("feasible@1" if m >= 1.0 else "no")
        print(f"a={a} n={n}: best min dist {m:.9f}  [{ok}] after {t+1} tries", flush=True)
        res[n] = {"a": a, "min_dist": m, "pts": pts}
        with open(os.path.join(here, 'out', f'feas_a{a}.json'), 'w') as f:
            json.dump(res, f)
