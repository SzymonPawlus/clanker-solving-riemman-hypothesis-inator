"""Specialized exact self-check of the algebraic n=8 lift.

This is the author's checker, not the independent checker required for
``verified:review``.  It uses exact arithmetic in Q(sqrt(3), sqrt(11)) and
rigorous rational root enclosures for signs; no float or symbolic parser appears.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __mul__(self, other: "Interval") -> "Interval":
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))


@dataclass(frozen=True)
class Biquad:
    """c0 + c1*sqrt(3) + c2*sqrt(11) + c3*sqrt(33)."""

    coeffs: tuple[Fraction, Fraction, Fraction, Fraction]

    @staticmethod
    def rational(value: int | Fraction) -> "Biquad":
        return Biquad((Fraction(value), Fraction(0), Fraction(0), Fraction(0)))

    def __add__(self, other: "Biquad" | int) -> "Biquad":
        other = as_biquad(other)
        return Biquad(tuple(a + b for a, b in zip(self.coeffs, other.coeffs, strict=True)))

    __radd__ = __add__

    def __neg__(self) -> "Biquad":
        return Biquad(tuple(-value for value in self.coeffs))

    def __sub__(self, other: "Biquad" | int) -> "Biquad":
        return self + (-as_biquad(other))

    def __rsub__(self, other: "Biquad" | int) -> "Biquad":
        return as_biquad(other) - self

    def __mul__(self, other: "Biquad" | int) -> "Biquad":
        other = as_biquad(other)
        out = [Fraction(0)] * 4
        # Basis index is the bit pair (power of sqrt(3), power of sqrt(11)).
        for left_index, left in enumerate(self.coeffs):
            for right_index, right in enumerate(other.coeffs):
                a = (left_index & 1) + (right_index & 1)
                b = ((left_index >> 1) & 1) + ((right_index >> 1) & 1)
                factor = (3 if a >= 2 else 1) * (11 if b >= 2 else 1)
                index = (a % 2) | ((b % 2) << 1)
                out[index] += left * right * factor
        return Biquad(tuple(out))

    __rmul__ = __mul__

    def __truediv__(self, denominator: int) -> "Biquad":
        return Biquad(tuple(value / denominator for value in self.coeffs))

    def is_zero(self) -> bool:
        return all(value == 0 for value in self.coeffs)


def as_biquad(value: Biquad | int) -> Biquad:
    return value if isinstance(value, Biquad) else Biquad.rational(value)


ZERO = Biquad.rational(0)
ONE = Biquad.rational(1)
SQRT3 = Biquad((Fraction(0), Fraction(1), Fraction(0), Fraction(0)))
SQRT11 = Biquad((Fraction(0), Fraction(0), Fraction(1), Fraction(0)))
SQRT33 = SQRT3 * SQRT11


def _root_interval(radicand: int, decimal_digits: int) -> Interval:
    scale = 10**decimal_digits
    floor = math.isqrt(radicand * scale * scale)
    return Interval(Fraction(floor, scale), Fraction(floor + 1, scale))


def _enclose(value: Biquad, decimal_digits: int) -> Interval:
    sqrt3 = _root_interval(3, decimal_digits)
    sqrt11 = _root_interval(11, decimal_digits)
    basis = (
        Interval(Fraction(1), Fraction(1)),
        sqrt3,
        sqrt11,
        sqrt3 * sqrt11,
    )
    result = Interval(Fraction(0), Fraction(0))
    for coefficient, element in zip(value.coeffs, basis, strict=True):
        scalar = Interval(coefficient, coefficient)
        result = result + scalar * element
    return result


def sign(value: Biquad) -> int:
    if value.is_zero():
        return 0
    for digits in (10, 20, 40, 80, 160):
        enclosure = _enclose(value, digits)
        if enclosure.lo > 0:
            return 1
        if enclosure.hi < 0:
            return -1
    raise ArithmeticError(f"sign remained undecided: {value}")


def n8_formula() -> tuple[Biquad, Biquad, tuple[tuple[Biquad, Biquad], ...]]:
    """Return (container side s, centre-triangle side D, exact point coordinates)."""
    d = 2 + 2 * SQRT33 / 3
    side = d + 2 * SQRT3
    middle_y = (3 * SQRT11 - SQRT3) / 6
    points = (
        (ZERO, ZERO),
        ((3 + SQRT33) / 2, middle_y),
        ((3 + SQRT33) / 3, ZERO),
        (d, ZERO),
        ((3 + SQRT33) / 3, SQRT3 + SQRT11),
        ((6 + SQRT33) / 3, SQRT11),
        ((3 + SQRT33) / 6, middle_y),
        (SQRT33 / 3, SQRT11),
    )
    return side, d, points


def verify_n8() -> dict[str, int]:
    side, d, points = n8_formula()
    if side - 2 * SQRT3 != d:
        raise AssertionError("side conversion is inconsistent")

    pair_equalities = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            gap = dx * dx + dy * dy - 4
            gap_sign = sign(gap)
            if gap_sign < 0:
                raise AssertionError(f"pair {i}-{j} is too close")
            pair_equalities += gap_sign == 0

    wall_equalities = 0
    for i, (x, y) in enumerate(points):
        for wall, slack in (
            ("bottom", y),
            ("left", SQRT3 * x - y),
            ("right", SQRT3 * (d - x) - y),
        ):
            slack_sign = sign(slack)
            if slack_sign < 0:
                raise AssertionError(f"point {i} is outside the {wall} wall")
            wall_equalities += slack_sign == 0

    return {
        "points": len(points),
        "pair_constraints": len(points) * (len(points) - 1) // 2,
        "pair_equalities": pair_equalities,
        "wall_constraints": 3 * len(points),
        "wall_equalities": wall_equalities,
    }


if __name__ == "__main__":
    print(verify_n8())
