"""Independent dicut / dijoin / tau toolkit for the tau = 2 write-up (issue #152).

Status of everything computed with this file: `numerical`.  Written from the definitions,
without reading experiments/woodalls-dicuts/ or experiments/woodall-zeroweight-census/ code
paths, per problems/woodalls-conjecture/RULES.md.  Pure standard library, deterministic.

Conventions (match attacks/tau2-complete/README.md):
  * A digraph is (n, arcs) with vertices 0..n-1 and arcs a list of (tail, head).
    Parallel arcs and antiparallel arcs are allowed; each arc is its own index.
  * For nonempty proper U (a bitmask), delta_out(U) = arcs with tail in U, head outside;
    delta_in(U) = arcs with tail outside, head in U.
  * A dicut is delta_out(U) for a nonempty proper U with delta_in(U) empty.  The EMPTY set
    counts as a dicut when it arises this way (weakly disconnected digraphs), so tau = 0 there.
  * A dijoin is an arc set meeting every dicut; a weight-respecting packing of dijoins is a
    family in which arc a lies in at most w(a) members.
"""
from __future__ import annotations
from itertools import product


def dicuts(n: int, arcs: list[tuple[int, int]]) -> dict[int, int]:
    """Map U (vertex bitmask) -> arc bitmask of delta_out(U), for every dicut shore U."""
    full = (1 << n) - 1
    out = {}
    for U in range(1, full):
        enters = False
        leaving = 0
        for i, (t, h) in enumerate(arcs):
            tin = (U >> t) & 1
            hin = (U >> h) & 1
            if hin and not tin:
                enters = True
                break
            if tin and not hin:
                leaving |= 1 << i
        if not enters:
            out[U] = leaving
    return out


def tau(n, arcs, w=None) -> int:
    """Minimum (weighted) dicut size; w defaults to all-ones. Returns a large sentinel if no dicut."""
    if w is None:
        w = [1] * len(arcs)
    best = None
    for U, C in dicuts(n, arcs).items():
        s = sum(w[i] for i in range(len(arcs)) if (C >> i) & 1)
        best = s if best is None or s < best else best
    return best if best is not None else 10 ** 9


def is_dijoin(n, arcs, J: set[int]) -> bool:
    Jm = 0
    for i in J:
        Jm |= 1 << i
    return all(C & Jm for C in dicuts(n, arcs).values())


def strong_components(n, arcs):
    """Return list mapping vertex -> component id (Kosaraju, small n)."""
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    for t, h in arcs:
        adj[t].append(h)
        radj[h].append(t)
    order, seen = [], [False] * n

    def dfs1(v):
        seen[v] = True
        for x in adj[v]:
            if not seen[x]:
                dfs1(x)
        order.append(v)
    for v in range(n):
        if not seen[v]:
            dfs1(v)
    comp = [-1] * n
    c = 0
    for v in reversed(order):
        if comp[v] != -1:
            continue
        stack = [v]
        comp[v] = c
        while stack:
            y = stack.pop()
            for x in radj[y]:
                if comp[x] == -1:
                    comp[x] = c
                    stack.append(x)
        c += 1
    return comp, c


def condensation(n, arcs):
    """(n', arcs', keep) where arcs' are the inter-component arcs, keep[i] = index in arcs' or None."""
    comp, c = strong_components(n, arcs)
    arcs2, keep = [], []
    for t, h in arcs:
        if comp[t] == comp[h]:
            keep.append(None)
        else:
            keep.append(len(arcs2))
            arcs2.append((comp[t], comp[h]))
    return c, arcs2, keep


def two_colourable_traces(traces: list[int], m: int) -> list[int] | None:
    """Find a 2-colouring of arcs 0..m-1 in which every trace (arc bitmask) sees both colours.
    Returns the colouring as a list of 0/1 or None.  Backtracking, fine for m <= ~20."""
    traces = [t for t in traces]
    col = [-1] * m

    def ok():
        for t in traces:
            seen0 = seen1 = False
            undecided = False
            for i in range(m):
                if (t >> i) & 1:
                    if col[i] == 0:
                        seen0 = True
                    elif col[i] == 1:
                        seen1 = True
                    else:
                        undecided = True
            if not undecided and not (seen0 and seen1):
                return False
        return True

    def rec(i):
        if i == m:
            return ok()
        for c in (0, 1):
            col[i] = c
            if ok() and rec(i + 1):
                return True
        col[i] = -1
        return False
    return list(col) if rec(0) else None


def two_packing_within(n, arcs, w) -> list[int] | None:
    """Two dijoins J0, J1 with J0 ∩ J1 = ∅ and both inside the weight-1 arcs (w in {0,1}), or None.
    Returned as a colouring of ALL arcs where weight-0 arcs get colour -1 (unused)."""
    ones = [i for i in range(len(arcs)) if w[i] == 1]
    idx = {a: k for k, a in enumerate(ones)}
    traces = []
    for C in dicuts(n, arcs).values():
        t = 0
        for i in ones:
            if (C >> i) & 1:
                t |= 1 << idx[i]
        traces.append(t)
    sub = two_colourable_traces(traces, len(ones))
    if sub is None:
        return None
    col = [-1] * len(arcs)
    for k, a in enumerate(ones):
        col[a] = sub[k]
    return col


def robbins_orientation(n, edges: list[tuple[int, int]]) -> list[tuple[int, int]] | None:
    """Ear-by-ear strong orientation of a connected bridgeless multigraph, exactly the
    constructive proof of Theorem R in the write-up.  Returns oriented edges (same index
    order) or None if the procedure gets stuck (which certifies a bridge or disconnection)."""
    m = len(edges)
    orient: list[tuple[int, int] | None] = [None] * m
    inH = [False] * n
    inH[0] = True
    while True:
        # pick an edge with at least one end in H and not yet oriented
        cand = None
        for i, (u, v) in enumerate(edges):
            if orient[i] is None and (inH[u] or inH[v]):
                cand = i
                break
        if cand is None:
            break
        u, v = edges[cand]
        if not inH[u]:
            u, v = v, u
        if inH[v]:
            orient[cand] = (u, v)      # chord (or loop / parallel edge): any direction
            continue
        # ear: path from v to H in G - e, using unoriented edges only
        prev = {v: None}
        stack = [v]
        hit = None
        while stack and hit is None:
            x = stack.pop()
            for j, (a, b) in enumerate(edges):
                if j == cand or orient[j] is not None:
                    continue
                if a == x or b == x:
                    y = b if a == x else a
                    if y not in prev:
                        prev[y] = (x, j)
                        if inH[y]:
                            hit = y
                            break
                        stack.append(y)
        if hit is None:
            return None                  # e would be a bridge
        orient[cand] = (u, v)
        inH[v] = True
        y = hit
        while prev[y] is not None:
            x, j = prev[y]
            orient[j] = (x, y)
            inH[x] = True
            y = x
    if any(o is None for o in orient):
        return None                      # disconnected
    return orient  # type: ignore


def strongly_connected(n, arcs) -> bool:
    _, c = strong_components(n, arcs)
    return c == 1


def robbins_split(n, arcs):
    """The construction of the write-up: orient the underlying multigraph strongly, colour each
    arc by agreement (0) / disagreement (1).  Returns (colouring, orientation)."""
    edges = [(t, h) for t, h in arcs]
    O = robbins_orientation(n, edges)
    if O is None:
        return None, None
    assert strongly_connected(n, O)
    col = [0 if O[i] == arcs[i] else 1 for i in range(len(arcs))]
    return col, O


def check_split(n, arcs, col) -> bool:
    """Every dicut sees both colours among arcs with colour 0/1 (colour -1 = unused)."""
    m0 = m1 = 0
    for i, c in enumerate(col):
        if c == 0:
            m0 |= 1 << i
        elif c == 1:
            m1 |= 1 << i
    return all((C & m0) and (C & m1) for C in dicuts(n, arcs).values())
