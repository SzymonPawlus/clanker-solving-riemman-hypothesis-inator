"""Faster local optimiser: incremental power-diagram cell updates.

FLOATS ONLY (search stage).  Nothing here decides anything.
"""
import math, random, json, sys
from search import triangle, clip, diam2, power_cells, diams

SQ3 = math.sqrt(3.0)

class Diagram:
    def __init__(self, a, sites, weights, knn=14):
        self.a = a
        self.tri = triangle(a)
        self.s = [list(p) for p in sites]
        self.w = list(weights)
        self.n = len(sites)
        self.knn = min(knn, self.n - 1)
        self.d = [0.0] * self.n
        self.rebuild()

    def neigh(self, i):
        xi, yi = self.s[i]
        ds = sorted(range(self.n), key=lambda j: (self.s[j][0]-xi)**2 + (self.s[j][1]-yi)**2)
        return [j for j in ds if j != i][:self.knn]

    def cell(self, i):
        xi, yi = self.s[i]
        wi = self.w[i]
        poly = self.tri
        for j in self.nb[i]:
            xj, yj = self.s[j]
            nx = 2.0 * (xj - xi); ny = 2.0 * (yj - yi)
            c = (xj*xj + yj*yj - self.w[j]) - (xi*xi + yi*yi - wi)
            poly = clip(poly, nx, ny, c)
            if not poly:
                return []
        return poly

    def rebuild(self):
        self.nb = [self.neigh(i) for i in range(self.n)]
        for i in range(self.n):
            self.d[i] = math.sqrt(diam2(self.cell(i)))

    def affected(self, k):
        # cells that can change when site k moves: k and everyone having k as neighbour
        return [k] + [i for i in range(self.n) if i != k and k in self.nb[i]]

    def update(self, k):
        for i in self.affected(k):
            self.d[i] = math.sqrt(diam2(self.cell(i)))

    def obj(self, p):
        mx = max(self.d)
        if mx <= 0:
            return 0.0
        return mx * (sum((x / mx) ** p for x in self.d)) ** (1.0 / p)

    def truemax(self):
        # honest recomputation with all sites (no knn pruning)
        return max(diams(self.s, self.w, self.tri))

def descend(dg, ps=(12.,25.,50.,100.,200.,400.,900.), step0=0.05, tol=1e-11):
    n = dg.n
    scale = dg.a / math.sqrt(n)
    for p in ps:
        cur = dg.obj(p)
        step = step0 * scale
        while step > tol * scale:
            improved = False
            for k in range(n):
                for d in range(3):
                    for sgn in (1.0, -1.0):
                        old = (dg.s[k][0], dg.s[k][1], dg.w[k])
                        if d == 0: dg.s[k][0] += sgn * step
                        elif d == 1: dg.s[k][1] += sgn * step
                        else: dg.w[k] += sgn * step * scale
                        dg.update(k)
                        v = dg.obj(p)
                        if v < cur * (1.0 - 1e-14):
                            cur = v; improved = True
                        else:
                            dg.s[k][0], dg.s[k][1], dg.w[k] = old
                            dg.update(k)
            if not improved:
                step *= 0.5
        dg.rebuild()
    return dg.truemax()

def lattice_init(a, n, rng, jitter=0.0):
    cx, cy = a / 2.0, a * SQ3 / 6.0
    area = SQ3 / 4.0 * a * a
    s = math.sqrt(2.0 * area / (SQ3 * n)) * rng.uniform(0.9, 1.1)
    th = rng.uniform(0, math.pi / 3)
    ox, oy = rng.uniform(-s/2, s/2), rng.uniform(-s/2, s/2)
    e1 = (s*math.cos(th), s*math.sin(th))
    e2 = (s*math.cos(th+math.pi/3), s*math.sin(th+math.pi/3))
    pts = []
    R = int(a/s) + 3
    for i in range(-R, R+1):
        for j in range(-R, R+1):
            x = cx+ox+i*e1[0]+j*e2[0]; y = cy+oy+i*e1[1]+j*e2[1]
            pts.append((x + rng.gauss(0,jitter), y + rng.gauss(0,jitter)))
    pts.sort(key=lambda q: (q[0]-cx)**2 + (q[1]-cy)**2)
    return [list(q) for q in pts[:n]], [0.0]*n

def basin(a, n, seed, tries=6, verbose=True):
    rng = random.Random(seed)
    best = 1e18; bestcfg = None
    for t in range(tries):
        if bestcfg is None or rng.random() < 0.5:
            s0, w0 = lattice_init(a, n, rng, jitter=0.03*a/math.sqrt(n))
        else:
            s0 = [[x + rng.gauss(0, 0.10*a/math.sqrt(n)), y + rng.gauss(0, 0.10*a/math.sqrt(n))]
                  for x, y in bestcfg[0]]
            w0 = [w + rng.gauss(0, 0.05*a/math.sqrt(n)) for w in bestcfg[1]]
        dg = Diagram(a, s0, w0)
        v = descend(dg)
        if v < best:
            best = v; bestcfg = ([list(p) for p in dg.s], list(dg.w))
            if verbose: print("   try %d: %.9f" % (t, v), flush=True)
        elif verbose:
            print("   try %d: %.9f (best %.9f)" % (t, v, best), flush=True)
    return best, bestcfg

if __name__ == "__main__":
    a = float(sys.argv[1]); n = int(sys.argv[2])
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    b, cfg = basin(a, n, seed, tries)
    print("a=%g n=%d BEST %.12f" % (a, n, b))
    json.dump({"a": a, "n": n, "max_diam": b, "sites": cfg[0], "weights": cfg[1]},
              open("/home/user/clanker-solving-riemman-hypothesis-inator/experiments/packing-eo-covering/opt_a%g_n%d.json" % (a, n), "w"))
