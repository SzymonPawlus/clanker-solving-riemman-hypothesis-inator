"""Corner refinement: give each corner group extra arc vertices.

At a 60-degree corner V of T_a, EVERY point of the closed sector S(V,r) is within
distance r of every other (see attacks/n16-shapes/README.md, Lemma S).  So a group
whose vertices all lie in S(V, D) has diameter exactly D no matter how many arc
vertices it has -- but its AREA grows with the number of chords:

    n chords, radius r  ->  area = n * (r^2/2) * sin(60/n degrees)
    n = 1: 0.4330 r^2   n = 2: 0.5000 r^2   n = 4: 0.5176 r^2   n -> oo: 0.5236 r^2

In a convex PARTITION each extra chord needs its own neighbouring cell.  Here the
extra area is carved out of the neighbouring cell, which becomes non-convex; its
piece is the convex hull of what remains, and that hull is unchanged, so the extra
corner area is free.  This is the one thing a convex partition cannot do.
"""
import math

def uv_to_xy(p):
    return (p[0] + 0.5 * p[1], (math.sqrt(3) / 2) * p[1])

def xy_to_uv(q):
    v = q[1] / (math.sqrt(3) / 2)
    return (q[0] - 0.5 * v, v)


def corner_index(a, f, tol=1e-9):
    for i, p in enumerate(f):
        for c in ((0.0, 0.0), (a, 0.0), (0.0, a)):
            if abs(p[0] - c[0]) < tol and abs(p[1] - c[1]) < tol:
                return i
    return None


def neighbour_map(faces, tol=1e-9):
    """(rounded point pair) -> face index, for the directed edges of each face."""
    key = lambda p: (round(p[0], 10), round(p[1], 10))
    m = {}
    for fi, f in enumerate(faces):
        n = len(f)
        for i in range(n):
            m[(key(f[i]), key(f[(i + 1) % n]))] = (fi, i)
    return m, key


def refine(a, faces, per_gap=1):
    """Insert `per_gap` new arc vertices into every gap of every corner face.
    Returns (new_faces, extra) where extra[fi] is a list of (insert_after_index, pt)
    to be carved out of neighbour face fi.  new_faces[ci] is the enlarged corner face."""
    m, key = neighbour_map(faces)
    new_faces = [list(f) for f in faces]
    bites = {}          # neighbour face index -> list of (i, j, Q)  (Q bites edge f[i]->f[j])
    for ci, f in enumerate(faces):
        k = corner_index(a, f)
        if k is None:
            continue
        V = f[k]
        arc = f[k + 1:] + f[:k]                 # arc vertices, in order away from V
        Vxy = uv_to_xy(V)
        newarc = [arc[0]]
        for t in range(len(arc) - 1):
            P, Q = arc[t], arc[t + 1]
            nb = m.get((key(Q), key(P)))         # neighbour across edge P->Q of the corner face
            Pxy, Qxy = uv_to_xy(P), uv_to_xy(Q)
            aP = math.atan2(Pxy[1] - Vxy[1], Pxy[0] - Vxy[0])
            aQ = math.atan2(Qxy[1] - Vxy[1], Qxy[0] - Vxy[0])
            while aQ - aP > math.pi: aQ -= 2 * math.pi
            while aP - aQ > math.pi: aP -= 2 * math.pi
            rP = math.hypot(Pxy[0] - Vxy[0], Pxy[1] - Vxy[1])
            rQ = math.hypot(Qxy[0] - Vxy[0], Qxy[1] - Vxy[1])
            r = min(rP, rQ)
            for s in range(1, per_gap + 1):
                th = aP + (aQ - aP) * s / (per_gap + 1)
                W = xy_to_uv((Vxy[0] + r * math.cos(th), Vxy[1] + r * math.sin(th)))
                newarc.append(W)
                if nb is not None:
                    bites.setdefault(nb[0], []).append((key(Q), key(P), W))
            newarc.append(Q)
        new_faces[ci] = [V] + newarc
    return new_faces, bites


def triangulate(a, faces, bites):
    """Build V, tris, grp.  Corner faces are fanned from the corner; a face with
    bites has each bite triangle removed and the remainder fanned from the bite
    point.  (At most one bite per face is supported -- true for the record.)"""
    V, idx = [], {}
    def vid(p):
        k = (round(p[0], 12), round(p[1], 12))
        if k not in idx:
            idx[k] = len(V); V.append([p[0], p[1]])
        return idx[k]
    key = lambda p: (round(p[0], 10), round(p[1], 10))
    tris, grp = [], []
    for fi, f in enumerate(faces):
        ids = [vid(p) for p in f]
        s = 0.0
        for i in range(len(ids)):
            x1, y1 = V[ids[i]]; x2, y2 = V[ids[(i + 1) % len(ids)]]
            s += x1 * y2 - x2 * y1
        if s < 0:
            ids = ids[::-1]; f = f[::-1]
        bl = bites.get(fi, [])
        if not bl:
            for i in range(1, len(ids) - 1):
                tris.append((ids[0], ids[i], ids[i + 1])); grp.append(fi)
            continue
        assert len(bl) == 1, "only one bite per face supported"
        kP, kQ, W = bl[0]
        pos = {key((V[j][0], V[j][1])): t for t, j in enumerate(ids)}
        iP, iQ = pos[kP], pos[kQ]
        n = len(ids)
        assert (iP + 1) % n == iQ, "bite edge must be a directed edge of the face"
        w = vid(W)
        chain = [ids[(iQ + t) % n] for t in range(n)]   # from Q around to P
        for t in range(len(chain) - 1):
            tris.append((w, chain[t], chain[t + 1])); grp.append(fi)
    return V, tris, grp
