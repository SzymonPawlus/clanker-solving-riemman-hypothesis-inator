"""Exact arithmetic for the Erdos-Oler verification pass.

Written independently for `attacks/eo-verification/`.  The only thing borrowed
from elsewhere in the repo is the idea of `sqrt_bounds` (rational enclosure of a
square root via `math.isqrt`), read from `experiments/packing-oler-slack/exact.py`
as the task permitted.  The geometry, the number type and every check are mine.

Number type
-----------
`Surd` is a finite formal sum  sum_f  c_f * sqrt(f)  with c_f rational and f a
squarefree positive integer (f = 1 is the rational part).  Distinct square roots
of squarefree integers are linearly independent over Q, so two `Surd`s are equal
iff their coefficient dictionaries agree -- equality is decided exactly, with no
tolerance anywhere.  Order comparisons fall back to interval evaluation with
escalating precision, which terminates because a nonzero `Surd` is bounded away
from zero.

`Surd` is closed under +, -, and multiplication by a rational.  It is NOT closed
under multiplication of two general surds, which is fine: every quantity used
here (Oler's bound, areas, perimeters, deficits) is a rational combination of
sqrt(rational)s.

Coordinates
-----------
All geometry is done in *lattice coordinates* (u, v), mapped to the plane by

    (u, v)  |-->  (u + v/2,  v * sqrt(3)/2).

The image of the unit lattice square-basis is the unit triangular lattice, and

  * squared distance   = du^2 + du*dv + dv^2          (rational)
  * planar area        = (sqrt(3)/2) * shoelace(u,v)  so that Oler's area term
    (2/sqrt3)*A  is exactly the rational number shoelace(u,v).

So Oler's bound  B(P) = (2/sqrt3)A(P) + M(P)/2 + 1  is a `Surd` whose rational
part is shoelace + 1 and whose irrational part comes only from edge lengths.

The equilateral triangle of side a is  T_a = conv{(0,0), (a,0), (0,a)}  in these
coordinates.
"""

from fractions import Fraction as F
from math import isqrt

# --------------------------------------------------------------------------
# squarefree reduction
# --------------------------------------------------------------------------


def _squarefree(n: int):
    """Write positive integer n = s^2 * f with f squarefree.  Returns (s, f)."""
    assert n > 0
    s, f = 1, 1
    d = 2
    m = n
    while d * d <= m:
        e = 0
        while m % d == 0:
            m //= d
            e += 1
        if e:
            s *= d ** (e // 2)
            if e % 2:
                f *= d
        d += 1 if d == 2 else 2
    if m > 1:
        f *= m
    return s, f


def sqrt_of(q: F):
    """sqrt(q) for a non-negative rational q, as (coefficient, squarefree part).

    sqrt(p/r) = sqrt(p*r)/r, so reduce the integer p*r.
    """
    q = F(q)
    if q < 0:
        raise ValueError("negative radicand")
    if q == 0:
        return F(0), 1
    p, r = q.numerator, q.denominator
    s, f = _squarefree(p * r)
    return F(s, r), f


def sqrt_bounds(q: F, prec: int = 80):
    """Rational lo <= sqrt(q) <= hi.  (Idea taken from packing-oler-slack/exact.py.)"""
    q = F(q)
    if q < 0:
        raise ValueError("negative radicand")
    if q == 0:
        return F(0), F(0)
    num, den = q.numerator, q.denominator
    scale = 10 ** prec
    root = isqrt(num * den * scale * scale)
    if root * root == num * den * scale * scale:
        return F(root, den * scale), F(root, den * scale)
    return F(root, den * scale), F(root + 1, den * scale)


# --------------------------------------------------------------------------
# Surd
# --------------------------------------------------------------------------


class Surd:
    """sum_f c_f sqrt(f), f squarefree positive integers, c_f in Q."""

    __slots__ = ("c",)

    def __init__(self, arg=0):
        if isinstance(arg, Surd):
            self.c = dict(arg.c)
        elif isinstance(arg, dict):
            self.c = {f: F(v) for f, v in arg.items() if v != 0}
        else:
            v = F(arg)
            self.c = {1: v} if v != 0 else {}

    @staticmethod
    def root(q):
        """sqrt(q) as a Surd, q a non-negative rational."""
        coeff, f = sqrt_of(F(q))
        return Surd({f: coeff})

    def __add__(self, other):
        other = other if isinstance(other, Surd) else Surd(other)
        d = dict(self.c)
        for f, v in other.c.items():
            d[f] = d.get(f, F(0)) + v
        return Surd(d)

    __radd__ = __add__

    def __neg__(self):
        return Surd({f: -v for f, v in self.c.items()})

    def __sub__(self, other):
        return self + (-(other if isinstance(other, Surd) else Surd(other)))

    def __rsub__(self, other):
        return Surd(other) - self

    def __mul__(self, k):
        """Multiplication by a rational scalar only."""
        k = F(k)
        return Surd({f: v * k for f, v in self.c.items()})

    __rmul__ = __mul__

    def __truediv__(self, k):
        return Surd({f: v / F(k) for f, v in self.c.items()})

    def __eq__(self, other):
        other = other if isinstance(other, Surd) else Surd(other)
        return self.c == other.c

    def __hash__(self):
        return hash(tuple(sorted(self.c.items())))

    def is_rational(self):
        return all(f == 1 for f in self.c)

    def rational_value(self):
        assert self.is_rational()
        return self.c.get(1, F(0))

    def bounds(self, prec=80):
        lo = hi = F(0)
        for f, v in self.c.items():
            a, b = sqrt_bounds(F(f), prec)
            if v >= 0:
                lo += v * a
                hi += v * b
            else:
                lo += v * b
                hi += v * a
        return lo, hi

    def sign(self):
        """Exact sign: 0 iff the surd is identically zero."""
        if not self.c:
            return 0
        prec = 40
        while prec <= 2000:
            lo, hi = self.bounds(prec)
            if lo > 0:
                return 1
            if hi < 0:
                return -1
            prec *= 4
        raise RuntimeError("sign undecided -- surd is (numerically) zero but not formally")

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __le__(self, other):
        return (self - other).sign() <= 0

    def __gt__(self, other):
        return (self - other).sign() > 0

    def __ge__(self, other):
        return (self - other).sign() >= 0

    def __float__(self):
        lo, hi = self.bounds(40)
        return float((lo + hi) / 2)

    def __repr__(self):
        if not self.c:
            return "0"
        parts = []
        for f in sorted(self.c):
            v = self.c[f]
            parts.append(f"{v}" if f == 1 else f"{v}*sqrt{f}")
        return " + ".join(parts) + f"  (~{float(self):.9f})"


# --------------------------------------------------------------------------
# planar geometry in lattice coordinates
# --------------------------------------------------------------------------


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def dist2(p, q):
    du, dv = p[0] - q[0], p[1] - q[1]
    return du * du + du * dv + dv * dv


def edge_len(p, q):
    return Surd.root(dist2(p, q))


def shoelace(poly):
    """Twice-signed-area/2 in (u,v) coordinates; equals (2/sqrt3) * planar area."""
    s = F(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def perimeter(poly):
    n = len(poly)
    tot = Surd(0)
    for i in range(n):
        tot = tot + edge_len(poly[i], poly[(i + 1) % n])
    return tot


def oler_bound(poly):
    """B(P) = (2/sqrt3)A(P) + M(P)/2 + 1, exactly, for a polygon in (u,v) coords."""
    return Surd(shoelace(poly)) + perimeter(poly) * F(1, 2) + Surd(1)


def convex_hull(points):
    """Monotone chain, exact. Returns hull vertices CCW, or the extreme points if
    the input is degenerate (collinear / <=2 points)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    if len(hull) <= 2:
        return [pts[0], pts[-1]]
    return hull


def hull_oler_bound(points):
    """B(conv E) with the degenerate cases treated as convex bodies:
    a segment has area 0 and 'perimeter' 2*length; a point has both 0."""
    h = convex_hull(points)
    if len(h) == 0:
        return Surd(1)
    if len(h) == 1:
        return Surd(1)
    if len(h) == 2:
        return edge_len(h[0], h[1]) + Surd(1)   # (1/2)*2*len
    return oler_bound(h)


def tri(a):
    """T_a in lattice coordinates."""
    return [(F(0), F(0)), (F(a), F(0)), (F(0), F(a))]


def oler_of_side(a):
    """Oler(a) = a^2/2 + 3a/2 + 1 -- and a cross-check that it equals B(T_a)."""
    a = F(a)
    return a * a / 2 + 3 * a / 2 + 1


def levels(p, a):
    """(level_A, level_B, level_C): the side of the corner triangle at each corner
    whose far edge passes through p.  level_A = u+v, level_B = a-u, level_C = a-v."""
    u, v = p
    return (u + v, F(a) - u, F(a) - v)


def in_triangle(p, a):
    lv = levels(p, a)
    return all(x >= 0 for x in lv) and lv[0] <= F(a)


def lattice(m):
    """The T(m+1) points of the unit triangular lattice in T_m."""
    return [(F(i), F(j)) for i in range(m + 1) for j in range(m + 1 - i)]


def T(k):
    return k * (k + 1) // 2
