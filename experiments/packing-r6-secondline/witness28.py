"""EXACT witness: 28 points at pairwise distance >= 1 in the CLOSED triangle T(6).

claim kind: CONSTRUCTION.  status: numerical (exact rational arithmetic; no floats).

Why this matters here.  r5-eo7 §7 measures its delta-robust counting bound on the grid at
a = 6 and reports "max bound 28, target 26, loss 2 units".  This script establishes that at
a = 6 the TRUE maximum is at least 28, so *no correct upper bound whatsoever* can return
<= 26 there.  The 28 is not slack in the relaxation; it is the answer.

Points: p(i,j) = (j/2 + i, j*sqrt3/2), j = 0..6, i = 0..6-j.  Row j has 7-j points, total 28.
Every coordinate is (rational) + (rational)*sqrt3 with the sqrt3 part carried symbolically as
y/sqrt3, so every test below is a comparison of exact rationals.
"""
from fractions import Fraction as F
import json

A = 6  # side

pts = []                       # (x, Y) with the real point (x, Y*sqrt3)
for j in range(7):
    for i in range(7 - j):
        pts.append((F(j, 2) + i, F(j, 2)))
assert len(pts) == 28

# containment in the closed T(6):  y >= 0 ; sqrt3*x - y >= 0 ; sqrt3*(6-x) - y >= 0
# with y = Y*sqrt3 these are  Y >= 0 ; x - Y >= 0 ; (6-x) - Y >= 0   (exact rationals)
inside = all(Y >= 0 and x - Y >= 0 and (A - x) - Y >= 0 for (x, Y) in pts)

# pairwise squared distance = (dx)^2 + 3*(dY)^2, exact rational
mind2 = None
for u in range(28):
    for v in range(u + 1, 28):
        dx = pts[u][0] - pts[v][0]
        dY = pts[u][1] - pts[v][1]
        d2 = dx * dx + 3 * dY * dY
        if mind2 is None or d2 < mind2:
            mind2 = d2

res = {"n": len(pts), "side_a": A, "all_inside_closed_T6": bool(inside),
       "min_pairwise_squared_distance": str(mind2),
       "separation_ok(>=1)": bool(mind2 >= 1),
       "coordinate_type": "exact: x rational, y = Y*sqrt3 with Y rational",
       "conclusion": "T(6) contains 28 points at pairwise distance >= 1, so ANY correct "
                     "upper bound at a = 6 is >= 28.  A target of <= 26 at a = 6 is unreachable."}
print(json.dumps(res, indent=1))
json.dump(res, open("out/witness28.json", "w"), indent=1)
assert inside and mind2 == 1
