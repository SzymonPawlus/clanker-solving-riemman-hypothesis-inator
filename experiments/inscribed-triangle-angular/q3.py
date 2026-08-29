"""Exact arithmetic in K = Q(sqrt 3), written from scratch for the angular lane.

This module is deliberately INDEPENDENT of experiments/inscribed-triangle-polygons/k3.py:
it is a separate implementation, with a different internal representation (an immutable
2-tuple of Fractions carried on the instance, no operator coercion from strings), a
different sign algorithm, and its own tests.  Nothing here imports that file, sympy, or
numpy.  The only dependency is `fractions` from the standard library.

Why Q(sqrt 3) is enough
-----------------------
The only irrational the problem produces is sin 60 = sqrt(3)/2 (cos 60 = 1/2 is rational).
Rotating a point of K^2 by +-60 degrees about a point of K^2 stays in K^2, and every other
operation used by the decision procedure (cross products, dot products, one division per
ray/line meet, comparisons of squared radii) is a field operation.  So the whole pipeline
lives in K and every decision is an exact rational comparison.

Exactness
---------
* Equality: sqrt(3) is irrational, so a + b sqrt3 = 0 iff a = b = 0.  Equality is
  coefficientwise and there is no tolerance anywhere.
* Sign: computed by isolating the radical.  a + b sqrt3 > 0 iff  a > -b sqrt3.  If the two
  sides have known signs the answer is immediate; otherwise both sides are >= 0 and squaring
  is an equivalence, giving a comparison of a^2 with 3 b^2 in Q.  a^2 = 3 b^2 with b != 0
  would make sqrt 3 = |a/b| rational, so that case is impossible and the code raises rather
  than returning 0.

float() is provided for printing and for the float pre-screen in the self-tests only.  No
predicate used by a reported decision ever calls it; see `angular.py`.
"""

from __future__ import annotations

from fractions import Fraction

__all__ = ["Q3", "q3", "rat", "ZERO", "ONE", "TWO", "HALF", "SQRT3", "C60", "S60"]

_SQRT3_FLOAT = 1.7320508075688772935


def rat(x) -> Fraction:
    """Coerce int / Fraction / str to Fraction.  Floats are refused on purpose."""
    if type(x) is Fraction:
        return x
    if isinstance(x, bool):
        raise TypeError("bool is not a number here")
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, Fraction):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x)
    if isinstance(x, float):
        raise TypeError("refusing to build an exact number from a float")
    raise TypeError("cannot coerce %s" % type(x).__name__)


class Q3:
    """The real number  a + b*sqrt(3)  with a, b in Q.  Immutable."""

    __slots__ = ("_ab",)

    def __init__(self, a=0, b=0):
        self._ab = (rat(a), rat(b))

    # ---- accessors -----------------------------------------------------------
    @property
    def a(self) -> Fraction:
        return self._ab[0]

    @property
    def b(self) -> Fraction:
        return self._ab[1]

    @staticmethod
    def of(x) -> "Q3":
        return x if isinstance(x, Q3) else Q3(x, 0)

    def pair(self):
        """Exact JSON serialisation: ["a", "b"] meaning a + b*sqrt(3)."""
        return [str(self._ab[0]), str(self._ab[1])]

    @staticmethod
    def from_pair(p) -> "Q3":
        return Q3(Fraction(p[0]), Fraction(p[1]))

    def __repr__(self):
        a, b = self._ab
        if b == 0:
            return str(a)
        if a == 0:
            return "%s*r3" % b
        return "(%s%s%s*r3)" % (a, "+" if b > 0 else "-", abs(b))

    def __float__(self):
        """DISPLAY / PRE-SCREEN ONLY.  Never called by a reported decision."""
        return float(self._ab[0]) + float(self._ab[1]) * _SQRT3_FLOAT

    # ---- field ---------------------------------------------------------------
    def __add__(self, o):
        o = Q3.of(o)
        return Q3(self._ab[0] + o._ab[0], self._ab[1] + o._ab[1])

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self._ab[0], -self._ab[1])

    def __sub__(self, o):
        o = Q3.of(o)
        return Q3(self._ab[0] - o._ab[0], self._ab[1] - o._ab[1])

    def __rsub__(self, o):
        return Q3.of(o).__sub__(self)

    def __mul__(self, o):
        o = Q3.of(o)
        a, b = self._ab
        c, d = o._ab
        return Q3(a * c + 3 * b * d, a * d + b * c)

    __rmul__ = __mul__

    def inv(self) -> "Q3":
        a, b = self._ab
        n = a * a - 3 * b * b          # the field norm
        if n == 0:
            if a == 0 and b == 0:
                raise ZeroDivisionError("0 has no inverse in Q(sqrt 3)")
            raise AssertionError("norm 0 at a nonzero element => sqrt 3 rational")
        return Q3(a / n, -b / n)

    def __truediv__(self, o):
        return self * Q3.of(o).inv()

    def __rtruediv__(self, o):
        return Q3.of(o) * self.inv()

    # ---- order ---------------------------------------------------------------
    def sgn(self) -> int:
        """Exact sign.  See the module docstring for why this is total."""
        a, b = self._ab
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        # a and b have strictly opposite signs: compare |a| with |b| sqrt 3.
        t = a * a - 3 * b * b
        if t == 0:
            raise AssertionError("a^2 = 3b^2 with b != 0 => sqrt 3 rational")
        # value = sign(a) * (|a| - |b| sqrt3)
        inner = 1 if t > 0 else -1
        return inner if a > 0 else -inner

    def is_zero(self) -> bool:
        return self._ab[0] == 0 and self._ab[1] == 0

    def __eq__(self, o):
        if isinstance(o, Q3):
            return self._ab == o._ab
        if isinstance(o, (int, Fraction)):
            return self._ab == (Fraction(o), Fraction(0))
        return NotImplemented

    def __hash__(self):
        return hash(self._ab)

    def __lt__(self, o):
        return (self - Q3.of(o)).sgn() < 0

    def __le__(self, o):
        return (self - Q3.of(o)).sgn() <= 0

    def __gt__(self, o):
        return (self - Q3.of(o)).sgn() > 0

    def __ge__(self, o):
        return (self - Q3.of(o)).sgn() >= 0

    def __abs__(self):
        return self if self.sgn() >= 0 else -self


def q3(a=0, b=0) -> Q3:
    return Q3(a, b)


ZERO = Q3(0, 0)
ONE = Q3(1, 0)
TWO = Q3(2, 0)
HALF = Q3(Fraction(1, 2), 0)
SQRT3 = Q3(0, 1)
C60 = HALF                       # cos 60
S60 = Q3(0, Fraction(1, 2))      # sin 60 = sqrt(3)/2
