"""Fair comparison: the closed-form slice bound must be capped by the
isodiametric pi/4 (n16-covering-limit lists both as bounds on f, so the usable
closed form is their minimum).  mpmath, 200 bits; cross-check only."""
from mpmath import mp, mpf, pi, sqrt, asin, findroot
mp.prec = 200
slice_b = lambda l: pi / 2 - asin(l / 2) - (l / 2) * sqrt(1 - l ** 2 / 4)
f = lambda l: min(pi / 4, slice_b(l))
r3 = sqrt(mpf(3))


def root(rhs_fn, guess='4.9'):
    return findroot(lambda a: r3 / 4 * a ** 2 - rhs_fn(a), mpf(guess))


tn = root(lambda a: 3 * (pi / 6) + 9 * f((a - 4 / r3) / 3) + 3 * (pi / 4))
print("Theorem N forced 3/9/3, middle a-4/sqrt3, capped closed-form f :", mp.nstr(tn, 10))
best = None
for k1 in range(3, 7):
    for k2 in range(3, 7):
        for k3 in range(3, 7):
            if k1 + k2 + k3 > 12:
                continue
            ks = (k1, k2, k3)
            v = root(lambda a, ks=ks: 3 * (pi / 6) + (12 - sum(ks)) * (pi / 4)
                     + sum(k * f((a - 2) / k) for k in ks))
            if best is None or v > best[0]:
                best = (v, ks)
print("Lemma S, max over admissible k, same capped f, middle a-2    :",
      mp.nstr(best[0], 10), "at k =", best[1])
print("published U2 (same structure, LP-certified f)                : 4.914308")
print("published U1 (no f at all)                                   : 5.039166")
