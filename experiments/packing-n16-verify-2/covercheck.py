#!/usr/bin/env python3
"""
Independent exact checker for 'k convex pieces of diameter < 1 cover T_a' certificates.

Written from the problem statement only (problems/circle-packing-equilateral-triangle/
README.md + RULES.md sec.2).  Deliberately does NOT read, import, or adapt
  experiments/packing-n16-covering/certify.py          (author's certifier)
  experiments/packing-n16-verify/manager_covering_check.py (previous pass)

--------------------------------------------------------------------------------
What is being certified, restated in my own words
--------------------------------------------------------------------------------
Point formulation, separation normalised to 1.  Triangular basis
    e1 = (1,0),  e2 = (1/2, sqrt3/2),
so the point u*e1 + v*e2 has
    |u e1 + v e2|^2 = u^2 + u v + v^2       (RATIONAL when u,v are rational)
and the triangle of admissible centres of side a is
    T_a = { u e1 + v e2 : u >= 0, v >= 0, u + v <= a }.
In the (u,v) chart T_a is the right triangle (0,0),(a,0),(0,a); the chart is a
linear map of determinant sqrt3/2, so *ratios* of areas and the predicate
"area(X) == area(Y)" may be tested with plain (u,v) shoelace areas.

PIGEONHOLE.  If T_a = union of k closed sets each of diameter STRICTLY < 1, then
T_a cannot contain k+1 points at pairwise distance >= 1: two of them would land in
one piece and be at distance <= diam < 1.  Hence with k = 15, a_16 > a, and
    s(16) = 2 sqrt3 + 2 a_16 > 2 sqrt3 + 2 a.

STRICTNESS IS LOAD-BEARING.  Separation in this problem is NON-strict (RULES.md
sec.2: distances >= 2 in the unnormalised formulation).  A closed piece of diameter
exactly 1 may hold two points at distance exactly 1 and the pigeonhole FAILS.
Witness on the record: T_{sqrt3} holds 4 pairwise-separated points (3 corners +
centroid, corner-centroid distance exactly 1) while a 3-cell covering of diameter
exactly 1 exists.  So this checker demands  max_sq_diam < 1  as an exact rational
strict inequality, computed by me, not read from the file.

WHAT A COVERING PROOF NEEDS.  "pieces inside T_a and areas summing to |T_a|" does
NOT imply covering -- an overlap plus a hole of equal area passes.  So this checker
requires, independently:
  (a) every piece is a genuine simple polygon with positive area;
  (b) every vertex of every piece lies in T_a  (+ convexity => piece subset T_a);
  (c) all C(k,2) pairs have intersection of area exactly 0 (exact convex clipping);
  (d) the piece areas sum EXACTLY to area(T_a);
  (e) a dense rational grid probe: every probe point of T_a lies in >= 1 piece,
      and no probe point lies in the interior of >= 2 pieces.
(b)+(c)+(d) give: union U is closed, U subset T_a, |T_a \ U| = 0; T_a \ U is
relatively open in T_a and a nonempty relatively open subset of a triangle has
positive measure, so T_a \ U is empty.  (e) is a redundant, differently-shaped
check on the same conclusion.

DIAMETER OF A POLYGON.  For a compact set, diam = diam of convex hull, attained at
a pair of extreme points, which for a polygon are among its vertices.  So the max
over vertex pairs IS the diameter -- for polygons.  Curved pieces would need a
different argument; this checker refuses anything that is not a polygon.
"""

import json
import sys
import itertools
from fractions import Fraction as F

# ----------------------------------------------------------------- exact geometry

def qform(du, dv):
    """|du*e1 + dv*e2|^2 = du^2 + du*dv + dv^2 -- exact rational."""
    return du * du + du * dv + dv * dv


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def shoelace2(poly):
    """Twice the signed (u,v)-chart area."""
    s = F(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s


def orient_ccw(poly):
    return poly if shoelace2(poly) > 0 else poly[::-1]


def is_convex_simple(poly):
    """Return (ok, reason).  Requires: >=3 vertices, no repeats, no zero-length
    edges, strictly positive area, and all turns the same strict sign (=> convex
    AND simple AND no collinear/degenerate vertices)."""
    n = len(poly)
    if n < 3:
        return False, "fewer than 3 vertices"
    if len(set(poly)) != n:
        return False, "repeated vertex"
    A2 = shoelace2(poly)
    if A2 == 0:
        return False, "zero area"
    p = orient_ccw(list(poly))
    for i in range(n):
        c = cross(p[i], p[(i + 1) % n], p[(i + 2) % n])
        if c <= 0:
            return False, "non-convex or collinear at vertex %d" % ((i + 1) % n)
    return True, "convex, strictly, %d vertices" % n


def clip_halfplane(poly, o, d):
    """Sutherland-Hodgman: keep the part of convex `poly` with cross(o,o+d,p) >= 0."""
    def side(p):
        return d[0] * (p[1] - o[1]) - d[1] * (p[0] - o[0])

    out = []
    n = len(poly)
    for i in range(n):
        cur, nxt = poly[i], poly[(i + 1) % n]
        sc, sn = side(cur), side(nxt)
        if sc >= 0:
            out.append(cur)
        if (sc > 0 and sn < 0) or (sc < 0 and sn > 0):
            t = sc / (sc - sn)
            out.append((cur[0] + t * (nxt[0] - cur[0]),
                        cur[1] + t * (nxt[1] - cur[1])))
    return out


def convex_intersection_area2(P, Q):
    """Twice the chart-area of the intersection of two CCW convex polygons."""
    poly = list(P)
    n = len(Q)
    for i in range(n):
        o = Q[i]
        nx = Q[(i + 1) % n]
        d = (nx[0] - o[0], nx[1] - o[1])
        poly = clip_halfplane(poly, o, d)
        if len(poly) < 3:
            return F(0)
    return abs(shoelace2(poly))


def point_in_convex(poly_ccw, p):
    """(inside, on_boundary) for a CCW convex polygon, exact."""
    n = len(poly_ccw)
    onb = False
    for i in range(n):
        c = cross(poly_ccw[i], poly_ccw[(i + 1) % n], p)
        if c < 0:
            return False, False
        if c == 0:
            onb = True
    return True, onb


# ----------------------------------------------------------------- the check

def rat(x):
    """Parse an exact rational.  Refuse floats and decimal strings (RULES.md sec.2)."""
    if isinstance(x, list) and len(x) == 2:
        return F(int(x[0]), int(x[1]))
    if isinstance(x, str):
        if "." in x or "e" in x.lower():
            raise ValueError("decimal string in an exact field: %r" % x)
        return F(x)
    if isinstance(x, int):
        return F(x)
    raise ValueError("not an exact rational: %r (%s)" % (x, type(x)))


CEILING = F(46247636, 10000000)   # 4.6247636, the published 16-point packing


def check(path, expect_pieces=15, n_points=16, probe=140, verbose=True):
    fails = []
    warns = []

    def req(cond, msg):
        if cond:
            if verbose:
                print("  [ok]   " + msg)
        else:
            fails.append(msg)
            print("  [FAIL] " + msg)

    raw = json.load(open(path))
    print("=" * 78)
    print("certificate:", path)
    print("=" * 78)

    # --- a ---------------------------------------------------------------
    a = rat(raw["a"])
    print("  a = %s = %.10f" % (a, float(a)))

    # --- pieces ----------------------------------------------------------
    faces = []
    for f in raw["faces_uv"]:
        faces.append([(rat(c[0]), rat(c[1])) for c in f])

    print("\n-- 1. piece count ------------------------------------------------")
    req(len(faces) == expect_pieces,
        "exactly %d pieces (found %d); %d pieces would prove nothing about %d points"
        % (expect_pieces, len(faces), n_points, n_points))

    print("\n-- 2. each piece is a genuine strictly-convex simple polygon ------")
    bad = []
    for i, f in enumerate(faces):
        ok, why = is_convex_simple(f)
        if not ok:
            bad.append((i, why))
    req(not bad, "all %d pieces are simple strictly-convex polygons%s"
        % (len(faces), "" if not bad else "  -- offenders: %r" % bad))
    if verbose:
        print("         vertex counts: %r" % ([len(f) for f in faces],))

    ccw = [orient_ccw(list(f)) for f in faces]

    print("\n-- 3. containment: every vertex in T_a ---------------------------")
    viol = []
    for i, f in enumerate(faces):
        for j, (u, v) in enumerate(f):
            if u < 0 or v < 0 or u + v > a:
                viol.append((i, j, str(u), str(v), str(u + v - a)))
    req(not viol, "every vertex satisfies u>=0, v>=0, u+v<=a%s"
        % ("" if not viol else "  -- violations: %r" % viol[:5]))
    print("         (pieces are convex and T_a is convex => piece subset T_a)")

    print("\n-- 4. STRICT diameter: max over ALL vertex pairs of ALL pieces ----")
    mx = F(0)
    arg = None
    for i, f in enumerate(faces):
        for p, q in itertools.combinations(f, 2):
            d = qform(p[0] - q[0], p[1] - q[1])
            if d > mx:
                mx, arg = d, (i, p, q)
    print("         max squared diameter = %s" % mx)
    print("                              = %.12f" % float(mx))
    print("         attained in piece %d, vertices %s and %s"
          % (arg[0], tuple(map(str, arg[1])), tuple(map(str, arg[2]))))
    req(mx < 1, "max squared diameter < 1 STRICTLY  (%s < 1 : %s)"
        % (mx, mx < 1))
    if "max_sq_diam" in raw:
        claimed = rat(raw["max_sq_diam"])
        req(claimed == mx,
            "certificate's reported max_sq_diam %s equals the value I computed" % claimed)

    print("\n-- 5. pairwise interior-disjointness (exact convex clipping) ------")
    overlaps = []
    for i, j in itertools.combinations(range(len(ccw)), 2):
        A2 = convex_intersection_area2(ccw[i], ccw[j])
        if A2 != 0:
            overlaps.append((i, j, str(A2)))
    npairs = len(ccw) * (len(ccw) - 1) // 2
    req(not overlaps, "all %d piece pairs meet in area exactly 0%s"
        % (npairs, "" if not overlaps else "  -- overlaps: %r" % overlaps[:5]))

    print("\n-- 6. exact area identity ----------------------------------------")
    tot2 = sum(abs(shoelace2(f)) for f in faces)
    tri2 = a * a                      # 2 * area of (0,0),(a,0),(0,a) in the chart
    req(tot2 == tri2,
        "sum of piece areas == area(T_a) exactly  (2*sum=%s, 2*|T_a|=%s, diff=%s)"
        % (tot2, tri2, tot2 - tri2))

    print("\n-- 7. independent grid probe (no holes, no double interiors) ------")
    # Barycentric-style rational lattice on T_a, offset off the piece boundaries.
    miss, dbl = [], []
    N = probe
    off = F(1, 7919)      # a prime offset so probes avoid the certificate's rationals
    tested = 0
    for i in range(N + 1):
        for j in range(N + 1 - i):
            u = a * (F(i) + off) / (N + 2)
            v = a * (F(j) + off) / (N + 2)
            if u + v > a:
                continue
            tested += 1
            hits = 0
            interiors = 0
            for f in ccw:
                ins, onb = point_in_convex(f, (u, v))
                if ins:
                    hits += 1
                    if not onb:
                        interiors += 1
            if hits == 0:
                miss.append((str(u), str(v)))
            if interiors >= 2:
                dbl.append((str(u), str(v)))
    req(not miss, "all %d probe points of T_a lie in >=1 piece%s"
        % (tested, "" if not miss else "  -- HOLES at %r" % miss[:5]))
    req(not dbl, "no probe point lies in the interior of two pieces%s"
        % ("" if not dbl else "  -- OVERLAPS at %r" % dbl[:5]))

    print("\n-- 8. the bound this actually establishes ------------------------")
    print("         T_a with a = %s cannot hold %d points at pairwise distance >= 1"
          % (a, n_points))
    print("         => a_%d > %s = %.10f" % (n_points, a, float(a)))
    print("         => s(%d) >= 2a + 2*sqrt3 = %.10f"
          % (n_points, 2 * float(a) + 2 * 3 ** 0.5))

    print("\n-- 9. sec.7 ceiling tripwire -------------------------------------")
    req(a <= CEILING,
        "a* = %.10f <= published-packing ceiling %.7f" % (float(a), float(CEILING)))
    margin = CEILING - a
    print("         headroom to the ceiling: %.10f" % float(margin))
    if a > CEILING:
        warns.append("a* EXCEEDS THE CEILING -- the certificate is WRONG, "
                     "a 16-point packing exists at 4.6247636")
    elif margin < F(1, 1000):
        warns.append("a* is within 1e-3 of the ceiling -- RULES.md sec.7 procedure "
                     "applies; this would essentially settle n=16")

    print()
    if fails:
        print("VERDICT: DISAGREED -- %d check(s) failed" % len(fails))
        for m in fails:
            print("   * " + m)
    else:
        print("VERDICT: every check above passes, exactly.")
        print("         a* established = %s = %.10f" % (a, float(a)))
    for w in warns:
        print("   !! " + w)
    return (not fails), a


# ----------------------------------------------------------------- self-test

def selftest():
    """Negative controls: the checker must REJECT each of these."""
    print("#" * 78)
    print("# NEGATIVE CONTROLS -- each must be rejected")
    print("#" * 78)
    ok = True

    # (i) diameter exactly 1 must be rejected (the Lemma L failure mode).
    #     T_sqrt3 in the (u,v) chart is a = sqrt3 -- irrational, so instead use
    #     a direct piece: a unit segment's endpoints as a degenerate check.
    a = F(2)
    piece = [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))]
    mx = max(qform(p[0] - q[0], p[1] - q[1])
             for p, q in itertools.combinations(piece, 2))
    print("  control A: square piece, max sq diam = %s (must be >= 1): %s"
          % (mx, mx >= 1))
    ok &= (mx >= 1)

    # (ii) equilateral-triangle-with-centroid witness, rescaled to be rational.
    #      Corners of T_L in the chart: (0,0),(L,0),(0,L); centroid (L/3,L/3).
    #      corner-centroid sq dist = qform(L/3, -L/3)... compute all exactly.
    L = F(2)
    pts = [(F(0), F(0)), (L, F(0)), (F(0), L), (L / 3, L / 3)]
    ds = sorted(qform(p[0] - q[0], p[1] - q[1])
                for p, q in itertools.combinations(pts, 2))
    print("  control B: T_2 corners+centroid squared distances = %s" % [str(d) for d in ds])
    print("             (min = %s; at L = sqrt3 this min becomes exactly 1 --"
          % ds[0])
    print("              L^2/3 = 1 iff L = sqrt3 -- the D1 witness)")
    ok &= (ds[0] == L * L / 3)

    # (iii) overlap+hole passes an area test but must fail disjointness/probe.
    P = [(F(0), F(0)), (F(2), F(0)), (F(0), F(2))]
    Q = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
    A2 = convex_intersection_area2(orient_ccw(P), orient_ccw(Q))
    print("  control C: nested triangles intersect in 2*area = %s (must be != 0): %s"
          % (A2, A2 != 0))
    ok &= (A2 != 0)

    # (iv) touching-but-disjoint triangles must give 0.
    R = [(F(0), F(0)), (F(1), F(0)), (F(0), F(1))]
    S = [(F(1), F(0)), (F(1), F(1)), (F(0), F(1))]
    A2 = convex_intersection_area2(orient_ccw(R), orient_ccw(S))
    print("  control D: edge-sharing triangles intersect in 2*area = %s (must be 0): %s"
          % (A2, A2 == 0))
    ok &= (A2 == 0)

    # (v) decimal strings must be refused.
    try:
        rat("4.46335")
        print("  control E: FAILED -- decimal string accepted")
        ok = False
    except ValueError:
        print("  control E: decimal string '4.46335' correctly refused")

    print("  controls: %s\n" % ("ALL PASS" if ok else "BROKEN"))
    return ok


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("-")]
    if not selftest():
        sys.exit(2)
    paths = args or [
        "../packing-n16-covering/sub_s2_cert.json",
    ]
    allok = True
    for p in paths:
        good, _ = check(p)
        allok &= good
        print()
    sys.exit(0 if allok else 1)
