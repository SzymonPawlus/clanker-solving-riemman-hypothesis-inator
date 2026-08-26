"""EXACT check, in Q(sqrt 3), of the 22-point unit-separation lattice witness in T(a), a < 6.

This is the matching LOWER bound for the certified upper bound in certify.py:
the max over unit-separation lattices of |Lambda cap T(a)| for a < 6 is >= 22.
No floats are used in any accept/reject decision.  STATUS: numerical (a construction).
"""
from fractions import Fraction as F
import json, sys


class Q3:
    """p + q*sqrt(3) with p, q rational.  Exact."""
    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = F(p); self.q = F(q)

    def __add__(s, o): o = _c(o); return Q3(s.p + o.p, s.q + o.q)
    def __sub__(s, o): o = _c(o); return Q3(s.p - o.p, s.q - o.q)
    def __neg__(s): return Q3(-s.p, -s.q)
    __radd__ = __add__
    def __rsub__(s, o): return _c(o) - s
    def __mul__(s, o):
        o = _c(o)
        return Q3(s.p * o.p + 3 * s.q * o.q, s.p * o.q + s.q * o.p)
    __rmul__ = __mul__
    def sgn(s):
        """Exact sign of p + q sqrt3."""
        p, q = s.p, s.q
        if p == 0 and q == 0: return 0
        if p >= 0 and q >= 0: return 1
        if p <= 0 and q <= 0: return -1
        # opposite signs: compare p^2 with 3 q^2
        d = p * p - 3 * q * q
        if p > 0:                    # q < 0 : positive iff p^2 > 3q^2
            return 1 if d > 0 else (-1 if d < 0 else 0)
        return -1 if d > 0 else (1 if d < 0 else 0)
    def __ge__(s, o): return (s - _c(o)).sgn() >= 0
    def __repr__(s): return "(%s + %s*sqrt3)" % (s.p, s.q)


def _c(o):
    return o if isinstance(o, Q3) else Q3(o, 0)


SQ3 = Q3(0, 1)
HALF_SQ3 = Q3(0, F(1, 2))


def build(cos_p, cos_q, sin_p, sin_q, alpha, beta, a, rng=9):
    """cos phi = cos_p/cos_q, sin phi = sin_p/sin_q (exact rationals, a Pythagorean pair).
    Lattice: v1 = (cos, sin) (length 1), v2 = v1/2 + (sqrt3/2)*(-sin, cos)  (hexagonal, lambda_1 = 1).
    Returns the list of lattice points inside the closed T(a)."""
    c = Q3(F(cos_p, cos_q)); s = Q3(F(sin_p, sin_q))
    assert F(cos_p, cos_q) ** 2 + F(sin_p, sin_q) ** 2 == 1, "not a unit vector"
    v1 = (c, s)
    v2 = (c * F(1, 2) - HALF_SQ3 * s, s * F(1, 2) + HALF_SQ3 * c)
    A = Q3(a)
    pts = []
    for i in range(-rng, rng + 1):
        for j in range(-rng, rng + 1):
            u = Q3(F(alpha) + i); v = Q3(F(beta) + j)
            X = u * v1[0] + v * v2[0]
            Y = u * v1[1] + v * v2[1]
            sq3X = Q3(3 * X.q, X.p)          # sqrt3 * X
            if Y.sgn() >= 0 and (sq3X - Y).sgn() >= 0 and (Q3(3 * (A - X).q, (A - X).p) - Y).sgn() >= 0:
                pts.append(((i, j), X, Y))
    return pts


def min_sq_distance(pts):
    """Exact min squared pairwise distance (must be >= 1)."""
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx = pts[i][1] - pts[j][1]; dy = pts[i][2] - pts[j][2]
            d2 = dx * dx + dy * dy
            if best is None or (best - d2).sgn() > 0:
                best = d2
    return best


if __name__ == "__main__":
    # phi = 2 arctan(6/23):  cos = 493/565, sin = 276/565  (493^2 + 276^2 = 565^2)
    a = F(5999, 1000)
    pts = build(493, 565, 276, 565, F(1, 20), F(1, 20), a)
    print("a =", a, "=", float(a), " (a < 6:", a < 6, ")")
    print("points in closed T(a):", len(pts))
    m = min_sq_distance(pts)
    print("exact min squared pairwise distance:", m, "=", float(m.p + m.q * 3 ** 0.5))
    print("separation >= 1 :", (m - 1).sgn() >= 0)
    json.dump({"a": [a.numerator, a.denominator], "count": len(pts),
               "cos": [493, 565], "sin": [276, 565], "alpha": [1, 20], "beta": [1, 20],
               "min_sq_dist": [str(m.p), str(m.q)],
               "indices": [p[0] for p in pts]},
              open("out/exact_witness22.json", "w"), indent=1)
