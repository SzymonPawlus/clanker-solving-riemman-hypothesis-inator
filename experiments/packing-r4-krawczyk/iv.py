"""Rigorous rational interval arithmetic on a fixed decimal grid.

CONSTRUCTION-SIDE TOOLING ONLY. Nothing here bears on optimality.

An interval is a pair of Python ints ``(lo, hi)`` denoting the closed real interval
``[lo / DEN, hi / DEN]`` with ``DEN = 10**SCALE``.  Endpoints are therefore exact
rationals.  Every operation rounds *outward* to the grid, so a computed interval always
contains the exact result set.  No floating point appears anywhere in this module.
"""

from __future__ import annotations

from fractions import Fraction

SCALE = 50
DEN = 10 ** SCALE


def _fdiv(a: int, b: int) -> int:
    """floor(a / b) for b > 0."""
    return a // b


def _cdiv(a: int, b: int) -> int:
    """ceil(a / b) for b > 0."""
    return -((-a) // b)


def from_frac(q: Fraction) -> tuple[int, int]:
    """Smallest grid interval containing the exact rational ``q``."""
    return (_fdiv(q.numerator * DEN, q.denominator), _cdiv(q.numerator * DEN, q.denominator))


def from_int_units(k: int) -> tuple[int, int]:
    """Degenerate interval [k/DEN, k/DEN]."""
    return (k, k)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[1], a[1] - b[0])


def neg(a):
    return (-a[1], -a[0])


def mul(a, b):
    """Outward-rounded product.  Endpoints are in units of 1/DEN, so the raw products
    are in units of 1/DEN**2 and are divided back down with directed rounding."""
    a0, a1 = a
    b0, b1 = b
    p1 = a0 * b0
    p2 = a0 * b1
    p3 = a1 * b0
    p4 = a1 * b1
    lo = p1 if p1 < p2 else p2
    if p3 < lo:
        lo = p3
    if p4 < lo:
        lo = p4
    hi = p1 if p1 > p2 else p2
    if p3 > hi:
        hi = p3
    if p4 > hi:
        hi = p4
    return (_fdiv(lo, DEN), _cdiv(hi, DEN))


def width(a) -> int:
    return a[1] - a[0]


def contains_strict(outer, inner) -> bool:
    """True iff ``inner`` lies in the topological interior of ``outer``."""
    return outer[0] < inner[0] and inner[1] < outer[1]


def to_frac_lo(a) -> Fraction:
    return Fraction(a[0], DEN)


def to_frac_hi(a) -> Fraction:
    return Fraction(a[1], DEN)


def as_float(a) -> float:
    return (a[0] + a[1]) / 2.0 / DEN
