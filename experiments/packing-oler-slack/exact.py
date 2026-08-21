"""Exact arithmetic for the Oler slack decomposition.

Two independent number types, used for two different jobs:

`Alg`      elements of the field Q(sqrt3, sqrt11), written on the basis
           (1, sqrt3, sqrt11, sqrt33) with rational coefficients.  Every
           coordinate appearing in this repo's exact certificates lies in this
           field (13 of the 14 are in Q(sqrt3); n = 8 is the one that needs
           sqrt11/sqrt33).  Areas, orientation determinants and the total face
           excess are polynomial in the coordinates, so they stay in the field
           and are computed with no error at all.

`Ival`     rational intervals, for the quantities that leave the field --
           anything with a square root of a non-square, i.e. edge *lengths* and
           hence the perimeter term.  Endpoints are exact `Fraction`s and every
           operation rounds outward, so a reported interval is a rigorous
           enclosure, not a floating-point estimate.

Sign decisions on `Alg` are exact and terminating: 1, sqrt3, sqrt11, sqrt33 are
linearly independent over Q (Q(sqrt3, sqrt11) has degree 4 over Q, with that
basis), so an element is zero iff all four coefficients are zero.  Anything else
is bounded away from zero, so interval refinement decides its sign in finitely
many steps.
"""

from fractions import Fraction as F
from math import isqrt

# --- rational enclosures of the radicals -----------------------------------


def sqrt_bounds(q, prec=60):
    """Rational lo <= sqrt(q) <= hi for a non-negative rational q."""
    if q < 0:
        raise ValueError("sqrt of a negative rational")
    if q == 0:
        return F(0), F(0)
    scale = 10 ** prec
    # sqrt(num/den) = sqrt(num*den)/den
    num, den = q.numerator, q.denominator
    exact = isqrt(num * den)
    if exact * exact == num * den:      # rational square: enclose it exactly
        return F(exact, den), F(exact, den)
    root = isqrt(num * den * scale * scale)
    lo = F(root, den * scale)
    hi = F(root + 1, den * scale)
    return lo, hi


# basis radicals, in the order used by Alg's coefficient tuple
RADICANDS = (1, 3, 11, 33)


class Alg:
    """a + b*sqrt3 + c*sqrt11 + d*sqrt33, with a, b, c, d rational."""

    __slots__ = ("c",)

    def __init__(self, a=0, b=0, c=0, d=0):
        self.c = (F(a), F(b), F(c), F(d))

    # -- constructors
    @staticmethod
    def rational(q):
        return Alg(F(q))

    @staticmethod
    def sqrt(k):
        k = int(k)
        if k == 3:
            return Alg(0, 1, 0, 0)
        if k == 11:
            return Alg(0, 0, 1, 0)
        if k == 33:
            return Alg(0, 0, 0, 1)
        r = isqrt(k)
        if r * r == k:
            return Alg(r)
        raise ValueError(f"sqrt({k}) is outside Q(sqrt3, sqrt11)")

    # -- ring operations
    def __add__(self, o):
        o = _coerce(o)
        return Alg(*(x + y for x, y in zip(self.c, o.c)))

    __radd__ = __add__

    def __neg__(self):
        return Alg(*(-x for x in self.c))

    def __sub__(self, o):
        return self + (-_coerce(o))

    def __rsub__(self, o):
        return _coerce(o) + (-self)

    def __mul__(self, o):
        o = _coerce(o)
        a1, b1, c1, d1 = self.c
        a2, b2, c2, d2 = o.c
        # sqrt3*sqrt3=3, sqrt11*sqrt11=11, sqrt3*sqrt11=sqrt33,
        # sqrt33*sqrt33=33, sqrt3*sqrt33=3*sqrt11, sqrt11*sqrt33=11*sqrt3
        a = a1 * a2 + 3 * b1 * b2 + 11 * c1 * c2 + 33 * d1 * d2
        b = a1 * b2 + b1 * a2 + 11 * (c1 * d2 + d1 * c2)
        c = a1 * c2 + c1 * a2 + 3 * (b1 * d2 + d1 * b2)
        d = a1 * d2 + d1 * a2 + b1 * c2 + c1 * b2
        return Alg(a, b, c, d)

    __rmul__ = __mul__

    def conjugates(self):
        """The four Galois conjugates (sign flips of sqrt3, sqrt11)."""
        a, b, c, d = self.c
        for s3 in (1, -1):
            for s11 in (1, -1):
                yield Alg(a, s3 * b, s11 * c, s3 * s11 * d)

    def inverse(self):
        if self.is_zero():
            raise ZeroDivisionError("inverse of 0")
        prod = Alg(1)
        for k, conj in enumerate(self.conjugates()):
            if k:  # skip the element itself
                prod = prod * conj
        norm = self * prod          # rational by construction
        a, b, c, d = norm.c
        assert (b, c, d) == (F(0), F(0), F(0)), "norm should be rational"
        return prod * Alg(1 / a)

    def __truediv__(self, o):
        return self * _coerce(o).inverse()

    def __rtruediv__(self, o):
        return _coerce(o) * self.inverse()

    # -- comparisons
    def is_zero(self):
        return all(x == 0 for x in self.c)

    def interval(self, prec=60):
        lo = hi = F(0)
        for coeff, k in zip(self.c, RADICANDS):
            rlo, rhi = sqrt_bounds(F(k), prec)
            if coeff >= 0:
                lo += coeff * rlo
                hi += coeff * rhi
            else:
                lo += coeff * rhi
                hi += coeff * rlo
        return lo, hi

    def sign(self):
        if self.is_zero():
            return 0
        prec = 30
        while True:
            lo, hi = self.interval(prec)
            if lo > 0:
                return 1
            if hi < 0:
                return -1
            prec *= 2
            if prec > 4000:                     # unreachable: see module docstring
                raise RuntimeError("sign refinement failed")

    def __eq__(self, o):
        return (self - _coerce(o)).is_zero()

    def __hash__(self):
        return hash(self.c)

    def __lt__(self, o):
        return (self - _coerce(o)).sign() < 0

    def __le__(self, o):
        return (self - _coerce(o)).sign() <= 0

    def __gt__(self, o):
        return (self - _coerce(o)).sign() > 0

    def __ge__(self, o):
        return (self - _coerce(o)).sign() >= 0

    def rational_value(self):
        """The element as a Fraction, or None if it is irrational."""
        a, b, c, d = self.c
        return a if (b == 0 and c == 0 and d == 0) else None

    def float(self):
        lo, hi = self.interval(30)
        return float((lo + hi) / 2)

    def __repr__(self):
        names = ("", "*sqrt3", "*sqrt11", "*sqrt33")
        parts = [f"{co}{nm}" for co, nm in zip(self.c, names) if co != 0]
        return " + ".join(parts) if parts else "0"


def _coerce(o):
    if isinstance(o, Alg):
        return o
    if isinstance(o, (int, F)):
        return Alg(F(o))
    raise TypeError(f"cannot mix Alg with {type(o)}")


ZERO = Alg(0)
ONE = Alg(1)


def parse_alg(s):
    """Parse a certificate coordinate string such as '2*sqrt(3)' or '1 + sqrt(33)/3'.

    Evaluated with an empty builtins namespace and only `sqrt` in scope; integer
    literals become exact `Alg` values through the operator overloads above.
    """
    import re

    # every integer literal becomes a Fraction, so that '1/2' is exact rather
    # than a float -- decimal literals are rejected outright (problem RULES.md
    # §2 bans decimal strings in exact fields)
    if re.search(r"\d\.\d|[eE][-+]?\d", s):
        raise ValueError(f"decimal literal in an exact field: {s!r}")
    src = re.sub(r"(?<![\w.])(\d+)(?![\w.])", r"F(\1)", s)
    env = {"__builtins__": {}, "sqrt": Alg.sqrt, "F": F}
    value = eval(src, env)                                   # noqa: S307 - repo-local data
    return _coerce(value)


# --- rational intervals ----------------------------------------------------


class Ival:
    """A rigorous rational enclosure [lo, hi]; every operation rounds outward."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo if hi is None else hi)
        assert self.lo <= self.hi

    @staticmethod
    def of(alg, prec=60):
        lo, hi = alg.interval(prec) if isinstance(alg, Alg) else (F(alg), F(alg))
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
        products = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Ival(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _iv(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("interval spans zero")
        quotients = (self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi)
        return Ival(min(quotients), max(quotients))

    def __rtruediv__(self, o):
        return _iv(o) / self

    def sqrt(self, prec=60):
        if self.lo < 0:
            raise ValueError("sqrt of an interval below zero")
        lo, _ = sqrt_bounds(self.lo, prec)
        _, hi = sqrt_bounds(self.hi, prec)
        return Ival(lo, hi)

    def sign(self):
        """+1 / -1 if the enclosure decides the sign, else None."""
        if self.lo > 0:
            return 1
        if self.hi < 0:
            return -1
        return None

    def floor(self):
        """floor(x) if the enclosure decides it, else None."""
        import math
        f_lo, f_hi = math.floor(self.lo), math.floor(self.hi)
        return f_lo if f_lo == f_hi else None

    def mid(self):
        return float((self.lo + self.hi) / 2)

    def width(self):
        return float(self.hi - self.lo)

    def __repr__(self):
        return f"[{float(self.lo):.12f}, {float(self.hi):.12f}]"


def _iv(o):
    if isinstance(o, Ival):
        return o
    if isinstance(o, Alg):
        return Ival.of(o)
    if isinstance(o, (int, F)):
        return Ival(F(o))
    raise TypeError(f"cannot mix Ival with {type(o)}")
