"""Numerical search (FLOATS, search only) for the minimum over m-piece convex
partitions of T(a) of the maximum piece diameter.

Family searched: power diagrams (weighted Voronoi) with m sites, clipped to T(a).
Power cells are convex and tile the plane, so any parameter vector gives a genuine
convex partition of T(a).  This gives an UPPER bound on the true min-max diameter.

Known targets (these calibrate the optimiser):
   (a=2, m=4) -> exactly 1        (medial subdivision; >=1 because 6 points at
                                   pairwise distance >= 1 fit in T(2))
   (a=3, m=9) -> <= 1             (nine unit triangles)
   (a=3, m=8) -> >= 1             (9 points at pairwise distance >=1 fit in T(3))
                                  ... is it EQUAL to 1?   <-- the k=4 question
"""
import numpy as np
from scipy.optimize import minimize
import sys, json, os

S3 = np.sqrt(3.0)


def tri(a):
    return np.array([[0.0, 0.0], [a, 0.0], [a / 2, a * S3 / 2]])


def clip(poly, n, c):
    """keep {x : n.x <= c}"""
    if len(poly) == 0:
        return poly
    out = []
    L = len(poly)
    d = poly @ n - c
    for i in range(L):
        j = (i + 1) % L
        if d[i] <= 0:
            out.append(poly[i])
        if d[i] * d[j] < 0:
            t = d[i] / (d[i] - d[j])
            out.append(poly[i] + t * (poly[j] - poly[i]))
    return np.array(out) if out else np.zeros((0, 2))


def cells(a, P, W):
    T = tri(a)
    m = len(P)
    res = []
    for i in range(m):
        poly = T.copy()
        for j in range(m):
            if j == i:
                continue
            n = 2 * (P[j] - P[i])
            c = P[j] @ P[j] - P[i] @ P[i] - W[j] + W[i]
            poly = clip(poly, n, c)
            if len(poly) == 0:
                break
        res.append(poly)
    return res


def diam(poly):
    if len(poly) < 2:
        return 0.0
    d = poly[:, None, :] - poly[None, :, :]
    return float(np.sqrt((d ** 2).sum(-1)).max())


def maxdiam(x, a, m, beta=0.0):
    P = x[:2 * m].reshape(m, 2)
    W = np.concatenate([[0.0], x[2 * m:]])
    ds = np.array([diam(c) for c in cells(a, P, W)])
    if beta > 0:
        return np.log(np.exp(beta * ds).sum()) / beta
    return ds.max()


def solve(a, m, tries=200, seed=0):
    rng = np.random.default_rng(seed)
    T = tri(a)
    best, bx = 1e9, None
    for t in range(tries):
        # random points uniform in T
        u = rng.random((m, 2))
        f = u.sum(1) > 1
        u[f] = 1 - u[f]
        P = T[0] + u[:, :1] * (T[1] - T[0]) + u[:, 1:] * (T[2] - T[0])
        x = np.concatenate([P.ravel(), rng.normal(0, 0.02, m - 1)])
        for beta in (60.0, 0.0):
            r = minimize(maxdiam, x, args=(a, m, beta), method="Nelder-Mead",
                         options=dict(maxiter=2500, maxfev=2500, fatol=1e-12,
                                      xatol=1e-12))
            x = r.x
        val = maxdiam(x, a, m, 0.0)
        if val < best:
            best, bx = val, x.copy()
    return best, bx


if __name__ == "__main__":
    a = float(sys.argv[1]); m = int(sys.argv[2])
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    best, bx = solve(a, m, tries, seed)
    print(f"a={a} m={m} tries={tries} seed={seed}  best max-diameter = {best:.9f}")
    P = bx[:2 * m].reshape(m, 2); W = np.concatenate([[0.0], bx[2 * m:]])
    print("sites:"); print(np.round(P, 6))
    print("weights:", np.round(W, 6))
    for i, c in enumerate(cells(a, P, W)):
        print(f"  cell {i}: diam={diam(c):.6f} verts={len(c)}")
        print("   ", np.round(c, 5).tolist())
    d = os.path.dirname(os.path.abspath(__file__))
    json.dump({"a": a, "m": m, "best": best, "x": bx.tolist()},
              open(os.path.join(d, f"minmax_a{a}_m{m}_s{seed}.json"), "w"), indent=2)
