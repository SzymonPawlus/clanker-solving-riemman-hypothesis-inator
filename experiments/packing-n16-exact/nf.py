"""Exact arithmetic in the number field Q[x]/(f) for a fixed irreducible f, over Fraction.

Standard-library only.  Used by the constructor; the checker (check_n16.py) carries its own
independent copy so that verifying a certificate never imports the code that made it.

Sign of an element is decided by rigorous rational interval arithmetic on an isolating interval
for the chosen real root, refined by exact bisection until the interval excludes 0.  That
terminates for every nonzero element, and the answer it gives is a proof rather than an estimate.
Equality is syntactic on the reduced coefficient vector, which is exact because {1, a, ..., a^(n-1)}
is a Q-basis of Q(a).
"""
from __future__ import annotations
from fractions import Fraction as F


def poly_trim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return c


def poly_mul(a, b):
    if not a or not b:
        return []
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    out[i + j] += ai * bj
    return poly_trim(out)


def poly_divmod(a, b):
    a = list(a); q = [F(0)] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and poly_trim(a):
        k = len(a) - len(b)
        f = a[-1] / b[-1]
        q[k] = f
        for i, bi in enumerate(b):
            a[k + i] -= f * bi
        a = poly_trim(a)
    return poly_trim(q), poly_trim(a)


class Field:
    """Q(alpha) with alpha the unique root of `minpoly` inside the rational interval `iso`."""

    def __init__(self, minpoly, iso):
        c = [F(v) for v in minpoly]
        self.f = poly_trim([v / c[-1] for v in c])       # monic
        self.n = len(self.f) - 1
        self.lo, self.hi = F(iso[0]), F(iso[1])

    # --- rigorous root refinement ------------------------------------
    def _eval_f(self, v):
        acc = F(0)
        for c in reversed(self.f):
            acc = acc * v + c
        return acc

    def refine(self, bits):
        """Bisect until hi - lo <= 2^-bits.  Requires exactly one root in [lo,hi]."""
        target = F(1, 1 << bits) if bits >= 0 else F(1 << (-bits))
        flo = self._eval_f(self.lo)
        if flo == 0 or self._eval_f(self.hi) == 0:
            raise ValueError("endpoint is a root; isolating interval is bad")
        slo = 1 if flo > 0 else -1
        while self.hi - self.lo > target:
            mid = (self.lo + self.hi) / 2
            fm = self._eval_f(mid)
            if fm == 0:
                raise ValueError("rational root; minpoly is not irreducible of degree n")
            if (1 if fm > 0 else -1) == slo:
                self.lo = mid
            else:
                self.hi = mid

    def __call__(self, coeffs):
        return El(self, [F(v) for v in coeffs])

    def rat(self, v):
        return El(self, [F(v)])

    @property
    def gen(self):
        return El(self, [F(0), F(1)])


class El:
    __slots__ = ("K", "c")

    def __init__(self, K, c):
        self.K = K
        c = poly_trim([F(v) for v in c])
        if len(c) > K.n:
            _, c = poly_divmod(c, K.f)
        self.c = poly_trim(c)

    def _co(self, o):
        if isinstance(o, El):
            assert o.K is self.K
            return o
        if isinstance(o, (int, F)):
            return El(self.K, [F(o)])
        raise TypeError(f"cannot combine field element with {type(o).__name__}")

    def __add__(self, o):
        o = self._co(o)
        m = max(len(self.c), len(o.c))
        return El(self.K, [(self.c[i] if i < len(self.c) else F(0)) +
                           (o.c[i] if i < len(o.c) else F(0)) for i in range(m)])
    __radd__ = __add__

    def __neg__(self):
        return El(self.K, [-v for v in self.c])

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) + (-self)

    def __mul__(self, o):
        o = self._co(o)
        return El(self.K, poly_mul(self.c, o.c))
    __rmul__ = __mul__

    def inverse(self):
        if self.is_zero():
            raise ZeroDivisionError
        # extended Euclid in Q[x]
        r0, r1 = list(self.K.f), list(self.c)
        s0, s1 = [], [F(1)]
        while poly_trim(r1):
            q, r = poly_divmod(r0, r1)
            r0, r1 = r1, r
            s0, s1 = s1, poly_trim([a - b for a, b in zip(
                s0 + [F(0)] * (len(poly_mul(q, s1)) - len(s0)),
                poly_mul(q, s1) + [F(0)] * (len(s0) - len(poly_mul(q, s1))))])
        if len(poly_trim(r0)) != 1:
            raise ZeroDivisionError("not invertible; minpoly reducible?")
        inv = poly_trim([v / r0[0] for v in s0])
        return El(self.K, inv)

    def __truediv__(self, o):
        return self * self._co(o).inverse()

    def __rtruediv__(self, o):
        return self._co(o) * self.inverse()

    def __pow__(self, k):
        out, b = El(self.K, [F(1)]), self
        while k:
            if k & 1:
                out = out * b
            b = b * b
            k >>= 1
        return out

    def is_zero(self):
        return not self.c

    def __eq__(self, o):
        return (self - self._co(o)).is_zero()

    def enclosure(self):
        lo, hi = self.K.lo, self.K.hi
        assert lo > 0, "this routine assumes the root is positive"
        acc_lo = acc_hi = F(0)
        plo = phi = F(1)
        for v in self.c:
            a, b = (v * plo, v * phi) if v >= 0 else (v * phi, v * plo)
            acc_lo += a
            acc_hi += b
            plo *= lo
            phi *= hi
        return acc_lo, acc_hi

    def sign(self):
        if self.is_zero():
            return 0
        bits = 64
        for _ in range(30):
            self.K.refine(bits)
            lo, hi = self.enclosure()
            if lo > 0:
                return 1
            if hi < 0:
                return -1
            bits *= 2
        raise RuntimeError("sign test did not converge")

    def __lt__(self, o): return (self - self._co(o)).sign() < 0
    def __le__(self, o): return (self - self._co(o)).sign() <= 0
    def __gt__(self, o): return (self - self._co(o)).sign() > 0
    def __ge__(self, o): return (self - self._co(o)).sign() >= 0

    def approx(self):
        lo, hi = self.enclosure()
        return float((lo + hi) / 2)

    def __repr__(self):
        if not self.c:
            return "0"
        return " + ".join(f"({v})*a^{i}" if i else f"({v})" for i, v in enumerate(self.c) if v)


# ---------------------------------------------------------------- Sturm
def poly_derivative(c):
    return poly_trim([c[i] * i for i in range(1, len(c))])


def sturm_chain(f):
    chain = [poly_trim(list(f)), poly_derivative(f)]
    while poly_trim(chain[-1]):
        _, r = poly_divmod(chain[-2], chain[-1])
        if not poly_trim(r):
            break
        chain.append(poly_trim([-v for v in r]))
    return chain


def _sign_changes(chain, v):
    vals = []
    for p in chain:
        acc = F(0)
        for c in reversed(p):
            acc = acc * v + c
        vals.append(acc)
    vals = [x for x in vals if x != 0]
    return sum(1 for i in range(len(vals) - 1) if (vals[i] > 0) != (vals[i + 1] > 0))


def count_roots(f, lo, hi):
    """Number of DISTINCT real roots of f in (lo, hi], by Sturm.  Exact, no tolerance."""
    lo, hi = F(lo), F(hi)
    ch = sturm_chain([F(v) for v in f])
    return _sign_changes(ch, lo) - _sign_changes(ch, hi)
