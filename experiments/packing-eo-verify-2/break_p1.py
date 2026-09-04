"""Break attempt on P1 (eo-boundary-counting §3.1):  |E cap dT| <= 3*floor(a)  for a >= 1.

Strategy: the maximum is determined by the six 'legs' (distance from each corner to the
nearest point of E on each adjacent side).  I enumerate Pareto-minimal leg pairs at each
corner on a rational grid, build the ACTUAL point set, and verify every pairwise squared
distance exactly.  Any construction with more than 3*floor(a) boundary points refutes P1.
"""
from fractions import Fraction as F
from itertools import product
import sys

def corner_pairs(g, a):
    """Pareto-minimal (x,y) leg pairs at an unoccupied corner: x^2-xy+y^2 >= 1, 0<x,y<=a.
    Plus the 'corner occupied' option (0,0)."""
    out = [(F(0), F(0), True)]           # corner occupied
    N = int(a / g)
    for i in range(0, N + 1):
        x = i * g
        # minimal grid y with x^2-xy+y^2 >= 1 and y > 0
        for j in range(0, N + 1):
            y = j * g
            if x == 0 and y == 0:
                continue
            if x * x - x * y + y * y >= 1:
                out.append((x, y, False))
                break
    for i in range(0, N + 1):
        y = i * g
        for j in range(0, N + 1):
            x = j * g
            if x == 0 and y == 0:
                continue
            if x * x - x * y + y * y >= 1:
                out.append((x, y, False))
                break
    return sorted(set(out))


def build(a, legs, occ):
    """legs[j] = (beta_{j-1}, alpha_j) at corner j.  Returns list of (side, offset) points."""
    pts = []
    for i in range(3):
        al = legs[i][1]
        be = legs[(i + 1) % 3][0]
        span = a - al - be
        if span < 0:
            return None
        m = int(span) + 1
        # place m points at al, al+1, ..., al+m-1 ; last must be <= a-be
        if al + (m - 1) > a - be:
            m -= 1
        if m <= 0:
            continue
        for t in range(m):
            off = al + t
            # skip a point that coincides with the shared corner of the previous side
            pts.append((i, off))
    return pts


def cart(a, p):
    """(side, offset) -> exact cartesian in Q(sqrt3) represented as (u,v) lattice coords
    where the triangle is 0, a*u, a*v with u=(1,0), v=(1/2,sqrt3/2)."""
    i, t = p
    if i == 0:      # A1=(0,0) -> A2=(a,0):  u = t, v = 0
        return (t, F(0))
    if i == 1:      # A2=(a,0) -> A3=(0,a) in (u,v):  u = a-t, v = t
        return (a - t, t)
    return (F(0), a - t)   # A3 -> A1


def sq(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv


def maxB(a, g):
    best = 0; bestcfg = None
    cps = corner_pairs(g, a)
    for c0, c1, c2 in product(cps, repeat=3):
        legs = [(c0[0], c0[1]), (c1[0], c1[1]), (c2[0], c2[1])]
        occ = [c0[2], c1[2], c2[2]]
        pts = build(a, legs, occ)
        if pts is None:
            continue
        C = [cart(a, p) for p in pts]
        # dedupe (a corner point appears on two sides)
        C = sorted(set(C))
        if len(C) <= best:
            continue
        ok = True
        for i in range(len(C)):
            for j in range(i + 1, len(C)):
                if sq(C[i], C[j]) < 1:
                    ok = False; break
            if not ok: break
        if ok and len(C) > best:
            best = len(C); bestcfg = (legs, occ)
    return best, bestcfg


if __name__ == "__main__":
    print(f"{'a':>10} {'floor(a)':>9} {'3*floor(a)':>11} {'floor(3a)':>10} {'best found':>11} {'verdict'}")
    for a_s, g in (("1", F(1,4)), ("3/2", F(1,4)), ("2", F(1,4)), ("5/2", F(1,4)),
                   ("3", F(1,4)), ("17/5", F(1,5)), ("4", F(1,4)), ("9/2", F(1,4)),
                   ("5", F(1,4)), ("59/10", F(1,5)), ("6", F(1,4))):
        a = F(a_s)
        b, cfg = maxB(a, g)
        k = int(a)
        v = "OK" if b <= 3 * k else "*** REFUTES P1 ***"
        print(f"{a_s:>10} {k:>9} {3*k:>11} {int(3*a):>10} {b:>11} {v}")
        sys.stdout.flush()
