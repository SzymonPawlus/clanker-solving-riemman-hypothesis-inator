"""
Realisability check for the C2 table.

An earlier draft minimised max(sqrt(r), M/3) over ALL integer (r, M) with r + M = 2(n-1).
That is unsound as an upper bound on rho(n): such a pair need not be realised by any
configuration.  This script instead CONSTRUCTS lattice configurations, verifies separation >= 1,
computes r and M from the actual convex hull, checks Oler tightness, and reports

    phi(E) = max(sqrt(r), M/3),      rho(n) <= min over constructed E with |E| = n.

Families constructed (all subsets of the unit triangular lattice, so separation is exactly 1):
  * T(m) minus up to three corner sub-triangles T(j1), T(j2), T(j3)   (triangle / trapezoid / hexagon)
  * P x Q lattice rhombus
"""
import math, json, itertools
import numpy as np
from scipy.spatial import ConvexHull

SQ3 = math.sqrt(3.0)
def tri(k): return k*(k+1)//2
def a_oler(n): return (math.sqrt(8*n+1)-3)/2

def hull_rM(P):
    h = ConvexHull(P)
    return 4.0*h.volume/SQ3, h.area

def min_sep(P):
    d = np.linalg.norm(P[:,None,:]-P[None,:,:], axis=-1)
    np.fill_diagonal(d, np.inf)
    return d.min()

def tri_lattice(m):
    """rows of T(m): points p*u + q*v, p,q >= 0, p+q <= m."""
    return {(p, q) for q in range(m+1) for p in range(m+1-q)}

def to_xy(S):
    return np.array([(p + q*0.5, q*SQ3/2) for (p, q) in sorted(S)])

def corner_cut(m, j1, j2, j3):
    """T(m) minus corner sub-triangles of sides j1 (at origin), j2 (at (m,0)), j3 (at top)."""
    S = tri_lattice(m)
    out = set()
    for (p, q) in S:
        if p + q <= j1 - 1: continue                 # corner at (0,0)
        if (m - p - q) + q <= j2 - 1: continue       # corner at (m,0):  distance m-p-q along, q up
        if p + (m - p - q) <= j3 - 1: continue       # corner at top
        out.add((p, q))
    return out

def rhombus(P, Q):
    return {(p, q) for p in range(P+1) for q in range(Q+1)}

def catalogue(mmax=9):
    recs = {}
    def add(S, tag):
        if len(S) < 3: return
        pts = to_xy(S)
        if min_sep(pts) < 1 - 1e-9: return
        try: r, M = hull_rM(pts)
        except Exception: return
        n = len(S)
        phi = max(math.sqrt(r), M/3.0)
        oler = (r + M)/2 + 1
        rec = recs.setdefault(n, [])
        rec.append((phi, r, M, oler, tag))
    for m in range(1, mmax+1):
        for j1 in range(0, m):
            for j2 in range(0, m):
                for j3 in range(0, m):
                    if j1 + j2 > m or j2 + j3 > m or j1 + j3 > m: continue
                    add(corner_cut(m, j1, j2, j3), f"T({m})-cut({j1},{j2},{j3})")
    for P in range(1, mmax+1):
        for Q in range(1, mmax+1):
            add(rhombus(P, Q), f"rhombus{P}x{Q}")
    return recs

if __name__ == "__main__":
    recs = catalogue()
    print("rho(n) <= min over CONSTRUCTED lattice configurations of max(sqrt r, M/3)")
    print(f"{'n':>4} {'a_Oler':>10} {'rho<=':>10} {'(r,M)':>12} {'Oler RHS':>9} {'tight?':>7} "
          f"{'gain in d':>10}  best family")
    rows = {}
    for n in sorted(recs):
        if n < 3 or n > 36: continue
        phi, r, M, oler, tag = min(recs[n])
        ao = a_oler(n)
        tight = abs(oler - n) < 1e-9
        assert phi >= ao - 1e-9, (n, phi, ao)      # C2 is never worse than Oler
        rows[n] = dict(a_oler=ao, rho_upper=phi, r=r, M=M, oler_rhs=oler,
                       oler_tight=bool(tight), gain_d=2*(phi-ao), family=tag)
        print(f"{n:>4} {ao:>10.6f} {phi:>10.6f} {f'({r:.3f},{M:.3f})':>12} {oler:>9.4f} "
              f"{str(tight):>7} {2*(phi-ao):>10.6f}  {tag}")
    with open("out/families.json", "w") as f:
        json.dump(rows, f, indent=1)
    print()
    print("assertion checked for every n above: rho_upper >= a_Oler  (C2 is never worse than Oler)")
    print()
    print("triangular n: gain must be exactly 0 ->",
          {n: round(rows[n]['gain_d'], 12) for n in rows if n in {tri(k) for k in range(2, 9)}})
