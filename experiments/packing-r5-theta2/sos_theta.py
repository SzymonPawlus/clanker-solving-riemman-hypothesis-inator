"""
Prong 2: actually SOLVE the container-theta' SOS problem that attacks/r4-theta specified
but never ran, and read an actual theta'-derived floor for d(n) off it.

WHAT IS BEING SOLVED
--------------------
Rescale the triangle to unit side: u in T_1 (A=(0,0), B=(1,0), C=(1/2, sqrt3/2)), and put
rho = 2/d, so "distance >= 2 in T_d" becomes "distance >= rho in T_1".  Look for a
symmetric psd kernel Z(u,v) = w_m(u)^T C w_m(v), C psd, w_m = monomials of degree <= m in
two variables, with

    (P1)   lam - 1 - Z(u,u) >= 0            for all u in T_1
    (P2)   -1 - Z(u,v)      >= 0            for all u,v in T_1 with ||u-v||^2 >= rho^2

Any such (C, lam) certifies theta'(G_d) <= lam (soundness lemma, re-derived in
theta2_core).  So  lam < n  =>  alpha(G_d) < n  =>  d(n) > d = 2/rho.

Both non-negativity conditions are discharged by a Putinar representation:

    P1 = sig0 + sig1 g1 + sig2 g2 + sig3 g3                       (2 variables)
    P2 = tau0 + sum_{i=1}^{6} tau_i G_i + tau7 h                  (4 variables)

with g1 = u2, g2 = sqrt3 u1 - u2, g3 = sqrt3 (1-u1) - u2 the three half-planes of T_1,
G_1..3 = g_1..3 in u, G_4..6 = g_1..3 in v, h = ||u-v||^2 - rho^2, and every sig/tau an
SOS (a psd Gram matrix against a monomial basis).  Minimise lam.

DIRECTION OF THE ERROR.  SOS is a RESTRICTION of the kernel problem, so the optimum
lam_SOS(m, d) >= theta'(G_d).  That is the useful direction: an upper bound on theta' is
what turns into a lower bound on d(n).  It is the opposite direction from the finite-
witness instrument of Prong 1, which lower-bounds theta'.

STATUS.  Every number here is float SDP output, hence `numerical` (RULES.md section 3).
It is NOT a bound until the certificate is rounded to exact arithmetic; see
`repair_bound` for the honest partial repair actually performed and its limits.
"""
from __future__ import annotations

import itertools
import math

import numpy as np
import scipy.sparse as sp

try:
    import cvxpy as cp
except ImportError:  # pragma: no cover
    cp = None

SQRT3 = math.sqrt(3.0)


# ------------------------------------------------------------------ polynomial algebra
def monomials(nv: int, D: int):
    """All exponent tuples in nv variables of total degree <= D, graded lex."""
    out = []
    for total in range(D + 1):
        for c in itertools.combinations_with_replacement(range(nv), total):
            e = [0] * nv
            for i in c:
                e[i] += 1
            out.append(tuple(e))
    return out


def padd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def pmul(p: dict, q: dict) -> dict:
    r = {}
    for ea, ca in p.items():
        for eb, cb in q.items():
            k = padd(ea, eb)
            r[k] = r.get(k, 0.0) + ca * cb
    return r


def pdeg(p: dict) -> int:
    return max(sum(e) for e in p) if p else 0


# ------------------------------------------------------------------ the semialgebraic sets
def triangle_gs(nv: int, off: int) -> list:
    """The three half-planes of the UNIT triangle T_1 acting on variables off, off+1."""
    def m(*pairs):
        e = [0] * nv
        for i, k in pairs:
            e[i] = k
        return tuple(e)
    one = tuple([0] * nv)
    g1 = {m((off + 1, 1)): 1.0}                                   # u2 >= 0
    g2 = {m((off, 1)): SQRT3, m((off + 1, 1)): -1.0}              # sqrt3 u1 - u2 >= 0
    g3 = {one: SQRT3, m((off, 1)): -SQRT3, m((off + 1, 1)): -1.0}  # sqrt3(1-u1) - u2 >= 0
    return [g1, g2, g3]


def sep_h(rho: float) -> dict:
    """h(u,v) = ||u-v||^2 - rho^2 >= 0, in variables (u1,u2,v1,v2)."""
    h = {}
    for (i, j) in ((0, 2), (1, 3)):
        for (a, b, c) in ((i, i, 1.0), (j, j, 1.0), (i, j, -2.0)):
            e = [0, 0, 0, 0]
            e[a] += 1
            e[b] += 1
            h[tuple(e)] = h.get(tuple(e), 0.0) + c
    h[(0, 0, 0, 0)] = h.get((0, 0, 0, 0), 0.0) - rho * rho
    return h


# ------------------------------------------------------------------ SOS block -> coeff map
def block_map(basis, g: dict, idx: dict, nmon: int):
    """Sparse matrix S with  (S @ vec(M))[mu] = coefficient of mu in  (b^T M b) * g."""
    k = len(basis)
    rows, cols, vals = [], [], []
    for i in range(k):
        for j in range(k):
            base = padd(basis[i], basis[j])
            for eg, cg in g.items():
                mu = padd(base, eg)
                r = idx.get(mu)
                if r is None:
                    raise KeyError(f"monomial {mu} outside the truncation")
                rows.append(r)
                cols.append(i * k + j)
                vals.append(cg)
    return sp.csr_matrix((vals, (rows, cols)), shape=(nmon, k * k))


def build_sos(m: int, rho: float, lam_fixed: float | None = None, D: int | None = None):
    """Assemble the SDP.  Returns (problem, variables dict).

    `m`  : bidegree of the kernel Z (so rank Z <= C(m+2,2); see Lemma 4 of r4-theta).
    `D`  : total-degree budget of the Putinar certificates, D >= 2m and even.  D = 2m is
           the tightest truncation; raising D strictly enlarges the set of representable
           certificates and can only lower lam.  This is the "order" of the relaxation and
           is a separate knob from the kernel degree m -- attacks/r4-theta's cost table
           only counted the D = 2m case.
    """
    ONE2 = (0, 0)
    ONE4 = (0, 0, 0, 0)
    if D is None:
        D = 2 * m
    assert D >= 2 * m and D % 2 == 0
    D2, D4 = D, D

    mon2 = monomials(2, D2)
    idx2 = {e: i for i, e in enumerate(mon2)}
    mon4 = monomials(4, D4)
    idx4 = {e: i for i, e in enumerate(mon4)}

    wm = monomials(2, m)                       # kernel basis
    K = len(wm)

    C = cp.Variable((K, K), symmetric=True)
    lam = cp.Variable() if lam_fixed is None else cp.Constant(lam_fixed)

    # ---- Z(u,u): substitute v := u, so monomial is wm[p] + wm[q] in 2 vars ----------
    rows, cols, vals = [], [], []
    for p in range(K):
        for q in range(K):
            rows.append(idx2[padd(wm[p], wm[q])]); cols.append(p * K + q); vals.append(1.0)
    Sdiag = sp.csr_matrix((vals, (rows, cols)), shape=(len(mon2), K * K))

    # ---- Z(u,v): monomial is (wm[p] in u) x (wm[q] in v) in 4 vars ------------------
    rows, cols, vals = [], [], []
    for p in range(K):
        for q in range(K):
            e = (wm[p][0], wm[p][1], wm[q][0], wm[q][1])
            rows.append(idx4[e]); cols.append(p * K + q); vals.append(1.0)
    Skern = sp.csr_matrix((vals, (rows, cols)), shape=(len(mon4), K * K))

    cons = [C >> 0]
    blocks = {"C": C}

    # ---- (P1) on T_1, 2 variables ---------------------------------------------------
    g2v = triangle_gs(2, 0)
    b0 = monomials(2, D // 2)
    b1 = monomials(2, (D - 1) // 2)
    S0 = block_map(b0, {ONE2: 1.0}, idx2, len(mon2))
    rhs2 = -Sdiag @ cp.vec(C, order="C")
    e = np.zeros(len(mon2)); e[idx2[ONE2]] = 1.0
    lhs2 = rhs2 + (lam - 1) * e
    M0 = cp.Variable((len(b0), len(b0)), PSD=True)
    blocks["sig0"] = M0
    acc = S0 @ cp.vec(M0, order="C")
    for i, g in enumerate(g2v):
        Mi = cp.Variable((len(b1), len(b1)), PSD=True)
        blocks[f"sig{i+1}"] = Mi
        acc = acc + block_map(b1, g, idx2, len(mon2)) @ cp.vec(Mi, order="C")
    cons.append(lhs2 == acc)

    # ---- (P2) on Sigma, 4 variables --------------------------------------------------
    G = triangle_gs(4, 0) + triangle_gs(4, 2)
    h = sep_h(rho)
    c0 = monomials(4, D // 2)
    c1 = monomials(4, (D - 1) // 2)
    c2 = monomials(4, (D - 2) // 2)
    e4 = np.zeros(len(mon4)); e4[idx4[ONE4]] = 1.0
    lhs4 = -Skern @ cp.vec(C, order="C") - e4
    N0 = cp.Variable((len(c0), len(c0)), PSD=True)
    blocks["tau0"] = N0
    acc4 = block_map(c0, {ONE4: 1.0}, idx4, len(mon4)) @ cp.vec(N0, order="C")
    for i, g in enumerate(G + [h]):
        bas = c1 if i < len(G) else c2
        Ni = cp.Variable((len(bas), len(bas)), PSD=True)
        blocks[f"tau{i+1}"] = Ni
        acc4 = acc4 + block_map(bas, g, idx4, len(mon4)) @ cp.vec(Ni, order="C")
    cons.append(lhs4 == acc4)

    obj = cp.Minimize(lam if lam_fixed is None else cp.Constant(0.0))
    prob = cp.Problem(obj, cons)
    blocks["lam"] = lam
    blocks["sizes"] = {"m": m, "D": D, "K": K, "sig0": len(b0), "sig_i": len(b1),
                       "tau0": len(c0), "tau_i": len(c1), "tau_h": len(c2),
                       "eqs2": len(mon2), "eqs4": len(mon4)}
    return prob, blocks


def solve_lambda(m: int, d: float, solver="SCS", eps=1e-7, max_iters=400000,
                 time_limit=None, verbose=False, D=None):
    """Minimise lam.  Returns dict with the SOS value (an UPPER bound on theta'(G_d),
    modulo solver accuracy -- `numerical`, not a proof)."""
    rho = 2.0 / d
    prob, B = build_sos(m, rho, D=D)
    kw = {}
    if solver == "SCS":
        kw = dict(eps=eps, max_iters=max_iters)
        if time_limit:
            kw["time_limit_secs"] = float(time_limit)
    try:
        prob.solve(solver=solver, verbose=verbose, **kw)
    except Exception as exc:
        return {"m": m, "D": B["sizes"]["D"], "d": d, "rho": rho, "lam": float("nan"),
                "status": f"solver-error:{exc}", "sizes": B["sizes"]}
    lam = B["lam"].value
    return {"m": m, "D": B["sizes"]["D"], "d": d, "rho": rho,
            "lam": float(lam) if lam is not None else float("nan"),
            "status": str(prob.status), "sizes": B["sizes"],
            "C": None if B["C"].value is None else np.asarray(B["C"].value)}


# ------------------------------------------------------------------ honest repair
def repair_bound(C: np.ndarray, m: int, d: float, ngrid: int = 90, nsep: int = 400000,
                 seed: int = 20260824):
    """A SAMPLED repair of the solver's kernel into a self-consistent lam.

    If Z is a psd kernel with  max_{T_1} Z(u,u) <= A  and  max_{Sigma} Z(u,v) = -b < 0,
    then Z/b is psd, has every non-adjacent off-diagonal entry <= -1 and diagonal <= A/b,
    so lam = A/b + 1 is feasible.  This function estimates A and b by SAMPLING (a dense
    grid on T_1 for A; grid + random pairs on Sigma for b) and returns A/b + 1.

    LIMITATION, stated plainly: sampling gives no rigorous bound on a supremum, so the
    number returned is `numerical` in exactly the same way the raw SDP value is.  A
    rigorous version needs interval branch-and-bound on the 4-dimensional Sigma, or an
    exact rational rounding of the Putinar Gram matrices.  Neither is done here.
    """
    C = 0.5 * (C + C.T)
    w, V = np.linalg.eigh(C)
    C = (V * np.maximum(w, 0.0)) @ V.T          # project to psd: keeps Z a psd kernel
    wm = monomials(2, m)

    def basis(P):
        return np.stack([P[:, 0] ** a * P[:, 1] ** b for (a, b) in wm], axis=1)

    # grid on the unit triangle
    us = []
    for i in range(ngrid + 1):
        for j in range(ngrid + 1 - i):
            a, b = i / ngrid, j / ngrid
            us.append((a + 0.5 * b, b * SQRT3 / 2))
    U = np.asarray(us)
    W = basis(U)
    diag = np.einsum("ij,jk,ik->i", W, C, W)
    A = float(diag.max())

    rho = 2.0 / d
    rng = np.random.default_rng(seed)
    worst = -np.inf
    # (a) all grid pairs at separation >= rho
    step = max(1, len(U) // 700)
    Us = U[::step]
    Ws = basis(Us)
    D2 = ((Us[:, None, :] - Us[None, :, :]) ** 2).sum(-1)
    ok = D2 >= rho * rho
    if ok.any():
        Zs = Ws @ C @ Ws.T
        worst = max(worst, float(Zs[ok].max()))
    # (b) random pairs, rejection-sampled onto Sigma
    got = 0
    while got < nsep:
        k = min(200000, nsep - got)
        a = rng.random(k); b = rng.random(k)
        fl = a + b > 1
        a[fl], b[fl] = 1 - a[fl], 1 - b[fl]
        P = np.stack([a + 0.5 * b, b * SQRT3 / 2], 1)
        a = rng.random(k); b = rng.random(k)
        fl = a + b > 1
        a[fl], b[fl] = 1 - a[fl], 1 - b[fl]
        Q = np.stack([a + 0.5 * b, b * SQRT3 / 2], 1)
        sel = ((P - Q) ** 2).sum(1) >= rho * rho
        if sel.any():
            Wp, Wq = basis(P[sel]), basis(Q[sel])
            worst = max(worst, float(np.einsum("ij,jk,ik->i", Wp, C, Wq).max()))
        got += k
    b = -worst
    return {"A": A, "max_offdiag": worst, "b": b,
            "lam_repaired": (A / b + 1.0) if b > 0 else float("inf")}
