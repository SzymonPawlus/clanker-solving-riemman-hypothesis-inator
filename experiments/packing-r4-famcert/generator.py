"""THE GENERATOR.  Closed-form four-grain construction, parameterised by j.

CONSTRUCTION (upper bound) only.  Emitting a configuration here claims nothing;
only check.py's exact verdict does.

Reverse-engineered from the n = 17/24/31 certificates by dissect.py, then written
as a single formula in j and validated against the known members (validate.py).

Setting.  L = {(2i+r, r*sqrt3)} is the triangular lattice of separation 2.
Write a lattice site as (row r, abscissa x) with x = 2i + r, x = r (mod 2).
The four grains are translates of L by the fixed offsets

    g_BL = (0,0)      g_C = (sqrt3, 1)      g_T = (sqrt3, 3)     g_BR = (2 sqrt3, 0)

all of which are sums of length-2 "stacking-fault" vectors:
    (sqrt3,1) and (0,2) have length 2, and g_BR = (sqrt3,1) + (sqrt3,-1).

With  d = 2j + 2 sqrt3,  put  U = ceil(j/2),  M = floor(j/2)  (so U + M = j), and

    BL : rows r = 0 .. U,            x in [r, 2U - r]                 (upward,  corner A)
    BR : rows r = 0 .. U,            x in [2j-2U+r, 2j-r]             (upward,  corner B)
         MINUS its bottom-left site (2j-2U, 0) when j is odd
    C  : rows r = (j mod 2) .. (j mod 2)+M,  x in [j-(r-j mod 2), j+(r-j mod 2)]
                                                                      (INVERTED, centre)
    T  : rows r = U .. j,            x in [r, 2j-r]                   (upward,  corner C)

Counts:  |BL| = |BR| + (j mod 2) = Delta(U+1),  |C| = |T| = Delta(M+1), so
    n(j) = 2*Delta(U+1) + 2*Delta(M+1) - (j mod 2) = Delta(j+2) + floor(j/2) + 1,
which is exactly the merged A/B staircase (family_law.py).

The bottom edge is the clearest way to see the fault: it carries j+2 points, with
j gaps of length 2 and ONE gap of length 2*sqrt3 -- and 2j + 2 sqrt3 = d exactly.
"""
from qsqrt3 import Q3, q3

OFF = {
    "BL": (Q3(0, 0), Q3(0, 0)),
    "BR": (Q3(0, 2), Q3(0, 0)),
    "C":  (Q3(0, 1), Q3(1, 0)),
    "T":  (Q3(0, 1), Q3(3, 0)),
}


def site(name, r, x):
    gx, gy = OFF[name]
    return (Q3(x, 0) + gx, Q3(0, r) + gy)


def grains(j):
    """Return {grain name: [(r, x), ...]} in lattice coordinates."""
    U = (j + 1) // 2          # ceil(j/2)
    M = j // 2                # floor(j/2)
    par = j % 2
    g = {"BL": [], "BR": [], "C": [], "T": []}

    for r in range(0, U + 1):
        for x in range(r, 2 * U - r + 1, 2):
            g["BL"].append((r, x))

    for r in range(0, U + 1):
        for x in range(2 * j - 2 * U + r, 2 * j - r + 1, 2):
            if par == 1 and r == 0 and x == 2 * j - 2 * U:
                continue          # dropped: it would clash with BL's bottom row
            g["BR"].append((r, x))

    for r in range(par, par + M + 1):
        k = r - par
        for x in range(j - k, j + k + 1, 2):
            g["C"].append((r, x))

    for r in range(U, j + 1):
        for x in range(r, 2 * j - r + 1, 2):
            g["T"].append((r, x))

    return g


def generate(j):
    """Exact Q(sqrt 3) point list for family member j.  Deterministic order."""
    g = grains(j)
    pts = []
    for name in ("BL", "BR", "C", "T"):
        for (r, x) in g[name]:
            pts.append(site(name, r, x))
    return pts


def labelled(j):
    g = grains(j)
    return [(name, r, x, site(name, r, x))
            for name in ("BL", "BR", "C", "T") for (r, x) in g[name]]


def d_of(j):
    return Q3(2 * j, 2)


def s_of(j):
    return Q3(2 * j, 4)


if __name__ == "__main__":
    import sys
    from family_law import law_n
    from check import check
    js = [int(a) for a in sys.argv[1:]] or list(range(0, 11))
    print("%-3s %-4s %-18s %-5s %-6s %-6s %-6s %-9s %-6s" %
          ("j", "n", "s", "cnt?", "feas", "tight", "minD2", "contacts", "bdry"))
    for j in js:
        pts = generate(j)
        n = law_n(j)
        rep = check(len(pts), s_of(j), pts)
        print("%-3d %-4d %-18s %-5s %-6s %-6s %-6s %-9d %-6d" %
              (j, n, s_of(j).sexpr(), "OK" if len(pts) == n else "MISMATCH:%d" % len(pts),
               rep["ok"], rep["tight"], rep["min_sq_distance"],
               rep["contacts_at_distance_exactly_2"], rep["points_on_boundary"]))
        if not rep["ok"]:
            for f in rep["failures"][:6]:
                print("     FAIL", f)
