#!/usr/bin/env python3
"""Exact-rational audit of the load-bearing decimal trigonometry.

This uses Fraction interval arithmetic only.  A Machin formula encloses pi;
alternating Taylor partial sums enclose sin and cos.  No floating-point value
is used in an accepted predicate.
"""

from fractions import Fraction as Q
from math import factorial


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    products = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(products), max(products)


def scale(c, x):
    return (c * x[0], c * x[1]) if c >= 0 else (c * x[1], c * x[0])


def power(x, n):
    assert 0 <= x[0] <= x[1]
    return x[0] ** n, x[1] ** n


def atan_alt(x, n):
    """Enclose atan(x), 0<x<=1, between consecutive partial sums."""
    terms = [(-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(n + 2)]
    a, b = sum(terms[:-1]), sum(terms)
    return min(a, b), max(a, b)


def pi_interval():
    # Machin: pi = 16 atan(1/5) - 4 atan(1/239).
    a = atan_alt(Q(1, 5), 80)
    b = atan_alt(Q(1, 239), 30)
    return add(scale(16, a), scale(-4, b))


PI = pi_interval()


def radians(degrees):
    return scale(degrees / 180, PI)


def taylor_poly(x, parity, last):
    """Interval evaluation of a sin/cos Taylor partial sum.

    parity=1 gives powers 1,3,... (sin); parity=0 gives 0,2,... (cos).
    """
    out = (Q(0), Q(0))
    for k in range(last + 1):
        n = 2 * k + parity
        out = add(out, scale(Q((-1) ** k, factorial(n)), power(x, n)))
    return out


def trig_alt(x, parity, even_last=30):
    """Enclose sin/cos using consecutive, decreasing alternating sums."""
    limit = Q(2) if parity == 1 else Q(1)
    assert Q(0) <= x[0] <= x[1] <= limit
    assert even_last % 2 == 0
    a = taylor_poly(x, parity, even_last)
    b = taylor_poly(x, parity, even_last + 1)
    return min(a[0], b[0]), max(a[1], b[1])


def sin_deg(d):
    return trig_alt(radians(d), 1)


def cos_deg(d):
    # All calls use 0 <= d <= 36 degrees.
    return trig_alt(radians(d), 0)


def show(name, interval):
    # Binary floats are used only for compact human-readable diagnostics; all
    # accepted comparisons below remain exact Fraction comparisons.
    print(f"{name}: [{float(interval[0]):.15g}, {float(interval[1]):.15g}]")


def main():
    c = Q(113749, 500000)  # 0.227498 exactly
    alpha_hi = Q(748385, 10000)
    beta_lo = Q(844957, 10000)
    beta_hi = Q(955043, 10000)

    # sqrt(2) enclosure, with its validity checked exactly here.
    sqrt2 = (
        Q(1414213562373095048801688724209698078569, 10**39),
        Q(1414213562373095048801688724209698078570, 10**39),
    )
    assert sqrt2[0] ** 2 < 2 < sqrt2[1] ** 2

    g_cut = scale(Q(1, 6), mul(sqrt2, sin_deg(alpha_hi)))
    h_lo_cut = scale(Q(1, 4), sin_deg(beta_lo + 30))
    h_hi_cut = scale(Q(1, 4), sin_deg(beta_hi - 30))

    # Worst beta endpoint for alpha <= 75 is beta_hi.  At alpha_hi the
    # resulting positive cosine argument has magnitude beta_hi-15-alpha_hi.
    q_right = scale(
        Q(1, 6),
        add(scale(Q(1, 2), cos_deg(beta_hi - 15 - alpha_hi)),
            cos_deg(alpha_hi - 45)),
    )
    q_left = scale(
        Q(1, 6),
        add(scale(Q(1, 2), cos_deg(beta_hi - 60)), (Q(1), Q(1))),
    )

    for name, value in (
        ("pi", PI),
        ("g(alpha_hi)", g_cut),
        ("h(beta_lo)", h_lo_cut),
        ("h(beta_hi)", h_hi_cut),
        ("q(45)", q_left),
        ("q(alpha_hi)", q_right),
    ):
        show(name, value)

    assert g_cut[0] > c
    assert h_lo_cut[0] > c
    assert h_hi_cut[0] > c
    assert q_left[0] > c
    assert q_right[0] > c
    print("PASS: every directed lower endpoint is greater than 0.227498")


if __name__ == "__main__":
    main()
