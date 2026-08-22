#!/usr/bin/env python3
"""Kill-experiment: 6-direction (dodecagonal-norm) tomography relaxation.

Sequel to hexnorm.py.  Project pair differences onto SIX lines at 30deg spacing
(the 3 side normals + the 3 side directions).  For any planar vector,
max of the six |projections| >= cos(15deg)*|v|, so

  Euclid |pq| >= 1  ==>  dod(pq) := max_f w_f |L_f(pq)| >= t := cos(15deg),

where in oblique coordinates (basis e1=(1,0), e2=(1/2,sqrt3/2)) the six forms are
  normals:  w=sqrt3/2,  L in { du, dv, du+dv }
  sides:    w=1/2,      L in { 2du+dv, du+2dv, dv-du }.
Define M6(n) = least a admitting n points pairwise dod >= t in the simplex.
Then a_n >= M6(n) >= M(n) (hex).  Constraints are still disjunctions of half-
planes, so a lower bound on M6(16) would be LP/Farkas-certifiable in Q(sqrt3)
(t^2 = (2+sqrt3)/4).

KILL-CRITERION (fixed in advance): exhibit a configuration, verified EXACTLY in
Q(sqrt3), showing M6(16) < 1+2*sqrt(3).  Then the 6-direction relaxation can
never beat the standing record and dies like its 3-direction parent.
If the search finds nothing below ~4.55, the proposal survives triage.

Search: iterated LP over active disjuncts (as hexnorm.py), multistart.
Exact verification: rational coordinates; pair passes iff for some form,
w^2*L^2 >= t^2, an exact comparison of a rational against (2+sqrt3)/4.
"""
from fractions import Fraction
from itertools import combinations
import json, math, random
import numpy as np
from scipy.optimize import linprog

random.seed(20260822)
np.random.seed(20260822)

SQRT3 = math.sqrt(3.0)
T = math.cos(math.pi / 12)         # cos 15deg = 0.9659258...
W = [SQRT3/2]*3 + [0.5]*3

def forms(du, dv):
    return [du, dv, du + dv, 2*du + dv, du + 2*dv, dv - du]

def dodmin(P):
    m = float("inf")
    for (a1, b1), (a2, b2) in combinations(P, 2):
        fs = forms(a1 - a2, b1 - b2)
        d = max(w * abs(f) for w, f in zip(W, fs))
        if d < m: m = d
    return m

# form coefficient vectors on (u_i, v_i, u_j, v_j) as multiples: L = c_ui*u_i + ...
FORM_COEFS = [    # (cu, cv) applied to difference (du, dv)
    (1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (-1, 1),
]

def actives_of(P):
    act = {}
    for i, j in combinations(range(len(P)), 2):
        du = P[i][0] - P[j][0]; dv = P[i][1] - P[j][1]
        fs = forms(du, dv)
        vals = [w * abs(f) for w, f in zip(W, fs)]
        f = max(range(6), key=lambda k: vals[k])
        s = 1.0 if fs[f] >= 0 else -1.0
        act[(i, j)] = (f, s)
    return act

def solve_lp(n, a, active):
    """max s s.t. containment and per pair (w_f/t)*sign*L_f >= s."""
    nv = 2 * n + 1
    c = np.zeros(nv); c[-1] = -1.0
    A, b = [], []
    for i in range(n):
        row = np.zeros(nv); row[2*i] = 1; row[2*i+1] = 1
        A.append(row); b.append(a)
    for (i, j), (f, s) in active.items():
        cu, cv = FORM_COEFS[f]; w = W[f]
        row = np.zeros(nv)
        row[2*i] += -s * w / T * cu; row[2*i+1] += -s * w / T * cv
        row[2*j] += s * w / T * cu;  row[2*j+1] += s * w / T * cv
        row[-1] = 1.0
        A.append(row); b.append(0.0)
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b),
                  bounds=[(0, None)] * (2*n) + [(None, None)], method="highs")
    if not res.success: return None
    x = res.x
    return [(x[2*i], x[2*i+1]) for i in range(n)]

def polish(P, a, iters=50):
    best = dodmin(P); bestP = P
    for _ in range(iters):
        P2 = solve_lp(len(P), a, actives_of(P))
        if P2 is None: break
        m = dodmin(P2)
        if m > best + 1e-12: best, bestP = m, P2
        else: break
        P = P2
    return best, bestP

def random_start(n, a):
    P = []
    while len(P) < n:
        u = random.uniform(0, a); v = random.uniform(0, a)
        if u + v <= a: P.append((u, v))
    return P

def packing_seed(a):
    d = json.load(open("../circle-packing-search/out/n16.json"))
    P = []
    for x, y in d["unit_triangle_points"]:
        v = 2 * y / SQRT3; u = x - y / SQRT3
        P.append((u * a, v * a))
    return P

def lattice_seed(n, a, jit):
    pts = [(i, j) for i in range(9) for j in range(9) if i + j <= 8]
    pts.sort(key=lambda p: (p[0] + p[1], p[0]))
    base = pts[:n]
    s = a / max(u + v for u, v in base)
    return [(u*s + random.uniform(-jit, jit), v*s + random.uniform(-jit, jit))
            for u, v in base]

def exact_feasible(P, a):
    """Exact: are these (clipped, rationalized) points pairwise dod >= t in T_a?
    Pair passes iff exists form with w^2*L^2 >= t^2 = (2+sqrt3)/4, i.e.
    r := w2*L*L (rational) satisfies 4r-2 >= sqrt3  <=>  4r>=2 and (4r-2)^2>=3."""
    aF = Fraction(a).limit_denominator(10**6)
    Q = []
    for u, v in P:
        u = max(Fraction(0), min(Fraction(u).limit_denominator(10**9), aF))
        v = max(Fraction(0), min(Fraction(v).limit_denominator(10**9), aF))
        if u + v > aF:
            ex = (u + v - aF) / 2; u -= ex; v -= ex
        Q.append((u, v))
    W2 = [Fraction(3, 4)]*3 + [Fraction(1, 4)]*3
    for p, q in combinations(Q, 2):
        du, dv = p[0]-q[0], p[1]-q[1]
        fs = [du, dv, du+dv, 2*du+dv, du+2*dv, dv-du]
        ok = False
        for w2, L in zip(W2, fs):
            r = w2 * L * L
            if 4*r >= 2 and (4*r - 2)**2 >= 3:
                ok = True; break
        if not ok: return False, aF
    return True, aF

def search_at(a, restarts):
    starts = [packing_seed(a)] + [lattice_seed(16, a, j) for j in (0.05, 0.2, 0.35)]
    starts += [random_start(16, a) for _ in range(restarts)]
    best, bestP = -1.0, None
    for P0 in starts:
        m, P = polish(P0, a)
        if m > best: best, bestP = m, P
    return best, bestP

if __name__ == "__main__":
    print("t = cos15 = %.7f;  record threshold a = 1+2sqrt3 = 4.4641016" % T)
    # sanity control: n=4 at the hex cheat point -- does dodeca forbid it?
    Pcheat = [(0.0, 0.0), (1.5, 0.0), (0.0, 1.5), (0.5, 0.5)]
    print("control: hex cheat config (M(4)<=1.5 witness): dodmin/t = %.4f  (<1 kills the cheat?)"
          % (dodmin(Pcheat) / T))
    verdict = None
    for a in (4.40, 4.44, 4.46, 4.50, 4.55, 4.60):
        m, P = search_at(a, 60)
        feas_float = m >= T - 1e-9
        line = "a = %.2f: best min dod = %.6f (= %.4f * t) -> float-%s" % (
            a, m, m / T, "FEASIBLE" if feas_float else "infeasible")
        if feas_float:
            ok, aF = exact_feasible(P, a)
            line += "; exact check: %s" % ("PASS -> M6(16) <= %s = %.6f" % (aF, float(aF)) if ok else "fail")
            if ok and verdict is None:
                verdict = float(aF)
                with open("out/dodeca_best16.json", "w") as f:
                    json.dump({"a": a, "min_dod": m, "points_uv": P}, f, indent=1)
        print(line)
    if verdict is not None and verdict < 4.4641016:
        print("KILL-CRITERION FIRED: M6(16) <= %.6f < 1+2sqrt3; 6-direction route dead vs record." % verdict)
    elif verdict is not None:
        print("Feasible only at a >= %.6f: NOT killed below the record at this effort." % verdict)
    else:
        print("No exactly-verified feasible config found: NOT killed at this effort; promising.")
