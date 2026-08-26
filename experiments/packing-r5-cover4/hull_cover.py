"""YES-pipeline: take an 8-colouring of a fine lattice in T(a), convex-hull each
colour class, and verify EXACTLY (Q(sqrt3), inclusion-exclusion areas) whether the
8 hulls cover T(a) with squared diameter <= 1.

A hull of a class has the same diameter as the class, so the diameter test is
automatic; the real question is coverage.
"""
import sys, os, json, time
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exactgeom import Q3, pt, verify_cover, area, triangle, cross
from sat_cover import tri_lattice, colourable


def hull(points):
    """Exact convex hull (monotone chain) of (x,u) rational points, returned as
    Q3 points (x, u*sqrt3), CCW."""
    P = sorted(set(points))
    if len(P) <= 2:
        return None
    def cr(o, a, b):
        return (a[0]-o[0])*3*(b[1]-o[1]) - 3*(a[1]-o[1])*(b[0]-o[0])
    # careful: real coords are (x, u*sqrt3); cross = dx1*sqrt3*du2 - sqrt3*du1*dx2
    # = sqrt3*(dx1*du2 - du1*dx2); sign is that of the rational bracket.
    def cr2(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in P:
        while len(lo) >= 2 and cr2(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cr2(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    H = lo[:-1] + up[:-1]
    if len(H) < 3:
        return None
    return [(Q3(x), Q3(0, u)) for (x, u) in H]


def run(a, k, m, seed_note=""):
    pts = tri_lattice(a, m)
    sat, col, cl, ne, dt = colourable(pts, k)
    if not sat:
        print("UNSAT -> no cover"); return None
    cls = [[] for _ in range(k)]
    for i, c in enumerate(col):
        cls[c].append(pts[i])
    hulls = [hull(c) for c in cls]
    sizes = [len(c) for c in cls]
    print("class sizes:", sizes)
    if any(h is None for h in hulls):
        print("degenerate class -> hull missing:", [i for i,h in enumerate(hulls) if h is None])
        hulls = [h for h in hulls if h is not None]
    t0 = time.time()
    ok, rep = verify_cover(a, hulls)
    print(f"exact verification of {len(hulls)} hulls: OK={ok}  ({time.time()-t0:.2f}s)")
    print("  union_area =", rep.get("union_area"), " T_area =", rep.get("T_area"),
          " covers =", rep.get("covers"))
    bad = [kk for kk, v in rep.items() if kk.endswith("diam_ok") and not v]
    print("  pieces failing diameter:", bad)
    return ok, rep, hulls


if __name__ == "__main__":
    a = int(sys.argv[1]); k = int(sys.argv[2]); m = int(sys.argv[3])
    run(a, k, m)
