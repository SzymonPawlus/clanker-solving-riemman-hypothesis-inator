"""Exact real arithmetic for the packing checker. No floating point, anywhere.

Why this module exists
----------------------
Optimal circle packings in an equilateral triangle have *algebraic*, not rational,
coordinates: the known optima involve sqrt(3) throughout (a triangular-lattice row
offset is exactly sqrt(3)), and some best-known packings involve sqrt(6), sqrt(33),
etc. So `fractions.Fraction` alone is not enough to represent a certificate, and a
`float` is not merely imprecise -- it makes the whole check meaningless, since the
inequalities we test are *tight* at the optimum (distances are exactly 2, points sit
exactly on the boundary). A checker that rounds cannot distinguish "touching" from
"overlapping".

Representation choice
---------------------
Two representations are supported, matching the certificate's `coordinate_type`:

1. `rational` / `algebraic` -> **exact symbolic algebraic numbers** (`sympy.Expr`
   built only from integers, rationals and radicals).  Arithmetic is symbolic and
   therefore exact.  The only hard part is *deciding a sign*, which is what the
   checker actually needs (`is this quantity >= 0?`).  That is done by
   `sign_of()` below with a decision procedure that never guesses.

2. `interval` -> **rigorous rational interval enclosures** (`RatInterval`), with
   `fractions.Fraction` endpoints.  Every operation rounds outward, so an enclosure
   always contains the true value.  A certificate of this type is accepted only if
   the constraints hold for *every* point in the enclosure, i.e. the check is
   conservative: it can refuse a feasible packing, but it can never accept an
   infeasible one.

Trade-offs
----------
* Symbolic (1) is exact and gives crisp yes/no answers including the boundary case
  "distance is exactly 2", which is the case that matters most here.  Cost: sign
  decisions on algebraic numbers need a zero test, which is `minimal_polynomial`
  and can be slow for deeply nested radicals.  For the expressions that appear in
  this problem (a couple of square roots) it is fast.
* Interval (2) is fast and needs no symbolic machinery, but it is one-sided: it
  can never certify an equality, so a packing whose circles exactly touch will be
  *rejected* unless the certificate's intervals are degenerate (lo == hi).  This is
  the right failure direction, but it means intervals are only useful for strictly
  feasible packings.

How sign decisions are made (representation 1)
----------------------------------------------
For an algebraic real `a`, `sign_of(a)` is decided as:

  1. Cheap exact path: if `a` is a rational number, read off its sign.
  2. Enclose `a` in a rational interval at moderate precision using exact integer
     root extraction (`math.isqrt` / integer n-th root).  If the enclosure excludes
     0, the sign is decided -- rigorously, because the enclosure is guaranteed to
     contain `a`.
  3. Otherwise run an *exact* zero test: `a == 0` iff the minimal polynomial of `a`
     over Q is the polynomial `x`.  This is a decision procedure, not a heuristic.
  4. If `a != 0`, go back to step 2 with repeatedly doubled precision.  This
     terminates because the enclosure width goes to 0 while `|a| > 0` is fixed.

At no point is a Python `float` created, and at no point is "close to zero" treated
as "zero".  If a sign genuinely cannot be decided (an unsupported expression, or the
precision ceiling is hit), the module raises `UndecidedSign` rather than guessing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

import sympy

__all__ = [
    "UndecidedSign",
    "UnsupportedExpression",
    "RatInterval",
    "sign_of",
    "is_nonneg",
    "is_exactly_zero",
    "iroot",
    "SQRT3",
]

SQRT3 = sympy.sqrt(3)

# Precision ladder for interval refinement, in bits of the dyadic denominator.
_START_BITS = 64
_MAX_BITS = 1 << 16  # 65536 bits; far beyond anything a real certificate needs.


class UndecidedSign(Exception):
    """Raised when a sign could not be decided exactly. Never returned as a guess."""


class UnsupportedExpression(Exception):
    """Raised for input this module refuses to interpret (e.g. a float literal)."""


# --------------------------------------------------------------------------- #
# Exact integer roots -- the only "numeric" primitive, and it is exact.
# --------------------------------------------------------------------------- #

def iroot(a: int, n: int) -> int:
    """Exact floor(a ** (1/n)) for integers a >= 0, n >= 1. No floats."""
    if a < 0:
        raise ValueError("iroot of a negative integer")
    if n < 1:
        raise ValueError("iroot needs n >= 1")
    if n == 1:
        return a
    if n == 2:
        return math.isqrt(a)
    if a == 0:
        return 0
    # Newton iteration on integers, started from a safe over-estimate.
    x = 1 << ((a.bit_length() + n - 1) // n + 1)
    while True:
        y = ((n - 1) * x + a // x ** (n - 1)) // n
        if y >= x:
            break
        x = y
    while x ** n > a:
        x -= 1
    while (x + 1) ** n <= a:
        x += 1
    return x


def _root_bounds(f: Fraction, n: int, bits: int) -> tuple[Fraction, Fraction]:
    """Rational lo <= f**(1/n) <= hi, for f >= 0, with dyadic granularity 2**-bits."""
    if f < 0:
        raise UnsupportedExpression(f"even/rational root of a negative value: {f}")
    if f == 0:
        return Fraction(0), Fraction(0)
    scale = 1 << bits
    # floor( (f * scale**n) ** (1/n) ) == floor( floor(f * scale**n) ** (1/n) )
    inner = (f.numerator * scale**n) // f.denominator
    t = iroot(inner, n)
    return Fraction(t, scale), Fraction(t + 1, scale)


# --------------------------------------------------------------------------- #
# Rigorous rational intervals
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class RatInterval:
    """A closed interval [lo, hi] with exact Fraction endpoints.

    Every operation rounds outward, so the result always encloses the true value.
    Endpoints are `Fraction`; no float ever enters.
    """

    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError(f"empty interval [{self.lo}, {self.hi}]")

    @staticmethod
    def exact(value) -> "RatInterval":
        f = Fraction(value)
        return RatInterval(f, f)

    def __add__(self, other: "RatInterval") -> "RatInterval":
        other = _as_interval(other)
        return RatInterval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "RatInterval":
        return RatInterval(-self.hi, -self.lo)

    def __sub__(self, other: "RatInterval") -> "RatInterval":
        return self + (-_as_interval(other))

    def __rsub__(self, other) -> "RatInterval":
        return _as_interval(other) + (-self)

    def __mul__(self, other: "RatInterval") -> "RatInterval":
        other = _as_interval(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return RatInterval(min(products), max(products))

    __rmul__ = __mul__

    def __pow__(self, k: int) -> "RatInterval":
        if not isinstance(k, int) or k < 0:
            raise UnsupportedExpression("RatInterval supports non-negative integer powers only")
        result = RatInterval.exact(1)
        for _ in range(k):
            result = result * self
        return result

    def contains_zero(self) -> bool:
        return self.lo <= 0 <= self.hi

    def width(self) -> Fraction:
        return self.hi - self.lo


def _as_interval(x) -> RatInterval:
    if isinstance(x, RatInterval):
        return x
    return RatInterval.exact(x)


# --------------------------------------------------------------------------- #
# Enclosing a symbolic algebraic number in a rational interval
# --------------------------------------------------------------------------- #

def enclose(expr: sympy.Expr, bits: int) -> RatInterval:
    """Rigorous rational enclosure of a real algebraic `expr`, granularity 2**-bits.

    Recurses over the sympy expression tree. Only integers, rationals, sums,
    products and rational powers are accepted; anything else raises
    `UnsupportedExpression` rather than being approximated.
    """
    expr = sympy.sympify(expr)

    if isinstance(expr, sympy.Float):
        raise UnsupportedExpression(
            "float literal in the verification path; certificates must be exact"
        )
    if expr.is_Rational:
        return RatInterval.exact(Fraction(int(expr.p), int(expr.q)))
    if expr.is_Integer:
        return RatInterval.exact(Fraction(int(expr)))
    if expr.is_Add:
        acc = RatInterval.exact(0)
        for term in expr.args:
            acc = acc + enclose(term, bits)
        return acc
    if expr.is_Mul:
        acc = RatInterval.exact(1)
        for factor in expr.args:
            acc = acc * enclose(factor, bits)
        return acc
    if expr.is_Pow:
        base, exponent = expr.args
        if not exponent.is_Rational:
            raise UnsupportedExpression(f"non-rational exponent in {expr}")
        p, q = int(exponent.p), int(exponent.q)
        base_iv = enclose(base, bits + 8)
        if q != 1:
            if base_iv.lo < 0:
                # Either the base is genuinely negative (a non-real root, which a
                # coordinate must not be) or the enclosure is too coarse to tell.
                if sign_of(base) < 0:
                    raise UnsupportedExpression(f"non-real radical: {expr}")
                base_iv = RatInterval(Fraction(0), base_iv.hi)
            lo, _ = _root_bounds(base_iv.lo, q, bits + 8)
            _, hi = _root_bounds(base_iv.hi, q, bits + 8)
            base_iv = RatInterval(lo, hi)
        if p >= 0:
            return base_iv**p
        if base_iv.contains_zero():
            raise UndecidedSign(f"cannot invert an interval containing 0: {expr}")
        inv = RatInterval(1 / base_iv.hi, 1 / base_iv.lo)
        return inv ** (-p)

    raise UnsupportedExpression(f"unsupported expression for exact enclosure: {expr}")


# --------------------------------------------------------------------------- #
# Exact zero test and sign decision
# --------------------------------------------------------------------------- #

_X = sympy.Symbol("_zero_test_x")


def is_exactly_zero(expr: sympy.Expr) -> bool:
    """Decide `expr == 0` exactly for an algebraic `expr`.

    `sympy.minimal_polynomial(a)` is the monic generator of the ideal of rational
    polynomials vanishing at `a`; it equals `x` exactly when `a == 0`. This is a
    decision procedure, so the answer is a proof, not evidence.
    """
    expr = sympy.sympify(expr)
    expanded = sympy.expand(expr)
    if expanded.is_Number:
        return bool(expanded == 0)
    if expanded == sympy.Integer(0):
        return True
    return sympy.minimal_polynomial(expanded, _X) == _X


def sign_of(expr: sympy.Expr) -> int:
    """Exact sign of a real algebraic number: -1, 0 or +1.

    Raises `UndecidedSign` rather than returning a guess.
    """
    expr = sympy.sympify(expr)
    if isinstance(expr, sympy.Float):
        raise UnsupportedExpression(
            "float literal in the verification path; certificates must be exact"
        )
    if expr.is_Rational or expr.is_Integer:
        value = Fraction(int(expr.p), int(expr.q)) if expr.is_Rational else Fraction(int(expr))
        return (value > 0) - (value < 0)

    bits = _START_BITS
    iv = enclose(expr, bits)
    if iv.lo > 0:
        return 1
    if iv.hi < 0:
        return -1

    # Inconclusive at low precision: settle the equality case exactly, once.
    if is_exactly_zero(expr):
        return 0

    # Non-zero, so refinement is guaranteed to separate it from 0.
    while bits <= _MAX_BITS:
        bits *= 2
        iv = enclose(expr, bits)
        if iv.lo > 0:
            return 1
        if iv.hi < 0:
            return -1
    raise UndecidedSign(f"sign undecided at {_MAX_BITS} bits: {expr}")


def is_nonneg(value) -> bool:
    """True iff `value >= 0` is *certified*.

    Accepts either a symbolic algebraic number (decided exactly) or a
    `RatInterval` (certified only if the whole enclosure is >= 0 -- conservative).
    """
    if isinstance(value, RatInterval):
        return value.lo >= 0
    return sign_of(value) >= 0
