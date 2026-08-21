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


def _dedupe(cons_list):
    """Merge constraints that share a member set; drop nothing else."""
    best = {}
    for (nm, mem, lo, hi) in cons_list:
        key = frozenset(mem)
        if key in best:
            onm, olo, ohi = best[key]
            best[key] = (onm, max(olo, lo), min(ohi, hi))
        else:
            best[key] = (nm, lo, hi)
    return [(nm, sorted(k), lo, hi) for k, (nm, lo, hi) in best.items()]


def _prepare(cells, cellcap, cons_list):
    m = len(cells)
    cl = _dedupe(cons_list)
    ub = list(cellcap)
    for (_, mem, lo, hi) in cl:
        if len(mem) == 1:
            ub[mem[0]] = min(ub[mem[0]], hi)
    C = len(cl)
    lo_c = [c[2] for c in cl]
    hi_c = [c[3] for c in cl]
    mem_c = [c[1] for c in cl]
    cons_of = [[] for _ in range(m)]
    for ci in range(C):
        for i in mem_c[ci]:
            cons_of[i].append(ci)
    return ub, C, lo_c, hi_c, mem_c, cons_of


def feasible(cells, cellcap, cons_list, n, node_limit=20_000_000):
    """Exhaustive DFS with incremental constraint state.

    Returns (z, nodes) with z a feasible integer point, None if the system is
    infeasible, or the string 'timeout' if the node limit was hit first.
    """
    m = len(cells)
    ub, C, lo_c, hi_c, mem_c, cons_of = _prepare(cells, cellcap, cons_list)

    # branch on the most constrained cells first
    tight = [10 ** 9] * m
    for ci in range(C):
        cap_sum = sum(ub[i] for i in mem_c[ci])
        slack = hi_c[ci] - cap_sum
        for i in mem_c[ci]:
            tight[i] = min(tight[i], slack)
    order = sorted(range(m), key=lambda i: (tight[i], -ub[i]))

    suffix = [0] * (m + 1)
    for p in range(m - 1, -1, -1):
        suffix[p] = suffix[p + 1] + ub[order[p]]

    cur = [0] * m
    cur_sum = [0] * C
    rem_cap = [sum(ub[i] for i in mem_c[ci]) for ci in range(C)]
    nodes = [0]

    def rec(p, placed):
        nodes[0] += 1
        if nodes[0] > node_limit:
            raise TimeoutError
        if p == m:
            return placed == n
        i = order[p]
        cs = cons_of[i]
        top = min(ub[i], n - placed)
        for ci in cs:
            t = hi_c[ci] - cur_sum[ci]
            if t < top:
                top = t
        if top < 0:
            return False
        for ci in cs:
            rem_cap[ci] -= ub[i]
        try:
            for v in range(top, -1, -1):
                if placed + v + suffix[p + 1] < n:
                    return False            # smaller v is only worse
                ok = True
                for ci in cs:
                    cur_sum[ci] += v
                for ci in cs:
                    if cur_sum[ci] + rem_cap[ci] < lo_c[ci]:
                        ok = False
                        break
                if ok:
                    cur[i] = v
                    if rec(p + 1, placed + v):
                        return True
                    cur[i] = 0
                for ci in cs:
                    cur_sum[ci] -= v
            return False
        finally:
            for ci in cs:
                rem_cap[ci] += ub[i]

    try:
        ok = rec(0, 0)
    except TimeoutError:
        return "timeout", nodes[0]
    return (list(cur) if ok else None), nodes[0]


def find_feasible_random(cells, cellcap, cons_list, n, tries=4000, seed=20260821):
    """Randomised-restart DFS.  Finds a feasible integer point fast when one exists;
    proves nothing when it fails."""
    import random
    rnd = random.Random(seed)
    m = len(cells)
    cl = _dedupe(cons_list)
    ub = list(cellcap)
    for (_, mem, lo, hi) in cl:
        if len(mem) == 1:
            ub[mem[0]] = min(ub[mem[0]], hi)
    C = len(cl)
    lo_c = [c[2] for c in cl]
    hi_c = [c[3] for c in cl]
    mem_c = [c[1] for c in cl]
    cons_of = [[] for _ in range(m)]
    for ci in range(C):
        for i in mem_c[ci]:
            cons_of[i].append(ci)

    for t in range(tries):
        order = list(range(m))
        rnd.shuffle(order)
        cur = [0] * m
        cur_sum = [0] * C
        rem_cap = [sum(ub[i] for i in mem_c[ci]) for ci in range(C)]
        placed = 0
        ok = True
        for p, i in enumerate(order):
            top = min(ub[i], n - placed)
            for ci in cons_of[i]:
                top = min(top, hi_c[ci] - cur_sum[ci])
            if top < 0:
                ok = False
                break
            # bias towards filling: pick a value near the top, sometimes lower
            v = top if rnd.random() < 0.7 else rnd.randint(0, max(top, 0))
            cur[i] = v
            placed += v
            for ci in cons_of[i]:
                cur_sum[ci] += v
                rem_cap[ci] -= ub[i]
                if cur_sum[ci] + rem_cap[ci] < lo_c[ci]:
                    ok = False
            if not ok:
                break
        if ok and placed == n:
            if not check_solution(cells, cons_list, cur):
                return cur, t
    return None, tries


def check_solution(cells, cons_list, z):
    """Independently re-verify a claimed feasible point against every constraint."""
    bad = []
    for (nm, mem, lo, hi) in cons_list:
        s = sum(z[i] for i in mem)
        if not (lo <= s <= hi):
            bad.append((nm, s, lo, hi))
    return bad
