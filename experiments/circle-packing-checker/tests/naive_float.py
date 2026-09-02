"""A deliberately naive FLOATING-POINT checker -- the anti-example.

This is NOT part of the verification path and nothing in `packcheck` imports it. It
exists only so the test suite can demonstrate, concretely, what exact arithmetic buys.

The dilemma it illustrates is not a coding mistake, it is intrinsic to floats here:

* With tolerance 0 it *rejects a valid packing*, because `sqrt(3)` is not exactly
  representable, so a pair of circles that touch exactly comes out at distance
  1.9999999999999998.
* Any tolerance large enough to fix that (>= ~1e-15) also *accepts an infeasible
  packing* whose overlap is smaller than the tolerance.

There is no tolerance that does both. That is the whole argument for `packcheck`.
"""

from __future__ import annotations

import math

import sympy


def _to_float(text) -> float:
    return float(sympy.sympify(text).evalf(30))


def naive_float_check(cert: dict, tol: float) -> bool:
    """True iff the certificate looks feasible in double precision at tolerance `tol`."""
    s = _to_float(cert["side_length"])
    d = s - 2.0 * math.sqrt(3.0)
    pts = [(_to_float(x), _to_float(y)) for x, y in cert["coordinates"]]

    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx = pts[i][0] - pts[j][0]
            dy = pts[i][1] - pts[j][1]
            if dx * dx + dy * dy - 4.0 < -tol:
                return False

    root3 = math.sqrt(3.0)
    for x, y in pts:
        if y < -tol:
            return False
        if root3 * x - y < -tol:
            return False
        if root3 * (d - x) - y < -tol:
            return False
    return True
