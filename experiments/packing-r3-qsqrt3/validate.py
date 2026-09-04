"""Validation of check.py on instances whose answer is already known, plus
negative controls.  Run this BEFORE trusting any output of check.py.

Positive controls
  * Triangular n = k(k+1)/2 for k = 2..6 (n = 3, 6, 10, 15, 21).  These are
    settled cases; the optimum is the triangular lattice with d = 2(k-1),
    s = 2(k-1) + 2*sqrt(3).  Built here from first principles, not snapped.
  * n = 12, a SETTLED case (frontier: all n <= 15 settled) whose published
    optimum s(12) = 4 + 4*sqrt(3) also lies in Q(sqrt 3).  Snapped from
    ../circle-packing-ls/out/n12.json by the same procedure used for 17/24/31,
    so it exercises the whole pipeline end to end against a known answer.

Negative controls -- the checker MUST reject each of these
  * a point nudged by 1/1000 toward a contact neighbour   -> separation failure
  * a point nudged by 1/1000 outside edge BC              -> containment failure
  * the same configuration declared at d - 1/1000         -> not tight / reject
  * a configuration declared at d + 1/1000                -> feasible but NOT tight
"""
from fractions import Fraction as F
from qsqrt3 import Q3, q3
from check import check

FAILS = []


def expect(name, cond):
    print(("  PASS  " if cond else "  FAIL  ") + name)
    if not cond:
        FAILS.append(name)


def triangular(k):
    """n = k(k+1)/2 points of the triangular lattice, side d = 2(k-1)."""
    pts = []
    for row in range(k):
        y = Q3(0, row)            # row * sqrt(3)
        for col in range(k - row):
            x = Q3(2 * col + row, 0)
            pts.append((x, y))
    return Q3(2 * (k - 1), 0), pts


def _p(ax, bx, ay, by):
    return (Q3(ax, bx), Q3(ay, by))


D12 = Q3(4, 2)
P12 = [
    _p(1, 1, 3, 1), _p(4, 2, 0, 0), _p(2, 2, 0, 0), _p(3, 1, 1, 1),
    _p(2, 1, 1, 0), _p(1, 1, 1, 1), _p(1, 0, 0, 1), _p(2, 0, 0, 0),
    _p(3, 2, 0, 1), _p(2, 1, 3, 2), _p(3, 1, 3, 1), _p(0, 0, 0, 0),
]

print("=== positive control: triangular lattice, settled n = k(k+1)/2")
for k in range(2, 7):
    d, pts = triangular(k)
    n = k * (k + 1) // 2
    r = check(n, d, pts, verbose=False)
    expect("n=%2d  feasible, tight, d = %s" % (n, d.sexpr()),
           r["ok"] and r["tight"] and d == Q3(2 * (k - 1), 0))

print()
print("=== positive control: n = 12, settled, published s(12) = 4 + 4*sqrt(3)")
r = check(12, D12, P12, verbose=False)
expect("n=12  feasible", r["ok"])
expect("n=12  tight at d = 4 + 2*sqrt(3)", r["tight"])
expect("n=12  s = 4 + 4*sqrt(3) matches the published optimum",
       r["s_exact"] == "4 + 4*sqrt(3)")

print()
print("=== negative controls (the checker must REJECT all four)")
import configs
d17, p17 = configs.D17, list(configs.P17)

bad = list(p17)
bad[1] = (p17[1][0] + Q3(F(1, 1000)), p17[1][1])     # slide toward its neighbour
expect("nudged point violates separation", not check(17, d17, bad, verbose=False)["ok"])

bad = list(p17)
bad[3] = (p17[3][0] + Q3(F(1, 1000)), p17[3][1])     # push corner B outside
expect("point pushed outside BC violates containment",
       not check(17, d17, bad, verbose=False)["ok"])

r = check(17, d17 - Q3(F(1, 1000)), p17, verbose=False)
expect("under-declared d is rejected", not r["ok"])

r = check(17, d17 + Q3(F(1, 1000)), p17, verbose=False)
expect("over-declared d is feasible but reported NOT tight", r["ok"] and not r["tight"])

print()
if FAILS:
    print("VALIDATION FAILED: %s" % FAILS)
    raise SystemExit(1)
print("validation: all controls behaved as required.")
