"""Outward-rounded interval arithmetic over IEEE-754 binary64.

Floating-point model (this is the assumption the rigour of every bound here rests on):

* Python ``float`` is IEEE-754 binary64.
* ``+``, ``-``, ``*``, ``/`` and ``math.sqrt`` are *correctly rounded* under the current
  rounding mode, which CPython never changes from round-to-nearest-ties-to-even.
* Under round-to-nearest, the true real result ``t`` of one such operation and its
  rounded value ``fl(t)`` satisfy ``nextafter(fl(t), -inf) <= t <= nextafter(fl(t), +inf)``.
  (In fact ``|t - fl(t)| <= ulp/2``, so one ulp outward is strictly conservative.)

So every operation below computes the endpoint in binary64 and then pushes it one ulp
*outward* with :func:`math.nextafter`.  The resulting interval provably contains the exact
real result.  Widening is never optional and never skipped: a routine that returns a
narrower interval than the maths permits is the one bug that would silently invalidate an
exhaustion proof, so the code errs outward everywhere, including on exactly representable
inputs where the widening is merely wasteful.

Intervals are only ever used here to bound the *algebraic constants* d(k) (see
``cpbnb/caps.py``).  The branch-and-bound geometry itself runs in exact integer arithmetic
(``cpbnb/lattice.py``) and touches no floating point at all.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

_INF = math.inf


def _down(x: float) -> float:
    return math.nextafter(x, -_INF)


def _up(x: float) -> float:
    return math.nextafter(x, _INF)


@dataclass(frozen=True)
class Interval:
    """A closed real interval ``[lo, hi]`` with binary64 endpoints, ``lo <= hi``."""

    lo: float
    hi: float

    def __post_init__(self) -> None:
        if math.isnan(self.lo) or math.isnan(self.hi):
            raise ValueError("NaN endpoint")
        if self.lo > self.hi:
            raise ValueError(f"empty interval [{self.lo}, {self.hi}]")

    # -- constructors ----------------------------------------------------------

    @staticmethod
    def exact(x: float) -> "Interval":
        """The degenerate interval at an exactly representable value."""
        return Interval(float(x), float(x))

    @staticmethod
    def from_int(k: int) -> "Interval":
        f = float(k)
        if int(f) == k:
            return Interval(f, f)
        return Interval(_down(f), _up(f))

    # -- arithmetic ------------------------------------------------------------

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(_down(self.lo + other.lo), _up(self.hi + other.hi))

    def __sub__(self, other: "Interval") -> "Interval":
        return Interval(_down(self.lo - other.hi), _up(self.hi - other.lo))

    def __mul__(self, other: "Interval") -> "Interval":
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(_down(min(products)), _up(max(products)))

    def __truediv__(self, other: "Interval") -> "Interval":
        if other.lo <= 0.0 <= other.hi:
            raise ZeroDivisionError("interval divisor straddles zero")
        quotients = (
            self.lo / other.lo,
            self.lo / other.hi,
            self.hi / other.lo,
            self.hi / other.hi,
        )
        return Interval(_down(min(quotients)), _up(max(quotients)))

    def sqrt(self) -> "Interval":
        if self.lo < 0.0:
            raise ValueError("sqrt of an interval containing negative reals")
        return Interval(_down(math.sqrt(self.lo)), _up(math.sqrt(self.hi)))

    # -- comparison ------------------------------------------------------------

    def gt_fraction(self, q: Fraction) -> bool:
        """``True`` only if *every* real in this interval is ``> q``.

        Compared exactly: ``self.lo`` is a binary64 and therefore an exact rational, so
        ``Fraction(self.lo) > q`` decides the question with no rounding of its own.
        """
        return Fraction(self.lo) > q

    def lt_fraction(self, q: Fraction) -> bool:
        """``True`` only if *every* real in this interval is ``< q``."""
        return Fraction(self.hi) < q

    def width(self) -> float:
        return _up(self.hi - self.lo)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"[{self.lo!r}, {self.hi!r}]"


def isqrt_interval(k: int) -> Interval:
    """Rigorous enclosure of ``sqrt(k)`` for a non-negative integer ``k``."""
    if k < 0:
        raise ValueError("negative radicand")
    return Interval.from_int(k).sqrt()
