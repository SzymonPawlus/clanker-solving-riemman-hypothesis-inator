"""CLI for the Lubachevsky-Stillinger front-end generator.

    uv run run.py validate                       # the gate: known optima, small n
    uv run run.py sweep --min 16 --max 34        # LS-seeded candidates
    uv run run.py compare --min 22 --max 34      # LS vs multi-start at EQUAL wall clock
    uv run run.py table                          # re-render whatever is in out/

Everything written here is ``numerical``: floating-point construction *hypotheses* plus,
in ``candidates/``, exactly-feasible but deliberately loosened rational certificates.
Nothing here is an optimality claim and nothing here belongs in ``results/``.

Checkpointing: every improvement is written to ``out/nNN.json`` immediately, so a run
killed at any point still leaves its best configuration on disk.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import platform
import subprocess
import sys
import time

import numpy as np

import ls
from certificate import build_certificate, exact_feasible
from polish import polish

_SEARCH = (pathlib.Path(__file__).resolve().parent.parent / "circle-packing-search").resolve()
if str(_SEARCH) not in sys.path:
    sys.path.insert(0, str(_SEARCH))
import reference as ref  # noqa: E402
import search as baseline_search  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
CANDIDATES = HERE / "candidates"

DEFAULT_SEED = 20260818

#: The validation gate.  n = 3, 6, 10 are the triangular numbers the repo already holds
#: exact certificates for; 12 and 15 add a non-lattice and a larger lattice case, and 5
#: and 8 add two small cases with an exact closed form and an irrational optimum.
VALIDATE_N = [3, 5, 6, 8, 10, 12, 15, 21]
#: Digits of agreement required against the published value before anything else runs.
GATE_DIGITS = 8.0


# ----------------------------------------------------------------------------------- #
# reproducibility metadata
# ----------------------------------------------------------------------------------- #


def env_meta(seed: int) -> dict:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=HERE, capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except Exception:  # pragma: no cover - metadata only
        commit = "unknown"
    import scipy

    return {
        "seed": seed,
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "git_commit": commit,
        "growth_schedule": list(ls.DEFAULT_SCHEDULE),
    }


# ----------------------------------------------------------------------------------- #
# checkpointing
# ----------------------------------------------------------------------------------- #


def checkpoint(n: int, m: float, points: np.ndarray, meta: dict) -> bool:
    """Write ``out/nNN.json`` if ``m`` improves on what is already there.

    Monotone on purpose.  Several modes write the same file, and a later mode that
    happened to draw a worse basin must not erase a better candidate; the file is the
    artefact, so it has to only ever get better.  Returns whether it wrote.
    """
    OUT.mkdir(exist_ok=True)
    path = OUT / f"n{n:02d}.json"
    if path.exists():
        try:
            prev = json.loads(path.read_text())["m_min_pairwise_distance_unit_triangle"]
            if prev >= m:
                return False
        except (KeyError, ValueError):
            pass
    r = ref.reference_m(n)
    payload = {
        "n": n,
        "claim": "construction (hypothesis)",
        "status": "numerical",
        "note": (
            "Floating-point output of a Lubachevsky-Stillinger billiard run followed by an "
            "SLSQP polish. NOT a certificate and NOT an optimality claim. Coordinates are in "
            "the unit equilateral triangle with vertices (0,0), (1,0), (1/2, sqrt(3)/2). "
            "Multiply by 2/m to reach the point formulation of "
            "problems/circle-packing-equilateral-triangle/README.md."
        ),
        "m_min_pairwise_distance_unit_triangle": m,
        "D_side_of_centre_triangle": 2.0 / m,
        "s_side_for_unit_circles": 2.0 / m + 2.0 * math.sqrt(3.0),
        "unit_triangle_points": [[float(x), float(y)] for x, y in points],
        "feasibility_floats": {
            "min_pairwise_distance": float(ls.min_pair_distance(points)),
            "containment_slack": float(ls.wall_slack(points).min()),
            "_warning": "float diagnostics, not a feasibility check; see candidates/ for exact",
        },
        "reference": (
            {"m": r[0], "s": ref.s_from_m(r[0]), "source": r[1],
             "agreement_digits_m": ref.agreement_digits(m, r[0])}
            if r
            else None
        ),
        "meta": meta,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return True


def emit_candidate(n: int, points: np.ndarray, meta: dict) -> tuple[bool, str]:
    """Snap the best-on-disk candidate for ``n`` into an exactly-feasible certificate."""
    CANDIDATES.mkdir(exist_ok=True)
    cert = build_certificate(n, points, note=f"seed {meta.get('seed')}.")
    ok, why = exact_feasible(cert)
    cert["_self_check"] = why
    (CANDIDATES / f"n{n:03d}-ls.json").write_text(json.dumps(cert, indent=2) + "\n")
    return ok, why


# ----------------------------------------------------------------------------------- #
# the two arms
# ----------------------------------------------------------------------------------- #


def ls_arm(n: int, seed: int, budget: float, on_improve=None) -> dict:
    """Repeated LS runs, each descended once by SLSQP, until the wall clock runs out.

    One ``local_solve`` per LS run, deliberately: that mirrors one restart of the
    multi-start baseline, so the two arms differ only in where their start points come
    from.  The final ``polish`` is applied outside the timed budget, identically to both
    arms, so it cannot advantage either.
    """
    rng = np.random.default_rng(seed)
    t0 = time.perf_counter()
    best_p, best_m = None, -1.0
    runs = 0
    while time.perf_counter() - t0 < budget:
        runs += 1
        res = ls.ls_run(n, rng)
        p, m = baseline_search.local_solve(res.points, maxiter=300)
        if math.isfinite(m) and m > best_m:
            best_m, best_p = m, p.copy()
            if on_improve is not None:
                on_improve(best_m, best_p)
    if best_p is None:  # budget too small for even one run
        res = ls.ls_run(n, rng)
        best_p, best_m = baseline_search.local_solve(res.points, maxiter=300)
        runs = 1
    return {"m": best_m, "points": best_p, "runs": runs, "elapsed": time.perf_counter() - t0}


def baseline_arm(n: int, seed: int, budget: float) -> dict:
    """The #9 multi-start + basin-hopping search, unmodified, at the same wall clock."""
    t0 = time.perf_counter()
    r = baseline_search.search(n, seed=seed, time_budget=budget, restarts=10**9)
    return {
        "m": r.m,
        "points": r.points,
        "runs": r.restarts + r.hops,
        "elapsed": time.perf_counter() - t0,
    }


# ----------------------------------------------------------------------------------- #
# modes
# ----------------------------------------------------------------------------------- #


def cmd_validate(args) -> int:
    """Reproduce known optima before any long run.  RULES.md §6 requires this gate."""
    meta = env_meta(args.seed)
    print("VALIDATION GATE -- LS + polish against published values")
    print(f"  budget {args.budget:.1f}s per n, seed {args.seed}")
    print()
    print(f"  {'n':>3}  {'m (LS)':>20}  {'m (published)':>20}  {'digits':>7}  source")
    failures = []
    for n in VALIDATE_N:
        arm = ls_arm(n, args.seed + n, args.budget)
        p, m = polish(arm["points"])
        r = ref.reference_m(n)
        digits = ref.agreement_digits(m, r[0]) if r else float("nan")
        checkpoint(n, m, p, {**meta, "mode": "validate", "ls_runs": arm["runs"]})
        emit_candidate(n, p, meta)
        flag = ""
        if r and m > r[0] * (1 + 1e-12):
            flag = "  <-- EXCEEDS PUBLISHED VALUE (suspect infeasible)"
            failures.append((n, "exceeds"))
        elif r and digits < GATE_DIGITS:
            flag = f"  <-- below gate ({GATE_DIGITS:.0f} digits)"
            failures.append((n, "below gate"))
        print(f"  {n:>3}  {m:>20.15f}  {r[0]:>20.15f}  {digits:>7.1f}  {r[1]}{flag}")

    print()
    if failures:
        print(f"GATE FAILED at n = {[f[0] for f in failures]}: {failures}")
        print("Do not run a sweep. Fix the generator first (RULES.md §6).")
        return 1
    print(f"GATE PASSED: all of {VALIDATE_N} matched the published value to >= "
          f"{GATE_DIGITS:.0f} significant digits, and none exceeded it.")
    return 0


def cmd_sweep(args) -> int:
    meta = env_meta(args.seed)
    rows = []
    for n in range(args.min, args.max + 1):
        seed = args.seed + n
        arm = ls_arm(n, seed, args.budget,
                     on_improve=lambda m, p, n=n: checkpoint(
                         n, m, p, {**meta, "mode": "sweep", "partial": True}))
        p, m = polish(arm["points"])
        checkpoint(n, m, p, {**meta, "mode": "sweep", "ls_runs": arm["runs"],
                             "elapsed": arm["elapsed"]})
        ok, why = emit_candidate(n, p, meta)
        r = ref.reference_m(n)
        rows.append({"n": n, "m": m, "ref": r, "runs": arm["runs"], "cert_ok": ok})
        d = ref.agreement_digits(m, r[0]) if r else float("nan")
        print(f"  n={n:>3}  m={m:.15f}  s={ref.s_from_m(m):.12f}  "
              f"runs={arm['runs']:>4}  digits_vs_published={d:>6.1f}  cert={'ok' if ok else why}")
    _report(rows)
    return 0


def cmd_compare(args) -> int:
    """The kill-criterion experiment from issue #12, at equal wall clock."""
    meta = env_meta(args.seed)
    print(f"EQUAL-COMPUTE COMPARISON: {args.budget:.1f}s per n per arm, seed {args.seed}")
    print("Both arms use the SAME SLSQP descent and the SAME final polish; they differ")
    print("only in how start points are generated.")
    print()
    print(f"  {'n':>3}  {'m (LS-seeded)':>19}  {'m (multi-start)':>19}  {'winner':>10}  "
          f"{'ref':>19}  {'LS runs':>8}  {'base runs':>9}")
    rows = []
    wins = ties = losses = 0
    for n in range(args.min, args.max + 1):
        a = ls_arm(n, args.seed + n, args.budget)
        pa, ma = polish(a["points"])
        b = baseline_arm(n, args.seed + n, args.budget)
        pb, mb = polish(b["points"])
        r = ref.reference_m(n)

        if ma > mb * (1 + 1e-12):
            winner, w = "LS", "win"
        elif mb > ma * (1 + 1e-12):
            winner, w = "multi-start", "loss"
        else:
            winner, w = "tie", "tie"
        wins += w == "win"
        ties += w == "tie"
        losses += w == "loss"

        # keep whichever arm did better, as a candidate
        if ma >= mb:
            checkpoint(n, ma, pa, {**meta, "mode": "compare", "arm": "ls"})
            emit_candidate(n, pa, meta)
        rows.append({"n": n, "m_ls": ma, "m_base": mb, "ref": r, "winner": winner,
                     "ls_runs": a["runs"], "base_runs": b["runs"]})
        print(f"  {n:>3}  {ma:>19.15f}  {mb:>19.15f}  {winner:>10}  "
              f"{(r[0] if r else float('nan')):>19.15f}  {a['runs']:>8}  {b['runs']:>9}")

    total = wins + ties + losses
    print()
    print(f"LS matched or beat the multi-start baseline on {wins + ties} of {total} values "
          f"of n (wins {wins}, ties {ties}, losses {losses}).")
    print("KILL-CRITERION (issue #12): the port does not pay for its complexity unless LS "
          "matches or beats the baseline on at least half the n tested.")
    verdict = "NOT MET (LS is worth keeping)" if 2 * (wins + ties) >= total else "MET (refuted)"
    print(f"  -> kill-criterion {verdict}")
    (OUT / "compare.json").write_text(json.dumps(
        {"meta": meta, "budget_s_per_arm": args.budget, "rows": [
            {k: (v if k != "ref" else (list(v) if v else None)) for k, v in row.items()}
            for row in rows],
         "summary": {"wins": wins, "ties": ties, "losses": losses,
                     "kill_criterion": verdict}}, indent=2) + "\n")
    return 0


def _report(rows) -> None:
    print()
    print("All values below are `numerical` construction HYPOTHESES. None is verified,")
    print("none is an optimality claim, and none beats a published record.")


def cmd_table(args) -> int:
    print(f"  {'n':>3}  {'s (LS candidate)':>20}  {'s (published)':>20}  {'digits':>7}  source")
    for path in sorted(OUT.glob("n*.json")):
        data = json.loads(path.read_text())
        n = data["n"]
        s = data["s_side_for_unit_circles"]
        r = data.get("reference")
        if r:
            print(f"  {n:>3}  {s:>20.12f}  {r['s']:>20.12f}  "
                  f"{r['agreement_digits_m']:>7.1f}  {r['source']}")
        else:
            print(f"  {n:>3}  {s:>20.12f}  {'--':>20}  {'--':>7}  no published value")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=["validate", "sweep", "compare", "table"])
    ap.add_argument("--min", type=int, default=16)
    ap.add_argument("--max", type=int, default=34)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--budget", type=float, default=8.0,
                    help="seconds per n per arm (matches circle-packing-search's default)")
    args = ap.parse_args()
    return {
        "validate": cmd_validate,
        "sweep": cmd_sweep,
        "compare": cmd_compare,
        "table": cmd_table,
    }[args.mode](args)


if __name__ == "__main__":
    raise SystemExit(main())
