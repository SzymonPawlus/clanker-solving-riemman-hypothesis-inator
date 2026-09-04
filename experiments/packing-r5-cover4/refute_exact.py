"""EXACT finite refutation of the k=4 covering route.

CLAIM (refutation, status: numerical/sketch -- reconstruction, not new maths):
    T(3) admits NO cover by 8 sets of diameter <= 1.
Consequently the covering/pigeonhole route cannot prove a(9) >= 3, i.e. cannot
reprove Melissen's s(9) = 6 + 2*sqrt(3).

REDUCTION (exact, elementary).  Let S_1..S_8 cover T(3), each of diameter <= 1.
The corners A,B,C are pairwise at distance 3 > 1, so they lie in three distinct
pieces.  A piece containing corner V has diameter <= 1, hence is contained in the
CLOSED unit disc Bbar(V,1).  Therefore every point of
        U = { z in T(3) : |z-V| > 1 for all three corners V }
lies in one of the remaining FIVE pieces.  So U -- and every finite subset of it --
admits a partition into 5 classes of diameter <= 1, i.e. a proper 5-colouring of
the graph with edges { p,q : |p-q| > 1 }.

We exhibit a finite P subset U whose graph is NOT 5-colourable.

EXACTNESS.  Points have rational (x,y).  Then
    in T(3):      y >= 0,  y^2 <= 3x^2  (x>=0),  y^2 <= 3(3-x)^2  (x<=3)
    |z-A|^2, |z-B|^2, |p-q|^2   are RATIONAL
    |z-C|^2 = (x-3/2)^2 + y^2 + 27/4  -  3y*sqrt3   lies in Q(sqrt3),
              and its comparison with 1 is decided by the exact sign test in Q(sqrt3).
No floating point enters any accept/reject decision.
"""
import sys, os, time, json
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exactgeom import Q3

A = 3  # side


def in_T(p):
    x, y = p
    if y < 0: return False
    if x < 0 or x > A: return False
    if y * y > 3 * x * x: return False
    if y * y > 3 * (A - x) ** 2: return False
    return True


def d2A(p): return p[0] ** 2 + p[1] ** 2
def d2B(p): return (p[0] - A) ** 2 + p[1] ** 2
def d2C_gt1(p):
    """exact test  |p-C|^2 > 1  with C = (3/2, (3/2)sqrt3)"""
    x, y = p
    val = Q3((x - F(A, 2)) ** 2 + y * y + F(3 * A * A, 4) - 1, -A * y)
    return val.sign() > 0


def in_U(p):
    return in_T(p) and d2A(p) > 1 and d2B(p) > 1 and d2C_gt1(p)


def sq(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def edges(P):
    n = len(P)
    return [(i, j) for i in range(n) for j in range(i + 1, n) if sq(P[i], P[j]) > 1]


def solve(P, k, proof=None):
    from pysat.solvers import Cadical153
    n = len(P); E = edges(P)
    var = lambda p, c: p * k + c + 1
    cnf = [[var(p, c) for c in range(k)] for p in range(n)]
    for (i, j) in E:
        for c in range(k):
            cnf.append([-var(i, c), -var(j, c)])
    s = Cadical153(bootstrap_with=cnf, with_proof=(proof is not None))
    t0 = time.time(); r = s.solve(); dt = time.time() - t0
    pf = s.get_proof() if (proof and not r) else None
    s.delete()
    return r, dt, len(E), cnf, pf


def rat_pts(den, nb, ni):
    """rational candidate points: dense interior grid + dense sampling just
    inside the three circular arcs and the three straight edges of U."""
    import math
    S3 = math.sqrt(3)
    cand = set()
    # interior triangular grid
    for j in range(ni + 1):
        for i in range(ni + 1 - j):
            x = F(A) * (2 * i + j) / (2 * ni)
            y = F(round(float(F(A) * j * S3 / (2 * ni)) * den), den)
            cand.add((x, y))
    # arcs of radius slightly > 1 around each corner, and points on the sides
    corners = [(0.0, 0.0), (float(A), 0.0), (A / 2, A * S3 / 2)]
    dirs = [(0.0, 60.0), (120.0, 180.0), (240.0, 300.0)]
    for (cx, cy), (a1, a2) in zip(corners, dirs):
        for t in range(nb + 1):
            th = math.radians(a1 + (a2 - a1) * t / nb)
            for rr in (1.004, 1.02, 1.06, 1.12):
                x = cx + rr * math.cos(th); y = cy + rr * math.sin(th)
                cand.add((F(round(x * den), den), F(round(y * den), den)))
    for (P0, P1) in [((0.0, 0.0), (float(A), 0.0)),
                     ((float(A), 0.0), (A / 2, A * S3 / 2)),
                     ((A / 2, A * S3 / 2), (0.0, 0.0))]:
        for t in range(nb + 1):
            s = 1.0 + t / nb          # arclength along the side, in [1,2]
            x = P0[0] + (P1[0] - P0[0]) * s / A
            y = P0[1] + (P1[1] - P0[1]) * s / A
            # pull very slightly inward so it stays in T under rounding
            gx, gy = A / 2, A * S3 / 6
            x += 1e-4 * (gx - x); y += 1e-4 * (gy - y)
            cand.add((F(round(x * den), den), F(round(y * den), den)))
    return sorted(p for p in cand if in_U(p))


if __name__ == "__main__":
    den = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    nb = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    ni = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    P = rat_pts(den, nb, ni)
    print(f"exact rational point set: |P| = {len(P)} (all verified in U exactly)")
    r, dt, ne, cnf, pf = solve(P, 5, proof=True)
    print(f"edges={ne}  5-colourable? {'SAT' if r else 'UNSAT'}   ({dt:.2f}s)")
    d = os.path.dirname(os.path.abspath(__file__))
    if not r:
        print("*** EXACT UNSAT ***")
        json.dump({"a": A, "k_total": 8, "k_residual": 5, "n": len(P),
                   "edges": ne, "sec": dt,
                   "points": [[str(x), str(y)] for x, y in P]},
                  open(os.path.join(d, "refutation_points.json"), "w"), indent=2)
        if pf:
            with open(os.path.join(d, "refutation.drat"), "w") as f:
                f.write("\n".join(pf) + "\n")
            print("wrote DRAT proof:", len(pf), "lemmas")
        with open(os.path.join(d, "refutation.cnf"), "w") as f:
            nv = max(abs(l) for cl in cnf for l in cl)
            f.write(f"p cnf {nv} {len(cnf)}\n")
            for cl in cnf:
                f.write(" ".join(map(str, cl)) + " 0\n")
        print("wrote CNF")
