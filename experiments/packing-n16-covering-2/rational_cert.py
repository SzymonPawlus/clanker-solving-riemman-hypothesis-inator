"""A purely RATIONAL strict certificate, as close to a = 1+2*sqrt3 as we like.

Substituting a rational R ~ sqrt3 for sqrt3 in the exact Q(sqrt3) configuration of
exact_1p2r3.py turns every coordinate rational; the pieces stay a subdivision of
T_{1+2R} (the combinatorics and the area identity are unaffected by which value is
substituted), but the tight squared diameters, which were exactly 1, move by O(|R-sqrt3|)
and may land marginally above 1.  Dilating by the largest admissible rational factor
puts them strictly below 1 again and gives the bound.  Everything below is exact
rational arithmetic; the certificate is self-contained and needs no limiting argument.
"""
import json, math, os, sys
from fractions import Fraction as F
from q3 import Q3
import exact_1p2r3 as E
import verify_c1 as V


def build(k=12, verbose=True):
    den = 10 ** k
    R = F(int(math.isqrt(3 * den * den)), den)          # largest p/den with p/den <= sqrt3
    sub = lambda z: z.a + z.b * R
    A = sub(E.A)
    faces = [[(sub(E.P[i][0]), sub(E.P[i][1])) for i in f] for f in E.FACES]
    D = F(0)
    for f in faces:
        for i in range(len(f)):
            for j in range(i + 1, len(f)):
                q = V.Q(f[i][0] - f[j][0], f[i][1] - f[j][1])
                if q > D: D = q
    # largest a' = m/10^n with (a'/A)^2 * D < 1
    best = None
    for n in (9, 10, 11, 12, 13, 14):
        d2 = 10 ** n
        m = int(float(A) / math.sqrt(float(D)) * d2) + 2
        while F(m, d2) ** 2 * D >= A * A:
            m -= 1
        c = F(m, d2)
        if best is None or c > best:
            best = c
    mu = best / A
    faces = [[(u * mu, w * mu) for (u, w) in f] for f in faces]
    D2 = F(0)
    for f in faces:
        for i in range(len(f)):
            for j in range(i + 1, len(f)):
                q = V.Q(f[i][0] - f[j][0], f[i][1] - f[j][1])
                if q > D2: D2 = q
    if verbose:
        print("sqrt3 -> %s   (error %.2e)" % (R, math.sqrt(3) - float(R)))
        print("before dilation: max sq diam - 1 = %.3e" % (float(D) - 1))
        print("dilated to a = %s = %.15f" % (best, float(best)))
        print("           1 + 2*sqrt3           = %.15f" % (1 + 2 * math.sqrt(3)))
        print("max squared diameter %.15f  < 1 : %s" % (float(D2), D2 < 1))
    return best, faces, D2


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    a, faces, D = build(k)
    json.dump({"a": [str(a.numerator), str(a.denominator)],
               "faces_uv": [[[str(u), str(w)] for (u, w) in f] for f in faces],
               "max_sq_diam": str(D),
               "source": "rational_cert.py from exact_1p2r3.py, sqrt3 -> rational"},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cert_rational.json"), "w"), indent=1)
    print("written cert_rational.json")
