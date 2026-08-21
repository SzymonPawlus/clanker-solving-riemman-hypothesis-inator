"""Exact rational geometry for the equilateral triangle.  No floats anywhere in this module.

NORMALISATION -- asserted, not assumed (this has bitten several workers on this problem):
  * separation 1 (NOT 2);
  * T_a is the closed equilateral triangle of side a.

TRIANGULAR COORDINATES.  Write a point as (u, v) meaning the Cartesian point
    x = u + v/2 ,  y = v * sqrt(3)/2 .
Then
    T_a = { (u,v) : u >= 0, v >= 0, u + v <= a }          (three rational half-planes)
    |P-Q|^2 = du^2 + du*dv + dv^2                          (a rational quadratic form)
so every containment test and every distance test is an exact comparison of rationals.
This is why nothing here needs Q(sqrt 3).
"""
from fractions import Fraction as F

def in_triangle(p, a):
    u, v = p
    return u >= 0 and v >= 0 and u + v <= a

def d2(p, q):
    du = p[0] - q[0]; dv = p[1] - q[1]
    return du * du + du * dv + dv * dv

def check_separated(pts, a, sep2=F(1)):
    """Return (ok, failures).  Every point in T_a, every pairwise squared distance >= sep2."""
    bad = []
    for i, p in enumerate(pts):
        if not in_triangle(p, a):
            bad.append(("outside", i, p))
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            if d2(pts[i], pts[j]) < sep2:
                bad.append(("close", i, j, d2(pts[i], pts[j])))
    return (len(bad) == 0), bad

def cart_to_tri(x, y, sq3):
    """float helper only -- callers must round the result to Fractions themselves."""
    v = 2.0 * y / sq3
    u = x - y / sq3
    return u, v

def rationalise(u, v, den):
    """Snap a float triangular coordinate to a rational with the given denominator."""
    return (F(round(u * den), den), F(round(v * den), den))
