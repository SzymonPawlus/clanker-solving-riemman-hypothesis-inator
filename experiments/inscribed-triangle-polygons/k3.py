"""Exact arithmetic in the real quadratic field K = Q(sqrt 3).

Written from scratch for issue #132. Standard library only (`fractions`); nothing here
imports sympy, numpy, or any other checker in this repo.

Representation
--------------
An element is a pair of rationals (a, b) standing for the real number

    a + b * sqrt(3).

K is closed under +, -, *, / because 3 is not a rational square, so this is the whole
field Q(sqrt 3) and every operation below is total (except division by 0).

Why this suffices for the experiment
------------------------------------
The only irrational quantity that enters an inscribed-equilateral-triangle computation on a
*rational* polygon is sqrt(3), from cos 60 = 1/2 and sin 60 = sqrt(3)/2. Rotating a rational
point by +-60 degrees lands in K; intersecting two K-segments uses only field operations, so
it lands in K again. Hence every number in the whole pipeline lives here and every decision is
made by exact rational comparisons.

Two facts make the arithmetic exact and total:

1. **Zero test is syntactic.** sqrt(3) is irrational, so a + b*sqrt(3) = 0 with a, b in Q
   forces a = b = 0. Equality is therefore coefficientwise; no tolerance is involved anywhere.

2. **Sign test is a rational comparison.** If a and b have the same (or zero) sign the answer
   is immediate. Otherwise the two terms fight, and since both |a| and |b|*sqrt(3) are >= 0 we
   may square: sign(a + b*sqrt 3) is decided by comparing a^2 with 3b^2. That comparison is
   exact in Q, and a^2 = 3b^2 with b != 0 would make sqrt(3) = |a/b| rational, so it never
   happens -- the code asserts this rather than silently returning 0.

`float(x)` exists for *display only* and is never consulted by any decision procedure.
"""

from __future__ import annotations

from fractions import Fraction

__all__ = ["K", "kq", "SQRT3", "ZERO", "ONE", "HALF", "SIN60", "COS60"]


def _fr(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x)
    if isinstance(x, float):
        raise TypeError("refusing to build an exact number from a float")
    raise TypeError(f"cannot coerce {type(x).__name__} to Fraction")


class K:
    """The real number a + b*sqrt(3), with a, b rational."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = _fr(a)
        self.b = _fr(b)

    # -- construction / display -------------------------------------------------
    @staticmethod
    def coerce(x) -> "K":
        if isinstance(x, K):
            return x
        return K(x, 0)

    def __repr__(self) -> str:
        return f"K({self.a}, {self.b})"

    def __str__(self) -> str:
        if self.b == 0:
            return str(self.a)
        if self.a == 0:
            return f"{self.b}*sqrt3"
        return f"{self.a}{'+' if self.b > 0 else '-'}{abs(self.b)}*sqrt3"

    def as_pair(self):
        """JSON-friendly exact serialisation: [a, b] as strings, meaning a + b*sqrt(3)."""
        return [str(self.a), str(self.b)]

    def __float__(self) -> float:
        """DISPLAY ONLY. No decision procedure in this experiment calls this."""
        return float(self.a) + float(self.b) * 1.7320508075688772935

    # -- ring / field operations ------------------------------------------------
    def __add__(self, o):
        o = K.coerce(o)
        return K(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, o):
        o = K.coerce(o)
        return K(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return K.coerce(o) - self

    def __mul__(self, o):
        o = K.coerce(o)
        # (a + b s)(c + d s) = (ac + 3bd) + (ad + bc) s,  s^2 = 3
        return K(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def inv(self) -> "K":
        # 1/(a + b s) = (a - b s)/(a^2 - 3 b^2); the norm vanishes only at 0.
        n = self.a * self.a - 3 * self.b * self.b
        if n == 0:
            if self.a == 0 and self.b == 0:
                raise ZeroDivisionError("division by zero in Q(sqrt 3)")
            raise AssertionError("norm 0 at a nonzero element: sqrt(3) would be rational")
        return K(self.a / n, -self.b / n)

    def __truediv__(self, o):
        return self * K.coerce(o).inv()

    def __rtruediv__(self, o):
        return K.coerce(o) * self.inv()

    # -- order ------------------------------------------------------------------
    def sign(self) -> int:
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        # opposite signs: compare |a| against |b|*sqrt 3 by squaring (both nonneg)
        d = a * a - 3 * b * b
        if d == 0:
            raise AssertionError("a^2 = 3b^2 with b != 0: sqrt(3) would be rational")
        if a > 0:  # value = a - |b| sqrt3, positive iff a^2 > 3b^2
            return 1 if d > 0 else -1
        # a < 0 < b: value = |b| sqrt3 - |a|, positive iff 3b^2 > a^2
        return -1 if d > 0 else 1

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def __eq__(self, o) -> bool:
        if not isinstance(o, K):
            if isinstance(o, (int, Fraction, str)):
                o = K.coerce(o)
            else:
                return NotImplemented
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __lt__(self, o):
        return (self - K.coerce(o)).sign() < 0

    def __le__(self, o):
        return (self - K.coerce(o)).sign() <= 0

    def __gt__(self, o):
        return (self - K.coerce(o)).sign() > 0

    def __ge__(self, o):
        return (self - K.coerce(o)).sign() >= 0


def kq(a=0, b=0) -> K:
    """Shorthand constructor: kq(a, b) == a + b*sqrt(3)."""
    return K(a, b)


ZERO = K(0, 0)
ONE = K(1, 0)
HALF = K(Fraction(1, 2), 0)
SQRT3 = K(0, 1)
COS60 = HALF
SIN60 = K(0, Fraction(1, 2))
