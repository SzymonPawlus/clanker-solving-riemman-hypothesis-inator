"""The ANGULAR exact decision procedure for the inscribed-equilateral-triangle vertex
problem, over K = Q(sqrt 3).

Everything here is exact.  `float()` is called only inside `*_display` fields and inside
`brute.py` (which decides nothing).  No library geometry predicate is used anywhere.

THE CRITERION (R)
=================
Let J be a closed curve, O in J, and rho the rotation by +60 degrees about O.  Call O
*good* if some NONDEGENERATE equilateral triangle has all three vertices on J and one of
them equal to O.

    (R)   O is good  <=>  there are an angle t and a radius r > 0 with
                          O + r u(t) in J   AND   O + r u(t+60) in J,     u(t) = e^{it}.

Proof (three lines, as advertised).
(<=)  Put A = O + r u(t), B = O + r u(t+60).  Then |OA| = |OB| = r > 0 and angle AOB = 60.
      An isoceles triangle with apex angle 60 has base angles (180-60)/2 = 60, so OAB is
      equiangular, hence equilateral with side r > 0; A,B != O and A != B, so it is
      nondegenerate, and all three vertices are on J.
(=>)  Let O,A,B be a nondegenerate equilateral triangle on J with side s > 0.  Then
      |OA| = |OB| = s and angle AOB = 60, so with A = O + s u(alpha), B = O + s u(beta) we
      get beta - alpha = +-60 (mod 360).  Take (t,r) = (alpha,s) if beta = alpha+60 and
      (t,r) = (beta,s) otherwise.                                                       []

r > 0 IS THE WHOLE DEGENERACY QUESTION.  r = 0 is available at every O and every t and is
the "triangle" O,O,O.  Every radial set below is built with s > 0 by construction; that is
where this implementation pays the debt the rotation picture pays by discarding the fixed
point O of the rotation.

SCALE PARAMETRISATION (why no square roots appear)
==================================================
Fix a nonzero DIRECTION VECTOR v in K^2 -- not a unit vector; directions are taken up to
positive scaling.  Since |rho v| = |v|, matching the radius r on the two rays is the same
as matching the SCALE s in

    S(v) = { s > 0 : O + s*v in J }.

So (R) becomes:  O is good  <=>  S(v) meets S(rho v) for some nonzero v in K^2.

That is worth stating because it removes the only place a square root could enter: a
witness triangle is (O, O + s v, O + s rho v) with s in K, so its vertices are exactly
representable.  `_edge_scales` computes S(v) edge by edge with one division.

THE SWEEP (why this is a different algorithm, not the same one twice)
====================================================================
The committed sibling `experiments/inscribed-triangle-polygons/` decides goodness by
intersecting the polygon with its own 60-degree rotate: O(n^2) segment-segment
intersections in the PLANE, solving for two segment parameters, then discarding the
component equal to {O}.  This module never intersects two segments.  It works in DIRECTION
space and computes the whole good-direction set

    G(O) = { direction v : S(v) meets S(rho v) },

by a sweep:

1.  BREAKPOINTS.  Let D be the directions of (V - O) for the vertices V != O, together
    with their rho^{-1} images, together with the four axis directions.  D is finite.
    Between two cyclically consecutive elements of D, both the set of edges met by the ray
    at v and the set met by the ray at rho v are CONSTANT, and both consist only of edges
    whose line misses O ("transversal" edges): an edge whose line contains O is met only in
    the one or two directions along it, and those are vertex directions, hence in D.  (The
    axis directions are thrown in only to force every gap below 180 degrees, so that
    d_i + d_{i+1} is a valid representative of the open gap.)

2.  ON AN OPEN GAP.  For a transversal edge e = [A,B], a = A-O, b = B-O, k = cross(a,b) != 0,
    the ray at v meets e iff v is in the closed cone spanned by a and b, and then at the
    single scale s_e(v) = k / cross(v, b-a) > 0.  For an ordered pair (e,f) of edges met
    respectively by v and by rho v, equal scales means

        k_e / cross(v, b-a)  =  k_f / cross(rho v, d-c),

    and since a rotation preserves the cross product, cross(rho v, m) = cross(v, rho^{-1} m).
    Both denominators are nonzero on the gap, so cross-multiplying is an equivalence and the
    condition is the single LINEAR form

        cross( v ,  M ) = 0,   M = k_e * rho^{-1}(d - c)  -  k_f * (b - a).      (*)

    M != 0  =>  at most the two directions +-M in this gap are good from the pair (e,f);
    M == 0  =>  the ENTIRE gap is good from that pair.  (M = 0 says the line of f is the
    60-degree rotate about O of the line of e -- the only way a one-parameter family of
    inscribed triangles can sit at O.)

    Since there are finitely many pairs, a gap that is entirely good must have M = 0 for
    some pair; so step 2 finds every component of G(O), not merely a witness.

3.  AT A BREAKPOINT.  Decided directly and independently by `good_at_direction`, which
    rebuilds S(v) and S(rho v) from scratch.  This is where collinear rays live -- a ray
    running ALONG an edge through O sees a whole interval of scales, not a point -- and it
    is the case a sampling cross-check steps over.

The output is exact: G(O) is a finite union of closed arcs and isolated directions with
endpoints in K^2.  O is good iff G(O) is nonempty.  The degeneracies land in different
places from the sibling's (there: collinear overlap of an edge with a rotated edge; here:
M = 0 and the collinear-ray intervals), which is what makes agreement between the two
informative.
"""

from __future__ import annotations

import functools
from fractions import Fraction

from q3 import Q3, ZERO, ONE, HALF, S60, C60

__all__ = [
    "V", "vadd", "vsub", "vscale", "cross", "dot", "norm2", "veq", "is_zero_vec",
    "rot", "rot_about", "dir_canon", "dir_key", "dir_eq", "dir_cmp", "in_arc",
    "edges", "point_on_segment", "point_on_polygon", "is_simple", "is_convex",
    "signed_area2", "interior_angle_info",
    "ray_scales", "good_at_direction", "good_directions", "decide", "recheck_witness",
]


# --------------------------------------------------------------------- vectors
def V(x, y):
    return (Q3.of(x), Q3.of(y))


def vadd(p, q):
    return (p[0] + q[0], p[1] + q[1])


def vsub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def vscale(t, p):
    t = Q3.of(t)
    return (t * p[0], t * p[1])


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def norm2(p):
    return p[0] * p[0] + p[1] * p[1]


def veq(p, q):
    return p[0] == q[0] and p[1] == q[1]


def is_zero_vec(p):
    return p[0].is_zero() and p[1].is_zero()


def vfloat(p):
    return [float(p[0]), float(p[1])]


def vpair(p):
    return [p[0].pair(), p[1].pair()]


def rot(v, sign=1):
    """Rotate the VECTOR v by sign*60 degrees, sign in {+1,-1}.  Exact in K."""
    s = S60 if sign == 1 else -S60
    return (C60 * v[0] - s * v[1], s * v[0] + C60 * v[1])


def rot_about(p, o, sign=1):
    return vadd(o, rot(vsub(p, o), sign))


# ------------------------------------------------------------------ directions
# A direction is a nonzero vector of K^2 taken up to POSITIVE scaling.

def dir_canon(v):
    c = v[0] if not v[0].is_zero() else v[1]
    m = abs(c)
    return (v[0] / m, v[1] / m)


def dir_key(v):
    c = dir_canon(v)
    return (c[0].pair()[0], c[0].pair()[1], c[1].pair()[0], c[1].pair()[1])


def dir_eq(u, w):
    """Same direction (not merely the same line)."""
    return cross(u, w).is_zero() and dot(u, w).sgn() > 0


def _half(v):
    """0 for polar angle in [0,180), 1 for [180,360)."""
    sy = v[1].sgn()
    if sy > 0:
        return 0
    if sy < 0:
        return 1
    return 0 if v[0].sgn() > 0 else 1


def dir_cmp(u, w):
    """Total order on directions by polar angle in [0,360), measured CCW from +x."""
    hu, hw = _half(u), _half(w)
    if hu != hw:
        return -1 if hu < hw else 1
    s = cross(u, w).sgn()
    if s > 0:
        return -1
    if s < 0:
        return 1
    return 0


def _rel(base, v):
    """v rewritten in the frame whose +x axis is `base` (a positive multiple of the true
    rotation, so direction-preserving)."""
    return (dot(base, v), cross(base, v))


def in_arc(v, a, b):
    """Is direction v on the closed arc running CCW from a to b?  a == b means {a}."""
    return dir_cmp(_rel(a, v), _rel(a, b)) <= 0


# -------------------------------------------------------------------- polygons
def edges(poly):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n)]


def point_on_segment(x, a, b):
    if veq(a, b):
        return veq(x, a)
    if not cross(vsub(b, a), vsub(x, a)).is_zero():
        return False
    t = dot(vsub(x, a), vsub(b, a))
    return t.sgn() >= 0 and (t - norm2(vsub(b, a))).sgn() <= 0


def point_on_polygon(x, poly):
    return any(point_on_segment(x, a, b) for a, b in edges(poly))


def signed_area2(poly):
    t = ZERO
    n = len(poly)
    for i in range(n):
        t = t + cross(poly[i], poly[(i + 1) % n])
    return t


def _seg_meets(a, b, c, d):
    """Do closed segments [a,b] and [c,d] share a point?  Boolean only; used by the
    simplicity check, never by a goodness decision."""
    r = vsub(b, a)
    s = vsub(d, c)
    den = cross(r, s)
    qp = vsub(c, a)
    if not den.is_zero():
        t = cross(qp, s) / den
        u = cross(qp, r) / den
        return (t.sgn() >= 0 and (t - ONE).sgn() <= 0
                and u.sgn() >= 0 and (u - ONE).sgn() <= 0)
    if not cross(qp, r).is_zero():
        return False
    rr = norm2(r)
    if rr.is_zero():
        return point_on_segment(a, c, d)
    t0 = dot(qp, r) / rr
    t1 = t0 + dot(s, r) / rr
    lo, hi = (t0, t1) if (t1 - t0).sgn() >= 0 else (t1, t0)
    return (hi.sgn() >= 0) and ((lo - ONE).sgn() <= 0)


def is_simple(poly):
    """Exact test that the closed polygonal curve is a Jordan curve."""
    n = len(poly)
    if n < 3:
        return False, "fewer than 3 vertices"
    E = edges(poly)
    for i, (a, b) in enumerate(E):
        if veq(a, b):
            return False, "zero-length edge %d" % i
    for i in range(n):
        for j in range(i + 1, n):
            adj = (j == i + 1) or (i == 0 and j == n - 1)
            a, b = E[i]
            c, d = E[j]
            if adj:
                shared = b if (veq(b, c) or veq(b, d)) else a
                other_i = a if veq(b, shared) else b
                other_j = c if veq(d, shared) else d
                if point_on_segment(other_i, c, d) or point_on_segment(other_j, a, b):
                    return False, "adjacent edges %d,%d overlap" % (i, j)
            else:
                if _seg_meets(a, b, c, d):
                    return False, "non-adjacent edges %d,%d meet" % (i, j)
    return True, "simple"


def is_convex(poly):
    n = len(poly)
    sgns = []
    for i in range(n):
        u = vsub(poly[i], poly[(i - 1) % n])
        w = vsub(poly[(i + 1) % n], poly[i])
        s = cross(u, w).sgn()
        if s == 0:
            return False
        sgns.append(s)
    return all(s == sgns[0] for s in sgns)


def interior_angle_info(poly, i):
    """Interior angle at vertex i: reflex flag, exact comparison with 60 degrees, and a
    DISPLAY-ONLY degree value."""
    import math
    n = len(poly)
    Vv, U, W = poly[i], poly[(i - 1) % n], poly[(i + 1) % n]
    u = vsub(U, Vv)
    w = vsub(W, Vv)
    orient = signed_area2(poly).sgn()
    turn = cross(vsub(Vv, U), vsub(W, Vv)).sgn()
    reflex = (turn * orient) < 0
    c = dot(u, w)
    s = cross(u, w)
    if reflex or c.sgn() <= 0:
        cmp60 = 1                       # angle >= 90 > 60 (or reflex)
    else:
        d = (s * s) - Q3(3) * (c * c)   # sin^2 vs 3 cos^2  <=>  tan vs sqrt3
        sg = d.sgn()
        cmp60 = -1 if sg < 0 else (0 if sg == 0 else 1)
    ang = math.degrees(math.atan2(abs(float(s)), float(c)))
    if reflex:
        ang = 360.0 - ang
    return {"reflex": reflex, "cmp60": cmp60, "degrees_display": ang}


# ------------------------------------------------- scale intervals on one ray
# An interval is (lo, hi, lo_open, hi_open) with 0 <= lo <= hi, all scales > 0.

def _edge_scales(O, A, B, v):
    """{ s > 0 : O + s*v in [A,B] } as a list of at most one interval.

    Two regimes, and the second is the one a sampling check never sees:
      cross(a,b) != 0 -- O is off the line of the edge; the ray meets it in at most a point.
      cross(a,b) == 0 -- O is ON the line of the edge; the ray either misses it entirely or
                         runs along it and meets it in a whole closed interval of scales.
    """
    a = vsub(A, O)
    b = vsub(B, O)
    k = cross(a, b)
    if not k.is_zero():
        al = cross(v, b)          # alpha * k
        be = cross(a, v)          # beta  * k
        if k.sgn() > 0:
            if al.sgn() < 0 or be.sgn() < 0:
                return []
        else:
            if al.sgn() > 0 or be.sgn() > 0:
                return []
        den = cross(v, vsub(b, a))
        if den.is_zero():
            raise AssertionError("ray parallel to a transversal edge inside its own cone")
        s = k / den
        if s.sgn() <= 0:
            raise AssertionError("non-positive scale on a transversal hit")
        return [(s, s, False, False)]
    # O is on the line of [A,B]: the ray must run along that line.
    n2 = norm2(v)
    ta = _ratio(a, v, n2)
    tb = _ratio(b, v, n2)
    if ta is None or tb is None:
        return []
    lo, hi = (ta, tb) if (ta - tb).sgn() <= 0 else (tb, ta)
    if hi.sgn() <= 0:
        return []
    if lo.sgn() > 0:
        return [(lo, hi, False, False)]
    return [(ZERO, hi, True, False)]      # half-open: s = 0 is the degenerate triangle


def _ratio(w, v, n2):
    """t with w = t*v, or None if w is not a multiple of v.  (v != 0, n2 = |v|^2.)"""
    if not cross(v, w).is_zero():
        return None
    return dot(w, v) / n2


def ray_scales(O, poly, v):
    """S(v) = { s > 0 : O + s*v on the polygon }, as a list of intervals."""
    out = []
    for (A, B) in edges(poly):
        out.extend(_edge_scales(O, A, B, v))
    return out


def _interval_meet(i1, i2):
    lo1, hi1, lo1o, hi1o = i1
    lo2, hi2, lo2o, hi2o = i2
    c = (lo1 - lo2).sgn()
    if c > 0:
        lo, loo = lo1, lo1o
    elif c < 0:
        lo, loo = lo2, lo2o
    else:
        lo, loo = lo1, (lo1o or lo2o)
    c = (hi1 - hi2).sgn()
    if c < 0:
        hi, hio = hi1, hi1o
    elif c > 0:
        hi, hio = hi2, hi2o
    else:
        hi, hio = hi1, (hi1o or hi2o)
    d = (lo - hi).sgn()
    if d > 0:
        return None
    if d == 0:
        return None if (loo or hio) else (lo, hi, False, False)
    return (lo, hi, loo, hio)


def _interval_pick(iv):
    """Some scale inside the interval, exactly in K."""
    lo, hi, loo, hio = iv
    if not loo:
        return lo
    if not hio:
        return hi
    return (lo + hi) * HALF


def good_at_direction(O, poly, v):
    """Exact: is the direction v good?  Returns (bool, s) with s in K a witness scale.

    Rebuilt from scratch out of `ray_scales`; it knows nothing about how v was found, so
    it doubles as the checker for every candidate the sweep proposes.
    """
    if is_zero_vec(v):
        raise ValueError("zero direction")
    S1 = ray_scales(O, poly, v)
    S2 = ray_scales(O, poly, rot(v, 1))
    best = None
    for i1 in S1:
        for i2 in S2:
            m = _interval_meet(i1, i2)
            if m is None:
                continue
            s = _interval_pick(m)
            if s.sgn() <= 0:
                continue
            if best is None or (s - best).sgn() < 0:
                best = s
    return (best is not None), best


# ----------------------------------------------------------------- the sweep
def _breakpoints(O, poly):
    """The finite direction set outside which the combinatorics cannot change."""
    D = []
    for Vv in poly:
        w = vsub(Vv, O)
        if is_zero_vec(w):
            continue                      # O itself is a vertex: it has no direction
        D.append(w)
        D.append(rot(w, -1))              # endpoint of rho^{-1}(arc of an edge)
    D.extend([V(1, 0), V(0, 1), V(-1, 0), V(0, -1)])
    seen = {}
    for w in D:
        seen.setdefault(dir_key(w), w)
    out = list(seen.values())
    out.sort(key=functools.cmp_to_key(dir_cmp))
    return out


def _transversals(O, poly):
    """(a, b, k, arc_start, arc_end) for every edge whose line misses O."""
    T = []
    for idx, (A, B) in enumerate(edges(poly)):
        a = vsub(A, O)
        b = vsub(B, O)
        k = cross(a, b)
        if k.is_zero():
            continue
        arc = (a, b) if k.sgn() > 0 else (b, a)
        T.append((idx, a, b, k, arc))
    return T


def _in_cone(v, a, b, k):
    al = cross(v, b)
    be = cross(a, v)
    if k.sgn() > 0:
        return al.sgn() >= 0 and be.sgn() >= 0
    return al.sgn() <= 0 and be.sgn() <= 0


def good_directions(O, poly, verify=True):
    """The complete exact good-direction set G(O).

    Returns a dict:
      good        bool
      atoms       the circular decomposition, in CCW order: alternating
                  {"kind":"point", "dir":v, "good":bool} and
                  {"kind":"gap", "a":u, "b":w, "full":bool, "points":[v,...]}
      components  list of components of G(O), each
                  {"type":"arc"|"point", "start":v, "end":v} (start == end for a point)
      n_components, n_arc_components, n_point_components
      witness     (P, Q, s, v) for one good direction, or None
    """
    D = _breakpoints(O, poly)
    T = _transversals(O, poly)
    m = len(D)

    atoms = []
    for i in range(m):
        u = D[i]
        w = D[(i + 1) % m]
        gu, _ = good_at_direction(O, poly, u)
        atoms.append({"kind": "point", "dir": u, "good": gu})
        rep = vadd(u, w)
        if is_zero_vec(rep):
            raise AssertionError("gap of exactly 180 degrees: breakpoint set is wrong")
        E1 = [t for t in T if _in_cone(rep, t[1], t[2], t[3])]
        rr = rot(rep, 1)
        E2 = [t for t in T if _in_cone(rr, t[1], t[2], t[3])]
        full = False
        pts = {}
        for (_i, a, b, k, _arc) in E1:
            for (_j, c, d, k2, _arc2) in E2:
                M = vsub(vscale(k, rot(vsub(d, c), -1)), vscale(k2, vsub(b, a)))
                if is_zero_vec(M):
                    full = True
                    continue
                for cand in (M, (-M[0], -M[1])):
                    if not in_arc(cand, u, w):
                        continue
                    if dir_cmp(cand, u) == 0 or dir_cmp(cand, w) == 0:
                        continue          # an endpoint, decided as a breakpoint
                    pts[dir_key(cand)] = cand
        plist = sorted(pts.values(), key=functools.cmp_to_key(
            lambda x, y: dir_cmp(_rel(u, x), _rel(u, y))))
        if verify:
            for v in plist:
                ok, _ = good_at_direction(O, poly, v)
                if not ok:
                    raise AssertionError("sweep proposed a direction the checker rejects")
            if full:
                ok, _ = good_at_direction(O, poly, rep)
                if not ok:
                    raise AssertionError("M=0 gap is not good at its representative")
        atoms.append({"kind": "gap", "a": u, "b": w, "full": full,
                      "points": [] if full else plist})

    comps = _components(atoms)
    wdir = None
    for c in comps:
        wdir = c["start"]
        break
    wit = None
    if wdir is not None:
        ok, s = good_at_direction(O, poly, wdir)
        if not ok:
            raise AssertionError("component start is not good")
        P = vadd(O, vscale(s, wdir))
        Q = vadd(O, vscale(s, rot(wdir, 1)))
        wit = (P, Q, s, wdir)
    return {
        "good": bool(comps),
        "atoms": atoms,
        "components": comps,
        "n_components": len(comps),
        "n_arc_components": sum(1 for c in comps if c["type"] == "arc"),
        "n_point_components": sum(1 for c in comps if c["type"] == "point"),
        "witness": wit,
    }


def _components(atoms):
    """Maximal runs of consecutive fully-good atoms, plus isolated interior points."""
    n = len(atoms)
    full = []
    for at in atoms:
        full.append(at["good"] if at["kind"] == "point" else at["full"])
    comps = []
    if all(full):
        comps.append({"type": "arc", "start": atoms[0]["dir"], "end": atoms[0]["dir"],
                      "whole_circle": True})
        return comps
    if any(full):
        start = next(i for i in range(n) if full[i] and not full[(i - 1) % n])
        i = start
        for _ in range(n):
            if full[i]:
                j = i
                run = [i]
                while full[(j + 1) % n]:
                    j = (j + 1) % n
                    run.append(j)
                    if j == i:
                        break
                s_at = atoms[run[0]]
                e_at = atoms[run[-1]]
                # A full gap forces both its endpoints good (the two edges realising M = 0
                # are met on the CLOSED cones), so a maximal run always begins and ends at
                # a breakpoint atom, and a run of length 1 is a single direction.
                assert s_at["kind"] == "point" and e_at["kind"] == "point", \
                    "a maximal good run must start and end at a breakpoint"
                sd, ed = s_at["dir"], e_at["dir"]
                comps.append({"type": "point" if len(run) == 1 else "arc",
                              "start": sd, "end": ed, "whole_circle": False})
                i = (j + 1) % n
                if i == start:
                    break
            else:
                i = (i + 1) % n
                if i == start:
                    break
    for at in atoms:
        if at["kind"] == "gap" and not at["full"]:
            for v in at["points"]:
                comps.append({"type": "point", "start": v, "end": v,
                              "whole_circle": False})
    return comps


def decide(O, poly):
    """Just the boolean plus a witness triangle.  Stops at the first good direction.

    Same sweep, short-circuited -- used for the bulk fixture comparison, where only the
    boolean is compared.
    """
    D = _breakpoints(O, poly)
    T = _transversals(O, poly)
    m = len(D)
    for i in range(m):
        u = D[i]
        ok, s = good_at_direction(O, poly, u)
        if ok:
            return True, _mk(O, u, s)
    for i in range(m):
        u = D[i]
        w = D[(i + 1) % m]
        rep = vadd(u, w)
        E1 = [t for t in T if _in_cone(rep, t[1], t[2], t[3])]
        rr = rot(rep, 1)
        E2 = [t for t in T if _in_cone(rr, t[1], t[2], t[3])]
        for (_i, a, b, k, _arc) in E1:
            for (_j, c, d, k2, _arc2) in E2:
                M = vsub(vscale(k, rot(vsub(d, c), -1)), vscale(k2, vsub(b, a)))
                if is_zero_vec(M):
                    ok, s = good_at_direction(O, poly, rep)
                    if not ok:
                        raise AssertionError("M=0 gap is not good")
                    return True, _mk(O, rep, s)
                for cand in (M, (-M[0], -M[1])):
                    if not in_arc(cand, u, w):
                        continue
                    ok, s = good_at_direction(O, poly, cand)
                    if ok:
                        return True, _mk(O, cand, s)
    return False, None


def _mk(O, v, s):
    return (vadd(O, vscale(s, v)), vadd(O, vscale(s, rot(v, 1))), s, v)


def recheck_witness(poly, O, P, Q):
    """Independent re-check of a reported triangle.  Knows nothing about how it was found:
    all three on J, pairwise distinct, pairwise equidistant, positive side."""
    d = {
        "O_on_J": point_on_polygon(O, poly),
        "P_on_J": point_on_polygon(P, poly),
        "Q_on_J": point_on_polygon(Q, poly),
        "distinct": (not veq(O, P)) and (not veq(O, Q)) and (not veq(P, Q)),
    }
    s1 = norm2(vsub(P, O))
    s2 = norm2(vsub(Q, O))
    s3 = norm2(vsub(Q, P))
    d["equilateral"] = (s1 == s2) and (s2 == s3)
    d["nondegenerate"] = s1.sgn() > 0
    d["side2"] = s1.pair()
    d["side_display"] = float(s1) ** 0.5
    ok = all(d[k] for k in ("O_on_J", "P_on_J", "Q_on_J", "distinct",
                            "equilateral", "nondegenerate"))
    return ok, d
