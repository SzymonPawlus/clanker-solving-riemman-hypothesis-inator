"""Independent exact checker for the finite-polygon mixed-area bridge.

All arithmetic is rational.  For a CCW edge d=(dx,dy), ``rot_cw(d)`` is
the *unnormalized* outward normal.  Thus

    length(d) * h_K(unit_outward(d)) = h_K(rot_cw(d)),

so no square roots or floating point arithmetic occur.
"""

from fractions import Fraction as Q


def qpoint(x, y):
    return (Q(x), Q(y))


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def area2(poly):
    return sum(cross(poly[i], poly[(i + 1) % len(poly)])
               for i in range(len(poly)))


def strict_ccw_convex(poly):
    """Reject malformed boundary data instead of silently repairing it."""
    if len(poly) < 3 or len(set(poly)) != len(poly) or area2(poly) <= 0:
        return False
    return all(cross(sub(poly[(i + 1) % len(poly)], poly[i]),
                     sub(poly[(i + 2) % len(poly)], poly[(i + 1) % len(poly)])) > 0
               for i in range(len(poly)))


def on_or_inside_ccw_convex(poly, p):
    if not strict_ccw_convex(poly):
        raise ValueError("container must be a strict CCW convex polygon")
    return all(cross(sub(poly[(i + 1) % len(poly)], poly[i]),
                     sub(p, poly[i])) >= 0 for i in range(len(poly)))


def validate_inner(inner):
    if len(inner) == 2:
        if inner[0] == inner[1]:
            raise ValueError("segment endpoints must differ")
        return
    if not strict_ccw_convex(inner):
        raise ValueError("inner must be a segment or strict CCW convex polygon")


def boundary_edges(inner):
    """CCW polygon edges, or both oriented sides of a segment."""
    validate_inner(inner)
    if len(inner) == 2:
        return ((inner[0], inner[1]), (inner[1], inner[0]))
    return tuple((inner[i], inner[(i + 1) % len(inner)])
                 for i in range(len(inner)))


def support(poly, normal):
    return max(dot(normal, x) for x in poly)


def twice_mixed_area(inner, container, *, inward=False, omit_last=False):
    """Return sum_e |e| h_K(n_e), exactly (twice the mixed area).

    ``inward`` and ``omit_last`` intentionally expose two common mutations for
    adversarial tests; production callers must leave both false.
    """
    if not strict_ccw_convex(container):
        raise ValueError("container must be a strict CCW convex polygon")
    edges = list(boundary_edges(inner))
    if omit_last:
        edges = edges[:-1]
    total = Q(0)
    for a, b in edges:
        dx, dy = sub(b, a)
        normal = (-dy, dx) if inward else (dy, -dx)
        total += support(container, normal)
    return total


def bridge_check(inner, container):
    """Check hypotheses and the claimed mixed-area inequality exactly."""
    validate_inner(inner)
    if not strict_ccw_convex(container):
        raise ValueError("container must be a strict CCW convex polygon")
    if not all(on_or_inside_ccw_convex(container, p) for p in inner):
        raise ValueError("inner is not contained in container")
    lhs = twice_mixed_area(inner, container) / 2
    rhs = area2(container) / 2
    return lhs, rhs, lhs <= rhs


def convex_hull(points):
    """Monotone-chain hull, useful only for generating exact test instances."""
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and cross(sub(out[-1], out[-2]),
                                          sub(p, out[-1])) <= 0:
                out.pop()
            out.append(p)
        return out

    return half(pts)[:-1] + half(reversed(pts))[:-1]
