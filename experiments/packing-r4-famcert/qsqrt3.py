"""Exact arithmetic in Q(sqrt 3), stdlib only.

REUSED VERBATIM from experiments/packing-r3-qsqrt3/qsqrt3.py (worker r3-qsqrt3,
2026-08-23), with permission from the r4-famcert assignment ("You may read and
reuse this code").  Only this docstring differs.

Every comparison below is exact: no floats are used anywhere in this module.
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    # --- ring operations -------------------------------------------------
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
        # (a+b r)(c+d r) = ac + 3bd + (ad+bc) r
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def inv(self):
        # 1/(a+b r) = (a - b r)/(a^2 - 3 b^2)
        n = self.a * self.a - 3 * self.b * self.b
        if n == 0:
            raise ZeroDivisionError("Q3 zero divisor")
        return Q3(self.a / n, -self.b / n)

    def __truediv__(self, o):
        return self * q3(o).inv()

    def __rtruediv__(self, o):
        return q3(o) * self.inv()

    # --- exact ordering --------------------------------------------------
    def sign(self):
        """Exact sign of a + b*sqrt(3), by rational comparison only."""
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        # opposite signs: compare a^2 with 3 b^2
        lhs = a * a
        rhs = 3 * b * b
        if a > 0:  # b < 0, value > 0 iff a^2 > 3 b^2
            return 1 if lhs > rhs else (0 if lhs == rhs else -1)
        else:      # a < 0, b > 0, value > 0 iff 3 b^2 > a^2
            return 1 if rhs > lhs else (0 if rhs == lhs else -1)

    def __eq__(self, o):
        o = q3(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __lt__(self, o):
        return (self - q3(o)).sign() < 0

    def __le__(self, o):
        return (self - q3(o)).sign() <= 0

    def __gt__(self, o):
        return (self - q3(o)).sign() > 0

    def __ge__(self, o):
        return (self - q3(o)).sign() >= 0

    # --- presentation ----------------------------------------------------
    def __repr__(self):
        return self.sexpr()

    def sexpr(self):
        """Exact expression string. Never a decimal."""
        def fr(x):
            return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
        a, b = self.a, self.b
        if b == 0:
            return fr(a)
        bt = "sqrt(3)" if b == 1 else ("-sqrt(3)" if b == -1 else fr(b) + "*sqrt(3)")
        if a == 0:
            return bt
        return fr(a) + (" + " if bt[0] != "-" else " - ") + bt.lstrip("-")

    def approx(self):
        """FOR DISPLAY / SEARCH ONLY. Never used in a verification decision."""
        import math
        return float(self.a) + float(self.b) * math.sqrt(3.0)


def q3(x):
    if isinstance(x, Q3):
        return x
    return Q3(x, 0)


R3 = Q3(0, 1)   # sqrt(3)
