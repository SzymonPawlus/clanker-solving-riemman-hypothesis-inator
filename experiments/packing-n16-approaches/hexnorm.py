#!/usr/bin/env python3
"""Kill-experiment for the hexagonal-norm (3-direction tomography) relaxation.

Proposal (worker I1, issue #97).  For any two points of T_a, project onto the
three side-normal directions.  In oblique coordinates u,v (basis e1=(1,0),
e2=(1/2,sqrt3/2)) the squared projections of a difference vector (du,dv) onto
the three normals are (3/4)du^2, (3/4)dv^2, (3/4)(du+dv)^2, so

    Euclid |pq| >= 1   ==>   hex(pq) := max(|du|,|dv|,|du+dv|) >= 1,

with equality exactly for side-parallel unit vectors.  ("hex" because its unit
ball is a regular hexagon; the implication is the worst-case cos(30deg)=sqrt3/2
projection onto three lines at 60deg spacing.)  Define

    M(n) = least a such that n points with pairwise hex >= 1 fit in the simplex
           {u >= 0, v >= 0, u+v <= a}.

Then a_n >= M(n): a certified lower bound on M(16) would be a lower bound on
a_16, obtained from a PIECEWISE-LINEAR problem (each pair constraint is a
disjunction of 6 half-planes), i.e. exactly-certifiable by finite LP/Farkas data
with no square roots anywhere.

KILL-CRITERION (fixed before running): if an explicit configuration certifies
M(16) < 1+2*sqrt(3) = 4.4641... (the standing record), the relaxation can never
beat the record and the proposal dies.  Comparison is exact: the witness bound
is rational, the record is quadratic.

Method: maximize the min pairwise hex norm at fixed a by iterated LP over active
disjuncts (each pair's constraint linearized at its current argmax projection),
multistart from random + lattice + packing-derived seeds.  Any feasible output
is then made EXACT: coordinates -> Fractions, exact min hex norm m, exact
certificate M(n) <= a/m.  (Seeds from the numerical packing search are inputs
to a *kill decision* about this method's ceiling, not to any bound on a_16.)
"""
from fractions import Fraction
from itertools import combinations
import json, math, random
import numpy as np
from scipy.optimize import linprog

random.seed(20260822)
np.random.seed(20260822)

SQRT3 = math.sqrt(3.0)

def hexmin(P):
    m = float("inf")
    n = len(P)
    for i in range(n):
        for j in range(i + 1, n):
            du = P[i][0] - P[j][0]; dv = P[i][1] - P[j][1]
            h = max(abs(du), abs(dv), abs(du + dv))
            if h < m: m = h
    return m

def solve_lp(n, a, active):
    """max t s.t. simplex containment and, per pair, chosen signed form >= t.
    Variables: u0,v0,...,u_{n-1},v_{n-1},t   (2n+1).
    active[(i,j)] = (form, sign), form in {0:u, 1:v, 2:u+v}."""
    nv = 2 * n + 1
    c = np.zeros(nv); c[-1] = -1.0            # maximize t
    A, b = [], []
    for i in range(n):                         # u+v <= a  (u,v >= 0 via bounds)
        row = np.zeros(nv); row[2*i] = 1; row[2*i+1] = 1
        A.append(row); b.append(a)
    for (i, j), (f, s) in active.items():      # -s*(form_i - form_j) + t <= 0
        row = np.zeros(nv)
        if f == 0: cols = [(2*i, 1), (2*j, -1)]
        elif f == 1: cols = [(2*i+1, 1), (2*j+1, -1)]
        else: cols = [(2*i, 1), (2*i+1, 1), (2*j, -1), (2*j+1, -1)]
        for col, val in cols: row[col] = -s * val
        row[-1] = 1.0
        A.append(row); b.append(0.0)
    bounds = [(0, None)] * (2 * n) + [(None, None)]
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=bounds,
                  method="highs")
    if not res.success: return None, None
    x = res.x
    P = [(x[2*i], x[2*i+1]) for i in range(n)]
    return P, x[-1]

def actives_of(P):
    act = {}
    for i, j in combinations(range(len(P)), 2):
        du = P[i][0] - P[j][0]; dv = P[i][1] - P[j][1]
        vals = [du, dv, du + dv]
        f = max(range(3), key=lambda k: abs(vals[k]))
        s = 1.0 if vals[f] >= 0 else -1.0
        act[(i, j)] = (f, s)
    return act

def polish(P, a, iters=40):
    best = hexmin(P); bestP = P
    for _ in range(iters):
        act = actives_of(P)
        P2, t = solve_lp(len(P), a, act)
        if P2 is None: break
        m = hexmin(P2)
        if m > best + 1e-12: best, bestP = m, P2
        if m <= best - 1e-12 and t is not None and t <= best + 1e-12: break
        P = P2
    return best, bestP

def random_start(n, a):
    P = []
    while len(P) < n:
        u = random.uniform(0, a); v = random.uniform(0, a)
        if u + v <= a: P.append((u, v))
    return P

def lattice_starts(n, a):
    """near-triangular-lattice integer seeds, jittered."""
    outs = []
    pts = [(i, j) for i in range(10) for j in range(10) if i + j <= 8]
    pts.sort(key=lambda p: (p[0] + p[1], p[0]))
    base = pts[:n]
    for jit in (0.0, 0.15, 0.3):
        s = a / max(u + v for u, v in base)
        outs.append([(min(u*s + random.uniform(-jit, jit), a),
                      min(v*s + random.uniform(-jit, jit), a)) for u, v in base])
    return outs

def packing_seed(a):
    """oblique-converted numerical 16-point packing (kill-decision input only)."""
    d = json.load(open("../circle-packing-search/out/n16.json"))
    P = []
    for x, y in d["unit_triangle_points"]:
        v = 2 * y / SQRT3; u = x - y / SQRT3
        P.append((u, v))
    s = a  # unit triangle -> scale to a
    return [(u * s, v * s) for u, v in P]

def estimate_M(n, a, restarts, seeds=()):
    best, bestP = -1.0, None
    starts = list(seeds) + lattice_starts(n, a) if n >= 10 else list(seeds)
    for _ in range(restarts): starts.append(random_start(n, a))
    for P0 in starts:
        m, P = polish(P0, a)
        if m > best: best, bestP = m, P
    return best, bestP

def exact_bound(P, a):
    """exact certificate M(n) <= a_ex/m_ex from a float configuration."""
    Q = [(Fraction(u).limit_denominator(10**9), Fraction(v).limit_denominator(10**9))
         for u, v in P]
    # clip into simplex exactly
    aF = Fraction(a).limit_denominator(10**6)
    Q2 = []
    for u, v in Q:
        u = max(Fraction(0), min(u, aF)); v = max(Fraction(0), min(v, aF))
        if u + v > aF:
            ex = (u + v - aF) / 2
            u -= ex; v -= ex
        Q2.append((u, v))
    m = min(max(abs(p[0]-q[0]), abs(p[1]-q[1]), abs(p[0]+p[1]-q[0]-q[1]))
            for p, q in combinations(Q2, 2))
    assert m > 0
    return aF / m      # exact rational upper bound on M(n)

def frac_lt_quad(r: Fraction, c0: int, c1: int, k: int) -> bool:
    """exact test  r < c0 + c1*sqrt(k)  for rational r, integers c0,c1>0,k>0."""
    t = r - c0
    if t < 0: return True
    return t * t < c1 * c1 * k

if __name__ == "__main__":
    print("control n=3 at a=1.0 (Euclid a_3 = 1):")
    m, P = estimate_M(3, 1.0, 40)
    print("  best min-hex = %.6f  => M(3) <~ %.6f" % (m, 1.0 / m))
    print("control n=4 at a=1.5 (Euclid a_4 = sqrt3 = 1.732; hand cheat says M(4)<=1.5):")
    m, P = estimate_M(4, 1.5, 60)
    print("  best min-hex = %.6f  => M(4) <~ %.6f" % (m, 1.5 / m))
    b = exact_bound(P, 1.5)
    print("  exact:  M(4) <= %s = %.9f" % (b, float(b)))

    print("n=15 at a=4.0 (Euclid a_15 = 4, cited):")
    m, P = estimate_M(15, 4.0, 60)
    print("  best min-hex = %.6f  => M(15) <~ %.6f" % (m, 4.0 / m))
    b15 = exact_bound(P, 4.0)
    print("  exact:  M(15) <= %s = %.9f" % (b15, float(b15)))

    print("n=16 at a=4.5:")
    m16, P16 = estimate_M(16, 4.5, 150, seeds=[packing_seed(4.5)])
    print("  best min-hex = %.6f  => M(16) <~ %.6f" % (m16, 4.5 / m16))
    b16 = exact_bound(P16, 4.5)
    print("  exact certificate:  M(16) <= %s = %.9f" % (b16, float(b16)))
    dead_record = frac_lt_quad(b16, 1, 2, 3)     # < 1+2*sqrt(3) ?
    dead_oler = (2*b16 + 3)**2 < 129             # < (-3+sqrt129)/2 ?
    print("  M(16) < 1+2sqrt3 (record)?  %s   (exact)" % dead_record)
    print("  M(16) < Oler?               %s   (exact)" % dead_oler)
    if dead_record:
        print("  KILL-CRITERION FIRED: hexnorm relaxation can never beat the record.")
    else:
        print("  KILL-CRITERION NOT FIRED at this search effort.")
    with open("out/hexnorm_best16.json", "w") as f:
        json.dump({"a": 4.5, "min_hex": m16, "points_uv": P16}, f, indent=1)
