"""The targeted attack: take a packing of Delta(k) - 2 points that genuinely beats side k-1,
and try to insert one more point.

Why this is the sharpest move available. Erdos-Oler(k) says Delta(k) - 1 points force side k-1.
One point fewer does *not*: the best known Delta(k) - 2 packings sit strictly below side k-1
(e.g. d(26) = 0.16673839... > 1/6, i.e. a = 5.99742... < 6). So a counterexample to EO(k) is
exactly "a Delta(k)-2 packing below side k-1 with room for one more point". Rather than hoping a
random multi-start stumbles into it, this script starts from the sub-(k-1) packings and hunts the
insertion directly:

  stage 1  search for the best Delta(k) - 2 configurations (an elite pool, not just the best);
  stage 2  for each elite, try inserting the extra point at every locally-deepest hole plus a
           dense grid of candidate sites, and re-optimise the resulting Delta(k) - 1 points;
  stage 3  report the best Delta(k) - 1 separation obtained, against 1/(k-1).

Also runs the reverse move ("delete one, reinsert elsewhere") on the incumbent Delta(k)-1
configuration, which is the same degree of freedom approached from the other side.

Status: ``numerical``. A hit here is a hypothesis and goes straight to ``exact_check.gate``.
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
from exact_check import gate  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def candidate_sites(p: np.ndarray, m: float, rng, grid_mult: float = 0.22, keep: int = 220):
    """Sites where a new point could go: a triangular grid over T plus random jitter, ranked by
    clearance (distance to the nearest existing point). The deepest holes come first."""
    step = max(m * grid_mult, 1e-3)
    pts = []
    y = 0.0
    while y <= H.HALF_SQRT3 + 1e-12:
        xlo, xhi = y / H.SQRT3, 1.0 - y / H.SQRT3
        x = xlo
        while x <= xhi + 1e-12:
            pts.append((x, y))
            x += step
        y += step * H.HALF_SQRT3
    g = np.array(pts) if pts else H.seed_uniform(200, rng)
    g = np.vstack([g, H.seed_uniform(400, rng)])
    d = np.linalg.norm(g[:, None, :] - p[None, :, :], axis=-1).min(axis=1)
    order = np.argsort(-d)[:keep]
    return g[order], d[order]


def stage1(k, seconds, rng):
    """Elite pool of Delta(k) - 2 configurations."""
    n2 = H.tri(k) - 2
    elites = []
    t0 = time.perf_counter()
    fams = list(H.SEED_FAMILIES)
    i = 0
    best = -1.0
    while time.perf_counter() - t0 < seconds:
        if not elites or rng.random() < 0.5:
            p0 = H.make_seed(fams[i % len(fams)], n2, k, rng)
        else:
            j = int(rng.integers(0, len(elites)))
            p0 = H.perturb(elites[j][1], elites[j][0], rng)
        i += 1
        p, m = H.local_solve(p0)
        p, m = H.polish(p)
        if not math.isfinite(m) or m <= 0:
            continue
        best = max(best, m)
        if len(elites) < 12 or m > elites[-1][0]:
            if not any(abs(m - e[0]) < 1e-9 for e in elites):
                elites.append((m, p.copy()))
                elites.sort(key=lambda e: -e[0])
                del elites[12:]
    return elites, i, best


def run_k(k, stage1_seconds, stage2_seconds, seed):
    rng = np.random.default_rng(seed)
    n1, n2 = H.tri(k) - 1, H.tri(k) - 2
    thr = 1.0 / (k - 1)
    print(f"--- k={k}: insert into Delta(k)-2 = {n2} to reach {n1}; threshold m > {thr!r}")
    elites, solves1, best2 = stage1(k, stage1_seconds, rng)
    print(f"  stage 1: {solves1} solves, best m({n2}) = {best2!r} (a = {1.0 / best2!r})")
    print(f"           elites: {[round(e[0], 12) for e in elites]}")

    best_m, best_p, best_src = -1.0, None, None
    tried = 0
    t0 = time.perf_counter()
    # stage 2: insertion
    ei = 0
    while time.perf_counter() - t0 < stage2_seconds and elites:
        m2, p2 = elites[ei % len(elites)]
        ei += 1
        sites, clear = candidate_sites(p2, m2, rng)
        for s in sites:
            if time.perf_counter() - t0 > stage2_seconds:
                break
            p0 = np.vstack([p2, s[None, :]])
            p, m = H.local_solve(p0)
            if m > thr - 1e-5:
                p, m = H.polish(p)
            tried += 1
            if m > best_m:
                best_m, best_p, best_src = m, p.copy(), ("insert", float(m2))
    # stage 3: delete-and-reinsert on the incumbent Delta(k)-1
    t1 = time.perf_counter()
    if best_p is not None:
        cur_p, cur_m = best_p.copy(), best_m
        while time.perf_counter() - t1 < stage2_seconds * 0.35:
            i = int(rng.integers(0, n1))
            rest = np.delete(cur_p, i, axis=0)
            rp, rm = H.local_solve(rest)
            sites, _ = candidate_sites(rp, rm, rng, keep=40)
            for s in sites:
                p0 = np.vstack([rp, s[None, :]])
                p, m = H.local_solve(p0)
                if m > thr - 1e-5:
                    p, m = H.polish(p)
                tried += 1
                if m > best_m:
                    best_m, best_p, best_src = m, p.copy(), ("delete_reinsert", float(rm))
            if best_m > cur_m:
                cur_p, cur_m = best_p.copy(), best_m

    print(f"  stage 2+3: {tried} insertions, best m({n1}) = {best_m!r}")
    print(f"             threshold {thr!r}; excess = {best_m - thr!r}")
    verdict, detail = gate(best_p.tolist(), k, verbose=False)
    print(f"             exact gate: a_min = {detail['barycentric']['a_min_float']!r}, "
          f"refutes EO({k}) = {verdict}")
    return {
        "k": k,
        "n_minus_2": n2,
        "n": n1,
        "threshold_m": thr,
        "threshold_a": float(k - 1),
        "stage1_solves": solves1,
        "best_m_n_minus_2": best2,
        "best_a_n_minus_2": 1.0 / best2,
        "elite_ms": [e[0] for e in elites],
        "insertions_tried": tried,
        "best_m": best_m,
        "best_a": 1.0 / best_m if best_m > 0 else None,
        "excess_over_threshold": best_m - thr,
        "exact_a_min": detail["barycentric"]["a_min_float"],
        "exact_q_min": str(detail["barycentric"]["q_min"]),
        "exact_refutes": bool(verdict),
        "best_points": best_p.tolist() if best_p is not None else None,
        "source_move": best_src,
    }


if __name__ == "__main__":
    ks = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [7]
    s1 = float(sys.argv[2]) if len(sys.argv) > 2 else 120.0
    s2 = float(sys.argv[3]) if len(sys.argv) > 3 else 240.0
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 424242
    rows = [run_k(k, s1, s2, seed + k) for k in ks]
    json.dump(
        {"status": "numerical", "rows": rows},
        open(os.path.join(OUT, f"insert-k{'-'.join(map(str, ks))}.json"), "w"),
        indent=2,
    )
