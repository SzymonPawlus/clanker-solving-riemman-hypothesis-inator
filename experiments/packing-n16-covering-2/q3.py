"""Exact arithmetic in Q(sqrt 3), written for this attack by claude / worker C1.

An element is a + b*sqrt(3) with a,b exact Fractions.  Every comparison is decided
exactly: sign(a + b*sqrt3) is read off the signs of a and b when they agree, and from
sign(a^2 - 3b^2) when they differ.  No floats are consulted anywhere.
"""
from fractions import Fraction as F


class Q3:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a); self.b = F(b)

    @staticmethod
    def cast(x):
        return x if isinstance(x, Q3) else Q3(x, 0)

    def __add__(s, o):
        o = Q3.cast(o); return Q3(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __neg__(s):
        return Q3(-s.a, -s.b)

    def __sub__(s, o):
        return s + (-Q3.cast(o))

    def __rsub__(s, o):
        return Q3.cast(o) + (-s)

    def __mul__(s, o):
        o = Q3.cast(o)
        return Q3(s.a * o.a + 3 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        d = s.a * s.a - 3 * s.b * s.b
        if d == 0:
            raise ZeroDivisionError
        return Q3(s.a / d, -s.b / d)

    def __truediv__(s, o):
        return s * Q3.cast(o).inv()

    def __rtruediv__(s, o):
        return Q3.cast(o) * s.inv()

    def sign(s):
        a, b = s.a, s.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        c = a * a - 3 * b * b            # sign of a^2 - 3b^2 decides
        if c == 0:
            return 0
        return (1 if a > 0 else -1) if c > 0 else (-1 if a > 0 else 1)

    def __eq__(s, o):  return (s - Q3.cast(o)).sign() == 0
    def __ne__(s, o):  return (s - Q3.cast(o)).sign() != 0
    def __lt__(s, o):  return (s - Q3.cast(o)).sign() < 0
    def __le__(s, o):  return (s - Q3.cast(o)).sign() <= 0
    def __gt__(s, o):  return (s - Q3.cast(o)).sign() > 0
    def __ge__(s, o):  return (s - Q3.cast(o)).sign() >= 0
    def __hash__(s):   return hash((s.a, s.b))
    def __float__(s):  return float(s.a) + float(s.b) * 1.7320508075688772935

    def __repr__(s):
        if s.b == 0: return str(s.a)
        if s.a == 0: return "%s*r3" % s.b
        return "%s%+s*r3" % (s.a, s.b)


R3 = Q3(0, 1)
