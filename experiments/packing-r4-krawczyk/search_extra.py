"""Bounded multistart SLSQP maximin search -- a FRONT END only, floats only.

CONSTRUCTION SIDE ONLY.  Output is a hypothesis, never a certificate: it is fed to
run_all.py, which is where every accept/reject decision is made in exact arithmetic.

Run:  python3 search_extra.py <n> <restarts>

A *restart count*, not a wall-clock budget, so the artifact does not depend on how loaded the
machine was.  The starting points come from ``default_rng(SEED + n)`` and SLSQP is
deterministic, so the best over the first R restarts is a deterministic function of (n, R).

Used only for the n where the candidates already on disk are visibly worse local optima
than the published Graham-Lubachevsky packing.
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
from scipy.optimize import NonlinearConstraint, minimize

SQRT3 = np.sqrt(3.0)
SEED = 20260824
OUTDIR = os.path.join(os.path.dirname(__file__), "out", "extra")


def unpack(v, n):
    return v[: 2 * n].reshape(n, 2), v[2 * n]


def solve_once(n, pts0, rng):
    v0 = np.concatenate([pts0.reshape(-1), [0.0]])
    iu = np.triu_indices(n, 1)

    def obj(v):
        return -v[2 * n]

    def obj_grad(v):
        g = np.zeros_like(v)
        g[2 * n] = -1.0
        return g

    def cons(v):
        p, t = unpack(v, n)
        dif = p[iu[0]] - p[iu[1]]
        sep = (dif ** 2).sum(axis=1) - t
        return np.concatenate([sep, p[:, 1], SQRT3 * p[:, 0] - p[:, 1],
                               SQRT3 * (1 - p[:, 0]) - p[:, 1]])

    nc = NonlinearConstraint(cons, 0.0, np.inf)
    res = minimize(obj, v0, jac=obj_grad, constraints=[nc], method="SLSQP",
                   options={"maxiter": 400, "ftol": 1e-14})
    p, t = unpack(res.x, n)
    if t <= 0:
        return None, -1.0
    d = np.sqrt(((p[iu[0]] - p[iu[1]]) ** 2).sum(axis=1)).min()
    slack = min(p[:, 1].min(), (SQRT3 * p[:, 0] - p[:, 1]).min(),
                (SQRT3 * (1 - p[:, 0]) - p[:, 1]).min())
    if slack < -1e-9:
        return None, -1.0
    return p, d


def main():
    n = int(sys.argv[1])
    restarts = int(sys.argv[2])
    rng = np.random.default_rng(SEED + n)
    os.makedirs(OUTDIR, exist_ok=True)
    best_m, best_p, tries = -1.0, None, 0
    t0 = time.time()
    for _ in range(restarts):
        tries += 1
        a = rng.random((n, 2))
        m = a.sum(axis=1) > 1
        a[m] = 1 - a[m]
        pts = np.column_stack([a[:, 0] + a[:, 1] * 0.5, a[:, 1] * SQRT3 / 2])
        p, d = solve_once(n, pts, rng)
        if p is not None and d > best_m:
            best_m, best_p = d, p
            with open(os.path.join(OUTDIR, f"n{n}.json"), "w") as fh:
                json.dump({
                    "n": n,
                    "claim": "construction (hypothesis)",
                    "status": "numerical",
                    "note": "Floating-point optimiser output. NOT a certificate.",
                    "unit_triangle_points": best_p.tolist(),
                    "m_min_pairwise_distance_unit_triangle": float(best_m),
                    "D_side_of_centre_triangle": float(2.0 / best_m),
                    "seed": SEED + n, "restarts_used": tries,
                    "numpy": np.__version__,
                }, fh, indent=2)
    print(f"n={n} restarts={tries} seconds={time.time() - t0:.0f} best_m={best_m!r} "
          f"D={2.0 / best_m!r}", flush=True)


if __name__ == "__main__":
    main()
