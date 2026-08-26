"""Active-region branch and bound for the decision problem

    "do n points at pairwise distance >= 2 fit in the closed equilateral triangle
     T_d of side d = p/q ?"

An `unsat` verdict means d(n) > d.  A `sat` verdict means only that *this relaxation*
cannot refute d; it is NOT a packing.

THE RELAXATION (this is the only place a mathematical claim is made).
Fix the level-L dyadic subdivision of T_d into 4^L closed cells covering T_d, of side
h = d/2^L < 2.  Let n points of T_d have pairwise distance >= 2.  Each point lies in
at least one cell; choose one.  Two points in the same cell would be at distance
<= h < 2, so the n cells are distinct; and for cells e != f holding two of the points,
the maximum separation of e and f is >= 2.  Hence the n cells form an independent set
of size n in

    G_L = (cells,  e ~ f  iff  max separation of e and f is < 2),

so   alpha(G_L) < n  ==>  no such n points exist  ==>  d(n) > d.

The maximum of |x-y| over a product of two convex polygons is attained at a vertex
pair, so the adjacency test is the exact integer comparison in `geom`.

THE SEARCH decides "alpha(G_L) >= n?" exactly and completely.  A "tile" is a dyadic
cell of the coarsest level jt whose side is < 2; every tile is a clique of G_L, so it
holds at most one point.  State: a global candidate bitset C, a set of tiles already
declared OCCUPIED (with their point not yet located), and the cells already placed.

  * TILE FORCING.  If the number of tiles still meeting C equals the number of points
    still to place, every one of them is occupied.  (Counting; sound.)
  * ACTIVE-REGION PROPAGATION.  For an occupied tile t with active region
    D_t = C & tile_t, every cell g conflicting with *every* cell of D_t is impossible:
    the point of t sits in some cell of D_t and would be within distance < 2 of g.
    So C &= ~ AND_{f in D_t} adj[f].  Run to fixpoint over all occupied tiles.
    The AND is evaluated over a dyadic *cover* of D_t (using precomputed
    AND-of-neighbourhood per dyadic subtree) when D_t is large, which under-estimates
    the kill set and is therefore sound.
  * HIERARCHICAL OCCUPANCY BOUND.  b(R) = 1 if R is a tile meeting C, else
    min(cap(R), sum of children); prune when b(root) < points remaining.  cap(R) is a
    sound capacity from Oler's inequality (`cited`) applied to the cell centroids.
  * BRANCHING.  Either declare the most constrained tile empty / occupied, or split
    the active region of an occupied tile along the dyadic tree (4 ways).  The product
    over tiles of sub-positions is never enumerated - that is the difference from
    experiments/circle-packing-bnb, which branched each cell independently.
"""

import time
from fractions import Fraction

from . import geom

INV_SQRT3_UP = Fraction(577351, 1000000)     # > 1/sqrt(3)
assert INV_SQRT3_UP ** 2 > Fraction(1, 3)


def oler_capacity(a, h):
    """Sound upper bound on the number of pairwise non-conflicting level-L cells
    (side h) inside an equilateral region of side a.

    Centroids of such cells lie in the region and are pairwise at distance
    >= 2 - 2h/sqrt(3) =: rho (circumradius of an equilateral triangle of side h is
    h/sqrt(3)).  Rescale by 2/rho and apply Oler: for m points at pairwise distance
    >= 2 in an equilateral triangle of side a', m <= a'^2/8 + 3a'/4 + 1.
    A rational OVER-estimate of 1/sqrt(3) under-estimates rho, which over-estimates
    the capacity: the safe direction."""
    if a < 2:
        return 1
    rho = 2 - 2 * h * INV_SQRT3_UP
    if rho <= 0:
        return None
    ap = 2 * a / rho
    return int(ap * ap / 8 + 3 * ap / 4 + 1)


class _Abort(Exception):
    pass


class Instance:
    def __init__(self, n, p, q, L, verbose=False):
        self.n, self.p, self.q, self.L = n, p, q, L
        self.d = Fraction(p, q)
        self.h = self.d / (1 << L)
        assert self.h < 2, "cell side must be < 2"
        self.M = 1 << (2 * L)
        if verbose:
            print(f"[build] n={n} d={p}/{q}={float(self.d):.6f} L={L} cells={self.M}",
                  flush=True)
        self.adj, self.cells, self.verts = geom.conflict_bitsets(L, p, q, progress=False)
        self.jt = geom.tile_level(p, q, L)
        assert self.jt is not None and self.jt <= L
        self.level_mask, self.level_anc, self.children = {}, {}, {}
        for j in range(L + 1):
            anc, nj = geom.ancestor_map(L, j)
            self.level_anc[j] = anc
            masks = [0] * nj
            for k in range(self.M):
                masks[anc[k]] |= 1 << k
            self.level_mask[j] = masks
        for j in range(L):
            a2, _ = geom.ancestor_map(j + 1, j)
            ch = [[] for _ in range(1 << (2 * j))]
            for k in range(1 << (2 * (j + 1))):
                ch[a2[k]].append(k)
            self.children[j] = ch
        self.cap = {}
        for j in range(L + 1):
            c = oler_capacity(self.d / (1 << j), self.h)
            cnt = 1 << (2 * (L - j))
            self.cap[j] = min(cnt if c is None else c, cnt)
        for j in range(L - 1, -1, -1):
            self.cap[j] = min(self.cap[j], 4 * self.cap[j + 1])
        self.capadj = {L: list(self.adj)}
        for j in range(L - 1, -1, -1):
            prev = self.capadj[j + 1]
            cur = []
            for kids in self.children[j]:
                acc = prev[kids[0]]
                for kk in kids[1:]:
                    acc &= prev[kk]
                cur.append(acc)
            self.capadj[j] = cur
        self.tiles = self.level_mask[self.jt]
        self.ntiles = len(self.tiles)
        # counters
        self.nodes = self.props = self.prop_rounds = 0
        self.killed = self.bound_prunes = self.count_prunes = self.forced = 0
        self.witness = None
        self._killcache = {}

    # ---------- capacity bound ----------
    def bound(self, C):
        b = [1 if (C & m) else 0 for m in self.tiles]
        for j in range(self.jt - 1, -1, -1):
            capj = self.cap[j]
            nb = []
            for kids in self.children[j]:
                s = b[kids[0]] + b[kids[1]] + b[kids[2]] + b[kids[3]]
                nb.append(capj if s > capj else s)
            b = nb
        return b[0]

    # ---------- active-region kill set ----------
    def killset(self, D, t):
        """AND over a dyadic cover of D of the conflict neighbourhoods.  Sound
        (a cover only shrinks the kill set); exact when D is small."""
        got = self._killcache.get(D)
        if got is not None:
            return got
        pc = D.bit_count()
        if pc <= 48:
            it, acc = D, None
            while it:
                b = it & -it
                f = b.bit_length() - 1
                acc = self.adj[f] if acc is None else (acc & self.adj[f])
                it ^= b
        else:
            nodes = [(self.jt, t)]
            while len(nodes) < 24:
                nxt = []
                grew = False
                for (j, idx) in nodes:
                    if j == self.L:
                        nxt.append((j, idx))
                        continue
                    kids = [c for c in self.children[j][idx] if D & self.level_mask[j + 1][c]]
                    if kids:
                        grew = True
                        nxt.extend((j + 1, c) for c in kids)
                    else:
                        nxt.append((j, idx))
                if not grew or len(nxt) > 96:
                    break
                nodes = nxt
            acc = None
            for (j, idx) in nodes:
                a = self.capadj[j][idx]
                acc = a if acc is None else (acc & a)
        if len(self._killcache) < 400000:
            self._killcache[D] = acc
        return acc

    # ---------- driver ----------
    def solve(self, node_budget=None, time_budget=None):
        self._t0 = time.time()
        self._nb, self._tb = node_budget, time_budget
        try:
            ok = self._node((1 << self.M) - 1, frozenset(), 0, [])
        except _Abort:
            return "unknown"
        return "sat" if ok else "unsat"

    def _tick(self):
        self.nodes += 1
        if self._nb is not None and self.nodes > self._nb:
            raise _Abort()
        if (self.nodes & 255) == 0 and self._tb is not None:
            if time.time() - self._t0 > self._tb:
                raise _Abort()

    def _node(self, C, occ, placed, chosen):
        """occ: frozenset of tiles declared occupied whose point is not yet located.
        placed: number of points already located.  chosen: their cells."""
        self._tick()
        need = self.n - placed
        if need == 0:
            self.witness = list(chosen)
            return True
        occ = set(occ)
        # ---------------- propagation to fixpoint ----------------
        while True:
            changed = False
            live = [t for t in range(self.ntiles) if C & self.tiles[t]]
            if len(live) < need:
                self.count_prunes += 1
                return False
            for t in occ:
                if not (C & self.tiles[t]):
                    return False
            if len(live) == need and len(occ) < need:
                occ = set(live)
                self.forced += 1
                changed = True
            for t in list(occ):
                D = C & self.tiles[t]
                if D == 0:
                    return False
                k = self.killset(D, t)
                self.props += 1
                if C & k:
                    self.killed += (C & k).bit_count()
                    C &= ~k
                    changed = True
            if not changed:
                break
            self.prop_rounds += 1
        if self.bound(C) < need:
            self.bound_prunes += 1
            return False
        # ---------------- branch ----------------
        if occ:
            # locate the point of the most constrained occupied tile
            t = min(occ, key=lambda x: (C & self.tiles[x]).bit_count())
            D = C & self.tiles[t]
            if D.bit_count() == 1:
                cell = (D & -D).bit_length() - 1
                nxt = C & ~self.adj[cell] & ~self.tiles[t]
                return self._node(nxt, frozenset(occ - {t}), placed + 1,
                                  chosen + [cell])
            j, idx = self._split_node(D, t)
            for c in self.children[j][idx]:
                sub = self.level_mask[j + 1][c]
                if D & sub:
                    if self._node(C & ~(self.tiles[t] & ~sub), frozenset(occ),
                                  placed, chosen):
                        return True
            return False
        # no occupied tile pending: decide occupancy of the most constrained live tile
        live = [t for t in range(self.ntiles) if C & self.tiles[t]]
        t = min(live, key=lambda x: (C & self.tiles[x]).bit_count())
        if len(live) > need:
            if self._node(C & ~self.tiles[t], frozenset(), placed, chosen):
                return True
        return self._node(C, frozenset({t}), placed, chosen)

    def _split_node(self, D, t):
        """Deepest dyadic node whose subtree still contains all of D."""
        j, idx = self.jt, t
        while j < self.L:
            kids = [c for c in self.children[j][idx] if D & self.level_mask[j + 1][c]]
            if len(kids) > 1:
                return j, idx
            j, idx = j + 1, kids[0]
        return j - 1, self.level_anc[j - 1][(D & -D).bit_length() - 1]
