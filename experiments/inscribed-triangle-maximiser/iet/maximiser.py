"""An exact MAXIMISER for inscribed equilateral triangles on a simple polygon.

The two committed lanes -- `experiments/inscribed-triangle-polygons/` and
`experiments/inscribed-triangle-angular/` -- answer

        is there ANY nondegenerate equilateral triangle inscribed in J with a vertex at O?

and both short-circuit at the first witness.  This module answers

        what is the LARGEST such triangle?                      (per-O maximiser, exact)
        what is the largest one anywhere on J?                  (global maximiser, exact)

Everything below is exact in K = Q(sqrt 3) (`qs3.py`).  Sides are never taken: the module
compares and reports side^2, which lies in K.


1.  The per-O maximiser
=======================
Fix O on the polygon and let rho be the rotation by +60 degrees about O.  As in the angular
lane's criterion (R), which is re-derived here rather than imported:

    (O, P, Q) is a nondegenerate inscribed equilateral triangle with P = rho(Q) or
    Q = rho(P)   <=>   for some direction v and some scale s > 0 the two points O + s v and
    O + s rho_0(v) both lie on the polygon,     rho_0 = rotation of VECTORS by +60.

(=>) is the isoceles-with-60-degree-apex closure; (<=) is the same computation read
backwards.  Sweeping v over ALL directions covers both chiralities, so only +60 appears.

Directions are nonzero vectors of K^2 taken up to positive scaling -- never unit vectors --
which is what keeps the field at Q(sqrt 3): the witness triangle is (O, O + s v, O + s
rho_0 v) with s in K, and its side^2 = s^2 |v|^2 is in K.

Define the scale set of a direction,   S(v) = { s > 0 : O + s v lies on the polygon }.
Each edge contributes to S(v) either nothing, or one scale (when the edge's line misses O),
or a whole closed interval of scales (when O lies on the edge's line and the ray runs along
it).  So S(v) is a finite union of points and closed intervals, computed exactly.  Then

    maxside2(O) = max { s^2 |v|^2 : v a direction, s in S(v) ∩ S(rho_0 v) }.

**Where the maximum can sit -- the finite candidate set.**  Let e = [A,B] and f = [C,D] be
edges whose lines miss O, put a = A-O, b = B-O, c = C-O, d = D-O, k_e = cross(a,b) != 0,
k_f = cross(c,d) != 0.  Inside the cone of e the ray at v meets e at the single scale
s_e(v) = k_e / cross(v, b-a), and the ray at rho_0 v meets f at s_f(v) = k_f / cross(rho_0
v, d-c) = k_f / cross(v, rho_0^{-1}(d-c)) (a rotation preserves the cross product).  The two
denominators are nonzero there, so

        s_e(v) = s_f(v)   <=>   cross(v, M_ef) = 0,
        M_ef = k_e * rho_0^{-1}(d - c)  -  k_f * (b - a).                        (*)

Hence for a pair (e,f) with M_ef != 0 the only directions that can realise it are +-M_ef,
and for a pair with M_ef = 0 the pair is realised on a whole arc, on which

        side^2(v) = k_e^2 |v|^2 / cross(v, b-a)^2 = k_e^2 / (|b-a|^2 sin^2 t),

t the angle from v to b-a.  On the arc, sin t never vanishes (a ray parallel to a
transversal edge cannot meet it), so t stays inside an open half turn, where |sin| is
concave and therefore attains its MINIMUM at an endpoint of the arc.  So side^2 attains its
maximum at an endpoint of the arc -- and the arc's endpoints are directions of the form
(V - O) or rho_0^{-1}(V - O) for polygon vertices V, because the arc is
cone(a,b) ∩ rho_0^{-1} cone(c,d).

Every non-transversal edge -- one whose line passes through O -- is met only in directions
along that line, which are again of the form (V - O) or rho_0^{-1}(V - O).

    CANDIDATES:   { V - O, rho_0^{-1}(V - O) : V a vertex, V != O }
                  ∪ { ±M_ef : e, f transversal edges, M_ef != 0 }.

That set is finite (O(n^2)), and by the three paragraphs above it contains a maximiser.
Each candidate is then scored by rebuilding S(v) and S(rho_0 v) FROM SCRATCH and taking the
largest common scale, so the scorer knows nothing about how the direction was proposed and
doubles as the checker for it.

This is deliberately *not* the angular lane's algorithm.  That lane sweeps a circular
sequence of gaps and needs cone bookkeeping to know which edges are live on each gap; this
one enumerates all ordered edge pairs, proposes both signs unconditionally, and lets the
independent scorer discard the ones that do not realise.  The shared content is the algebra
(*), which was re-derived here before that file was read in detail.


2.  The global maximiser
========================
> **Lemma V (mine, `sketch`).**  Let P be a simple polygon and let T be an inscribed
> equilateral triangle of maximal side.  Then at least one vertex of T is a VERTEX of P.

*Proof.*  The maximum is attained: the set of triples on the compact set bd(P) satisfying
the two exact equations |XY| = |YZ| = |ZX| and the closed condition side^2 >= s0^2 (any
s0 > 0 below the max) is compact, and side is continuous.  Suppose all three vertices of a
maximiser T lie in the relative interiors of edges.

*Case 1: three distinct edge lines.*  Write them ⟨x,n_i⟩ = c_i.  With the vertices
A, A + s u, A + s rho_0 u (u a unit vector of angle t) the incidences are three linear
equations in the three unknowns (A_x, A_y, s):

        ⟨A,n_1⟩ = c_1,  ⟨A,n_2⟩ + s⟨u,n_2⟩ = c_2,  ⟨A,n_3⟩ + s⟨rho_0 u,n_3⟩ = c_3.

Expanding the determinant along the third column, det = ⟨u, alpha⟩ for a FIXED vector alpha
depending only on the n_i, while Cramer's numerator for s is the determinant of the matrix
whose columns are n_1, n_2, n_3 and c -- a constant K independent of u.  So along the
one-parameter family

        s(t) = K / ⟨u(t), alpha⟩ = K / (|alpha| cos(t - t_0)).

If alpha != 0 then on the range where s > 0 the only critical point of s is t = t_0, where
cos is maximal and s is therefore minimal: an interior local MAXIMUM of s is impossible, so
T can be grown while all three vertices stay in their (relatively open) edges -- contra
maximality.  If alpha = 0 and K = 0 the three lines are concurrent and any solution can be
dilated about the common point, again growing T; if alpha = 0 and K != 0 there is no
solution at all.

*Case 2: only two distinct edge lines*, say A, A + su on L_1 and A + s rho_0 u on L_2.
Subtracting the first two incidences gives s⟨u,n_1⟩ = 0, so u is along L_1 and only the
position of A along L_1 is free; the third incidence makes s an affine function of that
position, which is either non-constant (grow it) or constant (then the whole family has the
same side, and its closure contains a configuration with a vertex at an edge endpoint).
Either way a maximiser with a vertex of P among its vertices exists.  Three vertices on one
line is degenerate and excluded.  []

Consequently  max_{O in bd P} maxside2(O)  =  max_{V a vertex of P} maxside2(V),  and the
global maximiser is exact: finitely many exact per-O computations.  Lemma V is my own
argument and carries status `sketch` (`../../RULES.md` §3); the *computation* at each vertex
is exact regardless, so `global_max` also offers a `sampled` mode that re-runs the exact
per-O maximiser at many rational interior edge points as an independent corroboration that
no interior O beats the vertices.
"""

from __future__ import annotations

from fractions import Fraction

from .qs3 import Q3, ZERO, ONE, HALF, C60, S60

__all__ = [
    "V", "vadd", "vsub", "vscale", "cross", "dot", "norm2", "veq", "is_zero_vec",
    "rot", "dir_key", "vfloat", "vpair", "edges", "point_on_segment", "point_on_polygon",
    "signed_area2", "is_simple", "is_convex",
    "scale_set", "max_scale_at_direction", "candidate_directions",
    "max_at_point", "global_max", "verify_triangle", "triangle_at",
    "edge_sample_points",
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
    """Rotate the VECTOR v by sign*60 degrees.  Exact: cos60 = 1/2, sin60 = sqrt3/2."""
    s = S60 if sign == 1 else -S60
    return (C60 * v[0] - s * v[1], s * v[0] + C60 * v[1])


def dir_key(v):
    """Canonical key for a direction (a nonzero vector up to POSITIVE scaling)."""
    c = v[0] if not v[0].is_zero() else v[1]
    m = abs(c)
    x, y = v[0] / m, v[1] / m
    return ((x.a, x.b, x.c), (y.a, y.b, y.c))


def vfloat(p):
    return [float(p[0]), float(p[1])]


def vpair(p):
    return [p[0].pair(), p[1].pair()]


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
    t0 = dot(qp, r) / rr
    t1 = t0 + dot(s, r) / rr
    lo, hi = (t0, t1) if (t1 - t0).sgn() >= 0 else (t1, t0)
    return (hi.sgn() >= 0) and ((lo - ONE).sgn() <= 0)


def is_simple(poly):
    """Exact Jordan check for the closed polygonal curve."""
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
            elif _seg_meets(a, b, c, d):
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


# ------------------------------------------------------- scale sets on one ray
# An interval is (lo, hi, lo_open): the scales s with lo <= s <= hi, excluding lo when
# lo_open.  hi is always attained.  Every scale in every interval is > 0 except possibly
# the excluded left endpoint 0, which is the degenerate "triangle" (O, O, O).

def _edge_scales(O, A, B, v):
    a = vsub(A, O)
    b = vsub(B, O)
    k = cross(a, b)
    if not k.is_zero():
        # O is off the line of [A,B]: the ray meets the edge in at most one point, and
        # only if v lies in the closed cone spanned by a and b.
        al = cross(v, b)
        be = cross(a, v)
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
        return [(s, s, False)]
    # O lies on the line of [A,B]: the ray meets the edge in a whole interval, or not at all.
    n2 = norm2(v)
    ta = _ratio(a, v, n2)
    tb = _ratio(b, v, n2)
    if ta is None or tb is None:
        return []
    lo, hi = (ta, tb) if (ta - tb).sgn() <= 0 else (tb, ta)
    if hi.sgn() <= 0:
        return []
    if lo.sgn() > 0:
        return [(lo, hi, False)]
    return [(ZERO, hi, True)]


def _ratio(w, v, n2):
    """t with w = t v, else None."""
    if not cross(v, w).is_zero():
        return None
    return dot(w, v) / n2


def scale_set(O, poly, v):
    """S(v) = { s > 0 : O + s v lies on the polygon }, as a list of intervals."""
    if is_zero_vec(v):
        raise ValueError("zero direction")
    out = []
    for (A, B) in edges(poly):
        out.extend(_edge_scales(O, A, B, v))
    return out


def _meet_sup(i1, i2):
    """The LARGEST scale in the intersection of two intervals, or None if empty."""
    lo1, hi1, o1 = i1
    lo2, hi2, o2 = i2
    cl = (lo1 - lo2).sgn()
    if cl > 0:
        lo, loo = lo1, o1
    elif cl < 0:
        lo, loo = lo2, o2
    else:
        lo, loo = lo1, (o1 or o2)
    hi = hi1 if (hi1 - hi2).sgn() <= 0 else hi2
    d = (lo - hi).sgn()
    if d > 0:
        return None
    if d == 0 and loo:
        return None
    if hi.sgn() <= 0:
        return None
    return hi


def max_scale_at_direction(O, poly, v):
    """The largest s > 0 with O + s v and O + s rho_0(v) both on the polygon, or None.

    Rebuilt from scratch; it is told nothing about where v came from.
    """
    S1 = scale_set(O, poly, v)
    S2 = scale_set(O, poly, rot(v, 1))
    best = None
    for i1 in S1:
        for i2 in S2:
            s = _meet_sup(i1, i2)
            if s is None:
                continue
            if best is None or (s - best).sgn() > 0:
                best = s
    return best


# ------------------------------------------------------------ candidate directions
def _transversals(O, poly):
    T = []
    for (A, B) in edges(poly):
        a = vsub(A, O)
        b = vsub(B, O)
        k = cross(a, b)
        if not k.is_zero():
            T.append((a, b, k))
    return T


def candidate_directions(O, poly):
    """The finite set proved in the module docstring to contain a maximiser."""
    out = {}

    def add(w):
        if not is_zero_vec(w):
            out.setdefault(dir_key(w), w)

    for Vv in poly:
        w = vsub(Vv, O)
        if is_zero_vec(w):
            continue
        add(w)                 # the ray at v hits the vertex V
        add(rot(w, -1))        # the ray at rho_0 v hits the vertex V

    T = _transversals(O, poly)
    for (a, b, k) in T:
        ba = vsub(b, a)
        for (c, d, k2) in T:
            M = vsub(vscale(k, rot(vsub(d, c), -1)), vscale(k2, ba))
            if is_zero_vec(M):
                continue       # a whole arc: its maximum sits at an arc endpoint, and
                               # every arc endpoint is already a vertex direction above
            add(M)
            add((-M[0], -M[1]))
    return list(out.values())


def triangle_at(O, v, s):
    return (vadd(O, vscale(s, v)), vadd(O, vscale(s, rot(v, 1))))


def max_at_point(O, poly, check=True):
    """EXACT largest inscribed equilateral triangle with a vertex at O.

    Returns {"good", "side2", "scale", "dir", "P", "Q", "n_candidates"}; side2 is the exact
    maximum of side^2 over all nondegenerate inscribed equilateral triangles with a vertex
    at O, and (P, Q) the other two vertices of a maximiser.
    """
    assert point_on_polygon(O, poly), "O must lie on the polygon"
    cands = candidate_directions(O, poly)
    best = None
    for v in cands:
        s = max_scale_at_direction(O, poly, v)
        if s is None:
            continue
        side2 = s * s * norm2(v)
        if best is None or (side2 - best[0]).sgn() > 0:
            best = (side2, s, v)
    res = {"good": best is not None, "n_candidates": len(cands),
           "side2": None, "scale": None, "dir": None, "P": None, "Q": None}
    if best is None:
        return res
    side2, s, v = best
    P, Q = triangle_at(O, v, s)
    res.update({"side2": side2, "scale": s, "dir": v, "P": P, "Q": Q})
    if check:
        ok, detail = verify_triangle(poly, O, P, Q)
        if not ok:
            raise AssertionError("maximiser proposed a triangle the verifier rejects: %r"
                                 % (detail,))
        if detail["side2_q3"] != side2:
            raise AssertionError("reported side^2 disagrees with the verifier's")
    return res


def verify_triangle(poly, O, P, Q):
    """Independent re-check: three points on the polygon, pairwise distinct, pairwise
    equidistant, positive side.  Knows nothing about how the triangle was found."""
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
    d["side2_q3"] = s1
    d["side2"] = s1.pair()
    d["side_display"] = float(s1) ** 0.5
    ok = all(d[k] for k in ("O_on_J", "P_on_J", "Q_on_J", "distinct",
                            "equilateral", "nondegenerate"))
    return ok, d


# ------------------------------------------------------------------ global maximum
def edge_sample_points(poly, ts):
    """Rational interior points of every edge, for the corroboration sweep."""
    pts = []
    for i, (A, B) in enumerate(edges(poly)):
        for t in ts:
            f = Fraction(t)
            pts.append((i, f, vadd(A, vscale(Q3.of(f), vsub(B, A)))))
    return pts


def global_max(poly, sample_ts=()):
    """The largest inscribed equilateral triangle anywhere on the polygon.

    Exact, given Lemma V (module docstring, status `sketch`): a maximiser has a vertex at a
    polygon vertex, so the maximum over the vertices is the global maximum.  `sample_ts`
    adds interior edge points as an independent corroboration; they can only confirm, never
    raise, the vertex answer if Lemma V holds -- and a sample that BEAT the vertex answer
    would refute Lemma V, which is exactly what the sweep is for.
    """
    best = None
    per_vertex = []
    for i, O in enumerate(poly):
        r = max_at_point(O, poly)
        per_vertex.append((i, r))
        if r["good"] and (best is None or (r["side2"] - best[1]["side2"]).sgn() > 0):
            best = (("vertex", i), r)
    sampled = []
    violation = None
    for (i, t, O) in edge_sample_points(poly, sample_ts):
        r = max_at_point(O, poly)
        sampled.append((i, t, r))
        if r["good"] and best is not None and (r["side2"] - best[1]["side2"]).sgn() > 0:
            violation = (i, t, r)
    return {"best": best, "per_vertex": per_vertex, "sampled": sampled,
            "lemma_v_violation": violation}
