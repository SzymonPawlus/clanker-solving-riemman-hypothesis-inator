"""Independent exact arithmetic in Q(sqrt 3).  Written for worker r5-n17.

Elements are pairs (a, b) of Fractions meaning a + b*sqrt(3).  Stdlib only.
No floats appear anywhere in this file.  Comparison uses the exact sign rule
for a + b*sqrt(3) (compare a^2 vs 3b^2 with sign bookkeeping), never a float cast.
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    # --- ring ops ---
    def __add__(self, o):
        o = _c(o)
        return Q3(self.a + o.a, self.b + o.b)

    def __radd__(self, o):
        return _c(o) + self

    def __sub__(self, o):
        o = _c(o)
        return Q3(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return _c(o) - self

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __mul__(self, o):
        o = _c(o)
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)

    def __rmul__(self, o):
        return _c(o) * self

    def inv(self):
        den = self.a * self.a - 3 * self.b * self.b
        if den == 0:
            raise ZeroDivisionError("Q3 inverse of zero")
        return Q3(self.a / den, -self.b / den)

    def __truediv__(self, o):
        return self * _c(o).inv()

    def __rtruediv__(self, o):
        return _c(o) * self.inv()

    # --- exact sign, no floats ---
    def sign(self):
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if b == 0:
            return 1 if a > 0 else -1
        if a == 0:
            return 1 if b > 0 else -1
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        # opposite signs: compare a^2 with 3b^2
        c = a * a - 3 * b * b          # sign of (a-b*r3)(a+b*r3)
        if a > 0:                       # b < 0 : value = a - |b|r3
            if c > 0:
                return 1
            if c < 0:
                return -1
            return 0
        else:                           # a < 0, b > 0 : value = b*r3 - |a|
            if c > 0:
                return -1
            if c < 0:
                return 1
            return 0

    def __eq__(self, o):
        o = _c(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __lt__(self, o):
        return (self - _c(o)).sign() < 0

    def __le__(self, o):
        return (self - _c(o)).sign() <= 0

    def __gt__(self, o):
        return (self - _c(o)).sign() > 0

    def __ge__(self, o):
        return (self - _c(o)).sign() >= 0

    def is_zero(self):
        return self.a == 0 and self.b == 0

    def __repr__(self):
        return self.sexpr()

    def sexpr(self):
        if self.b == 0:
            return str(self.a)
        if self.a == 0:
            return ("" if self.b == 1 else ("-" if self.b == -1 else str(self.b) + "*")) + "sqrt(3)"
        bs = "" if self.b == 1 else ("-" if self.b == -1 else str(self.b) + "*")
        return "%s + %ssqrt(3)" % (self.a, bs) if self.b > 0 or True else ""

    def approx(self, prec=40):
        """DISPLAY ONLY.  Never used in a decision."""
        import decimal
        decimal.getcontext().prec = prec
        r3 = decimal.Decimal(3).sqrt()
        return decimal.Decimal(self.a.numerator) / self.a.denominator + \
            (decimal.Decimal(self.b.numerator) / self.b.denominator) * r3


def _c(o):
    if isinstance(o, Q3):
        return o
    return Q3(o, 0)


ZERO = Q3(0, 0)
ONE = Q3(1, 0)
R3 = Q3(0, 1)


def mat_inv2(m):
    """Exact inverse of a 2x2 matrix over Q(sqrt3).  m = ((a,b),(c,d))."""
    (a, b), (c, d) = m
    det = a * d - b * c
    if det.is_zero():
        raise ZeroDivisionError("singular")
    di = det.inv()
    return ((d * di, -b * di), (-c * di, a * di))


def mat_vec(m, v):
    (a, b), (c, d) = m
    return (a * v[0] + b * v[1], c * v[0] + d * v[1])


def mat_mul(m, k):
    return tuple(tuple(sum((m[i][t] * k[t][j] for t in range(2)), ZERO)
                       for j in range(2)) for i in range(2))
