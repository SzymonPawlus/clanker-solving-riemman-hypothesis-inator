"""Exact arithmetic in Q(sqrt 3), written for worker V3's independent check.

A value is p + q*sqrt(3) with p, q in Fraction.  Nothing here is imported from or
adapted from any existing certifier in this repository; it is written from the
problem statement in problems/circle-packing-equilateral-triangle/README.md.
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = F(p)
        self.q = F(q)

    # --- field ops -------------------------------------------------------
    def __add__(self, o):
        o = q3(o)
        return Q3(self.p + o.p, self.q + o.q)

    def __radd__(self, o):
        return self + o

    def __neg__(self):
        return Q3(-self.p, -self.q)

    def __sub__(self, o):
        return self + (-q3(o))

    def __rsub__(self, o):
        return q3(o) + (-self)

    def __mul__(self, o):
        o = q3(o)
        return Q3(self.p * o.p + 3 * self.q * o.q, self.p * o.q + self.q * o.p)

    __rmul__ = __mul__

    def inv(self):
        d = self.p * self.p - 3 * self.q * self.q
        if d == 0:
            raise ZeroDivisionError
        return Q3(self.p / d, -self.q / d)

    def __truediv__(self, o):
        return self * q3(o).inv()

    def __rtruediv__(self, o):
        return q3(o) * self.inv()

    # --- ordering (exact) ------------------------------------------------
    def sign(self):
        p, q = self.p, self.q
        if p == 0 and q == 0:
            return 0
        if p >= 0 and q >= 0:
            return 1
        if p <= 0 and q <= 0:
            return -1
        # mixed signs: compare p^2 with 3 q^2
        if p > 0:          # q < 0 ; positive iff p^2 > 3 q^2
            return 1 if p * p > 3 * q * q else (-1 if p * p < 3 * q * q else 0)
        else:              # p < 0, q > 0 ; positive iff 3 q^2 > p^2
            return 1 if 3 * q * q > p * p else (-1 if 3 * q * q < p * p else 0)

    def __eq__(self, o):
        return (self - q3(o)).sign() == 0

    def __lt__(self, o):
        return (self - q3(o)).sign() < 0

    def __le__(self, o):
        return (self - q3(o)).sign() <= 0

    def __gt__(self, o):
        return (self - q3(o)).sign() > 0

    def __ge__(self, o):
        return (self - q3(o)).sign() >= 0

    def __hash__(self):
        return hash((self.p, self.q))

    def __float__(self):
        return float(self.p) + float(self.q) * 3.0 ** 0.5

    def __repr__(self):
        return f"({self.p}+{self.q}r3)"


def q3(x):
    if isinstance(x, Q3):
        return x
    return Q3(F(x), 0)


ZERO = Q3(0, 0)
ONE = Q3(1, 0)
R3 = Q3(0, 1)


def parse_exact(tok):
    """Parse an exact scalar.  Accepts an int, a Fraction, a string 'p/q',
    or a two-element [p, q] meaning p + q*sqrt(3).  DECIMAL STRINGS ARE
    REJECTED (problem RULES.md section 2)."""
    if isinstance(tok, (list, tuple)):
        if len(tok) != 2:
            raise ValueError("exact scalar must be [p, q]")
        return Q3(_rat(tok[0]), _rat(tok[1]))
    return Q3(_rat(tok), 0)


def _rat(t):
    if isinstance(t, F):
        return t
    if isinstance(t, int):
        return F(t)
    if isinstance(t, float):
        raise ValueError("bare float in exact field")
    s = str(t).strip()
    if "." in s or "e" in s.lower():
        raise ValueError(f"decimal string {s!r} in exact field: banned by RULES.md s2")
    return F(s)
