"""Build the exact n = 16 configuration in Q(alpha) and emit the certificate.

CONSTRUCTION only (problem RULES.md 1): every statement produced here is of the form
s(16) <= c, witnessed by an explicit packing.  Nothing here is an optimality claim.

alpha is the unique real root in (9,10) of the degree-10 irreducible

  f(x) = 9x^10 - 492x^9 + 12448x^8 - 190688x^7 + 1945984x^6 - 13742336x^5
       + 67583872x^4 - 226861568x^3 + 492993280x^2 - 620155904x + 339613696

produced by eliminating the contact system in exactify.py.  d = alpha, s = d + 2 sqrt(3).

Sheared chart: x = X, y = sqrt(3) Y (see system.py).  All of X_i, Y_i lie in Q(alpha); sqrt(3)
does not (f is irreducible over Q(sqrt 3)), so the certificate's (x,y) coordinates live in the
degree-20 field Q(alpha, sqrt 3) with x_i in Q(alpha) and y_i in sqrt(3) Q(alpha).

Every PSLQ guess below is *proved* by exact arithmetic in nf.Field before it is used.
"""
import json, pathlib, sys
from fractions import Fraction as Fr

import sympy as sp
from mpmath import mp, mpmathify, mpf, sqrt as msqrt, pslq, nstr, findroot, polyval

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nf import Field, count_roots

mp.dps = 300

F10 = [339613696, -620155904, 492993280, -226861568, 67583872,
       -13742336, 1945984, -190688, 12448, -492, 9]           # ascending
ISO = (Fr(9), Fr(10))

assert count_roots(F10, *ISO) == 1, "isolating interval must contain exactly one root"
K = Field(F10, ISO)
A = K.gen                                                      # alpha = d


def hp_alpha():
    c = [mpmathify(v) for v in reversed(F10)]
    return findroot(lambda z: polyval(c, z), mpf("9.2495271590127914277871897476431"))


def rep(val, alpha, maxcoeff=10**24):
    basis = [alpha ** k for k in range(10)] + [val]
    r = pslq(basis, maxcoeff=maxcoeff, maxsteps=200000, tol=mpf(10) ** (-mp.dps + 60))
    if r is None or r[-1] == 0:
        raise RuntimeError("PSLQ found no representation")
    den = -r[-1]
    return [Fr(int(r[k]), int(den)) for k in range(10)]


# ---------------------------------------------------------------- numeric chain at 300 dps
al = hp_alpha()
g_n = msqrt(-3 * al ** 2 + 36 * al - 60)
Y2_n = (3 * al + 6 - g_n) / 12
X2_n = 3 * Y2_n - 2
X15_n = al / 2 + 1
Y15_n = 2 * Y2_n - al / 2 + 1
X1_n, Y1_n = X2_n - 2, Y2_n
# point 9: circle(15,2) cap circle(13,2), branch chosen to match the refined float solution
P13_n = (al - 2, mpf(0))
aa = 2 * (P13_n[0] - X15_n)
bb = 6 * (P13_n[1] - Y15_n)
cc = P13_n[0] ** 2 - X15_n ** 2 + 3 * (P13_n[1] ** 2 - Y15_n ** 2)
# aa*X + bb*Y = cc, with (X-(al-2))^2 + 3Y^2 = 4
qa = (bb / aa) ** 2 * 0 + 1  # placeholder
# X = (cc - bb Y)/aa
Aq = (bb / aa) ** 2 + 3
Bq = -2 * (cc / aa - (al - 2)) * (bb / aa)
Cq = (cc / aa - (al - 2)) ** 2 - 4
disc = Bq ** 2 - 4 * Aq * Cq
cands = [(-Bq + s * msqrt(disc)) / (2 * Aq) for s in (1, -1)]
Y9_n = min(cands, key=lambda v: abs(v - mpf("0.18958752218746243222549190763808961191887172518453")))
X9_n = (cc - bb * Y9_n) / aa
u_n = 2 * X9_n - (al - 2)
Y14_n = msqrt((16 - u_n ** 2) / 12)
t_n = (u_n + 6 * Y14_n) / 4

print("numeric chain (300 dps):")
for nm, v in [("alpha", al), ("g", g_n), ("Y2", Y2_n), ("Y9", Y9_n), ("u", u_n),
              ("Y14", Y14_n), ("t", t_n)]:
    print(f"  {nm:5s} {nstr(v, 40)}")

# ---------------------------------------------------------------- exact lifts
g = K(rep(g_n, al));      assert (g * g - (-3 * A * A + 36 * A - 60)).is_zero(), "g^2 wrong"
assert g.sign() > 0
Y9 = K(rep(Y9_n, al))
Y14 = K(rep(Y14_n, al));  assert Y14.sign() > 0

Y2 = (3 * A + 6 - g) / 12
X2 = 3 * Y2 - 2
P = {}
P[6] = (K.rat(0), K.rat(0))
P[7] = (A, K.rat(0))
P[0] = (A / 2, A / 2)
P[13] = (A - 2, K.rat(0))
P[8] = (A - 1, K.rat(1))
P[3] = (A - 2, K.rat(2))
P[12] = (A / 2 - 1, A / 2 - 1)
P[10] = (A / 2 + 1, A / 2 - 1)
P[2] = (X2, Y2)
P[15] = (A / 2 + 1, 2 * Y2 - A / 2 + 1)
P[1] = (X2 - 2, Y2)
# X9 from the exact line through the two circle centres
aaK = 2 * (P[13][0] - P[15][0])
bbK = 6 * (P[13][1] - P[15][1])
ccK = P[13][0] ** 2 - P[15][0] ** 2 + 3 * (P[13][1] ** 2 - P[15][1] ** 2)
X9 = (ccK - bbK * Y9) / aaK
P[9] = (X9, Y9)
u = 2 * X9 - (A - 2)
assert (12 * Y14 * Y14 - (16 - u * u)).is_zero(), "Y14 relation wrong"
P[14] = (u / 2, Y14)
t = (u + 6 * Y14) / 4
P[5] = (t, t)
P[11] = (u, K.rat(0))


def D2(i, j):
    dx = P[i][0] - P[j][0]
    dy = P[i][1] - P[j][1]
    return dx * dx + 3 * dy * dy


CONTACTS = [(0, 10), (0, 12), (10, 12), (7, 8), (7, 13), (8, 13), (3, 8),
            (2, 3), (2, 10), (1, 2), (1, 5), (1, 12), (2, 15), (3, 15),
            (9, 15), (9, 13), (9, 11), (5, 14), (6, 14), (11, 14)]
print("\nexact contact check (each must be exactly 4):")
allok = True
for i, j in CONTACTS:
    ok = (D2(i, j) - 4).is_zero()
    allok &= ok
    print(f"  |{i:2d}-{j:2d}|^2 == 4 : {ok}")
assert allok, "a contact failed exactly -- the exactification is wrong"

# ---------------------------------------------------------------- rattler (point 4)
# Point 4 has no contacts (problem RULES.md 5: rattlers are normal, do not 'fix' them).  It is
# placed at an explicitly chosen RATIONAL point of its free cell; any point of the cell would do.
print("\nrattler cell probe (distances from the float position, exact neighbours):")
