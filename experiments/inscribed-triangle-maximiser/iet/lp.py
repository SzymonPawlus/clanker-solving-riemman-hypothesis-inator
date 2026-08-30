"""An EXACT upper bound on the largest equilateral triangle that fits in a convex body,
by linear-programming duality with certificates in Q(sqrt 3).

Why this exists
===============
The `extremal-size` attack's headline -- that the disk is NOT the extremal convex body for
m(K)/w(K) -- rests on a FLOAT computation: the constant-width body with support function
h(theta) = 1 + cos(5 theta)/24 has w = 2 exactly and m ~ 1.714410, i.e. ratio ~ 0.857205
against the disk's sqrt3/2 ~ 0.866025.  Making that exact needs an upper bound on m for a
NON-polygonal body, which the polygon maximiser of `maximiser.py` cannot supply.  This module
supplies it, and it does so without assuming anything about where a maximal triangle's
vertices sit.

The chain, in full
==================
Write K for the body, T(u) for the equilateral triangle with vertices 0, u, rho u (rho =
rotation by +60 degrees), and note that every equilateral triangle with a positively oriented
labelling is  t + lambda T(u)  for a unit u and lambda > 0, with side lambda|u|.

(1) **Outer polygon.**  For any finite set of nonzero rational normals n_j,
        K  subset  Q = { x : <x, n_j> <= h_K(n_j) for all j },
    because h_K is exactly the support function.  Any rational UPPER bound c_j >= h_K(n_j)
    still gives K subset Q, so no tangency computation and no rounding argument is needed --
    the containment is免费.  For h(theta) = 1 + eps cos 5theta and n = (x,y),
        h_K(n) = |n| + eps * (x^5 - 10x^3y^2 + 5xy^4) / (x^2+y^2)^2,
    whose second term is exactly rational; only |n| needs an upper bound (`sqrt_upper`).

(2) **Every triangle inscribed in the boundary of K has its three vertices IN K**, hence in
    Q.  So m(K) <= M(Q) := sup{ side of an equilateral triangle contained in Q }.  This step
    is why no lemma about maximal triangles touching the boundary is needed anywhere.

(3) **Containment is a linear program.**  t + lambda T(u) subset Q  iff for every j
        <t,n_j> + lambda * m_j(u) <= c_j,      m_j(u) = max(0, <u,n_j>, <rho u, n_j>),
    (using lambda >= 0), because a half plane contains a triangle iff it contains its three
    vertices.  So M(Q) for the fixed direction u is |u| * lambda*(u) with
        lambda*(u) = max { lambda : exists t, <t,n_j> + lambda m_j <= c_j for all j }.

(4) **Weak duality gives an exact certificate.**  If y_i, y_j, y_k >= 0 satisfy
        y_i n_i + y_j n_j + y_k n_k = 0    and    y_i m_i + y_j m_j + y_k m_k = 1,
    then for every feasible (t, lambda),  lambda = sum y_r (<t,n_r> + lambda m_r) <= sum y_r
    c_r.  Cramer on that 3x3 system gives, with D = m_i X_i + m_j X_j + m_k X_k and
    X_i = cross(n_j,n_k), X_j = cross(n_k,n_i), X_k = cross(n_i,n_j),
        y_i = X_i / D,   y_j = X_j / D,   y_k = X_k / D,
        lambda*(u) <= (c_i X_i + c_j X_j + c_k X_k) / D           whenever all y_r >= 0.
    Every quantity here is in Q(sqrt 3) and every comparison is exact.  **The bound is valid
    for ANY triple with y >= 0** -- optimality of the triple affects only how tight it is, so
    the floating-point search that proposes triples cannot make a reported bound wrong.

(5) **From finitely many directions to all of them.**  Sample directions u_1..u_D (rational
    vectors) whose consecutive angular gaps are at most gamma, verified exactly by
    gamma_k <= tan gamma_k = cross(u_k,u_{k+1}) / dot(u_k,u_{k+1}) (valid while dot > 0).
    Let T be an equilateral triangle of side s contained in Q, of direction v.  Some sample
    u_k has angle(v, u_k) <= gamma/2.  Rotating T about its centroid by that angle moves each
    vertex by at most 2R sin(gamma/4) <= R gamma/2 with R = s/sqrt3 the circumradius, so the
    rotated triangle -- which has direction exactly u_k and the same side s -- is contained in
        Q_r = { x : <x,n_j> <= c_j + r |n_j| },      r = s_ub * gamma / (2 sqrt3),
    the outer parallel body of Q at distance r (again any rational upper bound on |n_j| is
    safe), where s_ub is any upper bound on s.  Hence
        M(Q)  <=  max_k  |u_k| * lambda*(Q_r, u_k)  <=  max_k |u_k| * (dual bound at u_k).
    Squaring keeps everything in Q(sqrt 3): the reported quantity is a bound on side^2.

s_ub is legitimate because s <= diam(Q) and Q is bounded by construction; the code recomputes
a rational diameter bound from the half planes and asserts s_ub is above it.

Floats appear only in `_best_triples`, which PROPOSES index triples.  Nothing it returns is
believed: each proposal is re-derived exactly and rejected unless y >= 0 holds exactly.
"""

from __future__ import annotations

import math
from fractions import Fraction

from .qs3 import Q3

__all__ = ["sqrt_upper", "sqrt_lower", "cw_support_bounds", "outer_halfplanes",
           "inflate", "erode_const", "dual_bound", "lambda_upper_at",
           "sample_directions", "max_gap_tan", "upper_bound", "feasible_lambda_lower"]


# ------------------------------------------------------------------ rational roots
def sqrt_upper(x: Fraction, prec: int = 10 ** 24) -> Fraction:
    """A rational UPPER bound for sqrt(x), x >= 0.  Exact by construction."""
    if x < 0:
        raise ValueError("sqrt of a negative rational")
    if x == 0:
        return Fraction(0)
    # sqrt(p/q) = sqrt(p q)/q; bound sqrt(p q) above by (isqrt(p q * prec^2) + 1)/prec.
    p, q = x.numerator, x.denominator
    n = p * q * prec * prec
    r = math.isqrt(n) + 1
    return Fraction(r, prec * q)


def sqrt_lower(x: Fraction, prec: int = 10 ** 24) -> Fraction:
    """A rational LOWER bound for sqrt(x), x >= 0."""
    if x < 0:
        raise ValueError("sqrt of a negative rational")
    if x == 0:
        return Fraction(0)
    p, q = x.numerator, x.denominator
    n = p * q * prec * prec
    r = math.isqrt(n)
    return Fraction(r, prec * q)


# ------------------------------------------------- the constant-width test body
def cw_support_bounds(n, eps=Fraction(1, 24)):
    """Rational (lower, upper) bounds for the support function of the body with
    h(theta) = 1 + eps*cos(5 theta), evaluated at the nonzero rational vector n.

        h_K(n) = |n| * (1 + eps cos 5theta) = |n| + eps * P(n) / (x^2+y^2)^2,
        P(n)   = x^5 - 10 x^3 y^2 + 5 x y^4     (so that cos 5theta = P/|n|^5).

    Only |n| is irrational, and it is bracketed exactly.
    """
    x, y = Fraction(n[0]), Fraction(n[1])
    q = x * x + y * y
    if q == 0:
        raise ValueError("zero normal")
    P = x ** 5 - 10 * x ** 3 * y * y + 5 * x * y ** 4
    tail = eps * P / (q * q)
    return sqrt_lower(q) + tail, sqrt_upper(q) + tail


def _round_up(x: Fraction, den: int) -> Fraction:
    """The smallest multiple of 1/den that is >= x.  Keeps certificate integers small."""
    return Fraction(-((-x.numerator * den) // x.denominator), den)


def _round_down(x: Fraction, den: int) -> Fraction:
    return Fraction((x.numerator * den) // x.denominator, den)


def outer_halfplanes(J: int, scale: int = 10 ** 6, eps=Fraction(1, 24),
                     den: int = 10 ** 12):
    """J rational normals spread around the circle, with rational offsets that are UPPER
    bounds on the body's support function.  Returns [(n, c_upper, c_lower, |n|_upper)].

    The offsets are rounded OUTWARD to multiples of 1/den, which keeps K subset Q0 (any
    upper bound on the support function does) while keeping the exact integers small.
    J must be even so that the normal set is antipodally closed, which the a priori side
    bound in `cw.py` uses.
    """
    if J % 2:
        raise ValueError("J must be even (antipodal closure)")
    out = []
    for j in range(J):
        a = 2 * math.pi * j / J
        nx = Fraction(round(scale * math.cos(a)), scale)
        ny = Fraction(round(scale * math.sin(a)), scale)
        if nx == 0 and ny == 0:
            raise AssertionError("degenerate sampled normal")
        lo, hi = cw_support_bounds((nx, ny), eps)
        out.append(((nx, ny), _round_up(hi, den), _round_down(lo, den),
                    _round_up(sqrt_upper(nx * nx + ny * ny), den)))
    return out


def inflate(hps, r: Fraction):
    """Outer parallel body at distance r: c_j -> c_j + r|n_j| (upper bound on |n_j|)."""
    return [(n, c + r * nrm, clo, nrm) for (n, c, clo, nrm) in hps]


def erode_const(hps, eta: Fraction):
    """Inner body: use the LOWER support bounds and erode by eta, giving a polygon that is
    contained in the body (see the README's derivation of eta)."""
    return [(n, clo - eta * nrm, clo, nrm) for (n, c, clo, nrm) in hps]


# ------------------------------------------------------------------ the exact LP bound
def _rot60(u):
    """(x,y) rational -> rho u in Q(sqrt3)^2, rho = rotation by +60 degrees."""
    x, y = Q3.of(u[0]), Q3.of(u[1])
    half = Q3(1, 0, 2)
    s60 = Q3(0, 1, 2)
    return (half * x - s60 * y, s60 * x + half * y)


def m_coefficients(u, hps):
    """m_j = max(0, <u,n_j>, <rho u, n_j>) in Q(sqrt 3), exactly."""
    ru = _rot60(u)
    ux, uy = Q3.of(u[0]), Q3.of(u[1])
    out = []
    for (n, c, clo, nrm) in hps:
        nx, ny = Q3.of(n[0]), Q3.of(n[1])
        a = ux * nx + uy * ny
        b = ru[0] * nx + ru[1] * ny
        m = Q3(0)
        if a.sgn() > 0:
            m = a
        if (b - m).sgn() > 0:
            m = b
        out.append(m)
    return out


def dual_bound(hps, ms, i, j, k):
    """The exact weak-duality bound from the triple (i,j,k), or None if y >= 0 fails."""
    def nv(t):
        return (Q3.of(hps[t][0][0]), Q3.of(hps[t][0][1]))
    a, b, c = nv(i), nv(j), nv(k)

    def cross(p, q):
        return p[0] * q[1] - p[1] * q[0]

    Xi = cross(b, c)
    Xj = cross(c, a)
    Xk = cross(a, b)
    D = ms[i] * Xi + ms[j] * Xj + ms[k] * Xk
    d = D.sgn()
    if d == 0:
        return None
    # y_r = X_r / D >= 0 for all three
    if Xi.sgn() * d < 0 or Xj.sgn() * d < 0 or Xk.sgn() * d < 0:
        return None
    num = Q3.of(hps[i][1]) * Xi + Q3.of(hps[j][1]) * Xj + Q3.of(hps[k][1]) * Xk
    return num / D


def _float_tables(hps, ms):
    import numpy as np
    N = np.array([[float(n[0]), float(n[1])] for (n, c, clo, nrm) in hps])
    C = np.array([float(c) for (n, c, clo, nrm) in hps])
    M = np.array([float(m) for m in ms])
    return N, C, M


def _best_t(N, C, M, levels=18, span=2.0):
    """Float search (guidance only) for t maximising min_j (C_j - <t,n_j>)/M_j.

    Concave and piecewise linear, so a shrinking full 2-D local grid is used rather than an
    axis-wise move, which can stall at a kink.
    """
    import numpy as np
    pos = M > 1e-14
    Np, Cp, Mp = N[pos], C[pos], M[pos]
    Nz, Cz = N[~pos], C[~pos]

    def f(pts):                       # pts: (P,2)
        val = ((Cp[None, :] - pts @ Np.T) / Mp[None, :]).min(axis=1)
        if Nz.shape[0]:
            viol = (pts @ Nz.T - Cz[None, :]).max(axis=1)
            val = np.where(viol > 0, -1e9 - viol, val)
        return val

    t = np.zeros(2)
    step = span
    for _ in range(levels):
        gx, gy = np.meshgrid(np.linspace(-step, step, 9), np.linspace(-step, step, 9))
        pts = t[None, :] + np.stack([gx.ravel(), gy.ravel()], axis=1)
        v = f(pts)
        t = pts[int(np.argmax(v))]
        step *= 0.5
    return t, float(f(t[None, :])[0])


def lambda_upper_at(hps, u, cand=13):
    """EXACT upper bound on lambda*(u) for the half-plane body `hps`.

    Floats PROPOSE the candidate active triple; every returned number is the exact
    Q(sqrt 3) value of a weak-duality certificate checked exactly (`dual_bound`), so a bad
    proposal can only make the bound loose, never wrong.

    The candidates are the constraints with the smallest exact-form RESIDUAL
    c_j - (<t,n_j> + lambda m_j) at the float optimum -- including the constraints with
    m_j = 0, which are ordinary walls of the polytope in t and can perfectly well sit in
    the optimal basis.  (The first version of this function ranked by (c-<t,n>)/m and so
    could never propose them; it then found no valid triple at all on the very direction
    that attains the maximum.  That was the bug this lane was warned to look for.)
    """
    import numpy as np
    ms = m_coefficients(u, hps)
    N, C, M = _float_tables(hps, ms)
    t, lam = _best_t(N, C, M)
    res = C - (N @ t + lam * M)
    idx = [int(i) for i in np.argsort(res)[:cand]]
    best = None
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            for c in range(b + 1, len(idx)):
                v = dual_bound(hps, ms, idx[a], idx[b], idx[c])
                if v is None or v.sgn() <= 0:
                    continue
                if best is None or (v - best).sgn() < 0:
                    best = v
    return best, lam


def feasible_lambda_lower(hps, u, denom=10 ** 6):
    """An exactly certified FEASIBLE (t, lambda): a triangle really contained in the body.

    The float optimum is rounded to rationals and then every constraint is re-checked
    exactly; the returned lambda is a valid lower bound on lambda*(u), or None.
    """
    import numpy as np
    ms = m_coefficients(u, hps)
    N, C, M = _float_tables(hps, ms)
    t, lam = _best_t(N, C, M)
    tq = (Q3.of(Fraction(round(t[0] * denom), denom)),
          Q3.of(Fraction(round(t[1] * denom), denom)))
    lo, hi = Fraction(0), Fraction(round(lam * denom) + 1, denom)
    # bisect on an exact feasibility test
    for _ in range(40):
        mid = (lo + hi) / 2
        lq = Q3.of(mid)
        ok = True
        for r, (n, c, clo, nrm) in enumerate(hps):
            lhs = tq[0] * Q3.of(n[0]) + tq[1] * Q3.of(n[1]) + lq * ms[r]
            if (lhs - Q3.of(c)).sgn() > 0:
                ok = False
                break
        if ok:
            lo = mid
        else:
            hi = mid
    if lo == 0:
        return None, tq
    return Q3.of(lo), tq


# ------------------------------------------------------------------ direction sampling
def sample_directions(D: int, scale: int = 10 ** 6):
    """D rational direction vectors around the whole circle, in angular order."""
    out = []
    for k in range(D):
        a = 2 * math.pi * k / D
        out.append((Fraction(round(scale * math.cos(a)), scale),
                    Fraction(round(scale * math.sin(a)), scale)))
    return out


def max_gap_tan(dirs):
    """An exact rational upper bound on the largest angular gap between consecutive
    sampled directions: gamma <= tan gamma = cross/dot, valid while dot > 0."""
    worst = Fraction(0)
    D = len(dirs)
    for k in range(D):
        u = dirs[k]
        v = dirs[(k + 1) % D]
        cr = u[0] * v[1] - u[1] * v[0]
        dt = u[0] * v[0] + u[1] * v[1]
        if dt <= 0:
            raise AssertionError("sampled gap is at least 90 degrees: refusing to bound it")
        if cr <= 0:
            raise AssertionError("sampled directions are not in increasing angular order")
        g = cr / dt
        if g > worst:
            worst = g
    return worst


def upper_bound(hps, dirs, s_ub: Fraction, progress=None):
    """The exact upper bound on side^2 for every equilateral triangle contained in the body
    described by `hps`.  Returns (side2_bound, per-direction records).

    `hps` must ALREADY be the inflated body Q_r with r = s_ub * gamma / (2 sqrt3).
    """
    best = None
    recs = []
    for i, u in enumerate(dirs):
        lam, lam_float = lambda_upper_at(hps, u)
        if lam is None:
            raise AssertionError("no exact dual certificate at direction %d" % i)
        u2 = Q3.of(Fraction(u[0]) ** 2 + Fraction(u[1]) ** 2)
        s2 = lam * lam * u2
        recs.append({"i": i, "u": [str(u[0]), str(u[1])], "lambda_ub": lam.pair(),
                     "side2_ub": s2.pair(), "side_ub_display": float(s2) ** 0.5,
                     "lambda_float": lam_float})
        if best is None or (s2 - best).sgn() > 0:
            best = s2
        if progress and i % progress == 0:
            print("      dir %d/%d  running max side <= %.9f"
                  % (i, len(dirs), float(best) ** 0.5), flush=True)
    return best, recs


def halfplanes_from_convex_polygon(poly):
    """[(n_j, c_j, c_j, |n_j|_upper)] for a convex RATIONAL polygon given counterclockwise.

    Used to run the containment bound on a body whose answer is known independently.
    """
    n = len(poly)
    out = []
    for i in range(n):
        (ax, ay), (bx, by) = poly[i], poly[(i + 1) % n]
        ax, ay, bx, by = Fraction(ax), Fraction(ay), Fraction(bx), Fraction(by)
        nx, ny = (by - ay), -(bx - ax)          # outward normal for ccw orientation
        c = nx * ax + ny * ay
        out.append(((nx, ny), c, c, sqrt_upper(nx * nx + ny * ny)))
    # The bounding box, appended so that the family is antipodally closed and the a priori
    # side bound of `cw.a_priori_side_bound` applies.  These half planes are implied by the
    # edge ones, so Q0 is unchanged.
    xs = [Fraction(p[0]) for p in poly]
    ys = [Fraction(p[1]) for p in poly]
    one = sqrt_upper(Fraction(1))
    out.append((((Fraction(1), Fraction(0))), max(xs), max(xs), one))
    out.append((((Fraction(-1), Fraction(0))), -min(xs), -min(xs), one))
    out.append((((Fraction(0), Fraction(1))), max(ys), max(ys), one))
    out.append((((Fraction(0), Fraction(-1))), -min(ys), -min(ys), one))
    return out
