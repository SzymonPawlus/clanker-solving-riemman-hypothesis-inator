"""How good can a ROTATED hexagonal lattice be? A restricted but sharp sub-question.

Noticed while sanity-checking the seed families: a hexagonal lattice at spacing ~1/(k-1), placed
at a random rotation and offset, does not even *hold* Delta(k)-1 points inside the unit triangle.
The aligned T(k) lattice holds T(k) = Delta(k) because every one of its boundary points sits
exactly on an edge; rotate it and that boundary bonus is destroyed.

That turns into a question worth answering directly, because "a differently oriented lattice
fragment" is the most obvious shape for a counterexample:

    over all rotations theta and offsets, what is the LARGEST spacing s of a hexagonal lattice
    such that at least Delta(k)-1 of its points lie in the unit equilateral triangle?

If that maximum is 1/(k-1), attained only at the aligned orientation, then no rotated-lattice
fragment beats the T(k) lattice -- a genuine, if heavily restricted, negative result about where
a counterexample cannot be.

Method: for fixed (theta, offset) the count is non-increasing in s, so bisect on s for the largest
s with count >= n; maximise over a deterministic grid of theta plus random (theta, offset) draws.
Status: `numerical`. It samples (theta, offset); it does not prove anything about the ones it
missed, and a lattice fragment is not the only shape a packing can take.
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hunt as H  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def count_inside(s, theta, off, need):
    """How many points of the hex lattice (spacing s, rotation theta, offset off) lie in T."""
    c, sn = math.cos(theta), math.sin(theta)
    rad = int(math.ceil(2.0 / s)) + 3
    i = np.arange(-rad, rad + 1)
    I, J = np.meshgrid(i, i, indexing="ij")
    I = I.ravel()
    J = J.ravel()
    vx = s * (I + 0.5 * J)
    vy = s * (H.HALF_SQRT3 * J)
    x = vx * c - vy * sn + off[0]
    y = vx * sn + vy * c + off[1]
    inside = (y >= -1e-12) & (H.SQRT3 * x - y >= -1e-12) & (H.SQRT3 * (1.0 - x) - y >= -1e-12)
    return int(inside.sum())


def best_spacing(theta, off, n, lo=0.05, hi=0.35):
    """Largest s with count >= n, by bisection (count is non-increasing in s)."""
    if count_inside(lo, theta, off, n) < n:
        return 0.0
    if count_inside(hi, theta, off, n) >= n:
        return hi
    for _ in range(46):
        mid = 0.5 * (lo + hi)
        if count_inside(mid, theta, off, n) >= n:
            lo = mid
        else:
            hi = mid
    return lo


def main(k=7, n_random=3000, seed=13131313):
    n = H.tri(k) - 1
    thr = 1.0 / (k - 1)
    rng = np.random.default_rng(seed)
    best = (-1.0, None)
    aligned = None

    # deterministic sweep: theta on a grid, offset on a grid within one lattice cell
    for ti in range(0, 61):
        th = math.radians(ti)
        for ox in np.linspace(0.0, 1.0, 9):
            for oy in np.linspace(0.0, H.HALF_SQRT3, 9):
                s = best_spacing(th, (float(ox), float(oy)), n)
                if s > best[0]:
                    best = (s, (math.degrees(th), float(ox), float(oy), "grid"))
                if ti == 0 and abs(ox) < 1e-12 and abs(oy) < 1e-12:
                    aligned = s
    # random draws
    for _ in range(n_random):
        th = float(rng.uniform(0, math.pi / 3))
        off = (float(rng.uniform(-0.2, 1.2)), float(rng.uniform(-0.2, 1.0)))
        s = best_spacing(th, off, n)
        if s > best[0]:
            best = (s, (math.degrees(th), off[0], off[1], "random"))

    print(f"k={k}, n=Delta(k)-1={n}, aligned lattice spacing 1/(k-1) = {thr!r}")
    print(f"aligned-at-origin bisection recovers s = {aligned!r}")
    print(f"best rotated/offset hex lattice holding {n} points: s = {best[0]!r}")
    print(f"  at (theta_deg, ox, oy, source) = {best[1]}")
    print(f"  s - 1/(k-1) = {best[0] - thr:+.6e}   "
          f"({'BEATS the aligned lattice' if best[0] > thr + 1e-12 else 'does NOT beat it'})")
    res = {
        "status": "numerical",
        "k": k,
        "n": n,
        "aligned_spacing": thr,
        "aligned_bisected": aligned,
        "best_rotated_spacing": best[0],
        "best_at": best[1],
        "excess": best[0] - thr,
        "beats_aligned": bool(best[0] > thr + 1e-12),
        "samples": {"grid_thetas": 61, "grid_offsets": 81, "random": n_random},
    }
    json.dump(res, open(os.path.join(OUT, f"lattice-scan-k{k}.json"), "w"), indent=2)
    return res


if __name__ == "__main__":
    for k in [int(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else ["7"])]:
        main(k, n_random=int(sys.argv[2]) if len(sys.argv) > 2 else 3000)
        print()
