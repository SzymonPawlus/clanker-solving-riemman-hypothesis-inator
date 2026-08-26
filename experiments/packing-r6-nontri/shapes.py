"""Shape library + maximin (spreading) optimiser.

For a compact shape S (the "unit representative"), define

    delta_S(m) = max over m-point subsets of S of the minimum pairwise distance,
    a_S(m)     = 1 / delta_S(m)
               = least lambda such that lambda*S holds m points at pairwise separation >= 1.

Capacity of lambda*S at threshold t (STRICT separation > t) is
    cap_>(lambda*S) = max { m : a_S(m) < lambda/t }.
So capacity m is SKIPPED by the family {lambda*S} iff a_S(m) == a_S(m+1).

Numerics here are search only (RULES.md, problems/.../RULES.md Sec.5); every claim in the
write-up that is called exact is proved separately.
"""
import numpy as np
from scipy.optimize import linprog, minimize

SQ3 = np.sqrt(3.0)


class Shape:
    def __init__(self, name, kind, **kw):
        self.name = name
        self.kind = kind          # 'poly' | 'disc' | 'halfdisc' | 'sector'
        self.__dict__.update(kw)

    # --- membership / projection -------------------------------------------------
    def constraints(self, p):
        """list of g(p) >= 0 values"""
        x, y = p
        if self.kind == 'poly':
            A, b = self.A, self.b
            return list(b - A @ np.array([x, y]))
        if self.kind == 'disc':
            return [1.0 - (x * x + y * y)]
        if self.kind == 'halfdisc':
            return [1.0 - (x * x + y * y), y]
        if self.kind == 'sector':
            # wedge of half-angle self.half (radians) about +x axis, radius 1
            h = self.half
            return [1.0 - (x * x + y * y),
                    x * np.sin(h) - y * np.cos(h),
                    x * np.sin(h) + y * np.cos(h)]
        raise ValueError(self.kind)

    def contains(self, p, tol=1e-9):
        return all(g >= -tol for g in self.constraints(p))

    def sample(self, rng, n):
        lo, hi = self.bbox
        out = []
        while len(out) < n:
            p = rng.uniform(lo, hi)
            if self.contains(p):
                out.append(p)
        return np.array(out)


def polygon(name, verts):
    V = np.array(verts, float)
    k = len(V)
    A = np.zeros((k, 2)); b = np.zeros(k)
    c = V.mean(axis=0)
    for i in range(k):
        p, q = V[i], V[(i + 1) % k]
        nvec = np.array([q[1] - p[1], -(q[0] - p[0])])
        if nvec @ (c - p) > 0:
            nvec = -nvec
        A[i] = nvec
        b[i] = nvec @ p
    s = Shape(name, 'poly', A=A, b=b, verts=V)
    s.bbox = (V.min(axis=0), V.max(axis=0))
    return s


def make_shapes():
    S = {}
    S['triangle'] = polygon('triangle', [(0, 0), (1, 0), (0.5, SQ3 / 2)])
    S['square'] = polygon('square', [(0, 0), (1, 0), (1, 1), (0, 1)])
    S['rhombus60'] = polygon('rhombus60', [(0, 0), (1, 0), (1.5, SQ3 / 2), (0.5, SQ3 / 2)])
    # regular hexagon, side 1 (circumradius 1)
    S['hexagon'] = polygon('hexagon', [(np.cos(k * np.pi / 3), np.sin(k * np.pi / 3)) for k in range(6)])
    # right isoceles / half of the equilateral triangle (a "30-60-90" cell)
    S['halftri'] = polygon('halftri', [(0, 0), (1, 0), (0.5, SQ3 / 2)][:0] + [(0, 0), (0.5, 0), (0.5, SQ3 / 2)])
    # 3:1 and 6:1 slabs
    S['slab3'] = polygon('slab3', [(0, 0), (1, 0), (1, 1 / 3), (0, 1 / 3)])
    S['slab6'] = polygon('slab6', [(0, 0), (1, 0), (1, 1 / 6), (0, 1 / 6)])
    d = Shape('disc', 'disc'); d.bbox = (np.array([-1, -1.]), np.array([1, 1.])); S['disc'] = d
    hd = Shape('halfdisc', 'halfdisc'); hd.bbox = (np.array([-1, 0.]), np.array([1, 1.])); S['halfdisc'] = hd
    for deg, key in ((60, 'sector60'), (90, 'sector90'), (120, 'sector120')):
        sc = Shape(key, 'sector', half=np.radians(deg) / 2)
        sc.bbox = (np.array([-1, -1.]), np.array([1, 1.]))
        S[key] = sc
    return S


# ---------------------------------------------------------------------------------
def _lin_containment(shape):
    """Return (A,b) with A p <= b for polygon shapes, else None."""
    if shape.kind == 'poly':
        return shape.A, shape.b
    return None


def maximin(shape, m, restarts=60, seed=0, iters=2):
    """max over m points in `shape` of the min pairwise distance. SEARCH ONLY."""
    rng = np.random.default_rng(seed)
    n = m
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    pi = np.array([p[0] for p in pairs]); pj = np.array([p[1] for p in pairs])
    ncon = len(shape.constraints(np.zeros(2)))
    best, bestP = -1.0, None

    def cons_f(z):
        P = z[:-1].reshape(n, 2); t = z[-1]
        d = P[pi] - P[pj]
        sep = np.einsum('ij,ij->i', d, d) - t * t
        cont = np.concatenate([shape.constraints(P[i]) for i in range(n)])
        return np.concatenate([sep, cont])

    def cons_j(z):
        P = z[:-1].reshape(n, 2); t = z[-1]
        J = np.zeros((len(pairs) + n * ncon, 2 * n + 1))
        d = P[pi] - P[pj]
        for k, (i, j) in enumerate(pairs):
            J[k, 2 * i:2 * i + 2] = 2 * d[k]
            J[k, 2 * j:2 * j + 2] = -2 * d[k]
            J[k, -1] = -2 * t
        eps = 1e-7
        for i in range(n):
            for c in range(ncon):
                row = len(pairs) + i * ncon + c
                base = shape.constraints(P[i])[c]
                for ax in range(2):
                    q = P[i].copy(); q[ax] += eps
                    J[row, 2 * i + ax] = (shape.constraints(q)[c] - base) / eps
        return J

    for r in range(restarts):
        P0 = shape.sample(rng, n)
        z = np.concatenate([P0.ravel(), [max(minpair(P0), 1e-3)]])
        for _ in range(iters):
            res = minimize(lambda z: -z[-1], z,
                           jac=lambda z: np.concatenate([np.zeros(2 * n), [-1.0]]),
                           constraints=[{'type': 'ineq', 'fun': cons_f, 'jac': cons_j}],
                           method='SLSQP', options={'maxiter': 250, 'ftol': 1e-12})
            z = res.x
        P = np.array([project(shape, p) for p in z[:-1].reshape(n, 2)])
        val = minpair(P)
        if val > best:
            best, bestP = val, P
    return best, bestP


def minpair(P):
    n = len(P)
    if n < 2:
        return np.inf
    d = np.inf
    for i in range(n):
        for j in range(i + 1, n):
            d = min(d, np.linalg.norm(P[i] - P[j]))
    return d


def project(shape, p, tol=1e-12):
    """project p onto shape (only needed for tiny violations)"""
    if shape.contains(p, tol=0.0):
        return p
    if shape.kind == 'poly':
        # small LP-free fix: iterate over violated halfplanes
        q = p.copy()
        for _ in range(50):
            g = shape.b - shape.A @ q
            k = int(np.argmin(g))
            if g[k] >= 0:
                break
            nvec = shape.A[k]
            q = q + nvec * g[k] / (nvec @ nvec)
        return q
    if shape.kind in ('disc', 'halfdisc', 'sector'):
        q = p.copy()
        for _ in range(50):
            gs = shape.constraints(q)
            k = int(np.argmin(gs))
            if gs[k] >= 0:
                break
            if k == 0:
                q = q / np.linalg.norm(q)
            elif shape.kind == 'halfdisc':
                q = np.array([q[0], 0.0])
            else:
                h = shape.half
                nvec = np.array([np.sin(h), -np.cos(h)]) if k == 1 else np.array([np.sin(h), np.cos(h)])
                q = q + nvec * (-gs[k]) / (nvec @ nvec)
        return q
    return p
