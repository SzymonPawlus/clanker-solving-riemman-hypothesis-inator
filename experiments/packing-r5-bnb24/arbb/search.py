"""Active-region branch and bound for the decision problem

    "do n points at pairwise distance >= 2 fit in the closed equilateral triangle
     T_d of side d = p/q ?"

A UNSAT verdict means d(n) > d.  A SAT verdict means only that *this relaxation*
cannot refute d; it is not a packing.

Relaxation.  Fix the level-L dyadic subdivision of T_d into 4^L closed cells that
cover T_d.  Any n points at pairwise distance >= 2 give n cells (one containing each
point).  The cells are distinct whenever the cell side h = d/2^L is < 2, and any two
of them have maximum separation >= 2.  So a packing yields an independent set of
size n in the conflict graph G_L (cells adjacent iff their max separation is < 2),
and

        alpha(G_L) < n   ==>   no packing at side d   ==>   d(n) > d.

Everything below decides "alpha(G_L) >= n?" exactly.

Three ingredients, and the first two are what the repo's earlier dyadic B&B
(experiments/circle-packing-bnb) did not have:

 1. ACTIVE-REGION PROPAGATION.  A node of the search knows that some tile (a dyadic
    cell of side < 2, hence holding at most one point) is occupied, and knows a
    dyadic sub-region "node" of it in which that point lies.  Every cell g that
    conflicts with *every* cell of that sub-region is then impossible and is deleted
    globally.  The AND-of-neighbourhoods over a whole dyadic subtree is precomputed
    once (`capadj`), so this costs one bitset AND.

 2. HIERARCHICAL OCCUPANCY / AREA BOUND.  Every dyadic cell R carries a precomputed
    capacity cap(R) >= (max independent set of G_L inside R).  The bound of a node is
    computed bottom-up over the dyadic tree,
        b(R) = 1                                     if side(R) < 2 and R meets C
        b(R) = min( cap(R), sum of b over children ) otherwise,
    and the node is pruned when b(root) < (points still to place).  This is the
    area-reduction signal: as propagation empties sub-regions, b drops.

 3. TILE-STRUCTURED BRANCHING.  Branch on one tile at a time: either it is empty, or
    it is occupied and we refine the point's position down the dyadic tree, running
    (1) at every refinement step.  The product over tiles of sub-positions is never
    enumerated.

Soundness of cap(R): the centroids of an independent set of level-L cells inside R
lie in R and are pairwise at distance >= 2 - 2h/sqrt(3) (circumradius of an
equilateral triangle of side h is h/sqrt(3)).  Rescaling by 2/rho and applying Oler's
inequality (`cited`; see attacks/oler-lower-bound/) to the equilateral triangle of
side a' = 2a/rho gives  #points <= a'^2/8 + 3a'/4 + 1.  A rational OVER-estimate of
1/sqrt(3) is used so rho is under-estimated and the capacity over-estimated, which is
the safe direction.  cap(R) = 1 whenever side(R) < 2 needs no Oler at all.
"""

from fractions import Fraction

import numpy as np

from . import geom

INV_SQRT3_UP = Fraction(577351, 1000000)   # > 1/sqrt(3) = 0.5773502691...
assert INV_SQRT3_UP ** 2 > Fraction(1, 3)


def oler_capacity(a, h):
    """Sound upper bound on the number of level-L cells (side h) inside an
    equilateral region of side a that can be pairwise non-conflicting."""
    if a < 2:
        return 1
    rho = 2 - 2 * h * INV_SQRT3_UP
    if rho <= 0:
        return None                      # no bound from this device
    ap = 2 * a / rho
    val = ap * ap / 8 + 3 * ap / 4 + 1
    return int(val)                      # floor


class Instance:
    def __init__(self, n, p, q, L, verbose=False):
        self.n, self.p, self.q, self.L = n, p, q, L
        self.d = Fraction(p, q)
        self.h = self.d / (1 << L)
        assert self.h < 2, "cell side must be < 2 so a cell holds at most one point"
        self.M = 1 << (2 * L)
        if verbose:
            print(f"[build] n={n} d={p}/{q}={float(self.d):.6f} L={L} cells={self.M}",
                  flush=True)
        self.adj, self.cells, self.verts = geom.conflict_bitsets(L, p, q, progress=verbose)
        self.jt = geom.tile_level(p, q, L)
        assert self.jt is not None
        # dyadic level masks
        self.level_mask = {}
        self.level_anc = {}
        for j in range(0, L + 1):
            anc, nj = geom.ancestor_map(L, j)
            self.level_anc[j] = anc
            masks = [0] * nj
            for k in range(self.M):
                masks[anc[k]] |= 1 << k
            self.level_mask[j] = masks
        # child lists
        self.children = {}
        for j in range(0, L):
            a2, n2 = geom.ancestor_map(j + 1, j)
            ch = [[] for _ in range(1 << (2 * j))]
            for k in range(1 << (2 * (j + 1))):
                ch[a2[k]].append(k)
            self.children[j] = ch
        # capacities
        self.cap = {}
        for j in range(0, L + 1):
            a = self.d / (1 << j)
            c = oler_capacity(a, self.h)
            cnt = 1 << (2 * (L - j))
            if c is None:
                c = cnt
            self.cap[j] = min(c, cnt)
        # tighten downward: cap(level j) <= 4 * cap(level j+1)
        for j in range(L - 1, -1, -1):
            self.cap[j] = min(self.cap[j], 4 * self.cap[j + 1])
        # AND-of-neighbourhood over each dyadic subtree
        self.capadj = {L: list(self.adj)}
        for j in range(L - 1, -1, -1):
            prev = self.capadj[j + 1]
            cur = []
            for idx, kids in enumerate(self.children[j]):
                acc = prev[kids[0]]
                for kk in kids[1:]:
                    acc &= prev[kk]
                cur.append(acc)
            self.capadj[j] = cur
        self.tiles = self.level_mask[self.jt]
        self.nodes = 0
        self.props = 0
        self.prop_killed = 0
        self.bound_prunes = 0
        self.witness = None

    # ---------------- bound ----------------
    def bound(self, C):
        """Hierarchical occupancy/area upper bound on the size of an independent set
        contained in the candidate set C."""
        jt = self.jt
        b = [1 if (C & m) else 0 for m in self.level_mask[jt]]
        for j in range(jt - 1, -1, -1):
            capj = self.cap[j]
            nb = []
            for kids in self.children[j]:
                s = b[kids[0]] + b[kids[1]] + b[kids[2]] + b[kids[3]]
                nb.append(s if s < capj else capj)
            b = nb
        return b[0]

    # ---------------- search ----------------
    def solve(self, node_budget=None, time_budget=None):
        import time
        self._t0 = time.time()
        self._node_budget = node_budget
        self._time_budget = time_budget
        self._aborted = False
        try:
            full = (1 << self.M) - 1
            r = self._solve(full, self.n, [])
        except _Abort:
            return "unknown"
        if self._aborted:
            return "unknown"
        return "sat" if r else "unsat"

    def _check_budget(self):
        import time
        self.nodes += 1
        if self._node_budget is not None and self.nodes > self._node_budget:
            self._aborted = True
            raise _Abort()
        if (self.nodes & 1023) == 0 and self._time_budget is not None:
            if time.time() - self._t0 > self._time_budget:
                self._aborted = True
                raise _Abort()

    def _solve(self, C, k, chosen):
        """Is there an independent set of size k inside C (using at most one cell per
        tile, which is automatic)?"""
        self._check_budget()
        if k == 0:
            self.witness = list(chosen)
            return True
        avail = [t for t, m in enumerate(self.tiles) if C & m]
        if len(avail) < k:
            self.bound_prunes += 1
            return False
        if self.bound(C) < k:
            self.bound_prunes += 1
            return False
        # most-constrained tile
        best, bestc = -1, None
        for t in avail:
            c = (C & self.tiles[t]).bit_count()
            if bestc is None or c < bestc:
                best, bestc = t, c
        t = best
        # branch A: tile t empty
        if len(avail) > k:
            if self._solve(C & ~self.tiles[t], k, chosen):
                return True
        # branch B: tile t occupied
        return self._refine(C, k, self.jt, t, chosen)

    def _refine(self, C, k, j, idx, chosen):
        """The point of tile (jt,t) lies in dyadic node (j, idx).  Propagate, then
        split."""
        self._check_budget()
        mask = self.level_mask[j][idx]
        dom = C & mask
        if dom == 0:
            return False
        # ---- active-region propagation ----
        pc = dom.bit_count()
        if dom == mask:
            kill = self.capadj[j][idx]
        elif pc <= 64:
            it = dom
            kill = None
            while it:
                b = it & -it
                f = b.bit_length() - 1
                kill = self.adj[f] if kill is None else (kill & self.adj[f])
                it ^= b
        else:
            kill = self.capadj[j][idx]
        self.props += 1
        Cp = C & ~kill
        self.prop_killed += (C & kill).bit_count()
        Cp |= dom                       # the point itself lives in dom
        if self.bound(Cp) < k:
            self.bound_prunes += 1
            return False
        if j == self.L:
            # a leaf dyadic node is a single cell
            b = dom & -dom
            cell = b.bit_length() - 1
            nxt = Cp & ~self.adj[cell] & ~self.tiles[self.level_anc[self.jt][cell]]
            return self._solve(nxt, k - 1, chosen + [cell])
        for ch in self.children[j][idx]:
            if Cp & self.level_mask[j + 1][ch]:
                if self._refine(Cp, k, j + 1, ch, chosen):
                    return True
        return False


class _Abort(Exception):
    pass
