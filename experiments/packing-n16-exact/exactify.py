"""Exactify the n=16 contact chain: eliminate to a univariate polynomial in d.

CONSTRUCTION only.  This produces a *candidate* exact value; nothing is certified here.
Certification happens in check_n16.py, in exact arithmetic, from the certificate alone.

Structure of the chain (derived in the attack README; each identity below is *proved* here by
sympy `simplify`/`expand` on the ideal, not assumed from the floats):

    g^2 = -3 d^2 + 36 d + (-60)              g = sqrt(3 (10-d)(d-2))
    P2  = (3*Y2 - 2, Y2),   Y2 = (3d + 6 - g)/12          [from contacts 2-3 and 2-10]
    P15 = (d/2 + 1, 2*Y2 - d/2 + 1)                        [from contacts 2-15 and 3-15]
    P1  = P2 - (2, 0)                                      [from contacts 1-2 and 1-12]
    P9  = circle(P15,2) cap circle(P13,2)                  [contacts 9-15 and 9-13]
    u   = 2*X9 - (d-2)                                     [contact 9-11]
    P14 = (u/2, K),  12 K^2 = 16 - u^2                     [contacts 6-14 and 11-14]
    t   = (u + 6K)/4                                       [contact 5-14, the other root t=0 is P6]
    closure: |P1 - P5|^2 = 4 with P5 = (t,t)               [contact 1-5]
"""
import sympy as sp

d, g, X9, Y9, K = sp.symbols("d g X9 Y9 K", real=True)


def D2(P, Q):
    return (P[0] - Q[0]) ** 2 + 3 * (P[1] - Q[1]) ** 2


# --- corner-forced points -------------------------------------------------
P6 = (sp.Integer(0), sp.Integer(0))
P7 = (d, sp.Integer(0))
P0 = (d / 2, d / 2)
P13 = (d - 2, sp.Integer(0))
P8 = (d - 1, sp.Integer(1))
P3 = (d - 2, sp.Integer(2))
P12 = (d / 2 - 1, d / 2 - 1)
P10 = (d / 2 + 1, d / 2 - 1)

REL_G = g ** 2 - (-3 * d ** 2 + 36 * d - 60)

Y2 = (3 * d + 6 - g) / 12
X2 = 3 * Y2 - 2
P2 = (X2, Y2)
P15 = (d / 2 + 1, 2 * Y2 - d / 2 + 1)
P1 = (X2 - 2, Y2)


def red(e):
    """Reduce mod g^2 = ... and expand."""
    e = sp.expand(e)
    p = sp.Poly(e, g)
    out = 0
    for (k,), c in p.terms():
        gk = sp.Integer(1) if k == 0 else (g if k % 2 else 1)
        base = (-3 * d ** 2 + 36 * d - 60) ** (k // 2)
        out += c * base * gk
    return sp.expand(out)


print("=== identities forced by the chain (must all reduce to 0) ===")
for name, expr in [
    ("|2-3|^2 - 4", D2(P2, P3) - 4),
    ("|2-10|^2 - 4", D2(P2, P10) - 4),
    ("|2-15|^2 - 4", D2(P2, P15) - 4),
    ("|3-15|^2 - 4", D2(P3, P15) - 4),
    ("|1-2|^2 - 4", D2(P1, P2) - 4),
    ("|1-12|^2 - 4", D2(P1, P12) - 4),
    ("|0-10|^2 - 4", D2(P0, P10) - 4),
    ("|0-12|^2 - 4", D2(P0, P12) - 4),
    ("|10-12|^2 - 4", D2(P10, P12) - 4),
    ("|7-8|^2 - 4", D2(P7, P8) - 4),
    ("|7-13|^2 - 4", D2(P7, P13) - 4),
    ("|8-13|^2 - 4", D2(P8, P13) - 4),
    ("|3-8|^2 - 4", D2(P3, P8) - 4),
]:
    r = sp.simplify(red(sp.together(expr) * 1))
    print(f"  {name:16s} -> {r}")
    assert r == 0, name

# --- the part that still needs solving -----------------------------------
P9s = (X9, Y9)
C1 = sp.expand(D2(P9s, P13) - 4)          # 9-13
C2 = sp.expand(red(D2(P9s, P15) - 4))     # 9-15
u = 2 * X9 - (d - 2)                       # 9-11 given 9-13
P14 = (u / 2, K)
REL_K = sp.expand(12 * K ** 2 - (16 - u ** 2))     # 6-14 and 11-14
t = (u + 6 * K) / 4
P5 = (t, t)
CLOSE = sp.expand(red(D2(P1, P5) - 4))     # 1-5

print("\n=== elimination ===")
# eliminate Y9 between C1 and C2 is wrong-way; instead: C1 - C2 is linear in (X9,Y9)
LIN = sp.expand(sp.numer(sp.together(red(C1 - C2))))
print("C1 - C2 (linear in X9,Y9):", sp.factor(LIN))

import pathlib, pickle
pathlib.Path("experiments/packing-n16-exact/out").mkdir(exist_ok=True)

# X9 solved linearly from LIN (valid because d != 6 at the root; checked later)
X9_sol = sp.simplify(sp.solve(LIN, X9)[0])
print("X9 =", X9_sol)

def sub9(e):
    return sp.expand(red(sp.numer(sp.together(sp.expand(e.subs(X9, X9_sol))))))

Q9 = sub9(C1)                     # quadratic in Y9 (times (d-6)^2)
Q9 = sp.Poly(Q9, Y9)
print("\nquadratic in Y9, degree", Q9.degree())

u_s = sp.together(2 * X9_sol - (d - 2))
CLOSE_s = sp.expand(red(sp.expand(CLOSE.subs(X9, X9_sol))))
# reduce mod 12 K^2 = 16 - u^2 before reading off the K-degree
u_sub = sp.together(2 * X9_sol - (d - 2))
def redK(e):
    e = sp.expand(sp.together(e))
    pp = sp.Poly(sp.numer(sp.together(e)), K)
    den = sp.denom(sp.together(e))
    out = 0
    for (k,), c in pp.terms():
        q, r = divmod(k, 2)
        out += c * ((16 - u_sub ** 2) / 12) ** q * (K if r else 1)
    return sp.together(out / den)
CLOSE_s = redK(CLOSE_s)
pk = sp.Poly(sp.numer(sp.together(CLOSE_s)), K)
print("CLOSE is degree", pk.degree(), "in K (after reducing K^2)")
assert pk.degree() == 1, "closure must be linear in K"
Bc, Ac = pk.all_coeffs()          # Ac + Bc*K = 0  ->  K = -Ac/Bc
RELK_s = sp.expand(red(sp.expand(REL_K.subs(X9, X9_sol))))
pkk = sp.Poly(sp.numer(sp.together(RELK_s)), K)
c2, c1, c0 = pkk.all_coeffs()
assert c1 == 0
# c2*K^2 + c0 = 0  and  K = -Ac/Bc   ->  c2*Ac^2 + c0*Bc^2 = 0
ELIM_K = sp.expand(red(sp.expand(c2 * Ac ** 2 + c0 * Bc ** 2)))
ELIM_K = sp.numer(sp.together(ELIM_K))
print("after eliminating K: poly in (d,g,Y9), degree in Y9 =", sp.Poly(ELIM_K, Y9).degree())

R_Y9 = sp.resultant(Q9.as_expr(), ELIM_K, Y9)
R_Y9 = sp.expand(red(sp.expand(R_Y9)))
print("after eliminating Y9: degree in g =", sp.Poly(R_Y9, g).degree(),
      " degree in d =", sp.Poly(R_Y9, d).degree())

# reduce mod g^2 then eliminate g:  R = P + Q*g  ->  P^2 - Q^2*(3(10-d)(d-2)) = 0
pg = sp.Poly(R_Y9, g)
P_part = sum(c * g ** k for (k,), c in pg.terms() if k % 2 == 0).subs(g, 1) if pg.degree() > 0 else R_Y9
Pp = sp.expand(sum(c for (k,), c in pg.terms() if k == 0))
Qq = sp.expand(sum(c for (k,), c in pg.terms() if k == 1))
assert sp.expand(Pp + Qq * g - R_Y9) == 0
FIN = sp.expand(Pp ** 2 - Qq ** 2 * (-3 * d ** 2 + 36 * d - 60))
FIN = sp.Poly(FIN, d)
print("\nunivariate in d: degree", FIN.degree())
fac = sp.factor_list(FIN.as_expr())
print("factors:")
for f, m in fac[1]:
    print("   mult", m, " deg", sp.Poly(f, d).degree(), " :", sp.Poly(f,d).all_coeffs() if sp.Poly(f,d).degree()<=20 else "...")

import json, pathlib
pathlib.Path("experiments/packing-n16-exact/out/elim.txt").write_text(
    "FIN = " + sp.srepr(FIN.as_expr()) + "\n")
pathlib.Path("experiments/packing-n16-exact/out/factors.txt").write_text(
    "\n".join(f"{m}  {sp.Poly(f,d).all_coeffs()}" for f, m in fac[1]))
