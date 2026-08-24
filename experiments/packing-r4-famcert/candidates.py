"""Candidate point set for the four-grain mechanism, in exact Q(sqrt 3).

The claimed mechanism (attacks/r3-approaches/README.md §0.2, second correction
block) is: four SAME-ORIENTATION triangular-lattice grains -- two bottom corners,
an inverted centre, a top corner -- separated by length-2 "stacking-fault" seams.

Made precise here, and CONFIRMED against the n = 17/24/31 certificates by
dissect.py: every non-rattler point of all three lies in

    U(d) = union over g in G of ((L + g) intersect T(d)),
    L = {(2i+r, r*sqrt3) : i, r in Z},
    G = { (0,0), (2sqrt3,0), (sqrt3,1), (sqrt3,3) }.

|(sqrt3,1)| = |(0,2)| = 2 and (2sqrt3,0) = (sqrt3,1) + (sqrt3,-1), so every offset
is a sum of length-2 seam vectors.  What the mechanism does NOT fix is which
lattice sites each grain keeps -- the "seam depth" freedom.  search.py resolves
that by exact maximum-independent-set search rather than by extrapolation.

Everything below is exact; no float participates in any accept/reject decision.
"""
from qsqrt3 import Q3, q3

OFFSETS = [
    ("BL", (Q3(0, 0), Q3(0, 0))),
    ("BR", (Q3(0, 2), Q3(0, 0))),
    ("C",  (Q3(0, 1), Q3(1, 0))),
    ("T",  (Q3(0, 1), Q3(3, 0))),
]

R3 = Q3(0, 1)


def d_of(j):
    return Q3(2 * j, 2)


def in_triangle(pt, d):
    """Closed triangle A=(0,0), B=(d,0), C=(d/2, d sqrt3/2).  Exact, non-strict."""
    x, y = pt
    return (y >= q3(0)) and (R3 * x - y >= q3(0)) and (R3 * (d - x) - y >= q3(0))


def candidates(j):
    """All sites of the four shifted lattices lying in the closed triangle.

    Returns a list of (label, r, i, (x, y)).
    """
    d = d_of(j)
    out = []
    rmax = j + 3
    for name, (gx, gy) in OFFSETS:
        for r in range(0, rmax + 1):
            y = Q3(0, r) + gy
            if y > R3 * d * Q3(1, 0) * q3(1) / q3(2):  # y > d*sqrt3/2 -> above apex
                continue
            for i in range(-(j + 4), 2 * j + 8):
                x = Q3(2 * i + r, 0) + gx
                p = (x, y)
                if in_triangle(p, d):
                    out.append((name, r, i, p))
    return out


if __name__ == "__main__":
    for j in range(0, 9):
        c = candidates(j)
        from collections import Counter
        cnt = Counter(t[0] for t in c)
        print("j = %d  d = %-16s  candidates %3d   %s"
              % (j, d_of(j).sexpr(), len(c), dict(cnt)))
