"""Prong 2 driver: scan lam_SOS(m, d), then bisect the crossings lam = n.

d*_m(n) := sup{ d : lam_SOS(m,d) < n }  is a theta'-derived floor candidate for d(n):
lam_SOS(m,d) >= theta'(G_d) >= alpha(G_d), so lam_SOS(m,d) < n forces alpha(G_d) < n,
i.e. d(n) > d.  Every number is float SDP output => `numerical`, not a proof.

Checkpoints to results_p2.json after every solve.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _deps

_deps.require("run_p2.py")   # fail fast, before sos_theta pulls in numpy/scipy/cvxpy

import sos_theta as S

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_p2.json")


def load():
    if os.path.exists(OUT):
        try:
            return json.load(open(OUT))
        except Exception:
            return []
    return []


def append(rec):
    data = load()
    data.append(rec)
    json.dump(data, open(OUT, "w"), indent=1)


def one(m, d, tl):
    t0 = time.time()
    r = S.solve_lambda(m, d, time_limit=tl)
    rec = {"m": m, "d": float(d), "lam": r["lam"], "status": r["status"],
           "t": time.time() - t0, "sizes": r["sizes"]}
    append(rec)
    print(f"  m={m} d={d:.6f}: lam={rec['lam']:.6f} [{rec['status']}] {rec['t']:.1f}s",
          flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=1200.0)
    ap.add_argument("--ms", default="2,3,4")
    ap.add_argument("--tl", type=float, default=120.0)
    args = ap.parse_args()
    t0 = time.time()

    def left():
        return args.budget - (time.time() - t0)

    for m in [int(x) for x in args.ms.split(",")]:
        print(f"=== m = {m} ===", flush=True)
        # coarse scan
        grid = [2.0, 2.4, 2.8, 3.2, 3.4641016151, 3.8, 4.0, 4.4, 4.8, 5.2,
                5.4641016152, 5.8, 5.8297, 6.2, 6.6, 7.0]
        vals = {}
        for d in grid:
            if left() < args.tl + 20:
                print("budget"); return
            r = one(m, d, args.tl)
            vals[d] = r
            if r["status"] not in ("optimal", "optimal_inaccurate"):
                break
        # bisect the crossings lam = n for n = 4..12, and the feasibility edge
        feas = [d for d in vals if vals[d]["status"] in ("optimal", "optimal_inaccurate")]
        if not feas:
            continue
        lo_ok = max(feas)
        hi_bad = min([d for d in vals if d > lo_ok], default=None)
        if hi_bad is not None:
            a, b = lo_ok, hi_bad
            for _ in range(6):
                if left() < args.tl + 20:
                    break
                mid = 0.5 * (a + b)
                r = one(m, mid, args.tl)
                if r["status"] in ("optimal", "optimal_inaccurate"):
                    a = mid
                else:
                    b = mid
            append({"m": m, "feasibility_edge": [a, b]})
            print(f"  m={m}: SOS feasible up to d in [{a:.5f}, {b:.5f}]", flush=True)

        for n in (4, 5, 6, 7, 8, 9, 10, 11, 12):
            ok = [d for d in feas if vals[d]["lam"] < n]
            bad = [d for d in feas if vals[d]["lam"] >= n]
            if not ok or not bad:
                continue
            a, b = max(ok), min([d for d in bad if d > max(ok)], default=None)
            if b is None:
                continue
            for _ in range(8):
                if left() < args.tl + 20:
                    break
                mid = 0.5 * (a + b)
                r = one(m, mid, args.tl)
                vals[mid] = r
                if r["status"] in ("optimal", "optimal_inaccurate"):
                    feas.append(mid)
                    if r["lam"] < n:
                        a = mid
                    else:
                        b = mid
                else:
                    b = mid
            append({"m": m, "n": n, "d_star": a, "bracket": [a, b],
                    "oler": math.sqrt(8 * n + 1) - 3,
                    "known_d": S and None})
            print(f"  m={m} n={n}: d*_m(n) >= {a:.6f}  (Oler {math.sqrt(8*n+1)-3:.6f})",
                  flush=True)

    print("done %.0f s" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
