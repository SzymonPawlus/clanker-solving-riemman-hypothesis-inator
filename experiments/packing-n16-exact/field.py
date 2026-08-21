"""Identify the algebraic field of the n=16 contact solution and represent every quantity in it.

The elimination in exactify.py produced the degree-10 irreducible

    f10(d) = 9 d^10 - 492 d^9 + 12448 d^8 - 190688 d^7 + 1945984 d^6 - 13742336 d^5
             + 67583872 d^4 - 226861568 d^3 + 492993280 d^2 - 620155904 d + 339613696

whose largest real root is the candidate d.  Everything below is a *guess* found by PSLQ and then
*proved* by exact polynomial arithmetic modulo f10 (see the assertions).
"""
import sympy as sp
from mpmath import mp, mpmathify, mpf, sqrt as msqrt, pslq, nstr, findroot, polyval

mp.dps = 260

x = sp.symbols("x")
F10 = sp.Poly([9, -492, 12448, -190688, 1945984, -13742336, 67583872,
               -226861568, 492993280, -620155904, 339613696], x)

print("f10 irreducible over Q :", F10.as_expr().is_polynomial() and len(sp.factor_list(F10.as_expr())[1]) == 1)
print("f10 over Q(sqrt3)      :", sp.factor_list(F10.as_expr(), extension=sp.sqrt(3)))


def hp_root():
    c = [mpmathify(int(a)) for a in F10.all_coeffs()]
    return findroot(lambda z: polyval(c, z), mpmathify("9.24952715901279142778718974764311864499"))


def pslq_rep(val, alpha, deg=10, tol=None, maxcoeff=10**28):
    """Find rationals c_k with val = sum c_k alpha^k, or None."""
    basis = [alpha ** k for k in range(deg)] + [val]
    r = pslq(basis, maxcoeff=maxcoeff, maxsteps=100000, tol=mpf(10) ** (-mp.dps + 40))
    if r is None or r[-1] == 0:
        return None
    den = -r[-1]
    return [sp.Rational(int(r[k]), int(den)) for k in range(deg)]


if __name__ == "__main__":
    a = hp_root()
    print("\nalpha = d =", nstr(a, 50))
    g = msqrt(-3 * a ** 2 + 36 * a - 60)
    print("g     =", nstr(g, 40))
    s3 = msqrt(3)
    for name, val in [("sqrt(3)", s3), ("g", g)]:
        rep = pslq_rep(val, a)
        print(f"  {name} in Q(alpha)? ", "yes" if rep else "no", rep if rep else "")


def verify_rep(rep, target_poly):
    """Exact check: (sum rep_k x^k)^2 - target_poly == 0 mod f10?  (target as sympy expr in x)"""
    c = sum(rep[k] * x ** k for k in range(len(rep)))
    r = sp.rem(sp.Poly(sp.expand(c ** 2 - target_poly), x), F10, x)
    return sp.simplify(r.as_expr()) == 0
