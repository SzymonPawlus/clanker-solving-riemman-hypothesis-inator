"""Core routines for certified checking of Robin's inequality.

Robin's criterion (Robin 1984): RH is equivalent to
    sigma(n) < e^gamma * n * log(log(n))   for all n > 5040,
where sigma is the sum-of-divisors function and gamma is Euler's constant.

Everything arithmetic here is exact (Python ints); everything transcendental
is enclosed with mpmath's interval arithmetic (mpmath.iv), which provides
certified outward-rounded enclosures.  No floating-point comparison in this
module is load-bearing.
"""

import math
import mpmath
from mpmath import iv

# ---------------------------------------------------------------------------
# Exact arithmetic side
# ---------------------------------------------------------------------------

def factorize(n: int):
    """Exact factorization by deterministic trial division (fine for n <= ~1e14)."""
    assert n >= 1
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def sigma_exact(n: int) -> int:
    """Exact sum of divisors, sigma(n), as a Python int."""
    s = 1
    for p, e in factorize(n).items():
        s *= (p ** (e + 1) - 1) // (p - 1)
    return s


# ---------------------------------------------------------------------------
# Certified transcendental side
# ---------------------------------------------------------------------------

def rhs_enclosure(n: int, prec: int):
    """Certified interval enclosure of e^gamma * n * log(log(n)), n >= 2.

    Returns an mpmath iv.mpf interval.  For n = 2 the value is negative
    (log log 2 < 0); for n = 1 it is undefined and we refuse.
    """
    assert n >= 2
    old = iv.prec
    try:
        iv.prec = prec
        nn = iv.mpf(n)          # exact: n is an integer
        egamma = iv.exp(iv.euler)
        return egamma * nn * iv.log(iv.log(nn))
    finally:
        iv.prec = old


def robin_decide(n: int, sigma_n: int | None = None, precs=(80, 120, 200)):
    """Certified decision of Robin's inequality at n.

    Returns (verdict, lo, hi) where verdict is one of
      'holds'     : certified  sigma(n) <  e^gamma n log log n
      'violates'  : certified  sigma(n) >= e^gamma n log log n
      'undecided' : interval could not separate at max precision (kill K3)
    and (lo, hi) are float bounds of the last RHS enclosure used.
    n = 1 is refused (log log 1 undefined).
    """
    assert n >= 2, "log log n undefined/complex for n = 1"
    if sigma_n is None:
        sigma_n = sigma_exact(n)
    # Compare the exact integer sigma_n against the enclosure's own endpoints
    # (mpmath mpf comparisons are exact, regardless of ambient precision).
    # Converting endpoints to the ambient 53-bit context first could round an
    # endpoint past the true value and is deliberately avoided.
    for prec in precs:
        r = rhs_enclosure(n, prec)
        if r.a > sigma_n:
            return "holds", float(r.a), float(r.b)
        if r.b <= sigma_n:
            return "violates", float(r.a), float(r.b)
    return "undecided", float(r.a), float(r.b)


def ratio_enclosure(n: int, sigma_n: int | None = None, prec: int = 120):
    """Certified enclosure (lo, hi) of the Robin ratio
    sigma(n) / (e^gamma n log log n), for n >= 16 (so RHS > 0)."""
    assert n >= 16
    if sigma_n is None:
        sigma_n = sigma_exact(n)
    old = iv.prec
    try:
        iv.prec = prec
        r = iv.mpf(int(sigma_n)) / rhs_enclosure(n, prec)
        return float(mpmath.mpf(r.a)), float(mpmath.mpf(r.b))
    finally:
        iv.prec = old


def certified_threshold_double(L: int, margin: float = 1e-9) -> float:
    """A double T such that, certifiably,
        T <= (1 - margin) * e^gamma * log(log(m))  for every m >= L  (L >= 16).

    Used by the C sieve as a per-segment flagging threshold: since
    log log is increasing, any m in [L, R) with sigma(m) >= e^gamma m log log m
    has sigma(m)/m >= e^gamma log log L > T, so comparing against T with a
    relative safety margin can only over-flag, never miss a violation.
    The margin (1e-9) dwarfs the worst-case double rounding error of the
    handful of flops the C code performs (~1e-15 relative).
    """
    assert L >= 16
    old = iv.prec
    try:
        iv.prec = 120
        r = iv.exp(iv.euler) * iv.log(iv.log(iv.mpf(L)))
        lo = float(mpmath.mpf(r.a))  # float() rounds to nearest — may round UP
    finally:
        iv.prec = old
    # step down: cover float()'s possible upward rounding, then apply margin
    t = math.nextafter(math.nextafter(lo, 0.0), 0.0) * (1.0 - margin)
    return math.nextafter(t, 0.0)
