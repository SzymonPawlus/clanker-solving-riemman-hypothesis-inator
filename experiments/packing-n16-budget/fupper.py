"""Certified UPPER bound on

    f(l) = sup{ area(S) : diam(S) <= 1, S subset {y >= 0}, (0,0) in S, (l,0) in S }.

Independent reimplementation (n16-budget lane) of the slab relaxation described in
attacks/n16-covering-limit/ Sec.3.  Nothing is imported from that lane's code; the
LP is re-derived here, its dual is written out explicitly, and weak duality is the
only thing relied on, checked in exact rational arithmetic.

DERIVATION (re-derived here, not inherited)
  Replacing S by the closed convex hull of its closure raises area, preserves
  diam <= 1, the half-plane and the two points.  So assume S compact convex.
  Slice S_y = [alpha(y), beta(y)], width w(y) = beta(y)-alpha(y), y in [0,H].
  (i)   A=(0,0), B=(l,0) in S_0 => alpha(0) <= 0, beta(0) >= l.  Every x in S is
        within 1 of A and of B, so beta(y) <= sqrt(1-y^2) (distance to A) and
        alpha(y) >= l - sqrt(1-y^2) (distance to B):
            w(y) <= 2 sqrt(1-y^2) - l.
  (ii)  w(y) <= diam(S) <= 1.
  (iii) The apex (at height H) is within 1 of A and of B, so H <= sqrt(1-l^2/4).
  (iv)  For y, y' the cross pairs (beta(y), alpha(y')) and (beta(y'), alpha(y))
        are both at distance <= 1, and (beta(y)-alpha(y'))^2 + (y-y')^2 <= 1 etc.,
        so beta(y)-alpha(y') <= sqrt(1-(y-y')^2) and symmetrically; adding,
            w(y) + w(y') <= 2 sqrt(1-(y-y')^2).
        (Needs BOTH slices non-empty -- hence the loop over the slab containing H.)
  area(S) = int_0^H w.  Cut [0, Hmax] into N slabs of thickness d = Hmax/N.  Let m
  be the index of the slab containing H, and W_j = sup{w(y) : y in slab j, y <= H}
  for j = 0..m (each such set is non-empty).  Then
        area(S) <= d * sum_{j=0}^m W_j,
        W_j <= ub_j := min(1, 2 sqrt(1-(j d)^2) - l)         [(i),(ii); w decreasing
                                                              majorant at slab's foot]
        W_j + W_k <= C_{k-j-1} := min(2, 2 sqrt(1-((k-j-1) d)^2))  for j < k  [(iv)]
  which is a linear program in W.  Maximising over m covers every possible H.

  LP_m:  max d * sum_j W_j   s.t.  W_j <= ub_j;  W_j + W_k <= C_{k-j-1};  W >= 0.
  Dual:  min sum_j u_j ub_j + sum_{j<k} z_{jk} C_{k-j-1}
         s.t.  u_j + sum_{k != j} z_{{j,k}} >= d  for every j;  u, z >= 0.
  Weak duality (the only thing used):
      d sum_j W_j <= sum_j (u_j + sum_k z) W_j
                   = sum_j u_j W_j + sum_{j<k} z_{jk} (W_j + W_k)
                  <= sum_j u_j ub_j + sum_{j<k} z_{jk} C_{k-j-1}.
  So ANY exactly-verified dual-feasible (u,z) is a rigorous upper bound; scipy is
  used only to propose one, and its proposal is rounded up, repaired and checked
  in Fractions.  A wrong LP solve can only make the certificate weaker, not wrong.
"""
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog

from exact import PI_HI, asin_lo, sqrt_hi, sqrt_lo

RDEN = 10 ** 9          # denominator used when rationalising scipy's dual proposal


def _data(ell, N):
    """Exact rational slab data (all UPPER bounds)."""
    ell = F(ell)
    hmax = sqrt_hi(1 - ell * ell / 4)
    d = hmax / N
    ub = []
    for j in range(N):
        y = j * d
        v = 2 * sqrt_hi(max(F(0), 1 - y * y)) - ell
        ub.append(max(F(0), min(F(1), v)))
    C = []
    for g in range(N):
        t = g * d
        C.append(F(0) if t >= 1 else min(F(2), 2 * sqrt_hi(1 - t * t)))
    return d, ub, C


def _dual_value(d, ub, C, n, u, z):
    """Exact value of a dual point, after checking exact dual feasibility."""
    row = list(u)
    for (j, k), q in z.items():
        row[j] += q
        row[k] += q
    for j in range(n):
        assert u[j] >= 0
        assert row[j] >= d, "dual infeasible"
    for q in z.values():
        assert q >= 0
    val = sum((u[j] * ub[j] for j in range(n)), F(0))
    val += sum((q * C[k - j - 1] for (j, k), q in z.items()), F(0))
    return val


def _lp_m(d, ub, C, m):
    """Certified upper bound on LP_m via an exactly verified dual point."""
    n = m + 1
    if n == 1:
        return d * ub[0]
    rows, rhs, meta = [], [], []
    for j in range(n):
        r = np.zeros(n)
        r[j] = 1.0
        rows.append(r)
        rhs.append(float(ub[j]))
        meta.append(("u", j, j))
    for j in range(n):
        for k in range(j + 1, n):
            r = np.zeros(n)
            r[j] = 1.0
            r[k] = 1.0
            rows.append(r)
            rhs.append(float(C[k - j - 1]))
            meta.append(("z", j, k))
    res = linprog(-np.full(n, float(d)), A_ub=np.array(rows), b_ub=np.array(rhs),
                  bounds=[(0, None)] * n, method="highs")
    if res.status != 0:
        # fall back to the trivial dual u_j = d (always feasible)
        return sum((d * ub[j] for j in range(n)), F(0))
    duals = -res.ineqlin.marginals
    u = [F(0)] * n
    z = {}
    for val, (tag, j, k) in zip(duals, meta):
        if val <= 0:
            continue
        q = F(int(-(-val * RDEN // 1)), RDEN)      # round UP to a rational
        if tag == "u":
            u[j] += q
        else:
            z[(j, k)] = z.get((j, k), F(0)) + q
    # repair to exact dual feasibility by topping up u (u_j pays ub_j >= 0)
    row = list(u)
    for (j, k), q in z.items():
        row[j] += q
        row[k] += q
    for j in range(n):
        if row[j] < d:
            u[j] += d - row[j]
    return _dual_value(d, ub, C, n, u, z)


def slab_bound(ell, N=64):
    """Certified rational upper bound on f(ell) from the slab LP."""
    d, ub, C = _data(ell, N)
    best = F(0)
    pref = [F(0)] * (N + 1)
    for j in range(N):
        pref[j + 1] = pref[j] + d * ub[j]
    for m in range(N):
        if pref[m + 1] <= best:          # trivial dual already loses: skip the LP
            continue
        b = _lp_m(d, ub, C, m)
        if b > best:
            best = b
    return best


def analytic_bound(ell):
    """f(l) <= int_0^h (2 sqrt(1-y^2) - l) dy = pi/2 - asin(l/2) - l*h/2,
    h = sqrt(1 - l^2/4).  Concave in l (derivative -sqrt(1-l^2/4)); exact at l=1,
    where it equals pi/3 - sqrt3/4, the area of B(A,1) cap B(B,1) cap {y>=0}."""
    ell = F(ell)
    return PI_HI / 2 - asin_lo(ell / 2) - ell * sqrt_lo(1 - ell * ell / 4) / 2


def f_upper(ell, N=64):
    """min of: isodiametric pi/4, the integrated slice bound, the slab LP."""
    ell = F(ell)
    return min(PI_HI / 4, analytic_bound(ell), slab_bound(ell, N))


if __name__ == "__main__":
    import sys
    from exact import PI_LO, SQRT3_HI
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    lens = PI_LO / 3 - SQRT3_HI / 4          # exact f(1), rounded DOWN
    print(f"N = {N} slabs;   pi/4 = {float(PI_HI/4):.7f}")
    for num, den in ((0, 1), (1, 4), (13, 20), (9, 10), (95, 100), (1, 1)):
        ell = F(num, den)
        a, s = analytic_bound(ell), slab_bound(ell, N)
        print(f"  f({float(ell):.4f}) <= {float(min(PI_HI/4,a,s)):.7f}"
              f"    [analytic {float(a):.7f}, lp {float(s):.7f}]")
    print(f"  sanity: f(1) is exactly pi/3-sqrt3/4 = {float(lens):.7f};"
          f" every certified upper bound must be >= it")
