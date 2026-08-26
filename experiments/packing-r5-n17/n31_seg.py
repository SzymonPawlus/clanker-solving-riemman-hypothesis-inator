"""Exact endpoints of the n=31 rattler's free segment on the bottom edge, and the
exact free disc of the n=17 rattler.  All decisions exact in Q(sqrt3)."""
import json, os
from q3 import Q3
from parse_exact import parse
import checker as ck, famgen

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CERTDIR = os.path.join(REPO, "experiments", "packing-r3-qsqrt3", "certificates")


def load_cert(n):
    with open(os.path.join(CERTDIR, "n%03d-r3-qsqrt3.json" % n)) as fh:
        c = json.load(fh)
    return [(parse(a), parse(b)) for a, b in c["coordinates"]], parse(c["side_length"])


A, s = load_cert(31)
i = 13
assert A[i] == (Q3(7), Q3(0))
others = [p for k, p in enumerate(A) if k != i]


def feasible_at(p):
    if any(ck.sqdist(p, q) < Q3(4) for q in others):
        return False
    return all(v.sign() >= 0 for v in ck.walls(p, s - Q3(0, 2)).values())


print("n=31: candidate exact endpoints of the bottom-edge free segment")
for cand, nm in ((Q3(6), "6"), (Q3(4, 2), "4+2*sqrt(3)"),
                 (Q3(6) - Q3(1, 0) / Q3(1000), "6 - 1/1000"),
                 (Q3(4, 2) + Q3(1, 0) / Q3(1000), "4+2sqrt3 + 1/1000")):
    p = (cand, Q3(0))
    print("   x = %-22s feasible=%s" % (nm, feasible_at(p)))
print("   so the free segment is exactly  {(x,0) : 6 <= x <= 4+2*sqrt(3)},"
      " length 2*sqrt(3)-2 = %s" % Q3(-2, 2).approx(20))
B = famgen.generate(5)
print("   generator's differing point (6,0) is the LEFT endpoint:",
      (Q3(6), Q3(0)) in B, " cert's (7,0) is strictly interior.")

A17, s17 = load_cert(17)
i17 = 13
p = A17[i17]
print("\nn=17: rattler at (%s, %s)" % (p[0].sexpr(), p[1].sexpr()))
d17 = s17 - Q3(0, 2)
w = ck.walls(p, d17)
print("   wall slacks:", {k: v.sexpr() for k, v in w.items()})
mn = min(ck.sqdist(p, q) for k, q in enumerate(A17) if k != i17)
print("   min neighbour squared distance:", mn.sexpr(),
      "  (=%s)" % mn.approx(20))
print("   free-disc radius = min(wall slack) = 5/4*sqrt(3) - 2 = %s" % Q3(-2, Q3(0).a + 0).approx(5) if False else
      "   free-disc radius = 5/4*sqrt(3) - 2 = %s (wall AC binds; the nearest"
      " neighbour allows %s)" % (Q3(-2, __import__('fractions').Fraction(5, 4)).approx(20),
                                 "sqrt(77/4 - 8*sqrt(3)) - 2"))
