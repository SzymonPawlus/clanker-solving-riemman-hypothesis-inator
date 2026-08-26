"""Exact arithmetic in Q(sqrt 3).  Written for r6-stairthm from scratch.

An element is a + b*sqrt(3) with a, b in Q, stored as a pair of Fractions.
Every ordering decision is exact; no float is ever consulted in an accept/reject
step anywhere in this directory.

Sign rule.  For v = a + b*sqrt3:
  - a >= 0 and b >= 0 and not both zero  ->  +
  - a <= 0 and b <= 0 and not both zero  ->  -
  - mixed signs: compare a^2 against 3 b^2, with the sign of a deciding which
    way the comparison points.  (a - b sqrt3)(a + b sqrt3) = a^2 - 3 b^2.
"""
from fractions import Fraction as F


class E:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = a if isinstance(a, F) else F(a)
        self.b = b if isinstance(b, F) else F(b)

    @staticmethod
    def of(x):
        return x if isinstance(x, E) else E(x, 0)

    def __add__(self, o):
        o = E.of(o); return E(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __neg__(self):
        return E(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-E.of(o))

    def __rsub__(self, o):
        return E.of(o) + (-self)

    def __mul__(self, o):
        o = E.of(o)
        return E(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = E.of(o)
        n = o.a * o.a - 3 * o.b * o.b
        if n == 0:
            raise ZeroDivisionError
        return self * E(o.a / n, -o.b / n)

    def sgn(self):
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if a >= 0 and b >= 0:
            return 1
        if a <= 0 and b <= 0:
            return -1
        # mixed
        lhs, rhs = a * a, 3 * b * b
        if a > 0:            # b < 0
            return 1 if lhs > rhs else (0 if lhs == rhs else -1)
        else:                # a < 0, b > 0
            return 1 if rhs > lhs else (0 if rhs == lhs else -1)

    def __eq__(self, o):
        o = E.of(o); return self.a == o.a and self.b == o.b

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash((self.a, self.b))

    def __lt__(self, o):  return (self - E.of(o)).sgn() < 0
    def __le__(self, o):  return (self - E.of(o)).sgn() <= 0
    def __gt__(self, o):  return (self - E.of(o)).sgn() > 0
    def __ge__(self, o):  return (self - E.of(o)).sgn() >= 0

    def __repr__(self):
        return self.s()

    def s(self):
        """Exact expression string.  NEVER a decimal."""
        def fr(x):
            return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
        if self.b == 0:
            return fr(self.a)
        if self.b == 1:
            t = "sqrt(3)"
        elif self.b == -1:
            t = "-sqrt(3)"
        else:
            t = fr(self.b) + "*sqrt(3)"
        if self.a == 0:
            return t
        return fr(self.a) + (" - " + t[1:] if t[0] == "-" else " + " + t)

    def f(self):
        """DISPLAY / SEARCH ONLY.  Never used in a verification decision."""
        import math
        return float(self.a) + float(self.b) * math.sqrt(3.0)


SQ3 = E(0, 1)
ZERO = E(0, 0)


def selftest():
    assert (SQ3 * SQ3) == E(3, 0)
    assert E(1, 1) > E(2, 0)          # 1+1.732 > 2
    assert E(2, -1) > E(0, 0)         # 2-1.732 > 0
    assert E(1, -1) < E(0, 0)         # 1-1.732 < 0
    assert E(3, -1) > E(0, 0) and E(0, 1) * E(0, 1) == E(3, 0)
    assert E(0, 2) == E(0, 2) and E(0, 2) > E(3, 0)   # 2sqrt3=3.46 > 3
    assert E(0, 2) < E(4, 0)
    assert E(F(1, 3), 0) + E(F(2, 3), 0) == E(1, 0)
    assert (E(1, 1) * E(1, -1)) == E(-2, 0)
    # sqrt3 is irrational => a+b sqrt3 = 0 iff a=b=0
    assert E(3, -2).sgn() == -1        # 3 - 3.46 < 0
    assert E(-3, 2).sgn() == 1
    print("q3 selftest OK")


if __name__ == "__main__":
    selftest()
