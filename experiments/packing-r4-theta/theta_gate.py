"""
Container-theta' gate for circle packing in an equilateral triangle (round-4, worker r4-theta).

WHAT THIS IS
------------
NEITHER a construction nor an optimality claim.  It is a measurement of a *ceiling*
on how strong the Lovasz theta' relaxation of the geometric conflict graph can ever be.

Setting (repo conventions, problems/circle-packing-equilateral-triangle/RULES.md):
    T_d = closed equilateral triangle A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2).
    G_d = graph with vertex set T_d, edge {x,y} iff 0 < ||x-y|| < 2.
    An independent set of G_d = a set of points at pairwise distance >= 2 = a packing.
    So alpha(G_d) = max number of points, and d(n) = min{ d : alpha(G_d) >= n }.

theta' (the "prime" variant, alpha <= theta' <= theta) in its *covering / kernel* form:

    theta'(G) = min { lam : exists a symmetric psd kernel Z on V x V with
                             Z(x,x) <= lam - 1        for all x in V,
                             Z(x,y) <= -1             for all x != y NON-adjacent }.

Soundness of that as an upper bound on alpha, re-derived from scratch (no citation used):
    let S be independent, |S| = m.  Z psd  =>  sum_{x,y in S} Z(x,y) >= 0.
    The m diagonal terms are <= lam - 1 each, the m(m-1) off-diagonal terms <= -1 each,
    so 0 <= m(lam-1) - m(m-1), i.e. lam >= m.  Hence alpha(G) <= theta'(G).

Therefore:  if theta'(G_d) < n  then  alpha(G_d) < n  then  d(n) > d.
The best floor this method can ever give is

    d_theta'(n) := sup { d : theta'(G_d) < n }   <=  d(n).

THE CEILING LEMMA (this is what makes the gate cheap)
-----------------------------------------------------
For any FINITE W subset of T_d, restricting a feasible kernel Z to W x W gives a feasible
solution of the finite-graph theta' program for the induced subgraph G_d[W].  Hence

    theta'(G_d[W])  <=  theta'(G_d)                                     (*)

for every finite W.  So if we exhibit a finite W with theta'(G_d[W]) >= n, then
theta'(G_d) >= n and the theta' method CANNOT certify d(n) > d.  That is,

    d_theta'(n)  <=  d      whenever   theta'(G_d[W]) >= n  for some finite W.

Finite subgraphs therefore give UPPER bounds on the theta' floor, with no SOS/kernel
machinery at all, and the bound holds against *every* kernel, of every degree.

The test is one-sided.  A grid value BELOW n proves nothing (the grid only lower-bounds
theta'(G_d)); it merely fails to fire the gate at that resolution.

Every number produced here is float SDP output and is therefore `numerical` -- a
hypothesis, not a bound (RULES.md section 3).

Usage:  python3 theta_gate.py --selftest
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np

try:
    import cvxpy as cp
except ImportError:  # pragma: no cover
    cp = None


# ----------------------------------------------------------------------------------
# finite-graph theta'
# ----------------------------------------------------------------------------------
def theta_prime(adj: np.ndarray, solver: str = "SCS", eps: float = 1e-6,
                max_iters: int = 200000, verbose: bool = False):
    """theta'(G) for a finite simple graph given by a boolean adjacency matrix.

    Primal:  max <J,B>  s.t.  B psd,  B >= 0 entrywise,  tr B = 1,  B_ij = 0 on edges.
    (theta' is the variant with the entrywise nonnegativity; alpha <= theta' <= theta.)
    Dense parametrisation -- used for the small self-test graphs only.
    """
    N = adj.shape[0]
    if N == 0:
        return 0.0, "trivial"
    B = cp.Variable((N, N), PSD=True)
    cons = [cp.trace(B) == 1, B >= 0]
    if adj.any():
        cons.append(cp.multiply(adj.astype(float), B) == 0)
    prob = cp.Problem(cp.Maximize(cp.sum(B)), cons)
    kw = dict(eps=eps, max_iters=max_iters) if solver == "SCS" else {}
    prob.solve(solver=solver, verbose=verbose, **kw)
    return float(prob.value), prob.status


_last_problem = {}


def theta_prime_sparse(adj: np.ndarray, solver: str = "SCS", eps: float = 1e-6,
                       max_iters: int = 100000, verbose: bool = False,
                       time_limit: float | None = None):
    """Same program as theta_prime, but B is parametrised only on the diagonal and on
    the NON-edges (every other entry is structurally zero), so the entrywise-nonnegativity
    cone has size N + |non-edges| instead of N^2.  Identical optimal value."""
    import scipy.sparse as spar
    N = adj.shape[0]
    iu, ju = np.triu_indices(N, 1)
    keep = ~adj[iu, ju]
    pi, pj = iu[keep], ju[keep]
    M = len(pi)
    # variable order: N diagonal entries, then M off-diagonal (each placed twice)
    rows = np.concatenate([np.arange(N) * N + np.arange(N), pi * N + pj, pj * N + pi])
    cols = np.concatenate([np.arange(N), N + np.arange(M), N + np.arange(M)])
    Cmat = spar.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N * N, N + M))
    z = cp.Variable(N + M, nonneg=True)
    B = cp.reshape(Cmat @ z, (N, N), order="C")
    prob = cp.Problem(cp.Maximize(cp.sum(z[:N]) + 2 * cp.sum(z[N:])),
                      [cp.sum(z[:N]) == 1, B >> 0])
    kw = {}
    if solver == "SCS":
        kw = dict(eps=eps, max_iters=max_iters)
        if time_limit:
            kw["time_limit_secs"] = time_limit
    prob.solve(solver=solver, verbose=verbose, **kw)
    _last_problem["prob"] = prob
    _last_problem["B"] = B
    return float(prob.value), prob.status, M


def theta_prime_lb(adj: np.ndarray, solver: str = "SCS", eps: float = 1e-5,
                   max_iters: int = 60000, time_limit: float | None = None):
    """Lower bound on theta'(G) obtained by REPAIRING the solver's primal iterate into an
    exactly feasible point of

        max <J,B>  s.t.  B psd, B >= 0, tr B = 1, B_ij = 0 on edges.

    Repair (each step preserves the constraints already imposed):
      1. symmetrise; zero every edge entry; clip negative entries to 0  -> B >= 0, edges 0
      2. add t*I with t = max(0, -lambda_min)                           -> psd, still B >= 0
      3. divide by the trace                                            -> tr = 1
    The returned value sum(B)/tr(B) is then the objective at a feasible point, hence
    <= theta'(G).  Solver inaccuracy can only make this bound WORSE, never invalid --
    which is the direction we need, because the whole argument uses theta'(G_d[W]) as a
    LOWER bound on theta'(G_d).

    (Still `numerical`: the eigenvalue and the sum are float64.  A fully rigorous version
    would round B to rationals and certify psd-ness exactly; not done here.)
    """
    val_solver, status, M = theta_prime_sparse(adj, solver=solver, eps=eps,
                                               max_iters=max_iters, time_limit=time_limit)
    N = adj.shape[0]
    B = np.asarray(_last_problem["B"].value, dtype=float)
    B = 0.5 * (B + B.T)
    B[adj] = 0.0
    B = np.maximum(B, 0.0)
    lam = np.linalg.eigvalsh(B).min()
    if lam < 0:
        B = B + (-lam) * np.eye(N)
    tr = np.trace(B)
    if tr <= 0:
        return 1.0, status, M, val_solver
    return float(B.sum() / tr), status, M, val_solver


def alpha_exact(adj: np.ndarray) -> int:
    """Exact max independent set via HiGHS binary ILP."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    N = adj.shape[0]
    ii, jj = np.nonzero(np.triu(adj, 1))
    if len(ii) == 0:
        return N
    A = np.zeros((len(ii), N))
    A[np.arange(len(ii)), ii] = 1
    A[np.arange(len(ii)), jj] = 1
    res = milp(c=-np.ones(N), constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(N), bounds=Bounds(0, 1))
    return int(round(-res.fun))


def frac_clique_cover(adj: np.ndarray) -> float:
    """chi-bar_f(G): LP over the maximal cliques of G.  Small N only."""
    import networkx as nx
    from scipy.optimize import linprog
    N = adj.shape[0]
    cliques = list(nx.find_cliques(nx.from_numpy_array(adj.astype(int))))
    A = np.zeros((N, len(cliques)))
    for c, cl in enumerate(cliques):
        for v in cl:
            A[v, c] = 1
    res = linprog(c=np.ones(len(cliques)), A_ub=-A, b_ub=-np.ones(N),
                  bounds=(0, None), method="highs")
    return float(res.fun)


# ----------------------------------------------------------------------------------
# the geometric conflict graph on a triangular grid inside T_d
# ----------------------------------------------------------------------------------
def tri_grid(k: int):
    """Lattice coordinates (i,j), i,j>=0, i+j<=k-1, of the k-per-side triangular grid.
    Cartesian point = h*(i*(1,0) + j*(1/2,sqrt3/2)) with h = d/(k-1); this places the
    three corners exactly at A, B, C of the repo convention."""
    return [(i, j) for j in range(k) for i in range(k - j)]


def conflict_adj(k: int, d_expr):
    """Adjacency of G_d restricted to the k-per-side corner-to-corner grid.  `d_expr` is
    a sympy expression for the exact side length d.

    Squared distance between lattice points differing by (a,b) is h^2*(a^2+ab+b^2)
    with h = d/(k-1).  Edge iff that is STRICTLY < 4 (distance exactly 2 is allowed:
    all inequalities in this problem are non-strict), i.e. iff the Loeschian number
    m = a^2+ab+b^2 satisfies m < R := 4(k-1)^2/d^2.

    The comparison is integer-vs-algebraic and is decided SYMBOLICALLY (sympy), never
    by a float tolerance.  Exact ties (m == R) occur -- e.g. d = 2(k-1) puts the grid
    spacing at exactly 2 -- and are resolved as NON-edges, which is the correct reading
    of the non-strict convention.

    KNOWN DEFECT (see the write-up section 4.4): for generic d the spacing d/(k-1) is
    incommensurate with 2, so this grid contains no pair at distance exactly 2 and its
    alpha can fall well below alpha(T_d).  Use conflict_adj_anchored for a sharper witness.
    """
    import sympy as sp
    pts = tri_grid(k)
    N = len(pts)
    R = sp.simplify(sp.nsimplify(4 * (k - 1) ** 2) / (sp.together(d_expr) ** 2))
    ms = set()
    for u in range(N):
        iu, ju = pts[u]
        for v in range(u + 1, N):
            a, b = pts[v][0] - iu, pts[v][1] - ju
            ms.add(a * a + a * b + b * b)
    is_edge, ties = {}, 0
    for m in ms:
        diff = sp.simplify(R - m)
        if diff.equals(0):
            is_edge[m] = False            # distance exactly 2 -> not an edge
            ties += 1
        else:
            val = sp.N(diff, 60)
            assert abs(val) > sp.Float("1e-40"), f"undecided comparison m={m}"
            is_edge[m] = bool(val > 0)    # m < R  <=>  R - m > 0
    adj = np.zeros((N, N), dtype=bool)
    for u in range(N):
        iu, ju = pts[u]
        for v in range(u + 1, N):
            a, b = pts[v][0] - iu, pts[v][1] - ju
            if is_edge[a * a + a * b + b * b]:
                adj[u, v] = adj[v, u] = True
    return adj, pts, ties


def conflict_adj_anchored(d_expr, refine: int):
    """Same conflict graph, but on the lattice-ANCHORED grid: spacing h = 2/refine exactly,
    lattice anchored at the corner A = (0,0).

    Motivation.  The corner-to-corner grid of `conflict_adj` has spacing d/(k-1), which for
    a generic d is incommensurate with the packing distance 2.  Such a grid cannot hold any
    pair at distance exactly 2, so alpha(grid) can fall far below alpha(T_d) -- at d = 7.99
    it gave 10 where the container holds 14.  A grid of spacing exactly 2/refine contains
    the full triangular packing of spacing 2 and does not have that defect.

    Points are h*(i*(1,0) + j*(1/2,sqrt3/2)) for i, j >= 0 with i + j <= floor(d/h); that
    last inequality is exactly containment in the closed triangle (the three half-plane
    conditions reduce to i >= 0, j >= 0, h(i+j) <= d).  Adjacency is the pure INTEGER test
    a^2+ab+b^2 < refine^2, so ties -- the distance-2 pairs -- are exact and resolve to
    non-edges, as the convention requires.
    """
    import sympy as sp
    h = sp.Rational(2, refine)
    K = int(sp.floor(sp.nsimplify(d_expr) / h))
    pts = [(i, j) for j in range(K + 1) for i in range(K + 1 - j)]
    N = len(pts)
    thr = refine * refine
    adj = np.zeros((N, N), dtype=bool)
    for u in range(N):
        iu, ju = pts[u]
        for v in range(u + 1, N):
            a, b = pts[v][0] - iu, pts[v][1] - ju
            if a * a + a * b + b * b < thr:
                adj[u, v] = adj[v, u] = True
    return adj, pts, float(h)


def oler_floor(n: int) -> float:
    """Oler 1961 applied to the equilateral triangle: n <= d^2/8 + 3d/4 + 1
    => d(n) >= sqrt(8n+1) - 3.   (`cited` inequality, `sketch` application -- see
    attacks/r3-approaches/README.md section 0.1.  Used here only as a comparison target.)"""
    return math.sqrt(8 * n + 1) - 3.0


# ----------------------------------------------------------------------------------
# self-tests
# ----------------------------------------------------------------------------------
def selftest():
    import sympy as sp
    import networkx as nx
    ok = True

    def check(name, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: got {got:.6f}, want {want:.6f}")

    print("finite-graph theta' self-tests")
    A = np.ones((5, 5), dtype=bool); np.fill_diagonal(A, False)
    check("theta'(K5) = 1", theta_prime(A, solver="CLARABEL")[0], 1.0, 1e-6)
    A = np.zeros((6, 6), dtype=bool)
    check("theta'(empty_6) = 6", theta_prime(A, solver="CLARABEL")[0], 6.0, 1e-6)
    A = np.zeros((5, 5), dtype=bool)
    for i in range(5):
        A[i, (i + 1) % 5] = A[(i + 1) % 5, i] = True
    check("theta'(C5) = sqrt5", theta_prime(A, solver="CLARABEL")[0], math.sqrt(5), 1e-5)
    A = nx.to_numpy_array(nx.petersen_graph()).astype(bool)
    check("theta'(Petersen) = 4", theta_prime(A, solver="CLARABEL")[0], 4.0, 1e-5)

    print("sandwich alpha <= theta' <= chi-bar_f on random graphs")
    rng = np.random.default_rng(20260824)
    for trial in range(6):
        N = 9
        A = rng.random((N, N)) < 0.45
        A = np.triu(A, 1); A = A | A.T
        a, (t, st), f = alpha_exact(A), theta_prime(A, solver="CLARABEL"), frac_clique_cover(A)
        good = (a - 1e-6 <= t <= f + 1e-6)
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] trial {trial}: alpha={a}  theta'={t:.6f}"
              f"  chi-bar_f={f:.6f}  ({st})")

    # geometry: the grid conflict graph must reproduce the KNOWN alpha of the container.
    # At d = 2(k-1) exactly, the triangular packing of Delta(k) points is optimal (`cited`),
    # so a grid whose spacing divides 2 must give alpha = Delta(k).
    print("geometry, corner-to-corner grid, at the exactly-solved triangular cases")
    for kk in (3, 4, 5, 6):
        dd = sp.Integer(2 * (kk - 1))
        adj, pts, ties = conflict_adj(kk, dd)
        a, want = alpha_exact(adj), kk * (kk + 1) // 2
        ok &= (a == want)
        print(f"  [{'PASS' if a == want else 'FAIL'}] k={kk} d={dd}: alpha={a}, "
              f"Delta({kk})={want} ({ties} exact distance-2 tie classes)")
    for (kk, refine) in ((4, 3), (5, 3), (5, 4)):
        dd = sp.Integer(2 * (kk - 1))
        K = (kk - 1) * refine + 1
        adj, pts, _ = conflict_adj(K, dd)
        a, want = alpha_exact(adj), kk * (kk + 1) // 2
        ok &= (a == want)
        print(f"  [{'PASS' if a == want else 'FAIL'}] d={dd}, refined grid {K}/side "
              f"({len(pts)} pts): alpha={a}, Delta({kk})={want}")

    print("geometry, lattice-anchored grid, same cases")
    for (kk, refine) in ((5, 4), (5, 6), (4, 6), (6, 4)):
        dd = sp.Integer(2 * (kk - 1))
        adj, pts, h = conflict_adj_anchored(dd, refine)
        a, want = alpha_exact(adj), kk * (kk + 1) // 2
        ok &= (a == want)
        print(f"  [{'PASS' if a == want else 'FAIL'}] d={dd}, spacing {h:.4f} "
              f"({len(pts)} pts): alpha={a}, Delta({kk})={want}")

    print("\nSELFTEST", "PASSED" if ok else "FAILED")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(0 if selftest() else 1)
