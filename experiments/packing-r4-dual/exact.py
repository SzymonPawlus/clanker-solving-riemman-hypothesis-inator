"""Exact arithmetic and an exact LP dual-feasibility checker.

NO FLOATING POINT APPEARS IN ANY ACCEPT/REJECT DECISION IN THIS FILE.
Everything is `fractions.Fraction` and Python integers.

Three pieces:

  1. `Quad(D)` -- the ring Q(sqrt D) for a non-square positive integer D,
     elements p + q*sqrt(D) with p, q rational.  Exact equality and exact sign.
  2. `Surd3`   -- the field Q(sqrt 3), used only for the configuration geometry
     (areas of triangular-lattice polygons live there).
  3. `dual_certificate_value` -- given a rational LP

            minimise  c . x        subject to   A x >= b,  x >= 0

     and a candidate rational dual vector y >= 0, verify

            y >= 0,   A^T y <= c

     exactly, and return the dual objective y . b, which by weak duality is a
     rigorous LOWER bound on the primal optimum.  Rejection is a hard failure,
     never a tolerance.

Weak duality, stated so it can be checked rather than trusted:
    for any primal-feasible x and any dual-feasible y,
        c . x  >=  (A^T y) . x  =  y . (A x)  >=  y . b,
    the first step using x >= 0 and c >= A^T y, the second using y >= 0 and
    A x >= b.  Hence min c.x >= y.b.
"""

from fractions import Fraction as F


# ---------------------------------------------------------------- Q(sqrt D)

class Quad:
    """Element p + q*sqrt(D) of Q(sqrt D); D a positive non-square integer."""

    __slots__ = ("D", "p", "q")

    def __init__(self, D, p=0, q=0):
        self.D = D
        self.p = F(p)
        self.q = F(q)

    # -- ring operations ---------------------------------------------------
    def _co(self, o):
        if isinstance(o, Quad):
            assert o.D == self.D, "mixing different quadratic fields"
            return o
        return Quad(self.D, o, 0)

    def __add__(self, o):
        o = self._co(o)
        return Quad(self.D, self.p + o.p, self.q + o.q)

    __radd__ = __add__

    def __neg__(self):
        return Quad(self.D, -self.p, -self.q)

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) + (-self)

    def __mul__(self, o):
        o = self._co(o)
        return Quad(self.D,
                    self.p * o.p + self.D * self.q * o.q,
                    self.p * o.q + self.q * o.p)

    __rmul__ = __mul__

    def inv(self):
        den = self.p * self.p - self.D * self.q * self.q
        assert den != 0, "zero divisor"
        return Quad(self.D, self.p / den, -self.q / den)

    def __truediv__(self, o):
        return self * self._co(o).inv()

    def __rtruediv__(self, o):
        return self._co(o) * self.inv()

    def __eq__(self, o):
        o = self._co(o)
        return self.p == o.p and self.q == o.q

    def __repr__(self):
        return f"({self.p} + {self.q}*sqrt{self.D})"

    # -- exact sign --------------------------------------------------------
    def sign(self):
        """Exact sign of p + q sqrt(D).  sqrt(D) is irrational (D non-square),
        so the value vanishes iff p = q = 0."""
        p, q = self.p, self.q
        if p == 0 and q == 0:
            return 0
        if q == 0:
            return 1 if p > 0 else -1
        if p == 0:
            return 1 if q > 0 else -1
        if p > 0 and q > 0:
            return 1
        if p < 0 and q < 0:
            return -1
        # opposite signs: compare p^2 with D q^2 (never equal: D non-square)
        bigger = p * p > self.D * q * q
        if p > 0:                     # p > 0 > q sqrt D
            return 1 if bigger else -1
        return -1 if bigger else 1    # p < 0 < q sqrt D

    def __lt__(self, o):
        return (self - self._co(o)).sign() < 0

    def __le__(self, o):
        return (self - self._co(o)).sign() <= 0

    def __gt__(self, o):
        return (self - self._co(o)).sign() > 0

    def __ge__(self, o):
        return (self - self._co(o)).sign() >= 0

    def approx(self, digits=25):
        """Rational (lo, hi) enclosure.  For DISPLAY ONLY -- no decision in
        this repository is taken on the strength of this function's output."""
        lo, hi = sqrt_bounds(self.D, 10 ** digits)
        if self.q >= 0:
            return (self.p + self.q * lo, self.p + self.q * hi)
        return (self.p + self.q * hi, self.p + self.q * lo)


def sqrt_bounds(D, den=10 ** 40):
    """Certified rationals lo <= sqrt(D) <= hi with hi - lo = 1/den."""
    from math import isqrt
    r = isqrt(D * den * den)
    lo, hi = F(r, den), F(r + 1, den)
    assert lo * lo <= D <= hi * hi
    return lo, hi


def sqrt_up(x, den=10 ** 40):
    """Rational UPPER bound for sqrt(x), x a non-negative Fraction."""
    from math import isqrt
    assert x >= 0
    r = isqrt((x.numerator * den * den) // x.denominator) + 1
    out = F(r, den)
    assert out * out >= x
    return out


# ------------------------------------------------------------- Q(sqrt 3)

def Surd3(p=0, q=0):
    return Quad(3, p, q)


# ------------------------------------------------- exact LP dual checking

class DualRejected(Exception):
    pass


def dual_certificate_value(A, b, c, y, name="LP", ring_zero=None, log=None):
    """Verify that `y` is dual-feasible for   min c.x  s.t.  A x >= b, x >= 0.

    A : list of rows (each a list of ring elements), one row per constraint
    b : list of ring elements, one per constraint
    c : list of ring elements, one per variable
    y : list of ring elements, one per constraint  (the candidate dual)

    Ring elements may be Fraction or Quad; both carry exact >= .  Returns the
    exact dual objective y.b.  Raises DualRejected on any violation -- there is
    no tolerance anywhere in this function.
    """
    m = len(A)
    assert len(b) == m and len(y) == m
    nvar = len(c)
    for row in A:
        assert len(row) == nvar

    zero = ring_zero if ring_zero is not None else F(0)

    for i, yi in enumerate(y):
        if not (yi >= zero):
            raise DualRejected(f"{name}: dual variable y[{i}] is negative")

    for j in range(nvar):
        acc = zero
        for i in range(m):
            acc = acc + y[i] * A[i][j]
        if not (acc <= c[j]):
            raise DualRejected(
                f"{name}: dual constraint {j} violated: "
                f"(A^T y)[{j}] = {acc} > c[{j}] = {c[j]}")
        if log is not None:
            slack = c[j] - acc
            tight = "TIGHT (equality)" if slack == zero else f"slack {slack}"
            log(f"      dual constraint {j}: (A^T y)[{j}] <= c[{j}]  OK, {tight}")

    val = zero
    for i in range(m):
        val = val + y[i] * b[i]
    return val


# ------------------------------------------------------------- self-tests

def _selftest(log=print):
    log("  [exact.py self-test]")

    # -- Quad sign predicate, against facts checkable by integers -----------
    q = Quad(129)
    assert Quad(129, -3, 1).sign() > 0          # sqrt129 > 3
    assert Quad(129, -12, 1).sign() < 0         # sqrt129 < 12
    assert Quad(129, -11, 1).sign() > 0         # sqrt129 > 11
    assert (Quad(129, 0, 1) * Quad(129, 0, 1)) == Quad(129, 129, 0)
    assert Quad(3, 0, 1) * Quad(3, 0, 1) == Quad(3, 3, 0)
    assert Quad(3, 0, 0).sign() == 0
    lo, hi = sqrt_bounds(3)
    assert lo * lo < 3 < hi * hi
    assert sqrt_up(F(2)) ** 2 >= 2
    log("    Quad exact sign + field ops: OK")

    # -- the dual checker on a TINY LP with a hand-solved answer -----------
    #    min x + y   s.t.  x + 2y >= 2,  3x + y >= 3,  x,y >= 0
    #    vertices: (2,0) -> 2 ; (0,3) -> 3 ; (4/5, 3/5) -> 7/5   => opt 7/5
    #    dual: max 2u + 3v  s.t.  u + 3v <= 1, 2u + v <= 1, u,v >= 0
    #          u = 2/5, v = 1/5 -> 4/5 + 3/5 = 7/5, both constraints tight.
    A = [[F(1), F(2)], [F(3), F(1)]]
    b = [F(2), F(3)]
    c = [F(1), F(1)]
    val = dual_certificate_value(A, b, c, [F(2, 5), F(1, 5)], name="tiny")
    assert val == F(7, 5), val
    log(f"    tiny LP: dual value {val} == known optimum 7/5: OK")

    # a strictly interior (suboptimal but feasible) dual must be ACCEPTED
    val2 = dual_certificate_value(A, b, c, [F(1, 5), F(1, 5)], name="tiny-int")
    assert val2 == F(2, 5) + F(3, 5) == F(1)
    assert val2 < F(7, 5)
    log(f"    tiny LP: interior dual accepted, value {val2} < 7/5: OK")

    # -- NEGATIVE CONTROLS: the checker must REJECT bad duals ---------------
    for bad, why in (([F(1), F(-1, 100)], "negative component"),
                     ([F(1), F(1)], "A^T y > c"),
                     ([F(2, 5) + F(1, 1000), F(1, 5)], "epsilon-infeasible")):
        try:
            dual_certificate_value(A, b, c, bad, name="tiny-bad")
        except DualRejected:
            log(f"    tiny LP: rejected bad dual ({why}): OK")
        else:
            raise AssertionError(f"checker accepted a bad dual ({why})")

    # -- the checker over Q(sqrt D), not just Q ----------------------------
    #    min sqrt3 * x  s.t.  x >= 1, x >= 0.  Optimum sqrt3.
    A3 = [[Surd3(1, 0)]]
    b3 = [Surd3(1, 0)]
    c3 = [Surd3(0, 1)]
    v3 = dual_certificate_value(A3, b3, c3, [Surd3(0, 1)], name="surd",
                                ring_zero=Surd3(0, 0))
    assert v3 == Surd3(0, 1)
    try:
        dual_certificate_value(A3, b3, c3, [Surd3(0, 1) + Surd3(F(1, 10 ** 9))],
                               name="surd-bad", ring_zero=Surd3(0, 0))
    except DualRejected:
        log("    Q(sqrt3) LP: accepted tight dual, rejected over-large one: OK")
    else:
        raise AssertionError("Q(sqrt3) checker accepted an infeasible dual")

    log("  [exact.py self-test PASSED]")


if __name__ == "__main__":
    _selftest()
