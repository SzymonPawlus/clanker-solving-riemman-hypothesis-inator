"""Section 5.1 row 2 cross-check: the same budget with the closed-form slice
bound on the 9 edge pieces.  Transcendental (arcsin), so this one is done in
mpmath at 200 bits rather than in Fraction; the decision being made is only
'does it round to 4.920766', which is robust at that precision.
"""
from mpmath import mp, mpf, pi, sqrt, asin, findroot
mp.prec = 200

f = lambda l: pi / 2 - asin(l / 2) - (l / 2) * sqrt(1 - l ** 2 / 4)


def gap(a, corner=3, edge=9, deep=3, ell=lambda a: (a - 4 / sqrt(mpf(3))) / 3):
    budget = corner * (pi / 6) + edge * f(ell(a)) + deep * (pi / 4)
    return sqrt(mpf(3)) / 4 * a ** 2 - budget


a = findroot(gap, mpf('4.9'))
print("Theorem-N classes + closed-form f on the 9 edge pieces :", mp.nstr(a, 12))
print("  published in n16-structure section 5.1                :  4.920766")
print("  published U2 in n16-covering-limit (certified slab LP) :  4.914308")

# and the same with Lemma S's own middle length a-2 (k_e = 3), for the
# 'same argument reached twice' claim
a2 = findroot(lambda a: gap(a, ell=lambda a: (a - 2) / 3), mpf('4.9'))
print("same budget but with Lemma S's middle length a-2        :", mp.nstr(a2, 12))

# U1 again, for cross-consistency with the exact rational computation
a1 = findroot(lambda a: sqrt(mpf(3)) / 4 * a ** 2 - (3 * pi / 6 + 12 * pi / 4), mpf('5'))
print("U1 = sqrt(14 pi/sqrt3)                                  :", mp.nstr(a1, 12))

print()
print("apples-to-apples: Lemma S's own optimisation (max over admissible k) with")
print("the SAME closed-form f, versus Theorem N's forced 3/9/3 with that f:")
best = None
for k1 in range(3, 7):
    for k2 in range(3, 7):
        for k3 in range(3, 7):
            if k1 + k2 + k3 > 12:
                continue
            ks = (k1, k2, k3)
            def g(a, ks=ks):
                rhs = 3 * (pi / 6) + (12 - sum(ks)) * (pi / 4)
                for k in ks:
                    rhs += k * f((a - 2) / k)
                return sqrt(mpf(3)) / 4 * a ** 2 - rhs
            try:
                root = findroot(g, mpf('4.9'))
            except Exception:
                continue
            print(f"   k = {ks}  ->  A_15 <= {mp.nstr(root, 10)}")
            if best is None or root > best[0]:
                best = (root, ks)
print(f"  Lemma S with the closed-form f, worst admissible k = {best[1]}: {mp.nstr(best[0], 10)}")
print(f"  Theorem N's forced 3/9/3 with the same f            : 4.92076578")
