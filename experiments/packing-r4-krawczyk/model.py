"""Contact system for n points in an equilateral triangle -- CONSTRUCTION SIDE ONLY.

Nothing in this file bears on optimality; it only manipulates candidate packings.

Sheared coordinates
-------------------
The repo convention (problems/circle-packing-equilateral-triangle/RULES.md §2) places the
triangle at A=(0,0), B=(d,0), C=(d/2, d*sqrt(3)/2).  Substituting  y = sqrt(3) * u  turns
every constraint rational:

    containment   u >= 0            (side AB)
                  x - u >= 0        (side AC)
                  d - x - u >= 0    (side BC)
    separation    (xi-xj)^2 + 3*(ui-uj)^2 >= 4
    minimal side  d_min = max_i (x_i + u_i)

so no irrational constant ever enters the arithmetic.  All exact work is done here; the
sqrt(3) only reappears when a certificate is written back in (x, y).

Variable vector:  z[0] = d,  z[1+2i] = x_i,  z[2+2i] = u_i.
"""

from __future__ import annotations

import json
from fractions import Fraction

from mpmath import mp

DVAR = 0


def xvar(i: int) -> int:
    return 1 + 2 * i


def uvar(i: int) -> int:
    return 2 + 2 * i


def load_candidate(path: str):
    """Read an LS candidate certificate and return (n, x list, u list) as mpf."""
    with open(path) as fh:
        cert = json.load(fh)
    n = cert["n"]
    xs, us = [], []
    sqrt3 = mp.sqrt(3)
    for sx, sy in cert["coordinates"]:
        fx = Fraction(sx)
        fy = Fraction(sy)
        xs.append(mp.mpf(fx.numerator) / fx.denominator)
        us.append((mp.mpf(fy.numerator) / fy.denominator) / sqrt3)
    assert len(xs) == n
    return n, xs, us


def pack(d, xs, us):
    z = [d]
    for x, u in zip(xs, us):
        z.append(x)
        z.append(u)
    return z


def unpack(z):
    d = z[0]
    xs = z[1::2]
    us = z[2::2]
    return d, xs, us


def tight_structure(n, d, xs, us, tol):
    """Return the list of tight constraints at the given configuration.

    Each entry is a tuple ('pair', i, j) / ('wA', i) / ('wB', i) / ('wC', i).
    """
    eqs = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = xs[i] - xs[j]
            du = us[i] - us[j]
            if abs(dx * dx + 3 * du * du - 4) < tol:
                eqs.append(("pair", i, j))
    for i in range(n):
        if abs(us[i]) < tol:
            eqs.append(("wA", i))
        if abs(xs[i] - us[i]) < tol:
            eqs.append(("wB", i))
        if abs(d - xs[i] - us[i]) < tol:
            eqs.append(("wC", i))
    return eqs


def residual(eq, z):
    """Exact-in-the-ring residual of one equation, evaluated with whatever number type z holds."""
    kind = eq[0]
    if kind == "pair":
        _, i, j = eq
        dx = z[xvar(i)] - z[xvar(j)]
        du = z[uvar(i)] - z[uvar(j)]
        return dx * dx + 3 * du * du - 4
    i = eq[1]
    if kind == "wA":
        return z[uvar(i)]
    if kind == "wB":
        return z[xvar(i)] - z[uvar(i)]
    if kind == "wC":
        return z[DVAR] - z[xvar(i)] - z[uvar(i)]
    raise ValueError(kind)


def jac_row(eq, z):
    """Sparse Jacobian row as {column: value}; values in the same number type as z."""
    kind = eq[0]
    if kind == "pair":
        _, i, j = eq
        dx = z[xvar(i)] - z[xvar(j)]
        du = z[uvar(i)] - z[uvar(j)]
        return {
            xvar(i): 2 * dx,
            xvar(j): -2 * dx,
            uvar(i): 6 * du,
            uvar(j): -6 * du,
        }
    i = eq[1]
    one = z[0] * 0 + 1
    if kind == "wA":
        return {uvar(i): one}
    if kind == "wB":
        return {xvar(i): one, uvar(i): -one}
    if kind == "wC":
        return {DVAR: one, xvar(i): -one, uvar(i): -one}
    raise ValueError(kind)


def select_square(eqs, z, nvar, thresh_rel=mp.mpf("1e-20"), dboost=mp.mpf("1e6")):
    """Full-pivot Gaussian elimination on the tight-constraint Jacobian.

    Returns (rows, cols) -- an ordered list of independent equation indices and an ordered
    list of variable indices -- such that the square subsystem d(F_rows)/d(z_cols) is
    nonsingular at ``z``.  Variables outside ``cols`` are the ones the tight system does not
    determine (rattler degrees of freedom and other flat directions); they get frozen.
    The d column is boosted so that d is chosen free whenever it can be.
    """
    m = [[mp.mpf(0)] * nvar for _ in eqs]
    for r, eq in enumerate(eqs):
        for c, v in jac_row(eq, z).items():
            m[r][c] = v
    scale = max((abs(v) for row in m for v in row), default=mp.mpf(1))
    if scale == 0:
        return [], []
    thresh = scale * thresh_rel
    rows_left = list(range(len(eqs)))
    cols_left = list(range(nvar))
    rows, cols = [], []
    while rows_left and cols_left:
        best = None
        for r in rows_left:
            for c in cols_left:
                w = abs(m[r][c]) * (dboost if c == DVAR else 1)
                if best is None or w > best[0]:
                    best = (w, r, c)
        _, pr, pc = best
        if abs(m[pr][pc]) < thresh:
            break
        rows.append(pr)
        cols.append(pc)
        rows_left.remove(pr)
        cols_left.remove(pc)
        piv = m[pr][pc]
        for r in rows_left:
            f = m[r][pc] / piv
            if f != 0:
                for c in cols_left:
                    m[r][c] -= f * m[pr][c]
                m[r][pc] = mp.mpf(0)
    return rows, cols


def newton(eqs, rows, cols, z, iters=60):
    """Newton on the square subsystem F_rows = 0 in the free variables z_cols."""
    z = list(z)
    k = len(rows)
    for _ in range(iters):
        f = mp.matrix([residual(eqs[r], z) for r in rows])
        j = mp.zeros(k, k)
        for a, r in enumerate(rows):
            row = jac_row(eqs[r], z)
            for b, c in enumerate(cols):
                if c in row:
                    j[a, b] = row[c]
        try:
            step = mp.lu_solve(j, -f)
        except Exception:
            return z, None
        for b, c in enumerate(cols):
            z[c] = z[c] + step[b]
        if max(abs(s) for s in step) < mp.mpf(10) ** (-(mp.dps - 12)):
            break
    res = max((abs(residual(e, z)) for e in eqs), default=mp.mpf(0))
    return z, res


def load_search_candidate(path: str):
    """Read a multistart-NLP output (unit-triangle points) and return (n, x, u) as mpf.

    The file stores points in the unit triangle (0,0), (1,0), (1/2, sqrt(3)/2) together with
    the achieved minimum pairwise distance m; scaling by 2/m reaches the point formulation.
    """
    with open(path) as fh:
        cert = json.load(fh)
    n = cert["n"]
    pts = cert["unit_triangle_points"]
    sqrt3 = mp.sqrt(3)
    P = [(mp.mpf(repr(px)), mp.mpf(repr(py))) for px, py in pts]
    m = min(
        mp.sqrt((P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2)
        for i in range(n)
        for j in range(i + 1, n)
    )
    sc = 2 / m
    xs = [p[0] * sc for p in P]
    us = [p[1] * sc / sqrt3 for p in P]
    return n, xs, us
