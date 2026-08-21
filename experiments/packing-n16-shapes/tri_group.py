"""Search over 15-piece coverings of T_a by GROUPS of triangles.  FLOATS ONLY.

Representation
--------------
A triangulation of T_a (vertices V, triangles as index triples, all positively
oriented) together with a map  triangle -> group  onto {0,...,14}.

    piece_g := conv( union of the triangles of group g )

Coverage of T_a is then automatic and needs no checking during the search: the
triangles tile T_a and each triangle lies inside its group's piece.  A group
whose triangles form a NON-convex region gives a piece that overlaps its
neighbours -- which is legal (a covering need not be a partition) and is exactly
the freedom a convex partition (the previous attack) does not have.

    diam(piece_g) = max pairwise distance among the vertices used by group g
                    (the diameter of a polygon is attained at a vertex pair).

Everything here is float and decides nothing; certificates are re-derived exactly
in `certify.py`.
"""
import math, random

SQ3 = math.sqrt(3.0)


def sq(p, q):
    du = p[0] - q[0]
    dv = p[1] - q[1]
    return du * du + du * dv + dv * dv


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


class Cover:
    def __init__(self, a, V, tris, grp):
        self.a = float(a)
        self.V = [list(p) for p in V]
        self.tris = [tuple(t) for t in tris]
        self.grp = list(grp)
        self.ng = max(grp) + 1
        self.gverts = [set() for _ in range(self.ng)]
        for t, g in zip(self.tris, self.grp):
            self.gverts[g].update(t)
        self.gverts = [sorted(s) for s in self.gverts]
        self.vtris = [[] for _ in self.V]
        for i, t in enumerate(self.tris):
            for k in t:
                self.vtris[k].append(i)
        self.vgrps = [sorted({self.grp[i] for i in self.vtris[k]}) for k in range(len(self.V))]
        self.cls = self.classify()
        self.d = [self.gdiam2(g) for g in range(self.ng)]

    # ---------------- vertex classes: pinned corner / slides on a side / free
    def classify(self):
        a = self.a
        eps = 1e-9 * max(1.0, a)
        cls = []
        for (u, v) in self.V:
            on = []
            if abs(u) < eps: on.append(0)          # side u = 0
            if abs(v) < eps: on.append(1)          # side v = 0
            if abs(u + v - a) < eps: on.append(2)  # side u + v = a
            if len(on) >= 2:
                cls.append(("pin", None))
            elif len(on) == 1:
                cls.append(("side", on[0]))
            else:
                cls.append(("free", None))
        return cls

    def gdiam2(self, g):
        vs = self.gverts[g]
        V = self.V
        m = 0.0
        for i in range(len(vs)):
            pi = V[vs[i]]
            for j in range(i + 1, len(vs)):
                d = sq(pi, V[vs[j]])
                if d > m:
                    m = d
        return m

    # ---------------- validity
    def tri_ok(self, i, tol=1e-12):
        t = self.tris[i]
        V = self.V
        return orient(V[t[0]], V[t[1]], V[t[2]]) > tol

    def vertex_ok(self, k):
        u, v = self.V[k]
        a = self.a
        if u < -1e-12 or v < -1e-12 or u + v > a + 1e-12:
            return False
        return all(self.tri_ok(i) for i in self.vtris[k])

    def all_ok(self):
        return all(self.tri_ok(i) for i in range(len(self.tris)))

    # ---------------- objective
    def obj(self, p):
        mx = max(self.d)
        if mx <= 0:
            return 0.0
        return mx * (sum((x / mx) ** p for x in self.d)) ** (1.0 / p)

    def maxd(self):
        return max(self.d)

    def refresh(self):
        self.d = [self.gdiam2(g) for g in range(self.ng)]

    # ---------------- local descent
    def descend(self, ps=(4.0, 20.0, 100.0, 500.0), step0=0.04, tol=1e-9, maxpass=4000):
        n = len(self.V)
        moved_dirs = [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, -1.0)]
        for p in ps:
            cur = self.obj(p)
            step = step0 * self.a
            while step > tol * self.a:
                improved = False
                for k in range(n):
                    c, si = self.cls[k]
                    if c == "pin":
                        continue
                    if c == "side":
                        dirs = [(1.0, 0.0)] if si == 0 else ([(0.0, 1.0)] if si == 1 else [(1.0, -1.0)])
                        # side 0 is u=0 -> move in v ; side 1 is v=0 -> move in u
                        if si == 0: dirs = [(0.0, 1.0)]
                        elif si == 1: dirs = [(1.0, 0.0)]
                        else: dirs = [(1.0, -1.0)]
                    else:
                        dirs = moved_dirs
                    for (du, dv) in dirs:
                        for s in (1.0, -1.0):
                            old = list(self.V[k])
                            oldd = {g: self.d[g] for g in self.vgrps[k]}
                            self.V[k][0] += s * step * du
                            self.V[k][1] += s * step * dv
                            if not self.vertex_ok(k):
                                self.V[k] = old
                                continue
                            for g in self.vgrps[k]:
                                self.d[g] = self.gdiam2(g)
                            nv = self.obj(p)
                            if nv < cur - 1e-15:
                                cur = nv
                                improved = True
                            else:
                                self.V[k] = old
                                for g, dv2 in oldd.items():
                                    self.d[g] = dv2
                if not improved:
                    step *= 0.5
        self.refresh()
        return self.maxd()
