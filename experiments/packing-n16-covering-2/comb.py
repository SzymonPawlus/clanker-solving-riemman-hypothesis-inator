"""Purely combinatorial handling of a subdivision structure + Tutte embedding.

A structure is just a list of faces (index cycles, ccw).  Everything geometric is
derived: the boundary cycle gives which vertices lie on which side of T_1, the three
corners are the boundary vertices of graph-degree 2, and Tutte's barycentric embedding
(1963) then produces a straight-line embedding with all faces convex, for ANY such
structure -- so a combinatorial move never needs geometric repair.
FLOATS ONLY -- search stage.
"""
import numpy as np
from slp import Struct


def boundary_cycle(faces):
    dirs = set()
    for f in faces:
        m = len(f)
        for i in range(m):
            dirs.add((f[i], f[(i + 1) % m]))
    bnd = {q: p for (p, q) in dirs if (q, p) not in dirs}   # reversed: outer face cycle
    if not bnd:
        return None
    start = next(iter(bnd))
    cyc = [start]; cur = bnd[start]
    while cur != start:
        cyc.append(cur)
        if cur not in bnd:
            return None
        cur = bnd[cur]
        if len(cyc) > len(bnd) + 2:
            return None
    return cyc if len(cyc) == len(bnd) else None


def classify_comb(faces):
    """corners = boundary vertices incident to exactly one face; returns (cls, sides)"""
    cyc = boundary_cycle(faces)
    if cyc is None:
        return None, None
    nv = max(max(f) for f in faces) + 1
    inc = [0] * nv
    for f in faces:
        for k in set(f):
            inc[k] += 1
    corners = [k for k in cyc if inc[k] == 1]
    if len(corners) != 3:
        return None, None
    i0 = cyc.index(corners[0])
    cyc = cyc[i0:] + cyc[:i0]
    ci = [cyc.index(c) for c in corners]
    ci.sort()
    sides = [cyc[ci[0]:ci[1] + 1], cyc[ci[1]:ci[2] + 1], cyc[ci[2]:] + [cyc[0]]]
    cls = ['F'] * nv
    names = ['AB', 'BC', 'CA']
    for s, nm in zip(sides, names):
        for k in s[1:-1]:
            cls[k] = nm
    for c in corners:
        cls[c] = 'C'
    return cls, sides


def embed(faces, iters_ok=True):
    """Tutte embedding of the structure in T_1; returns a Struct or None."""
    cls, sides = classify_comb(faces)
    if cls is None:
        return None
    nv = len(cls)
    corner_pos = {sides[0][0]: (0.0, 0.0), sides[1][0]: (1.0, 0.0), sides[2][0]: (0.0, 1.0)}
    pos = [[0.0, 0.0] for _ in range(nv)]
    for k, p in corner_pos.items():
        pos[k] = list(p)
    ends = [((0.0, 0.0), (1.0, 0.0)), ((1.0, 0.0), (0.0, 1.0)), ((0.0, 1.0), (0.0, 0.0))]
    for s, (P, Qe) in zip(sides, ends):
        inner = s[1:-1]
        n = len(inner)
        for r, k in enumerate(inner):
            t = (r + 1.0) / (n + 1.0)
            pos[k] = [P[0] + t * (Qe[0] - P[0]), P[1] + t * (Qe[1] - P[1])]
    nbr = [set() for _ in range(nv)]
    for f in faces:
        m = len(f)
        for i in range(m):
            a, b = f[i], f[(i + 1) % m]
            nbr[a].add(b); nbr[b].add(a)
    free = [k for k in range(nv) if cls[k] == 'F']
    if not free:
        return None
    ix = {k: i for i, k in enumerate(free)}
    n = len(free)
    A = np.zeros((n, n)); rhs = np.zeros((n, 2))
    for k in free:
        i = ix[k]
        A[i, i] = len(nbr[k])
        for j in nbr[k]:
            if cls[j] == 'F':
                A[i, ix[j]] -= 1.0
            else:
                rhs[i, 0] += pos[j][0]; rhs[i, 1] += pos[j][1]
    try:
        sol = np.linalg.solve(A, rhs)
    except Exception:
        return None
    for k in free:
        pos[k] = [sol[ix[k], 0], sol[ix[k], 1]]
    try:
        S = Struct(pos, [list(f) for f in faces], cls)
    except Exception:
        return None
    c, _, _, _ = S.cvals(S.x)
    if c.min() < -1e-12:          # Tutte gives convexity; flat vertices are allowed
        return None
    if min(S.areas(S.x)) < 1e-7:  # but no face may be degenerate
        return None
    return S


def key(faces):
    return tuple(sorted(tuple(sorted(f)) for f in faces))


def rot(f, p, q):
    m = len(f)
    for i in range(m):
        if f[i] == p and f[(i + 1) % m] == q:
            return f[i:] + f[:i]
    return None


def all_flips(faces):
    """every re-splitting of every pair of faces sharing an interior edge"""
    dirs = {}
    for fi, f in enumerate(faces):
        m = len(f)
        for i in range(m):
            dirs[(f[i], f[(i + 1) % m])] = fi
    out = []
    seen = set()
    for (p, q), fi in list(dirs.items()):
        if (q, p) not in dirs:
            continue
        gi = dirs[(q, p)]
        if (min(p, q), max(p, q)) in seen:
            continue
        seen.add((min(p, q), max(p, q)))
        f = rot(list(faces[fi]), p, q); g = rot(list(faces[gi]), q, p)
        if f is None or g is None:
            continue
        M = [q] + f[2:] + [p] + g[2:]
        if len(set(M)) != len(M):
            continue
        m = len(M)
        existing = set()
        for fk, ff in enumerate(faces):
            if fk in (fi, gi):
                continue
            for i in range(len(ff)):
                existing.add((min(ff[i], ff[(i + 1) % len(ff)]),
                              max(ff[i], ff[(i + 1) % len(ff)])))
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                A = M[i:j + 1]; B = M[j:] + M[:i + 1]
                if len(A) < 3 or len(B) < 3:
                    continue
                e = (min(M[i], M[j]), max(M[i], M[j]))
                if e in existing or e == (min(p, q), max(p, q)):
                    continue
                nf = [list(x) for x in faces]
                nf[fi] = A; nf[gi] = B
                out.append(nf)
    return out
