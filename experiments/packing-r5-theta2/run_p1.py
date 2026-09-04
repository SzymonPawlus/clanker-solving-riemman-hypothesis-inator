"""Prong 1: sweep structurally different witness families and measure gain = theta' - alpha.

Firing the one-sided ceiling gate at n needs a witness W in T_d, d < d(n), with
theta'(G_d[W]) >= n.  Since alpha(W) <= alpha(G_d) = n-1 there, that means gain >= 1.
attacks/r4-theta observed a best gain of +0.447 over 20 solves.  This script asks whether
any of six further families does better.

Checkpoints to results_p1.json after every solve.  Honour --budget (seconds).
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

_deps.require("run_p1.py")   # fail fast, before the numeric imports below

import numpy as np
import mpmath as mp

import theta2_core as T

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_p1.json")


def append(rec):
    data = []
    if os.path.exists(OUT):
        try:
            data = json.load(open(OUT))
        except Exception:
            data = []
    data.append(rec)
    json.dump(data, open(OUT, "w"), indent=1)


def measure(tag, family, params, n, d, pts, want_chi=False, time_limit=25.0):
    d = float(d)
    if not T.inside(pts, d):
        return {"tag": tag, "family": family, "params": params, "n": n, "d": d,
                "skipped": "outside T_d"}
    adj, ties, gap = T.adjacency(pts)
    N = len(pts)
    t0 = time.time()
    a = T.alpha_exact(adj)
    t_alpha = time.time() - t0
    solver = "CLARABEL" if N <= 60 else "SCS"
    t0 = time.time()
    lb, sv, st = T.theta_prime_repaired(adj, solver=solver, time_limit=time_limit)
    t_solve = time.time() - t0
    rec = {"tag": tag, "family": family, "params": params, "n": n, "d": d, "N": N,
           "alpha": a, "theta_lb": lb, "solver_value": sv, "status": st,
           "solver": solver, "gain": lb - a, "ties": ties, "min_gap": float(gap),
           "t_alpha": t_alpha, "t_solve": t_solve, "reaches_n": bool(lb >= n)}
    if want_chi and N <= 40:
        try:
            rec["chi_bar_f"] = T.chi_bar_f(adj)
        except Exception:
            pass
    append(rec)
    print(f"  {tag:34s} N={N:4d} alpha={a:3d} theta'>={lb:8.4f} gain={lb - a:+7.4f} "
          f"[{st}] {t_solve:.1f}s")
    return rec


def probes():
    """(n, d, label).  d just below the `cited` d(n): there alpha(G_d) = n-1 exactly."""
    eps = 0.01
    out = []
    for n in (7, 8, 11, 12, 13, 15):
        out.append((n, T.KNOWN_D[n] - eps, "just-below-d(n)"))
    # n = 16 is OPEN: 8.9282 is the covering plateau of unmerged PRs #98/#104 (`sketch`,
    # quoted only), 9.2395 sits just under the best-known construction 9.2495.
    out.append((16, 2 + 4 * math.sqrt(3) + 0.001, "just-above-covering-plateau"))
    out.append((16, 9.2395, "just-below-best-known"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=900.0)
    ap.add_argument("--stage", default="all")
    args = ap.parse_args()
    t_start = time.time()

    def left():
        return args.budget - (time.time() - t_start)

    rng = np.random.default_rng(20260824)

    for (n, d, lab) in probes():
        if left() < 30:
            print("budget exhausted"); return
        print(f"\n=== n={n}  d={d:.6f}  ({lab})   Oler={T.oler_floor(n):.4f} ===")
        inr = d / (2 * math.sqrt(3))          # inradius: max ring radius about centroid

        # --- baseline: anchored grid (the family attacks/r4-theta used) --------------
        for ref in (1, 2, 3):
            if left() < 30: break
            measure(f"n{n}/grid/ref{ref}", "G-anchored-grid", {"refine": ref}, n, d,
                    T.w_anchored_grid(d, ref))

        # --- FAMILY R: single equally spaced ring (the lane's own suggestion) --------
        for m in (5, 7, 9, 11, 13, 15, 17, 19, 21, 23):
            for frac in (0.35, 0.55, 0.75, 0.95):
                R = frac * inr
                if 2 * R * math.sin(math.pi / m) >= 2:      # no edges at all: trivial
                    continue
                if left() < 20: break
                measure(f"n{n}/ring/m{m}/R{frac}", "R-ring", {"m": m, "R": R}, n, d,
                        T.w_ring(d, m, R), want_chi=True)

        # --- FAMILY CR: concentric rings (+ optional centre) -------------------------
        for (m1, m2) in ((5, 10), (7, 14), (5, 11), (6, 12), (9, 9), (7, 12)):
            for (f1, f2) in ((0.35, 0.85), (0.45, 0.9), (0.3, 0.7)):
                for ctr in (False, True):
                    if left() < 20: break
                    spec = [(m1, f1 * inr, 0.0), (m2, f2 * inr, math.pi / m2)]
                    if ctr:
                        spec = [(1, 0.0, 0.0)] + spec
                    measure(f"n{n}/conc/{m1}+{m2}/{f1},{f2}{'+c' if ctr else ''}",
                            "CR-concentric", {"m1": m1, "m2": m2, "f1": f1, "f2": f2,
                                              "centre": ctr}, n, d,
                            T.w_concentric(d, spec), want_chi=True)

        # --- FAMILY E: boundary / edge-anchored -------------------------------------
        for ps in (3, 4, 5, 6, 7, 8, 9, 10, 12):
            for ins in (0.0, 0.4, 0.8):
                if left() < 20: break
                measure(f"n{n}/edge/{ps}/in{ins}", "E-edge-ring",
                        {"per_side": ps, "inset": ins}, n, d,
                        T.w_edge_ring(d, ps, ins), want_chi=True)

        # --- FAMILY CF: corner fans --------------------------------------------------
        for pc in (1, 2, 3):
            for radii in ([1.0, 2.2], [0.0, 2.0, 3.5], [1.2, 2.6, 4.0]):
                if left() < 20: break
                pts = T.w_corner_fan(d, pc, radii)
                measure(f"n{n}/fan/{pc}/{radii}", "CF-corner-fan",
                        {"per_corner": pc, "radii": radii}, n, d, pts, want_chi=True)

        # --- FAMILY C5: unions of C_5 clusters (gains add over components) -----------
        for R5 in (1.10, 1.35, 1.60):
            for k in (2, 3, 4, 5, 6, 7):
                if left() < 20: break
                # k cluster centres on a shrunken triangle / centroid pattern
                cx, cy = T.centroid(d)
                rad = float(d) / 2 - R5 - 0.05
                if rad <= 0:
                    continue
                centers = [(cx + rad * mp.cos(2 * mp.pi * i / k + mp.mpf('0.2')) / 1.15,
                            cy + rad * mp.sin(2 * mp.pi * i / k + mp.mpf('0.2')) / 1.15)
                           for i in range(k)]
                pts = T.w_c5_clusters(d, centers, R5)
                measure(f"n{n}/c5/{k}x/R{R5}", "C5-clusters",
                        {"k": k, "R": R5}, n, d, pts, want_chi=True)

        # --- FAMILY PG: perturbed lattice -------------------------------------------
        for ref in (1, 2):
            for sig in (0.05, 0.12, 0.25, 0.4):
                for s in range(2):
                    if left() < 20: break
                    r2 = np.random.default_rng(1000 * ref + int(100 * sig) + s)
                    measure(f"n{n}/pgrid/ref{ref}/s{sig}/{s}", "PG-perturbed-grid",
                            {"refine": ref, "sigma": sig, "seed": s}, n, d,
                            T.w_perturbed_grid(d, ref, sig, r2))

        # --- FAMILY RND: random point sets ------------------------------------------
        for Np in (12, 18, 24, 30):
            for s in range(3):
                if left() < 20: break
                r3 = np.random.default_rng(7000 + 13 * Np + s)
                measure(f"n{n}/rnd/N{Np}/{s}", "RND-random", {"N": Np, "seed": s}, n, d,
                        T.w_random(d, Np, r3))

    print("\ndone, elapsed %.0f s" % (time.time() - t_start))


if __name__ == "__main__":
    main()
