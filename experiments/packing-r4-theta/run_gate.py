"""Round-4 worker r4-theta: the container-theta' ceiling gate (battery 1, corner grid).

For each n we evaluate  theta'(G_d[W])  on a finite triangular grid W inside T_d, at
values of d BELOW the truth d(n).  By the ceiling lemma in theta_gate.py,

        theta'(G_d[W]) >= n   ==>   theta'(G_d) >= n   ==>   the theta' method cannot
                                    certify d(n) > d,  i.e.  d_theta'(n) <= d.

So a value >= n FIRES the gate (theta' is provably too weak at that d); a value < n
proves nothing (the grid only lower-bounds theta'(G_d)).

Everything written here is `numerical`.  Reproduce with:  python3 run_gate.py --all
"""
from __future__ import annotations
import argparse, json, os, time
import sympy as sp

from theta_gate import conflict_adj, theta_prime_lb, alpha_exact, oler_floor

OUT = "results.json"

# exact known d(n) (point formulation), from problems/.../README.md (`cited` there)
KNOWN_D = {
    3:  sp.Integer(2),                       # Delta(2)
    6:  sp.Integer(4),                       # Delta(3)
    8:  2 + 2 * sp.sqrt(33) / 3,
    10: sp.Integer(6),                       # Delta(4)
    12: 4 + 2 * sp.sqrt(3),
    15: sp.Integer(8),                       # Delta(5)
    21: sp.Integer(10),                      # Delta(6)
}


def grid_k(d: float, refine: int) -> int:
    """k points per side so that the spacing d/(k-1) is about 2/refine."""
    return max(3, int(round(d * refine / 2.0)) + 1)


def run_case(n, d_expr, label, refine, per_solve=110.0, eps=1e-5):
    d = float(d_expr)
    k = grid_k(d, refine)
    t0 = time.time()
    adj, pts, ties = conflict_adj(k, d_expr)
    N = len(pts)
    a = alpha_exact(adj)
    t1 = time.time()
    lb, status, M, vsolver = theta_prime_lb(adj, eps=eps, time_limit=per_solve)
    return dict(n=n, label=label, d=d, refine=refine, k=k, N=N,
                spacing=d / (k - 1), alpha_grid=a, theta_lb=lb,
                theta_solver=vsolver, status=status, nonedges=M,
                build_s=round(t1 - t0, 1), solve_s=round(time.time() - t1, 1),
                fires=bool(lb >= n))


def append(rec, path=OUT):
    data = json.load(open(path)) if os.path.exists(path) else []
    data.append(rec)
    json.dump(data, open(path, "w"), indent=1)
    print(json.dumps(rec), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--budget", type=float, default=1800.0)
    args = ap.parse_args()
    t_start = time.time()
    deadline = t_start + args.budget

    eps_probe = sp.Rational(1, 100)   # probe just below the truth

    cases = []
    # (A) resolution ladder at the single most informative point: n = 8 at Oler's floor
    dO8 = sp.sqrt(65) - 3
    for r in (4, 6, 8, 10):
        cases.append((8, dO8, "oler-floor", r))
    # (B) n = 8 and n = 12: Oler's floor, and just below the true d(n)
    dO12 = sp.sqrt(97) - 3
    cases += [(12, dO12, "oler-floor", 6),
              (8, KNOWN_D[8] - eps_probe, "just-below-d(n)", 6),
              (12, KNOWN_D[12] - eps_probe, "just-below-d(n)", 6)]
    # (C) triangular n: Oler is exactly tight there (Oler floor == d(n)), so the only
    #     meaningful probe is just below d(n).
    for n in (3, 6, 10, 15, 21):
        cases.append((n, KNOWN_D[n] - eps_probe, "just-below-d(n)", 6 if n <= 10 else 4))
    # (D) the open case n = 16, at Oler's floor
    cases.append((16, sp.sqrt(129) - 3, "oler-floor", 4))
    cases.append((16, sp.sqrt(129) - 3, "oler-floor", 6))

    for (n, d_expr, label, r) in cases:
        if time.time() > deadline:
            print("BUDGET EXHAUSTED, stopping", flush=True)
            break
        try:
            rec = run_case(n, d_expr, label, r)
            rec["d_exact"] = str(d_expr)
            rec["oler_floor"] = oler_floor(n)
            rec["d_known"] = float(KNOWN_D[n]) if n in KNOWN_D else None
            append(rec)
        except Exception as e:
            append(dict(n=n, label=label, refine=r, error=f"{type(e).__name__}: {e}"))
    print(f"TOTAL {time.time() - t_start:.0f}s", flush=True)


if __name__ == "__main__":
    main()
