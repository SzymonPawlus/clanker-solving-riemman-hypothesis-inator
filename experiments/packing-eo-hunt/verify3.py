"""A THIRD, from-scratch exact checker, sharing no representation with the other two.

Rationale (problem ``RULES.md`` SS3, and the manager's instruction to re-verify any candidate from
a freshly constructed checker): ``exact_check.py`` has a barycentric checker and a Q(sqrt3)
Cartesian checker. This one is built from a different observation entirely and is the simplest of
the three.

Put the triangle at (0,0), (L,0), (L/2, L*sqrt(3)/2) with L rational. Any point that is a rational
convex combination of the vertices has the form

    (x, y) = (x, t*sqrt(3))      with x, t RATIONAL.

Then every test is a comparison between rationals, with sqrt(3) divided out by hand:

    y >= 0                  <=>  t >= 0
    sqrt(3) x - y >= 0      <=>  x - t >= 0        (divide by sqrt 3 > 0)
    sqrt(3)(L - x) - y >= 0 <=>  L - x - t >= 0
    |P-Q|^2                  =   (dx)^2 + 3 (dt)^2

No barycentric distance formula, no field class, no sign-by-squaring. Reads the certificate file
and re-derives (x, t) from the stored barycentric triples using only the vertex coordinates.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))


def verify(bary_strings, side_string, min_sep_sq=1, k=None):
    L = F(side_string)
    # vertices: (0, 0), (L, 0), (L/2, (L/2)*sqrt3)  -> stored as (x, t) with y = t*sqrt3
    VX = [F(0), L, L / 2]
    VT = [F(0), F(0), L / 2]
    pts = []
    for trip in bary_strings:
        l = [F(s) for s in trip]
        assert sum(l) == 1, f"barycentric triple does not sum to 1: {trip}"
        x = sum(l[i] * VX[i] for i in range(3))
        t = sum(l[i] * VT[i] for i in range(3))
        pts.append((x, t))

    bad_containment = []
    for i, (x, t) in enumerate(pts):
        if not (t >= 0):
            bad_containment.append((i, "below bottom edge"))
        if not (x - t >= 0):
            bad_containment.append((i, "outside left edge"))
        if not (L - x - t >= 0):
            bad_containment.append((i, "outside right edge"))

    n = len(pts)
    dmin2 = None
    arg = None
    for i in range(n):
        for j in range(i + 1, n):
            dx = pts[i][0] - pts[j][0]
            dt = pts[i][1] - pts[j][1]
            d2 = dx * dx + 3 * dt * dt
            if dmin2 is None or d2 < dmin2:
                dmin2, arg = d2, (i, j)

    out = {
        "n": n,
        "side": str(L),
        "side_float": float(L),
        "contained_exact": not bad_containment,
        "containment_violations": bad_containment,
        "min_sq_distance": str(dmin2),
        "min_sq_distance_float": float(dmin2),
        "closest_pair": arg,
        "separation_ok": dmin2 >= min_sep_sq,
    }
    if k is not None:
        out["side_below_k_minus_1"] = L < k - 1
        out["fits_strictly_below_side_k_minus_1"] = bool(
            out["contained_exact"] and out["separation_ok"] and out["side_below_k_minus_1"]
        )
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "control-n26.json")
    d = json.load(open(path))
    r = verify(d["certificate_barycentric"], d["certificate_side"], k=7)
    print(f"third checker on {os.path.basename(path)}")
    for key in ("n", "side", "side_float", "contained_exact", "min_sq_distance_float",
                "separation_ok", "side_below_k_minus_1", "fits_strictly_below_side_k_minus_1"):
        print(f"  {key:36s} {r[key]}")
    print(f"  min squared distance (exact)         {r['min_sq_distance'][:70]}...")
    print(f"  closest pair                         {r['closest_pair']}")
    json.dump(r, open(os.path.join(HERE, "out", "verify3-n26.json"), "w"), indent=2)
