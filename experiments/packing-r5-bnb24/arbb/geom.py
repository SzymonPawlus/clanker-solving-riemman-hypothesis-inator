"""Exact dyadic-triangle geometry for the active-region branch and bound.

Container (problem RULES.md Sec.2): A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2), closed.

Level-L subdivision.  With h = d/2^L, u = (h,0), v = (h/2, h*sqrt(3)/2), every vertex
produced by L rounds of the standard 4-way split of an equilateral triangle is
a*u + b*v with integers a,b >= 0, a+b <= 2^L.  Cells:

    up(i,j)   : vertices (i,j), (i+1,j), (i,j+1)          i,j>=0, i+j <= 2^L-1
    down(i,j) : vertices (i+1,j), (i,j+1), (i+1,j+1)      i,j>=0, i+j <= 2^L-2

There are 4^L of them and they cover T_d exactly (closed cells, shared edges).

ALL arithmetic that enters an accept/reject decision is integer.  For a lattice
displacement a*u + b*v,

    |a*u + b*v|^2 = h^2 * (a^2 + a*b + b^2),      h = p / (q * 2^L)   for d = p/q,

so with Q := a^2 + a*b + b^2 (an integer),

    max separation of cells e,f is  < 2   <==>   p^2 * maxQ(e,f)  <  4 * q^2 * 4^L .

No float ever enters an accept/reject decision.
"""

from fractions import Fraction

import numpy as np


def cell_labels(L):
    """(orientation, i, j) label of every cell, in the canonical index order."""
    N = 1 << L
    out = []
    for j in range(N):
        for i in range(N - j):
            out.append((0, i, j))
    for j in range(N - 1):
        for i in range(N - 1 - j):
            out.append((1, i, j))
    return out


def cells_of_level(L):
    """(cells, verts): cells[k] = triple of vertex indices, verts[m] = (a,b)."""
    N = 1 << L
    vid = {}
    verts = []
    for b in range(N + 1):
        for a in range(N + 1 - b):
            vid[(a, b)] = len(verts)
            verts.append((a, b))
    cells = []
    for j in range(N):
        for i in range(N - j):
            cells.append((vid[(i, j)], vid[(i + 1, j)], vid[(i, j + 1)]))
    for j in range(N - 1):
        for i in range(N - 1 - j):
            cells.append((vid[(i + 1, j)], vid[(i, j + 1)], vid[(i + 1, j + 1)]))
    assert len(cells) == N * N
    return np.array(cells, dtype=np.int64), np.array(verts, dtype=np.int64)


def _q_matrix(verts):
    a = verts[:, 0].astype(np.int64)
    b = verts[:, 1].astype(np.int64)
    da = a[:, None] - a[None, :]
    db = b[:, None] - b[None, :]
    return (da * da + da * db + db * db).astype(np.int64)


def conflict_bitsets(L, p, q, chunk=128, progress=False):
    """Adjacency bitsets of the cell conflict graph at level L for d = p/q.

    Cells e != f conflict  <=>  their maximum separation is < 2, i.e. they cannot
    simultaneously host two points at distance >= 2.  The maximum of |x-y| over a
    product of two convex polygons is attained at a vertex pair, so the 3x3 vertex
    scan is exact.

    Returns (adj, cells, verts) with adj[e] a Python int bitset, diagonal clear.
    """
    cells, verts = cells_of_level(L)
    M = cells.shape[0]
    Q = _q_matrix(verts)
    thresh = 4 * (q * q) * (1 << (2 * L))
    p2 = p * p
    assert p2 * int(Q.max()) < 2**62, "int64 overflow risk; reduce p/q or L"

    flat_all = cells.reshape(-1)
    adj = []
    for s in range(0, M, chunk):
        e = min(s + chunk, M)
        rows = cells[s:e].reshape(-1)
        sub = Q[np.ix_(rows, flat_all)]
        sub = sub.reshape(e - s, 3, M, 3).max(axis=3).max(axis=1)
        bad = (p2 * sub) < thresh
        for k in range(e - s):
            row = bad[k]
            row[s + k] = False
            adj.append(int.from_bytes(np.packbits(row, bitorder="little").tobytes(), "little"))
        if progress and (s // chunk) % 8 == 0:
            print(f"  adjacency {e}/{M}", flush=True)
    return adj, cells, verts


def locate(a, b, L):
    """Index of a cell of level L containing the point with lattice coords (a,b).

    a, b are Fractions with a,b >= 0 and a+b <= 2^L.  Returns a cell index; when the
    point lies on a cell boundary any containing cell is returned (all are valid:
    the conflict test only needs p_i in c_i).
    """
    N = 1 << L
    i = int(a) if a == int(a) else int(a // 1)
    j = int(b) if b == int(b) else int(b // 1)
    i = min(max(i, 0), N - 1)
    j = min(max(j, 0), N - 1)
    while i + j > N - 1:
        if i > 0:
            i -= 1
        else:
            j -= 1
    fa, fb = a - i, b - j
    if fa + fb <= 1 or i + j > N - 2:
        return _index_up(i, j, L)
    return _index_down(i, j, L)


def _index_up(i, j, L):
    N = 1 << L
    # rows j' < j contribute (N - j') cells each
    return sum(N - jj for jj in range(j)) + i


def _index_down(i, j, L):
    N = 1 << L
    base = N * (N + 1) // 2
    return base + sum(N - 1 - jj for jj in range(j)) + i


def tile_level(p, q, L):
    """Smallest level j <= L with side d/2^j < 2, i.e. every cell of that level
    holds at most one packing point (its diameter is its side).  Returns None if
    no such level <= L exists."""
    for j in range(L + 1):
        # d / 2^j < 2  <=>  p < 2 * q * 2^j
        if p < 2 * q * (1 << j):
            return j
    return None


def ancestor_map(L, j):
    """anc[k] = canonical index at level j of the ancestor of level-L cell k."""
    assert 0 <= j <= L
    shift = L - j
    labels = cell_labels(L)
    Nj = 1 << j
    up_base = 0
    down_base = Nj * (Nj + 1) // 2

    def idx_up(i, jj):
        return sum(Nj - t for t in range(jj)) + i

    def idx_down(i, jj):
        return down_base + sum(Nj - 1 - t for t in range(jj)) + i

    out = []
    for (o, i, jj) in labels:
        # cell occupies the lattice square-ish region; its ancestor is determined by
        # the coarse lattice cell containing its centroid.
        # centroid lattice coords (times 3): up -> (3i+1, 3j+1), down -> (3i+2, 3j+2)
        if o == 0:
            ca, cb = 3 * i + 1, 3 * jj + 1
        else:
            ca, cb = 3 * i + 2, 3 * jj + 2
        # scale to level-j lattice: divide by 2^shift
        s = 3 * (1 << shift)
        ia, ib = ca // s, cb // s
        ra, rb = ca - ia * s, cb - ib * s
        if ra + rb < s:
            out.append(idx_up(ia, ib))
        else:
            out.append(idx_down(ia, ib))
    return np.array(out, dtype=np.int64), Nj * Nj
