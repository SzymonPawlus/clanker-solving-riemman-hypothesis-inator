"""Exact branch-and-bound refutation of

    P(n, t, strict):  n points in the CLOSED unit equilateral triangle T(1)
                      with all pairwise distances  > t   (strict=True)
                                              or  >= t   (strict=False).

Why this parameterisation (see attacks/r5-exhaust4/README.md sec.1).  A
configuration of n points at separation >= 1 in T(a) rescales by 1/a to n points
in T(1) at separation >= 1/a.  So

    "no n points at separation >= 1 in T(a)"        <=>  P(n, 1/a, strict=False)
    "no n points at separation >= 1 in T(a), ALL a < A"
                                                    <=>  P(n, 1/A, strict=True)

The second line is an argument UNIFORM in a, which is what
attacks/eo-exhaustion/ sec.1.2(a) says a finite computation must produce; a
family of fixed-rational-side runs never gets there (its sec.1.1).

All arithmetic is exact integer/rational.  No floats anywhere in a decision.
"""
import json
import time
from fractions import Fraction

from .caps import refutes_multiplicity
from . import geom


class Prover:
    def __init__(self, n, t, strict, max_level, use_oler=True, use_symmetry=True,
                 max_cited=8):
        self.n = n
        self.t = Fraction(t)
        self.strict = strict
        self.max_level = max_level
        self.use_symmetry = use_symmetry
        self.max_cited = max_cited
        self.LM = max_level                     # reference lattice level
        self.pow4 = 4 ** self.LM
        # Oler validity guard: conv(E) must not be degenerate.  Collinear points
        # at separation >= t span >= (n-1)t, exceeding the container diameter 1.
        self.oler_ok = (self.n - 1) * self.t > 1
        self.use_oler = use_oler and self.oler_ok
        self.oler_refused = use_oler and not self.oler_ok
        # integer threshold for the pair test
        self.num, self.den = self.t.numerator, self.t.denominator
        self.pair_rhs = self.num * self.num * self.pow4      # compare vs maxq*den^2
        self._vcache = {}
        self._pcache = {}
        self.nodes = 0
        self.survivor = None

    # ---- exact tests -----------------------------------------------------
    def verts(self, cell):
        v = self._vcache.get(cell)
        if v is None:
            v = geom.verts_at(cell, self.LM)
            self._vcache[cell] = v
        return v

    def pair_refutes(self, c1, c2):
        """maxsep(c1,c2)^2 = maxq / 4^LM.  Two distinct points in distinct closed
        cells are at distance <= maxsep, so:
          strict  : need maxsep > t  -> refute if maxsep <= t
          closed  : need maxsep >= t -> refute if maxsep <  t
        """
        key = (c1, c2) if c1 < c2 else (c2, c1)
        r = self._pcache.get(key)
        if r is None:
            q = geom.maxq(self.verts(c1), self.verts(c2))
            lhs = q * self.den * self.den
            r = (lhs <= self.pair_rhs) if self.strict else (lhs < self.pair_rhs)
            self._pcache[key] = r
        return r

    def cell_refutes(self, cell, m):
        h = Fraction(1, 1 << cell[0])
        return refutes_multiplicity(m, h, self.t, self.strict, self.max_cited)

    def oler_refutes(self, node):
        """Oler (1961), cited: for a finite E with pairwise distances >= 1 whose
        convex hull is a Jordan polygon, |E| <= (2/sqrt3)A + M/2 + 1.
        Rescaling by 1/t for separation >= t and relaxing conv(E) to the convex
        hull K of the occupied closed cells (A and M are monotone under
        inclusion of convex sets) gives

            n <= h^2 * S / t^2 + h * P / (2t) + 1,

        S = lattice-coordinate area of K, P = perimeter of K in units of
        h = 2^-LM.  The sqrt3 in the area cancels exactly; only P leaves Q and is
        over-estimated, which can only make the rule fire less often.

        Strict mode: separation > t means >= t+eps, and the bound is strictly
        decreasing in t, so `bound <= n` already refutes.
        """
        pts = []
        for cell, _m in node:
            pts.extend(self.verts(cell))
        hull = geom.convex_hull(pts)
        if len(hull) < 3:
            return False
        area2 = geom.hull_area2(hull)                      # 2 * lattice area
        per = geom.hull_perimeter_upper(hull)              # units of h
        t = self.t
        bound = (Fraction(area2, 2) / (self.pow4 * t * t)
                 + per / (Fraction(1 << self.LM) * 2 * t) + 1)
        return bound <= self.n if self.strict else bound < self.n

    def node_refuted(self, node):
        for cell, m in node:
            if self.cell_refutes(cell, m):
                return True
        k = len(node)
        for a in range(k):
            for b in range(a + 1, k):
                if self.pair_refutes(node[a][0], node[b][0]):
                    return True
        if self.use_oler and self.oler_refutes(node):
            return True
        return False

    # ---- branching -------------------------------------------------------
    @staticmethod
    def compositions(m):
        for a in range(m + 1):
            for b in range(m - a + 1):
                for c in range(m - a - b + 1):
                    yield (a, b, c, m - a - b - c)

    def branch(self, node):
        """Split a cell of minimal level (ties: largest multiplicity)."""
        idx = min(range(len(node)), key=lambda k: (node[k][0][0], -node[k][1]))
        cell, m = node[idx]
        kids = geom.children(cell)
        rest = node[:idx] + node[idx + 1:]
        at_root = (cell[0] == 0)
        for comp in self.compositions(m):
            if at_root and self.use_symmetry:
                # D3 permutes the three level-1 corner cells kids[0..2] as S3 and
                # fixes the middle cell kids[3]; so we may assume the corner
                # multiplicities are non-increasing.
                if not (comp[0] >= comp[1] >= comp[2]):
                    continue
            child = tuple(sorted(rest + tuple(
                (kids[i], comp[i]) for i in range(4) if comp[i] > 0)))
            yield child

    # ---- driver ----------------------------------------------------------
    def run_enumerate(self, node_limit=None, time_limit=None, checkpoint=None):
        """Do NOT stop at the first survivor: collect every max-level leaf that
        no rule refutes.  This is the finite reduction AF asks for -- the set of
        occupancy profiles that survive at resolution `max_level`."""
        t0 = time.time()
        root = ((geom.root_cell(), self.n),)
        survivors = []
        if self.node_refuted(root):
            return {"outcome": "proved", "survivors": [], "nodes": 1,
                    "seconds": round(time.time() - t0, 2)}
        stack = [root]
        while stack:
            node = stack.pop()
            self.nodes += 1
            if node_limit and self.nodes > node_limit:
                return {"outcome": "nodelimit", "survivors": survivors,
                        "nodes": self.nodes, "frontier": len(stack),
                        "seconds": round(time.time() - t0, 2)}
            if time_limit and (self.nodes & 1023) == 0 and time.time() - t0 > time_limit:
                return {"outcome": "timeout", "survivors": survivors,
                        "nodes": self.nodes, "frontier": len(stack),
                        "seconds": round(time.time() - t0, 2)}
            if min(c[0][0] for c in node) >= self.max_level:
                survivors.append(node)
                continue
            for child in self.branch(node):
                if not self.node_refuted(child):
                    stack.append(child)
            if checkpoint and (self.nodes & 65535) == 0:
                with open(checkpoint, "w") as f:
                    json.dump({"nodes": self.nodes, "frontier": len(stack),
                               "survivors": len(survivors),
                               "seconds": round(time.time() - t0, 1)}, f)
        return {"outcome": ("proved" if not survivors else "survivors"),
                "survivors": survivors, "nodes": self.nodes,
                "seconds": round(time.time() - t0, 2)}

    def run(self, node_limit=None, time_limit=None, checkpoint=None):
        t0 = time.time()
        root = ((geom.root_cell(), self.n),)
        if self.node_refuted(root):
            return self._res("proved", 1, t0)
        stack = [root]
        while stack:
            node = stack.pop()
            self.nodes += 1
            if node_limit and self.nodes > node_limit:
                return self._res("nodelimit", len(stack), t0, node)
            if time_limit and (self.nodes & 1023) == 0 and time.time() - t0 > time_limit:
                return self._res("timeout", len(stack), t0, node)
            if min(c[0][0] for c in node) >= self.max_level:
                # every cell at max level and nothing refuted it
                return self._res("unresolved", len(stack), t0, node)
            for child in self.branch(node):
                if not self.node_refuted(child):
                    stack.append(child)
            if checkpoint and (self.nodes & 65535) == 0:
                with open(checkpoint, "w") as f:
                    json.dump({"nodes": self.nodes, "frontier": len(stack),
                               "seconds": round(time.time() - t0, 1)}, f)
        return self._res("proved", 0, t0)

    def _res(self, outcome, frontier, t0, node=None):
        return {
            "outcome": outcome, "n": self.n, "t": str(self.t),
            "strict": self.strict, "max_level": self.max_level,
            "use_oler": self.use_oler, "oler_refused": self.oler_refused,
            "use_symmetry": self.use_symmetry, "max_cited": self.max_cited,
            "nodes": self.nodes, "frontier": frontier,
            "seconds": round(time.time() - t0, 2),
            "witness_node": [[list(c), m] for c, m in node] if node else None,
        }
