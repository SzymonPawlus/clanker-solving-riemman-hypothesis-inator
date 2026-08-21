"""Independent exact certifier for a 15-piece covering of T_a by sets of diameter < 1.

Written from scratch by claude / worker C1 (2026-08-22) from the problem statement in
problems/circle-packing-equilateral-triangle/{RULES.md,README.md} and the mechanism
statement, WITHOUT reading or importing the certifier of attacks/n16-covering.

EXACT RATIONAL ARITHMETIC THROUGHOUT.  Coordinates live in the triangular basis
    e1 = (1,0),  e2 = (1/2, sqrt3/2),      point (u,v) = u*e1 + v*e2,
in which the squared Euclidean length of (du,dv) is the RATIONAL form
    Q(du,dv) = du^2 + du*dv + dv^2,
and                T_a = { u >= 0, v >= 0, u+v <= a }
has plane corners (0,0), (a,0), (a/2, a*sqrt3/2) -- the placement fixed by the problem's
RULES.md section 2.  Plane area = (sqrt3/4) * (uv-shoelace), so an area *identity* between
subsets of T_a is a rational identity and no square root is ever needed.

Floats appear only in printed approximations; nothing is decided by one.

The pigeonhole this certifies:
    T_a covered by 15 sets each of diameter STRICTLY < 1
      => no 16 points of T_a are pairwise at distance >= 1   (two share a piece)
      => a_16 >= a,  hence  s(16) >= 2a + 2*sqrt(3).
"Strictly" is load-bearing: separation in this problem is non-strict, so a closed piece of
diameter exactly 1 may hold two admissible points.

Usage:  python3 verify_c1.py <cert.json> [--nocover]
"""
import json, math, sys
from fractions import Fraction as F

# ----------------------------------------------------------------- primitives

def Q(du, dv):
    """squared euclidean length of du*e1 + dv*e2"""
    return du * du + du * dv + dv * dv

def cross(o, p, q):
    """2 * signed uv-area of (o,p,q); same sign as the plane orientation"""
    return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])

def shoelace2(poly):
    """2 * signed uv-area"""
    s = F(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s

def dedup(poly):
    out = []
    for p in poly:
        if not out or out[-1] != p:
            out.append(p)
    while len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out

def clip_le(poly, A, B, C):
    """poly (convex, ccw, exact) intersected with the closed halfplane A*u + B*v <= C."""
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]
        q = poly[(i + 1) % n]
        dp = A * p[0] + B * p[1] - C
        dq = A * q[0] + B * q[1] - C
        if dp <= 0:
            out.append(p)
        if (dp > 0) != (dq > 0):
            t = dp / (dp - dq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return dedup(out)

def edge_halfplane(p, q):
    """For a ccw polygon, the interior side of directed edge p->q is cross(p,q,x) >= 0.
    Return (A,B,C) with the OUTSIDE closed halfplane written as A*u + B*v <= C."""
    # cross(p,q,x) = (q0-p0)(x1-p1) - (q1-p1)(x0-p0)
    #             = -(q1-p1)*x0 + (q0-p0)*x1 + [ (q1-p1)*p0 - (q0-p0)*p1 ]
    A = (q[1] - p[1])
    B = -(q[0] - p[0])
    C = (q[1] - p[1]) * p[0] - (q[0] - p[0]) * p[1]
    # cross(p,q,x) = -(A*x0 + B*x1) + C  ... check: -A*x0 - B*x1 + C
    #   = -(q1-p1)x0 + (q0-p0)x1 + (q1-p1)p0 - (q0-p0)p1  == cross  OK
    # cross <= 0  <=>  A*x0 + B*x1 >= C  <=>  -A*x0 - B*x1 <= -C
    return (-A, -B, -C)          # OUTSIDE (cross <= 0) as  A'u + B'v <= C'

def intersect_convex(P, R):
    """exact intersection polygon of two convex ccw polygons"""
    out = P
    n = len(R)
    for i in range(n):
        p, q = R[i], R[(i + 1) % n]
        # keep cross(p,q,x) >= 0, i.e. NOT (outside)
        A, B, C = edge_halfplane(p, q)     # outside is A*u+B*v <= C
        # inside is A*u+B*v >= C  <=>  -A*u-B*v <= -C
        out = clip_le(out, -A, -B, -C)
        if len(out) < 3:
            return out
    return out

def contains(P, x):
    """x in the closed convex ccw polygon P"""
    n = len(P)
    for i in range(n):
        if cross(P[i], P[(i + 1) % n], x) < 0:
            return False
    return True

def bbox(P):
    us = [p[0] for p in P]; vs = [p[1] for p in P]
    return min(us), max(us), min(vs), max(vs)

def bbox_disjoint(b1, b2):
    return b1[1] < b2[0] or b2[1] < b1[0] or b1[3] < b2[2] or b2[3] < b1[2]

# ----------------------------------------------------------------- the checks

def check(a, faces, do_cover=True, verbose=True, strict=True):
    fail = []
    say = (lambda s: print(s)) if verbose else (lambda s: None)
    tri = [(F(0), F(0)), (a, F(0)), (F(0), a)]

    say("a = %s = %.12f      pieces = %d" % (a, float(a), len(faces)))

    # (1) each piece lies in T_a, is a strictly convex ccw polygon
    for k, f in enumerate(faces):
        if len(f) < 3:
            fail.append("piece %d has < 3 vertices" % k); continue
        if len(dedup(list(f))) != len(f):
            fail.append("piece %d has a repeated vertex" % k)
        for (u, v) in f:
            if u < 0 or v < 0 or u + v > a:
                fail.append("piece %d has a vertex outside T_a" % k)
        m = len(f)
        for i in range(m):
            if cross(f[i], f[(i + 1) % m], f[(i + 2) % m]) <= 0:
                fail.append("piece %d not strictly convex / not ccw at vertex %d" % (k, i))
    say("  [1] all %d pieces are strictly convex ccw polygons with every vertex in T_a : %s"
        % (len(faces), "ok" if not fail else "FAIL"))

    # (2) strict diameters
    worst = F(0); wk = -1
    for k, f in enumerate(faces):
        d = F(0)
        for i in range(len(f)):
            for j in range(i + 1, len(f)):
                q = Q(f[i][0] - f[j][0], f[i][1] - f[j][1])
                if q > d: d = q
        if (d >= 1) if strict else (d > 1):
            fail.append("piece %d has squared diameter %s %s 1"
                        % (k, d, ">=" if strict else ">"))
        if d > worst:
            worst, wk = d, k
    say("  [2] max squared diameter = %s" % worst)
    say("      = %.15f   %s : %s   (piece %d)"
        % (float(worst), "< 1 STRICTLY" if strict else "<= 1 (non-strict test)",
           (worst < 1) if strict else (worst <= 1), wk))

    # (3) pairwise interior-disjointness, by exact convex clipping
    nover = 0
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            R = intersect_convex(list(faces[i]), list(faces[j]))
            if len(R) >= 3 and shoelace2(R) != 0:
                fail.append("pieces %d,%d overlap in positive area" % (i, j)); nover += 1
    say("  [3] all %d piece pairs meet in ZERO area (exact convex clipping) : %s"
        % (len(faces) * (len(faces) - 1) // 2, "ok" if nover == 0 else "FAIL (%d)" % nover))

    # (4) exact area identity
    tot = F(0)
    for f in faces:
        s = shoelace2(f)
        if s <= 0:
            fail.append("piece with non-positive shoelace")
        tot += s
    tgt = shoelace2(tri)
    if tot != tgt:
        fail.append("area sum %s != area(T_a) %s" % (tot, tgt))
    say("  [4] sum of piece areas == area(T_a) exactly : %s   (%s vs %s)"
        % (tot == tgt, tot, tgt))

    # (5) INDEPENDENT covering proof: T_a minus the union is empty.
    #     Q \ P  =  union over edges e of P of ( Q  intersect  {outside of e} ),
    #     each of which is a convex polygon; recurse and prune zero-area parts.
    #     This uses NO measure-theoretic inference and no disjointness assumption.
    if do_cover:
        regions = [tri]
        boxes = [bbox(tri)]
        pb = [bbox(f) for f in faces]
        cap = 400000
        peak = 1
        for k, f in enumerate(faces):
            new, nbx = [], []
            for Rg, bx in zip(regions, boxes):
                if bbox_disjoint(bx, pb[k]):
                    new.append(Rg); nbx.append(bx); continue
                m = len(f)
                for i in range(m):
                    A, B, C = edge_halfplane(f[i], f[(i + 1) % m])   # outside halfplane
                    S = clip_le(Rg, A, B, C)
                    if len(S) >= 3 and shoelace2(S) > 0:
                        new.append(S); nbx.append(bbox(S))
            # drop regions contained in another region (redundant)
            keep = []
            for i in range(len(new)):
                red = False
                for j in range(len(new)):
                    if i == j: continue
                    if len(new[j]) < 3: continue
                    if all(contains(new[j], x) for x in new[i]):
                        if not (len(new[i]) == len(new[j]) and j > i and
                                sorted(new[i]) == sorted(new[j])):
                            red = True; break
                if not red:
                    keep.append(i)
            new = [new[i] for i in keep]; nbx = [nbx[i] for i in keep]
            regions, boxes = new, nbx
            peak = max(peak, len(regions))
            if len(regions) > cap:
                fail.append("covering search exceeded the node cap"); break
        say("  [5] residue T_a \\ (union of pieces) : %d convex parts of positive area"
            " (peak %d)  -> %s" % (len(regions), peak, "EMPTY, covering proved"
                                   if not regions else "NOT EMPTY -- NOT A COVERING"))
        if regions:
            fail.append("the pieces do not cover T_a: %d gaps" % len(regions))

    ok = not fail
    say("")
    for m in fail:
        say("  FAIL: " + m)
    say("  VERDICT : %s" % ("PASS" if ok else "FAIL"))
    if ok:
        s = 2.0 * float(a) + 2.0 * math.sqrt(3.0)
        say("")
        say("  => a_16 >= %s = %.12f" % (a, float(a)))
        say("  => s(16) >= 2*(%s) + 2*sqrt(3) = %.12f" % (a, s))
    return ok, worst


def load(path):
    d = json.load(open(path))
    an, ad = d["a"]
    a = F(int(an), int(ad))
    faces = [[(F(u), F(v)) for (u, v) in f] for f in d["faces_uv"]]
    return a, faces


if __name__ == "__main__":
    path = sys.argv[1]
    a, faces = load(path)
    ok, w = check(a, faces, do_cover=("--nocover" not in sys.argv))
    sys.exit(0 if ok else 1)
