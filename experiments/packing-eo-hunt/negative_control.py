"""Negative control for the exact gate: it must REJECT a near-miss.

Problem RULES.md SS0: "every optimiser will return a configuration that is slightly infeasible --
two circles overlapping by 1e-9 -- and will report a side length beating the world record. That
result is always wrong." A gate is only worth something if it catches exactly that. So: take the
T(7) lattice minus its apex (27 points, side exactly 6, separation exactly 1) and shrink the
triangle by a hair. The result "fits 27 points below side 6" -- and is infeasible by ~1e-7, which
a float check at tolerance 1e-9, or a solver reporting its own m, would happily accept.

The gate must say no at every shrink factor, and must say yes at none of them.
"""

from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_check import to_rational_barycentric, check_barycentric  # noqa: E402
from verify3 import verify  # noqa: E402
from fractions import Fraction as F  # noqa: E402

SQRT3 = math.sqrt(3.0)
V = [(0.0, 0.0), (1.0, 0.0), (0.5, SQRT3 / 2.0)]


def lattice_minus_apex(k=7):
    pts = []
    for row in range(k):
        for col in range(row + 1):
            a, b = row / (k - 1), col / (k - 1)
            pts.append((
                (1 - a) * V[0][0] + (a - b) * V[1][0] + b * V[2][0],
                (1 - a) * V[0][1] + (a - b) * V[1][1] + b * V[2][1],
            ))
    return pts[1:]  # drop the apex -> 27 points


def main():
    base = lattice_minus_apex(7)
    bary = to_rational_barycentric(base, max_den=10**7)
    rows = []
    print("negative control: 27 points, lattice minus apex, in a triangle of side 6*(1-eps).")
    print("A float feasibility check with tolerance 1e-9 accepts eps <= ~1e-10; the exact gate")
    print("must reject EVERY row, because the true answer is that they do not fit.")
    print()
    print(f"{'shrink eps':>12} {'side a':>22} {'min sq dist (exact)':>26} {'sep>=1?':>9} {'gate says refutes?':>20}")
    for eps in (1e-3, 1e-5, 1e-7, 1e-9, 1e-12):
        side = F(6) * (1 - F(eps).limit_denominator(10**15))
        r3 = verify([[str(c) for c in t] for t in bary], str(side), k=7)
        # the barycentric gate is scale-free: it reports the LEAST side that works
        r1 = check_barycentric(bary, k=7)
        refutes = bool(r3["contained_exact"] and r3["separation_ok"] and side < 6)
        print(f"{eps:>12.0e} {float(side):>22.15f} {r3['min_sq_distance_float']:>26.18f} "
              f"{str(r3['separation_ok']):>9} {str(refutes):>20}")
        rows.append({"eps": eps, "side": str(side), "side_float": float(side),
                     "min_sq_distance_float": r3["min_sq_distance_float"],
                     "separation_ok": r3["separation_ok"], "gate_refutes": refutes})
    print()
    print(f"least side that actually holds these 27 points at separation 1: "
          f"a_min = {r1['a_min_float']:.15f}  (q_min = {r1['q_min']})")
    print(f"any row reported as a refutation: {any(r['gate_refutes'] for r in rows)}  (must be False)")
    json.dump({"rows": rows, "a_min_float": r1["a_min_float"], "q_min": str(r1["q_min"]),
               "any_false_positive": any(r["gate_refutes"] for r in rows)},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "out", "negative-control.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
