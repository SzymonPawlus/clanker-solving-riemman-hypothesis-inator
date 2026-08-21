"""Exact geometry for the sub-integer corner-coordinate relaxation (Erdos-Oler).

NORMALISATION (asserted, not inherited): Oler normalisation throughout --
minimum separation 1, containing equilateral triangle T of side `a`.
The repo's certificates use separation 2 and side d = 2a; anything loaded from
`results/` is halved on load (see controls.py).

Corner coordinates.  With A=(0,0), B=(a,0), C=(a/2, a*sqrt3/2),

    u_A = x + y/sqrt3,  u_B = (a-x) + y/sqrt3,  u_C = a - 2y/sqrt3,
    u_A + u_B + u_C = 2a          (Viviani)

and Delta_V(t) = {u_V <= t} is the closed corner triangle of side t at V.

Two facts make everything below exact rational arithmetic, with no sqrt(3):

  (1) squared distance.  Inverting, x = u_A - (a-u_C)/2, y = (sqrt3/2)(a-u_C), so
      dx = du_A + du_C/2, dy = -(sqrt3/2) du_C and

          d^2 = du_A^2 + du_A*du_C + du_C^2 .

  (2) Oler's terms.  The map (u_A,u_C) -> (x,y) has |Jacobian| = sqrt3/2, so
      (2/sqrt3)*Area_xy = Area_(u_A,u_C) = plain shoelace area in u-coordinates.
      Every edge of a corner-coordinate box has one u_V constant, and for such an
      edge d^2 collapses to the square of a single coordinate difference, so its
      Euclidean length equals that difference.  Hence

          Oler(R) = (2/sqrt3)A + P/2 + 1 = shoelace_u(R) + perim_u(R)/2 + 1

      is exactly rational.  Checked against the whole triangle: shoelace = a^2/2,
      perimeter = 3a, giving a^2/2 + 3a/2 + 1.  [Oler 1961, `cited`.]
"""

from fractions import Fraction as F
from itertools import combinations

# ---------------------------------------------------------------- polygons

def d2(p, q):
    """Exact squared Euclidean distance between two points given as (u_A,u_C)."""
    s = p[0] - q[0]
    t = p[1] - q[1]
    return s * s + s * t + t * t


def polygon(total, lo, hi):
    """Vertices of {v : sum v = total, lo[V] <= v[V] <= hi[V]} in (v_A, v_C).

    Returned counter-clockwise-ordered (orientation fixed by |shoelace|), or []
    if the region is empty or lower-dimensional.
    """
    # half-planes  n . (vA,vC) <= c
    H = [((-1, 0), -lo[0]), ((1, 0), hi[0]),          # v_A
         ((0, -1), -lo[2]), ((0, 1), hi[2]),          # v_C
         ((1, 1), total - lo[1]), ((-1, -1), hi[1] - total)]  # v_B = total-vA-vC
    pts = []
    for (n1, c1), (n2, c2) in combinations(H, 2):
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if det == 0:
            continue
        x = F(c1 * n2[1] - c2 * n1[1], 1) / det
        y = F(n1[0] * c2 - n2[0] * c1, 1) / det
        if all(n[0] * x + n[1] * y <= c for n, c in H):
            if (x, y) not in pts:
                pts.append((x, y))
    if len(pts) < 3:
        return pts
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)

    def ang(p):
        dx, dy = p[0] - cx, p[1] - cy
        # half-plane key then cross-product comparison, all exact
        return (0 if (dy > 0 or (dy == 0 and dx > 0)) else 1, )

    def cmpkey(p):
        dx, dy = p[0] - cx, p[1] - cy
        half = 0 if (dy > 0 or (dy == 0 and dx > 0)) else 1
        return (half, dx, dy)

    import functools

    def cmp(p, q):
        dxp, dyp = p[0] - cx, p[1] - cy
        dxq, dyq = q[0] - cx, q[1] - cy
        hp = 0 if (dyp > 0 or (dyp == 0 and dxp > 0)) else 1
        hq = 0 if (dyq > 0 or (dyq == 0 and dxq > 0)) else 1
        if hp != hq:
            return -1 if hp < hq else 1
        cr = dxp * dyq - dyp * dxq
        if cr > 0:
            return -1
        if cr < 0:
            return 1
        return 0

    pts.sort(key=functools.cmp_to_key(cmp))
    return pts


def shoelace(pts):
    if len(pts) < 3:
        return F(0)
    s = F(0)
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def isqrt_exact(q):
    """Exact square root of a nonnegative Fraction, or None if irrational."""
    from math import isqrt
    n, d = q.numerator, q.denominator
    rn, rd = isqrt(n), isqrt(d)
    if rn * rn == n and rd * rd == d:
        return F(rn, rd)
    return None


def perimeter(pts):
    """Exact perimeter.  Every edge of a corner-coordinate box is axis-parallel in
    one of the three corner coordinates, so its length is rational; we assert it."""
    if len(pts) < 2:
        return F(0)
    p = F(0)
    for i in range(len(pts)):
        r = isqrt_exact(d2(pts[i], pts[(i + 1) % len(pts)]))
        assert r is not None, "non-rational edge length: region is not a corner box"
        p += r
    return p


def diam2(pts):
    return max((d2(p, q) for p, q in combinations(pts, 2)), default=F(0))


# ---------------------------------------------------------------- capacities

def oler_cap(pts, mu):
    """floor( Oler(R) ) for the polygon, where mu = separation measured in the
    same length unit as the coordinates.  Rigorous upper bound on the number of
    mu-separated points in the convex region R.   Oler (1961), `cited`."""
    A = shoelace(pts) / (mu * mu)
    P = perimeter(pts) / mu
    val = A + P / 2 + 1
    return int(val)  # Fraction -> floor for positive val


def _fine_cells(total, lo, hi, eta):
    """Cover the region by closed grid cells of the triangular grid of step eta
    (aligned to the region's own lower bounds).  Returns list of vertex-lists.
    Each cell has diameter <= eta, so eta < mu forces <=1 point per cell."""
    import math
    idx = []
    rng = []
    for V in range(3):
        n0 = 0
        n1 = int((hi[V] - lo[V]) / eta)
        if lo[V] + n1 * eta < hi[V]:
            n1 += 1
        rng.append(range(n0, max(n1, 1)))
    cells = []
    for jA in rng[0]:
        for jB in rng[1]:
            for jC in rng[2]:
                clo = [lo[V] + (jA, jB, jC)[V] * eta for V in range(3)]
                chi = [min(clo[V] + eta, hi[V]) for V in range(3)]
                clo = [max(clo[V], lo[V]) for V in range(3)]
                if any(clo[V] > chi[V] for V in range(3)):
                    continue
                if sum(clo) > total or sum(chi) < total:
                    continue
                # unclipped cell (valid, and a superset of the clipped one)
                ulo = [lo[V] + (jA, jB, jC)[V] * eta for V in range(3)]
                uhi = [ulo[V] + eta for V in range(3)]
                pts = polygon(total, ulo, uhi)
                if len(pts) >= 1:
                    cells.append(pts)
    return cells


def _greedy_clique_cover(n, adj):
    """Upper bound on max independent set: partition into cliques greedily."""
    remaining = (1 << n) - 1
    k = 0
    while remaining:
        v = (remaining & -remaining).bit_length() - 1
        clique = 1 << v
        cand = adj[v] & remaining & ~(1 << v)
        while cand:
            w = (cand & -cand).bit_length() - 1
            clique |= 1 << w
            cand &= adj[w]
            cand &= ~(1 << w)
        remaining &= ~clique
        k += 1
    return k


def _mis(n, adj, budget=[0]):
    """Exact maximum independent set by branch and bound (clique-cover bound)."""
    best = [0]

    def rec(cand, size):
        budget[0] -= 1
        if budget[0] < 0:
            raise TimeoutError
        if cand == 0:
            if size > best[0]:
                best[0] = size
            return
        # bound
        verts = []
        m = cand
        while m:
            v = (m & -m).bit_length() - 1
            verts.append(v)
            m &= m - 1
        loc = {v: i for i, v in enumerate(verts)}
        k = len(verts)
        ladj = [0] * k
        for v in verts:
            mm = adj[v] & cand
            b = 0
            while mm:
                w = (mm & -mm).bit_length() - 1
                b |= 1 << loc[w]
                mm &= mm - 1
            ladj[loc[v]] = b
        ub = _greedy_clique_cover(k, ladj)
        if size + ub <= best[0]:
            return
        # branch on max-degree vertex
        v = max(verts, key=lambda x: bin(adj[x] & cand).count("1"))
        # include v
        rec(cand & ~adj[v] & ~(1 << v), size + 1)
        # exclude v
        rec(cand & ~(1 << v), size)

    rec((1 << n) - 1, 0)
    return best[0]


def grid_cap(total, lo, hi, mu, eta, max_cells=260, node_budget=400000):
    """Rigorous upper bound on the number of mu-separated points in the region,
    by covering it with grid cells of diameter eta < mu and taking a maximum
    independent set of the 'can be >= mu apart' graph.

    Validity: each closed cell has diameter eta < mu, so holds at most one point
    of a mu-separated set (assign boundary points to one cell); if two cells have
    max mutual distance < mu they cannot both be occupied.  Hence the occupied
    cells form an independent set.  Returns None if the instance is too big."""
    if eta >= mu:
        return None
    cells = _fine_cells(total, lo, hi, eta)
    n = len(cells)
    if n == 0:
        return 0
    if n > max_cells:
        return None
    mu2 = mu * mu
    adj = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            mx = max(d2(p, q) for p in cells[i] for q in cells[j])
            if mx < mu2:                      # cannot both be occupied
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    try:
        return _mis(n, adj, [node_budget])
    except TimeoutError:
        return _greedy_clique_cover(n, adj)


def capacity(total, lo, hi, mu, extra_etas=(), max_cells=400):
    """cap(R): rigorous upper bound on the number of mu-separated points in the
    corner box R = {lo <= u <= hi} inside the triangle.  The minimum of

      * the diameter test          (diam < mu  =>  cap = 1),
      * Oler's inequality          [Oler 1961, `cited`],
      * self-similar subdivision / independent-set bounds at step D/m, where D is
        the region's own scale -- this is the mechanism that is strictly stronger
        than Oler on small regions, and it is the whole budget of this attack.

    NO value of d(n) from the literature table enters here (kill-criterion K2)."""
    pts = polygon(total, lo, hi)
    if not pts:
        return 0, "empty"
    if len(pts) < 3:
        return 1, "degenerate"
    if diam2(pts) < mu * mu:
        return 1, "diameter"
    best = oler_cap(pts, mu)
    why = "oler"
    d = disk_cap(pts, mu)
    if d < best:
        best, why = d, "disk"
    s = star_cap(pts, mu)
    if s < best:
        best, why = s, "star"
    D = max(min(hi[V] - lo[V], total - sum(lo)) for V in range(3))
    etas = []
    for m in range(2, 13):
        e = D / m
        if e < mu:
            etas.append(e)
            if len(etas) >= 4:
                break
    etas.extend(e for e in extra_etas if e < mu)
    for eta in etas:
        if eta <= 0:
            continue
        g = grid_cap(total, lo, hi, mu, eta, max_cells=max_cells)
        if g is not None and g < best:
            best, why = g, "grid(eta=%s)" % eta
    return best, why


# ------------------------------------------------- circumradius (disk) bound
#
# Lemma D (derived here, elementary).  Let 2 <= m <= 6 points be pairwise at
# distance >= 1 inside a closed disk of radius rho, centre O.  Sort them by polar
# angle about O; some angular gap satisfies Delta <= 2*pi/m.  For that pair, with
# radii r_i, r_j <= rho and c = cos(2*pi/m),
#     |P_iP_j|^2 = r_i^2 - 2 c r_i r_j + r_j^2  <=  rho^2 * max(1, 2-2c) = rho^2*(2-2c)
# (the last equality because c <= 1/2 for m >= 3, and for m = 2 directly).  Hence
#     1 <= rho * 2 sin(pi/m),   i.e.   rho >= 1 / (2 sin(pi/m)).
# Contrapositive, used as a capacity bound:  rho < 1/(2 sin(pi/m))  =>  cap <= m-1.
# Tight: the regular m-gon inscribed in that circle attains it.  In particular a
# region of circumradius < 1 has capacity at most 5.
#
# Exactness: all comparisons are done as  rho^2 * (2 - 2 cos(2 pi/m)) < mu^2  with
# 2-2cos(2pi/m) in {4, 3, 2, (5-sqrt5)/2, 1} for m = 2,3,4,5,6; only m = 5 is
# irrational and it is compared via its exact minimal polynomial bound below.

def _mec(pts):
    """Minimum enclosing circle of the points in the (v_A,v_C) chart, returned as
    (centre, squared radius) with the metric d2.  Exact rational arithmetic:
    in coordinates X = vA + vC/2, Y = vC the form is X^2 + (3/4) Y^2."""
    P = [(p[0] + p[1] / 2, p[1]) for p in pts]

    def q(u, v):
        dx = u[0] - v[0]
        dy = u[1] - v[1]
        return dx * dx + F(3, 4) * dy * dy

    best = None
    cands = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            cands.append(((P[i][0] + P[j][0]) / 2, (P[i][1] + P[j][1]) / 2))
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            for k in range(j + 1, len(P)):
                a, b, c = P[i], P[j], P[k]
                # solve q(c,a)=q(c,b)=q(c,cc) linear system
                a1 = 2 * (b[0] - a[0]); b1 = F(3, 2) * (b[1] - a[1])
                c1 = (b[0]**2 - a[0]**2) + F(3, 4) * (b[1]**2 - a[1]**2)
                a2 = 2 * (c[0] - a[0]); b2 = F(3, 2) * (c[1] - a[1])
                c2 = (c[0]**2 - a[0]**2) + F(3, 4) * (c[1]**2 - a[1]**2)
                det = a1 * b2 - a2 * b1
                if det == 0:
                    continue
                cands.append(((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det))
    for cc in cands:
        r2 = max(q(cc, p) for p in P)
        if best is None or r2 < best[1]:
            best = (cc, r2)
    return best


def disk_cap(pts, mu):
    """cap bound from Lemma D.  Returns an integer upper bound (>=1)."""
    if len(pts) < 2:
        return 1
    _, rho2 = _mec(pts)
    mu2 = mu * mu
    # m = 2,3,4,6 : 2-2cos(2pi/m) = 4, 3, 2, 1  (exact rationals)
    for m, fac in ((2, F(4)), (3, F(3)), (4, F(2))):
        if rho2 * fac < mu2:
            return m - 1
    # m = 5 : 2-2cos(72deg) = (5 - sqrt5)/2 = 1.3819660...;  rho2*fac < mu2
    # <=> 2*rho2*(5) ... use exact algebraic test: fac = (5-sqrt5)/2, so
    # rho2*fac < mu2  <=>  (5-sqrt5)*rho2 < 2*mu2  <=>  5*rho2 - 2*mu2 < sqrt5*rho2
    lhs = 5 * rho2 - 2 * mu2
    if lhs < 0 or lhs * lhs < 5 * rho2 * rho2:
        return 4
    if rho2 < mu2:
        return 5
    return 10 ** 9


# ------------------------------------------------- centroid star cover
#
# Any convex polygon is covered by the m pieces  conv(g, m_{i-1}, p_i, m_i),
# g the centroid of the vertices and m_i the edge midpoints.  If every piece has
# diameter < mu the polygon has capacity at most m.  For an equilateral triangle
# of side t the three pieces are kites of diameter t/sqrt3, which gives the exact
# threshold cap <= 3 for t < sqrt3 -- the case a plain grid cover misses.

def star_cap(pts, mu):
    m = len(pts)
    if m < 3:
        return 10 ** 9
    gx = sum(p[0] for p in pts) / m
    gy = sum(p[1] for p in pts) / m
    g = (gx, gy)
    mids = [((pts[i][0] + pts[(i + 1) % m][0]) / 2,
             (pts[i][1] + pts[(i + 1) % m][1]) / 2) for i in range(m)]
    mu2 = mu * mu
    for i in range(m):
        piece = [g, mids[i - 1], pts[i], mids[i]]
        if diam2(piece) >= mu2:
            return 10 ** 9
    return m
