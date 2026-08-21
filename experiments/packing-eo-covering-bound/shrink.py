"""Shrink-the-triangle search for the least a admitting n points at pairwise distance >= 1.

NUMERICAL / float only.  Hypothesis generator; verify.py re-checks in exact rationals.
Normalisation: separation 1; T_a corners (0,0), (a,0), (a/2, a*sqrt(3)/2).
"""
import math, random, json, sys, os

SQ3 = math.sqrt(3.0)

def clamp(x, y, a):
    for _ in range(3):
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

def min_dist(pts):
    m = float('inf'); n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            if d < m: m = d
    return m

def relax(pts, a, target, sweeps, rng, alpha=0.5):
    n = len(pts)
    for s in range(sweeps):
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
            if fx or fy:
                pts[i] = clamp(xi + alpha * fx, yi + alpha * fy, a)
        if worst < 1e-11:
            return True
    return min_dist(pts) >= target - 1e-10

def run(n, a0, a_floor, rng, margin=1.002, sweeps=500, kicks=25, start=None):
    pts = list(start) if start is not None else [sample(a0, rng) for _ in range(n)]
    if not relax(pts, a0, margin, 6000, rng):
        return None, a0
    a = a0
    step = 0.004
    while step > 2e-8 and a > a_floor:
        na = max(a * (1.0 - step), a_floor)
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

def lattice28(a):
    """The side-a triangular lattice with 7 rows: 28 points, min pairwise distance a/6."""
    s = a / 6.0
    pts = []
    for row in range(7):
        for i in range(7 - row):
            pts.append((row * s / 2.0 + i * s, row * s * SQ3 / 2.0))
    return pts

if __name__ == '__main__':
    n = int(sys.argv[1]); a_floor = float(sys.argv[2]); trials = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    margin = float(sys.argv[5]) if len(sys.argv) > 5 else 1.002
    tag = sys.argv[6] if len(sys.argv) > 6 else ''
    here = os.path.dirname(os.path.abspath(__file__))
    rng = random.Random(seed)
    besta = 1e9; bestp = None
    for t in range(trials):
        start = None
        if n <= 28 and t % 2 == 0:
            base = lattice28(6.35)
            idx = list(range(28)); rng.shuffle(idx)
            start = [base[i] for i in sorted(idx[:n])]
        p, a = run(n, 6.35, a_floor, rng, margin=margin, start=start)
        if p is not None and a < besta:
            besta, bestp = a, p
            print(f"  n={n} trial {t}: a={a:.8f} mind={min_dist(p):.9f} margin={margin}", flush=True)
            with open(os.path.join(here, 'out', f'shrink_n{n}{tag}.json'), 'w') as f:
                json.dump({"n": n, "a": besta, "pts": bestp, "min_dist": min_dist(bestp),
                           "margin": margin}, f)
    print(f"n={n}: best a = {besta:.8f}   (min pairwise distance {min_dist(bestp):.9f})", flush=True)
