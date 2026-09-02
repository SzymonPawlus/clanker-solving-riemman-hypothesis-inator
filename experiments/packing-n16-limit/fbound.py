"""Certified upper bound for

    f(l) = sup { area(S) : diam(S) <= 1, S in the half-plane {y >= 0},
                 and S contains two points at distance l on the line y = 0 }.

This is the "edge piece" bound: a covering piece that meets an edge of T_a in a
trace of diameter l can contribute at most f(l) of area to T_a.

METHOD (all of it proved in the attack README, section "Lemma F"):

  WLOG S compact convex.  Let H = max height.  Slices S_y = [alpha(y), beta(y)]
  are non-empty intervals for y in [0,H], of width w(y).
    (a)  w(y) + w(y') <= 2*sqrt(1 - (y-y')^2)     [diameter, cross pairs]
    (b)  w(y) <= 2*sqrt(1 - y^2) - l              [(a) against the two edge points]
    (c)  H <= sqrt(1 - l^2/4)                     [apex within distance 1 of both]
  area(S) = int_0^H w.  Discretise [0, H_max] into N slabs; for each index m of
  the slab containing H, relax to a finite LP in the slab suprema.  The LP is
  solved numerically and then a RATIONAL DUAL CERTIFICATE is produced and checked
  in exact arithmetic, so the returned Fraction is a rigorous upper bound.

Nothing here uses any packing or covering value from the literature (K2).
"""
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

from exactconst import sqrt_hi, sqrt_lo, asin_lo, PI_HI

DEN = 10 ** 9   # denominator used when rationalising dual multipliers


def _constants(ell, N):
    """Rational data for the slab relaxation.  All values are UPPER bounds."""
    ell = F(ell)
    h = sqrt_hi(1 - ell * ell / 4)          # H <= h
    d = h / N                               # slab thickness
    ub = []
    for j in range(N):
        y = j * d
        val = 2 * sqrt_hi(max(F(0), 1 - y * y)) - ell
        val = min(val, F(1))                # width <= diam <= 1
        ub.append(max(F(0), val))
    # pair constants C[g] for a gap of g slabs between the two slabs (g = k-j-1)
    C = []
    for g in range(N):
        dist = g * d
        if dist >= 1:
            C.append(F(0))
        else:
            C.append(min(F(2), 2 * sqrt_hi(1 - dist * dist)))
    return d, ub, C


def _solve_m(d, ub, C, m):
    """Numerically solve the LP for 'top slab index = m'; return (value, duals)."""
    n = m + 1
    rows, rhs, meta = [], [], []
    for j in range(n):
        r = np.zeros(n); r[j] = 1.0
        rows.append(r); rhs.append(float(ub[j])); meta.append(('u', j))
    for j in range(n):
        for k in range(j + 1, n):
            r = np.zeros(n); r[j] = 1.0; r[k] = 1.0
            rows.append(r); rhs.append(float(C[k - j - 1])); meta.append(('z', j, k))
    c = -np.full(n, float(d))
    res = linprog(c, A_ub=np.array(rows), b_ub=np.array(rhs),
                  bounds=[(0, None)] * n, method='highs')
    assert res.status == 0, res.message
    duals = -res.ineqlin.marginals
    return -res.fun, duals, meta


def _certify(d, ub, C, m, duals, meta):
    """Rational dual certificate -> exact upper bound on the LP value."""
    n = m + 1
    u = [F(0)] * n
    z = {}
    for val, mt in zip(duals, meta):
        q = F(int(np.ceil(max(val, 0.0) * DEN)), DEN)
        if q == 0:
            continue
        if mt[0] == 'u':
            u[mt[1]] += q
        else:
            z[(mt[1], mt[2])] = z.get((mt[1], mt[2]), F(0)) + q
    # repair: every row must satisfy  u_j + sum_k z_{jk} >= d
    rowsum = list(u)
    for (j, k), q in z.items():
        rowsum[j] += q
        rowsum[k] += q
    for j in range(n):
        if rowsum[j] < d:
            u[j] += d - rowsum[j]
    # verify exactly
    rowsum = list(u)
    for (j, k), q in z.items():
        rowsum[j] += q
        rowsum[k] += q
    for j in range(n):
        assert rowsum[j] >= d, "dual infeasible after repair"
        assert u[j] >= 0
    bound = sum((u[j] * ub[j] for j in range(n)), F(0))
    bound += sum((q * C[k - j - 1] for (j, k), q in z.items()), F(0))
    return bound


def slab_bound(ell, N=32, verbose=False):
    """Certified rational upper bound on f(ell) from the slab LP alone."""
    ell = F(ell)
    d, ub, C = _constants(ell, N)
    best = F(0)
    for m in range(N):
        _, duals, meta = _solve_m(d, ub, C, m)
        b = _certify(d, ub, C, m, duals, meta)
        if b > best:
            best = b
            if verbose:
                print(f"  l={float(ell):.4f} m={m} bound={float(b):.6f}")
    return best


def analytic_bound(ell):
    """Certified upper bound from constraint (b) alone:

        f(l) <= int_0^h (2 sqrt(1-y^2) - l) dy = pi/2 - arcsin(l/2) - l*h/2,
        h = sqrt(1 - l^2/4).

    Exact at l = 1: the admissible region is then B(A,1) cap B(B,1) cap {y>=0},
    of area pi/3 - sqrt(3)/4 = 0.6141848...
    """
    ell = F(ell)
    return PI_HI / 2 - asin_lo(ell / 2) - ell * sqrt_lo(1 - ell * ell / 4) / 2


def f_upper(ell, N=32, verbose=False):
    """Certified rational upper bound on f(ell): the best of the three bounds.

      * pi/4              -- isodiametric (Bieberbach), `cited`
      * analytic_bound    -- constraint (b) integrated
      * slab_bound        -- the LP over vertical slabs
    """
    ell = F(ell)
    return min(PI_HI / 4, analytic_bound(ell), slab_bound(ell, N, verbose))


if __name__ == "__main__":
    import sys
    from exactconst import PI_HI
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    print(f"N = {N} slabs")
    print(f"  sanity: pi/4 = {float(PI_HI/4):.6f}  (f(0) must not exceed it materially)")
    for num in (0, 6, 12, 16, 20, 24):
        ell = F(num, 24)
        print(f"  f({float(ell):.4f}) <= {float(f_upper(ell, N)):.6f}"
              f"   [lp {float(slab_bound(ell, N)):.6f}, analytic {float(analytic_bound(ell)):.6f}]")
