"""Exact geometry over Q(sqrt 3).  No floats anywhere in this module.

Used to verify, exactly:
  * a list of convex polygons is contained in the equilateral triangle T(a)
    with A=(0,0), B=(a,0), C=(a/2, a*sqrt(3)/2)   [repo convention, scaled];
  * their union covers T(a)  (exact inclusion-exclusion of areas);
  * each polygon has squared diameter <= 1 (or < 1).

Everything is decided by the exact sign of an element of Q(sqrt 3).
"""
from fractions import Fraction as F


class Q3:
    """p + q*sqrt(3), p,q rational.  Exact field arithmetic and exact sign."""
    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = F(p)
        self.q = F(q)

    def __repr__(self):
        return f"Q3({self.p},{self.q})"

    def __str__(self):
        if self.q == 0:
            return str(self.p)
        return f"{self.p}+{self.q}*sqrt3"

    @staticmethod
    def _c(o):
        return o if isinstance(o, Q3) else Q3(o)

    def __add__(self, o):
        o = Q3._c(o); return Q3(self.p + o.p, self.q + o.q)
    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.p, -self.q)

    def __sub__(self, o):
        return self + (-Q3._c(o))

    def __rsub__(self, o):
        return Q3._c(o) + (-self)

    def __mul__(self, o):
        o = Q3._c(o)
        return Q3(self.p * o.p + 3 * self.q * o.q, self.p * o.q + self.q * o.p)
    __rmul__ = __mul__

    def inv(self):
        den = self.p * self.p - 3 * self.q * self.q
        if den == 0:
            raise ZeroDivisionError("Q3 zero")
        return Q3(self.p / den, -self.q / den)

    def __truediv__(self, o):
        return self * Q3._c(o).inv()

    def __rtruediv__(self, o):
        return Q3._c(o) * self.inv()

    def sign(self):
        p, q = self.p, self.q
        if p == 0 and q == 0:
            return 0
        if p >= 0 and q >= 0:
            return 1
        if p <= 0 and q <= 0:
            return -1
        # opposite signs: compare p^2 with 3 q^2 (sqrt3 irrational => never equal
        # unless p=q=0, already handled)
        d = p * p - 3 * q * q
        if p > 0:          # p>0, q<0  -> positive iff p^2 > 3q^2
            return 1 if d > 0 else -1
        else:              # p<0, q>0  -> positive iff 3q^2 > p^2
            return -1 if d > 0 else 1

    def __eq__(self, o):
        return (self - Q3._c(o)).sign() == 0

    def __hash__(self):
        return hash((self.p, self.q))

    def __lt__(self, o):
        return (self - Q3._c(o)).sign() < 0

    def __le__(self, o):
        return (self - Q3._c(o)).sign() <= 0

    def __gt__(self, o):
        return (self - Q3._c(o)).sign() > 0

    def __ge__(self, o):
        return (self - Q3._c(o)).sign() >= 0

    def to_float(self):
        return float(self.p) + float(self.q) * 1.7320508075688772


SQRT3 = Q3(0, 1)
ZERO = Q3(0)
ONE = Q3(1)


# ---------------------------------------------------------------- points
def pt(x, y):
    return (x if isinstance(x, Q3) else Q3(x), y if isinstance(y, Q3) else Q3(y))


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def sq_dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


# ---------------------------------------------------------------- polygons
def shoelace2(poly):
    """Twice the signed area (positive if CCW)."""
    s = ZERO
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s = s + (x1 * y2 - x2 * y1)
    return s


def area(poly):
    if len(poly) < 3:
        return ZERO
    s = shoelace2(poly)
    return s * Q3(F(1, 2)) if s.sign() >= 0 else s * Q3(F(-1, 2))


def is_ccw(poly):
    return shoelace2(poly).sign() > 0


def is_convex(poly):
    """Strictly-or-weakly convex, consistently oriented, no repeated points."""
    n = len(poly)
    if n < 3:
        return False
    for i in range(n):
        if sq_dist(poly[i], poly[(i + 1) % n]).sign() == 0:
            return False
    sgn = 0
    for i in range(n):
        c = cross(poly[i], poly[(i + 1) % n], poly[(i + 2) % n]).sign()
        if c == 0:
            continue
        if sgn == 0:
            sgn = c
        elif c != sgn:
            return False
    return sgn != 0


def dedup(poly):
    out = []
    for p in poly:
        if not out or sq_dist(out[-1], p).sign() != 0:
            out.append(p)
    while len(out) > 1 and sq_dist(out[0], out[-1]).sign() == 0:
        out.pop()
    return out


def clip_halfplane(poly, a, b):
    """Sutherland-Hodgman: keep the part of `poly` left of directed line a->b."""
    if not poly:
        return []
    out = []
    n = len(poly)
    for i in range(n):
        cur = poly[i]
        nxt = poly[(i + 1) % n]
        sc = cross(a, b, cur).sign()
        sn = cross(a, b, nxt).sign()
        if sc >= 0:
            out.append(cur)
        if (sc > 0 and sn < 0) or (sc < 0 and sn > 0):
            # segment crosses the line: exact intersection
            d1 = cross(a, b, cur)
            d2 = cross(a, b, nxt)
            t = d1 / (d1 - d2)
            ix = cur[0] + (nxt[0] - cur[0]) * t
            iy = cur[1] + (nxt[1] - cur[1]) * t
            out.append((ix, iy))
    return dedup(out)


def convex_intersect(p, q):
    """Intersection of two convex polygons, both given CCW."""
    res = p
    n = len(q)
    for i in range(n):
        res = clip_halfplane(res, q[i], q[(i + 1) % n])
        if len(res) < 3:
            return []
    return res


def poly_diam_sq(poly):
    """Squared diameter of a convex polygon = max squared distance of vertices."""
    best = ZERO
    for i in range(len(poly)):
        for j in range(i + 1, len(poly)):
            d = sq_dist(poly[i], poly[j])
            if d > best:
                best = d
    return best


def union_area_incl_excl(polys):
    """Exact area of the union, by inclusion-exclusion over all 2^m - 1 subsets.

    Every pairwise/triple/... intersection of convex polygons is convex, so each
    term is computed by iterated exact half-plane clipping.  Exact, no sampling.
    """
    m = len(polys)
    total = ZERO
    # iterate subsets in an order that lets us reuse the running intersection
    def rec(idx, cur, cnt):
        nonlocal total
        if cnt > 0:
            a = area(cur)
            total = total + (a if cnt % 2 == 1 else -a)
        for j in range(idx, m):
            nxt = convex_intersect(cur, polys[j]) if cnt > 0 else polys[j]
            if len(nxt) >= 3:
                rec(j + 1, nxt, cnt + 1)
    rec(0, None, 0)
    return total


def triangle(a):
    """T(a):  A=(0,0), B=(a,0), C=(a/2, a*sqrt(3)/2).  CCW."""
    a = a if isinstance(a, Q3) else Q3(a)
    return [pt(ZERO, ZERO), pt(a, ZERO), (a * Q3(F(1, 2)), a * Q3(0, F(1, 2)))]


def contains(convex_poly, p):
    """Closed containment in a CCW convex polygon."""
    n = len(convex_poly)
    for i in range(n):
        if cross(convex_poly[i], convex_poly[(i + 1) % n], p).sign() < 0:
            return False
    return True


def verify_cover(a, pieces, strict=False):
    """Exact verification that `pieces` cover T(a) with squared diameter <= 1
    (or < 1 if strict).  Returns (ok, report dict)."""
    T = triangle(a)
    rep = {}
    ok = True
    norm = []
    for k, P in enumerate(pieces):
        P = dedup(list(P))
        if not is_convex(P):
            rep[f"piece{k}_convex"] = False
            ok = False
            continue
        if not is_ccw(P):
            P = P[::-1]
        norm.append(P)
        inside = all(contains(T, v) for v in P)
        rep[f"piece{k}_in_T"] = inside
        ok = ok and inside
        d2 = poly_diam_sq(P)
        good = (d2 < ONE) if strict else (d2 <= ONE)
        rep[f"piece{k}_diam2"] = str(d2)
        rep[f"piece{k}_diam_ok"] = good
        ok = ok and good
    if len(norm) == len(pieces):
        ua = union_area_incl_excl(norm)
        ta = area(T)
        rep["union_area"] = str(ua)
        rep["T_area"] = str(ta)
        cov = (ua - ta).sign() == 0
        rep["covers"] = cov
        ok = ok and cov
    rep["OK"] = ok
    return ok, rep
