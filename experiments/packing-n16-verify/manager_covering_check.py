"""Independent check of the 15-piece covering certificate for T_a, written by the
manager from the problem statement, without using the author's `certify.py`.

The claim under test: T_a for a = 89267/20000 is covered by 15 convex polygons,
each of squared diameter STRICTLY below 1.  If it holds, then 16 points at
pairwise distance >= 1 cannot fit in T_a (two would share a piece), so

    a_16 >= 89267/20000 = 4.46335,

improving the repo's current best lower bound of 5*sqrt3/2 = 4.330127 (Lemma L).

Coordinates are in the triangular basis e1 = (1,0), e2 = (1/2, sqrt3/2), where
|u e1 + v e2|^2 = u^2 + uv + v^2 is RATIONAL and T_a = {u >= 0, v >= 0, u+v <= a}.
Areas in that basis are (sqrt3/2) times the uv-shoelace area, so comparing a sum
of areas against the whole triangle needs no irrationals either.  Every decision
below is an exact Fraction comparison.

ONE STEP IS CHECKED HERE THAT THE CERTIFICATE'S OWN REASONING ASSUMES.  Its
docstring argues: faces are inside T_a, and their areas sum to |T_a|, therefore
they cover T_a.  That inference needs the interiors to be pairwise disjoint --
without it, an overlap plus a hole of equal area passes the area test while
leaving T_a uncovered.  The construction is described as a "fixed planar
subdivision", but disjointness is assumed rather than verified.  So this script
verifies it explicitly, by exact convex-polygon intersection.
"""

import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, "..", "packing-n16-covering", "sub_s2_cert.json")


def q(s):
    return F(s)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def shoelace2(poly):
    """Twice the signed uv-area."""
    t = F(0)
    for i, p in enumerate(poly):
        r = poly[(i + 1) % len(poly)]
        t += p[0] * r[1] - r[0] * p[1]
    return t


def sqdist(p, r):
    du, dv = p[0] - r[0], p[1] - r[1]
    return du * du + du * dv + dv * dv          # the triangular-basis metric


def is_convex_simple(poly):
    """All turns strictly the same sign => simple and strictly convex."""
    n = len(poly)
    if n < 3:
        return False
    signs = set()
    for i in range(n):
        c = cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n])
        if c == 0:
            return False                         # collinear vertex: reject, be strict
        signs.add(c > 0)
    return len(signs) == 1


def ccw(poly):
    return poly if shoelace2(poly) > 0 else poly[::-1]


def clip(subject, clipper):
    """Sutherland-Hodgman, exact. Both CCW convex. Returns their intersection."""
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


def main():
    with open(CERT) as fh:
        cert = json.load(fh)

    a = F(int(cert["a"][0]), int(cert["a"][1]))
    faces = [[(q(u), q(v)) for u, v in f] for f in cert["faces_uv"]]
    claimed_max = F(cert["max_sq_diam"])

    print(f"certificate: a = {a} = {float(a):.9f},  {len(faces)} faces")
    print(f"claimed max squared diameter = {claimed_max} = {float(claimed_max):.12f}")
    print()

    ok = True

    # 1. piece count -- 15 pieces is what bounds 16 points
    n_ok = len(faces) == 15
    print(f"[{'ok' if n_ok else 'FAIL'}] exactly 15 faces")
    ok &= n_ok

    # 2. every vertex inside T_a; each face convex => face is a subset of T_a
    inside = all(
        u >= 0 and v >= 0 and u + v <= a for f in faces for (u, v) in f
    )
    print(f"[{'ok' if inside else 'FAIL'}] every vertex satisfies u>=0, v>=0, u+v<=a")
    ok &= inside

    convex = all(is_convex_simple(f) for f in faces)
    print(f"[{'ok' if convex else 'FAIL'}] every face is a simple, strictly convex polygon")
    ok &= convex

    # 3. squared diameters STRICTLY below 1 (a convex polygon attains its
    #    diameter at a pair of vertices, so vertex pairs suffice)
    worst = max(sqdist(p, r) for f in faces for p in f for r in f)
    strict = worst < 1
    print(f"[{'ok' if strict else 'FAIL'}] max squared diameter over all faces = "
          f"{worst} = {float(worst):.12f}  (< 1 strictly: {strict})")
    print(f"       agrees with the certificate's own figure: {worst == claimed_max}")
    ok &= strict

    # 4. areas sum exactly to |T_a|
    total2 = sum(abs(shoelace2(f)) for f in faces)
    tri2 = abs(shoelace2([(F(0), F(0)), (a, F(0)), (F(0), a)]))
    area_ok = total2 == tri2
    print(f"[{'ok' if area_ok else 'FAIL'}] face areas sum exactly to area(T_a)  "
          f"({total2} vs {tri2})")
    ok &= area_ok

    # 5. THE STEP THE CERTIFICATE ASSUMES: pairwise disjoint interiors.
    #    Without this, sum(areas) == |T_a| does not imply a covering.
    cc = [ccw(f) for f in faces]
    overlaps = []
    for i in range(len(cc)):
        for j in range(i + 1, len(cc)):
            inter = clip(cc[i], cc[j])
            if len(inter) >= 3 and abs(shoelace2(inter)) != 0:
                overlaps.append((i, j, abs(shoelace2(inter))))
    disj = not overlaps
    print(f"[{'ok' if disj else 'FAIL'}] all {len(cc)*(len(cc)-1)//2} face pairs have "
          f"interior-disjoint intersection (exact convex clipping)")
    if overlaps:
        for i, j, ar in overlaps[:5]:
            print(f"       OVERLAP faces {i},{j}: twice-area {ar} = {float(ar):.10f}")
    ok &= disj

    print()
    if ok:
        print("ALL CHECKS PASS.")
        print(f"  Faces are inside T_a, pairwise interior-disjoint, and their areas")
        print(f"  sum exactly to |T_a| -- so they cover T_a with no sliver.")
        print(f"  Every face has squared diameter < 1 strictly, so it holds at most")
        print(f"  one point of a set with pairwise distances >= 1.")
        print(f"  15 faces => at most 15 such points => 16 do not fit.")
        print()
        print(f"  THEREFORE  a_16 >= {a} = {float(a):.9f}")
        print(f"  previous best (Lemma L, 5*sqrt3/2)     = 4.330127018")
        print(f"  improvement                            = {float(a) - 4.330127018922194:+.9f}")
        print(f"  best known upper bound                 = 4.624763590")
        print(f"  open interval was [4.330127, 4.624764], now [{float(a):.6f}, 4.624764]")
        gap_before = 4.624763590 - 4.330127018922194
        gap_after = 4.624763590 - float(a)
        print(f"  fraction of the remaining gap closed   = {100*(1-gap_after/gap_before):.1f}%")
    else:
        print("CHECKS FAILED - the certificate does not establish the bound.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
