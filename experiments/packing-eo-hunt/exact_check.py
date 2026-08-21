"""The exact gate. A float configuration is a hypothesis; this decides.

Two independent exact representations are implemented on purpose, because the single most likely
cause of a "counterexample" is an infeasible configuration that a float check waves through
(problem ``RULES.md`` SS0, SS4).

Checker 1 -- barycentric, pure Q
--------------------------------
Write each point by its barycentric coordinates ``(l0, l1, l2)``, ``l_i >= 0``, ``sum l_i = 1``,
with respect to the equilateral triangle of side ``a``. Containment is then *literally*
``l_i >= 0`` -- no irrational enters. For two points with barycentric difference
``u = lP - lQ`` (so ``u0 + u1 + u2 = 0``), the standard barycentric distance formula for a
triangle with side lengths ``a0 = a1 = a2 = a`` gives

    |P - Q|^2 = -( a^2 u1 u2 + a^2 u2 u0 + a^2 u0 u1 ) = -a^2 * (u0u1 + u1u2 + u2u0),

and since ``(u0+u1+u2)^2 = 0`` forces ``u0u1 + u1u2 + u2u0 = -(u0^2+u1^2+u2^2)/2``,

    |P - Q|^2 = a^2 * (u0^2 + u1^2 + u2^2) / 2.

Everything is rational when the ``l_i`` and ``a^2`` are. So, with ``q_min`` the minimum of
``(u0^2+u1^2+u2^2)/2`` over all pairs, the least side admitting this configuration at separation
1 is ``a = 1/sqrt(q_min)``, and

    Erdos-Oler(k) is refuted by this configuration  <=>  q_min > 1/(k-1)^2   (exact rational test).

Checker 2 -- Cartesian over Q(sqrt 3)
-------------------------------------
Independent of checker 1: coordinates ``x = p + q*sqrt(3)`` with ``p, q`` rational, exact sign
decision for ``p + q*sqrt(3)``, containment as the three half-plane inequalities, squared
distances in Q(sqrt 3) compared against the separation. Written from the geometry, not from
checker 1's formula. Agreement of the two is the point; disagreement is a finding to investigate,
never something to average (problem ``RULES.md`` SS3).
"""

from __future__ import annotations

import math
from fractions import Fraction as F

SQRT3 = math.sqrt(3.0)


# ------------------------------------------------------------------ rationalisation

def to_rational_barycentric(points, max_den: int = 10**7):
    """Float Cartesian points in the unit triangle -> exact rational barycentric triples.

    The rounding is *not* assumed harmless: the caller must re-run the separation test on the
    rounded points. Rounding always lands inside the closed triangle (negatives are clamped and
    the triple renormalised), so containment is exact by construction and only the separation can
    fail."""
    out = []
    for x, y in points:
        l2 = F(y / (SQRT3 / 2.0)).limit_denominator(max_den)
        l1 = F(x - y / SQRT3).limit_denominator(max_den)
        if l1 < 0:
            l1 = F(0)
        if l2 < 0:
            l2 = F(0)
        if l1 + l2 > 1:
            s = l1 + l2
            l1, l2 = l1 / s, l2 / s
        l0 = 1 - l1 - l2
        out.append((l0, l1, l2))
    return out


# ------------------------------------------------------------------ checker 1

def check_barycentric(bary, k=None):
    """Returns a dict. ``q_min`` is exact; ``a_min = 1/sqrt(q_min)`` is the least side of an
    equilateral triangle holding these points at separation >= 1."""
    n = len(bary)
    for l in bary:
        assert sum(l) == 1, "barycentric triple does not sum to 1"
    contained = all(all(c >= 0 for c in l) for l in bary)
    q_min = None
    arg = None
    for i in range(n):
        for j in range(i + 1, n):
            u = tuple(bary[i][t] - bary[j][t] for t in range(3))
            q = (u[0] * u[0] + u[1] * u[1] + u[2] * u[2]) / 2
            if q_min is None or q < q_min:
                q_min, arg = q, (i, j)
    res = {
        "n": n,
        "contained_exact": contained,
        "q_min": q_min,
        "closest_pair": arg,
        "a_min_float": float(1.0 / math.sqrt(float(q_min))) if q_min else None,
    }
    if k is not None:
        thr = F(1, (k - 1) ** 2)
        res["k"] = k
        res["threshold_q"] = thr
        res["refutes_EO"] = bool(contained and q_min > thr)
        res["margin_q"] = q_min - thr
    return res


# ------------------------------------------------------------------ Q(sqrt 3) arithmetic

class S3:
    """p + q*sqrt(3) with p, q rational. Exact comparisons."""

    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p = F(p)
        self.q = F(q)

    def __add__(self, o):
        o = o if isinstance(o, S3) else S3(o)
        return S3(self.p + o.p, self.q + o.q)

    def __sub__(self, o):
        o = o if isinstance(o, S3) else S3(o)
        return S3(self.p - o.p, self.q - o.q)

    def __mul__(self, o):
        o = o if isinstance(o, S3) else S3(o)
        return S3(self.p * o.p + 3 * self.q * o.q, self.p * o.q + self.q * o.p)

    __rmul__ = __mul__

    def sign(self):
        """Exact sign of p + q*sqrt(3), by squaring rather than by evaluating sqrt(3)."""
        p, q = self.p, self.q
        if p == 0 and q == 0:
            return 0
        if p >= 0 and q >= 0:
            return 1
        if p <= 0 and q <= 0:
            return -1
        # opposite signs: compare p^2 with 3 q^2
        if p > 0:  # q < 0, value = p - |q|sqrt3
            d = p * p - 3 * q * q
            return 1 if d > 0 else (0 if d == 0 else -1)
        d = 3 * q * q - p * p  # p < 0, q > 0
        return 1 if d > 0 else (0 if d == 0 else -1)

    def __ge__(self, o):
        return (self - (o if isinstance(o, S3) else S3(o))).sign() >= 0

    def __gt__(self, o):
        return (self - (o if isinstance(o, S3) else S3(o))).sign() > 0

    def __lt__(self, o):
        return (self - (o if isinstance(o, S3) else S3(o))).sign() < 0

    def __float__(self):
        return float(self.p) + float(self.q) * SQRT3

    def __repr__(self):
        return f"({self.p} + {self.q}*sqrt3)"


def check_cartesian(bary, a2, k=None):
    """Independent check: build Cartesian coordinates over Q(sqrt 3) for the triangle of side
    ``a`` with ``a^2 = a2`` rational -- vertices (0,0), (a,0), (a/2, a*sqrt(3)/2) -- and test the
    three half planes and all pairwise separations directly.

    To keep every coordinate in Q(sqrt 3) the side is taken rational, ``a = sqrt(a2)`` with a2 a
    rational square; callers pass ``a2 = a*a`` for rational ``a``."""
    a = F(a2)
    ra = a.numerator, a.denominator
    root = F(math.isqrt(ra[0] * ra[1]), ra[1]) if False else None
    # require a2 to be an exact rational square
    num_r = math.isqrt(a.numerator)
    den_r = math.isqrt(a.denominator)
    assert num_r * num_r == a.numerator and den_r * den_r == a.denominator, (
        "check_cartesian needs a rational side length (a^2 must be a rational square)"
    )
    side = F(num_r, den_r)
    V = [
        (S3(0), S3(0)),
        (S3(side), S3(0)),
        (S3(side / 2), S3(0, side / 2)),
    ]
    pts = []
    for l0, l1, l2 in bary:
        x = S3(l0) * V[0][0] + S3(l1) * V[1][0] + S3(l2) * V[2][0]
        y = S3(l0) * V[0][1] + S3(l1) * V[1][1] + S3(l2) * V[2][1]
        pts.append((x, y))
    # containment: y >= 0 ; sqrt3*x - y >= 0 ; sqrt3*(side - x) - y >= 0
    sqrt3 = S3(0, 1)
    ok = True
    for x, y in pts:
        if not (y.sign() >= 0):
            ok = False
        if not ((sqrt3 * x - y).sign() >= 0):
            ok = False
        if not ((sqrt3 * (S3(side) - x) - y).sign() >= 0):
            ok = False
    dmin2 = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            d2 = dx * dx + dy * dy
            if dmin2 is None or (d2 - dmin2).sign() < 0:
                dmin2 = d2
    res = {
        "side": side,
        "contained_exact": ok,
        "min_sq_distance": dmin2,
        "min_sq_distance_float": float(dmin2),
        "separation_at_least_1": bool(dmin2.sign() >= 0 and (dmin2 - S3(1)).sign() >= 0),
    }
    if k is not None:
        res["k"] = k
        res["side_below_k_minus_1"] = bool(side < k - 1)
        res["refutes_EO"] = bool(
            ok and res["separation_at_least_1"] and res["side_below_k_minus_1"]
        )
    return res


def gate(points, k, max_den: int = 10**7, verbose: bool = True):
    """Full gate on a float configuration in the *unit* triangle. Returns (verdict, detail)."""
    bary = to_rational_barycentric(points, max_den=max_den)
    r1 = check_barycentric(bary, k=k)
    detail = {"barycentric": r1}
    verdict = r1["refutes_EO"]
    if verdict:
        # cross-check at a rational side strictly between a_min and k-1
        a_lo = r1["a_min_float"]
        side = F(math.ceil(a_lo * 10**6), 10**6)
        while side * side < 1 / r1["q_min"]:
            side += F(1, 10**6)
        r2 = check_cartesian(bary, side * side, k=k)
        detail["cartesian"] = r2
        verdict = bool(r2["refutes_EO"])
        detail["checkers_agree"] = bool(r1["refutes_EO"] == r2["refutes_EO"])
    if verbose:
        print(f"exact gate: n={r1['n']} k={k} contained={r1['contained_exact']}")
        print(f"  q_min      = {r1['q_min']}")
        print(f"  a_min      = {r1['a_min_float']!r}  (need < {k - 1} to refute)")
        print(f"  verdict    = {'CANDIDATE COUNTEREXAMPLE' if verdict else 'no refutation'}")
    return verdict, detail
