"""Multistart maximin search: n points in the closed unit equilateral triangle, maximise the
minimum pairwise distance m.  Upper-bound lane for n = 16 (attack n16-upper-2, issue #97).

Written from scratch for this lane; shares no code with experiments/packing-n16-upper/ or
experiments/circle-packing-search/.

Conventions (re-derived in targets.py):
    a = 1/m   (covering-lane side, separation 1)
    d = 2/m   (repo point-formulation side, separation 2)
    s = 2/m + 2*sqrt(3)   (side of the triangle holding n unit circles)

Usage:
    python3 search.py --n 16 --starts 1500 --seed 20260822 --out out/n16.json

Floats are for search only (problem RULES.md section 5); the exact gate is exact_gate.py.
Library versions used for the recorded runs: numpy 2.4.6, scipy 1.17.1, Python 3.11.15.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np
from scipy.optimize import minimize

SQRT3 = math.sqrt(3.0)


def pair_index(n: int) -> tuple[np.ndarray, np.ndarray]:
    iu = np.triu_indices(n, k=1)
    return iu[0], iu[1]


def constraints_fun(z: np.ndarray, n: int, ii: np.ndarray, jj: np.ndarray) -> np.ndarray:
    pts = z[: 2 * n].reshape(n, 2)
    t = z[-1]
    dx = pts[ii, 0] - pts[jj, 0]
    dy = pts[ii, 1] - pts[jj, 1]
    pair = dx * dx + dy * dy - t * t
    x, y = pts[:, 0], pts[:, 1]
    walls = np.concatenate([y, SQRT3 * x - y, SQRT3 * (1.0 - x) - y])
    return np.concatenate([pair, walls])


def constraints_jac(z: np.ndarray, n: int, ii: np.ndarray, jj: np.ndarray) -> np.ndarray:
    npair = len(ii)
    pts = z[: 2 * n].reshape(n, 2)
    t = z[-1]
    J = np.zeros((npair + 3 * n, 2 * n + 1))
    dx = pts[ii, 0] - pts[jj, 0]
    dy = pts[ii, 1] - pts[jj, 1]
    rows = np.arange(npair)
    J[rows, 2 * ii] = 2 * dx
    J[rows, 2 * ii + 1] = 2 * dy
    J[rows, 2 * jj] = -2 * dx
    J[rows, 2 * jj + 1] = -2 * dy
    J[rows, -1] = -2 * t
    for k in range(n):
        J[npair + k, 2 * k + 1] = 1.0                      # y_k >= 0
        J[npair + n + k, 2 * k] = SQRT3                    # sqrt3 x - y >= 0
        J[npair + n + k, 2 * k + 1] = -1.0
        J[npair + 2 * n + k, 2 * k] = -SQRT3               # sqrt3 (1-x) - y >= 0
        J[npair + 2 * n + k, 2 * k + 1] = -1.0
    return J


def min_dist(pts: np.ndarray) -> float:
    n = len(pts)
    ii, jj = pair_index(n)
    d = np.hypot(pts[ii, 0] - pts[jj, 0], pts[ii, 1] - pts[jj, 1])
    return float(d.min())


def project_into_triangle(pts: np.ndarray) -> np.ndarray:
    """Clamp points into the closed unit triangle (used on seeds and on solver output before
    measuring m, so the reported m is always for a strictly feasible configuration)."""
    out = pts.copy()
    for _ in range(50):
        moved = False
        y = out[:, 1]
        bad = y < 0
        out[bad, 1] = 0.0
        # left edge: sqrt3 x - y >= 0 ; unit inward normal (sqrt3/2, -1/2)
        g = SQRT3 * out[:, 0] - out[:, 1]
        bad = g < 0
        if bad.any():
            out[bad, 0] -= (SQRT3 / 2) * (g[bad] / 2)
            out[bad, 1] += 0.5 * (g[bad] / 2)
            moved = True
        g = SQRT3 * (1.0 - out[:, 0]) - out[:, 1]
        bad = g < 0
        if bad.any():
            out[bad, 0] += (SQRT3 / 2) * (g[bad] / 2)
            out[bad, 1] += 0.5 * (g[bad] / 2)
            moved = True
        if not moved and (out[:, 1] >= 0).all():
            break
    return out


def feasible_m(pts: np.ndarray) -> float:
    """m of the projection of pts into the closed triangle. Projection can only move points
    inward by the (tiny) violation, so this is an honest, if very slightly conservative,
    feasible value."""
    q = project_into_triangle(pts)
    y = q[:, 1]
    g1 = SQRT3 * q[:, 0] - y
    g2 = SQRT3 * (1.0 - q[:, 0]) - y
    if not (y.min() >= -1e-15 and g1.min() >= -1e-12 and g2.min() >= -1e-12):
        return float("nan")
    q[:, 1] = np.maximum(q[:, 1], 0.0)
    return min_dist(q)


# ---------------------------------------------------------------- seed families

def tri_lattice(rows: int) -> np.ndarray:
    """rows-row triangular lattice filling the unit triangle: T(rows) points."""
    pts = []
    for r in range(rows):  # r = 0 top ... rows-1 bottom
        yfrac = 1.0 - r / (rows - 1) if rows > 1 else 0.0
        y = yfrac * SQRT3 / 2
        count = r + 1
        for k in range(count):
            xw = (1.0 - yfrac)
            x = 0.5 - xw / 2 + (k / r * xw if r > 0 else 0.0)
            pts.append((x, y))
    return np.array(pts)


def sample_uniform(rng: np.random.Generator, n: int) -> np.ndarray:
    r1 = np.sqrt(rng.random(n))
    r2 = rng.random(n)
    A = np.array([0.0, 0.0]); B = np.array([1.0, 0.0]); C = np.array([0.5, SQRT3 / 2])
    return (1 - r1)[:, None] * A + (r1 * (1 - r2))[:, None] * B + (r1 * r2)[:, None] * C


def make_seed(rng: np.random.Generator, family: str, n: int, best: np.ndarray | None) -> np.ndarray:
    if family == "uniform":
        return sample_uniform(rng, n)
    if family == "lattice_defect":
        lat = tri_lattice(6)  # T(6) = 21
        if n > len(lat):
            return sample_uniform(rng, n)
        idx = rng.choice(len(lat), size=n, replace=False)
        pts = lat[idx] + rng.normal(scale=0.01, size=(n, 2))
        return project_into_triangle(pts)
    if family == "t5_plus_one":
        lat = tri_lattice(5)  # T(5) = 15
        extra = sample_uniform(rng, max(n - len(lat), 1))
        pts = np.vstack([lat, extra])[:n] + rng.normal(scale=0.01, size=(n, 2))
        return project_into_triangle(pts)
    if family == "perturb_best":
        if best is None:
            return sample_uniform(rng, n)
        pts = best + rng.normal(scale=rng.choice([0.002, 0.01, 0.05]), size=best.shape)
        return project_into_triangle(pts)
    raise ValueError(family)


# ---------------------------------------------------------------- solver

def solve_once(seed_pts: np.ndarray) -> tuple[np.ndarray, float]:
    n = len(seed_pts)
    ii, jj = pair_index(n)
    z0 = np.concatenate([seed_pts.ravel(), [max(min_dist(seed_pts), 1e-3)]])
    cons = [{
        "type": "ineq",
        "fun": constraints_fun, "jac": constraints_jac,
        "args": (n, ii, jj),
    }]
    obj = lambda z: -z[-1]
    grad = np.zeros(2 * n + 1); grad[-1] = -1.0
    res = minimize(obj, z0, jac=lambda z: grad, constraints=cons, method="SLSQP",
                   options={"maxiter": 400, "ftol": 1e-14})
    pts = res.x[: 2 * n].reshape(n, 2)
    return pts, feasible_m(pts)


def run(n: int, starts: int, seed: int, out_path: str, time_budget_s: float) -> dict:
    rng = np.random.default_rng(seed)
    families = ["uniform", "lattice_defect", "t5_plus_one", "perturb_best"]
    best_m, best_pts = -1.0, None
    counts = {f: 0 for f in families}
    t0 = time.time()
    for k in range(starts):
        if time.time() - t0 > time_budget_s:
            break
        family = families[k % len(families)]
        seed_pts = make_seed(rng, family, n, best_pts)
        pts, m = solve_once(seed_pts)
        counts[family] += 1
        if math.isfinite(m) and m > best_m:
            best_m, best_pts = m, pts.copy()
            save(out_path, n, seed, best_m, best_pts, counts, time.time() - t0, done=False)
    elapsed = time.time() - t0
    save(out_path, n, seed, best_m, best_pts, counts, elapsed, done=True)
    return {"n": n, "best_m": best_m, "counts": counts, "elapsed_s": elapsed}


def save(path: str, n: int, seed: int, best_m: float, best_pts: np.ndarray | None,
         counts: dict, elapsed: float, done: bool) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    payload = {
        "n": n, "rng_seed": seed, "best_m": best_m,
        "best_a": (1.0 / best_m) if best_m and best_m > 0 else None,
        "best_s": (2.0 / best_m + 2 * SQRT3) if best_m and best_m > 0 else None,
        "points_unit_triangle": best_pts.tolist() if best_pts is not None else None,
        "solves_per_family": counts, "elapsed_s": elapsed, "complete": done,
        "versions": {"numpy": np.__version__},
    }
    with open(path, "w") as fh:
        json.dump(payload, fh, indent=1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--starts", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20260822)
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--time-budget", type=float, default=900.0)
    args = ap.parse_args()
    summary = run(args.n, args.starts, args.seed, args.out, args.time_budget)
    print(json.dumps(summary, indent=1))
