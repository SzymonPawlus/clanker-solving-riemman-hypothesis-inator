"""Battery 2: the same ceiling gate on the LATTICE-ANCHORED grid.

The corner-to-corner grid of battery 1 has spacing d/(k-1), incommensurate with the packing
distance 2, so it cannot hold a pair at distance exactly 2 and its alpha undershoots
alpha(T_d).  The anchored grid has spacing exactly 2/refine and contains the triangular
packing.  Since a better witness W can only raise theta'(G_d[W]) -- and by the ceiling
lemma any finite W is admissible -- this is a strictly sharper version of the same test.

Appends to results.json with label "<label>-anchored".  `numerical`, like everything else.
Reproduce:  python3 run_anchored.py
"""
import time
import sympy as sp

from theta_gate import conflict_adj_anchored, theta_prime_lb, alpha_exact, oler_floor
from run_gate import KNOWN_D, append

EPS = sp.Rational(1, 100)
CASES = [
    # (n, d, label, refine)
    (8,  sp.sqrt(65) - 3,   "oler-floor", 6),
    (12, sp.sqrt(97) - 3,   "oler-floor", 6),
    (16, sp.sqrt(129) - 3,  "oler-floor", 4),
    (16, sp.sqrt(129) - 3,  "oler-floor", 6),
    (8,  KNOWN_D[8] - EPS,  "just-below-d(n)", 6),
    (12, KNOWN_D[12] - EPS, "just-below-d(n)", 6),
]

if __name__ == "__main__":
    for (n, d_expr, label, refine) in CASES:
        d = float(d_expr)
        t0 = time.time()
        adj, pts, h = conflict_adj_anchored(d_expr, refine)
        a = alpha_exact(adj)
        t1 = time.time()
        lb, status, M, vs = theta_prime_lb(adj, eps=1e-5, time_limit=90.0)
        append(dict(n=n, label=label + "-anchored", d=d, refine=refine,
                    k=int(sp.floor(sp.nsimplify(d_expr) / sp.Rational(2, refine))) + 1,
                    N=len(pts), spacing=h, alpha_grid=a, theta_lb=lb, theta_solver=vs,
                    status=status, nonedges=M, build_s=round(t1 - t0, 1),
                    solve_s=round(time.time() - t1, 1), fires=bool(lb >= n),
                    d_exact=str(d_expr), oler_floor=oler_floor(n),
                    d_known=float(KNOWN_D[n]) if n in KNOWN_D else None))
