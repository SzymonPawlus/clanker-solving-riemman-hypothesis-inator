"""The corner-occupancy relaxation, built exactly.

For n = T(k)-1 unit-separated points in T of side a < k-1 we build an integer
feasibility system whose variables count points per corner-coordinate cell:

    z[alpha,beta,gamma] = #{ p : floor(u_A)=alpha, floor(u_B)=beta, floor(u_C)=gamma }

Constraints, all of them consequences of the true geometric system:

  (T)   sum z = n
  (C-j) sum_{alpha < j} z >= T(j)          -- Prover A's CIO contrapositive
  (K-j) sum_{alpha < j} z <= N(j^-)        -- capacity of the OPEN corner triangle
  (B)   sum_{cells in box} z <= cap(box)   -- capacity of every corner-coordinate box,
                                              cap computed by Oler on that convex region
                                              (and by the cited N table when the box is
                                              an equilateral triangle)

If this system is FEASIBLE then no argument using only corner occupancy plus region
capacity can refute a k-counterexample.  Erdos-Oler is `cited`-true for k <= 6, so
feasibility at k = 6 is a proof that the relaxation is too weak, full stop.
"""

from fractions import Fraction as F
import geom as G


def tri(m):
    return m * (m + 1) // 2


def oler(a):
    return F(a) * F(a) / 2 + 3 * F(a) / 2 + 1


def build(k, a, use_lower_eo=True):
    """Return (cells, cellcap, constraints, info).  a is a Fraction with a < k-1."""
    a = F(a)
    n = tri(k) - 1
    J = int(a)                      # floor(a) = k-2 in the range of interest
    assert J == k - 2, (J, k)
    assert oler(a) - n < 1, "a must be below k-1 so that eps(a) < 1"
    # circularity guard: never use d(T(k)-1) = k-1, the statement under test.
    G.EXCLUDE = {n}
    if not use_lower_eo:
        # additionally drop every Erdos-Oler value at lower levels (d(T(m)-1)),
        # leaving only Oler's triangular values and the non-EO optimality results
        for m in range(2, k):
            G.EXCLUDE.add(tri(m) - 1)
    base = G.tri_constraints(a)

    # ---- cells -----------------------------------------------------------
    cells = []
    for al in range(J + 1):
        for be in range(J + 1):
            for ga in range(J + 1):
                cons = list(base)
                for c, lo in ((0, al), (1, be), (2, ga)):
                    cons += G.bound_constraints(a, c, lo, lo + 1)
                vs = G.vertices(cons)
                if not vs:
                    continue
                # half-open cell non-empty?  test the centroid of the closed cell
                cx = sum(p[0] for p in vs) / len(vs)
                cy = sum(p[1] for p in vs) / len(vs)
                cz = 2 * a - cx - cy
                if not (al <= cx < al + 1 and be <= cy < be + 1 and ga <= cz < ga + 1):
                    continue
                cells.append((al, be, ga))
    idx = {c: i for i, c in enumerate(cells)}

    cellcap = []
    for (al, be, ga) in cells:
        cons = list(base)
        for c, lo in ((0, al), (1, be), (2, ga)):
            cons += G.bound_constraints(a, c, lo, lo + 1)
        cellcap.append(G.capacity(a, cons))

    # ---- constraints -----------------------------------------------------
    cons_list = []   # (name, [cell indices], lo, hi)  meaning lo <= sum <= hi

    cons_list.append(("total", list(range(len(cells))), n, n))

    for V in range(3):
        for j in range(1, J + 1):
            members = [i for i, c in enumerate(cells) if c[V] < j]
            lo = tri(j)                       # CIO
            hi = G.N_upper_open(j)            # capacity of the open corner triangle
            cons_list.append(("corner%d_j%d" % (V, j), members, lo, hi))

    # ---- box capacities --------------------------------------------------
    boxes = []
    rng = [(l, h) for l in range(J + 1) for h in range(l + 1, J + 2)]
    for (lA, hA) in rng:
        for (lB, hB) in rng:
            for (lC, hC) in rng:
                members = [i for i, c in enumerate(cells)
                           if lA <= c[0] < hA and lB <= c[1] < hB and lC <= c[2] < hC]
                if not members:
                    continue
                naive = min(n, sum(cellcap[i] for i in members))
                if naive == 0:
                    continue
                cons = list(base)
                cons += G.bound_constraints(a, 0, lA, hA)
                cons += G.bound_constraints(a, 1, lB, hB)
                cons += G.bound_constraints(a, 2, lC, hC)
                cap = G.capacity(a, cons)
                if cap < naive:                       # only keep binding constraints
                    boxes.append(((lA, hA, lB, hB, lC, hC), members, cap))
    for (b, members, cap) in boxes:
        cons_list.append(("box%s" % (b,), members, 0, cap))

    info = dict(n=n, J=J, a=a, ncells=len(cells), nbox=len(boxes),
                eps=oler(a) - n, cellcap=cellcap, cells=cells)
    return cells, cellcap, cons_list, info


# ---------------------------------------------------------------- ILP search


def feasible(cells, cellcap, cons_list, n, node_limit=4_000_000):
    """DFS for an integer point of the system.  Returns (z, nodes) or (None, nodes)."""
    m = len(cells)
    ub = list(cellcap)
    # tighten single-cell upper bounds from the constraints
    for (_, mem, lo, hi) in cons_list:
        if len(mem) == 1:
            ub[mem[0]] = min(ub[mem[0]], hi)

    # constraints touching each cell, for incremental checking
    cons = [(mem_set, lo, hi, sorted(mem)) for (_, mem, lo, hi) in
            [(nm, mem, lo, hi) for (nm, mem, lo, hi) in cons_list]
            for mem_set in [set(mem)]]

    # order cells so that heavily-constrained ones come first
    order = sorted(range(m), key=lambda i: -ub[i])
    pos = {c: p for p, c in enumerate(order)}
    # for each constraint precompute, in the DFS order, the last position it touches
    prepared = []
    for (mem_set, lo, hi, mem) in cons:
        last = max(pos[i] for i in mem)
        prepared.append((mem_set, lo, hi, last, sum(ub[i] for i in mem)))

    by_last = [[] for _ in range(m)]
    for c in prepared:
        by_last[c[3]].append(c)

    cur = [0] * m
    nodes = [0]

    # suffix capacity for the total constraint
    suffix = [0] * (m + 1)
    for p in range(m - 1, -1, -1):
        suffix[p] = suffix[p + 1] + ub[order[p]]

    def partial_ok(p):
        """check constraints fully determined at position p, and prune on the rest"""
        for (mem_set, lo, hi, last, capsum) in by_last[p]:
            s = sum(cur[i] for i in mem_set)
            if s < lo or s > hi:
                return False
        # prune: any constraint whose remaining cells cannot bring it up to lo
        for (mem_set, lo, hi, last, capsum) in prepared:
            if lo == 0:
                continue
            s = 0
            rem = 0
            for i in mem_set:
                if pos[i] <= p:
                    s += cur[i]
                else:
                    rem += ub[i]
            if s + rem < lo:
                return False
            if s > hi:
                return False
        return True

    total_lo = n

    def rec(p, placed):
        nodes[0] += 1
        if nodes[0] > node_limit:
            raise TimeoutError
        if p == m:
            return placed == n
        i = order[p]
        hi = min(ub[i], n - placed)
        for v in range(hi, -1, -1):
            cur[i] = v
            if placed + v + suffix[p + 1] < n:
                cur[i] = 0
                return False        # v only decreases from here
            if partial_ok(p):
                if rec(p + 1, placed + v):
                    return True
        cur[i] = 0
        return False

    try:
        ok = rec(0, 0)
    except TimeoutError:
        return "timeout", nodes[0]
    return (list(cur) if ok else None), nodes[0]
