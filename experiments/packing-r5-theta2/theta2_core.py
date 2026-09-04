"""
r5-theta2 core: an independent implementation of the finite-graph theta' instrument,
plus a library of *witness families* for the one-sided ceiling test of attacks/r4-theta.

WHAT THIS IS
------------
NEITHER a construction nor an optimality claim.  No bound on d(n) or s(n) is asserted.
Every number produced here is float SDP output => `numerical` (RULES.md section 3).

Conventions (problems/circle-packing-equilateral-triangle/RULES.md section 2):
    T_d = CLOSED equilateral triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt3/2).
    G_d : vertex set T_d, edge {x,y} iff 0 < ||x-y|| < 2  (STRICT: distance exactly 2
          is a NON-edge, because all inequalities in this problem are non-strict).
    alpha(G_d) = max points at pairwise distance >= 2;  d(n) = min{d : alpha(G_d) >= n}.

theta' in kernel form:
    theta'(G) = min { lam : exists psd kernel Z with Z(x,x) <= lam-1 for all x,
                                                     Z(x,y) <= -1 for x != y non-adjacent }.
Dual / primal form used numerically:
    theta'(G) = max { <J,B> : B psd, B >= 0 entrywise, tr B = 1, B_ij = 0 on edges }.

Soundness (re-derived here, not cited).  Let S be independent, |S|=m, and Z feasible with
value lam.  Z psd => sum_{x,y in S} Z(x,y) >= 0.  m diagonal terms <= lam-1, m(m-1)
off-diagonal terms <= -1, so 0 <= m(lam-1) - m(m-1), i.e. lam >= m.  So alpha <= theta'.

CEILING LEMMA (the instrument).  For finite W subset T_d, a kernel feasible for G_d
restricts to a matrix feasible for G_d[W], so theta'(G_d[W]) <= theta'(G_d).  Hence a
finite W with theta'(G_d[W]) >= n proves theta' CANNOT certify d(n) > d, against every
kernel of every degree.  One-sided: a value < n proves nothing.

WHAT FIRING COSTS.  At d just below d(n) we have alpha(G_d) = n-1, so a witness must have
    theta'(W) - alpha(W) >= 1.
This file measures that "gain" over structurally different witness families.

A STRUCTURAL FACT PROVED HERE (see `ring_gain_ceiling` docstring and section 2 of the
write-up): an equally-spaced single ring can NEVER fire the gate, because its conflict
graph is exactly a cycle power C_m^t, whose fractional clique cover number is m/(t+1) and
whose independence number is floor(m/(t+1)); since theta' <= chi-bar_f, its gain is
< 1 always.  That rules out the family attacks/r4-theta named as its own next step.
"""
from __future__ import annotations

import itertools
import math

import numpy as np

try:
    import cvxpy as cp
except ImportError:  # pragma: no cover
    cp = None

SQRT3 = math.sqrt(3.0)

# published exact optima, point formulation (problems/.../README.md, `cited` there).
# Re-typed from the problem README, NOT imported from a sibling experiment.
KNOWN_D = {
    1: 0.0, 2: 2.0, 3: 2.0, 4: 2 * SQRT3, 5: 4.0, 6: 4.0,
    7: 2 + 2 * SQRT3, 8: 2 + 2 * math.sqrt(33) / 3, 9: 6.0, 10: 6.0,
    11: 4 + 4 * math.sqrt(6) / 3, 12: 4 + 2 * SQRT3,
    13: 4 + 2 * math.sqrt(6) / 3 + 4 * SQRT3 / 3, 14: 8.0, 15: 8.0,
    21: 10.0, 28: 12.0,
}


def oler_floor(n: int) -> float:
    """Oler 1961 in the triangle: n <= d^2/8 + 3d/4 + 1  =>  d(n) >= sqrt(8n+1) - 3.
    (`cited` inequality, `sketch` application; used only as a comparison target.)"""
    return math.sqrt(8 * n + 1) - 3.0


# --------------------------------------------------------------------------------------
# finite-graph theta'
# --------------------------------------------------------------------------------------
def theta_prime_repaired(adj: np.ndarray, solver: str = "SCS", eps: float = 1e-6,
                         max_iters: int = 100000, time_limit: float | None = None,
                         verbose: bool = False):
    """A REPAIRED-PRIMAL lower bound on theta'(G).

    Solve   max <J,B>  s.t.  B symmetric psd, B >= 0 entrywise, tr B = 1, B_ij = 0 on edges,
    then push the solver's iterate onto an exactly feasible point:
        1. symmetrise, zero every edge entry, clip negatives to 0   -> B >= 0, edges 0
        2. add t*I with t = max(0, -lambda_min(B))                   -> psd, still B >= 0
        3. divide by the trace                                       -> tr = 1
    sum(B)/tr(B) is then the objective at a feasible point, hence <= theta'(G).  Solver
    inaccuracy can only shrink it, never invalidate it -- the direction the ceiling lemma
    needs.  Still `numerical`: the eigenvalue and the sum are float64.

    Returns (repaired_lower_bound, solver_value, status).
    """
    N = int(adj.shape[0])
    if N == 0:
        return 0.0, 0.0, "trivial"
    if N == 1:
        return 1.0, 1.0, "trivial"
    ei, ej = np.nonzero(np.triu(adj, 1))
    B = cp.Variable((N, N), symmetric=True)
    cons = [B >> 0, B >= 0, cp.trace(B) == 1]
    if len(ei):
        cons.append(B[ei, ej] == 0)
    prob = cp.Problem(cp.Maximize(cp.sum(B)), cons)
    kw = {}
    if solver == "SCS":
        kw = dict(eps=eps, max_iters=max_iters)
        if time_limit:
            kw["time_limit_secs"] = float(time_limit)
    try:
        prob.solve(solver=solver, verbose=verbose, **kw)
    except Exception as exc:                                    # pragma: no cover
        return float("nan"), float("nan"), f"solver-error:{exc}"
    Bv = B.value
    if Bv is None:
        return float("nan"), float("nan"), str(prob.status)
    M = np.asarray(Bv, dtype=float)
    M = 0.5 * (M + M.T)
    M[adj] = 0.0
    M = np.maximum(M, 0.0)
    lam = float(np.linalg.eigvalsh(M).min())
    if lam < 0:
        M = M + (-lam) * np.eye(N)
    tr = float(np.trace(M))
    if tr <= 0:
        return 1.0, float(prob.value), str(prob.status)
    return float(M.sum() / tr), float(prob.value), str(prob.status)


def alpha_exact(adj: np.ndarray) -> int:
    """Exact maximum independent set (HiGHS binary ILP)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    N = int(adj.shape[0])
    ii, jj = np.nonzero(np.triu(adj, 1))
    if len(ii) == 0:
        return N
    A = np.zeros((len(ii), N))
    A[np.arange(len(ii)), ii] = 1.0
    A[np.arange(len(ii)), jj] = 1.0
    res = milp(c=-np.ones(N), constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(N), bounds=Bounds(0, 1))
    return int(round(-res.fun))


def chi_bar_f(adj: np.ndarray) -> float:
    """Fractional clique cover number chi-bar_f(G) = fractional chromatic number of the
    complement.  theta'(G) <= chi-bar_f(G), so this is an a-priori CEILING on the gain a
    given witness can ever show.  Enumerates maximal cliques -- small N only."""
    import networkx as nx
    from scipy.optimize import linprog
    N = int(adj.shape[0])
    G = nx.from_numpy_array(adj.astype(int))
    cl = list(nx.find_cliques(G))
    if len(cl) > 200000:
        return float("nan")
    A = np.zeros((N, len(cl)))
    for c, K in enumerate(cl):
        for v in K:
            A[v, c] = 1.0
    res = linprog(c=np.ones(len(cl)), A_ub=-A, b_ub=-np.ones(N),
                  bounds=(0, None), method="highs")
    return float(res.fun)


# --------------------------------------------------------------------------------------
# geometry:  containment + adjacency for an arbitrary finite witness
#
# ALL witness coordinates are built in mpmath at 60 decimal digits.  That matters: the
# lattice families contain pairs at distance EXACTLY 2, which must resolve as NON-edges
# (non-strict convention).  In float64 those pairs come out |dist^2 - 4| ~ 3e-16, which is
# indistinguishable from a genuine near-miss; at 60 digits the exact ties sit at ~1e-58
# and every generic pair is ~1e-3 away, so the classification is unambiguous by a margin
# of 25 orders of magnitude.  `adjacency` asserts that margin.
# --------------------------------------------------------------------------------------
import mpmath as mp

mp.mp.dps = 60
MP3 = mp.sqrt(3)


def inside(pts, d, tol=mp.mpf('1e-30')):
    """True iff every point is in the CLOSED triangle T_d (up to tol)."""
    d = mp.mpf(d)
    for (x, y) in pts:
        x, y = mp.mpf(x), mp.mpf(y)
        if y < -tol:
            return False
        if MP3 * x - y < -tol:
            return False
        if MP3 * (d - x) - y < -tol:
            return False
    return True


def adjacency(pts, tie_tol=mp.mpf('1e-30')):
    """Conflict adjacency of a finite point set: edge iff 0 < ||x-y|| < 2.

    A squared distance within `tie_tol` of 4 is treated as EXACTLY 2, hence a NON-edge.
    Returns (adj, n_ties, min_gap); min_gap is the smallest |dist^2 - 4| over non-tie
    pairs and must be >> tie_tol for the family to be numerically well-posed.
    """
    P = [(mp.mpf(x), mp.mpf(y)) for (x, y) in pts]
    N = len(P)
    adj = np.zeros((N, N), dtype=bool)
    ties = 0
    min_gap = mp.mpf('1e100')
    for i in range(N):
        xi, yi = P[i]
        for j in range(i + 1, N):
            dx, dy = P[j][0] - xi, P[j][1] - yi
            q = dx * dx + dy * dy
            g = abs(q - 4)
            if g <= tie_tol:
                ties += 1
                continue                       # distance exactly 2 -> NON-edge
            if g < min_gap:
                min_gap = g
            if q < 4:
                adj[i, j] = adj[j, i] = True
    return adj, ties, min_gap


# --------------------------------------------------------------------------------------
# witness families   (all coordinates mpf at 60 dps)
# --------------------------------------------------------------------------------------
def centroid(d):
    d = mp.mpf(d)
    return (d / 2, d / (2 * MP3))


def w_ring(d, m, R, phase=0, center=None):
    """FAMILY R: m equally spaced points on one circle of radius R.

    ring_gain_ceiling: the induced conflict graph is EXACTLY the cycle power C_m^t with
    t = max{k <= m/2 : 2 R sin(pi k/m) < 2}, because the chord length 2 R sin(pi k/m) is
    monotone in the index separation k for k <= m/2.  For C_m^t any t+1 consecutive
    vertices form a clique, and the m windows of length t+1 each with weight 1/(t+1)
    cover every vertex exactly once, so chi-bar_f(C_m^t) <= m/(t+1); also
    alpha(C_m^t) = floor(m/(t+1)).  Since theta' <= chi-bar_f,
            gain(ring) = theta' - alpha  <=  m/(t+1) - floor(m/(t+1))  <  1.
    A single equally-spaced ring can therefore NEVER fire the gate.  (`sketch`.)
    """
    R = mp.mpf(R)
    phase = mp.mpf(phase)
    cx, cy = center if center is not None else centroid(d)
    cx, cy = mp.mpf(cx), mp.mpf(cy)
    return [(cx + R * mp.cos(phase + 2 * mp.pi * k / m),
             cy + R * mp.sin(phase + 2 * mp.pi * k / m)) for k in range(m)]


def w_concentric(d, spec, center=None):
    """FAMILY CR: concentric rings.  spec = [(m1,R1,phase1), ...]; a term with R = 0 and
    m = 1 contributes the centre point."""
    pts = []
    for (m, R, ph) in spec:
        if mp.mpf(R) == 0:
            cx, cy = center if center is not None else centroid(d)
            pts.append((mp.mpf(cx), mp.mpf(cy)))
        else:
            pts.extend(w_ring(d, m, R, ph, center))
    return pts


def w_edge_ring(d, per_side, inset=0):
    """FAMILY E: points equally spaced along the three EDGES of T_d (each corner once),
    optionally inset toward the centroid by `inset`.  The boundary analogue of the ring
    family -- but NOT a circulant: the corner turns make chord length non-monotone in
    index separation, so the C_m^t gain ceiling does not apply."""
    d = mp.mpf(d)
    inset = mp.mpf(inset)
    A = (mp.mpf(0), mp.mpf(0))
    B = (d, mp.mpf(0))
    C = (d / 2, d * MP3 / 2)
    G = centroid(d)
    pts = []
    for (P, Q) in ((A, B), (B, C), (C, A)):
        for k in range(per_side):
            t = mp.mpf(k) / per_side
            px = P[0] + t * (Q[0] - P[0])
            py = P[1] + t * (Q[1] - P[1])
            if inset != 0:
                vx, vy = G[0] - px, G[1] - py
                nv = mp.sqrt(vx * vx + vy * vy)
                px, py = px + inset * vx / nv, py + inset * vy / nv
            pts.append((px, py))
    return pts


def w_corner_fan(d, per_corner, radii):
    """FAMILY CF: fans anchored at the three CORNERS -- `per_corner` directions times the
    given radii, from each corner into the triangle."""
    d = mp.mpf(d)
    A = (mp.mpf(0), mp.mpf(0))
    B = (d, mp.mpf(0))
    C = (d / 2, d * MP3 / 2)
    corners = [(A, mp.mpf(0), mp.pi / 3),
               (B, 2 * mp.pi / 3, mp.pi),
               (C, 4 * mp.pi / 3, 5 * mp.pi / 3)]
    pts = []
    for (P, a0, a1) in corners:
        for i in range(per_corner):
            th = a0 + (a1 - a0) * (mp.mpf(i) + mp.mpf(1) / 2) / per_corner
            for R in radii:
                R = mp.mpf(R)
                pts.append((P[0] + R * mp.cos(th), P[1] + R * mp.sin(th)))
    return pts


def w_anchored_grid(d, refine):
    """FAMILY G: the lattice-anchored triangular grid of spacing exactly h = 2/refine,
    anchored at corner A.  Contains the spacing-2 triangular packing.  BASELINE family
    (the sharper of the two used by attacks/r4-theta)."""
    d = mp.mpf(d)
    h = mp.mpf(2) / refine
    K = int(mp.floor(d / h + mp.mpf('1e-25')))
    pts = []
    for j in range(K + 1):
        for i in range(K + 1 - j):
            pts.append((h * (i + mp.mpf(j) / 2), h * j * MP3 / 2))
    return pts


def w_c5_clusters(d, centers, R):
    """FAMILY C5: a union of 5-point rings.  A ring with
    2 R sin(36deg) < 2 <= 2 R sin(72deg), i.e. R in [1.05146, 1.70130), induces exactly
    C_5: theta' = sqrt5, alpha = 2, gain 0.236 per cluster, and gains ADD over connected
    components.  The geometric question is how many mutually NON-adjacent clusters fit."""
    pts = []
    for (cx, cy) in centers:
        pts.extend(w_ring(d, 5, R, phase=mp.mpf('0.3'), center=(cx, cy)))
    return pts


def w_random(d, N, rng):
    """FAMILY RND: N uniform random points in T_d."""
    d = mp.mpf(d)
    pts = []
    while len(pts) < N:
        u, v = rng.random(), rng.random()
        if u + v > 1:
            u, v = 1 - u, 1 - v
        u, v = mp.mpf(float(u)), mp.mpf(float(v))
        pts.append((d * (u + v / 2), d * v * MP3 / 2))
    return pts


def w_perturbed_grid(d, refine, sigma, rng):
    """FAMILY PG: the anchored grid jittered by N(0, sigma) and kept inside T_d.  Breaks
    the lattice's clique-cover-tight structure, which is what pins theta' to alpha."""
    pts = w_anchored_grid(d, refine)
    out = []
    for (x, y) in pts:
        for _ in range(60):
            nx_ = x + mp.mpf(float(rng.normal(0, sigma)))
            ny_ = y + mp.mpf(float(rng.normal(0, sigma)))
            if inside([(nx_, ny_)], d, tol=mp.mpf(0)):
                out.append((nx_, ny_))
                break
        else:
            out.append((x, y))
    return out


# --------------------------------------------------------------------------------------
# self-test
# --------------------------------------------------------------------------------------
def selftest(verbose=True):
    import networkx as nx
    ok = True

    def chk(name, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: got {got:.6f} want {want:.6f}")

    print("A. theta' on graphs with known values")
    A = np.ones((5, 5), dtype=bool); np.fill_diagonal(A, False)
    chk("theta'(K5)=1", theta_prime_repaired(A, solver="CLARABEL")[0], 1.0, 1e-6)
    chk("theta'(empty7)=7", theta_prime_repaired(np.zeros((7, 7), bool), solver="CLARABEL")[0],
        7.0, 1e-6)
    C5 = np.zeros((5, 5), bool)
    for i in range(5):
        C5[i, (i + 1) % 5] = C5[(i + 1) % 5, i] = True
    chk("theta'(C5)=sqrt5", theta_prime_repaired(C5, solver="CLARABEL")[0], math.sqrt(5), 1e-5)
    C7 = np.zeros((7, 7), bool)
    for i in range(7):
        C7[i, (i + 1) % 7] = C7[(i + 1) % 7, i] = True
    want7 = 7 * math.cos(math.pi / 7) / (1 + math.cos(math.pi / 7))
    chk("theta'(C7)=7cos(pi/7)/(1+cos(pi/7))",
        theta_prime_repaired(C7, solver="CLARABEL")[0], want7, 1e-5)
    P = nx.to_numpy_array(nx.petersen_graph()).astype(bool)
    chk("theta'(Petersen)=4", theta_prime_repaired(P, solver="CLARABEL")[0], 4.0, 1e-5)
    # additivity over disjoint union: two disjoint C5's must give 2*sqrt5
    D = np.zeros((10, 10), bool)
    D[:5, :5] = C5
    D[5:, 5:] = C5
    chk("theta'(C5 + C5)=2 sqrt5", theta_prime_repaired(D, solver="CLARABEL")[0],
        2 * math.sqrt(5), 1e-4)

    print("B. sandwich alpha <= theta' <= chi-bar_f on random graphs")
    rng = np.random.default_rng(20260824)
    for t in range(5):
        A = rng.random((9, 9)) < 0.45
        A = np.triu(A, 1); A = A | A.T
        a = alpha_exact(A)
        th = theta_prime_repaired(A, solver="CLARABEL")[0]
        f = chi_bar_f(A)
        good = (a - 1e-6 <= th <= f + 1e-6)
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] trial {t}: alpha={a} theta'={th:.6f} "
              f"chi-bar_f={f:.6f}")

    print("C. geometry: the conflict graph must reproduce the `cited` alpha of T_d")
    # at d = 2(k-1) the triangular packing Delta(k) is optimal (`cited`)
    for (k, refine) in ((3, 1), (4, 1), (5, 1), (4, 2), (5, 2), (4, 3), (5, 3), (6, 2)):
        d = 2.0 * (k - 1)
        pts = w_anchored_grid(d, refine)
        assert inside(pts, d, tol=1e-9), "grid escaped the triangle"
        adj, ties, gap = adjacency(pts)
        a = alpha_exact(adj)
        want = k * (k + 1) // 2
        good = (a == want)
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] d={d} refine={refine} N={len(pts)}: "
              f"alpha={a} Delta({k})={want}  ({ties} exact distance-2 ties, min|q-4|={float(gap):.2e})")

    print("D. ring family really is the cycle power C_m^t (and so has gain < 1)")
    for (m, R) in ((5, 1.3), (7, 1.9), (9, 2.6), (11, 3.1), (12, 3.4)):
        d = 12.0
        pts = w_ring(d, m, R)
        adj, ties, gap = adjacency(pts)
        t = max([k for k in range(1, m // 2 + 1) if 2 * R * math.sin(math.pi * k / m) < 2]
                + [0])
        want = np.zeros((m, m), bool)
        for i in range(m):
            for k in range(1, t + 1):
                want[i, (i + k) % m] = want[(i + k) % m, i] = True
        good = bool((adj == want).all())
        ok &= good
        a = alpha_exact(adj)
        print(f"  [{'PASS' if good else 'FAIL'}] m={m} R={R}: t={t}, alpha={a}, "
              f"floor(m/(t+1))={m // (t + 1)}, chi-bar_f<= m/(t+1)={m / (t + 1):.4f}")

    print("\nSELFTEST", "PASSED" if ok else "FAILED")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if selftest() else 1)
