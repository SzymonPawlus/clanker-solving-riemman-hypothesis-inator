"""
Numerical probe of the CEILING of candidate C2.

C2's conclusion:  a(n) >= rho(n) := min over n-point unit-separated E of max( sqrt(r(E)), M(E)/3 ),
with r(E) = 4*area(conv E)/sqrt(3), M(E) = perim(conv E).

rho(n) >= a_Oler(n) always (proved in the README).  This script computes an UPPER bound on rho(n)
by direct multistart minimisation, i.e. it measures how much C2 can possibly gain over Oler.
A low value found here KILLS C2; a value stuck at the lattice value CONFIRMS the gain.

Everything here is `numerical`.  Separation-1 normalisation, container-free (C2 has no container).
"""
import sys, json, math, time
import numpy as np
from scipy.optimize import minimize, NonlinearConstraint
from scipy.spatial import ConvexHull

SQ3 = math.sqrt(3.0)
rng = np.random.default_rng(20260826)

def hull_rM(P):
    try:
        h = ConvexHull(P)
    except Exception:
        return None
    area = h.volume            # 2-D: .volume is area, .area is perimeter
    per = h.area
    return 4.0*area/SQ3, per

def objective(z, n):
    P = z.reshape(n, 2)
    got = hull_rM(P)
    if got is None:
        return 1e3
    r, M = got
    return max(math.sqrt(max(r, 0.0)), M/3.0)

def pair_con(z, n, idx):
    P = z.reshape(n, 2)
    d = P[idx[0]] - P[idx[1]]
    return np.einsum('ij,ij->i', d, d)          # squared distances, need >= 1

def lattice_points(kmax):
    pts = []
    for q in range(kmax+1):
        for p in range(kmax+1-q):
            pts.append((p + q*0.5, q*SQ3/2))
    return np.array(pts)

def starts(n, ntries):
    out = []
    # lattice-derived starts: take n points from a big triangular lattice, various subsets
    L = lattice_points(8)
    for _ in range(ntries//2):
        c = L[rng.choice(len(L), size=1)][0]
        order = np.argsort(((L - c)**2).sum(1))
        P = L[order[:n]].astype(float) + rng.normal(0, 0.05, (n, 2))
        out.append(P)
    # random starts inside a triangle of a generous side
    for _ in range(ntries - len(out)):
        a = 5.5
        P = []
        while len(P) < n:
            x, y = rng.uniform(0, a), rng.uniform(0, a*SQ3/2)
            if y <= SQ3*x + 1e-9 and y <= SQ3*(a-x) + 1e-9:
                P.append((x, y))
        out.append(np.array(P))
    return out

def solve_one(P0, n, idx):
    nc = NonlinearConstraint(lambda z: pair_con(z, n, idx), 1.0, np.inf)
    res = minimize(objective, P0.ravel(), args=(n,), method='SLSQP',
                   constraints=[{'type': 'ineq',
                                 'fun': lambda z: pair_con(z, n, idx) - 1.0}],
                   options={'maxiter': 400, 'ftol': 1e-10})
    return res

def feasible_value(z, n, idx, tol=1e-9):
    """Recompute the objective after rescaling to make separation exactly >= 1 (repairs slop)."""
    P = z.reshape(n, 2).copy()
    d2 = pair_con(z, n, idx)
    m = math.sqrt(max(d2.min(), 1e-12))
    if m < 1.0:
        P = P / m                      # scale up so min separation is exactly 1
    got = hull_rM(P)
    if got is None:
        return None, None
    r, M = got
    return max(math.sqrt(r), M/3.0), (r, M)

def run(n, ntries):
    idx = np.array(np.triu_indices(n, 1))
    best = (1e9, None, None)
    t0 = time.time()
    for i, P0 in enumerate(starts(n, ntries)):
        try:
            res = solve_one(P0, n, idx)
        except Exception:
            continue
        v, rM = feasible_value(res.x, n, idx)
        if v is not None and v < best[0]:
            best = (v, rM, res.x.reshape(n, 2).tolist())
    return best, time.time()-t0

if __name__ == "__main__":
    n = int(sys.argv[1]); ntries = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    (v, rM, P), el = run(n, ntries)
    ao = (math.sqrt(8*n+1)-3)/2
    out = {"n": n, "tries": ntries, "a_oler": ao, "rho_upper": v,
           "r_M": rM, "gain_in_a": v-ao, "gain_in_d": 2*(v-ao),
           "seconds": el, "config": P}
    with open(f"out/rho_n{n}.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"n={n}  a_Oler={ao:.6f}  rho_upper={v:.6f}  (r,M)={rM}  "
          f"gain_a={v-ao:+.6f}  gain_d={2*(v-ao):+.6f}  [{el:.0f}s, {ntries} starts]")
