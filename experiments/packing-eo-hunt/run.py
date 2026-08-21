"""Driver for the Erdos-Oler counterexample hunt. Everything it writes is ``numerical``.

Subcommands
-----------
    bench     time one SLSQP solve at each target n; writes out/bench.json
    validate  reproduce the PROVEN cases k = 2..6 (n = 2,5,9,14,20). Must return exactly
              m = 1/(k-1) and must not exceed it. Gate before any target run.
    hunt      the sweep at one k, checkpointing to out/hunt-k<k>-<tag>.json

Usage:
    uv run run.py bench
    uv run run.py validate
    uv run run.py hunt --k 7 --seconds 600 --seed 1 --tag a
"""

from __future__ import annotations

import argparse
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
os.makedirs(OUT, exist_ok=True)

ABORT_TOL = 1e-9  # a solve above threshold + this halts the sweep for the exact gate


def _env():
    import scipy

    return {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    }


def cmd_bench(args):
    rng = np.random.default_rng(0)
    rows = []
    for k in (5, 6, 7, 8, 9, 10):
        n = H.tri(k) - 1
        t0 = time.perf_counter()
        reps = 5 if n <= 40 else 3
        for _ in range(reps):
            H.local_solve(H.seed_uniform(n, rng))
        dt = (time.perf_counter() - t0) / reps
        rows.append({"k": k, "n": n, "seconds_per_solve": dt})
        print(f"k={k} n={n:3d}  {dt * 1000:8.1f} ms/solve")
    json.dump({"env": _env(), "rows": rows}, open(os.path.join(OUT, "bench.json"), "w"), indent=2)


def cmd_validate(args):
    """The proven cases. An optimiser that beats these is broken, not brilliant."""
    out = []
    ok = True
    for k in range(2, 7):
        n = H.tri(k) - 1
        thr = 1.0 / (k - 1)
        rng = np.random.default_rng(1000 + k)
        best_m, best_p = -1.0, None
        t0 = time.perf_counter()
        budget = 4.0 if n <= 9 else (12.0 if n <= 14 else 30.0)
        fams = H.SEED_FAMILIES
        i = 0
        while time.perf_counter() - t0 < budget:
            fam = fams[i % len(fams)]
            i += 1
            p, m = H.local_solve(H.make_seed(fam, n, k, rng))
            if m > best_m:
                p, m = H.polish(p)
                if m > best_m:
                    best_m, best_p = m, p
        digits = -math.log10(abs(best_m - thr)) if best_m != thr else 16.0
        exceeded = best_m > thr + 1e-9
        # exact gate on the best, exactly as a real candidate would be treated
        verdict, detail = gate(best_p.tolist(), k, verbose=False)
        row = {
            "k": k,
            "n": n,
            "threshold_m": thr,
            "best_m": best_m,
            "agreement_digits": digits,
            "float_exceeds_threshold": bool(exceeded),
            "exact_gate_refutes": bool(verdict),
            "exact_q_min": str(detail["barycentric"]["q_min"]),
            "exact_a_min": detail["barycentric"]["a_min_float"],
            "solves": i,
        }
        out.append(row)
        good = (digits >= 10) and not verdict
        ok = ok and good
        print(
            f"k={k} n={n:2d}  best_m={best_m:.15f}  target={thr:.15f}  "
            f"digits={digits:5.1f}  exact a_min={detail['barycentric']['a_min_float']:.12f}  "
            f"{'OK' if good else 'FAIL'}"
        )
    json.dump(
        {"env": _env(), "rows": out, "all_ok": bool(ok)},
        open(os.path.join(OUT, "validate.json"), "w"),
        indent=2,
    )
    print("VALIDATION", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def _checkpoint(path, census, meta):
    top = sorted(census.counts.items(), key=lambda kv: -kv[0])[:40]
    doc = {
        "status": "numerical",
        "note": (
            "Floating-point optimiser output. NOT a certificate and NOT an optimality claim. "
            "Points are in the unit equilateral triangle (0,0),(1,0),(1/2,sqrt(3)/2); the "
            "separation-1 side is a = 1/m. Erdos-Oler(k) fails iff m > 1/(k-1)."
        ),
        **meta,
        "solves": census.solves,
        "best_m": census.best_m,
        "best_a": 1.0 / census.best_m if census.best_m > 0 else None,
        "threshold_m": census.threshold,
        "threshold_a": 1.0 / census.threshold,
        "best_minus_threshold": census.best_m - census.threshold,
        "hits_threshold": census.hits_threshold,
        "n_over_threshold": len(census.over_threshold),
        "runner_up_m": census.runner_up,
        "runner_up_a": 1.0 / census.runner_up if census.runner_up > 0 else None,
        "runner_up_gap": census.threshold - census.runner_up if census.runner_up > 0 else None,
        "distinct_local_optima": len(census.counts),
        "top_local_optima": [{"m": v, "count": c} for v, c in top],
        "by_family": census.by_family,
        "best_points": census.best_p.tolist() if census.best_p is not None else None,
        "runner_up_points": (
            census.runner_up_p.tolist() if census.runner_up_p is not None else None
        ),
        "best_corner_counts": (
            H.corner_counts(census.best_p, census.best_m) if census.best_p is not None else None
        ),
        "runner_up_corner_counts": (
            H.corner_counts(census.runner_up_p, census.runner_up)
            if census.runner_up_p is not None
            else None
        ),
    }
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, indent=2)
    os.replace(tmp, path)


def cmd_hunt(args):
    k = args.k
    n = H.tri(k) - 1
    thr = 1.0 / (k - 1)
    rng = np.random.default_rng(args.seed)
    census = H.Census(n=n, k=k, threshold=thr)
    path = os.path.join(OUT, f"hunt-k{k}-{args.tag}.json")
    meta = {
        "k": k,
        "n": n,
        "seed": args.seed,
        "tag": args.tag,
        "time_budget_seconds": args.seconds,
        "env": _env(),
        "aborted_for_exact_gate": False,
    }
    t0 = time.perf_counter()
    last_ckpt = t0
    fams = list(H.SEED_FAMILIES)
    elites: list[tuple[float, np.ndarray]] = []
    i = 0
    phase_a = args.seconds * args.multistart_fraction
    while True:
        el = time.perf_counter() - t0
        if el > args.seconds:
            break
        if el < phase_a or not elites or rng.random() < 0.35:
            fam = fams[i % len(fams)]
            p0 = H.make_seed(fam, n, k, rng)
        else:
            fam = "hop"
            j = int(rng.integers(0, len(elites)))
            p0 = H.perturb(elites[j][1], elites[j][0], rng)
        i += 1
        p, m = H.local_solve(p0, maxiter=args.maxiter)
        if m > thr - 1e-6:
            p, m = H.polish(p)
        census.offer(p, m, fam)
        # elite pool, kept diverse by value
        if m > 0 and (len(elites) < args.elites or m > elites[-1][0]):
            if not any(abs(m - e[0]) < 1e-10 for e in elites):
                elites.append((m, p.copy()))
                elites.sort(key=lambda e: -e[0])
                del elites[args.elites :]
        if m > thr + ABORT_TOL:
            meta["aborted_for_exact_gate"] = True
            meta["abort_m"] = m
            _checkpoint(path, census, meta)
            print(f"!! ABORT: local solve at m={m!r} exceeds 1/{k - 1}={thr!r}; running exact gate")
            verdict, detail = gate(p.tolist(), k)
            meta["exact_gate_verdict"] = bool(verdict)
            meta["exact_q_min"] = str(detail["barycentric"]["q_min"])
            meta["exact_a_min"] = detail["barycentric"]["a_min_float"]
            _checkpoint(path, census, meta)
            if verdict:
                print("CANDIDATE COUNTEREXAMPLE -- stopping. Needs the RULES.md SS7 procedure.")
                return 2
            print("exact gate refuted it (float slop). Continuing.")
            meta["aborted_for_exact_gate"] = False
        if time.perf_counter() - last_ckpt > args.checkpoint_every:
            _checkpoint(path, census, meta)
            last_ckpt = time.perf_counter()
            print(
                f"[k={k} {args.tag}] {el:6.0f}s solves={census.solves:6d} "
                f"best={census.best_m:.12f} (thr {thr:.12f}) "
                f"hits={census.hits_threshold} runner_up={census.runner_up:.12f}",
                flush=True,
            )
    meta["elapsed_seconds"] = time.perf_counter() - t0
    _checkpoint(path, census, meta)
    print(
        f"[k={k} {args.tag}] DONE solves={census.solves} best={census.best_m!r} "
        f"thr={thr!r} over={len(census.over_threshold)} runner_up={census.runner_up!r}"
    )
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("bench")
    sub.add_parser("validate")
    h = sub.add_parser("hunt")
    h.add_argument("--k", type=int, required=True)
    h.add_argument("--seconds", type=float, default=600.0)
    h.add_argument("--seed", type=int, default=1)
    h.add_argument("--tag", type=str, default="a")
    h.add_argument("--maxiter", type=int, default=250)
    h.add_argument("--elites", type=int, default=8)
    h.add_argument("--multistart-fraction", type=float, default=0.4)
    h.add_argument("--checkpoint-every", type=float, default=20.0)
    args = ap.parse_args(argv)
    if args.cmd == "bench":
        return cmd_bench(args)
    if args.cmd == "validate":
        return cmd_validate(args)
    return cmd_hunt(args)


if __name__ == "__main__":
    raise SystemExit(main())
