"""Exact plane geometry over K = Q(sqrt 3): segments, simple polygons, and the decision
procedure for "is this point of the curve the vertex of an inscribed equilateral triangle?".

Standard library only. Every predicate here is an exact sign test in K; nothing branches on a
float. `float()` appears only inside `*_display` helpers.

THE REDUCTION (proved in README.md; restated here because the whole file rests on it)
-------------------------------------------------------------------------------------
Let J be a closed curve, O in J, and rho_sigma the rotation by sigma*60 degrees about O.

    O is the vertex of a nondegenerate equilateral triangle with all three vertices on J
      <=>  for some sigma in {+1,-1} there is X in rho_sigma(J) & J with X != O.

(<=) Given such an X, put Q = rho_sigma^{-1}(X) in J. Then |OQ| = |OX| (rotations are
     isometries fixing O) and the angle QOX is 60 degrees. An isoceles triangle with apex
     angle 60 has base angles (180-60)/2 = 60, so OQX is equilateral. It is nondegenerate:
     X != O gives |OQ| = |OX| > 0, and a 60-degree angle at O forces Q != X.
(=>) Given an equilateral triangle O,A,B on J with side s > 0, B is the image of A under a
     rotation about O by +60 or -60 (the two vertices adjacent to O in an equilateral triangle
     sit at exactly those two angles, at equal radius). For that sigma, X = B lies in
     rho_sigma(J) & J -- it is in J by hypothesis and equals rho_sigma(A) with A in J -- and
     X != O since s > 0.

Both J and rho_sigma(J) are finite unions of closed segments, so the intersection is computed
by finitely many exact segment-segment intersections. The intersection ALWAYS contains O
(rho_sigma fixes O and O is on J), which is exactly the degenerate "triangle" with two
coincident vertices; excluding it is the crux of the implementation.
"""

from __future__ import annotations

from fractions import Fraction

from k3 import K, kq, ZERO, ONE, HALF, SIN60, COS60

__all__ = [
    "P", "padd", "psub", "cross", "dot", "scal", "peq", "norm2",
    "rot60", "seg_intersect", "point_on_segment", "point_on_polygon",
    "edges", "is_simple", "signed_area2", "orientation", "is_convex",
    "vertex_angle_class", "decide_good", "verify_triangle", "sample_edge_point",
]


# --------------------------------------------------------------------------- points
def P(x, y):
    """A point with K coordinates. Accepts ints/Fractions/strs/K."""
    return (K.coerce(x), K.coerce(y))


def padd(A, B):
    return (A[0] + B[0], A[1] + B[1])


def psub(A, B):
    return (A[0] - B[0], A[1] - B[1])


def scal(t, A):
    t = K.coerce(t)
    return (t * A[0], t * A[1])


def cross(U, V):
    return U[0] * V[1] - U[1] * V[0]


def dot(U, V):
    return U[0] * V[0] + U[1] * V[1]


def norm2(U):
    return dot(U, U)


def peq(A, B) -> bool:
    return A[0] == B[0] and A[1] == B[1]


def pt_pair(A):
    return [A[0].as_pair(), A[1].as_pair()]


def pt_float(A):
    return [float(A[0]), float(A[1])]


# --------------------------------------------------------------------------- rotation
def rot60(A, O, sigma: int):
    """Rotate A about O by sigma*60 degrees, sigma in {+1,-1}. Exact: cos60 = 1/2 in Q,
    sin60 = sqrt(3)/2 in K."""
    assert sigma in (1, -1)
    vx = A[0] - O[0]
    vy = A[1] - O[1]
    s = SIN60 if sigma == 1 else -SIN60
    return (O[0] + COS60 * vx - s * vy, O[1] + s * vx + COS60 * vy)


# --------------------------------------------------------------------------- segments
def point_on_segment(X, A, B) -> bool:
    """Is X on the closed segment [A,B]? Handles the degenerate A == B."""
    if peq(A, B):
        return peq(X, A)
    if not cross(psub(B, A), psub(X, A)).is_zero():
        return False
    t = dot(psub(X, A), psub(B, A))
    return t.sign() >= 0 and (t - norm2(psub(B, A))).sign() <= 0


def seg_intersect(A, B, C, D):
    """Exact intersection of closed segments [A,B] and [C,D].

    Returns one of
        ("empty",)
        ("point", X)
        ("segment", X, Y)      # collinear overlap; X != Y
    Degenerate (zero-length) inputs are handled; collinear overlap that shrinks to one point is
    reported as ("point", X).
    """
    ab_deg = peq(A, B)
    cd_deg = peq(C, D)
    if ab_deg and cd_deg:
        return ("point", A) if peq(A, C) else ("empty",)
    if ab_deg:
        return ("point", A) if point_on_segment(A, C, D) else ("empty",)
    if cd_deg:
        return ("point", C) if point_on_segment(C, A, B) else ("empty",)

    r = psub(B, A)
    s = psub(D, C)
    denom = cross(r, s)
    qp = psub(C, A)

    if not denom.is_zero():
        t = cross(qp, s) / denom
        u = cross(qp, r) / denom
        if t.sign() < 0 or (t - ONE).sign() > 0:
            return ("empty",)
        if u.sign() < 0 or (u - ONE).sign() > 0:
            return ("empty",)
        return ("point", padd(A, scal(t, r)))

    # parallel
    if not cross(qp, r).is_zero():
        return ("empty",)  # parallel, distinct lines

    # collinear: project C and D onto the parameter of [A,B]
    rr = norm2(r)  # > 0 since r != 0
    t0 = dot(qp, r) / rr
    t1 = t0 + dot(s, r) / rr
    lo, hi = (t0, t1) if (t1 - t0).sign() >= 0 else (t1, t0)
    if lo.sign() < 0:
        lo = ZERO
    if (hi - ONE).sign() > 0:
        hi = ONE
    d = hi - lo
    if d.sign() < 0:
        return ("empty",)
    X = padd(A, scal(lo, r))
    if d.is_zero():
        return ("point", X)
    return ("segment", X, padd(A, scal(hi, r)))


# --------------------------------------------------------------------------- polygons
def edges(poly):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n)]


def point_on_polygon(X, poly) -> bool:
    return any(point_on_segment(X, A, B) for A, B in edges(poly))


def signed_area2(poly) -> K:
    """Twice the signed area. Positive <=> counter-clockwise."""
    tot = ZERO
    n = len(poly)
    for i in range(n):
        A, B = poly[i], poly[(i + 1) % n]
        tot = tot + cross(A, B)
    return tot


def orientation(poly) -> int:
    return signed_area2(poly).sign()


def is_simple(poly):
    """Exact Jordan check for a closed polygonal curve.

    Returns (ok, reason). Requires: at least 3 vertices, no zero-length edge, adjacent edges
    meeting exactly in their shared vertex, non-adjacent edges disjoint. That is precisely the
    condition for the closed polygonal curve to be a Jordan curve.
    """
    n = len(poly)
    if n < 3:
        return False, "fewer than 3 vertices"
    E = edges(poly)
    for i, (A, B) in enumerate(E):
        if peq(A, B):
            return False, f"zero-length edge {i}"
    for i in range(n):
        for j in range(i + 1, n):
            adjacent = (j == i + 1) or (i == 0 and j == n - 1)
            res = seg_intersect(*E[i], *E[j])
            if adjacent:
                shared = E[i][1] if j == i + 1 else E[i][0]
                if res[0] != "point" or not peq(res[1], shared):
                    return False, f"adjacent edges {i},{j} meet in more than their shared vertex"
            else:
                if res[0] != "empty":
                    return False, f"non-adjacent edges {i},{j} intersect"
    return True, "simple"


def is_convex(poly) -> bool:
    """Strictly convex: every turn is nonzero and all turns share a sign."""
    n = len(poly)
    signs = []
    for i in range(n):
        U = psub(poly[i], poly[(i - 1) % n])
        V = psub(poly[(i + 1) % n], poly[i])
        s = cross(U, V).sign()
        if s == 0:
            return False
        signs.append(s)
    return all(s == signs[0] for s in signs)


def vertex_angle_class(poly, i):
    """Classify the INTERIOR angle at vertex i of a simple polygon.

    Returns dict with
      reflex : bool                      (interior angle > 180)
      cmp60  : -1 / 0 / +1               (interior angle <, =, > 60 degrees)
      degrees_display : float            (display only)

    Exactness: let u, w be the two edge vectors leaving the vertex, c = u.w, s = cross(u,w).
    The unsigned angle theta in (0,180) between them satisfies
        theta < 60  <=>  c > 0 and s^2 < 3 c^2,      theta = 60  <=>  c > 0 and s^2 = 3 c^2,
    since tan theta = |s|/c for c > 0 and tan 60 = sqrt 3; for c <= 0, theta >= 90 > 60.
    The interior angle equals theta at a convex vertex and 360 - theta at a reflex one, and
    360 - theta > 180 > 60 always, so a reflex vertex is unconditionally cmp60 = +1.
    """
    import math

    n = len(poly)
    V = poly[i]
    U = poly[(i - 1) % n]
    W = poly[(i + 1) % n]
    u = psub(U, V)
    w = psub(W, V)
    ornt = orientation(poly)
    # turn at V for the traversal ...U -> V -> W...
    turn = cross(psub(V, U), psub(W, V)).sign()
    reflex = (turn * ornt) < 0

    c = dot(u, w)
    s = cross(u, w)
    if reflex:
        cmp60 = 1
    elif c.sign() <= 0:
        cmp60 = 1
    else:
        d = (s * s) - K(3) * (c * c)
        sg = d.sign()
        cmp60 = -1 if sg < 0 else (0 if sg == 0 else 1)

    ang = math.degrees(math.atan2(abs(float(s)), float(c)))
    if reflex:
        ang = 360.0 - ang
    return {"reflex": reflex, "cmp60": cmp60, "degrees_display": ang}


def sample_edge_point(A, B, t: Fraction):
    """The point A + t(B-A) for rational t in (0,1)."""
    return padd(A, scal(K(t, 0), psub(B, A)))


# --------------------------------------------------------------------------- the decision
def verify_triangle(poly, O, Q, X):
    """Independent re-check of a reported witness. Returns (ok, detail).

    Deliberately does NOT reuse the search's reasoning: it just asks whether the three points
    are on the polygon, pairwise distinct, and pairwise equidistant.
    """
    d = {
        "O_on_J": point_on_polygon(O, poly),
        "Q_on_J": point_on_polygon(Q, poly),
        "X_on_J": point_on_polygon(X, poly),
        "distinct": (not peq(O, Q)) and (not peq(O, X)) and (not peq(Q, X)),
    }
    a = norm2(psub(Q, O))
    b = norm2(psub(X, O))
    c = norm2(psub(X, Q))
    d["equilateral"] = (a == b) and (b == c)
    d["side_squared"] = a.as_pair()
    d["side_display"] = float(a) ** 0.5
    d["nondegenerate"] = a.sign() > 0
    ok = all(d[k] for k in ("O_on_J", "Q_on_J", "X_on_J", "distinct", "equilateral", "nondegenerate"))
    return ok, d


def decide_good(poly, O, want_all: bool = False):
    """Decide whether O in J = boundary(poly) is *good*.

    Returns a dict:
      good            : bool
      witness         : {sigma, Q, X} or None      (X = rho_sigma(Q); O,Q,X equilateral)
      verified        : the verify_triangle detail for the witness
      pairs_tested    : number of (rotated edge, edge) pairs examined
      trivial_only    : number of pairs whose intersection was exactly {O}
      nonempty_pairs  : number of pairs with nonempty intersection

    Search order is deterministic (sigma = +1 then -1; edges in polygon order) so the reported
    witness is reproducible.
    """
    E = edges(poly)
    assert point_on_polygon(O, poly), "O must lie on the curve"

    pairs = 0
    trivial = 0
    nonempty = 0
    witness = None

    for sigma in (1, -1):
        RE = [(rot60(A, O, sigma), rot60(B, O, sigma)) for A, B in E]
        for RA, RB in RE:
            for C, D in E:
                pairs += 1
                res = seg_intersect(RA, RB, C, D)
                if res[0] == "empty":
                    continue
                nonempty += 1
                cands = [res[1]] if res[0] == "point" else [res[1], res[2]]
                found = None
                for Xc in cands:
                    if not peq(Xc, O):
                        found = Xc
                        break
                if found is None:
                    trivial += 1
                    continue
                if witness is None:
                    witness = {"sigma": sigma, "X": found, "Q": rot60(found, O, -sigma)}
                    if not want_all:
                        break
            if witness is not None and not want_all:
                break
        if witness is not None and not want_all:
            break

    out = {
        "good": witness is not None,
        "pairs_tested": pairs,
        "nonempty_pairs": nonempty,
        "trivial_only_pairs": trivial,
        "witness": None,
        "verified": None,
        "verified_ok": None,
    }
    if witness is not None:
        ok, detail = verify_triangle(poly, O, witness["Q"], witness["X"])
        out["witness"] = {
            "sigma": witness["sigma"],
            "Q_exact": pt_pair(witness["Q"]),
            "X_exact": pt_pair(witness["X"]),
            "Q_display": pt_float(witness["Q"]),
            "X_display": pt_float(witness["X"]),
        }
        out["verified"] = detail
        out["verified_ok"] = ok
    return out
