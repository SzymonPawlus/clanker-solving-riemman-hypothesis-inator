"""Positive control: n = 26 really does fit in a triangle of side a < 6.

Two things nothing else in this directory tests.

1. **The search's power to find a sub-lattice-side packing.** The Erdos-Oler hunt asks whether 27
   points fit in a < 6. Twenty-six points *do*: the published record is
   d(26) = 0.166738399395271 > 1/6 (Graham-Lubachevsky 1995), i.e. a = 5.99742... < 6, and its
   optimum is irregular, not a lattice fragment. If the machinery cannot rediscover that, then a
   negative result at n = 27 says little, because n = 26 is precisely the shape of thing a
   counterexample at n = 27 would be. This is the most informative validation available here.

2. **The positive branch of the exact gate.** Every other run makes ``exact_check.gate`` return
   False. A gate that only ever says "no" is not evidence of anything. Here it must say "yes":
   26 exact rational points, pairwise separation >= 1, inside an exactly rational side a < 6.

Neither is a claim about Erdos-Oler. n = 26 is not Delta(k) - 1 for any k; it is a control.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hunt as H  # noqa: E402
from exact_check import check_barycentric, check_cartesian, to_rational_barycentric  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
REF_D26 = 0.166738399395271  # Graham-Lubachevsky 1995, 15 s.f. -- reference, not computed here
THRESHOLD = 1.0 / 6.0  # the k = 7 Erdos-Oler side, a = 6


def main(seconds=240.0, seed=26262626):
    n = 26
    k = 7  # only to reuse the seed families' spacing prior; n is NOT Delta(7) - 1
    rng = np.random.default_rng(seed)
    census = H.Census(n=n, k=k, threshold=THRESHOLD)
    t0 = time.perf_counter()
    fams = list(H.SEED_FAMILIES)
    elites = []
    i = 0
    while time.perf_counter() - t0 < seconds:
        if time.perf_counter() - t0 < seconds * 0.4 or not elites or rng.random() < 0.35:
            fam = fams[i % len(fams)]
            p0 = H.make_seed(fam, n, k, rng)
        else:
            fam = "hop"
            j = int(rng.integers(0, len(elites)))
            p0 = H.perturb(elites[j][1], elites[j][0], rng)
        i += 1
        p, m = H.local_solve(p0)
        p, m = H.polish(p)
        census.offer(p, m, fam)
        if m > 0 and (len(elites) < 8 or m > elites[-1][0]):
            if not any(abs(m - e[0]) < 1e-10 for e in elites):
                elites.append((m, p.copy()))
                elites.sort(key=lambda e: -e[0])
                del elites[8:]

    best_m, best_p = census.best_m, census.best_p
    rel = abs(best_m - REF_D26) / REF_D26
    digits = -math.log10(rel) if rel > 0 else float("inf")
    print(f"n=26 solves={census.solves} best_m={best_m:.15f} ref={REF_D26:.15f} digits={digits:.2f}")
    print(f"      best a = 1/m = {1.0 / best_m:.15f}   (must be < 6 to be a sub-6 packing of 26)")

    # --- exact gate, positive branch -------------------------------------------------------
    # Round to rationals, then find the largest exact rational side a < 6 that still holds them
    # at separation >= 1. The rounding LOSES separation, so a_exact >= a_float always.
    result = {"search": {"solves": census.solves, "best_m": best_m, "ref_d26": REF_D26,
                         "agreement_digits": digits, "by_family": census.by_family}}
    for max_den in (10**6, 10**8, 10**10, 10**12):
        bary = to_rational_barycentric(best_p.tolist(), max_den=max_den)
        r1 = check_barycentric(bary, k=7)
        a_min = r1["a_min_float"]
        print(f"  max_den=1e{int(math.log10(max_den))}: exact q_min={float(r1['q_min']):.15f} "
              f"a_min={a_min:.15f} contained={r1['contained_exact']} "
              f"beats a=6: {r1['refutes_EO']}")
        result[f"exact_den_1e{int(math.log10(max_den))}"] = {
            "q_min": str(r1["q_min"]),
            "a_min_float": a_min,
            "contained_exact": r1["contained_exact"],
            "fits_below_side_6": bool(r1["refutes_EO"]),
        }
        if r1["refutes_EO"]:
            # cross-check in the independent Q(sqrt 3) Cartesian checker at a rational side < 6
            from fractions import Fraction as F

            side = F(math.ceil(a_min * 10**6) + 1, 10**6)
            r2 = check_cartesian(bary, side * side, k=7)
            print(f"      Q(sqrt3) checker at exact side {side} = {float(side):.9f}: "
                  f"contained={r2['contained_exact']} sep>=1: {r2['separation_at_least_1']} "
                  f"side<6: {r2['side_below_k_minus_1']}")
            result[f"exact_den_1e{int(math.log10(max_den))}"]["cartesian"] = {
                "side": str(side),
                "side_float": float(side),
                "contained_exact": r2["contained_exact"],
                "separation_at_least_1": r2["separation_at_least_1"],
                "side_below_6": r2["side_below_k_minus_1"],
                "both_checkers_agree": bool(r1["refutes_EO"] == r2["refutes_EO"]),
            }
            result["certificate_barycentric"] = [[str(c) for c in l] for l in bary]
            result["certificate_side"] = str(side)
            break
    result["best_points_unit_triangle"] = best_p.tolist()
    result["status"] = "numerical (search) + exact (certificate)"
    json.dump(result, open(os.path.join(OUT, "control-n26.json"), "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(float(sys.argv[1]) if len(sys.argv) > 1 else 240.0))
