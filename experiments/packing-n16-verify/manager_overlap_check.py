"""Manager's independent check of an OVERLAPPING 15-piece covering certificate.

The author proves coverage by exact polygon difference (T_a minus the union is
empty).  This script proves it a different way, so that a bug in one method does
not hide a bug in the other:

    if no three pieces share area, then by inclusion-exclusion
        |union| = sum |P_i| - sum_{i<j} |P_i cap P_j|,
    and if that equals |T_a| while every P_i is inside T_a, the union is a closed
    subset of T_a of full measure, hence all of T_a.

Everything is exact rational arithmetic in the triangular basis e1=(1,0),
e2=(1/2,sqrt3/2), where |u e1 + v e2|^2 = u^2 + uv + v^2 is rational and
T_a = {u,v >= 0, u+v <= a}.  Intersections of convex polygons are computed by
exact Sutherland-Hodgman clipping, so every area is a Fraction.

The bound: a piece set of maximum diameter D < 1 covering T_a proves
a_16 >= a/D, since dilating by mu < 1/D keeps every diameter strictly below 1.
"""

import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, "..", "packing-n16-shapes", "best_ref_cert.json")


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def shoelace2(poly):
    t = F(0)
    for i, p in enumerate(poly):
        r = poly[(i + 1) % len(poly)]
        t += p[0] * r[1] - r[0] * p[1]
    return t


def ccw(poly):
    return poly if shoelace2(poly) > 0 else poly[::-1]


def sqdist(p, r):
    du, dv = p[0] - r[0], p[1] - r[1]
    return du * du + du * dv + dv * dv


def diam2(poly):
    return max(sqdist(p, r) for p in poly for r in poly)


def is_convex(poly):
    n = len(poly)
    if n < 3:
        return False
    s = set()
    for i in range(n):
        c = cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n])
        if c == 0:
            return False
        s.add(c > 0)
    return len(s) == 1


def clip(subject, clipper):
    """Exact convex-convex intersection (both ccw)."""
    out = list(subject)
    n = len(clipper)
    for i in range(n):
        if not out:
            return []
        a, b = clipper[i], clipper[(i + 1) % n]
        new, m = [], len(out)
        for j in range(m):
            p, r = out[j], out[(j + 1) % m]
            sp, sr = cross(a, b, p), cross(a, b, r)
            if sp >= 0:
                new.append(p)
            if (sp > 0 and sr < 0) or (sp < 0 and sr > 0):
                t = F(sp, sp - sr)
                new.append((p[0] + t * (r[0] - p[0]), p[1] + t * (r[1] - p[1])))
        out = new
    return out


def area2(poly):
    return abs(shoelace2(poly)) if len(poly) >= 3 else F(0)


def isqrt_frac(x):
    """Exact square root of a Fraction if it is a perfect square, else None."""
    import math
    n, d = x.numerator, x.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    return F(rn, rd) if rn * rn == n and rd * rd == d else None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    c = json.load(open(path))
    a = F(int(c["a"][0]), int(c["a"][1]))
    P = [ccw([(F(p[0]), F(p[1])) for p in poly]) for poly in c["pieces_uv"]]
    claimed_S = F(c["max_sq_diam"])
    claimed_star = F(c["a_star_rational_lower_bound"])

    print(f"certificate : {os.path.basename(path)}")
    print(f"a           = {a} = {float(a):.9f}")
    print(f"pieces      = {len(P)}")
    ok = True

    def chk(name, cond, extra=""):
        nonlocal ok
        ok = ok and bool(cond)
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")

    chk("exactly 15 pieces", len(P) == 15)
    chk("every piece simple and strictly convex", all(is_convex(q) for q in P))
    chk("every vertex in T_a", all(p[0] >= 0 and p[1] >= 0 and p[0] + p[1] <= a
                                   for q in P for p in q))

    S = max(diam2(q) for q in P)
    chk("max squared diameter < 1 STRICTLY", S < 1,
        f"\n         S = {S} = {float(S):.12f}")
    chk("agrees with the certificate's own figure", S == claimed_S)

    # --- coverage, by inclusion-exclusion (independent of the author's method)
    pairs = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            inter = clip(P[i], P[j])
            if area2(inter) != 0:
                pairs.append((i, j, area2(inter)))
    print(f"  ..    overlapping pairs: {len(pairs)} of {len(P)*(len(P)-1)//2}"
          f"  (a partition would have 0)")

    triples = 0
    involved = sorted({i for i, j, _ in pairs} | {j for i, j, _ in pairs})
    for x in range(len(involved)):
        for y in range(x + 1, len(involved)):
            for z in range(y + 1, len(involved)):
                i, j, k = involved[x], involved[y], involved[z]
                t = clip(clip(P[i], P[j]), P[k])
                if area2(t) != 0:
                    triples += 1
    chk("no three pieces share area (so inclusion-exclusion truncates)", triples == 0,
        f"({triples} triple overlaps)")

    union2 = sum(area2(q) for q in P) - sum(ar for _, _, ar in pairs)
    tri2 = area2([(F(0), F(0)), (a, F(0)), (F(0), a)])
    chk("|union| == |T_a| exactly, so the pieces cover T_a", union2 == tri2,
        f"\n         union {union2}  vs  T_a {tri2}")

    overlap2 = sum(ar for _, _, ar in pairs)
    print(f"  ..    total overlap area (uv-shoelace x2) = {overlap2} "
          f"= {float(overlap2):.9f}")

    # --- the bound
    D = isqrt_frac(S)
    print()
    if D is None:
        print(f"  max squared diameter is not a perfect rational square;")
        print(f"  bounding a/sqrt(S) from below by rational arithmetic instead.")
        lo = claimed_star
        chk("claimed a* satisfies (a*)^2 * S <= a^2", lo * lo * S <= a * a)
        astar = lo
    else:
        astar = a / D
        print(f"  max diameter = sqrt(S) = {D} exactly")
        chk("claimed a* does not exceed a/diam_max", claimed_star <= astar)

    if ok:
        import math
        prev = F(446335, 99998)
        print()
        print("ALL CHECKS PASS.")
        print(f"  a_16 >= {astar} = {float(astar):.12f}")
        print(f"  previous certified record      = {float(prev):.12f}")
        print(f"  gain                           = {float(astar - prev):+.3e}")
        print(f"  s(16) >= 2*a_16 + 2*sqrt3      = {2*float(astar)+2*math.sqrt(3):.9f}")
        print(f"  ceiling (published packing)    = 4.624763590  -> headroom "
              f"{4.624763590-float(astar):.9f}")
        return 0
    print("\nCHECKS FAILED - the certificate does not establish the bound.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
