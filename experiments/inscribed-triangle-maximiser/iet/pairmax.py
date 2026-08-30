"""A SECOND, structurally different exact per-O maximiser: the edge-pair parametrisation.

`maximiser.py` works in DIRECTION space: it proposes a finite set of candidate directions
(vertex directions and the O(n^2) vectors M_ef of the linear form cross(v, M_ef) = 0), then
rebuilds the two radial scale sets from scratch at each candidate.

This module never looks at a direction.  It walks ORDERED PAIRS OF EDGES and parametrises
the triangle by the position of one vertex ALONG an edge:

    P(t) = A + t (B - A),  t in [0,1]          (the second vertex, on edge e = [A,B])
    Q(t) = O + rho_sigma(P(t) - O),  sigma = +-1   (the third, forced by P once O is fixed)

Both are AFFINE in t, exactly, in K = Q(sqrt 3).  The whole content is then:

* **Completeness.**  Let (O, P, Q) be any nondegenerate inscribed equilateral triangle.
  |OP| = |OQ| and angle POQ = 60 degrees, so Q = O + rho_sigma(P - O) for sigma = +1 or -1.
  P lies on some edge e and Q on some edge f, so the triple is seen by the pair (e, f, sigma).

* **Where the maximum sits.**  For a fixed (e, f, sigma) the feasible set

        F = { t in [0,1] : Q(t) lies on the segment f }

  is the intersection of [0,1] with the preimage of a convex set under an affine map, hence a
  CLOSED INTERVAL (possibly a point, possibly empty).  On it,

        side^2(t) = |P(t) - O|^2

  is a CONVEX quadratic in t, so its maximum over F is attained at an ENDPOINT of F.  That is
  the entire optimality argument -- there is no critical-point case at all, and in particular
  no rational function to differentiate.

* **Endpoints, exactly.**  With w = D - C and g(t) = cross(w, Q(t) - C) affine:
    - g1 != 0: one root t0 = -g0/g1; F is {t0} if t0 in [0,1] and Q(t0) is inside the segment.
    - g1 == 0 == g0: Q(t) is on the LINE of f for every t; F is cut out by the along-edge
      parameter u(t) = <Q(t) - C, w>/|w|^2 in [0,1], again affine, so F is an interval whose
      two endpoints are exact.
    - g1 == 0 != g0: F is empty.

Nondegeneracy (`../../problems/inscribed-equilateral-triangle/RULES.md` §2) is the condition
side^2 > 0, i.e. P != O, imposed on every candidate before it is scored.

Every candidate is finally re-checked by `maximiser.verify_triangle`, which knows nothing
about how it was produced.
"""

from __future__ import annotations

from .qs3 import Q3, ZERO, ONE
from .maximiser import (V, vadd, vsub, vscale, cross, dot, norm2, veq, rot,
                        edges, point_on_polygon, verify_triangle, vfloat)

__all__ = ["max_at_point_pairs", "feasible_ts"]


def _affine_pt(p0, p1, t):
    """p0 + t p1, componentwise, exact."""
    return (p0[0] + t * p1[0], p0[1] + t * p1[1])


def feasible_ts(O, A, B, C, D, sigma):
    """Endpoints of F = { t in [0,1] : O + rho_sigma(P(t)-O) lies on the segment [C,D] }.

    Returns a list of at most two exact t values (the endpoints of a closed interval),
    or [] when F is empty.
    """
    # Q(t) = q0 + t q1
    q0 = vadd(O, rot(vsub(A, O), sigma))
    q1 = rot(vsub(B, A), sigma)
    w = vsub(D, C)
    if w[0].is_zero() and w[1].is_zero():
        raise ValueError("zero-length edge")
    # g(t) = cross(w, Q(t) - C) = g0 + t g1
    g0 = cross(w, vsub(q0, C))
    g1 = cross(w, q1)
    ww = norm2(w)
    # u(t) = <Q(t)-C, w>/ww = u0 + t u1  (the along-edge parameter, must lie in [0,1])
    u0 = dot(vsub(q0, C), w) / ww
    u1 = dot(q1, w) / ww

    def u_ok(t):
        u = u0 + t * u1
        return u.sgn() >= 0 and (u - ONE).sgn() <= 0

    if not g1.is_zero():
        t0 = -g0 / g1
        if t0.sgn() < 0 or (t0 - ONE).sgn() > 0:
            return []
        return [t0] if u_ok(t0) else []
    if not g0.is_zero():
        return []
    # Q(t) sweeps along the LINE of f; cut by 0 <= u(t) <= 1 and 0 <= t <= 1.
    lo, hi = ZERO, ONE
    if u1.is_zero():
        return [lo, hi] if u_ok(ZERO) else []
    a = (ZERO - u0) / u1          # u(t) = 0
    b = (ONE - u0) / u1           # u(t) = 1
    if (a - b).sgn() > 0:
        a, b = b, a
    if (a - lo).sgn() > 0:
        lo = a
    if (b - hi).sgn() < 0:
        hi = b
    if (lo - hi).sgn() > 0:
        return []
    return [lo, hi] if (lo - hi).sgn() != 0 else [lo]


def max_at_point_pairs(O, poly, check=True):
    """EXACT max side^2 of a nondegenerate inscribed equilateral triangle with a vertex at O.

    Independent of `maximiser.max_at_point`: different parametrisation, different candidate
    set, different optimality argument.
    """
    assert point_on_polygon(O, poly), "O must lie on the polygon"
    E = edges(poly)
    best = None
    n_cand = 0
    for (A, B) in E:
        for (C, D) in E:
            for sigma in (1, -1):
                for t in feasible_ts(O, A, B, C, D, sigma):
                    n_cand += 1
                    P = _affine_pt(A, vsub(B, A), t)
                    Q = vadd(O, rot(vsub(P, O), sigma))
                    s2 = norm2(vsub(P, O))
                    if s2.sgn() <= 0:
                        continue          # the degenerate triangle (O, O, O)
                    if best is None or (s2 - best[0]).sgn() > 0:
                        best = (s2, P, Q)
    res = {"good": best is not None, "n_candidates": n_cand,
           "side2": None, "P": None, "Q": None}
    if best is None:
        return res
    s2, P, Q = best
    res.update({"side2": s2, "P": P, "Q": Q})
    if check:
        ok, detail = verify_triangle(poly, O, P, Q)
        if not ok:
            raise AssertionError("pair maximiser proposed a rejected triangle: %r" % (detail,))
        if detail["side2_q3"] != s2:
            raise AssertionError("reported side^2 disagrees with the verifier's")
    return res
