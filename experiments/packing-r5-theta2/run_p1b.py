"""Prong 1b: AUGMENT a critical witness.

Prong 1 found that every witness with alpha(W) = n-1 has gain exactly 0, and that all the
gain lives on witnesses with alpha(W) far below n-1.  Since theta' is monotone under
induced subgraphs (W subset W' => theta'(G_d[W]) <= theta'(G_d[W'])), the way to keep the
criticality and buy gain is to ADD points to a critical witness.  That is exactly the
"ring-augmented grid" attacks/r4-theta suggested.  This script does it.

Checkpoints to results_p1b.json.
"""
from __future__ import annotations

import argparse, json, math, os, time
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _deps

_deps.require("run_p1b.py")   # fail fast, before the numeric imports below

import numpy as np
import mpmath as mp
import theta2_core as T

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_p1b.json")


def append(rec):
    d = []
    if os.path.exists(OUT):
        try:
            d = json.load(open(OUT))
        except Exception:
            d = []
    d.append(rec)
    json.dump(d, open(OUT, "w"), indent=1)


def dedup(pts, tol=mp.mpf('1e-9')):
    out = []
    for p in pts:
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > tol for q in out):
            out.append(p)
    return out


def run(tag, n, d, pts, tl=45.0):
    pts = dedup(pts)
    if not T.inside(pts, d):
        print(f"  {tag}: outside"); return None
    adj, ties, gap = T.adjacency(pts)
    N = len(pts)
    a = T.alpha_exact(adj)
    solver = "CLARABEL" if N <= 60 else "SCS"
    t0 = time.time()
    lb, sv, st = T.theta_prime_repaired(adj, solver=solver, time_limit=tl)
    rec = dict(tag=tag, n=n, d=float(d), N=N, alpha=a, theta_lb=lb, solver_value=sv,
               status=st, solver=solver, gain=lb - a, critical=(a == n - 1),
               reaches_n=bool(lb >= n), t=time.time() - t0, ties=ties)
    append(rec)
    print(f"  {tag:40s} N={N:4d} alpha={a:3d}{'*' if a == n-1 else ' '} "
          f"theta'>={lb:8.4f} gain={lb-a:+7.4f} [{st}] {rec['t']:.1f}s", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=900.0)
    args = ap.parse_args()
    t0 = time.time()
    probes = [(7, T.KNOWN_D[7] - 0.01), (8, T.KNOWN_D[8] - 0.01),
              (12, T.KNOWN_D[12] - 0.01), (15, T.KNOWN_D[15] - 0.01),
              (16, 2 + 4 * math.sqrt(3) + 0.001), (16, 9.2395)]
    rng = np.random.default_rng(20260824)
    for (n, d) in probes:
        if time.time() - t0 > args.budget - 60:
            print("budget"); return
        inr = float(d) / (2 * math.sqrt(3))
        print(f"\n=== n={n} d={float(d):.5f}  (alpha(G_d) should be {n-1}) ===", flush=True)
        for ref in (1, 2):
            base = T.w_anchored_grid(d, ref)
            b = run(f"n{n}/base-grid-ref{ref}", n, d, base)
            if b is None:
                continue
            # (a) grid + one ring
            for m in (11, 13, 17, 19, 23):
                for frac in (0.5, 0.75, 0.9):
                    if time.time() - t0 > args.budget - 40:
                        return
                    R = frac * inr
                    if 2 * R * math.sin(math.pi / m) >= 2:
                        continue
                    run(f"n{n}/grid{ref}+ring{m}@{frac}", n, d,
                        base + T.w_ring(d, m, R))
            # (b) grid + boundary points
            for ps in (4, 6, 9):
                for ins in (0.0, 0.5):
                    if time.time() - t0 > args.budget - 40:
                        return
                    run(f"n{n}/grid{ref}+edge{ps}@{ins}", n, d,
                        base + T.w_edge_ring(d, ps, ins))
            # (c) grid + random extras (many seeds: the cheapest way to break perfection)
            for k in (6, 12, 20):
                for s in range(3):
                    if time.time() - t0 > args.budget - 40:
                        return
                    r = np.random.default_rng(555 + 17 * k + s)
                    run(f"n{n}/grid{ref}+rnd{k}/{s}", n, d, base + T.w_random(d, k, r))
            # (d) everything at once
            if time.time() - t0 < args.budget - 60:
                run(f"n{n}/grid{ref}+ring17+edge6", n, d,
                    base + T.w_ring(d, 17, 0.75 * inr) + T.w_edge_ring(d, 6, 0.5))
    print("done %.0f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
