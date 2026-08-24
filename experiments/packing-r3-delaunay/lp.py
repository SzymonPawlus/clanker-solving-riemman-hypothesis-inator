"""The two LPs of the Euler-localised-scoring gate.

Both are *relaxations* of the score family: every constraint imposed is a
necessary condition satisfied by every sound member of the family, so the LP
optimum is a LOWER bound on the best bound any member can prove.  Oler is a
member, so if the LP optimum equals Oler's value the family is exactly as
strong as Oler and no stronger.

Normalisation: X = (sqrt3/4)*alpha, Y = 3*beta, Z = 2*pi*gamma, t = c' - 1/2.
The bound a member proves at container side ``a`` is

    n <= 1 + X a^2 + Y a + Z - 3 t .

Oler is (X, Y, Z, t) = (1/2, 3/2, 0, 0), giving n <= 1 + a^2/2 + 3a/2.
"""

import math
import numpy as np
from scipy.optimize import linprog

SQRT3 = math.sqrt(3.0)
BIG = 1e4


# ------------------------------------------------------------------ LP 1
def reduced_lp(cfgs, a):
    """Variables v = (X, Y, Z, t).  Minimise X a^2 + Y a + Z - 3 t subject to
    the necessary condition  X*Ahat + Y*Mhat + Z - t*b >= n - 1  for every
    configuration that exists."""
    c = np.array([a * a, a, 1.0, -3.0])
    A_ub, b_ub = [], []
    for k in cfgs:
        # -(X*Ahat + Y*Mhat + Z - t*b) <= -(n-1)
        A_ub.append([-float(k.Ahat_up), -float(k.Mhat_up), -1.0, float(k.b)])
        b_ub.append(-(k.n - 1))
    bounds = [(0, BIG), (0, BIG), (-BIG, BIG), (0, BIG)]
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=bounds, method="highs")
    return res


# ------------------------------------------------------------------ LP 2
def score_lp(cfgs, a):
    """Variables: one sigma per distinct face shape, one tau per distinct
    boundary-edge length, plus (alpha, beta, gamma, cprime).

    Constraints
      (i)   sigma_s - alpha * area_up(s) <= 0            [pointwise domination]
      (ii)  tau_j  - beta  * len_up(j)  <= 0             [pointwise domination]
      (iii) sum sigma + sum tau + 2 pi gamma - F/2 - cprime * b >= 0
            for every configuration that exists          [necessary for (S2)]
    Objective
      min alpha*(sqrt3/4)a^2 + beta*3a + 2 pi gamma - 3 (cprime - 1/2).
    """
    shapes, edges = {}, {}
    for k in cfgs:
        for key, area_up in k.face_shapes:
            if key not in shapes:
                shapes[key] = float(area_up)
            else:
                shapes[key] = max(shapes[key], float(area_up))
        for i in range(k.b):
            e2 = tuple(k.cycle[i]), tuple(k.cycle[(i + 1) % k.b])
            key = _edge_key(k, i)
            L = float(k.edge_len_up[i])
            edges[key] = max(edges.get(key, L), L)

    slist = list(shapes)
    elist = list(edges)
    ns, ne = len(slist), len(elist)
    sidx = {s: i for i, s in enumerate(slist)}
    eidx = {e: ns + i for i, e in enumerate(elist)}
    IA, IB, IG, IC = ns + ne, ns + ne + 1, ns + ne + 2, ns + ne + 3
    nv = ns + ne + 4

    c = np.zeros(nv)
    c[IA] = (SQRT3 / 4.0) * a * a
    c[IB] = 3.0 * a
    c[IG] = 2.0 * math.pi
    c[IC] = -3.0
    const = 1.5                      # from -3*(cprime - 1/2)

    A_ub, b_ub = [], []
    for s in slist:                                        # (i)
        row = np.zeros(nv); row[sidx[s]] = 1.0; row[IA] = -shapes[s]
        A_ub.append(row); b_ub.append(0.0)
    for e in elist:                                        # (ii)
        row = np.zeros(nv); row[eidx[e]] = 1.0; row[IB] = -edges[e]
        A_ub.append(row); b_ub.append(0.0)
    for k in cfgs:                                         # (iii)
        row = np.zeros(nv)
        for key, _ in k.face_shapes:
            row[sidx[key]] -= 1.0
        for i in range(k.b):
            row[eidx[_edge_key(k, i)]] -= 1.0
        row[IG] = -2.0 * math.pi
        row[IC] = float(k.b)
        A_ub.append(row); b_ub.append(-0.5 * k.F)

    bounds = [(-BIG, BIG)] * (ns + ne) + [(0, BIG), (0, BIG), (-BIG, BIG), (0.5, BIG)]
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=bounds, method="highs")
    return res, const, (ns, ne)


def _edge_key(k, i):
    from geom import d2
    return d2(k.cycle[i], k.cycle[(i + 1) % k.b])


# ------------------------------------------------------------------ driver
def best_side(cfgs, n_target, solver="reduced", lo=0.5, hi=40.0, iters=80):
    """Largest a for which the family can still certify 'at most n_target - 1
    points fit'.  Returns that a (Oler normalisation) and d = 2a."""
    def bound(a):
        if solver == "reduced":
            r = reduced_lp(cfgs, a)
            assert r.status == 0, r.message
            return 1.0 + r.fun
        r, const, _ = score_lp(cfgs, a)
        assert r.status == 0, r.message
        return 1.0 + r.fun + const

    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if bound(mid) < n_target:
            lo = mid
        else:
            hi = mid
    return lo, 2.0 * lo


def oler_side(n):
    """Oler's own answer: largest a with 1 + a^2/2 + 3a/2 < n."""
    a = (-3.0 + math.sqrt(8.0 * n + 1.0)) / 2.0
    return a, 2.0 * a
