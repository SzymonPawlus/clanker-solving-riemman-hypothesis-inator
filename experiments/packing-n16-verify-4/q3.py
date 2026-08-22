"""Exact arithmetic in Q(sqrt 3), written for verification worker V4 (issue #97).

Independent of experiments/packing-n16-structure/ and packing-n16-covering-2/ --
no code from either was read or imported.  Standard library only.
"""
from fractions import Fraction as F


class Q3:
    """p + q*sqrt(3) with p, q rational.  A field: sqrt(3) is irrational, so
    p + q*sqrt3 == 0 iff p == q == 0, and the norm p^2 - 3q^2 vanishes only there."""

    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = F(p)
        self.q = F(q)

    # --- ring ops -----------------------------------------------------
    def __add__(self, o):
        o = _co(o)
        return Q3(self.p + o.p, self.q + o.q)

    def __radd__(self, o):
        return _co(o) + self

    def __neg__(self):
        return Q3(-self.p, -self.q)

    def __sub__(self, o):
        return self + (-_co(o))

    def __rsub__(self, o):
        return _co(o) - self

    def __mul__(self, o):
        o = _co(o)
        return Q3(self.p * o.p + 3 * self.q * o.q, self.p * o.q + self.q * o.p)

    __rmul__ = __mul__

    def inv(self):
        n = self.p * self.p - 3 * self.q * self.q
        if n == 0:
            raise ZeroDivisionError("Q3 inverse of 0")
        return Q3(self.p / n, -self.q / n)

    def __truediv__(self, o):
        return self * _co(o).inv()

    def __rtruediv__(self, o):
        return _co(o) * self.inv()

    # --- exact ordering ----------------------------------------------
    def sign(self):
        """Exact sign of p + q*sqrt3, decided by rational comparison only."""
        p, q = self.p, self.q
        if p == 0 and q == 0:
            return 0
        if p == 0:
            return 1 if q > 0 else -1
        if q == 0:
            return 1 if p > 0 else -1
        if p > 0 and q > 0:
            return 1
        if p < 0 and q < 0:
            return -1
        # opposite signs: compare p^2 with 3 q^2, sign follows the larger term
        d = p * p - 3 * q * q          # >0 => |p| dominates
        if p > 0:                      # q < 0 : positive iff p^2 > 3 q^2
            return 1 if d > 0 else (-1 if d < 0 else 0)
        else:                          # p < 0, q > 0 : positive iff 3q^2 > p^2
            return -1 if d > 0 else (1 if d < 0 else 0)

    def __eq__(self, o):
        o = _co(o)
        return self.p == o.p and self.q == o.q

    def __hash__(self):
        return hash((self.p, self.q))

    def __lt__(self, o):
        return (self - _co(o)).sign() < 0

    def __le__(self, o):
        return (self - _co(o)).sign() <= 0

    def __gt__(self, o):
        return (self - _co(o)).sign() > 0

    def __ge__(self, o):
        return (self - _co(o)).sign() >= 0

    def approx(self):
        # printing / seeding only; never decides anything
        return float(self.p) + float(self.q) * 1.7320508075688772

    def __repr__(self):
        return f"({self.p}+{self.q}r3)"


def _co(o):
    return o if isinstance(o, Q3) else Q3(o, 0)


R3 = Q3(0, 1)          # sqrt 3
ZERO = Q3(0, 0)
ONE = Q3(1, 0)


def floor_q3(x):
    """Exact floor of a Q3 number: seed with float, then confirm by exact signs."""
    k = int(x.approx() // 1)
    while not Q3(k, 0) <= x:
        k -= 1
    while Q3(k + 1, 0) <= x:
        k += 1
    assert Q3(k, 0) <= x < Q3(k + 1, 0)
    return k


if __name__ == "__main__":
    # sign self-test on the mixed-sign cases where a naive implementation fails
    cases = [(Q3(2, -1), 1), (Q3(1, -1), -1), (Q3(-3, 2), 1), (Q3(-7, 4), -1),
             (Q3(0, 0), 0), (Q3(F(-5, 2), F(3, 2)), 1), (Q3(F(5, 2), F(-3, 2)), -1),
             (Q3(3, -F(3, 1)), -1), (Q3(-1, 1), 1)]
    for x, s in cases:
        got = x.sign()
        assert got == s, (x, got, s)
        assert abs(x.approx()) < 1e-12 or (got > 0) == (x.approx() > 0), x
    # field ops
    assert (R3 * R3) == Q3(3, 0)
    assert (Q3(1, 1) * Q3(1, -1)) == Q3(-2, 0)
    assert (ONE / R3) == Q3(0, F(1, 3))
    assert floor_q3(Q3(0, 2)) == 3 and floor_q3(Q3(1, 2)) == 4 and floor_q3(Q3(4, 0)) == 4
    assert floor_q3(Q3(0, -2)) == -4
    print("q3 self-test: OK")
