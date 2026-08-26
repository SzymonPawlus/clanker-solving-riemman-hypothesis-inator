"""Shared geometry for the r5-eo7 lattice-count bound.

Normalisation (problem README / eo-exhaustion §0): points at pairwise separation >= 1
in a closed equilateral triangle T(a) of side a.  Erdos-Oler at k = 7 is the statement
that 27 = Delta(7) - 1 such points force a >= 6.

Triangle placement (problem RULES.md §2): A = (0,0), B = (a,0), C = (a/2, a*sqrt(3)/2).

STATUS: numerical / sketch.  Nothing here is assumable.
"""
import math

SQRT3 = math.sqrt(3.0)


def tent(phi, a=6.0):
    """Chord-length profile of T(a) for a family of lines of direction phi.

    Lines have unit direction u = (cos phi, sin phi); the family is indexed by the
    signed level along the unit normal n = (-sin phi, cos phi).  We measure levels
    by s = (n.x) - min_{T} (n.x), so s ranges over [0, w].

    Returns (d1, w, Lstar) where the chord length profile is the "tent"
        g(s) = Lstar * s / d1                for 0 <= s <= d1
        g(s) = Lstar * (w - s) / (w - d1)    for d1 <= s <= w
    Valid for phi in [0, pi/3] (see README): there min(n.x) is at B, the middle
    vertex is A, and max is at C.
    """
    sp, cp = math.sin(phi), math.cos(phi)
    scale = a / 6.0
    d1 = 6.0 * sp * scale                       # level gap  B -> A
    w = (3.0 * SQRT3 * cp + 3.0 * sp) * scale   # total width = 6 cos(phi - pi/6)
    Lstar = (6.0 * SQRT3 / (SQRT3 * cp + sp)) * scale  # 3 sqrt3 / cos(phi - pi/6)
    return d1, w, Lstar


def chord(phi, s, a=6.0):
    d1, w, Lstar = tent(phi, a)
    if s < 0.0 or s > w:
        return -1.0
    if s <= d1:
        return Lstar if d1 == 0.0 else Lstar * s / d1
    return Lstar * (w - s) / (w - d1)


def line_bound(phi, h, theta, a=6.0, tol=1e-12):
    """Upper bound on |(Lambda+t) cap T(a)| from the line relaxation.

    Lambda has shortest vector v1 of length r = lambda_1; after scaling we take
    r = 1 and require a < 6 strictly.  Lambda lies on lines parallel to v1 spaced
    h = covol/r >= sqrt(3)/2 apart, with points spaced exactly r = 1 on each line.
    A chord of length L then carries at most ceil(L) points when the separation is
    > 1 (which is what a < 6 gives after rescaling to T(6)), and at most 1 if L = 0.

    theta in [0,1) is the offset of the line family in units of h.
    """
    d1, w, Lstar = tent(phi, a)
    total = 0
    j = 0
    while True:
        s = (theta + j) * h
        if s > w + tol:
            break
        L = chord(phi, min(s, w), a)
        if L < -tol:
            break
        total += max(1, math.ceil(L - tol))
        j += 1
    return total
