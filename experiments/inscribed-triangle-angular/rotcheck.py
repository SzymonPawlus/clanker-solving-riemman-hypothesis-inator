"""A SECOND exact decider for the same question, written from scratch in this lane, used
only to cross-examine `angular.py` where the sibling's fixture battery is thin.

The sibling battery is 182 convex fixtures against 8 non-convex ones, so agreement there
says very little about the non-convex answers this lane is asked for.  This module supplies
the missing coverage from inside the lane.  It is the ROTATION algorithm:

    O is good  <=>  there is X != O with X in J and X in rho(J),

where rho is the +60-degree rotation about O.  (rho^{-1} need not be tried separately:
X in J & rho^{-1}(J) with X != O gives rho(X) in rho(J) & J, and rho(X) != O.)  Both J and
rho(J) are unions of closed segments, so this is finitely many exact segment-segment
intersections in the PLANE -- no direction space, no arcs, no linear form.  It shares no
code with the sweep beyond the field arithmetic in `q3.py` and the vector helpers.

The crux is the same one the sibling's file warns about: rho fixes O and O is on J, so O is
in the intersection ALWAYS.  A decider that forgets to exclude it calls every point good.
That is why every branch below discards components equal to {O} and reports only X != O.

This is deliberately the sibling's algorithm and not an independent idea: two
implementations of the same idea agreeing is weaker evidence than the sweep agreeing with
it, which is the point -- if the sweep and this disagree, one of them is wrong and the
disagreement is exactly the thing worth having.
"""

from __future__ import annotations

from angular import (V, vadd, vsub, vscale, cross, dot, norm2, veq, is_zero_vec,
                     rot_about, edges, point_on_segment)
from q3 import Q3, ZERO, ONE


def _seg_seg_not_O(A, B, C, D, O):
    """Some point of [A,B] & [C,D] other than O, or None."""
    r = vsub(B, A)
    s = vsub(D, C)
    den = cross(r, s)
    qp = vsub(C, A)
    if not den.is_zero():
        t = cross(qp, s) / den
        u = cross(qp, r) / den
        if t.sgn() < 0 or (t - ONE).sgn() > 0:
            return None
        if u.sgn() < 0 or (u - ONE).sgn() > 0:
            return None
        X = vadd(A, vscale(t, r))
        return None if veq(X, O) else X
    if not cross(qp, r).is_zero():
        return None                       # parallel, distinct lines
    rr = norm2(r)
    if rr.is_zero():
        return None if veq(A, O) or not point_on_segment(A, C, D) else A
    t0 = dot(qp, r) / rr
    t1 = t0 + dot(s, r) / rr
    if (t1 - t0).sgn() >= 0:
        lo, hi = t0, t1
    else:
        lo, hi = t1, t0
    if lo.sgn() < 0:
        lo = ZERO
    if (hi - ONE).sgn() > 0:
        hi = ONE
    if (hi - lo).sgn() < 0:
        return None
    P = vadd(A, vscale(lo, r))
    Qd = vadd(A, vscale(hi, r))
    if not veq(P, O):
        return P
    if not veq(Qd, O):
        return Qd
    return None                           # the overlap is exactly {O}


def decide_rot(O, poly):
    """(good, X) with X in J & rho(J), X != O.  Exact."""
    E = edges(poly)
    RE = [(rot_about(A, O, 1), rot_about(B, O, 1)) for (A, B) in E]
    for (A, B) in E:
        for (C, D) in RE:
            X = _seg_seg_not_O(A, B, C, D, O)
            if X is not None:
                return True, X
    return False, None


def triangle_from(O, X):
    """The inscribed triangle O, rho^{-1}(X), X."""
    return (rot_about(X, O, -1), X)
