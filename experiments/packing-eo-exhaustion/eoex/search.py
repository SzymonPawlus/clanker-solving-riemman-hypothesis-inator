"""Depth-first exact exhaustion: does T(d) admit n points at pairwise separation >= 2?

A **node** is a multiset of closed cells with positive multiplicities summing to ``n``.
Its meaning is: *there is a configuration of n points at separation >= 2 in the container,
together with an assignment of each point to one closed cell containing it, realising these
multiplicities.*  The root is "all n points in the container".

Every point of a parent cell lies in at least one of its four children (they are closed and
cover the parent), so distributing a parent's k points over the children in all
``C(k+3,3)`` ways is exhaustive: any configuration consistent with the parent is consistent
with at least one child node.  Therefore if every branch is refuted, no configuration exists.

Three refutation rules, each one-sided (it fires only when infeasibility is certain):

1. **pair**   two distinct cells whose maximum separation is < 2 cannot both be occupied.
2. **self**   a cell of side < 2 holds at most one point; more generally a cell holds at
              most ``capacity(side)`` points (``caps.py``).
3. **oler**   Oler's inequality applied to the convex hull of the occupied cells bounds
              the total number of points in the node (``oler.node_bound``).

Rule 3 is the structure-aware one and is what this directory adds over a plain geometric
branch and bound.  At the root it reproduces Oler's closed-form bound exactly, so a run
with ``--oler-hull`` never does worse than Oler.

Outcomes: ``proved`` (no configuration exists, so d(n) > d), ``unresolved`` (a node
survived with every cell already at ``max_level``: nothing is proved), ``timeout``
(budget exhausted: nothing is proved; the remaining DFS stack is checkpointed).
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from fractions import Fraction

from .caps import capacity
from .lattice import UP, Cell, children, pair_compatible, side_fraction
from .oler import node_bound

Node = tuple[tuple[Cell, int], ...]


def _compositions(k: int, caps: tuple[int, int, int, int]):
    """All (k0,k1,k2,k3) >= 0 summing to k with ki <= caps[i]."""
    for a in range(min(k, caps[0]) + 1):
        ra = k - a
        for b in range(min(ra, caps[1]) + 1):
            rb = ra - b
            lo = max(0, rb - caps[3])
            for c in range(lo, min(rb, caps[2]) + 1):
                yield (a, b, c, rb - c)


@dataclass
class Result:
    status: str
    nodes: int
    elapsed: float
    frontier: list = field(default_factory=list)
    witness: Node | None = None


class Prover:
    def __init__(
        self,
        n: int,
        d: Fraction,
        max_level: int,
        max_cited: int = 15,
        use_oler_caps: bool = True,
        use_oler_hull: bool = True,
        oler_hull_max_level: int = 3,
        symmetry: bool = True,
    ) -> None:
        self.n = n
        self.d = Fraction(d)
        self.max_level = max_level
        self.max_cited = max_cited
        self.use_oler_caps = use_oler_caps
        self.use_oler_hull = use_oler_hull
        # The per-node hull rule costs a convex hull per candidate child.  Measured
        # (README §4.5) it removes ~23% of nodes and costs ~6x per node, so it is a net
        # loss when applied everywhere.  Applying it only near the root -- where cells
        # are large, the hull is cheap and the test is informative -- keeps the useful
        # part.  It is a pruning rule, so restricting where it fires can only lose
        # pruning, never soundness.
        self.oler_hull_max_level = oler_hull_max_level
        self.symmetry = symmetry
        self._pair_cache: dict[tuple[Cell, Cell], bool] = {}
        self._cap_cache: dict[int, int] = {}
        # Oler needs conv(E) to be a Jordan polygon; the collinear escape clause of
        # oler.py requires d < 2*(n-1).  Checked, never assumed.
        self.oler_ok = self.d < 2 * (n - 1)
        if not self.oler_ok:
            raise ValueError(
                f"Oler hull rule needs d < 2*(n-1) to exclude collinear E; got d={d}, n={n}"
            )

    # ---------------------------------------------------------------- primitives
    def cap(self, level: int) -> int:
        c = self._cap_cache.get(level)
        if c is None:
            c = capacity(
                side_fraction(self.d, level),
                self.n,
                max_cited=self.max_cited,
                use_oler=self.use_oler_caps,
            )
            self._cap_cache[level] = c
        return c

    def compatible(self, c1: Cell, c2: Cell) -> bool:
        key = (c1, c2) if c1 <= c2 else (c2, c1)
        v = self._pair_cache.get(key)
        if v is None:
            v = pair_compatible(key[0], key[1], self.d)
            self._pair_cache[key] = v
        return v

    # ------------------------------------------------------------------- the DFS
    def run(self, time_limit: float | None = None, node_limit: int | None = None,
            initial_stack: list[Node] | None = None) -> Result:
        t0 = time.monotonic()
        root: Node = (((0, UP, 0, 0), self.n),)
        stack: list[Node] = list(initial_stack) if initial_stack is not None else [root]
        # A supplied stack is re-validated: every node must be a node of *this* search.
        for nd in stack:
            self._validate(nd)
        nodes = 0
        # Root check: Oler's closed form is exactly the hull rule applied to the
        # container.  It is unconditional (it costs one hull of one cell), so NO run of
        # this prover is ever weaker than Oler's inequality.
        if initial_stack is None and node_bound([(0, UP, 0, 0)], self.d) < self.n:
            return Result("proved", 1, time.monotonic() - t0, [])
        while stack:
            node = stack.pop()
            nodes += 1
            if node_limit is not None and nodes > node_limit:
                stack.append(node)
                return Result("timeout", nodes - 1, time.monotonic() - t0, stack)
            if time_limit is not None and (nodes & 1023) == 0:
                if time.monotonic() - t0 > time_limit:
                    stack.append(node)
                    return Result("timeout", nodes, time.monotonic() - t0, stack)

            # pick a cell of minimal level (largest cell); tie-break on multiplicity
            idx = min(range(len(node)), key=lambda t: (node[t][0][0], -node[t][1]))
            cell, mult = node[idx]
            if cell[0] >= self.max_level:
                return Result("unresolved", nodes, time.monotonic() - t0, stack, node)

            rest = node[:idx] + node[idx + 1 :]
            kids = children(cell)
            kid_cap = self.cap(kids[0][0])
            caps = (kid_cap, kid_cap, kid_cap, kid_cap)

            is_root_split = cell[0] == 0 and self.symmetry
            for comp in _compositions(mult, caps):
                if is_root_split:
                    # D3 acts on the three level-1 corner cells up(0,0), up(1,0), up(0,1)
                    # as the full S3 (the middle cell down(0,0) is fixed), so every
                    # configuration has an image with non-increasing corner multiplicities.
                    if not (comp[0] >= comp[1] >= comp[2]):
                        continue
                occ = [(kids[t], comp[t]) for t in range(4) if comp[t] > 0]
                if not self._ok(occ, rest):
                    continue
                stack.append(tuple(rest) + tuple(occ))
            # falls through: node fully expanded (possibly to nothing)
        return Result("proved", nodes, time.monotonic() - t0, [])

    def _ok(self, occ: list[tuple[Cell, int]], rest: tuple[tuple[Cell, int], ...]) -> bool:
        """Do the newly created cells survive the pair and Oler rules?"""
        m = len(occ)
        for a in range(m):
            ca, ma = occ[a]
            if ma >= 2 and side_fraction(self.d, ca[0]) < 2:
                return False
            for b in range(a + 1, m):
                if not self.compatible(ca, occ[b][0]):
                    return False
            for cb, _ in rest:
                if not self.compatible(ca, cb):
                    return False
        if self.use_oler_hull:
            cells = [c for c, _ in rest] + [c for c, _ in occ]
            if max(c[0] for c in cells) <= self.oler_hull_max_level:
                if node_bound(cells, self.d) < self.n:
                    return False
        return True

    # ------------------------------------------------------------- checkpointing
    def _validate(self, node: Node) -> None:
        if not node:
            raise ValueError("empty node")
        total = 0
        seen = set()
        for cell, mult in node:
            L, orient, i, j = cell
            if not (0 <= L <= self.max_level) or orient not in (0, 1) or mult <= 0:
                raise ValueError(f"malformed cell {cell}")
            m = 1 << L
            ok = (0 <= i and 0 <= j and i + j <= m - 1) if orient == 0 else (
                0 <= i and 0 <= j and i + j <= m - 2
            )
            if not ok:
                raise ValueError(f"cell {cell} is not a cell of this container")
            if cell in seen:
                raise ValueError(f"duplicate cell {cell}")
            seen.add(cell)
            total += mult
        if total != self.n:
            raise ValueError(f"node multiplicities sum to {total}, not n={self.n}")


def frontier_digest(frontier: list[Node]) -> str:
    h = hashlib.sha256()
    for node in frontier:
        h.update(json.dumps(node, sort_keys=True, separators=(",", ":")).encode())
        h.update(b"|")
    return h.hexdigest()
