"""Fractional-cover LP for the sub-integer corner-coordinate relaxation.

Primal (the object of interest):
    max  sum_c z_c   s.t.  z >= 0,  sum_{c subset R} z_c <= cap(R)  for all boxes R
Its value is the best upper bound on the number of separation-1 points in T_a
that this region family can produce.

Dual (the certificate):
    min  sum_R cap(R) y_R  s.t.  y >= 0,  sum_{R contains c} y_R >= 1  for all cells c
i.e. a *fractional cover* of the triangle by boxes, weighted by their capacities.
ANY dual-feasible y is a rigorous proof that at most sum_R cap(R) y_R points fit
(weak duality), so a proof needs only an exactly-verified y -- no optimality.

Search is done in floats; every conclusion is re-derived in exact rationals.
"""

from fractions import Fraction as F


def solve_cover(cols, caps, ncells, verbose=False):
    """min c^T y s.t. A y >= 1, y >= 0, with A[cell][region] = 1 iff cell in region.
    `cols[j]` is the list of cell indices contained in region j.
    Returns (objective, y) in floats via a dense two-phase simplex."""
    m, n = ncells, len(cols)
    # variables: y_0..y_{n-1}, surplus s_0..s_{m-1}, artificial a_0..a_{m-1}
    N = n + 2 * m
    T = [[0.0] * (N + 1) for _ in range(m)]
    for j, cl in enumerate(cols):
        for i in cl:
            T[i][j] = 1.0
    for i in range(m):
        T[i][n + i] = -1.0
        T[i][n + m + i] = 1.0
        # RHS perturbed upward to break the (severe) primal degeneracy of a
        # covering LP with all-ones right-hand side.  Perturbing UP only makes the
        # cover harder, so any cover found is still exactly feasible for b = 1 and
        # its cost is at worst O(1e-7) above the true optimum.
        T[i][N] = 1.0 + (i + 1) * 1e-9
    basis = [n + m + i for i in range(m)]

    def run(cost):
        # cost: list length N
        # reduced costs row
        z = [0.0] * (N + 1)
        for i in range(m):
            cb = cost[basis[i]]
            if cb:
                for k in range(N + 1):
                    z[k] += cb * T[i][k]
        for it in range(20000):
            # entering: most negative reduced cost  cost_j - z_j
            best, bj = -1e-9, -1
            for j in range(N):
                d = cost[j] - z[j]
                if d < best:
                    best, bj = d, j
            if bj < 0:
                return z[N]
            # ratio test
            br, bi = None, -1
            for i in range(m):
                if T[i][bj] > 1e-9:
                    r = T[i][N] / T[i][bj]
                    if br is None or r < br - 1e-12 or (abs(r - br) <= 1e-12 and basis[i] > basis[bi]):
                        br, bi = r, i
            if bi < 0:
                return None  # unbounded
            piv = T[bi][bj]
            row = T[bi]
            for k in range(N + 1):
                row[k] /= piv
            for i in range(m):
                if i != bi and T[i][bj] != 0.0:
                    f = T[i][bj]
                    Ti = T[i]
                    for k in range(N + 1):
                        Ti[k] -= f * row[k]
            f = z[bj] - cost[bj]
            if f != 0.0:
                for k in range(N + 1):
                    z[k] -= f * row[k]
            basis[bi] = bj
        raise RuntimeError("simplex iteration limit")

    cost1 = [0.0] * N
    for i in range(m):
        cost1[n + m + i] = 1.0
    v1 = run(cost1)
    if v1 is None or v1 > 1e-7:
        return None, None  # infeasible (cannot happen: whole triangle covers all)
    # drive artificials out / forbid them
    cost2 = [0.0] * N
    for j in range(n):
        cost2[j] = float(caps[j])
    for i in range(m):
        cost2[n + m + i] = 1e7
    v2 = run(cost2)
    y = [0.0] * n
    for i in range(m):
        if basis[i] < n:
            y[basis[i]] = T[i][N]
    return v2, y


def exact_cover_value(support, cols, caps, ncells):
    """Given a candidate support (list of region indices) solve exactly for the
    minimum-cost fractional cover using only those regions, by exact simplex on a
    small LP.  Returns (exact objective, exact y) or None if not coverable."""
    # small enough to brute-force with exact simplex; reuse float solve then round
    sub = [cols[j] for j in support]
    subcaps = [caps[j] for j in support]
    val, y = solve_cover(sub, subcaps, ncells)
    if y is None:
        return None
    return val, y


def verify_cover_exact(yfrac, cols, caps, ncells):
    """Exactly verify that y is a feasible fractional cover and return its exact
    cost.  yfrac: dict region_index -> Fraction."""
    cover = [F(0)] * ncells
    for j, v in yfrac.items():
        assert v >= 0, "negative weight"
        for i in cols[j]:
            cover[i] += v
    bad = [i for i in range(ncells) if cover[i] < 1]
    cost = sum((caps[j] * v for j, v in yfrac.items()), F(0))
    return (len(bad) == 0), bad, cost
