#!/usr/bin/env python3
"""Exact-rational terminal check for a repaired Proposition 3.5 case cover.

This is conditional on the literature input b0 >= 0.438925. It does not
certify that input or the geometric interpretation of p, q, f, and g.
"""

from fractions import Fraction as Q
from math import factorial, isqrt


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    products = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return min(products), max(products)


def scale(c, x):
    return (c * x[0], c * x[1]) if c >= 0 else (c * x[1], c * x[0])


def reciprocal(x):
    assert Q(0) < x[0] <= x[1]
    return Q(1, 1) / x[1], Q(1, 1) / x[0]


def atan_alt(x, n):
    terms = [(-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(n + 2)]
    a, b = sum(terms[:-1]), sum(terms)
    return min(a, b), max(a, b)


PI = add(scale(16, atan_alt(Q(1, 5), 80)), scale(-4, atan_alt(Q(1, 239), 30)))


def power(x, n):
    assert Q(0) <= x[0] <= x[1]
    return x[0] ** n, x[1] ** n


def taylor(x, parity, last):
    out = (Q(0), Q(0))
    for k in range(last + 1):
        n = 2 * k + parity
        out = add(out, scale(Q((-1) ** k, factorial(n)), power(x, n)))
    return out


def trig(x, parity):
    assert Q(0) <= x[0] <= x[1] <= Q(2)
    a, b = taylor(x, parity, 30), taylor(x, parity, 31)
    return min(a[0], b[0]), max(a[1], b[1])


def sin(x):
    return trig(x, 1)


def cos(x):
    return trig(x, 0)


def sqrt_interval(n, digits=60):
    scale10 = 10**digits
    lo_int = isqrt(n * scale10**2)
    out = Q(lo_int, scale10), Q(lo_int + 1, scale10)
    assert out[0] ** 2 <= n < out[1] ** 2
    return out


SQRT5 = sqrt_interval(5)
INV_SQRT5 = reciprocal(SQRT5)


def point(x):
    return x, x


def cos_alpha_minus_theta(alpha):
    # theta=atan(1/2), so cos(theta)=2/sqrt(5), sin(theta)=1/sqrt(5).
    return mul(add(scale(2, cos(point(alpha))), sin(point(alpha))), INV_SQRT5)


def second_f_sine(alpha, beta_sign, d):
    # beta=pi/2 +/- d. Put X=2*pi/3 +/- d-alpha, then
    # sin(X+theta)=(2 sin(X)+cos(X))/sqrt(5).
    x = add(scale(Q(2, 3), PI), point(beta_sign * d - alpha))
    return mul(add(scale(2, sin(x)), cos(x)), INV_SQRT5)


def show(name, x, target):
    print(f"{name}: lower margin {float(x[0] - target):.15g}")


def main():
    if not __debug__:
        raise RuntimeError("replay requires assertions; do not run Python with -O")

    target = Q(232239, 10**6)
    b_lower = Q(17557, 40000)  # 0.438925; literature dependency, not proved here
    alpha_lo = Q(66367, 100000)
    alpha_hi = Q(490347, 500000)  # 0.980694
    d = Q(1443851, 10**7)

    g_edge = scale(Q(1, 4), add(scale(Q(1, 2), cos_alpha_minus_theta(alpha_lo)), point(b_lower)))
    p_edge = scale(Q(1, 8), mul(SQRT5, sin(point(alpha_hi))))
    q_edge = scale(Q(1, 4), sin(add(scale(Q(1, 3), PI), point(d))))

    corners = []
    for alpha in (alpha_lo, alpha_hi):
        first = cos_alpha_minus_theta(alpha)
        for sign in (-1, 1):
            second = second_f_sine(alpha, sign, d)
            corners.append((alpha, sign, scale(Q(1, 8), add(first, second))))

    assert g_edge[0] > target
    assert p_edge[0] > target
    assert q_edge[0] > target
    assert all(value[0] > target for _, _, value in corners)

    show("g(alpha_lo)", g_edge, target)
    show("p(alpha_hi)", p_edge, target)
    show("q(pi/2 +/- d)", q_edge, target)
    for alpha, sign, value in corners:
        show(f"f(alpha={float(alpha)}, beta_sign={sign:+d})", value, target)
    print("PASS conditional on b0 >= 0.438925 and the analytic p,q,f,g bounds")


if __name__ == "__main__":
    main()
