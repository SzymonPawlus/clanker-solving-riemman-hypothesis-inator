"""The polygon battery for issue #132.

Every fixture is exact: coordinates are rationals, or elements of Q(sqrt 3) where an angle of
exactly 60 or 30 degrees is wanted. Nothing is a decimal approximation of an intended shape --
each polygon is literally the polygon named.

Groups
------
controls     the three hand-checked shapes from the brief
convex       convex polygons, including the 60-degree boundary family
nonconvex    designed non-convex shapes, including the sub-60-good construction
random       seeded pseudorandom convex polygons (convex hulls of rational points)
"""

from __future__ import annotations

import random
from fractions import Fraction as F

from k3 import K
from geom import P, cross, psub

SQ3H = K(0, F(1, 2))    # sqrt(3)/2
SQ3 = K(0, 1)


def _reg(n_over, radius_num, radius_den=1):
    """Regular n-gon vertices for n in {3,4,6,12} only (the n whose vertices lie in Q(sqrt3))."""
    r = F(radius_num, radius_den)
    tab12 = [  # (cos, sin) for k*30 degrees, k = 0..11, as K
        (K(1), K(0)), (K(0, F(1, 2)), K(F(1, 2))), (K(F(1, 2)), K(0, F(1, 2))),
        (K(0), K(1)), (K(F(-1, 2)), K(0, F(1, 2))), (K(0, F(-1, 2)), K(F(1, 2))),
        (K(-1), K(0)), (K(0, F(-1, 2)), K(F(-1, 2))), (K(F(-1, 2)), K(0, F(-1, 2))),
        (K(0), K(-1)), (K(F(1, 2)), K(0, F(-1, 2))), (K(0, F(1, 2)), K(F(-1, 2))),
    ]
    step = 12 // n_over
    return [(K(r) * c, K(r) * s) for c, s in tab12[::step]]


def _iso(t: F):
    """Isoceles triangle O=(0,0), A=(1,0), B on the unit circle at angle 2*arctan(t).
    Rational for rational t via the tangent half-angle parametrisation. |OA| = |OB| = 1, so the
    interior angle at O is exactly 2*arctan(t); 2*arctan(1/sqrt3) = 60 degrees."""
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    return [P(0, 0), P(1, 0), P(c, s)]


def _cstrip(w=F(2), h=F(2), m=F(10), side=F(14)):
    """A 'C'-shaped strip (three sides of a square frame) whose free end tapers to a sharp
    point at the origin. The interior angle at the origin is arctan(h/m), which can be made
    arbitrarily small, yet the far arm of the C sits at a wide angle as seen from the origin.
    Designed so that Q = (2(side-w)/sqrt3, 0) on the bottom outer edge has
    rho_{+60}(Q) = ((side-w)/sqrt3, side-w) on the TOP INNER edge."""
    return [P(0, 0), P(side, 0), P(side, side), P(0, side), P(0, side - w),
            P(side - w, side - w), P(side - w, h), P(m, h)]


def _hull(pts):
    """Exact strictly-convex hull (Andrew monotone chain), collinear points dropped."""
    pts = sorted(set(pts), key=lambda p: (p[0].a, p[0].b, p[1].a, p[1].b))
    if len(pts) < 3:
        return []

    def build(seq):
        st = []
        for p in seq:
            while len(st) >= 2 and cross(psub(st[-1], st[-2]), psub(p, st[-2])).sign() <= 0:
                st.pop()
            st.append(p)
        return st

    lower = build(pts)
    upper = build(list(reversed(pts)))
    h = lower[:-1] + upper[:-1]
    return h if len(h) >= 3 else []


def random_convex(seed: int, count: int, max_pts: int = 9):
    """Seeded pseudorandom convex polygons with rational vertices. A random rational squash
    (x, y) -> (x, y/k) is applied half the time: it preserves convexity and manufactures very
    sharp and very flat vertices, which is where the 60-degree characterisation is stressed."""
    rng = random.Random(seed)
    out = []
    tries = 0
    while len(out) < count and tries < count * 40:
        tries += 1
        npts = rng.randint(3, max_pts)
        pts = []
        for _ in range(npts):
            den = rng.randint(1, 8)
            pts.append(P(F(rng.randint(-60, 60), den), F(rng.randint(-60, 60), den)))
        h = _hull(pts)
        if not h:
            continue
        if rng.random() < 0.5:
            k = F(rng.randint(2, 30))
            h = [(p[0], p[1] / K(k)) for p in h]
            h = _hull(h)
            if not h:
                continue
        out.append({"name": f"rand-convex-{len(out):03d}", "poly": h,
                    "expect_convex": True, "group": "random"})
    return out


def battery():
    fx = []

    # ---------------------------------------------------------------- controls
    fx.append({"name": "ctl-equilateral", "group": "controls", "expect_convex": True,
               "note": "the curve IS an equilateral triangle; every vertex must be good",
               "poly": [P(0, 0), P(1, 0), (K(F(1, 2)), SQ3H)]})
    fx.append({"name": "ctl-tri-30-30-120", "group": "controls", "expect_convex": True,
               "note": "brief's prediction: the two 30-degree apexes are NOT good, the 120 is",
               "poly": [P(-1, 0), P(1, 0), (K(0), K(0, F(1, 3)))]})
    fx.append({"name": "ctl-unit-square", "group": "controls", "expect_convex": True,
               "note": "all four interior angles 90 > 60, so all corners should be good",
               "poly": [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]})

    # ---------------------------------------------------------------- convex, exact angles
    fx.append({"name": "cvx-hexagon", "group": "convex", "expect_convex": True,
               "poly": _reg(6, 1)})
    fx.append({"name": "cvx-12gon", "group": "convex", "expect_convex": True,
               "poly": _reg(12, 1)})
    fx.append({"name": "cvx-60deg-scalene", "group": "convex", "expect_convex": True,
               "note": "interior angle at (0,0) is EXACTLY 60 but the triangle is not equilateral",
               "poly": [P(0, 0), P(2, 0), (K(F(1, 2)), SQ3H)]})
    fx.append({"name": "cvx-60deg-kite", "group": "convex", "expect_convex": True,
               "note": "exactly-60 vertex at the origin of a quadrilateral",
               "poly": [P(0, 0), P(3, 0), P(2, 2), (K(F(1, 2)), SQ3H)]})
    fx.append({"name": "cvx-square-10x1", "group": "convex", "expect_convex": True,
               "poly": [P(0, 0), P(10, 0), P(10, 1), P(0, 1)]})
    fx.append({"name": "cvx-square-1000x1", "group": "convex", "expect_convex": True,
               "poly": [P(0, 0), P(1000, 0), P(1000, 1), P(0, 1)]})
    fx.append({"name": "cvx-right-tri-1-eps", "group": "convex", "expect_convex": True,
               "note": "right angle at O but an extremely thin triangle",
               "poly": [P(0, 0), P(1, 0), P(0, F(1, 1000))]})
    fx.append({"name": "cvx-sliver-tri", "group": "convex", "expect_convex": True,
               "note": "two sub-60 vertices; the maximum a convex polygon can have if the "
                       "exterior-angle argument is right",
               "poly": [P(0, 0), P(100, 0), P(50, 1)]})
    fx.append({"name": "cvx-sliver-tri-thin", "group": "convex", "expect_convex": True,
               "poly": [P(0, 0), P(1000, 0), P(500, 1)]})
    fx.append({"name": "cvx-pentagon-irreg", "group": "convex", "expect_convex": True,
               "poly": [P(0, 0), P(7, 1), P(9, 6), P(4, 9), P(-1, 4)]})
    fx.append({"name": "cvx-obtuse-tri", "group": "convex", "expect_convex": True,
               "poly": [P(0, 0), P(10, 0), P(9, 1)]})

    # 60-degree boundary family: interior angle at O is exactly 2*arctan(t).
    # tan(30 deg) = 0.5773502691896258...
    # tan(30 deg) = 0.57735026918962576450914878050196...
    for t in ["1/2", "5/9", "57/100", "577/1000", "5773/10000", "57735/100000",
              "577350/1000000", "5773502/10000000",
              "5773502691896257/10000000000000000",
              "5773502691896258/10000000000000000",
              "5773503/10000000", "577351/1000000", "57736/100000", "5774/10000",
              "578/1000", "3/5", "7/10", "1"]:
        tt = F(t)
        fx.append({"name": f"cvx-iso-t{t.replace('/', '_')}", "group": "convex-boundary",
                   "expect_convex": True, "t": t,
                   "note": "apex angle 2*arctan(t) at the origin; 60 deg <=> t = 1/sqrt3",
                   "poly": _iso(tt)})

    # ---------------------------------------------------------------- non-convex
    fx.append({"name": "ncv-L", "group": "nonconvex", "expect_convex": False,
               "poly": [P(0, 0), P(2, 0), P(2, 1), P(1, 1), P(1, 2), P(0, 2)]})
    fx.append({"name": "ncv-dart", "group": "nonconvex", "expect_convex": False,
               "note": "sharp vertex at O, but the WHOLE curve lies in an 11-degree cone at O, "
                       "so O should still not be good: non-convexity alone is not enough",
               "poly": [P(0, 0), P(10, 1), P(5, F(1, 5)), P(10, -1)]})
    fx.append({"name": "ncv-star6", "group": "nonconvex", "expect_convex": False,
               "note": "Star of David outline; alternating radius 2 and 1",
               "poly": [v for k in range(6) for v in
                        (_reg(6, 2)[k], (_reg(12, 1)[2 * k + 1][0], _reg(12, 1)[2 * k + 1][1]))]})
    for h, m in [(F(2), F(10)), (F(1), F(10)), (F(1, 2), F(10)), (F(1, 4), F(10)),
                 (F(1, 20), F(10))]:
        nm = f"ncv-cstrip-h{h.numerator}_{h.denominator}"
        fx.append({"name": nm, "group": "nonconvex-cstrip", "expect_convex": False,
                   "note": f"C-strip with taper angle arctan({h}/{m}) at the origin",
                   "poly": _cstrip(h=h, m=m)})

    # ---------------------------------------------------------------- random convex
    fx.extend(random_convex(seed=20260829, count=150))
    return fx
