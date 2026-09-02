#!/usr/bin/env python3
"""Exact arithmetic in the real quadratic field Q(sqrt 3).

An element is stored as an ordered pair of `fractions.Fraction`, `(a, b)`
representing the real number `a + b * sqrt(3)`. Every operation below is exact;
there is no floating point anywhere on this module's path. `float()` is provided
only for printing and is never used by a decision procedure.

Sign testing is the only non-obvious operation. For `x = a + b*sqrt(3)` with
`a, b` rational, `sqrt(3)` is irrational, so `x = 0` iff `a = b = 0`. When `a`
and `b` have the same (or a zero) sign the sign of `x` is immediate; when they
have opposite signs the comparison `|a| <=> |b| * sqrt(3)` is decided exactly by
comparing `a**2` with `3 * b**2`, both rational.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Union

Rationalish = Union[int, Fraction, "Q3"]


@dataclass(frozen=True)
class Q3:
    """The real number `a + b * sqrt(3)` with `a`, `b` rational."""

    a: Fraction
    b: Fraction

    def __init__(self, a: Union[int, Fraction] = 0, b: Union[int, Fraction] = 0) -> None:
        object.__setattr__(self, "a", Fraction(a))
        object.__setattr__(self, "b", Fraction(b))

    # -- coercion ---------------------------------------------------------
    @staticmethod
    def coerce(value: Rationalish) -> "Q3":
        if isinstance(value, Q3):
            return value
        if isinstance(value, (int, Fraction)):
            return Q3(value, 0)
        raise TypeError(f"cannot coerce {value!r} into Q(sqrt 3)")

    # -- ring operations --------------------------------------------------
    def __add__(self, other: Rationalish) -> "Q3":
        o = Q3.coerce(other)
        return Q3(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self) -> "Q3":
        return Q3(-self.a, -self.b)

    def __sub__(self, other: Rationalish) -> "Q3":
        return self + (-Q3.coerce(other))

    def __rsub__(self, other: Rationalish) -> "Q3":
        return Q3.coerce(other) + (-self)

    def __mul__(self, other: Rationalish) -> "Q3":
        o = Q3.coerce(other)
        return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def conjugate(self) -> "Q3":
        return Q3(self.a, -self.b)

    def norm(self) -> Fraction:
        """The field norm `a**2 - 3*b**2`; zero only for the zero element."""
        return self.a * self.a - 3 * self.b * self.b

    def inverse(self) -> "Q3":
        norm = self.norm()
        if norm == 0:
            raise ZeroDivisionError("inverse of zero in Q(sqrt 3)")
        return Q3(self.a / norm, -self.b / norm)

    def __truediv__(self, other: Rationalish) -> "Q3":
        return self * Q3.coerce(other).inverse()

    def __rtruediv__(self, other: Rationalish) -> "Q3":
        return Q3.coerce(other) * self.inverse()

    # -- ordering ---------------------------------------------------------
    def sign(self) -> int:
        """Exact sign of `a + b*sqrt(3)`, in {-1, 0, 1}."""
        a, b = self.a, self.b
        if a == 0 and b == 0:
            return 0
        if b == 0:
            return 1 if a > 0 else -1
        if a == 0:
            return 1 if b > 0 else -1
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        # Opposite signs: compare a**2 against 3*b**2.
        left, right = a * a, 3 * b * b
        if left == right:
            # Would force sqrt(3) = |a/b|, rational. Impossible, so unreachable.
            raise AssertionError("sqrt(3) is irrational; this branch cannot occur")
        bigger_is_a = left > right
        return (1 if a > 0 else -1) if bigger_is_a else (1 if b > 0 else -1)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (Q3, int, Fraction)):
            return NotImplemented
        return (self - Q3.coerce(other)).sign() == 0

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    def __lt__(self, other: Rationalish) -> bool:
        return (self - Q3.coerce(other)).sign() < 0

    def __le__(self, other: Rationalish) -> bool:
        return (self - Q3.coerce(other)).sign() <= 0

    def __gt__(self, other: Rationalish) -> bool:
        return (self - Q3.coerce(other)).sign() > 0

    def __ge__(self, other: Rationalish) -> bool:
        return (self - Q3.coerce(other)).sign() >= 0

    # -- presentation -----------------------------------------------------
    def __repr__(self) -> str:
        return f"Q3({self.a}, {self.b})"

    def __str__(self) -> str:
        return f"{self.a} + {self.b}*sqrt(3)"

    def approx(self) -> float:
        """Decimal preview only. Never used by any check in this directory."""
        return float(self.a) + float(self.b) * 3.0 ** 0.5


SQRT3 = Q3(0, 1)
ZERO = Q3(0, 0)
ONE = Q3(1, 0)
