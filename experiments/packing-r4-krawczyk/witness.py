"""From a high-precision contact solution to an EXACT, exactly-verified packing.

CONSTRUCTION SIDE ONLY (upper bound).  Nothing here bears on optimality.

An enclosure of a stationary point is not a packing certificate.  This module produces the
explicit configuration that *is* one, and proves it feasible in exact rational arithmetic:

 1. snap the sheared coordinates (x, u) to rationals with denominator 10**SNAP;
 2. restore exact wall incidences (u = 0 on AB, x = u on AC) and clamp so that
    u >= 0 and x >= u hold *exactly* for every point;
 3. compute the exact minimum squared separation  m2 = min (dx^2 + 3 du^2);
 4. if m2 < 4, apply the homothety  p -> lambda p  about A = (0,0) with lambda a rational
    satisfying lambda^2 >= 4/m2.  A homothety about A maps T_d onto T_{lambda d}, so
    containment is preserved and every separation is multiplied by lambda >= 1;
 5. declare  d = max_i (x_i + u_i), which is exactly the minimal side of the fixed-placement
    triangle containing the point set, so the certificate is TIGHT for its point set;
 6. re-verify everything from scratch in exact rational arithmetic.

Step 4 is what makes this unconditional: whatever the snapping did, scaling repairs it, and
the repair is measured (lambda - 1 is reported).
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

from mpmath import mp

SNAP = 40           # snapping denominator 10**SNAP
LAM_DEN = 10 ** 45  # denominator used for the repair factor lambda


def _snap(v, den: int) -> Fraction:
    return Fraction(int(mp.floor(v * den + mp.mpf("0.5"))), den)


def ceil_sqrt_frac(t: Fraction, q: int) -> Fraction:
    """Smallest p/q with (p/q)**2 >= t  (t >= 0)."""
    num = t.numerator * q * q
    den = t.denominator
    n = -((-num) // den)          # ceil(t * q^2)
    p = isqrt(n)
    while p * p < n:
        p += 1
    return Fraction(p, q)


def build_witness(n, z_mp, eqs, extra_slack: Fraction | None = None):
    """Return an exact witness packing in sheared coordinates."""
    wallA = {e[1] for e in eqs if e[0] == "wA"}
    wallB = {e[1] for e in eqs if e[0] == "wB"}
    den = 10 ** SNAP
    xs = [_snap(z_mp[1 + 2 * i], den) for i in range(n)]
    us = [_snap(z_mp[2 + 2 * i], den) for i in range(n)]
    for i in range(n):
        if i in wallA:
            us[i] = Fraction(0)
        if i in wallB:
            xs[i] = us[i]
        if us[i] < 0:
            us[i] = Fraction(0)
        if xs[i] < us[i]:
            xs[i] = us[i]
    m2 = min(
        (xs[i] - xs[j]) ** 2 + 3 * (us[i] - us[j]) ** 2
        for i in range(n)
        for j in range(i + 1, n)
    )
    lam = Fraction(1)
    if m2 < 4:
        lam = ceil_sqrt_frac(Fraction(4) / m2, LAM_DEN)
    if extra_slack is not None:
        lam = lam * (1 + extra_slack)
    if lam != 1:
        xs = [lam * v for v in xs]
        us = [lam * v for v in us]
    d = max(xs[i] + us[i] for i in range(n))
    return {"n": n, "xs": xs, "us": us, "d": d, "lam": lam, "snap_den": den}


def verify_exact(w):
    """Exact re-verification, from scratch, in sheared coordinates.  Returns a report."""
    n, xs, us, d = w["n"], w["xs"], w["us"], w["d"]
    assert len(xs) == n == len(us)
    pairs_ok = True
    m2 = None
    contacts = 0
    for i in range(n):
        for j in range(i + 1, n):
            q = (xs[i] - xs[j]) ** 2 + 3 * (us[i] - us[j]) ** 2
            if q < 4:
                pairs_ok = False
            if q == 4:
                contacts += 1
            m2 = q if m2 is None or q < m2 else m2
    contain_ok = True
    boundary = 0
    for i in range(n):
        on = False
        if us[i] < 0:
            contain_ok = False
        elif us[i] == 0:
            on = True
        if xs[i] - us[i] < 0:
            contain_ok = False
        elif xs[i] - us[i] == 0:
            on = True
        if d - xs[i] - us[i] < 0:
            contain_ok = False
        elif d - xs[i] - us[i] == 0:
            on = True
        boundary += 1 if on else 0
    d_min = max(xs[i] + us[i] for i in range(n))
    distinct = len({(xs[i], us[i]) for i in range(n)}) == n
    return {
        "separation_ok": pairs_ok,
        "containment_ok": contain_ok,
        "distinct": distinct,
        "min_squared_distance": m2,
        "contacts_exactly_2": contacts,
        "boundary_points": boundary,
        "d_min": d_min,
        "tight": d == d_min,
        "feasible": pairs_ok and contain_ok and distinct and d >= d_min,
    }
