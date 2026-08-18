"""Driver: run the search over a range of n, checkpoint, and report against the literature.

    uv run run.py validate                 # the mandatory gate: known n, exact targets
    uv run run.py sweep --min 16 --max 34  # candidate generation for the open range

Checkpoints land in ``out/n<NN>.json`` and are rewritten on every improvement, so a killed run
still leaves its best configuration on disk (repo ``RULES.md`` SS6).
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import platform
import sys
import time

import numpy as np
import scipy

import reference as ref
from search import SQRT3, containment_slack, local_solve, min_pair_distance, search

OUT = pathlib.Path(__file__).parent / "out"

# The validation gate. The kill-criterion in issue #9 names n = 3, 6, 10, 12 specifically; the
# rest are run because they are just as cheap and a wider gate is a stronger gate.
VALIDATE_N = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
GATE_N = [3, 6, 10, 12]
GATE_DIGITS = 8.0


def polish(p: np.ndarray, rounds: int = 4) -> tuple[np.ndarray, float]:
    """Warm-start SLSQP repeatedly from its own output. Each round re-linearises about a point
    already on the active set, which is where SLSQP converges fastest; it typically buys 3-5
    digits over the single solve done during the search."""
    best_p, best_m = p, min_pair_distance(p)
    for _ in range(rounds):
        q, m = local_solve(best_p, maxiter=500, ftol=1e-16)
        if m > best_m:
            best_p, best_m = q, m
    return best_p, best_m


def checkpoint(n: int, m: float, points: np.ndarray, meta: dict) -> None:
    OUT.mkdir(exist_ok=True)
    r = ref.reference_m(n)
    payload = {
        "n": n,
        "claim": "construction (hypothesis)",
        "status": "numerical",
        "note": (
            "Floating-point optimiser output. NOT a certificate and NOT an optimality claim. "
            "Coordinates are in the unit equilateral triangle with vertices (0,0), (1,0), "
            "(1/2, sqrt(3)/2). Multiply by 2/m to reach the point formulation of "
            "problems/circle-packing-equilateral-triangle/README.md."
        ),
        "m_min_pairwise_distance_unit_triangle": m,
        "D_side_of_centre_triangle": 2.0 / m,
        "s_side_for_unit_circles": 2.0 / m + 2.0 * SQRT3,
        "unit_triangle_points": [[float(x), float(y)] for x, y in points],
        "feasibility_floats": {
            "min_pairwise_distance": min_pair_distance(points),
            "containment_slack": containment_slack(points),
        },
        "reference_m": None if r is None else r[0],
        "reference_source": None if r is None else r[1],
        "agreement_digits_vs_reference": None if r is None else ref.agreement_digits(m, r[0]),
        **meta,
    }
    (OUT / f"n{n:02d}.json").write_text(json.dumps(payload, indent=2) + "\n")


def env_meta(seed: int) -> dict:
    return {
        "seed": seed,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }


def run_one(n: int, seed: int, budget: float) -> dict:
    def on_improve(m, p):
        checkpoint(n, m, p, env_meta(seed) | {"stage": "in-progress"})

    res = search(n, seed=seed, time_budget=budget, on_improve=on_improve)
    p, m = polish(res.points)
    checkpoint(
        n,
        m,
        p,
        env_meta(seed)
        | {
            "stage": "final",
            "restarts": res.restarts,
            "basin_hops": res.hops,
            "search_seconds": res.elapsed,
        },
    )
    r = ref.reference_m(n)
    return {
        "n": n,
        "m": m,
        "s": 2.0 / m + 2.0 * SQRT3,
        "ref_m": None if r is None else r[0],
        "ref_src": None if r is None else r[1],
        "digits": None if r is None else ref.agreement_digits(m, r[0]),
        "min_dist": min_pair_distance(p),
        "slack": containment_slack(p),
        "restarts": res.restarts,
        "hops": res.hops,
        "seconds": res.elapsed,
    }


def report(rows: list[dict]) -> None:
    print()
    print(f"{'n':>3} {'best found m':>18} {'published m':>18} {'digits':>7} "
          f"{'best found s':>16} {'published s':>16} {'verdict':>12}  source")
    print("-" * 130)
    for r in rows:
        if r["ref_m"] is None:
            print(f"{r['n']:>3} {r['m']:>18.15f} {'-':>18} {'-':>7} "
                  f"{r['s']:>16.12f} {'-':>16} {'no reference':>12}")
            continue
        ref_s = 2.0 / r["ref_m"] + 2.0 * SQRT3
        d = r["digits"]
        if r["m"] > r["ref_m"] * (1 + 1e-9):
            verdict = "BEATS?!"
        elif d >= 8:
            verdict = "match"
        elif d >= 5:
            verdict = "close"
        else:
            verdict = "MISS"
        ds = "inf" if math.isinf(d) else f"{d:.1f}"
        print(f"{r['n']:>3} {r['m']:>18.15f} {r['ref_m']:>18.15f} {ds:>7} "
              f"{r['s']:>16.12f} {ref_s:>16.12f} {verdict:>12}  {r['ref_src']}")
    print()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["validate", "sweep"])
    ap.add_argument("--min", type=int, default=16)
    ap.add_argument("--max", type=int, default=34)
    ap.add_argument("--seed", type=int, default=20260817)
    ap.add_argument("--budget", type=float, default=8.0, help="seconds of search per n")
    args = ap.parse_args()

    ns = VALIDATE_N if args.mode == "validate" else list(range(args.min, args.max + 1))
    t0 = time.perf_counter()
    rows = []
    for n in ns:
        r = run_one(n, seed=args.seed + n, budget=args.budget)
        rows.append(r)
        print(
            f"n={n:>3}  m={r['m']:.12f}  s={r['s']:.9f}  "
            f"digits={'-' if r['digits'] is None else f'{r['digits']:.1f}'}  "
            f"({r['restarts']} restarts, {r['hops']} hops, {r['seconds']:.1f}s)",
            flush=True,
        )
    report(rows)
    print(f"total wall clock: {time.perf_counter() - t0:.1f}s")

    if args.mode == "validate":
        gate = [r for r in rows if r["n"] in GATE_N]
        failed = [r for r in gate if r["digits"] is None or r["digits"] < GATE_DIGITS]
        if failed:
            print(f"\nKILL-CRITERION MET: {[r['n'] for r in failed]} below "
                  f"{GATE_DIGITS} digits. Approach is refuted as implemented.")
            return 1
        print(f"\nValidation gate PASSED on n={GATE_N} at >= {GATE_DIGITS} significant digits.")
        print("This validates the search pipeline only. Every packing above remains a")
        print("floating-point CONSTRUCTION HYPOTHESIS with status `numerical`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
