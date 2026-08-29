"""Hand-checked tests for the exact inscribed-equilateral-triangle decider (issue #132).

Every expected value below was computed by hand and is written out in the docstring of the
test that uses it. Run:  python3 test_iet.py
"""

from __future__ import annotations

import sys
from fractions import Fraction as F

from k3 import K, SQRT3, ONE, ZERO
from geom import (P, peq, rot60, seg_intersect, point_on_segment, point_on_polygon,
                  is_simple, is_convex, orientation, vertex_angle_class, decide_good,
                  verify_triangle, norm2, psub)

FAILS = []


def check(name, cond, extra=""):
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name} {extra}")
        FAILS.append(name)


# ---------------------------------------------------------------- 1. field arithmetic
def test_field():
    """sqrt3 = 1.7320508075688772...  so 1732/1000 < sqrt3 < 17321/10000, and
    (2-sqrt3)^2 = 7-4sqrt3 > 0 while 1-sqrt3 < 0."""
    print("field")
    check("sqrt3^2 == 3", SQRT3 * SQRT3 == K(3))
    check("1 - sqrt3 < 0", (ONE - SQRT3).sign() == -1)
    check("2 - sqrt3 > 0", (K(2) - SQRT3).sign() == 1)
    check("7 - 4 sqrt3 > 0", (K(7) - K(4) * SQRT3).sign() == 1)
    check("1732/1000 - sqrt3 < 0", (K(F(1732, 1000)) - SQRT3).sign() == -1)
    check("17321/10000 - sqrt3 > 0", (K(F(17321, 10000)) - SQRT3).sign() == 1)
    check("1/(2-sqrt3) == 2+sqrt3", ONE / (K(2) - SQRT3) == K(2) + SQRT3)
    check("(2-sqrt3)(2+sqrt3) == 1", (K(2) - SQRT3) * (K(2) + SQRT3) == ONE)


# ---------------------------------------------------------------- 2. rotation
def test_rotation():
    """Rotating (1,0) about the origin by +60 gives (1/2, sqrt3/2); by -60 gives
    (1/2, -sqrt3/2); twice by +60 (i.e. 120) gives (-1/2, sqrt3/2); six times gives (1,0)."""
    print("rotation")
    O = P(0, 0)
    A = P(1, 0)
    check("rot +60", peq(rot60(A, O, 1), (K(F(1, 2)), K(0, F(1, 2)))))
    check("rot -60", peq(rot60(A, O, -1), (K(F(1, 2)), K(0, F(-1, 2)))))
    check("rot +120", peq(rot60(rot60(A, O, 1), O, 1), (K(F(-1, 2)), K(0, F(1, 2)))))
    X = A
    for _ in range(6):
        X = rot60(X, O, 1)
    check("rot 6x60 == identity", peq(X, A))
    check("rotation is an isometry about O",
          norm2(psub(rot60(P(3, 5), O, 1), O)) == norm2(psub(P(3, 5), O)))
    C = P(F(7, 3), F(-2, 5))
    check("rot(-sigma) inverts rot(sigma)", peq(rot60(rot60(C, O, 1), O, -1), C))
    # off-origin centre
    Oc = P(2, -1)
    check("rot about (2,-1) fixes it", peq(rot60(Oc, Oc, 1), Oc))


# ---------------------------------------------------------------- 3. segment intersection
def test_segments():
    print("segment intersection")
    check("crossing X", seg_intersect(P(0, 0), P(2, 0), P(1, -1), P(1, 1))
          == ("point", P(1, 0)))
    r = seg_intersect(P(0, 0), P(2, 0), P(1, 0), P(3, 0))
    check("collinear overlap -> segment [(1,0),(2,0)]",
          r[0] == "segment" and peq(r[1], P(1, 0)) and peq(r[2], P(2, 0)), r)
    check("shared endpoint", seg_intersect(P(0, 0), P(1, 0), P(1, 0), P(1, 1))
          == ("point", P(1, 0)))
    check("parallel disjoint", seg_intersect(P(0, 0), P(1, 0), P(0, 1), P(1, 1))[0] == "empty")
    check("collinear disjoint", seg_intersect(P(0, 0), P(1, 0), P(2, 0), P(3, 0))[0] == "empty")
    check("collinear touching at a point",
          seg_intersect(P(0, 0), P(1, 0), P(1, 0), P(2, 0)) == ("point", P(1, 0)))
    check("lines cross outside both segments",
          seg_intersect(P(0, 0), P(1, 0), P(5, -1), P(5, 1))[0] == "empty")
    check("T junction", seg_intersect(P(0, 0), P(2, 0), P(1, 0), P(1, 5))
          == ("point", P(1, 0)))
    check("degenerate segment on a segment",
          seg_intersect(P(1, 0), P(1, 0), P(0, 0), P(2, 0)) == ("point", P(1, 0)))
    check("degenerate segment off a segment",
          seg_intersect(P(1, 1), P(1, 1), P(0, 0), P(2, 0))[0] == "empty")
    # an intersection that is irrational in the rational world but exact in K
    r = seg_intersect(P(0, 0), (K(1), K(0, 1)), P(0, 1), P(5, 1))
    check("K-valued crossing point", r[0] == "point" and r[1][1] == K(1)
          and r[1][0] == K(0, F(1, 3)) * K(1), r)


# ---------------------------------------------------------------- 4. polygon predicates
def test_polygons():
    print("polygon predicates")
    sq = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
    check("square simple", is_simple(sq)[0])
    check("square convex", is_convex(sq))
    check("square ccw", orientation(sq) == 1)
    check("square cw when reversed", orientation(list(reversed(sq))) == -1)
    bow = [P(0, 0), P(1, 1), P(1, 0), P(0, 1)]
    check("bowtie not simple", not is_simple(bow)[0])
    ell = [P(0, 0), P(2, 0), P(2, 1), P(1, 1), P(1, 2), P(0, 2)]
    check("L-shape simple", is_simple(ell)[0])
    check("L-shape not convex", not is_convex(ell))
    check("L-shape reflex at (1,1)", vertex_angle_class(ell, 3)["reflex"])
    check("L reflex interior angle 270", abs(vertex_angle_class(ell, 3)["degrees_display"] - 270) < 1e-9)
    check("square corner angle 90 > 60", vertex_angle_class(sq, 0)["cmp60"] == 1)

    eq = [P(0, 0), P(1, 0), (K(F(1, 2)), K(0, F(1, 2)))]
    check("equilateral triangle simple+convex", is_simple(eq)[0] and is_convex(eq))
    for i in range(3):
        check(f"equilateral vertex {i} has interior angle exactly 60",
              vertex_angle_class(eq, i)["cmp60"] == 0)

    # 30-30-120 triangle: base (-1,0),(1,0), apex (0, 1/sqrt3) = (0, sqrt3/3)
    t = [P(-1, 0), P(1, 0), (K(0), K(0, F(1, 3)))]
    check("30-30-120 simple+convex", is_simple(t)[0] and is_convex(t))
    check("30-apex (-1,0) < 60", vertex_angle_class(t, 0)["cmp60"] == -1)
    check("30-apex (1,0) < 60", vertex_angle_class(t, 1)["cmp60"] == -1)
    check("120-apex > 60", vertex_angle_class(t, 2)["cmp60"] == 1)
    check("30 degrees displayed", abs(vertex_angle_class(t, 0)["degrees_display"] - 30) < 1e-9)
    check("120 degrees displayed", abs(vertex_angle_class(t, 2)["degrees_display"] - 120) < 1e-9)


# ---------------------------------------------------------------- 5. the controls
def test_controls():
    print("controls")
    # (a) equilateral triangle: every vertex trivially good, the curve IS the triangle
    eq = [P(0, 0), P(1, 0), (K(F(1, 2)), K(0, F(1, 2)))]
    for i in range(3):
        r = decide_good(eq, eq[i])
        check(f"equilateral vertex {i} good", r["good"] and r["verified_ok"], r)
        check(f"equilateral vertex {i} side^2 == 1",
              r["verified"]["side_squared"] == ["1", "0"], r["verified"]["side_squared"])

    # (b) 30-30-120
    t = [P(-1, 0), P(1, 0), (K(0), K(0, F(1, 3)))]
    r0 = decide_good(t, t[0])
    r1 = decide_good(t, t[1])
    r2 = decide_good(t, t[2])
    check("30-30-120: 30-apex (-1,0) NOT good", not r0["good"], r0)
    check("30-30-120: 30-apex (1,0) NOT good", not r1["good"], r1)
    check("30-30-120: 120-apex IS good", r2["good"] and r2["verified_ok"], r2)

    # (c) unit square: all four corners good.
    sq = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
    for i in range(4):
        r = decide_good(sq, sq[i])
        check(f"square corner {i} good", r["good"] and r["verified_ok"], r)

    # Hand-computed witness at the square's corner (0,0):
    #   rho_{+60}(1, t) = (1/2 - t sqrt3/2, sqrt3/2 + t/2); its y equals 1 iff t = 2 - sqrt3,
    #   and then its x = 1/2 - (2-sqrt3)sqrt3/2 = (4 - 2sqrt3)/2 = 2 - sqrt3 in [0,1].
    #   So Q = (1, 2-sqrt3) on the right edge and X = (2-sqrt3, 1) on the top edge.
    two_m = K(2) - SQRT3
    Q = (K(1), two_m)
    X = (two_m, K(1))
    ok, det = verify_triangle(sq, P(0, 0), Q, X)
    check("hand witness in the unit square verifies", ok, det)
    check("hand witness is rho_{+60}(Q)", peq(rot60(Q, P(0, 0), 1), X))
    # side^2 = 1 + (2-sqrt3)^2 = 1 + 7 - 4sqrt3 = 8 - 4sqrt3
    check("hand witness side^2 == 8 - 4 sqrt3", det["side_squared"] == ["8", "-4"], det["side_squared"])


# ---------------------------------------------------------------- 6. the trivial-intersection trap
def test_trivial_exclusion():
    """The 30-degree apex of the 30-30-120 triangle is the sharpest test that O itself is
    excluded: rho(J) meets J there, but ONLY at O."""
    print("degenerate-intersection handling")
    t = [P(-1, 0), P(1, 0), (K(0), K(0, F(1, 3)))]
    r = decide_good(t, t[0], want_all=True)
    check("30-apex: some pairs DO intersect", r["nonempty_pairs"] > 0, r)
    check("30-apex: every intersecting pair meets only at O",
          r["nonempty_pairs"] == r["trivial_only_pairs"], r)
    check("30-apex: verdict not good", not r["good"])
    # and O is genuinely in the intersection for both senses
    for sigma in (1, -1):
        check(f"O is fixed by rho_{sigma}", peq(rot60(t[0], t[0], sigma), t[0]))


# ---------------------------------------------------------------- 7. the 60-degree boundary
def test_boundary_60():
    """The two fixtures that straddle 60 degrees by 7e-15 of a degree.

    Isoceles triangle O=(0,0), A=(1,0), B=((1-t^2)/(1+t^2), 2t/(1+t^2)); |OA| = |OB| = 1 and
    the apex angle at O is exactly 2*arctan(t), so it is < 60 iff t < tan 30 = 1/sqrt3 iff
    3t^2 < 1. For t = 5773502691896257/10^16, 3t^2 = 0.9999999999999997... < 1, so the apex is
    just under 60 and (the polygon being inside a sub-60 cone at O) O is NOT good. For
    t = 5773502691896258/10^16, 3t^2 > 1, the apex exceeds 60, and O IS good.

    sympy's own geometry gets both of these wrong; see diagnose_disagreement.py.
    """
    from fixtures import _iso
    print("60-degree boundary")
    lo = F(5773502691896257, 10 ** 16)
    hi = F(5773502691896258, 10 ** 16)
    check("3t^2 < 1 for the low t", 3 * lo * lo < 1, 3 * lo * lo)
    check("3t^2 > 1 for the high t", 3 * hi * hi > 1, 3 * hi * hi)
    plo, phi = _iso(lo), _iso(hi)
    check("low t: apex angle < 60", vertex_angle_class(plo, 0)["cmp60"] == -1)
    check("high t: apex angle > 60", vertex_angle_class(phi, 0)["cmp60"] == 1)
    check("low t: apex NOT good", not decide_good(plo, plo[0])["good"])
    check("high t: apex IS good", decide_good(phi, phi[0])["good"])
    # base angles are (180 - apex)/2, so they sit on the opposite side of 60 from the apex
    check("low t: base angles > 60", vertex_angle_class(plo, 1)["cmp60"] == 1
          and vertex_angle_class(plo, 2)["cmp60"] == 1)
    check("high t: base angles < 60", vertex_angle_class(phi, 1)["cmp60"] == -1
          and vertex_angle_class(phi, 2)["cmp60"] == -1)
    check("low t: base vertices good", decide_good(plo, plo[1])["good"]
          and decide_good(plo, plo[2])["good"])
    check("high t: base vertices NOT good", (not decide_good(phi, phi[1])["good"])
          and (not decide_good(phi, phi[2])["good"]))


def main():
    test_field()
    test_rotation()
    test_segments()
    test_polygons()
    test_controls()
    test_trivial_exclusion()
    test_boundary_60()
    print()
    if FAILS:
        print(f"{len(FAILS)} FAILURES: {FAILS}")
        return 1
    print("all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
