"""Task (e): try to BREAK the claim a_16 >= 1 + 2 sqrt3.

The claim is false iff there is some a < A = 1+2sqrt3 with 16 points in T_a at
pairwise distance >= 1.  Equivalently, writing m = max over 16-point
configurations in the UNIT-side triangle of the minimum pairwise distance,
a_16 = 1/m, so the claim fails iff  m > 1/A = 0.2240092...

This is a NUMERICAL search.  Per problem RULES.md s5 it can only ever produce a
counterexample (which would then need an exact certificate); it can never
confirm the bound.  Its role here is the RULES.md s5 point 4 obligation to try
to break a claim before accepting it.

Reproduce: python3 break_attempt.py [n_restarts] [seed]
"""
import sys, math, time
import numpy as np
from scipy.optimize import linprog

N = 16
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20260822
RESTARTS = int(sys.argv[1]) if len(sys.argv) > 1 else 400

V = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, math.sqrt(3) / 2]])
# inward normals of the unit triangle, n.x >= c
NRM = np.array([[0.0, 1.0], [-math.sqrt(3) / 2, -0.5], [math.sqrt(3) / 2, -0.5]])
OFF = np.array([0.0, -math.sqrt(3) / 2, 0.0])


def inside_dist(P):
    return (P @ NRM.T) - OFF          # >= 0 iff inside


def minsep(P):
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    np.fill_diagonal(D, np.inf)
    return D.min()


def project(P):
    """Push points back into the triangle."""
    for _ in range(50):
        d = inside_dist(P)
        bad = d < 0
        if not bad.any():
            break
        for k in range(3):
            idx = bad[:, k]
            P[idx] -= np.outer(d[idx, k], NRM[k])
    return P


def slp_polish(P, iters=200):
    """Sequential LP on the minimax problem: maximise t subject to linearised
    |pi-pj| >= t and containment, with a trust region."""
    P = P.copy()
    tr = 0.05
    best = minsep(P)
    bestP = P.copy()
    for it in range(iters):
        pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
        nv = 2 * N + 1
        A_ub, b_ub = [], []
        for (i, j) in pairs:
            d = P[i] - P[j]
            nd = np.linalg.norm(d)
            if nd < 1e-12:
                continue
            u = d / nd
            row = np.zeros(nv)
            row[2 * i:2 * i + 2] = -u
            row[2 * j:2 * j + 2] = u
            row[-1] = 1.0
            A_ub.append(row); b_ub.append(nd)
        for i in range(N):
            for k in range(3):
                row = np.zeros(nv)
                row[2 * i:2 * i + 2] = -NRM[k]
                A_ub.append(row); b_ub.append(inside_dist(P[i:i + 1])[0, k])
        c = np.zeros(nv); c[-1] = -1.0
        bounds = [(-tr, tr)] * (2 * N) + [(0, 2.0)]
        r = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=bounds,
                    method="highs")
        if not r.success:
            break
        step = r.x[:2 * N].reshape(N, 2)
        Q = project(P + step)
        m = minsep(Q)
        if m > best + 1e-12:
            best, bestP, P = m, Q.copy(), Q
            tr = min(tr * 1.3, 0.2)
        else:
            tr *= 0.5
            P = Q if m > minsep(P) else P
            if tr < 1e-9:
                break
    return best, bestP


rng = np.random.default_rng(SEED)
A_EXACT = 1 + 2 * math.sqrt(3)
THRESH = 1.0 / A_EXACT
best_m, best_P = 0.0, None
t0 = time.time()
for r in range(RESTARTS):
    w = rng.dirichlet(np.ones(3), size=N)
    P = w @ V
    m, P = slp_polish(P, iters=120)
    if m > best_m:
        best_m, best_P = m, P
    if best_m > THRESH:
        break
    if time.time() - t0 > 600:
        print(f"time budget reached after {r+1} restarts")
        break

print(f"restarts run          : {r+1}   seed {SEED}")
print(f"best min separation m : {best_m:.10f}")
print(f"implied a_16 <=  1/m  : {1/best_m:.10f}")
print(f"threshold to BREAK    : m > 1/(1+2sqrt3) = {THRESH:.10f}"
      f"   (i.e. a < {A_EXACT:.10f})")
print(f"best known a_16 (Melissen-Schuur, s=12.713629) = "
      f"{(12.713629 - 2*math.sqrt(3))/2:.10f}")
print()
if best_m > THRESH:
    print("*** CLAIM BROKEN NUMERICALLY -- needs an exact certificate ***")
    np.save("break_witness.npy", best_P)
else:
    print("NO counterexample found: every local optimum sits ABOVE "
          f"a = {A_EXACT:.7f}, consistent with the claim.")
    print("This is a failed break attempt, not evidence for the bound.")
# (the best configuration is float output and certifies nothing; see break.log)
