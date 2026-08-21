#!/usr/bin/env python3
"""Independent exact checker for "Lemma L" and the bound it is claimed to give.

Written from the STATEMENT of the lemma only (attacks/eo-covering-construct/README.md
section 2, prose), not from the author's code.  Nothing here is imported from, or
adapted from, experiments/packing-eo-covering/.

Normalisation (this file's own, fixed here):
  separation 1; T_a = closed equilateral triangle of side a with corners
  (0,0), (a,0), (a/2, a*sqrt3/2).

Coordinates.  Work in the triangular-lattice basis e1=(1,0), e2=(1/2,sqrt3/2) and then
rescale by g = sqrt3/2, i.e. a point written (x,y) here denotes the plane point
      g * ( x*e1 + y*e2 ).
Then
      |g*(x e1 + y e2)|^2 = g^2 (x^2 + x y + y^2) = (3/4) * Q(x,y),   Q(x,y)=x^2+xy+y^2,
      T_a = { x>=0, y>=0, x+y <= lam },  where a = lam * g.
Everything is therefore RATIONAL whenever lam is rational: no sqrt3 ever appears, and
      diam <= 1   <=>   Q <= 4/3.
The lemma's threshold a <= p*sqrt3/2 is exactly lam <= p.

Run:  python3 lemmaL.py
"""

from fractions import Fraction as F
import itertools
import json
import sys

# ----------------------------------------------------------------- exact geometry

def Q(x, y):
    """Squared Euclidean length of g*(x e1 + y e2), divided by g^2 = 3/4."""
    return x * x + x * y + y * y


def qdist2(P, R):
    return Q(P[0] - R[0], P[1] - R[1])


def bilin(A, B):
    """Symmetric bilinear form with bilin(X,X) = Q(X)."""
    return A[0] * B[0] + F(1, 2) * (A[0] * B[1] + A[1] * B[0]) + A[1] * B[1]


def clip(poly, c, d):
    """Sutherland-Hodgman: intersect convex polygon with half-plane c.x <= d (exact)."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        P = poly[i]
        R = poly[(i + 1) % n]
        vp = c[0] * P[0] + c[1] * P[1] - d
        vr = c[0] * R[0] + c[1] * R[1] - d
        if vp <= 0:
            out.append(P)
        if (vp < 0 and vr > 0) or (vp > 0 and vr < 0):
            t = vp / (vp - vr)
            out.append((P[0] + t * (R[0] - P[0]), P[1] + t * (R[1] - P[1])))
    # drop consecutive duplicates
    ded = []
    for pt in out:
        if not ded or ded[-1] != pt:
            ded.append(pt)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded


def area2(poly):
    """Twice the signed shoelace area in (x,y) coordinates (a fixed positive multiple
    of the true Euclidean area: the basis has determinant g^2*sqrt3/2 > 0)."""
    s = F(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s


def diam2(poly):
    """Max Q over vertex pairs.  For a convex polygon this IS the squared diameter,
    since diam(conv V) = diam(V) for any norm."""
    best = F(0)
    arg = None
    for A, B in itertools.combinations(poly, 2):
        q = qdist2(A, B)
        if q > best:
            best, arg = q, (A, B)
    return best, arg


# ----------------------------------------------------------------- the construction

def sites(p, lam):
    """Delta(p) lattice sites of spacing sqrt3/2 (=1 in x,y units), centred in T_a."""
    u0 = (lam - (p - 1)) / 3
    return [((u0 + i), (u0 + j)) for i in range(p) for j in range(p) if i + j <= p - 1]


def voronoi_cells(p, lam):
    """Voronoi cells of those sites, clipped to T_a.  Convex by construction."""
    S = sites(p, lam)
    tri = [(F(0), F(0)), (lam, F(0)), (F(0), lam)]
    cells = []
    for i, P in enumerate(S):
        poly = list(tri)
        for j, R in enumerate(S):
            if i == j:
                continue
            # keep { x : Q(x-P) <= Q(x-R) }  <=>  2 B(x, R-P) <= Q(R) - Q(P)
            D = (R[0] - P[0], R[1] - P[1])
            c = (2 * bilin((F(1), F(0)), D), 2 * bilin((F(0), F(1)), D))
            d = Q(R[0], R[1]) - Q(P[0], P[1])
            poly = clip(poly, c, d)
            if not poly:
                break
        cells.append(poly)
    return S, cells


def kind(p, i, j):
    on = [i == 0, j == 0, i + j == p - 1]
    return {3: "corner", 2: "corner", 1: "edge", 0: "interior"}[sum(on)]


# ----------------------------------------------------------------- the checks

FAIL = []
NCHECK = [0]


def check(cond, label):
    NCHECK[0] += 1
    if not cond:
        FAIL.append(label)
        print("  FAIL: " + label)
    return cond


def examine(p, lam, verbose=True, want_ok=True):
    """Full exact examination of the construction at (p, lam).  Returns max Q-diameter."""
    S, cells = voronoi_cells(p, lam)
    idx = [(i, j) for i in range(p) for j in range(p) if i + j <= p - 1]
    npts = p * (p + 1) // 2

    check(len(S) == npts, f"p={p}: site count is Delta(p)={npts}")

    # every cell nonempty with positive area
    tot = F(0)
    worst = F(0)
    worstkind = None
    per_kind = {}
    for (i, j), poly in zip(idx, cells):
        k = kind(p, i, j)
        if not poly or len(poly) < 3:
            check(False, f"p={p} lam={lam}: cell {(i,j)} is empty/degenerate")
            continue
        A = abs(area2(poly))
        check(A > 0, f"p={p} lam={lam}: cell {(i,j)} has positive area")
        tot += A
        # containment in T_a  (vertices suffice: T_a convex)
        for (x, y) in poly:
            check(x >= 0 and y >= 0 and x + y <= lam,
                  f"p={p} lam={lam}: cell {(i,j)} vertex inside T_a")
        d2, _ = diam2(poly)
        per_kind.setdefault(k, F(0))
        if d2 > per_kind[k]:
            per_kind[k] = d2
        if d2 > worst:
            worst, worstkind = d2, (k, (i, j))

    # areas sum EXACTLY to area(T_a):  shoelace of the triangle is lam^2
    check(tot == lam * lam, f"p={p} lam={lam}: cell areas sum exactly to area(T_a)")

    # pairwise interiors disjoint: intersection of two cells has zero area
    for (ia, pa), (ib, pb) in itertools.combinations(list(zip(idx, cells)), 2):
        if not pa or not pb:
            continue
        # clip pa by the half-planes of pb (pb convex, orientation-independent test)
        inter = list(pa)
        n = len(pb)
        # ensure pb is CCW for the edge-normal test
        pbo = pb if area2(pb) > 0 else pb[::-1]
        for t in range(n):
            x1, y1 = pbo[t]
            x2, y2 = pbo[(t + 1) % n]
            # inside is to the left: (x2-x1)(y-y1)-(y2-y1)(x-x1) >= 0
            c = (-(y2 - y1), (x2 - x1))
            d = -(y2 - y1) * x1 + (x2 - x1) * y1
            inter = clip(inter, (-c[0], -c[1]), -d)
            if not inter:
                break
        if inter and len(inter) >= 3:
            check(abs(area2(inter)) == 0,
                  f"p={p} lam={lam}: cells {ia},{ib} have disjoint interiors")

    ok = worst <= F(4, 3)
    if want_ok:
        check(ok, f"p={p} lam={lam}: every cell has squared diameter <= 1")
    if verbose:
        sq = F(3, 4) * worst
        print(f"  p={p:2d} lam={lam!s:>10} cells={npts:3d}  max diam^2 = {sq} "
              f"= {float(sq):.9f}  (worst cell: {worstkind[0]} {worstkind[1]})")
        pk = {k: float(F(3, 4) * v) for k, v in sorted(per_kind.items())}
        print(f"        by kind: " + ", ".join(f"{k}={v:.9f}" for k, v in pk.items()))
    return worst, ok


def main():
    print("=" * 78)
    print("A. Lemma L at the threshold a = p*sqrt3/2  (lam = p): every cell diam <= 1?")
    print("=" * 78)
    rows = {}
    for p in range(2, 13):
        w, ok = examine(p, F(p))
        rows[p] = (str(F(3, 4) * w), ok)

    print()
    print("=" * 78)
    print("B. Just below and just above the threshold")
    print("=" * 78)
    for p in (5, 7):
        print(f" p={p}, lam = p - 1/1000  (a < p*sqrt3/2): expect max diam < 1")
        examine(p, F(p) - F(1, 1000))
        print(f" p={p}, lam = p + 1/1000  (a > p*sqrt3/2): expect FAILURE (diam > 1)")
        w, ok = examine(p, F(p) + F(1, 1000), want_ok=False)
        check(not ok, f"p={p}: construction genuinely fails above the threshold")

    print()
    print("=" * 78)
    print("C. The equality-case witness: at a = a_0 exactly the pigeonhole step is FALSE")
    print("=" * 78)
    # p=2, lam=2  (a = sqrt3).  Corners of T_a plus its centroid: 4 points, pairwise
    # distance >= 1, inside a triangle covered by only Delta(2)=3 cells.
    lam = F(2)
    pts = [(F(0), F(0)), (lam, F(0)), (F(0), lam), (lam / 3, lam / 3)]
    ds = []
    for A, B in itertools.combinations(pts, 2):
        ds.append(F(3, 4) * qdist2(A, B))
    check(min(ds) == 1, "p=2: the 4 witness points have min squared distance exactly 1")
    for (x, y) in pts:
        check(x >= 0 and y >= 0 and x + y <= lam, "p=2: witness point inside T_sqrt3")
    print("  witness squared distances:", [str(d) for d in ds])
    print("  -> T_{sqrt3} carries 4 points at pairwise distance >= 1, but Lemma L")
    print("     covers it with only Delta(2) = 3 cells of diameter <= 1.")
    print("     So 'diam <= 1' + pigeonhole at a = a_0 is FALSE; the strict-scaling")
    print("     repair (a < a_0 => diam <= a/a_0 < 1) is NECESSARY, not cosmetic.")

    print()
    print("=" * 78)
    print("D. The derived bound a_{Delta(p)+1} >= p*sqrt3/2 against known values")
    print("=" * 78)
    # known a_n in THIS normalisation: a = (s(n) - 2 sqrt3)/2, separation 1 <-> /2
    import math
    s3 = math.sqrt(3)
    known = {   # n : exact s(n) as a float, from the problem README `cited` table
        4: 4 * s3, 7: 2 + 4 * s3, 11: 4 + 2 * s3 + 4 * math.sqrt(6) / 3,
        6: 4 + 2 * s3, 10: 6 + 2 * s3, 15: 8 + 2 * s3, 21: 10 + 2 * s3,
        28: 12 + 2 * s3,
    }
    a_of = lambda n: (known[n] - 2 * s3) / 2
    print(f"  {'p':>2} {'n=D(p)+1':>9} {'bound p*sqrt3/2':>16} {'Oler':>10} "
          f"{'known a_n':>12} {'a_{D(p)} known':>14}")
    for p in range(2, 9):
        n = p * (p + 1) // 2 + 1
        bound = p * s3 / 2
        oler = (math.sqrt(8 * n + 1) - 3) / 2
        kn = f"{a_of(n):.6f}" if n in known else "open"
        kd = f"{a_of(n-1):.6f}" if (n - 1) in known else "open"
        print(f"  {p:>2} {n:>9} {bound:>16.6f} {oler:>10.6f} {kn:>12} {kd:>14}")
        if n in known:
            check(bound <= a_of(n) + 1e-12,
                  f"p={p}: bound {bound:.6f} does not exceed the known a_{n}")
        # the TRIVIAL bound a_{D(p)+1} >= a_{D(p)} = p-1 (monotone in n); the covering
        # bound is only worth anything when it beats BOTH that and Oler.
        triv = p - 1
        useful = bound > triv and bound > oler
        print(f"     {'':>2} {'':>9} trivial a_{{D(p)}}={triv}  "
              f"covering beats both: {useful}")
        check(bound <= max(bound, triv) + 1e-12, "informational")

    print()
    print(f"  n=16 (p=5): covering bound {5*s3/2:.7f}  vs Oler {(math.sqrt(129)-3)/2:.7f}"
          f"  -> improvement {5*s3/2 - (math.sqrt(129)-3)/2:.7f}")
    print(f"  in side-length terms s(16) >= 2sqrt3 + 2*(5sqrt3/2) = 7 sqrt3 = "
          f"{7*s3:.7f}   (Oler: {2*s3 + 2*(math.sqrt(129)-3)/2:.7f})")

    print()
    print("=" * 78)
    print(f"{NCHECK[0]} checks run, {len(FAIL)} failures")
    print("=" * 78)
    if FAIL:
        for f in FAIL:
            print("  FAILED:", f)
        sys.exit(1)
    json.dump({"threshold_max_sq_diam": {str(k): v[0] for k, v in rows.items()}},
              open("out/lemmaL.json", "w"), indent=1)


if __name__ == "__main__":
    main()
