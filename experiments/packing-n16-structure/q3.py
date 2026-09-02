"""Exact arithmetic in Q(sqrt3): numbers p + q*sqrt(3), p,q rational.

Every comparison below is decided exactly.  No float appears anywhere in this
module.  Written for the n=16 structure theorem (attacks/n16-structure/).
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = F(p)
        self.q = F(q)

    def __add__(s, o):
        o = q3(o)
        return Q3(s.p + o.p, s.q + o.q)

    __radd__ = __add__

    def __neg__(s):
        return Q3(-s.p, -s.q)

    def __sub__(s, o):
        return s + (-q3(o))

    def __rsub__(s, o):
        return q3(o) + (-s)

    def __mul__(s, o):
        o = q3(o)
        # (a+b r)(c+d r) = ac + 3bd + (ad+bc) r,  r^2 = 3
        return Q3(s.p * o.p + 3 * s.q * o.q, s.p * o.q + s.q * o.p)

    __rmul__ = __mul__

    def inv(s):
        # 1/(p+q r) = (p - q r)/(p^2 - 3 q^2)
        d = s.p * s.p - 3 * s.q * s.q
        assert d != 0, "zero divisor in Q(sqrt3)"
        return Q3(s.p / d, -s.q / d)

    def __truediv__(s, o):
        return s * q3(o).inv()

    def sign(s):
        """Exact sign of p + q*sqrt(3)."""
        if s.p == 0 and s.q == 0:
            return 0
        if s.p >= 0 and s.q >= 0:
            return 1
        if s.p <= 0 and s.q <= 0:
            return -1
        # opposite signs: compare p^2 with 3 q^2, sign follows the larger term
        d = s.p * s.p - 3 * s.q * s.q
        if s.p > 0:          # q < 0: positive iff p^2 > 3q^2
            return 1 if d > 0 else (-1 if d < 0 else 0)
        else:                # p < 0, q > 0: positive iff 3q^2 > p^2
            return -1 if d > 0 else (1 if d < 0 else 0)

    def __eq__(s, o):
        return (s - q3(o)).sign() == 0

    def __lt__(s, o):
        return (s - q3(o)).sign() < 0

    def __le__(s, o):
        return (s - q3(o)).sign() <= 0

    def __gt__(s, o):
        return (s - q3(o)).sign() > 0

    def __ge__(s, o):
        return (s - q3(o)).sign() >= 0

    def __hash__(s):
        return hash((s.p, s.q))

    def __repr__(s):
        return f"({s.p}+{s.q}r)"

    def approx(s):
        return float(s.p) + float(s.q) * 1.7320508075688772


def q3(x):
    return x if isinstance(x, Q3) else Q3(x, 0)


R = Q3(0, 1)      # sqrt(3)
ZERO, ONE = Q3(0), Q3(1)
