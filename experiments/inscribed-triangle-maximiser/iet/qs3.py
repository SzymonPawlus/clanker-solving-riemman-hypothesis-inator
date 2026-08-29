"""Exact arithmetic in the real field K = Q(sqrt 3), written from scratch for the
MAXIMISER lane.

Independence
------------
This file shares no code with `experiments/inscribed-triangle-polygons/k3.py` or with
`experiments/inscribed-triangle-angular/q3.py`, and it uses a different internal
representation from both: a value is the triple of PYTHON INTEGERS (a, b, c), c > 0,
gcd(a, b, c) = 1, standing for

        (a + b*sqrt(3)) / c

(the other two lanes each carry a pair of `fractions.Fraction`).  Integers keep the
maximiser's cubic-in-n candidate loop cheap and make the sign test a comparison of two
integers rather than of two rationals.

Why Q(sqrt 3) closes the problem
--------------------------------
The rotation by +-60 degrees has matrix [[1/2, -+sqrt3/2], [+-sqrt3/2, 1/2]], so it maps
K^2 into K^2.  Every other operation this lane performs -- cross and dot products, one
division per ray/edge meet, comparison of squared side lengths, and the 3x3 solves of the
LP certificates -- is a field operation.  So no square root ever has to be taken: the
maximiser compares side^2, never side.  `float()` exists for display and for the float
pre-screens that *guide* a search; no reported decision passes through it.

Exactness of the two predicates that matter
-------------------------------------------
* Equality.  sqrt(3) is irrational, so (a + b sqrt3)/c = 0 iff a = b = 0.  Equality is
  therefore structural and there is no tolerance anywhere in this lane.
* Sign.  With integers a, b and c > 0, sgn((a + b sqrt3)/c) = sgn(a + b sqrt3).  If a and b
  have the same sign (or one is zero) the answer is immediate.  Otherwise exactly one of
  them is negative and the comparison |a| vs |b| sqrt3 is equivalent, after squaring two
  nonnegative integers, to a*a vs 3*b*b.  Equality a^2 = 3 b^2 with b != 0 would make
  sqrt(3) = |a/b| rational, so it cannot occur and the code asserts rather than guessing.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd

__all__ = ["Q3", "q3", "SQRT3", "ZERO", "ONE", "HALF", "C60", "S60", "as_q3"]

_SQRT3 = 1.7320508075688772935


class Q3:
    """(a + b*sqrt(3))/c with a, b, c integers, c > 0, gcd(a,b,c) = 1.  Immutable."""

    __slots__ = ("a", "b", "c")

    def __init__(self, a=0, b=0, c=1):
        if isinstance(a, float) or isinstance(b, float) or isinstance(c, float):
            raise TypeError("refusing to build an exact number out of a float")
        a, b, c = int(a), int(b), int(c)
        if c == 0:
            raise ZeroDivisionError("zero denominator in Q3")
        if c < 0:
            a, b, c = -a, -b, -c
        g = gcd(gcd(abs(a), abs(b)), c)
        if g > 1:
            a, b, c = a // g, b // g, c // g
        object.__setattr__(self, "a", a)
        object.__setattr__(self, "b", b)
        object.__setattr__(self, "c", c)

    def __setattr__(self, *_):
        raise AttributeError("Q3 is immutable")

    # ---------------------------------------------------------------- construction
    @staticmethod
    def of(x) -> "Q3":
        """int / Fraction / str('p/q') / Q3 -> Q3.  Floats are refused on purpose."""
        if isinstance(x, Q3):
            return x
        if isinstance(x, bool):
            raise TypeError("bool is not a number here")
        if isinstance(x, int):
            return Q3(x, 0, 1)
        if isinstance(x, Fraction):
            return Q3(x.numerator, 0, x.denominator)
        if isinstance(x, str):
            f = Fraction(x)
            return Q3(f.numerator, 0, f.denominator)
        if isinstance(x, float):
            raise TypeError("refusing to build an exact number out of a float")
        raise TypeError("cannot coerce %s to Q3" % type(x).__name__)

    @staticmethod
    def from_pair(pair) -> "Q3":
        """Read the other lanes' serialisation ["a", "b"] meaning a + b*sqrt(3)."""
        fa, fb = Fraction(pair[0]), Fraction(pair[1])
        d = fa.denominator * fb.denominator // gcd(fa.denominator, fb.denominator)
        return Q3(fa.numerator * (d // fa.denominator),
                  fb.numerator * (d // fb.denominator), d)

    def pair(self):
        """Serialise as ["a", "b"] meaning a + b*sqrt(3), matching the sibling lanes."""
        return [str(Fraction(self.a, self.c)), str(Fraction(self.b, self.c))]

    # ---------------------------------------------------------------- arithmetic
    def __add__(self, o):
        o = Q3.of(o)
        return Q3(self.a * o.c + o.a * self.c, self.b * o.c + o.b * self.c, self.c * o.c)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b, self.c)

    def __sub__(self, o):
        return self + (-Q3.of(o))

    def __rsub__(self, o):
        return Q3.of(o) + (-self)

    def __mul__(self, o):
        o = Q3.of(o)
        return Q3(self.a * o.a + 3 * self.b * o.b,
                  self.a * o.b + self.b * o.a,
                  self.c * o.c)

    __rmul__ = __mul__

    def inv(self) -> "Q3":
        if self.is_zero():
            raise ZeroDivisionError("inverse of 0 in Q3")
        # 1/((a + b r)/c) = c (a - b r) / (a^2 - 3 b^2); the denominator is a nonzero
        # integer because a^2 = 3 b^2 forces a = b = 0 over the integers.
        d = self.a * self.a - 3 * self.b * self.b
        assert d != 0, "a^2 = 3b^2 with (a,b) != 0 would make sqrt3 rational"
        return Q3(self.c * self.a, -self.c * self.b, d)

    def __truediv__(self, o):
        return self * Q3.of(o).inv()

    def __rtruediv__(self, o):
        return Q3.of(o) * self.inv()

    def __pow__(self, n: int):
        if n < 0:
            return self.inv() ** (-n)
        r = ONE
        base = self
        while n:
            if n & 1:
                r = r * base
            base = base * base
            n >>= 1
        return r

    # ---------------------------------------------------------------- predicates
    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def sgn(self) -> int:
        """Exact sign.  No tolerance, no float."""
        a, b = self.a, self.b
        if a == 0:
            return (b > 0) - (b < 0)
        if b == 0:
            return (a > 0) - (a < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        # opposite signs: compare a^2 with 3 b^2, both nonnegative integers.
        lhs, rhs = a * a, 3 * b * b
        if lhs == rhs:
            raise AssertionError("a^2 = 3b^2 with a,b != 0 is impossible over Z")
        big_a = lhs > rhs
        return (1 if a > 0 else -1) if big_a else (1 if b > 0 else -1)

    def __eq__(self, o):
        if not isinstance(o, Q3):
            try:
                o = Q3.of(o)
            except TypeError:
                return NotImplemented
        return self.a == o.a and self.b == o.b and self.c == o.c

    def __hash__(self):
        return hash((self.a, self.b, self.c))

    def __lt__(self, o):
        return (self - Q3.of(o)).sgn() < 0

    def __le__(self, o):
        return (self - Q3.of(o)).sgn() <= 0

    def __gt__(self, o):
        return (self - Q3.of(o)).sgn() > 0

    def __ge__(self, o):
        return (self - Q3.of(o)).sgn() >= 0

    def __abs__(self):
        return -self if self.sgn() < 0 else self

    # ---------------------------------------------------------------- display only
    def __float__(self):
        return (self.a + self.b * _SQRT3) / self.c

    def __repr__(self):
        return "Q3(%d,%d,%d)~%.12g" % (self.a, self.b, self.c, float(self))


def q3(a=0, b=0, c=1) -> Q3:
    return Q3(a, b, c)


def as_q3(x) -> Q3:
    return Q3.of(x)


ZERO = Q3(0, 0, 1)
ONE = Q3(1, 0, 1)
HALF = Q3(1, 0, 2)
SQRT3 = Q3(0, 1, 1)
C60 = HALF                 # cos 60
S60 = Q3(0, 1, 2)          # sin 60 = sqrt3 / 2
