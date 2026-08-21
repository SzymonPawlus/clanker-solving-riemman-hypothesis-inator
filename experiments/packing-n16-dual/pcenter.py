"""Seed the subdivision from a COVERING, not from a packing.

Key elementary fact (this is the "dual" the attack is named for):

    Let C = {c_1..c_m} subset T and r = max_{x in T} min_i |x - c_i|
    (the covering radius of C in T).  Let V_i be the Voronoi cell of c_i.
    Then  V_i cap T  is contained in the disk D(c_i, r), so

        diam(V_i cap T)  <=  2r .

    Proof: x in V_i cap T is within r of *some* c_j, and |x-c_i| <= |x-c_j| <= r.

So a good m-point covering of T_1 hands us m CONVEX pieces of diameter <= 2r for
free, and minimising r (the classical p-centre / "cover a triangle by m equal
circles" problem) is a far better conditioned search than blind descent on the
max piece diameter.  The pieces are then handed to the free-vertex descent in
dual.py, which is strictly more general than Voronoi and can only improve them.

FLOATS ONLY.  Decides nothing; every output is re-frozen exactly in dual.py.
"""
import math, random, itertools

SQ3 = math.sqrt(3.0)

def tri_xy(a):
    return [(0.0, 0.0), (a, 0.0), (a/2.0, a*SQ3/2.0)]

def clip(poly, nx, ny, c):
    out = []; n = len(poly)
    for i in range(n):
        p = poly[i]; q = poly[(i+1) % n]
        fp = nx*p[0]+ny*p[1]-c; fq = nx*q[0]+ny*q[1]-c
        if fp <= 0: out.append(p)
        if (fp > 0) != (fq > 0):
            t = fp/(fp-fq)
            out.append((p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])))
    return out

def vcells(a, C):
    T = tri_xy(a); cells = []
    for i, p in enumerate(C):
        poly = list(T)
        for j, q in enumerate(C):
            if i == j: continue
            nx, ny = q[0]-p[0], q[1]-p[1]
            c = (q[0]*q[0]+q[1]*q[1] - p[0]*p[0] - p[1]*p[1])/2.0
            poly = clip(poly, nx, ny, c)
            if len(poly) < 3: poly = []; break
        cells.append(poly)
    return cells

def circum(A, B, C):
    d = 2*(A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))
    if abs(d) < 1e-15: return None
    ux = ((A[0]**2+A[1]**2)*(B[1]-C[1]) + (B[0]**2+B[1]**2)*(C[1]-A[1]) + (C[0]**2+C[1]**2)*(A[1]-B[1]))/d
    uy = ((A[0]**2+A[1]**2)*(C[0]-B[0]) + (B[0]**2+B[1]**2)*(A[0]-C[0]) + (C[0]**2+C[1]**2)*(B[0]-A[0]))/d
    return (ux, uy)

def mec(P):
    """minimum enclosing circle of a small point set (brute force)."""
    best = None
    for A, B in itertools.combinations(P, 2):
        c = ((A[0]+B[0])/2, (A[1]+B[1])/2); r = math.dist(A, c)
        if all(math.dist(x, c) <= r+1e-12 for x in P) and (best is None or r < best[1]):
            best = (c, r)
    for A, B, C in itertools.combinations(P, 3):
        c = circum(A, B, C)
        if c is None: continue
        r = math.dist(A, c)
        if all(math.dist(x, c) <= r+1e-12 for x in P) and (best is None or r < best[1]):
            best = (c, r)
    if best is None:
        best = (P[0], 0.0)
    return best

def cover_radius(a, C):
    cells = vcells(a, C)
    r = 0.0
    for i, cell in enumerate(cells):
        if not cell: continue
        r = max(r, max(math.dist(C[i], v) for v in cell))
    return r

def maxcelldiam(a, C):
    cells = vcells(a, C)
    d = 0.0
    for cell in cells:
        if len(cell) < 3: return float("inf")
        d = max(d, max(math.dist(p, q) for p, q in itertools.combinations(cell, 2)))
    return d

def inside(a, p, eps=1e-9):
    x, y = p
    return y >= -eps and y <= (a*SQ3/2)+eps and \
        (y*1.0) <= SQ3*x + eps and y <= SQ3*(a-x) + eps

def clampT(a, p):
    x, y = p
    y = min(max(y, 0.0), a*SQ3/2 - 1e-12)
    lo = y/SQ3; hi = a - y/SQ3
    x = min(max(x, lo), hi)
    return (x, y)

def pcenter(a, C, iters=400, damp=1.0):
    """Lloyd-type min-max iteration: move each site to the centre of the minimum
    enclosing circle of its Voronoi cell."""
    C = [tuple(p) for p in C]
    best = (cover_radius(a, C), list(C))
    for _ in range(iters):
        cells = vcells(a, C)
        newC = []
        for i, cell in enumerate(cells):
            if len(cell) < 3: newC.append(C[i]); continue
            c, r = mec(cell)
            newC.append(clampT(a, (C[i][0] + damp*(c[0]-C[i][0]),
                                   C[i][1] + damp*(c[1]-C[i][1]))))
        C = newC
        r = cover_radius(a, C)
        if r < best[0] - 1e-15: best = (r, list(C))
    return best

def to_uv(x, y): return (x - y/SQ3, 2.0*y/SQ3)
