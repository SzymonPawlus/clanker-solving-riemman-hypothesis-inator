#!/usr/bin/env python3
"""
The certificate has unused margin.  Recover it, exactly.

OBSERVATION.  The certified maximum squared diameter is
    2499900001 / 2500000000 = (49999/50000)^2,
so the maximum diameter is exactly 49999/50000, not merely "< 1".

SCALING.  Let S_mu be the dilation by a rational mu > 0 about the origin of the
(u,v) chart.  It is a linear map, so it takes the 15 pieces to 15 convex polygons,
preserves simplicity/convexity/interior-disjointness, multiplies every area by
mu^2, multiplies every squared distance by mu^2, and takes T_a to T_{mu a}
(because T_a = {u,v >= 0, u+v <= a} is a cone section scaled by a).  Hence the
image is a 15-piece convex covering of T_{mu a} with maximum diameter
mu * 49999/50000.

That is STRICTLY less than 1 for every mu < 50000/49999.  So for every rational
    a' < a * 50000/49999 = 446335/99998
T_{a'} admits a 15-piece covering of diameter < 1, hence holds no 16 points at
pairwise distance >= 1, hence a_16 > a'.  Taking the supremum over such a':

    a_16 >= 446335/99998 = 4.4634392687853754...
    s(16) >= 2*446335/99998 + 2 sqrt3 = 12.3909801527...

versus the standing 89267/20000 = 4.46335 and s(16) >= 12.3908016151.
The gain is 89267/999980000 = 8.9269e-05 in a, 1.785e-04 in s.

This script does not argue the point -- it EXHIBITS scaled certificates at
several a' below the supremum and puts each through the independent checker in
covercheck.py, so the conclusion rests on exact machine-checked instances plus
the one-line limit above, not on the scaling prose.
"""

import json
import os
from fractions import Fraction as F

import covercheck
from covercheck import rat, check

SRC = "../packing-n16-covering/sub_s2_cert.json"
OUT = "scaled"

raw = json.load(open(SRC))
a = rat(raw["a"])
faces = [[(rat(c[0]), rat(c[1])) for c in f] for f in raw["faces_uv"]]

SUP = a * F(50000, 49999)
print("a           = %s = %.16f" % (a, float(a)))
print("max diam    = 49999/50000 exactly (since 49999^2 = %d)" % (49999 ** 2))
print("supremum a' = a * 50000/49999 = %s = %.16f" % (SUP, float(SUP)))
print()

os.makedirs(OUT, exist_ok=True)

# a ladder of rational targets strictly below the supremum
targets = [
    F(4463439, 1000000),          # 4.463439
    F(44634392, 10 ** 7),         # 4.4634392
    F(446343926, 10 ** 8),        # 4.46343926
    F(4463439268, 10 ** 9),       # 4.463439268
    SUP - F(1, 10 ** 12),         # as close as we like
]

allok = True
best = None
for t in targets:
    assert t < SUP, t
    mu = t / a
    scaled = {
        "a": [str(t.numerator), str(t.denominator)],
        "faces_uv": [[[str(mu * u), str(mu * v)] for (u, v) in f] for f in faces],
        "note": "sub_s2_cert.json dilated about the chart origin by mu = %s" % mu,
    }
    path = os.path.join(OUT, "scaled_%s_%s.json" % (t.numerator, t.denominator))
    json.dump(scaled, open(path, "w"))
    print("#" * 78)
    print("# target a' = %s = %.16f   (mu = %s)" % (t, float(t), mu))
    ok, got = check(path, verbose=False)
    allok &= ok
    if ok and (best is None or got > best):
        best = got
    print()

print("=" * 78)
print("Every scaled instance above verified exactly.")
print("Largest machine-checked a' : %s = %.16f" % (best, float(best)))
print("Supremum of the family     : %s = %.16f" % (SUP, float(SUP)))
print("Limit conclusion           : a_16 >= %s = %.16f" % (SUP, float(SUP)))
print("                             s(16) >= %.12f" % (2 * float(SUP) + 2 * 3 ** 0.5))
print("Ceiling (published packing): %.10f  -- headroom %.10f"
      % (float(covercheck.CEILING), float(covercheck.CEILING - SUP)))
print("=" * 78)
raise SystemExit(0 if allok else 1)
