"""Exact arithmetic in Q(sqrt 3), written from scratch for verification round 2.

Elements are a + b*sqrt(3) with a, b in Q.  sqrt(3) is irrational, so a + b*r == 0
iff a == b == 0, which makes equality and sign tests exact.
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    # ---- ring ops -------------------------------------------------
    def __add__(self, o):
        o = q3(o)
        return Q3(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-q3(o))

    def __rsub__(self, o):
        return q3(o) + (-self)

    def __mul__(self, o):
        o = q3(o)
        # (a1+b1 r)(a2+b2 r) = a1a2+3b1b2 + (a1b2+a2b1) r
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + o.a * self.b)

    __rmul__ = __mul__

    def inv(self):
        # 1/(a+b r) = (a - b r)/(a^2 - 3 b^2)
        den = self.a * self.a - 3 * self.b * self.b
        if den == 0:
            raise ZeroDivisionError
        return Q3(self.a / den, -self.b / den)

    def __truediv__(self, o):
        return self * q3(o).inv()

    def __rtruediv__(self, o):
        return q3(o) * self.inv()

    # ---- comparison -----------------------------------------------
    def __eq__(self, o):
        o = q3(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def sign(self):
        """Exact sign of a + b*sqrt(3)."""
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a == 0:
            return 1 if b > 0 else -1
        if b == 0:
            return 1 if a > 0 else -1
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        # opposite signs: compare a^2 with 3 b^2, sign follows the larger term
        d = a * a - 3 * b * b
        if a > 0:  # b < 0 : positive iff a^2 > 3b^2
            return 1 if d > 0 else (-1 if d < 0 else 0)
        else:      # a < 0, b > 0 : positive iff 3b^2 > a^2
            return -1 if d > 0 else (1 if d < 0 else 0)

    def __lt__(self, o):
        return (self - q3(o)).sign() < 0

    def __le__(self, o):
        return (self - q3(o)).sign() <= 0

    def __gt__(self, o):
        return (self - q3(o)).sign() > 0

    def __ge__(self, o):
        return (self - q3(o)).sign() >= 0

    def float(self):
        return float(self.a) + float(self.b) * 3 ** 0.5

    def __repr__(self):
        return f"({self.a}+{self.b}r3={self.float():.10f})"


def q3(x):
    if isinstance(x, Q3):
        return x
    return Q3(x, 0)


R3 = Q3(0, 1)          # sqrt(3)
HALF_R3 = Q3(0, F(1, 2))


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def smul(s, p):
    return (q3(s) * p[0], q3(s) * p[1])


def d2(p, q):
    v = sub(p, q)
    return v[0] * v[0] + v[1] * v[1]


def cross(o, p, q):
    return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])


def convex_hull(pts):
    """Monotone chain, exact.  Returns hull vertices CCW, no collinear points kept."""
    P = sorted(set(pts), key=lambda p: (p[0].a, p[0].b, p[1].a, p[1].b))
    # sorting key above is lexicographic on the representation; re-sort exactly:
    P = sorted(set(pts), key=_CmpKey)
    if len(P) <= 2:
        return P
    lower = []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p).sign() <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p).sign() <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


class _CmpKey:
    __slots__ = ("p",)

    def __init__(self, p):
        self.p = p

    def __lt__(self, o):
        if self.p[0] != o.p[0]:
            return self.p[0] < o.p[0]
        return self.p[1] < o.p[1]


def shoelace2(poly):
    """Twice the signed area of a polygon (CCW positive)."""
    s = q3(0)
    m = len(poly)
    for i in range(m):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % m]
        s = s + (x1 * y2 - x2 * y1)
    return s


def on_segment(p, u, v):
    """p on closed segment uv (exact)."""
    if cross(u, v, p).sign() != 0:
        return False
    # within bounding box along the segment
    t = dot(sub(p, u), sub(v, u))
    L = dot(sub(v, u), sub(v, u))
    return t >= q3(0) and t <= L


def on_hull_boundary(p, hull):
    m = len(hull)
    if m == 1:
        return p == hull[0]
    if m == 2:
        return on_segment(p, hull[0], hull[1])
    for i in range(m):
        if on_segment(p, hull[i], hull[(i + 1) % m]):
            return True
    return False
