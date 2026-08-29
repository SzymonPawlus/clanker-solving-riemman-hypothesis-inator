"""The angular decision procedure for the inscribed-equilateral-triangle vertex problem.

THE CRITERION (R)
=================
Let J be a closed curve and O in J.  Call O *good* if some nondegenerate equilateral
triangle has all three vertices on J, one of them equal to O.  Write rho for rotation by
+60 degrees about O and u(t) for the unit vector at angle t.

    (R)   O is good  <=>  there exist an angle t and a radius r > 0 with
                          O + r u(t) in J   AND   O + r u(t+60) in J.

Proof.
(<=)  Put A = O + r u(t), B = O + r u(t+60).  Then |OA| = |OB| = r > 0 and the angle AOB
      is exactly 60 degrees.  A triangle that is isoceles with apex angle 60 has base
      angles (180-60)/2 = 60, so OAB is equiangular, hence equilateral, with side r > 0.
      It is nondegenerate: r > 0 gives A, B != O, and the 60-degree separation gives
      A != B.  All three vertices lie on J.
(=>)  Let O, A, B be equilateral, nondegenerate, all on J, side s > 0.  Then |OA| = |OB| = s
      and the angle AOB is 60 degrees, so writing A = O + s u(alpha), B = O + s u(beta) we
      have beta - alpha = +-60 (mod 360).  If beta = alpha + 60 take (t, r) = (alpha, s);
      if beta = alpha - 60 take (t, r) = (beta, s).  Either way (R) holds.               []

Two consequences worth stating, because both matter for the implementation:

*  ONE ROTATION SIGN SUFFICES.  (R) quantifies over all t, and the pair {t, t+60} is the
   same object whether it is read as "t rotated by +60" or "t+60 rotated by -60".  The
   sigma = -1 branch of the rotation-based decider is therefore redundant *as a decision*
   (it can still surface a different witness first).  This is checked empirically in
   run.py --mode selftest.
*  r > 0 IS THE WHOLE DEGENERACY QUESTION.  r = 0 gives the "triangle" O, O, O and is
   available for every O and every t.  Every radial set built below excludes 0 by
   construction, which is where this implementation pays the debt that the rotation
   picture pays by discarding the fixed point O of the rotation.

THE ALGORITHM
=============
Define the (multivalued) radial set of J at O in direction t:

    R(t) = { r > 0 : O + r u(t) in J }.

For a simple polygon J = union of closed edges, R(t) is a finite union of points and closed
intervals, and (R) reads:  O is good  <=>  R(t) meets R(t+60) for some t.

The set is assembled edge by edge.  Fix an edge e = [A, B] and put a = A - O, b = B - O and
k = cross(a, b).

  * k != 0 (O is NOT on the line of e).  The ray from O in direction v meets e iff v lies in
    the closed arc Arc(e) from a to b, an arc of width < 180 degrees because the whole
    segment is strictly on one side of O.  There the meet is a single point at parameter
    s(v) = k / cross(v, b - a) > 0, i.e. at radius^2 = k^2 |v|^2 / cross(v, b-a)^2.
    Call this a TRANSVERSAL contribution.

  * k == 0 (O is on the line of e).  Then only the one or two directions along that line
    see e at all, and each sees a whole closed interval of radii.  Call this a COLLINEAR
    contribution.  This case is not exotic: if O is a vertex of the polygon, BOTH edges at
    O are collinear contributions, and if O is interior to an edge, that edge contributes
    two opposite directions.

Now take an ordered pair of edges (e, f) and ask for the directions v with the ray at v
meeting e and the ray at rho(v) meeting f, at a COMMON radius.  For two transversal
contributions the common-radius equation is

      k_e / cross(v, b - a)  =  k_f / cross(rho v, d - c)

(the |v| factors cancel because |rho v| = |v|), and cross(rho v, m) = cross(v, rho^{-1} m)
because a rotation preserves the cross product.  Cross-multiplying -- legitimate, since on
the domain both denominators are nonzero -- and using bilinearity of the cross product:

      cross( v ,  k_e * rho^{-1}(d - c) - k_f * (b - a) ) = 0,        (*)

a single LINEAR condition on the direction v.  Writing M for the vector in (*):

      M != 0  ->  the only candidate directions are +-M, each then tested for membership
                  in Arc(e) and rho^{-1} Arc(f);
      M == 0  ->  the radii agree identically, and the entire arc Arc(e) & rho^{-1} Arc(f)
                  consists of good directions.

M = 0 happens exactly when the line of f is the 60-degree rotation about O of the line of e
(equal distance from O, direction rotated) -- the only way an inscribed triangle at O can
come in a one-parameter family.  Mixed transversal/collinear and collinear/collinear pairs
are finitely many direct checks (a fixed direction, then an exact comparison of squared
radii).

The output is therefore the exact GOOD-DIRECTION SET

    G(O) = { t : R(t) meets R(t+60) },

a finite union of closed arcs and isolated directions, with exact endpoints in K^2.  O is
good iff G(O) is nonempty.

WHY THIS IS NOT THE ROTATION ALGORITHM
--------------------------------------
The committed experiment `experiments/inscribed-triangle-polygons/` decides goodness by
intersecting the polygon with its own 60-degree rotate, i.e. by O(n^2) segment-segment
intersections in the plane, solving for two segment parameters and discarding components
equal to {O}.  This module never intersects two segments.  It works in direction space:
one linear form per ordered edge pair, membership tests in circular arcs, and comparisons
of squared radii.  The degeneracies land in different places (there: collinear overlap of a
rotated edge with an edge; here: M = 0), and the output is different in kind -- the whole
set G(O), not one witness.  Agreement between the two is therefore worth something.

Everything below is exact.  float() appears only in *_display fields.
"""

from __future__ import annotations

from fractions import Fraction

from q3 import Q3, ZERO, ONE, HALF, S60, C60

__all__ = [
    "V", "vsub", "vadd", "vscale", "cross", "dot", "norm2", "veq", "is_zero_vec",
    "rot", "dir_canon", "dir_eq", "dir_cmp", "in_arc", "arc_inter", "arc_contains_arc",
    "edges", "point_on_segment", "point_on_polygon", "is_simple", "is_convex",
    "signed_area2", "good_directions", "recheck_witness", "interior_angle_info",
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


def rot(v, sign=1):
    """Rotate the VECTOR v by sign*60 degrees (sign in {+1,-1}).  Exact in K."""
    s = S60 if sign == 1 else -S60
    return (C60 * v[0] - s * v[1], s * v[0] + C60 * v[1])


def rot_about(p, o, sign=1):
    return vadd(o, rot(vsub(p, o), sign))


# ------------------------------------------------------------------ directions
# A direction is a nonzero vector taken up to POSITIVE scaling.

def dir_canon(v):
    """Canonical representative of the direction of v under positive scaling.

    Divides by |first nonzero coordinate|, which is a positive scalar, so the direction is
    unchanged and the result is unique.  Used only for hashing / deduplication.
    """
    c = v[0] if not v[0].is_zero() else v[1]
    m = abs(c)
    return (v[0] / m, v[1] / m)


def dir_key(v):
    return (dir_canon(v)[0]._ab, dir_canon(v)[1]._ab)


def dir_eq(u, v):
    """Same direction (not merely the same line)."""
    return cross(u, v).is_zero() and dot(u, v).sgn() > 0


def _half(v):
    """0 for angle in [0,180), 1 for angle in [180,360)."""
    sy = v[1].sgn()
    if sy > 0:
        return 0
    if sy < 0:
        return 1
    return 0 if v[0].sgn() > 0 else 1


def dir_cmp(u, v):
    """Total order on directions by angle measured CCW from the +x axis, in [0,360)."""
    hu, hv = _half(u), _half(v)
    if hu != hv:
        return -1 if hu < hv else 1
    s = cross(u, v).sgn()
    if s > 0:
        return -1
    if s < 0:
        return 1
    return 0


def _rel(base, v):
    """v expressed in the frame whose +x axis is `base`: a positive multiple of the
    rotation of v by -angle(base).  Direction-preserving because |base|^2 > 0."""
    return (dot(base, v), cross(base, v))


def in_arc(v, a, b):
    """Is direction v in the closed arc running CCW from direction a to direction b?

    Works for any arc of width < 360.  The degenerate a == b is the single direction a.
    """
    rv = _rel(a, v)
    rb = _rel(a, b)
    return dir_cmp(rv, rb) <= 0


def arc_inter(a1, b1, a2, b2):
    """Intersection of two closed CCW arcs [a1,b1], [a2,b2], each of width < 180 degrees.

    Returns a list of (start, end) arcs (possibly empty; at most two components in
    general, though widths < 180 make two impossible -- the code does not rely on that).
    """
    out = []
    for s in (a1, a2):
        if in_arc(s, a1, b1) and in_arc(s, a2, b2):
            # the arc from s runs to whichever of b1, b2 comes first
            e = b1 if dir_cmp(_rel(s, b1), _rel(s, b2)) <= 0 else b2
            out.append((s, e))
    # deduplicate / absorb
    res = []
    for (s, e) in out:
        dup = False
        for (s2, e2) in res:
            if dir_cmp(s, s2) == 0 and dir_cmp(e, e2) == 0:
                dup = True
                break
        if not dup:
            res.append((s, e))
    if len(res) == 2:
        (s1, e1), (s2, e2) = res
        if in_arc(s2, s1, e1) and in_arc(e2, s1, e1):
            return [(s1, e1)]
        if in_arc(s1, s2, e2) and in_arc(e1, s2, e2):
            return [(s2, e2)]
    return res


def arc_contains_arc(a, b, s, e):
    return in_arc(s, a, b) and in_arc(e, a, b) and dir_cmp(_rel(a, s), _rel(a, e)) <= 0


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
    """Do the closed segments [a,b] and [c,d] share at least one point?  (Boolean only --
    this is used for the simplicity check, never for a goodness decision.)"""
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
                shared = E[i][1] if j == i + 1 else E[i][0]
                # adjacent edges must meet exactly in the shared vertex
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
    """Interior-angle classification at vertex i.  cmp60 in {-1,0,+1}; display degrees."""
    import math
    n = len(poly)
    Vv = poly[i]
    U = poly[(i - 1) % n]
    W = poly[(i + 1) % n]
    u = vsub(U, Vv)
    w = vsub(W, Vv)
    orient = signed_area2(poly).sgn()
    turn = cross(vsub(Vv, U), vsub(W, Vv)).sgn()
    reflex = (turn * orient) < 0
    c = dot(u, w)
    s = cross(u, w)
    if reflex or c.sgn() <= 0:
        cmp60 = 1
    else:
        d = (s * s) - Q3(3) * (c * c)
        sg = d.sgn()
        cmp60 = -1 if sg < 0 else (0 if sg == 0 else 1)
    ang = math.degrees(math.atan2(abs(float(s)), float(c)))
    if reflex:
        ang = 360.0 - ang
    return {"reflex": reflex, "cmp60": cmp60, "degrees_display": ang}


# ------------------------------------------------------- radial contributions
def edge_contribution(O, A, B):
    """Radial data of the edge [A,B] as seen from O.

    Returns ("T", a, b, k)  with k = cross(a,b) != 0, arc from a to b (width < 180); or
            ("C", entries)  with entries a list of (direction, r2lo, r2hi, lo_open).
    """
    a = vsub(A, O)
    b = vsub(B, O)
    k = cross(a, b)
    if not k.is_zero():
        return ("T", a, b, k)
    # O lies on the line of the edge
    za, zb = is_zero_vec(a), is_zero_vec(b)
    if za and zb:
        raise ValueError("zero-length edge")
    if za:                       # O == A: radii (0, |b|]
        return ("C", [(b, ZERO, norm2(b), True)])
    if zb:                       # O == B
        return ("C", [(a, ZERO, norm2(a), True)])
    if dot(a, b).sgn() > 0:      # O outside the segment, on its line
        na, nb = norm2(a), norm2(b)
        lo, hi = (na, nb) if na <= nb else (nb, na)
        return ("C", [(a, lo, hi, False)])
    # O strictly inside the segment: two opposite directions, each a half-open interval
    return ("C", [(a, ZERO, norm2(a), True), (b, ZERO, norm2(b), True)])


def _r2_transversal(v, a, b, k):
    """Squared radius at which the ray in direction v meets the transversal edge."""
    den = cross(v, vsub(b, a))
    assert not den.is_zero(), "ray parallel to a transversal edge inside its arc"
    return (k * k) * norm2(v) / (den * den)


def _interval_has(r2, lo, hi, lo_open):
    if lo_open:
        if (r2 - lo).sgn() <= 0:
            return False
    else:
        if (r2 - lo).sgn() < 0:
            return False
    return (r2 - hi).sgn() <= 0


def _intervals_meet(i1, i2):
    lo1, hi1, o1 = i1
    lo2, hi2, o2 = i2
    lo, lo_open = (lo1, o1) if (lo1 - lo2).sgn() >= 0 else (lo2, o2)
    if (lo1 - lo2).sgn() == 0:
        lo_open = o1 or o2
    hi = hi1 if (hi1 - hi2).sgn() <= 0 else hi2
    c = (lo - hi).sgn()
    if c > 0:
        return False
    if c == 0:
        return not lo_open
    return True


# ------------------------------------------------------------- the decision
def good_directions(poly, O, collect_all=True):
    """Exact good-direction set G(O) for O on the boundary of `poly`.

    Returns a dict with
      good        : bool
      arcs        : list of (start_dir, end_dir) exact K^2 arcs of good directions
      points      : list of isolated good directions (not covered by any arc)
      raw         : every (pair, kind, direction/arc) hit before merging, for diagnostics
      witness     : an explicit inscribed triangle (P, Q) with O,P,Q equilateral, or None
    Directions are exact vectors in K^2, taken up to positive scaling.
    """
    E = edges(poly)
    contribs = [edge_contribution(O, A, B) for (A, B) in E]
    n = len(E)

    raw_points = []   # (dir, meta)
    raw_arcs = []     # (start, end, meta)

    for i in range(n):
        ce = contribs[i]
        for j in range(n):
            cf = contribs[j]
            meta = (i, j)
            if ce[0] == "T" and cf[0] == "T":
                _, a, b, k = ce
                _, c, d, k2 = cf
                # M = k * rho^{-1}(d - c) - k2 * (b - a)
                M = vsub(vscale(k, rot(vsub(d, c), -1)), vscale(k2, vsub(b, a)))
                arc_e = (a, b) if k.sgn() > 0 else (b, a)
                cc, dd = rot(c, -1), rot(d, -1)
                arc_f = (cc, dd) if k2.sgn() > 0 else (dd, cc)
                if is_zero_vec(M):
                    for (s, e) in arc_inter(arc_e[0], arc_e[1], arc_f[0], arc_f[1]):
                        if dir_cmp(s, e) == 0:
                            raw_points.append((s, meta + ("TT-M0-pt",)))
                        else:
                            raw_arcs.append((s, e, meta + ("TT-M0-arc",)))
                else:
                    for v in (M, (-M[0], -M[1])):
                        if in_arc(v, arc_e[0], arc_e[1]) and in_arc(v, arc_f[0], arc_f[1]):
                            raw_points.append((v, meta + ("TT",)))
            elif ce[0] == "T" and cf[0] == "C":
                _, a, b, k = ce
                arc_e = (a, b) if k.sgn() > 0 else (b, a)
                for (w, lo, hi, op) in cf[1]:
                    v = rot(w, -1)
                    if not in_arc(v, arc_e[0], arc_e[1]):
                        continue
                    r2 = _r2_transversal(v, a, b, k)
                    if _interval_has(r2, lo, hi, op):
                        raw_points.append((v, meta + ("TC",)))
            elif ce[0] == "C" and cf[0] == "T":
                _, c, d, k2 = cf
                arc_f = (c, d) if k2.sgn() > 0 else (d, c)
                for (w, lo, hi, op) in ce[1]:
                    rv = rot(w, 1)
                    if not in_arc(rv, arc_f[0], arc_f[1]):
                        continue
                    r2 = _r2_transversal(rv, c, d, k2)
                    if _interval_has(r2, lo, hi, op):
                        raw_points.append((w, meta + ("CT",)))
            else:
                for (w1, lo1, hi1, o1) in ce[1]:
                    rv = rot(w1, 1)
                    for (w2, lo2, hi2, o2) in cf[1]:
                        if not dir_eq(rv, w2):
                            continue
                        if _intervals_meet((lo1, hi1, o1), (lo2, hi2, o2)):
                            raw_points.append((w1, meta + ("CC",)))

    arcs = _merge_arcs(raw_arcs)
    pts = []
    seen = set()
    for (v, meta) in raw_points:
        if any(in_arc(v, s, e) for (s, e) in arcs):
            continue
        kk = dir_key(v)
        if kk in seen:
            continue
        seen.add(kk)
        pts.append(v)
    pts.sort(key=_sort_key)

    out = {
        "good": bool(arcs or pts),
        "arcs": arcs,
        "points": pts,
        "n_raw_points": len(raw_points),
        "n_raw_arcs": len(raw_arcs),
    }
    # an explicit witness, from the first arc start or first isolated direction
    wdir = arcs[0][0] if arcs else (pts[0] if pts else None)
    out["witness"] = _witness_for(poly, O, wdir) if wdir is not None else None
    return out


def _sort_key(v):
    c = dir_canon(v)
    return (_half(v), float(c[0]), float(c[1]))


def _merge_arcs(raw):
    """Union of closed CCW arcs, each of width < 180 degrees."""
    arcs = [(s, e) for (s, e, _m) in raw]
    changed = True
    while changed and len(arcs) > 1:
        changed = False
        out = []
        used = [False] * len(arcs)
        for i in range(len(arcs)):
            if used[i]:
                continue
            s, e = arcs[i]
            for j in range(i + 1, len(arcs)):
                if used[j]:
                    continue
                s2, e2 = arcs[j]
                if arc_contains_arc(s, e, s2, e2):
                    used[j] = True
                    changed = True
                elif arc_contains_arc(s2, e2, s, e):
                    s, e = s2, e2
                    used[j] = True
                    changed = True
                elif in_arc(s2, s, e):          # overlap: s..e..  s2..e2
                    if not in_arc(e2, s, e):
                        e = e2
                        used[j] = True
                        changed = True
                elif in_arc(s, s2, e2):
                    s = s2
                    if not in_arc(e, s2, e2):
                        pass
                    else:
                        e = e2
                    used[j] = True
                    changed = True
            used[i] = True
            out.append((s, e))
        arcs = out
    return arcs


def _witness_for(poly, O, v):
    """Rebuild the actual triangle (O, P, Q) for a good direction v, exactly.

    Recomputes the radius from scratch: it takes the smallest squared radius that the ray
    at v and the ray at rho(v) have in common, found by enumerating both radial sets.
    """
    E = edges(poly)
    rv = rot(v, 1)
    set1 = _radii_at(O, E, v)
    set2 = _radii_at(O, E, rv)
    best = None
    for (lo1, hi1, o1) in set1:
        for (lo2, hi2, o2) in set2:
            if not _intervals_meet((lo1, hi1, o1), (lo2, hi2, o2)):
                continue
            lo = lo1 if (lo1 - lo2).sgn() >= 0 else lo2
            if lo.sgn() == 0:
                # both intervals open at 0 -> take a point strictly inside
                hi = hi1 if (hi1 - hi2).sgn() <= 0 else hi2
                lo = hi
            if best is None or (lo - best).sgn() < 0:
                best = lo
    if best is None:
        return None
    # r^2 = best; the actual points are O + (r/|v|) v with r^2 = best
    # scale^2 = best / |v|^2 ; we need the point exactly, so use the radial set's own
    # parametrisation: find the point on the ray at squared distance `best`.
    return _point_at(O, v, best), _point_at(O, rv, best), best


def _radii_at(O, E, v):
    """The radial set in direction v as a list of (lo2, hi2, lo_open) squared-radius
    intervals (a single point is (r2, r2, False))."""
    out = []
    for (A, B) in E:
        c = edge_contribution(O, A, B)
        if c[0] == "T":
            _, a, b, k = c
            arc = (a, b) if k.sgn() > 0 else (b, a)
            if in_arc(v, arc[0], arc[1]):
                r2 = _r2_transversal(v, a, b, k)
                out.append((r2, r2, False))
        else:
            for (w, lo, hi, op) in c[1]:
                if dir_eq(w, v):
                    out.append((lo, hi, op))
    return out


def _point_at(O, v, r2):
    """The point O + r*v/|v| with r^2 = r2 -- exact when r2/|v|^2 is a square in K.

    Used only for witness reporting; if the scale is not exactly representable the caller
    gets None and falls back to reporting the direction alone.
    """
    lam2 = r2 / norm2(v)
    lam = _sqrt_in_K(lam2)
    if lam is None:
        return None
    return vadd(O, vscale(lam, v))


def _sqrt_in_K(x):
    """Exact square root in Q(sqrt 3) if one exists, else None.

    x = a + b sqrt3.  If b == 0 and a is a rational square, done.  Otherwise look for
    y = p + q sqrt3 with p^2 + 3q^2 = a and 2pq = b; then p^2 is a root of
    4 t^2 - 4 a t + b^2 * 3 ... solved directly below with rational square tests.
    """
    a, b = x.a, x.b
    if x.sgn() < 0:
        return None
    if b == 0:
        r = _rat_sqrt(a)
        return Q3(r, 0) if r is not None else None
    # p^2 + 3 q^2 = a, 2 p q = b  =>  p^2 = (a +- sqrt(a^2 - 3 b^2)) / 2
    disc = a * a - 3 * b * b
    if disc < 0:
        return None
    sd = _rat_sqrt(disc)
    if sd is None:
        return None
    for sgn in (1, -1):
        p2 = (a + sgn * sd) / 2
        if p2 < 0:
            continue
        p = _rat_sqrt(p2)
        if p is None or p == 0:
            continue
        q = b / (2 * p)
        cand = Q3(p, q)
        if (cand * cand) == x and cand.sgn() > 0:
            return cand
        cand = Q3(-p, -q)
        if (cand * cand) == x and cand.sgn() > 0:
            return cand
    return None


def _rat_sqrt(r: Fraction):
    if r < 0:
        return None
    num, den = r.numerator, r.denominator
    sn, sd = _isqrt_exact(num), _isqrt_exact(den)
    if sn is None or sd is None:
        return None
    return Fraction(sn, sd)


def _isqrt_exact(n: int):
    import math
    if n < 0:
        return None
    r = math.isqrt(n)
    return r if r * r == n else None


def recheck_witness(poly, O, P, Q):
    """Independent re-check of a reported triangle: all three on J, pairwise distinct,
    pairwise equidistant.  Knows nothing about how the triangle was found."""
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
