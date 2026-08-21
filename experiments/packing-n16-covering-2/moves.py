"""Combinatorial moves on a convex subdivision of T_1, plus a convexity-repair LP.

FLOATS ONLY -- search stage.

The coarse structure of any 15-piece covering of T_a with a in (4,5) is forced:
every side of T_a must meet > a pieces, hence >= 5, hence >= 3 non-corner pieces per
side, hence >= 12 boundary pieces and <= 3 interior ones -- with equality throughout
when a > 4.  What is NOT forced is the fine adjacency (which faces touch which, and
the face degrees), and that is what these moves explore.
"""
import math, random, copy
import numpy as np
from scipy.optimize import linprog
from slp import Struct


def face_edges(faces):
    """directed edge -> face index"""
    d = {}
    for fi, f in enumerate(faces):
        m = len(f)
        for i in range(m):
            d[(f[i], f[(i + 1) % m])] = fi
    return d


def interior_edges(faces):
    d = face_edges(faces)
    out = []
    for (p, q), fi in d.items():
        if (q, p) in d and p < q:
            out.append((p, q, fi, d[(q, p)]))
    return out


def rot(f, p, q):
    """rotate cycle f so that it starts p,q"""
    m = len(f)
    for i in range(m):
        if f[i] == p and f[(i + 1) % m] == q:
            return f[i:] + f[:i]
    return None


def flip(faces, p, q, fi, gi, rng):
    """remove interior edge (p,q), re-split the merged polygon by another diagonal"""
    f = rot(list(faces[fi]), p, q)
    g = rot(list(faces[gi]), q, p)
    if f is None or g is None:
        return None
    M = [q] + f[2:] + [p] + g[2:]
    if len(set(M)) != len(M):
        return None
    m = len(M)
    if m < 4:
        return None
    existing = set()
    for fk, ff in enumerate(faces):
        if fk in (fi, gi): continue
        for i in range(len(ff)):
            existing.add((ff[i], ff[(i + 1) % len(ff)]))
    cand = []
    for i in range(m):
        for j in range(i + 2, m):
            if i == 0 and j == m - 1: continue
            A = M[i:j + 1]
            B = M[j:] + M[:i + 1]
            if len(A) < 3 or len(B) < 3: continue
            if (M[i], M[j]) in existing or (M[j], M[i]) in existing: continue
            if (M[i], M[j]) == (p, q) or (M[i], M[j]) == (q, p): continue
            cand.append((A, B))
    if not cand:
        return None
    A, B = rng.choice(cand)
    nf = [list(x) for x in faces]
    nf[fi] = A; nf[gi] = B
    return nf


def contract(faces, p, q, rng):
    """merge vertex q into p (edge (p,q) must be interior); faces lose a vertex"""
    nf = []
    for f in faces:
        g = [p if k == q else k for k in f]
        h = []
        for k in g:
            if not h or h[-1] != k: h.append(k)
        while len(h) > 1 and h[0] == h[-1]: h.pop()
        if len(h) < 3:
            return None
        nf.append(h)
    if len(set(tuple(sorted(f)) for f in nf)) != len(nf):
        return None
    return nf


def repair(S, delta=1e-5, iters=200, rho0=0.02):
    """push a (possibly non-convex) embedding back to strict convexity: max min cross"""
    nd = S.nd
    rho = rho0
    for it in range(iters):
        x = S.x
        cv, o, p, q = S.cvals(x)
        if cv.min() >= delta:
            return True
        U, V = S.coords(x)
        H = ((V[q] - V[o])[:, None] * (S.Au[p] - S.Au[o])
             + (U[p] - U[o])[:, None] * (S.Av[q] - S.Av[o])
             - (U[q] - U[o])[:, None] * (S.Av[p] - S.Av[o])
             - (V[p] - V[o])[:, None] * (S.Au[q] - S.Au[o]))
        nA = len(H) + len(S.L)
        A = np.zeros((nA, nd + 1)); b = np.zeros(nA)
        A[:len(H), :nd] = -H; A[:len(H), nd] = 1.0; b[:len(H)] = cv
        if len(S.L):
            A[len(H):, :nd] = S.L; b[len(H):] = S.r - S.L @ x
        c = np.zeros(nd + 1); c[nd] = -1.0
        bnds = [(-rho, rho)] * nd + [(None, None)]
        res = linprog(c, A_ub=A, b_ub=b, bounds=bnds, method="highs")
        if not res.success:
            rho *= 0.5
            if rho < 1e-12: return False
            continue
        step = res.x[:nd]
        cur = cv.min()
        t = 1.0; ok = False
        for _ in range(30):
            xt = x + t * step
            c2, _, _, _ = S.cvals(xt)
            lin_ok = True
            if len(S.r):
                lin_ok = (S.L @ xt - S.r).max() <= 1e-12
            if lin_ok and c2.min() > cur:
                S.x = xt; ok = True; break
            t *= 0.6
        if not ok:
            rho *= 0.5
            if rho < 1e-12: return False
        else:
            rho = min(rho * 1.5, 0.05)
    cv, _, _, _ = S.cvals(S.x)
    return cv.min() >= delta


def mutate(S, rng):
    """return a new Struct with a mutated combinatorial structure, or None"""
    faces = [list(f) for f in S.faces]
    ie = interior_edges(faces)
    if not ie: return None
    kind = rng.random()
    for _ in range(12):
        p, q, fi, gi = rng.choice(ie)
        if kind < 0.8:
            nf = flip(faces, p, q, fi, gi, rng)
        else:
            if S.cls[q] != 'F' and S.cls[p] != 'F':
                continue
            if S.cls[q] != 'F':
                p, q = q, p
            nf = contract(faces, p, q, rng)
        if nf is None: continue
        used = sorted(set(k for f in nf for k in f))
        remap = {k: i for i, k in enumerate(used)}
        uv = [list(S.uv[k]) for k in used]
        cls = [S.cls[k] for k in used]
        nf = [[remap[k] for k in f] for f in nf]
        try:
            T = Struct(uv, nf, cls)
        except Exception:
            continue
        return T
    return None
