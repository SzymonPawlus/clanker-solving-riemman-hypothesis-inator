"""Turn the polished high-precision n = 16 configuration into an exact rational certificate in
the repo convention (problem RULES.md section 2):

    16 points, pairwise distance >= 2, in the closed equilateral triangle
    A = (0,0), B = (d,0), C = (d/2, d*sqrt3/2),  d = s - 2*sqrt3,  side_length = s.

Recipe (all margins chosen so every rounding loss is orders of magnitude below the slack):
  1. scale the unit-triangle points by rational d_cert chosen ~1e-13 relatively above 2/m,
     so the min pairwise distance is 2*(1 + ~1e-13);
  2. contract toward the incenter by (1 - eta), eta = 1e-14: every point acquires distance
     >= eta * inradius ~ 2.7e-14 from the boundary while distances shrink by only (1 - eta);
  3. round every coordinate to a rational with denominator 10**18 (moves each point < 7.1e-19).

The result is checked EXACTLY (Fractions, no floats) by exact_gate.py; this script only builds
the candidate JSON.
"""
from __future__ import annotations

import json
from fractions import Fraction

from mpmath import mp, mpf, sqrt, nstr

mp.dps = 60

DEN = 10 ** 18          # coordinate denominator
DDEN = 10 ** 15         # denominator for d_cert
EPS = mpf("1e-13")      # relative inflation of d over 2/m
ETA = mpf("1e-14")      # contraction toward incenter


def main() -> None:
    with open("out/n16-polished.json") as fh:
        pol = json.load(fh)
    pts = [(mpf(p[0]), mpf(p[1])) for p in pol["points_unit_triangle"]]
    m = mpf(pol["m"])

    d_star = 2 / m
    # rational d_cert = ceil(d_star * (1 + EPS) * DDEN) / DDEN
    target = d_star * (1 + EPS) * DDEN
    d_num = int(mp.ceil(target))
    d_cert = Fraction(d_num, DDEN)
    d_mp = mpf(d_num) / DDEN

    s3 = sqrt(mpf(3))
    cx, cy = d_mp / 2, d_mp / (2 * s3)      # incenter
    coords = []
    for (ux, uy) in pts:
        x = d_mp * ux
        y = d_mp * uy
        x = cx + (1 - ETA) * (x - cx)
        y = cy + (1 - ETA) * (y - cy)
        qx = Fraction(int(mp.nint(x * DEN)), DEN)
        qy = Fraction(int(mp.nint(y * DEN)), DEN)
        coords.append((qx, qy))

    cert = {
        "n": 16,
        "claim": "construction",
        "side_length": f"{d_cert.numerator}/{d_cert.denominator} + 2*sqrt(3)",
        "side_length_note": (
            "s = d + 2*sqrt(3) with d = " f"{d_cert.numerator}/{d_cert.denominator}"
            " exactly; numerically s = " + nstr(d_mp + 2 * s3, 22)
        ),
        "coordinates": [[f"{q.numerator}/{q.denominator}" for q in p] for p in coords],
        "coordinate_type": "rational",
        "verified_by": "experiments/packing-n16-upper-2/exact_gate.py",
        "status": "numerical",
        "beats_record": (
            "no; reproduces Melissen & Schuur (1995) / Graham & Lubachevsky (1995) "
            "d(16)=0.216227269309782 to all 15 printed digits; this exact certificate sits "
            "~9.3e-13 above the numerical optimum by construction"
        ),
    }
    with open("out/n16-certificate.json", "w") as fh:
        json.dump(cert, fh, indent=1)
    print("d_cert =", d_cert, "=", nstr(d_mp, 22))
    print("s_cert = d + 2*sqrt3  =", nstr(d_mp + 2 * s3, 22))
    print("s_float optimum       =", nstr(2 / m + 2 * s3, 22))
    print("certificate excess    =", nstr(d_mp - d_star, 8))


if __name__ == "__main__":
    main()
