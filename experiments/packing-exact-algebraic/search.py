"""Multi-start SLSQP search for good point configurations (candidate generator only).

Status of everything this file produces: `numerical`. It is a hypothesis generator; the exact
certificate is what counts, and that is produced by construct.py and checked by exact_check.py.

Formulation matches the repo convention: n points in the closed equilateral triangle
A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2), pairwise distance >= 2, minimise d.
Then s = d + 2*sqrt(3).

Reproduce:  python3 search.py --nmax 15 --starts 300 --seed 20260819
"""
from __future__ import annotations

import argparse
import json
import math

import numpy as np
from scipy.optimize import minimize

R3 = math.sqrt(3.0)


def solve_n(n: int, starts: int, seed: int):
    rng = np.random.default_rng(seed + 1000 * n)
    best = None
    d0 = 2.0 * math.sqrt(n) + 2.0
    for _ in range(starts):
        d = d0 * (1.0 + 0.3 * rng.random())
        # random points inside the triangle via barycentric sampling
        u = rng.random((n, 3))
        u /= u.sum(axis=1, keepdims=True)
        P = u @ np.array([[0.0, 0.0], [d, 0.0], [d / 2, d * R3 / 2]])
        z0 = np.concatenate([P.ravel(), [d]])

        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]

        def unpack(z):
            return z[:-1].reshape(n, 2), z[-1]

        def cons_f(z):
            P, d = unpack(z)
            out = []
            if pairs:
                diff = P[[i for i, _ in pairs]] - P[[j for _, j in pairs]]
                out.append((diff ** 2).sum(axis=1) - 4.0)
            out.append(P[:, 1])
            out.append(R3 * P[:, 0] - P[:, 1])
            out.append(R3 * (d - P[:, 0]) - P[:, 1])
            return np.concatenate(out)

        res = minimize(lambda z: z[-1], z0, method="SLSQP",
                       constraints=[{"type": "ineq", "fun": cons_f}],
                       options={"maxiter": 400, "ftol": 1e-14})
        z = res.x
        P, d = unpack(z)
        if cons_f(z).min() < -1e-9:
            continue
        if best is None or d < best[0]:
            best = (d, P.copy())
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=15)
    ap.add_argument("--nmin", type=int, default=1)
    ap.add_argument("--starts", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20260819)
    ap.add_argument("--out", default="search_results.json")
    a = ap.parse_args()

    out = {}
    for n in range(a.nmin, a.nmax + 1):
        d, P = solve_n(n, a.starts, a.seed)
        out[str(n)] = {"d": d, "s": d + 2 * R3, "points": P.tolist()}
        print(f"n={n:3d}  d={d:.12f}  s={d + 2 * R3:.12f}", flush=True)
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
