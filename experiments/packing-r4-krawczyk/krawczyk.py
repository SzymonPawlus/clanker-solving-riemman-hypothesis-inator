"""Interval Krawczyk existence/uniqueness test over exact rational intervals.

CONSTRUCTION SIDE ONLY -- nothing here bears on optimality.

Given a square system F: R^k -> R^k (a selected subsystem of the tight contact equations,
with the undetermined variables frozen at exact rational values), a rational midpoint
yhat and a rational radius R, the operator

    K(X) = yhat - C F(yhat) + (I - C J(X)) (X - yhat),      X = yhat + [-R, R]^k

satisfies:  if K(X) is contained in the *interior* of X then F has exactly one zero in X,
and that zero lies in K(X) ∩ X.  (Krawczyk 1969; Moore 1977; Neumaier, *Interval Methods
for Systems of Equations*, Thm 5.1.7.)  C is any real matrix -- it does not have to be a
good inverse for the conclusion to be valid, only for the test to succeed -- so rounding
C to the rational grid costs nothing but sharpness.

All arithmetic below is exact rational interval arithmetic (see iv.py).  Floats/mpf are
used only to *propose* yhat and C; both then enter as exact rationals.
"""

from __future__ import annotations

from mpmath import mp

import iv
from model import DVAR, uvar, xvar

FOUR = iv.from_int_units(4 * iv.DEN)
THREE = iv.from_int_units(3 * iv.DEN)
TWO = iv.from_int_units(2 * iv.DEN)
SIX = iv.from_int_units(6 * iv.DEN)


def ires(eq, Z):
    kind = eq[0]
    if kind == "pair":
        _, i, j = eq
        dx = iv.sub(Z[xvar(i)], Z[xvar(j)])
        du = iv.sub(Z[uvar(i)], Z[uvar(j)])
        return iv.sub(iv.add(iv.mul(dx, dx), iv.mul(THREE, iv.mul(du, du))), FOUR)
    i = eq[1]
    if kind == "wA":
        return Z[uvar(i)]
    if kind == "wB":
        return iv.sub(Z[xvar(i)], Z[uvar(i)])
    if kind == "wC":
        return iv.sub(iv.sub(Z[DVAR], Z[xvar(i)]), Z[uvar(i)])
    raise ValueError(kind)


ONE = iv.from_int_units(iv.DEN)
MONE = iv.from_int_units(-iv.DEN)


def ijac(eq, Z):
    kind = eq[0]
    if kind == "pair":
        _, i, j = eq
        dx = iv.sub(Z[xvar(i)], Z[xvar(j)])
        du = iv.sub(Z[uvar(i)], Z[uvar(j)])
        a = iv.mul(TWO, dx)
        b = iv.mul(SIX, du)
        return {xvar(i): a, xvar(j): iv.neg(a), uvar(i): b, uvar(j): iv.neg(b)}
    i = eq[1]
    if kind == "wA":
        return {uvar(i): ONE}
    if kind == "wB":
        return {xvar(i): ONE, uvar(i): MONE}
    if kind == "wC":
        return {DVAR: ONE, xvar(i): MONE, uvar(i): MONE}
    raise ValueError(kind)


def to_units(v) -> int:
    """Nearest grid integer to an mpf.  Only ever used to *propose* rational data."""
    return int(mp.floor(v * iv.DEN + mp.mpf("0.5")))


def krawczyk_test(eqs, rows, cols, z_mp, radius_units: int):
    """Run one Krawczyk test.  Returns a dict of results (no exceptions on failure)."""
    k = len(rows)
    yhat = [to_units(v) for v in z_mp]              # grid ints, all variables
    R = radius_units

    # --- approximate inverse C of the square Jacobian, proposed in mpf, used as rationals
    J = mp.zeros(k, k)
    for a, r in enumerate(rows):
        from model import jac_row

        row = jac_row(eqs[r], z_mp)
        for b, c in enumerate(cols):
            if c in row:
                J[a, b] = row[c]
    try:
        Cm = J ** -1
    except Exception:
        return {"ok": False, "reason": "jacobian inverse failed"}
    C = [[iv.from_int_units(to_units(Cm[a, b])) for b in range(k)] for a in range(k)]

    # --- box: free columns widened by R, everything else frozen at its grid value
    Z = [iv.from_int_units(v) for v in yhat]
    for c in cols:
        Z[c] = (yhat[c] - R, yhat[c] + R)

    # --- F(yhat): exact (degenerate) evaluation
    Zc = [iv.from_int_units(v) for v in yhat]
    Fy = [ires(eqs[r], Zc) for r in rows]

    # --- C F(yhat)
    CF = []
    for a in range(k):
        acc = (0, 0)
        for b in range(k):
            acc = iv.add(acc, iv.mul(C[a][b], Fy[b]))
        CF.append(acc)

    # --- C J(X), exploiting row sparsity of J
    colpos = {c: b for b, c in enumerate(cols)}
    acc = [[(0, 0)] * k for _ in range(k)]
    for bidx, r in enumerate(rows):
        jr = ijac(eqs[r], Z)
        for c, val in jr.items():
            b = colpos.get(c)
            if b is None:
                continue
            for a in range(k):
                acc[a][b] = iv.add(acc[a][b], iv.mul(C[a][bidx], val))
    # --- M = I - C J(X); then w = M * [-R, R]^k, bounded by row magnitude sums
    K = []
    maxmag = 0
    for a in range(k):
        mags = 0
        for b in range(k):
            lo, hi = acc[a][b]
            if a == b:
                lo, hi = iv.DEN - hi, iv.DEN - lo
            else:
                lo, hi = -hi, -lo
            mags += max(abs(lo), abs(hi))
        maxmag = max(maxmag, mags)
        half = -((-(mags * R)) // iv.DEN)          # ceil, outward
        w = (-half, half)
        K.append(iv.add(iv.sub(iv.from_int_units(yhat[cols[a]]), CF[a]), w))

    ok = all(
        (yhat[cols[a]] - R) < K[a][0] and K[a][1] < (yhat[cols[a]] + R) for a in range(k)
    )
    # solution lies in K(X) ∩ X
    encl = [
        (max(K[a][0], yhat[cols[a]] - R), min(K[a][1], yhat[cols[a]] + R)) for a in range(k)
    ]
    return {
        "ok": ok,
        "k": k,
        "radius_units": R,
        "enclosure": encl,
        "cols": list(cols),
        "yhat": yhat,
        "max_row_mag": maxmag,
        "max_width": max((e[1] - e[0] for e in encl), default=0),
    }
