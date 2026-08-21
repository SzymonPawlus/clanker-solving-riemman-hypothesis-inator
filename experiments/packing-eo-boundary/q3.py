"""Exact arithmetic in Q(sqrt 3), written for this experiment only.

Every coordinate that occurs here -- triangular-lattice points, the corners of an
equilateral triangle with rational side, points on its sides -- lies in Q(sqrt 3).
Areas, orientation determinants and squared distances are polynomial in the
coordinates, so they stay in the field and are computed with no error at all.
Sign decisions are exact and terminating because 1 and sqrt3 are linearly
independent over Q.

Deliberately independent of `experiments/packing-oler-slack/exact.py`: two
checkers that share a number type share its bugs.
"""

from fractions import Fraction as F


class Q3:
    """p + q*sqrt(3) with p, q rational."""

    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = F(p)
        self.q = F(q)

    # -- construction ------------------------------------------------------
    @staticmethod
    def of(x):
        return x if isinstance(x, Q3) else Q3(x, 0)

    # -- ring operations ---------------------------------------------------
    def __add__(self, o):
        o = Q3.of(o)
        return Q3(self.p + o.p, self.q + o.q)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.p, -self.q)

    def __sub__(self, o):
        return self + (-Q3.of(o))

    def __rsub__(self, o):
        return Q3.of(o) + (-self)

    def __mul__(self, o):
        o = Q3.of(o)
        return Q3(self.p * o.p + 3 * self.q * o.q, self.p * o.q + self.q * o.p)

    __rmul__ = __mul__

    def inverse(self):
        d = self.p * self.p - 3 * self.q * self.q
        if d == 0:
            raise ZeroDivisionError("zero in Q(sqrt3)")
        return Q3(self.p / d, -self.q / d)

    def __truediv__(self, o):
        return self * Q3.of(o).inverse()

    def __rtruediv__(self, o):
        return Q3.of(o) * self.inverse()

    # -- exact sign --------------------------------------------------------
    def sign(self):
        """-1, 0 or +1.  Exact: p + q*sqrt3 = 0 iff p = q = 0."""
        p, q = self.p, self.q
        if p == 0 and q == 0:
            return 0
        if p == 0:
            return 1 if q > 0 else -1
        if q == 0:
            return 1 if p > 0 else -1
        if p > 0 and q > 0:
            return 1
        if p < 0 and q < 0:
            return -1
        # opposite signs: compare p^2 with 3 q^2
        c = p * p - 3 * q * q          # never 0: sqrt3 is irrational
        if p > 0:                      # p > 0 > q ; positive iff p > |q| sqrt3
            return 1 if c > 0 else -1
        return -1 if c > 0 else 1      # p < 0 < q

    def __eq__(self, o):
        return (self - Q3.of(o)).sign() == 0

    def __lt__(self, o):
        return (self - Q3.of(o)).sign() < 0

    def __le__(self, o):
        return (self - Q3.of(o)).sign() <= 0

    def __gt__(self, o):
        return (self - Q3.of(o)).sign() > 0

    def __ge__(self, o):
        return (self - Q3.of(o)).sign() >= 0

    def __hash__(self):
        return hash((self.p, self.q))

    def float(self):
        return float(self.p) + float(self.q) * 3 ** 0.5

    def __repr__(self):
        if self.q == 0:
            return f"{self.p}"
        return f"({self.p} + {self.q}*sqrt3)"


SQ3 = Q3(0, 1)          # sqrt 3
HALF_SQ3 = Q3(0, F(1, 2))


# --- planar predicates, all exact -----------------------------------------

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cross(o, a, b):
    """Orientation determinant of (a-o, b-o); exact element of Q(sqrt3)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def triangle(side):
    """Equilateral triangle A=(0,0), B=(side,0), C=(side/2, side*sqrt3/2)."""
    s = Q3.of(side)
    return [(Q3(0), Q3(0)), (s, Q3(0)), (s * Q3(F(1, 2)), s * HALF_SQ3)]


def in_triangle(p, tri):
    """Closed containment, exact.  tri given counter-clockwise."""
    for i in range(3):
        if cross(tri[i], tri[(i + 1) % 3], p).sign() < 0:
            return False
    return True


def on_boundary(p, tri):
    """p lies on the closed boundary of tri (assumes in_triangle(p, tri))."""
    for i in range(3):
        if cross(tri[i], tri[(i + 1) % 3], p).sign() == 0:
            return True
    return False


def convex_hull(pts):
    """Andrew monotone chain, exact.  Returns hull vertices counter-clockwise."""
    P = sorted(set(pts), key=lambda p: (p[0].p, p[0].q, p[1].p, p[1].q))
    P = sorted(P, key=lambda p: (p[0].float(), p[1].float()))
    # exact insertion sort on the exact order, to avoid trusting the float key
    for i in range(1, len(P)):
        j = i
        while j > 0 and (P[j][0] < P[j - 1][0]
                         or (P[j][0] == P[j - 1][0] and P[j][1] < P[j - 1][1])):
            P[j], P[j - 1] = P[j - 1], P[j]
            j -= 1
    if len(P) <= 2:
        return P

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and cross(out[-2], out[-1], p).sign() <= 0:
                out.pop()
            out.append(p)
        return out

    lower = half(P)
    upper = half(reversed(P))
    return lower[:-1] + upper[:-1]


def on_segment(p, a, b):
    """p on the closed segment ab, exact."""
    if cross(a, b, p).sign() != 0:
        return False
    return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def hull_boundary_count(pts):
    """Number of points of `pts` lying on the boundary of conv(pts)."""
    hull = convex_hull(pts)
    if len(hull) < 3:
        return len(pts)
    cnt = 0
    for p in pts:
        for i in range(len(hull)):
            if on_segment(p, hull[i], hull[(i + 1) % len(hull)]):
                cnt += 1
                break
    return cnt


def polygon_area2(poly):
    """Twice the signed area of a polygon, exact."""
    s = Q3(0)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s = s + (a[0] * b[1] - b[0] * a[1])
    return s


def min_sep2(pts):
    m = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = dist2(pts[i], pts[j])
            if m is None or d < m:
                m = d
    return m
