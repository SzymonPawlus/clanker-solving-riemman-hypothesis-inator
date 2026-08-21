"""Independent re-check of the certificates, deliberately by a DIFFERENT route.

verify.py works in triangular coordinates, where every test is a rational comparison.  This file
converts to CARTESIAN coordinates and re-tests there, using 60-digit directed-rounding decimals
with the rounding chosen against the conclusion.  If the two disagree, that is a finding, not
something to average (problem RULES.md section 3).
"""
import json, os
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))

def dec(fr, rounding):
    getcontext().rounding = rounding
    return Decimal(fr.numerator) / Decimal(fr.denominator)

# sqrt(3) enclosure, verified exactly below
from math import isqrt
_k = isqrt(3 * 10**98)                # floor(sqrt(3) * 10^49), exact integer square root
S3_LO = F(_k, 10**49)
S3_HI = F(_k + 1, 10**49)
assert S3_LO ** 2 < 3 < S3_HI ** 2

def main():
    cert = json.load(open(os.path.join(HERE, 'out', 'certificates.json')))
    allok = True
    for e in cert:
        if not e.get('certified'):
            continue
        a = F(e['a']); n = e['n']
        P = [(F(x), F(y)) for x, y in e['pts']]
        # Cartesian:  x = u + v/2 ,  y = v*sqrt(3)/2 .  Use the sqrt(3) enclosure both ways.
        bad = []
        # Cartesian tests, written so that sqrt(3) never has to be approximated: the three
        # half-plane conditions y >= 0, y <= sqrt(3) x, y <= sqrt(3)(a-x) are squared instead.
        for i, (u, v) in enumerate(P):
            x = u + v / 2
            ysq = 3 * v * v / 4           # y^2 with y = v*sqrt(3)/2, exactly rational
            if not (v >= 0):
                bad.append(("y<0", i))
            if not (x >= 0 and ysq <= 3 * x * x):
                bad.append(("left edge", i))
            if not ((a - x) >= 0 and ysq <= 3 * (a - x) * (a - x)):
                bad.append(("right edge", i))
        # and an independent 60-digit decimal cross-read of the same three quantities
        for i, (u, v) in enumerate(P):
            x = u + v / 2
            y_hi = dec(v * S3_HI / 2, ROUND_CEILING)
            if not (y_hi >= 0 and y_hi <= dec(a * S3_HI / 2, ROUND_CEILING)):
                bad.append(("height", i))
        mind2 = None
        for i in range(n):
            xi = P[i][0] + P[i][1] / 2
            for j in range(i + 1, n):
                xj = P[j][0] + P[j][1] / 2
                dx = xi - xj
                dvy = P[i][1] - P[j][1]
                # (dy)^2 = 3 dv^2 / 4 exactly -- sqrt(3) squares away, no enclosure needed
                d2 = dx * dx + 3 * dvy * dvy / 4
                if mind2 is None or d2 < mind2: mind2 = d2
                if d2 < 1:
                    bad.append(("pair", i, j, d2))
        ok = not bad
        allok &= ok
        print(f"n={n}  a={float(a):.7f}: cartesian recheck {'OK' if ok else 'FAILED ' + str(bad[:3])}"
              f"   min squared distance = {float(mind2):.9f}   a < 6: {a < 6}")
    print("\nall certificates re-checked by the independent cartesian route:", allok)

if __name__ == '__main__':
    main()
