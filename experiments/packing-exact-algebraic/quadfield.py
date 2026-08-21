"""Exact arithmetic in a multiquadratic field Q(sqrt p_1, ..., sqrt p_k) over Fraction.

Written from scratch for issue #74. It deliberately does NOT import, adapt, or read any other
checker in this repo (problems/circle-packing-equilateral-triangle/RULES.md 3 asks for
independent reimplementation), and it deliberately does not depend on sympy: the whole point is
that the arithmetic underneath a certificate should be auditable in a couple of screens.

Representation
--------------
An element is a finite Q-linear combination

    x = sum_S c_S * sqrt(prod S)

where S ranges over *sets of distinct primes* and c_S is a Fraction. Products of square roots
reduce by

    sqrt(prod S) * sqrt(prod T) = prod(S & T) * sqrt(prod(S ^ T)),

so the representation is closed under multiplication.

Two facts make this exact and total:

1. **Zero test is syntactic.** The square roots of distinct squarefree integers > 1 are linearly
   independent over Q (standard; the multiquadratic field Q(sqrt p_1..p_k) has degree 2^k with
   exactly this basis). So x == 0 iff every stored coefficient is 0. No numerical tolerance is
   involved anywhere in deciding equality.

2. **Sign test terminates.** For x != 0 we bracket each sqrt(m) by rationals
   isqrt(m*4^p)/2^p <= sqrt(m) <= (isqrt(m*4^p)+1)/2^p and evaluate the sum in rational interval
   arithmetic, doubling p until the interval excludes 0. Because x != 0 this halts, and the answer
   it gives is a proof, not an estimate.

Division by an arbitrary nonzero element uses the norm: multiplying x by its 2^k - 1 conjugates
(all sign patterns on the generators) gives a rational, so 1/x = (prod of conjugates) / norm.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

__all__ = ["Q", "sqrt", "QF", "sign", "cmp"]


def _factor_squarefree(m: int) -> frozenset:
    """Return the prime set of the squarefree part of m; m must be a positive integer."""
    if m <= 0:
        raise ValueError("sqrt of non-positive integer is not supported")
    primes = set()
    d = 2
    while d * d <= m:
        e = 0
        while m % d == 0:
            m //= d
            e += 1
        if e % 2 == 1:
            primes.add(d)
        d += 1 if d == 2 else 2
    if m > 1:
        primes.add(m)
    return frozenset(primes)


def _rad(S: frozenset) -> int:
    r = 1
    for p in S:
        r *= p
    return r


class QF:
    """An element of a multiquadratic field over Q."""

    __slots__ = ("c",)

    def __init__(self, coeffs=None):
        c = {}
        if coeffs:
            for S, v in coeffs.items():
                v = Fraction(v)
                if v:
                    c[frozenset(S)] = c.get(frozenset(S), Fraction(0)) + v
            c = {S: v for S, v in c.items() if v}
        self.c = c

    # ---- construction -------------------------------------------------
    @staticmethod
    def rational(v) -> "QF":
        return QF({frozenset(): Fraction(v)})

    @staticmethod
    def sqrt_int(m: int) -> "QF":
        """sqrt(m) for a positive integer m, with the square part pulled out exactly."""
        if m < 0:
            raise ValueError("sqrt of a negative integer")
        if m == 0:
            return QF()
        S = _factor_squarefree(m)
        outside = isqrt(m // _rad(S))
        assert outside * outside * _rad(S) == m, "square-part extraction failed"
        return QF({S: Fraction(outside)})

    # ---- ring ops -----------------------------------------------------
    def _coerce(self, o):
        if isinstance(o, QF):
            return o
        if isinstance(o, (int, Fraction)):
            return QF.rational(o)
        raise TypeError(f"cannot combine QF with {type(o).__name__}; floats are refused on purpose")

    def __add__(self, o):
        o = self._coerce(o)
        out = dict(self.c)
        for S, v in o.c.items():
            w = out.get(S, Fraction(0)) + v
            if w:
                out[S] = w
            else:
                out.pop(S, None)
        return QF(out)

    __radd__ = __add__

    def __neg__(self):
        return QF({S: -v for S, v in self.c.items()})

    def __sub__(self, o):
        return self + (-self._coerce(o))

    def __rsub__(self, o):
        return self._coerce(o) + (-self)

    def __mul__(self, o):
        o = self._coerce(o)
        out = {}
        for S, a in self.c.items():
            for T, b in o.c.items():
                inter = S & T
                key = S ^ T
                coeff = a * b * _rad(inter)
                w = out.get(key, Fraction(0)) + coeff
                if w:
                    out[key] = w
                else:
                    out.pop(key, None)
        return QF(out)

    __rmul__ = __mul__

    def _conjugates(self):
        """All sign patterns on the generators, as maps applied to self."""
        gens = sorted({p for S in self.c for p in S})
        for mask in range(1 << len(gens)):
            flip = {g for i, g in enumerate(gens) if mask >> i & 1}
            yield QF({S: (-v if len(S & flip) % 2 else v) for S, v in self.c.items()})

    def inverse(self) -> "QF":
        if self.is_zero():
            raise ZeroDivisionError("inverse of exact zero")
        num = QF.rational(1)
        conjs = list(self._conjugates())
        for k in conjs[1:]:
            num = num * k
        norm = self * num
        assert set(norm.c) <= {frozenset()}, "norm of a multiquadratic element must be rational"
        r = norm.c.get(frozenset(), Fraction(0))
        if not r:
            raise ZeroDivisionError("degenerate norm")
        return num * QF.rational(Fraction(1, 1) / r)

    def __truediv__(self, o):
        return self * self._coerce(o).inverse()

    def __rtruediv__(self, o):
        return self._coerce(o) * self.inverse()

    def __pow__(self, k: int):
        if not isinstance(k, int) or k < 0:
            raise ValueError("only non-negative integer powers")
        out, base = QF.rational(1), self
        while k:
            if k & 1:
                out = out * base
            base = base * base
            k >>= 1
        return out

    # ---- exact comparison ---------------------------------------------
    def is_zero(self) -> bool:
        return not self.c

    def enclosure(self, p: int):
        """A rational interval [lo, hi] containing self, using 2^-p bounds on each sqrt."""
        two_p = 1 << p
        lo = hi = Fraction(0)
        for S, v in self.c.items():
            m = _rad(S)
            if m == 1:
                lo += v
                hi += v
                continue
            r_lo = Fraction(isqrt(m * two_p * two_p), two_p)
            r_hi = r_lo + Fraction(1, two_p)
            a, b = (v * r_lo, v * r_hi) if v > 0 else (v * r_hi, v * r_lo)
            lo += a
            hi += b
        return lo, hi

    def sign(self) -> int:
        if self.is_zero():
            return 0
        p = 16
        while True:
            lo, hi = self.enclosure(p)
            if lo > 0:
                return 1
            if hi < 0:
                return -1
            p *= 2
            if p > 1 << 16:  # far beyond anything a genuine nonzero element needs
                raise RuntimeError("sign test failed to converge; representation is inconsistent")

    def __eq__(self, o):
        return (self - self._coerce(o)).is_zero()

    def __lt__(self, o):
        return (self - self._coerce(o)).sign() < 0

    def __le__(self, o):
        return (self - self._coerce(o)).sign() <= 0

    def __gt__(self, o):
        return (self - self._coerce(o)).sign() > 0

    def __ge__(self, o):
        return (self - self._coerce(o)).sign() >= 0

    def __hash__(self):
        return hash(frozenset(self.c.items()))

    def approx(self, p: int = 64) -> float:
        lo, hi = self.enclosure(p)
        return float((lo + hi) / 2)

    def __repr__(self):
        if self.is_zero():
            return "0"
        parts = []
        for S, v in sorted(self.c.items(), key=lambda kv: (len(kv[0]), sorted(kv[0]))):
            m = _rad(S)
            parts.append(str(v) if m == 1 else f"{v}*sqrt({m})")
        return " + ".join(parts)


def Q(v) -> QF:
    return QF.rational(v)


def sqrt(m: int) -> QF:
    return QF.sqrt_int(m)


def sign(x: QF) -> int:
    return x.sign()


def cmp(a: QF, b: QF) -> int:
    return (a - b).sign()
