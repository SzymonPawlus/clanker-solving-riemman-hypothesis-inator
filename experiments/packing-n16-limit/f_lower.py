"""NUMERICAL lower bound on f(l): the best explicit polygon the search found.

f(l) = sup{ area(S) : diam S <= 1, S subset {y>=0}, S contains (0,0) and (l,0) }.

Star-shaped parametrisation about a scanned centre c: vertices are A=(0,0),
B=(l,0) and K free vertices on fixed rays from c at strictly increasing angles,
so the polygon is simple and its shoelace IS its area, its diameter IS the max
vertex distance, and containment in the half-plane is vertex-wise.  Every
returned value is therefore a genuine (float-level) lower bound on f(l).

Status: `numerical`.  Used only to measure the slack in the certified upper
bound of fbound.py; no bound in this attack depends on it.
"""
import numpy as np
from scipy.optimize import minimize


def best_polygon(ell, K=20, seed=20260822):
    best, bestv = 0.0, None
    A = np.array([0.0, 0.0]); B = np.array([ell, 0.0])
    for t in np.linspace(0.10, 0.55, 10):
        c = np.array([ell / 2, t])
        aA = np.arctan2(A[1] - c[1], A[0] - c[0]) % (2 * np.pi)
        aB = np.arctan2(B[1] - c[1], B[0] - c[0]) % (2 * np.pi)
        lo, hi = min(aA, aB), max(aA, aB)
        # free rays strictly between aB..aA going the long way (through the top)
        ang = np.linspace(hi, lo + 2 * np.pi, K + 2)[1:-1]
        fixed = np.stack([np.cos(ang), np.sin(ang)], 1)

        def verts(r):
            free = c + r[:, None] * fixed
            order = [B if aB < aA else A] + list(free) + [A if aB < aA else B]
            return np.array(order)

        def negarea(r):
            v = verts(r)
            return -0.5 * np.sum(v[:, 0] * np.roll(v[:, 1], -1) - np.roll(v[:, 0], -1) * v[:, 1])

        def cons(r):
            v = verts(r)
            d = [1.0 - np.sum((v[i] - v[j]) ** 2)
                 for i in range(len(v)) for j in range(i + 1, len(v))]
            return np.array(d + list(v[:, 1]) + list(r - 1e-4))

        r0 = np.full(K, 0.45)
        res = minimize(negarea, r0, method='SLSQP',
                       constraints=[{'type': 'ineq', 'fun': cons}],
                       options={'maxiter': 400, 'ftol': 1e-12})
        v = verts(res.x)
        dmax = max(np.linalg.norm(v[i] - v[j])
                   for i in range(len(v)) for j in range(i + 1, len(v)))
        if v[:, 1].min() < -1e-9 or dmax > 1 + 1e-9:
            continue
        a = -negarea(res.x) / max(1.0, dmax) ** 2   # scale-safe
        if a > best:
            best, bestv = a, v
    return best, bestv


if __name__ == "__main__":
    print("numerical lower bounds on f(l)  (star polygons, K=20):")
    for num in range(0, 13):
        ell = num / 12
        a, _ = best_polygon(ell)
        print(f"  f({ell:.4f}) >= {a:.6f}")
