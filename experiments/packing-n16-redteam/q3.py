"""Exact arithmetic in Q(sqrt3): x = p + q*sqrt3 with p,q Fraction."""
from fractions import Fraction as F

class Q3:
    __slots__ = ("p", "q")
    def __init__(self, p=0, q=0):
        self.p = F(p); self.q = F(q)
    def __add__(s, o):
        o = q3(o); return Q3(s.p + o.p, s.q + o.q)
    __radd__ = __add__
    def __neg__(s): return Q3(-s.p, -s.q)
    def __sub__(s, o): return s + (-q3(o))
    def __rsub__(s, o): return q3(o) + (-s)
    def __mul__(s, o):
        o = q3(o); return Q3(s.p*o.p + 3*s.q*o.q, s.p*o.q + s.q*o.p)
    __rmul__ = __mul__
    def inv(s):
        d = s.p*s.p - 3*s.q*s.q
        assert d != 0
        return Q3(s.p/d, -s.q/d)
    def __truediv__(s, o): return s * q3(o).inv()
    def __rtruediv__(s, o): return q3(o) * s.inv()
    def sign(s):
        # sign of p + q*sqrt3, exact
        if s.p == 0 and s.q == 0: return 0
        if s.p >= 0 and s.q >= 0: return 1
        if s.p <= 0 and s.q <= 0: return -1
        # opposite signs: compare p^2 vs 3q^2
        if s.p > 0:  # q < 0 : p + q sqrt3 >0 iff p^2 > 3q^2
            return 1 if s.p*s.p > 3*s.q*s.q else (-1 if s.p*s.p < 3*s.q*s.q else 0)
        else:        # p < 0, q > 0
            return 1 if 3*s.q*s.q > s.p*s.p else (-1 if 3*s.q*s.q < s.p*s.p else 0)
    def __eq__(s, o): return (s - q3(o)).sign() == 0
    def __lt__(s, o): return (s - q3(o)).sign() < 0
    def __le__(s, o): return (s - q3(o)).sign() <= 0
    def __gt__(s, o): return (s - q3(o)).sign() > 0
    def __ge__(s, o): return (s - q3(o)).sign() >= 0
    def __hash__(s): return hash((s.p, s.q))
    def __float__(s): return float(s.p) + float(s.q)*(3**0.5)
    def __repr__(s): return f"({s.p}+{s.q}r3)"

def q3(x):
    if isinstance(x, Q3): return x
    return Q3(F(x), 0)

R = Q3(0, 1)   # sqrt3
