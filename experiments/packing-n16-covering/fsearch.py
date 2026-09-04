"""Search for partitions of the equilateral triangle T_a into N convex pieces of
diameter <= 1, via power diagrams (weighted Voronoi) clipped to T_a.

FLOATS ONLY -- this is the search stage.  Nothing here decides anything; every
reported scheme must be re-verified by exact.py.

Normalisation asserted below: separation 1, T_a = closed equilateral triangle of
side a with corners (0,0), (a,0), (a/2, a*sqrt3/2).  Target: a = 6, N = 26.
"""
import math, random, sys, json

SQ3 = math.sqrt(3.0)

def triangle(a):
    return [(0.0, 0.0), (a, 0.0), (a / 2.0, a * SQ3 / 2.0)]

def clip(poly, nx, ny, c):
    """keep the part of convex polygon poly with nx*x+ny*y <= c"""
    if not poly:
        return []
    out = []
    m = len(poly)
    for i in range(m):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % m]
        d1 = nx * x1 + ny * y1 - c
        d2 = nx * x2 + ny * y2 - c
        if d1 <= 0.0:
            out.append((x1, y1))
        if (d1 > 0.0) != (d2 > 0.0):
            t = d1 / (d1 - d2)
            out.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
    return out

def power_cells(sites, weights, tri):
    n = len(sites)
    res = []
    for i in range(n):
        xi, yi = sites[i]
        wi = weights[i]
        poly = tri
        for j in range(n):
            if j == i:
                continue
            xj, yj = sites[j]
            wj = weights[j]
            nx = 2.0 * (xj - xi)
            ny = 2.0 * (yj - yi)
            c = (xj * xj + yj * yj - wj) - (xi * xi + yi * yi - wi)
            poly = clip(poly, nx, ny, c)
            if not poly:
                break
        res.append(poly)
    return res

def diam2(poly):
    d = 0.0
    m = len(poly)
    for i in range(m):
        xi, yi = poly[i]
        for j in range(i + 1, m):
            dx = xi - poly[j][0]
            dy = yi - poly[j][1]
            v = dx * dx + dy * dy
            if v > d:
                d = v
    return d

def diams(sites, weights, tri):
    return [math.sqrt(diam2(p)) for p in power_cells(sites, weights, tri)]

def objective(sites, weights, tri, p):
    ds = diams(sites, weights, tri)
    mx = max(ds)
    if mx <= 0.0:
        return 0.0
    s = sum((d / mx) ** p for d in ds)
    return mx * s ** (1.0 / p)

def init_lattice(a, n, rng):
    """triangular lattice, random spacing/rotation/offset, keep n sites nearest the triangle"""
    tri = triangle(a)
    cx = a / 2.0
    cy = a * SQ3 / 6.0
    area = SQ3 / 4.0 * a * a
    s = math.sqrt(2.0 * area / (SQ3 * n)) * rng.uniform(0.85, 1.15)
    th = rng.uniform(0, math.pi)
    ox = rng.uniform(-s, s)
    oy = rng.uniform(-s, s)
    e1 = (s * math.cos(th), s * math.sin(th))
    e2 = (s * math.cos(th + math.pi / 3), s * math.sin(th + math.pi / 3))
    pts = []
    R = int(a / s) + 3
    for i in range(-R, R + 1):
        for j in range(-R, R + 1):
            x = cx + ox + i * e1[0] + j * e2[0]
            y = cy + oy + i * e1[1] + j * e2[1]
            pts.append((x, y))
    def dist_tri(p):
        # crude: distance from centroid
        return (p[0] - cx) ** 2 + (p[1] - cy) ** 2
    pts.sort(key=dist_tri)
    return [list(q) for q in pts[:n]], [0.0] * n

def init_random(a, n, rng):
    tri = triangle(a)
    pts = []
    while len(pts) < n:
        x = rng.uniform(0, a)
        y = rng.uniform(0, a * SQ3 / 2)
        if y <= x * SQ3 + 1e-9 and y <= (a - x) * SQ3 + 1e-9:
            pts.append([x, y])
    return pts, [0.0] * n

def anneal(a, n, rng, iters=20000, verbose=False, init=None):
    tri = triangle(a)
    if init is None:
        sites, weights = (init_lattice if rng.random() < 0.7 else init_random)(a, n, rng)
    else:
        sites = [list(s) for s in init[0]]
        weights = list(init[1])
    best = None
    bestval = 1e18
    scale = a / math.sqrt(n)
    for it in range(iters):
        frac = it / iters
        p = 6.0 + 60.0 * frac
        T = 0.02 * scale * (1.0 - frac) ** 2
        step = scale * (0.35 * (1.0 - frac) + 0.01)
        cur = objective(sites, weights, tri, p)
        k = rng.randrange(n)
        which = rng.random()
        old = (sites[k][0], sites[k][1], weights[k])
        if which < 0.45:
            sites[k][0] += rng.gauss(0, step)
        elif which < 0.9:
            sites[k][1] += rng.gauss(0, step)
        else:
            weights[k] += rng.gauss(0, step * scale)
        new = objective(sites, weights, tri, p)
        if new <= cur or rng.random() < math.exp(-(new - cur) / max(T, 1e-12)):
            pass
        else:
            sites[k][0], sites[k][1], weights[k] = old
        mx = max(diams(sites, weights, tri))
        if mx < bestval:
            bestval = mx
            best = ([tuple(s) for s in sites], list(weights))
    return bestval, best

def polish(a, n, sites, weights, rng, rounds=4000):
    """coordinate descent on a p-norm of the cell diameters, p annealed upward."""
    tri = triangle(a)
    sites = [list(s) for s in sites]
    weights = list(weights)
    scale = a / math.sqrt(n)
    for p in (12.0, 25.0, 50.0, 100.0, 200.0, 400.0, 800.0):
        cur = objective(sites, weights, tri, p)
        step = 0.05 * scale
        while step > 1e-10 * scale:
            improved = False
            for k in range(n):
                for d in range(3):
                    for sgn in (1.0, -1.0):
                        old = (sites[k][0], sites[k][1], weights[k])
                        if d == 0:
                            sites[k][0] += sgn * step
                        elif d == 1:
                            sites[k][1] += sgn * step
                        else:
                            weights[k] += sgn * step * scale
                        v = objective(sites, weights, tri, p)
                        if v < cur * (1.0 - 1e-13):
                            cur = v
                            improved = True
                        else:
                            sites[k][0], sites[k][1], weights[k] = old
            if not improved:
                step *= 0.5
    return max(diams(sites, weights, tri)), (sites, weights)

def run(a, n, restarts, seed, iters=20000, quiet=False):
    rng = random.Random(seed)
    best = 1e18
    bestcfg = None
    for r in range(restarts):
        v, cfg = anneal(a, n, rng, iters=iters)
        v2, cfg2 = polish(a, n, cfg[0], cfg[1], rng)
        if v2 < best:
            best = v2
            bestcfg = cfg2
            if not quiet:
                print("  restart %d: max diam = %.9f" % (r, best), flush=True)
    return best, bestcfg

if __name__ == "__main__":
    a = float(sys.argv[1]); n = int(sys.argv[2])
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 12345
    iters = int(sys.argv[5]) if len(sys.argv) > 5 else 20000
    best, cfg = run(a, n, restarts, seed, iters)
    print("a=%g n=%d  BEST max diameter = %.12f  (need <= 1)" % (a, n, best))
    out = {"a": a, "n": n, "max_diam": best,
           "sites": [[c for c in s] for s in cfg[0]], "weights": cfg[1]}
    fn = "/home/user/clanker-solving-riemman-hypothesis-inator/experiments/packing-eo-covering/best_a%g_n%d.json" % (a, n)
    json.dump(out, open(fn, "w"))
    print("wrote", fn)
