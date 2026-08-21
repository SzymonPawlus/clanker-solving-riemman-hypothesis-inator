"""Minimal exact rational-interval arithmetic, written independently for this attack.

Deliberately NOT imported from ../packing-oler-slack/exact.py: the point of a second
implementation is that it can disagree.  `selfcheck.py` compares this module's
`sqrt_iv` against that one on a grid of rationals.

Every endpoint is a Fraction; every operation rounds outward, so an Ival is a
rigorous enclosure.  No float is ever compared against anything.
"""

from fractions import Fraction as F
from math import isqrt


def sqrt_iv(q, prec=40):
    """Rational interval [lo, hi] with lo <= sqrt(q) <= hi, for rational q >= 0."""
    if q < 0:
        raise ValueError("sqrt of negative rational")
    if q == 0:
        return F(0), F(0)
    num, den = q.numerator, q.denominator
    r = isqrt(num * den)
    if r * r == num * den:
        return F(r, den), F(r, den)
    s = 10 ** prec
    r = isqrt(num * den * s * s)
    return F(r, den * s), F(r + 1, den * s)


class Ival:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("empty interval")

    @staticmethod
    def sqrt_of(q, prec=40):
        lo, hi = sqrt_iv(F(q), prec)
        return Ival(lo, hi)

    def __add__(self, o):
        o = _iv(o)
        return Ival(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Ival(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-_iv(o))

    def __rsub__(self, o):
        return _iv(o) + (-self)

    def __mul__(self, o):
        o = _iv(o)
        c = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Ival(min(c), max(c))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _iv(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("interval straddles zero")
        c = [self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi]
        return Ival(min(c), max(c))

    def floor_upper(self):
        """Largest integer m with m <= hi -- i.e. floor of an upper bound."""
        import math
        return math.floor(self.hi)

    def certainly_lt(self, o):
        return self.hi < _iv(o).lo

    def certainly_le(self, o):
        return self.hi <= _iv(o).lo

    def __repr__(self):
        return "[%.10f, %.10f]" % (float(self.lo), float(self.hi))


def _iv(o):
    return o if isinstance(o, Ival) else Ival(F(o))
