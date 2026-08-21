"""Search for large 1-separated point sets in an equilateral triangle T_a, a < 6.

NUMERICAL / float only.  Output is a *hypothesis*; nothing here decides anything.
The exact rational verification lives in verify.py.

Normalisation asserted here and nowhere reinterpreted:
  separation 1; T_a has corners (0,0), (a,0), (a/2, a*sqrt(3)/2).
"""
import math, random, sys, json, os

SQ3 = math.sqrt(3.0)

def clamp_to_triangle(x, y, a):
    """Project (x,y) into the closed equilateral triangle T_a (corners (0,0),(a,0),(a/2,a*sq3/2))."""
    # three half-planes: y >= 0 ; sq3*x - y >= 0 ; sq3*(a-x) - y >= 0
    for _ in range(8):
        moved = False
        if y < 0.0:
            y = 0.0; moved = True
        # edge from (0,0) to (a/2, a sq3/2): inward normal (sq3,-1)/2, constraint sq3*x - y >= 0
        g = SQ3 * x - y
        if g < 0.0:
            # normal direction (sq3,-1)/2 has norm 1
            t = -g / 2.0
            x += t * SQ3 / 2.0 * 1.0
            y += t * (-1.0) / 2.0 * 1.0
            # recompute: gradient of g is (sq3,-1), |grad|=2, step = -g/4 * grad
            moved = True
        g = SQ3 * (a - x) - y
        if g < 0.0:
            x -= (-g) / 4.0 * SQ3
            y -= (-g) / 4.0 * 1.0
            moved = True
        if not moved:
            break
    return x, y

def inside(x, y, a, tol=1e-12):
    return y >= -tol and SQ3 * x - y >= -tol and SQ3 * (a - x) - y >= -tol

def min_dist(pts):
    m = float('inf')
    n = len(pts)
    for i in range(n):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            dx = xi - pts[j][0]; dy = yi - pts[j][1]
            d = math.hypot(dx, dy)
            if d < m: m = d
    return m

def relax(pts, a, target, iters=4000, rng=None):
    n = len(pts)
    for it in range(iters):
        step = 0.5
        worst = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                dx = pts[j][0] - pts[i][0]; dy = pts[j][1] - pts[i][1]
                d = math.hypot(dx, dy)
                if d < 1e-12:
                    ang = random.random() * 6.283
                    dx, dy, d = math.cos(ang) * 1e-6, math.sin(ang) * 1e-6, 1e-6
                if d < target:
                    push = (target - d) * step / d
                    worst = max(worst, target - d)
                    pts[i] = (pts[i][0] - dx * push * 0.5, pts[i][1] - dy * push * 0.5)
                    pts[j] = (pts[j][0] + dx * push * 0.5, pts[j][1] + dy * push * 0.5)
        for i in range(n):
            pts[i] = clamp_to_triangle(pts[i][0], pts[i][1], a)
        if worst < 1e-14:
            break
    return pts

def random_start(n, a, rng):
    pts = []
    while len(pts) < n:
        u, v = rng.random(), rng.random()
        if u + v > 1.0:
            u, v = 1.0 - u, 1.0 - v
        # barycentric in triangle
        x = a * (u + v * 0.5)
        y = a * v * SQ3 / 2.0
        pts.append((x, y))
    return pts

def grow(pts, a, iters_per=300, rounds=400, tol=1e-11):
    """Inflation loop: repeatedly try to push the separation target up."""
    target = min_dist(pts)
    if target <= 0: target = 1e-3
    for r in range(rounds):
        trial = list(pts)
        newt = target * 1.02 + 1e-6
        trial = relax(trial, a, newt, iters=iters_per)
        m = min_dist(trial)
        if m >= newt - tol:
            pts = trial; target = m
        else:
            if m > target:
                pts = trial; target = m
            # try a smaller step
            newt = target * 1.002 + 1e-9
            trial = relax(list(pts), a, newt, iters=iters_per)
            m2 = min_dist(trial)
            if m2 >= newt - tol:
                pts = trial; target = m2
            else:
                break
    return min_dist(pts), pts

def lattice_start(n, a, rng):
    """Rows of a triangular lattice, jittered."""
    pts = []
    k = 1
    while k * (k + 1) // 2 < n: k += 1
    step = a / max(k - 1, 1)
    for row in range(k):
        cnt = k - row
        for i in range(cnt):
            x = row * step / 2.0 + i * step
            y = row * step * SQ3 / 2.0
            x += (rng.random() - 0.5) * step * 0.25
            y += (rng.random() - 0.5) * step * 0.25
            pts.append(clamp_to_triangle(x, y, a))
    rng.shuffle(pts)
    return pts[:n]

def search(n, a, restarts=200, seed=0, iters=3000):
    rng = random.Random(seed)
    best = None; bestmin = -1.0
    for r in range(restarts):
        if r % 3 == 0:
            pts = lattice_start(n, a, rng)
        else:
            pts = random_start(n, a, rng)
        m, pts = grow(pts, a)
        if m > bestmin:
            bestmin = m; best = list(pts)
    return bestmin, best

if __name__ == '__main__':
    a = float(sys.argv[1]) if len(sys.argv) > 1 else 5.99
    ns = [int(t) for t in sys.argv[2].split(',')] if len(sys.argv) > 2 else [26]
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 12345
    out = {}
    for n in ns:
        m, pts = search(n, a, restarts=restarts, seed=seed + n)
        print(f"a={a}  n={n}  best min pairwise distance = {m:.9f}   (need >= 1)", flush=True)
        out[n] = {"a": a, "min_dist": m, "pts": pts}
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'), exist_ok=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'configs_a{a}.json'), 'w') as f:
        json.dump(out, f)
