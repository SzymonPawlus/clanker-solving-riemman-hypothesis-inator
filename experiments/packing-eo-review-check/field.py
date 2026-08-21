"""Exact arithmetic in Q(sqrt3, sqrt11), plus rigorous rational enclosures.

Written from scratch for the independent review of the Oler-slack attack
(problem RULES.md section 3: the reviewer reimplements, never imports the
author's code).  Nothing here is adapted from experiments/packing-oler-slack.

Basis over Q: (1, sqrt3, sqrt11, sqrt33).  These four are Q-linearly
independent (3, 11, 33 are distinct squarefree integers), so an element is
zero iff all four coordinates vanish -- that is what makes exact sign tests
terminate.
"""

from fractions import Fraction as F
from math import isqrt

# multiplication table exponents: sqrt3^2=3, sqrt11^2=11, sqrt3*sqrt11=sqrt33
RADS = (1, 3, 11, 33)


class Alg:
    """a + b*sqrt3 + c*sqrt11 + d*sqrt33 with a,b,c,d rational."""

    __slots__ = ("c",)

    def __init__(self, a=0, b=0, c=0, d=0):
        self.c = (F(a), F(b), F(c), F(d))

    # -- constructors -----------------------------------------------------
    @staticmethod
    def rat(q):
        return Alg(F(q))

    @staticmethod
    def sqrt(k):
        if k == 1:
            return Alg(1)
        if k == 3:
            return Alg(0, 1)
        if k == 11:
            return Alg(0, 0, 1)
        if k == 33:
            return Alg(0, 0, 0, 1)
        r = isqrt(k)
        if r * r == k:
            return Alg(r)
        raise ValueError("sqrt(%d) is outside Q(sqrt3,sqrt11)" % k)

    # -- ring ops ---------------------------------------------------------
    def __add__(s, o):
        o = _co(o)
        return Alg(*[x + y for x, y in zip(s.c, o.c)])

    def __sub__(s, o):
        o = _co(o)
        return Alg(*[x - y for x, y in zip(s.c, o.c)])

    def __neg__(s):
        return Alg(*[-x for x in s.c])

    __radd__ = __add__

    def __rsub__(s, o):
        return _co(o) - s

    def __mul__(s, o):
        o = _co(o)
        a, b, c, d = s.c
        p, q, r, t = o.c
        return Alg(
            a * p + 3 * b * q + 11 * c * r + 33 * d * t,
            a * q + b * p + 11 * (c * t + d * r),
            a * r + c * p + 3 * (b * t + d * q),
            a * t + d * p + b * r + c * q,
        )

    __rmul__ = __mul__

    def _conj(s, s3, s11):
        a, b, c, d = s.c
        return Alg(a, s3 * b, s11 * c, s3 * s11 * d)

    def inv(s):
        if s.is_zero():
            raise ZeroDivisionError
        m = s._conj(-1, 1) * s._conj(1, -1) * s._conj(-1, -1)
        norm = (s * m).c
        assert all(x == 0 for x in norm[1:]), "norm must be rational"
        return m * Alg(1 / norm[0])

    def __truediv__(s, o):
        o = _co(o)
        if all(x == 0 for x in o.c[1:]):          # cheap path: rational divisor
            return s * Alg(1 / o.c[0])
        return s * o.inv()

    def __rtruediv__(s, o):
        return _co(o) / s

    def __pow__(s, k):
        r = Alg(1)
        for _ in range(k):
            r = r * s
        return r

    # -- comparison -------------------------------------------------------
    def is_zero(s):
        return all(x == 0 for x in s.c)

    def __eq__(s, o):
        return (s - _co(o)).is_zero()

    def __hash__(s):
        return hash(s.c)

    def sign(s):
        """Exact sign.  Zero is decided algebraically, not numerically."""
        if s.is_zero():
            return 0
        n = 10 ** 40
        while True:
            lo, hi = s.enclose(n)
            if lo > 0:
                return 1
            if hi < 0:
                return -1
            n *= n                       # square the precision and retry

    def __lt__(s, o):
        return (s - _co(o)).sign() < 0

    def __le__(s, o):
        return (s - _co(o)).sign() <= 0

    def __gt__(s, o):
        return (s - _co(o)).sign() > 0

    def __ge__(s, o):
        return (s - _co(o)).sign() >= 0

    # -- enclosure --------------------------------------------------------
    def enclose(s, n=10 ** 40):
        """Rational interval [lo, hi] containing the real value, outward rounded."""
        lo = hi = s.c[0]
        for coef, rad in zip(s.c[1:], RADS[1:]):
            if coef == 0:
                continue
            rl, rh = sqrt_bounds(F(rad), n)
            terms = (coef * rl, coef * rh)
            lo += min(terms)
            hi += max(terms)
        return lo, hi

    def approx(s, digits=10):
        lo, hi = s.enclose(10 ** (digits + 25))
        return float((lo + hi) / 2)

    def __repr__(s):
        names = ("", "*r3", "*r11", "*r33")
        parts = [f"{x}{nm}" for x, nm in zip(s.c, names) if x != 0]
        return " + ".join(parts) if parts else "0"


def _co(o):
    return o if isinstance(o, Alg) else Alg(F(o))


def sqrt_bounds(q, n=10 ** 40):
    """Rational L <= sqrt(q) <= U with denominator n, for rational q >= 0."""
    q = F(q)
    assert q >= 0
    num, den = q.numerator, q.denominator
    lo_int = isqrt((num * n * n) // den)                  # floor underestimates
    up_int = isqrt(-((-num * n * n) // den)) + 1          # ceil then bump
    return F(lo_int, n), F(up_int, n)


class Iv:
    """Rational interval with outward-rounded arithmetic (for lengths)."""

    __slots__ = ("lo", "hi", "exact")

    def __init__(self, lo, hi=None):
        if hi is None:
            hi = lo
        self.lo, self.hi = F(lo), F(hi)
        self.exact = None
        assert self.lo <= self.hi

    @staticmethod
    def of(x, n=10 ** 40):
        lo, hi = x.enclose(n) if isinstance(x, Alg) else (F(x), F(x))
        return Iv(lo, hi)

    def __add__(s, o):
        o = _iv(o)
        return Iv(s.lo + o.lo, s.hi + o.hi)

    __radd__ = __add__

    def __sub__(s, o):
        o = _iv(o)
        return Iv(s.lo - o.hi, s.hi - o.lo)

    def __rsub__(s, o):
        return _iv(o) - s

    def __mul__(s, o):
        o = _iv(o)
        p = (s.lo * o.lo, s.lo * o.hi, s.hi * o.lo, s.hi * o.hi)
        return Iv(min(p), max(p))

    __rmul__ = __mul__

    def __truediv__(s, o):
        o = _iv(o)
        assert o.lo > 0 or o.hi < 0
        p = (s.lo / o.lo, s.lo / o.hi, s.hi / o.lo, s.hi / o.hi)
        return Iv(min(p), max(p))

    def sqrt(s, n=10 ** 40):
        assert s.lo >= 0
        return Iv(sqrt_bounds(s.lo, n)[0], sqrt_bounds(s.hi, n)[1])

    def sign(s):
        if s.lo > 0:
            return 1
        if s.hi < 0:
            return -1
        return None                     # undecided

    def mid(s):
        return float((s.lo + s.hi) / 2)

    def width(s):
        return float(s.hi - s.lo)

    def __repr__(s):
        return f"[{float(s.lo):.10f}, {float(s.hi):.10f}]"


def _iv(o):
    return o if isinstance(o, Iv) else Iv.of(o)
