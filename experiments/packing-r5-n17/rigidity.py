"""Exact infinitesimal rigidity over Q(sqrt 3), plus exact 1-D slide intervals
for zero-contact points that sit on a wall.

The triangle is FIXED (RULES.md sec 2: no rigid motions), so a packing is
infinitesimally rigid iff the only infinitesimal motion is zero, i.e. the
rigidity matrix (contact rows + active-wall rows) has rank 2n.

Rows:
  contact (i,j):  (p_i - p_j) . v_i + (p_j - p_i) . v_j >= 0   -> equality row
  active wall w at i:  grad w . v_i >= 0                       -> equality row
We compute the rank of the equality system; its kernel dimension is the number
of independent first-order flexes (an upper bound on the true DOF count, and a
lower bound of 0 -- a nonzero kernel does not prove a finite flex exists).
"""
from fractions import Fraction as F
from q3 import Q3, ZERO
import checker as ck

R3 = Q3(0, 1)
GRAD = {  # gradients of the (unscaled) wall functionals y, sqrt3*x - y, sqrt3*(d-x) - y
    "AB": (Q3(0), Q3(1)),
    "AC": (R3, Q3(-1)),
    "BC": (-R3, Q3(-1)),
}


def rigidity_matrix(pts, s):
    d = s - Q3(0, 2)
    n = len(pts)
    rows = []
    labels = []
    for i in range(n):
        for j in range(i + 1, n):
            if ck.sqdist(pts[i], pts[j]) == Q3(4, 0):
                row = [ZERO] * (2 * n)
                dx = pts[i][0] - pts[j][0]
                dy = pts[i][1] - pts[j][1]
                row[2 * i] = dx
                row[2 * i + 1] = dy
                row[2 * j] = -dx
                row[2 * j + 1] = -dy
                rows.append(row)
                labels.append(("contact", i, j))
    for i in range(n):
        for k, v in ck.walls(pts[i], d).items():
            if v.is_zero():
                row = [ZERO] * (2 * n)
                g = GRAD[k]
                row[2 * i] = g[0]
                row[2 * i + 1] = g[1]
                rows.append(row)
                labels.append(("wall", i, k))
    return rows, labels, 2 * n


def rank(rows, ncols):
    m = [list(r) for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(m)):
            if not m[i][c].is_zero():
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = m[r][c].inv()
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and not m[i][c].is_zero():
                f = m[i][c]
                m[i] = [m[i][k] - f * m[r][k] for k in range(ncols)]
        r += 1
        if r == len(m):
            break
    return r


def slide_interval(pts, i, s, direction, tol=F(1, 10 ** 12)):
    """Largest [-a, b] such that p_i + t*direction stays feasible, direction a
    unit-ish Q3 vector.  Exact comparisons; returns rational brackets."""
    d = s - Q3(0, 2)
    n = len(pts)

    def ok(t):
        tq = Q3(t, 0)
        p = (pts[i][0] + tq * direction[0], pts[i][1] + tq * direction[1])
        for j in range(n):
            if j == i:
                continue
            if ck.sqdist(p, pts[j]) < Q3(4, 0):
                return False
        for v in ck.walls(p, d).values():
            if v.sign() < 0:
                return False
        return True

    res = []
    for sgn in (1, -1):
        lo, hi = F(0), F(1)
        while ok(sgn * hi) and hi < 100:
            hi *= 2
        while hi - lo > tol:
            mid = (lo + hi) / 2
            if ok(sgn * mid):
                lo = mid
            else:
                hi = mid
        res.append(lo)
    return (-res[1], res[0])
