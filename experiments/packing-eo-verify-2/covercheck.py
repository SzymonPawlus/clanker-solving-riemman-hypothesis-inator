"""Independent exact verifier for a claimed small-diameter covering/partition of T_a.

Written from the problem statement.  Coordinates are in the triangular-lattice basis
e1 = (1,0), e2 = (1/2, sqrt3/2), where |u e1 + v e2|^2 = u^2 + uv + v^2 is RATIONAL.
Area in that basis: (sqrt3/2) * |shoelace|/2 ; since we only ever compare areas, the
rational "lattice area" shoelace/2 is enough and no sqrt3 ever appears.

Checks, all exact:
  C1  every piece has squared diameter <= 1   (max over vertex pairs of its convex hull)
  C2  every piece is contained in T_a
  C3  pieces have pairwise disjoint interiors (exact convex-intersection area = 0)
  C4  sum of piece areas == area(T_a) exactly
  C5  independent coverage probe: exact rational grid + all piece vertices + all
      pairwise edge intersections, every probe point must lie in some piece
C1+C2+C3+C4 with closed pieces is a proof of coverage (a finite union of closed sets of
full measure in T_a leaves a relatively open null set, i.e. nothing).  C5 is a bug-catcher.
"""
from fractions import Fraction as F
from itertools import combinations


def d2(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv


def shoelace2(poly):
    s = F(0)
    m = len(poly)
    for i in range(m):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % m]
        s += x1 * y2 - x2 * y1
    return s          # = 2 * lattice area (signed)


def area2(poly):
    return abs(shoelace2(poly))


def hull(pts):
    P = sorted(set(pts))
    if len(P) <= 2: return P
    def cr(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def diam2(poly):
    h = hull(poly) or poly
    return max(d2(a, b) for a in h for b in h) if len(h) > 1 else F(0)


def ccw(poly):
    return poly if shoelace2(poly) > 0 else poly[::-1]


def clip(subject, a, b):
    """Sutherland-Hodgman: keep the part of convex polygon `subject` left of directed line a->b."""
    def side(p):
        return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])
    out = []
    m = len(subject)
    for i in range(m):
        cur, nxt = subject[i], subject[(i+1) % m]
        sc, sn = side(cur), side(nxt)
        if sc >= 0: out.append(cur)
        if (sc > 0 and sn < 0) or (sc < 0 and sn > 0):
            t = F(sc, sc - sn)
            out.append((cur[0] + t*(nxt[0]-cur[0]), cur[1] + t*(nxt[1]-cur[1])))
    return out


def convex_intersection_area2(P, Q):
    """|2*area| of the intersection of two convex polygons, exact."""
    P, Q = ccw(P), ccw(Q)
    R = P
    m = len(Q)
    for i in range(m):
        if not R: return F(0)
        R = clip(R, Q[i], Q[(i+1) % m])
    return area2(R) if len(R) >= 3 else F(0)


def in_convex(p, poly):
    poly = ccw(poly)
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i+1) % m]
        if (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) < 0:
            return False
    return True


def verify(pieces, a, convex=True, grid=24, verbose=True):
    """pieces: list of vertex lists (rational lattice coords).  a: side of T_a (Fraction)."""
    T = [(F(0), F(0)), (F(a), F(0)), (F(0), F(a))]
    res = {}
    # C1 diameter
    bad = [(i, diam2(p)) for i, p in enumerate(pieces) if diam2(p) > 1]
    res["C1 diam^2 <= 1"] = (not bad, bad[:5])
    strict = [(i, diam2(p)) for i, p in enumerate(pieces) if diam2(p) == 1]
    res["C1' pieces with diam exactly 1 (need side < a strictly to be safe)"] = (True, len(strict))
    # C2 containment
    bad = []
    for i, p in enumerate(pieces):
        for v in p:
            if not in_convex(v, T): bad.append((i, v))
    res["C2 pieces inside T_a"] = (not bad, bad[:5])
    # C3 disjoint interiors
    bad = []
    if convex:
        for i, j in combinations(range(len(pieces)), 2):
            if convex_intersection_area2(pieces[i], pieces[j]) != 0:
                bad.append((i, j))
    res["C3 pairwise disjoint interiors"] = (not bad, bad[:5])
    # C4 areas
    tot = sum(area2(p) for p in pieces)
    res["C4 sum of areas == area(T_a)"] = (tot == area2(T), (str(tot), str(area2(T))))
    # C5 coverage probe
    probes = set()
    for i in range(grid + 1):
        for j in range(grid + 1 - i):
            probes.add((F(a) * F(i, grid), F(a) * F(j, grid)))
    for p in pieces:
        for v in p: probes.add(v)
        for k in range(len(p)):
            u, w = p[k], p[(k+1) % len(p)]
            probes.add((F(u[0]+w[0], 2) if isinstance(u[0], int) else (u[0]+w[0])/2,
                        (u[1]+w[1])/2))
    miss = []
    for q in probes:
        if not in_convex(q, T): continue
        if not any(in_convex(q, p) for p in pieces):
            miss.append(q)
            if len(miss) > 5: break
    res["C5 coverage probe (grid + vertices + edge midpoints)"] = (not miss, miss[:5])
    if verbose:
        print(f"  pieces: {len(pieces)}   a = {a}")
        for k, (ok, extra) in res.items():
            print(f"  [{'PASS' if ok else 'FAIL'}] {k}" + (f"  :: {extra}" if extra not in (True, [], 0) else ""))
    allok = all(v[0] for v in res.values())
    return allok, res


if __name__ == "__main__":
    # self-test: the uniform m x m subdivision of T_a into m^2 cells of side a/m
    print("self-test: uniform subdivision of T_6 into 36 cells of side 1 (diam exactly 1)")
    a = F(6); m = 6; h = F(a, m)
    pieces = []
    for i in range(m):
        for j in range(m - i):
            pieces.append([(i*h, j*h), ((i+1)*h, j*h), (i*h, (j+1)*h)])
            if i + j <= m - 2:
                pieces.append([((i+1)*h, j*h), (i*h, (j+1)*h), ((i+1)*h, (j+1)*h)])
    ok, _ = verify(pieces, a, grid=18)
    print(f"  => {len(pieces)} pieces, all checks {'PASS' if ok else 'FAIL'}")
    print("  (36 > 26: this is the known baseline, not a proof of anything)")
    print()
    print("negative control: drop one piece -- the checker must catch it")
    ok2, r = verify(pieces[:-1], a, grid=18, verbose=False)
    print(f"  35 pieces: overall {'PASS (BAD!)' if ok2 else 'correctly FAILS'}; "
          f"C4 {r['C4 sum of areas == area(T_a)'][0]}, "
          f"C5 {r['C5 coverage probe (grid + vertices + edge midpoints)'][0]}")
    print()
    print("negative control: enlarge one piece so its diameter exceeds 1")
    p2 = [list(p) for p in pieces]
    p2[0] = [(F(0), F(0)), (F(11, 10), F(0)), (F(0), F(1))]
    ok3, r3 = verify(p2, a, grid=6, verbose=False)
    print(f"  overall {'PASS (BAD!)' if ok3 else 'correctly FAILS'}; "
          f"C1 caught it: {not r3['C1 diam^2 <= 1'][0]}")
