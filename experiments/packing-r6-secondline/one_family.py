"""One-family (per-strip) counting bound: reproduction of r5-eo7, and the coupled version.

Two caps are implemented.

  CAP-CEIL  (r5-eo7's convention).  Rescale a' < 6 up to T(6); separation becomes r = 6/a' > 1
            STRICTLY, so k-1 <= L/r < L and k <= ceil(L).  Valid only if the scan is run at
            side 6 with the understanding that the separation is > 1.
  CAP-FLOOR (mine, "honest at side a").  Work directly in T(a) with separation >= 1 (no
            strictness available), so k - 1 <= L and k <= floor(L) + 1.

They agree whenever L is not an integer; they differ by exactly 1 per strip when it is.
That single fact is the whole of r5-eo7 §2.2, and the whole of its delta discontinuity.

delta-robust form.  If the points lie within delta of the lines, two points in one slab differ
by >= sqrt(sep^2 - 4 delta^2) along u, and the slab's u-extent is
sup_{|t - s_j| <= delta} ell(t).  So L -> chord_sup(s_j - delta, s_j + delta) and
sep -> sqrt(sep^2 - 4 delta^2).

STATUS: numerical (float scan; evidence only).  Nothing here is assumable.
"""
import json, math, sys
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _deps

_deps.require('one_family.py')   # fail fast, before the numpy import below

import numpy as np
from geom2 import profile, chord_sup, SQRT3

TOL = 1e-12


def strip_bound(p, a, h, theta, delta, cap="ceil", sep=1.0):
    """Vectorised over theta (array).  Returns integer bound per theta."""
    d1, w, Lstar = profile(p, a)
    theta = np.asarray(theta, dtype=float)
    jmax = int(math.floor(w / h)) + 2
    j = np.arange(jmax)[:, None]                      # (J,1)
    s = (theta[None, :] + j) * h                      # (J,T)
    alive = (s - delta <= w + TOL) & (s + delta >= -TOL)
    L = chord_sup(p, a, s - delta, s + delta)
    r = math.sqrt(max(1e-300, sep * sep - 4.0 * delta * delta))
    q = L / r
    if cap == "ceil":
        c = np.maximum(1, np.ceil(q - TOL))
    else:
        c = np.floor(q + TOL) + 1.0
    c = np.where(alive & (L >= -TOL), c, 0.0)
    return c.sum(axis=0).astype(int)


def scan(a, delta, cap="ceil", sep=1.0, nphi=181, nh=121, nth=181, hmax=None):
    """max over (phi in [0,pi/3], h in [sqrt3/2, hmax], theta in [0,1)) of the strip bound."""
    hmax = hmax if hmax is not None else a + 0.6
    th = np.arange(nth) / nth
    best, arg = 0, None
    for i in range(nphi):
        p = (np.pi / 3.0) * i / (nphi - 1)
        for jh in range(nh):
            h = SQRT3 / 2 + (hmax - SQRT3 / 2) * jh / (nh - 1)
            v = strip_bound(p, a, h, th, delta, cap=cap, sep=sep)
            k = int(v.argmax())
            if v[k] > best:
                best, arg = int(v[k]), (p, h, float(th[k]))
    return best, arg


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "repro"
    if what == "repro":
        # r5-eo7 §7 table, reproduced with CAP-CEIL at a = 6.
        rows = []
        for delta in (0.0, 1e-9, 1e-6, 1e-4):
            b, arg = scan(6.0, delta, cap="ceil")
            rows.append({"delta": delta, "max_bound": b,
                         "arg_phi_deg": math.degrees(arg[0]), "arg_h": arg[1], "arg_theta": arg[2]})
            print(json.dumps(rows[-1]), flush=True)
        json.dump({"convention": "CAP-CEIL at a=6 (r5-eo7)", "rows": rows},
                  open("out/repro_r5eo7_delta.json", "w"), indent=1)


def validate():
    """Validate the relaxation on the cited cases k = 4,5,6 (and 3,7), CAP-CEIL at a = k-1."""
    out = []
    for k in (3, 4, 5, 6, 7):
        a = float(k - 1)
        tgt = k * (k + 1) // 2 - 2
        b, arg = scan(a, 0.0, cap="ceil", hmax=a + 0.6)
        out.append({"k": k, "a": a, "EO_target": tgt, "relaxation_max": b, "closes": b <= tgt,
                    "arg_phi_deg": math.degrees(arg[0]), "arg_h": arg[1], "arg_theta": arg[2]})
        print(json.dumps(out[-1]), flush=True)
    json.dump(out, open("out/validate_one_family.json", "w"), indent=1)
    return out


def window(a, cap="floor", tgt=26, lo=0.0, hi=0.5, iters=26, **kw):
    """Largest delta for which the scanned max is <= tgt (bisection; monotone in delta)."""
    b0, _ = scan(a, lo, cap=cap, **kw)
    if b0 > tgt:
        return 0.0, b0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        b, _ = scan(a, mid, cap=cap, **kw)
        if b <= tgt:
            lo = mid
        else:
            hi = mid
    return lo, b0
